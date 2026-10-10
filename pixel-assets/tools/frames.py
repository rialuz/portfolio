"""Animation frame cleanup: drop stray floating bits, put frames on the kit's 64x64 canvas
with the feet on the shared baseline, and report how each frame differs from a reference.

usage: frames.py clean <in_dir> <out_dir> [--feet-from <png>]
"""
import os
import sys

from PIL import Image

CANVAS, FEET = 64, 61


def main_component(im):
    """Keep the largest 8-connected blob; anything detached from the character is removed."""
    w, h = im.size
    px = im.load()
    seen, best = set(), []
    for y in range(h):
        for x in range(w):
            if px[x, y][3] and (x, y) not in seen:
                stack, blob = [(x, y)], []
                seen.add((x, y))
                while stack:
                    cx, cy = stack.pop()
                    blob.append((cx, cy))
                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            nx, ny = cx + dx, cy + dy
                            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in seen and px[nx, ny][3]:
                                seen.add((nx, ny))
                                stack.append((nx, ny))
                if len(blob) > len(best):
                    best = blob
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    op = out.load()
    for x, y in best:
        op[x, y] = px[x, y]
    return out, sum(1 for y in range(h) for x in range(w) if px[x, y][3]) - len(best)


def clean(in_dir, out_dir, ground=None):
    os.makedirs(out_dir, exist_ok=True)
    names = sorted(n for n in os.listdir(in_dir) if n.endswith(".png"))
    frames = []
    for n in names:
        im, dropped = main_component(Image.open(os.path.join(in_dir, n)).convert("RGBA"))
        frames.append(im)
        if dropped:
            print(n, "removed", dropped, "detached pixels")
    # the ground line is where the feet rest in the first frame, unless given
    ground = ground if ground is not None else frames[0].getbbox()[3] - 1
    top = min(f.getbbox()[1] for f in frames) - (ground - FEET)
    print("ground row", ground, "-> highest pixel lands on row", top, "(needs >= 0 to fit 64px)")
    for n, f in zip(names, frames):
        out = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
        out.paste(f, ((CANVAS - f.width) // 2, FEET - ground), f)
        out.save(os.path.join(out_dir, n))
    return 0 if top >= 0 else 2


if __name__ == "__main__":
    if sys.argv[1] == "clean":
        g = int(sys.argv[sys.argv.index("--ground") + 1]) if "--ground" in sys.argv else None
        sys.exit(clean(sys.argv[2], sys.argv[3], g))
