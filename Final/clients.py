from openai import OpenAI
from config import api_key_nvd

# OPENAPI LLM CLIENT
client = OpenAI(
            base_url = "https://integrate.api.nvidia.com/v1",
            api_key = api_key_nvd
        )
