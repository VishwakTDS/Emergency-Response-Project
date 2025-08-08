import os

from dotenv import load_dotenv

load_dotenv()

# NVIDIA model initialization
embedding_model = 'nvidia/nv-embedqa-e5-v5'
reranker_model = 'nvidia/nv-rerankqa-mistral-4b-v3'
# cause_prediction_llm_model = 'nvidia/llama-3.3-nemotron-super-49b-v1'
cause_prediction_llm_model = 'nvidia/llama-3.1-nemotron-ultra-253b-v1'
insights_agents_model = 'nvidia/llama-3.1-nemotron-ultra-253b-v1'

# SQL database
sql_database = os.environ.get("SQL_DATABASE","Wildfire_Response_Database")
sql_user = os.environ.get("SQL_USER", "postgres")
sql_password = os.environ.get("SQL_PASSWORD", "tdsynnex123")
sql_host = os.environ.get("SQL_HOST_IP", "localhost")
sql_port = os.environ.get("SQL_PORT", "5432")

# Input API Key
api_key_nvd = os.environ.get("NVIDIA_API_KEY", "")
api_key_openWeather = os.environ.get("GEOCODE_API_KEY", "47e473a0579dabe11724d58ed2d05719")

# Send email
sender_email = os.environ.get("SENDER_EMAIL", "sender@sender.com")
sender_password = os.environ.get("SENDER_PASSWORD", "password123")

# SMTP Server Config
smtp_config = {
    "smtp_server": "192.168.24.2",
    "smtp_port": 1025,
    "smtp_user": "ares@tdsynnex.com",
    "smtp_password": None,
}