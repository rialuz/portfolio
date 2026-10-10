"""Seasonal environment kits: the code-built half.

Each season swaps the pixel environment only. The site theme and the character stay as they
are, so every piece here fits the slot its candy original fills: same file name, same size,
same anchor rows. That lets the site switch season by changing one folder.

  bg-hero.png            344x192. Feet rest on row 172, as in the candy scene; the walkable
                         surface runs to row 177 and the ground's face fills the rest.
  bg-cloud-1..3.png      the candy clouds' shapes in the season's sky colours
  prop-cloud.png         the puff that drifts over the Experience road
  prop-flag.png          the goal flag, 4 frames, with the cloth in a season colour
  tile-road-*.png        straight, corner and faded road tiles, 32x32

Backgrounds come from PixelLab (raw/bg-a.png, see season_gen.py and the ledger); here they are
moved onto the shared ground line and given a ground face.

Props and the moving pieces are made in season_fx.py; the tables under "kits" say which each
season has and where the moving ones go in the hero scene.

Output: seasons/<season>/drawn/ (working copies), then <candy sprites dir>/seasons/<season>/
with manifest.json beside the season folders, and preview/seasons-data.js for the preview page.

usage: seasons.py <pixel-assets dir> <candy sprites dir>
"""
import colorsys
import json
import math
import os
import shutil
import sys
from collections import Counter

from PIL import Image

import season_fx as fx

NAVY = (0x23, 0x30, 0x4D, 255)
CREAM = (0xFF, 0xF7, 0xEE, 255)
WHITE = (255, 255, 255, 255)
CLEAR = (0, 0, 0, 0)
N = 32
BG_W, BG_H = 344, 192
SCALLOP = [0, 1, 1, 2, 2, 1, 1, 0]  # piping, reads the same forwards and backwards


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


def mix(a, b, t):
    return tuple(round(x + (y - x) * t) for x, y in zip(a[:3], b[:3])) + (255,)


# ---------------------------------------------------------------- backgrounds

def speck(x, y, a, b):
    return (x * a + y * b) % 29 == 0


