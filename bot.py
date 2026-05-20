import os
import requests
from datetime import datetime

print("BOT START")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("ERROR: GEMINI_API_KEY is missing")
    exit(1)

# ----------------------------
# 🎯 会話台本生成プロンプト
# ----------------------------
prompt = """
あなたはYouTube Shorts / TikTok向けの台本作成AIです。

# 登場人物
男性：視聴者代表（悩み・初心者）
女性：解説者（やさしく説明）

# テーマ
初心者でもできるAI副業・スマホ副業・通勤中でもできる稼ぎ方

# ルール
- 30〜45秒
- 必ず会話形式
- 1文は短く
- 最初の3秒で興味を引く
- 難しい言葉は禁止
- ストーリー（悩み→解決）
- 最後に軽い行動促し

# 出力形式
タイトル:
男性:
女性:
男性:
女性:
まとめ:
"""

# ----------------------------
# 🤖 Gemini API
# ----------------------------
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

headers = {"Content-Type": "application/json"}

data = {
    "contents": [
        {"parts": [{"text": prompt}]}
    ]
}

print("Requesting Gemini...")

response = requests.post(url, headers=headers, json=data)

print("STATUS:", response.status_code)
print("RAW:", response.text)

result = response.json()

if "error" in result:
    print("API ERROR")
    exit(1)

text = result["candidates"][0]["content"]["parts"][0]["text"]

print("\n=== SCRIPT ===\n")
print(text)

# ----------------------------
# 💾 保存
# ----------------------------
os.makedirs("output", exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

txt_path = f"output/{timestamp}.txt"

with open(txt_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Saved:", txt_path)

# ----------------------------
# 🎯 男女分割（音声用）
# ----------------------------

def extract_lines(text):
    male_lines = []
    female_lines = []

    for line in text.split("\n"):
        line = line.strip()

        if line.startswith("男性"):
            male_lines.append(line.replace("男性:", "").strip())

        if line.startswith("女性"):
            female_lines.append(line.replace("女性:", "").strip())

    return male_lines, female_lines


male, female = extract_lines(text)

print("\n=== MALE LINES ===")
print(male)

print("\n=== FEMALE LINES ===")
print(female)

# ----------------------------
# 🎤 Azure TTS（音声生成準備）
# ※キー入れたらそのまま使える形
# ----------------------------

AZURE_KEY = os.getenv("AZURE_TTS_KEY")
AZURE_REGION = os.getenv("AZURE_REGION", "japaneast")

def make_voice(text, voice, filename):
    url = f"https://{AZURE_REGION}.tts.speech.microsoft.com/cognitiveservices/v1"

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3"
    }

    ssml = f"""
<speak version='1.0' xml:lang='ja-JP'>
    <voice name='{voice}'>
        {text}
    </voice>
</speak>
"""

    res = requests.post(url, headers=headers, data=ssml)

    with open(filename, "wb") as f:
        f.write(res.content)

# ----------------------------
# 🎧 音声生成（男女）
# ----------------------------

if AZURE_KEY:
    os.makedirs("output/audio", exist_ok=True)

    male_text = " ".join(male)
    female_text = " ".join(female)

    if male_text:
        make_voice(male_text, "ja-JP-IchiroNeural", f"output/audio/{timestamp}_male.mp3")

    if female_text:
        make_voice(female_text, "ja-JP-NanamiNeural", f"output/audio/{timestamp}_female.mp3")

    print("Audio generated")
else:
    print("AZURE_TTS_KEY not set - skipping audio generation")
