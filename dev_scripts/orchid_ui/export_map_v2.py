"""
MAP v2 (approved 2026-11-17, mock_map.py): Tosa Rail line-map look for the Town Map / Fly map / Rotom
Phone MAP app. Called from export_region_map.py (which owns the terrain art and section data).

Writes:
  graphics/pokenav/region_map/orchid_frame.png    BG1 tiles: frame (header + tray) + route tube tiles
  graphics/pokenav/region_map/orchid_frame.bin    BG1 map: frame with the MAP pictogram (tube cells added in C)
  graphics/pokenav/region_map/orchid_frame_fly.bin  same with the FLY pictogram
  graphics/pokenav/region_map/orchid_frame.pal    64 colours: pal 1 = kit "map" (leaf) theme for frame + text,
                                                  then tube palettes gold / grey / sea (BG pals 4-6 in C)
  graphics/pokenav/region_map/orchid_nodes.png    OBJ 16x16 x 4: town, town (unvisited), landmark, landmark (unv.)
  graphics/pokenav/region_map/cursor_small.png    OBJ 16x16 x 2: gold ring cursor (both frames the same)
  graphics/pokenav/region_map/cursor.pal          OBJ palette shared by nodes, ring and rail chip
  graphics/pokenav/region_map/orchid_rail_chip.png  OBJ 32x16: tray chip with the rail pictogram
  graphics/pokenav/region_map/orchid_keypad_a.png 8x8 Ⓐ keypad glyph in kit colours (blitted into the tray)
  src/data/region_map/orchid_map_v2.h             nodes, tube cells, route components
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from PIL import Image
import kit
from kit import (Canvas, rounded_box, disc, ring, stamp, to_tiles, tiles_to_image, write_tilemap, write_jasc,
                 snap, INK, INK_SOFT, WHITE, PANEL, PANEL_SHADE, PANEL_DARK, ACCENT_DARK, ACCENT, ACCENT_LIGHT,
                 SELECT, SELECT_DARK, SELECT_LIGHT)
import dex_ext as D
import system_ext as X
import mock_map as MM

ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
P = lambda *p: os.path.join(ROOT, *p)
RM = lambda *p: P("graphics", "pokenav", "region_map", *p)
W, H = 240, 160
GX, GY = MM.GX, MM.GY

# tube palette indices (each tube palette: 1 ink, 2 light, 3 face, 4 dark)
T_INK, T_LT, T_FC, T_DK = 1, 2, 3, 4
TUBE_PALS = [MM.ROUTE_C, MM.GREY_C, MM.SEA_C]     # C: TUBE_PAL_GOLD / GREY / SEA


def pad16(p):
    return [snap(c) for c in p] + [(0, 0, 0)] * (16 - len(p))


def mapsec_of(n):
    if n == 4:
        return "MAPSEC_TOSA_PORT"
    if n == 10:
        return "MAPSEC_OLDALE_TOWN"
    return "MAPSEC_TOSA_PH_%02d" % n


# ---------------------------------------------------------------- tubes
def tube_mask(cells, nodes):
    """mock_map.tube_layer's mask, for all route cells as one group (colour is per cell in C)."""
    allc = set(cells) | set(nodes.values())
    mask = set()
    for (cx, cy) in cells:
        x0, y0 = GX + cx * 8, GY + cy * 8
        for j in range(1, 7):
            for i in range(1, 7):
                mask.add((x0 + i, y0 + j))
        for d in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            n = (cx + d[0], cy + d[1])
            if n in allc:
                for j in range(1, 7):
                    for k in (7, 8) if d[0] > 0 or d[1] > 0 else (0, -1):
                        if d[0]:
                            mask.add((x0 + k, y0 + j))
                        else:
                            mask.add((x0 + j, y0 + k))
    return mask


