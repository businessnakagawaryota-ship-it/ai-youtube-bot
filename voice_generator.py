from gtts import gTTS
import os


def generate_voice(text):
    path = "output/voice.mp3"

    os.makedirs("output", exist_ok=True)

    tts = gTTS(text=text, lang="ja")
    tts.save(path)

    return path
