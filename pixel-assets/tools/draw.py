"""Code-drawn kit pieces: gingerbread road tiles (straight, corner, faded) and the sparkle twinkle.

The road fills the whole 32px tile and turns at right angles, like the Experience road in the
wireframe. Every tile is built from one cross-section, so edges meet exactly when tiles are
placed side by side or rotated in quarter turns.

usage: draw.py <tiles_dir> <props_dir>
"""
import os
import sys

from PIL import Image

NAVY = (0x23, 0x30, 0x4D, 255)
CORAL = (0xC6, 0x5F, 0x4E, 255)
CREAM = (0xFF, 0xF7, 0xEE, 255)
WHITE = (255, 255, 255, 255)
GINGER = (0xB3, 0x6A, 0x3A, 255)
GINGER_LIGHT = (0xC9, 0x84, 0x50, 255)
GINGER_DARK = (0x8F, 0x4F, 0x2A, 255)
CLEAR = (0, 0, 0, 0)

N = 32
SCALLOP = [0, 1, 1, 2, 2, 1, 1, 0]  # icing piping, reads the same forwards and backwards


def road(u, v):
    """Colour at distance u along the road and v across it (both 0..31)."""
    m = min(v, N - 1 - v)  # distance in from the nearer edge, so both sides mirror
    if m in (0, 4):
        return NAVY
    if m < 4:  # candy cane rail
        return CORAL if (u + m) % 8 < 4 else WHITE
    if m == 5:
        return GINGER_LIGHT if v < N // 2 else GINGER_DARK
    if m == 7 + SCALLOP[u % 8]:
        return CREAM
    if m == 15 and 4 <= u % 16 <= 11:  # icing dashes down the middle
        return CREAM
    if 10 <= m <= 13 and (u * 7 + m * 13) % 29 == 0:
        return GINGER_DARK  # baked speckles
    return GINGER


def straight():
    im = Image.new("RGBA", (N, N), CLEAR)
    px = im.load()
    for y in range(N):
        for x in range(N):
            px[x, y] = road(x, y)
    return im


def corner():
    """Road enters at the left edge and leaves through the top edge (a turn upward).

    Mitred like a picture frame: below the diagonal it is the horizontal road, above it the
    vertical one, so the left and top edges match a straight tile and its quarter turn.
    """
    im = Image.new("RGBA", (N, N), CLEAR)
    px = im.load()
    for y in range(N):
        for x in range(N):
            v = max(x, y)
            u = x if y >= x else N - 1 - y
            if v >= N // 2:
                px[x, y] = road(u, v)
            else:
                # inside of the turn: only the small rail post at the corner, then plain road
                px[x, y] = road(u, v) if v <= 9 else GINGER
    # the centre dashes follow the turn
    for i in range(4, 12):
        px[i, 15] = px[i, 16] = CREAM
        px[15, i] = px[16, i] = CREAM
    return im


def faded(im, toward=(0xFF, 0xF7, 0xEE), amount=0.62):
    """Same road blended toward the cream page colour, for the stretch not travelled yet."""
    out = im.copy()
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = px[x, y]
            if a:
                px[x, y] = tuple(round(c + (t - c) * amount) for c, t in zip((r, g, b), toward)) + (255,)
    return out


def sparkle_frame(size, glints=False):
    """Four-point star centred between the middle pixels, so it mirrors exactly both ways."""
    c = (N - 1) / 2
    p = 0.62

    def inside(x, y):
        dx, dy = abs(x - c), abs(y - c)
        if dx ** p + dy ** p <= size ** p:
            return True
        return glints and (round(dx - 0.5), round(dy - 0.5)) == (5, 5)

    im = Image.new("RGBA", (N, N), CLEAR)
    px = im.load()
    for y in range(N):
        for x in range(N):
            dx, dy = abs(x - c), abs(y - c)
            if inside(x, y):
                px[x, y] = WHITE if dx + dy <= max(1.0, size * 0.3) else CREAM
            elif any(0 <= nx < N and 0 <= ny < N and inside(nx, ny)
                     for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))):
                px[x, y] = NAVY
    return im


def main():
    tiles, props = sys.argv[1], sys.argv[2]
    s = straight()
    s.save(os.path.join(tiles, "tile-road-straight.png"))
    corner().save(os.path.join(tiles, "tile-road-corner.png"))
    faded(s).save(os.path.join(tiles, "tile-road-faded.png"))

    frames = [sparkle_frame(3.5), sparkle_frame(8.5), sparkle_frame(13.5), sparkle_frame(7.5, glints=True)]
    strip = Image.new("RGBA", (N * len(frames), N), CLEAR)
    for i, f in enumerate(frames):
        strip.paste(f, (i * N, 0))
    strip.save(os.path.join(props, "prop-sparkle.png"))
    print("drew 3 road tiles and a", len(frames), "frame sparkle strip")


if __name__ == "__main__":
    main()
