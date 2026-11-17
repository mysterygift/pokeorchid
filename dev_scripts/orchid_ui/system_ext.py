"""
Helpers for the Options / Save prompt / Start menu mockups (mock_options.py, mock_system.py,
anim_options.py). PROPOSED kit additions live here until the user approves them.

Compositing follows kit_ext: BG3 grid (or field) -> BG art -> text -> OBJ.

Palettes used (all 16 colours, index 0 transparent):
  * kit 'orchid' palette with SPARE_A / SPARE_B = the player's name colour (fg, shadow),
    patched at load time from the save's gender -> std windows, start menu, save card.
  * FIELD_PAL_A / FIELD_PAL_B: option icon fields (BW colour-coded, Gen 3 3-step ramps).
  * ARROW_PAL: Gen 3 red chevrons (+ one flash colour).
  * menu_icons.PALETTE: start menu icons, reused for the saving Poké Ball.
"""
import math
import os
from PIL import Image
from kit import *
import kit_ext as K
import windows as Wn
import menu_icons as MI
from gamefont import draw_text, text_width
from battle_ext import NAME_MALE, NAME_FEMALE, silhouette

W, H = 240, 160
G = K.G
HERE = os.path.dirname(os.path.abspath(__file__))


def p_sheet(w, h, pal):
    im = Image.new("P", (w, h), 0)
    flat = [c for rgb in pal for c in rgb]
    im.putpalette(flat + [0] * (768 - len(flat)))
    return im


def comp(out, im, pal=None, at=(0, 0)):
    out.alpha_composite(K.sheet_rgba(im, pal), at)


def name_colours(gender):
    return NAME_MALE if gender == "M" else NAME_FEMALE


def std_pal_kw(gender="M"):
    """kit palette kwargs for std windows that print the player's name."""
    fg, sh = name_colours(gender)
    return dict(spare_a=fg, spare_b=sh)


# ------------------------------------------------------------------ icon-field palettes
# Same ramps as the battle action buttons (light, face, dark) + purple / teal for the extra rows.
RAMPS = {
    "red": ((248, 160, 136), (224, 80, 64), (152, 32, 48)),
    "yellow": ((248, 224, 120), (224, 168, 32), (152, 96, 16)),
    "green": ((160, 224, 120), (80, 168, 72), (32, 104, 56)),
    "blue": ((152, 192, 248), (72, 128, 216), (40, 72, 152)),
    "purple": ((216, 168, 240), (152, 88, 200), (88, 40, 136)),
    "teal": ((144, 224, 216), (48, 168, 160), (24, 104, 104)),
}
_FA, _FB = ["red", "yellow", "green", "blue"], ["purple", "teal"]
FIELD_PAL_A = [snap(c) for c in [(0, 0, 0), (40, 40, 64), (248, 248, 248)]
               + [c for k in _FA for c in RAMPS[k]] + [(0, 0, 0)]]
FIELD_PAL_B = [snap(c) for c in [(0, 0, 0), (40, 40, 64), (248, 248, 248)]
               + [c for k in _FB for c in RAMPS[k]] + [(0, 0, 0)] * 7]


def field_pal_idx(colour, step):
    """(palette, index) for a ramp step (0 light, 1 face, 2 dark)."""
    if colour in _FA:
        return "A", 3 + _FA.index(colour) * 3 + step
    return "B", 3 + _FB.index(colour) * 3 + step


