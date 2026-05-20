from prompt_templates import build_prompt
from validators import score_script

# =========================
# メイン生成関数
# =========================
def generate_final_script(topic: str):

    prompt = build_prompt(topic)

    # ここは本来 Gemini / OpenAI
    # 今は安定版テンプレ生成（API依存しない）
    script = local_fallback_script(topic)

    score = score_script(script)

    if score < 80:
        print("⚠ LOW QUALITY SCRIPT - regenerating...")
        script = local_fallback_script(topic)

    return script


# =========================
# 安定テンプレ生成（重要）
# =========================
def local_fallback_script(topic):

    return f"""
【タイトル】
カフェで発見！AIで人生変わるレベルだった件

【ジャンル】
{topic}

【構成】

0-3秒
ユウタ「え、これ本当にAIでできるの？」
ミオ「そうだよ、もう常識変わってる」

3-10秒
ユウタ「難しそう…」
ミオ「実はめっちゃ簡単」

10-20秒
ミオ「キーワード入れるだけでOK」
ユウタ「意味わからんレベルで簡単じゃん…」

20-27秒
（実演カット想定）
ユウタ「一瞬でできた…やば」

27-30秒
ミオ「フォローして続き見てね」
"""
