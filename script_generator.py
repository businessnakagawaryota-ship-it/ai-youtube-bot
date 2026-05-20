def generate_script(trend):

    prompt = f"""
TikTokショート台本を作成してください。

テーマ: {trend}

条件:
- 30秒以内
- 会話形式（ミオ・ユウタ）
- 0-3秒フック必須
"""

    try:
        from google import genai
        client = genai.Client()

        res = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return res.text

    except Exception:
        return f"""
【0-3秒】ミオ「これ知ってる？」ユウタ「何それ？」
【3-10秒】{trend}解説
【10-30秒】フォロー誘導
"""
