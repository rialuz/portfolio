"""Ask PixelLab's Pro generator for new pictures of the subject of a reference picture.

The reference is also given as the style picture, so pixel size and shading follow it. The
answer is several options, saved as numbered frames in the output folder. Logged to the
ledger like every other call.

usage: reference.py <reference.png> <out_dir> <seed> <what to keep> <description>
"""
import base64
import io
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pl  # noqa: E402


def main():
    reference, out, seed, keep, description = sys.argv[1:6]
    im = Image.open(reference).convert("RGBA")
    buf = io.BytesIO()
    im.save(buf, "PNG")
    image = {"type": "base64", "base64": base64.b64encode(buf.getvalue()).decode(), "format": "png"}
    size = {"width": im.width, "height": im.height}
    body = {
        "description": description,
        "image_size": size,
        "no_background": True,
        "seed": int(seed),
        "reference_images": [{"image": image, "size": size, "usage_description": keep}],
        "style_image": {"image": image, "size": size, "usage_description": "Pixel size, outline and shading style."},
    }
    return pl.run("/generate-image-v2", body, out, is_job=True, note=description[:80])


if __name__ == "__main__":
    sys.exit(main())
