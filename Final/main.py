import os
import json
from dotenv import load_dotenv

from sql_connection import connection_sql, preprocess_summary_sql, preprocess_whole_sql
from embeddings_reranker import embedder_reranker
from weather_api import current_weather,hourly_weather
from cause_prediction_llm import cause_prediction_LLM
from vila_image_summarizer import image_summarizer
from insights_agent import insights_agent
from alert_agent import dispatch_to_responders

load_dotenv()

# NVIDIA model initialization
embedding_model = 'nvidia/nv-embedqa-e5-v5'
reranker_model = 'nvidia/nv-rerankqa-mistral-4b-v3'
cause_prediction_llm_model = 'nvidia/llama-3.3-nemotron-super-49b-v1'
insights_agents_model = 'nvidia/llama-3.1-nemotron-ultra-253b-v1'

# Input API Key
current_key = os.environ.get("NVIDIA_API_KEY", "")

if not current_key.startswith("nvapi-"):
    print("NVIDIA API Key is invalid. Please enter a new key.")
    exit()

# Connect to database
results = connection_sql("Wildfire_Response_Database")
threat_summary_meta_data = preprocess_summary_sql(results)

if results:
    # documents = preprocess_whole_sql(results)
    print("Connected to database")
else:
    print("No database results found")
    exit()


# Image to summary using vila
image_summary = image_summarizer('Test.png')

#################################################
########## Hardcoded Now, change Later ########## 
#################################################
lat = "33"
lon = "-111"

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
print("\n\n Getting top 2 situations \n\n\n")
print(top2)

# Fetch the top 2 event ids
event_ids = [doc.metadata["event_id"] for doc in top2]
print("Top-2 event IDs:", event_ids) 


# From the results , grab values of all columns for that 2 ids

documents = preprocess_whole_sql(results,event_ids)
# Convert it into a document or a string
# Pass it into the cause prediction model

# LLM
# cause_prediction_llm_output = cause_prediction_LLM(NV_rerank, vectorstore, cause_prediction_llm_model, image_summary,weather_api_data.strip())
cause_prediction_llm_output = cause_prediction_LLM(documents, cause_prediction_llm_model, image_summary,weather_api_data.strip())
print("Cause :")
print(cause_prediction_llm_output)

# Insights LLM
insights_agent_output_json = insights_agent(image_summary,weather_api_data.strip(),insights_agents_model,cause_prediction_llm_output)

# Alert LLM
agencies = insights_agent_output_json.get("agency","")

print(f"PRINTING AGENCIES: {agencies}")

if agencies:
    dispatch_to_responders(agencies)