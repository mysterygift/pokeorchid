"""
Pokédex helpers for the Orchid UI mockups (PROPOSED kit additions live here
until the user approves them).

  * Real dex data parsed from the ROM source: regional dex order (the ROM's
    Hoenn list, shown as the TOSA dex until Orchid's own order exists)
    (include/constants/pokedex.h), species name / category / height / weight /
    description / types (src/data/pokemon/species_info/gen_*_families.h),
    footprints (graphics/pokemon/<species>/footprint.png, 1bpp 16x16).
  * New primitives: dais(), label_pill(), tab_pill(), well(), tray(),
    caught_ball() (vanilla graphic remapped to kit roles), silhouette().
"""
import os
import re
from PIL import Image
from kit import *
from backdrop import band, pill
import kit_ext as KX

ROOT = KX.ROOT
G = KX.G

# Poké Ball red for the caught marker (graphics/items/icon_palettes/poke_ball.pal, 222,90,57).
BALL_RED = snap((222, 90, 57))
# Optional "device" theme for the A/B comparison only (BW Pokédex red/black).
DEVICE_RED = [(136, 24, 32), (200, 48, 48), (240, 128, 112), (248, 208, 200)]


def ensure_device_theme():
    """Register the comparison theme at runtime (kit.py itself is not edited)."""
    THEMES.setdefault("dex_red", DEVICE_RED)


def dex_palette(theme="orchid"):
    return palette(theme, spare_a=BALL_RED)


def selected(pal):
    p = list(pal)
    p[PANEL], p[WHITE], p[PANEL_SHADE] = pal[SELECT], pal[SELECT_LIGHT], pal[SELECT_DARK]
    return p


# ------------------------------------------------------------------ data
_cache = {}


def _flag(name):
    src = open(os.path.join(ROOT, "include", "config", "species_enabled.h")).read()
    m = re.search(r"#define\s+%s\s+(\w+)" % name, src)
    v = m.group(1) if m else "FALSE"
    if v in ("TRUE", "FALSE"):
        return v == "TRUE"
    return _flag(v)


def hoenn_order():
    """Species constants in Hoenn dex order, honouring HOENN_DEX_IF(config) entries."""
    if "hoenn" in _cache:
        return _cache["hoenn"]
    src = open(os.path.join(ROOT, "include", "constants", "pokedex.h")).read()
    body = src.split("#define FOREACH_SPECIES_IN_HOENN_DEX_ORDER(F)", 1)[1]
    out = []
    for line in body.splitlines()[1:]:
        line = line.strip()
        if not line:
            break
        m = re.match(r"HOENN_DEX_IF\((\w+),\s*F\((\w+)\)\)", line)
        if m:
            if _flag(m.group(1)):
                out.append(m.group(2))
        else:
            m = re.match(r"F\((\w+)\)", line)
            if m:
                out.append(m.group(1))
        if not line.endswith("\\"):
            break
    _cache["hoenn"] = out
    return out


def _species_blocks():
    if "blocks" in _cache:
        return _cache["blocks"]
    blocks = {}
    d = os.path.join(ROOT, "src", "data", "pokemon", "species_info")
    for fn in sorted(os.listdir(d)):
        if not fn.startswith("gen_"):
            continue
        src = open(os.path.join(d, fn)).read()
        parts = re.split(r"\n    \[SPECIES_(\w+)\]\s*=\s*\n", src)
        for i in range(1, len(parts) - 1, 2):
            blocks.setdefault(parts[i], parts[i + 1])
    _cache["blocks"] = blocks
    return blocks


