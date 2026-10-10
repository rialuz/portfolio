"""Candy dialogue UI pieces, drawn in code so every edge tiles exactly.

- ui-dialogue-frame.png: 9-slice frame (slice 14px, edge tile 16px). From the outside in:
  candy-cane rail, gingerbread band with icing piping, then the cream writing area. A
  peppermint sits on each corner.
- ui-nameplate.png: 9-slice plate (slice 7px, edge tile 8px): a gingerbread cookie with a
  candy-cane rim and a row of icing dots.
- ui-continue.png: the "more to read" arrow. ui-pointer.png: the marker beside a choice.

usage: ui.py <out_dir>
"""
import math
import os
import sys

from PIL import Image

NAVY = (0x23, 0x30, 0x4D, 255)
CORAL = (0xC6, 0x5F, 0x4E, 255)
CREAM = (0xFF, 0xF7, 0xEE, 255)
WHITE = (255, 255, 255, 255)
GINGER = (0xB3, 0x6A, 0x3A, 255)
GINGER_LIGHT = (0xC9, 0x84, 0x50, 255)
GINGER_DARK = (0x8F, 0x4F, 0x2A, 255)
CLEAR = (0, 0, 0, 0)
SCALLOP = [0, 1, 1, 2, 2, 1, 1, 0]


def frame_band(u, m):
    """Colour at distance m in from the frame's outer edge, u along it."""
    if m in (0, 4, 10):
        return NAVY
    if m < 4:
        return CORAL if (u + m) % 8 < 4 else WHITE
    if m < 10:
        if m == 6 + SCALLOP[u % 8]:
            return CREAM
        return GINGER_LIGHT if m == 5 else GINGER_DARK if m == 9 else GINGER
    return CREAM


def peppermint(lx, ly, size):
    """A round peppermint filling a size x size corner; None outside the sweet."""
    c = (size - 1) / 2
    r = math.hypot(lx - c, ly - c)
    if r > size / 2:
        return None
    if r > size / 2 - 1.1:
        return NAVY
    if r < 1.2:
        return CORAL
    wedge = int((math.atan2(ly - c, lx - c) + math.pi) / (math.pi / 4)) % 2
    return CORAL if wedge else WHITE


def dialogue_frame(slice_px=14, edge=16):
    n = slice_px * 2 + edge
    im = Image.new("RGBA", (n, n), CLEAR)
    for y in range(n):
        for x in range(n):
            dx, dy = min(x, n - 1 - x), min(y, n - 1 - y)
            m = min(dx, dy)
            u = x if dy <= dx else y
            if dx < slice_px and dy < slice_px:        # a corner
                sweet = peppermint(dx, dy, slice_px)
                if sweet:
                    im.putpixel((x, y), sweet)
                elif dx + dy >= slice_px - 5:          # the bands run in under the sweet
                    im.putpixel((x, y), frame_band(u, m))
            else:
                im.putpixel((x, y), frame_band(u, m))
    return im


def plate_band(u, m):
    if m in (0, 3):
        return NAVY
    if m < 3:
        return CORAL if (u + m) % 4 < 2 else WHITE
    if m == 5 and u % 4 < 2:
        return CREAM                                   # piped icing dots
    return GINGER_LIGHT if m == 4 else GINGER if m < 7 else GINGER_DARK   # the lettering sits on the darker centre


def nameplate(slice_px=7, edge=8):
    n = slice_px * 2 + edge
    im = Image.new("RGBA", (n, n), CLEAR)
    for y in range(n):
        for x in range(n):
            dx, dy = min(x, n - 1 - x), min(y, n - 1 - y)
            if dx + dy < 2:                            # nibble the corners so it reads as a cookie
                continue
            im.putpixel((x, y), plate_band(x if dy <= dx else y, min(dx, dy)))
    return im


def glyph(rows, fill):
    """Pixel shape with a one-pixel navy outline around it."""
    h, w = len(rows), len(rows[0])
    im = Image.new("RGBA", (w + 2, h + 2), CLEAR)
    on = {(x + 1, y + 1) for y, row in enumerate(rows) for x, ch in enumerate(row) if ch == "#"}
    for x, y in on:
        im.putpixel((x, y), fill)
    for y in range(h + 2):
        for x in range(w + 2):
            if (x, y) not in on and any((x + dx, y + dy) in on for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                im.putpixel((x, y), NAVY)
    return im


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    dialogue_frame().save(os.path.join(out, "ui-dialogue-frame.png"))
    nameplate().save(os.path.join(out, "ui-nameplate.png"))
    glyph(["#######", ".#####.", "..###..", "...#..."], CORAL).save(os.path.join(out, "ui-continue.png"))
    glyph(["#....", "##...", "###..", "####.", "###..", "##...", "#...."], CORAL).save(os.path.join(out, "ui-pointer.png"))
    for name in sorted(os.listdir(out)):
        print(name, Image.open(os.path.join(out, name)).size)


main()
