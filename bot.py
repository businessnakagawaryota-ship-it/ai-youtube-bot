import os
import json
import random
import requests
from datetime import datetime

# =========================
# Gemini API KEY
# =========================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# =========================
# Files
# =========================
SCORE_FILE = "score.json"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# AI副業ジャンル
# =========================
GENRES = [
    "AI動画編集",
    "ChatGPTライティング",
    "AIブログ副業",
    "AI画像生成",
    "AIショート動画量産",
    "AI翻訳副業",
    "AI文字起こし",
    "AI資料作成",
    "AI SNS運用",
    "AIナレーション作成",
    "AI YouTube運営",
    "AI広告作成",
    "AIアフィリエイト",
    "AI台本制作",
    "AI電子書籍販売",
    "AIサムネイル作成"
]

# =========================
# score.json 作成
# =========================
if not os.path.exists(SCORE_FILE):
    default_scores = {}

    for genre in GENRES:
        default_scores[genre] = 100

    with open(SCORE_FILE, "w", encoding="utf-8") as f:
        json.dump(default_scores, f, ensure_ascii=False, indent=2)

# =========================
# score読み込み
# =========================
with open(SCORE_FILE, "r", encoding="utf-8") as f:
    scores = json.load(f)

# =========================
# スコア順
# =========================
sorted_genres = sorted(
    scores.items(),
    key=lambda x: x[1],
    reverse=True
)

top_genres = [g[0] for g in sorted_genres[:5]]

selected_genre = random.choice(top_genres)

# =========================
# 朝 / 夕方 判定
# =========================
hour = datetime.now().hour

if hour < 12:
    mode = "short"
else:
    mode = "detail"

print("=== SELECTED GENRE ===")
print(selected_genre)
print("MODE:", mode)

# =========================
# キャラクター固定設定
# =========================
CHARACTER_SETTING = """
【登場人物固定】

■ 女性解説キャラ
名前: ミオ
年齢感: 26歳
雰囲気:
・落ち着いている
・優しい
・AIに詳しい
・少しお姉さん感
・テンポよく話す

見た目:
・黒髪ロング
・白系トップス
・シンプルで清潔感
・カフェでノートPCを使ってそうな雰囲気

■ 男性初心者キャラ
名前: ユウタ
年齢感: 28歳
雰囲気:
・副業初心者
・少し疲れ気味
・会社員
・リアクション大きめ

見た目:
・黒髪短髪
・パーカー or シャツ
・スマホをよく触る
・通勤中っぽい

【動画全体ルール】

・毎回同じキャラとして描写
・背景や小道具も統一感を出す
・スマホ
・ノートPC
・通勤
・カフェ
・デスク
を中心に構成

【映像ルール】

・映像とセリフを一致させる
・スマホと言ったらスマホ映像
・通勤と言ったら電車映像
・AIと言ったらPCやチャット画面

【編集ルール】

・テンポ重視
・1カット2〜4秒
・Shorts向け
・縦動画前提
・テロップ短め
"""

# =========================
# 朝ショート
# =========================
if mode == "short":

    PROMPT = f"""
{CHARACTER_SETTING}

あなたはTikTokとYouTube Shortsの
超人気AI副業チャンネルの動画構成作家です。

テーマ:
{selected_genre}

目的:
・Shortsでバズる
・フォロー誘導
・夕方動画へ誘導

動画時間:
30〜45秒

構成:
・会話形式
・女性が解説
・男性が驚く
・テンポ速く

以下の形式で出力してください。

【0-3秒】
映像:
セリフ:
テロップ:
SE:

【3-7秒】
映像:
セリフ:
テロップ:
SE:

最後は必ず
「夕方に詳しく解説するからフォローして待ってて」
で終わる。
"""

# =========================
# 夕方詳細
# =========================
else:

    PROMPT = f"""
{CHARACTER_SETTING}

あなたはTikTokとYouTube Shortsの
超人気AI副業チャンネルの動画構成作家です。

テーマ:
{selected_genre}

目的:
・副業内容を詳しく説明
・初心者でもできそうと思わせる
・AIツールを紹介
・保存したくなる内容

動画時間:
2〜4分

構成:
・会話形式
・女性が解説
・男性が質問
・具体例を入れる

以下の形式で出力してください。

【時間】
映像:
セリフ:
テロップ:
SE:

映像は毎回、
同じ男女キャラ・同じ世界観で統一してください。

最後は
「フォローしておくと次のAI副業も学べます」
で終わる。
"""

# =========================
# Gemini API
# =========================
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

headers = {
    "Content-Type": "application/json"
}

data = {
    "contents": [
        {
            "parts": [
                {
                    "text": PROMPT
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

# =========================
# テキスト抽出
# =========================
try:

    generated_text = result["candidates"][0]["content"]["parts"][0]["text"]

    print("\n=== GENERATED SCRIPT ===\n")
    print(generated_text)

    filename = datetime.now().strftime("%Y%m%d_%H%M%S.txt")

    filepath = os.path.join(
        OUTPUT_DIR,
        filename
    )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(generated_text)

    print(f"\nSaved: {filepath}")

except Exception as e:

    print("\nERROR")
    print(result)
    print(e)

# =========================
# score保存
# =========================
with open(SCORE_FILE, "w", encoding="utf-8") as f:
    json.dump(scores, f, ensure_ascii=False, indent=2)

print("\nscore.json saved")

print("\n=== BOT END ===")
