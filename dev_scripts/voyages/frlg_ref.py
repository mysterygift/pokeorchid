"""
Reference renders of the deleted FRLG Sevii 1-3 layouts (read from git at FRLG_REF, the commit before
"Removed FRLG maps"), drawn with the FRLG tilesets still in data/tilesets (primary 640 metatiles / 7 palettes,
u32 attributes). For design reference only: the FRLG tilesets need the FRLG primary, so none of these cells
can be copied into an Emerald map.

usage: <venv python> dev_scripts/voyages/frlg_ref.py   -> dev_scripts/voyages/ref/frlg/<layout>.png
"""
import json
import os
import re
import struct
import subprocess

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
FRLG_REF = "8ee39561d7~1"
DIRS = {"gTileset_General_Frlg": "primary/general_frlg", "gTileset_SeviiIslands123": "secondary/sevii_islands_123_frlg",
        "gTileset_BerryForest": "secondary/berry_forest_frlg", "gTileset_MtEmber": "secondary/mt_ember_frlg",
        "gTileset_BuildingFrlg": "primary/building_frlg"}


def _dir(sym):
    """Tileset symbol -> data/tilesets/<dir> (DIRS first, else from src/data/tilesets/metatiles.h; batch 3)."""
    if sym not in DIRS:
        src = open(os.path.join(ROOT, "src", "data", "tilesets", "metatiles.h")).read()
        m = re.search(r"gMetatiles_%s\[\] = INCBIN_U16\(\"data/tilesets/([^\"]+)/metatiles\.bin" % sym[len("gTileset_"):], src)
        DIRS[sym] = m.group(1)
    return DIRS[sym]


def _git(path):
    return subprocess.run(["git", "-C", ROOT, "show", "%s:%s" % (FRLG_REF, path)], capture_output=True,
                          check=True).stdout


def _jasc(path):
    v = open(path).read().split()[3:]
    return [tuple(int(c) // 8 * 8 for c in v[i * 3:i * 3 + 3]) for i in range(len(v) // 3)]


class FTileset:
    def __init__(self, sym):
        d = os.path.join(ROOT, "data", "tilesets", _dir(sym))
        im = Image.open(os.path.join(d, "tiles.png"))
        self.w, self.px, self.n = im.width // 8, im.load(), (im.width // 8) * (im.height // 8)
        raw = open(os.path.join(d, "metatiles.bin"), "rb").read()
        self.meta = [struct.unpack_from("<8H", raw, i * 16) for i in range(len(raw) // 16)]
        raw = open(os.path.join(d, "metatile_attributes.bin"), "rb").read()
        self.attrs = list(struct.unpack("<%dI" % (len(raw) // 4), raw))
        self.pals = [_jasc(os.path.join(d, "palettes", "%02d.pal" % i)) for i in range(16)]


def render(layout_id, out):
    js = json.loads(_git("data/layouts/layouts.json"))
    e = next(x for x in js["layouts"] if x.get("id") == layout_id)
    w, h = e["width"], e["height"]
    vals = struct.unpack("<%dH" % (w * h), _git(e["blockdata_filepath"])[:2 * w * h])
    p, s = FTileset(e["primary_tileset"]), FTileset(e["secondary_tileset"])
    pals = p.pals[:7] + s.pals[7:13] + p.pals[13:]
    im = Image.new("RGB", (w * 16, h * 16))
    px = im.load()
    for idx, v in enumerate(vals):
        mid = v & 0x3FF
        ts, i = (p, mid) if mid < 640 else (s, mid - 640)
        if i >= len(ts.meta):
            continue
        layer = (ts.attrs[i] >> 29) & 3
        for k, ent in enumerate(ts.meta[i]):
            t, hf, vf, pal = ent & 0x3FF, (ent >> 10) & 1, (ent >> 11) & 1, ent >> 12
            tt, ti = (p, t) if t < 640 else (s, t - 640)
            if ti >= tt.n:
                continue
            ox, oy = (ti % tt.w) * 8, (ti // tt.w) * 8
            q = k & 3
            bx, by = (idx % w) * 16 + (q & 1) * 8, (idx // w) * 16 + (q >> 1) * 8
            for y in range(8):
                for x in range(8):
                    ci = tt.px[ox + (7 - x if hf else x), oy + (7 - y if vf else y)] & 15
                    if ci == 0 and k >= 4:
                        continue
                    px[bx + x, by + y] = pals[pal][ci]
        del layer
    im.save(out)
    return w, h


BATCH2 = ["LAYOUT_ONE_ISLAND", "LAYOUT_TWO_ISLAND", "LAYOUT_THREE_ISLAND", "LAYOUT_ONE_ISLAND_KINDLE_ROAD",
                "LAYOUT_TWO_ISLAND_CAPE_BRINK", "LAYOUT_THREE_ISLAND_BOND_BRIDGE", "LAYOUT_MT_EMBER_EXTERIOR",
                "LAYOUT_MT_EMBER_SUMMIT", "LAYOUT_THREE_ISLAND_BERRY_FOREST"]

# batch 3 (Sevii 4-7): towns, landmarks, the routes between them, Icefall Cave, Dotted Hole, a Tanoby chamber
BATCH3 = [
    "LAYOUT_FOUR_ISLAND", "LAYOUT_FOUR_ISLAND_ICEFALL_CAVE_ENTRANCE", "LAYOUT_FOUR_ISLAND_ICEFALL_CAVE_1F",
    "LAYOUT_FOUR_ISLAND_ICEFALL_CAVE_B1F", "LAYOUT_FOUR_ISLAND_ICEFALL_CAVE_BACK",
    "LAYOUT_FIVE_ISLAND", "LAYOUT_FIVE_ISLAND_MEADOW", "LAYOUT_FIVE_ISLAND_MEMORIAL_PILLAR",
    "LAYOUT_FIVE_ISLAND_WATER_LABYRINTH", "LAYOUT_FIVE_ISLAND_RESORT_GORGEOUS",
    "LAYOUT_SIX_ISLAND", "LAYOUT_SIX_ISLAND_RUIN_VALLEY", "LAYOUT_SIX_ISLAND_WATER_PATH",
    "LAYOUT_SIX_ISLAND_GREEN_PATH", "LAYOUT_SIX_ISLAND_OUTCAST_ISLAND", "LAYOUT_SIX_ISLAND_DOTTED_HOLE_1F",
    "LAYOUT_SEVEN_ISLAND", "LAYOUT_SEVEN_ISLAND_TANOBY_RUINS", "LAYOUT_SEVEN_ISLAND_TRAINER_TOWER",
    "LAYOUT_SEVEN_ISLAND_SEVAULT_CANYON_ENTRANCE", "LAYOUT_SEVEN_ISLAND_SEVAULT_CANYON",
    "LAYOUT_SEVEN_ISLAND_TANOBY_RUINS_MONEAN_CHAMBER",
]

if __name__ == "__main__":
    import sys
    # no args = batch 2's list (unchanged); "batch3" = BATCH3; or explicit LAYOUT_ ids
    args = sys.argv[1:]
    todo = BATCH2 if not args else BATCH3 if args == ["batch3"] else args
    for lid in todo:
        print(lid, render(lid, os.path.join(HERE, "ref", "frlg", lid[7:].lower() + ".png")))