# ------------------------------------------------------------------ silhouettes (white, 1px drop shadow)
SIL = {
    "text": [              # speech bubble with "..." + speed lines
        ".....XXXXXXX.",
        "XXX.XXXXXXXXX",
        "....XX.X.X.XX",
        ".XX.XXXXXXXXX",
        ".....XXXXXXX.",
        "........XX...",
        ".......X.....",
    ],
    "scene": [             # sparkle burst (move animations)
        "....X.....X.",
        "....X....XXX",
        "...XXX....X.",
        "..XXXXX.....",
        "XXXXXXXXX...",
        "..XXXXX.....",
        "...XXX......",
        "....X.......",
        "....X.......",
    ],
    "style": [             # swap arrows (shift)
        ".......X...",
        ".......XX..",
        "XXXXXXXXXX.",
        ".......XX..",
        ".......X...",
        "...X.......",
        "..XX.......",
        ".XXXXXXXXXX",
        "..XX.......",
        "...X.......",
    ],
    "sound": [             # speaker + waves
        "....X.....X.",
        "...XX...X..X",
        "XXXXX.X..X.X",
        "XXXXX..X.X.X",
        "XXXXX..X.X.X",
        "XXXXX.X..X.X",
        "...XX...X..X",
        "....X.....X.",
    ],
    "button": [            # L shoulder button
        "...XXXXXXXX.",
        "..XXXXXXXXXX",
        ".XXX.XXXXXXX",
        "XXXX.XXXXXXX",
        "XXXX.XXXXXXX",
        "XXXX...XXXXX",
        "XXXXXXXXXXXX",
    ],
    "frame": [             # window with two text lines
        "XXXXXXXXXXX",
        "X.........X",
        "X.XXXXXX..X",
        "X.........X",
        "X.XXXX....X",
        "X.........X",
        "XXXXXXXXXXX",
    ],
    "cancel": [            # back arrow (U-turn)
        "...X.....",
        "..XX.....",
        ".XXXXXXX.",
        "XXXXXXXXX",
        ".XXX...XX",
        "..XX...XX",
        "...X..XX.",
        "...XXXX..",
    ],
    # save card
    "pin": ["..XXX..", ".XXXXX.", "XXX.XXX", "XX...XX", "XXX.XXX", ".XXXXX.", "..XXX..", "...X..."],
    "player": ["..XXX..", ".XXXXX.", ".XXXXX.", "..XXX..", ".......", ".XXXXX.", "XXXXXXX", "XXXXXXX"],
    "badge": ["...X...", "...X...", "XXXXXXX", ".XXXXX.", "..XXX..", ".XX.XX.", ".X...X."],
    "dex": ["..XXXX..", ".XXXXXX.", "XXX..XXX", "...XX...", "...XX...", "XXX..XXX", ".XXXXXX.", "..XXXX.."],
    "clock": ["..XXX..", ".XXXXX.", "XXX.XXX", "XXX..XX", "XXXXXXX", ".XXXXX.", "..XXX.."],
}


def sil_size(rows):
    return len(rows[0]) + 1, len(rows) + 1


