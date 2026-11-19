"""
Wavebreak Voyages region maps (regionmap/IMPLEMENTATION.md, decided 2026-11-19). Idempotent.

Writes:
  graphics/pokenav/region_map/map_eon.{png,pal,bin}            REGION_MAP_EON: vanilla Hoenn + dense intro clouds
  graphics/pokenav/region_map/map_holon.{png,pal,bin}          REGION_MAP_HOLON: the user's terrain art
                                                               (ref/holon_region_terrain.png), Tiksi recipe
  graphics/pokedex/region_map_holon.{png,pal,bin}              its Dex AREA copy (user's routes art + markers baked)
  graphics/pokenav/region_map/map_sinnoh.{png,pal,bin}         REGION_MAP_SINNOH (Newmoon + Fullmoon): the Gen 4
                                                               Sinnoh map redrawn Gen 3-style under Eon's clouds
                                                               (regionmap/sinnoh_moons.py)
  graphics/pokedex/region_map_{eon,sinnoh}.bin                 Dex AREA tilemaps (u16 32x32; same tiles/palette)
  graphics/pokenav/region_map/map_sevii_*.bin, graphics/pokedex/region_map_sevii*.bin
                                                               FRLG "switch map" button erased (sea tile)
  src/data/region_map/region_map_layout_sevii{123,45,67}.h     cursor grids (vanilla FRLG from git HEAD + edits)
  src/data/region_map/region_map_layout_voyages.h              Eon / Holon / Sinnoh grids
  src/data/region_map/orchid_map_v2_voyages.h                  MAP v2 nodes / sea tubes / components + strait cells
  src/data/region_map/region_map_sections.json                 the voyage block entries + Eon Island (x/y/w/h)
The Tosa / Tiksi exporters leave all of these alone (export_region_map.py KEEP, Tiksi kanto_block ends at
MAPSEC_ONE_ISLAND).

usage: <venv python> dev_scripts/voyages/export_region_maps.py
"""
import json
import os
import struct
import subprocess
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "regionmap"))
import rm_common as C  # noqa: E402
import eon_clouds as E  # noqa: E402
import sinnoh_moons as SM  # noqa: E402
import sevii as S  # noqa: E402
import export_map_v2 as V2  # noqa: E402  (dev_scripts/orchid_ui, on sys.path via rm_common)
import export_region_map as T  # noqa: E402  (Tosa / Tiksi terrain helpers: build_tiles, palette_of, ...)
import mock_map as MM  # noqa: E402
from PIL import Image  # noqa: E402

ROOT = C.ROOT
RM = C.RM
DEX = os.path.join(ROOT, "graphics", "pokedex")
DATA = os.path.join(ROOT, "src", "data", "region_map")
SECTIONS = os.path.join(DATA, "region_map_sections.json")

STRAIT_IDS = {"MAPSEC_SEVII_ISLE_22": "MAPSEC_ONE_TWO_STRAIT", "MAPSEC_SEVII_ISLE_23": "MAPSEC_TWO_THREE_STRAIT",
              "MAPSEC_SEVII_ISLE_24": "MAPSEC_FOUR_FIVE_STRAIT", "MAPSEC_THREE_ISLE_PATH": "MAPSEC_SIX_SEVEN_STRAIT"}
