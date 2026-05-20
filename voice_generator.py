from gtts import gTTS

def generate_voice(text, output_path="output/voice.mp3"):
    tts = gTTS(text=text, lang="ja")
    tts.save(output_path)
    return output_path
