#!/usr/bin/env python3
"""
gTileset_ColdStorage: the inside of the Tosa Port Cold Storage, a secondary tileset that pairs
with the interior primary gTileset_Building. Steel deck and sheet ice, insulated panel walls,
shipping containers to build a maze from, and loose props to stop a slide against.

    python export_tileset.py                 # tileset files only (safe to re-run)
    python export_tileset.py --paint-layout  # also repaint data/layouts/ColdStorageTest/{map,border}.bin
    python export_tileset.py --previews      # also write previews to ./out
    python export_tileset.py --labels        # print METATILE_ColdStorage_* defines
    python export_tileset.py --solve         # print the puzzle analysis for the test map

Writes data/tilesets/secondary/cold_storage/{tiles.png, metatiles.bin, metatile_attributes.bin,
palettes/00..15.pal}. Deterministic. NOTE: re-running overwrites any Porymap edits to this tileset.

How the pieces combine (everything is 16x16):

    floors      Floor / Ice (MB_ICE: the player slides) / Wet (thawed ice), each with _ShadeN,
                _ShadeW, _ShadeNW for the tile south / east of a wall or container
    north wall  Cap_N over <X>_Upper over <X>_Lower   (X = Wall, Wall_Pipes, Wall_Frost, ...)
    side walls  Cap_W / Cap_E columns, Cap_S along the bottom, Cap_NW/NE/SW/SE corners
    container lying east-west, any length >= 2, colour C in Rust / Green / Amber / Navy
                C_H_Top_L  C_H_Top_M*  C_H_Top_R
              [ C_H_Mid_L  C_H_Mid_M*  C_H_Mid_R ]      optional: makes it a stack of two
                C_H_Bot_L  C_H_Bot_M*  C_H_Bot_R        (C_H_Bot_M_Label = plate on the side)
    container lying north-south (doors facing the camera), 2 wide, any length >= 3
                C_V_Top_L  C_V_Top_R
              [ C_V_Mid_L  C_V_Mid_R ]*
                C_V_FaceA_L C_V_FaceA_R
                C_V_FaceB_L C_V_FaceB_R
    props       <Prop> sits on deck, <Prop>_OnIce on ice: Crate, IceBlock, Barrel, Cone; deck only:
                FishBoxes, WetSign, Gate (locked security gate), Console_On / Console_Off

Layers: ice is LAYER_COVERED with the ice alone in the bottom layer, so the reflection the engine
draws under a sprite next to MB_ICE shows on it. Props are LAYER_COVERED too (floor below, prop on
the middle layer, both under sprites). Every other tile is LAYER_NORMAL: its art sits on the middle
layer, which hides a reflection spilling onto deck, walls or containers; container frost overlays
then land on the top layer, in the part of the tile a sprite's head never reaches.

Palettes (secondary slots 6-12, all used):
    6  floors + void      7  walls + frost      8-11  containers (same slot layout, so the four
    colours share every tile)                   12  props
"""
import os
import struct
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit                                                            # noqa: E402
from kit import Metatile, LAYER_COVERED, LAYER_NORMAL, ROOT, OUT                    # noqa: E402
import art_interior as A                                              # noqa: E402

TS_DIR = os.path.join(ROOT, "data", "tilesets", "secondary", "cold_storage")


