"""
Sailor's Voyages, core stream: writes the batch-1 maps for real (approved specs in specs_batch1.py).

  * gTileset_TosaPort: APPENDS the 12 approved metatiles (Briney's dock x6, crates/fish crate, rods, bucket) into
    free all-zero metatile slots 0x2E0-0x2EB and their 15 tiles into tile slots no metatile references.
    Nothing existing moves or changes; palettes are untouched.
  * WavebreakTown map.bin: only the cells that the approved patch changes (south-west beach + dock + props,
    the hut, and the two house roofs repainted purple) are written onto the current file, so the user's own
    Porymap edits elsewhere survive. The patch is computed against the HEAD copy of the layout.
  * New layouts: WavebreakTown_SailorsHut (vanilla Route104_MrBrineysHouse from git 1d1d50b3a2~1),
    NewmoonIsland / NewmoonIsland_Interior (General + Dewford), FullmoonIsland / FullmoonIsland_Interior
    (General + Rustboro), registered append-only in layouts.json.

Events / scripts / map.json are written by build_core_events.py.
usage: <venv python> dev_scripts/voyages/core/build_core_maps.py
"""
import json
import os
import struct
import subprocess
import sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import voyage_compose as vc                 # noqa: E402
import compose                              # noqa: E402  (dev_scripts/tiksi_maps)
import specs_batch1 as sp                   # noqa: E402
import tileset_addition_batch1 as add       # noqa: E402
from PIL import Image                       # noqa: E402

ROOT = vc.ROOT
P = lambda *a: os.path.join(ROOT, *a)       # noqa: E731
TP_DIR = P("data", "tilesets", "secondary", "tosa_port")
RB_DIR = P("data", "tilesets", "secondary", "rustboro")

# ------------------------------------------------------------------ TosaPort addition
# metatile slot -> piece; all 12 slots are all-zero and unused by any General+TosaPort layout (plan())
DOCK = [0x33D, 0x26E, 0x345, 0x26D, 0x335, 0x276]             # Rustboro metatiles copied as they are
PROPS = ["crate_sand", "crates_stacked_sand", "fish_crate_sand", "rods_top", "rods_base", "bucket_sand"]
MT_BASE = 0x2E0
NEW_MT = {}
for _i, _m in enumerate(DOCK):
    NEW_MT["dock_%03X" % _m] = MT_BASE + _i
for _i, _n in enumerate(PROPS):
    NEW_MT[_n] = MT_BASE + len(DOCK) + _i
# tile slots (TosaPort-local index) that no metatile references (plan(): free_tiles), below the balloon
# animation at 224-227
DOCK_TILES = [0x30, 0x31, 0x40, 0x41, 0x50]                    # Rustboro-local tiles used by the dock
NEW_TILE_NAMES = ["fish_l", "fish_r", "rod_a", "rod_b", "rod_c", "rod_d",
                  "bucket_a", "bucket_b", "bucket_c", "bucket_d"]
TILE_SLOTS = [0xD1, 0xD2, 0xD3, 0xD4, 0xD5, 0x107, 0x108, 0x109, 0x10A, 0x125, 0x126, 0x135, 0x145, 0x155, 0x165]
SLOT_OF = {("rb", t): s for t, s in zip(DOCK_TILES, TILE_SLOTS[:5])}
SLOT_OF.update({("new", n): s for n, s in zip(NEW_TILE_NAMES, TILE_SLOTS[5:])})


def _entry(tile, pal, h=0, v=0):
    return (tile & 0x3FF) | (h << 10) | (v << 11) | (pal << 12)


