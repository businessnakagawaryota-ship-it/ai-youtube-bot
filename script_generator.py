import random

def generate_script(mode="SHORT"):
    try:
        return call_ai(mode)
    except Exception as e:
        print("AI failed → fallback")
        return fallback_script(mode)


def call_ai(mode):
    # ここにGemini入れる想定
    raise Exception("disabled for safety")


def fallback_script(mode):
    if mode == "SHORT":
        return """
【0-3秒】ユウタ「これ何？」ミオ「AIだよ」
【3-10秒】ユウタ「すご」ミオ「簡単だよ」
【10-20秒】実演カット
【20-30秒】フォローしてね
"""
    else:
        return """
【導入】AI画像生成の話
【説明】プロンプトで生成
【実演】変化を見せる
【まとめ】誰でもできる
"""
