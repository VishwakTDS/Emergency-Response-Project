import tempfile

import json
from config import *
import time
from sql_connection import connection_sql, preprocess_summary_sql, preprocess_whole_sql
from embeddings_reranker import embedder_reranker
from weather_api import current_weather,hourly_weather, get_location
from cause_prediction_llm import cause_prediction_LLM
from vila_image_summarizer import image_summarizer
from insights_agent import insights_agent
from alert_agent import dispatch_to_responders, alert_agencies, build_alert_payload
from uuid import uuid4
import shutil

# Process the POST input
def input_processing(data):

    # Check latitude range
    if data.latitude < -90 or data.latitude > 90:
        err = f"Latitude must be between -90 and 90"
        print(f"error: {err}")
        raise Exception(err)

    # Check longitude range
    if data.longitude < -180 or data.longitude > 180:
        err = f"Longitude must be between -90 and 90"
        print(f"error: {err}")
        raise Exception(err)
    
    # Save image in a temporary file in memory for further processing
    img_format = f'.{data.input_media.content_type.split("/")[-1]}'

    with tempfile.NamedTemporaryFile(delete=False, suffix=img_format) as tmpimg:
        shutil.copyfileobj(data.input_media.file, tmpimg)

    return tmpimg

def response_generator(img, lat, lon):
    # Connect to database
    # try:
    #     results = connection_sql(sql_database)

    # except Exception as e:
    #     err = "Unsuccessful database connection attempt"
    #     print(f"error: {err}\n{e}")
    #     raise Exception(err) from e
    
    # if results:
    #     print(f"Connected to database")
    # else:
    #     err = "No database results found"
    #     print(f"error: {err}")
    #     raise Exception(err)

    # # Preprocess data
    # threat_summary_meta_data = preprocess_summary_sql(results)
    # print(f"Loaded {len(threat_summary_meta_data)} rows from the database")
    # print('\n\n----------\n\n')

    # Image to summary using vila
    image_summary = image_summarizer(img, api_key_nvd)
    print("Image summary:")
    print(image_summary)
    print('\n\n----------\n\n')

    #################################################
    ########## Hardcoded Now, change Later ########## 
    #################################################

    # calling weather API
    summary = json.loads(image_summary)
    current_weather_json = current_weather(lat,lon)
    # hourly_weather_json = hourly_weather(lat,lon)
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
    # emergency = check_condition(summary, json.loads(current_weather_json))
    # if emergency == 0:
    #     return("No Emergency")
    # elif emergency == 1:
    #     return("Drone Sent !")
    # else:

    location = get_location(lat, lon)
    top_match = embedder_reranker(embedding_model, reranker_model, summary, location)

    DRONE_AVAILABLE = True

    for attempt in (1, 2):

        # Fetch the top 2 event ids
        # event_ids = [doc.metadata["event_id"] for doc in top_match]

        # Get full table data from top 2 occurrences
        # documents = preprocess_whole_sql(results, event_ids)

        # Check API Key
        if not api_key_nvd.startswith("nvapi-"):
            err = "Invalid API key"
            print(f"error: {err}")
            raise Exception(err)

        try:
        # Cause Prediction LLM
            agencies_alerted = None
            if not DRONE_AVAILABLE or summary['probability'] > 0.8:
                agencies_alerted = alert_agencies(data=top_match)
                print("Agenices Alerted: \n", agencies_alerted)
            # cause_prediction_llm_buffer = []
            # for tok in cause_prediction_LLM(top_match, cause_prediction_llm_model, image_summary, api_key_nvd, location, weather_api_data.strip()):
            #     cause_prediction_llm_buffer.append(tok)
            #     yield json.dumps({"type": "cause_prediction", "data": tok},
            #                  ensure_ascii=False) + "\n"
            # cause_prediction_llm_output = "".join(cause_prediction_llm_buffer)
            cause_prediction_llm_output = cause_prediction_LLM(top_match, cause_prediction_llm_model, summary, api_key_nvd, location, weather_api_data.strip())
            print("\n\nCause prediction LLM:")
            print(cause_prediction_llm_output)
            print('\n\n----------\n\n')

        # Insights LLM
            insights_agent_output_json = insights_agent(summary, weather_api_data.strip(), insights_agents_model, cause_prediction_llm_output, agencies_alerted, api_key_nvd, DRONE_AVAILABLE)
            
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

            if attempt == 1 and insights_agent_output_json['action'].strip() == "launch_drone" and DRONE_AVAILABLE:
                DRONE_AVAILABLE = False
                print("\n\nDRONE LAUNCHED. Awaiting updated Input....")
                time.sleep(5)
                print("\nNEW INPUT Received...")
                print('\n\n---------\n\n')

                continue
            
            break

        except Exception as e:
            err = "Encountered issues while invoking agents"
            print("error: {err}\n{e}")
            raise Exception(err) from e
        

    # Alert LLM
    try:
        agencies = insights_agent_output_json.get("agency","")
        # print("AGENCIES: ", agencies)
        messages = insights_agent_output_json.get("messages","")
        # print("MESSAGE TO AGENCIES: ", messages)

        print("Alert LLM:")

        if agencies:
            agency_res = build_alert_payload(cause_prediction_llm_output, messages, agencies, lat, lon, json.loads(current_weather_json))
        # else:
        #     agency_res = 

        print(json.dumps(agency_res, indent=2))
        # if agency_res:
        #     yield json.dumps({"type": "alert", "data": agency_res},
        #                 ensure_ascii=False) + "\n"

    
    except Exception as e:
        err = "Encountered issues while invoking agents"
        print("error: {err}\n{e}")
        raise Exception(err) from e
    