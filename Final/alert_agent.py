
import json
import requests



# dispatcher function
def dispatch_to_responders(agencies):
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

    print("\n Dispatching alerts to responders...\n")

    if not result or "responders" not in result:
        print(" No valid 'responders' field in result.")
        return

    for responder in result["responders"]:
        url = responder_urls.get(responder, default_url)

        payload = {
            "responder": responder,
            "message": result.get("message", "No message provided."),
            "priority": result.get("priority", "Unknown"),
            "actions": result.get("actions", [])
        }

        print(f"\n Sending alert to {responder} → {url}")
        print("Payload:\n", json.dumps(payload, indent=2))

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                print(f" Successfully sent to {responder}")
            else:
                print(f" Failed to send to {responder} – Status code: {response.status_code}")
        except Exception as e:
            print(f" Error while sending to {responder}: {e}")
    return None 

