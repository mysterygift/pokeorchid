#!/usr/bin/env python3
"""Turn the Centre and Mart interior mockups into real tilesets, layouts and map events.

  * gTileset_OrchidCentre / gTileset_OrchidMart: new secondary tilesets (pair with gTileset_Building),
    built from the two art layers of centre_interior.py / mart_interior.py.
  * LAYOUT_POKEMON_CENTER_1F (14x10), LAYOUT_LAVARIDGE_TOWN_POKEMON_CENTER_1F (same, with the back
    door to the hot springs) and LAYOUT_MART (14x9) are repainted and re-pointed in layouts.json.
  * Every map on those layouts: exit warps move to the new mat, the Centre's escalator warp is
    parked on a wall tile (there is no second floor any more), NPCs standing where furniture now
    is move to the nearest free floor tile, the Mart clerk moves behind the new counter, and each
    Centre gets a cafe clerk who sells Kopi, Steamed Bao and Kaya Toast.

    python integrate_interior.py            # dry run
    python integrate_interior.py --write
"""
import json
import os
import re
import struct
import sys
from collections import deque

from PIL import Image

import centre_interior
import inventory
import mart_interior
from vanilla import ROOT

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "hawker_tileset"))
from kit import TileBank  # noqa: E402

NORMAL, COVERED = 0, 1
BLACK = (0, 0, 0)
WALK, BLOCK = 0x3000, 0x0400


def behaviours():
    text = open(os.path.join(ROOT, "include", "constants", "metatile_behaviors.h")).read()
    names = re.findall(r"^\s*(MB_\w+)\s*,", text[text.index("enum"):], re.M)
    return {n: i for i, n in enumerate(names)}


MB = behaviours()