def metatile_defs():
    mb = kit.behaviours()
    defs = []

    def add(label, bottom, top=None, behaviour="MB_NORMAL", group="", walk=False):
        # Sprites standing next to ice get a reflection, drawn above the bottom BG layer only.
        # Ice (and props standing on ice) keep the ice in the bottom layer so it shows; every
        # other single-surface tile is LAYER_NORMAL, which puts its art on the middle layer and
        # hides a reflection that spills onto it. Props on deck stay COVERED (deck below, prop on
        # the middle layer) so they still draw under sprites.
        prop_on_floor = group == "props" and top is not None
        layer = LAYER_COVERED if behaviour == "MB_ICE" or prop_on_floor else LAYER_NORMAL
        defs.append(Metatile(label, bottom, top, mb[behaviour], layer, group, walk))

    deck, ice, wet = A.deck(), A.ice(0), A.wet()
    for name, base, beh in (("Floor", deck, "MB_NORMAL"), ("Ice", ice, "MB_ICE"), ("Wet", wet, "MB_NORMAL")):
        add(name, base, None, beh, "floors", True)
        add(name + "_ShadeN", A.shaded(base, north=True), None, beh, "floors", True)
        add(name + "_ShadeW", A.shaded(base, west=True), None, beh, "floors", True)
        add(name + "_ShadeNW", A.shaded(base, north=True, west=True), None, beh, "floors", True)
    add("Ice_B", A.ice(1), None, "MB_ICE", "floors", True)
    add("Floor_Frost", A.frosty(), None, "MB_NORMAL", "floors", True)
    add("Floor_LaneH", A.lane(False), None, "MB_NORMAL", "floors", True)
    add("Floor_LaneV", A.lane(True), None, "MB_NORMAL", "floors", True)
    add("Floor_Hazard", A.hazard(), None, "MB_NORMAL", "floors", True)
    add("Floor_Drain", A.drain(), None, "MB_NORMAL", "floors", True)
    add("Exit", A.exit_mat(), None, "MB_SOUTH_ARROW_WARP", "floors", True)
    add("Void", A.void(), group="floors")

    add("Cap_N", A.cap(s=True), group="walls")
    add("Cap_S", A.cap(n=True), group="walls")
    add("Cap_W", A.cap(e=True), group="walls")
    add("Cap_E", A.cap(w=True), group="walls")
    add("Cap_NW", A.cap(corner="se"), group="walls")
    add("Cap_NE", A.cap(corner="sw"), group="walls")
    add("Cap_SW", A.cap(corner="ne"), group="walls")
    add("Cap_SE", A.cap(corner="nw"), group="walls")
    add("Cap_Fill", A.cap(), group="walls")
    for name, a in (("Wall", A.wall(1)), ("Wall_Pipes", A.wall_pipes()), ("Wall_Frost", A.wall_frost()),
                    ("Wall_Gauge", A.wall_gauge())):
        add(name + "_Upper", a.cell(0, 0), group="walls")
        add(name + "_Lower", a.cell(0, 1), group="walls")
    v = A.wall_vent()
    for cx, col in enumerate("LR"):
        add(f"Wall_Vent_Upper_{col}", v.cell(cx, 0), group="walls")
        add(f"Wall_Vent_Lower_{col}", v.cell(cx, 1), group="walls")

    for colour, leg in A.CONTAINERS.items():
        g = "containers " + colour.lower()
        h = A.container_h(leg, 3, tall=True)
        hl = A.container_h(leg, 3, tall=False, label=True)
        for ry, row in enumerate(("Top", "Mid", "Bot")):
            for cx, col in enumerate("LMR"):
                add(f"{colour}_H_{row}_{col}", h.cell(cx, ry), group=g)
        add(f"{colour}_H_Bot_M_Label", hl.cell(1, 1), group=g)
        add(f"{colour}_H_Top_M_Frost", h.cell(1, 0), A.roof_frost(0), group=g)
        add(f"{colour}_H_Bot_M_Icicles", h.cell(1, 2), A.face_icicles(1), group=g)
        vv = A.container_v(leg, 4)
        for ry, row in enumerate(("Top", "Mid", "FaceA", "FaceB")):
            for cx, col in enumerate("LR"):
                add(f"{colour}_V_{row}_{col}", vv.cell(cx, ry), group=g)
        add(f"{colour}_V_Mid_L_Frost", vv.cell(0, 1), A.roof_frost(1), group=g)

    for name, prop in (("Crate", A.CRATE), ("IceBlock", A.ICE_BLOCK), ("Barrel", A.BARREL), ("Cone", A.CONE)):
        add(name, deck, prop, group="props")
        add(name + "_OnIce", ice, A.CRATE_FROST if name == "Crate" else prop, group="props")
    add("FishBoxes", deck, A.FISH_BOXES, group="props")
    add("WetSign", deck, A.WET_SIGN, group="props")
    add("Gate", A.hazard(), A.GATE, group="props")
    add("Console_On", deck, A.console(True), group="props")
    add("Console_Off", deck, A.console(False), group="props")
    return defs


