from openai import OpenAI
from config import api_key_nvd, api_key_hf

# OPENAPI LLM CLIENT
client_nvidia = OpenAI(
            base_url = "https://integrate.api.nvidia.com/v1",
            api_key = api_key_nvd
        )

# HUGGINGFACE LLM CLIENT

client_hf = OpenAI(
        base_url = "https://router.huggingface.co/v1",
        api_key = api_key_hf
    )