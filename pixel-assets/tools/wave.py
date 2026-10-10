"""One-handed wave where only the arm moves.

Every wave frame is the base sprite with the resting arm lifted off (the plate) and one raised
arm drawn on top; hair, face and the rest of the body are the base's own pixels.

The arm is drawn here, not taken from PixelLab. PixelLab's raised arm was a short wedge of
sleeve with a two-pixel hand cut off from it by an outline: Luz said it "looks like a stub"
and "doesn't look connected". This one is as long as her resting arm, the same thickness the
whole way, starts inside her shoulder, and its hand sits directly on the cuff.

usage: wave.py <base.png> <out_dir>
"""
import os
import sys

from PIL import Image

K, CLEAR = (0, 0, 0, 255), (0, 0, 0, 0)
SLEEVE, SLEEVE_SHADE, CUFF = (0xF0, 0x5E, 0x08, 255), (0xD5, 0x3B, 0x12, 255), (0x9C, 0x1E, 0x1A, 255)
HAND, HAND_SHADE = (0xF0, 0xAB, 0x7B, 255), (0xC2, 0x60, 0x49, 255)
EDGE = (0xA4, 0x23, 0x1A, 255)   # the hoodie's side, seen once the sleeve is lifted off it
D1, D2 = (33, 20, 18, 255), (58, 33, 26, 255)      # her hair's two darks

SHOULDER = (26, 45)              # the arm starts on this pixel, inside the hoodie's side
BODY_X = 27                      # from this column on is her torso: the arm's outline stops there
# Each pose is how the arm climbs per step (columns left, rows up) and how many steps of sleeve
# come before the cuff. The slopes are whole-number ones, so the arm's edges are even stair
# steps with no wobble, and the step counts keep the arm the length of her resting arm (ten
# pixels from shoulder to fingertips) at every angle.
POSES = {
    "low": dict(left=1, up=-0.5, sleeve=5),         # half way up: out to the side, hand below the shoulder
    "out": dict(left=1, up=0.5, sleeve=5),
    "in": dict(left=1, up=1, sleeve=4),
}
# The strip starts on her resting pose. A visitor with animation off sees only a strip's first
# frame, and the hero opens on this strip: she must be standing there, not caught mid-gesture.
ORDER = ["rest", "out", "in", "out", "in", "low"]   # from rest, wave twice, lower


def plate(base):
    """The base with the resting arm lifted off, drawn on purpose so the same pixels sit under
    the arm in every wave frame: the side of the hoodie, and her hair hanging behind where the
    sleeve used to be."""
    out = base.copy()
    for y in range(43, 50):                       # hoodie side: outline, edge shade, then body colour
        out.putpixel((25, y), K)
        out.putpixel((26, y), EDGE)
        out.putpixel((27, y), base.getpixel((28, y)))
    hair = {43: (D2, D1, D1), 44: (D1, D2, D1), 45: (D2, D1, D1), 46: (D1, D1, D1), 47: (K, D1, D1), 48: (K, K, K)}
    for y, row in hair.items():                   # hair behind the lifted sleeve, closed off along row 48
        for x, c in zip((22, 23, 24), row):
            out.putpixel((x, y), c)
    for x, y in [(23, 49), (24, 49), (22, 50), (23, 50), (24, 50), (22, 51), (23, 51), (24, 51), (23, 52), (24, 52)]:
        out.putpixel((x, y), CLEAR)               # sleeve cuff and hand
    return out


def arm(pose):
    """The raised arm as {pixel: colour}: sleeve, cuff, hand and the outline round them.

    The arm is a row of short runs, one per step from the shoulder. A shallow arm steps a
    column at a time and its runs stand upright, three pixels each. The steep one steps a row
    at a time on the diagonal and its runs lie across, four pixels each, which on a diagonal
    is the same thickness to the eye. The hand carries straight on from the cuff: three runs
    for an open palm, the last one of the steep pose narrowed to round its fingertips."""
    left, up, sleeve = (POSES[pose][k] for k in ("left", "up", "sleeve"))
    steep = up >= 1
    runs = []
    for i in range(sleeve + 1):                    # the sleeve, then the cuff
        if steep:
            x, y = SHOULDER[0] - int(i * left / up), SHOULDER[1] - i
            runs.append([(x - 2, y), (x - 1, y), (x, y), (x + 1, y)])   # outer side first
        else:
            x, y = SHOULDER[0] - i, SHOULDER[1] - int(i * up / left)
            runs.append([(x, y + 1), (x, y), (x, y - 1)])               # underside first
    cuff = runs[-1]
    step = (0, -1) if steep else (-1, 0)
    hand = [[(x + step[0] * j, y + step[1] * j) for x, y in cuff] for j in (1, 2, 3)]
    if steep:
        hand[-1] = hand[-1][1:-1]
    out = {}
    for run in runs[:-1]:
        for n, p in enumerate(run):
            out[p] = SLEEVE_SHADE if n == 0 else SLEEVE
    for p in cuff:
        out[p] = CUFF
    for j, run in enumerate(hand):
        for n, p in enumerate(run):
            out[p] = HAND_SHADE if (j, n) == (0, 0) else HAND
    shape = set(out)
    for x, y in shape:
        for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if n not in shape and n[0] < BODY_X:
                out[n] = K
    return out


def frames(base):
    """The six wave frames, and for each the set of pixels the arm and its outline cover."""
    under = plate(base)
    made = []
    for pose in ORDER:
        if pose == "rest":
            made.append((base.copy(), set()))
            continue
        frame = under.copy()
        drawn = arm(pose)
        for p, c in drawn.items():
            frame.putpixel(p, c)
        made.append((frame, set(drawn)))
    return made


def main():
    base = Image.open(sys.argv[1]).convert("RGBA")
    out_dir = sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    under = plate(base)
    n = base.width
    for k, (frame, drawn) in enumerate(frames(base)):
        frame.save(os.path.join(out_dir, f"frame_{k:02d}.png"))
        # only the arm may move: nothing outside the arm and the plate differs from the base
        stray = sum(1 for y in range(n) for x in range(n) if frame.getpixel((x, y)) != base.getpixel((x, y))
                    and (x, y) not in drawn and under.getpixel((x, y)) == base.getpixel((x, y)))
        print(f"wave frame {k} ({ORDER[k]}): arm and outline {len(drawn)}px; changed outside the arm and the plate: {stray}")
    # the poses on their own, for the cheer, which raises both arms
    for pose in POSES:
        frame = under.copy()
        for p, c in arm(pose).items():
            frame.putpixel(p, c)
        frame.save(os.path.join(out_dir, f"pose_{pose}.png"))
    under.save(os.path.join(out_dir, "_plate.png"))


if __name__ == "__main__":
    main()
