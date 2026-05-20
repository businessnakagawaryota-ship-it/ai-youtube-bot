import os
import json
import time
import random
from datetime import datetime

from google import genai
from google.genai.errors import ClientError


# =========================
# API設定
# =========================
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None


# =========================
# ジャンル
# =========================
GENRES = [
    "AI画像生成",
    "AI動画編集",
    "AI副業"
]


# =========================
# バズテンプレ（強化版）
# =========================
TEMPLATES = {
    "AI画像生成": [
        "【0-3秒】ユウタが画像を見て驚く\nミオ「これAIだよ」\nテロップ：衝撃のAI画像",
        "【0-3秒】カフェでスマホ\nユウタ「これ本物？」\nミオ「AI生成」",
    ],
    "AI動画編集": [
        "【0-3秒】編集に悩むユウタ\nミオ「AIで一瞬だよ」\nテロップ：編集革命",
        "【0-3秒】動画編集画面\nユウタ絶望→ミオ解決",
    ],
    "AI副業": [
        "【0-3秒】ユウタ「副業むずい」\nミオ「AIなら簡単」",
        "【0-3秒】カフェ会話\nミオが稼ぎ方を見せる"
    ]
}


# =========================
# スコアリング（バズ評価）
# =========================
def score_script(text: str) -> int:
    score = 50

    if "フォロー" in text:
        score += 10
    if "AI" in text:
        score += 10
    if "すご" in text or "ヤバ" in text:
        score += 10
    if "！" in text:
        score += 5

    return min(score, 100)


# =========================
# Gemini呼び出し（安定版）
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
            print(f"[Gemini retry {i+1}] {e}")

            if "429" in str(e):
                wait = 5 + i * 10
                time.sleep(wait)
                continue

            return None

    return None


# =========================
# プロンプト生成
# =========================
def build_prompt(genre):
    return f"""
あなたはTikTok/YouTube Shorts専門ディレクター。

ジャンル：{genre}

条件：
- 30秒動画
- カフェの男女2人
- セリフ・テロップ・SE必須
- 冒頭3秒でフック
- バズ重視
"""


# =========================
# ローカル生成（完全fallback）
# =========================
def local_generate(genre):
    base = random.choice(TEMPLATES.get(genre, ["【0-3秒】会話開始"]))

    return f"""{base}

【3-10秒】
ミオがAI解説
ユウタ驚く
テロップ：AIすごい

【10-20秒】
実演シーン
一瞬で変化
テロップ：時短革命

【20-30秒】
ユウタ「やってみたい！」
ミオ「フォローしてね」
テロップ：フォローして続き見てね
"""


# =========================
# メイン処理
# =========================
def main():
    print("=== BOT START ===")

    genre = random.choice(GENRES)
    print("=== SELECTED GENRE ===")
    print(genre)

    prompt = build_prompt(genre)

    print("=== GENERATING SCRIPT ===")

    script = call_gemini(prompt)

    # fallback
    if not script:
        print("=== LOCAL MODE ===")
        script = local_generate(genre)

    score = score_script(script)

    print("=== GENERATED SCRIPT ===")
    print(script)
    print(f"=== SCORE: {score}/100 ===")

    # 保存
    os.makedirs("output", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    data = {
        "genre": genre,
        "script": script,
        "score": score,
        "timestamp": timestamp
    }

    with open("output/latest_script.txt", "w", encoding="utf-8") as f:
        f.write(script)

    with open("output/latest_script.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("=== BOT END ===")


if __name__ == "__main__":
    main()
