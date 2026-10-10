"""Dress every character strip in each scene's outfit.

The strips Luz was first drawn in (the orange hoodie, kept in outfits/source) are the
source. Each frame is repainted for an outfit by what its pixels are: hoodie, pants, shoes,
hands. Wherever a front-view frame still holds the approved still's pose, the approved
outfit's own pixels are used instead, so the looks Luz signed off are reproduced exactly and
only the parts that moved (a raised arm, a stepping leg) come from the rules.

Head, hair and face are never redrawn: they are the source frame's pixels, with her skin
in the tone she chose (tone.py). Halloween is the orange hoodie itself with only that change.

Writes outfits/<name>/<strip>.png for every scene. luz-celebrate is
left out: the site does not use it, and its leaping frames hold no pose the stills cover.
seasons.py then puts each outfit in its scene's folder.

usage: wardrobe.py <pixel-assets dir>
"""
import colorsys
import importlib.util
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import outfits  # noqa: E402
import tone  # noqa: E402

# tools/wave.py draws the raised arm and knows the plate under it. It is loaded by path: a
# plain "import wave" could find Python's own wave module instead.
_spec = importlib.util.spec_from_file_location("luz_wave", os.path.join(os.path.dirname(os.path.abspath(__file__)), "wave.py"))
raised_arm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(raised_arm)

CELL = 64
SPLIT = 55                       # idle's breath moves the rows above this one
CLEAR = (0, 0, 0, 0)
BLACK = (0, 0, 0, 255)

# strip name: which way she faces in it
STRIPS = {
    "luz-base-front": "front", "luz-idle": "front", "luz-wave": "front", "luz-walk-down": "front",
    "luz-emote-wow": "front", "luz-emote-grin": "front", "luz-emote-happy": "front", "luz-emote-starry": "front",
    "luz-emote-student": "front", "luz-emote-cheer": "front",
    "luz-side-right": "side", "luz-walk": "side", "luz-hop": "side",
    "luz-walk-up": "back",
}
ARMS_UP = {"luz-wave": ("left",), "luz-emote-cheer": ("left", "right")}


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (255,)


def hsv(p):
    h, s, v = colorsys.rgb_to_hsv(p[0] / 255, p[1] / 255, p[2] / 255)
    return h * 360, s, v


def luminance(p):
    return 0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]


# ---------------------------------------------------------------- what a pixel is

def is_hoodie(p):
    if not p[3]:
        return False
    h, s, v = hsv(p)
    # every hoodie shade is at least 0.83 saturated; her hair's warmest lights reach 0.79
    return (h <= 40 or h >= 345) and s > 0.8 and v > 0.3


def is_pants(p):
    if not p[3]:
        return False
    h, s, v = hsv(p)
    return s < 0.2 and 0.1 < v < 0.25 and 180 <= h <= 260


def is_shoe(p):
    if not p[3]:
        return False
    h, s, v = hsv(p)
    return (s < 0.3 and 0.14 < v < 0.25 and h < 60) or p[:3] == (0x92, 0x7F, 0x76)


def is_skin(p):
    if not p[3]:
        return False
    h, s, v = hsv(p)
    return 5 <= h <= 45 and 0.3 < s < 0.72 and v >= 0.75


def ink(p):
    """Black, or the near-black maroon PixelLab shaded the far leg and the deepest folds with."""
    if not p[3]:
        return False
    _, s, v = hsv(p)
    return v < 0.05 or (v < 0.3 and s > 0.8)


def is_hair(p):
    if not p[3]:
        return False
    h, s, v = hsv(p)
    return 5 <= h <= 30 and 0.35 <= s <= 0.8 and 0.1 <= v <= 0.7 and not is_hoodie(p)


def stray(p):
    """A red that is neither hoodie nor skin: the in-between tones PixelLab left where the
    hoodie met something else. In any other outfit they are specks."""
    if not p[3] or is_hoodie(p) or tone.lit(p) or tone.shaded(p):
        return False
    h, s, v = hsv(p)
    return (h >= 340 or h <= 12) and s > 0.6 and v >= 0.3


FOUR = ((1, 0), (-1, 0), (0, 1), (0, -1))
EIGHT = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy]
FLAT = (0xF0, 0x5E, 0x08, 255)   # the hoodie's own mid orange: what a covered-up pixel is taken for

