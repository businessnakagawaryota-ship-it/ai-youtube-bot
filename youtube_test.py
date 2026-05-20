from googleapiclient.discovery import build

print("START")

API_KEY = "AIzaSyCxKq2XmUUE3NFWXqyeIzUiUBA1GGnGcYE"
CHANNEL_ID = "UCSjAJUWarh09IbYsLNlu2vA"

youtube = build("youtube", "v3", developerKey=API_KEY)

# 最新動画取得
search_response = youtube.search().list(
    part="id",
    channelId=CHANNEL_ID,
    maxResults=5,
    order="date",
    type="video"
).execute()

video_ids = [
    item["id"]["videoId"]
    for item in search_response["items"]
]

print("VIDEO IDS:")
print(video_ids)

# 動画詳細取得
video_response = youtube.videos().list(
    part="statistics,snippet",
    id=",".join(video_ids)
).execute()

print("\n=== VIDEO DATA ===\n")

for item in video_response["items"]:

    title = item["snippet"]["title"]

    views = item["statistics"].get("viewCount", 0)
    likes = item["statistics"].get("likeCount", 0)
    comments = item["statistics"].get("commentCount", 0)

    print("タイトル:", title)
    print("再生数:", views)
    print("いいね:", likes)
    print("コメント:", comments)
    print("------")

print("END")