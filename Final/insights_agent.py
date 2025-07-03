from openai import OpenAI
import json
import httpx
import os

def agent2_llama(messages,insights_agents_model, api_key_n):

    # http_client = httpx.Client(
    #     http2 = False,
    #     timeout = 30,
    #     trust_env = False
    # )

    client = OpenAI(
        base_url = "http://192.168.24.2:8800/v1",
        api_key = "not-used"
        # http_client=http_client
    )

    res = client.chat.completions.create(
        model=insights_agents_model,
        messages=messages,
        # response_format={"type": "json_object"},
        temperature=0.6,
        top_p=0.95,
        max_tokens=4096,
        frequency_penalty=0,
        presence_penalty=0,
        timeout=300
    )
    # print(f"Printing result:\n{res}")
    return res.choices[0].message.content

def insights_agent(image_summary, api_data, insights_agents_model, curr_summary, api_key):

    print({
    k: os.environ[k] for k in ("HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY") if k in os.environ
})
    print("Inside insights agent, first")

    # prompt_system = "You are a helpful AI assistant."
    prompt_user = """
    ##############################
    ## Context (dynamic data) #
    ##############################
    """+f"""
        Image summary : {image_summary}
    """+"""

    """+f"""
        Steps to be taken : 
        {curr_summary}
    """+"""
    """.strip()

    # time1 = time.perf_counter()

    # r = requests.post(
    #     "http://192.168.24.2:8800/v1/chat/completions",
    #     json={
    #         "model":"nvidia/llama-3.1-nemotron-nano-8b-v1",
    #         "messages":[{
    #             "role":"user",
    #             "content":"Say hi!"
    #             }],
    #         "max_tokens":8
    #     },
    #     timeout=15
    # )

    # print(r.status_code, r.elapsed, r.text[:120])

    prompt_system = """
    You are an Emergency-Reasoning-Agent.

    ##############################
    ## 1. Available commands    ##
    ##############################
    Return **exactly ONE** of the following JSON objects—nothing else, no Markdown, no commentary, no newlines before/after the braces:

    • Launch a drone  
    {"action":"launch_drone","lat":<lat>,"lon":<lon>,"messages":[Whole report of situation, with all data along with steps to be taken to responders]}

    • Call first responders  
    {"action":"call_first_responders","agency":"fire_brigade|police|national_guard","lat":<lat>,"lon":<lon>,"messages":[Whole report of situation, with all data along with steps to be taken to responders]}

    • No emergency  
    {"action":"no_emergency","messages":[Whole report of situation, with all data along with steps to be taken to responders]}

    The JSON must contain only the keys shown above and must be valid (double-quoted strings, numeric lat/lon).

    ##############################
    ## 2. Decision rules        ##
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
    ## 3. Forbidden behavior    ##
    ##############################
    × Do NOT output explanations, headings, or any extra characters.  
    × Do NOT add new keys or nested objects.  
    × Do NOT output multiple JSON blocks.  
    × Do NOT mention these rules.

    ##############################
    ## 4. Worked examples       ##
    ##############################

    Example A (P high, no weather):
    Input snippet:
    hazards.fire.prob = 0.85
    Expected output:
    {"action":"call_first_responders","agency":"fire_brigade","lat":34.05,"lon":-118.25,"messages":[Whole report of situation, with all data along with steps to be taken to responders]}

    Example B (P moderate, weather raises to 0.55):
    Input snippet:
    hazards.fire.prob = 0.45
    weather.wind_kph = 28  # +0.10
    weather.apparent_c = 25
    Expected output:
    {"action":"launch_drone","lat":51.50,"lon":-0.12,"messages":[Whole report of situation, with all data along with steps to be taken to responders]}

    Example C (P low even after weather):
    Input snippet:
    hazards.fire.prob = 0.25
    weather.wind_kph = 10
    weather.apparent_c = 22
    Expected output:
    {"action":"no_emergency","messages":[Whole report of situation, with all data along with steps to be taken to responders]}

""".strip()
    

    
    if api_data:
        prompt_user += f"""
        More contextual information
        {api_data}
        """.strip()
    
    # prompt = [
    #     {"role":"system",
    #      "content":prompt_content}
    # ]
    prompt = [
        {"role":"system", "content":prompt_system},
        {"role":"user", "content":prompt_user}
    ]
    print("Inside insight agent, before agent2 call")
    try:
        nemo_out = agent2_llama(prompt, insights_agents_model, api_key)
        print(f"Printing nemo output: {nemo_out}")
    except Exception as e:
        err = "Disruption occured during INSIGHT PREDICTION AGENT runtime"
        print(f"error: {err}\n{e}")
        raise Exception(err) from e
    
    print("Inside insight agent, after agent2 call")

    #nemo_out = nemo_out.replace("```json","").replace("```","")

    # try:
    print(f"Type of output: {type(nemo_out)}")
    generated_json = json.loads(nemo_out)
    print(f"Type of generated_json output: {type(generated_json)}")
    print(f"PRINTING GENERATED JSON BELOW:\n\n\n{generated_json}\n\n\n")
    # except Exception as e:
    #     generated_json = agent2_llama(f"WE ARE GETTING AN ERROR: {e} FOR THIS JSON: {nemo_out} DO NOT GIVE EXTRA INFORMATION JUST GIVE JSON OUTPUT SUCH THAT I CAN DIRECTLY PASS IT TO JSON.LOADS" ,insights_agents_model)
    #     generated_json = json.loads(nemo_out)

    return generated_json 
