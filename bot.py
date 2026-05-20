import os
from google import genai

# APIキー
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("=== BOT START ===")

def generate_script(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text


if __name__ == "__main__":
    genre = "AI画像生成"

    prompt = f"""
あなたはTikTok・YouTube Shorts専門の動画ディレクターです。
バズる実写ショート動画台本を作ってください。

ジャンル: {genre}

条件:
- 30〜40秒
- 実写（男女2人：ミオ・ユウタ）
- カフェ設定
- テンポ重視
- SE・テロップ付き
- フォロー誘導あり

出力は台本のみ
"""

    print("=== SELECTED GENRE ===")
    print(genre)

    print("=== GENERATING SCRIPT ===")

    script = generate_script(prompt)

    print("=== GENERATED SCRIPT ===")
    print(script)

    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(script)

    print("=== BOT END ===")
