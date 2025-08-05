import json
import requests


# threat_type = history_summary['threat_type']
#     ics_level = history_summary['ics_level']
#     threat_cause = history_summary['anticipated_cause']
#     sops_data = fetch_sops(threat_type, threat_cause, ics_level, agencies_alerted)
#     print(sops_data)


# dispatcher function
def dispatch_to_responders(agencies, messages):
    # simulated responder endpoints
    default_url = "https://httpbin.org/post"
    responder_urls = {
        "Fire": default_url,
        "EMS": default_url,
        "Police": default_url,
        "Animal Control": default_url,
        "Local Security": default_url,
        "Event Staff": default_url,
        "Event Manager": default_url,
        "Janitor": default_url,
        "Military": default_url,
        "Public Works": default_url,
        "Utility Crews": default_url
    }

    responders = [r.strip() for r in agencies.split("|") if r.strip()]
    if not responders:
        return {"error": "no valid responders"}

    results = []

    for responder in responders:
        url = responder_urls.get(responder, default_url)

        payload = {
            "responder": responder,
            "message": messages,
            "url": url
        }

        results.append(payload)

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                print(f" Successfully sent to {responder}")
            else:
                print(f" Failed to send to {responder} - Status code: {response.status_code}")
        except Exception as e:
            err = f" Unable to send request to {responder}"
            print(f"error: {err}\n{e}")

        
    return responder_data

def alert_agencies(data):
    if not data:
        return []

    agencies = set()
    for inc in data:
        resp = inc.get("responding_agencies", "") or ""
        for name in resp.split(","):
            name = name.strip()
            if name:
                agencies.add(name)

    return sorted(agencies)


def check_condition(image_data, weather_data):
    current_probability = image_data['probability']
    wind_speed = weather_data['current_wind_gusts_10m']
    wind_gust = weather_data['current_wind_speed_10m']
    rain = weather_data['current_rain']
    shower = weather_data['current_showers']
    snow = weather_data['current_snowfall']

    if current_probability > 0.4:
        return 0

    if wind_speed > 25:
        current_probability += 0.1
    if wind_gust > 32:
        current_probability += 0.05


    if not rain or not shower or not snow:
        if current_probability < 0.8 and current_probability > 0.4:
            return 1
        else:
            return 2
    else:
        return 2

    # 0 - No Emergency
    # 1 - Send Drone
    # 2 - Emergency (Activate Response Agents)


def build_alert_payload(historic_output, insight_messages, agencies, lat, lon, weather_info):
   
    threat_type  = historic_output["threat_type"]
    threat_cause = historic_output["anticipated_cause"]
    ics_level    = historic_output["ics_level"]

    from sql_connection import fetch_sops
    sops_by_agency = fetch_sops(
        threat_type=threat_type,
        threat_cause=threat_cause,
        ics_level=ics_level,
        agencies=agencies
    )

    common = {
        "location":            historic_output["location"], 
        "latitude":            lat,
        "longitude":           lon,
        "threat_type":         threat_type,
        "anticipated_cause":   threat_cause,
        "ics_level":           ics_level,
        "priority_level":      historic_output['priority'],
        "current_weather":     historic_output["current_weather"],
        "previous_event_insights": historic_output['similar_event_insights'],
        "recommended_measures": historic_output["recommended_measures"],
    }

    insight_text = " ".join(insight_messages)

    payload = []
    for agency in agencies:
        sop = sops_by_agency.get(agency)
        payload.append({
            "agency":          agency,
            "common_info":     common,
            "insight_summary": insight_text,
            "weather_data":    weather_info,
            "sop":             sop or {
                                   "procedure": "No SOP found for this agency at this level.",
                                   "resources":  ""
                               }
        })
    return payload
