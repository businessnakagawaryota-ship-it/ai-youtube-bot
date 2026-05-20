import os
import subprocess

OUTPUT_DIR = "output"
CLIP_DIR = os.path.join(OUTPUT_DIR, "clips")
LIST_PATH = os.path.join(OUTPUT_DIR, "list.txt")
OUTPUT_VIDEO = os.path.join(OUTPUT_DIR, "video.mp4")


def build_video(script, images=None, audio_path=None):
    print("=== BUILD VIDEO START ===")

    # ----------------------------------
    # ① フォルダ作成（重要）
    # ----------------------------------
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(CLIP_DIR, exist_ok=True)

    # ----------------------------------
    # ② シーン分割（簡易版）
    # ----------------------------------
    scenes = script.split("\n")
    scenes = [s for s in scenes if s.strip()]

    print(f"Scenes: {len(scenes)}")

    clip_paths = []

    # ----------------------------------
    # ③ clip生成（ここが核心）
    # ----------------------------------
    for i, scene in enumerate(scenes):
        clip_path = os.path.join(CLIP_DIR, f"clip_{i}.mp4")
        clip_paths.append(clip_path)

        text = scene.replace('"', '').replace("'", "")

        cmd = [
            "ffmpeg",
            "-y",
            "-f", "lavfi",
            "-i", "color=c=black:s=1080x1920:d=3",
            "-vf", f"drawtext=text='{text}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2",
            clip_path
        ]

        subprocess.run(cmd, check=True)

    # ----------------------------------
    # ④ list.txt生成（concat用）
    # ----------------------------------
    with open(LIST_PATH, "w") as f:
        for path in clip_paths:
            f.write(f"file '{path}'\n")

    # ----------------------------------
    # ⑤ 動画結合
    # ----------------------------------
    cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", LIST_PATH,
        "-c", "copy",
        OUTPUT_VIDEO
    ]

    subprocess.run(cmd, check=True)

    print("=== VIDEO DONE ===")
    return OUTPUT_VIDEO
