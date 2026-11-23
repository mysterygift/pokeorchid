"""
Export the Rotom Phone home screen (mock_phone.py, approved 2026-11-17) to game assets.

Writes (under the repo root):
  graphics/rotom_phone/shell.png      BG2 tiles: coral shell, screen, glare, eye notch, status bar art,
                                      speech strip. 4bpp, palette below. Grid tiles appended (BG3).
  graphics/rotom_phone/shell.bin      BG2 tilemap 32x32 (grid tiles are not in it)
  graphics/rotom_phone/shell_off.bin  BG2 tilemap for the offline phone (X-eyed Rotom, empty signal)
  graphics/rotom_phone/shell.pal      48 colours: pal 0 shell (eye dark), pal 1 shell (eye glowing),
                                      pal 2 grid
  graphics/rotom_phone/apps.png       OBJ 32x32 x 5 frames: MAP, CALL, QUESTS, RADIO, locked "?"
  graphics/rotom_phone/apps.pal       pal 0 = app colours, pal 1 = dimmed (locked frame uses MAP indices)
  graphics/rotom_phone/pill.png       OBJ 64x64: the gold selection pill (40x48 at 0,0)
  graphics/rotom_phone/badge.png      OBJ 16x16 x 9 frames: red quest badge with 1..9
  graphics/rotom_phone/ui.pal         OBJ palette for pill + badge
  graphics/rotom_phone/text.pal       BG text palette (white, shadow, grey label, deep, ink, gold)
  src/data/rotom_phone_layout.h       generated constants (tile/pill/label positions)

usage: export_phone.py
"""
import os
import sys

KIT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KIT)
from PIL import Image
import kit
from kit import Canvas, rounded_box, disc, to_tiles, tiles_to_image, write_tilemap, write_jasc, snap
from backdrop import GRID_PAL, grid_tile_image
from gamefont import draw_text
import mock_phone as M

ROOT = os.path.abspath(os.path.join(KIT, "..", ".."))
P = lambda *p: os.path.join(ROOT, *p)
OUT = P("graphics", "rotom_phone")
W, H = 240, 160

EYE_DARK = (64, 72, 96)
EYE_GLOW = (120, 200, 248)
SHADOW = (88, 88, 104)

# ---------------------------------------------------------------- shell (BG2)
SHELL_PAL = [(0, 0, 0), M.INK, M.R_LIGHT, M.R_FACE, M.R_SHADE, M.R_DARK, M.SCR, M.SCR_GLARE, M.SCR_DEEP,
             M.WHITE, (224, 72, 56), EYE_DARK, EYE_DARK, M.PIP_EMPTY]
S_INK, S_RL, S_RF, S_RS, S_RD, S_SCR, S_GLARE, S_DEEP, S_WHITE, S_RED, S_PUPIL, S_HILITE, S_PIP_EMPTY = range(1, 14)


def pad16(p):
    return [snap(c) for c in p] + [(0, 0, 0)] * (16 - len(p))