SKIN, SKIN_SHADE, SKIN_DARK = rgb(tone.LIT), rgb(tone.SHADE), rgb(tone.DEEP)
ORANGE_LUM = [luminance(rgb(c)) for c in outfits.ORANGE]


def ramp(p, colours):
    """The hoodie's shade at this pixel, carried over to another ramp of the same length."""
    lum = luminance(p)
    i = min(range(len(ORANGE_LUM)), key=lambda k: abs(ORANGE_LUM[k] - lum))
    return rgb(colours[i])


def as_skin(p):
    """A sleeve pixel as bare arm: the hoodie's light and middle tones lit, its dark ones shade."""
    v = hsv(p)[2]
    return SKIN if v > 0.75 else SKIN_SHADE if v > 0.5 else SKIN_DARK


def bbox(points):
    xs, ys = [p[0] for p in points], [p[1] for p in points]
    return (min(xs), min(ys), max(xs), max(ys)) if points else None


def near(point, others, reach):
    x, y = point
    return any(abs(x - ox) <= reach and abs(y - oy) <= reach for ox, oy in others)


# ---------------------------------------------------------------- the looks

class Look:
    """One outfit. `still` is the approved front sprite; the methods say what each kind of
    pixel becomes in a frame the still does not cover."""
    bare_arms = False
    redraws = True                                   # the side views are repainted part by part

    def __init__(self, still):
        self.still = still

    def fabric(self, p, x, y, f):
        return p

    def legs(self, p, x, y, f):
        return p

    def shoes(self, p, x, y, f):
        return p

    def finish(self, out, src, f):
        pass


class AsDrawn(Look):
    """The orange hoodie she was first drawn in: nothing is repainted."""
    redraws = False


class Hoodie(Look):
    """A recoloured hoodie over her own black pants and shoes."""

    def __init__(self, still, colours):
        super().__init__(still)
        self.colours = colours

    def fabric(self, p, x, y, f):
        return ramp(p, self.colours)

    def finish(self, out, src, f):
        if f["kind"] == "back":
            unprint(out, src, f, ramp(FLAT, self.colours))


class CandyHoodie(Hoodie):
    """White, with the hood, the cuffs and the hem in candy red."""

    def fabric(self, p, x, y, f):
        hood = f["kind"] != "front" and y <= f["hoodie"][1] + 2
        return ramp(p, outfits.RED if hood else self.colours)

    def finish(self, out, src, f):
        super().finish(out, src, f)
        px, sp = out.load(), src.load()
        if f["kind"] == "side":                     # the red hem and cuff: the hoodie's lower edge
            for x, y in f["torso"]:
                if (x, y + 1) not in f["torso"] and y >= f["hoodie"][1] + 5:
                    px[x, y] = rgb(outfits.RED[5])
            return
        for x, y in f["hoodie_px"]:                 # a cuff: hoodie right beside a hand
            if near((x, y), f["hands"], 1):
                px[x, y] = ramp(sp[x, y], outfits.RED)


def unprint(out, src, f, colour):
    """From the side or the back the chest print shows as a few black pixels inside the hoodie.
    Paint them the hoodie's own colour: the new prints are drawn for the front view only."""
    sp, px = src.load(), out.load()
    for x, y in [(x, y) for x in range(CELL) for y in range(CELL) if sp[x, y][:3] == (0, 0, 0) and sp[x, y][3]]:
        around = [sp[x + dx, y + dy] for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                  if (dx or dy) and 0 <= x + dx < CELL and 0 <= y + dy < CELL]
        if all(is_hoodie(q) or (q[:3] == (0, 0, 0) and q[3]) for q in around) and sum(is_hoodie(q) for q in around) >= 5:
            px[x, y] = colour


