#!/usr/bin/env python3
"""
Cold Storage exterior for Tosa Port: appends metatiles to gTileset_Slateport (General + Slateport
is what LAYOUT_TOSA_PORT uses) without touching anything the tileset already has.

    python export_exterior.py              # patch the tileset (idempotent)
    python export_exterior.py --previews   # also write previews to ./out
    python export_exterior.py --labels     # print METATILE_Slateport_ColdStorage_* defines
    python export_exterior.py --paint-layout   # repaint data/layouts/ColdStorageTestOutside
    python export_exterior.py --paint-tosa-port   # put the building on Tosa Port (replaces the
                                                  # warehouse at x 21-28, y 5-9; door stays at 27,9)

What it changes in data/tilesets/secondary/slateport/:
    tiles.png      new 8x8 tiles go into slots that are blank AND unreferenced by the original
                   406 metatiles (list below); no existing tile moves, so Slateport City etc. are
                   unaffected
    metatiles.bin / metatile_attributes.bin   truncated to the original 406, then re-appended
    palettes/12.pal   was all black and unused by any Slateport metatile; now the building palette
It also writes graphics/door_anims/cold_storage.png (3 frames, sliding double door).

Building kit (all 16x16, any width >= 2):
    row 0  Roof_TL  Roof_T*  Roof_TR          ridge
    row 1  Roof_ML  Roof_M*  Roof_MR          repeat or leave out; Roof_Unit / Roof_Skylight go here
    row 2  Roof_BL  Roof_B*  Roof_BR          scalloped eave + fascia
    row 3  Wall_TL  Wall_T*  Wall_TR          vent band; Sign / Gauge / Door_Top / Shutter_T? go here
    row 4  Wall_BL  Wall_B*  Wall_BR          plinth; Door (warp, animated) / Shutter_B? go here
"""
import os
import struct
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit                                                  # noqa: E402
from kit import Metatile, LAYER_COVERED, ROOT, OUT           # noqa: E402
import art_exterior as X                                    # noqa: E402

TS_DIR = os.path.join(ROOT, "data", "tilesets", "secondary", "slateport")
ORIG_METATILES = 406
PAL_SLOT = 12
# Blank tiles that none of the original 406 metatiles reference (tile 0 is left alone; tiles
# >= 504 are cut off by the -num_tiles 504 build option).
FREE_TILES = [1, 15, 16, 17, 31, 34, 35, 47, 51, 63, 64, 67, 68, 79, 80, 81, 82, 83, 95, 111, 115,
              127, 143, 174, 175, 188, 189, 202, 203, 269, 281, 297, 308, 315, 328, 335, 344, 370,
              371, 375, 393, 427, 441, 443, 451, 456, 457, 459, 490, 491, 502,
              # overflow: leftover art that no original metatile references either
              45, 46, 61, 62]
DOOR_ANIM = os.path.join(ROOT, "graphics", "door_anims", "cold_storage.png")


def metatile_defs():
    mb = kit.behaviours()
    b = X.building(3)
    defs = []

    def add(label, a, behaviour="MB_NORMAL", group="building"):
        defs.append(Metatile("ColdStorage_" + label, a, None, mb[behaviour], LAYER_COVERED, group))

    for ry, row in enumerate(("Roof_T", "Roof_M", "Roof_B", "Wall_T", "Wall_B")):
        for cx, col in enumerate(("L", "", "R")):
            add(row + col, b.cell(cx, ry))
    add("Roof_Unit", X.roof_unit(), group="details")
    add("Roof_Skylight", X.skylight(), group="details")
    add("Wall_Sign", X.sign(), group="details")
    add("Wall_Gauge", X.gauge(), group="details")
    d = X.door()
    add("Door_Top", d.crop(0, 0), group="door")
    add("Door", d.crop(0, 16), "MB_ANIMATED_DOOR", group="door")
    s = X.shutter()
    for cx, col in enumerate("LR"):
        add("Shutter_T" + col, s.crop(cx * 16, 0), group="door")
    for cx, col in enumerate("LR"):
        add("Shutter_B" + col, s.crop(cx * 16, 16), group="door")
    return defs


DEFS = metatile_defs()


def load_tiles_png():
    im = Image.open(os.path.join(TS_DIR, "tiles.png"))
    assert im.mode == "P" and im.size == (128, 256), (im.mode, im.size)
    return im


