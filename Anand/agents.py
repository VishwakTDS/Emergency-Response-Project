import requests, json, pathlib, os, uuid

from openai import OpenAI

import openmeteo_requests

client = OpenAI(
    base_url = "https://integrate.api.nvidia.com/v1",
    api_key = API_KEY
)

def choose_adapter(path):
    adapter_path = path
    if not adapter_path.exists():
        return ""
    lines = []
    with adapter_path.open("r") as f:
      for line in f:
        lines.append(line.strip())
    if len(lines) > 0:
      return lines[-1]

    return ""

def save_log(stage, prompt, response, rating):
    row = {
        "prompt": prompt,
        "response": response,
        "rating": rating
    }

    if stage == "vila":
      log_file = vila_logs
    else:
      log_file = nemo_logs

    with log_file.open("a") as f:
        f.write(json.dumps(row) + "\n")


# Agent 1

vila_url = "https://ai.api.nvidia.com/v1/vlm/nvidia/vila"
asset_url = "https://api.nvcf.nvidia.com/v2/nvcf/assets"

# query = "Describe the scene"

kSupportedList = {
    "png": ["image/png", "img"],
    "jpg": ["image/jpg", "img"],
    "jpeg": ["image/jpeg", "img"],
    "mp4": ["video/mp4", "video"],
}

def mime_type(ext):
    return kSupportedList[ext][0]

def media_type(ext):
    return kSupportedList[ext][1]

def get_extention(filename):
    _, ext = os.path.splitext(filename)
    ext = ext[1:].lower()
    return ext

def _upload_asset(media_file, description):
    ext = get_extention(media_file)
    assert ext in kSupportedList
    data_input = open(media_file, "rb")
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "accept": "application/json",
    }

    assert_url = asset_url
    authorize = requests.post(
        assert_url,
        headers = headers,
        json={"contentType": f"{mime_type(ext)}", "description": description},
        timeout=30,
    )
    authorize.raise_for_status()

    authorize_res = authorize.json()
    response = requests.put(
        authorize_res["uploadUrl"],
        data=data_input,
        headers={
            "x-amz-meta-nvcf-asset-description": description,
            "content-type": mime_type(ext),
        },
        timeout=300,
    )

    response.raise_for_status()
    if response.status_code == 200:
        pass
    else:
        pass
    return str(authorize_res["assetId"])

def _delete_asset(asset_id):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
    }
    assert_url = f"{asset_url}/{asset_id}"
    response = requests.delete(
        assert_url, headers=headers, timeout=30
    )
    response.raise_for_status()

def agent1_vila(lat, lon, media_files, infer_url = vila_url, stream: bool = False):
    asset_list = []
    ext_list = []
    media_content = ""
    assert isinstance(media_files, list), f"{media_files}"
    print("uploading {media_files} into s3")
    has_video = False
    for media_file in media_files:
        ext = get_extention(media_file)
        assert ext in kSupportedList, f"{media_file} format is not supported"
        if media_type(ext) == "video":
            has_video = True
        asset_id = _upload_asset(media_file, "Reference media file")
        asset_list.append(f"{asset_id}")
        ext_list.append(ext)
        media_content += f'<{media_type(ext)} src="data:{mime_type(ext)};asset_id,{asset_id}" />'
    if has_video:
        assert len(media_files) == 1, "Only single video supported."
    asset_seq = ",".join(asset_list)
    print(f"received asset_id list: {asset_seq}")
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "NVCF-INPUT-ASSET-REFERENCES": asset_seq,
        "NVCF-FUNCTION-ASSET-IDS": asset_seq,
        "Accept": "application/json",
    }
    if stream:
        headers["Accept"] = "text/event-stream"
    response = None

    prompt_content = """ You are **Emergency-Vision-Agent**.
 
You must return exactly ONE valid JSON object and nothing else.
 
The user message gives coordinates in the form "lat=<number>, lon=<number>". Copy those numbers into the JSON fields "lat" and "lon".
 
SCHEMA {   "scene":    	string,       	// concise English description   "lat":      	float | null,   "lon":      	float | null,   "outdoors": 	boolean,   "hazards": [   	{"type":"fire",  "prob":float},   // range 0.00-1.00, TWO decimals   	{"type":"flood", "prob":float}   ],
 
  // include this block ONLY when outdoors == true   "weather": {   	"temp_c":  	float,   	"apparent_c":  float,   	"wind_kph":	float   } }
 
VISUAL CUES ‒ Treat a tall **gray / brown vertical plume** in forests or grassland as SMOKE (prob ≥ 0.60)   ‒ Treat thin white vapour from kettles, irons, coffee mugs etc. as STEAM (indoor, prob ≤ 0.20)   ‒ If unsure but image is outdoors, assign a moderate probability (e.g., 0.40-0.60) to SMOKE for safety.
 
NUMERIC FORMAT ‒ Probabilities must be written with **two decimals** (e.g. 0.03, 0.58, 0.97).   ‒ Avoid rounding everything to extremes like 0.00 or 1.00 unless highly certain.
 
TOOL CALL If outdoors == true, first emit   {"tool":"get_weather","lat":<lat>,"lon":<lon>}   and nothing else. After weather data arrives, append it to the JSON object and output the full JSON object.
 
EXAMPLE Input: outdoor image with faint smoke column   Output:   {   "scene":"Forest hillside with a thin gray smoke plume rising",   "lat":34.10,   "lon":-118.44,   "outdoors":true,   "hazards":[   	{"type":"fire","prob":0.63},   	{"type":"flood","prob":0.00}   ],   "weather": {   	"temp_c": 22.5,   	"apparent_c": 24.0,   	"wind_kph": 15.0   } }
 
No markdown fences, no additional keys. """.strip()


