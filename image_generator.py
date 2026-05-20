import requests
import os

def generate_images(script):
    os.makedirs("output/images", exist_ok=True)

    images = []

    for i, s in enumerate(script["scenes"]):

        if s["speaker"] == "mio":
            prompt = "anime girl japanese, cafe, soft smile, cinematic light"
        else:
            prompt = "anime boy japanese, surprised expression, cafe"

        url = f"https://image.pollinations.ai/prompt/{prompt}"

        r = requests.get(url)

        path = f"output/images/{i}.jpg"

        with open(path, "wb") as f:
            f.write(r.content)

        images.append(path)

    return images
