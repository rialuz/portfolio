"""Ask PixelLab to redraw one area of a picture and leave the rest alone.

The mask is white where it may draw and black where the picture must stay. This uses the
plain /inpaint endpoint (pictures up to 200x200): the Pro one, /inpaint-v3, is not open to
this account. Logged to the ledger like every other call.

usage: inpaint.py <image.png> <mask.png> <out.png> <seed> <description of the whole picture>
"""
import base64
import io
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pl  # noqa: E402


def b64(im):
    buf = io.BytesIO()
    im.save(buf, "PNG")
    return {"type": "base64", "base64": base64.b64encode(buf.getvalue()).decode(), "format": "png"}


def main():
    image, mask, out, seed, description = sys.argv[1:6]
    im = Image.open(image).convert("RGBA")
    body = {
        "description": description,
        "image_size": {"width": im.width, "height": im.height},
        "inpainting_image": b64(im),
        "mask_image": b64(Image.open(mask).convert("RGB")),
        "no_background": True,
        "outline": "selective outline",
        "shading": "detailed shading",
        "detail": "highly detailed",
        "seed": int(seed),
    }
    return pl.run("/inpaint", body, out, note=description[:80])


if __name__ == "__main__":
    sys.exit(main())
