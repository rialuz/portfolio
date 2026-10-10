"""The waist-up portrait in each scene's outfit.

The portrait Luz approved (outfits/source/luz-portrait.png: the orange hoodie) is the source.
Only what she wears is changed, and every version is given the skin tone she asked for
(fair() below).

- halloween is the source itself; candy and valentines are recolours of its hoodie with a new
  chest print. Their faces and hair are the source's pixels.
- easter and summer need different clothes. PixelLab's Pro generator drew them with the
  source as its reference (reference.py; the picks are outfits/<name>/raw/portrait-pro), so
  they are the same face and hair redrawn, not the same pixels.

usage: portraits.py <pixel-assets dir>
"""
import math
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import outfits  # noqa: E402
import season_fx as fx  # noqa: E402
from tone import FAIR  # noqa: E402
from wardrobe import hsv, luminance, rgb  # noqa: E402

CLEAR = (0, 0, 0, 0)

# ---------------------------------------------------------------- her skin tone

# The tone and its ramp are in tone.py. These are where her skin is in the portrait.
FACE = (38, 24, 90, 98)
HANDS = [(34, 126, 56, 150), (72, 126, 94, 150)]          # in the hoodie's pocket
BODY = [(6, 82, 122, 168)]                                # bare arms and shoulders


def skin_like(p):
    if not p[3]:
        return False
    h, s, v = hsv(p)
    return 8 <= h <= 40 and 0.2 < s < 0.7 and v >= 0.55


def fair(im, boxes):
    """Her skin in the tone she chose, and nothing else changed.

    Skin's lighter tones are its own: any warm pixel that bright, inside the boxes, is skin.
    Its darker shading shares colours with the lights in her hair, so a darker pixel counts
    only where it lies within two pixels of a lighter skin pixel."""
    out = im.copy()
    px, sp = out.load(), im.load()
    w, h = im.size

    def inside(x, y):
        return any(x0 <= x <= x1 and y0 <= y <= y1 for x0, y0, x1, y1 in boxes)

    light = {(x, y) for y in range(h) for x in range(w) if inside(x, y) and skin_like(sp[x, y]) and hsv(sp[x, y])[2] >= 0.7}
    skin = set(light)
    for x in range(w):
        for y in range(h):
            if (x, y) in skin or not inside(x, y) or not skin_like(sp[x, y]):
                continue
            if any((x + dx, y + dy) in light for dx in range(-2, 3) for dy in range(-2, 3)):
                skin.add((x, y))
    for x, y in skin:
        v = hsv(sp[x, y])[2]
        px[x, y] = rgb(next(colour for floor, colour in FAIR if v >= floor))
    return out


# ---------------------------------------------------------------- the hoodie

def warm(p):
    """Hoodie orange, or the dark red of its folds."""
    if not p[3]:
        return False
    h, s, v = hsv(p)
    return (h <= 40 or h >= 345) and s > 0.72 and v > 0.3


def hoodie_mask(im):
    """Every hoodie pixel: the warm pixels joined to her chest. The rim light on her hair and
    the reds of her face are the same hues but stand apart, so they are left out."""
    px = im.load()
    w, h = im.size
    todo = [(x, y) for y in range(90, 164) for x in range(30, 98) if warm(px[x, y])]
    mask = set(todo)
    while todo:
        x, y = todo.pop()
        for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if n not in mask and 0 <= n[0] < w and 68 <= n[1] < h and warm(px[n]):
                mask.add(n)
                todo.append(n)
    # a few fold shadows touch the hoodie only at a corner; left out they would stay red
    corners = {(x, y) for y in range(68, h) for x in range(w) if (x, y) not in mask and warm(px[x, y])
               and any((x + dx, y + dy) in mask for dx in (-1, 1) for dy in (-1, 1))}
    return mask | corners


CHEST = rgb("#da4308")                               # the flat orange of the chest


def on_string(x, y):
    """The two drawstrings hang from the collar to row 109: three pixels of cord with a pixel
    of shadow each side, and a wider tip. The jack-o'-lantern's eyes are drawn right against
    them, so the two are told apart by place."""
    if y <= 105:
        return 55 <= x <= 59 or 67 <= x <= 71
    return y <= 109 and (55 <= x <= 58 or 68 <= x <= 71)


def print_pixels(im):
    """The jack-o'-lantern on her chest: its black shapes and every darker pixel that edges
    them, and none of the drawstrings."""
    px = im.load()
    box = [(x, y) for y in range(97, 126) for x in range(44, 87) if px[x, y][3] and not on_string(x, y)]
    black = {p for p in box if hsv(px[p])[2] < 0.2}
    edge = {(x, y) for x, y in box if luminance(px[x, y]) < luminance(CHEST) - 6
            and any((x + dx, y + dy) in black for dx in (-1, 0, 1) for dy in (-1, 0, 1))}
    return black | edge


