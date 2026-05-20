import os
import requests
from datetime import datetime

API_KEY = os.getenv("GEMINI_API_KEY")

print("BOT START")

if not API_KEY:
    print("ERROR: GEMINI_API_KEY is missing")
    exit(1)

prompt = """
YouTube Shorts / TikTok向けに、
「初心者でもできる・スマホだけ・通勤中でもできる」
AI副業についての縦動画用台本を作成してください。

条件:
- 30〜45秒程度
- 最初の1文で強く興味を引く
- 初者向け
- 難しい言葉を使わない
- スマホだけでできる内容
- 通勤・移動中にできる内容
- 無料AIを中心にする
- 1文を短く
- テロップ向き
- TikTok / Shorts向けテンポ
- 最後に行動を促す一言

出力形式:
タイトル:
台本:
"""

# ★ここが重要（最新安定版）
url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

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
