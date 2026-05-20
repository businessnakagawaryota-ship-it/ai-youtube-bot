from script_engine import generate_final_script
import os

def main():
    print("=== BOT START ===")

    topic = "AI画像生成"

    script = generate_final_script(topic)

    os.makedirs("output", exist_ok=True)

    with open("output/latest_script.txt", "w", encoding="utf-8") as f:
        f.write(script)

    print(script)
    print("=== BOT END ===")

if __name__ == "__main__":
    main()
