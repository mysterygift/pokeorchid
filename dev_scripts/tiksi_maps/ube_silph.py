#!/usr/bin/env python3
"""
Ube City's Silph Co. office: Mossdeep's Space Center, recoloured, in Ube City's own secondary tileset.

  - gTileset_UbeCity: a copy of gTileset_Rustboro (same metatile IDs and tile slots, so Ube's map and
    Rustboro's animated water / fountain tiles keep working) with the building appended. Tiles only
    Ube-unused Rustboro metatiles needed are reused for the building; Rustboro itself is untouched
    (Route 116, Southern Island and Faraway Island still use it).
  - The building is the Space Center's 9x8 block (vanilla Mossdeep City x 60-68, y 8-15). Its roof is
    flattened: each roof row keeps its rim, mirrors it on the right and fills the middle with plain roof,
    so the dishes, the stair hatch and the dome go (the rocket and gantries above row 8 aren't taken).
  - Recolour (the user: "replacing the marshy green of the building"): Mossdeep palette 8's three olive
    entries become lilac-greys of the same brightness; it lives in Ube's free palette slot 6.
  - The grass under the building's transparent edges becomes Ube's paving (metatile 0x2BB).
  - Ube City: the old office and the tall block beside it (x 17-29, rows 2-9) are cleared to paving and
    the building stands at x 18-26, rows 2-9, door (22, 9). The door stays closed: the Silph sign moves
    onto it, and the NPC who stood there moves out front.

usage: <venv>/python dev_scripts/tiksi_maps/ube_silph.py   (needs Pillow)
"""
import json
import os
import shutil
import struct
import sys
from collections import OrderedDict
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "dev_scripts", "tosa_maps"))
import placeholders as PH        # noqa: E402

P = PH.P
SRC = P("data", "tilesets", "secondary", "rustboro")
OUT = P("data", "tilesets", "secondary", "ube_city")
MOSS = P("data", "tilesets", "secondary", "mossdeep")
# Space Center, Mossdeep City (x 60-68, y 8-15), block values from the vanilla map (bb92d78aaf^1)
BUILDING = [
    [0x3A0, 0x3A1, 0x3A2, 0x3A3, 0x3A4, 0x3A5, 0x3A6, 0x3A7, 0x32E],
    [0x3A8, 0x3A9, 0x3AA, 0x3AB, 0x3AC, 0x3AD, 0x3AE, 0x3AF, 0x336],
    [0x3B0, 0x3B1, 0x3B2, 0x3B3, 0x3B4, 0x3B5, 0x3B6, 0x3B7, 0x35B],
    [0x3B8, 0x3B9, 0x3B9, 0x3BA, 0x2DD, 0x3BB, 0x3BC, 0x3BC, 0x3BD],
    [0x3C0, 0x3C1, 0x3C1, 0x3C2, 0x2DD, 0x3C3, 0x3C4, 0x3C4, 0x3C5],
    [0x2DA, 0x2DB, 0x2DB, 0x2DC, 0x2DD, 0x2DE, 0x2DF, 0x2DF, 0x2C7],
    [0x2E2, 0x2E3, 0x2E3, 0x2E4, 0x2E5, 0x2E6, 0x2E7, 0x2E7, 0x2CF],
    [0x2EA, 0x2EB, 0x2EB, 0x2EC, 0x2ED, 0x2EE, 0x2EF, 0x2EF, 0x2D7],
]
ROOF_ROWS = 46                    # roof pixel rows (0-45); 46-47 are its front edge, kept as drawn
MOSS_PAL, NEW_PAL = 8, 6
RECOLOUR = {13: (200, 192, 216), 14: (144, 136, 168), 15: (88, 80, 112)}   # olive -> lilac grey
PAVING = 0x2BB
ANIMATED = set(range(128, 160)) | set(range(448, 452))                    # Rustboro tile anims
AT, DOOR = (18, 2), (4, 7)        # building's top-left in Ube City; door within the building
CLEAR = (17, 2, 29, 9)


def read_pal(path):
    tok = open(path).read().split()
    return [tuple(map(int, tok[3 + i * 3:6 + i * 3])) for i in range(int(tok[2]))]


def write_pal(path, cols):
    with open(path, "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n16\n" + "".join("%d %d %d\n" % c for c in cols))


