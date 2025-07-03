import io
import tempfile

from PIL import Image

from config import *

from sql_connection import connection_sql, preprocess_summary_sql, preprocess_whole_sql
from embeddings_reranker import embedder_reranker
from weather_api import current_weather,hourly_weather
from cause_prediction_llm import cause_prediction_LLM
from vila_image_summarizer import image_summarizer
from insights_agent import insights_agent
from alert_agent import dispatch_to_responders

# Process the POST input
def input_processing(request):

    # Check whether required media file was provided
    if 'input_media' not in request.files:
        err = f"Media file not provided in the request"
        print(f"error: {err}")
        raise Exception(err)
    
    # Check whether required coordinates were provided
    if 'latitude' not in request.form or 'longitude' not in request.form:
        err = f"Required coordinates were not provided"
        print(f"error: {err}")
        raise Exception(err)
    
    # Process media file to correct format
    imgfile = request.files['input_media']

    raw_bytes = imgfile.read()
    if len(raw_bytes) == 0:
        err = "Empty media file uploaded"
        print(f"error: {err}")
        raise Exception(err)

    try:
        img = Image.open(io.BytesIO(raw_bytes))
        img_format = img.format

    except Exception as e:
        err = "Unable to open media file"
        print(f"error: {err}:\n{e}")
        raise Exception(err) from e

    formats = {"jpg","png","jpeg","mp4"}

    img_format = img_format.lower()

    if img_format not in formats:
        err = f"Media file is of an unsupported format"
        print(f"error: {err}")
        raise Exception(err)

    extension = img_format.lower()

    # Store uploaded media file in a temporary filename and path
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{extension}") as tmpimg:
        tmpimg.write(raw_bytes)
        tmpimg_path = tmpimg.name


    # Get provided coordinates
    latitude = request.form['latitude']
    longitude = request.form['longitude']

    print(f"Coordinates: lat:{latitude}, long:{longitude}")

    print(f"Image path: {tmpimg_path}")

    return tmpimg_path, latitude, longitude
    


def response_generator(img, lat, lon):
    # Connect to database
    try:
        results = connection_sql(sql_database)

    except Exception as e:
        err = "Unsuccessful database connection attempt"
        print(f"error: {err}\n{e}")
        raise Exception(err) from e
    
    if results:
        print(f"Connected to database")
    else:
        err = "No database results found"
        print(f"error: {err}")
        raise Exception(err)

    # Preprocess data
    threat_summary_meta_data = preprocess_summary_sql(results)
    print(f"Loaded {len(threat_summary_meta_data)} rows from the database")
    print('\n\n----------\n\n')

    # Image to summary using vila
    image_summary = image_summarizer(img, api_key_nvd)
    print("Image summary:")
    print(image_summary)
    print('\n\n----------\n\n')

    #################################################
    ########## Hardcoded Now, change Later ########## 
    #################################################

    # calling weather API
    current_weather_json = current_weather(lat,lon)
    hourly_weather_json = hourly_weather(lat,lon)
    weather_api_data = ""
    if current_weather_json :
        weather_api_data += """
        Current weather data:
        """+ current_weather_json
    # if hourly_weather_json:
    #     weather_api_data += """\n
    #     Hourly weather Data:
    #     """+ hourly_weather_json

    # Embedding and reranking
    top2 = embedder_reranker(embedding_model, reranker_model, threat_summary_meta_data ,image_summary)

    # Fetch the top 2 event ids
    event_ids = [doc.metadata["event_id"] for doc in top2]

    # Get full table data from top 2 occurrences
    documents = preprocess_whole_sql(results, event_ids)

    # Check API Key
    if not api_key_nvd.startswith("nvapi-"):
        err = "Invalid API key"
        print(f"error: {err}")
        raise Exception(err)

    try:
    # Cause Prediction LLM
        cause_prediction_llm_output = cause_prediction_LLM(documents, cause_prediction_llm_model, image_summary, weather_api_data.strip())
        print("Cause prediction LLM:")
        print(cause_prediction_llm_output)
        print('\n\n----------\n\n')

    # Insights LLM
        insights_agent_output_json = insights_agent(image_summary, weather_api_data.strip(), insights_agents_model, cause_prediction_llm_output, api_key_nvd)
        print("Insights LLM:")
        print(insights_agent_output_json)
        print('\n\n----------\n\n')

    # Alert LLM
        agencies = insights_agent_output_json.get("agency","")
        messages = insights_agent_output_json.get("messages","")

        agency_res = []

        if agencies:
            agency_res = dispatch_to_responders(agencies, messages)
        else:
            agency_res = ["No agency data"]

        return cause_prediction_llm_output, insights_agent_output_json, agency_res

    
    except Exception as e:
        err = "Encountered issues while invoking agents"
        print("error: {err}\n{e}")
        raise Exception(err) from e