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
sql_host = os.environ.get("SQL_HOST_IP", "192.168.24.2")

# Input API Key
api_key_nvd = os.environ.get("NVIDIA_API_KEY", "")