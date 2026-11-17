"""
Trainer Card helpers for the Orchid UI mockups (PROPOSED kit additions live here
until the user approves them). Used by mock_card.py / anim_card.py.

Card palette (one 16-colour BG palette, kit role layout with the selection
slots re-used, because the card has no cursor):

    1-10  kit roles (INK ... ACCENT_PALE), accents = gender theme
    11-13 METAL_DARK / METAL / METAL_LIGHT  -> card TIER (brass, bronze, copper,
          silver, gold). Changing tier = rewriting these 3 colours, no tiles.
    14-15 NAME fg / shadow  -> battle_ext.NAME_MALE / NAME_FEMALE

New primitives: card_shell(), header_tab(), star_pip(), icon_pill(), badge_case(),
socket(), sig_well(), card ICONS (white silhouettes on an accent cap), and the
vanilla flip maths (flip_rows / darken) so the GIF matches trainer_card.c.
"""
import os
from PIL import Image
from kit import *
import kit_ext as KX
from battle_ext import big_round_box, mask_box, round_mask, chamfer_mask, NAME_MALE, NAME_FEMALE
from dex_ext import dais

G = KX.G
METAL_DARK, METAL, METAL_LIGHT, NAME_FG, NAME_SH = 11, 12, 13, 14, 15

# Tier metals (dark, mid, light). 0 stars = brass "standard issue"; 1-4 follow vanilla's
# bronze -> copper -> silver -> gold order (vanilla's 0-star tier was a green card).
TIERS = [
    ("brass", [(136, 104, 56), (192, 160, 88), (232, 216, 152)]),
    ("bronze", [(120, 64, 32), (176, 112, 64), (224, 168, 120)]),
    ("copper", [(144, 56, 40), (208, 104, 72), (248, 168, 136)]),
    ("silver", [(104, 112, 136), (168, 176, 200), (240, 240, 248)]),
    ("gold", [(200, 112, 0), (248, 192, 0), (248, 248, 144)]),
]


def card_palette(theme="male", tier=0):
    p = palette(theme)
    for i, c in zip((METAL_DARK, METAL, METAL_LIGHT), TIERS[tier][1]):
        p[i] = snap(c)
    fg, sh = NAME_FEMALE if theme == "female" else NAME_MALE
    p[NAME_FG], p[NAME_SH] = snap(fg), snap(sh)
    return p


def card_sheet(w, h, theme="male", tier=0):
    im = Image.new("P", (w, h), 0)
    flat = [c for rgb in card_palette(theme, tier) for c in rgb]
    im.putpalette(flat + [0] * (768 - len(flat)))
    return im