def plain(im):
    """The orange hoodie with its jack-o'-lantern taken off. The eyes covered the outer shadow
    of each drawstring for a few rows; that is put back from the rows above."""
    out = im.copy()
    px = out.load()
    for p in print_pixels(im):
        px[p] = CHEST
    for x, rows in ((55, range(99, 106)), (71, range(100, 106))):
        for y in rows:
            px[x, y] = px[x, 97]
    return out


def shade(p, colours, low, high):
    """This hoodie pixel's place between its darkest and lightest, on another ramp."""
    t = (luminance(p) - low) / max(1, high - low)
    return rgb(colours[min(len(colours) - 1, max(0, round(t * (len(colours) - 1))))])


def recoloured(im, colours, hood=None):
    """The hoodie in a new ramp, its print gone. `hood` is a second ramp for the hood round
    her neck."""
    out = plain(im)
    px = out.load()
    mask = hoodie_mask(im)
    lums = [luminance(im.getpixel(p)) for p in mask]
    low, high = min(lums), max(lums)
    # the print was black, so it is not in the mask: it is cloth now, wherever plain() changed it
    cloth = mask | {(x, y) for y in range(im.height) for x in range(im.width) if px[x, y] != im.getpixel((x, y))}
    for x, y in cloth:
        in_hood = hood and y <= 91 and 38 <= x <= 90
        px[x, y] = shade(px[x, y], hood if in_hood else colours, low, high)
    return out, mask


def valentines(im):
    """Pink, with four candy hearts, each its own colour: a pair either side of the
    drawstrings, a pixel clear of them, mirrored about the line between the strings."""
    out, _ = recoloured(im, outfits.PINK)
    hearts = (("#ffe066", "#d9a21b", 43, 98), ("#7fe0c3", "#3fae8e", 73, 98),
              ("#8fd3f4", "#4f9fd0", 43, 112), ("#ffffff", "#d9c7d6", 73, 112))
    for colour, edge, x, y in hearts:
        out.alpha_composite(fx.outlined(fx.bitmap(fx.HEARTS[11], {"X": colour}), rgb(edge)), (x, y))
    return out


def candy(im):
    out, mask = recoloured(im, outfits.WHITE, hood=outfits.RED)
    px = out.load()
    bottom = max(y for _, y in mask)
    for x, y in mask:                               # a red hem
        if y >= bottom - 4:
            px[x, y] = rgb(outfits.RED[6] if y > bottom - 4 else outfits.RED[3])
    wrapped_mint(out)
    return out


# One end of the sweet's wrapper, from the mint outward; the other end is its mirror.
TWIST = [
    ".......X",
    "......XX",
    "....XXoX",
    "...XoooX",
    ".XXooooX",
    "XrrrrooX",
    ".XXooooX",
    "...XoooX",
    "....XXoX",
    "......XX",
    ".......X",
]


def wrapped_mint(im, cx=63, cy=119, r=9.5):
    """The sweet on the candy hoodie: a wrapped peppermint below the drawstrings, centred on
    the line between them and mirrored about it.

    A white mint with twelve thin stripes, six red and six white, meeting at a white middle,
    and a twist of wrapper at each side. (A first try with a few broad wedges on a red disc
    read as a hazard sign. Many thin stripes on white, and the wrapper, say sweet.)"""
    px = im.load()
    red, edge, white = rgb("#d92b3f"), rgb("#8f1729"), rgb("#ffffff")
    key = {"X": edge, "o": rgb("#fbd3db"), "r": red}
    reach = int(r) + 1
    for j, row in enumerate(TWIST):
        for i, ch in enumerate(row):
            if ch != ".":
                for side in (-1, 1):
                    px[cx + side * (reach + i), cy - len(TWIST) // 2 + j] = key[ch]
    for y in range(cy - reach, cy + reach + 1):
        for x in range(cx - reach, cx + reach + 1):
            d = math.hypot(x - cx, y - cy)
            if d > r:
                continue
            # twelve stripes of 30 degrees; a red one points straight up, so the halves mirror
            stripe = int((math.degrees(math.atan2(cy - y, x - cx)) - 75) % 360 // 30) % 2 == 0
            px[x, y] = edge if d > r - 1.1 else white if d < 2.4 or not stripe else red


def main():
    root = sys.argv[1]
    source = Image.open(os.path.join(root, "outfits", "source", "luz-portrait.png")).convert("RGBA")
    made = {"halloween": source, "candy": candy(source), "valentines": valentines(source)}
    for name in ("easter", "summer"):
        made[name] = Image.open(os.path.join(root, "outfits", name, "raw", "portrait-pro", "frame_00.png")).convert("RGBA")
    for name, im in made.items():
        boxes = [FACE] + (BODY if name in ("easter", "summer") else HANDS)
        folder = os.path.join(root, "outfits", name)
        os.makedirs(folder, exist_ok=True)
        fair(im, boxes).save(os.path.join(folder, "luz-portrait.png"))
        print(name, "portrait")


if __name__ == "__main__":
    main()
