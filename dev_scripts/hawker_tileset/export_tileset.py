#!/usr/bin/env python3
"""
gTileset_HawkerCentre: an open-air hawker centre (roofed food court with open sides) as a
secondary tileset that pairs with the interior primary gTileset_Building. It is an indoor map:
the open sides end in a kerb, a covered drain and a railing, and beyond them is the black void.

    python export_tileset.py                 # tileset files only (safe to re-run)
    python export_tileset.py --paint-layout  # also repaint data/layouts/HawkerCentre/{map,border}.bin
    python export_tileset.py --previews      # also write previews to ./out
    python export_tileset.py --labels        # print METATILE_HawkerCentre_* defines

Writes data/tilesets/secondary/hawker_centre/{tiles.png, metatiles.bin, metatile_attributes.bin,
palettes/00..15.pal}. Deterministic. NOTE: re-running overwrites any Porymap edits to this tileset.

How the pieces combine (everything is 16x16 and modular, so stalls can be recombined per town):

    stall facing south, 3 wide x 4 tall, with a Pillar_* column between neighbours
        row 0  Sign_<Stall>_L / _M / _R            lit signboard on the roof fascia
        row 1  BackWall*  (+ wall props)             white tiles; the hawker's head overlaps this row
        row 2  Kit_<Stall>_L, KitchenFloor, Kit_<Stall>_R      hawker NPC stands on the middle tile
        row 3  Counter_<Stall>_L, Counter_<Stall>_Mid, Counter_<Stall>_R   (MB_COUNTER: talk across)
    stall facing east/west (side of the hall), 3 wide x 4 tall
        row 0  the same three Sign_* tiles
        rows 1-3  kit column | hawker column (KitchenFloor) | VCounter_<Stall>_Top, VCounter_Mid,
                  VCounter_<Stall>_Bot      (mirror the columns for the east side)

Layers: floors are single-layer. Everything else is LAYER_COVERED with the neutral shell or floor
in the bottom layer and the cuisine art / furniture in the top layer, so both draw under sprites.
Only RoofPillar_Top is LAYER_NORMAL (drawn over the player, who can walk behind it).

Palettes (secondary slots 6-12, all used):
    6  floors + void          dining tile, shade, quarry walkway, potted palm, black void
    7  stall shell            walls, steel counters, pillars, kitchen floor, railings
    8  furniture              tables, stools (orange / teal), trays, tableware, bins
    9  curry + satay          10  hokkien mee + chicken rice
    11 crab + kopi            12  berries + ice kachang
Stall palettes share slots (1-4 greys, 5-7 sign ramp A, 8-10 sign ramp B, 11-15 food), so sign
frames and counter stripes are the same tiles for every stall.
"""
import json
import os
import re
import struct
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit                                                            # noqa: E402
from kit import Art, Metatile, LAYER_NORMAL, LAYER_COVERED, ROOT, OUT  # noqa: E402
import art_shell as S                                                 # noqa: E402
import art_stalls                                                     # noqa: E402

LAYOUT_DIR = os.path.join(ROOT, "data", "layouts", "HawkerCentre")


def behaviours():
    text = open(os.path.join(ROOT, "include", "constants", "metatile_behaviors.h")).read()
    names = re.findall(r"^\s*(MB_\w+)\s*,", text[text.index("enum"):], re.M)
    return {n: i for i, n in enumerate(names)}


MB = behaviours()


