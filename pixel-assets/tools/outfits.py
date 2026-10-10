"""Outfits for Luz, one per scene, as stills for approval before any animation is built.

Each outfit is the approved front sprite (outfits/source/luz-base-front.png, the orange
hoodie she was first drawn in) with only her clothes repainted: head, hair, face, hands and pose are the same pixels (Summer also rests a
pair of sunglasses on her hair). An outfit is a block of rows over the body, columns 22 to 41
and rows 40 to 61 of the 64x64 frame; a dot keeps the original pixel. Every row is written
symmetric about the sprite's centre line.

approved() gives the stills Luz chose; wardrobe.py dresses every animation from them.
Run on its own, this writes the sheet preview/outfits-approved.png.

usage: outfits.py <pixel-assets dir> <sprites dir>
"""
import math
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tone  # noqa: E402

X0, Y0 = 22, 40          # where the outfit rows start in the 64x64 frame
# bare skin an outfit draws (lit, shade, deep shade), then the outline and her hair's two darks
SKIN = {"E": tone.LIT, "L": tone.SHADE, "H": tone.DEEP, "A": "#000000", "D": "#211412", "B": "#3a211a"}


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (255,)


def out_from_centre(x):
    """Whole pixels from the sprite's centre line: the same on both sides, so patterns mirror."""
    return int(abs(x - 31.5))


def dress(base, rows, key, pattern=None):
    """Paint the rows over the body. A letter in `pattern` is filled by its function of
    (column, row) instead of one colour."""
    out = base.copy()
    px = out.load()
    for j, row in enumerate(rows):
        assert len(row) == 20, (j, len(row), row)
        for i, ch in enumerate(row):
            if ch == ".":
                continue
            x, y = X0 + i, Y0 + j
            px[x, y] = rgb(pattern[ch](x, y) if pattern and ch in pattern else {**SKIN, **key}[ch])
    return out


def recolour(base, table, box):
    """Swap colours inside box (x0, y0, x1, y1 inclusive), leaving everything else alone."""
    out = base.copy()
    px = out.load()
    swap = {rgb(a)[:3]: rgb(b) for a, b in table.items()}
    for y in range(box[1], box[3] + 1):
        for x in range(box[0], box[2] + 1):
            if px[x, y][3] and px[x, y][:3] in swap:
                px[x, y] = swap[px[x, y][:3]]
    return out


def stamp(im, rows, x0, y0, key):
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch != ".":
                im.putpixel((x0 + i, y0 + j), rgb(key[ch]))


# The hoodie's orange ramp, darkest to lightest. Each hoodie below is this ramp in new colours.
ORANGE = ["#5d130e", "#791123", "#831521", "#91191b", "#9c1e1a", "#a4231a", "#d53b12", "#d84112",
          "#e54e09", "#ed5708", "#f05e08", "#f16108", "#f26509"]

# ---------------------------------------------------------------- Candy land: white hoodie, red hood

WHITE = ["#a797aa", "#b9aabb", "#c4b6c3", "#cbbdc9", "#d2c5cf", "#d9cdd6", "#f1ebee", "#f4eff1",
         "#f8f5f6", "#fbf9fa", "#ffffff", "#ffffff", "#ffffff"]
RED = ["#7a1223", "#8f1729", "#971a2c", "#a01c2e", "#a81d30", "#b01f33", "#d92b3f", "#dd3145",
       "#e53b4e", "#ea4355", "#ef4a5c", "#ef4a5c", "#f25565"]


def peppermint(im, x0, y0, size=6):
    """A round red and white sweet on the chest, where the jack-o'-lantern was."""
    c = (size - 1) / 2
    for j in range(size):
        for i in range(size):
            r = math.hypot(i - c, j - c)
            if r > size / 2 + 0.2:
                continue
            # the angle is taken from the centre line outward, so the two halves mirror
            wedge = int((math.atan2(j - c, abs(i - c)) + math.pi) / (math.pi / 4)) % 2
            im.putpixel((x0 + i, y0 + j), rgb("#d92b3f" if r > size / 2 - 0.9 or wedge else "#ffffff"))


def candy(base):
    out = recolour(base, dict(zip(ORANGE, WHITE)), (22, 43, 41, 52))
    out = recolour(out, dict(zip(ORANGE, RED)), (22, 40, 41, 42))          # the hood
    px = out.load()
    for x in (24, 25, 38, 39):                                             # red cuffs
        px[x, 49] = rgb("#d92b3f")
    for x in range(27, 37):                                                # and a red hem
        px[x, 52] = rgb("#b01f33")
    for y in range(43, 49):                                                # clear the old print
        for x in range(29, 35):
            px[x, y] = rgb("#ffffff")
    peppermint(out, 29, 43)
    return out


