def generate_detailed_script(trend):

    prompt = f"""
YouTube解説動画台本を作成してください。

テーマ: {trend}

構成:
- 導入
- 問題提起
- 解説3ポイント
- 事例
- まとめ
- CTA
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
【導入】{trend}とは？
【解説】重要ポイント
【まとめ】結論
【CTA】チャンネル登録
"""