def write_door_anim(packer):
    """16x96 indexed PNG, 3 frames (ajar, half, open); indices follow palette 12."""
    pal = packer.palettes[PAL_SLOT]
    im = Image.new("P", (16, 96), 0)
    flat = pal + [kit.BLACK] * (16 - len(pal))
    im.putpalette([v for c in flat for v in c])
    px = im.load()
    for f, open_px in enumerate((2, 5, 7)):
        a = X.door(open_px)
        for y in range(32):
            for x in range(16):
                px[x, f * 32 + y] = pal.index(a.px[y][x], 1)
    im.save(DOOR_ANIM, bits=4, optimize=False)


def main(argv):
    labels = [m.label for m in DEFS]
    assert len(set(labels)) == len(labels), "duplicate labels"
    bank = kit.TileBank(slots=FREE_TILES)
    packer = kit.Packer({PAL_SLOT: X.EXT}, bank)
    data, attrs = packer.pack(DEFS)

    # tiles.png: paint the new tiles into their slots, keep the file's own palette
    im = load_tiles_png()
    px = im.load()
    for idx, tile in bank.tiles.items():
        if idx == 0:
            continue
        ox, oy = (idx % 16) * 8, (idx // 16) * 8
        for y in range(8):
            for x in range(8):
                px[ox + x, oy + y] = tile[y][x]
    im.save(os.path.join(TS_DIR, "tiles.png"), bits=4, optimize=False)

    for name, fmt, rows in (("metatiles.bin", "<8H", data), ("metatile_attributes.bin", "<H", attrs)):
        path = os.path.join(TS_DIR, name)
        size = struct.calcsize(fmt)
        raw = open(path, "rb").read()[:ORIG_METATILES * size]
        assert len(raw) == ORIG_METATILES * size, name
        with open(path, "wb") as f:
            f.write(raw)
            for r in rows:
                f.write(struct.pack(fmt, *r) if fmt == "<8H" else struct.pack(fmt, r))
    kit.write_pal(os.path.join(TS_DIR, "palettes", f"{PAL_SLOT:02d}.pal"), packer.palettes[PAL_SLOT])
    write_door_anim(packer)

    print(f"new tiles: {bank.new_count} / {len(FREE_TILES)} free slots")
    print(f"metatiles: {ORIG_METATILES} + {len(data)} = {ORIG_METATILES + len(data)} / 512")
    print(f"palette {PAL_SLOT}: {len(packer.palettes[PAL_SLOT]) - 1} colours")
    base = kit.SECONDARY_METATILE_BASE + ORIG_METATILES
    if "--labels" in argv:
        for i, lab in enumerate(labels):
            print(f"#define METATILE_Slateport_{lab:<28} 0x{base + i:03X}")
    if "--previews" in argv:
        os.makedirs(OUT, exist_ok=True)
        previews(packer, data, labels)
    if "--paint-layout" in argv:
        paint_layout(labels)
        print("painted data/layouts/ColdStorageTestOutside")
    if "--paint-tosa-port" in argv:
        paint_tosa_port(labels)
        print("painted the Cold Storage onto data/layouts/TosaPort/map.bin")
    return 0


# ------------------------------------------------------------------ Tosa Port
TOSA_W, TOSA_H = 38, 40
TOSA_AT = (21, 5)                          # top-left of the old warehouse (8 wide, 5 tall)
OLD_WAREHOUSE = range(0x290, 0x2B5)        # Slateport storage-building metatiles it was made of


def paint_tosa_port(labels):
    """Swap the grey warehouse the sailor guards for the Cold Storage. Same footprint and the
    door stays on (27, 9), so the guard and the sign beside it need no changes. Refuses to paint
    over anything that is neither the old warehouse nor an earlier run of this function."""
    base = kit.SECONDARY_METATILE_BASE + ORIG_METATILES
    ids = {lab[len("ColdStorage_"):]: base + i for i, lab in enumerate(labels)}
    path = os.path.join(ROOT, "data", "layouts", "TosaPort", "map.bin")
    blocks = list(struct.unpack(f"<{TOSA_W * TOSA_H}H", open(path, "rb").read()))
    x0, y0 = TOSA_AT
    for ry, row in enumerate(EXAMPLE_8x5):
        for cx, name in enumerate(row):
            i = (y0 + ry) * TOSA_W + x0 + cx
            old = blocks[i] & 0x3FF
            assert old in OLD_WAREHOUSE or base <= old < base + len(labels), \
                f"unexpected metatile 0x{old:03X} at ({x0 + cx}, {y0 + ry}); has the map changed?"
            blocks[i] = ids[name] | (0x3000 if name == "Door" else 0x0400)
    with open(path, "wb") as f:
        f.write(struct.pack(f"<{TOSA_W * TOSA_H}H", *blocks))


# ------------------------------------------------------------------ outdoor test layout
# A scrap of Tosa Port (General + Slateport) with the building on it, so the exterior tiles and
# the door animation can be checked in-game without editing the real Tosa Port map.
OUT_W, OUT_H = 16, 12
BUILDING_AT = (4, 1)                       # top-left of the 8x5 example
DOOR_AT = (10, 5)
GRASS, SIGN = 0x001, 0x003                 # gTileset_General
PAVE = {"tl": 0x208, "t": 0x209, "tr": 0x20A, "l": 0x210, "m": 0x211, "r": 0x212,
        "bl": 0x218, "b": 0x219, "br": 0x21A}             # gTileset_Slateport cobbles
PAVED = (3, 6, 12, 9)                      # x0, y0, x1, y1


def paint_layout(labels):
    base = kit.SECONDARY_METATILE_BASE + ORIG_METATILES
    ids = {lab[len("ColdStorage_"):]: base + i for i, lab in enumerate(labels)}
    grid = [[GRASS | 0x3000] * OUT_W for _ in range(OUT_H)]
    x0, y0, x1, y1 = PAVED
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            key = ("t" if y == y0 else "b" if y == y1 else "") + ("l" if x == x0 else "r" if x == x1 else "")
            grid[y][x] = PAVE[key or "m"] | 0x3000
    bx, by = BUILDING_AT
    for ry, row in enumerate(EXAMPLE_8x5):
        for cx, name in enumerate(row):
            walk = name == "Door"
            grid[by + ry][bx + cx] = ids[name] | (0x3000 if walk else 0x0400)
    grid[6][12] = SIGN | 0x0400
    d = os.path.join(ROOT, "data", "layouts", "ColdStorageTestOutside")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "map.bin"), "wb") as f:
        f.write(struct.pack(f"<{OUT_W * OUT_H}H", *[v for row in grid for v in row]))
    with open(os.path.join(d, "border.bin"), "wb") as f:
        f.write(struct.pack("<4H", *([GRASS | 0x3000] * 4)))


