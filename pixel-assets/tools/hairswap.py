"""Option C's face and outfit with option A's hair shape, recoloured from plum to brown.

Both inputs are the mirrored 64x64 sprites, centred on the same axis, so the result stays
symmetric. usage: hairswap.py <c.png> <a.png> <out.png>
"""
import colorsys
import sys

from PIL import Image

# brown ramp, darkest to lightest; the mid and highlight tones are option C's own hair colours
BROWNS = [(0, 0, 0), (33, 20, 18), (58, 33, 26), (94, 50, 36), (132, 72, 50), (168, 92, 68)]
LEVELS = [10, 31, 55, 90, 125]  # luminance cut-offs between the ramp steps

# option C: columns (inclusive) kept per row
FACE = {26: (30, 33), 27: (29, 34), 28: (29, 34), 29: (28, 35), 30: (28, 35), 31: (27, 36),
        32: (25, 38), 33: (24, 39), 34: (24, 39), 35: (24, 39), 36: (25, 38), 37: (25, 38),
        38: (26, 37), 39: (28, 35)}
BODY = {40: (25, 38), 41: (24, 39), 42: (24, 39), 43: (23, 40), 44: (22, 41), 45: (22, 41),
        46: (22, 41), 47: (22, 41), 48: (22, 41), 49: (23, 40), 50: (22, 41), 51: (22, 41),
        52: (23, 40)}
HAIR_LAST_ROW = 48  # option A's hair ends here; below it only A's body remains


def lum(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]


def brown(c):
    return BROWNS[sum(lum(c) > t for t in LEVELS)] + (255,)


def is_hair(c):
    """Option A's hair is black or plum; its skin, hoodie and eye whites are not."""
    h, s, v = colorsys.rgb_to_hsv(*(k / 255 for k in c[:3]))
    return v < 0.13 or 250 <= h * 360 <= 345


def main():
    c = Image.open(sys.argv[1]).convert("RGBA")
    a = Image.open(sys.argv[2]).convert("RGBA")
    cp, ap = c.load(), a.load()
    n = c.width

    keep = set()
    for y, (x0, x1) in FACE.items():
        keep.update((x, y) for x in range(x0, x1 + 1))
    # one-pixel ring around the face, so C's own dark edge sits between skin and the new hair
    keep |= {(x + dx, y + dy) for x, y in keep for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
    for y, (x0, x1) in BODY.items():
        keep.update((x, y) for x in range(x0, x1 + 1))
    keep.update((x, y) for y in range(53, n) for x in range(n))

    out = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    op = out.load()
    for y in range(HAIR_LAST_ROW + 1):
        for x in range(n):
            p = ap[x, y]
            if p[3]:
                # leftovers of A's face and ears become a dark hair tone
                op[x, y] = brown(p) if is_hair(p) else BROWNS[2] + (255,)
    for x, y in keep:
        if 0 <= x < n and 0 <= y < n and cp[x, y][3]:
            p = cp[x, y]
            h, s, v = colorsys.rgb_to_hsv(*(k / 255 for k in p[:3]))
            ring_plum = y < 40 and 280 <= h * 360 <= 345 and v < 0.3  # C's plum-dark hair edge
            op[x, y] = BROWNS[1] + (255,) if ring_plum else p
    out.save(sys.argv[3])

    bad = sum(1 for y in range(n) for x in range(n // 2) if op[x, y] != op[n - 1 - x, y])
    print("saved", sys.argv[3], "bbox", out.getbbox(), "asymmetric pixel pairs:", bad)


main()
