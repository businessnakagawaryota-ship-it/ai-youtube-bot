import requests
import os

DID_API = "https://api.d-id.com"

def generate_avatar(image_url, script_text):
    headers = {
        "Authorization": f"Basic {os.getenv('D_ID_API_KEY')}",
        "Content-Type": "application/json"
    }

    payload = {
        "source_url": image_url,
        "script": {
            "type": "text",
            "input": script_text
        }
    }

    res = requests.post(f"{DID_API}/talks", json=payload, headers=headers)
    return res.json()