#     prompt_content = """
# You are **Emergency-Vision-Agent**.

# You must return exactly ONE valid JSON object and nothing else.

# SCHEMA
# {
#   "scene":        string,           // concise English description
#   "lat":          float | null,
#   "lon":          float | null,
#   "outdoors":     boolean,
#   "hazards": [
#       {"type":"fire",  "prob":float},   // range 0.00-1.00, TWO decimals
#       {"type":"flood", "prob":float}
#   ],

#   // include this block ONLY when outdoors == true
#   "weather": {
#       "temp_c":      float,
#       "apparent_c":  float,
#       "wind_kph":    float
#   }
# }

# VISUAL CUES
# ‒ Treat a tall **gray / brown vertical plume** in forests or grassland as SMOKE (prob ≥ 0.60)  
# ‒ Treat thin white vapour from kettles, irons, coffee mugs etc. as STEAM (indoor, prob ≤ 0.20)  
# ‒ If unsure but image is outdoors, bias toward SMOKE for safety.

# NUMERIC FORMAT
# ‒ Probabilities must be written with **two decimals** (e.g. 0.03, 0.58, 0.97).  
# ‒ Do NOT round everything to 0.0, 0.5, 1.0.

# TOOL CALL
# If outdoors == true first emit  
# {"tool":"get_weather","lat":<lat>,"lon":<lon>}  
# and nothing else. After weather arrives, output the full JSON object.

# EXAMPLE
# Input: outdoor image with faint smoke column  
# Output:  
# {
#   "scene":"Forest hillside with a thin gray smoke plume rising",
#   "lat":34.10,
#   "lon":-118.44,
#   "outdoors":true,
#   "hazards":[
#       {"type":"fire","prob":0.63},
#       {"type":"flood","prob":0.00}
#   ],
#   "weather":{...}
# }