def previews(packer, data, labels):
    ix = {lab[len("ColdStorage_"):]: i for i, lab in enumerate(labels)}

    def tile(name):
        return packer.render_metatile(data[ix[name]])

    # sheet
    scale, cols = 4, 6
    cw, ch = 16 * scale + 150, 16 * scale + 10
    rows = (len(labels) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cw, rows * ch), (32, 32, 44))
    dr = ImageDraw.Draw(sheet)
    base = kit.SECONDARY_METATILE_BASE + ORIG_METATILES
    for i, lab in enumerate(labels):
        x, y = (i % cols) * cw, (i // cols) * ch
        sheet.paste(kit.up(packer.render_metatile(data[i]).convert("RGB"), scale), (x + 4, y + 4))
        dr.text((x + 16 * scale + 10, y + 16), f"{base + i:03X}", fill=(160, 160, 176))
        dr.text((x + 16 * scale + 10, y + 30), lab[len("ColdStorage_"):], fill=(232, 232, 232))
    sheet.save(os.path.join(OUT, "exterior_sheet_4x.png"))

    # the building as it would sit on Tosa Port (8 wide x 5 tall, door second from the right)
    for name, grid in (("exterior_tosa_port", EXAMPLE_8x5),):
        w, h = len(grid[0]), len(grid)
        im = Image.new("RGBA", (w * 16, h * 16), (112, 200, 160, 255))
        for y, row in enumerate(grid):
            for x, n in enumerate(row):
                im.alpha_composite(tile(n), (x * 16, y * 16))
        im.save(os.path.join(OUT, name + ".png"))
        kit.up(im, 4).save(os.path.join(OUT, name + "_4x.png"))


EXAMPLE_8x5 = [
    ["Roof_TL"] + ["Roof_T"] * 6 + ["Roof_TR"],
    ["Roof_ML", "Roof_M", "Roof_Unit", "Roof_M", "Roof_M", "Roof_Skylight", "Roof_M", "Roof_MR"],
    ["Roof_BL"] + ["Roof_B"] * 6 + ["Roof_BR"],
    ["Wall_TL", "Shutter_TL", "Shutter_TR", "Wall_T", "Wall_Sign", "Wall_T", "Door_Top", "Wall_TR"],
    ["Wall_BL", "Shutter_BL", "Shutter_BR", "Wall_B", "Wall_B", "Wall_B", "Door", "Wall_BR"],
]

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
