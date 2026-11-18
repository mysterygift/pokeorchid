"""
Tiksi region map (second region, west of Tosa): ROM art + map data from the USER's art
(dev_scripts/orchid_ui/ref/tiksi_terrain.png + tiksi_towns_routes.png, 240x160, NOT rotated) and the
region map tagger's Tiksi tags (dev_scripts/region_map_tagger/tags_tiksi.json, `server.py 8766 --region tiksi`).

Tiksi reuses the vanilla Kanto/Sevii map sections (the block from the old MAPSEC_PALLET_TOWN up to
MAPSEC_SPECIAL_AREA): Orchid has no Kanto, map sections are a u8 with ~25 free values left, and that block
is what GetRegionForSectionId() maps to REGION_TIKSI. Tagged sections are renamed in place (enum slot
kept); their old ids live on in include/constants/region_map_section_aliases.h (shared with the Tosa
exporter, cumulative). Tosa's pipeline (export_region_map.py) leaves the block alone.

Same grid as Tosa: cursor cell (x, y) of the 28x15 grid = 8x8 px at (8 + 8x, 16 + 8y).

Writes:
  graphics/pokenav/region_map/map_tiksi.png / .pal / .bin   terrain (affine 8bpp, 64x64 map), MAP v2
  graphics/pokedex/region_map_tiksi.png / .pal / .bin       dex AREA copy (routes + markers baked in)
  graphics/pokenav/region_map/orchid_frame_tiksi.png        BG1 sheet: frame tiles (same as orchid_frame.png,
                                                            so orchid_frame*.bin are shared) + Tiksi tubes
  graphics/pokenav/region_map/orchid_switch_hint.png        phone MAP header hint: R = switch region
  src/data/region_map/region_map_layout_tiksi.h             sRegionMapSections_Tiksi cursor grid
  src/data/region_map/orchid_map_v2_tiksi.h                 Tiksi nodes / tubes / route components
  src/data/region_map/region_map_sections.json              Kanto-block entries only
  include/constants/region_map_section_aliases.h            + old ids of renamed Tiksi sections
  data/maps/*/map.json                                      maps assigned to Tiksi sections (Maps tab)
  dev_scripts/orchid_ui/ref/tiksi_places.md                 place table
then rebases tags_tiksi.json (keys = current ids, Tiksi areas only) so the tagger shows no pending changes.

usage: export_region_map_tiksi.py
"""
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from PIL import Image
import export_region_map as T          # Tosa exporter: tile / palette helpers
import export_map_v2 as V2             # MAP v2: frame + tube helpers
import mock_map as MM
import region_tags as RT
from kit import to_tiles, tiles_to_image
import dex_ext as D

ROOT = T.ROOT
P = T.P
REF = T.REF
W, H, GX, GY = T.W, T.H, T.GX, T.GY
RED = (255, 0, 0)
TERRAIN = "tiksi_terrain.png"
ROUTES = "tiksi_towns_routes.png"
TAGS = os.path.join(ROOT, "dev_scripts", "region_map_tagger", "tags_tiksi.json")
SECTIONS = P("src", "data", "region_map", "region_map_sections.json")
ALIASES = P("include", "constants", "region_map_section_aliases.h")
# where the cursor goes when the player's section has no cell on the Tiksi map (C: GetRegionMapFallbackMapSec)
FALLBACK = "MAPSEC_FURONG_VILLAGE"


def load(name):
    return Image.open(os.path.join(REF, name)).convert("RGB")


def classify():
    """{cell: 'land'|'sea'} from the user's route art (mock_map.classify, unrotated)."""
    rt = load(ROUTES).load()
    cells = {}
    for cy in range(15):
        for cx in range(28):
            x0, y0 = GX + cx * 8, GY + cy * 8
            land = sea = 0
            for j in range(8):
                for i in range(8):
                    p = rt[x0 + i, y0 + j]
                    if p[0] > 200 and p[2] < 130 and p != RED:
                        land += 1
                    elif p == (72, 152, 224):
                        sea += 1
            if land >= 12:
                cells[(cx, cy)] = "land"
            elif sea >= 12:
                cells[(cx, cy)] = "sea"
    return cells


def kanto_block(ids):
    """[start, end) indices of the Kanto/Sevii block in the sections list (start may be renamed)."""
    start = RT.resolve_alias("MAPSEC_PALLET_TOWN")
    return ids.index(start), ids.index("MAPSEC_SPECIAL_AREA")


def load_tags():
    tags = RT.Tags(TAGS, region="tiksi")
    for a in tags.areas:
        assert '"' not in a.name and len(a.name) <= 16, a.name    # MAP_NAME_LENGTH
    return tags