# ---------------------------------------------------------------- Valentine's: pink hoodie, candy hearts

PINK = ["#7a1f4a", "#8a2752", "#93305a", "#a03a66", "#ab4270", "#b84d7c", "#e86fa3", "#ea74a6",
        "#f081b0", "#f48ab6", "#f790ba", "#f993bc", "#fb97bf"]
# Four candy hearts, each its own colour, over columns 28 to 35 and rows 43 to 48.
CANDY_HEARTS = ["y.y..g.g", "yyy..ggg", ".y....g.", "b.b..w.w", "bbb..www", ".b....w."]


def valentines(base):
    out = recolour(base, dict(zip(ORANGE, PINK)), (22, 40, 41, 52))
    stamp(out, [r.replace(".", "p") for r in CANDY_HEARTS], 28, 43,
          {"g": "#7fe0c3", "y": "#ffe066", "b": "#8fd3f4", "w": "#ffffff", "p": "#f790ba"})
    return out


# ---------------------------------------------------------------- Easter: blue and white dress

EASTER = [
    "....DBD......DBD....",   # 40  no hood: her hair falls where it sat
    "....AppWW..WWppA....",   # 41  puff sleeves and a white collar
    "...ppppWWWWWWpppp...",   # 42
    "...ttnppppppppntt...",   # 43  sleeve hems
    "..AELHppppppppHLEA..",   # 44  bodice
    ".AEELHppppppppHLEEA.",   # 45
    ".AEELHttttttttHLEEA.",   # 46  waistband
    ".AEELppppppppppLEEA.",   # 47  the skirt flares
    ".AELppppppppppppLEA.",   # 48
    ".AELppppppppppppLEA.",   # 49
    "....pppppppppppp....",   # 50
    "....pppppppppppp....",   # 51
    "...AppppppppppppA...",   # 52
    "...AppppppppppppA...",   # 53
    "...AwwwwwwwwwwwwA...",   # 54  a white hem
    "....AAAELAALEAAA....",   # 55  a little leg
    "......AWwAAwWA......",   # 56  white boots
    "......AWwAAwWA......",   # 57
    "......AWwAAwWA......",   # 58
    ".....AWWwAAwWWA.....",   # 59
    ".....AwwwAAwwwA.....",   # 60
    "....................",   # 61
]
EASTER_KEY = {"t": "#4f7ad6", "n": "#2f4a8f", "W": "#ffffff", "w": "#d6e2f7"}
BLUE, PALE = "#6f9df2", "#b9d2fa"


def polka(x, y):
    """White dots on blue, staggered row to row."""
    d = out_from_centre(x)
    return "#ffffff" if (y % 4 == 0 and d % 4 == 1) or (y % 4 == 2 and d % 4 == 3) else BLUE


def polka_on_white(x, y):
    d = out_from_centre(x)
    return BLUE if (y % 4 == 0 and d % 4 == 1) or (y % 4 == 2 and d % 4 == 3) else "#ffffff"


