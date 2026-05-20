from gtts import gTTS
import os

def generate_voice(script):
    os.makedirs("output/audio", exist_ok=True)

    audio_files = []

    for i, s in enumerate(script["scenes"]):
        path = f"output/audio/{i}.mp3"

        tts = gTTS(s["text"], lang="ja")
        tts.save(path)

        audio_files.append(path)

    return audio_files