# ------------------------------------------------------------------ metatile list
def metatile_defs():
    defs = []

    def add(label, bottom, top=None, beh="MB_NORMAL", layer=None, group=""):
        if layer is None:
            layer = LAYER_NORMAL if top is None else LAYER_COVERED
        defs.append(Metatile(label, bottom, top, MB[beh], layer, group))

    shade_n = lambda x, y: y < 3
    shade_w = lambda x, y: x < 3
    shade_nw = lambda x, y: y < 3 or x < 3
    dining, quarry = S.floor(S.dining_px), S.floor(S.quarry_px)

    # ---- floors
    add("Floor", dining, group="Floor")
    add("Floor_ShadeN", S.floor(S.dining_px, shade_n), group="Floor")
    add("Floor_ShadeW", S.floor(S.dining_px, shade_w), group="Floor")
    add("Floor_ShadeNW", S.floor(S.dining_px, shade_nw), group="Floor")
    add("Walkway", quarry, group="Floor")
    add("Walkway_ShadeN", S.floor(S.quarry_px, shade_n), group="Floor")
    add("Walkway_ShadeW", S.floor(S.quarry_px, shade_w), group="Floor")
    add("Walkway_ShadeNW", S.floor(S.quarry_px, shade_nw), group="Floor")

    # ---- open sides (the hall has a roof but no walls; beyond it is the usual indoor void)
    add("Void", S.VOID, group="Open sides")
    for side, rail in (("S", S.RAIL_S), ("W", S.RAIL_W), ("E", S.RAIL_E)):
        add(f"Edge_{side}", S.edge(S.dining_px, side), group="Open sides")
        add(f"Edge_{side}_Rail", S.edge(S.dining_px, side), rail, group="Open sides")
    for side, rail in (("W", S.RAIL_W), ("E", S.RAIL_E)):
        add(f"Walkway_Edge_{side}", S.edge(S.quarry_px, side), group="Open sides")
        add(f"Walkway_Edge_{side}_Rail", S.edge(S.quarry_px, side), rail, group="Open sides")
    add("Edge_SW", S.edge(S.dining_px, "SW"), group="Open sides")
    add("Edge_SE", S.edge(S.dining_px, "SE"), group="Open sides")
    pillar_top, pillar_base = S.ROOF_PILLAR.crop(0, 0), S.ROOF_PILLAR.crop(0, 16)
    add("RoofPillar_Top", dining, pillar_top, layer=LAYER_NORMAL, group="Open sides")
    add("RoofPillar_Base", S.edge(S.dining_px, "S"), S.RAIL_S.over(pillar_base), group="Open sides")
    exit_tile = quarry.copy().blit(S.EXIT_STEPS, 0, 8)
    add("Exit_Steps", exit_tile, beh="MB_SOUTH_ARROW_WARP", group="Open sides")

    # ---- stall shell
    wall, wall_shelf, kfloor = S.back_wall(), S.back_wall(shelf=True), S.kitchen_floor()
    add("Fascia", S.FASCIA, group="Stall shell")
    add("BackWall", wall, group="Stall shell")
    add("BackWall_Shelf", wall_shelf, group="Stall shell")
    add("BackWall_Menu", wall, S.WALL_MENU, group="Stall shell")
    add("BackWall_Bowls", wall_shelf, S.WALL_BOWLS, group="Stall shell")
    add("BackWall_Utensils", wall, S.WALL_UTENSILS, group="Stall shell")
    add("KitchenFloor", kfloor, group="Stall shell")
    add("Counter", S.COUNTER, beh="MB_COUNTER", group="Stall shell")
    for side in "WE":
        for part in ("top", "mid", "bot"):
            add(f"VCounter_{side}_{part.title()}", S.vcounter(part, side), beh="MB_COUNTER",
                group="Stall shell")
    for part in ("top", "plate", "mid", "base"):
        add(f"Pillar_{part.title()}", S.pillar(part), group="Stall shell")
    add("LowWall", S.LOW_WALL, group="Stall shell")
    add("OuterWall_W", S.outer_wall("W"), group="Stall shell")
    add("OuterWall_E", S.outer_wall("E"), group="Stall shell")

    # ---- furniture (on the dining floor)
    def on_floor(label, top, shadow, **kw):
        add(label, S.floor(S.dining_px, shadow), top, group="Furniture", **kw)

    on_floor("Stool", S.STOOL, S.stool_shadow)
    on_floor("Stool_Teal", S.STOOL_TEAL, S.stool_shadow)
    t = S.TABLE_ROUND
    on_floor("Table", t, S.table_shadow)
    on_floor("Table_Laksa", t.over(S.BOWL_LAKSA, 4, 2), S.table_shadow)
    on_floor("Table_Meal", t.over(S.PLATE_RICE, 2, 2).over(S.CUP_KOPI, 10, 3), S.table_shadow)
    on_floor("Table_Chope", t.over(S.TISSUE, 5, 3), S.table_shadow)      # tissue packet = seat taken
    for part in "lmr":
        lt = S.long_table(part)
        sh = S.long_table_shadow(part)
        name = {"l": "L", "m": "M", "r": "R"}[part]
        on_floor(f"LongTable_{name}", lt, sh)
    on_floor("LongTable_L_Meal", S.long_table("l").over(S.BOWL_SOUP, 4, 2).over(S.CHOPSTICKS, 12, 2),
             S.long_table_shadow("l"))
    on_floor("LongTable_M_Laksa", S.long_table("m").over(S.BOWL_LAKSA, 1, 3).over(S.CUP_KOPI, 10, 2),
             S.long_table_shadow("m"))
    on_floor("LongTable_M_Rice", S.long_table("m").over(S.PLATE_RICE, 4, 2),
             S.long_table_shadow("m"))
    on_floor("LongTable_R_Chope", S.long_table("r").over(S.TISSUE, 3, 3).over(S.CUP_KOPI, 10, 4),
             S.long_table_shadow("r"))
    add("TrayReturn_Top", S.LOW_WALL, S.TRAY_RETURN.crop(0, 0), group="Furniture")
    add("TrayReturn_Top_Floor", dining, S.TRAY_RETURN.crop(0, 0), group="Furniture")
    on_floor("TrayReturn_Base", S.TRAY_RETURN.crop(0, 16), S.box_shadow)
    on_floor("PottedPalm", S.POTTED_PALM, S.box_shadow)
    on_floor("Bin", S.BIN, S.box_shadow)
    on_floor("Basin", S.BASIN, S.box_shadow)

    # ---- stalls
    for st in art_stalls.STALLS:
        n, a = st["name"], art_stalls.build(st)
        g = f"Stall: {n}"
        add(f"Sign_{n}_L", S.FASCIA, a["sign_l"], group=g)
        add(f"Sign_{n}_M", S.FASCIA, a["sign_m"], group=g)
        add(f"Sign_{n}_R", S.FASCIA, a["sign_r"], group=g)
        if "wall" in a:
            add(f"BackWall_{n}", wall, a["wall"], group=g)
        add(f"Kit_{n}_L", kfloor, a["kit_l"], group=g)
        add(f"Kit_{n}_R", kfloor, a["kit_r"], group=g)
        add(f"Counter_{n}_L", S.COUNTER, a["cab_l"], beh="MB_COUNTER", group=g)
        add(f"Counter_{n}_Mid", S.COUNTER, a["stripe"], beh="MB_COUNTER", group=g)
        add(f"Counter_{n}_R", S.COUNTER, a["cab_r"], beh="MB_COUNTER", group=g)
        for side in "WE":
            add(f"VCounter_{side}_{n}_Top", S.vcounter("top", side), a["cab_l_plain"],
                beh="MB_COUNTER", group=g)
            add(f"VCounter_{side}_{n}_Bot", S.vcounter("bot", side), a["cab_r"],
                beh="MB_COUNTER", group=g)
    return defs


