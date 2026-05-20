import os
from google import genai

from script_generator import generate_script
from video_builder import build_video
from voice_generator import generate_voice


def main():
    print("=== BOT START ===")

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    prompt = "AI動画のバズ用ショート台本を作って。3〜5シーンで短く"

    script = generate_script(client, prompt)

    audio = generate_voice(script["body"])

    video = build_video(script, None, audio)

    print(video)


if __name__ == "__main__":
    main()
