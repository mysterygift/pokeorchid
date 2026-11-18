"""
Export the Orchid field message box (windows.dialogue_box, as drawn by system_ext.message) to game assets.

The frame is drawn with the mockup's own code on a full 240x160 sheet, then cut into the 14-tile
message_box.png sheet (7x2 tiles, vanilla's size, so every LoadMessageBoxGfx caller keeps its tile budget).
The box is not vertically symmetric (light bevel on top, shade + hairline at the bottom), so the bottom
row gets its own tiles in the slots vanilla left blank instead of v-flipping the top row, and the right
end-cap reaches 1px into the window's last column, so that column (middle rows) is a frame tile too:

    slot  0 bottom col R      1 top col L2      2 bottom col R1     3 top col L1     4 top edge
          5 top col R1        6 top col R
          7 mid col L2        8 mid col R1      9 mid col L1       10 mid col R
         11 bottom col L2    12 bottom col L1  13 bottom edge

    (L2 = left - 2, L1 = left - 1, R1 = left + width - 1 (window's last column), R = left + width)

menu.c (WindowFunc_DrawDialogueFrame / DrawDialogueFrameRightEdge) tiles the frame with these slots via
src/data/msgbox_orchid.h; the script rebuilds the box from the sheet exactly like the C code does and
asserts it equals the mock, pixel for pixel.

Palette (gMessageBox_Pal, also GetOverworldTextboxPalettePtr / GetTextWindowPalette(0)):
    0 transparent   1 WHITE (window fill)   2 INK (text)   3 PANEL_SHADE (text shadow)
    4-12 vanilla (TEXT_COLOR_RED .. LIGHT_BLUE, 10-12 vanilla whites) so {COLOR} codes read as before
    13 ACCENT_DARK  14 ACCENT  15 ACCENT_LIGHT (end caps)
Field text keeps printing DARK_GRAY / WHITE / LIGHT_GRAY (2 / 1 / 3), which now are INK / WHITE / PANEL_SHADE.

Writes graphics/text_window/message_box.png, src/data/msgbox_orchid.h.
usage: export_msgbox.py
"""
import os
from PIL import Image
from kit import *
import windows as Wn

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PNG = os.path.join(ROOT, "graphics", "text_window", "message_box.png")
HEADER = os.path.join(ROOT, "src", "data", "msgbox_orchid.h")

# field message window (menu.c sStandardTextBox_WindowTemplates[0]) as in system_ext.message
LEFT, TOP, WIDTH, HEIGHT = 2, 15, 27, 4

REMAP = {TRANSPARENT: 0, WHITE: 1, INK: 2, PANEL_SHADE: 3, ACCENT_DARK: 13, ACCENT: 14, ACCENT_LIGHT: 15}

# vanilla message_box.png palette entries kept as they were (text colours 4-9, unused whites 10-12)
VANILLA_PAL = [(112, 200, 160), (248, 248, 248), (96, 96, 96), (208, 208, 200), (224, 8, 8), (248, 184, 112),
               (32, 152, 8), (144, 240, 144), (48, 80, 200), (160, 192, 240), (248, 248, 248), (224, 232, 224),
               (248, 248, 248), (0, 248, 152), (0, 200, 184), (72, 112, 160)]

# slot -> (tile column relative to the frame, row kind)
SLOTS = {
    "TOP_L2": 1, "TOP_L1": 3, "TOP_EDGE": 4, "TOP_R1": 5, "TOP_R": 6,
    "MID_L2": 7, "MID_R1": 8, "MID_L1": 9, "MID_R": 10,
    "BOT_L2": 11, "BOT_L1": 12, "BOT_EDGE": 13, "BOT_R1": 2, "BOT_R": 0,
}
N_TILES = 14


def palette16():
    k = palette("orchid")
    p = list(VANILLA_PAL)
    p[0] = (0, 0, 0)
    p[1], p[2], p[3] = k[WHITE], k[INK], k[PANEL_SHADE]
    p[13], p[14], p[15] = k[ACCENT_DARK], k[ACCENT], k[ACCENT_LIGHT]
    return p


def mock_frame():
    """The mock's message box, re-indexed into the ROM palette (240x160)."""
    src = new_sheet(240, 160)
    Wn.dialogue_box(Canvas(src), LEFT, TOP, WIDTH, HEIGHT)
    out = Image.new("P", src.size, 0)
    sp, op = src.load(), out.load()
    for y in range(src.size[1]):
        for x in range(src.size[0]):
            v = sp[x, y]
            assert v in REMAP, "unexpected colour role %d at (%d,%d)" % (v, x, y)
            op[x, y] = REMAP[v]
    return out


