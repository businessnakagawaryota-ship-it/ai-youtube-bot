import os
import time
from datetime import datetime
from google import genai
from tenacity import retry, wait_fixed
from youtube_analyzer import get_trend, calculate_buzz_score

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)


# ------------------------
# Gemini呼び出し
# ------------------------
@retry(wait=wait_fixed(2), stop=lambda retry_state: retry_state.attempt_number > 3)
def call_gemini(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        print("Gemini API Error:", e)
        raise


# ------------------------
# フォールバック
# ------------------------
def fallback_script(trend: str):
    return f"""【0-3秒】
ミオ「これ知ってる？」
ユウタ「何それ？」
テロップ：{trend}

【3-10秒】
ミオ「AIで全部できる時代だよ」

【10-30秒】
ユウタ「すごすぎ」
ミオ「フォローしてね」
"""


# ------------------------
# プロンプト生成（バズ最適化）
# ------------------------
def build_prompt(trend: str):
    return f"""
あなたはTikTokトップ動画ディレクター。

テーマ: {trend}

条件:
- 30秒ショート
- 実写（ミオ・ユウタ）
- 冒頭3秒で驚き
- 最後にフォロー誘導
- バズる構成
- テンポ最優先
- セリフ短く

出力は台本のみ
"""


# ------------------------
# メイン
# ------------------------
def main():
    print("=== BOT START ===")

    trend = get_trend()
    print("TREND:", trend)

    prompt = build_prompt(trend)

    script = ""
    try:
        script = call_gemini(prompt)
    except:
        print("API limit → fallback mode")
        script = fallback_script(trend)

    score = calculate_buzz_score(script)

    print("=== GENERATED SCRIPT ===")
    print(script)
    print("=== SCORE ===", score)

    os.makedirs("output", exist_ok=True)

    filename = f"output/{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(script + f"\n\nSCORE:{score}")

    with open("output/latest.txt", "w", encoding="utf-8") as f:
        f.write(script)

    print("Saved:", filename)
    print("=== BOT END ===")


if __name__ == "__main__":
    main()
