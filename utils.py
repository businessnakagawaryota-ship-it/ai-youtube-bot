import os
from PIL import Image


def ensure_dirs():
    os.makedirs("assets", exist_ok=True)
    os.makedirs("output", exist_ok=True)


def create_dummy_scene():
    path = "assets/scene.jpg"

    if os.path.exists(path):
        return path

    img = Image.new("RGB", (1080, 1920), color=(20, 20, 20))

    img.save(path)

    return path
