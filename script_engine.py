from buzz_engine import generate_hook, generate_cta, score_script

def generate_final_script(topic):

    hook = generate_hook()
    cta = generate_cta()

    script = f"""
【タイトル】
{topic}で人生変わった件

【フック】
ミオ「{hook}」
ユウタ「え、それ何！？」

【本編】
0-3秒：衝撃スタート
ユウタ「これマジ？」
ミオ「AI使えば一瞬だよ」

3-10秒
ミオが解説
ユウタ驚く

10-20秒
実演パート
ユウタ「やば…」

20-27秒
ミオ「誰でもできる」

27-30秒
ミオ「{cta}」
"""

    score = score_script(script)

    if score < 40:
        script += "\n※再生成推奨レベル"

    return script
