"""
Export the Rotom Phone CALL app (mock_call.py, approved 2026-11-17) to game assets.

Static art (BG2, plus BG1 for the button chips) is cut from the mock's own drawing code with the
per-contact parts left out; names, locations, pills of variable width, heads, tags, portraits and the
ringing rings are drawn at runtime (src/rotom_phone_call.c).

Writes graphics/rotom_phone/:
  call_bg.png        tiles for every CALL screen (+ 4 grid tiles at the end)
  call_list.bin      contact list: header, 5 row pills, scrollbar track, tray
  call_card.bin      contact card: portrait well + dais, info panel, button pills
  call_card_strip.bin  the card with the red "wants a rematch" strip
  call_chips.bin     BG1 over the card buttons: phone chip on CALL, B disc on BACK
  call_ring.bin      ringing / talking: header + portrait discs
  call_bg.pal        pal 0 kit (male blue), pal 1 rematch-red accent (strip), pal 2 grid
  call_row_pill.png  OBJ 4 x 64x32: the gold row pill (218x16) cut in 64px columns
  call_btn_pill.png  OBJ 2 x 64x32: the gold button pill (108x22)
  call_tags.png      OBJ 32x16 x 2: rematch (Poke Ball), home
  call_tags.pal      OBJ palette for the tags
  call_glyphs.png    blit sources in kit colours: pin cap (17x14), keypad A at x 24, keypad B at x 32 (8x8)
src/data/rotom_phone_call_layout.h  tile count
usage: export_call.py
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
import mock_call as MC

ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
P = lambda *p: os.path.join(ROOT, *p)
OUT = P("graphics", "rotom_phone")
W, H = 240, 160
THEME = "male"
PAL = kit.palette(THEME)
REMATCH = MC.TAG["rematch"]


def pad16(p):
    return [snap(c) for c in p] + [(0, 0, 0)] * (16 - len(p))


def sheet():
    im = kit.new_sheet(W, H, THEME)
    return im, Canvas(im)


def header(cv):
    D.header_band(cv, 0, 239, round_left=False)
    rounded_box(cv, 4, 2, 14, 12, 3, ACCENT_LIGHT, INK, WHITE, ACCENT)
    X.centred_sil(cv, 5, 3, 13, 10, "phone", ACCENT_DARK, None)


def list_art():
    im, cv = sheet()
    header(cv)
    for r in range(MC.ROWS):
        rounded_box(cv, 8, MC.ROW_Y + r * MC.ROW_H, 218, 16, 4, PANEL, INK, WHITE, PANEL_SHADE)
    D.track(cv, 230, MC.ROW_Y, 236, MC.ROW_Y + MC.ROWS * MC.ROW_H - 3)
    D.tray(cv, 114)
    return im


def card_art(strip):
    im, cv = sheet()
    header(cv)
    rounded_box(cv, 6, 20, 76, 92, 4, PANEL, INK, WHITE, PANEL_SHADE)
    disc(cv, 44, 62, 33, PANEL_SHADE, INK)
    disc(cv, 44, 62, 31, ACCENT_PALE, None)
    disc(cv, 43, 61, 26, WHITE, None)
    ring(cv, 44, 62, 32, ACCENT_LIGHT)
    rounded_box(cv, 86, 20, 150, 92, 4, PANEL, INK, WHITE, PANEL_SHADE)
    cv.hline(92, 230, 55, PANEL_SHADE)
    cv.hline(92, 230, 56, WHITE)
    if strip:   # accent roles here use palette 1 (rematch reds), see the tilemap pass below
        rounded_box(cv, 92, 92, 138, 15, 4, ACCENT, INK, ACCENT_LIGHT, ACCENT_DARK)
    for i in range(2):
        rounded_box(cv, 8 + i * 116, 118, 108, 22, 4, PANEL, INK, WHITE, PANEL_SHADE)
    return im


def chips_art():
    im, cv = sheet()
    rounded_box(cv, 14, 122, 18, 14, 3, ACCENT, INK, ACCENT_LIGHT, ACCENT_DARK)
    X.centred_sil(cv, 15, 123, 17, 12, "phone", WHITE, ACCENT_DARK)
    X.b_disc(cv, 124 + 15, 129)
    return im


def ring_art():
    im, cv = sheet()
    header(cv)
    cx, cy = 120, 58
    disc(cv, cx, cy, 30, ACCENT, INK)
    disc(cv, cx, cy, 27, WHITE, INK)
    disc(cv, cx - 1, cy - 1, 25, ACCENT_PALE, None)
    return im


def save(im, path, pal):
    flat = [c for rgb in pal for c in rgb]
    out = im.copy()
    out.putpalette(flat + [0] * (768 - len(flat)))
    out.save(path, transparency=0)


def tilemap(tm, pal_of=None):
    cells = [None] * (32 * 32)
    for i, item in enumerate(tm):
        cy, cx = divmod(i, 30)
        if item[0] == 0:
            continue
        p = pal_of(cx, cy) if pal_of else 0
        cells[cy * 32 + cx] = item + (p,)
    return cells


def export_bg():
    tiles, tms = None, {}
    arts = [("call_list", list_art()), ("call_card", card_art(False)), ("call_card_strip", card_art(True)),
            ("call_chips", chips_art()), ("call_ring", ring_art())]
    for name, im in arts:
        tiles, tm = to_tiles(im, base=tiles)
        tms[name] = tm
    n_art = len(tiles)
    g = grid_tile_image().load()
    for ty in range(2):
        for tx in range(2):
            tiles.append(tuple(g[tx * 8 + x, ty * 8 + y] for y in range(8) for x in range(8)))
    assert len(tiles) <= 512, len(tiles)
    save(tiles_to_image(tiles, arts[0][1]), os.path.join(OUT, "call_bg.png"), PAL)
    # the rematch strip's tiles (rows 11-13, cols 11-28) use palette 1
    strip_pal = lambda cx, cy: 1 if (11 <= cy <= 13 and 11 <= cx <= 28) else 0
    for name, tm in tms.items():
        write_tilemap(os.path.join(OUT, name + ".bin"),
                      tilemap(tm, strip_pal if name == "call_card_strip" else None))
    red = list(PAL)
    red[ACCENT_DARK], red[ACCENT], red[ACCENT_LIGHT] = REMATCH
    write_jasc(os.path.join(OUT, "call_bg.pal"), pad16(PAL) + pad16(red) + pad16(GRID_PAL))
    return n_art


def export_obj():
    # gold row pill (218x16) and button pill (108x22), cut into 64x32 OBJ frames
    for name, (w, h) in (("call_row_pill", (218, 16)), ("call_btn_pill", (108, 22))):
        n = (w + 63) // 64
        full = kit.new_sheet(n * 64, 32, THEME)
        rounded_box(Canvas(full), 0, 0, w, h, 4, SELECT, INK, SELECT_LIGHT, SELECT_DARK)
        strip = kit.new_sheet(64, 32 * n, THEME)
        for k in range(n):
            strip.paste(full.crop((k * 64, 0, k * 64 + 64, 32)), (0, k * 32))
        save(strip, os.path.join(OUT, name + ".png"), PAL)
    # tags: rematch (Poke Ball), home
    tpal = [(0, 0, 0), (40, 40, 64), (248, 248, 248)]
    for state in ("rematch", "home"):
        tpal += list(MC.TAG[state])
    im = Image.new("P", (32, 32), 0)
    cv = Canvas(im)
    for k, state in enumerate(("rematch", "home")):
        dk, fc, lt = 3 + k * 3, 4 + k * 3, 5 + k * 3
        rounded_box(cv, 0, k * 16, 18, 12, 3, fc, 1, lt, dk)
        X.centred_sil(cv, 1, k * 16 + 1, 16, 10, state, 2, dk)
    save(im, os.path.join(OUT, "call_tags.png"), pad16(tpal))
    write_jasc(os.path.join(OUT, "call_tags.pal"), pad16(tpal))
    # window blit sources: pin cap (17x14 at 0,0, divider included), keypad A (24,0), keypad B (32,0)
    im = kit.new_sheet(40, 16, THEME)
    cv = Canvas(im)
    X.label_pill(cv, 0, 0, 40, "pin")
    for x in range(17, 40):
        for y in range(16):
            cv.set(x, y, 0)
    X.keypad(cv, 24, 0, "A")
    X.keypad(cv, 32, 0, "B")
    save(im, os.path.join(OUT, "call_glyphs.png"), PAL)


def main():
    os.makedirs(OUT, exist_ok=True)
    n = export_bg()
    export_obj()
    with open(P("src", "data", "rotom_phone_call_layout.h"), "w") as f:
        f.write("// Generated by dev_scripts/orchid_ui/export_call.py - do not edit.\n")
        f.write("#define CALL_BG_TILES %d   // grid tiles (2x2) follow\n" % n)
    print("call tiles", n)


if __name__ == "__main__":
    main()
