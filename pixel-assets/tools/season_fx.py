"""Seasonal kits: props and the moving pieces.

Two kinds of piece are made here.

- From PixelLab stills (raw/*.png): cleaned of their drop shadow, seated on the bottom row of
  the frame, and, for the creatures, animated by moving whole columns or rows of pixels, so
  every frame keeps the still's exact pixels (the way the flag and the wave were built).
- Drawn in code: the small things that have to be exact or tiny (eggs, hearts, the arrow, the
  butterfly, the dolphin's leap) and the sea, which is cut from the painting itself.

Every strip is horizontal, one frame per cell, like the rest of the kit.
"""
import colorsys
import math
from collections import Counter

from PIL import Image

NAVY = (0x23, 0x30, 0x4D, 255)
WHITE = (255, 255, 255, 255)
CLEAR = (0, 0, 0, 0)


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


def mix(a, b, t):
    return tuple(round(x + (y - x) * t) for x, y in zip(a[:3], b[:3])) + (255,)


def strip(frames):
    w, h = frames[0].size
    assert all(f.size == (w, h) for f in frames)
    out = Image.new("RGBA", (w * len(frames), h), CLEAR)
    for i, f in enumerate(frames):
        out.paste(f, (i * w, 0))
    return out


def shifted(im, dx=0, dy=0):
    out = Image.new("RGBA", im.size, CLEAR)
    out.paste(im, (dx, dy), im)
    return out


# ---------------------------------------------------------------- cleaning PixelLab stills

def drop_shadow(im):
    """PixelLab sets some items on a soft blob of shadow. Remove it and nothing else.

    A shadow pixel is dull, sits in the bottom five rows, and has no dark outline under it in
    its column (a sand mound or a glass foot is closed off by its outline; a shadow is not).
    It goes if its colour lives almost only there, or if it is a stray hanging directly under
    the outline. Pixels of a shadow colour that touch a removed one go with it."""
    out = im.copy()
    px = out.load()
    w, h = out.size

    def tone(p):
        _, s, v = colorsys.rgb_to_hsv(*(c / 255 for c in p[:3]))
        return s, v

    def dull(p):
        s, v = tone(p)
        return s < 0.45 and 0.36 < v < 0.9

    def dark(p):
        return p[3] and tone(p)[1] < 0.36

    removed = 0
    seen = set()
    floor = out.getbbox()[3] if out.getbbox() else 0
    for _ in range(4):
        box = out.getbbox()
        if not box:
            break
        low_rows = range(max(0, box[3] - 5), box[3])
        everywhere = Counter(px[x, y][:3] for y in range(h) for x in range(w) if px[x, y][3])
        is_open = {(x, y) for x in range(w) for y in low_rows
                   if px[x, y][3] and dull(px[x, y]) and not any(dark(px[x, yy]) for yy in range(y + 1, h))}
        low = Counter(px[p][:3] for p in is_open)
        # six or more: two grey pixels under a bat are its claws, not a shadow
        shadow = {c for c, k in low.items() if k >= 6 and k >= 0.75 * everywhere[c]}
        gone = {p for p in is_open if px[p][:3] in shadow}
        for x in range(w):                         # strays: the lowest pixel of a column, right under the outline
            ys = [y for y in range(h) if px[x, y][3]]
            if len(ys) > 1 and (x, ys[-1]) in is_open and dark(px[x, ys[-1] - 1]):
                gone.add((x, ys[-1]))
        todo = list(gone)                          # shadow-coloured pixels touching a removed one
        while todo:
            x, y = todo.pop()
            for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if n not in gone and 0 <= n[0] < w and n[1] in low_rows and px[n][3] and px[n][:3] in shadow:
                    gone.add(n)
                    todo.append(n)
        if not gone:
            break
        seen |= shadow
        for p in gone:
            px[p] = CLEAR
        removed += len(gone)
    # flecks of a shadow colour left at the edge, where a leg or a paw stood on the shadow
    again = True
    while again:
        again = False
        for y in range(max(0, floor - 6), floor):
            for x in range(w):
                if px[x, y][3] and px[x, y][:3] in seen and any(
                        not (0 <= nx < w and 0 <= ny < h) or not px[nx, ny][3]
                        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))):
                    px[x, y] = CLEAR
                    removed += 1
                    again = True
    # a fleck of shadow colour floating on its own, wherever it is
    for y in range(h):
        for x in range(w):
            if px[x, y][3] and px[x, y][:3] in seen and not any(
                    0 <= x + dx < w and 0 <= y + dy < h and px[x + dx, y + dy][3]
                    for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy):
                px[x, y] = CLEAR
                removed += 1
    # a single dull pixel left on its own under the drawing
    box = out.getbbox()
    if box:
        for y in range(max(0, box[3] - 6), box[3]):
            for x in range(w):
                if px[x, y][3] and dull(px[x, y]) and not any(
                        0 <= x + dx < w and 0 <= y + dy < h and px[x + dx, y + dy][3]
                        for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy):
                    px[x, y] = CLEAR
                    removed += 1
    return out, removed


