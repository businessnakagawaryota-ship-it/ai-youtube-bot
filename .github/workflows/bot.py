import os
import requests
from datetime import datetime

API_KEY = os.getenv("GEMINI_API_KEY")

prompt = """
YouTube Shorts / TikTok向けに、
「初心者でもできる・スマホだけ・通勤中でもできる」
AI副業についての縦動画用台本を作成してください。

条件:
- 30〜45秒程度
- 最初の1文で強く興味を引く
- 初心者向け
- 難しい言葉を使わない
- スマホだけでできる内容
- 通勤・移動中にできる内容
- 無料AIを中心にする
- 1文を短く
- テロップ向き
- TikTok / Shorts向けテンポ
- 最後に行動を促す一言を入れる

出力形式:
タイトル:
台本:
"""

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

headers = {
    "Content-Type": "application/json"
}

data = {
    "contents": [
        {
            "parts": [
                {
                    "text": prompt
                }
            ]
        }
    ]
}

try:
    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    print("=== AI Generated Shorts Script ===")

    text = result["candidates"][0]["content"]["parts"][0]["text"]

    print(text)

    os.makedirs("output", exist_ok=True)

    filename = datetime.now().strftime("%Y%m%d_%H%M%S.txt")

    filepath = f"output/{filename}"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"\nSaved: {filepath}")

except Exception as e:
    print("ERROR")
    print(e)

    try:
        print(result)
    except:
        pass
