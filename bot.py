import datetime
from utils import ensure_dirs, create_dummy_scene
from script_generator import generate_script
from voice_generator import generate_voice
from video_editor import make_video


def get_mode():
    hour = datetime.datetime.now().hour
    return "SHORT" if hour < 17 else "DETAIL"


def main():
    print("=== BOT START ===")

    ensure_dirs()

    mode = get_mode()
    print(f"MODE: {mode}")

    script = generate_script(mode)

    voice_path = generate_voice(script)

    image_path = create_dummy_scene()

    video_path = make_video(image_path, voice_path, script)

    print("=== DONE ===")
    print(video_path)


if __name__ == "__main__":
    main()
