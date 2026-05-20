import os
from google import genai

print("=== BOT START ===")

# Geminiクライアント初期化
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_script(genre: str) -> str:
    prompt = f"""
あなたはTikTok/YouTube Shorts専門の動画ディレクターです。

# 目的
バズる実写ショート動画の撮影台本を作る

# 条件
- 30〜35秒
- 実写（カフェ・男女2人：ミオ・ユウタ）
- SE・テロップ・セリフ必須
- 秒単位で区切る
- Markdown禁止
- タイトル禁止
- 説明文禁止

# 登場人物
ミオ：AIに詳しい女性（落ち着いている）
ユウタ：初心者男性（リアクション大きい）

# ジャンル
{genre}

# 出力フォーマット（厳守）

【0-3秒】
映像:
セリフ:
テロップ:
SE:

【3-6秒】
映像:
セリフ:
テロップ:
SE:

【6-9秒】
映像:
セリフ:
テロップ:
SE:

【9-12秒】
映像:
セリフ:
テロップ:
SE:

【12-15秒】
映像:
セリフ:
テロップ:
SE:

【15-18秒】
映像:
セリフ:
テロップ:
SE:

【18-21秒】
映像:
セリフ:
テロップ:
SE:

【21-24秒】
映像:
セリフ:
テロップ:
SE:

【24-27秒】
映像:
セリフ:
テロップ:
SE:

【27-30秒】
映像:
セリフ:
テロップ:
SE:

# 重要
- 必ずフォーマット厳守
- ストーリーではなく撮影台本
- 余計な文章を書かない
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "temperature": 0.4
        }
    )

    return response.text


if __name__ == "__main__":
    genre = "AI画像生成"

    print("=== SELECTED GENRE ===")
    print(genre)

    print("=== GENERATING SCRIPT ===")

    script = generate_script(genre)

    print("=== GENERATED SCRIPT ===")
    print(script)

    # 保存
    os.makedirs("output", exist_ok=True)

    with open("output/latest_script.txt", "w", encoding="utf-8") as f:
        f.write(script)

    print("Saved: output/latest_script.txt")
    print("=== BOT END ===")
