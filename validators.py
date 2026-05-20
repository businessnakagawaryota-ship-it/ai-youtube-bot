def score_script(script: str):

    score = 0

    # フックチェック
    if "え" in script:
        score += 20

    # 会話形式チェック
    if "ミオ" in script and "ユウタ" in script:
        score += 30

    # 構成チェック
    if "0-3秒" in script:
        score += 20

    # CTAチェック
    if "フォロー" in script:
        score += 30

    return score
