"""Moving parts of the environment.

- Lifts the three sky clouds out of the hero background into their own sprites and repaints
  the sky behind them, so the site can drift them.
- Turns the flag prop into a 4-frame waving strip by rippling the cloth along the pole.

usage: env.py <raw bg-hero.png> <raw prop-flag.png> <out_dir>
"""
import math
import os
import sys
from collections import Counter

from PIL import Image

SKY = {(251, 209, 227), (252, 222, 238), (253, 214, 233), (252, 229, 238)}
CLOUD_BOXES = [(33, 22, 71, 39), (221, 25, 287, 55), (81, 53, 141, 79)]  # found by blob search


def clouds(bg_path, out_dir):
    bg = Image.open(bg_path).convert("RGBA")
    px = bg.load()
    w, _ = bg.size
    for i, (x0, y0, x1, y1) in enumerate(CLOUD_BOXES, 1):
        x0, y0, x1, y1 = x0 - 2, y0 - 2, x1 + 2, y1 + 2
        cloud = Image.new("RGBA", (x1 - x0 + 1, y1 - y0 + 1), (0, 0, 0, 0))
        moved = 0
        for y in range(y0, y1 + 1):
            row_sky = Counter(px[x, y][:3] for x in range(w) if px[x, y][:3] in SKY).most_common(1)[0][0]
            for x in range(x0, x1 + 1):
                if px[x, y][:3] not in SKY:
                    cloud.putpixel((x - x0, y - y0), px[x, y])
                    px[x, y] = row_sky + (255,)
                    moved += 1
        box = cloud.getbbox()
        cloud = cloud.crop(box)
        cloud.save(os.path.join(out_dir, f"bg-cloud-{i}.png"))
        print(f"bg-cloud-{i}.png {cloud.size}, {moved} pixels, was at x={x0 + box[0]} y={y0 + box[1]} in the background")
    bg.save(os.path.join(out_dir, "bg-hero.png"))


def flag(flag_path, out_dir, frames=4):
    src = Image.open(flag_path).convert("RGBA")
    n = src.width
    pole_x = 19                      # cloth is everything left of the pole, from row 4 down
    strip = Image.new("RGBA", (n * frames, n), (0, 0, 0, 0))
    for t in range(frames):
        frame = Image.new("RGBA", (n, n), (0, 0, 0, 0))
        for y in range(n):           # pole and finial stay put
            for x in range(n):
                if x >= pole_x or y < 4:
                    frame.putpixel((x, y), src.getpixel((x, y)))
        prev = 0
        for x in range(pole_x - 1, -1, -1):
            d = pole_x - 1 - x       # distance from the pole; the ripple grows toward the free end
            amp = min(1.0, max(0.0, (d - 1) / 2))   # a one-pixel ripple keeps the outline intact
            off = round(amp * math.sin(2 * math.pi * (d / 16 - t / frames)))
            off = max(prev - 1, min(prev + 1, off))   # neighbouring columns never tear apart
            prev = off
            for y in range(4, n):
                p = src.getpixel((x, y))
                if p[3] and 0 <= y + off < n:
                    frame.putpixel((x, y + off), p)
        strip.paste(frame, (t * n, 0))
    strip.save(os.path.join(out_dir, "prop-flag.png"))
    print("prop-flag.png", strip.size, f"{frames} frames")


if __name__ == "__main__":
    os.makedirs(sys.argv[3], exist_ok=True)
    clouds(sys.argv[1], sys.argv[3])
    flag(sys.argv[2], sys.argv[3])