# ------------------------------------------------------------------ silhouettes (white + 1px shadow)
ICONS = {
    "money": ["...XXXXX...",        # mon coin with a square hole
              ".XXXXXXXXX.",
              ".XXXXXXXXX.",
              "XXXX...XXXX",
              "XXXX...XXXX",
              "XXXX...XXXX",
              ".XXXXXXXXX.",
              ".XXXXXXXXX.",
              "...XXXXX..."],
    "dex": ["...XXXX...",           # Poké Ball (caught count): band gap, centre button
            ".XXXXXXXX.",
            "XXXXXXXXXX",
            "XXX....XXX",
            "....XX....",
            "XXX....XXX",
            "XXXXXXXXXX",
            ".XXXXXXXX.",
            "...XXXX..."],
    "time": ["..XXXXX..",           # clock, hands at 12 and 3
             ".XXXX.XXX.",
             "XXXXX.XXXX",
             "XXXXX.XXXX",
             "XXXXX...XX",
             "XXXXXXXXXX",
             "XXXXXXXXXX",
             ".XXXXXXXX.",
             "..XXXXXX.."],
    "hof": ["XXXXXXXXXX",           # trophy
            "X.XXXXXX.X",
            "X.XXXXXX.X",
            ".XXXXXXXX.",
            "..XXXXXX..",
            "....XX....",
            "....XX....",
            "..XXXXXX..",
            "..XXXXXX.."],
    "link": ["X........X",          # crossed blades (battles)
             "XX......XX",
             ".XX....XX.",
             "..XX..XX..",
             "...XXXX...",
             "....XX....",
             "...XXXX...",
             ".XXX..XXX.",
             "XXX....XXX",
             "XX......XX"],
    "trade": [".....XX...",          # swap arrows
              "XXXXXXXX..",
              "XXXXXXXXX.",
              "XXXXXXXX..",
              ".....XX...",
              "...XX.....",
              "..XXXXXXXX",
              ".XXXXXXXXX",
              "..XXXXXXXX",
              "...XX....."],
    "union": ["..XX...XX..",         # two trainers
              ".XXXX.XXXX.",
              ".XXXX.XXXX.",
              "..XX...XX..",
              "...........",
              ".XXXX.XXXX.",
              "XXXXX.XXXXX",
              "XXXXX.XXXXX"],
    "berry": ["....XX...",           # Oran-style berry with a leaf
              "...X.XXX.",
              ".XXXXXX..",
              "XXXXXXXX.",
              "XXXXXXXXX",
              "XXXXXXXXX",
              "XXXXXXXXX",
              ".XXXXXXX.",
              "..XXXXX.."],
    "contest": ["..XXXXX..",         # rosette ribbon
                ".XXXXXXX.",
                "XXXX.XXXX",
                "XXX...XXX",
                "XXXX.XXXX",
                ".XXXXXXX.",
                "..XXXXX..",
                "..XX.XX..",
                ".XX...XX.",
                ".X.....X."],
    "pen": ["........XX",            # signature nib
            ".......XXX",
            "......XXX.",
            ".....XXX..",
            "....XXX...",
            "...XXX....",
            "..XXX.....",
            ".XX.......",
            "X.........",
            "XXXXXXXXXX"],
}


def icon(cv, x, y, name, fg=WHITE, shadow=ACCENT_DARK):
    rows = ICONS[name]
    for dx, dy, c in ((1, 1, shadow), (0, 0, fg)):
        for r, row in enumerate(rows):
            for q, ch in enumerate(row):
                if ch == "X":
                    cv.set(x + q + dx, y + r + dy, c)


def icon_size(name):
    rows = ICONS[name]
    return max(len(r) for r in rows), len(rows)


# ------------------------------------------------------------------ card pieces
def card_shell(cv, x0, y0, w, h, head_h):
    """
    The card: rounded ink outline, 3px gender-accent band (light TL, dark BR) that
    widens into a header strip of head_h px, a 1px tier-metal trim line, an ink
    line, then the panel face. Returns the face rect (x0, y0, x1, y1) inside the ink.
    """
    big_round_box(cv, x0, y0, w, h, 7, ACCENT, INK, ACCENT_LIGHT, ACCENT_DARK)
    fx0, fy0, fx1, fy1 = x0 + 4, y0 + head_h, x0 + w - 5, y0 + h - 5
    # metal trim (1px) just outside the face's ink line: light on top/left, dark bottom/right
    m = round_mask(fx1 - fx0 + 3, fy1 - fy0 + 3, 4)
    for (x, y) in m:
        if (x - 1, y) not in m or (x, y - 1) not in m:
            cv.set(fx0 - 1 + x, fy0 - 1 + y, METAL_LIGHT)
        elif (x + 1, y) not in m or (x, y + 1) not in m:
            cv.set(fx0 - 1 + x, fy0 - 1 + y, METAL_DARK)
    mask_box(cv, fx0, fy0, round_mask(fx1 - fx0 + 1, fy1 - fy0 + 1, 3), PANEL, INK, WHITE, PANEL_SHADE)
    return fx0 + 1, fy0 + 1, fx1 - 1, fy1 - 1