def tosaport_metatiles():
    """-> {slot: (8 u16 entries, attr u16)}"""
    rb = vc.scene(add.RB)
    out = {}
    for m in DOCK:
        ents = []
        for e in rb.s.metatiles[m - 0x200]:
            t = e & 0x3FF
            if t >= 512:
                assert ("rb", t - 512) in SLOT_OF, hex(t)
                e = (e & ~0x3FF) | (512 + SLOT_OF[("rb", t - 512)])
            ents.append(e)
        out[NEW_MT["dock_%03X" % m]] = (ents, rb.s.attrs[m - 0x200])
    sand_raw = list(vc.scene(add.TP).p.metatiles[0x124][:4])
    for name in PROPS:
        entries, layer, _coll = add.PROPOSED[name]
        ents = list(sand_raw)
        for t, pal, h, v in entries[4:]:
            if isinstance(t, str):
                t = 512 + SLOT_OF[("new", t)]
            ents.append(_entry(t, pal, h, v))
        out[NEW_MT[name]] = (ents, (layer << 12) | 0x00)          # MB_NORMAL
    return out


def apply_tosaport():
    mts = tosaport_metatiles()
    # tiles.png
    path = os.path.join(TP_DIR, "tiles.png")
    im = Image.open(path)
    assert im.mode == "P" and im.size == (128, 256), (im.mode, im.size)
    rbim = Image.open(os.path.join(RB_DIR, "tiles.png"))
    px, rpx = im.load(), rbim.load()
    # every slot we write must still be unreferenced by any ORIGINAL metatile
    raw = open(os.path.join(TP_DIR, "metatiles.bin"), "rb").read()
    ents = struct.unpack("<%dH" % (len(raw) // 2), raw)
    ours = set(range(MT_BASE, MT_BASE + 12))
    ref = {e & 0x3FF for i, e in enumerate(ents) if 0x200 + i // 8 not in ours}
    for s in TILE_SLOTS:
        assert 512 + s not in ref, "tile slot 0x%X is referenced" % s
    for (kind, key), s in SLOT_OF.items():
        ox, oy = (s % 16) * 8, (s // 16) * 8
        if kind == "rb":
            sx, sy = (key % 16) * 8, (key // 16) * 8
            for y in range(8):
                for x in range(8):
                    px[ox + x, oy + y] = rpx[sx + x, sy + y]
        else:
            t = add.NEW_TILES[key]
            for y in range(8):
                for x in range(8):
                    px[ox + x, oy + y] = t[y][x]
    im.save(path, bits=4, optimize=False)
    # metatiles.bin / attributes: overwrite only our 12 slots (all-zero before, see plan())
    mraw = bytearray(raw)
    araw = bytearray(open(os.path.join(TP_DIR, "metatile_attributes.bin"), "rb").read())
    for slot, (e8, attr) in mts.items():
        i = slot - 0x200
        old = struct.unpack_from("<8H", mraw, i * 16)
        assert old == (0,) * 8 or list(old) == e8, "metatile 0x%X not free" % slot
        struct.pack_into("<8H", mraw, i * 16, *e8)
        struct.pack_into("<H", araw, i * 2, attr)
    open(os.path.join(TP_DIR, "metatiles.bin"), "wb").write(mraw)
    open(os.path.join(TP_DIR, "metatile_attributes.bin"), "wb").write(araw)
    vc._SCENES.clear()           # re-read TosaPort with the new metatiles
    print("TosaPort: metatiles 0x%X-0x%X, tiles %s" % (MT_BASE, MT_BASE + 11, [hex(s) for s in TILE_SLOTS]))


# ------------------------------------------------------------------ Wavebreak
def head_layout(layout_id, folder):
    e, _ = vc.raw_layout(layout_id)
    raw = subprocess.run(["git", "-C", ROOT, "show", "HEAD:data/layouts/%s/map.bin" % folder],
                         capture_output=True, check=True).stdout
    w, h = e["width"], e["height"]
    vals = struct.unpack("<%dH" % (w * h), raw[:2 * w * h])
    return e, [list(vals[y * w:(y + 1) * w]) for y in range(h)]


def apply_wavebreak():
    compose._LAYOUTS[sp.WB] = head_layout(sp.WB, "WavebreakTown")
    _, g0 = compose._LAYOUTS[sp.WB]
    g = vc.build(sp.WAVEBREAK_AFTER)
    # Briney's dock: Route 104's raw cells (collision/elevation as on Route 104), metatile id -> our copy
    _, r104 = vc.raw_layout(sp.R104)
    for x, y, name in sp.DOCK:
        m = int(name[5:], 16)
        col = {0x33D: 11, 0x345: 11, 0x335: 11}.get(m, 12)
        row = {0x33D: 51, 0x26E: 51, 0x345: 52, 0x26D: 52, 0x335: 53, 0x276: 53}[m]
        src = r104[row][col]
        assert src & 0x3FF == m, (name, hex(src))
        g[y][x] = (src & ~0x3FF) | NEW_MT[name]
        if (src >> 10) & 3 == 0:          # walkable planks: Route 104's elevation 4 -> Wavebreak's sand level 3
            g[y][x] = (g[y][x] & 0x0FFF) | 0x3000
    for x, y, name in sp.BEACH_PROPS:
        coll = add.PROPOSED[name][2]
        g[y][x] = (g[y][x] & 0xF000) | (coll << 10) | NEW_MT[name]
    # Reachability fix (mapcheck.py): with the hut on x12-15 y26-29 the beach pocket in front of its door
    # (x11-15, y30-31) was walled in by the user's 2x2 tree at x16-17 y30-31 (only Route 312's edge led in).
    # The tree goes; its crown peeks become grass, and the tree row below gets its usual peeks.
    TREE_FIX = {(16, 29): 0x3001, (17, 29): 0x3001, (16, 30): 0x3001, (17, 30): 0x3001,
                (16, 31): 0x31CE, (17, 31): 0x31CF}
    assert g0[30][16] & 0x3FF == 0x1D4 and g0[32][16] & 0x3FF == 0x1D4, (hex(g0[30][16]), hex(g0[32][16]))
    for (x, y), v in TREE_FIX.items():
        g[y][x] = v
    changed = [(x, y) for y in range(len(g)) for x in range(len(g[0])) if g[y][x] != g0[y][x]]
    # apply onto the CURRENT file (user's Porymap edits elsewhere are kept)
    path = P("data", "layouts", "WavebreakTown", "map.bin")
    w, h = len(g[0]), len(g)
    cur = list(struct.unpack("<%dH" % (w * h), open(path, "rb").read()[:2 * w * h]))
    for x, y in changed:
        cur[y * w + x] = g[y][x]
    open(path, "wb").write(struct.pack("<%dH" % (w * h), *cur))
    xs, ys = [c[0] for c in changed], [c[1] for c in changed]
    print("Wavebreak: %d cells changed, bbox x%d-%d y%d-%d" % (len(changed), min(xs), max(xs), min(ys), max(ys)))
    outside = [(x, y) for x, y in changed if not (x <= 17 and y >= 26) and not (19 <= x <= 22 and 10 <= y <= 13)
               and not (27 <= x <= 30 and 12 <= y <= 15) and (x, y) not in {(c[0], c[1]) for c in sp.BEACH_PROPS}]
    assert not outside, outside
    del compose._LAYOUTS[sp.WB]
    return g


# ------------------------------------------------------------------ new layouts
NEW_LAYOUTS = OrderedDict()   # folder -> (grid, (primary, secondary), border raw[4])


def git_bin(path):
    return subprocess.run(["git", "-C", ROOT, "show", "1d1d50b3a2~1:" + path], capture_output=True, check=True).stdout


def build_new():
    hut = git_bin("data/layouts/Route104_MrBrineysHouse/map.bin")
    vals = struct.unpack("<%dH" % (12 * 9), hut[:2 * 12 * 9])
    NEW_LAYOUTS["WavebreakTown_SailorsHut"] = ([list(vals[y * 12:(y + 1) * 12]) for y in range(9)],
                                               ("gTileset_Building", "gTileset_GenericBuilding"),
                                               list(struct.unpack("<4H", git_bin(
                                                   "data/layouts/Route104_MrBrineysHouse/border.bin")[:8])))
    sea = [0x0170] * 4
    # seam fixes found by mapcheck.py (the mockups were never walked):
    #  Fullmoon: Route 104's pier planks are elevation 4, the island is 3 -> planks set to 3
    fm = vc.build(sp.FULLMOON_EXT)
    for y in (15, 16):
        for x in (11, 12, 13):
            assert (fm[y][x] >> 10) & 3 == 0, (x, y, hex(fm[y][x]))
            fm[y][x] = (fm[y][x] & 0x0FFF) | 0x3000
    #  Fullmoon: the mask's path from the pier's land end (13,15) north to the meadow ran through (13,14),
    #  which the rim autotiler turned into a cliff corner -> grass like (13,13)
    fm[14][13] = fm[13][13]
    NEW_LAYOUTS["FullmoonIsland"] = (fm, sp.RB, sea)
    NEW_LAYOUTS["FullmoonIsland_Interior"] = (vc.build(sp.FULLMOON_INT), sp.RB, [0x01D4, 0x01D5, 0x01DC, 0x01DD])
    #  Newmoon: the pier's land end (16,15) abutted the solid rock plateau x10-15 -> plateau trimmed to x10-14
    nm = dict(sp.NEWMOON_EXT)
    rows = [list(r) for r in sp.NEWMOON_EXT_MASK]
    for y in (15, 16, 17):
        assert rows[y][15] == "M"
        rows[y][15] = "."
    rows = ["".join(r) for r in rows]
    nm["mask"] = vc.ring_classes(rows, land_chars=".TbM")
    NEW_LAYOUTS["NewmoonIsland"] = (vc.build(nm), sp.DEW_PAIR, sea)
    NEW_LAYOUTS["NewmoonIsland_Interior"] = (vc.build(sp.NEWMOON_INT), sp.DEW_PAIR, [0x0243] * 4)


def snake(name):
    import re
    s = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name.replace("_", "_"))
    return s.upper()


def write_layouts():
    lj_path = P("data", "layouts", "layouts.json")
    lj = json.load(open(lj_path), object_pairs_hook=OrderedDict)
    for folder, (g, ts, border) in NEW_LAYOUTS.items():
        h, w = len(g), len(g[0])
        vc.check_size(w, h) if folder != "WavebreakTown_SailorsHut" else None
        os.makedirs(P("data", "layouts", folder), exist_ok=True)
        vc.write_blocks(g, P("data", "layouts", folder, "map.bin"))
        open(P("data", "layouts", folder, "border.bin"), "wb").write(struct.pack("<4H", *border))
        lid = "LAYOUT_" + snake(folder)
        entry = OrderedDict([
            ("id", lid), ("name", folder + "_Layout"), ("width", w), ("height", h),
            ("primary_tileset", ts[0]), ("secondary_tileset", ts[1]),
            ("border_filepath", "data/layouts/%s/border.bin" % folder),
            ("blockdata_filepath", "data/layouts/%s/map.bin" % folder), ("layout_version", "emerald")])
        for i, e in enumerate(lj["layouts"]):
            if e.get("id") == lid:
                lj["layouts"][i] = entry
                break
        else:
            lj["layouts"].append(entry)
        print("layout %-34s %2dx%-2d %s/%s" % (lid, w, h, ts[0][9:], ts[1][9:]))
    with open(lj_path, "w") as f:
        json.dump(lj, f, indent=2, ensure_ascii=False)
        f.write("\n")


def previews(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    vc._SCENES.clear()
    compose._LAYOUTS.clear()
    for lid, name in (("LAYOUT_WAVEBREAK_TOWN", "wavebreak"),):
        vc.catalog(lid, os.path.join(out_dir, name + "_grid.png"), scale=2)
    for folder in NEW_LAYOUTS:
        vc.catalog("LAYOUT_" + snake(folder), os.path.join(out_dir, folder + "_grid.png"), scale=2)


if __name__ == "__main__":
    apply_tosaport()
    apply_wavebreak()
    build_new()
    write_layouts()
    if "--previews" in sys.argv:
        previews(sys.argv[sys.argv.index("--previews") + 1])
