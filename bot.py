import os
import json
from datetime import datetime
from google import genai
from google.genai import types

# =========================
# Gemini API設定
# =========================
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=API_KEY)


# =========================
# ジャンル選択（今は固定 or 拡張可）
# =========================
GENRES = [
    "AI文字起こし",
    "AIブログ副業",
    "AI画像生成",
    "AI動画編集"
]

def select_genre():
    # 今はランダムでもOK（後で拡張可）
    import random
    return random.choice(GENRES)


# =========================
# プロンプト生成
# =========================
def build_prompt(genre: str) -> str:
    return f"""
あなたはTikTok・YouTube Shorts専門のトップ動画ディレクターです。

以下の条件でバズる実写ショート動画台本を作ってください：

# ジャンル
{genre}

# 条件
- 30〜40秒
- 実写（カフェ・男女2人：ミオとユウタ）
- 会話ベースでテンポよく
- 視聴維持率最優先
- 冒頭3秒で必ずフック
- セリフ・映像・SE・テロップを必ず分ける
- AI副業系でリアルに感じる内容

# 出力形式
【0-3秒】
カメラ:
映像:
動き:
セリフ:
テロップ:
SE:
"""


# =========================
# Gemini呼び出し
# =========================
def generate_script(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if not response or not response.text:
            raise Exception("Empty response from Gemini")

        return response.text

    except Exception as e:
        return f"[ERROR] Gemini API failed: {str(e)}"


# =========================
# 保存処理
# =========================
def save_output(text: str, genre: str):
    os.makedirs("output", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_path = f"output/{timestamp}.txt"
    json_path = f"output/{timestamp}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "genre": genre,
                "timestamp": timestamp,
                "text": text
            },
            f,
            ensure_ascii=False,
            indent=2
        )

    print(f"Saved: {file_path}")
    print(f"Saved: {json_path}")


# =========================
# メイン処理
# =========================
def main():
    print("=== BOT START ===")

    genre = select_genre()
    print(f"=== SELECTED GENRE ===\n{genre}")

    prompt = build_prompt(genre)

    print("=== GENERATING SCRIPT ===")

    script = generate_script(prompt)

    print("=== GENERATED SCRIPT ===")
    print(script[:2000])  # ログ爆発防止

    save_output(script, genre)

    print("=== BOT END ===")


if __name__ == "__main__":
    main()
