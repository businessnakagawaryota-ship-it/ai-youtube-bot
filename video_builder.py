import os
import subprocess

OUTPUT_DIR = "output"
CLIPS_DIR = os.path.join(OUTPUT_DIR, "clips")
LIST_FILE = os.path.join(OUTPUT_DIR, "list.txt")
OUTPUT_VIDEO = os.path.join(OUTPUT_DIR, "video.mp4")


def build_video(script, images=None, audio=None):
    print("=== BUILD VIDEO START ===")

    # ---------------------------
    # ① フォルダ作成
    # ---------------------------
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(CLIPS_DIR, exist_ok=True)

    # ---------------------------
    # ② script型の吸収（ここ重要）
    # ---------------------------
    if isinstance(script, dict):
        text = script.get("body") or script.get("script") or ""
    else:
        text = str(script)

    scenes = [s.strip() for s in text.split("\n") if s.strip()]

    print(f"Scenes: {len(scenes)}")

    clip_paths = []

    # ---------------------------
    # ③ clip生成
    # ---------------------------
    for i, scene in enumerate(scenes):
        clip_path = os.path.join(CLIPS_DIR, f"clip_{i}.mp4")
        clip_paths.append(clip_path)

        safe_text = scene.replace('"', '').replace("'", "")

        cmd = [
            "ffmpeg",
            "-y",
            "-f", "lavfi",
            "-i", "color=c=black:s=1080x1920:d=3",
            "-vf",
            f"drawtext=text='{safe_text}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2",
            clip_path
        ]

        subprocess.run(cmd, check=True)

    # ---------------------------
    # ④ list.txt生成
    # ---------------------------
    with open(LIST_FILE, "w") as f:
        for path in clip_paths:
            f.write(f"file '{path}'\n")

    # ---------------------------
    # ⑤ ffmpeg結合
    # ---------------------------
    cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", LIST_FILE,
        "-c", "copy",
        OUTPUT_VIDEO
    ]

    subprocess.run(cmd, check=True)

    print("=== VIDEO DONE ===")
    return OUTPUT_VIDEO
