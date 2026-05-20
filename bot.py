import os
import requests
from datetime import datetime, date

print("BOT START")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("ERROR: GEMINI_API_KEY is missing")
    exit(1)

# ----------------------------
# 🎯 副業ジャンル（拡張版）
# ----------------------------
JOBS = [
    # AI系
    "AIライティング副業（文章生成）",
    "AI画像生成副業（イラスト販売）",
    "AI動画編集副業（ショート量産）",
    "AI音声生成副業（ナレーション）",
    "AI翻訳副業",
    "AI要約副業",

    # スキル軽作業系
    "文字起こし副業",
    "データ入力副業",
    "SNS運用代行副業",
    "商品説明文作成副業",
    "Canvaデザイン副業",

    # スマホ完結系
    "メルカリ転売副業",
    "ポイ活副業",
    "アンケート副業",
    "写真販売副業",
    "アプリレビュー副業"
]

# ----------------------------
# 🧠 日替わりテーマ固定
# ----------------------------
today_index = int(date.today().strftime("%Y%m%d")) % len(JOBS)
job_type = JOBS[today_index]

print("TODAY THEME:", job_type)

# ----------------------------
# ⏰ 朝 / 夕方判定
# ----------------------------
hour = datetime.now().hour
mode = "morning" if hour < 12 else "evening"

print("MODE:", mode)

# ----------------------------
# 🌅 朝ショート（興味＋軽フォロー）
# ----------------------------
morning_prompt = f"""
あなたはYouTube Shorts台本AIです。

# テーマ
{job_type}

# 目的
視聴者の興味を引くショート動画を作る

# ルール
- 20〜35秒
- 会話形式（男性＝驚き・質問、女性＝軽く説明）
- 副業の詳細は絶対に言わない
- 存在だけ見せる
- 最後に軽くフォロー誘導（見逃し防止）

# 出力形式
タイトル:
男性:
女性:
男性:
女性:
女性:
まとめ:

# フォロールール（朝）
- 押し付けない
- 「夕方に続きがある」＋「見逃し防止」
"""

# ----------------------------
# 🌇 夕方動画（解説＋強フォロー）
# ----------------------------
evening_prompt = f"""
あなたはYouTube解説動画台本AIです。

# テーマ
{job_type}

# 目的
副業のやり方を完全に解説する

# ルール
- 45〜90秒
- 会話形式
- 男性＝質問・理解
- 女性＝具体的に説明
- ステップ形式で説明
- 必ず実例を入れる
- 最後に強いフォロー誘導

# 出力形式
タイトル:
男性:
女性:
男性:
女性:
女性:
まとめ:

# フォロールール（夕方）
- このチャンネルが毎日違う副業を解説していると伝える
- 続きが見たい人にフォローを促す
"""

# ----------------------------
# 🤖 プロンプト選択
# ----------------------------
prompt = morning_prompt if mode == "morning" else evening_prompt

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

print("\n=== GENERATED SCRIPT ===\n")
print(text)

# ----------------------------
# 💾 保存
# ----------------------------
os.makedirs("output", exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

filename = f"output/{mode}_{timestamp}.txt"

with open(filename, "w", encoding="utf-8") as f:
    f.write(text)

print("Saved:", filename)

# ----------------------------
# 📊 メタ情報
# ----------------------------
print("\n=== META ===")
print("MODE:", mode)
print("THEME:", job_type)
