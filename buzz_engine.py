import random

HOOKS = [
    "え、これ知らないの損してる",
    "9割が知らないAIの使い方",
    "これマジで人生変わる",
    "一瞬でプロ級になる方法",
    "今バズってるAIの裏技"
]

CTA = [
    "フォローして続き見てね",
    "コメントで教えて",
    "保存して後で見て",
    "これ知らないと損"
]

KEYWORDS = [
    "無料", "一瞬", "簡単", "神", "やばい", "爆速", "AI", "副業"
]


# =========================
# フック生成
# =========================
def generate_hook():
    return random.choice(HOOKS)


# =========================
# CTA生成
# =========================
def generate_cta():
    return random.choice(CTA)


# =========================
# タイトル生成（10個）
# =========================
def generate_titles(topic):

    base = [
        f"【{topic}】これ知らないと損",
        f"{topic}が一瞬で変わる方法",
        f"AIで人生変わった件",
        f"プロ級が一瞬で作れる時代",
        f"初心者でもできる{topic}",
        f"{topic}の裏技がヤバい",
        f"無料でここまでできるAI",
        f"9割が知らないAI活用",
        f"爆速でプロになる方法",
        f"今話題の{topic}"
    ]

    return base


# =========================
# スコアリング
# =========================
def score_script(script: str):

    score = 0

    for k in KEYWORDS:
        if k in script:
            score += 5

    if "フォロー" in script:
        score += 20

    if "え" in script:
        score += 10

    if len(script) > 200:
        score += 10

    return score
