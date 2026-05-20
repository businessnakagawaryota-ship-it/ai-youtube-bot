from gtts import gTTS
import os

def generate_voice(text):

    os.makedirs("output", exist_ok=True)

    path = "output/voice.mp3"

    tts = gTTS(text=text, lang="ja")
    tts.save(path)

    return path