def build_shell(offline=False):
    im = Image.new("P", (W, H), 0)
    cv = Canvas(im)
    m = M.silhouette_mask().load()
    inside = lambda x, y: 0 <= x < W and 0 <= y < H and m[x, y]
    for y in range(H):
        for x in range(W):
            if not inside(x, y):
                continue
            if not all(inside(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                cv.set(x, y, S_INK)
            elif not inside(x - 1, y - 1) or not inside(x, y - 2):
                cv.set(x, y, S_RL)
            elif not inside(x + 1, y + 1) or not inside(x, y + 2):
                cv.set(x, y, S_RS)
            else:
                cv.set(x, y, S_RF)
    rounded_box(cv, 28, 30, 184, 102, 4, S_RS, S_RD, S_RS, S_RL)
    rounded_box(cv, 30, 32, 180, 98, 3, S_SCR, S_DEEP, S_SCR, S_SCR, bevel=False)
    for y in range(33, 129):
        for x in range(31, 209):
            if 150 < x + (y - 33) * 0.6 < 196 and cv.get(x, y) == S_SCR:
                cv.set(x, y, S_GLARE)
    disc(cv, 30, 80.5, 6, S_RF, S_INK)
    disc(cv, 30, 80.5, 3.5, S_DEEP, S_RD)
    disc(cv, 30, 80.5, 1.5, S_PUPIL, None)
    cv.set(29, 79, S_HILITE)
    # status bar: newspaper pictogram, signal pips, divider (clock + ticker text are BG0/BG1)
    if not offline:
        kit.stamp(cv, 38, 34, M.NEWS_ICON, {"#": S_WHITE, "=": S_RED, ".": S_DEEP})
    for k in range(3):
        cv.rect(154 + k * 3, 41 - 2 * k, 155 + k * 3, 42, S_PIP_EMPTY if offline else S_WHITE)
    cv.hline(36, 203, 45, S_DEEP)
    if offline:                       # mock_phone.draw_phone_offline: X-eyed Rotom, no speech strip
        for ex in (90, 134):
            kit.stamp(cv, ex + 1, 63, M.X_EYE, {"#": S_DEEP})
            kit.stamp(cv, ex, 62, M.X_EYE, {"#": S_WHITE})
        kit.stamp(cv, 109, 93, M.MOUTH, {"#": S_DEEP})
        kit.stamp(cv, 108, 92, M.MOUTH, {"#": S_WHITE})
        return im
    # Rotom speech strip
    rounded_box(cv, 35, 100, 170, 28, 3, S_DEEP, S_DEEP, S_DEEP, S_DEEP, bevel=False)
    return im


def export_shell():
    im = build_shell()
    flat = [c for rgb in pad16(SHELL_PAL) for c in rgb]
    im.putpalette(flat + [0] * (768 - len(flat)))
    tiles, tm = to_tiles(im)
    off = build_shell(offline=True)
    off.putpalette(im.getpalette())
    tiles, tm_off = to_tiles(off, base=tiles)
    n_shell = len(tiles)
    g = grid_tile_image().load()
    for ty in range(2):
        for tx in range(2):
            tiles.append(tuple(g[tx * 8 + x, ty * 8 + y] for y in range(8) for x in range(8)))
    assert len(tiles) <= 512, len(tiles)
    kit_sheet = tiles_to_image(tiles, im)
    save(kit_sheet, os.path.join(OUT, "shell.png"), pad16(SHELL_PAL))
    cells = [None] * (32 * 32)
    for i, item in enumerate(tm):
        cells[(i // 30) * 32 + i % 30] = item
    write_tilemap(os.path.join(OUT, "shell.bin"), cells)
    cells = [None] * (32 * 32)
    for i, item in enumerate(tm_off):
        cells[(i // 30) * 32 + i % 30] = item
    write_tilemap(os.path.join(OUT, "shell_off.bin"), cells)
    glow = list(SHELL_PAL)
    glow[S_PUPIL], glow[S_HILITE] = EYE_GLOW, M.WHITE
    write_jasc(os.path.join(OUT, "shell.pal"), pad16(SHELL_PAL) + pad16(glow) + pad16(GRID_PAL))
    return n_shell


# ---------------------------------------------------------------- app tiles (OBJ)
APP_PAL = [(0, 0, 0), M.INK, M.WHITE, (224, 72, 56)]
for _name, ramp, _ in M.APPS:
    APP_PAL += list(ramp)                      # dark, face, light per app
LOCKED = [(72, 72, 88), (112, 112, 128), (152, 152, 168)]
LOCKED_WHITE = (184, 184, 200)

QMARK = [
    "................",
    "................",
    ".....######.....",
    "....########....",
    "...###....###...",
    "...##......##...",
    "...........##...",
    "..........###...",
    "........####....",
    ".......###......",
    ".......##.......",
    ".......##.......",
    "................",
    ".......##.......",
    ".......##.......",
    "................",
]


def draw_tile(cv, ox, oy, rows, app_index):
    dk, fc, lt = 4 + app_index * 3, 5 + app_index * 3, 6 + app_index * 3
    rounded_box(cv, ox, oy, 29, 29, 4, fc, 1, lt, dk)
    for yy, row in enumerate(rows):
        for xx, ch in enumerate(row):
            px, py = ox + 7 + xx, oy + 7 + yy
            if ch == "#":
                nxt = rows[yy + 1 if yy + 1 < 16 else yy][min(xx + 1, 15)]
                if nxt not in "#":
                    cv.set(px + 1, py + 1, dk)
                cv.set(px, py, 2)
            elif ch == "=":
                cv.set(px, py, lt)
            elif ch == "r":
                cv.set(px, py, 3)
            elif ch == "w":
                cv.set(px, py, 2)


def export_apps():
    names = [a[0] for a in M.APPS]
    im = Image.new("P", (32, 32 * 5), 0)
    cv = Canvas(im)
    for i, n in enumerate(names):
        draw_tile(cv, 0, i * 32, M.ICONS[n], i)
    draw_tile(cv, 0, 4 * 32, QMARK, 0)          # locked: MAP indices, dimmed palette
    save(im, os.path.join(OUT, "apps.png"), pad16(APP_PAL))
    dim = list(APP_PAL)
    dim[2] = LOCKED_WHITE
    dim[4:7] = LOCKED
    write_jasc(os.path.join(OUT, "apps.pal"), pad16(APP_PAL) + pad16(dim))


# ---------------------------------------------------------------- pill + badge (OBJ)
UI_PAL = [(0, 0, 0), M.INK, M.GOLD[0], M.GOLD[1], M.GOLD[2], (224, 72, 56), M.WHITE]


def export_ui():
    im = Image.new("P", (64, 64), 0)
    rounded_box(Canvas(im), 0, 0, 40, 48, 4, 3, 1, 4, 2)
    save(im, os.path.join(OUT, "pill.png"), pad16(UI_PAL))
    b = Image.new("P", (16, 16 * 9), 0)
    cv = Canvas(b)
    for k in range(9):
        # mock: disc(tx+27, ty+2, 4) and the digit at (tx+25, ty-6); sprite origin = (tx+20, ty-6)
        disc(cv, 7, k * 16 + 8, 4, 5, 1)
        draw_text(cv, 5, k * 16, str(k + 1), 6, None, font="small")
    save(b, os.path.join(OUT, "badge.png"), pad16(UI_PAL))
    write_jasc(os.path.join(OUT, "ui.pal"), pad16(UI_PAL))


TEXT_PAL = [(0, 0, 0), M.WHITE, SHADOW, M.GREY_TXT, M.SCR_DEEP, M.INK, M.GOLD[0], M.GOLD[1]]


def save(im, path, pal):
    flat = [c for rgb in pal for c in rgb]
    out = im.copy()
    out.putpalette(flat + [0] * (768 - len(flat)))
    out.save(path, transparency=0)


# Field match-call window: the PokéNav's spinning icon becomes a buzzing Rotom Phone (start-menu PHONE icon,
# shaking with buzz arcs). 32x32 x 8 frames on the call window's white (index 8, as the vanilla icon; matches the
# Orchid message box WHITE, since the call box is the field message box).
RING_PAL = [(255, 255, 255), M.INK, (248, 144, 56), (224, 88, 56), (176, 72, 56), (96, 96, 120), (160, 160, 184),
            (112, 112, 136), (255, 255, 255)]
RING_CMAP = {"k": 1, "o": 2, "r": 3, "R": 4, "d": 5, "m": 6}
BUZZ = [".#.", "#..", "#..", "#..", ".#."]


def export_ring_icon():
    im = Image.new("P", (32, 256), 8)
    cv = Canvas(im)
    shake = [0, -1, 1, -1, 1, 0, 0, 0]
    for f in range(8):
        dx = shake[f]
        kit.stamp(cv, 8 + dx, f * 32 + 8, M.PHONE_ICON, RING_CMAP)
        if 1 <= f <= 4:
            kit.stamp(cv, 4 + dx, f * 32 + 12, BUZZ, {"#": 7})
            kit.stamp(cv, 25 + dx, f * 32 + 12, BUZZ, {"#": 7}, hflip=True)
    # 16-entry PLTE: match_call.c loads sizeof(sPokenavIcon_Pal) into BG palette 15, so a 256-colour PNG would
    # spill 240 colours into the sprite palettes (every overworld sprite went black during calls).
    flat = [c for rgb in pad16(RING_PAL) for c in rgb]
    im.putpalette(flat)
    im.save(P("graphics", "pokenav", "match_call", "nav_icon.png"), transparency=0, bits=4)


def main():
    os.makedirs(OUT, exist_ok=True)
    export_ring_icon()
    n_shell = export_shell()
    export_apps()
    export_ui()
    write_jasc(os.path.join(OUT, "text.pal"), pad16(TEXT_PAL))
    with open(P("src", "data", "rotom_phone_layout.h"), "w") as f:
        f.write("// Generated by dev_scripts/orchid_ui/export_phone.py - do not edit.\n")
        f.write("#define PHONE_SHELL_TILES %d    // grid tiles (2x2) follow\n" % n_shell)
        f.write("#define PHONE_APP_X(i)    (38 + (i) * 42)   // slot column; tile at +5, pill at -1\n")
        f.write("#define PHONE_APP_TILE_Y  52\n#define PHONE_PILL_Y      49\n#define PHONE_LABEL_Y     81\n")
        f.write("#define PHONE_TICK_L      %d\n#define PHONE_TICK_R      %d\n" % (M.TICK_L, M.TICK_R))
    print("shell tiles:", n_shell)


if __name__ == "__main__":
    main()
