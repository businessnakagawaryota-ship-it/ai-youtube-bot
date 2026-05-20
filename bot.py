import os
import google.genai as genai

from script_generator import generate_script
from video_builder import build_video
from voice_generator import generate_voice


def main():
    print("=== BOT START ===")

    # ---------------------------------
    # Gemini client
    # ---------------------------------
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY")
    )

    # ---------------------------------
    # prompt（ここは後で自由に変えてOK）
    # ---------------------------------
    prompt = """
    30秒のバズ用ショート動画台本を作ってください。
    ・3〜5シーン
    ・会話形式（ミオ・ユウタ）
    ・TikTok / YouTube Shorts向け
    ・最初3秒でフック
    """

    # ---------------------------------
    # script生成
    # ---------------------------------
    script = generate_script(client, prompt)

    print("SCRIPT:", script)

    # ---------------------------------
    # 音声生成
    # ---------------------------------
    audio = generate_voice(script["body"])

    # ---------------------------------
    # 動画生成
    # ---------------------------------
    video_path = build_video(script, None, audio)

    print("VIDEO OUTPUT:", video_path)
    print("=== BOT END ===")


if __name__ == "__main__":
    main()