def rivet(cv, x, y):
    """2x2 tier-metal rivet with an ink rim (3x3 footprint incl. shade)."""
    cv.set(x, y, METAL_LIGHT)
    cv.set(x + 1, y, METAL)
    cv.set(x, y + 1, METAL)
    cv.set(x + 1, y + 1, METAL_DARK)


def header_tab(cv, x, y, w, h):
    """Stepped dark tab (ACCENT_DARK) with a chamfered right end and tier-metal top lip."""
    m = chamfer_mask(w, h, tr=h - 4, br=1, tl=1, bl=1)
    mask_box(cv, x, y, m, ACCENT_DARK, INK, METAL, INK)
    # lower step: a 1px accent line under the tab's face, like healthbox B's body seam
    return m


STAR7 = ["...L...",
         "..LLL..",
         "LLLLLMM",
         ".LLLMM.",
         "..LMM..",
         ".LMDMD.",
         ".MD..D."]


def star_pip(cv, x, y, lit):
    """11x11 pip: round ink recess with an accent catch-light; lit = 7x7 tier-metal star."""
    disc(cv, x + 5.5, y + 5.5, 5.5, INK, None)
    if lit:
        stamp(cv, x + 2, y + 2, STAR7, {"L": METAL_LIGHT, "M": METAL, "D": METAL_DARK})
    else:
        stamp(cv, x + 2, y + 2, STAR7, {"L": ACCENT_DARK, "M": ACCENT_DARK, "D": ACCENT_DARK})


def label_cap_pill(cv, x, y, w, cap_w, h=14, cap=(ACCENT, ACCENT_LIGHT, ACCENT_DARK)):
    """dex_ext.label_pill with selectable cap colours (face, light, shade)."""
    face, light, shade = cap
    rounded_box(cv, x, y, w, h, 4, PANEL, INK, WHITE, PANEL_SHADE)
    for yy in range(1, h - 1):
        for xx in range(1, cap_w):
            if cv.get(x + xx, y + yy) in (PANEL, WHITE, PANEL_SHADE):
                c = face
                if yy == 1 or cv.get(x + xx - 1, y + yy) == INK:
                    c = light
                elif yy == h - 2:
                    c = shade
                cv.set(x + xx, y + yy, c)
    cv.vline(x + cap_w, y + 1, y + h - 2, INK)