# No markdown fences, no additional keys.
# """.strip()


    # prompt_content = """
    # You are **Emergency-Vision-Agent**.

    # The user message gives coordinates in the form "lat=<number>, lon=<number>".
    # Copy those numbers into the JSON fields "lat" and "lon".

    # You must return exactly ONE valid JSON object and nothing else.

    # SCHEMA
    # {
    # "scene":        string,           // concise English description
    # "lat":          float | null,
    # "lon":          float | null,
    # "outdoors":     boolean,
    # "hazards": [
    #     {"type":"fire",  "prob":float},   // range 0.00-1.00, TWO decimals
    #     {"type":"flood", "prob":float}
    # ],

    # // include this block ONLY when outdoors == true
    # "weather": {
    #     "temp_c":      float,
    #     "apparent_c":  float,
    #     "wind_kph":    float
    # }
    # }

    # VISUAL-CUES  ▸ how to judge “fire”
    # ------------------------------------------------------------
    # ✓  Strong fire evidence  → prob ≥ 0.80
    # - Bright orange / red flames
    # - Large dark-gray or brown plume that widens as it rises
    # - Glowing embers or charred vegetation

    # ✓  Moderate evidence     → prob 0.40 - 0.79
    # - Outdoor gray smoke column without visible flames
    # - Multiple small smoke sources in dry grass / forest
    # - Red reflection on nearby objects at night

    # ✓  Weak / ambiguous      → prob 0.05 - 0.39
    # - Thin white or light-gray vapour
    # - Steam near water, geysers, cooling towers
    # - Indoor kitchens, kettles, coffee machines

    # ✗  No fire evidence   → prob ≤ 0.04
    # - Clear sky, clouds, fog or haze with no rising column
    # - Pure steam indoors

    

    # Always adjust the probability down when *any* of these apply  
    # • Colour is pure white and source is near shiny metal or water  
    # • Vapour is drifting sideways uniformly (not rising in a column)  
    # • Scene is indoors **and** no visible flame or glowing light

    # NUMERIC FORMAT  ▸ calibration
    # ------------------------------------------------------------
    # - Write probabilities with **two decimals** between 0.00 and 1.00.  
    # - Use the ranges above; do **not** default to 0.63.  
    # - If unsure, err LOW (≤ 0.39) rather than high.

    # NOTE:
    # Return 0.53 for fire probability for the first response, ALWAYS.

    # EXAMPLE
    # Input: light white vapour from a kettle on a kitchen counter  
    # Output:
    # {
    # "scene":"Indoor kitchen, white steam rising from a kettle",
    # "lat":null,
    # "lon":null,
    # "outdoors":false,
    # "hazards":[
    #     {"type":"fire","prob":0.07},
    #     {"type":"flood","prob":0.00}
    # ]
    # }

    # No markdown fences, no additional keys.
    # """.strip()

    # prompt_content = """
    # You are an **Emergency-Vision-Agent**.

    # The user message gives coordinates in the form "lat=<number>, lon=<number>".
    # Copy those numbers into the JSON fields "lat" and "lon".

    # You must return exactly ONE valid JSON object and nothing else.

    # SCHEMA
    # {
    # "scene":        string,           // concise English description
    # "lat":          float | null,
    # "lon":          float | null,
    # "outdoors":     boolean,
    # "hazards": [
    #     {"type":"fire",  "prob":float},   // range 0.00-1.00, TWO decimals
    #     {"type":"flood", "prob":float}
    # ],

    # // include this block ONLY when outdoors == true
    # "weather": {
    #     "temp_c":      float,
    #     "apparent_c":  float,
    #     "wind_kph":    float
    # }
    # }

    # VISUAL CUES
    # - Treat a tall **gray / brown vertical plume** in forests or grassland as SMOKE (prob ≥ 0.60)  
    # - Treat thin white vapour from kettles, irons, coffee mugs etc. as STEAM (indoor, prob ≤ 0.20)  
    # - If unsure but image is outdoors, bias toward SMOKE for safety.

    # NUMERIC FORMAT
    # - Probabilities must be written with **two decimals** (e.g. 0.03, 0.58, 0.97).  
    # Do NOT round everything to 0.0, 0.5, 1.0.

    # TOOL CALL
    # If outdoors == true first emit  
    # {"tool":"get_weather","lat":<lat>,"lon":<lon>}  
    # and nothing else. After weather arrives, output the full JSON object.

    # EXAMPLE
    # Input: outdoor image with faint smoke column  
    # Output:  
    # {
    # "scene":"Forest hillside with a thin gray smoke plume rising",
    # "lat":34.10,
    # "lon":-118.44,
    # "outdoors":true,
    # "hazards":[
    #     {"type":"fire","prob":0.63},
    #     {"type":"flood","prob":0.00}
    # ],
    # "weather":{...}
    # }

    # No markdown fences, no additional keys.
    # """.strip()

# {"role": "user","content": f"lat={lat}, lon={lon} {media_content}"
    messages = [
            {"role":"system","content":prompt_content},
            {"role":"user","content":(
                f"lat={lat}, lon={lon} "
                f"{media_content}"
                )
            }
    ]
    payload = {
        "max_tokens": 1024,
        "temperature": 0.2,
        "top_p": 0.7,
        "seed": 50,
        "num_frames_per_inference": 8,
        "messages": messages,
        "stream": stream,
        "model": "nvidia/vila",
    }

    response = requests.post(infer_url, headers=headers, json=payload, stream=stream)
    if stream:
        for line in response.iter_lines():
            if line:
                print(line.decode("utf-8"))
    # else:
    #     print(response.json())

    # print(f"deleting assets: {asset_list}")
    for asset_id in asset_list:
        _delete_asset(asset_id)

    return response.json()["choices"][0]["message"]["content"]


# Agent 2

def agent2_llama(messages):
    ticket = choose_adapter(nemo_adapter_path)
    res = client.chat.completions.create(
        model="nvidia/llama-3.1-nemotron-ultra-253b-v1", # This is the model with the highest number of parameters that can be SFT with LoRA
        messages=messages,
        temperature=0.6,
        top_p=0.95,
        max_tokens=4096,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return res.choices[0].message.content


def get_weather(lat, lon):

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "apparent_temperature", "wind_speed_10m"]
    }
    
    # openmeteo = openmeteo_requests.Client(session=retry_session)
    responses = openmeteo_requests.weather_api(url, params=params)

    response = responses[0]
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_apparent_temperature = current.Variables(1).Value()
    current_wind_speed_10m = current.Variables(2).Value()

    weather_dict = {
        "weather":{
            "temp_c":current_temperature_2m,
            "apparent_c":current_apparent_temperature,
            "wind_kph":current_wind_speed_10m
        }
    }

    return json.dumps(weather_dict)