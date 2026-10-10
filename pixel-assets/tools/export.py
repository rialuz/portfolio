"""Assemble the final kit: named sprites, horizontal strips, and animated previews.

usage: export.py <pixel-assets dir> <sprites out dir>
"""
import colorsys
import os
import shutil
import sys

from PIL import Image

from skin import lighten

CANVAS, FEET = 64, 61
BLUSH = (251, 233, 229)
CHEEK_REDS = {(200, 74, 65), (183, 67, 61), (181, 49, 62)}
FACE_ROWS = range(26, 42)


def load(*parts):
    return Image.open(os.path.join(*parts)).convert("RGBA")


def frames(folder, indices):
    return [load(folder, f"frame_{i:02d}.png") for i in indices]


def on_baseline(im):
    """Re-seat a sprite so its feet rest on the shared baseline row."""
    out = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    out.paste(im, (0, FEET - (im.getbbox()[3] - 1)), im)
    return out


def is_skin(c):
    if not c[3]:
        return False
    h, s, v = colorsys.rgb_to_hsv(c[0] / 255, c[1] / 255, c[2] / 255)
    return 12 <= h * 360 <= 45 and s < 0.6 and v > 0.75


def no_blush(im):
    """Side view: PixelLab adds a red cheek pixel or two while animating. Paint them skin."""
    out = im.copy()
    fixed = 0
    for y in FACE_ROWS:
        for x in range(CANVAS):
            if im.getpixel((x, y))[:3] in CHEEK_REDS:
                near = [im.getpixel((x + dx, y + dy)) for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                        if 0 <= x + dx < CANVAS and (dx or dy)]
                skin = [c for c in near if is_skin(c)]
                if skin:
                    out.putpixel((x, y), max(set(skin), key=skin.count))
                    fixed += 1
    return out, fixed