# ------------------------------------------------------------------ the mock map
W, H = 19, 16
TOP_STALLS = ["Curry", "HokkienMee", "Crab", "ChickenRice"]      # columns 2, 6, 10, 14
WEST_STALLS = ["Satay", "Kopi"]                                    # rows 5, 9
EAST_STALLS = ["Berry", "IceKachang"]
ROOF_PILLARS = (5, 8, 10, 13)
EXIT_X = 9

people = "graphics/object_events/pics/people/"
pals = "graphics/object_events/palettes/"
# (png, palette, frame, tile x, tile y, hflip). Frames: 0 down, 1 up, 2 left (hflip = right).
NPCS = [
    # hawkers
    ("cook.png", "npc_3.pal", 0, 3, 2, False),               # curry
    ("fat_man.png", "npc_1.pal", 0, 7, 2, False),            # hokkien mee
    ("fisherman.png", "npc_2.pal", 0, 11, 2, False),         # soft-shell crab
    ("chef.png", "npc_white.pal", 0, 15, 2, False),          # chicken rice
    ("man_5.png", "npc_2.pal", 2, 2, 7, True),               # satay
    ("old_man.png", "npc_4.pal", 2, 2, 11, True),            # kopi
    ("expert_f.png", "npc_4.pal", 2, 16, 7, False),          # berries
    ("pokefan_f.png", "npc_2.pal", 2, 16, 11, False),        # ice kachang
    # diners
    ("woman_1.png", "npc_1.pal", 0, 6, 6, False),
    ("gentleman.png", "npc_3.pal", 1, 6, 8, False),
    ("girl_1.png", "npc_2.pal", 0, 12, 6, False),
    ("boy_1.png", "npc_3.pal", 2, 13, 11, False),
    ("old_woman.png", "npc_3.pal", 2, 5, 11, True),
    ("youngster.png", "npc_1.pal", 1, 9, 12, False),
    ("lass.png", "npc_4.pal", 1, 11, 4, False),               # queueing at the crab stall
    ("brendan/walking.png", "brendan.pal", 1, 7, 4, False),   # player ordering hokkien mee
]


