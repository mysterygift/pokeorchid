"""
Export the Rotom Phone QUESTS app (mock_quests.py, approved 2026-11-17) to game assets.

Static BG2 art is cut from the mock's own drawing code. Row pills, the gold selection, stars, text,
the scroll thumb and the steps progress fill are drawn into windows at runtime
(src/rotom_phone_quests.c) so unused rows show the backdrop; state tags, the selected filter tab and
the quest sprite are OBJs.

Writes graphics/rotom_phone/:
  quests_bg.png        tiles (+ 4 grid tiles at the end)
  quests_list.bin      header, filter tabs (unselected) + L/R, scroll track, tray with icon well
  quests_steps.bin     header, B, progress trough, scroll track, tray
  quests_bg.pal        pal 0 kit orchid (SPARE_A = star yellow), pal 1 kit leaf (progress fill), pal 2 grid
  quests_tab.png       OBJ 32x16 x 5: the gold selected tab with its pictogram (all/new/active/reward/done)
  quests_tags_a.png    OBJ 32x16 x 3: new / active / reward tags   (+ .pal)
  quests_tags_b.png    OBJ 32x16 x 2: done / locked tags           (+ .pal)
  quests_glyphs.png    window blit sources (kit orchid indices): pin cap 17x14 @0, keypad A @24, star 9x9 @32
src/data/rotom_phone_quests_layout.h
usage: export_quests.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from PIL import Image
import kit
from kit import *
import dex_ext as D
import system_ext as X
from backdrop import GRID_PAL, grid_tile_image
import mock_quests as MQ

ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
P = lambda *p: os.path.join(ROOT, *p)
OUT = P("graphics", "rotom_phone")
W, H = 240, 160
PAL = kit.palette("orchid")
PAL[SPARE_A] = snap((248, 192, 48))          # star yellow (mock_quests STAR 'y')
LEAF = kit.palette("leaf")
LEAF[SPARE_A] = PAL[SPARE_A]


def pad16(p):
    return [snap(c) for c in p] + [(0, 0, 0)] * (16 - len(p))


def save(im, path, pal):
    flat = [c for rgb in pad16(pal) for c in rgb]
    out = im.copy()
    out.putpalette(flat + [0] * (768 - len(flat)))
    out.save(path, transparency=0)


def header(cv):
    D.header_band(cv, 0, 239, round_left=False)
    rounded_box(cv, 4, 2, 14, 12, 3, ACCENT_LIGHT, INK, WHITE, ACCENT)
    X.centred_sil(cv, 5, 3, 13, 10, "quest", ACCENT_DARK, None)


def tray(cv):
    y = MQ.TRAY_Y
    D.tray(cv, y)
    disc(cv, 20, 137, 16, PANEL_SHADE, None)
    disc(cv, 20, 137, 15, WHITE, INK)
    disc(cv, 20.5, 137.5, 13, PANEL, None)
    ring(cv, 20, 137, 14, PANEL_SHADE)
    cv.vline(40, y + 6, H - 6, PANEL_SHADE)
    cv.vline(41, y + 6, H - 6, WHITE)


def track(cv):
    D.track(cv, 230, MQ.ROW_Y, 236, MQ.ROW_Y + MQ.ROWS * MQ.ROW_H - 3)


def list_art():
    im = kit.new_sheet(W, H, "orchid")
    cv = Canvas(im)
    header(cv)
    X.keypad(cv, 4, 22, "L")
    for i, (key, _) in enumerate(MQ.FILTERS):
        x = 22 + i * 26
        rounded_box(cv, x, 18, 24, 14, 4, PANEL, INK, WHITE, PANEL_SHADE)
        X.centred_sil(cv, x + 1, 19, 22, 12, key, INK_SOFT, None)
    X.keypad(cv, 154, 22, "R")
    track(cv)
    tray(cv)
    return im


def steps_art():
    im = kit.new_sheet(W, H, "orchid")
    cv = Canvas(im)
    header(cv)
    X.keypad(cv, 4, 22, "B")
    rounded_box(cv, 52, 19, 184, 12, 3, PANEL_DARK, INK, PANEL_SHADE, PANEL_DARK)
    track(cv)
    tray(cv)
    return im


def export_bg():
    tiles, tms = None, {}
    for name, im in (("quests_list", list_art()), ("quests_steps", steps_art())):
        tiles, tm = to_tiles(im, base=tiles)
        tms[name] = (tm, im)
    n = len(tiles)
    g = grid_tile_image().load()
    for ty in range(2):
        for tx in range(2):
            tiles.append(tuple(g[tx * 8 + x, ty * 8 + y] for y in range(8) for x in range(8)))
    assert len(tiles) <= 512
    save(tiles_to_image(tiles, tms["quests_list"][1]), os.path.join(OUT, "quests_bg.png"), PAL)
    for name, (tm, _) in tms.items():
        cells = [None] * (32 * 32)
        for i, item in enumerate(tm):
            cy, cx = divmod(i, 30)
            if item[0]:
                cells[cy * 32 + cx] = item
        write_tilemap(os.path.join(OUT, name + ".bin"), cells)
    write_jasc(os.path.join(OUT, "quests_bg.pal"), pad16(PAL) + pad16(LEAF) + pad16(GRID_PAL))
    return n


def export_obj():
    im = kit.new_sheet(32, 16 * 5, "orchid")
    cv = Canvas(im)
    for i, (key, _) in enumerate(MQ.FILTERS):
        rounded_box(cv, 0, i * 16, 24, 14, 4, SELECT, INK, SELECT_LIGHT, SELECT_DARK)
        X.centred_sil(cv, 1, i * 16 + 1, 22, 12, key, INK, SELECT_DARK)
    save(im, os.path.join(OUT, "quests_tab.png"), PAL)
    for name, states in (("quests_tags_a", ("new", "active", "reward")), ("quests_tags_b", ("done", "locked"))):
        pal = [(0, 0, 0), (40, 40, 64), (248, 248, 248)]
        for st in states:
            pal += list(MQ.TAGS[st])
        im = Image.new("P", (32, 16 * len(states)), 0)
        cv = Canvas(im)
        for k, st in enumerate(states):
            dk, fc, lt = 3 + k * 3, 4 + k * 3, 5 + k * 3
            rounded_box(cv, 0, k * 16, 18, 12, 3, fc, 1, lt, dk)
            X.centred_sil(cv, 1, k * 16 + 1, 16, 10, st, 2, dk)
        save(im, os.path.join(OUT, name + ".png"), pal)
        write_jasc(os.path.join(OUT, name + ".pal"), pad16(pal))
    im = kit.new_sheet(48, 16, "orchid")
    cv = Canvas(im)
    X.label_pill(cv, 0, 0, 40, "pin")
    for x in range(17, 48):
        for y in range(16):
            cv.set(x, y, 0)
    X.keypad(cv, 24, 0, "A")
    stamp(cv, 32, 0, MQ.STAR, {"k": INK, "y": SPARE_A, "w": SELECT_LIGHT})
    save(im, os.path.join(OUT, "quests_glyphs.png"), PAL)


def main():
    os.makedirs(OUT, exist_ok=True)
    n = export_bg()
    export_obj()
    with open(P("src", "data", "rotom_phone_quests_layout.h"), "w") as f:
        f.write("// Generated by dev_scripts/orchid_ui/export_quests.py - do not edit.\n")
        f.write("#define QUESTS_BG_TILES %d   // grid tiles (2x2) follow\n" % n)
    print("quest tiles", n)


if __name__ == "__main__":
    main()
