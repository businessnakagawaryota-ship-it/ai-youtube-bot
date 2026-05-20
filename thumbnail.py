from PIL import Image, ImageDraw

def make_thumbnail(script):

    img = Image.new("RGB", (1280, 720), (30, 30, 30))
    draw = ImageDraw.Draw(img)

    draw.text((100, 300), script["title"], fill=(255,255,255))

    path = "output/thumb.jpg"
    img.save(path)

    return path
