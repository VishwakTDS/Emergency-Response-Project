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

    result = {
        "responders" : agencies.split("|")
    }

    if not result or "responders" not in result:
        resp = f"No valid 'responders' field in result."
        print(resp)
        return resp
    
    final_response = ""

    for responder in result["responders"]:
        url = responder_urls.get(responder, default_url)

        payload = {
            "responder": responder,
            "message": messages
        }

        final_response += f"\n Sending alert to {responder} → {url}"
        final_response += "Payload:\n"+ json.dumps(payload, indent=2)

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                print(f" Successfully sent to {responder}")
            else:
                print(f" Failed to send to {responder} - Status code: {response.status_code}")
        except Exception as e:
            err = f" Unable to send request to {responder}"
            print(f"error: {err}\n{e}")

    return final_response
        