def build_map(labels):
    """Returns (grid of metatile ids, grid of walkable flags)."""
    ids = {lab: kit.SECONDARY_METATILE_BASE + i for i, lab in enumerate(labels)}
    g = [["Floor"] * W for _ in range(H)]
    walk = [[True] * W for _ in range(H)]

    def put(x, y, label, walkable=False):
        g[y][x] = label
        walk[y][x] = walkable

    # void around the hall
    for y in range(H):
        for x in (0, W - 1):
            put(x, y, "Void")
    for y in range(5, 14):
        put(0, y, "OuterWall_W")
        put(W - 1, y, "OuterWall_E")

    # row of stalls along the north side
    for px in (1, 5, 9, 13, 17):
        for y, part in enumerate(("Top", "Plate", "Mid", "Base")):
            put(px, y, f"Pillar_{part}")
    wall_l = ["BackWall_Bowls", "BackWall_Utensils", "BackWall_Bowls", "BackWall_ChickenRice"]
    wall_r = ["BackWall_Utensils", "BackWall_Bowls", "BackWall_Utensils", "BackWall_Bowls"]
    for i, n in enumerate(TOP_STALLS):
        x = 2 + i * 4
        for dx, part in enumerate("LMR"):
            put(x + dx, 0, f"Sign_{n}_{part}")
        put(x, 1, wall_l[i]), put(x + 1, 1, "BackWall_Menu"), put(x + 2, 1, wall_r[i])
        put(x, 2, f"Kit_{n}_L"), put(x + 1, 2, "KitchenFloor"), put(x + 2, 2, f"Kit_{n}_R")
        put(x, 3, f"Counter_{n}_L"), put(x + 1, 3, f"Counter_{n}_Mid"), put(x + 2, 3, f"Counter_{n}_R")

    # serving walkway
    for x in range(2, W - 2):
        put(x, 4, "Walkway_ShadeN", True)
    put(1, 4, "Walkway_Edge_W_Rail"), put(W - 2, 4, "Walkway_Edge_E_Rail")
    for y in range(5, 14):
        put(4, y, "Walkway", True)
        put(W - 5, y, "Walkway", True)

    # stalls down both sides
    for side, names in (("W", WEST_STALLS), ("E", EAST_STALLS)):
        cols = (1, 2, 3) if side == "W" else (W - 2, W - 3, W - 4)       # kit, hawker, counter
        for i, n in enumerate(names):
            y = 5 + i * 4
            for dx, part in enumerate("LMR"):
                put(min(cols) + dx, y, f"Sign_{n}_{part}")
            put(cols[0], y + 1, f"Kit_{n}_L"), put(cols[0], y + 2, "KitchenFloor"), put(cols[0], y + 3, f"Kit_{n}_R")
            for dy in (1, 2, 3):
                put(cols[1], y + dy, "KitchenFloor")
            put(cols[2], y + 1, f"VCounter_{side}_{n}_Top"), put(cols[2], y + 2, f"VCounter_{side}_Mid")
            put(cols[2], y + 3, f"VCounter_{side}_{n}_Bot")
            if side == "W":
                for dy in (1, 2, 3):
                    put(4, y + dy, "Walkway_ShadeW", True)
        for x in sorted(cols):
            put(x, 13, "LowWall")
            put(x, 14, "Floor_ShadeN", True)

    # tables: two long tables + a round one, then three round tables
    for x0 in (5, 11):
        for dx, part in enumerate(("L", "M", "R")):
            put(x0 + dx, 7, f"LongTable_{part}")
            put(x0 + dx, 6, "Stool"), put(x0 + dx, 8, "Stool")
    put(5, 7, "LongTable_L_Meal"), put(6, 7, "LongTable_M_Laksa"), put(12, 7, "LongTable_M_Rice")
    put(13, 7, "LongTable_R_Chope")
    put(9, 7, "Table_Chope"), put(9, 6, "Stool_Teal"), put(9, 8, "Stool_Teal")
    for x0, top in ((6, "Table_Meal"), (9, "Table"), (12, "Table_Laksa")):
        put(x0, 11, top)
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            put(x0 + dx, 11 + dy, "Stool_Teal" if x0 == 9 else "Stool")

    # utilities
    put(2, 13, "TrayReturn_Top"), put(2, 14, "TrayReturn_Base")
    put(3, 14, "Bin"), put(15, 14, "Basin"), put(16, 14, "Bin")
    put(4, 14, "PottedPalm"), put(14, 14, "PottedPalm")
    # open south side
    put(1, 14, "Edge_W_Rail"), put(W - 2, 14, "Edge_E_Rail")
    for x in range(2, W - 2):
        put(x, 15, "Edge_S_Rail")
    put(1, 15, "Edge_SW"), put(W - 2, 15, "Edge_SE")
    for x in ROOF_PILLARS:
        put(x, 14, "RoofPillar_Top", True)
        put(x, 15, "RoofPillar_Base")
    put(EXIT_X, 15, "Exit_Steps", True)
    return [[ids[c] for c in row] for row in g], walk


