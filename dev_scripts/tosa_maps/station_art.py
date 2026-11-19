#!/usr/bin/env python3
"""
Tosa Rail station exterior: a medium (6x5 metatile) building for every station town, packed into
gTileset_TosaPort (the secondary all Tosa towns share).

Look: Singapore's original East-West Line elevated stations (a row of domed roof segments, "segmented
like a caterpillar", over the platform) crossed with Tosa Port's Cold Storage (ribbed ice-blue metal)
and the gatehouse (orange accents): blue domed segments, a white fascia with an orange stripe and a
rail roundel, glass bays between concrete pillars, an orange canopy over a two-tile walk-in entrance.

Only palette 12 (the Cold Storage palette, already in the tileset) is used, so no palette changes.
Quadrants with transparent pixels keep the General grass in the bottom layer and carry the art in the
top layer (layer COVERED); fully opaque quadrants carry the art in the bottom layer.

Tiles come from slots that only unused metatiles reference (they are blanked); metatiles are appended
after the last one. Re-running reuses the same slots (dev_scripts/tosa_maps/station_kit.json).

usage: python3 dev_scripts/tosa_maps/station_art.py [--preview out.png]     (needs Pillow)
"""
import json
import math
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
P = lambda *p: os.path.join(ROOT, *p)
TS = P("data", "tilesets", "secondary", "tosa_port")
KIT = os.path.join(HERE, "station_kit.json")
PAL = 10
W, H = 96, 80                      # 6 x 5 metatiles
DOOR_COLS = (2, 3)                 # walk-in entrance, bottom row
ANIM_TILES = {224, 225, 226, 227}  # Slateport balloons (InitTilesetAnim_Slateport)
MB_NON_ANIMATED_DOOR = 0x60
LAYER_COVERED = 1

# palette 10: a station palette at vanilla saturation (measured from the Centre / house palettes)
STATION_PAL = [(0, 0, 0), (64, 72, 104), (96, 96, 120), (128, 128, 144), (160, 168, 184), (200, 208, 216),
               (232, 232, 232), (248, 248, 248), (144, 72, 64), (184, 104, 80), (208, 136, 104), (224, 168, 128),
               (240, 200, 160), (96, 152, 200), (144, 192, 224), (104, 56, 56)]
T, O, SH, G3, G4, WALL, WL, WH, R0, R1, R2, R3, R4, GL0, GL1, RO = range(16)
VENT = RO