def cell(px, cx, cy):
    return tuple(px[cx * 8 + x, cy * 8 + y] for y in range(8) for x in range(8))


def layout(left, top, width, height):
    """{(cx, cy): slot name} for every frame cell, mirroring menu.c's WindowFunc_DrawDialogueFrame
    followed by PutWindowTilemap (window cells -> None) and DrawDialogueFrameRightEdge."""
    m = {}
    m[(left - 2, top - 1)] = "TOP_L2"
    m[(left - 1, top - 1)] = "TOP_L1"
    for cx in range(left, left + width - 1):
        m[(cx, top - 1)] = "TOP_EDGE"
    m[(left + width - 1, top - 1)] = "TOP_R1"
    m[(left + width, top - 1)] = "TOP_R"
    for cy in range(top, top + 5):
        m[(left - 2, cy)] = "MID_L2"
        m[(left - 1, cy)] = "MID_L1"
        for cx in range(left, left + width - 1):
            m[(cx, cy)] = "MID_L1"          # under the window
        m[(left + width - 1, cy)] = "MID_R1"
        m[(left + width, cy)] = "MID_R"
    m[(left - 2, top + height)] = "BOT_L2"
    m[(left - 1, top + height)] = "BOT_L1"
    for cx in range(left, left + width - 1):
        m[(cx, top + height)] = "BOT_EDGE"
    m[(left + width - 1, top + height)] = "BOT_R1"
    m[(left + width, top + height)] = "BOT_R"
    # PutWindowTilemap covers the window, then the right-edge pass puts MID_R1 back on its last column
    for cy in range(top, top + height):
        for cx in range(left, left + width - 1):
            m[(cx, cy)] = None
    return m


def main():
    frame = mock_frame()
    px = frame.load()
    lay = layout(LEFT, TOP, WIDTH, HEIGHT)

    tiles = [None] * N_TILES
    for (cx, cy), name in lay.items():
        t = cell(px, cx, cy)
        if name is None:
            assert set(t) == {1}, "window cell (%d,%d) is not plain fill" % (cx, cy)
            continue
        s = SLOTS[name]
        assert tiles[s] is None or tiles[s] == t, "cell (%d,%d) does not repeat slot %s" % (cx, cy, name)
        tiles[s] = t
    tiles = [t if t is not None else tuple([0] * 64) for t in tiles]

    # every cell of the mock's frame rows is covered, so rebuilding == mock
    for cy in range(TOP - 1, TOP + HEIGHT + 1):
        for cx in range(30):
            if (cx, cy) not in lay:
                assert set(cell(px, cx, cy)) == {0}, "mock cell (%d,%d) not covered by the frame" % (cx, cy)

    sheet = Image.new("P", (56, 16), 0)
    sp = sheet.load()
    for i, t in enumerate(tiles):
        ox, oy = (i % 7) * 8, (i // 7) * 8
        for j, c in enumerate(t):
            sp[ox + j % 8, oy + j // 8] = c

    # rebuild from the sheet the way the ROM tiles it and compare with the mock
    rebuilt = Image.new("P", (240, 160), 0)
    rp = rebuilt.load()
    for (cx, cy), name in lay.items():
        s = SLOTS[name] if name else None
        for y in range(8):
            for x in range(8):
                rp[cx * 8 + x, cy * 8 + y] = 1 if s is None else sp[(s % 7) * 8 + x, (s // 7) * 8 + y]
    diff = sum(1 for y in range(160) for x in range(240) if rp[x, y] != px[x, y])
    assert diff == 0, "rebuilt frame differs from the mock in %d pixels" % diff

    pal = palette16()
    flat = [c for rgb in pal for c in rgb]
    sheet.putpalette(flat + [0] * (768 - len(flat)))
    sheet.save(PNG, transparency=0, bits=4)          # 16-entry PLTE: sTextWindowPalettes[][16]
    print("wrote", PNG)

    L = ["// GENERATED by dev_scripts/orchid_ui/export_msgbox.py - do not edit by hand.",
         "// Orchid field message box: tile slots in graphics/text_window/message_box.png.",
         "#ifndef GUARD_DATA_MSGBOX_ORCHID_H",
         "#define GUARD_DATA_MSGBOX_ORCHID_H",
         ""]
    for name, s in sorted(SLOTS.items(), key=lambda kv: kv[1]):
        L.append("#define MSGBOX_TILE_%-9s %d" % (name, s))
    L += ["", "#endif // GUARD_DATA_MSGBOX_ORCHID_H", ""]
    with open(HEADER, "w", newline="\n") as f:
        f.write("\n".join(L))
    print("wrote", HEADER)


if __name__ == "__main__":
    main()
