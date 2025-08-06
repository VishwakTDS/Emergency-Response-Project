import io
import tempfile
import json
import string

from PIL import Image

from config import *

from sql_connection import connection_sql, preprocess_summary_sql, preprocess_whole_sql
from embeddings_reranker import embedder_reranker
from weather_api import current_weather,hourly_weather
from cause_prediction_llm import cause_prediction_LLM
from vila_image_summarizer import image_summarizer
from insights_agent import insights_agent
from alert_agent import dispatch_to_responders
from send_email import send_email

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
    # calling weather API
    current_weather_df = current_weather(lat,lon)
    current_weather_string = json.dumps(current_weather_df)
    print(current_weather_string)
    yield json.dumps({"type": "weather", "data": current_weather_df},
                        ensure_ascii=False) + "\n"
    hourly_weather_json = hourly_weather(lat,lon)
    weather_api_data = ""
    if current_weather_string :
        weather_api_data += """
        Current weather data:
        """+ current_weather_string
    # if hourly_weather_json:
    #     weather_api_data += """\n
    #     Hourly weather Data:
    #     """+ hourly_weather_json
    
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
        cause_prediction_llm_buffer = []
        for tok in cause_prediction_LLM(documents, cause_prediction_llm_model, image_summary, api_key_nvd, weather_api_data.strip()):
            cause_prediction_llm_buffer.append(tok)
            yield json.dumps({"type": "cause_prediction", "data": tok},
                         ensure_ascii=False) + "\n"
        cause_prediction_llm_output = "".join(cause_prediction_llm_buffer)
        print("\n\nCause prediction LLM:")
        print(cause_prediction_llm_output)
        print('\n\n----------\n\n')


        # insights_llm_buffer = []
        # for tok in insights_agent(image_summary, weather_api_data.strip(), insights_agents_model, cause_prediction_llm_output, api_key_nvd):
        #     insights_llm_buffer.append(tok)
        #     # yield tok
        #     yield json.dumps({"type": "insights", "data": tok},
        #              ensure_ascii=False) + "\n"
        
        # insights_agent_output = "".join(insights_llm_buffer)
        # print("\n\nInsights LLM:")
        # # print(insights_agent_output_json)
        # print(insights_agent_output)
        # # yield insights_agent_output_json
        # print('\n\n----------\n\n')

    # Insights LLM

        insights_agent_output_json = insights_agent(image_summary, weather_api_data.strip(), insights_agents_model, cause_prediction_llm_output, api_key_nvd)
        
        # insights_agent_output = "".join(insights_llm_buffer)
        print("\n\nInsights LLM:")
        print(insights_agent_output_json)

        print("\n\n TYPE OF INSIGHTS AGENT OUTPUT\n\n")
        print(type(insights_agent_output_json))

        # for key, val in insights_agent_output_json.items():
        #     yield json.dumps({"type": "insights", "data": f"{key} ---> {val}"}, 
        #                      ensure_ascii=False) + "\n"

        yield json.dumps({"type": "insights", "data": insights_agent_output_json},
                     ensure_ascii=False) + "\n"
        

        # print(insights_agent_output)
        # yield insights_agent_output_json
        print('\n\n----------\n\n')

    # Alert LLM
        # insights_agent_output_json = json.loads(insights_agent_output)
        # print(insights_agent_output_json)

        agencies = insights_agent_output_json.get("agency","")
        messages = insights_agent_output_json.get("messages","")
        action = insights_agent_output_json.get("action","")

        print("Alert LLM:")

        agency_res = False

        if agencies:
            agency_res = dispatch_to_responders(agencies, messages)
        # else:
        #     agency_res = 

        print(agency_res)
        if agency_res:
            yield json.dumps({"type": "alert", "data": agency_res},
                        ensure_ascii=False) + "\n"
            
            # Send email
            pretty_action = string.capwords(action.replace('_', ' '))
            subject = f"Alert from ARES - {pretty_action}"

            pretty_agencies = string.capwords(agencies.replace('_', ' '))
            body = f"Agencies: {pretty_agencies}\nLocation: ({lat}, {lon})\nMessage: {'\n'.join(messages)}"
            send_email(subject, body, img)

    
    except Exception as e:
        err = "Encountered issues while invoking agents"
        print("error: {err}\n{e}")
        raise Exception(err) from e