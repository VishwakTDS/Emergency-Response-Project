import os
from openai import OpenAI
import json

def agent2_llama(messages,insights_agents_model):
    
    client = OpenAI(
        base_url = "https://integrate.api.nvidia.com/v1",
        api_key = os.environ.get("NVIDIA_API_KEY", "")
    )

    res = client.chat.completions.create(
        model=insights_agents_model, # This is the model with the highest number of parameters that can be SFT with LoRA
        messages=messages,
        temperature=0.6,
        top_p=0.95,
        max_tokens=4096,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return res.choices[0].message.content


def insights_agent(image_summary,api_data, insights_agents_model):

    prompt_content = """
        You are **Emergency-Reasoning-Agent**.
        """+f"""
        Image summary : {image_summary}
        """+"""
        You receive exactly one JSON object (schema above; "weather" may be missing).

        Return ONE of these JSON commands and nothing else:

        • Drone:
        {"action":"launch_drone","lat":<lat>,"lon":<lon>}

        • First responders:
        {"action":"call_first_responders",
        "agency":"fire_brigade|police|national_guard",
        "lat":<lat>,"lon":<lon>}

        • No emergency:
        {"action":"no_emergency"}

        DECISION RULE
        Let P = hazards.fire.prob  
        - If "weather" present and wind_kph > 25 → P += 0.10  
        - If "weather" present and apparent_c > 32 → P += 0.05
        Clamp P to 1.0.

        - If P ≥ 0.80   → call_first_responders "fire_brigade"  
        - If 0.40 ≤ P < 0.80 → launch_drone  
        - Else (P < 0.40)   → no_emergency

        Output exactly one JSON object, no extra text.

        """.strip()
    
    if api_data:
        prompt_content += f"""
        More contextual information
        {api_data}
        """.strip()

    
    prompt = [
        {"role":"system",
         "content":prompt_content}
    ]
    nemo_out = agent2_llama(prompt,insights_agents_model)
    generated_json = json.loads(nemo_out)
    return generated_json 