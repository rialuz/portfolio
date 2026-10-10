"""Walk-down and walk-up cycles for the vertical stretches of the road.

PixelLab's own walk cycles changed the size of her head from frame to frame, so these are
built from its still views instead: the approved front sprite and the stored back view. The
head, hair and hoodie are the same pixels in every frame; only the legs step, the body sinks
one pixel as each foot lands, and the opposite hand swings.

usage: vwalk.py <front.png> <back_view.png> <out_dir>
"""
import os
import sys

from PIL import Image

N = 64
WAIST = 53                    # the black waist row; legs run from the row below to row 61
LEGS = {"left": (27, 31), "right": (32, 36)}     # viewer's left and right
HANDS = {"left": (22, 24), "right": (39, 41)}


def move_up(im, x0, x1, y0, y1, k):
    """Slide the block of columns x0..x1, rows y0..y1 up by k; the rows it leaves are cleared."""
    out = im.copy()
    block = im.crop((x0, y0, x1 + 1, y1 + 1))
    out.paste((0, 0, 0, 0), (x0, y0, x1 + 1, y1 + 1))
    out.paste(block, (x0, y0 - k))
    return out


def step(im, side, k, hand_rows):
    """Raise one foot by k pixels (the leg shortens from the top) and swing the opposite hand."""
    x0, x1 = LEGS[side]
    out = im.copy()
    leg = im.crop((x0, WAIST + 1 + k, x1 + 1, 62))
    out.paste((0, 0, 0, 0), (x0, WAIST + 1, x1 + 1, 62))
    out.paste(leg, (x0, WAIST + 1))
    hx0, hx1 = HANDS["right" if side == "left" else "left"]
    return move_up(out, hx0, hx1, hand_rows[0], hand_rows[1], 1)


def land(im):
    """Both feet down: everything above the legs sinks one pixel."""
    out = im.copy()
    upper = im.crop((0, 0, N, WAIST + 1))
    out.paste((0, 0, 0, 0), (0, 0, N, WAIST + 1))
    out.alpha_composite(upper, (0, 1))
    return out


def cycle(im, hand_rows):
    return [land(im), step(im, "left", 1, hand_rows), step(im, "left", 2, hand_rows), step(im, "left", 1, hand_rows),
            land(im), step(im, "right", 1, hand_rows), step(im, "right", 2, hand_rows), step(im, "right", 1, hand_rows)]


def back_view(front, north):
    """PixelLab drew the back view two pixels shorter with rough feet. Seat it so the waist
    lines up with the front view and give it the front view's legs, which look the same from
    behind: black trousers and shoes."""
    out = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    waist = max(y for y in range(N) if all(north.getpixel((x, y))[:3] == (0, 0, 0) and north.getpixel((x, y))[3]
                                           for x in range(28, 36)) and y < 56)
    upper = north.crop((0, 0, N, waist + 1))
    out.paste(upper, (0, WAIST - waist))
    legs = front.crop((LEGS["left"][0], WAIST + 1, LEGS["right"][1] + 1, 62))
    out.paste(legs, (LEGS["left"][0], WAIST + 1))
    return out, WAIST - waist


def strip(frames):
    out = Image.new("RGBA", (N * len(frames), N), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        out.paste(f, (i * N, 0))
    return out


def main():
    front = Image.open(sys.argv[1]).convert("RGBA")
    north = Image.open(sys.argv[2]).convert("RGBA")
    out = sys.argv[3]
    os.makedirs(out, exist_ok=True)
    back, shift = back_view(front, north)
    back.save(os.path.join(out, "luz-base-back.png"))
    strip(cycle(front, (50, 52))).save(os.path.join(out, "luz-walk-down.png"))
    strip(cycle(back, (50 + shift, 52 + shift))).save(os.path.join(out, "luz-walk-up.png"))
    print(f"luz-walk-down.png and luz-walk-up.png, 8 frames each; back view seated {shift} row(s) lower, bbox {back.getbbox()}")


main()
