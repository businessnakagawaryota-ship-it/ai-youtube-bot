from script_generator import generate_script
from image_generator import generate_images
from voice_generator import generate_voice
from video_builder import build_video
from thumbnail import make_thumbnail
from youtube_uploader import upload_video

def main():
    print("=== BOT START ===")

    script = generate_script()

    images = generate_images(script)
    audio = generate_voice(script)

    video_path = build_video(script, images, audio)
    thumb_path = make_thumbnail(script)

    upload_video(video_path, thumb_path, script["title"])

    print("=== DONE ===")

if __name__ == "__main__":
    main()