def seat(im, w=None, h=None):
    """Centre the drawing and rest it on the bottom row of a w x h frame."""
    w, h = w or im.width, h or im.height
    box = im.getbbox()
    cut = im.crop(box)
    out = Image.new("RGBA", (w, h), CLEAR)
    out.paste(cut, ((w - cut.width) // 2, h - cut.height), cut)
    return out


def mirrored(im):
    """Copy the left half onto the right about the drawing's own centre line."""
    left, _, right, _ = im.getbbox()
    out = im.copy()
    px = out.load()
    total = left + right - 1                      # x + mirror(x)
    for y in range(out.height):
        for x in range(left, (total + 1) // 2 + (1 if total % 2 == 0 else 0)):
            m = total - x
            if 0 <= m < out.width:
                px[m, y] = px[x, y]
    return out


def prop(raw, w=None, h=None, symmetric=False):
    im, removed = drop_shadow(raw.convert("RGBA"))
    if symmetric:
        im = mirrored(im)
    return seat(im, w, h), removed


def mirror_below(im, top):
    """Copy the left half onto the right from row `top` down, about those rows' own centre
    line. For the jack-o'-lantern: the face and body become exactly symmetric, and the stem,
    which leans, is left as it grew."""
    out = im.copy()
    px = out.load()
    body = out.crop((0, top, out.width, out.height)).getbbox()
    total = body[0] + body[2] - 1                 # x + mirror(x)
    for y in range(top, out.height):
        for x in range(body[0], (total + 1) // 2):
            px[total - x, y] = px[x, y]
    return out


def bitmap(rows, key):
    w = len(rows[0])
    assert all(len(r) == w for r in rows), [len(r) for r in rows]
    im = Image.new("RGBA", (w, len(rows)), CLEAR)
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != ".":
                im.putpixel((x, y), rgb(key[ch]))
    return im


def small_pumpkin():
    """A small jack-o'-lantern for the background, in the lit pumpkin's colours and as
    symmetric: 17 wide, 16 tall."""
    rows = [
        ".......NNN.......",
        ".......NGN.......",
        "....NNNNGNNNN....",
        "..NNOOOOOOOOONN..",
        ".NOLLOOOOOOOLLON.",
        ".NOLOOOOOOOOOLON.",
        "NOOOYYOOOOOYYOOON",
        "NOOOYYOOYOOYYOOON",
        "NOOOOOOYYYOOOOOON",
        "NOOYOOOOOOOOOYOON",
        "NOOYYYOYYYOYYYOON",
        "NDOOYYYYYYYYYOODN",
        ".NDOOOYYYYYOOODN.",
        ".NDDOOOOOOOOODDN.",
        "..NNDDDDDDDDDNN..",
        "....NNNNNNNNN....",
    ]
    return bitmap(rows, {"N": "#652a17", "O": "#eb7727", "L": "#f69848", "D": "#b84d20", "Y": "#f9f751", "G": "#3b591a"})


def present(box, lid, ribbon, small=False):
    """A wrapped present for the background: box, lid, a ribbon down the middle and a bow."""
    rows = [
        "..NN...NN..",
        ".NRRN.NRRN.",
        "..NRRNRRN..",
        "NNNNNRNNNNN",
        "NWWWWRWWWWN",
        "NNNNNRNNNNN",
        ".NBBBRBBBN.",
        ".NBBBRBBBN.",
        ".NBBBRBBBN.",
        ".NBBBRBBBN.",
        ".NNNNNNNNN.",
    ] if small else [
        "...NN.....NN...",
        "..NRRN...NRRN..",
        "..NRRRN.NRRRN..",
        "...NRRRNRRRN...",
        "....NNRRRNN....",
        ".NNNNNNRNNNNNN.",
        ".NWWWWWRWWWWWN.",
        ".NNNNNNRNNNNNN.",
        "..NBBBBRBBBBN..",
        "..NBBBBRBBBBN..",
        "..NBBBBRBBBBN..",
        "..NBBBBRBBBBN..",
        "..NBBBBRBBBBN..",
        "..NBBBBRBBBBN..",
        "..NNNNNNNNNNN..",
    ]
    return bitmap(rows, {"N": "#6b1830", "B": box, "W": lid, "R": ribbon})


# ---------------------------------------------------------------- animating stills

def flap(im, tips=(-4, 0, 4, 0), body=5, lift=(1, 0, -1, 0)):
    """Bat: the wings swing about the shoulders. Columns move whole, further the further out
    they are, and the body rides one pixel the other way."""
    left, top, right, bottom = im.getbbox()
    axis = (left + right - 1) / 2
    reach = (right - left) / 2 - body
    px = im.load()
    frames = []
    for tip, dy in zip(tips, lift):
        f = Image.new("RGBA", im.size, CLEAR)
        fp = f.load()
        for x in range(left, right):
            d = abs(x - axis) - body
            off = dy + (round(tip * d / reach) if d > 0 else 0)
            for y in range(top, bottom):
                if px[x, y][3] and 0 <= y + off < im.height:
                    fp[x, y + off] = px[x, y]
        frames.append(f)
    return frames


def bob(im, rise=(0, -1, -2, -1), hem=4):
    """Ghost: floats up and down while the bottom hem ripples one pixel."""
    left, top, right, bottom = im.getbbox()
    px = im.load()
    frames = []
    for t, dy in enumerate(rise):
        f = Image.new("RGBA", im.size, CLEAR)
        fp = f.load()
        for x in range(left, right):
            wave = round(0.6 * math.sin(2 * math.pi * ((x - left) / 8 - t / len(rise))))
            for y in range(top, bottom):
                if not px[x, y][3]:
                    continue
                ny = y + dy + (wave if y >= bottom - hem else 0)
                if 0 <= ny < im.height:
                    fp[x, ny] = px[x, y]
        frames.append(f)
    return frames


def hop(im, steps=((0, 0), (0, 1), (-3, 0), (-5, 0), (-3, 0), (0, 1))):
    """Bunny: crouch, spring, land. A crouch drops one row from the middle of the body."""
    left, top, right, bottom = im.getbbox()
    fold = top + round((bottom - top) * 0.62)
    frames = []
    for dy, squash in steps:
        f = Image.new("RGBA", im.size, CLEAR)
        if squash:
            upper = im.crop((0, 0, im.width, fold))
            lower = im.crop((0, fold + 1, im.width, im.height))
            f.paste(upper, (0, 1), upper)
            f.paste(lower, (0, fold + 1), lower)
        else:
            f.paste(im, (0, dy), im)
        frames.append(f)
    return frames


def scuttle(im, legs=3):
    """Crab: the body dips on alternate frames, the legs step side to side under it, and each
    claw lifts in turn."""
    left, top, right, bottom = im.getbbox()
    px = im.load()
    third = (right - left) // 3
    mid = top + (bottom - top) // 2
    frames = []
    for t in range(4):
        f = Image.new("RGBA", im.size, CLEAR)
        fp = f.load()
        dip = 1 if t % 2 else 0
        step = (0, 1, 0, -1)[t]
        for y in range(top, bottom):
            for x in range(left, right):
                p = px[x, y]
                if not p[3]:
                    continue
                if y >= bottom - legs:
                    nx, ny = x + step, y
                else:
                    claw = y < mid and ((t == 1 and x < left + third) or (t == 3 and x >= right - third))
                    nx, ny = x, y + dip - (1 if claw else 0)
                if 0 <= nx < im.width and 0 <= ny < im.height:
                    fp[nx, ny] = p
        frames.append(f)
    return frames


def flicker(im):
    """Jack-o'-lantern: the candle light in its face brightens and dims."""
    def lit(p):
        h, s, v = colorsys.rgb_to_hsv(*(c / 255 for c in p[:3]))
        return p[3] and 38 <= h * 360 <= 66 and s > 0.5 and v > 0.6

    frames = []
    for toward, amount in ((None, 0), ((255, 255, 235), 0.45), (None, 0), ((232, 118, 43), 0.4)):
        f = im.copy()
        if toward:
            px = f.load()
            for y in range(f.height):
                for x in range(f.width):
                    if lit(px[x, y]):
                        px[x, y] = mix(px[x, y], toward, amount)
        frames.append(f)
    return frames


def hop_across(im, w=48, reach=(0, 0, 5, 10, 14, 16)):
    """The bunny's hop with its travel built in: over the six frames it crosses 16 pixels of a
    48 wide frame, so the scene moves it 16 on every loop and it never slides while crouched."""
    frames = []
    for f, dx in zip(hop(im), reach):
        wide = Image.new("RGBA", (w, im.height), CLEAR)
        wide.paste(f, (dx, 0), f)
        frames.append(wide)
    return frames


def flying_arrow():
    """Cupid's arrow in flight, climbing to the right at 45 degrees: 12x12."""
    return bitmap(
        [
            ".......RR.RR",
            ".......RRRRR",
            "........RRR.",
            ".......G.R..",
            "......G.....",
            ".....G......",
            "....G.......",
            "...G........",
            ".PG.........",
            "PP..........",
            "P...........",
            "............",
        ],
        {"R": "#d8344f", "G": "#e0a52e", "P": "#f08aa0"},
    )


def tiny_heart(colour, size=3):
    rows = ["X.X", "XXX", ".X."] if size == 3 else ["XX.XX", "XXXXX", ".XXX.", "..X.."]
    return bitmap(rows, {"X": colour})


def cupid_act(folder, w=96, h=84):
    """The whole of Cupid's turn as one strip, so it plays the same wherever it is put.

    He flies at the lower left, wings beating (PixelLab's nine frames, animate-with-text-v3,
    from the still with the white wrap across his chest). He aims up and to the right at a
    heart floating ahead of him, looses, the arrow climbs at 45 degrees, strikes, and the
    heart bursts into a shower of small hearts; then a new heart swells in its place.
    Twelve frames; the cupid's own frame sits at (0, h - 48)."""
    c = [Image.open(f"{folder}/frame_{i:02d}.png").convert("RGBA") for i in range(9)]
    oy = h - 48
    tip = (45, 13)                                   # the nocked arrow's head, in his frame
    target = (tip[0] + 26, oy + tip[1] - 26)         # where it lands, in the strip's frame
    arrow = flying_arrow()
    red, pink, white = "#d8344f", "#ff4f87", "#ffffff"

    def at(im, sprite, cx, cy):
        im.alpha_composite(sprite, (round(cx - sprite.width / 2), round(cy - sprite.height / 2)))

    def burst(im, radius, kind):
        """Two rings of eight, the inner one turned half a step, so the shower looks full."""
        for ring, (reach, turn) in enumerate(((radius, math.pi / 8), (radius * 0.55, 0))):
            for k in range(8):
                a = math.pi / 4 * k + turn
                x, y = target[0] + reach * math.cos(a), target[1] - reach * math.sin(a)
                colour = (red, white, pink, white)[(k + ring) % 4]
                if kind == "hearts":
                    at(im, tiny_heart(colour, 5 if (k + ring) % 2 == 0 else 3), x, y)
                elif kind == "small":
                    at(im, tiny_heart(colour, 3), x, y)
                elif ring == 0 and 0 <= round(x) < w and 0 <= round(y) < h:
                    im.putpixel((round(x), round(y)), rgb(colour))

    def flash():
        f = heart(13).copy()
        px = f.load()
        for y in range(f.height):
            for x in range(f.width):
                if px[x, y][3]:
                    px[x, y] = rgb(white) if px[x, y] == rgb(red) else rgb(pink)
        return f

    #        his frame, what the heart is doing, where the arrow is along its 26 pixel climb
    script = [
        (0, 11, None), (1, 13, None), (2, 11, 6), (3, 13, 16), (4, "flash", None), (5, ("hearts", 7), None),
        (6, ("hearts", 12), None), (7, ("small", 16), None), (8, ("dots", 19), None), (5, None, None),
        (6, 9, None), (7, 11, None),
    ]
    frames = []
    for who, thing, flown in script:
        im = Image.new("RGBA", (w, h), CLEAR)
        if isinstance(thing, int):
            at(im, heart(thing), target[0], target[1])
        elif thing == "flash":
            at(im, flash(), target[0], target[1])
        elif thing:
            burst(im, thing[1], thing[0])
        if flown is not None:
            # the arrow's head leads: place the sprite so its heart is `flown` along the path
            im.alpha_composite(arrow, (tip[0] + flown - 9, oy + tip[1] - flown - 2))
        im.alpha_composite(c[who], (0, oy))
        frames.append(im)
    return frames


# ---------------------------------------------------------------- drawn in code

def outlined(fill, line):
    """Give a filled shape a one-pixel outline in `line`, drawn on its own edge pixels."""
    out = fill.copy()
    px, fp = out.load(), fill.load()
    w, h = fill.size
    for y in range(h):
        for x in range(w):
            if fp[x, y][3] and any(not (0 <= nx < w and 0 <= ny < h) or not fp[nx, ny][3]
                                   for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))):
                px[x, y] = line
    return out


HEARTS = {
    9: [".XX...XX.", "XXXX.XXXX", "XXXXXXXXX", "XXXXXXXXX", ".XXXXXXX.", "..XXXXX..", "...XXX...", "....X...."],
    11: ["..XX...XX..", ".XXXX.XXXX.", "XXXXXXXXXXX", "XXXXXXXXXXX", "XXXXXXXXXXX", ".XXXXXXXXX.",
         "..XXXXXXX..", "...XXXXX...", "....XXX....", ".....X....."],
    13: ["..XXX...XXX..", ".XXXXX.XXXXX.", "XXXXXXXXXXXXX", "XXXXXXXXXXXXX", "XXXXXXXXXXXXX", "XXXXXXXXXXXXX",
         ".XXXXXXXXXXX.", "..XXXXXXXXX..", "...XXXXXXX...", "....XXXXX....", ".....XXX.....", "......X......"],
}


def heart(size, n=16):
    """A heart `size` pixels wide (9, 11 or 13), centred in an n x n frame. Each size is set by
    hand: a curve this small rounds off into a shield."""
    red, light, line = rgb("#d8344f"), rgb("#f9c3cf"), rgb("#7a1730")
    rows = HEARTS[size]
    im = Image.new("RGBA", (n, n), CLEAR)
    x0, y0 = (n - size) // 2, (n - len(rows)) // 2
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch == "X":
                im.putpixel((x0 + i, y0 + j), red)
    im = outlined(im, line)
    im.putpixel((x0 + 2 + (size > 9), y0 + 2), light)      # the glint on the left lobe
    return im


def heart_pulse():
    return [heart(s) for s in (9, 11, 13, 11)]


def heart_arrow():
    """Cupid's arrow, flying right: pink fletching, a gold shaft, and a heart for a head, its
    point leading. 24x9."""
    gold, pink = rgb("#e0a52e"), rgb("#f08aa0")
    im = Image.new("RGBA", (24, 9), CLEAR)
    head = heart(9, 9).crop((0, 0, 9, 8)).transpose(Image.Transpose.ROTATE_270)   # point to the right
    for x in range(1, 17):
        im.putpixel((x, 4), gold)
    for x0 in (0, 3):                                 # two chevrons of feather
        for d, y in ((0, 2), (1, 3), (1, 5), (0, 6)):
            im.putpixel((x0 + d, y), pink)
            im.putpixel((x0 + d + 1, y), pink)
    im.alpha_composite(head, (16, 0))
    return im


EGGS = {
    # name: shell, pattern colour, second colour, pattern
    "prop-egg-pink": ("#f7a8c8", "#ffffff", "#ffe066", "zigzag"),
    "prop-egg-blue": ("#8fd3f4", "#ffffff", "#f7a8c8", "stripes"),
    "prop-egg-yellow": ("#ffe066", "#f7a8c8", "#8fd3f4", "bands"),
    "prop-egg-lilac": ("#c7a6ee", "#ffffff", "#ffe066", "dots"),
}


def egg(shell, a, b, pattern, n=32):
    """A painted egg, 18 wide and 24 tall, resting on the bottom row. Mirrored left to right."""
    shell, a, b = rgb(shell), rgb(a), rgb(b)
    im = Image.new("RGBA", (n, n), CLEAR)
    px = im.load()
    cy = n - 1 - 10                                # widest row sits 10 above the base
    for y in range(n):
        ry = 13.6 if y < cy else 10.6             # taller above the middle: the pointed end
        t = (y - cy) / ry
        if abs(t) > 1:
            continue
        half = 9.2 * math.sqrt(1 - t * t)
        for x in range(n):
            if abs(x - (n - 1) / 2) <= half:
                px[x, y] = shell
    top = im.getbbox()[1]
    for y in range(n):
        for x in range(n):
            if not px[x, y][3]:
                continue
            d = abs(x - (n - 1) / 2)              # mirror-safe distance from the centre line
            r = y - top
            if pattern == "zigzag":
                if (r + round(abs((d % 6) - 3))) % 8 in (0, 1):
                    px[x, y] = a
                elif r % 8 == 5 and round(d) % 4 == 1:
                    px[x, y] = b
            elif pattern == "stripes":
                if r % 6 in (0, 1):
                    px[x, y] = a
                elif r % 12 == 3 and round(d) % 4 == 1:
                    px[x, y] = b
            elif pattern == "bands":
                if r % 9 in (2, 3):
                    px[x, y] = a
                elif r % 9 in (6,):
                    px[x, y] = b
            elif pattern == "dots":
                if (r % 6 in (1, 2)) and (round(d + (3 if (r // 6) % 2 else 0)) % 6 in (1, 2)):
                    px[x, y] = a
                elif r % 12 == 10 and round(d) % 6 == 4:
                    px[x, y] = b
    im = outlined(im, NAVY)
    px = im.load()
    for x, y in ((12, top + 4), (13, top + 3), (12, top + 5)):      # one glint, upper left
        if px[x, y][3] and px[x, y] != NAVY:
            px[x, y] = WHITE
    return im


BUTTERFLY = [
    # wings open
    ["................", "................", ".....B....B.....", "......B..B......", ".PPP...BB...PPP.",
     "PPPPP..BB..PPPPP", "PPYPPP.BB.PPPYPP", "PPPPPPPBBPPPPPPP", ".PPPPPPBBPPPPPP.", "..PPPP.BB.PPPP..",
     ".PPPPP.BB.PPPPP.", ".PPYP..BB..PYPP.", "..PP........PP..", "................", "................", "................"],
    # half way
    ["................", "................", ".....B....B.....", "......B..B......", "....PP.BB.PP....",
     "...PPP.BB.PPP...", "...PYPPBBPPYP...", "...PPPPBBPPPP...", "....PPPBBPPP....", "....PP.BB.PP....",
     "...PPP.BB.PPP...", "...PYP.BB.PYP...", "....P......P....", "................", "................", "................"],
    # closed over her back
    ["................", "................", ".....B....B.....", "......B..B......", "......PBBP......",
     ".....PPBBPP.....", ".....PPBBPP.....", ".....PPBBPP.....", "......PBBP......", "......PBBP......",
     ".....PPBBPP.....", ".....PPBBPP.....", "................", "................", "................", "................"],
]


def butterfly():
    """Tiny pink butterfly, 4 frames in 16x16: wings open, half, closed, half."""
    wing, spot, line, body = rgb("#f7a8c8"), rgb("#ffe066"), rgb("#b84f84"), NAVY
    made = []
    for rows in BUTTERFLY:
        assert all(len(r) == 16 for r in rows) and len(rows) == 16
        wings = Image.new("RGBA", (16, 16), CLEAR)
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                if ch in "PY":
                    wings.putpixel((x, y), wing)
        im = outlined(wings, line)
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                if ch == "Y":
                    im.putpixel((x, y), spot)
                elif ch == "B":
                    im.putpixel((x, y), body)
        made.append(im)
    return [made[0], made[1], made[2], made[1]]


def dolphin(w=48, h=28, water=23, leap=8, rest=8):
    """A small far-off dolphin: one leap over `leap` frames, then under water for `rest`.
    Row `water` of the frame is the sea surface; anything below it is hidden. The body bends
    along the arc of the leap, so it curls over the top the way a dolphin does."""
    back, side, belly, foam = rgb("#2f6fb0"), rgb("#4c93d6"), rgb("#d6ecf7"), rgb("#fbfaf9")
    length, x0, x1, top = 18.0, 8.0, 40.0, 17.0
    half = length / 2

    def arc(tau):
        return x0 + (x1 - x0) * tau, water - 4 * top * tau * (1 - tau)

    def width(a):
        if a < -half or a > half + 1.2:
            return None
        if a <= 1.0:
            return 0.9 + 2.0 * (a + half) / (half + 1.0)            # tail stock up to the chest
        if a <= half - 0.6:
            return 2.9 - 0.6 * (a - 1.0) / (half - 1.6)             # chest to the round head
        return 0.95                                                # the short beak

    frames = []
    for i in range(leap):
        t = (i + 0.5) / leap
        vx, vy = (x1 - x0), -4 * top * (1 - 2 * t)
        speed = math.hypot(vx, vy)
        spine = []
        a = -half - 2.6
        while a <= half + 1.3:
            tau = t + a / speed
            px_, py_ = arc(tau)
            tx, ty = (x1 - x0), -4 * top * (1 - 2 * tau)
            n = math.hypot(tx, ty)
            spine.append((a, px_, py_, tx / n, ty / n))
            a += 0.25
        fill = Image.new("RGBA", (w, h), CLEAR)
        fp = fill.load()
        shade = {}
        for y in range(h):
            for x in range(w):
                cx, cy = x + 0.5, y + 0.5
                a, sx, sy, tx, ty = min(spine, key=lambda q: (q[1] - cx) ** 2 + (q[2] - cy) ** 2)
                dx, dy = cx - sx, cy - sy
                b = dx * ty - dy * tx                 # across the body, + toward the back
                if abs(dx * tx + dy * ty) > 0.6:      # past either end of the spine
                    continue
                wdt = width(a)
                inside = wdt is not None and abs(b) <= wdt
                if not inside and wdt is not None and -3.0 <= a <= 0.6 and 0 < b <= wdt + 2.9 - 1.25 * abs(a + 0.9):
                    inside = True                     # dorsal fin
                if not inside and -half - 2.6 <= a <= -half + 0.3:
                    inside = abs(b) <= 0.8 + 1.15 * (-half + 0.3 - a)   # tail fluke
                if inside:
                    fp[x, y] = side
                    shade[x, y] = b
        im = outlined(fill, NAVY)
        px = im.load()
        for (x, y), b in shade.items():
            if px[x, y] != NAVY:
                px[x, y] = back if b > 0.4 else belly if b < -0.9 else side
        for y in range(water, h):                    # under the surface
            for x in range(w):
                px[x, y] = CLEAR
        for sx, on in ((x0 - 1, i in (0, 1)), (x1 + 1, i in (leap - 2, leap - 1))):   # splash
            if on:
                for dxs, dys in ((-2, -1), (0, -3), (2, -2), (-1, 0), (1, 0), (3, 0), (-3, 0)):
                    xx, yy = round(sx + dxs), water - 1 + dys
                    if 0 <= xx < w and 0 <= yy < h and not px[xx, yy][3]:
                        px[xx, yy] = foam
        frames.append(im)
    for k in range(rest):                            # the ring it leaves, then calm water
        im = Image.new("RGBA", (w, h), CLEAR)
        if k < 2:
            for dxs in ((-2, 2) if k == 0 else (-4, 4)):
                im.putpixel((round(x1 + 1 + dxs), water - 1), foam)
        frames.append(im)
    return frames


def waves(bg, top=124, bottom=174, shore=146, clear=(110, 270)):
    """Summer: the sea, cut from the painting as an overlay strip, four frames.

    The water's edge washes up the beach and back: from row `shore` down, each frame takes its
    pixels from 0, 1, 2, 1 rows higher. Only sea, foam and sand move. Their colours are read
    from the open stretch of beach between columns `clear`; anything else (palms, umbrella,
    chair, board, their shadows) stays exactly where it is. Further out, a few highlights
    twinkle on the swell.
    """
    src = bg.convert("RGBA")
    sp = src.load()
    w = src.width
    movable = {sp[x, y][:3] for y in range(top, bottom) for x in range(*clear)}
    sea = [c for c in (rgb("#1da5ac"), rgb("#1fb4ba"), rgb("#2bc7c8"), rgb("#36d7d7"))]
    glints = []
    for y in range(top + 3, shore - 2, 3):
        for k in range(5):
            x = (y * 53 + k * 71 + (y // 3) * 29) % (w - 8)
            glints.append((x, y, 3 + (x + y) % 4, (x // 7 + y) % 4))
    frames = []
    for t, pull in enumerate((0, 1, 2, 1)):
        f = src.crop((0, top, w, bottom))
        fp = f.load()
        for y in range(shore, bottom):
            for x in range(w):
                if sp[x, y][:3] in movable and sp[x, y - pull][:3] in movable:
                    fp[x, y - top] = sp[x, y - pull]
        for x, y, n, phase in glints:
            if (t - phase) % 4 < 2:
                for i in range(n):
                    here = sp[x + i, y]
                    if here in sea:                  # only on open water, one band lighter
                        fp[x + i, y - top] = sea[min(len(sea) - 1, sea.index(here) + 1)] if here != sea[-1] else rgb("#4fe8e8")
        frames.append(f)
    return frames, top


# ---------------------------------------------------------------- foreground layers

# The Halloween painting, in background pixels.
FENCE_TOP = 148                  # from the fence down everything is scenery
OPEN_SKY = [(0, 0, 344, 26), (142, 26, 250, 140)]   # nothing but sky, moon and far hills in these
HILL_BEHIND = (55, 120)          # the far hill seen between the left tree and the house: shut in by a branch, but sky
# The painter edged the trunks, the gravestone and the fence in the moon halo's pale greys, and
# tiled the roof in them and in three dusk purples. So by colour alone those edges are sky, and
# a bat was drawn over them. Inside each of these boxes the listed colours are scenery.
PALE = {(0xAF, 0xAF, 0xA2), (0x9B, 0x87, 0x83), (0x7C, 0x62, 0x77), (0x7E, 0x82, 0x7C), (0x6C, 0x6E, 0x74)}
DUSK = {(0x6E, 0x3E, 0x68), (0x59, 0x39, 0x68), (0x87, 0x47, 0x6F)}
SOLID = [
    ((78, 104, 142, 148), PALE | DUSK),             # the house and its roof
    ((100, 88, 124, 108), PALE | DUSK),             # its chimney
    ((36, 80, 56, 148), PALE),                      # the pale edge of the left trunk
    ((304, 88, 324, 148), PALE),                    # and of the right one
    ((268, 116, 302, 148), PALE),                   # the gravestone's rim
    ((0, 134, 68, 148), PALE),                      # the fence's tips, left, middle and right;
    ((136, 140, 268, 148), PALE),                   # the middle starts lower, under the far hills' pale ridge line
    ((296, 134, 344, 148), PALE),
]
MOON = (212, 24, 297, 67)        # its halo is the same pale greys, and the right tree's branches cross it
INK = (5, 3, 25)                 # the near-black the trees are drawn in
# Checked after every build: these must be scenery, and these open sky.
MUST_COVER = [(46, 110), (43, 135), (318, 120), (318, 140), (108, 96), (100, 120), (110, 140), (273, 132), (285, 121), (30, 120), (328, 120)]
MUST_NOT_COVER = [(180, 60), (248, 60), (232, 34), (55, 120), (170, 120), (212, 137), (150, 20), (5, 60), (340, 30)]


def halloween_scenery(bg):
    """Everything a bat must pass behind: the house, both trees, the gravestone, the fence and
    the ground, each whole.

    The first version kept only the painting's near-black, which is the outlines. A bat then
    showed through the house's walls and the trunks with their outlines drawn over it: Luz saw
    bats "going through houses and trees". Now the backdrop is found instead, by flooding in
    from the top and sides of the frame through the colours the open sky and far hills are
    made of, and scenery is whatever the flood cannot reach."""
    px = bg.load()
    w, h = bg.size
    count = {}
    for x0, y0, x1, y1 in OPEN_SKY:
        for y in range(y0, y1):
            for x in range(x0, x1):
                count[px[x, y][:3]] = count.get(px[x, y][:3], 0) + 1
    sky = {c for c, n in count.items() if n >= 3}

    solid = {}
    for (x0, y0, x1, y1), colours in SOLID:
        for y in range(y0, y1):
            for x in range(x0, x1):
                solid[x, y] = solid.get((x, y), set()) | colours

    def glint(x, y):
        """A pale pixel touching the tree's black: a glint on a branch. (Not in the moon's
        halo, where a branch only passes by.)"""
        if px[x, y][:3] not in PALE or (MOON[0] <= x < MOON[2] and MOON[1] <= y < MOON[3]):
            return False
        near = [(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy]
        return any(0 <= nx < w and 0 <= ny < h and px[nx, ny][:3] == INK for nx, ny in near)

    def open_air(x, y):
        c = px[x, y][:3]
        return y < FENCE_TOP and c in sky and c not in solid.get((x, y), ()) and not glint(x, y)

    todo = [(x, y) for y in range(FENCE_TOP) for x in range(w) if (y == 0 or x in (0, w - 1)) and open_air(x, y)]
    assert open_air(*HILL_BEHIND), "the painting has changed: check the Halloween foreground by eye"
    todo.append(HILL_BEHIND)
    air = set(todo)
    while todo:
        x, y = todo.pop()
        for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= n[0] < w and 0 <= n[1] < h and n not in air and open_air(*n):
                air.add(n)
                todo.append(n)
    scenery = {(x, y) for y in range(h) for x in range(w)} - air
    # a star or a fleck of cloud is not scenery: drop the pieces that touch nothing else
    todo, kept = set(scenery), set()
    while todo:
        piece, stack = set(), [todo.pop()]
        while stack:
            x, y = stack.pop()
            piece.add((x, y))
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    n = (x + dx, y + dy)
                    if n in todo:
                        todo.remove(n)
                        stack.append(n)
        if len(piece) >= 12 or any(px[q][:3] in solid.get(q, ()) for q in piece):   # a fence tip is small too
            kept |= piece
    wrong = [p for p in MUST_COVER if p not in kept] + [p for p in MUST_NOT_COVER if p in kept]
    assert not wrong, f"the Halloween foreground is wrong at {wrong}: the painting has changed, check it by eye"
    return kept


def foreground(season, bg):
    """Scenery the sky's moving things pass behind: the same pixels as the painting, lifted
    into their own layer. Returns None for a season that needs none."""
    px = bg.load()
    w, h = bg.size
    mask = set()
    if season == "halloween":
        mask = halloween_scenery(bg)
    elif season == "summer":                       # palms and the spiky plants
        def kind(p):
            hh, s, v = colorsys.rgb_to_hsv(*(c / 255 for c in p[:3]))
            deg = hh * 360
            if 50 <= deg <= 110 and s > 0.5:
                return "leaf"
            if (8 <= deg <= 30 and s > 0.5 and v < 0.8) or (30 < deg < 60 and v < 0.5):
                return "trunk"
            return None
        todo = [(x, y) for y in range(172) for x in range(w) if kind(px[x, y]) == "leaf"]
        mask = set(todo)
        while todo:
            x, y = todo.pop()
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= nx < w and 0 <= ny < 172 and (nx, ny) not in mask and kind(px[nx, ny]):
                    if not (30 <= nx <= 80 and ny >= 128):     # not the umbrella pole or the chair
                        mask.add((nx, ny))
                        todo.append((nx, ny))
    if not mask:
        return None
    out = Image.new("RGBA", bg.size, CLEAR)
    op = out.load()
    for x, y in mask:
        op[x, y] = px[x, y]
    return out