def mirror(im):
    """Front view: copy the left half onto the right so the frame is symmetric to the pixel."""
    out = im.copy()
    for y in range(CANVAS):
        for x in range(CANVAS // 2):
            out.putpixel((CANVAS - 1 - x, y), im.getpixel((x, y)))
    return out


def strip(images):
    w, h = images[0].size
    assert all(i.size == (w, h) for i in images)
    out = Image.new("RGBA", (w * len(images), h), (0, 0, 0, 0))
    for n, im in enumerate(images):
        out.paste(im, (n * w, 0))
    return out


def gif(images, path, ms, scale=4, loop=True):
    big = []
    for im in images:
        bg = Image.new("RGBA", im.size, BLUSH + (255,))
        bg.alpha_composite(im)
        big.append(bg.convert("RGB").resize((im.width * scale, im.height * scale), Image.NEAREST))
    if not loop:
        big = big + [big[-1]] * 6  # hold the rest pose so a one-shot reads as one-shot
    big[0].save(path, save_all=True, append_images=big[1:], duration=ms, loop=0)


def main():
    W, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    prev = os.path.join(W, "preview")
    raw = os.path.join(W, "raw")

    front = load(W, "final-wip", "luz-base-front.png")
    side = on_baseline(load(raw, "character", "rotations", "east.png"))
    front.save(os.path.join(out, "luz-base-front.png"))
    side.save(os.path.join(out, "luz-side-right.png"))

    walk = []
    for f in frames(os.path.join(raw, "anim", "walk", "clean"), range(1, 9)):
        f, n = no_blush(f)
        walk.append(f)
    hop = frames(os.path.join(raw, "anim", "hop", "clean"), range(1, 4)) + [side]
    celebrate = [mirror(f) for f in frames(os.path.join(raw, "anim", "celebrate", "clean"), range(1, 6))] + [front]
    anims = {
        "luz-idle": (frames(os.path.join(W, "final-wip", "idle"), range(4)), 420, True),
        "luz-wave": (frames(os.path.join(W, "final-wip", "wave"), range(6)), 150, False),
        "luz-walk": (walk, 100, True),
        "luz-hop": (hop, 110, False),
        "luz-celebrate": (celebrate, 110, False),
    }
    for name, (fs, ms, loop) in anims.items():
        assert all(f.size == (CANVAS, CANVAS) for f in fs), name
        strip(fs).save(os.path.join(out, name + ".png"))
        gif(fs, os.path.join(prev, name + ".gif"), ms, loop=loop)
        top = min(f.getbbox()[1] for f in fs)
        print(f"{name}.png  {len(fs)} frames  {CANVAS * len(fs)}x{CANVAS}  highest pixel row {top}")

    for name in ("prop-gumdrop", "prop-lollipop", "prop-candy-cane-sign", "prop-cloud"):
        shutil.copyfile(os.path.join(raw, "props", name + ".png"), os.path.join(out, name + ".png"))
    # code-built pieces: sparkle and flag strips, road tiles, and the background with its
    # three sky clouds lifted out into their own sprites
    for name in ("prop-sparkle", "prop-flag", "tile-road-straight", "tile-road-corner", "tile-road-faded",
                 "bg-hero", "bg-cloud-1", "bg-cloud-2", "bg-cloud-3"):
        shutil.copyfile(os.path.join(W, "drawn", name + ".png"), os.path.join(out, name + ".png"))

    # walk cycles for the vertical stretches of the road, built from the still front and back views
    for name in ("luz-walk-down", "luz-walk-up"):
        shutil.copyfile(os.path.join(W, "drawn", "walk", name + ".png"), os.path.join(out, name + ".png"))
        s = Image.open(os.path.join(out, name + ".png")).convert("RGBA")
        gif([s.crop((i * CANVAS, 0, (i + 1) * CANVAS, CANVAS)) for i in range(s.width // CANVAS)],
            os.path.join(prev, name + ".gif"), 100)

    # emotion strips for the journey stops, and their speech bubbles
    for name in sorted(os.listdir(os.path.join(W, "drawn", "emotes"))):
        shutil.copyfile(os.path.join(W, "drawn", "emotes", name), os.path.join(out, name))

    # dialogue hero: the detailed portrait from PixelLab, and the code-drawn frame pieces
    # hips-up, hands in her hoodie pocket. raw/portrait also holds a waving pose, a hand-on-hip
    # pose and the first close-up bust. PixelLab drew her skin darker than the small sprite's,
    # so skin.py lifts it to match.
    lighten(load(raw, "portrait", "waist", "frame_03.png")).save(os.path.join(out, "luz-portrait.png"))
    for name in sorted(os.listdir(os.path.join(W, "drawn", "ui"))):
        shutil.copyfile(os.path.join(W, "drawn", "ui", name), os.path.join(out, name))

    # Everything of Luz written above is in the orange hoodie she was first drawn in. That is
    # now her Halloween outfit and the source for the others: keep a copy for outfits.py,
    # wardrobe.py and portraits.py to work from. seasons.py then puts her candy-land outfit
    # in this folder and each season's in its own, so run those after this.
    wardrobe = os.path.join(W, "outfits", "source")
    os.makedirs(wardrobe, exist_ok=True)
    for name in sorted(os.listdir(out)):
        if name.startswith("luz-") and name.endswith(".png"):
            shutil.copyfile(os.path.join(out, name), os.path.join(wardrobe, name))

    # final check: sizes, hard-edged alpha, front-view symmetry
    for name in sorted(os.listdir(out)):
        if not name.endswith(".png"):            # the seasons folder lives here too
            continue
        im = Image.open(os.path.join(out, name)).convert("RGBA")
        semi = sum(1 for p in im.getdata() if 0 < p[3] < 255)
        note = ""
        if name in ("luz-base-front.png", "luz-idle.png", "luz-celebrate.png") or name.startswith("luz-emote-"):
            n = im.width // CANVAS
            bad = sum(1 for k in range(n) for y in range(CANVAS) for x in range(CANVAS // 2)
                      if im.getpixel((k * CANVAS + x, y)) != im.getpixel((k * CANVAS + CANVAS - 1 - x, y)))
            note = f"  asymmetric pixel pairs: {bad}"
        print(f"  {name:28s} {im.width}x{im.height}  semi-transparent pixels: {semi}{note}")


main()
