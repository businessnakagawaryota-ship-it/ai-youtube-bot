import os
import requests
from datetime import datetime, date

print("BOT START")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("ERROR: GEMINI_API_KEY is missing")
    exit(1)

# ----------------------------
# 🎯 副業ジャンル（日替わり）
# ----------------------------
JOBS = [
    "AIライティング副業（文章生成で稼ぐ）",
    "画像生成副業（AIイラスト販売）",
    "文字起こし副業（音声→テキスト）",
    "ショート動画量産副業（AI動画編集）",
    "SNS運用代行副業（投稿作成）",
    "商品説明文作成副業（ECサイト向け）"
]

# 日付ベースで固定（毎日同じジャンルになる）
today_index = int(date.today().strftime("%Y%m%d")) % len(JOBS)
job_type = JOBS[today_index]

print("TODAY JOB:", job_type)

# ----------------------------
# 🎯 プロンプト生成
# ----------------------------
prompt = f"""
あなたはYouTube Shorts / TikTok向けの台本作成AIです。

# 今回のテーマ（絶対にこれ）
{job_type}

# 登場人物
男性：初心者・視聴者代表・悩んでいる
女性：解説者・わかりやすく説明

# ルール
- 30〜45秒
- 必ず会話形式
- 1文は短く
- 最初の3秒で興味を引く
- 難しい言葉は禁止
- ストーリー（悩み→解決）
- 具体例を必ず入れる
- 最後に行動促し

# 超重要ルール
必ずタイトルに「何の副業か」を明確に書くこと
例：
AIライティング副業
画像生成副業
文字起こし副業

# 出力形式
タイトル:
男性:
女性:
男性:
女性:
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

filename = f"output/{timestamp}.txt"

with open(filename, "w", encoding="utf-8") as f:
    f.write(text)

print("Saved:", filename)

# ----------------------------
# 🧠 軽いログ出力（分析用）
# ----------------------------
print("\n=== META ===")
print("DATE:", date.today())
print("JOB:", job_type)
