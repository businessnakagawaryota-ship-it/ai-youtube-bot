import os
from gtts import gTTS
import subprocess

os.makedirs("output", exist_ok=True)

# =========================
# ① テンプレ台本（安定化）
# =========================
def generate_script():
    return [
        ("mio.png", "AI画像生成って実はめっちゃ簡単なんだよ"),
        ("yuta.png", "え、マジで？"),
        ("mio.png", "キーワード入れるだけ"),
        ("yuta.png", "やば、プロレベルじゃん"),
        ("mio.png", "誰でもできるよ"),
    ]

# =========================
# ② 音声生成
# =========================
def make_voice(script):
    audio_files = []
    for i, (_, text) in enumerate(script):
        tts = gTTS(text, lang="ja")
        path = f"output/audio_{i}.mp3"
        tts.save(path)
        audio_files.append(path)
    return audio_files

# =========================
# ③ 動画生成
# =========================
def make_video(script, audio_files):
    clips = []

    for i, (img, _) in enumerate(script):
        out = f"output/clip_{i}.mp4"

        subprocess.run([
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", f"assets/{img}",
            "-i", audio_files[i],
            "-c:v", "libx264",
            "-c:a", "aac",
            "-shortest",
            "-t", "4",
            "-pix_fmt", "yuv420p",
            out
        ])

        clips.append(out)

    # concat
    with open("output/list.txt", "w") as f:
        for c in clips:
            f.write(f"file '{c}'\n")

    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", "output/list.txt",
        "-c", "copy",
        "output/final.mp4"
    ])

# =========================
# ④ メイン
# =========================
def main():
    print("=== FULL AUTO BOT START ===")

    script = generate_script()
    audio = make_voice(script)
    make_video(script, audio)

    print("完成：output/final.mp4")

if __name__ == "__main__":
    main()