def icon_pill(cv, x, y, w, name, cap_w=20, h=16):
    """Picture label: accent cap holding a white silhouette, panel value area."""
    label_cap_pill(cv, x, y, w, cap_w, h)
    iw, ih = icon_size(name)
    icon(cv, x + (cap_w - iw) // 2 + (1 if iw % 2 == 0 else 0), y + (h - ih) // 2, name)


def socket(cv, cx, cy, earned=False):
    """24px badge socket (integer centre = even diameter, symmetric): ink rim, tier-metal ring
    (lit TL, dark BR), ink lip, dark 16px recess. Empty = plain recess with a soft inner shadow
    (as the approved empty status socket); earned = badge art on BG3 covers the recess."""
    disc(cv, cx, cy, 12, METAL, INK, METAL_LIGHT, METAL_DARK)
    disc(cv, cx, cy, 9, INK, None)
    disc(cv, cx, cy, 8, ACCENT_DARK, None)
    if not earned:
        for yy in range(cy - 8, cy + 8):
            for xx in range(cx - 8, cx + 8):
                d2 = (xx + 0.5 - cx) ** 2 + (yy + 0.5 - cy) ** 2
                if 7 ** 2 < d2 <= 8 ** 2:
                    up = (xx + 0.5 - cx) + (yy + 0.5 - cy) < 0
                    cv.set(xx, yy, INK if up else ACCENT)


def nameplate(cv, x, y, w, h):
    """Engraved plate: ink rim, 1px tier-metal bezel (light TL / dark BR), ink lip, panel face."""
    big_round_box(cv, x - 2, y - 2, w + 4, h + 4, 5, METAL, INK, METAL_LIGHT, METAL_DARK)
    rounded_box(cv, x, y, w, h, 4, PANEL, INK, WHITE, PANEL_SHADE)


def badge_case(cv, x, y, w, h):
    """Recessed velvet case in a tier-metal bezel: metal ring (light TL, dark BR) around an
    ink rim, dark inner shadow top-left, accent lip bottom-right."""
    big_round_box(cv, x - 3, y - 3, w + 6, h + 6, 6, METAL, INK, METAL_LIGHT, METAL_DARK)
    rounded_box(cv, x, y, w, h, 4, ACCENT_DARK, INK, INK, ACCENT)


def sig_well(cv, x, y, w, h):
    """Signature panel: recessed white card stock, a ruled line near the bottom."""
    rounded_box(cv, x, y, w, h, 3, WHITE, INK, PANEL_SHADE, WHITE)
    for xx in range(x + 24, x + w - 6):
        cv.set(xx, y + h - 5, PANEL_SHADE if xx % 2 else PANEL_DARK)


# ------------------------------------------------------------------ ROM art
def badge_rgba(i):
    """16x16 badge i (0-7) from graphics/trainer_card/badges.png with its own palette (BG pal 3 in vanilla)."""
    im = Image.open(G("trainer_card", "badges.png"))
    pal = [snap(tuple(im.getpalette()[k * 3:k * 3 + 3])) for k in range(16)]
    return KX.sheet_rgba(im.crop((i * 16, 0, i * 16 + 16, 16)), pal)


def trainer_pic(gender="male"):
    name = "may" if gender == "female" else "brendan"
    pal = [snap(c) for c in KX.load_jasc(G("trainers", "front_pics", name + ".pal"))]
    return KX.sprite_rgba(G("trainers", "front_pics", name + ".png"), pal=pal), pal


# ------------------------------------------------------------------ vanilla flip maths (trainer_card.c)
CARD_FLIP_Y = 160 // 2 - 3


def flip_offsets(card_top, down=True):
    """Per-scanline BG VOFS exactly as Task_AnimateCardFlipDown / Up compute it.
    Returns a list of 160 source-row offsets (row shown at line i = i + vofs[i])."""
    H = 160
    vofs = [0] * H
    card_bottom = H - card_top
    card_h = card_bottom - card_top
    r6 = -card_top << 16
    r5 = (H << 16) // card_h
    r5 -= 1 << 16
    var24 = r6 + r5 * card_h
    r10 = r5 // card_h
    if down:
        r5 *= 2
    else:
        r5 //= 2
    for i in range(card_top):
        vofs[i] = -i
    for i in range(card_top, card_bottom):
        vofs[i] = r6 >> 16
        r6 += r5
        r5 = r5 - r10 if down else r5 + r10
    for i in range(card_bottom, H):
        vofs[i] = var24 >> 16
    return vofs


def blend_y(card_top):
    """UpdateCardFlipRegs: BLDY darken level (0-16)."""
    y = (card_top + 40) // 10
    return 0 if y <= 4 else y


def squash(card, card_top, down=True):
    """Apply the scanline VOFS + WIN0V clip to an RGBA card layer (transparent elsewhere)."""
    if card_top <= 0:
        return card.copy()
    vofs = flip_offsets(card_top, down)
    out = Image.new("RGBA", card.size, (0, 0, 0, 0))
    src, dst = card.load(), out.load()
    for i in range(card_top, 160 - card_top):
        sy = (i + vofs[i]) % 256
        if sy < 160:
            for x in range(card.size[0]):
                dst[x, i] = src[x, sy]
    return out


def darken(im, evy):
    """GBA darken blend: I - I*EVY/16, applied to opaque pixels, snapped to BGR555."""
    if not evy:
        return im
    out = im.copy()
    px = out.load()
    for y in range(out.size[1]):
        for x in range(out.size[0]):
            r, g, b, a = px[x, y]
            if a:
                f = lambda v: (v - v * evy // 16) // 8 * 8
                px[x, y] = (f(r), f(g), f(b), a)
    return out