def face_halloween(x, y, top, g):
    """A low wall of dark stone blocks."""
    r = y - top
    if r == 0:
        return mix(g, (0, 0, 0), 0.45)
    joint = (x + (8 if (r // 5) % 2 else 0)) % 16 == 0
    if r % 5 == 0 or (joint and r < 11):
        return mix(g, (0, 0, 0), 0.28) if r < 11 else g
    if r < 10 and speck(x, y, 7, 13):
        return mix(g, (255, 255, 255), 0.10)
    return g


def face_easter(x, y, top, g):
    """Garden soil with a few pebbles."""
    r = y - top
    if r == 0:
        return mix(g, (0, 0, 0), 0.30)
    if r == 1:
        return mix(g, (0, 0, 0), 0.12)
    if r < 10 and speck(x, y, 7, 13):
        return mix(g, (0, 0, 0), 0.18)
    if r < 10 and speck(x + 3, y, 11, 5):
        return mix(g, (255, 255, 255), 0.22)
    return g


def face_summer(x, y, top, g, sand=(246, 217, 167)):
    """Damp sand: the dry sand steps down to it in two dithered rows, no hard edge."""
    r = y - top
    if r == 0:
        return mix(sand, g, 0.5) if (x + y) % 2 else rgb("#f6d9a7")
    if r == 1:
        return mix(sand, g, 0.5)
    if r == 2:
        return g if (x + y) % 2 else mix(sand, g, 0.5)
    if r < 10 and speck(x, y, 7, 13):
        return mix(g, (0, 0, 0), 0.10)
    if r < 10 and speck(x + 5, y, 11, 5):
        return mix(g, (255, 255, 255), 0.25)
    return g


def unbat(im):
    """Halloween: the painting has one still bat on the moon's lower left. The animated bats
    replace it, so paint it out with the moon's own rings, mirrored from the clear upper left."""
    px = im.load()
    moon = [(x, y) for y in range(100) for x in range(200, 300) if px[x, y][:3] == (253, 236, 180)]
    if not moon:
        moon = [(x, y) for y in range(100) for x in range(200, 300) if sum(px[x, y][:3]) > 640]
    cy = round(sum(p[1] for p in moon) / len(moon))
    fixed = 0
    for y in range(cy + 8, cy + 30):
        for x in range(222, 252):
            r, g, b, _ = px[x, y]
            if r < 70 and g < 60:                       # the bat's near-black body
                px[x, y] = px[x, 2 * cy - y]
                fixed += 1
    return fixed


def hsv(p):
    return colorsys.rgb_to_hsv(*(c / 255 for c in p[:3]))


def patch_from(im, box, clean, rows=None):
    """Paint out what stands in `box` (x0, y0, x1, y1, inclusive) with the same rows of a clean
    stretch of the painting, columns `clean` = (first, last). The stretch is the one whose
    edges best match what borders the box, so a fence carries on through it."""
    px = im.load()
    x0, y0, x1, y1 = box
    ys = range(*(rows or (y0, y1 + 1)))
    width = x1 - x0 + 1
    edge = [x0 - 3, x0 - 2, x0 - 1, x1 + 1, x1 + 2, x1 + 3]

    def miss(src):
        return sum(px[x, y] != px[src + (x - x0), y] for y in ys for x in edge)

    best = min(range(clean[0] + 3, clean[1] - width - 2), key=miss)
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            px[x, y] = px[best + (x - x0), y]


def cover(im, old, sprite, left, bottom, was):
    """Stand `sprite` where an old painted thing was, its bottom row on `bottom`. Any of the
    old thing still showing round it (pixels in `old` that `was` recognises) is filled from
    the pixel above, so the fence or sky behind carries on down."""
    px = im.load()
    x0, y0, x1, y1 = old
    stale = {(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1) if was(px[x, y])}
    top = bottom - sprite.height + 1
    im.alpha_composite(sprite, (left, top))
    sp = sprite.load()
    covered = {(left + x, top + y) for y in range(sprite.height) for x in range(sprite.width) if sp[x, y][3]}
    left_over = sorted(stale - covered, key=lambda p: p[1])
    for x, y in left_over:
        px[x, y] = px[x, y - 1]
    return len(left_over)


def dress_halloween(im, base):
    """After the painting is on its ground line: PixelLab's jack-o'-lanterns had lopsided
    faces and its gravestone a stray ring. Each pumpkin becomes the lit pumpkin of the kit,
    mirrored so its face is exact, or its small twin; the stone gets a cross."""
    notes = []
    big = fx.mirror_below(fx.prop(Image.open(os.path.join(base, "raw", "prop-pumpkin.png")).convert("RGBA"))[0], 10)
    big = big.crop(big.getbbox())
    small = fx.small_pumpkin()

    def pumpkin(p):
        h, s, v = hsv(p)
        d = h * 360
        return ((d <= 70 or d >= 345) and s > 0.4 and v > 0.35) or (70 < d < 150 and s > 0.3 and v > 0.2)

    # the small one that would crowd the kit's own lit pumpkin goes; the fence closes over it
    patch_from(im, (231, 150, 246, 164), (160, 228))
    # old box (x0, y0, x1, y1), new sprite, its left column and bottom row
    for old, sprite, left, bottom in (
        ((87, 152, 103, 166), small, 87, 165),
        ((137, 152, 152, 165), small, 136, 164),
        ((53, 145, 78, 168), big, 51, 167),
        ((243, 140, 270, 167), big, 242, 166),
    ):
        n = cover(im, old, sprite, left, bottom, pumpkin)
        if n:
            notes.append(f"filled {n} pixels round a pumpkin")

    # the gravestone: smooth the ring away, then cut a cross with a lit edge
    px = im.load()
    stone, cut, lit = rgb("#3a3a59"), rgb("#190e3d"), rgb("#7e827c")
    for y in range(126, 134):
        for x in range(280, 291):
            if px[x, y] != rgb("#2a2750"):
                px[x, y] = stone
    cross = {(x, y) for y in range(128, 144) for x in (282, 283, 284)} | {(x, y) for y in (132, 133, 134) for x in range(278, 289)}
    for x, y in cross:
        px[x, y] = cut
    for x, y in cross:                                 # light catches the right and lower edges
        for n in ((x + 1, y), (x, y + 1)):
            if n not in cross and px[n] == stone:
                px[n] = lit
    return notes


def dress_valentines(im, base):
    """PixelLab's two gift boxes read as striped blocks. Paint them out, fence and all, and
    set down presents that are plainly presents: a box, a lid, a ribbon and a bow."""
    patch_from(im, (79, 138, 95, 157), (152, 226))
    patch_from(im, (227, 138, 254, 157), (152, 226))
    red = fx.present("#e8455f", "#f47a8e", "#fff6dc")
    cream = fx.present("#fff6dc", "#ffffff", "#d8344f")
    pink = fx.present("#f9a3bd", "#fcc6d6", "#ffd166", small=True)
    for sprite, left in ((red, 80), (cream, 229), (pink, 242)):
        im.alpha_composite(sprite, (left, 157 - sprite.height + 1))
    return []


BACKGROUNDS = {
    # dy moves the raw painting down (+) or up (-) so its walkable ground sits on rows 166-177.
    # face_row is the first row of the ground face; ground is its flat colour.
    # fix works on the raw painting, dress on the finished one.
    "halloween": dict(dy=19, face_row=178, ground=rgb("#231a3a"), face=face_halloween, fix=unbat, dress=dress_halloween),
    "valentines": dict(dy=0, face_row=None, ground=None, face=None, dress=dress_valentines),   # already on the line
    "easter": dict(dy=-10, face_row=179, ground=rgb("#a9764a"), face=face_easter),
    "summer": dict(dy=6, face_row=179, ground=rgb("#d9ad74"), face=face_summer),
}


def background(season, raw_path):
    cfg = BACKGROUNDS[season]
    raw = Image.open(raw_path).convert("RGBA")
    assert raw.size == (BG_W, BG_H), raw.size
    notes = []
    if cfg.get("fix"):
        notes.append(f"painted out {cfg['fix'](raw)} pixels")
    out = Image.new("RGBA", (BG_W, BG_H), CLEAR)
    out.paste(raw, (0, cfg["dy"]))
    px, rp = out.load(), raw.load()
    for y in range(max(0, cfg["dy"])):                  # sky above a painting moved down
        for x in range(BG_W):
            px[x, y] = rp[x, 0]
    if cfg["face"]:
        for y in range(cfg["face_row"], BG_H):
            for x in range(BG_W):
                px[x, y] = cfg["face"](x, y, cfg["face_row"], cfg["ground"])
    if cfg.get("dress"):
        notes += cfg["dress"](out, os.path.dirname(os.path.dirname(raw_path)))
    assert all(px[x, y][3] == 255 for x in range(BG_W) for y in range(BG_H)), "gap in the painting"
    sky = Counter(px[x, 0][:3] for x in range(BG_W)).most_common(1)[0][0]
    ground = (cfg["ground"] or Counter(px[x, BG_H - 1] for x in range(BG_W)).most_common(1)[0][0])[:3]
    return out, sky, ground, notes


# ---------------------------------------------------------------- clouds, puff, flag

CLOUD = {"halloween": rgb("#4d3a78"), "valentines": rgb("#fff6dc"), "easter": rgb("#fcfefd"), "summer": rgb("#f9fcfa")}

# Candy cloth colours, darkest to lightest, and each season's cloth in the same order.
FLAG_CANDY = ["#9c4638", "#c65f4e", "#e8a49c", "#f7c6c0"]
FLAG = {
    "halloween": ["#b4541a", "#e8762b", "#f5a85c", "#fbd3a5"],
    "valentines": ["#a32239", "#d8344f", "#f08aa0", "#f9c3cf"],
    "easter": ["#7c62b3", "#a78bd9", "#cdbbef", "#e9e0fa"],
    "summer": ["#14808c", "#1fa9b8", "#7fd8e0", "#c9f1f4"],
}
# The road puff: body and shade (its outline stays).
PUFF = {
    "halloween": ("#6a5596", "#4d3a78"),
    "valentines": ("#ffe3ec", "#f7b5cb"),
    "easter": ("#ffffff", "#dcefd2"),
    "summer": ("#ffffff", "#cdeef2"),
}


def recolour(im, mapping):
    out = im.copy()
    px = out.load()
    table = {rgb(a)[:3]: rgb(b) for a, b in mapping.items()}
    for y in range(out.height):
        for x in range(out.width):
            p = px[x, y]
            if p[3] and p[:3] in table:
                px[x, y] = table[p[:3]]
    return out


def cloud(src, colour):
    """A candy cloud's silhouette in one flat colour, as the candy clouds are."""
    out = src.copy()
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            if px[x, y][3]:
                px[x, y] = colour
    return out


def heart_cloud(w, h, colour, shade):
    """Valentine's: the middle cloud is a heart of puffs, the size of the cloud it replaces."""
    out = Image.new("RGBA", (w, h), CLEAR)
    px = out.load()
    cx, s = (w - 1) / 2, h / 2.55

    def inside(x, y):
        u, v = (x - cx) / (s * 1.08), (h * 0.44 - y) / s
        return (u * u + v * v - 1) ** 3 - u * u * v ** 3 <= 0

    for y in range(h):
        for x in range(w):
            if inside(x, y):
                px[x, y] = colour
    # a scalloped underside in the shade colour, two rows deep, so it reads as cloud
    for x in range(w):
        col = [y for y in range(h) if px[x, y][3]]
        if col:
            for k in range(1 + (1 if (x // 3) % 2 else 0)):
                if len(col) > k + 3:
                    px[x, col[-1 - k]] = shade
    # mirror the left half so it is symmetric to the pixel
    for y in range(h):
        for x in range(w // 2):
            px[w - 1 - x, y] = px[x, y]
    return out


# ---------------------------------------------------------------- road tiles

class Road:
    """One cross-section, like the candy road in draw.py: navy lines at 0 and 4 with a striped
    rail between, a bevel, then the body. Bodies read the same forwards and backwards along
    the road so the mitred corner joins cleanly."""

    rail = (WHITE, WHITE)
    bevel = (WHITE, WHITE)
    base = WHITE

    def body(self, u, m):
        return self.base

    def centre(self, px, ox, oy, turned=False):
        """Motif on the centre line; (ox, oy) is where the 16px cell starts."""

    def at(self, u, v):
        m = min(v, N - 1 - v)
        if m in (0, 4):
            return NAVY
        if m < 4:
            return self.rail_at(u, m)
        if m == 5:
            return self.bevel[0] if v < N // 2 else self.bevel[1]
        return self.body(u, m)

    def rail_at(self, u, m):
        return self.rail[0] if (u + m) % 8 < 4 else self.rail[1]

    def straight(self):
        im = Image.new("RGBA", (N, N), CLEAR)
        px = im.load()
        for y in range(N):
            for x in range(N):
                px[x, y] = self.at(x, y)
        for cell in (0, 16):
            self.centre(px, cell, 0)
        return im

    def corner(self):
        """Enters at the left edge, leaves through the top; mitred like a picture frame."""
        im = Image.new("RGBA", (N, N), CLEAR)
        px = im.load()
        for y in range(N):
            for x in range(N):
                v = max(x, y)
                u = x if y >= x else N - 1 - y
                if v >= N // 2 or v <= 9:
                    px[x, y] = self.at(u, v)
                else:
                    px[x, y] = self.body(u, 12)   # inside of the turn: plain road
        self.centre(px, 0, 0)
        self.centre(px, 0, 0, turned=True)
        return im


def stamp(px, rows, x0, y0, colours, turned=False):
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch != ".":
                x, y = (x0 + i, y0 + j) if not turned else (y0 + j, x0 + i)
                px[x, y] = colours[ch]


class Cobbles(Road):
    """Halloween: grey cobbles in brick bond, pumpkin-orange rails and lane dashes."""
    rail = (rgb("#e8762b"), rgb("#3a2456"))
    bevel = (rgb("#a6a2b6"), rgb("#4a4560"))
    base = rgb("#807c90")
    mortar = rgb("#4a4560")
    stones = (rgb("#807c90"), rgb("#8f8ba0"))
    light, dark = rgb("#aaa6ba"), rgb("#6a667a")

    def body(self, u, m):
        if m == 15:                                    # the centre joint, two rows with v
            return self.mortar
        if m == 10:
            return self.mortar
        k = u % 8
        outer = m < 10                                 # rows 6-9, then rows 11-14 offset
        if (k in (0, 7)) if outer else (k in (3, 4)):
            return self.mortar
        stone = (u + (0 if outer else 4)) // 8 % 2
        top = m in (6, 11)
        low = m in (9, 14)
        if top:
            return self.light
        if low:
            return self.dark
        return self.stones[stone if outer else 1 - stone]

    def centre(self, px, ox, oy, turned=False):
        for i in range(4, 12):
            for j in (15, 16):
                x, y = (ox + i, j) if not turned else (j, ox + i)
                px[x, y] = self.rail[0]


class Hearts(Road):
    """Valentine's: a pink road with lace piping and red hearts down the middle."""
    rail = (rgb("#d8344f"), WHITE)
    bevel = (rgb("#fbc6d6"), rgb("#d9708f"))
    base = rgb("#f29bb7")
    HEART = [".RR.RR.", "RWRRRRR", "RRRRRRR", ".RRRRR.", "..RRR..", "...R..."]

    def body(self, u, m):
        if m == 7 + SCALLOP[u % 8]:
            return WHITE
        if 10 <= m <= 12 and (u % 16 in (0, 15)) and m == 11:
            return rgb("#fbc6d6")                      # sugar dots between the hearts
        return self.base

    def centre(self, px, ox, oy, turned=False):
        stamp(px, self.HEART, ox + 4, 13, {"R": rgb("#d8344f"), "W": rgb("#fbc6d6")}, turned)


class Garden(Road):
    """Easter: a dirt garden path between flower beds, with pastel egg stepping stones."""
    bevel = (rgb("#f6e3b5"), rgb("#c99b63"))
    base = rgb("#eac98f")
    grass, blade = rgb("#6cc24a"), rgb("#93d86a")
    blooms = (rgb("#f7a8c8"), rgb("#ffe066"), rgb("#ffe066"), rgb("#f7a8c8"))
    EGG = [".PPPP.", "PWPPPP", "PPPPWP", ".PPPP."]

    def rail_at(self, u, m):
        k = u % 8
        if m == 2 and k in (3, 4):
            return self.blooms[u // 8 % 4]
        if (m == 1 and k in (0, 7)) or (m == 3 and k in (1, 6)):
            return self.blade
        return self.grass

    def body(self, u, m):
        if m == 7 + SCALLOP[u % 8]:
            return rgb("#fff7d6")
        if 10 <= m <= 13 and (u * 7 + m * 13) % 29 == 0:
            return rgb("#d2a66b")
        return self.base

    def centre(self, px, ox, oy, turned=False):
        pink = ox % 32 == 0
        stamp(px, self.EGG, ox + 5, 14,
              {"P": rgb("#f7a8c8") if pink else rgb("#8fd3f4"), "W": WHITE}, turned)


class Sand(Road):
    """Summer: a sand path with a foam line, turquoise pool-ring rails, shells and starfish."""
    rail = (rgb("#1fa9b8"), WHITE)
    bevel = (rgb("#fbe8bf"), rgb("#d9b37a"))
    base = rgb("#f3d9a2")
    SHELL = [".PPPP.", "PWPWPP", "PPWPPP", ".PPPP.", "..PP.."]
    STAR = ["..O..", ".OOO.", "OOYOO", ".OOO.", ".O.O."]

    def body(self, u, m):
        if m == 7 + SCALLOP[u % 8]:
            return WHITE
        if 10 <= m <= 13 and (u * 7 + m * 13) % 29 == 0:
            return rgb("#e3c286")
        return self.base

    def centre(self, px, ox, oy, turned=False):
        if ox % 32 == 0:
            stamp(px, self.SHELL, ox + 5, 13, {"P": rgb("#f4a6b8"), "W": rgb("#fde0e6")}, turned)
        else:
            stamp(px, self.STAR, ox + 6, 13, {"O": rgb("#f08a3c"), "Y": rgb("#fbd36a")}, turned)


ROADS = {"halloween": Cobbles(), "valentines": Hearts(), "easter": Garden(), "summer": Sand()}


def faded(im, amount=0.62):
    """The same road blended toward the cream page colour, for the stretch not travelled yet."""
    out = im.copy()
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            if px[x, y][3]:
                px[x, y] = mix(px[x, y], CREAM, amount)
    return out


# ---------------------------------------------------------------- interface

# The dialogue box's frame and name plate in each season's dress: the same build as the candy
# ones in ui.py (same sizes, same slices), so the site swaps them like any other piece.
#   rail: the two stripes of the outer rail.  band: light edge, body, dark edge of the band
#   inside it.  piping: the scalloped line on the band.  corner: what sits on each corner.
#   plate: the name plate's rim stripes, its body (light, body, dark centre) and its dots.
#   The plate's dark centre is also the colour the site paints behind the name.
UI = {
    "halloween": dict(rail=("#e8762b", "#3a2456"), band=("#7a6a9c", "#5a4a7a", "#3d3058"), piping="#fbd3a5", corner="pumpkin",
                      plate=dict(rim=("#e8762b", "#2a1a3a"), body=("#7a6a9c", "#5a4a7a", "#3d3058"), dots="#fbd3a5")),
    "valentines": dict(rail=("#d8344f", "#ffffff"), band=("#fbc6d6", "#f29bb7", "#d9708f"), piping="#ffffff", corner="heart",
                       plate=dict(rim=("#d8344f", "#ffffff"), body=("#e06a82", "#c22c46", "#a32239"), dots="#ffffff")),
    "easter": dict(rail=("#f7a8c8", "#ffffff"), band=("#a6e283", "#7fcf5a", "#57a83b"), piping="#ffffff", corner="egg",
                   plate=dict(rim=("#ffe066", "#ffffff"), body=("#a78bd9", "#8466c4", "#6247a3"), dots="#ffe066")),
    "summer": dict(rail=("#1fa9b8", "#ffffff"), band=("#fbe8bf", "#f3d9a2", "#d9b37a"), piping="#ffffff", corner="ring",
                   plate=dict(rim=("#1fa9b8", "#ffffff"), body=("#3fc1cc", "#1b8f9c", "#136f7a"), dots="#ffffff")),
}

# Corner pieces, 14x14, drawn upright on all four corners. N is the navy outline.
CORNERS = {
    "pumpkin": (
        ["......GG......", "....NNGGNN....", "..NNOOOOOONN..", ".NOOOOOOOOOON.", "NOOKKOOOOKKOON", "NOOKKOOOOKKOON",
         "NOOOOOKKOOOOON", "NOKOOOOOOOOKON", "NOKKOKKKKOKKON", "NOOKKKKKKKKOON", ".NOOOKKKKOOON.", "..NNOOOOOONN..",
         "....NNNNNN....", ".............."],
        {"G": "#4f8a2a", "O": "#e8762b", "K": "#2a1a3a"}),
    "heart": (
        ["..............", "..NNN....NNN..", ".NRRRN..NRRRN.", "NRWRRRNNRRRRRN", "NRWRRRRRRRRRRN", "NRRRRRRRRRRRRN",
         "NRRRRRRRRRRRRN", ".NRRRRRRRRRRN.", "..NRRRRRRRRN..", "...NRRRRRRN...", "....NRRRRN....", ".....NRRN.....",
         "......NN......", ".............."],
        {"R": "#d8344f", "W": "#f9c3cf"}),
    "egg": (
        [".....NNNN.....", "...NNPPPPNN...", "..NPPWPPPPPN..", "..NPWPPPPPPN..", ".NPPPPPPPPPPN.", ".NWWPPWWPPWWN.",
         ".NPPWWPPWWPPN.", ".NPPPPPPPPPPN.", ".NYPPYPPYPPYN.", ".NPPPPPPPPPPN.", "..NPPPPPPPPN..", "..NNPPPPPPNN..",
         "....NNNNNN....", ".............."],
        {"P": "#f7a8c8", "W": "#ffffff", "Y": "#ffe066"}),
}


def corner_piece(kind, lx, ly, size):
    """Colour of the corner piece at (lx, ly) of its size x size cell, or None outside it."""
    if kind == "ring":                             # a life ring: the candy peppermint with a hole of water
        c = (size - 1) / 2
        r = math.hypot(lx - c, ly - c)
        if r > size / 2:
            return None
        if r > size / 2 - 1.1 or 2.2 < r <= 3.3:
            return NAVY
        if r <= 2.2:
            return rgb("#7fd8e0")
        wedge = int((math.atan2(ly - c, lx - c) + math.pi) / (math.pi / 4)) % 2
        return rgb("#e0483f") if wedge else WHITE
    rows, key = CORNERS[kind]
    ch = rows[ly][lx]
    return None if ch == "." else NAVY if ch == "N" else rgb(key[ch])


def dialogue_frame(spec, slice_px=14, edge=16):
    light, body, dark = (rgb(c) for c in spec["band"])
    rail = [rgb(c) for c in spec["rail"]]
    piping = rgb(spec["piping"])

    def band(u, m):
        if m in (0, 4, 10):
            return NAVY
        if m < 4:
            return rail[0] if (u + m) % 8 < 4 else rail[1]
        if m < 10:
            if m == 6 + SCALLOP[u % 8]:
                return piping
            return light if m == 5 else dark if m == 9 else body
        return CREAM

    n = slice_px * 2 + edge
    im = Image.new("RGBA", (n, n), CLEAR)
    for y in range(n):
        for x in range(n):
            dx, dy = min(x, n - 1 - x), min(y, n - 1 - y)
            m = min(dx, dy)
            u = x if dy <= dx else y
            if dx < slice_px and dy < slice_px:        # a corner: the piece, upright, over the bands
                lx = x if x < slice_px else x - (n - slice_px)
                ly = y if y < slice_px else y - (n - slice_px)
                piece = corner_piece(spec["corner"], lx, ly, slice_px)
                if piece:
                    im.putpixel((x, y), piece)
                elif dx + dy >= slice_px - 5:
                    im.putpixel((x, y), band(u, m))
            else:
                im.putpixel((x, y), band(u, m))
    return im


def nameplate(spec, slice_px=7, edge=8):
    light, body, dark = (rgb(c) for c in spec["body"])
    rim = [rgb(c) for c in spec["rim"]]
    dots = rgb(spec["dots"])

    def band(u, m):
        if m in (0, 3):
            return NAVY
        if m < 3:
            return rim[0] if (u + m) % 4 < 2 else rim[1]
        if m == 5 and u % 4 < 2:
            return dots
        return light if m == 4 else body if m < 7 else dark   # the lettering sits on the darker centre

    n = slice_px * 2 + edge
    im = Image.new("RGBA", (n, n), CLEAR)
    for y in range(n):
        for x in range(n):
            dx, dy = min(x, n - 1 - x), min(y, n - 1 - y)
            if dx + dy < 2:                            # nibbled corners, as on the candy plate
                continue
            im.putpixel((x, y), band(x if dy <= dx else y, min(dx, dy)))
    return im


INTERFACE = ["ui-dialogue-frame", "ui-nameplate"]


# ---------------------------------------------------------------- kits

def still(w=32, h=32):
    return dict(w=w, h=h, frames=1, duration=0, loop=False)


def anim(frames, duration, w=32, h=32):
    return dict(w=w, h=h, frames=frames, duration=duration, loop=True)


LABELS = {"halloween": "Halloween", "valentines": "Valentine's Day", "easter": "Easter", "summer": "Summer"}

# Where the three clouds rest, in background pixels (candy: 33,22 / 221,25 / 81,53). Each
# season keeps them in open sky, clear of whatever stands in front.
CLOUDS = {
    "halloween": [(33, 22), (150, 34), (81, 56)],
    "valentines": [(33, 22), (262, 20), (118, 28)],
    "easter": [(24, 30), (118, 6), (175, 24)],
    "summer": [(33, 22), (221, 25), (81, 53)],
}

# Props: PixelLab stills. A plain name is a 32x32 prop saved under its raw name; a tuple is
# (raw name, sprite name, frame width, frame height).
PROPS = {
    "halloween": ["prop-pumpkin", "prop-tombstone", "prop-cauldron", "prop-witch-hat", "prop-black-cat"],
    "valentines": ["prop-teddy", "prop-gift", "prop-rose", "prop-heart-lock", "prop-chocolates", "prop-love-letter"],
    "easter": ["prop-basket", "prop-tulip", "prop-daffodil", "prop-chick", "prop-carrot",
               ("fx-butterfly-base", "prop-butterfly", 32, 32)],
    "summer": [("prop-palm", "prop-palm", 48, 64), ("prop-umbrella", "prop-umbrella", 48, 48), "prop-lawn-chair",
               "prop-shell", "prop-starfish", "prop-life-ring", "prop-watermelon", "prop-drink",
               ("fx-dolphin-base", "prop-dolphin", 48, 32)],
}

# The moving pieces in the hero scene. x and y are the sprite's top left in background pixels.
# scale: which of the scene's two pixel sizes it is drawn at, "bg" or "character".
# layer: "back" sits behind the season's foreground layer, "front" in front of it.
# motion: still | hover (a small loop in place)
#         | drift (crosses the sky as the clouds do, `seconds` per crossing, `to` left or right;
#           x is where it rests when animation is off, and where it starts)
#         | stride (crosses the ground from x to x2, moving `stride` sprite pixels on each loop of
#           its strip; the strip carries the travel within a loop, so nothing slides. `rest` is
#           where it stands when animation is off)
#         | patrol (walks from x to x2 and back, one sprite pixel per frame)
# low: another x for the dialogue hero on phones. Its stage there is a short strip of the foot of
#      the painting, and the site brings a drifting piece down to the highest row in view, never
#      below the ground. (From laptops up the dialogue lies over the whole scene and x is used.)
AMBIENT = {
    "halloween": [
        # The bats fly behind the house, the trees and the gravestone (fg-hero), so where each
        # one rests with animation off has to be open sky: across the moon, between the left
        # tree's branches and the moon, and high in the clear. Where the top of the painting is
        # out of view the high ones come down to the same row, so their columns keep them apart.
        # The phone's short strip has open sky for two; the third waits off its left edge.
        dict(sheet="fx-bat", x=232, y=30, scale="character", layer="back", motion="drift", to="left", seconds=26),
        dict(sheet="fx-bat", x=128, y=58, low=dict(x=-60), scale="character", layer="back", motion="drift", to="right", seconds=34),
        dict(sheet="fx-bat", x=176, y=12, scale="character", layer="back", motion="drift", to="left", seconds=44),
        # over the lit pumpkin, clear of both heroes' text and controls; in front of the fence,
        # which is foreground now that the bats pass behind all the scenery
        dict(sheet="fx-ghost", x=204, y=126, scale="character", layer="front", motion="still"),
        dict(sheet="fx-pumpkin", x=206, y=149, scale="character", layer="front", motion="still"),
    ],
    "valentines": [
        # His strip holds the whole turn: aim, shot, strike and the burst of hearts. In the
        # dialogue hero he starts further left (`low`), clear of the controls and the portrait.
        dict(sheet="fx-cupid", x=196, y=26, low=dict(x=100), scale="character", layer="back",
             motion="drift", to="right", seconds=38),
        dict(sheet="fx-heart", x=104, y=82, scale="character", layer="back", motion="hover"),
        dict(sheet="fx-heart", x=262, y=104, scale="character", layer="back", motion="hover", delay=-0.4),
    ],
    "easter": [
        dict(sheet="fx-bunny", x=-40, y=149, x2=344, rest=108, scale="character", layer="front", motion="stride", stride=16),
        dict(sheet="fx-butterfly", x=34, y=126, scale="character", layer="front", motion="hover"),
        dict(sheet="fx-butterfly", x=300, y=118, scale="character", layer="front", motion="hover", delay=-1.3),
    ],
    "summer": [
        dict(sheet="fx-wave", x=0, y=124, scale="bg", layer="back", motion="still"),
        dict(sheet="fx-dolphin", x=118, y=108, scale="bg", layer="back", motion="still"),
        dict(sheet="fx-dolphin", x=196, y=110, scale="bg", layer="back", motion="still", delay=-1.6, flipped=True),
        dict(sheet="fx-crab", x=96, y=149, x2=150, scale="character", layer="front", motion="patrol"),
    ],
}

# What paces the Experience road in each season, there and back. It has to look right going
# both ways, so the bunny, which faces one way, stays in the hero.
ROAD_WALKERS = {"halloween": ["fx-ghost"], "valentines": ["fx-heart"], "easter": ["fx-butterfly"], "summer": ["fx-crab"]}


def kit(season, base, out, bg):
    """Props and moving pieces for one season. Returns {sprite name: sheet facts}."""
    sheets = {}

    def raw(name):
        return Image.open(os.path.join(base, "raw", name + ".png")).convert("RGBA")

    def put(name, im, facts):
        assert im.size == (facts["w"] * facts["frames"], facts["h"]), (name, im.size, facts)
        im.save(os.path.join(out, name + ".png"))
        sheets[name] = facts

    for item in PROPS[season]:
        src, name, w, h = (item, item, 32, 32) if isinstance(item, str) else item
        im, removed = fx.prop(raw(src), w, h)
        if name == "prop-pumpkin":
            im = fx.mirror_below(im, 10)           # the face and body exact; the stem keeps its lean
        put(name, im, still(w, h))
        if removed:
            print(f"  {name}: removed a {removed} pixel shadow")

    if season == "halloween":
        bat, _ = fx.prop(raw("fx-bat-base"), symmetric=True)
        put("fx-bat", fx.strip(fx.flap(fx.shifted(bat, 0, -8))), anim(4, 0.5))
        ghost, _ = fx.prop(raw("fx-ghost-base"), symmetric=True)
        put("fx-ghost", fx.strip(fx.bob(fx.shifted(ghost, 0, -3))), anim(4, 1.4))
        pumpkin = Image.open(os.path.join(out, "prop-pumpkin.png")).convert("RGBA")
        put("fx-pumpkin", fx.strip(fx.flicker(pumpkin)), anim(4, 0.9))
    elif season == "valentines":
        put("fx-heart", fx.strip(fx.heart_pulse()), anim(4, 0.9, 16, 16))
        put("fx-heart-arrow", fx.heart_arrow(), still(24, 9))
        cupid = fx.cupid_act(os.path.join(base, "raw", "cupid2-anim-a"))
        put("fx-cupid", fx.strip(cupid), anim(len(cupid), 2.4, cupid[0].width, cupid[0].height))
    elif season == "easter":
        for name, spec in fx.EGGS.items():
            put(name, fx.egg(*spec), still())
        bunny, _ = fx.prop(raw("fx-bunny-base"))
        put("fx-bunny", fx.strip(fx.hop_across(bunny)), anim(6, 0.72, 48, 32))
        put("fx-butterfly", fx.strip(fx.butterfly()), anim(4, 0.5, 16, 16))
    elif season == "summer":
        frames, _ = fx.waves(bg)
        put("fx-wave", fx.strip(frames), anim(4, 2.4, frames[0].width, frames[0].height))
        leap = fx.dolphin()
        put("fx-dolphin", fx.strip(leap), anim(len(leap), 3.2, leap[0].width, leap[0].height))
        crab, _ = fx.prop(raw("fx-crab-base"), symmetric=True)
        put("fx-crab", fx.strip(fx.scuttle(crab)), anim(4, 0.5))
    return sheets


# ---------------------------------------------------------------- build

REPLACES = ["bg-hero", "bg-cloud-1", "bg-cloud-2", "bg-cloud-3", "prop-cloud", "prop-flag",
            "tile-road-straight", "tile-road-corner", "tile-road-faded"]

# Luz herself, in the scene's outfit: every strip the site plays, the two stills and the
# waist-up portrait. They are made by outfits.py, wardrobe.py and portraits.py in
# outfits/<scene>/; outfits/source holds the orange hoodie she was first drawn in.
CHARACTER = ["luz-base-front", "luz-side-right", "luz-idle", "luz-wave", "luz-walk", "luz-walk-down", "luz-walk-up",
             "luz-hop", "luz-emote-wow", "luz-emote-grin", "luz-emote-happy", "luz-emote-starry", "luz-emote-student",
             "luz-emote-cheer", "luz-portrait"]


def wear(root, scene, dest):
    """Put a scene's outfit in its folder, each piece checked against the one it was made from."""
    for name in CHARACTER:
        src = os.path.join(root, "outfits", scene, name + ".png")
        first = Image.open(os.path.join(root, "outfits", "source", name + ".png"))
        assert Image.open(src).size == first.size, f"{scene}/{name} is not the size of the original"
        shutil.copyfile(src, os.path.join(dest, name + ".png"))


def publish(root, season, out, candy):
    """Copy a season's finished pieces beside the candy kit, with Luz in the season's outfit,
    checking each on the way: hard-edged alpha, and the same size as any candy piece it replaces."""
    dest = os.path.join(candy, "seasons", season)
    shutil.rmtree(dest, ignore_errors=True)
    shutil.copytree(out, dest)
    wear(root, season, dest)
    for name in sorted(os.listdir(dest)):
        im = Image.open(os.path.join(dest, name)).convert("RGBA")
        soft = sum(1 for a in im.getchannel("A").tobytes() if 0 < a < 255)
        assert not soft, f"{season}/{name} has {soft} soft-edged pixels"
        if name[:-4] in REPLACES + INTERFACE:
            assert im.size == Image.open(os.path.join(candy, name)).size, f"{season}/{name} is not the candy size"
    print(f"  {len(os.listdir(dest))} files -> {dest}")


def build(root, candy):
    manifest = {"default": "candy", "replaces": REPLACES, "interface": INTERFACE, "character": CHARACTER, "seasons": {}}
    for season in BACKGROUNDS:
        base = os.path.join(root, "seasons", season)
        out = os.path.join(base, "drawn")
        shutil.rmtree(out, ignore_errors=True)
        os.makedirs(out)
        bg, sky, ground, notes = background(season, os.path.join(base, "raw", "bg-a.png"))
        bg.save(os.path.join(out, "bg-hero.png"))
        front = fx.foreground(season, bg)
        if front:
            front.save(os.path.join(out, "fg-hero.png"))
        for i in (1, 2, 3):
            src = Image.open(os.path.join(candy, f"bg-cloud-{i}.png")).convert("RGBA")
            if season == "valentines" and i == 2:
                c = heart_cloud(src.width, src.height, WHITE, rgb("#f9c9d6"))
            else:
                c = cloud(src, CLOUD[season])
            c.save(os.path.join(out, f"bg-cloud-{i}.png"))
        puff = Image.open(os.path.join(candy, "prop-cloud.png")).convert("RGBA")
        recolour(puff, {"#ffffff": PUFF[season][0], "#e7d9c8": PUFF[season][1]}).save(os.path.join(out, "prop-cloud.png"))
        flag = Image.open(os.path.join(candy, "prop-flag.png")).convert("RGBA")
        recolour(flag, dict(zip(FLAG_CANDY, FLAG[season]))).save(os.path.join(out, "prop-flag.png"))
        road = ROADS[season]
        s = road.straight()
        s.save(os.path.join(out, "tile-road-straight.png"))
        road.corner().save(os.path.join(out, "tile-road-corner.png"))
        faded(s).save(os.path.join(out, "tile-road-faded.png"))
        dialogue_frame(UI[season]).save(os.path.join(out, "ui-dialogue-frame.png"))
        nameplate(UI[season]["plate"]).save(os.path.join(out, "ui-nameplate.png"))
        print(season, "sky #%02x%02x%02x" % sky, "ground #%02x%02x%02x" % ground, *notes)
        sheets = kit(season, base, out, bg)
        publish(root, season, out, candy)
        manifest["seasons"][season] = dict(
            label=LABELS[season],
            sky="#%02x%02x%02x" % sky,
            ground="#%02x%02x%02x" % ground,
            plate=UI[season]["plate"]["body"][2],
            foreground=bool(front),
            clouds=[dict(sheet=f"bg-cloud-{i + 1}", x=x, y=y) for i, (x, y) in enumerate(CLOUDS[season])],
            sprites=sheets,
            ambient=AMBIENT[season],
            roadWalkers=ROAD_WALKERS[season],
        )
    wear(root, "candy", candy)                      # the candy scene is the kit's own folder
    text = json.dumps(manifest, indent=2)
    with open(os.path.join(candy, "seasons", "manifest.json"), "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
    with open(os.path.join(root, "preview", "seasons-data.js"), "w", encoding="utf-8", newline="\n") as f:
        f.write("// Written by tools/seasons.py: the same data as public/sprites/seasons/manifest.json.\n")
        f.write("window.SEASONS = " + text + ";\n")
    return manifest


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
