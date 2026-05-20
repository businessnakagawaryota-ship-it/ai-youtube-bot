def build_dynamic_prompt(topic, keywords):

    keyword_text = ", ".join([k[0] for k in keywords])

    return f"""
あなたはYouTube Shortsでバズる脚本家です。

テーマ：{topic}

最新トレンドキーワード：
{keyword_text}

必ず以下を守る：

- カフェ会話形式
- ミオ（解説役）
- ユウタ（驚き役）
- 冒頭3秒でフック必須
- トレンドワードを自然に含める
- 30秒構成

構成：
0-3秒：衝撃フック
3-10秒：問題提起
10-20秒：解決・実演
20-27秒：驚き
27-30秒：フォロー誘導
"""
