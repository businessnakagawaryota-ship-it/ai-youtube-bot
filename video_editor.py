import subprocess
import os

def make_video(image_path, voice_path, script):

    os.makedirs("output", exist_ok=True)

    output = "output/video.mp4"

    cmd = [
        "ffmpeg",
        "-y",
        "-loop", "1",
        "-i", image_path,
        "-i", voice_path,
        "-vf", "scale=1080:1920",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        output
    ]

    subprocess.run(cmd, check=True)

    return output
