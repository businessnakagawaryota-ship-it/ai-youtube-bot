import os
import json
import random
import requests
from datetime import datetime

# =========================================
# Gemini API Key
# =========================================

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("GEMINI_API_KEY が設定されていません")
    exit()

# =========================================
# score.json
# =========================================

SCORE_FILE = "score.json"

default_scores = {
    "ChatGPTライティング": 100,
    "AIブログ副業": 100,
    "AI動画編集": 100,
    "AI画像生成": 100,
    "AI文字起こし": 100,
    "AI翻訳副業": 100,
    "AIアフィリエイト": 100,
    "AIせどり": 90,
    "AI SNS運用": 90,
    "AI TikTok運用": 90,
    "AI YouTube運用": 90,
    "AI LINEスタンプ": 80,
    "AI Kindle出版": 80,
    "AIナレーション": 80,
    "Canva AI副業": 80,
    "AIデータ入力": 70,
    "AI営業代行": 70,
    "AI台本作成": 100,
    "AIショート動画": 100,
    "AI文字要約": 90
}

# score.json が無ければ生成
if not os.path.exists(SCORE_FILE):

    with open(SCORE_FILE, "w", encoding="utf-8") as f:
        json.dump(default_scores, f, ensure_ascii=False, indent=2)

# score.json 読み込み
with open(SCORE_FILE, "r", encoding="utf-8") as f:
    scores = json.load(f)

# =========================================
# 人気順でジャンル選択
# =========================================

sorted_genres = sorted(
    scores.items(),
    key=lambda x: x[1],
    reverse=True
)

# 上位5ジャンルからランダム選択
top_genres = [
    genre for genre, score in sorted_genres[:5]
]

selected_genre = random.choice(top_genres)

print("=== SELECTED GENRE ===")
print(selected_genre)

# =========================================
# 朝 / 夕方 判定
# =========================================

current_hour = datetime.now().hour

# 朝〜昼：Shorts
if current_hour < 12:

    mode = "short"

# 夕方〜夜：詳細解説
else:

    mode = "detail"

print("MODE:", mode)

# =========================================
# Shorts用プロンプト
# =========================================

if mode == "short":

    prompt = f"""
YouTube Shorts / TikTok向けに、
「{selected_genre}」についての
短尺動画用台本を作成してください。

条件:
- 30〜45秒
- 最初の1文で強く興味を引く
- AIを使って副業をラクにする内容
- 初心者向け
- スマホだけでできる
- 通勤中でもできる
- 無料AI中心
- 難しい言葉を使わない
- テロップ向き
- TikTok / Shorts向けテンポ
- 女性解説者
- 男性初心者との会話形式
- 1文を短く
- 音声読み上げしやすい
- 朝動画なので詳細は言いすぎない
- 「夕方に詳しく解説するのでフォローして待ってて」と自然に誘導
- 最後にフォロー促進を入れる
- 視聴者が「自分にもできそう」と感じる内容にする

出力形式:

タイトル:
台本:
"""

# =========================================
# 詳細動画用プロンプト
# =========================================

else:

    prompt = f"""
YouTube / TikTok向けに、
「{selected_genre}」についての
詳しい解説動画台本を作成してください。

条件:
- 2〜4分
- AIを使って副業をラクにする内容
- 初心者向け
- スマホだけで可能
- 無料AI中心
- 実際に何をする副業か明確に説明
- 稼ぎ方を具体的に説明
- 女性解説者
- 男性初心者との会話形式
- 難しい言葉を使わない
- 実践方法を具体的に説明
- テロップ向き
- 音声読み上げしやすい
- TikTok / YouTube向け
- 最後にフォロー誘導
- 「自分でもできそう」と感じる説明にする
- 実際に使うAIツール名も含める

出力形式:

タイトル:
台本:
"""

# =========================================
# Gemini API
# =========================================

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

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

print("\n=== BOT START ===")

response = requests.post(
    url,
    headers=headers,
    json=data
)

print("STATUS:", response.status_code)

result = response.json()

# =========================================
# API エラー
# =========================================

if "error" in result:

    print("\n=== API ERROR ===")
    print(result)

    exit()

# =========================================
# テキスト取得
# =========================================

try:

    text = result["candidates"][0]["content"]["parts"][0]["text"]

except Exception as e:

    print("\n=== PARSE ERROR ===")
    print(e)
    print(result)

    exit()

# =========================================
# 出力
# =========================================

print("\n=== GENERATED SCRIPT ===\n")

print(text)

# =========================================
# 保存
# =========================================

os.makedirs("output", exist_ok=True)

filename = datetime.now().strftime("%Y%m%d_%H%M%S.txt")

filepath = f"output/{filename}"

with open(filepath, "w", encoding="utf-8") as f:
    f.write(text)

print(f"\nSaved: {filepath}")

print("\n=== BOT END ===")
