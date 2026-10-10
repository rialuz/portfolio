"""Emotion animations for the journey stops, matching the wireframe's emotes:
o_o (wow), :D (grin), \\o/ (cheer), ^_^ (happy), *_* (starry).

Each is the base sprite with a new face, so hair and body are the base's own pixels, played
over the idle's breathing bob. Cheer also raises both arms, using the wave's arm mirrored.
A matching pixel speech bubble is drawn for each one (4-frame pop-in).

usage: emotes.py <base.png> <wave_frames_dir> <out_dir>
"""
import os
import sys

from PIL import Image

N = 64
SKIN, K, W = (240, 171, 123, 255), (0, 0, 0, 255), (254, 255, 254, 255)
MOUTH_DARK, MOUTH_RED, YELLOW = (70, 28, 27, 255), (159, 61, 54, 255), (255, 214, 90, 255)
PAL = {".": SKIN, "K": K, "W": W, "Y": YELLOW, "j": MOUTH_DARK, "r": MOUTH_RED}

# her right eye (viewer's left) occupies columns 25-29; each grid is mirrored onto the other eye
EYES = {
    "happy": (32, ["..K..", ".K.K.", "K...K", "....."]),            # ^ ^
    "wow": (31, [".KKK.", "KWWWK", "KWKWK", "KWWWK", ".KKK."]),      # o o
    "starry": (32, [".KKK.", "KKYKK", "KYWYK", ".KYK."]),            # * *
    "starry2": (32, [".KKK.", "KYKYK", "KKWKK", ".YKY."]),           # twinkle
}
# mouths are drawn across columns 30-33 (already symmetric)
MOUTHS = {
    "smile": (37, ["j..j", ".rr."]),
    "open": (37, ["jjjj", "jrrj", ".jj."]),
    "o": (37, [".jj.", ".jj."]),
}
SPLIT = 55  # rows above this bob with the breath; the legs stay planted


def bob(im, dy=1):
    out = im.copy()
    top = im.crop((0, 0, N, SPLIT))
    out.paste((0, 0, 0, 0), (0, 0, N, SPLIT))
    out.alpha_composite(top, (0, dy))
    return out


def face(im, eyes=None, mouth=None, brows_up=False):
    out = im.copy()
    if eyes:
        top, grid = EYES[eyes]
        for y in range(31, 36):                       # wipe the old eye first
            for x in range(25, 30):
                out.putpixel((x, y), SKIN)
                out.putpixel((N - 1 - x, y), SKIN)
        for dy, row in enumerate(grid):
            for dx, ch in enumerate(row):
                out.putpixel((25 + dx, top + dy), PAL[ch])
                out.putpixel((N - 1 - (25 + dx), top + dy), PAL[ch])
    if brows_up:
        for x in (28, 29, 34, 35):
            out.putpixel((x, 29), out.getpixel((x, 30)))
            out.putpixel((x, 30), SKIN)
    if mouth:
        top, grid = MOUTHS[mouth]
        for x in (31, 32):
            out.putpixel((x, 38), SKIN)               # wipe the resting mouth
        for dy, row in enumerate(grid):
            for dx, ch in enumerate(row):
                out.putpixel((30 + dx, top + dy), PAL[ch])
    return out


# ---- the student look for the Apprentice stop -----------------------------------------------
BEZEL, SCREEN, DECK, KEYS = (44, 50, 62, 255), (96, 170, 230, 255), (206, 210, 218, 255), (150, 156, 168, 255)
PAPER_Y, RULE, SPIRAL = (250, 214, 96, 255), (214, 160, 60, 255), (58, 33, 26, 255)


def student(base, typing=True):
    """An open laptop held in one hand, its screen toward us showing a line of code, and a
    spiral notepad in the other. Both hang from her hands, which stay in front of them, so
    each one reads as held. Her face keeps the base eyes, with a small smile."""
    im = face(base, mouth="smile")

    def opaque(x, y):
        return base.getpixel((x, y))[3] != 0

    # open laptop held by her right hand (viewer's left). Her hand, cuff and sleeve stay in
    # front of its right edge; the tips of her hair sit behind it.
    for y in range(46, 55):
        for x in range(11, 24):
            if opaque(x, y) and (x >= 23 or (x == 22 and y >= 50)):
                continue
            if y == 54:
                c = KEYS                                  # keyboard deck, seen edge-on
            elif 12 <= x <= 22 and (x in (12, 22) or y in (46, 53)):
                c = BEZEL
            elif 13 <= x <= 21:
                c = SCREEN
            else:
                continue
            im.putpixel((x, y), c)
    code = [(15, 47), (14, 48), (15, 49), (19, 47), (20, 48), (19, 49),   # < > on the first line
            (14, 51), (15, 51), (17, 51)]                                 # __ . on the second
    if typing:
        code.append((19, 51))                                             # the next character
    for x, y in code:
        im.putpixel((x, y), W)

    # spiral notepad hanging from her left hand (viewer's right)
    for y in range(48, 55):
        for x in range(40, 48):
            if opaque(x, y) and x <= 41:
                continue
            if x in (40, 47) or y in (48, 54):
                c = K
            elif y == 49:
                c = SPIRAL if x % 2 else DECK
            elif y in (51, 53) and 42 <= x <= 45:
                c = RULE
            else:
                c = PAPER_Y
            im.putpixel((x, y), c)
    return im


