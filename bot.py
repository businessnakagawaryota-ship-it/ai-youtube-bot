import os
import json
import random
import time
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
GENRES = ["AI画像生成", "AI動画編集", "AI副業"]


# =========================
# バズ構造テンプレ（核心）
# =========================
HOOKS = [
    "え、これAIでできるの！？",
    "たった3秒で人生変わるレベル",
    "これ知らないと損してる",
    "もう手作業には戻れない",
    "初心者でも一瞬でプロ級"
]

EMOTIONS = ["驚く", "焦る", "興奮する", "納得する", "感動する"]

CALL_TO_ACTION = [
    "フォローして続き見てね",
    "保存して後で試して",
    "コメントで教えて",
    "他のAIも見てみる？"
]


# =========================
# スコアリング（バズ強化版）
# =========================
def score_script(text: str) -> int:
    score = 50

    if any(h in text for h in HOOKS):
        score += 15
    if "フォロー" in text:
        score += 10
    if "AI" in text:
        score += 10
    if "！" in text:
        score += 5
    if "すご" in text or "ヤバ" in text:
        score += 10

    return min(score, 100)


# =========================
# Gemini（使えたら強化）
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
                time.sleep(5 + i * 10)
                continue

            return None

    return None


# =========================
# 超重要：構造型ローカル生成（完成形）
# =========================
def local_generate(genre):
    hook = random.choice(HOOKS)
    emotion = random.choice(EMOTIONS)
    cta = random.choice(CALL_TO_ACTION)

    return f"""
【0-3秒（フック）】
ミオ「{hook}」
ユウタ「えっ！？」
テロップ：衝撃スタート

【3-10秒】
ミオがAI（{genre}）を解説
ユウタが{emotion}
テロップ：AIで一瞬で変わる

【10-20秒】
実演シーン
ユウタ「これやばい…」
テロップ：プロ級クオリティ

【20-30秒】
ミオ「君もできるよ」
ユウタ「やりたい！」
テロップ：{cta}
"""


# =========================
# プロンプト（API用）
# =========================
def build_prompt(genre):
    return f"""
あなたはTikTok/YouTube Shortsのトップディレクター。

ジャンル：{genre}

必須：
- 30秒構成
- 0-3秒で強いフック
- カフェ男女2人
- セリフ＋テロップ＋SE
- バズ最優先構造
- 最後は必ずフォロー誘導
"""


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

    if not script:
        print("=== LOCAL MODE (STABLE GENERATION) ===")
        script = local_generate(genre)

    score = score_script(script)

    print("=== GENERATED SCRIPT ===")
    print(script)
    print(f"=== SCORE: {score}/100 ===")

    # 保存
    os.makedirs("output", exist_ok=True)

    data = {
        "genre": genre,
        "script": script,
        "score": score,
        "timestamp": datetime.now().isoformat()
    }

    with open("output/latest_script.txt", "w", encoding="utf-8") as f:
        f.write(script)

    with open("output/latest_script.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("=== BOT END ===")


if __name__ == "__main__":
    main()