def paint_layout(grid, walk, labels):
    os.makedirs(LAYOUT_DIR, exist_ok=True)
    blocks = [m | (0x3000 if w else 0x0400) for row, wrow in zip(grid, walk) for m, w in zip(row, wrow)]
    with open(os.path.join(LAYOUT_DIR, "map.bin"), "wb") as f:
        f.write(struct.pack(f"<{W * H}H", *blocks))
    void = (kit.SECONDARY_METATILE_BASE + labels.index("Void")) | 0x0400
    with open(os.path.join(LAYOUT_DIR, "border.bin"), "wb") as f:
        f.write(struct.pack("<4H", *([void] * 4)))


# ------------------------------------------------------------------ previews
def render_map(bank, data, grid, npcs=True, border=6):
    void = data[[m.label for m in DEFS].index("Void")]
    im = Image.new("RGBA", ((W + 2 * border) * 16, (H + 2 * border) * 16))
    for y in range(-border, H + border):
        for x in range(-border, W + border):
            inside = 0 <= x < W and 0 <= y < H
            entries = data[grid[y][x] - kit.SECONDARY_METATILE_BASE] if inside else void
            im.paste(kit.render_metatile(bank, entries), ((x + border) * 16, (y + border) * 16))
    if npcs:
        for png, pal, frame, tx, ty, hf in sorted(NPCS, key=lambda n: n[4]):
            s = kit.sprite(people + png, pals + pal, frame, hflip=hf)
            im.alpha_composite(s, ((tx + border) * 16, (ty + border) * 16 - 16))
        # the roof pillar tops draw over sprites (top layer of a LAYER_NORMAL metatile)
        top = S.ROOF_PILLAR.crop(0, 0)
        for x in ROOF_PILLARS:
            for yy in range(16):
                for xx in range(16):
                    c = top.px[yy][xx]
                    if c:
                        im.putpixel(((x + border) * 16 + xx, (14 + border) * 16 + yy), c + (255,))
    return im