def mirror(im):
    out = im.copy()
    for y in range(N):
        for x in range(N // 2):
            out.putpixel((N - 1 - x, y), im.getpixel((x, y)))
    return out


def strip(frames):
    w, h = frames[0].size
    out = Image.new("RGBA", (w * len(frames), h), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        out.paste(f, (i * w, 0))
    return out


# ---- speech bubbles -------------------------------------------------------------------------
NAVY, PAPER, CORAL = (35, 48, 77, 255), (255, 255, 255, 255), (198, 95, 78, 255)
GLYPHS = {
    "o": ["...", "...", "###", "#.#", "###"], "_": ["...", "...", "...", "...", "###"],
    "^": [".#.", "#.#", "...", "...", "..."], "*": ["...", ".#.", "###", ".#.", "..."],
    ":": ["...", ".#.", "...", ".#.", "..."], "D": ["##.", "#.#", "#.#", "#.#", "##."],
    "\\": ["#..", "#..", ".#.", "..#", "..#"], "/": ["..#", "..#", ".#.", "#..", "#.."],
}


def bubble(text, w, h, lift=0, size=32):
    """White speech bubble with a navy outline and a small tail, its tip resting on row 30."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    x0, y1 = (size - w) // 2, 27 - lift          # y1 = bottom row of the box
    y0 = y1 - h + 1
    for y in range(y0, y1 + 1):
        for x in range(x0, x0 + w):
            corner = (x in (x0, x0 + w - 1)) and (y in (y0, y1))
            if corner:
                continue
            edge = x in (x0, x0 + w - 1) or y in (y0, y1)
            im.putpixel((x, y), NAVY if edge else PAPER)
    cx = size // 2
    for i, row in enumerate(("#..#", ".##.")):    # tail under the middle of the box
        for j, ch in enumerate(row):
            px = (cx - 2 + j, y1 + 1 + i)
            im.putpixel(px, NAVY if ch == "#" else PAPER)
    for j in (1, 2):
        im.putpixel((cx - 2 + j, y1), PAPER)       # open the box into the tail
    if text:
        tw = len(text) * 3 + (len(text) - 1)
        gx, gy = (size - tw) // 2, y0 + (h - 5) // 2
        for n, ch in enumerate(text):
            for r, row in enumerate(GLYPHS[ch]):
                for c, bit in enumerate(row):
                    if bit == "#":
                        im.putpixel((gx + n * 4 + c, gy + r), CORAL if ch == "*" else NAVY)
    return im


def bubble_strip(text):
    return strip([bubble("", 7, 5), bubble("", 13, 9), bubble(text, 19, 13, lift=1), bubble(text, 19, 13)])


def main():
    base = Image.open(sys.argv[1]).convert("RGBA")
    wave_dir, out = sys.argv[2], sys.argv[3]
    os.makedirs(out, exist_ok=True)

    def breathing(a, b=None):
        b = b or a
        return [a, bob(a), b, bob(b)]

    happy = face(base, eyes="happy", mouth="smile")
    wow = face(base, eyes="wow", mouth="o", brows_up=True)
    grin = face(base, mouth="open")
    starry, starry2 = face(base, eyes="starry", mouth="open"), face(base, eyes="starry2", mouth="open")
    up, out_ = (Image.open(os.path.join(wave_dir, f"pose_{p}.png")).convert("RGBA") for p in ("in", "out"))
    # both arms: the raised arm's half mirrored onto the right, then the happy face. It loops and
    # starts with her arms up, so with animation off the still is the cheer itself.
    cheer = [face(mirror(pose), eyes="happy", mouth="open") for pose in (up, out_, up, out_, up, out_)]

    sets = {"wow": breathing(wow), "grin": breathing(grin), "cheer": cheer, "happy": breathing(happy),
            "starry": breathing(starry, starry2),
            "student": breathing(student(base), student(base, typing=False))}   # the last character blinks
    texts = {"wow": "o_o", "grin": ":D", "cheer": "\\o/", "happy": "^_^", "starry": "*_*"}
    for name, frames in sets.items():
        strip(frames).save(os.path.join(out, f"luz-emote-{name}.png"))
        if name in texts:
            bubble_strip(texts[name]).save(os.path.join(out, f"emote-{name}.png"))
        bad = sum(1 for f in frames for y in range(N) for x in range(N // 2) if f.getpixel((x, y)) != f.getpixel((N - 1 - x, y)))
        print(f"luz-emote-{name}.png {len(frames)} frames, asymmetric pixel pairs {bad}")


if __name__ == "__main__":
    main()