def tube_image(mask):
    im = Image.new("P", (W, H), 0)
    px = im.load()
    for (x, y) in mask:
        if not (MM.MAP_Y0 <= y <= MM.MAP_Y1 and 0 <= x < W):
            continue
        edge = any((x + a, y + b) not in mask for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        if edge:
            c = T_INK
        elif (x - 1, y) not in mask or (x, y - 1) not in mask or (x - 1, y - 1) not in mask:
            c = T_LT
        elif (x + 1, y) not in mask or (x, y + 1) not in mask or (x + 1, y + 1) not in mask:
            c = T_DK
        else:
            c = T_FC
        px[x, y] = c
    return im


# ---------------------------------------------------------------- frame
def frame_image(fly):
    im = kit.new_sheet(W, H, "leaf")
    cv = Canvas(im)
    D.header_band(cv, 0, W - 1, round_left=False)
    rounded_box(cv, 4, 2, 14, 12, 3, ACCENT_LIGHT, INK, WHITE, ACCENT)
    X.centred_sil(cv, 5, 3, 13, 10, "fly" if fly else "map", ACCENT_DARK, None)
    D.tray(cv, 136, seam=False)
    return im


def export(sq, cells, info=None):
    """sq = {node key: (cx, cy)}, cells = {(cx, cy): 'land'|'sea'} route cells (nodes excluded).
    info = {node key: (mapsec, is_landmark, label)} in node order (region_tags.Tags.nodes); without it,
    keys are the user's square numbers and mapsec_of / MM.LANDMARKS decide (the pre-tagger behaviour)."""
    os.makedirs(RM(), exist_ok=True)
    nodes = dict(sq)
    if info is None:
        info = {n: (mapsec_of(n), n in MM.LANDMARKS, "#%d" % n) for n in sorted(nodes)}
    assert len(info) <= 32, "sOrchidMapComponents is a u32 bitmask: at most 32 nodes"
    # ---- tiles: frame (map), frame (fly), then tubes
    fr_map, fr_fly = frame_image(False), frame_image(True)
    tiles, tm_map = to_tiles(fr_map)
    tiles, tm_fly = to_tiles(fr_fly, base=tiles)
    n_frame = len(tiles)
    timg = tube_image(tube_mask(cells, nodes))
    timg.putpalette(fr_map.getpalette())
    tiles, tm_tube = to_tiles(timg, base=tiles)
    assert len(tiles) <= 512, len(tiles)
    sheet = tiles_to_image(tiles, fr_map)
    pal = D.dex_palette("leaf")
    flat = [c for rgb in pal for c in rgb]
    sheet.putpalette(flat + [0] * (768 - len(flat)))
    sheet.save(RM("orchid_frame.png"), transparency=0)
    for name, tm in (("orchid_frame.bin", tm_map), ("orchid_frame_fly.bin", tm_fly)):
        out = [None] * (32 * 32)
        for i, item in enumerate(tm):
            cy, cx = divmod(i, 30)
            if 2 <= cy <= 16:          # tube rows: filled in by C
                continue
            out[cy * 32 + cx] = item
        write_tilemap(RM(name), out, pal_num=1)
    tube_pals = []
    for dk, fc, lt in TUBE_PALS:
        tube_pals += pad16([(0, 0, 0), (40, 40, 64), lt, fc, dk])
    write_jasc(RM("orchid_frame.pal"), pad16(pal) + tube_pals)

    # ---- components (mock_map.components): route cell -> set of node numbers it connects
    comp = MM.components(cells, nodes)
    comp_ids, comp_masks = {}, []
    tube_cells = []
    node_at = {v: k for k, v in nodes.items()}
    for (cx, cy), kind in sorted(cells.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        touched = frozenset(comp.get((cx, cy), set()))
        if touched not in comp_ids:
            comp_ids[touched] = len(comp_masks)
            comp_masks.append(touched)
        idx, hf, vf = tm_tube[(GY // 8 + cy) * 30 + GX // 8 + cx]
        tube_cells.append((cx, cy, idx | (hf << 10) | (vf << 11), kind == "sea", comp_ids[touched]))
    node_cells = []
    for n in info:
        cx, cy = nodes[n]
        idx, hf, vf = tm_tube[(GY // 8 + cy) * 30 + GX // 8 + cx]
        node_cells.append((n, cx, cy, idx | (hf << 10) | (vf << 11)))

    # ---- sprites
    spal = [(0, 0, 0), (40, 40, 64), (248, 248, 248), (192, 192, 184), (144, 144, 152),
            kit.palette()[SELECT], kit.palette()[SELECT_DARK], kit.palette()[SELECT_LIGHT]]
    leaf = kit.palette("leaf")
    spal += [leaf[ACCENT_DARK], leaf[ACCENT], leaf[ACCENT_LIGHT]]
    S_INK, S_WHITE, S_SHADE, S_DARK, S_SEL, S_SEL_DK, S_SEL_LT, S_ACC_DK, S_ACC, S_ACC_LT = range(1, 11)
    write_jasc(RM("cursor.pal"), pad16(spal))

    def save(im, path):
        flat = [c for rgb in pad16(spal) for c in rgb]
        im.putpalette(flat + [0] * (768 - len(flat)))
        im.save(path, transparency=0)

    im = Image.new("P", (16, 64), 0)
    cv = Canvas(im)
    for f, (lm, vis) in enumerate(((False, True), (False, False), (True, True), (True, False))):
        x, y = 7.5, f * 16 + 7.5          # cell (3.5, 3.5) with the sprite's top-left at cell - 4
        if lm:
            rows = (["...k...", "..kwk..", ".kwwwk.", "kwwwwwk", ".kwwws.", "..kss..", "...k..."] if vis else
                    ["...k...", "..kmk..", ".kmmmk.", "kmmmmmk", ".kmmmk.", "..kmk..", "...k..."])
            stamp(cv, int(x) - 3, int(y) - 3, rows, {"k": S_INK, "w": S_WHITE, "s": S_SHADE, "m": S_DARK})
        else:
            disc(cv, x, y, 4.6, S_WHITE if vis else S_DARK, S_INK)
            if vis:
                cv.set(int(x) + 1, int(y) + 1, S_SHADE)
                cv.set(int(x) + 2, int(y), S_SHADE)
    save(im, RM("orchid_nodes.png"))

    im = Image.new("P", (16, 32), 0)
    cv = Canvas(im)
    for f in range(2):
        ring(cv, 7.5, f * 16 + 7.5, 7.2, S_INK, 1.0)
        ring(cv, 7.5, f * 16 + 7.5, 6.2, S_SEL, 1.2)
        ring(cv, 7.5, f * 16 + 7.5, 5.2, S_SEL_DK, 0.6)
    save(im, RM("cursor_small.png"))

    im = Image.new("P", (32, 16), 0)
    cv = Canvas(im)
    rounded_box(cv, 0, 0, 18, 14, 3, S_ACC, S_INK, S_ACC_LT, S_ACC_DK)
    X.centred_sil(cv, 1, 1, 17, 12, "rail", S_WHITE, S_ACC_DK)
    save(im, RM("orchid_rail_chip.png"))

    im = kit.new_sheet(8, 8, "leaf")
    X.keypad(Canvas(im), 0, 0, "A")        # face WHITE, edge INK (kit roles of the frame palette)
    im.putpalette(flat + [0] * (768 - len(flat)))
    im.save(RM("orchid_keypad_a.png"), transparency=0)

    # ---- C data
    L = ["// GENERATED by dev_scripts/orchid_ui/export_map_v2.py (MAP v2, mock_map.py) - do not edit.",
         "// Tube cells / node cells are on the 28x15 cursor grid (screen tile = cell + (1, 2)).",
         "#define ORCHID_MAP_FRAME_TILES %d" % n_frame, "",
         "struct OrchidMapNode { u8 x, y; bool8 landmark; mapsec_u16_t mapsec; u16 tube; };",
         "struct OrchidMapTube { u8 x, y; bool8 sea; u8 component; u16 tile; };", "",
         "static const struct OrchidMapNode sOrchidMapNodes[] =", "{"]
    for n, cx, cy, t in node_cells:
        mapsec, landmark, label = info[n]
        L.append("    { %2d, %2d, %-6s %-31s 0x%03X }, // %s" % (cx, cy, "TRUE," if landmark else "FALSE,",
                                                                 mapsec + ",", t, label))
    L += ["};", "", "// bit i = sOrchidMapNodes[i]; a route is gold once every node it touches is visited",
          "static const u32 sOrchidMapComponents[] =", "{"]
    order = [n for n, _, _, _ in node_cells]
    for touched in comp_masks:
        m = 0
        for n in touched:
            m |= 1 << order.index(n)
        L.append("    0x%08X, // %s" % (m, ", ".join(info[n][2] for n in order if n in touched) or "(no node)"))
    L += ["};", "", "static const struct OrchidMapTube sOrchidMapTubes[] =", "{"]
    for cx, cy, t, sea, ci in tube_cells:
        L.append("    { %2d, %2d, %-6s %2d, 0x%03X }," % (cx, cy, "TRUE," if sea else "FALSE,", ci, t))
    L.append("};")
    open(P("src", "data", "region_map", "orchid_map_v2.h"), "w").write("\n".join(L) + "\n")
    return n_frame, len(tiles), len(tube_cells), len(comp_masks)
