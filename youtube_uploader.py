from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

def upload_video(video_path, thumb_path, title):

    api_key = os.getenv("YOUTUBE_API_KEY")

    youtube = build("youtube", "v3", developerKey=api_key)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": "AI自動生成動画",
                "categoryId": "22"
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=MediaFileUpload(video_path)
    )

    response = request.execute()

    print("uploaded:", response["id"])
