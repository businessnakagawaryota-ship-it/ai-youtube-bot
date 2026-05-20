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

■ ミオ（女性）
・26歳
・AIに詳しい
・優しい
・テンポ良く話す
・少しお姉さん感

見た目:
・黒髪ロング
・白トップス
・清潔感

■ ユウタ（男性）
・28歳
・副業初心者
・会社員
・少し疲れ気味
・リアクション大きめ

見た目:
・黒髪短髪
・パーカー or シャツ

【世界観】

・実写Shorts風
・リアルな日常
・スマホ時代感
・TikTok風テンポ

【背景】

・カフェ
・デスク
・通勤
・ノートPC
・スマホ
・ChatGPT画面

【超重要】

・実際に撮れる映像のみ
・素材使い回ししやすく
・同じ場所を使う
・編集負荷を下げる
・CapCut向け
・実写素材向け
・会話テンポ重視

【映像ルール】

優先:
・スマホ画面
・PC画面
・ChatGPT画面
・リアクション
・タイピング
・会話

禁止:
・アニメ演出
・魔法演出
・派手エフェクト
・非現実表現

【編集ルール】

・1カット3〜5秒
・30〜45秒
・カット数少なめ
・SE最小限
・テロップ短く
・冒頭1秒最強
・離脱防止重視
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
トップ動画ディレクターです。

テーマ:
{selected_genre}

目的:
・Shortsでバズる
・フォロー誘導
・夕方動画へ誘導
・初心者でもできそうと思わせる

重要:
・最初の1秒を超強く
・説明より先に驚き
・編集しやすさ重視
・素材使い回し前提
・撮影しやすさ重視

動画時間:
30〜45秒

ルール:
・カット数は少なめ
・同じ場所を使う
・スマホ/PC中心
・実写で簡単に撮れる
・SEは最低限
・テロップ短く

出力形式:

【0-4秒】

カメラ:
映像:
動き:
セリフ:
テロップ:
SE:

【4-8秒】

カメラ:
映像:
動き:
セリフ:
テロップ:
SE:

これを最後まで続ける。

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
・初心者向け解説
・保存したくなる
・コメントしたくなる
・実際に始めたくなる

動画時間:
2〜4分

重要:
・撮影しやすい
・素材使い回し
・ChatGPT画面中心
・実写で可能
・編集負荷を下げる

ルール:
・同じ場所を使う
・スマホ/PC中心
・カット数多すぎ禁止
・SE少なめ
・実用感重視

出力形式:

【時間】

カメラ:
映像:
動き:
セリフ:
テロップ:
SE:

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
