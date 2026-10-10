"""Pixel-art helpers: palette swatch, contact sheets, alpha cleanup, strips, info."""
import argparse
import os
import sys

from PIL import Image, ImageDraw

# The kit's nine colours, then supporting shades for shading, eyes and sandals.
KIT = ["#FBE9E5", "#FFF7EE", "#C65F4E", "#F7C6C0", "#EFC7A8", "#E9C29A", "#23304D", "#2A1E22", "#C99470"]
SHADES = ["#FFFFFF", "#A8714F", "#DDAA86", "#4A3238", "#8C5A3C", "#9C4638", "#E7D9C8", "#E8A49C",
          "#C99A6E", "#46557A"]


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def palette(out, extra=True):
    colors = KIT + (SHADES if extra else [])
    im = Image.new("RGB", (len(colors) * 4, 4))
    d = ImageDraw.Draw(im)
    for i, c in enumerate(colors):
        d.rectangle([i * 4, 0, i * 4 + 3, 3], fill=rgb(c))
    im.save(out)
    print("palette", len(colors), "colors ->", out)


def checker(w, h, cell=8, a=(236, 232, 238), b=(214, 208, 218)):
    im = Image.new("RGB", (w, h), a)
    d = ImageDraw.Draw(im)
    for y in range(0, h, cell):
        for x in range(0, w, cell):
            if (x // cell + y // cell) % 2:
                d.rectangle([x, y, x + cell - 1, y + cell - 1], fill=b)
    return im


def sheet(paths, out, scale=6, cols=4, bg="checker", labels=True):
    """Upscaled (nearest-neighbour) contact sheet so small sprites can be judged."""
    ims = [Image.open(p).convert("RGBA") for p in paths]
    cw = max(i.width for i in ims) * scale
    ch = max(i.height for i in ims) * scale
    pad, lab = 10, (18 if labels else 0)
    cols = min(cols, len(ims))
    rows = (len(ims) + cols - 1) // cols
    W = cols * (cw + pad) + pad
    H = rows * (ch + lab + pad) + pad
    canvas = Image.new("RGB", (W, H), (250, 244, 242))
    d = ImageDraw.Draw(canvas)
    for n, (p, im) in enumerate(zip(paths, ims)):
        x = pad + (n % cols) * (cw + pad)
        y = pad + (n // cols) * (ch + lab + pad)
        big = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
        cell = checker(cw, ch) if bg == "checker" else Image.new("RGB", (cw, ch), rgb(bg))
        cell.paste(big, ((cw - big.width) // 2, (ch - big.height) // 2), big)
        canvas.paste(cell, (x, y))
        if labels:
            d.text((x, y + ch + 3), os.path.basename(p), fill=(40, 40, 60))
    canvas.save(out)
    print("sheet", len(ims), "images ->", out, canvas.size)


def info(paths):
    for p in paths:
        im = Image.open(p)
        rgba = im.convert("RGBA")
        alphas = rgba.getchannel("A").getextrema()
        px = list(rgba.getdata())
        semi = sum(1 for q in px if 0 < q[3] < 255)
        opaque = [q[:3] for q in px if q[3] == 255]
        clear = sum(1 for q in px if q[3] == 0)
        print(f"{os.path.basename(p)}: {im.size} mode={im.mode} alpha={alphas} semi={semi} "
              f"transparent={clear} colors={len(set(opaque))} bbox={rgba.getbbox()}")


def clean_alpha(src, out, threshold=128):
    """Make every pixel fully opaque or fully transparent."""
    im = Image.open(src).convert("RGBA")
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            px[x, y] = (r, g, b, 255) if a >= threshold else (0, 0, 0, 0)
    im.save(out)
    print("clean_alpha ->", out)


def strip(paths, out):
    """Frames side by side, same size, no padding."""
    ims = [Image.open(p).convert("RGBA") for p in paths]
    w, h = ims[0].size
    assert all(i.size == (w, h) for i in ims), [i.size for i in ims]
    canvas = Image.new("RGBA", (w * len(ims), h), (0, 0, 0, 0))
    for n, im in enumerate(ims):
        canvas.paste(im, (n * w, 0))
    canvas.save(out)
    print("strip", len(ims), "frames ->", out, canvas.size)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("palette")
    p.add_argument("out")
    p.add_argument("--kit-only", action="store_true")
    p = sub.add_parser("sheet")
    p.add_argument("out")
    p.add_argument("paths", nargs="+")
    p.add_argument("--scale", type=int, default=6)
    p.add_argument("--cols", type=int, default=4)
    p.add_argument("--bg", default="checker")
    p = sub.add_parser("info")
    p.add_argument("paths", nargs="+")
    p = sub.add_parser("clean-alpha")
    p.add_argument("src")
    p.add_argument("out")
    p = sub.add_parser("strip")
    p.add_argument("out")
    p.add_argument("paths", nargs="+")
    a = ap.parse_args()
    if a.cmd == "palette":
        palette(a.out, extra=not a.kit_only)
    elif a.cmd == "sheet":
        sheet(a.paths, a.out, scale=a.scale, cols=a.cols, bg=a.bg)
    elif a.cmd == "info":
        info(a.paths)
    elif a.cmd == "clean-alpha":
        clean_alpha(a.src, a.out)
    elif a.cmd == "strip":
        strip(a.paths, a.out)


if __name__ == "__main__":
    sys.exit(main())
