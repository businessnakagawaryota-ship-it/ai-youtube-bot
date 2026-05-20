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
バズる実写ショート動画の台本を作る

# 絶対ルール
- 30秒固定
- 実写（カフェ・男女2人：ミオ・ユウタ）
- Markdown禁止
- 説明文禁止
- タイトル禁止
- 余計な文章禁止
- 秒構成変更禁止

# 登場人物
ミオ：AIに詳しい女性
ユウタ：初心者男性

# ジャンル
{genre}

# 固定秒構成（必ず守る）
0-3 / 3-6 / 6-9 / 9-12 / 12-15 / 15-18 / 18-21 / 21-24 / 24-27 / 27-30

# 出力フォーマット（完全固定）

【0-3秒】
映像：1行
セリフ：1行（なしなら「なし」）
テロップ：15文字以内
SE：短い効果音1つ

【3-6秒】
映像：1行
セリフ：1行
テロップ：15文字以内
SE：短い効果音1つ

（以降同様）

# 重要制約
- テロップは必ず短い（15文字以内）
- SEは1個だけ
- セリフは1行のみ
- ストーリー説明禁止
"""

    for i in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={
                    "temperature": 0.4
                }
            )
            return response.text

        except ClientError as e:
            print(f"API error retry {i+1}/3: {e}")
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
