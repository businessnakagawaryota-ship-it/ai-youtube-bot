from script_engine import generate_final_script
from buzz_engine import generate_titles
import os

def main():

    print("=== BOT START ===")

    topic = "AI画像生成"

    script = generate_final_script(topic)

    titles = generate_titles(topic)

    os.makedirs("output", exist_ok=True)

    with open("output/latest_script.txt", "w", encoding="utf-8") as f:
        f.write(script)

    with open("output/titles.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(titles))

    print(script)

    print("\n=== TITLES ===")
    for t in titles:
        print("-", t)

    print("=== BOT END ===")

if __name__ == "__main__":
    main()
