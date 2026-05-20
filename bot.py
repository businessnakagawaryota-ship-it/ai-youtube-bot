from youtube_analyzer import get_trend, calculate_buzz_score
from script_generator import generate_script
from voice_generator import generate_voice
from video_editor import make_video

def main():
    print("=== BOT START ===")

    trend = get_trend()
    script = generate_script(trend)

    voice_path = generate_voice(script)
    video_path = make_video("assets/mio.jpg", voice_path)

    score = calculate_buzz_score(script)

    print("TREND:", trend)
    print("SCORE:", score)
    print("VIDEO:", video_path)

    print("=== BOT END ===")

if __name__ == "__main__":
    main()