class Tileset:
    def __init__(self, dirname, palettes):
        """palettes: [dict name->colour] in slot order, starting at slot 6."""
        self.dir = os.path.join(ROOT, "data", "tilesets", "secondary", dirname)
        self.pals = []
        for i, p in enumerate(palettes):
            cols = list(dict.fromkeys(p.values()))
            if i == 0:
                cols.append(BLACK)                    # the void outside the room
            assert len(cols) <= 15, (dirname, i, len(cols))
            self.pals.append(cols)
        self.bank = TileBank()
        self.meta, self.attr, self.ids = [], [], {}
        black = tuple(tuple(self.pals[0].index(BLACK) + 1 for _ in range(8)) for _ in range(8))
        idx, _, _ = self.bank.add(black)
        void = (512 + idx) | 6 << 12
        self.void = self.metatile((void,) * 4 + (0,) * 4, COVERED << 12)

    def metatile(self, entries, attr):
        key = (tuple(entries), attr)
        if key not in self.ids:
            self.ids[key] = 0x200 + len(self.meta)
            self.meta.append(list(entries))
            self.attr.append(attr)
        return self.ids[key]

    def entry(self, art, tx, ty, q, transparent_ok):
        x0, y0 = tx * 16 + (q & 1) * 8, ty * 16 + (q >> 1) * 8
        px = [[art.px[y0 + y][x0 + x] for x in range(8)] for y in range(8)]
        cols = {c for r in px for c in r}
        if cols == {None}:
            assert transparent_ok
            return 0
        assert transparent_ok or None not in cols, ("hole in base layer", tx, ty)
        cols.discard(None)
        for i, pal in enumerate(self.pals):
            if cols <= set(pal):
                tile = tuple(tuple(0 if c is None else pal.index(c) + 1 for c in r) for r in px)
                idx, hf, vf = self.bank.add(tile)
                return (512 + idx) | hf << 10 | vf << 11 | (6 + i) << 12
        raise ValueError(f"cell ({tx},{ty}) q{q}: no palette holds {sorted(cols)}")

    def paint(self, base, top, w, h, info):
        """-> rows of block values. info(x, y) -> (behaviour name or None, walkable, over)."""
        rows = []
        for y in range(h):
            row = []
            for x in range(w):
                beh, walk, over = info(x, y)
                ent = [self.entry(base, x, y, q, False) for q in range(4)] + \
                      [self.entry(top, x, y, q, True) for q in range(4)]
                mid = self.metatile(ent, (MB[beh] if beh else 0) | (NORMAL if over else COVERED) << 12)
                row.append(mid | (WALK if walk else BLOCK))
            rows.append(row)
        return rows

    def save(self):
        os.makedirs(os.path.join(self.dir, "palettes"), exist_ok=True)
        n = len(self.bank.tiles)
        assert n <= 512 and len(self.meta) <= 512, (n, len(self.meta))
        im = Image.new("P", (128, ((n + 15) // 16) * 8), 0)
        flat = [BLACK] + self.pals[0] + [BLACK] * (15 - len(self.pals[0]))
        im.putpalette([v for c in flat for v in c])
        px = im.load()
        for i, tile in enumerate(self.bank.tiles):
            for y in range(8):
                for x in range(8):
                    px[(i % 16) * 8 + x, (i // 16) * 8 + y] = tile[y][x]
        im.save(os.path.join(self.dir, "tiles.png"), bits=4, optimize=False)
        with open(os.path.join(self.dir, "metatiles.bin"), "wb") as f:
            for m in self.meta:
                f.write(struct.pack("<8H", *m))
        with open(os.path.join(self.dir, "metatile_attributes.bin"), "wb") as f:
            f.write(struct.pack(f"<{len(self.attr)}H", *self.attr))
        for slot in range(16):
            cols = [BLACK] + (self.pals[slot - 6] if 6 <= slot < 6 + len(self.pals) else [])
            cols += [BLACK] * (16 - len(cols))
            with open(os.path.join(self.dir, "palettes", f"{slot:02d}.pal"), "w", newline="\r\n") as f:
                f.write("JASC-PAL\n0100\n16\n")
                for c in cols:
                    f.write(f"{c[0]} {c[1]} {c[2]}\n")


def save_layout(folder, rows, void):
    d = os.path.join(ROOT, "data", "layouts", folder)
    with open(os.path.join(d, "map.bin"), "wb") as f:
        f.write(struct.pack(f"<{len(rows) * len(rows[0])}H", *[c for r in rows for c in r]))
    with open(os.path.join(d, "border.bin"), "wb") as f:
        f.write(struct.pack("<4H", *([void | BLOCK] * 4)))


# ------------------------------------------------------------------ what each cell is
CW, CH = 14, 10
C_COUNTER = {(x, 3) for x in range(4, 10)} | {(x, 3) for x in range(11, 14)}
C_BLOCK = ({(x, y) for x in range(14) for y in (0, 1)} | C_COUNTER
           | {(0, 2), (3, 2), (4, 2), (5, 2), (6, 2), (9, 2), (10, 2), (11, 2), (13, 2)}
           | {(11, 4), (13, 4), (1, 6), (2, 6), (3, 6), (10, 7), (11, 7), (12, 7), (13, 9)})
C_OVER = {(1, 5), (2, 5), (3, 5), (13, 8)}     # tops of the bench, orchid and palm: drawn over the player
C_MATS = {(6, 9), (7, 9)}
C_KEEP_FREE = {(7, 4), (10, 3), (12, 4), (6, 8), (7, 8)} | C_MATS
C_BEHIND_COUNTER = {(7, 2), (8, 2), (12, 2)}   # staff only


def centre_info(back_door):
    def info(x, y):
        if back_door and (x, y) == (2, 1):
            return "MB_NON_ANIMATED_DOOR", True, False
        if (x, y) in C_COUNTER:
            return "MB_COUNTER", False, False
        if (x, y) == (10, 2):
            return "MB_PC", False, False
        if (x, y) in C_MATS:
            return "MB_SOUTH_ARROW_WARP", True, False
        return None, (x, y) not in C_BLOCK, (x, y) in C_OVER
    return info


MW, MH = 14, 9
M_COUNTER = {(x, 3) for x in range(0, 4)}
M_BLOCK = ({(x, y) for x in range(14) for y in (0, 1)} | M_COUNTER | {(0, 2), (2, 2), (3, 2)}
           | {(x, y) for x in (5, 6, 7, 9, 10, 11) for y in (4, 5)} | {(4, 7), (10, 7), (11, 7)})
M_MATS = {(6, 8), (7, 8)}
M_KEEP_FREE = {(1, 4), (6, 7), (7, 7)} | M_MATS
M_BEHIND_COUNTER = {(1, 2)}


def mart_info(x, y):
    if (x, y) in M_COUNTER:
        return "MB_COUNTER", False, False
    if (x, y) in M_MATS:
        return "MB_SOUTH_ARROW_WARP", True, False
    return None, (x, y) not in M_BLOCK, False


# ------------------------------------------------------------------ map events
def nearest_free(start, w, h, blocked, taken):
    """Breadth-first search for the closest floor tile that is free."""
    seen, queue = {start}, deque([start])
    while queue:
        x, y = queue.popleft()
        if 0 <= x < w and 0 <= y < h and (x, y) not in blocked and (x, y) not in taken:
            return x, y
        for dx, dy in ((0, 1), (-1, 0), (1, 0), (0, -1)):
            n = (x + dx, y + dy)
            if n not in seen and -1 <= n[0] <= w and -1 <= n[1] <= h:
                seen.add(n)
                queue.append(n)
    raise RuntimeError("no free tile")


CAFE_CLERK = {
    "graphics_id": "OBJ_EVENT_GFX_OLD_MAN",
    "x": 12,
    "y": 2,
    "elevation": 3,
    "movement_type": "MOVEMENT_TYPE_FACE_DOWN",
    "movement_range_x": 0,
    "movement_range_y": 0,
    "trainer_type": "TRAINER_TYPE_NONE",
    "trainer_sight_or_berry_tree_id": "0",
    "script": "Common_EventScript_OrchidCafe",
    "flag": "0",
}


def convert_centre(js, log):
    w, h = CW, CH
    unusable = C_BLOCK | C_KEEP_FREE | C_BEHIND_COUNTER
    objs = js.get("object_events") or []
    if any(o.get("script") == CAFE_CLERK["script"] for o in objs):
        return False                                   # already converted
    taken = {(7, 2), (12, 2)}
    for o in objs:
        if o["graphics_id"] == "OBJ_EVENT_GFX_NURSE":
            continue
        old = (o["x"], o["y"])
        want = (10, 3) if old == (10, 2) else old       # someone at the old PC stands at the new one
        new = want if (want == (10, 3) and want not in taken) else nearest_free(want, w, h, unusable, taken)
        taken.add(new)
        if new != old:
            log.append(f"{js['id']}: {o['graphics_id'][14:]} {old} -> {new}")
            o["x"], o["y"] = new
    objs.append(dict(CAFE_CLERK))
    js["object_events"] = objs
    for wp in js.get("warp_events") or []:
        if (wp["x"], wp["y"]) in ((6, 8), (7, 8)):
            wp["y"] = 9
        elif (wp["x"], wp["y"]) == (1, 6):               # escalator to the old second floor
            wp["x"], wp["y"] = 0, 0
    return True


def convert_mart(js, log):
    w, h = MW, MH
    unusable = M_BLOCK | M_KEEP_FREE | M_BEHIND_COUNTER
    objs = js.get("object_events") or []
    if any((wp["x"], wp["y"]) in M_MATS for wp in js.get("warp_events") or []):
        return False                                   # already converted
    taken = {(1, 2)}
    for o in objs:
        old = (o["x"], o["y"])
        if o["graphics_id"] == "OBJ_EVENT_GFX_MART_EMPLOYEE" and old == (1, 3):
            o["x"], o["y"], o["movement_type"] = 1, 2, "MOVEMENT_TYPE_FACE_DOWN"
            continue
        new = nearest_free(old, w, h, unusable, taken)
        taken.add(new)
        if new != old:
            log.append(f"{js['id']}: {o['graphics_id'][14:]} {old} -> {new}")
            o["x"], o["y"] = new
    for wp in js.get("warp_events") or []:
        if (wp["x"], wp["y"]) == (3, 7):
            wp["x"], wp["y"] = 6, 8
        elif (wp["x"], wp["y"]) == (4, 7):
            wp["x"], wp["y"] = 7, 8
    return True


# ------------------------------------------------------------------ wiring
def patch(path, marker, text, before=False):
    s = open(path).read()
    if text.strip().splitlines()[0] in s:
        return
    assert marker in s, (path, marker)
    s = s.replace(marker, text + marker if before else marker + text, 1)
    open(path, "w").write(s)


def wire(sym, dirname):
    base = f"data/tilesets/secondary/{dirname}"
    pals = "\n".join(f'    INCGFX_U16("{base}/palettes/{i:02d}.pal", ".gbapal"),' for i in range(16))
    g = os.path.join(ROOT, "src", "data", "tilesets", "graphics.h")
    s = open(g).read()
    if f"gTilesetTiles_{sym}[]" not in s:
        s = s.rstrip("\n") + f'''

const u32 gTilesetTiles_{sym}[] = INCGFX_U32("{base}/tiles.png", ".4bpp.fastSmol");

const u16 gTilesetPalettes_{sym}[][16] =
{{
{pals}
}};
'''
        open(g, "w").write(s)
    m = os.path.join(ROOT, "src", "data", "tilesets", "metatiles.h")
    s = open(m).read()
    if f"gMetatiles_{sym}[]" not in s:
        s = s.rstrip("\n") + f'''

const u16 gMetatiles_{sym}[] = INCBIN_U16("{base}/metatiles.bin");
const u16 gMetatileAttributes_{sym}[] = INCBIN_U16("{base}/metatile_attributes.bin");
'''
        open(m, "w").write(s)
    hd = os.path.join(ROOT, "src", "data", "tilesets", "headers.h")
    s = open(hd).read()
    if f"gTileset_{sym} =" not in s:
        s = s.rstrip("\n") + f'''

const struct Tileset gTileset_{sym} =
{{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_{sym},
    .palettes = gTilesetPalettes_{sym},
    .metatiles = gMetatiles_{sym},
    .metatileAttributes = gMetatileAttributes_{sym},
    .callback = NULL,
}};
'''
        open(hd, "w").write(s)


def set_layout(layout_id, w, h, secondary):
    p = os.path.join(ROOT, "data", "layouts", "layouts.json")
    s = open(p).read()
    m = re.search(r'\{\s*"id": "' + layout_id + r'",.*?\}', s, re.S)
    block = m.group(0)
    new = re.sub(r'"width": \d+', f'"width": {w}', block)
    new = re.sub(r'"height": \d+', f'"height": {h}', new)
    new = re.sub(r'"secondary_tileset": "\w+"', f'"secondary_tileset": "{secondary}"', new)
    open(p, "w").write(s.replace(block, new))


CAFE_SCRIPT = '''@ The kopi counter in every Pokemon Centre (Pokemon Orchid)
Common_EventScript_OrchidCafe::
	lock
	faceplayer
	message Common_Text_OrchidCafe_Welcome
	waitmessage
	pokemart Common_Pokemart_OrchidCafe
	msgbox Common_Text_OrchidCafe_ComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Common_Pokemart_OrchidCafe:
	.2byte ITEM_KOPI
	.2byte ITEM_STEAMED_BAO
	.2byte ITEM_KAYA_TOAST
	pokemartlistend

Common_Text_OrchidCafe_Welcome:
	.string "Kopi, bao, kaya toast!\\n"
	.string "What'll it be?$"

Common_Text_OrchidCafe_ComeAgain:
	.string "Come back while it's hot!$"
'''


def main(write):
    L, M = inventory.layouts(), inventory.maps()
    # ---- tilesets + layouts
    c_main, c_lava = centre_interior.build(), centre_interior.build(back_door=True)
    cp = c_main["palettes"]
    centre = Tileset("orchid_centre", [cp[k] for k in ("centre_floor", "centre_wall", "centre_furniture",
                                                       "centre_decor", "vanilla_pokemon_center")])
    c_rows = centre.paint(c_main["base"], c_main["top"], CW, CH, centre_info(False))
    l_rows = centre.paint(c_lava["base"], c_lava["top"], CW, CH, centre_info(True))
    m_art = mart_interior.build()
    mart = Tileset("orchid_mart", [m_art["palettes"][k] for k in ("mart_floor", "mart_shell", "mart_goods", "mart_chill")])
    m_rows = mart.paint(m_art["base"], m_art["top"], MW, MH, mart_info)
    for name, ts in (("OrchidCentre", centre), ("OrchidMart", mart)):
        print(f"{name}: {len(ts.bank.tiles)} tiles, {len(ts.meta)} metatiles, {len(ts.pals)} palettes")

    # ---- map events
    log, converted = [], []
    for mid, (path, js) in M.items():
        if js["layout"] in ("LAYOUT_POKEMON_CENTER_1F", "LAYOUT_LAVARIDGE_TOWN_POKEMON_CENTER_1F"):
            changed = convert_centre(js, log)
        elif js["layout"] == "LAYOUT_MART":
            changed = convert_mart(js, log)
        else:
            continue
        if changed:
            converted.append((path, js))
    print(f"maps converted: {len(converted)}")
    for line in log:
        print("  moved " + line)
    if not write:
        print("dry run; pass --write to apply")
        return
    centre.save(), mart.save()
    save_layout("PokemonCenter_1F", c_rows, centre.void)
    save_layout("LavaridgeTown_PokemonCenter_1F", l_rows, centre.void)
    save_layout("Mart", m_rows, mart.void)
    wire("OrchidCentre", "orchid_centre"), wire("OrchidMart", "orchid_mart")
    set_layout("LAYOUT_POKEMON_CENTER_1F", CW, CH, "gTileset_OrchidCentre")
    set_layout("LAYOUT_LAVARIDGE_TOWN_POKEMON_CENTER_1F", CW, CH, "gTileset_OrchidCentre")
    set_layout("LAYOUT_MART", MW, MH, "gTileset_OrchidMart")
    for path, js in converted:
        with open(path, "w") as f:
            json.dump(js, f, indent=2, ensure_ascii=False)
            f.write("\n")
    with open(os.path.join(ROOT, "data", "scripts", "orchid_cafe.inc"), "w") as f:
        f.write(CAFE_SCRIPT)
    patch(os.path.join(ROOT, "data", "event_scripts.s"), '\t.include "data/scripts/pkmn_center_nurse.inc"\n',
          '\t.include "data/scripts/orchid_cafe.inc"\n')
    print("written")


if __name__ == "__main__":
    main("--write" in sys.argv)
