"""
Shared helpers for the voyage region-map mocks (batch 6). Mock only: nothing under graphics/ src/ data/
include/ is written.

- bg2(png, bin)          ROM region-map BG2 (affine 8bpp tiles, 64x64 u8 tilemap) -> 240x160 RGB
- vanilla_hoenn()        the original Emerald Hoenn art, read from git (fead488d62^ = before the Tosa map)
- screen(...)            Orchid MAP v2 screen: BG2 terrain + kit header/tray (as mock_map.frame) + OBJ
                         nodes / cursor ring / player head, all from the ROM sheets
Grid: cursor cell (x, y) of the 28x15 grid = 8x8 px at (8 + 8x, 16 + 8y)  (MAPCURSOR_X_MIN 1, _Y_MIN 2).
"""
import io
import os
import re
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
KIT = os.path.join(ROOT, "dev_scripts", "orchid_ui")
sys.path.insert(0, KIT)
from PIL import Image  # noqa: E402
import kit  # noqa: E402
from kit import (Canvas, rounded_box, INK, WHITE, ACCENT, ACCENT_LIGHT, ACCENT_DARK, PANEL_SHADE,  # noqa: E402
                 INK_SOFT)
import kit_ext as K  # noqa: E402
import system_ext as X  # noqa: E402
import dex_ext as D  # noqa: E402
from gamefont import draw_text, text_width  # noqa: E402

W, H = 240, 160
GX, GY = 8, 16
RM = os.path.join(ROOT, "graphics", "pokenav", "region_map")
OUT = os.path.join(ROOT, "dev_scripts", "voyages", "out", "batch6_regionmap")
HOENN_REV = "fead488d62^"           # last commit with the vanilla Emerald Hoenn region map art
kit.THEMES.setdefault("map", kit.THEMES["leaf"])
X.SIL.setdefault("map", ["XX.XX.XX"] * 6)


def git_bytes(rev, path):
    return subprocess.check_output(["git", "-C", ROOT, "show", "%s:%s" % (rev, path)])


def tiles_of(sheet):
    cols = sheet.width // 8
    return [sheet.crop(((i % cols) * 8, (i // cols) * 8, (i % cols) * 8 + 8, (i // cols) * 8 + 8))
            for i in range(cols * (sheet.height // 8))]


def bg2_from(sheet, tmap):
    """sheet = 'P' 8bpp tile sheet, tmap = 4096 bytes (64x64 u8) -> 'P' 240x160 (palette kept)."""
    tl = tiles_of(sheet)
    im = Image.new("P", (W, H))
    im.putpalette(sheet.getpalette())
    for i, v in enumerate(tmap):
        x, y = i % 64, i // 64
        if x * 8 < W and y * 8 < H:
            im.paste(tl[v], (x * 8, y * 8))
    return im


def bg2(png, binf):
    return bg2_from(Image.open(png), open(binf, "rb").read())


def vanilla_hoenn():
    """(sheet 'P', tilemap bytes, layout rows) of the original Emerald Hoenn region map."""
    sheet = Image.open(io.BytesIO(git_bytes(HOENN_REV, "graphics/pokenav/region_map/map.png")))
    tmap = git_bytes(HOENN_REV, "graphics/pokenav/region_map/map.bin")
    src = git_bytes(HOENN_REV, "src/data/region_map/region_map_layout.h").decode()
    rows = [re.findall(r"MAPSEC_\w+", r) for r in src.split("\n") if r.strip().startswith("{MAPSEC")]
    return sheet, tmap, rows


def layout_rows(path):
    src = open(path).read()
    return [re.findall(r"MAPSEC_\w+", r) for r in src.split("\n") if r.strip().startswith("{MAPSEC")]


def sections_of(rows):
    secs = {}
    for y, r in enumerate(rows):
        for x, s in enumerate(r):
            if s != "MAPSEC_NONE":
                secs.setdefault(s, []).append((x, y))
    return secs


def cell_px(cell):
    return GX + cell[0] * 8, GY + cell[1] * 8


def cell_ctr(cell):
    x, y = cell_px(cell)
    return x + 4, y + 4


# ------------------------------------------------------------------ ROM sprites
def _jasc(path):
    v = open(path).read().split()
    n = int(v[2])
    return [(int(v[3 + i * 3]), int(v[4 + i * 3]), int(v[5 + i * 3])) for i in range(n)]


def _gbapal(path):
    raw = open(path, "rb").read()
    out = []
    for i in range(len(raw) // 2):
        c = struct.unpack_from("<H", raw, i * 2)[0]
        out.append(((c & 31) << 3, ((c >> 5) & 31) << 3, ((c >> 10) & 31) << 3))
    return out


def sprite_frames(png, pal, fw=16, fh=16):
    im = K.sheet_rgba(Image.open(png), pal)
    return [im.crop((0, y, fw, y + fh)) for y in range(0, im.height, fh)]


CURSOR_PAL = _jasc(os.path.join(RM, "cursor.pal"))
RING = sprite_frames(os.path.join(RM, "cursor_small.png"), CURSOR_PAL)[0]
NODES = sprite_frames(os.path.join(RM, "orchid_nodes.png"), CURSOR_PAL)   # town, town grey, landmark, grey
HEAD = sprite_frames(os.path.join(RM, "brendan_icon.png"), _gbapal(os.path.join(RM, "brendan_icon.gbapal")))[0]


# ------------------------------------------------------------------ MAP v2 screen
def frame(out, title, place, chips=(), switch_hint=False):
    """Header band + region name, tray + place name: same drawing as mock_map.frame (approved MAP v2)."""
    def fn(cv):
        D.header_band(cv, 0, 239, round_left=False)
        rounded_box(cv, 4, 2, 14, 12, 3, ACCENT_LIGHT, INK, WHITE, ACCENT)
        X.centred_sil(cv, 5, 3, 13, 10, "map", ACCENT_DARK, None)
        draw_text(cv, 23, 0, title, WHITE, ACCENT_DARK)
        D.tray(cv, 136, seam=False)
        if place:
            draw_text(cv, 8, 138, place, INK, PANEL_SHADE)
    K.layer(out, fn, "map")
    if switch_hint:
        out.alpha_composite(K.sheet_rgba(Image.open(os.path.join(RM, "orchid_switch_hint.png"))), (W - 40, 4))


def screen(terrain, title, place, nodes=(), cursor=None, here=None, tubes=None):
    """terrain: RGB/P 240x160. nodes: [(cell, landmark, visited)]. cursor/here: cell or None.
    tubes: optional RGBA 240x160 layer (routes)."""
    out = terrain.convert("RGBA")
    if tubes is not None:
        out.alpha_composite(tubes)
    for cell, landmark, visited in nodes:
        x, y = cell_ctr(cell)
        out.alpha_composite(NODES[(2 if landmark else 0) + (0 if visited else 1)], (x - 8, y - 8))
    if cursor is not None:
        x, y = cell_ctr(cursor)
        out.alpha_composite(RING, (x - 8, y - 8))
    if here is not None:
        x, y = cell_ctr(here)
        out.alpha_composite(HEAD, (x - 8, y - 8 - 11))          # ORCHID_MAP_HEAD_RAISE
    frame(out, title, place)
    return out


def save(im, name):
    os.makedirs(OUT, exist_ok=True)
    rgb = im.convert("RGB")
    rgb.save(os.path.join(OUT, name + ".png"))
    K.upscale(rgb, 3).save(os.path.join(OUT, name + "@3x.png"))
    return os.path.join(OUT, name + ".png")