def sheet(bank, data, scale=4):
    """Every metatile, grouped, straight from the packed data."""
    groups = {}
    for i, m in enumerate(DEFS):
        groups.setdefault(m.group, []).append(i)
    cols, cw, ch = 6, 16 * scale + 150, 16 * scale + 10
    rows = sum((len(v) + cols - 1) // cols for v in groups.values())
    im = Image.new("RGB", (cols * cw, rows * ch + len(groups) * 22), (32, 32, 44))
    dr = ImageDraw.Draw(im)
    y = 0
    for gname, idxs in groups.items():
        dr.text((6, y + 5), gname.upper(), fill=(248, 216, 120))
        y += 22
        for n, i in enumerate(idxs):
            x = (n % cols) * cw
            yy = y + (n // cols) * ch
            im.paste(kit.up(kit.render_metatile(bank, data[i]).convert("RGB"), scale), (x + 4, yy))
            dr.text((x + 16 * scale + 10, yy + 16), f"{0x200 + i:03X}", fill=(160, 160, 176))
            dr.text((x + 16 * scale + 10, yy + 30), DEFS[i].label[:22], fill=(232, 232, 232))
        y += ((len(idxs) + cols - 1) // cols) * ch
    return im


DEFS = metatile_defs()


def main(argv):
    labels = [m.label for m in DEFS]
    assert len(set(labels)) == len(labels), "duplicate labels"
    bank, data, attrs = kit.pack(DEFS)
    kit.write_tileset(bank, data, attrs)
    print(f"tiles: {len(bank.tiles)} (incl. blank tile 0) / 512")
    print(f"metatiles: {len(data)} / 512")
    for slot, pal in sorted(kit.PALETTES.items()):
        print(f"  pal {slot:2d}: {len(pal) - 1} colours")
    grid, walk = build_map(labels)
    if "--paint-layout" in argv:
        paint_layout(grid, walk, labels)
        print("painted data/layouts/HawkerCentre")
    if "--previews" in argv:
        os.makedirs(OUT, exist_ok=True)
        sheet(bank, data).save(os.path.join(OUT, "metatile_sheet_4x.png"))
        full = render_map(bank, data, grid)
        kit.up(full.crop((64, 64, full.width - 64, full.height - 64))).save(os.path.join(OUT, "hawker_centre_3x.png"))
        kit.up(render_map(bank, data, grid, npcs=False, border=0)).save(os.path.join(OUT, "hawker_centre_empty_3x.png"))
        # GBA camera (240x160) with the player on the serving walkway at (7,4): player tile at (112,64)
        for name, (tx, ty) in (("camera_stalls", (7, 4)), ("camera_tables", (9, 9)), ("camera_exit", (9, 14))):
            ox, oy = (tx + 6) * 16 - 112, (ty + 6) * 16 - 72
            cam = full.crop((ox, oy, ox + 240, oy + 160))
            kit.up(cam).save(os.path.join(OUT, f"{name}_3x.png"))
    if "--labels" in argv:
        for i, lab in enumerate(labels):
            print(f"#define METATILE_HawkerCentre_{lab:<28} 0x{kit.SECONDARY_METATILE_BASE + i:03X}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
