"""Ask PixelLab to dress animation frames in the outfit shown on a reference still.

Frames are cut from horizontal strips of 64x64 cells. The answer comes back as numbered
frames in the output folder, in the order the frames were given. One call holds up to 15
frames. Logged to the ledger like every other call.

usage: transfer.py <reference.png> <out_dir> <instructions> <strip.png>[:first-last] [...]
"""
import base64
import io
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pl  # noqa: E402

CELL = 64


def b64(im):
    buf = io.BytesIO()
    im.save(buf, "PNG")
    return {"type": "base64", "base64": base64.b64encode(buf.getvalue()).decode(), "format": "png"}


def cells(spec):
    path, _, span = spec.partition(":") if spec.count(":") == 1 and not spec[1:3] == ":/" else (spec, "", "")
    if spec[1:3] in (":/", ":\\"):                     # a Windows drive letter, then perhaps a span
        head, _, tail = spec[2:].partition(":")
        path, span = spec[:2] + head, tail
    strip = Image.open(path).convert("RGBA")
    count = strip.width // CELL
    first, last = (int(v) for v in span.split("-")) if span else (0, count - 1)
    return [strip.crop((i * CELL, 0, (i + 1) * CELL, CELL)) for i in range(first, last + 1)]


def main():
    reference, out, instructions = sys.argv[1], sys.argv[2], sys.argv[3]
    frames = [f for spec in sys.argv[4:] for f in cells(spec)]
    assert 2 <= len(frames) <= 15, len(frames)
    size = {"width": CELL, "height": CELL}
    body = {
        "reference_image": {"image": b64(Image.open(reference).convert("RGBA")), "size": size},
        "frames": [{"image": b64(f), "size": size} for f in frames],
        "image_size": size,
        "no_background": True,
        "additional_instructions": instructions,
        "seed": 7001,
    }
    return pl.run("/transfer-outfit-v2", body, out, is_job=True, note=f"{len(frames)} frames")


if __name__ == "__main__":
    sys.exit(main())
