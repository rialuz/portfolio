"""Lighten the skin of the waist-up portrait, and nothing else.

Skin shares some of its shading colours with the hair's highlights, so it is picked by place
as well as colour: the colours only skin uses are the seed, and the shared shading colours
count as skin only where they touch that seed inside the face, neck and hand boxes.

usage: skin.py <in.png> <out.png> [--mask mask.png]
"""
import argparse

from PIL import Image

# Only skin uses these.
SEED = {"#ffcaab", "#ed9b73", "#ea8c67", "#e17c54", "#d06d4f"}
# Skin shading that the hair also uses for its highlights.
SHARED = {"#c25e47", "#af533e", "#a85c44", "#975c49", "#925140", "#a47a6e"}
# Face and neck, left hand, right hand: x0, y0, x1, y1 inclusive.
BOXES = [(40, 26, 88, 96), (36, 128, 54, 148), (74, 128, 92, 148)]

# Old colour to new. The lit tone lands on the small sprite's skin (#f0ab7b), so the portrait
# and the walking character read as one person. Hue moves from 17 towards 22 degrees (less
# red), saturation drops and value rises; the darker the tone the less it moves, so the
# features keep their definition.
RAMP = {
    "#ffcaab": "#ffd9bf",
    "#ed9b73": "#f8c099",
    "#ea8c67": "#f1ae84",
    "#e17c54": "#e89d73",
    "#d06d4f": "#da8b64",
    "#c25e47": "#cb7a59",
    "#af533e": "#b96a4e",
    "#a85c44": "#b26a50",
    "#975c49": "#a26652",
    "#925140": "#9c5c48",
    "#a47a6e": "#b08678",
}


def hexc(p):
    return "#%02x%02x%02x" % tuple(p[:3])


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def skin_mask(im):
    px = im.load()
    w, h = im.size

    def inbox(x, y):
        return any(x0 <= x <= x1 and y0 <= y <= y1 for x0, y0, x1, y1 in BOXES)

    mask = {(x, y) for y in range(h) for x in range(w)
            if px[x, y][3] and hexc(px[x, y]) in SEED and inbox(x, y)}
    todo = list(mask)
    while todo:
        x, y = todo.pop()
        for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if n in mask or not (0 <= n[0] < w and 0 <= n[1] < h) or not inbox(*n):
                continue
            if px[n][3] and hexc(px[n]) in SHARED:
                mask.add(n)
                todo.append(n)
    return mask


def lighten(im):
    """Return a copy of the portrait with its skin moved up the ramp."""
    out = im.convert("RGBA")
    px = out.load()
    for xy in skin_mask(out):
        new = RAMP.get(hexc(px[xy]))
        if new:
            px[xy] = rgb(new) + (px[xy][3],)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--mask", help="also save a picture of which pixels count as skin")
    a = ap.parse_args()
    im = Image.open(a.src).convert("RGBA")
    mask = skin_mask(im)
    if a.mask:
        m = Image.new("RGBA", im.size, (40, 40, 40, 255))
        for y in range(im.height):
            for x in range(im.width):
                p = im.getpixel((x, y))
                if p[3]:
                    g = sum(p[:3]) // 3
                    m.putpixel((x, y), (255, 0, 255, 255) if (x, y) in mask else (g, g, g, 255))
        m.save(a.mask)
    lighten(im).save(a.out)
    print(f"skin pixels recoloured: {len(mask)}")


if __name__ == "__main__":
    main()
