import random

TREND_KEYWORDS = [
    "AI副業",
    "画像生成",
    "動画編集AI",
    "ChatGPT活用",
    "秒速時短"
]

def get_trend():
    return random.choice(TREND_KEYWORDS)

def calculate_buzz_score(script: str) -> int:
    score = 50

    buzz_words = ["やばい", "一瞬", "無料", "簡単", "爆速", "神"]
    for w in buzz_words:
        if w in script:
            score += 5

    if "フォロー" in script:
        score += 10

    if len(script) > 500:
        score -= 10

    return min(score, 100)
