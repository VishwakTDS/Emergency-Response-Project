from openai import OpenAI
import json
from sql_connection import fetch_sops

def agent2_llama(messages,insights_agents_model, api_key_n):
    
    client = OpenAI(
        base_url = "https://integrate.api.nvidia.com/v1",
        api_key = api_key_n
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
        stream=False
    )
    return res.choices[0].message.content

def insights_agent(image_summary, weather_data, insights_agents_model, history_summary, agencies_alerted, api_key, DRONE_AVAILABLE):

    prompt_content = f"""
    You are Emergency-Reasoning-Agent.

    ##############################
    ## 1. Context (dynamic data) #
    ##############################
    - Image summary : {image_summary}
    - Historic Incidents and other contextual information about current incident: {history_summary}
    - Current Weather data: {weather_data}
    - DRONE is AVAILABLE: {DRONE_AVAILABLE}
    - PROBABILITY: {image_summary['probability']}

    ##############################
    ## 2. Available commands    ##
    ##############################
    Return **exactly ONE** of the following JSON objects—nothing else, no Markdown, no commentary, no newlines before/after the braces:

    • Launch a drone (ONLY IF drone is available AND 0.4 < probability < 0.8 ELSE call first responders)
    {{"action":"launch_drone","lat":<lat>,"lon":<lon>,"messages":[Whole report of situation, with all data along with steps to be taken to responders]}}

    • Call first responders  
    {{"action":"call_first_responders","agency":{agencies_alerted},"lat":<lat>,"lon":<lon>,"messages":[Whole report of situation, with all data along with steps to be taken to responders]}}

    • No emergency  
    {{"action":"no_emergency","messages":[Whole report of situation, with all data along with steps to be taken to responders]}}

    The JSON must contain only the keys shown above and must be valid (double-quoted strings, numeric lat/lon). 

    ##############################
    ## 3. Decision rules        ##
    ##############################
    Let P = hazards.fire.prob (a float between 0-1) FROM given PROBABILITY

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
    X Do NOT provide the weather data as its given. Format it and explain humanized manner
    X **Do NOT Launch Drone** when **P >= 0.8**

    ##############################
    ## 5. Worked examples       ##
    ##############################

    Example A (P high, no weather):
    Input snippet:
    hazards.fire.prob = 0.85
    OR
    DRONE IS AVAILABLE: FALSE
    Expected output:
    {{"action":"call_first_responders","agency":"From list of agencies","lat":34.05,"lon":-118.25,"messages":[Whole report of situation, with all data along with steps to be taken to responders]}}

    Example B (P moderate, weather raises to 0.55):
    Input snippet:
    PROBABILITY <= 0.4
    hazards.fire.prob = 0.45
    weather.wind_kph = 28  # +0.10
    weather.apparent_c = 25
    DRONE is AVAILABLE: TRUE
    Expected output:
    {{"action":"launch_drone","lat":51.50,"lon":-0.12,"messages":[Whole report of situation, with all data along with steps to be taken to responders]}}

    Example C (P low even after weather):
    Input snippet:
    hazards.fire.prob = 0.25
    weather.wind_kph = 10
    weather.apparent_c = 22
    Expected output:
    {{"action":"no_emergency","messages": No Emergency Detected}}

""".strip()
    
    # if weather_data:
    #     prompt_content += f"""
    #     More contextual information use this 
    #     {weather_data}
    #     """.strip()
    
    # if sops_data is not None:
    #     prompt_content += f"""
    #     ALSO the SOPs the alerted agencies can follow are provided below, include them in your response as well:
    #     {sops_data}
    #     """.strip()
    
    prompt = [
        {"role":"system",
         "content":prompt_content}
    ]
    nemo_out = agent2_llama(prompt, insights_agents_model, api_key)

    #nemo_out = nemo_out.replace("```json","").replace("```","")

    # try:
    generated_json = json.loads(nemo_out)
    # except Exception as e:
    #     generated_json = agent2_llama(f"WE ARE GETTING AN ERROR: {e} FOR THIS JSON: {nemo_out} DO NOT GIVE EXTRA INFORMATION JUST GIVE JSON OUTPUT SUCH THAT I CAN DIRECTLY PASS IT TO JSON.LOADS" ,insights_agents_model)
    #     generated_json = json.loads(nemo_out)

    return generated_json