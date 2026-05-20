import os
import requests
from datetime import datetime

print("BOT START")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("ERROR: GEMINI_API_KEY is missing")
    exit(1)

prompt = """
YouTube Shorts / TikTok向けに、
「初心者でもできる・スマホだけ・通勤中でもできる」
AI副業についての縦動画用台本を作成してください。

条件:
- 30〜45秒
- 最初の1文で強く興味を引く
- 初心者向け
- 難しい言葉を使わない
- スマホだけでできる
- 通勤中でもできる
- 無料AI中心
- 1文は短く
- テロップ向け
- 最後に軽く行動促進

出力形式:
タイトル:
台本:
"""

# ★ここが最重要（現状これが一番安定）
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

headers = {
    "Content-Type": "application/json"
}

data = {
    "contents": [
        {
            "parts": [
                {"text": prompt}
            ]
        }
    ]
}

try:
    response = requests.post(url, headers=headers, json=data)

    print("STATUS:", response.status_code)
    print("RAW RESPONSE:", response.text)

    result = response.json()

    if "error" in result:
        print("API ERROR DETECTED")
        exit(1)

    text = result["candidates"][0]["content"]["parts"][0]["text"]

    print("\n=== AI GENERATED SHORTS SCRIPT ===\n")
    print(text)

    os.makedirs("output", exist_ok=True)

    filename = datetime.now().strftime("%Y%m%d_%H%M%S.txt")
    filepath = f"output/{filename}"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)

    print("\nSaved:", filepath)

except Exception as e:
    print("FATAL ERROR:", e)
