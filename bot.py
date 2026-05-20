import os
import requests
from datetime import datetime

print("BOT START")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("ERROR: GEMINI_API_KEY is missing")
    exit(1)

# ① まず使えるモデル一覧を取得
models_url = f"https://generativelanguage.googleapis.com/v1/models?key={API_KEY}"

print("Fetching available models...")

models_res = requests.get(models_url)
print("MODELS RAW:", models_res.text)

try:
    models_data = models_res.json()

    # flash系を優先して探す
    model_name = None
    for m in models_data.get("models", []):
        name = m.get("name", "")
        if "flash" in name:
            model_name = name
            break

    # fallback
    if not model_name:
        for m in models_data.get("models", []):
            if "gemini" in m.get("name", ""):
                model_name = m.get("name")
                break

    if not model_name:
        print("ERROR: No usable model found")
        exit(1)

    print("SELECTED MODEL:", model_name)

except Exception as e:
    print("MODEL FETCH ERROR:", e)
    exit(1)

# ② プロンプト
prompt = """
YouTube Shorts / TikTok向けに、
初心者でもできる・スマホだけ・通勤中でもできる
AI副業についての縦動画台本を作成してください。

条件:
- 30〜45秒
- 短くテンポよく
- 初心者向け
- 最後に行動を促す

出力:
タイトル:
台本:
"""

# ③ 本番生成
url = f"https://generativelanguage.googleapis.com/v1/{model_name}:generateContent?key={API_KEY}"

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

    if "error" in result:
        print("API ERROR DETECTED")
        exit(1)

    text = result["candidates"][0]["content"]["parts"][0]["text"]

    print("\n=== AI GENERATED SCRIPT ===\n")
    print(text)

    os.makedirs("output", exist_ok=True)

    filename = datetime.now().strftime("%Y%m%d_%H%M%S.txt")
    filepath = f"output/{filename}"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)

    print("\nSaved:", filepath)

except Exception as e:
    print("PARSE ERROR:", e)