DEFS = metatile_defs()
LABELS = [m.label for m in DEFS]
ID = {lab: kit.SECONDARY_METATILE_BASE + i for i, lab in enumerate(LABELS)}


def write_tileset(packer, data, attrs):
    os.makedirs(os.path.join(TS_DIR, "palettes"), exist_ok=True)
    tiles = packer.bank.tiles
    n = max(tiles) + 1
    rows = (n + 15) // 16
    im = Image.new("P", (128, rows * 8), 0)
    flat = list(packer.palettes[6]) + [kit.BLACK] * (16 - len(packer.palettes[6]))
    im.putpalette([v for c in flat for v in c])
    px = im.load()
    for i, tile in tiles.items():
        ox, oy = (i % 16) * 8, (i // 16) * 8
        for y in range(8):
            for x in range(8):
                px[ox + x, oy + y] = tile[y][x]
    im.save(os.path.join(TS_DIR, "tiles.png"), bits=4, optimize=False)
    with open(os.path.join(TS_DIR, "metatiles.bin"), "wb") as f:
        for m in data:
            f.write(struct.pack("<8H", *m))
    with open(os.path.join(TS_DIR, "metatile_attributes.bin"), "wb") as f:
        for a in attrs:
            f.write(struct.pack("<H", a))
    for slot in range(16):
        kit.write_pal(os.path.join(TS_DIR, "palettes", f"{slot:02d}.pal"), packer.palettes.get(slot, [kit.BLACK]))


def sheet(packer, data, scale=3):
    groups = {}
    for i, m in enumerate(DEFS):
        groups.setdefault(m.group, []).append(i)
    cols, cw, ch = 7, 16 * scale + 132, 16 * scale + 8
    rows = sum((len(v) + cols - 1) // cols for v in groups.values())
    im = Image.new("RGB", (cols * cw, rows * ch + len(groups) * 20), (32, 32, 44))
    dr = ImageDraw.Draw(im)
    y = 0
    for gname, idxs in groups.items():
        dr.text((6, y + 4), gname.upper(), fill=(248, 216, 120))
        y += 20
        for n, i in enumerate(idxs):
            x = (n % cols) * cw
            yy = y + (n // cols) * ch
            bg = Image.new("RGBA", (16, 16), (0, 0, 0, 255))
            bg.alpha_composite(packer.render_metatile(data[i]))
            im.paste(kit.up(bg.convert("RGB"), scale), (x + 4, yy))
            dr.text((x + 16 * scale + 8, yy + 6), f"{0x200 + i:03X}", fill=(160, 160, 176))
            dr.text((x + 16 * scale + 8, yy + 20), DEFS[i].label[:20], fill=(232, 232, 232))
        y += ((len(idxs) + cols - 1) // cols) * ch
    return im


def main(argv):
    assert len(set(LABELS)) == len(LABELS), "duplicate labels"
    packer = kit.Packer(A.LEGENDS)
    data, attrs = packer.pack(DEFS)
    write_tileset(packer, data, attrs)
    print(f"tiles: {packer.bank.new_count + 1} (incl. blank tile 0) / 512")
    print(f"metatiles: {len(data)} / 512")
    for slot, pal in sorted(packer.palettes.items()):
        print(f"  pal {slot:2d}: {len(pal) - 1} colours")
    if "--labels" in argv:
        for lab in LABELS:
            print(f"#define METATILE_ColdStorage_{lab:<24} 0x{ID[lab]:03X}")
    import test_map
    if "--solve" in argv:
        test_map.report()
    if "--paint-layout" in argv:
        test_map.paint_layout(ID)
        print("painted data/layouts/ColdStorageTest")
    if "--previews" in argv:
        os.makedirs(OUT, exist_ok=True)
        sheet(packer, data).save(os.path.join(OUT, "interior_sheet_3x.png"))
        test_map.previews(packer, data, ID)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