def draw():
    px = [[T] * W for _ in range(H)]

    def put(x, yy, v):
        if 0 <= x < W and 0 <= yy < H:
            px[yy][x] = v

    def rect(x0, y0, x1, y1, v):
        for yy in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                put(x, yy, v)

    def back_slope(x0, x1, y0, y1):
        """Far slope seen from above: the light top band, with faint tile seams."""
        rect(x0, y0, x1, y1, R3)
        for x in range(x0 + 2, x1, 4):
            rect(x, y0 + 1, x, y1, R2)

    def front_slope(x0, x1, y0, y1):
        """Near slope: tile courses, a darker line every 3 rows, seams staggered per course."""
        for yy in range(y0, y1 + 1):
            k = yy - y0
            line = k % 3 == 2
            for x in range(x0, x1 + 1):
                v = R1 if line else R2
                if not line and (x + (4 if (k // 3) % 2 else 0)) % 8 == 0:
                    v = R1
                put(x, yy, v)

    def ridge(x0, x1, yy):
        rect(x0, yy, x1, yy, R4)
        rect(x0, yy + 1, x1, yy + 1, R3)

    # --- lower tier far slope first (full width), the clerestory sits on top of it
    ux0, ux1 = 16, 79
    back_slope(1, W - 2, 14, 19)
    rect(2, 13, W - 3, 13, O)
    put(1, 14, O); put(W - 2, 14, O)
    # --- upper tier (clerestory): x 16..79
    back_slope(ux0 + 1, ux1 - 1, 3, 6)
    ridge(ux0 + 1, ux1 - 1, 7)
    front_slope(ux0 + 1, ux1 - 1, 9, 14)
    rect(ux0 + 1, 15, ux1 - 1, 15, R0)                    # eave lip
    rect(ux0 + 2, 2, ux1 - 2, 2, O)
    rect(ux0, 3, ux0, 15, O); rect(ux1, 3, ux1, 15, O)
    put(ux0 + 1, 2, T); put(ux1 - 1, 2, T); put(ux0 + 1, 3, O); put(ux1 - 1, 3, O)
    # clerestory vents
    rect(ux0 + 2, 16, ux1 - 2, 19, VENT)
    rect(ux0 + 2, 16, ux1 - 2, 16, O)
    for x in range(ux0 + 4, ux1 - 2, 6):
        rect(x, 17, x + 1, 19, G4)
    # --- lower tier: full width; its far slope shows either side of the clerestory
    ridge(1, W - 2, 20)
    front_slope(1, W - 2, 22, 40)
    rect(1, 41, W - 2, 42, R0)                            # eave lip
    rect(0, 14, 0, 42, O); rect(W - 1, 14, W - 1, 42, O)
    rect(0, 43, W - 1, 43, O)
    # --- small front gable over the entrance (pediment with the rail roundel)
    cx, peak, base, half = 47.5, 20, 42, 19
    for yy in range(peak, base + 1):
        f = (yy - peak) / (base - peak)
        a, b = round(cx - 1.5 - half * f), round(cx + 0.5 + half * f)
        for x in range(a, b + 1):
            put(x, yy, WL if yy > peak + 3 else WALL)
        for kk, v in enumerate((O, R3, R2, R1)):
            put(a + kk, yy, v)
        for kk, v in enumerate((O, R1, R2, R1)):
            put(b - kk, yy, v)
        if a + 4 <= b - 4:
            put(a + 4, yy, G4)
    rect(round(cx - 1.5), peak - 1, round(cx + 0.5), peak - 1, O)
    rect(round(cx - 16), 41, round(cx + 16), 42, R0)
    for yy in range(26, 40):
        for x in range(40, 56):
            dd = math.hypot(x - cx, yy - 34.0)
            if dd <= 5.3:
                put(x, yy, GL0 if yy > 33 else GL1)
            elif dd <= 6.3:
                put(x, yy, O)
    for j, row in enumerate(["..WWWW..", ".WGGGGW.", ".WWWWWW.", ".W.WW.W.", "..W..W.."]):
        for k, ch in enumerate(row):
            if ch == "W":
                put(44 + k, 31 + j, WH)
            elif ch == "G":
                put(44 + k, 31 + j, GL0)
    # roof edges in the roof's own dark brown, as vanilla roofs do (the roundel keeps its outline)
    for yy in range(0, 44):
        for x in range(W):
            if px[yy][x] == O and not (39 <= x <= 56 and 26 <= yy <= 41):
                px[yy][x] = RO
    # --- walls: one low storey, set in 3 px under the eave, rendered block courses
    xl, xr = 3, W - 4
    rect(xl, 44, xr, 77, WALL)
    for yy in range(46, 74):
        k = yy - 46
        for x in range(xl + 1, xr):
            if k % 5 == 4 or (x + (5 if (k // 5) % 2 else 0)) % 10 == 0:
                put(x, yy, G4 if k % 5 == 4 else WL)
    rect(xl + 1, 44, xr - 1, 45, SH)                      # eave shadow
    for p0 in (xl + 1, 28, 64, xr - 4):                   # posts, lit from the left
        rect(p0, 46, p0 + 3, 73, WL)
        rect(p0, 46, p0, 73, WH)
        rect(p0 + 3, 46, p0 + 3, 73, G4)
    for bx0, bx1 in ((10, 25), (70, 85)):                 # windows, vanilla style
        rect(bx0, 50, bx1, 62, G3)
        rect(bx0 + 1, 51, bx1 - 1, 56, GL1)
        rect(bx0 + 1, 57, bx1 - 1, 61, GL0)
        rect((bx0 + bx1) // 2, 51, (bx0 + bx1) // 2, 61, G3)
        for gx in (bx0 + 2, (bx0 + bx1) // 2 + 2):
            put(gx + 2, 52, WH); put(gx + 1, 53, WH); put(gx, 54, WH)
        rect(bx0, 63, bx1, 63, G4)                        # sill
    rect(xl, 44, xl, 77, O); rect(xr, 44, xr, 77, O)
    rect(xl + 1, 74, xr - 1, 74, WL)                      # plinth
    rect(xl + 1, 75, xr - 1, 77, G4)
    rect(xl, 78, xr, 78, O)
    # --- entrance: two tiles wide, vanilla door height
    ex0, ex1 = 34, 61
    rect(ex0 - 1, 57, ex1 + 1, 77, G3)
    rect(ex0, 59, ex1, 77, O)
    rect(ex0, 72, ex1, 77, G3)                            # hall floor
    for dx0 in (ex0, ex1 - 4):
        rect(dx0, 59, dx0 + 4, 77, G4)
        rect(dx0 + 1, 60, dx0 + 3, 76, GL0)
        rect(dx0 + 1, 60, dx0 + 3, 66, GL1)
        put(dx0 + 1, 61, WH); put(dx0 + 1, 62, WH)
    rect(ex0 - 1, 78, ex1 + 1, 79, WALL)                  # threshold
    rect(ex0 - 1, 78, ex1 + 1, 78, WL)
    return px


# ---------------------------------------------------------------- tileset packing
def read_u16(path):
    d = open(path, "rb").read()
    return list(struct.unpack(f"<{len(d) // 2}H", d))


def layouts_using_tosaport():
    return [l for l in json.load(open(P("data", "layouts", "layouts.json")))["layouts"]
            if l.get("secondary_tileset") == "gTileset_TosaPort"]


def pack(px):
    from PIL import Image
    kit = json.load(open(KIT)) if os.path.exists(KIT) else {}
    meta = read_u16(os.path.join(TS, "metatiles.bin"))
    attr = read_u16(os.path.join(TS, "metatile_attributes.bin"))
    n = len(attr)
    mine = set(kit.get("metatiles", []))
    used = set()
    for l in layouts_using_tosaport():
        for f in ("blockdata_filepath", "border_filepath"):
            used |= {v & 0x3FF for v in read_u16(P(l[f]))}
    labels = open(P("include", "constants", "metatile_labels.h")).read()
    used |= {int(v, 16) for v in re.findall(r"METATILE_Slateport_\w+\s+(0x[0-9A-Fa-f]+)", labels)}
    used -= mine
    need = {0} | ANIM_TILES
    for m in used:
        k = m - 0x200
        if 0 <= k < n:
            need |= {(v & 0x3FF) - 512 for v in meta[k * 8:k * 8 + 8] if (v & 0x3FF) >= 512}
    free = [t for t in range(512) if t not in need]
    prefer = [t for t in kit.get("tiles", []) if t in free]
    free = prefer + [t for t in free if t not in prefer]

    img = Image.open(os.path.join(TS, "tiles.png"))
    tw = img.size[0] // 8
    tpx = img.load()

    def get_tile(slot):
        return tuple(tuple(tpx[(slot % tw) * 8 + x, (slot // tw) * 8 + yy] for x in range(8)) for yy in range(8))

    def set_tile(slot, tile):
        for yy in range(8):
            for x in range(8):
                tpx[(slot % tw) * 8 + x, (slot // tw) * 8 + yy] = tile[yy][x]

    bank, slots_used = {}, []

    def tile_entry(tile):
        vars_ = {(0, 0): tile, (1, 0): tuple(r[::-1] for r in tile),
                 (0, 1): tile[::-1], (1, 1): tuple(r[::-1] for r in tile[::-1])}
        for (hf, vf), v in vars_.items():
            if v in bank:
                return (bank[v] + 512) | hf << 10 | vf << 11 | PAL << 12
        slot = free[len(slots_used)]
        slots_used.append(slot)
        bank[tile] = slot
        return (slot + 512) | PAL << 12

    gmeta = read_u16(P("data", "tilesets", "primary", "general", "metatiles.bin"))
    grass = gmeta[1 * 8:1 * 8 + 4]                    # bottom layer of the plain grass metatile
    ids = kit.get("metatiles") or [0x200 + n + k for k in range(30)]
    assert len(ids) == 30
    cells = []
    for my in range(5):
        for mx in range(6):
            bottom, topl = [], []
            for q in range(4):
                qx, qy = mx * 16 + (q & 1) * 8, my * 16 + (q >> 1) * 8
                tile = tuple(tuple(px[qy + yy][qx + x] for x in range(8)) for yy in range(8))
                if all(v == T for row in tile for v in row):
                    bottom.append(grass[q]); topl.append(0)
                elif any(v == T for row in tile for v in row):
                    bottom.append(grass[q]); topl.append(tile_entry(tile))
                else:
                    bottom.append(tile_entry(tile)); topl.append(0)
            cells.append(bottom + topl)
    # blank the unused metatiles whose tiles we took, then write ours
    taken = set(slots_used)
    for k in range(n):
        m = 0x200 + k
        if m in used or m in mine:
            continue
        if any((v & 0x3FF) - 512 in taken for v in meta[k * 8:k * 8 + 8]):
            meta[k * 8:k * 8 + 8] = [0] * 8
    for k, mid in enumerate(ids):
        idx = mid - 0x200
        while idx >= len(attr):
            attr.append(0)
            meta.extend([0] * 8)
        meta[idx * 8:idx * 8 + 8] = cells[k]
        my, mx = divmod(k, 6)
        beh = MB_NON_ANIMATED_DOOR if (my == 4 and mx in DOOR_COLS) else 0
        attr[idx] = beh | LAYER_COVERED << 12
    for slot in slots_used:
        set_tile(slot, next(t for t, s in bank.items() if s == slot))
    assert len(attr) <= 512, "secondary metatile limit"
    img.save(os.path.join(TS, "tiles.png"))
    with open(os.path.join(TS, "palettes", "%02d.pal" % PAL), "w") as f:
        f.write("JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % c for c in STATION_PAL))
    open(os.path.join(TS, "metatiles.bin"), "wb").write(struct.pack(f"<{len(meta)}H", *meta))
    open(os.path.join(TS, "metatile_attributes.bin"), "wb").write(struct.pack(f"<{len(attr)}H", *attr))
    # map.bin values: blocked at elevation 0, the two entrance tiles walk-in at elevation 0
    rows = [[ids[my * 6 + mx] | ((0 if (my == 4 and mx in DOOR_COLS) else 1) << 10) for mx in range(6)]
            for my in range(5)]
    kit = {"metatiles": ids, "tiles": sorted(slots_used), "rows": rows, "door": [2, 4], "door2": [3, 4],
           "size": [6, 5]}
    json.dump(kit, open(KIT, "w"), indent=1)
    open(KIT, "a").write("\n")
    print("station: %d tiles in slots %s.., metatiles 0x%03X-0x%03X" % (len(slots_used), sorted(slots_used)[:6], ids[0], ids[-1]))


def preview(px, out):
    from PIL import Image
    pal = STATION_PAL
    im = Image.new("RGB", (W + 32, H + 32), (104, 176, 120))
    for yy in range(H):
        for x in range(W):
            if px[yy][x]:
                im.putpixel((x + 16, yy + 16), pal[px[yy][x]])
    im.resize((im.width * 4, im.height * 4), Image.NEAREST).save(out)


if __name__ == "__main__":
    art = draw()
    if "--preview" in sys.argv:
        preview(art, sys.argv[sys.argv.index("--preview") + 1])
    else:
        pack(art)
