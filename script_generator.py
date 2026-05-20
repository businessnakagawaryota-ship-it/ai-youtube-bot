import os

def generate_script(client, prompt):
    print("=== GENERATING SCRIPT ===")

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = getattr(response, "text", None)

        # -----------------------------------
        # ① Gemini失敗対策
        # -----------------------------------
        if not text or not text.strip():
            raise ValueError("Gemini returned empty script")

        # -----------------------------------
        # ② 正規化（必須）
        # -----------------------------------
        script = {
            "title": extract_title(text),
            "body": text.strip()
        }

        print("SCRIPT OK")
        return script

    except Exception as e:
        print("SCRIPT GENERATION FAILED:", e)

        # -----------------------------------
        # ③ fallback（絶対空にしない）
        # -----------------------------------
        return {
            "title": "フォールバック動画",
            "body": (
                "ミオ「これ知ってる？」\n"
                "ユウタ「知らない」\n"
                "ミオ「AIで全部できる時代」\n"
                "ユウタ「すごい」\n"
                "ミオ「フォローしてね」"
            )
        }


def extract_title(text):
    # 超簡易タイトル生成
    first_line = text.strip().split("\n")[0]
    return first_line[:20] if first_line else "AI動画"
