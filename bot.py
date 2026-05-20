import os
import json
import time

# 新SDK（推奨）
from google import genai
from google.genai import types
from google.genai.errors import ClientError


# =========================
# Gemini初期化
# =========================
API_KEY = os.getenv("GEMINI_API_KEY")

client = None
if API_KEY:
    client = genai.Client(api_key=API_KEY)


# =========================
# フォールバック台本（API死んだ時用）
# =========================
def fallback_script(genre: str):
    return f"""【0-3秒】
映像：カフェでスマホを見るミオとユウタ
ユウタ：「これってAIでできるの？」
テロップ：{genre}って何？

【3-6秒】
ミオ：「実はめっちゃ簡単だよ」
テロップ：意外と簡単！

【6-10秒】
ミオがスマホ操作
ユウタ驚く
テロップ：一瞬で完成！

【10-15秒】
ユウタ：「すごすぎる…」
ミオ：「でしょ？」

【15-20秒】
ミオ：「フォローして続き見てね」
テロップ：フォローしてね！
"""


# =========================
# Gemini呼び出し
# =========================
def call_gemini(prompt: str):
    if client is None:
        raise Exception("No API key")

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text

    except ClientError as e:
        # 429含め全部ここで処理
        print("Gemini API Error:", e)

        if "429" in str(e):
            return None  # ← フォールバックへ
        raise


# =========================
# プロンプト生成
# =========================
def build_prompt(genre: str):
    return f"""
あなたはTikTok/YouTube Shorts専門の動画ディレクターです。

ジャンル: {genre}

条件:
- 30秒ショート動画台本
- カフェで男女2人
- セリフ・テロップ・SEを必ず入れる
- バズ重視
- 簡潔に

形式:
【0-3秒】
映像:
セリフ:
テロップ:
SE:
"""


# =========================
# メイン処理
# =========================
def main():
    print("=== BOT START ===")

    genre = "AI画像生成"
    print("=== SELECTED GENRE ===")
    print(genre)

    prompt = build_prompt(genre)

    print("=== GENERATING SCRIPT ===")

    text = call_gemini(prompt)

    # ===== フォールバック =====
    if text is None:
        print("API limit → fallback mode")
        text = fallback_script(genre)

    print("=== GENERATED SCRIPT ===")
    print(text)

    # 保存
    os.makedirs("output", exist_ok=True)

    with open("output/latest_script.txt", "w", encoding="utf-8") as f:
        f.write(text)

    with open("output/latest_script.json", "w", encoding="utf-8") as f:
        json.dump({"script": text}, f, ensure_ascii=False, indent=2)

    print("=== BOT END ===")


if __name__ == "__main__":
    main()