def metatiles(d):
    b = open(os.path.join(d, "metatiles.bin"), "rb").read()
    return [list(struct.unpack_from("<8H", b, i * 16)) for i in range(len(b) // 16)]


def attrs(d):
    b = open(os.path.join(d, "metatile_attributes.bin"), "rb").read()
    return [struct.unpack_from("<H", b, i * 2)[0] for i in range(len(b) // 2)]


class Sheet:
    def __init__(self, path):
        self.im = Image.open(path)
        assert self.im.mode == "P"
        self.px, self.tw = self.im.load(), self.im.width // 8

    def get(self, t):
        x0, y0 = (t % self.tw) * 8, (t // self.tw) * 8
        return [[self.px[x0 + i, y0 + j] & 15 for i in range(8)] for j in range(8)]

    def put(self, t, rows):
        x0, y0 = (t % self.tw) * 8, (t // self.tw) * 8
        for j in range(8):
            for i in range(8):
                self.px[x0 + i, y0 + j] = rows[j][i]


def main():
    # --- the tileset: a fresh copy of Rustboro each run
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(SRC, OUT, ignore=shutil.ignore_patterns("anim"))      # animation reads Rustboro's frames
    rmt, rat = metatiles(SRC), attrs(SRC)
    mmt, mat = metatiles(MOSS), attrs(MOSS)
    moss = Sheet(os.path.join(MOSS, "tiles.png"))
    sheet = Sheet(os.path.join(OUT, "tiles.png"))
    ube = PH.read_bin(P("data", "layouts", "UbeCity", "map.bin"))
    keep = set(ANIMATED) | {0}
    for v in ube:
        if (v & 0x3FF) >= 512:
            keep |= {(e & 0x3FF) - 512 for e in rmt[(v & 0x3FF) - 512] if (e & 0x3FF) >= 512}
    free = [t for t in range(sheet.tw * (sheet.im.height // 8)) if t not in keep]
    bank = {}

    def alloc(rows):
        key = tuple(map(tuple, rows))
        if not any(any(r) for r in rows):
            return None
        if key not in bank:
            t = free.pop(0)
            sheet.put(t, rows)
            bank[key] = 512 + t
        return bank[key]

    # --- the building as pixels: top layer over the secondary bottom layer ('.' = ground shows)
    W, H = 9 * 16, 8 * 16
    grid = [[None] * W for _ in range(H)]
    for j, row in enumerate(BUILDING):
        for i, m in enumerate(row):
            ent = mmt[m - 512]
            for layer in (0, 1):
                for q in range(4):
                    v = ent[layer * 4 + q]
                    t, hf, vf, p = v & 0x3FF, (v >> 10) & 1, (v >> 11) & 1, v >> 12
                    if t < 512:
                        continue
                    assert p == MOSS_PAL, (hex(m), p)
                    tp = moss.get(t - 512)
                    for y in range(8):
                        for x in range(8):
                            c = tp[7 - y if vf else y][7 - x if hf else x]
                            if c:
                                grid[j * 16 + (q // 2) * 8 + y][i * 16 + (q % 2) * 8 + x] = c
    # --- flatten the roof: rim on the left, mirrored on the right, plain fill between
    for y in range(ROOF_ROWS):
        fill = grid[y][10]
        L = next(x for x in range(W) if grid[y][x] == fill)
        rim = grid[y][:L]
        grid[y] = rim + [fill] * (W - 2 * L) + rim[::-1]
    # --- metatiles: building art on the top layer (palette slot 6), Ube paving underneath
    pave = rmt[PAVING - 512][:4]
    new_mts, new_attrs = [], []
    for j, row in enumerate(BUILDING):
        for i, m in enumerate(row):
            top = []
            for q in range(4):
                x0, y0 = i * 16 + (q % 2) * 8, j * 16 + (q // 2) * 8
                t = alloc([[grid[y0 + y][x0 + x] or 0 for x in range(8)] for y in range(8)])
                top.append(0 if t is None else (t | NEW_PAL << 12))
            new_mts.append(list(pave) + top)
            new_attrs.append((mat[m - 512] & 0x0FFF) | (1 << 12))      # keep the behaviour, layer COVERED
    base = len(rmt)
    assert base + len(new_mts) <= 512
    sheet.im.save(os.path.join(OUT, "tiles.png"))
    with open(os.path.join(OUT, "metatiles.bin"), "wb") as f:
        f.write(b"".join(struct.pack("<8H", *m) for m in rmt + new_mts))
    with open(os.path.join(OUT, "metatile_attributes.bin"), "wb") as f:
        f.write(b"".join(struct.pack("<H", a) for a in rat + new_attrs))
    cols = read_pal(os.path.join(MOSS, "palettes", "%02d.pal" % MOSS_PAL))
    for k, c in RECOLOUR.items():
        cols[k] = c
    write_pal(os.path.join(OUT, "palettes", "%02d.pal" % NEW_PAL), cols)

    # --- Ube City: clear the old office block, stand the building, move the sign and NPC
    lj_path = P("data", "layouts", "layouts.json")
    lj = json.load(open(lj_path), object_pairs_hook=OrderedDict)
    lay = next(l for l in lj["layouts"] if l.get("id") == "LAYOUT_UBE_CITY")
    lay["secondary_tileset"] = "gTileset_UbeCity"
    PH.write_json(lj_path, lj)
    w = lay["width"]
    x0, y0, x1, y1 = CLEAR
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            ube[y * w + x] = 0x3000 | PAVING
    for j in range(8):
        for i in range(9):
            ube[(AT[1] + j) * w + AT[0] + i] = 0x0400 | (0x200 + base + j * 9 + i)
    PH.write_bin(P("data", "layouts", "UbeCity", "map.bin"), ube)
    door = (AT[0] + DOOR[0], AT[1] + DOOR[1])
    mpath = P("data", "maps", "UbeCity", "map.json")
    m = json.load(open(mpath), object_pairs_hook=OrderedDict)
    for b in m["bg_events"]:
        if b["script"] == "UbeCity_EventScript_Sign1":                    # the Silph Co. sign
            b.update(x=door[0], y=door[1], player_facing_dir="BG_EVENT_PLAYER_FACING_NORTH")
    for o in m["object_events"]:
        if x0 <= o["x"] <= x1 and y0 <= o["y"] <= y1:
            o.update(x=door[0] - 2, y=door[1] + 2)
    PH.write_json(mpath, m)
    print("gTileset_UbeCity: building metatiles 0x%03X-0x%03X, %d new tiles; door %s" %
          (0x200 + base, 0x200 + base + len(new_mts) - 1, len(bank), door))


if __name__ == "__main__":
    main()
