import requests
from collections import Counter

# =========================
# YouTubeデータ取得（簡易版）
# =========================
def fetch_trending_videos(api_key, query="AI", max_results=10):

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

    videos = []

    for item in data.get("items", []):
        title = item["snippet"]["title"]
        videos.append(title)

    return videos


# =========================
# タイトル分析
# =========================
def analyze_titles(titles):

    words = []

    for t in titles:
        words.extend(t.lower().split())

    counter = Counter(words)

    common_words = counter.most_common(10)

    return common_words


# =========================
# バズ傾向スコア生成
# =========================
def generate_insights(common_words):

    hooks = ["神", "やばい", "衝撃", "簡単", "一瞬", "無料", "バズ"]

    score = 0

    for word, count in common_words:
        for h in hooks:
            if h in word:
                score += count * 10

    return {
        "trend_score": score,
        "top_keywords": common_words
    }


# =========================
# フルパイプライン
# =========================
def analyze_youtube(api_key, query="AI動画編集"):

    print("=== ANALYZING YOUTUBE ===")

    titles = fetch_trending_videos(api_key, query)

    keywords = analyze_titles(titles)

    insights = generate_insights(keywords)

    print("=== TREND INSIGHTS ===")
    print(insights)

    return insights
