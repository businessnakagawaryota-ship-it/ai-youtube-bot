import os
import json
import time
import google.generativeai as genai

# ========= CONFIG =========
API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-flash"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ========= GEMINI CALL =========
def generate_content(prompt: str):
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.8,
            "max_output_tokens": 4096
        }
    )
    return response


# ========= SAFE TEXT EXTRACTION =========
def extract_text(response):
    try:
        parts = response.candidates[0].content.parts
        return "".join([p.text for p in parts if hasattr(p, "text")])
    except Exception:
        return ""


# ========= CONTINUATION FIX =========
def continue_generation(prev_text: str):
    follow_prompt = f"""
途中で切れているので続きを書いてください。
前の続きとして自然につなげてください。

---ここまで---
{prev_text[-1500:]}
---続き---
"""
    res = generate_content(follow_prompt)
    return extract_text(res)


# ========= MAIN =========
def run_bot():
    print("=== BOT START ===")

    genre = "AI動画編集"  # 仮
    mode = "short"

    prompt = f"""
あなたはTikTok・YouTube Shortsのトップ動画ディレクターです。

ジャンル: {genre}
モード: {mode}

必ず以下形式で出力：
・0〜35秒のショート動画台本
・実写（カフェ・男女2人）
・カメラ指示あり
・セリフあり
・SEあり
・テロップあり
・途中で絶対に途切れない構成
"""

    response = generate_content(prompt)

    text = extract_text(response)

    # ========= 自動補完（途中切れ対策） =========
    if len(text) > 0:
        # 明らかに途中で終わっている場合だけ追記
        if not text.strip().endswith("】") and len(text) > 300:
            print("=== DETECTED CUT OFF → CONTINUING ===")
            extra = continue_generation(text)
            text += "\n" + extra

    # ========= SAVE =========
    ts = time.strftime("%Y%m%d_%H%M%S")
    out_path = f"{OUTPUT_DIR}/{ts}.txt"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)

    print("=== GENERATED SCRIPT ===")
    print(text)
    print(f"Saved: {out_path}")

    print("=== BOT END ===")


if __name__ == "__main__":
    try:
        run_bot()
    except Exception as e:
        print("ERROR:", str(e))
        exit(1)
