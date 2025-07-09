import json
import requests

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

    return {"alerts": results}
        