import os
import time
from datetime import datetime
from google import genai
from google.genai import types

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

GENRE = "AI画像生成"

SYSTEM_PROMPT = """
あなたはTikTok/YouTube Shorts専門のトップ動画ディレクター。

必ず以下ルールを守る：

- 30秒ショート台本
- 1シーン3秒刻み（0-30秒）
- 必ず「映像・セリフ・テロップ・SE」を書く
- 無駄な前置き禁止
- JSONではなくテキストのみ
- 絵コンテ形式で出力
- 絶対に説明しない
"""

def call_gemini(prompt, retry=3):
    for i in range(retry):
        try:
            res = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return res.text
        except Exception as e:
            print(f"API retry {i+1}/{retry}: {e}")
            time.sleep(5 * (i + 1))
    raise Exception("API failed")

def build_prompt():
    return f"""
{SYSTEM_PROMPT}

テーマ: {GENRE}

構成:
0-30秒のショート動画台本を作成

必須フォーマット:

【0-3秒】
映像:
セリフ:
テロップ:
SE:

【3-6秒】
...

必ず最後まで埋める
短くテンポ良く
バズ重視
"""

def save(text):
    os.makedirs("output", exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"output/{ts}.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

    with open("output/latest_script.txt", "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Saved: {path}")

def main():
    print("=== BOT START ===")
    print("=== SELECTED GENRE ===")
    print(GENRE)

    print("=== GENERATING SCRIPT ===")
    prompt = build_prompt()

    text = call_gemini(prompt)

    print("=== GENERATED SCRIPT ===")
    print(text)

    save(text)

    print("=== BOT END ===")

if __name__ == "__main__":
    main()
