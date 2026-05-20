import requests
from collections import Counter

# =========================
# トレンド動画取得
# =========================
def fetch_videos(api_key, query="AI", max_results=10):

    url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "order": "viewCount",
        "maxResults": max_results,
        "key": api_key
    }

    res = requests.get(url, params=params)
    data = res.json()

    titles = []

    for item in data.get("items", []):
        titles.append(item["snippet"]["title"])

    return titles


# =========================
# キーワード抽出
# =========================
def extract_keywords(titles):

    words = []

    for t in titles:
        words.extend(t.lower().split())

    counter = Counter(words)

    return counter.most_common(10)


# =========================
# トレンドスコア
# =========================
def trend_score(keywords):

    score = 0

    buzz_words = [
        "ai", "簡単", "無料", "やばい", "一瞬",
        "神", "バズ", "副業", "稼ぐ"
    ]

    for word, count in keywords:
        for b in buzz_words:
            if b in word:
                score += count * 10

    return score