def centred_sil(cv, x, y, w, h, key, fg, shadow):
    rows = SIL[key]
    pw, ph = sil_size(rows)
    silhouette(cv, x + (w - pw + 1) // 2, y + (h - ph + 1) // 2, rows, fg, shadow)


# ------------------------------------------------------------------ chevrons (OBJ 8x16 each)
ARROW_PAL = [snap(c) for c in [(0, 0, 0), ARROW_RED[1], ARROW_RED[0], (248, 200, 136)]] + [(0, 0, 0)] * 12


def chevron(out, x, y, left=True, flash=False):
    """Gen 3 6x9 chevron at its top-left pixel. flash: lit fill + 1px push outward."""
    im = p_sheet(8, 16, ARROW_PAL)
    stamp(Canvas(im), 1, 3, SMALL_ARROW, {"O": 1, "F": 3 if flash else 2}, hflip=not left)
    dx = (-1 if left else 1) if flash else 0
    comp(out, im, at=(x - 1 + dx, y - 3))


# ------------------------------------------------------------------ menu icons (start menu OBJ sheet)
_ICON_SHEET = os.path.join(K.ROOT, "graphics", "start_menu", "menu_icons.png")


def menu_icon(name, muted=0.0):
    """16x16 start-menu icon (real asset if present, else built from menu_icons.py)."""
    k = MI.NAMES.index(name)
    if os.path.exists(_ICON_SHEET):
        im = Image.open(_ICON_SHEET).crop((0, k * 16, 16, k * 16 + 16))
    else:
        im = MI.build().crop((0, k * 16, 16, k * 16 + 16))
    pal = list(MI.PALETTE)
    if muted:
        pal = [snap(tuple(int(v + (g - v) * muted) for v, g in zip(c, (184, 184, 200)))) for c in pal]
        pal[1] = MI.PALETTE[1]
    return K.sheet_rgba(im, pal)


# ------------------------------------------------------------------ field scene (approved look)
FIELD_KW = dict(spare_a=(120, 184, 96), spare_b=(96, 152, 80))


def field_scene(player="brendan", show_player=True):
    im = new_sheet(W, H, "orchid", **FIELD_KW)
    cv = Canvas(im)
    cv.rect(0, 0, W - 1, H - 1, SPARE_A)
    for y in range(0, H, 8):
        for x in range((y // 8 % 2) * 8, W, 16):
            cv.rect(x + 2, y + 3, x + 3, y + 4, SPARE_B)
    out = K.sheet_rgba(im)
    if show_player:
        spr = Image.open(G("object_events", "pics", "people", player, "walking.png"))
        out.alpha_composite(K.sheet_rgba(spr.crop((0, 0, 16, 32))), (112, 56))
    return out


# ------------------------------------------------------------------ message box + YES/NO (approved)
def message(out, text, gender="M"):
    def fn(cv):
        Wn.dialogue_box(cv, 2, 15, 27, 4)
        draw_text(cv, 16, 120, text, INK, PANEL_SHADE)
    K.layer(out, fn, "orchid", **std_pal_kw(gender))


def down_arrow(out, x, y, bob=0):
    """Gen 3 red 'continue' arrow (graphics/fonts/down_arrow.png shape)."""
    rows = ["XXXXXXX", "XRRRRRX", "XRRRRRX", "XRRRRRX", ".XRRRX.", "..XRX..", "...X..."]
    im = p_sheet(8, 8, ARROW_PAL)
    stamp(Canvas(im), 0, 0, rows, {"X": 1, "R": 2})
    comp(out, im, at=(x, y + bob))


YESNO = (23, 9, 5, 4)


def yes_no(out, cursor=0):
    tx, ty, tw, th = YESNO

    def fn(cv):
        Wn.std_frame(cv, tx, ty, tw, th)
        Wn.selection_bar(cv, tx * 8 + 2, ty * 8 + 1 + cursor * 16, 36, 14)
        draw_text(cv, tx * 8 + 8, ty * 8, "YES", INK, PANEL_SHADE)
        draw_text(cv, tx * 8 + 8, ty * 8 + 16, "NO", INK, PANEL_SHADE)
    K.layer(out, fn, "orchid")


# ------------------------------------------------------------------ save card (std window, 14x10 tiles)
SAVE_WIN = (1, 1, 14, 10)            # sSaveInfoWindowTemplate
CAP_W = 16


def recolour_cap(cv, x0, y0, x1, y1, face, light, dark, divider=True):
    """Re-ink the left end of a kit pill: WHITE->light, PANEL->face, PANEL_SHADE->dark (outline kept)."""
    m = {WHITE: light, PANEL: face, PANEL_SHADE: dark}
    for y in range(y0, y1 + 1):
        inside = False                      # only recolour right of the pill's left outline
        for x in range(x0, x1 + 1):
            c = cv.get(x, y)
            if c == INK:
                inside = True
            elif inside and c in m:
                cv.set(x, y, m[c])
    if divider:
        cv.vline(x1 + 1, y0 + 1, y1 - 1, INK)


def label_pill(cv, x, y, w, key):
    """Panel pill with an accent left cap holding a white silhouette (dex label-pill language)."""
    rounded_box(cv, x, y, w, 14, 4, PANEL, INK, WHITE, PANEL_SHADE)
    recolour_cap(cv, x, y, x + CAP_W - 1, y + 13, ACCENT, ACCENT_LIGHT, ACCENT_DARK)
    centred_sil(cv, x + 1, y + 1, CAP_W - 1, 12, key, WHITE, ACCENT_DARK)


def save_card(cv, data):
    tx, ty, tw, th = SAVE_WIN
    Wn.std_frame(cv, tx, ty, tw, th)
    x0, y0, w = tx * 8, ty * 8, tw * 8
    # location band
    rounded_box(cv, x0 + 1, y0 + 1, w - 2, 14, 4, ACCENT, INK, ACCENT_LIGHT, ACCENT_DARK)
    rows = SIL["pin"]
    silhouette(cv, x0 + 6, y0 + 3, rows, WHITE, ACCENT_DARK)
    loc = data["location"]
    draw_text(cv, x0 + (w - text_width(loc)) // 2 + 4, y0, loc, WHITE, ACCENT_DARK)
    entries = [("player", "PLAYER", data["name"], True), ("badge", "BADGES", str(data["badges"]), False),
               ("dex", "POKéDEX", str(data["dex"]), False), ("clock", "TIME", data["time"], False)]
    for i, (key, label, val, is_name) in enumerate(entries):
        y = y0 + 16 * (i + 1)
        label_pill(cv, x0 + 1, y + 1, w - 2, key)
        draw_text(cv, x0 + CAP_W + 5, y, label, INK, PANEL_SHADE, font="narrow")
        fg, sh = (SPARE_A, SPARE_B) if is_name else (INK, PANEL_SHADE)
        draw_text(cv, x0 + w - 6 - text_width(val), y, val, fg, sh)


# ------------------------------------------------------------------ saving Poké Ball (OBJ 16x16, menu-icon palette)
def pokeball_frame(angle_deg):
    """14px Poké Ball rocking like a capture wobble; menu_icons palette roles."""
    C = MI.CMAP
    im = p_sheet(16, 16, MI.PALETTE)
    cv = Canvas(im)
    cx, cy, r = 8.0, 8.0, 7.0
    a = math.radians(angle_deg)
    nx, ny = math.sin(a), -math.cos(a)                 # "up" normal of the band
    for y in range(16):
        for x in range(16):
            dx, dy = x + 0.5 - cx, y + 0.5 - cy
            d = math.hypot(dx, dy)
            if d > r:
                continue
            s = dx * nx + dy * ny                     # >0 = top (red) half
            lit = -(dx + dy) / r
            if d > r - 1.0:
                c = "k"
            elif abs(s) < 0.9:
                c = "k"
            elif s > 0:
                c = "o" if lit > 0.55 else ("R" if lit < -0.45 else "r")
            else:
                c = "w" if lit > 0.35 else ("m" if lit < -0.45 else "l")
            cv.set(x, y, C[c])
    # centre button: ink ring + white face, sits on the band
    bx, by = cx + 0.0, cy
    for y in range(16):
        for x in range(16):
            d = math.hypot(x + 0.5 - bx, y + 0.5 - by)
            if d <= 1.5:
                cv.set(x, y, C["w"])
            elif d <= 2.6:
                cv.set(x, y, C["k"])
    cv.set(int(cx - 3), int(cy - 3), C["w"])           # glint
    return K.sheet_rgba(im)


def sparkle(out, x, y, big=True):
    """Tiny capture-style star (gold, ink outline)."""
    rows = ([".k.", "kyk", ".k."] if not big else
            ["..k..", ".kyk.", "kyyyk", ".kyk.", "..k.."])
    im = p_sheet(8, 8, MI.PALETTE)
    stamp(Canvas(im), 0, 0, rows, {"k": MI.CMAP["k"], "y": MI.CMAP["y"]})
    comp(out, im, at=(x, y))


# ------------------------------------------------------------------ window-frame types (3x3 tiles)
# FRAME option: 8 kit-built frames replace vanilla types 2-20. Every frame is the approved std-frame
# geometry (2px transparent margin, ink, 3px band, ink, white fill) drawn with kit role indices;
# only the band ramp (ACCENT_DARK/ACCENT/ACCENT_LIGHT/ACCENT_PALE) and the trim change, so each frame
# is one 16-colour palette + one 24x24 tile set in graphics/text_window layout (9-slice).
FRAME_NAMES = ["Orchid", "Blue", "Rose", "Leaf", "Brass", "Grid", "Wood", "Poké Ball"]
FRAME_RAMPS = {   # ACCENT_DARK, ACCENT, ACCENT_LIGHT, ACCENT_PALE
    5: [(160, 104, 40), (216, 168, 72), (248, 224, 144), (248, 240, 200)],    # battle_ext HB brass ramp
    6: [(24, 24, 32), (56, 56, 72), (120, 128, 144), (184, 192, 208)],       # backdrop.GRID_PAL, lifted
    7: [(104, 64, 40), (152, 96, 56), (200, 136, 80), (232, 184, 128)],      # satchel leather ramp
    8: [(176, 72, 56), (224, 88, 56), (248, 144, 56), (248, 200, 160)],      # poke_ball.pal reds
}
FRAME_THEME = {1: "orchid", 2: "male", 3: "female", 4: "leaf"}


def frame_palette(n):
    if n in FRAME_THEME:
        return palette(FRAME_THEME[n])
    pal = palette("orchid")
    for i, c in zip((ACCENT_DARK, ACCENT, ACCENT_LIGHT, ACCENT_PALE), FRAME_RAMPS[n]):
        pal[i] = snap(c)
    return pal


def _corner_pts(x0, y0, w, h, k):
    """The four band-corner anchor points k px in from the outer edge."""
    return [(x0 + k, y0 + k), (x0 + w - 1 - k, y0 + k), (x0 + k, y0 + h - 1 - k), (x0 + w - 1 - k, y0 + h - 1 - k)]


def kit_frame(cv, n, tx, ty, tw, th):
    """Draw frame type n around text rect (tx, ty, tw, th). Trim repeats per 8px tile so it 9-slices."""
    Wn.std_frame(cv, tx, ty, tw, th)
    x0, y0 = tx * 8 - 8, ty * 8 - 8
    w, h = tw * 8 + 16, th * 8 + 16
    if n == 5:                       # brass: groove along the band + round rivets in the corners
        for (cx, cy) in _corner_pts(x0, y0, w, h, 3):      # 7px studs fill each corner tile's band
            disc(cv, cx + 0.5, cy + 0.5, 3.5, ACCENT, INK, ACCENT_PALE, ACCENT_DARK)
            cv.set(cx - 1, cy - 1, WHITE)
    elif n == 6:                     # grid: light tick across the band at every tile centre
        for x in range(x0 + 8, x0 + w - 8):
            if x % 8 == 4:
                cv.vline(x, y0 + 3, y0 + 5, ACCENT_PALE)
                cv.vline(x, y0 + h - 6, y0 + h - 4, ACCENT_PALE)
        for y in range(y0 + 8, y0 + h - 8):
            if y % 8 == 4:
                cv.hline(x0 + 3, x0 + 5, y, ACCENT_PALE)
                cv.hline(x0 + w - 6, x0 + w - 4, y, ACCENT_PALE)
        for (cx, cy) in _corner_pts(x0, y0, w, h, 4):       # corner plus
            cv.hline(cx - 1, cx + 1, cy, ACCENT_PALE)
            cv.vline(cx, cy - 1, cy + 1, ACCENT_PALE)
    elif n == 7:                     # wood: grain dashes along the band, mitred corners
        for x in range(x0 + 8, x0 + w - 8):
            if x % 8 in (1, 2, 3, 4):
                cv.set(x, y0 + 4, ACCENT_DARK)
                cv.set(x, y0 + h - 5, ACCENT_DARK)
        for y in range(y0 + 8, y0 + h - 8):
            if y % 8 in (3, 4, 5, 6):
                cv.set(x0 + 4, y, ACCENT_DARK)
                cv.set(x0 + w - 5, y, ACCENT_DARK)
        for k in (3, 4, 5):          # mitre joints
            cv.set(x0 + k, y0 + k, ACCENT_DARK)
            cv.set(x0 + w - 1 - k, y0 + k, ACCENT_DARK)
            cv.set(x0 + k, y0 + h - 1 - k, ACCENT_DARK)
            cv.set(x0 + w - 1 - k, y0 + h - 1 - k, ACCENT_DARK)
    elif n == 8:                     # Poké Ball: red band, a mini ball on each corner
        for (cx, cy) in _corner_pts(x0, y0, w, h, 3):
            mini_ball(cv, cx, cy)


def mini_ball(cv, cx, cy):
    """7x7 Poké Ball centred on pixel (cx, cy): red top, white bottom, ink band + button."""
    rows = ["..III..",
            ".IRRLI.",
            "IRRRRRI",
            "IIIWIII",
            "IWWWWSI",
            ".IWWSI.",
            "..III.."]
    stamp(cv, cx - 3, cy - 3, rows, {"I": INK, "R": ACCENT, "L": ACCENT_LIGHT, "W": WHITE, "S": PANEL_SHADE})


def frame_sheet(n):
    """24x24 'P' sheet in text_window layout (TL T TR / L C R / BL B BR) with the frame's palette."""
    im = new_sheet(24, 24, "orchid")
    flat = [c for rgb in frame_palette(n) for c in rgb]
    im.putpalette(flat + [0] * (768 - len(flat)))
    kit_frame(Canvas(im), n, 1, 1, 1, 1)
    return im


def frame_tiles(n):
    return K.sheet_rgba(frame_sheet(n))


def frame_tile_count(n):
    tiles, _ = to_tiles(frame_sheet(n))
    return len(tiles) - 1          # minus the blank tile


def draw_frame_type(out, n, tx, ty, tw, th, fill=(248, 248, 248)):
    """Frame type n (1-8) as a 9-slice of its 24x24 tile set (the way the ROM draws std frames)."""
    """9-slice a frame-type tile set around text rect (tx, ty, tw, th) like DrawStdFrameWithCustomTile."""
    t = frame_tiles(n)
    cell = lambda cx, cy: t.crop((cx * 8, cy * 8, cx * 8 + 8, cy * 8 + 8))
    x0, y0 = tx * 8 - 8, ty * 8 - 8
    for j in range(th + 2):
        for i in range(tw + 2):
            cx = 0 if i == 0 else (2 if i == tw + 1 else 1)
            cy = 0 if j == 0 else (2 if j == th + 1 else 1)
            if cx == 1 and cy == 1:
                out.paste(Image.new("RGBA", (8, 8), fill + (255,)), (x0 + i * 8, y0 + j * 8))
            else:
                out.alpha_composite(cell(cx, cy), (x0 + i * 8, y0 + j * 8))


# ------------------------------------------------------------------ keypad glyphs (graphics/fonts/keypad_icons.png)
KEYPAD = {"A": (0, 8), "B": (8, 8), "L": (16, 16), "R": (32, 16), "START": (48, 16), "SELECT": (64, 16)}


def keypad(cv, x, y, key, face=WHITE, edge=INK):
    """ROM keypad glyph (text-printer icon) mapped onto kit roles: face WHITE, edge INK."""
    im = Image.open(G("fonts", "keypad_icons.png"))
    px = im.load()
    ox, w = KEYPAD[key]
    for yy in range(4, 12):
        for xx in range(w):
            v = px[ox + xx, yy]
            if v == 1:
                cv.set(x + xx, y + yy - 4, face)
            elif v == 2:
                cv.set(x + xx, y + yy - 4, edge)
    return w


# ------------------------------------------------------------------ misc
def b_disc(cv, cx, cy):
    """Small white B-button disc (as the battle BACK tab)."""
    disc(cv, cx, cy, 5, WHITE, INK, None, PANEL_SHADE)
    stamp(cv, int(cx) - 2, int(cy) - 2, ["XXX.", "X..X", "XXX.", "X..X", "XXX."], {"X": INK})


def brass_rivet(cv, x, y):
    cv.set(x, y, SELECT_LIGHT)
    cv.set(x + 1, y, SELECT)
    cv.set(x, y + 1, SELECT)
    cv.set(x + 1, y + 1, SELECT_DARK)


def sheet_grid(panels, cols, scale=2, cap_h=16, pad=12, bg=(28, 28, 36)):
    """[(caption, RGBA 240x160)] -> captioned sheet."""
    from PIL import ImageDraw
    rows = (len(panels) + cols - 1) // cols
    pw, ph = panels[0][1].size[0] * scale, panels[0][1].size[1] * scale
    out = Image.new("RGBA", (cols * pw + (cols + 1) * pad, rows * (ph + cap_h) + (rows + 1) * pad), bg + (255,))
    d = ImageDraw.Draw(out)
    for i, (cap, im) in enumerate(panels):
        x = pad + (i % cols) * (pw + pad)
        y = pad + (i // cols) * (ph + cap_h + pad)
        d.text((x, y), cap, fill=(230, 230, 240))
        out.paste(K.upscale(im, scale), (x, y + cap_h))
    return out
