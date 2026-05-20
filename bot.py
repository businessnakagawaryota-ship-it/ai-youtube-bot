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

年齢感:
26歳

特徴:
・AIに詳しい
・優しい
・落ち着いている
・少しお姉さん感
・テンポよく話す

見た目:
・黒髪ロング
・白系トップス
・清潔感
・カフェでPCを触ってそう

■ 男性初心者キャラ
名前: ユウタ

年齢感:
28歳

特徴:
・副業初心者
・会社員
・疲れ気味
・リアクション大きめ

見た目:
・黒髪短髪
・パーカー or シャツ
・スマホをよく触る
・通勤中っぽい

【世界観固定】

・毎回同じ男女キャラ
・実写Shorts風
・リアルな日常感
・TikTok風テンポ
・スマホ時代感

【背景固定】

・通勤電車
・カフェ
・デスク
・ノートPC
・スマホ
・仕事終わり
・作業風景

【実写動画ルール】

・実際に撮影できる映像のみ
・現実的なカメラワーク
・実写ショート動画風
・非現実演出禁止
・アニメ表現禁止
・超能力演出禁止
・ゲームUI禁止

【映像ルール】

OK:
・スマホ操作
・PCタイピング
・ChatGPT画面
・YouTube画面
・デスク作業
・通勤中
・カフェ会話
・驚くリアクション
・スマホを見る手元
・PC画面アップ

NG:
・魔法演出
・アニメ風変形
・SF表現
・派手すぎる演出

【編集ルール】

・Shorts向け
・縦動画前提
・1カット2〜4秒
・テンポ最優先
・テロップは短く
・冒頭1秒で引き込む
・映像とセリフを一致
"""

# =========================
# 朝ショート動画
# =========================
if mode == "short":

    PROMPT = f"""
{CHARACTER_SETTING}

あなたは、
TikTokとYouTube Shortsで
バズる実写AI副業チャンネルの
動画ディレクターです。

テーマ:
{selected_genre}

目的:
・Shortsでバズる
・フォロー誘導
・夕方動画へ誘導
・「自分でもできそう」と思わせる

動画時間:
30〜45秒

重要:
・冒頭1秒を超強く
・会話テンポ速く
・映像とセリフを一致
・実写で撮影可能な内容のみ

出力形式:

【0-3秒】

カメラ:
映像:
動き:
セリフ:
テロップ:
SE:

【3-6秒】

カメラ:
映像:
動き:
セリフ:
テロップ:
SE:

この形式を最後まで続ける。

最後は必ず:

「夕方に詳しく解説するから
フォローして待ってて！」

で終わる。
"""

# =========================
# 夕方詳細動画
# =========================
else:

    PROMPT = f"""
{CHARACTER_SETTING}

あなたは、
TikTokとYouTube Shortsで
人気のAI副業チャンネルの
実写動画ディレクターです。

テーマ:
{selected_genre}

目的:
・副業内容を詳しく説明
・初心者でもできそうと思わせる
・保存したくなる内容
・コメントしたくなる内容

動画時間:
2〜4分

重要:
・実写で撮れる内容のみ
・現実感重視
・テンポ良く
・映像とセリフ一致

出力形式:

【時間】

カメラ:
映像:
動き:
セリフ:
テロップ:
SE:

毎回、
同じ男女キャラ・同じ世界観で
統一してください。

最後は:

「フォローしておくと
次のAI副業も学べます！」

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
