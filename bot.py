import os
import json
import time
import random

# Gemini（新SDK）
from google import genai
from google.genai import types
from google.genai.errors import ClientError


# =========================
# 設定
# =========================
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY) if API_KEY else None


# =========================
# ジャンル
# =========================
GENRES = ["AI画像生成", "AI動画編集", "AI副業"]


# =========================
# ローカル台本テンプレ（10パターン）
# =========================
LOCAL_TEMPLATES = [
    """【0-3秒】映像：カフェでスマホを見るミオとユウタ
ユウタ「これ何してるの？」
ミオ「AI画像生成だよ」
テロップ：AIってすごい
SE：軽いBGM""",

    """【0-3秒】ユウタ「AIって難しいよね？」
ミオ「実は逆だよ」
テロップ：意外と簡単
SE：ポン""",

    """【0-3秒】ユウタが悩む
ミオがスマホ見せる
テロップ：一瞬で変わる世界""",

    """【0-3秒】ミオ「これ全部AI」
ユウタ「え？」
テロップ：衝撃""",

    """【0-3秒】ユウタ「時間かかる…」
ミオ「AIで一瞬」
テロップ：時短革命""",

    """【0-3秒】カフェで会話
AI画像を見せる
テロップ：プロ級""",

    """【0-3秒】ユウタ困惑
ミオ解説
テロップ：初心者OK""",

    """【0-3秒】スマホ操作
AI生成開始
テロップ：自動生成""",

    """【0-3秒】ユウタ驚く
ミオニヤリ
テロップ：バズ技""",

    """【0-3秒】ミオ「やってみて」
ユウタ「すご！」
テロップ：体験型AI"""
]


# =========================
# プロンプト
# =========================
def build_prompt(genre):
    return f"""
あなたはTikTok/YouTube Shorts専門ディレクター。

ジャンル：{genre}

条件：
- 30秒ショート動画
- カフェの男女2人
- セリフ・テロップ・SE必須
- バズ重視
- 簡潔
"""


# =========================
# Gemini呼び出し（超安定版）
# =========================
def call_gemini(prompt, retries=3):
    if not client:
        return None

    for i in range(retries):
        try:
            res = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return res.text

        except ClientError as e:
            print(f"Gemini error {i+1}/{retries}: {e}")

            # 429は待つ
            if "429" in str(e):
                wait = 10 + i * 5
                print(f"wait {wait}s...")
                time.sleep(wait)
                continue

            return None

    return None


# =========================
# ローカル生成（必ず動く）
# =========================
def local_generate(genre):
    base = random.choice(LOCAL_TEMPLATES)

    extra = f"""

【後半補足】
ジャンル：{genre}
ミオが解説してユウタが驚く構成
フォロー誘導あり
"""

    return base + extra


# =========================
# メイン
# =========================
def main():
    print("=== BOT START ===")

    genre = random.choice(GENRES)
    print("=== SELECTED GENRE ===")
    print(genre)

    prompt = build_prompt(genre)

    print("=== GENERATING SCRIPT ===")

    script = call_gemini(prompt)

    if script is None:
        print("→ fallback mode")
        script = local_generate(genre)

    print("=== GENERATED SCRIPT ===")
    print(script)

    # 保存
    os.makedirs("output", exist_ok=True)

    with open("output/latest_script.txt", "w", encoding="utf-8") as f:
        f.write(script)

    with open("output/latest_script.json", "w", encoding="utf-8") as f:
        json.dump({
            "genre": genre,
            "script": script,
            "timestamp": time.time()
        }, f, ensure_ascii=False, indent=2)

    print("=== BOT END ===")


if __name__ == "__main__":
    main()
