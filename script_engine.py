from trend_prompt_engine import build_dynamic_prompt
from youtube_trend import fetch_videos, extract_keywords
import os

def generate_final_script(topic, api_key=None):

    # APIある場合：トレンド取得
    if api_key:
        titles = fetch_videos(api_key, topic)
        keywords = extract_keywords(titles)

        prompt = build_dynamic_prompt(topic, keywords)

        script = ai_generate_stub(prompt)

    else:
        script = fallback_script(topic)

    return script


# =========================
# AI生成（ダミー or 本体差し替え）
# =========================
def ai_generate_stub(prompt):

    return f"""
【トレンド反映台本】

{prompt}

0-3秒
ミオ「え、これ今めっちゃバズってるやつ」

ユウタ「マジで？」

3-10秒
AI活用説明

10-20秒
実演

20-27秒
ユウタ驚く

27-30秒
ミオ「フォローして続き見てね」
"""


def fallback_script(topic):

    return f"""
【安定版】

0-3秒
ミオ「これ知ってる？」

ユウタ「知らない」

3-30秒
説明構成
"""
