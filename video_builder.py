import subprocess
import os

def build_video(script, images, audio):

    os.makedirs("output", exist_ok=True)

    clips = []

    for i in range(len(script["scenes"])):

        out = f"output/clip_{i}.mp4"

        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", images[i],
            "-i", audio[i],
            "-vf", "zoompan=z='min(zoom+0.0015,1.1)':d=1",
            "-c:v", "libx264",
            "-c:a", "aac",
            "-shortest",
            out
        ]

        subprocess.run(cmd, check=True)

        clips.append(out)

    # concat
    with open("output/list.txt", "w") as f:
        for c in clips:
            f.write(f"file '{c}'\n")

    final = "output/video.mp4"

    subprocess.run([
        "ffmpeg","-y",
        "-f","concat",
        "-safe","0",
        "-i","output/list.txt",
        "-c","copy",
        final
    ], check=True)

    return final
