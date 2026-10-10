"""Put a generated character on the kit's 64x64 canvas: feet on a fixed baseline, centred,
optionally mirrored so the left and right halves match pixel for pixel.

usage: prep.py <src.png> <out_prefix> [--drop r,g,b]
writes <out_prefix>-raw.png, <out_prefix>-symL.png, <out_prefix>-symR.png
"""
import sys

from PIL import Image

sys.path.insert(0, __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0])
from sym import best_axis  # noqa: E402

CANVAS, FEET = 64, 61  # last opaque row of the feet


def place(im, axis_x2):
    """Paste so twice-the-axis `axis_x2` lands on the canvas centre line and feet on FEET."""
    left, top, right, bottom = im.getbbox()
    out = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    dx = round((CANVAS - axis_x2) / 2)
    out.paste(im, (dx, FEET - (bottom - 1)), im)
    return out


def mirrored(im, keep):
    w, h = im.size
    k, _ = best_axis(im)
    px = im.load()
    out = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    op = out.load()
    _, _, _, bottom = im.getbbox()
    dy = FEET - (bottom - 1)
    for y in range(h):
        if not 0 <= y + dy < CANVAS:
            continue
        for d in range(CANVAS // 2):
            sx = k - 1 - d if keep == "left" else k + d
            c = px[sx, y] if 0 <= sx < w else (0, 0, 0, 0)
            op[CANVAS // 2 - 1 - d, y + dy] = c
            op[CANVAS // 2 + d, y + dy] = c
    return out


def main():
    src, prefix = sys.argv[1], sys.argv[2]
    im = Image.open(src).convert("RGBA")
    if "--drop" in sys.argv:
        drop = tuple(int(v) for v in sys.argv[sys.argv.index("--drop") + 1].split(","))
        px = im.load()
        for y in range(im.height):
            for x in range(im.width):
                if px[x, y][:3] == drop:
                    px[x, y] = (0, 0, 0, 0)
    left, _, right, _ = im.getbbox()
    place(im, left + right).save(prefix + "-raw.png")
    mirrored(im, "left").save(prefix + "-symL.png")
    mirrored(im, "right").save(prefix + "-symR.png")
    k, bad = best_axis(im)
    print(f"{prefix}: bbox {im.getbbox()}, {bad} mismatched pixel pairs before mirroring")


main()