# strait -> (the two towns whose visits turn its tube blue, cursor mode). "h": progress = x / map width;
# "d" (L-shaped): progress = (x / width + y / height) / 2 (the sea route map enters at the top, leaves right)
STRAIT_INFO = {
    "MAPSEC_ONE_TWO_STRAIT": (("MAPSEC_ONE_ISLAND", "MAPSEC_TWO_ISLAND"), "h", False),
    "MAPSEC_TWO_THREE_STRAIT": (("MAPSEC_TWO_ISLAND", "MAPSEC_THREE_ISLAND"), "d", False),
    "MAPSEC_FOUR_FIVE_STRAIT": (("MAPSEC_FOUR_ISLAND", "MAPSEC_FIVE_ISLAND"), "d", False),
    # Sea Route D: Seven Island on the left, Six on the right; the cell list runs Six -> Seven, so reverse it
    "MAPSEC_SIX_SEVEN_STRAIT": (("MAPSEC_SIX_ISLAND", "MAPSEC_SEVEN_ISLAND"), "h", True),
}
# sections with no cell of their own: the entry borrows the parent's bbox (cursor scales into it)
BORROW = {
    "MAPSEC_ICEFALL_CAVE": "MAPSEC_FOUR_ISLAND", "MAPSEC_EMBER_SPA": "MAPSEC_KINDLE_ROAD",
    "MAPSEC_ROCKET_WAREHOUSE": "MAPSEC_FIVE_ISLE_MEADOW", "MAPSEC_DOTTED_HOLE": "MAPSEC_RUIN_VALLEY",
    "MAPSEC_TANOBY_KEY": "MAPSEC_TANOBY_RUINS", "MAPSEC_MONEAN_CHAMBER": "MAPSEC_TANOBY_RUINS",
    "MAPSEC_LIPTOO_CHAMBER": "MAPSEC_TANOBY_RUINS", "MAPSEC_WEEPTH_CHAMBER": "MAPSEC_TANOBY_RUINS",
    "MAPSEC_DILFORD_CHAMBER": "MAPSEC_TANOBY_RUINS", "MAPSEC_SCUFIB_CHAMBER": "MAPSEC_TANOBY_RUINS",
    "MAPSEC_RIXY_CHAMBER": "MAPSEC_TANOBY_RUINS", "MAPSEC_VIAPOIS_CHAMBER": "MAPSEC_TANOBY_RUINS",
}
SINGLES = {   # REGION_MAP_* -> [(mapsec, cell, landmark)]
    "EON": [("MAPSEC_EON_ISLAND", E.ISLAND, None)],                       # None = no node (ring + head only)
    # Holon (user, 2026-11-19; screen cells of holon_region_routes.png minus (1, 2)): Village (11,11) centre,
    # Mirage Forest (15,13) on the east coast, Research Tower (9,3) top, Holon Lake (3,15) bottom-left
    "HOLON": [("MAPSEC_HOLON_VILLAGE", (10, 9), False), ("MAPSEC_MIRAGE_FOREST", (14, 11), True),
              ("MAPSEC_RESEARCH_TOWER", (8, 1), True), ("MAPSEC_HOLON_LAKE", (2, 13), True)],
    "SINNOH": None,                      # Newmoon + Fullmoon: cells from sinnoh_moons.convert() (export_sinnoh)
}
# land route tubes (the user's yellow cells, cursor grid): Lake -> east -> junction, north up to the Tower,
# branch east to the Village, then east and south to Mirage Forest
HOLON_ROUTES = ([(x, 13) for x in range(3, 8)] + [(8, y) for y in range(2, 14)] + [(9, 9)]
                + [(x, 9) for x in range(11, 15)] + [(14, 10)])
HOLON_REF = os.path.join(HERE, "ref")
GEN = "// GENERATED by dev_scripts/voyages/export_region_maps.py - do not edit.\n"


def P(*p):
    return os.path.join(ROOT, *p)


