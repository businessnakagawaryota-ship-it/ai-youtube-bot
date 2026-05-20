import os
from gtts import gTTS

def generate_voice(text, output_path="output/voice.mp3"):
    # ★これ追加（重要）
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    tts = gTTS(text=text, lang="ja")
    tts.save(output_path)

    return output_path