def gingham(x, y):
    """Two-pixel checks: blue where the bands cross, pale where one runs, white between."""
    return ("#ffffff", PALE, PALE, BLUE)[(out_from_centre(x) // 2 % 2) * 2 + (y // 2 % 2)]


# ---------------------------------------------------------------- Summer: ruffle top, shorts, shades

SUMMER = [
    "....DBD......DBD....",   # 40
    "....AEYEE..EEYEA....",   # 41  shoulders and two thin straps
    "...rrrrrrrrrrrrrr...",   # 42  the ruffle, wide over her shoulders
    "...rrrrrrrrrrrrrr...",   # 43
    "...hhhhhhhhhhhhhh...",   # 44  its scalloped edge
    ".AEELHYYYYYYYYHLEEA.",   # 45  the body of the top, bare arms beside it
    ".AEELHYYYYYYYYHLEEA.",   # 46
    ".AEELHYYYYYYYYHLEEA.",   # 47
    ".AEELHYYYYYYYYHLEEA.",   # 48
    ".AELAhhhhhhhhhhALEA.",   # 49  a second ruffle at the hem
    "....ASSSSSSSSSSA....",   # 50  shorts
    "....AsSSSSSSSSsA....",   # 51
    "....AsSSSSSSSSsA....",   # 52
    ".....ASSSAASSSA.....",   # 53
    ".....AsssAAsssA.....",   # 54
    ".....AEELAALEEA.....",   # 55  bare legs
    "......AELAALEA......",   # 56
    "....................",   # 57
    "......AUUAAUUA......",   # 58  blue shoes
    ".....AuUuAAuUuA.....",   # 59
    ".....AWWWAAWWWA.....",   # 60  white soles
    "....................",   # 61
]
YELLOW, YELLOW_LIGHT, YELLOW_SHADE = "#ffd23f", "#ffe98a", "#d9a21b"
SUMMER_KEY = {"Y": YELLOW, "S": "#3d7bd9", "s": "#2a56a6", "U": "#3d7bd9", "u": "#8db8f2", "W": "#f4f7ff"}
SUMMER_PATTERN = {
    "r": lambda x, y: YELLOW_LIGHT if out_from_centre(x) % 2 else YELLOW,     # folds
    "h": lambda x, y: YELLOW_SHADE if out_from_centre(x) % 2 else YELLOW,     # a scalloped edge
}
# Sunglasses pushed up on her hair: columns 24 to 39, rows 20 to 23.
SHADES = [
    ".WWWWWW..WWWWWW.",
    "WNNgNNWWWWNNgNNW",
    "WNNNNNW..WNNNNNW",
    ".WWWWW....WWWWW.",
]


def summer(base):
    out = dress(base, SUMMER, SUMMER_KEY, SUMMER_PATTERN)
    stamp(out, SHADES, 24, 20, {"W": "#ffffff", "N": "#23304d", "g": "#8db8f2"})
    return out


def asymmetry(im):
    """Mismatched pixel pairs across the centre line: 0 for a front view that mirrors exactly."""
    return sum(1 for y in range(64) for x in range(32) if im.getpixel((x, y)) != im.getpixel((63 - x, y)))


def approved(base):
    """The outfits Luz approved on 2026-10-09, by scene. Halloween is the sprite as it was."""
    return {
        "candy": candy(base),
        "valentines": valentines(base),
        "easter": dress(base, EASTER, EASTER_KEY, {"p": gingham}),
        "summer": summer(base),
    }


def main():
    root, sprites = sys.argv[1], sys.argv[2]
    base = Image.open(os.path.join(root, "outfits", "source", "luz-base-front.png")).convert("RGBA")
    looks = approved(base)
    for name, im in looks.items():
        print(f"{name}: asymmetric pixel pairs {asymmetry(im)} (the Halloween sprite has {asymmetry(base)})")

    # the sheet: each look large on the page colour, then at her size on the site in its own scene,
    # with her skin in the tone she chose, as wardrobe.py leaves it
    looks = {name: tone.fair(im, base) for name, im in looks.items()}
    base = tone.fair(base.copy(), base)
    Z = 8
    order = [
        ("Halloween", base, "halloween"),
        ("Candy land", looks["candy"], None),
        ("Valentine's Day", looks["valentines"], "valentines"),
        ("Easter", looks["easter"], "easter"),
        ("Summer", looks["summer"], "summer"),
    ]
    cell = 40 * Z
    sheet = Image.new("RGBA", (cell * len(order) + 20, 48 * Z + 320), (255, 247, 238, 255))
    pen = ImageDraw.Draw(sheet)
    for i, (label, im, scene) in enumerate(order):
        crop = im.crop((12, 16, 52, 64))
        sheet.alpha_composite(crop.resize((40 * Z, 48 * Z), Image.NEAREST), (10 + i * cell, 0))
        bg_path = os.path.join(sprites, "seasons", scene, "bg-hero.png") if scene else os.path.join(sprites, "bg-hero.png")
        bg = Image.open(bg_path).convert("RGBA").crop((143, 112, 233, 180)).resize((360, 272), Image.NEAREST)
        bg.alpha_composite(im.resize((192, 192), Image.NEAREST), ((188 - 143) * 4 - 96, (173 - 112) * 4 - 186))
        sheet.alpha_composite(bg.crop((0, 0, cell - 20, 272)), (20 + i * cell, 48 * Z + 14))
        pen.text((24 + i * cell, 48 * Z + 292), label, fill=(35, 48, 77, 255))
    sheet.save(os.path.join(root, "preview", "outfits-approved.png"))


if __name__ == "__main__":
    main()
