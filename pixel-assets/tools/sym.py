"""Exact left/right pixel symmetry for a front-facing sprite.

Finds the vertical axis (between two pixel columns) the sprite is most symmetric about,
mirrors one half onto the other, and centres that axis on the canvas.

usage: sym.py score <png>...
       sym.py make <src.png> <out.png> --keep left|right
"""
import argparse
import sys

from PIL import Image


def mismatch(px, w, h, k):
    """Pixels that differ from their mirror about the axis between columns k-1 and k."""
    bad = 0
    for y in range(h):
        for x in range(k):
            m = 2 * k - 1 - x
            a = px[x, y] if 0 <= x < w else (0, 0, 0, 0)
            b = px[m, y] if 0 <= m < w else (0, 0, 0, 0)
            if a[3] == 0 and b[3] == 0:
                continue
            if a != b:
                bad += 1
    return bad


def best_axis(im):
    w, h = im.size
    px = im.load()
    left, _, right, _ = im.getbbox()
    mid = (left + right) // 2
    scores = {k: mismatch(px, w, h, k) for k in range(max(1, mid - 4), min(w - 1, mid + 5))}
    k = min(scores, key=scores.get)
    return k, scores[k]


def make(src, out, keep):
    im = Image.open(src).convert("RGBA")
    w, h = im.size
    px = im.load()
    k, _ = best_axis(im)
    res = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    rp = res.load()
    half = w // 2
    for y in range(h):
        for d in range(half):  # d = distance from the axis, 0 is the column touching it
            sx = k - 1 - d if keep == "left" else k + d
            c = px[sx, y] if 0 <= sx < w else (0, 0, 0, 0)
            rp[half - 1 - d, y] = c
            rp[half + d, y] = c
    res.save(out)
    print(f"{out}: axis after col {k - 1}, kept {keep} half, residual mismatch {best_axis(res)[1]}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("score")
    p.add_argument("paths", nargs="+")
    p = sub.add_parser("make")
    p.add_argument("src")
    p.add_argument("out")
    p.add_argument("--keep", choices=["left", "right"], default="left")
    a = ap.parse_args()
    if a.cmd == "score":
        for path in a.paths:
            im = Image.open(path).convert("RGBA")
            k, bad = best_axis(im)
            print(f"{path}: best axis after col {k - 1}, {bad} mismatched pixel pairs")
    else:
        make(a.src, a.out, a.keep)


if __name__ == "__main__":
    sys.exit(main())
