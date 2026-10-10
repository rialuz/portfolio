"""Site images built from the kit: favicon set (the pixel heart from the wireframe logo) and
the 1200x630 link-preview image (the hero scene with Luz waving).

usage: site_images.py <sprites_dir> <public_dir>
"""
import os
import sys

from PIL import Image

HEART = (0xE0, 0x7A, 0x5F, 255)     # the logo's own colours, read from the wireframe
SHINE = (0xFF, 0xF7, 0xEE, 255)
CREAM = (0xFF, 0xF7, 0xEE, 255)
NAVY = (0x23, 0x30, 0x4D, 255)
WHITE = (255, 255, 255, 255)
ROWS = [".##.##.", "#######", "#######", ".#####.", "..###..", "...#..."]   # 7x6, as in the wireframe


def heart(scale):
    im = Image.new("RGBA", (7, 6), (0, 0, 0, 0))
    for y, row in enumerate(ROWS):
        for x, ch in enumerate(row):
            if ch == "#":
                im.putpixel((x, y), HEART)
    im.putpixel((1, 1), SHINE)
    return im.resize((7 * scale, 6 * scale), Image.NEAREST)


def icon(size, scale, background=None):
    im = Image.new("RGBA", (size, size), background or (0, 0, 0, 0))
    h = heart(scale)
    im.alpha_composite(h, ((size - h.width) // 2, (size - h.height) // 2))
    return im


# 3x5 pixel letters for the speech bubble (m is 5 wide)
FONT = {
    "H": ["#.#", "#.#", "###", "#.#", "#.#"], "i": [".#.", "...", ".#.", ".#.", ".#."],
    ",": ["...", "...", "...", "...", ".#.", "#.."], "I": ["###", ".#.", ".#.", ".#.", "###"],
    "'": [".#.", ".#.", "...", "...", "..."], "m": [".....", ".....", "##.#.", "#.#.#", "#.#.#"],
    "L": ["#..", "#..", "#..", "#..", "###"], "u": ["...", "...", "#.#", "#.#", "###"],
    "z": ["...", "...", "###", ".#.", "###"], "!": [".#.", ".#.", ".#.", "...", ".#."],
}


def text(words):
    width = sum(2 if ch == " " else len(FONT[ch][0]) + 1 for ch in words) - 1
    im = Image.new("RGBA", (width, 6), (0, 0, 0, 0))             # five rows of letter, one for the comma's tail
    x = 0
    for ch in words:
        if ch == " ":
            x += 2
            continue
        for r, row in enumerate(FONT[ch]):
            for c, bit in enumerate(row):
                if bit == "#":
                    im.putpixel((x + c, r), NAVY)
        x += len(FONT[ch][0]) + 1
    return im


def bubble(words, pad=4):
    """Speech bubble in background pixels: white box, navy border, hard shadow, small tail."""
    t = text(words)
    w, h = t.width + 2 * pad + 2, t.height + 2 * pad + 2
    im = Image.new("RGBA", (w + 1, h + 4), (0, 0, 0, 0))
    for y in range(h):
        for x in range(w):
            if (x in (0, w - 1)) and (y in (0, h - 1)):
                continue
            edge = x in (0, w - 1) or y in (0, h - 1)
            im.putpixel((x, y), NAVY if edge else WHITE)
    for y in range(1, h):                      # one-pixel hard shadow, right and below
        im.putpixel((w, y), NAVY)
    cx = w // 2
    for i, row in enumerate(("#..#", ".##.")):
        for j, ch in enumerate(row):
            im.putpixel((cx - 2 + j, h + i), NAVY if ch == "#" else WHITE)
    for j in (1, 2):
        im.putpixel((cx - 2 + j, h - 1), WHITE)
    im.alpha_composite(t, (pad + 1, pad + 1))
    return im


def og(sprites, out_path):
    W, H, bg_scale, luz_scale = 1200, 630, 4, 3
    bg = Image.open(os.path.join(sprites, "bg-hero.png")).convert("RGBA")
    big = bg.resize((bg.width * bg_scale, bg.height * bg_scale), Image.NEAREST)
    x0, y0 = (big.width - W) // 2, 110          # keeps the frosting ground and a strip of its face
    scene = big.crop((x0, y0, x0 + W, y0 + H))

    def place(im, scale, x, y):
        im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
        scene.alpha_composite(im, (x, y))

    for name, x, y in (("bg-cloud-1.png", 120, 48), ("bg-cloud-2.png", 800, 28), ("bg-cloud-3.png", 300, 168)):
        place(Image.open(os.path.join(sprites, name)).convert("RGBA"), bg_scale, x, y)
    wave = Image.open(os.path.join(sprites, "luz-wave.png")).convert("RGBA").crop((128, 0, 192, 64))   # arm up
    ground = 173 * bg_scale - y0                # feet rest on background row 172
    luz_x = 950 - x0
    place(wave, luz_scale, luz_x, ground + 2 * luz_scale - 64 * luz_scale)
    b = bubble("Hi, I'm Luz!")
    bw = b.width * bg_scale
    place(b, bg_scale, luz_x + 96 - bw // 2, ground - 46 * luz_scale - b.height * bg_scale - 8)
    scene.convert("RGB").save(out_path)
    print("og-image.png", scene.size)


def main():
    sprites, public = sys.argv[1], sys.argv[2]
    icon(16, 2).save(os.path.join(public, "icon-16.png"))
    icon(32, 4).save(os.path.join(public, "icon-32.png"))
    icon(192, 24).save(os.path.join(public, "icon-192.png"))
    icon(180, 20, CREAM).save(os.path.join(public, "apple-touch-icon.png"))
    icon(48, 6).save(os.path.join(public, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    print("favicon.ico, icon-16.png, icon-32.png, icon-192.png, apple-touch-icon.png")
    og(sprites, os.path.join(public, "og-image.png"))


main()
