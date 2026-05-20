from googleapiclient.discovery import build
import json
import os

# =========================
# 設定
# =========================

API_KEY = "AIzaSyCxKq2XmUUE3NFWXqyeIzUiUBA1GGnGcYE"
CHANNEL_ID = "UCSjAJUWarh09IbYsLNlu2vA"

SCORE_FILE = "score.json"

# =========================
# YouTube API 接続
# =========================

youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY
)

print("=== YOUTUBE ANALYZER START ===")

# =========================
# 最新動画取得
# =========================

search_response = youtube.search().list(
    part="id,snippet",
    channelId=CHANNEL_ID,
    maxResults=20,
    order="date",
    type="video"
).execute()

video_ids = [
    item["id"]["videoId"]
    for item in search_response["items"]
]

if len(video_ids) == 0:
    print("動画が見つかりません")
    exit()

print(f"取得動画数: {len(video_ids)}")

# =========================
# 動画統計取得
# =========================

video_response = youtube.videos().list(
    part="statistics,snippet",
    id=",".join(video_ids)
).execute()

# =========================
# score.json 作成
# =========================

if not os.path.exists(SCORE_FILE):

    default_scores = {
        "AIライティング": 50,
        "AI画像生成": 50,
        "AI動画編集": 50,
        "AI文字起こし": 50,
        "AI翻訳": 50,
        "AIブログ": 50,
        "AI副業": 50,
        "SNS運用代行": 50,
        "ポイ活": 50,
        "せどり": 50,
        "クラウドワークス": 50,
        "ココナラ": 50,
        "LINEスタンプ": 50,
        "Canva副業": 50,
        "TikTok運用": 50
    }

    with open(SCORE_FILE, "w", encoding="utf-8") as f:
        json.dump(default_scores, f, ensure_ascii=False, indent=2)

# =========================
# score.json 読み込み
# =========================

with open(SCORE_FILE, "r", encoding="utf-8") as f:
    scores = json.load(f)

# =========================
# スコア更新
# =========================

print("\n=== ANALYZE RESULT ===\n")

for item in video_response["items"]:

    title = item["snippet"]["title"]

    views = int(item["statistics"].get("viewCount", 0))
    likes = int(item["statistics"].get("likeCount", 0))
    comments = int(item["statistics"].get("commentCount", 0))

    score = (
        views * 0.01 +
        likes * 0.5 +
        comments * 1
    )

    print("タイトル:", title)
    print("再生数:", views)
    print("いいね:", likes)
    print("コメント:", comments)
    print("計算スコア:", score)

    # =========================
    # タイトルから副業ジャンル判定
    # =========================

    for genre in scores.keys():

        if genre in title:

            scores[genre] += score

            print(f"ジャンル更新: {genre}")
            print(f"新スコア: {scores[genre]}")

    print("------")

# =========================
# 保存
# =========================

with open(SCORE_FILE, "w", encoding="utf-8") as f:
    json.dump(scores, f, ensure_ascii=False, indent=2)

# =========================
# ランキング表示
# =========================

print("\n=== 人気副業ランキング ===\n")

sorted_scores = sorted(
    scores.items(),
    key=lambda x: x[1],
    reverse=True
)

for rank, (genre, score) in enumerate(sorted_scores, start=1):

    print(f"{rank}位: {genre} / SCORE: {round(score, 2)}")

print("\n=== ANALYZER END ===")
