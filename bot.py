import os
import time
from google import genai
from google.genai.errors import ClientError

print("=== BOT START ===")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_script(genre: str):

    prompt = f"""
あなたはTikTok/YouTube Shorts専門の動画ディレクター。

# 目的
30秒でバズる実写ショート動画の撮影台本を作る

# 絶対ルール（最重要）
- 30秒固定
- 実写（カフェ・男女2人：ミオ・ユウタ）
- Markdown禁止
- 説明文禁止
- タイトル禁止
- ストーリー解説禁止
- 1カット＝1アクションのみ

# 登場人物
ミオ：AIに詳しい女性（落ち着いている）
ユウタ：初心者男性（リアクション大きい）

# ジャンル
{genre}

# 秒構成（絶対固定・変更禁止）
0-3 / 3-6 / 6-9 / 9-12 / 12-15 / 15-18 / 18-21 / 21-24 / 24-27 / 27-30

# 出力フォーマット（完全固定・厳守）

【0-3秒】
映像：1行
セリフ：短く感情だけ（15文字以内）
テロップ：10文字以内
SE：なし

【3-6秒】
映像：1行
セリフ：15文字以内
テロップ：10文字以内
SE：なし

【6-9秒】
映像：1行
セリフ：15文字以内
テロップ：10文字以内
SE：なし

（以下同様）

# 強制ルール
- セリフは説明禁止（感情だけ）
  例：NG「AIはこう使う」
  → OK「え、すご！」
- テロップは10文字以内
- SEは禁止（すべて「なし」）
- 情報量を増やさない
"""

    for i in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={
                    "temperature": 0.35
                }
            )
            return response.text

        except ClientError as e:
            print(f"API retry {i+1}/3: {e}")
            time.sleep(5)

    raise Exception("Gemini API failed after retries")


if __name__ == "__main__":
    genre = "AI画像生成"

    print("=== SELECTED GENRE ===")
    print(genre)

    print("=== GENERATING SCRIPT ===")

    script = generate_script(genre)

    print("=== GENERATED SCRIPT ===")
    print(script)

    os.makedirs("output", exist_ok=True)

    with open("output/latest_script.txt", "w", encoding="utf-8") as f:
        f.write(script)

    print("Saved: output/latest_script.txt")
    print("=== BOT END ===")