class Summer(Look):
    """Yellow ruffle top, blue shorts, bare arms and legs, blue shoes, sunglasses in her hair."""
    bare_arms = True

    SHORTS = 2                                       # rows of shorts below the top, side and back

    def fabric(self, p, x, y, f):
        top = f["hoodie"][1]
        odd = (x - f["hoodie"][0]) % 2
        if y <= top + 2:                            # the ruffle: folds, then its scalloped edge
            return rgb(outfits.YELLOW_LIGHT if odd else outfits.YELLOW) if y < top + 2 else \
                rgb(outfits.YELLOW_SHADE if odd else outfits.YELLOW)
        torso = f.get("torso")
        if torso is None:
            return rgb(outfits.YELLOW if hsv(p)[2] > 0.55 else outfits.YELLOW_SHADE)
        # from the side the top is flat: one line of shade down her back, a scalloped hem
        if (x, y + 1) not in torso:
            return rgb(outfits.YELLOW_SHADE if odd else outfits.YELLOW)
        return rgb(outfits.YELLOW_SHADE if (x - 1, y) not in torso else outfits.YELLOW)

    def legs(self, p, x, y, f):
        top = f["pants"][1]
        if y < top + self.SHORTS:
            return rgb("#2a56a6" if y == top + self.SHORTS - 1 else "#3d7bd9")
        return SKIN if hsv(p)[2] > 0.15 else SKIN_SHADE

    def shoes(self, p, x, y, f):
        if p[:3] == (0x92, 0x7F, 0x76):
            return rgb("#8db8f2")
        below = f["src"].getpixel((x, y + 1)) if y + 1 < CELL else CLEAR
        return rgb("#f4f7ff") if below[:3] == (0, 0, 0) or not below[3] else rgb("#3d7bd9")

    def far_leg(self, x, y, f):
        return rgb("#2a56a6") if y < f["pants"][1] + self.SHORTS else SKIN_SHADE

    def far_shoe(self, x, y, f):
        return rgb("#2a56a6")

    def finish(self, out, src, f):
        if f["kind"] == "side":                      # the sunglasses, seen from the side
            x0, y0, x1, _ = f["hair"]
            outfits.stamp(out, [".WWWWW.", "WNNgNNW", ".WWWWW."], x1 - 14, y0 + 2,
                          {"W": "#ffffff", "N": "#23304d", "g": "#8db8f2"})


