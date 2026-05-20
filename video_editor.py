import subprocess

def make_video(image_path, audio_path, output_path="output/video.mp4"):
    cmd = [
        "ffmpeg",
        "-loop", "1",
        "-i", image_path,
        "-i", audio_path,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        "-pix_fmt", "yuv420p",
        output_path
    ]

    subprocess.run(cmd, check=True)
    return output_path
