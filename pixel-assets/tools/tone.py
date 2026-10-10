"""Her skin tone, in one place.

Luz gave it on 2026-10-09 as #f6d9a7: lighter and more golden than the tan PixelLab drew her
in. That is her lit skin. The shading darkens toward orange, as skin does, so it stays warm
and never goes grey or pink.

The portrait is large enough for a ramp (FAIR). The small sprite has room for four tones.
Both are applied by where a pixel is as well as by its colour, because the darker skin tones
are also the lights in her hair.
"""
import colorsys

LIT = "#f6d9a7"

# The portrait. Each entry: at least this bright in the drawing (HSV value), becomes this colour.
FAIR = [(0.985, "#fff0d6"), (0.955, "#fbe3bd"), (0.93, LIT), (0.88, "#edc592"), (0.83, "#e2b07e"),
        (0.76, "#d49b6c"), (0.68, "#c2855b"), (0.6, "#b0744f"), (0.0, "#9f6648")]

# The small sprite: a highlight, a step between lit and shade for the frames PixelLab
# animated, the shade under her hair and along her arms, and the deep shade under her chin.
GLOW, SOFT, SHADE, DEEP = "#fbe3bd", "#e8bc8a", "#d49b6c", "#b0744f"

NECK, UNDER_CHIN, HAND_FROM_BEHIND = (0xD5, 0x77, 0x40), (0xA5, 0x3C, 0x34), (0xCF, 0x6D, 0x4F)


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (255,)


def hsv(p):
    h, s, v = colorsys.rgb_to_hsv(p[0] / 255, p[1] / 255, p[2] / 255)
    return h * 360, s, v


def lit(p):
    """Lit skin as first drawn. Nothing else on her is this light and this warm."""
    if not p[3]:
        return False
    h, s, v = hsv(p)
    return 15 <= h <= 30 and 0.3 <= s <= 0.62 and v >= 0.8


def shaded(p):
    """A colour her shaded skin can be. Her hair's rim light can be it too, so it counts as
    skin only next to lit skin (see skin_of). Her mouth is redder and darker than this."""
    if not p[3] or lit(p):
        return False
    h, s, v = hsv(p)
    return 8 <= h <= 26 and 0.45 <= s <= 0.72 and 0.68 <= v < 0.9


def flushed(p):
    """Two more things PixelLab drew on her face while animating: a hot orange where her skin
    meets her hair, and a pale pink under an eye. Luz asked for no blush, so both are skin.
    They count only right beside lit skin (see skin_of)."""
    if not p[3] or lit(p) or shaded(p):
        return False
    h, s, v = hsv(p)
    return v >= 0.75 and ((4 <= h <= 26 and 0.72 < s <= 0.8) or (h <= 14 and 0.2 <= s <= 0.4))


def deep(p):
    """The red-browns PixelLab put under and beside a hand. Her mouth is these colours too, so
    they count only beside a hand (see skin_of)."""
    if not p[3] or lit(p) or shaded(p):
        return False
    h, s, v = hsv(p)
    return (h <= 12 or h >= 350) and 0.6 <= s <= 0.8 and 0.3 <= v < 0.85


def skin_of(frame, kind="front", body=None):
    """The skin pixels of one 64x64 frame as first drawn, each with its new colour.

    Lit skin, then the shading within two pixels' walk of it (the shade on her ears touches
    only the shade on her cheeks). The rest is known by place: her neck by its own colour and
    the shadow under her chin as that red directly above it (an open mouth is the same red); from behind, her hands, which show no lit skin at all; and
    from the side, the far hand, which swings in shade alone in front of her. `body` is the
    box round her hoodie (x0, y0, x1, y1): her hands are below its collar and never behind
    her back, where her hair hangs and carries the same shade colours as rim light."""
    px = frame.load()
    w, h = frame.size
    skin = {(x, y) for y in range(h) for x in range(w) if lit(px[x, y])}
    lit_px = set(skin)

    def around(x, y):
        return [(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                if (dx or dy) and 0 <= x + dx < w and 0 <= y + dy < h]

    warm = {n for x, y in lit_px for n in around(x, y) if n not in lit_px and flushed(px[n])}
    for _ in range(2):
        skin |= {n for x, y in skin for n in around(x, y) if n not in skin and shaded(px[n])}
    skin |= warm
    under, far_hand = set(), set()
    if kind == "side" and body:
        zone = [(x, y) for y in range(body[1] + 2, h) for x in range(body[0], w)]
        # a hand swung behind her hangs just left of the hoodie, below where her hair ends
        zone += [(x, y) for y in range(body[3] - 3, h) for x in range(max(0, body[0] - 5), body[0])]
        far_hand = {p for p in zone if shaded(px[p])} - skin
        skin |= far_hand
        under = {p for p in zone if p not in skin and deep(px[p]) and any(n in skin for n in around(*p))}
    out = {}
    for x, y in skin:
        p = px[x, y]
        _, s, v = hsv(p)
        if (x, y) in lit_px:
            out[x, y] = rgb(GLOW if s < 0.45 else LIT if v >= 0.9 else SOFT)
        else:
            pale = (x, y) in warm and s <= 0.4
            out[x, y] = rgb(LIT if pale else SHADE if v >= 0.75 or (x, y) in far_hand else DEEP)
    for p in under:
        out[p] = rgb(DEEP)
    for y in range(h):
        for x in range(w):
            c = px[x, y][:3]
            if not px[x, y][3] or (x, y) in out:
                continue
            if c == NECK and kind == "front":
                out[x, y] = rgb(SHADE)
            elif c == UNDER_CHIN and kind == "front" and y + 1 < h and px[x, y + 1][:3] == NECK:
                out[x, y] = rgb(DEEP)
            elif c == HAND_FROM_BEHIND and kind == "back":
                out[x, y] = rgb(SHADE)
    return out


def fair(out, first, kind="front", body=None):
    """Give a dressed frame her skin tone: every pixel that is skin in the frame as first drawn
    and that the outfit left alone. Skin an outfit drew itself is already in these tones."""
    op, fp = out.load(), first.load()
    for (x, y), colour in skin_of(first, kind, body).items():
        if op[x, y] == fp[x, y]:
            op[x, y] = colour
    return out
