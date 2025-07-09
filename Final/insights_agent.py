from openai import OpenAI
import json

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
        stream=True
    )
    return res.choices[0].message.content

def insights_agent(image_summary, api_data, insights_agents_model, curr_summary, api_key):
#     prompt_content = """
#     You are Emergency-Reasoning-Agent.

#     ##############################
#     ## 1. Context (dynamic data) #
#     ##############################
#     """+f"""
#         Image summary : {image_summary}
#     """+"""

#     """+f"""
#         Steps to be taken : 
#         {curr_summary}
#     """+"""

#     ##############################
#     ## 2. Available commands    ##
#     ##############################
#     Return **exactly ONE** of the following JSON objects—nothing else, no Markdown, no commentary, no newlines before/after the braces:

#     • Launch a drone  
#     {"action":"launch_drone","lat":<lat>,"lon":<lon>,"messages":[Whole report of situation, with all data along with steps to be taken to responders]}

#     • Call first responders  
#     {"action":"call_first_responders","agency":"fire_brigade|police|national_guard","lat":<lat>,"lon":<lon>,"messages":[Whole report of situation, with all data along with steps to be taken to responders]}

#     • No emergency  
#     {"action":"no_emergency","messages":[Whole report of situation, with all data along with steps to be taken to responders]}

#     The JSON must contain only the keys shown above and must be valid (double-quoted strings, numeric lat/lon).

#     ##############################
#     ## 3. Decision rules        ##
#     ##############################
#     Let P = hazards.fire.prob (a float between 0-1).

#     If "weather" exists in the input:
#     • If weather.wind_kph   > 25 → P += 0.10  
#     • If weather.apparent_c > 32 → P += 0.05  

#     Clamp P to a maximum of 1.0.

#     Decision:
#     • If P ≥ 0.80               → call_first_responders with agency="fire_brigade"  
#     • If 0.40 ≤ P < 0.80        → launch_drone  
#     • If P < 0.40               → no_emergency

#     ##############################
#     ## 4. Forbidden behavior    ##
#     ##############################
#     × Do NOT output explanations, headings, or any extra characters.  
#     × Do NOT add new keys or nested objects.  
#     × Do NOT output multiple JSON blocks.  
#     × Do NOT mention these rules.

#     ##############################
#     ## 5. Worked examples       ##
#     ##############################

#     Example A (P high, no weather):
#     Input snippet:
#     hazards.fire.prob = 0.85
#     Expected output:
#     {"action":"call_first_responders","agency":"fire_brigade","lat":34.05,"lon":-118.25,"messages":[Whole report of situation, with all data along with steps to be taken to responders]}

#     Example B (P moderate, weather raises to 0.55):
#     Input snippet:
#     hazards.fire.prob = 0.45
#     weather.wind_kph = 28  # +0.10
#     weather.apparent_c = 25
#     Expected output:
#     {"action":"launch_drone","lat":51.50,"lon":-0.12,"messages":[Whole report of situation, with all data along with steps to be taken to responders]}

#     Example C (P low even after weather):
#     Input snippet:
#     hazards.fire.prob = 0.25
#     weather.wind_kph = 10
#     weather.apparent_c = 22
#     Expected output:
#     {"action":"no_emergency","messages":[Whole report of situation, with all data along with steps to be taken to responders]}

# """.strip()

    system_prompt = """
    You are an Insight Generation Agent for an Emergency Response System.

    You will be provided the following data by the user:
    - Image summary (this is the summary of an image; you will also be provided with a probability which depicts the probability of the image depicting a threat)
    - Steps to be taken
    - API data (optional)

    The objective is to look at all the context provided by the user and reason what steps should be taken next.

    Let P_threat = probability provided by the user in the image summary

    You must now use all the context you have to determine whether the provided probability is accurate.
    If it is not, raise it or bring it down to an appropriate and valid value.

    The steps that can be taken, along with the response you must generate, are all provided below.


    ##############################
    ## 1. Available commands    ##
    ##############################
    Return exactly ONE of the following JSON objects. Nothing else, no Markdown, no commentary, no newlines before/after the braces:

        a) Launch a drone  
        {"action":"launch_drone","lat":<lat>,"lon":<lon>,"messages":[Whole report of situation, with all data along with steps to be taken to responders]}

        b) Call first responders  
        {"action":"call_first_responders","agency":"fire_brigade|police|national_guard","lat":<lat>,"lon":<lon>,"messages":[Whole report of situation, with all data along with steps to be taken to responders]}

        c) No emergency  
        {"action":"no_emergency","messages":[Whole report of situation, with all data along with steps to be taken to responders]}

    The JSON must contain only the keys shown above and must be valid (double-quoted strings, numeric lat/lon).

    ##############################
    ## 2. Decision rules        ##
    ##############################
    
    If "weather" exists in the input:
        - If weather.wind_kph   > 25 → P_threat += 0.10
        - If weather.apparent_c > 32 → P_threat += 0.05

    Clamp P_threat to a maximum of 1.0.

    Decision:
    • If P_threat ≥ 0.80               → call_first_responders with the appropriate agency
    • If 0.40 ≤ P_threat < 0.80        → launch_drone
    • If P_threat < 0.40               → no_emergency

    ##############################
    ## 3. Forbidden behavior    ##
    ##############################
    x Do NOT output explanations, headings, or any extra characters.  
    x Do NOT add new keys or nested objects.  
    x Do NOT output multiple JSON blocks.  
    x Do NOT mention these rules.
    x Do NOT generate responses in a language other than English.

    ##############################
    ## 4. Worked examples       ##
    ##############################

    Example A (P_threat high, no weather):
    Input snippet:
        Probability = 0.85
    Expected output:
        {"action":"call_first_responders","agency":"fire_brigade","lat":34.05,"lon":-118.25,"messages":[Whole report of situation, along with all the data including steps to be taken by responders]}

    Example B (P moderate, weather raises to 0.55):
    Input snippet:
        Probability = 0.45
        weather.wind_kph = 28
        weather.apparent_c = 25
    Expected output:
        {"action":"launch_drone","lat":51.50,"lon":-0.12,"messages":[Whole report of situation, along with all the data including steps to be taken by responders]]}

    Example C (P low even after weather):
    Input snippet:
        Probability = 0.25
        weather.wind_kph = 10
        weather.apparent_c = 22
    Expected output:
        {"action":"no_emergency","messages":[Whole report of situation, along with all the data including steps to be taken by responders]]}

""".strip()
    
    user_prompt = f"""
    
    ################################
    ## Context (dynamic data provided by the user) ##
    ##############################

        Image summary : {image_summary}

        \n\n

        Steps to be taken : {curr_summary}

    """.strip()

    if api_data:
        user_prompt += f"""
        More contextual information provided through API calls:
        API DATA: 
        {api_data}
        """.strip()
    
    prompt = [
        {"role":"system",
         "content":system_prompt},
        {"role":"user",
         "content":user_prompt}
    ]

    nemo_out = agent2_llama(prompt, insights_agents_model, api_key)

    #nemo_out = nemo_out.replace("```json","").replace("```","")

    # try:
    generated_json = json.loads(nemo_out)
    # except Exception as e:
    #     generated_json = agent2_llama(f"WE ARE GETTING AN ERROR: {e} FOR THIS JSON: {nemo_out} DO NOT GIVE EXTRA INFORMATION JUST GIVE JSON OUTPUT SUCH THAT I CAN DIRECTLY PASS IT TO JSON.LOADS" ,insights_agents_model)
    #     generated_json = json.loads(nemo_out)

    return generated_json 