def species(name):
    """dict(name, category, height_dm, weight_hg, desc, types, folder) for SPECIES_<name>."""
    b = _species_blocks()[name]
    get = lambda pat: (re.search(pat, b, re.S) or [None, None])[1]
    types = re.search(r"\.types\s*=.*?MON_TYPES\(([^)]*)\)", b).group(1)
    types = [t.strip().replace("TYPE_", "").lower() for t in types.split(",")]
    desc = re.search(r"\.description\s*=\s*COMPOUND_STRING\((.*?)\),\s*\n", b, re.S).group(1)
    desc = "".join(re.findall(r'"((?:[^"\\]|\\.)*)"', desc)).replace("\\n", "\n")
    return {
        "const": name,
        "name": get(r'\.speciesName\s*=\s*_\("(.*?)"\)'),
        "category": get(r'\.categoryName\s*=\s*_\("(.*?)"\)'),
        "height": int(get(r"\.height\s*=\s*(\d+)")),
        "weight": int(get(r"\.weight\s*=\s*(\d+)")),
        "desc": desc,
        "types": [t if t != "fighting" else "fight" for t in types],
        "folder": name.lower(),
    }


def fmt_height(dm):
    return "%d.%d m" % (dm // 10, dm % 10)


def fmt_weight(hg):
    return "%d.%d kg" % (hg // 10, hg % 10)


def footprint_mask(folder):
    im = Image.open(G("pokemon", folder, "footprint.png")).convert("L")
    px = im.load()
    return [[px[x, y] < 128 for x in range(16)] for y in range(16)]


# ------------------------------------------------------------------ sprites
def silhouette(spr, rgb=(40, 40, 64)):
    """Unseen species: every opaque pixel -> one colour (one OBJ palette, all 15 slots = INK)."""
    out = spr.copy()
    px = out.load()
    for y in range(out.size[1]):
        for x in range(out.size[0]):
            if px[x, y][3]:
                px[x, y] = rgb + (255,)
    return out


def sprite_bottom(spr):
    """Lowest opaque row (ROM would use frontPicYOffset for the same thing)."""
    bb = spr.getbbox()
    return bb[3] if bb else spr.size[1]


# ------------------------------------------------------------------ primitives
# Vanilla caught_ball.png (8x16, only rows 5..12 used) uses indices 15 outline,
# 11 top, 1 bottom; remapped to kit roles so it sits in any kit text window.
_BALL_MAP = {15: INK, 11: SPARE_A, 1: WHITE}


def caught_ball(cv, x, y):
    """Blit the 8x8 caught marker with its top-left at (x, y)."""
    im = Image.open(G("pokedex", "caught_ball.png"))
    px = im.load()
    for yy in range(5, 13):
        for xx in range(8):
            v = px[xx, yy]
            if v in _BALL_MAP:
                cv.set(x + xx, y + yy - 5, _BALL_MAP[v])


def dais(cv, cx, cy, r_out, r_in, sockets=()):
    """
    Big round BW-style dais window: ink rim, accent band, recessed ink lip, pale
    3-step face, and an oval stage the Pokémon stands on (lower third of the face).
    """
    disc(cv, cx, cy, r_out, ACCENT_DARK, INK)
    ring(cv, cx, cy, r_out - 1, ACCENT, 1.0)
    # top-left specular arc on the band (Gen 3 bevel direction)
    import math
    for y in range(int(cy - r_out), int(cy + 1)):
        for x in range(int(cx - r_out), int(cx + 1)):
            d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
            a = math.degrees(math.atan2(y + 0.5 - cy, x + 0.5 - cx))
            if r_out - 2 < d <= r_out - 1 and -160 <= a <= -110:
                cv.set(x, y, ACCENT_LIGHT)
    ring(cv, cx, cy, r_in + 2, ACCENT, 1.0)
    disc(cv, cx, cy, r_in + 1, INK, None)
    disc(cv, cx, cy, r_in, ACCENT_LIGHT, None)
    disc(cv, cx - 1, cy - 1, r_in - 2, ACCENT_PALE, None)
    disc(cv, cx - 2, cy - 3, r_in - 9, WHITE, None)
    # stage: flat oval, ink rim, accent face, light top lip, shade below
    sy = cy + r_in * 0.55
    rx, ry = r_in * 0.72, r_in * 0.2
    for y in range(int(sy - ry - 2), int(sy + ry + 3)):
        for x in range(int(cx - rx - 2), int(cx + rx + 3)):
            dx, dy = (x + 0.5 - cx) / rx, (y + 0.5 - sy) / ry
            dx2, dy2 = (x + 0.5 - cx) / (rx + 1), (y + 0.5 - sy) / (ry + 1)
            if dx * dx + dy * dy <= 1:
                cv.set(x, y, ACCENT if y >= sy - ry * 0.2 else ACCENT_LIGHT)
            elif dx2 * dx2 + dy2 * dy2 <= 1:
                cv.set(x, y, INK if y >= sy else ACCENT)
    for bx, by in sockets:
        disc(cv, bx, by, 10.5, ACCENT_DARK, INK)
    return int(sy)


def label_pill(cv, x, y, w, cap_w, h=14):
    """Pill with an accent label cap on the left (SEEN / OWN / HT / WT) and a panel value area."""
    rounded_box(cv, x, y, w, h, 4, PANEL, INK, WHITE, PANEL_SHADE)
    # accent cap, clipped to the pill's rounded left end
    for yy in range(1, h - 1):
        for xx in range(1, cap_w):
            if cv.get(x + xx, y + yy) in (PANEL, WHITE, PANEL_SHADE):
                c = ACCENT
                if yy == 1 or cv.get(x + xx - 1, y + yy) == INK:
                    c = ACCENT_LIGHT
                elif yy == h - 2:
                    c = ACCENT_DARK
                cv.set(x + xx, y + yy, c)
    cv.vline(x + cap_w, y + 1, y + h - 2, INK)


def tab_pill(cv, x, y, w, h=14):
    """Header tab = small panel pill (selected tab gets the gold palette swap)."""
    rounded_box(cv, x, y, w, h, 4, PANEL, INK, WHITE, PANEL_SHADE)


def well(cv, x, y, w, h, r=3):
    """Recessed panel well (footprint, icon slots): ink rim, dark top-left inner shadow."""
    rounded_box(cv, x, y, w, h, r, PANEL, INK, PANEL_SHADE, WHITE)


def tray(cv, y0, y1=159, x0=0, x1=239, seam=True):
    """Bottom description tray (bag style): ink top line, light lip, stitched seam at y0+3."""
    cv.rect(x0, y0, x1, y1, PANEL)
    cv.hline(x0, x1, y0, INK)
    cv.hline(x0, x1, y0 + 1, WHITE)
    cv.hline(x0, x1, y1, PANEL_SHADE)
    if seam:
        for x in range(x0 + 2, x1 - 1):
            if x % 4 < 2:
                cv.set(x, y0 + 3, PANEL_SHADE)


def header_band(cv, x0, x1, y0=0, y1=15, round_left=True, round_right=False):
    band(cv, x0, y0, x1, y1 - 1, ACCENT, ACCENT_LIGHT, ACCENT_DARK)
    cv.hline(x0, x1, y1, INK)
    if round_left:
        cv.vline(x0, y0, y1, INK)
        cv.set(x0, y1, 0)
        cv.set(x0 + 1, y1, INK)
        cv.set(x0, y1 - 1, INK)
    if round_right:
        cv.vline(x1, y0, y1, INK)
        cv.set(x1, y1, 0)
        cv.set(x1 - 1, y1, INK)
        cv.set(x1, y1 - 1, INK)


def chevron(out, cx, cy, right=False):
    """6x9 Gen 3 red chevron OBJ centred on (cx, cy)."""
    px = out.load()
    for r, row in enumerate(SMALL_ARROW):
        row = row[::-1] if right else row
        for c, ch in enumerate(row):
            if ch in "OF":
                px[cx - 3 + c, cy - 4 + r] = (ARROW_RED[0] if ch == "F" else ARROW_RED[1]) + (255,)


def thumb(out, x, y, theme="orchid", h=12):
    im = new_sheet(4, h, theme)
    rounded_box(Canvas(im), 0, 0, 4, h, 1, SELECT, INK, SELECT_LIGHT, SELECT_DARK)
    out.alpha_composite(KX.sheet_rgba(im), (x, y))


def track(cv, x0, y0, x1, y1):
    rounded_box(cv, x0, y0, x1 - x0 + 1, y1 - y0 + 1, 2, PANEL_DARK, INK, PANEL_SHADE, PANEL_DARK)
    cv.hline(x0 + 2, x1 - 2, y0 + 1, INK_SOFT)


def mon_pic(folder):
    """Front pic; kit_ext.mon_front now handles front.png-only species itself."""
    return KX.mon_front(folder)


# ------------------------------------------------------------------ CRY / SIZE pages (round 3)
import math as _math

# Scope palette (BG palette 8 on the CRY page, like vanilla's cry_screen_bg.pal): 1 = scope face,
# 2 = graticule dot, 8..15 = trace ramp (8 at the centre line, 15 at the peaks) as vanilla's
# sWaveformColor expects; orchid at the centre warming to gold at the peaks.
SCOPE_FACE = (24, 24, 40)
SCOPE_DOT = (56, 56, 88)


def scope_palette():
    ramp_from, ramp_to = (200, 152, 224), (248, 240, 168)    # ACCENT_LIGHT -> SELECT_LIGHT
    pal = [(0, 0, 0), SCOPE_FACE, SCOPE_DOT] + [(0, 0, 0)] * 5
    for k in range(8):
        t = k / 7
        mid = (248, 208, 88)                                 # SELECT halfway
        if t < 0.5:
            c = tuple(int(a + (b - a) * t * 2) for a, b in zip(ramp_from, mid))
        else:
            c = tuple(int(a + (b - a) * (t - 0.5) * 2) for a, b in zip(mid, ramp_to))
        pal.append(snap(c))
    return pal


def scope_tile():
    """8x8 scope background tile (vanilla cry_screen_bg.png slot): face + one graticule dot."""
    im = Image.new("P", (8, 8), 1)
    flat = [c for rgb in scope_palette() for c in rgb]
    im.putpalette(flat + [0] * (768 - len(flat)))
    im.putpixel((0, 0), 2)
    return im


def scope_well(cv, x, y, w, h):
    """Recessed scope well with a gold ("brass") trim; its inside stays index 0 so BG0's
    scrolling waveform window shows through."""
    rounded_box(cv, x, y, w, h, 4, TRANSPARENT, INK, SELECT_DARK, SELECT_LIGHT)
    for yy in range(y + 2, y + h - 2):
        cv.set(x + 2, yy, INK)
        cv.set(x + w - 3, yy, INK)
    for xx in range(x + 2, x + w - 2):
        cv.set(xx, y + 2, INK)
        cv.set(xx, y + h - 3, INK)
    return (x + 3, y + 3, x + w - 4, y + h - 4)      # transparent hole (inclusive)


NEEDLE_REST, NEEDLE_MAX = 32, -32                   # vanilla MIN/MAX_NEEDLE_POS (256 = full turn)


def dial(cv, cx, cy, r):
    """VU dial in the dais language: half disc with accent band, pale face, ink ticks over the
    needle's +-45 deg sweep (the last stretch in ball red), hub at the pivot (cx, cy)."""
    for y in range(int(cy - r - 1), int(cy) + 1):
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            d = _math.hypot(x + 0.5 - cx, y + 0.5 - cy)
            if d <= r + 1:
                c = INK
                if d <= r:
                    c = ACCENT_DARK
                if d <= r - 1:
                    c = ACCENT
                if d <= r - 3:
                    c = INK
                if d <= r - 4:
                    c = ACCENT_PALE if d > r - 9 else WHITE
                cv.set(x, y, c)
    # base line under the half disc
    cv.hline(int(cx - r - 1), int(cx + r + 1), int(cy) + 1, INK)
    cv.hline(int(cx - r), int(cx + r), int(cy), ACCENT_DARK)
    # ticks: -45..+45 deg from vertical, every 15 deg; red from +25 deg
    for k in range(-3, 4):
        a = _math.radians(k * 15)
        major = k % 3 == 0
        r0 = r - 12 if major else r - 9
        for t in range(int((r - 6 - r0) * 3)):
            rr = r0 + t / 3
            x = int(round(cx + rr * _math.sin(a) - 0.5))
            y = int(round(cy - rr * _math.cos(a) - 0.5))
            cv.set(x, y, SPARE_A if k * 15 >= 25 else INK)
    for deg in range(25, 46):
        a = _math.radians(deg)
        for rr in (r - 6, r - 5.5):
            cv.set(int(round(cx + rr * _math.sin(a) - 0.5)), int(round(cy - rr * _math.cos(a) - 0.5)), SPARE_A)
    disc(cv, cx, cy - 0.5, 3.5, ACCENT_DARK, INK)


def needle_image(length=30):
    """64x64 affine needle OBJ (vanilla geometry: base 24px below the centre, pointing up)."""
    im = Image.new("P", (64, 64), 0)
    cv = Canvas(im)
    base, tip = 32 + 24, 32 + 24 - length
    for y in range(tip, base + 1):
        cv.set(31, y, INK)
        cv.set(32, y, SELECT if y > tip + 1 else INK)
        cv.set(33, y, INK)
    cv.set(32, tip, INK)
    return im


def affine_obj(src_rgba, cx, cy, pa, pb, pc, pd, out, size=64):
    """GBA affine OBJ (not double-size): every screen pixel of the size x size box centred on
    (cx, cy) samples the texture at centre + M * (dx, dy) >> 8."""
    sp = src_rgba.load()
    op = out.load()
    h = size // 2
    for dy in range(-h, h):
        for dx in range(-h, h):
            tx = h + ((pa * dx + pb * dy) >> 8)
            ty = h + ((pc * dx + pd * dy) >> 8)
            if 0 <= tx < size and 0 <= ty < size:
                p = sp[tx, ty]
                if p[3]:
                    X, Y = cx + dx, cy + dy
                    if 0 <= X < out.size[0] and 0 <= Y < out.size[1]:
                        op[X, Y] = p


def needle_matrix(rot):
    """ObjAffineSet(scale 256, rotation rot * 256) as the cry screen does."""
    th = (rot & 0xFF) / 256 * 2 * _math.pi
    c, s = int(256 * _math.cos(th)), int(256 * _math.sin(th))
    return c, -s, s, c


def needle_offset(rot):
    sine = lambda i: int(256 * _math.sin(2 * _math.pi * (i & 0xFF) / 256))
    i = (rot + 0x7F) & 0xFF
    return sine(i) * 24 // 256, sine(i + 64) * 24 // 256


def size_panel(cv, x0, y0, x1, y1, floor_y):
    """SIZE stage: recessed panel, floor band under floor_y, height ticks every 8px on the left
    (longer every 32px) measured up from the floor."""
    well(cv, x0, y0, x1 - x0 + 1, y1 - y0 + 1, r=4)
    cv.rect(x0 + 2, floor_y + 1, x1 - 2, y1 - 2, PANEL_SHADE)
    cv.hline(x0 + 2, x1 - 2, floor_y, INK)
    cv.hline(x0 + 2, x1 - 2, floor_y + 1, PANEL_DARK)
    y, k = floor_y - 8, 1
    while y > y0 + 3:
        n = 6 if k % 4 == 0 else 3
        cv.hline(x0 + 2, x0 + 1 + n, y, INK_SOFT)
        cv.hline(x1 - 1 - n, x1 - 2, y, INK_SOFT)
        y -= 8
        k += 1


def species_size(name):
    """pokemonScale / pokemonOffset / trainerScale / trainerOffset of SPECIES_<name>."""
    b = _species_blocks()[name]
    g = lambda f: int(re.search(r"\.%s\s*=\s*(-?\d+)" % f, b).group(1))
    return g("pokemonScale"), g("pokemonOffset"), g("trainerScale"), g("trainerOffset")