class EasterDress(Look):
    """Blue and white gingham dress with puff sleeves, bare forearms, white boots."""
    bare_arms = True
    sleeve = 2                                       # rows of puff sleeve before the bare arm
    SKIRT = 2                                        # rows of skirt below the bodice, side and back

    def far_leg(self, x, y, f):
        top = f["pants"][1]
        if y <= top + self.SKIRT:
            return self.fabric(None, x, y, f)
        return SKIN_SHADE if y == top + self.SKIRT + 1 else rgb("#b9c9ea")

    def far_shoe(self, x, y, f):
        return rgb("#b9c9ea")

    def skirt(self, out, f):
        """From the side the skirt hangs as one bell over both legs, not a wrap round each: on
        its rows everything from her back leg to her front leg is dress, the last row the pale
        hem, and under the hem a line closes it between her legs."""
        px = out.load()
        legs, skin, top = f["legs"], f["skin"], f["pants"][1]
        rows = range(min(y for _, y in legs), top + self.SKIRT + 1)
        guard = set(skin) | {(x + dx, y + dy) for x, y in skin for dx, dy in FOUR}   # a hand and its outline
        span = None
        for y in rows:
            xs = [x for x, yy in legs | f["torso"] if yy == y]     # where the bodice still shows, the skirt joins it
            if not xs:
                continue
            span = (min(xs) - 1, max(xs) + 1)
            for x in range(span[0], span[1] + 1):
                if (x, y) in guard:
                    continue
                edge = x in span
                px[x, y] = BLACK if edge else rgb("#d6e2f7") if y == top + self.SKIRT else self.fabric(None, x, y, f)
        if span:
            y = top + self.SKIRT + 1
            for x in range(span[0], span[1] + 1):
                if (x, y) not in legs and (x, y) not in guard and y < CELL:
                    px[x, y] = BLACK

    def finish(self, out, src, f):
        """From the side and the back the skirt stands a pixel proud of her legs, front and behind."""
        if f["kind"] == "front":
            # the skirt is wider than her legs and does not step with them: its last rows and the
            # line under its hem are the still's, whatever her legs are doing behind it
            px = out.load()
            for y in (52, 53, 54):
                for x in range(25, 39):
                    px[x, y + f["dy"]] = self.still.getpixel((x, y))
            for x in range(26, 38):
                if not px[x, 55 + f["dy"]][3]:
                    px[x, 55 + f["dy"]] = BLACK
            return
        if not f["pants"]:
            return
        if f["kind"] == "side":
            return self.skirt(out, f)
        px = out.load()
        top = f["pants"][1]
        for y in range(top, top + self.SKIRT + 1):
            xs = [x for x in range(CELL) if px[x, y][3]]
            for edge, step in ((min(xs), -1), (max(xs), 1)) if xs else ():
                if px[edge, y][:3] == (0, 0, 0) and 0 <= edge + step < CELL and not px[edge + step, y][3]:
                    px[edge, y] = self.fabric(None, edge, y, f)
                    px[edge + step, y] = BLACK

    def fabric(self, p, x, y, f):
        x0, y0 = f["hoodie"][0], f["hoodie"][1]
        return rgb(("#ffffff", outfits.PALE, outfits.PALE, outfits.BLUE)[((x - x0) // 2 % 2) * 2 + ((y - y0) // 2 % 2)])

    def legs(self, p, x, y, f):
        top = f["pants"][1]
        if f["kind"] == "front":
            if y <= SPLIT - 1 + f["dy"]:             # behind the skirt: the still's own pixel
                return self.still.getpixel((x, y - f["dy"]))
            return SKIN if y == SPLIT + f["dy"] else rgb("#ffffff" if hsv(p)[2] > 0.15 else "#d6e2f7")
        if y <= top + self.SKIRT:
            return self.fabric(p, x, y, f)
        if y == top + self.SKIRT + 1:
            return SKIN
        return rgb("#ffffff" if hsv(p)[2] > 0.15 else "#d6e2f7")

    def shoes(self, p, x, y, f):
        return rgb("#d6e2f7" if p[:3] == (0x2E, 0x2B, 0x28) else "#ffffff")


# ---------------------------------------------------------------- one frame

def bobbed(im, dy):
    """The still as idle moves it: everything above the knees down by dy."""
    if not dy:
        return im
    out = im.copy()
    top = im.crop((0, 0, CELL, SPLIT))
    out.paste(CLEAR, (0, 0, CELL, SPLIT))
    out.alpha_composite(top, (0, dy))
    return out


def held_pose(frame, orange):
    """How far the frame's body sits below the still's (0 or 1), or None if it is in another pose."""
    best = None
    for dy in (0, 1):
        ref = bobbed(orange, dy)
        bad = sum(frame.getpixel((x, y)) != ref.getpixel((x, y)) for y in range(43, 53) for x in range(27, 37))
        if best is None or bad < best[0]:
            best = (bad, dy)
    return best[1] if best[0] <= 15 else None


def lift_arm(out, frame, look, dy, side, under):
    """Wave and cheer lift an arm off her side. For a bare-armed look, close what the sleeve
    left behind: her hair hangs there, down to the line that ends it, and the top keeps its
    own edge. The raised arm itself is whatever the frame shows that the plate under it does
    not; it is left on top of all this, so it stays joined to her shoulder."""
    px, fp = out.load(), frame.load()

    def at(x):
        return x if side == "left" else CELL - 1 - x

    arm = {(x, y) for y in range(CELL) for x in range(28) if fp[at(x), y] != under.getpixel((at(x), y))}
    d1, d2 = rgb("#211412"), rgb("#3a211a")
    still = look.still
    for y in range(43, 49):
        row = y + dy
        for x in (25, 26):
            if (x, row) not in arm:
                px[at(x), row] = BLACK if y == 48 else (d1 if (x + y) % 2 else d2)
        inner = still.getpixel((at(28), y))
        own = still.getpixel((at(27), y))
        if (27, row) in arm or ((26, row) in arm and is_hoodie(fp[at(26), row])):
            px[at(27), row] = SKIN_DARK             # the arm leaves her shoulder here, in her top's shadow
        else:
            # the still has her arm's shadow on this column; without the arm it is the top's
            # outline, unless the dress is already there
            px[at(27), row] = own if own == inner or not is_skin_tone(own) else BLACK
    for x in (23, 24, 25):
        if (x, 49 + dy) not in arm:
            px[at(x), 49 + dy] = CLEAR
    for x, y in arm:                                # the arm is bare: no cuff, one line of shade beneath
        if x < 27 and is_hoodie(fp[at(x), y]):
            px[at(x), y] = SKIN_SHADE if fp[at(x), y] == raised_arm.SLEEVE_SHADE else SKIN


def is_skin_tone(p):
    return p in (SKIN, SKIN_SHADE, SKIN_DARK)


def side_arm(out, src, f, look):
    """From the side her sleeve cannot be told from the body of the hoodie, so a bare arm is
    drawn: a strip of skin from her shoulder to each hand, over what was hoodie, with its
    shadow on the side away from her face. A sleeved look keeps its top rows as sleeve."""
    sp, op = src.load(), out.load()
    cloth = f["torso"] - f["rim"]
    x0, y0, x1, _ = f["hoodie"]
    shoulder = ((x0 + x1) // 2, y0 + 3 + getattr(look, "sleeve", 0))
    hands, todo = [], set(f["hands"])
    while todo:                                     # each hand is one clump of skin
        clump, stack = [], [todo.pop()]
        while stack:
            p = stack.pop()
            clump.append(p)
            for n in ((p[0] + 1, p[1]), (p[0] - 1, p[1]), (p[0], p[1] + 1), (p[0], p[1] - 1)):
                if n in todo:
                    todo.remove(n)
                    stack.append(n)
        if len(clump) >= 2:
            hands.append((round(sum(p[0] for p in clump) / len(clump)), min(p[1] for p in clump)))
    for hx, hy in hands:
        steps = max(abs(hx - shoulder[0]), abs(hy - shoulder[1]), 1)
        for i in range(steps + 1):
            x = round(shoulder[0] + (hx - shoulder[0]) * i / steps)
            y = round(shoulder[1] + (hy - shoulder[1]) * i / steps)
            for dx, colour in ((-1, SKIN_SHADE), (0, SKIN), (1, SKIN)):
                if (x + dx, y) in cloth:
                    op[x + dx, y] = colour


def side_legs(out, src, f, look, shoe_px):
    """The far leg is drawn as solid black in the source, where black pants hid it. Under a
    bare-legged look that black would read as a missing leg, so the black that lies inside
    her legs, not on their outline, takes the look's own colour for that row."""
    sp, op = src.load(), out.load()
    top = f["pants"][1]
    bottom = min((y for _, y in shoe_px), default=CELL) - 1
    for y in range(top, bottom + 1):
        for x in range(1, CELL - 1):
            if sp[x, y][:3] != (0, 0, 0) or not sp[x, y][3]:
                continue
            around = [sp[x + 1, y], sp[x - 1, y], sp[x, y + 1], sp[x, y - 1]]
            if all(q[3] for q in around) and sum(is_pants(q) or (q[:3] == (0, 0, 0) and q[3]) for q in around) >= 3:
                op[x, y] = look.far_leg(x, y, f)


def parts(points):
    """The 4-connected pieces of a set of pixels, largest first."""
    todo, found = set(points), []
    while todo:
        piece, stack = set(), [todo.pop()]
        while stack:
            x, y = stack.pop()
            piece.add((x, y))
            for dx, dy in FOUR:
                if (x + dx, y + dy) in todo:
                    todo.remove((x + dx, y + dy))
                    stack.append((x + dx, y + dy))
        found.append(piece)
    return sorted(found, key=len, reverse=True)


def closed(out):
    """A one-pixel hole in her outline shows the page through it: fill it."""
    op = out.load()
    for y in range(1, CELL - 1):
        for x in range(1, CELL - 1):
            if not op[x, y][3] and all(op[x + dx, y + dy][3] for dx, dy in FOUR):
                op[x, y] = BLACK
    return out


def dress_side(frame, look):
    """A side view, repainted part by part.

    PixelLab animated these frames in the orange hoodie, with its jack-o'-lantern showing as
    black teeth along her front, her far leg as a block of near-black, and in-between reds
    wherever two things met. Recolouring pixel by pixel leaves all of that behind as specks.
    So the frame is first sorted into parts by place: the outline (whatever touches the empty
    background), her torso (the hoodie and every dark or stray pixel it encloses), her near
    leg and shoe, her far leg (the dark under the hoodie that is nobody's outline), her skin
    and her hair. Each part is then painted whole."""
    px = frame.load()
    opaque = {(x, y) for y in range(CELL) for x in range(CELL) if px[x, y][3]}
    rim = {(x, y) for x, y in opaque if any((x + dx, y + dy) not in opaque for dx, dy in FOUR)}
    hood = {p for p in opaque if is_hoodie(px[p])}
    hb = bbox(hood)
    skin = set(tone.skin_of(frame, "side", hb))
    hair = {p for p in opaque if is_hair(px[p])} - skin
    waist = hb[3] - 3
    pants = {p for p in opaque if p[1] >= waist and is_pants(px[p])}
    shoes = {p for p in opaque if p[1] >= waist and is_shoe(px[p])} - pants
    for piece in parts(shoes):                       # a shoe-grey pixel or two on its own is shading, not a shoe
        if len(piece) < 4:
            shoes -= piece
    span = {}                                        # column: the hoodie's top and bottom row in it
    for x, y in hood:
        lo, hi = span.get(x, (y, y))
        span[x] = (min(lo, y), max(hi, y))

    def loose(p):
        """Dark or stray, and nobody's outline: not on the rim, not round a hand, not round hair."""
        x, y = p
        return (p not in rim and (ink(px[p]) or stray(px[p]))
                and not any((x + dx, y + dy) in skin for dx, dy in EIGHT)
                and not any((x + dx, y + dy) in hair for dx, dy in FOUR))

    # below the hoodie there is no hair: the same dark browns are her far leg and shoe
    below = {p for p in opaque - rim - skin - pants - shoes if p[1] > hb[3] and hsv(px[p])[2] < 0.3
             and not any((p[0] + dx, p[1] + dy) in skin for dx, dy in EIGHT)}
    hair -= below
    free = {p for p in opaque - hood - skin - hair - pants - shoes if loose(p)} | below
    covered = {(x, y) for x, y in free if x in span and span[x][0] < y < span[x][1]}
    # and whatever else the hoodie encloses that is no hand and no hair: PixelLab's odd pixels
    odd = opaque - rim - hood - skin - hair - pants - shoes - free
    covered |= {(x, y) for x, y in odd if x in span and span[x][0] < y < span[x][1]
                and not any((x + dx, y + dy) in skin for dx, dy in EIGHT)
                and not any((x + dx, y + dy) in hair for dx, dy in FOUR)}
    far = {(x, y) for x, y in free - covered if y > span.get(x, (0, 0))[1] and y >= hb[3] - 1}
    # a shoe is three rows; PixelLab drew some up to her knee. What is above is leg.
    for piece in parts(shoes):
        foot = max(y for _, y in piece) - 2
        tall = {p for p in piece if p[1] < foot}
        shoes -= tall
        pants |= tall
    far_shoes = set()
    reach = min((y for _, y in pants), default=hb[3] + 1) + 3
    for piece in parts(far):                         # the far foot: the last three rows of a far leg that gets that low
        foot = max(y for _, y in piece)
        if foot >= reach and len(piece) >= 4:
            far_shoes |= {p for p in piece if p[1] >= foot - 2}
    far -= far_shoes
    torso = hood | covered
    pieces = parts(torso)
    bits = set().union(*pieces[1:]) if len(pieces) > 1 else set()
    hands = [p for p in skin if p[1] >= hb[1] + 2 and is_skin(px[p])]
    f = dict(kind="side", hoodie=hb, hoodie_px=sorted(torso), torso=torso, rim=rim, pants=bbox(pants), hands=hands,
             hair=frame.getbbox(), dy=0, src=frame, skin=skin, legs=pants | far)

    out = frame.copy()
    op = out.load()
    for x, y in torso:
        op[x, y] = look.fabric(px[x, y] if (x, y) in hood else FLAT, x, y, f)
    for x, y in pants:
        op[x, y] = look.legs(px[x, y], x, y, f)
    for x, y in shoes:
        op[x, y] = look.shoes(px[x, y], x, y, f)
    if hasattr(look, "far_leg") and pants:
        for x, y in far:
            op[x, y] = look.far_leg(x, y, f)
        for x, y in far_shoes:
            op[x, y] = look.far_shoe(x, y, f)
    if look.bare_arms:
        side_arm(out, frame, f, look)
        for p in bits:                               # the hood's tip under her chin: there is no hood now
            op[p] = BLACK
    look.finish(out, frame, f)
    hand = {p for p in skin if p[1] >= hb[1] + 2}
    for p in opaque - skin:
        if op[p] != px[p]:
            continue
        x, y = p
        by_hand = any((x + dx, y + dy) in hand for dx, dy in EIGHT)
        if by_hand and hsv(px[p])[2] < 0.3:          # a hand's outline, drawn in several dark browns
            op[p] = BLACK
        elif (ink(px[p]) or stray(px[p])) and not (by_hand and stray(px[p])):
            op[p] = BLACK                            # what is left of the darkest reds is outline
    return tone.fair(closed(out), frame, "side", hb)


def dress_frame(frame, look, kind, orange, arms_up=()):
    if kind == "side" and look.redraws:
        return dress_side(frame, look)
    px = frame.load()
    hoodie_px = [(x, y) for y in range(CELL) for x in range(CELL) if is_hoodie(px[x, y])]
    hb = bbox(hoodie_px)
    # her legs are below the hoodie: the same dark greys higher up are her eyes and hair
    waist = hb[3] - 3 if hb else 40
    pants_px = [(x, y) for y in range(waist, CELL) for x in range(CELL) if is_pants(px[x, y])]
    shoe_px = [(x, y) for y in range(waist, CELL) for x in range(CELL) if is_shoe(px[x, y])]
    floor = hb[1] + 2 if hb else 0
    hands = [(x, y) for y in range(floor, CELL) for x in range(CELL) if is_skin(px[x, y])]
    hair = frame.getbbox()
    dy = held_pose(frame, orange) if kind == "front" else None
    f = dict(kind=kind, hoodie=hb, hoodie_px=hoodie_px, pants=bbox(pants_px), hands=hands, hair=hair, dy=dy or 0, src=frame)

    out = frame.copy()
    op = out.load()
    for x, y in hoodie_px:
        if look.bare_arms and kind == "front" and abs(x - 31.5) >= 5:
            op[x, y] = as_skin(px[x, y])
        else:
            op[x, y] = look.fabric(px[x, y], x, y, f)
    for x, y in pants_px:
        op[x, y] = look.legs(px[x, y], x, y, f)
    for x, y in shoe_px:
        op[x, y] = look.shoes(px[x, y], x, y, f)
    if look.bare_arms and kind != "front" and pants_px:
        side_legs(out, frame, f, look, shoe_px)
    look.finish(out, frame, f)

    if dy is not None:                               # where she still holds the pose: the approved pixels
        ref, still = bobbed(orange, dy), bobbed(look.still, dy)
        rp, sp = ref.load(), still.load()
        for y in range(CELL):
            for x in range(CELL):
                if px[x, y] == rp[x, y]:
                    op[x, y] = sp[x, y]
        if look.bare_arms and arms_up:
            under = raised_arm.plate(orange)
            for side in arms_up:
                hand = 23 if side == "left" else CELL - 1 - 23
                if not px[hand, 51 + dy][3]:        # her resting hand is gone: the arm is up in this frame
                    lift_arm(out, frame, look, dy, side, under)
    return tone.fair(closed(out) if kind == "side" else out, frame, kind, hb)


def dress_strip(strip, look, kind, orange, arms_up=()):
    out = Image.new("RGBA", strip.size, CLEAR)
    for i in range(strip.width // CELL):
        frame = strip.crop((i * CELL, 0, (i + 1) * CELL, CELL))
        out.paste(dress_frame(frame, look, kind, orange, arms_up), (i * CELL, 0))
    return out


def main():
    root = sys.argv[1]
    source = os.path.join(root, "outfits", "source")
    orange = Image.open(os.path.join(source, "luz-base-front.png")).convert("RGBA")
    stills = outfits.approved(orange)
    looks = {
        "halloween": AsDrawn(orange),
        "candy": CandyHoodie(stills["candy"], outfits.WHITE),
        "valentines": Hoodie(stills["valentines"], outfits.PINK),
        "easter": EasterDress(stills["easter"]),
        "summer": Summer(stills["summer"]),
    }
    for name, look in looks.items():
        folder = os.path.join(root, "outfits", name)
        os.makedirs(folder, exist_ok=True)
        for strip_name, kind in STRIPS.items():
            strip = Image.open(os.path.join(source, strip_name + ".png")).convert("RGBA")
            dressed = dress_strip(strip, look, kind, orange, ARMS_UP.get(strip_name, ()))
            dressed.save(os.path.join(folder, strip_name + ".png"))
        print(name, "dressed", len(STRIPS), "strips")


if __name__ == "__main__":
    main()
