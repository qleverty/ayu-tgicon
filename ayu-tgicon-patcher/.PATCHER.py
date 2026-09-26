import os, sys, struct
from time import sleep
import win32api, win32con

d = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))

def load(name):
    with open(os.path.join(d, name), 'rb') as f:
        return f.read()

orig_ico = load('original.ico')
orig_png = load('original.png')
over_ico = load('override.ico')
over_png = load('override.png')

if len(over_ico) != len(orig_ico) or len(over_png) != len(orig_png):
    print("override files must be exactly the same size as originals, exiting")
    sleep(3)
    sys.exit(1)

path = input("Path to AyuGram EXE: ").strip().strip('"')

with open(path, 'rb') as f:
    data = f.read()

n_ico = data.count(orig_ico)
n_png = data.count(orig_png)

if n_ico == 0 or n_png == 0:
    print("couldn't find the original icons in this exe, exiting")
    sleep(3)
    sys.exit(1)

print(f"found {n_ico} ico match(es), {n_png} png match(es), patching...")

data = data.replace(orig_ico, over_ico).replace(orig_png, over_png)

out = os.path.splitext(path)[0] + "_patched.exe"
with open(out, 'wb') as f:
    f.write(data)

_, _, count = struct.unpack('<HHH', over_ico[:6])
entries = []
off = 6
for i in range(count):
    w, h, colors, res, planes, bpp, size, offset = struct.unpack('<BBBBHHII', over_ico[off:off+16])
    entries.append((w, h, colors, planes, bpp, size, offset))
    off += 16

group = struct.pack('<HHH', 0, 1, count)
rh = win32api.BeginUpdateResource(out, False)
for icon_id, (w, h_, colors, planes, bpp, size, offset) in enumerate(entries, start=1):
    img = over_ico[offset:offset+size]
    win32api.UpdateResource(rh, win32con.RT_ICON, icon_id, img, 1033)
    group += struct.pack('<BBBBHHIH', w, h_, colors, 0, planes, bpp, size, icon_id)
win32api.UpdateResource(rh, win32con.RT_GROUP_ICON, "IDI_ICON1", group, 1033)
win32api.EndUpdateResource(rh, False)

print(f"done -> {out}")
input()
