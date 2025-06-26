import os
from openai import OpenAI
import json

from config import insights_agents_model

def agent2_llama(messages,insights_agents_model):
    
    client = OpenAI(
        base_url = "https://integrate.api.nvidia.com/v1",
        api_key = os.environ.get("NVIDIA_API_KEY", "")
    )

    res = client.chat.completions.create(
        model=insights_agents_model,
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0.6,
        top_p=0.95,
        max_tokens=4096,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return res.choices[0].message.content

def insights_agent(image_summary,api_data, curr_summary):
    prompt_content = """
    You are Emergency-Reasoning-Agent.

    ##############################
    ## 1. Context (dynamic data) #
    ##############################
    """+f"""
        Image summary : {image_summary}
    """+"""

    """+f"""
        Summary of current situation : 
        {curr_summary}
    """+"""

    ##############################
    ## 2. Available commands    ##
    ##############################
    Return **exactly ONE** of the following JSON objects—nothing else, no Markdown, no commentary, no newlines before/after the braces:

    • Launch a drone  
    {"action":"launch_drone","lat":<lat>,"lon":<lon>,"messages":[Summary from current situation]}

    • Call first responders  
    {"action":"call_first_responders","agency":"fire_brigade|police|national_guard","lat":<lat>,"lon":<lon>,"messages":[Summary from current situation]}

    • No emergency  
    {"action":"no_emergency","messages":[Summary from current situation]}

    The JSON must contain only the keys shown above and must be valid (double-quoted strings, numeric lat/lon).

    ##############################
    ## 3. Decision rules        ##
    ##############################
    Let P = hazards.fire.prob (a float between 0-1).

    If "weather" exists in the input:
    • If weather.wind_kph   > 25 → P += 0.10  
    • If weather.apparent_c > 32 → P += 0.05  

    Clamp P to a maximum of 1.0.

    Decision:
    • If P ≥ 0.80               → call_first_responders with agency="fire_brigade"  
    • If 0.40 ≤ P < 0.80        → launch_drone  
    • If P < 0.40               → no_emergency

    ##############################
    ## 4. Forbidden behavior    ##
    ##############################
    × Do NOT output explanations, headings, or any extra characters.  
    × Do NOT add new keys or nested objects.  
    × Do NOT output multiple JSON blocks.  
    × Do NOT mention these rules.

    ##############################
    ## 5. Worked examples       ##
    ##############################

    Example A (P high, no weather):
    Input snippet:
    hazards.fire.prob = 0.85
    Expected output:
    {"action":"call_first_responders","agency":"fire_brigade","lat":34.05,"lon":-118.25,"messages":[Summary from current situation]}

    Example B (P moderate, weather raises to 0.55):
    Input snippet:
    hazards.fire.prob = 0.45
    weather.wind_kph = 28  # +0.10
    weather.apparent_c = 25
    Expected output:
    {"action":"launch_drone","lat":51.50,"lon":-0.12,"messages":[Summary from current situation]}

    Example C (P low even after weather):
    Input snippet:
    hazards.fire.prob = 0.25
    weather.wind_kph = 10
    weather.apparent_c = 22
    Expected output:
    {"action":"no_emergency","messages":[Summary from current situation]}

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

    #nemo_out = nemo_out.replace("```json","").replace("```","")

    # try:
    generated_json = json.loads(nemo_out)
    # except Exception as e:
    #     generated_json = agent2_llama(f"WE ARE GETTING AN ERROR: {e} FOR THIS JSON: {nemo_out} DO NOT GIVE EXTRA INFORMATION JUST GIVE JSON OUTPUT SUCH THAT I CAN DIRECTLY PASS IT TO JSON.LOADS" ,insights_agents_model)
    #     generated_json = json.loads(nemo_out)

    return generated_json 
