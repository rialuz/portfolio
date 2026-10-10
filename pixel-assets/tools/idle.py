"""Idle strip built from the base sprite so nothing shimmers between frames.

Frames: rest, breathe (upper body 1px down), rest, breathe with eyes closed. The closed eyes
are the ones PixelLab drew in its idle animation; every other pixel comes from the base.

usage: idle.py <base.png> <pixellab_closed_eyes_frame.png> <out_dir>
"""
import os
import sys

from PIL import Image

SPLIT = 55                      # rows above this move; the legs stay planted
EYES = (24, 30, 40, 38)         # box around both eyes in the breathing pose (x0, y0, x1, y1)


def bob(im, dy=1):
    out = im.copy()
    top = im.crop((0, 0, im.width, SPLIT))
    out.paste((0, 0, 0, 0), (0, 0, im.width, SPLIT))
    out.alpha_composite(top, (0, dy))
    return out


def main():
    base = Image.open(sys.argv[1]).convert("RGBA")
    closed = Image.open(sys.argv[2]).convert("RGBA")
    out_dir = sys.argv[3]
    os.makedirs(out_dir, exist_ok=True)
    breathe = bob(base)
    blink = breathe.copy()
    x0, y0, x1, y1 = EYES
    n = base.width
    changed = 0
    for y in range(y0, y1):
        for x in range(x0, n // 2):          # take the left eye, mirror it onto the right
            c = closed.getpixel((x, y))
            if c != breathe.getpixel((x, y)):
                changed += 1
            blink.putpixel((x, y), c)
            blink.putpixel((n - 1 - x, y), c)
    frames = [base, breathe, base, blink]
    for i, f in enumerate(frames):
        f.save(os.path.join(out_dir, f"frame_{i:02d}.png"))
    sym = sum(1 for f in frames for y in range(n) for x in range(n // 2) if f.getpixel((x, y)) != f.getpixel((n - 1 - x, y)))
    print("idle frames:", len(frames), "eye pixels changed per side:", changed, "asymmetric pixel pairs:", sym)


main()
