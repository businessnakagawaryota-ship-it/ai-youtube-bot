import os
import json
import random
import requests
from datetime import datetime, date

print("BOT START")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("ERROR: GEMINI_API_KEY is missing")
    exit(1)

# ----------------------------
# 🎯 副業ジャンル
# ----------------------------
JOBS = [
    "AIライティング副業（文章生成）",
    "AI画像生成副業（イラスト販売）",
    "AI動画編集副業（ショート量産）",
    "AI音声生成副業（ナレーション）",
    "AI翻訳副業",
    "AI要約副業",
    "文字起こし副業",
    "データ入力副業",
    "SNS運用代行副業",
    "商品説明文作成副業",
    "Canvaデザイン副業",
    "メルカリ転売副業",
    "ポイ活副業",
    "アンケート副業",
    "写真販売副業",
    "アプリレビュー副業"
]

# ----------------------------
# 📊 スコア管理（疑似バズ学習）
# ----------------------------
SCORE_FILE = "score.json"

if os.path.exists(SCORE_FILE):
    with open(SCORE_FILE, "r", encoding="utf-8") as f:
        scores = json.load(f)
else:
    scores = {job: 1 for job in JOBS}

# 新規ジャンル対応
for job in JOBS:
    if job not in scores:
        scores[job] = 1

# ----------------------------
# 🧠 バズ優先選択ロジック
# ----------------------------
sorted_jobs = sorted(JOBS, key=lambda x: scores.get(x, 1), reverse=True)

# 上位70%＋少しランダム
top_n = max(3, int(len(JOBS) * 0.7))
candidates = sorted_jobs[:top_n]

job_type = random.choice(candidates)

print("SELECTED THEME:", job_type)

# ----------------------------
# ⏰ 朝 / 夕方判定
# ----------------------------
hour = datetime.now().hour
mode = "morning" if hour < 12 else "evening"

print("MODE:", mode)

# ----------------------------
# 🌅 朝プロンプト
# ----------------------------
morning_prompt = f"""
テーマ: {job_type}

副業の“存在だけ”を見せるShorts台本を作成。
詳細は禁止。
最後に軽いフォロー誘導（見逃し防止）。
会話形式（男＝驚き、女＝軽く説明）。
"""

# ----------------------------
# 🌇 夕方プロンプト
# ----------------------------
evening_prompt = f"""
テーマ: {job_type}

副業のやり方を完全解説。
ステップ形式・具体例必須。
最後に強いフォロー誘導（シリーズ化）。
会話形式。
"""

prompt = morning_prompt if mode == "morning" else evening_prompt

# ----------------------------
# 🤖 API
# ----------------------------
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

headers = {"Content-Type": "application/json"}

data = {
    "contents": [{"parts": [{"text": prompt}]}]
}

print("Requesting Gemini...")

response = requests.post(url, headers=headers, json=data)

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

filename = f"output/{mode}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

with open(filename, "w", encoding="utf-8") as f:
    f.write(text)

print("Saved:", filename)

# ----------------------------
# 📊 疑似バズ更新（ランダムで成長）
# ----------------------------
# ※本来は再生数APIに置き換え
if job_type:
    scores[job_type] += random.choice([0, 0, 1, 2])

with open(SCORE_FILE, "w", encoding="utf-8") as f:
    json.dump(scores, f, ensure_ascii=False, indent=2)

print("\n=== SCORE UPDATED ===")
print(job_type, "->", scores[job_type])