# ------------------------------------------------------------------ graphics helpers
def write_sheet(path, tiles, pal):
    rows = (len(tiles) + 15) // 16
    sheet = Image.new("P", (128, rows * 8))
    sheet.putpalette(pal)
    for i, t in enumerate(tiles):
        sheet.paste(t if isinstance(t, Image.Image) else Image.frombytes("P", (8, 8), t), ((i % 16) * 8, (i // 16) * 8))
    sheet.save(path)


def write_pal48(path, pal):
    with open(path, "w") as f:      # the 48 colours loaded at BG_PLTT_ID(7) (indices 112-159)
        f.write("JASC-PAL\r\n0100\r\n48\r\n")
        for i in range(112, 160):
            f.write("%d %d %d\r\n" % tuple(pal[i * 3:i * 3 + 3]))


def dex_bin(tmap64):
    out = bytearray()
    for y in range(32):
        for x in range(32):
            out += struct.pack("<H", tmap64[y * 64 + x] if (x < 30 and y < 20) else 0)
    return bytes(out)


def export_eon():
    sheet, tmap, _ = C.vanilla_hoenn()
    im = E.build(C.bg2_from(sheet, tmap), "map", E.DENSE)
    tiles, tm = E.to_rom(im)
    assert len(tiles) <= 256, len(tiles)
    write_sheet(os.path.join(RM, "map_eon.png"), tiles, im.getpalette())
    write_pal48(os.path.join(RM, "map_eon.pal"), im.getpalette())
    open(os.path.join(RM, "map_eon.bin"), "wb").write(tm)
    open(os.path.join(DEX, "region_map_eon.bin"), "wb").write(dex_bin(tm))
    return len(tiles)


def export_holon():
    """Tiksi recipe (export_region_map_tiksi.write_terrain / write_dex) on the user's Holon art (not rotated)."""
    load = lambda n: Image.open(os.path.join(HOLON_REF, n)).convert("RGB")
    ttiles, tcells = T.build_tiles(load("holon_region_terrain.png"))
    assert len(ttiles) <= 256, len(ttiles)
    tcols = T.palette_of(ttiles)
    T.write_png8(os.path.join(RM, "map_holon.png"), ttiles, tcols)
    T.write_jasc48(os.path.join(RM, "map_holon.pal"), tcols)
    amap = bytearray(64 * 64)
    for i, t in enumerate(tcells):
        amap[(i // 30) * 64 + i % 30] = t
    open(os.path.join(RM, "map_holon.bin"), "wb").write(bytes(amap))
    # Dex AREA: the user's routes art with the Tosa city / landmark markers on the node cells
    im = load("holon_region_routes.png")
    px = im.load()
    for y in range(im.height):           # 256-tile budget: the darkest route shade (50 px) -> the next one
        for x in range(im.width):
            if px[x, y] == (224, 160, 0):
                px[x, y] = (232, 184, 56)
    for _, (cx, cy), lm in SINGLES["HOLON"]:
        t = T.landmark_tile() if lm else T.city_tile()
        for y in range(8):
            for x in range(8):
                px[C.GX + cx * 8 + x, C.GY + cy * 8 + y] = t[y][x]
    dtiles, dcells = T.build_tiles(im)
    assert len(dtiles) <= 256, len(dtiles)
    dcols = T.palette_of(dtiles)
    T.write_png8(os.path.join(DEX, "region_map_holon.png"), dtiles, dcols)
    T.write_jasc48(os.path.join(DEX, "region_map_holon.pal"), dcols)
    tmap = bytearray()
    for y in range(32):
        for x in range(32):
            tmap += struct.pack("<H", dcells[y * 30 + x] if (x < 30 and y < 20) else 0)
    open(os.path.join(DEX, "region_map_holon.bin"), "wb").write(bytes(tmap))
    src = open(os.path.join(ROOT, "src", "region_map.c")).read()
    for png, n in (("map_holon.png", len(ttiles)), ("region_map_holon.png", len(dtiles))):
        if '%s", ".8bpp.smol", "-num_tiles %d ' % (png, n) not in src:
            print("!! update src/region_map.c: %s needs \"-num_tiles %d\"" % (png, n))
    return len(ttiles), len(dtiles), len(tcols), len(dcols)


def export_sinnoh():
    """REGION_MAP_SINNOH: the Gen 3 conversion of the Sinnoh map, masked by Eon's clouds round the islets."""
    rgb, islets, _, _ = SM.convert()
    im = SM.masked(rgb, islets)
    tiles, tm = E.to_rom(im)
    assert len(tiles) <= 256, len(tiles)
    write_sheet(os.path.join(RM, "map_sinnoh.png"), tiles, im.getpalette())
    write_pal48(os.path.join(RM, "map_sinnoh.pal"), im.getpalette())
    open(os.path.join(RM, "map_sinnoh.bin"), "wb").write(tm)
    open(os.path.join(DEX, "region_map_sinnoh.bin"), "wb").write(dex_bin(tm))
    if '"-num_tiles %d ' % len(tiles) not in open(os.path.join(ROOT, "src", "region_map.c")).read():
        print("!! update src/region_map.c: map_sinnoh.png needs \"-num_tiles %d\"" % len(tiles))
    # cursor cells = screen tile - (1, 2); both islets are landmarks (diamonds), Newmoon first (fallback)
    SINGLES["SINNOH"] = [(m, (t[0] - 1, t[1] - 2), True) for m, t in sorted(islets.items(), key=lambda kv: kv[0] != "MAPSEC_NEWMOON_ISLAND")]
    return len(tiles), SINGLES["SINNOH"]


def erase_sevii_buttons():
    """FRLG's baked switch-map button (cells ERASE_BOX -> tiles +1 x, +2 y) -> the map's sea tile."""
    out = {}
    bx0, by0, bx1, by1 = S.ERASE_BOX
    box = [(tx, ty) for ty in range(by0 + 2, by1 + 2) for tx in range(bx0 + 1, bx1 + 1)]
    for key in ("123", "45", "67"):
        p = os.path.join(RM, "map_sevii_%s.bin" % key)
        tm = bytearray(open(p, "rb").read())
        sea = Counter(tm[y * 64 + x] for y in range(20) for x in range(30)).most_common(1)[0][0]
        n = 0
        for tx, ty in box:
            if tm[ty * 64 + tx] != sea:
                tm[ty * 64 + tx] = sea
                n += 1
        open(p, "wb").write(bytes(tm))
        p = os.path.join(DEX, "region_map_sevii%s.bin" % key)
        dm = bytearray(open(p, "rb").read())
        w = 32
        vals = [struct.unpack_from("<H", dm, (y * w + x) * 2)[0] for y in range(20) for x in range(30)]
        dsea = Counter(vals).most_common(1)[0][0]
        dn = 0
        for tx, ty in box:
            if struct.unpack_from("<H", dm, (ty * w + tx) * 2)[0] != dsea:
                struct.pack_into("<H", dm, (ty * w + tx) * 2, dsea)
                dn += 1
        open(p, "wb").write(bytes(dm))
        out[key] = (n, dn)
    return out


# ------------------------------------------------------------------ grids
def vanilla_grid(key):
    src = subprocess.check_output(["git", "-C", ROOT, "show",
                                   "HEAD:src/data/region_map/region_map_layout_sevii%s.h" % key]).decode()
    import re
    return [re.findall(r"MAPSEC_\w+", r) for r in src.split("\n") if r.strip().startswith("{MAPSEC")]


def sevii_grid(key, cl):
    g = [list(r) for r in vanilla_grid(key)]
    for y, r in enumerate(g):
        for x, s in enumerate(r):
            if s in cl["clear"]:
                g[y][x] = "MAPSEC_NONE"
    for (x, y), s in cl["moves"].items():
        g[y][x] = s
    for s, (_, cells, _j) in cl["straits"].items():
        for x, y in cells:
            assert g[y][x] == "MAPSEC_NONE", (key, s, x, y, g[y][x])
            g[y][x] = STRAIT_IDS[s]
    used = set(s for r in g for s in r) - {"MAPSEC_NONE"}
    names = dict(cl["towns"], **cl["landmarks"], **cl["routes"])
    names.update({STRAIT_IDS[s]: v[0] for s, v in cl["straits"].items()})
    stray = used - set(names)
    assert not stray, (key, stray)       # every remaining cell is a built place
    return g


def empty_grid():
    return [["MAPSEC_NONE"] * 28 for _ in range(15)]


def grid_c(name, g):
    lines = ["static const mapsec_u8_t %s[MAP_HEIGHT][MAP_WIDTH] = {" % name]
    for r in g:
        lines.append("    {" + ", ".join(r) + "},")
    lines.append("};")
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------ MAP v2 tubes
def frame_tiles():
    im = Image.open(os.path.join(RM, "orchid_frame.png"))
    cols = im.width // 8
    out = []
    for i in range(cols * (im.height // 8)):
        out.append(im.crop(((i % cols) * 8, (i // cols) * 8, (i % cols) * 8 + 8, (i // cols) * 8 + 8)))
    return out


def match_tile(t, frame):
    """t: 8x8 'P' tube tile (indices 0-4). -> tile id with BG flip bits from Tosa's orchid_frame.png."""
    if not any(t.tobytes()):
        return 0
    for i, f in enumerate(frame):
        if i < 16:                       # ORCHID_MAP_FRAME_TILES: the header / tray tiles
            continue
        for hf in (0, 1):
            for vf in (0, 1):
                g = f
                if hf:
                    g = g.transpose(Image.FLIP_LEFT_RIGHT)
                if vf:
                    g = g.transpose(Image.FLIP_TOP_BOTTOM)
                if g.tobytes() == t.tobytes():
                    return i | (hf << 10) | (vf << 11)
    frame.append(t.copy())               # new shape: appended to orchid_frame_voyages.png
    return len(frame) - 1


def v2_region(tag, nodes, straits, frame, routes=()):
    """nodes: [(mapsec, (x, y), landmark)], straits: {mapsec: [cells]}, routes: land tube cells (Tosa / Tiksi
    route-line look: gold once every place the route touches is visited) -> C text."""
    node_cells = {m: c for m, c, _ in nodes}
    cells = {c: "sea" for cs in straits.values() for c in cs}
    cells.update({c: "land" for c in routes})
    timg = V2.tube_image(V2.tube_mask(cells, node_cells)) if cells else None

    def tile_at(c):
        if timg is None:
            return 0
        x, y = V2.GX + c[0] * 8, V2.GY + c[1] * 8
        return match_tile(timg.crop((x, y, x + 8, y + 8)), frame)

    idx = {m: i for i, (m, _, _) in enumerate(nodes)}
    out = ["static const struct OrchidMapNode sOrchidMapNodes_%s[] =" % tag, "{"]
    for m, (x, y), lm in nodes:
        out.append("    { %2d, %2d, %-6s %-28s 0x%03X }," % (x, y, "TRUE," if lm else "FALSE,", m + ",", tile_at((x, y))))
    if not nodes:
        out.append("    {0}")
    out += ["};", "", "static const u32 sOrchidMapComponents_%s[] =" % tag, "{"]
    comps = []
    for s in straits:
        a, b = STRAIT_INFO[s][0]
        comps.append((1 << idx[a]) | (1 << idx[b]))
        out.append("    0x%05X, // %s" % (comps[-1], s))
    land = {c: "land" for c in routes}
    comp = MM.components(land, node_cells)
    comp_ids = {}
    for c in routes:
        touched = frozenset(comp.get(c, set()))
        if touched not in comp_ids:
            comp_ids[touched] = len(straits) + len(comp_ids)
            m = 0
            for s in touched:
                m |= 1 << idx[s]
            comps.append(m)
            out.append("    0x%05X, // %s" % (m, ", ".join(sorted(touched)) or "(no node)"))
    if not straits and not routes:
        out.append("    0")
    out += ["};", "", "static const struct OrchidMapTube sOrchidMapTubes_%s[] =" % tag, "{"]
    n = 0
    for ci, (s, cs) in enumerate(straits.items()):
        for c in cs:
            out.append("    { %2d, %2d, TRUE,  %d, 0x%03X }," % (c[0], c[1], ci, tile_at(c)))
            n += 1
    for c in sorted(routes, key=lambda c: (c[1], c[0])):
        out.append("    { %2d, %2d, FALSE, %d, 0x%03X }," % (c[0], c[1], comp_ids[frozenset(comp.get(c, set()))], tile_at(c)))
        n += 1
    if not n:
        out.append("    {0}")
    out += ["};", "#define ORCHID_V2_NODES_%s %d" % (tag, len(nodes)), "#define ORCHID_V2_TUBES_%s %d" % (tag, n), ""]
    return "\n".join(out), len(nodes), n


def main():
    report = []
    report.append("eon: %d tiles" % export_eon())
    report.append("holon: terrain / dex tiles, terrain / dex colours %s" % (export_holon(),))
    report.append("sinnoh: tiles, cells %s" % (export_sinnoh(),))
    report.append("sevii switch button erased (rm tiles, dex tiles): %s" % erase_sevii_buttons())

    data = json.load(open(SECTIONS))
    entries = {e["id"]: e for e in data["map_sections"]}
    bbox = {}
    frame = frame_tiles()
    n_tosa = len(frame)
    v2 = [GEN, "// Wavebreak Voyages MAP v2 (IMPLEMENTATION §4.7). Structs come from orchid_map_v2.h (Tosa); include that",
          "// first. Tube tiles index graphics/pokenav/region_map/orchid_frame_voyages.png (Tosa's sheet + new tube shapes).",
          "// Empty arrays hold one {0}: use the ORCHID_V2_* counts, not ARRAY_COUNT.", ""]
    strait_c = []
    counts = {}
    for key, cl in S.CLUSTERS.items():
        g = sevii_grid(key, cl)
        hdr = GEN + grid_c("sRegionMapSections_Sevii%s" % key, g)
        open(os.path.join(DATA, "region_map_layout_sevii%s.h" % key), "w").write(hdr)
        secs = C.sections_of(g)
        for s, cs in secs.items():
            xs, ys = [c[0] for c in cs], [c[1] for c in cs]
            bbox[s] = (min(xs), min(ys), max(xs) - min(xs) + 1, max(ys) - min(ys) + 1)
        nodes = [(s, secs[s][0], False) for s in cl["towns"]]
        nodes += [(s, secs[s][0], True) for s in cl["landmarks"] if len(secs.get(s, [])) == 1]
        straits = {}
        for s, (_, cs, _j) in cl["straits"].items():
            sid = STRAIT_IDS[s]
            straits[sid] = list(cs)
            ordered = list(reversed(cs)) if STRAIT_INFO[sid][2] else list(cs)
            strait_c.append((sid, ordered, STRAIT_INFO[sid][1]))
        txt, nn, nt = v2_region("Sevii%s" % key, nodes, straits, frame)
        v2.append(txt)
        counts["Sevii%s" % key] = (nn, nt)
    single_grids = {}
    for tag, places in SINGLES.items():
        g = empty_grid()
        for m, (x, y), _ in places:
            g[y][x] = m
            bbox[m] = (x, y, 1, 1)
        single_grids[tag] = g
        nodes = [(m, c, lm) for m, c, lm in places if lm is not None]
        txt, nn, nt = v2_region(tag.title(), nodes, {}, frame, HOLON_ROUTES if tag == "HOLON" else ())
        v2.append(txt)
        counts[tag.title()] = (nn, nt)
    for s, parent in BORROW.items():
        bbox[s] = bbox[parent]

    # strait cursor cells (C: InitMapBasedOnPlayerLocation special case)
    v2 += ["// L-shaped / long straits: the cursor follows the cell list by progress along the sea route map",
           "struct VoyageStraitCells { mapsec_u16_t mapsec; bool8 diagonal; u8 count; const u8 (*cells)[2]; };", ""]
    for sid, cs, mode in strait_c:
        v2.append("static const u8 sStraitCells_%s[][2] = { %s };" % (
            sid[7:].title().replace("_", ""), ", ".join("{%d, %d}" % c for c in cs)))
    v2 += ["", "static const struct VoyageStraitCells sVoyageStraitCells[] =", "{"]
    for sid, cs, mode in strait_c:
        v2.append("    { %s, %s, %d, sStraitCells_%s }," % (sid, "TRUE" if mode == "d" else "FALSE", len(cs),
                                                         sid[7:].title().replace("_", "")))
    v2 += ["};", ""]
    open(os.path.join(DATA, "orchid_map_v2_voyages.h"), "w").write("\n".join(v2))
    # BG1 frame sheet for the voyage maps = Tosa's sheet + any tube shapes it lacks
    src = Image.open(os.path.join(RM, "orchid_frame.png"))
    sheet = Image.new("P", (128, (len(frame) + 15) // 16 * 8), 0)
    sheet.putpalette(src.getpalette())
    for i, t in enumerate(frame):
        sheet.paste(t, ((i % 16) * 8, (i // 16) * 8))
    sheet.save(os.path.join(RM, "orchid_frame_voyages.png"), transparency=0)
    report.append("orchid_frame_voyages.png: %d tiles (%d new tube shapes)" % (len(frame), len(frame) - n_tosa))

    lay = [GEN]
    for tag, g in single_grids.items():
        lay.append(grid_c("sRegionMapSections_%s" % tag.title(), g))
    open(os.path.join(DATA, "region_map_layout_voyages.h"), "w").write("\n".join(lay))

    # sections json: x/y/w/h for every voyage section we place; the rest of the block stays width 0
    ids = [e["id"] for e in data["map_sections"]]
    block = ids[ids.index("MAPSEC_ONE_ISLAND"):ids.index("MAPSEC_SPECIAL_AREA")] + ["MAPSEC_EON_ISLAND"]
    for s in block:
        e = entries[s]
        if s in bbox:
            x, y, w, h = bbox[s]
            e.update({"x": x, "y": y, "width": w, "height": h})
        else:
            e.pop("x", None)
            e.pop("y", None)
            e.update({"width": 0, "height": 0})
        # keep key order like the other entries: id, name, x, y, width, height
        ordered = {k: e[k] for k in ("id", "name", "x", "y", "width", "height") if k in e}
        e.clear()
        e.update(ordered)
    with open(SECTIONS, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    report.append("MAP v2 (nodes, tube cells): %s" % counts)
    report.append("sections placed: %d" % len(bbox))
    print("\n".join(report))


if __name__ == "__main__":
    main()
