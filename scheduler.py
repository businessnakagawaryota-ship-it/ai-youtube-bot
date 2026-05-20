from datetime import datetime

def get_mode():
    return "short" if datetime.now().hour < 12 else "detail"
