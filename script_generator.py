import random

def generate_script():

    hooks = [
        "これ知らないと損",
        "AIで人生変わった瞬間",
        "3秒で理解できるAI活用"
    ]

    title = random.choice(hooks)

    scenes = [
        {"speaker":"yuta","text":"え、これ本当にできるの？","duration":3},
        {"speaker":"mio","text":"もう普通にできる時代だよ","duration":3},
        {"speaker":"mio","text":"キーワード入れるだけ","duration":4},
        {"speaker":"yuta","text":"意味わからんレベル","duration":4},
        {"speaker":"mio","text":"フォローして続き見てね","duration":3}
    ]

    return {
        "title": title,
        "scenes": scenes
    }
