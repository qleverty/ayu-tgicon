import os, sys, io
from PIL import Image
from time import sleep

d = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))

def load(name):
    with open(os.path.join(d, name), 'rb') as f:
        return f.read()

target_png = len(load('original.png'))
target_ico = len(load('original.ico'))
base_size = Image.open(io.BytesIO(load('original.png'))).size

path = input("PNG file: ").strip().strip('"')
img = Image.open(path).convert('RGBA').resize(base_size, Image.LANCZOS)

def fit(src, target, ico):
    for colors in (256, 128, 64, 48, 32, 24, 16, 12, 8, 6, 4, 3, 2):
        q = src if colors == 256 else src.quantize(colors=colors, method=Image.FASTOCTREE).convert('RGBA')
        buf = io.BytesIO()
        q.save(buf, format='ICO' if ico else 'PNG', optimize=not ico)
        data = buf.getvalue()
        if len(data) <= target:
            return data
    return None

png_data = fit(img, target_png, False)
ico_data = fit(img, target_ico, True)

if png_data is None or ico_data is None:
    print("couldn't squeeze the image small enough, try something else")
    sleep(3)
    sys.exit(1)

png_data += b'\x00' * (target_png - len(png_data))
ico_data += b'\x00' * (target_ico - len(ico_data))

with open(os.path.join(d, 'override.png'), 'wb') as f:
    f.write(png_data)
with open(os.path.join(d, 'override.ico'), 'wb') as f:
    f.write(ico_data)

print("done\noverride.png and override.ico are replaced, run .PATCHER.py")
input()
