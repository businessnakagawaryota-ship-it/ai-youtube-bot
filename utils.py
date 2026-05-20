import os

def ensure_dirs():
    os.makedirs("output", exist_ok=True)
    os.makedirs("assets", exist_ok=True)
