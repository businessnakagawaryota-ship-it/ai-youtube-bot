import os
from datetime import datetime
from youtube_analyzer import get_trend, calculate_buzz_score

API_KEY = os.getenv("GEMINI_API_KEY")


# -----------------------
# ローカル高品質生成（メイン）
# -----------------------
def local_generate(trend: str):
    return f"""【0-3秒】
ミオ「これ知ってる？」
ユウタ「何それ？」
テロップ：{trend}で人生変わる

【3-10秒】
ミオ「実はこれ、全部AIでできる」

【10-20秒】
ユウタ「え、マジで？」
ミオ「やり方は超シンプル」

【20-30秒】
ユウタ「やってみたい！」
ミオ「フォローしてね」
"""


# -----------------------
# Gemini（補助）
# -----------------------
def try_gemini(prompt):
    try:
        from google import genai
        client = genai.Client(api_key=API_KEY)

        res = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return res.text

    except Exception as e:
        print("Gemini failed → fallback:", e)
        return None


# -----------------------
# プロンプト
# -----------------------
def build_prompt(trend):
    return f"""
TikTokショート台本生成

テーマ: {trend}

条件:
- 30秒
- 実写（ミオ・ユウタ）
- 冒頭3秒で驚き
- テンポ重視
- バズ意識
"""


# -----------------------
# メイン
# -----------------------
def main():
    print("=== BOT START ===")

    trend = get_trend()
    print("TREND:", trend)

    script = None

    # 1. Gemini試す（軽く1回だけ）
    if API_KEY:
        script = try_gemini(build_prompt(trend))

    # 2. fallback（基本こっちが主）
    if not script:
        print("LOCAL MODE ACTIVE")
        script = local_generate(trend)

    score = calculate_buzz_score(script)

    print("=== GENERATED SCRIPT ===")
    print(script)
    print("=== SCORE ===", score)

    os.makedirs("output", exist_ok=True)

    filename = f"output/{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(script + f"\n\nSCORE:{score}")

    print("Saved:", filename)
    print("=== BOT END ===")


if __name__ == "__main__":
    main()
