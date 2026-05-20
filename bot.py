import os
import requests
from datetime import datetime

API_KEY = os.getenv("GEMINI_API_KEY")

print("BOT START")

prompt = """
YouTube Shorts / TikTok向けに、
初心者でもできる・スマホだけ・通勤中でもできる
AI副業の台本を作成して
"""

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

headers = {
    "Content-Type": "application/json"
}

data = {
    "contents": [
        {
            "parts": [{"text": prompt}]
        }
    ]
}

response = requests.post(url, headers=headers, json=data)

print("STATUS:", response.status_code)
print("RAW RESPONSE:", response.text)

try:
    result = response.json()

    text = result["candidates"][0]["content"]["parts"][0]["text"]

    print("=== AI GENERATED ===")
    print(text)

except Exception as e:
    print("PARSE ERROR:", e)
    print("FULL RESULT:", response.text)