def map_art(nodes):
    im = load(ROUTES)
    px = im.load()
    for _, (cx, cy), lm in nodes:
        t = T.landmark_tile() if lm else T.city_tile()
        x0, y0 = GX + cx * 8, GY + cy * 8
        for y in range(8):
            for x in range(8):
                px[x0 + x, y0 + y] = t[y][x]
    return im


def write_terrain():
    ttiles, tcells = T.build_tiles(load(TERRAIN))
    assert len(ttiles) <= 256, len(ttiles)
    tcols = T.palette_of(ttiles)
    T.write_png8(P("graphics", "pokenav", "region_map", "map_tiksi.png"), ttiles, tcols)
    T.write_jasc48(P("graphics", "pokenav", "region_map", "map_tiksi.pal"), tcols)
    amap = bytearray(64 * 64)
    for i, t in enumerate(tcells):
        amap[(i // 30) * 64 + i % 30] = t
    open(P("graphics", "pokenav", "region_map", "map_tiksi.bin"), "wb").write(bytes(amap))
    return len(ttiles)


def write_dex(nodes):
    tiles, cells = T.build_tiles(map_art(nodes))
    assert len(tiles) <= 256, len(tiles)
    cols = T.palette_of(tiles)
    T.write_png8(P("graphics", "pokedex", "region_map_tiksi.png"), tiles, cols)
    T.write_jasc48(P("graphics", "pokedex", "region_map_tiksi.pal"), cols)
    tmap = bytearray()
    for y in range(32):
        for x in range(32):
            tmap += struct.pack("<H", cells[y * 30 + x] if (x < 30 and y < 20) else 0)
    open(P("graphics", "pokedex", "region_map_tiksi.bin"), "wb").write(bytes(tmap))
    return len(tiles)


def update_sections(tags):
    """Kanto-block entries only: tagged areas renamed / named / placed, the rest off every grid."""
    data = json.load(open(SECTIONS))
    secs = data["map_sections"]
    k0, k1 = kanto_block([s["id"] for s in secs])
    by_id = {a.original_id: a for a in tags.areas if a.original_id}
    by_id.update({a.id: a for a in tags.areas})
    # areas added in the tagger take the next free Kanto slot (no tagged area, no map pointing at it); the
    # slot's old id becomes an alias like any rename (vanilla Kanto tables still reference it)
    used_by_maps = set()
    for folder in os.listdir(P("data", "maps")):
        mj = P("data", "maps", folder, "map.json")
        if os.path.isfile(mj):
            used_by_maps.add(json.load(open(mj)).get("region_map_section"))
    free = [secs[i]["id"] for i in range(k0, k1) if secs[i]["id"] not in by_id and secs[i]["id"] not in used_by_maps]
    for a in tags.areas:
        if a.original_id is None and a.cells and a.id not in by_id:
            assert free, "no free Kanto/Sevii slot left for " + a.id
            a.original_id = free.pop(0)
            by_id[a.original_id] = a
    for i in range(k0, k1):
        s = secs[i]
        a = by_id.get(s["id"])
        for k in ("x", "y", "width", "height"):
            s.pop(k, None)
        if a is not None:
            s["id"], s["name"] = a.id, a.name
        if a is not None and a.cells:
            x, y, w, h = a.bbox
            s.update(x=x, y=y, width=w, height=h)
        else:
            s.update(width=0, height=0)
    with open(SECTIONS, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    return [s["id"] for s in secs]


def write_aliases(tags):
    """Add Tiksi renames to the shared alias header (same format / rules as export_region_map.write_aliases)."""
    head, aliases = [], {}
    for line in open(ALIASES):
        parts = line.split()
        if len(parts) == 3 and parts[0] == "#define" and parts[1].startswith("MAPSEC_"):
            aliases[parts[1]] = parts[2]
    renames = tags.renames()
    for old, new in list(aliases.items()):         # chains: A -> B, then B renamed to C => A -> C
        aliases[old] = renames.get(new, new)
    aliases.update(renames)
    current = {a.id for a in tags.areas}
    L = ["// GENERATED by dev_scripts/orchid_ui/export_region_map.py from the region map tagger - do not edit.",
         "// Renamed map sections keep their enum slot; their old names point at the new ones.",
         "#ifndef GUARD_CONSTANTS_REGION_MAP_SECTION_ALIASES_H",
         "#define GUARD_CONSTANTS_REGION_MAP_SECTION_ALIASES_H", ""]
    for old, new in sorted(aliases.items()):
        if old not in current:
            L.append("#define %-36s %s" % (old, new))
    L += ["", "#endif // GUARD_CONSTANTS_REGION_MAP_SECTION_ALIASES_H"]
    open(ALIASES, "w").write("\n".join(L) + "\n")


def write_layout(tags):
    L = ["// GENERATED by dev_scripts/orchid_ui/export_region_map_tiksi.py from the region map tagger (tags_tiksi.json).",
         "static const mapsec_u8_t sRegionMapSections_Tiksi[MAP_HEIGHT][MAP_WIDTH] = {"]
    for row in tags.grid:
        L.append("    {" + ", ".join(row) + "},")
    L.append("};")
    open(P("src", "data", "region_map", "region_map_layout_tiksi.h"), "w").write("\n".join(L) + "\n")


def write_v2(nodes, cells):
    """Frame tiles (identical to orchid_frame.png's first ORCHID_MAP_FRAME_TILES) + Tiksi tubes.
    nodes = [(area, cell, is_landmark)], cells = {cell: 'land'|'sea'} tube cells (nodes excluded)."""
    node_cells = {a.id: c for a, c, _ in nodes}
    fr_map, fr_fly = V2.frame_image(False), V2.frame_image(True)
    tiles, _ = to_tiles(fr_map)
    tiles, _ = to_tiles(fr_fly, base=tiles)
    n_frame = len(tiles)
    timg = V2.tube_image(V2.tube_mask(cells, node_cells))
    timg.putpalette(fr_map.getpalette())
    tiles, tm_tube = to_tiles(timg, base=tiles)
    assert len(tiles) <= 512, len(tiles)
    sheet = tiles_to_image(tiles, fr_map)
    pal = D.dex_palette("leaf")
    flat = [c for rgb in pal for c in rgb]
    sheet.putpalette(flat + [0] * (768 - len(flat)))
    sheet.save(V2.RM("orchid_frame_tiksi.png"), transparency=0)

    tile_at = lambda cx, cy: (lambda t: t[0] | (t[1] << 10) | (t[2] << 11))(tm_tube[(GY // 8 + cy) * 30 + GX // 8 + cx])
    order = [a.id for a, _, _ in nodes]
    comp = MM.components(cells, node_cells)
    comp_ids, comp_masks, tube_cells = {}, [], []
    for (cx, cy), kind in sorted(cells.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        touched = frozenset(comp.get((cx, cy), set()))
        if touched not in comp_ids:
            comp_ids[touched] = len(comp_masks)
            comp_masks.append(touched)
        tube_cells.append((cx, cy, tile_at(cx, cy), kind == "sea", comp_ids[touched]))
    L = ["// GENERATED by dev_scripts/orchid_ui/export_region_map_tiksi.py (MAP v2, Tiksi) - do not edit.",
         "// Structs + ORCHID_MAP_FRAME_TILES come from orchid_map_v2.h (Tosa); include that first.",
         "// Tube tiles index graphics/pokenav/region_map/orchid_frame_tiksi.png.",
         "STATIC_ASSERT(ORCHID_MAP_FRAME_TILES == %d, TiksiFrameTilesMatchTosa);" % n_frame, "",
         "static const struct OrchidMapNode sOrchidMapNodes_Tiksi[] =", "{"]
    for a, (cx, cy), lm in nodes:
        L.append("    { %2d, %2d, %-6s %-27s 0x%03X }, // %s" % (cx, cy, "TRUE," if lm else "FALSE,", a.id + ",",
                                                               tile_at(cx, cy), a.name))
    L += ["};", "", "// bit i = sOrchidMapNodes_Tiksi[i]; a route is gold once every node it touches is visited",
          "static const u32 sOrchidMapComponents_Tiksi[] =", "{"]
    names = {a.id: a.name for a, _, _ in nodes}
    for touched in comp_masks:
        m = 0
        for n in touched:
            m |= 1 << order.index(n)
        L.append("    0x%05X, // %s" % (m, ", ".join(names[n] for n in sorted(touched, key=order.index)) or "(no node)"))
    L += ["};", "", "static const struct OrchidMapTube sOrchidMapTubes_Tiksi[] =", "{"]
    for cx, cy, t, sea, ci in tube_cells:
        L.append("    { %2d, %2d, %-6s %2d, 0x%03X }," % (cx, cy, "TRUE," if sea else "FALSE,", ci, t))
    L.append("};")
    open(P("src", "data", "region_map", "orchid_map_v2_tiksi.h"), "w").write("\n".join(L) + "\n")
    return n_frame, len(tiles), len(tube_cells)


SWITCH_MAP = ["KKKK..KKKK",      # tri-fold map, middle panel dropped 1 px (FRLG-style map-switch idea)
              "KWWKKKKWWK",
              "KWWKGGKWWK",
              "KWWKGDKWWK",
              "KWWKDGKWWK",
              "KWWKGGKWWK",
              "KKKKGGKKKK",
              "...KKKK..."]
SWITCH_ARROWS = ["...K.",
                 "KKKKK",
                 "...K.",
                 ".....",
                 ".K...",
                 "KKKKK",
                 ".K..."]


def write_switch_hint():
    """40x8 header hint for the phone MAP's region switch: Ⓡ keypad glyph + folded map + swap arrows,
    in the frame's kit palette (BG pal 1), blitted into the header window (RegionMap_BlitOrchidSwitchHint)."""
    import kit
    import system_ext as X
    from kit import Canvas, stamp, INK, WHITE, ACCENT_LIGHT, ACCENT_DARK
    im = kit.new_sheet(40, 8, "leaf")
    cv = Canvas(im)
    X.keypad(cv, 0, 0, "R")
    stamp(cv, 18, 0, SWITCH_MAP, {"K": INK, "W": WHITE, "G": ACCENT_LIGHT, "D": ACCENT_DARK})
    stamp(cv, 30, 0, SWITCH_ARROWS, {"K": WHITE})
    pal = D.dex_palette("leaf")
    flat = [c for rgb in pal for c in rgb]
    im.putpalette(flat + [0] * (768 - len(flat)))
    im.save(V2.RM("orchid_switch_hint.png"), transparency=0)


def write_places_md(tags, nodes):
    node_ids = {a.id for a, _, _ in nodes}
    L = ["# Tiksi region map places", "",
         "Generated by `dev_scripts/orchid_ui/export_region_map_tiksi.py` from the region map tagger",
         "(`dev_scripts/region_map_tagger/tags_tiksi.json`) and the user's art (`ref/tiksi_*.png`, not rotated).",
         "Tiksi reuses the vanilla Kanto/Sevii map sections; old ids are aliases in",
         "`include/constants/region_map_section_aliases.h`. Cells are on the 28x15 cursor grid.", "",
         "| Section | Name | Kind | Map node | Cells | Notes |", "|---|---|---|---|---|---|"]
    for a in tags.placed():
        x, y, w, h = a.bbox
        L.append("| `%s` | %s | %s | %s | %d at (%d,%d) %dx%d | %s |" % (
            a.id, a.name, a.kind, "yes" if a.id in node_ids else "-", len(a.cells), x, y, w, h,
            a.notes.replace("|", "/").replace("\n", " ")))
    open(os.path.join(REF, "tiksi_places.md"), "w").write("\n".join(L) + "\n")


def rebase(section_ids):
    """tags_tiksi.json: keys / originalIds = current ids, and only the Kanto-block (Tiksi) areas; the
    tagger re-adds every other section from the repo on load."""
    d = json.load(open(TAGS))
    d["areas"] = [a for a in d["areas"] if a.get("kanto")]
    with open(TAGS, "w") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write("\n")
    RT.rebase(TAGS, section_ids=set(section_ids))


def export():
    tags = load_tags()
    nodes = tags.nodes()
    node_cells = {c for _, c, _ in nodes}
    art = classify()
    cells = {c: art.get(c, "land") for a in tags.placed() for c in a.cells if c not in node_cells}
    nt, nd = write_terrain(), write_dex(nodes)
    print("terrain tiles", nt, "dex tiles", nd)
    src = open(P("src", "region_map.c")).read()      # INCGFX -num_tiles must match (sheets pad to 16/row)
    for png, n in (("map_tiksi.png", nt), ("region_map_tiksi.png", nd)):
        if '%s", ".8bpp.smol", "-num_tiles %d ' % (png, n) not in src:
            print("!! update src/region_map.c: %s needs \"-num_tiles %d\"" % (png, n))
    print("v2 (frame tiles, all tiles, tube cells)", write_v2(nodes, cells))
    write_switch_hint()
    ids = update_sections(tags)
    assert FALLBACK in ids, FALLBACK
    write_layout(tags)
    write_aliases(tags)
    changed = T.update_map_jsons(tags)
    write_places_md(tags, nodes)
    rebase(ids)
    print("nodes", [(a.name, c, "landmark" if lm else "town") for a, c, lm in nodes])
    print("renames", tags.renames())
    print("map.json changes", changed)


if __name__ == "__main__":
    export()
