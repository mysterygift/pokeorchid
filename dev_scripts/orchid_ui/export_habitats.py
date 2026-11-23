"""
Export the Orchid Pokédex HABITATS view (mock_habitats.py) to game assets.

Writes (repo root):
  graphics/pokedex/orchid/habitats_map.png   tile sheet: map-screen frame (pal 0/1) + zone overlay tiles (pal 3)
  graphics/pokedex/orchid/habitats_map_tosa1.bin / _tosa2.bin / _tiksi2.bin
                                             BG1 frame tilemaps: Tosa alone / Tosa with tabs / Tiksi with tabs
  graphics/pokedex/orchid/habitats_route.png route page art sheet (tiles 1-4 = the dex grid) + habitats_route.bin
  graphics/pokedex/orchid/habitats_overlay.pal  BG palette 3 of the map screen (dim / rim / glow)
  graphics/pokedex/orchid/hab_*.png          bitmaps blitted into text windows (wells, chips, pictograms, badges…)
  src/data/pokedex_habitats.h                layout constants, zone names, per-region habitat tables
                                             (section, zone, node cell, cells) and the per-cell zone grid

Habitat zones come from the region map tagger: each area's "habitat" field in
dev_scripts/region_map_tagger/tags.json (NORTH / EAST / SOUTH / WEST; Tiksi areas are one zone).
The first run seeds missing fields from mock_habitats.ZONE_OF; after that the tagger is the source.

The species on each habitat are NOT exported: the ROM reads them from gWildMonHeaders at runtime, so
the view always matches src/data/wild_encounters.json.

usage: export_habitats.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from PIL import Image
from kit import *
import kit as K
import dex_ext as D
import mock_habitats as MH
import region_tags as RT
import export_region_map as EM
import export_region_map_tiksi as ET
import export_dex as XD

ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
P = lambda *p: os.path.join(ROOT, *p)
OUT = P("graphics", "pokedex", "orchid")
W, H = 240, 160
ZONES = ["NORTH", "EAST", "SOUTH", "WEST"]           # zone ids 1-4 (0 = none / sea)
OVERLAY_PAL = 3
# overlay palette colours: 1 dim, 2 rim gold, 3 route edge (dark gold), 4 glow
OVERLAY_COLS = [(0, 0, 0), (16, 16, 32), K._NEUTRAL[SELECT], K._NEUTRAL[SELECT_DARK], K._NEUTRAL[SELECT_LIGHT]]


# ------------------------------------------------------------------ zones in the tagger
def seed_tag_zones():
    """Add "habitat" to every Tosa area of tags.json that lacks one (from mock_habitats.ZONE_OF)."""
    d = json.load(open(RT.TAGS))
    changed = 0
    for a in d["areas"]:
        if a.get("kanto"):
            continue
        if "habitat" not in a and a["id"] in MH.ZONE_OF:
            a["habitat"] = MH.ZONE_OF[a["id"]]
            changed += 1
    if changed:
        with open(RT.TAGS, "w") as f:
            json.dump(d, f, indent=2, ensure_ascii=False)
            f.write("\n")
    return {a["id"]: a.get("habitat") for a in d["areas"]}


# ------------------------------------------------------------------ art
def sheet():
    return MH.new_sheet(W, H, "orchid", spare_a=D.BALL_RED)


def overlay_tiles():
    """Tile list (tuples of 64 palette-3 indices): 0 empty, 1 dim, 2-17 rim[mask], 18-33 glow[mask].
    mask bits: 1 = N edge, 2 = E, 4 = S, 8 = W."""
    def tile(fill, edge_c, mask):
        px = [[fill] * 8 for _ in range(8)]
        for i in range(8):
            if mask & 1: px[0][i] = edge_c
            if mask & 2: px[i][7] = edge_c
            if mask & 4: px[7][i] = edge_c
            if mask & 8: px[i][0] = edge_c
        return tuple(v for row in px for v in row)
    tiles = [tuple([0] * 64), tuple([1] * 64)]
    tiles += [tile(0, 2, m) for m in range(16)]
    tiles += [tile(4, 3, m) for m in range(16)]
    return tiles


def export_map_sheet():
    pal = D.dex_palette("orchid")
    frames = {}
    for key, region, n in (("tosa1", "tosa", 1), ("tosa2", "tosa", 2), ("tiksi2", "tiksi", 2)):
        im = sheet()
        MH.draw_map_frame(Canvas(im), region, n)
        frames[key] = im
    tiles, tms = [tuple([0] * 64)], {}
    for key, im in frames.items():
        tiles, tm = to_tiles(im, base=tiles)
        tms[key] = tm
    n_frame = len(tiles)
    ov = overlay_tiles()
    sheet_tiles = list(tiles) + ov
    img = tiles_to_image(sheet_tiles, frames["tosa1"])
    XD.save_indexed(img, os.path.join(OUT, "habitats_map.png"), pal)
    for key, tm in tms.items():
        write_tilemap(os.path.join(OUT, "habitats_map_%s.bin" % key), XD.cells(tm))
    write_jasc(os.path.join(OUT, "habitats_overlay.pal"), OVERLAY_COLS + [(0, 0, 0)] * (16 - len(OVERLAY_COLS)))
    assert len(sheet_tiles) <= 512, len(sheet_tiles)
    return n_frame, len(sheet_tiles)


def export_route_sheet():
    pal = D.dex_palette("orchid")
    im = sheet()
    cv = Canvas(im)
    D.header_band(cv, 0, W - 1, round_left=False)
    D.tray(cv, MH.TRAY_Y)
    tiles, tm = to_tiles(im, base=XD.BASE)
    XD.save_indexed(tiles_to_image(tiles, im), os.path.join(OUT, "habitats_route.png"), pal)
    write_tilemap(os.path.join(OUT, "habitats_route.bin"), XD.cells(tm))
    return len(tiles)


def bitmap(name, w, h, fn):
    """Draw fn(Canvas) on a w x h kit sheet (w, h multiples of 8) and save it for INCGFX .4bpp."""
    im = MH.new_sheet(w, h, "orchid", spare_a=D.BALL_RED)
    fn(Canvas(im))
    XD.save_indexed(im, os.path.join(OUT, "hab_%s.png" % name), D.dex_palette("orchid"))


def export_bitmaps():
    sw, sh = MH.SLOT_W, MH.WELL_H
    bitmap("well", 40, 24, lambda c: D.well(c, 0, 0, sw, sh))
    bitmap("well_sel", 40, 24, lambda c: rounded_box(c, 0, 0, sw, sh, 3, SELECT, INK, SELECT_LIGHT, SELECT_DARK))
    bitmap("chip", 24, 24, lambda c: rounded_box(c, 0, 0, MH.CHIP_W, sh, 3, ACCENT, INK, ACCENT_LIGHT, ACCENT_DARK))
    for m, key in (("land_mons", "grass"), ("water_mons", "surf"), ("rock_smash_mons", "rock"), ("fishing_mons", "fish")):
        bitmap("p_" + key, 16, 16, lambda c, m=m: MH.stamp_rows(c, 0, 0, MH.PICTO[m], {"#": WHITE}))
        bitmap("ps_" + key, 16, 16, lambda c, m=m: MH.stamp_rows(c, 0, 0, MH.PICTO[m], {"#": INK_SOFT}))
    bitmap("ball_grey", 8, 8, lambda c: MH.grey_ball(c, 0, 0))
    bitmap("ball", 8, 8, lambda c: D.caught_ball(c, 0, 0))
    # map badge OBJ sheet: frame 0 grey ball (every species captured), 1 colour (all catalogued), 2 Palm's clipboard
    clip = ["..kkk..", "kkwwwkk", "kwkkkwk", "kwwwwwk", "kwkkkwk", "kwwwwwk", "kwkkwwk", "kkkkkkk"]
    bitmap("badges", 8, 24, lambda c: (MH.grey_ball(c, 0, 0), D.caught_ball(c, 0, 8),
                                        MH.stamp_rows(c, 0, 16, clip, {"k": INK, "w": SELECT_LIGHT})))
    bitmap("clip", 8, 8, lambda c: MH.stamp_rows(c, 0, 0, clip, {"k": INK, "w": SELECT_LIGHT}))
    # locked wells / chips, rare "?" (round 4, user 2026-11-23)
    bitmap("well_lock", 40, 24, lambda c: (rounded_box(c, 0, 0, sw, sh, 3, PANEL_DARK, INK, PANEL_SHADE, PANEL_DARK),
                                           MH.stamp_rows(c, sw // 2 - 2, sh // 2 - 3, MH.LOCK, {"k": INK_SOFT})))
    bitmap("well_lock_sel", 40, 24, lambda c: (rounded_box(c, 0, 0, sw, sh, 3, SELECT, INK, SELECT_LIGHT, SELECT_DARK),
                                               MH.stamp_rows(c, sw // 2 - 2, sh // 2 - 3, MH.LOCK, {"k": INK})))
    bitmap("chip_lock", 16, 16, lambda c: (rounded_box(c, 0, 0, 11, 9, 2, PANEL, INK, WHITE, PANEL_SHADE),
                                           MH.stamp_rows(c, 3, 1, MH.LOCK, {"k": INK})))
    bitmap("qmark", 8, 8, lambda c: MH.stamp_rows(c, 0, 0, MH.QMARK, {"k": INK}))
    bitmap("eye", 16, 8, lambda c: MH.stamp_rows(c, 0, 0, MH.EYE, {"#": INK, "+": WHITE}))
    bitmap("a_btn", 16, 16, lambda c: MH.stamp_rows(c, 0, 0, MH.A_BTN, {"#": INK, "+": WHITE}))
    bitmap("sun", 16, 16, lambda c: MH.stamp_rows(c, 0, 0, MH.SUN, {"#": SELECT_DARK, "+": SELECT}))
    bitmap("moon", 16, 16, lambda c: MH.stamp_rows(c, 0, 0, MH.MOON, {"#": INK, "+": INK_SOFT}))
    for zone in (None, "NORTH", "EAST", "SOUTH", "WEST"):
        bitmap("compass_%s" % (zone or "none").lower(), 16, 16, lambda c, z=zone: MH.compass(c, 0, 0, z))
    sx, sy, sw2, sh2 = MH.SEG

    def seg(c, time):
        rounded_box(c, 0, 0, sw2, sh2, 4, PANEL, INK, WHITE, PANEL_SHADE)
        half = (0, 0, sw2 // 2 + 1, sh2) if time == "day" else (sw2 // 2, 0, sw2 - sw2 // 2, sh2)
        rounded_box(c, *half, 4, SELECT, INK, SELECT_LIGHT, SELECT_DARK)
        c.vline(sw2 // 2, 1, sh2 - 2, INK)
        MH.stamp_rows(c, 4, 2, MH.SUN, {"#": SELECT_DARK if time == "day" else INK_SOFT,
                                        "+": SELECT_LIGHT if time == "day" else PANEL_SHADE})
        MH.stamp_rows(c, sw2 // 2 + 5, 2, MH.MOON, {"#": INK if time == "night" else INK_SOFT,
                                                   "+": SELECT_LIGHT if time == "night" else PANEL_SHADE})
    bitmap("seg_day", 40, 16, lambda c: seg(c, "day"))
    bitmap("seg_night", 40, 16, lambda c: seg(c, "night"))

    def chev_down(c):
        for r, row in enumerate(SMALL_ARROW):
            for col, ch in enumerate(row[::-1]):
                if ch in "OF":
                    c.set(r, col, SPARE_A if ch == "F" else INK)
    bitmap("down", 16, 8, chev_down)


# ------------------------------------------------------------------ data header
def region_data(region, zones_by_id):
    tags = RT.Tags(region="tosa") if region == "tosa" else ET.load_tags()
    if region == "tosa":
        art = EM.map_art(tags).convert("RGB")
    habitats, cells = [], []
    own = {}
    for a in tags.placed():
        z = zones_by_id.get(a.id) if region == "tosa" else None
        zid = ZONES.index(z) + 1 if z in ZONES else (1 if region == "tiksi" else 0)
        nx, ny = a.node_cell
        habitats.append((a.id, zid, nx, ny, len(cells), len(a.cells), a.name))
        for c in a.cells:
            cells.append(c)
            own[c] = zid
    grid = []
    pts = [(c, z) for c, z in own.items() if z]
    for cy in range(MH.ROWS):
        row = []
        for cx in range(MH.COLS):
            if (cx, cy) in own:
                row.append(own[(cx, cy)])
            elif region == "tosa" and MH.is_sea(art, cx, cy):
                row.append(0)
            elif region == "tosa":
                row.append(min(pts, key=lambda p: (p[0][0] - cx) ** 2 + (p[0][1] - cy) ** 2)[1])
            else:
                row.append(0)
        grid.append(row)
    return habitats, cells, grid


def write_header(n_frame, n_map_sheet, n_route):
    zones_by_id = seed_tag_zones()
    L = []
    a = L.append
    a("// Generated by dev_scripts/orchid_ui/export_habitats.py - do not edit.")
    a("// Pokédex HABITATS: layout constants and region habitat tables. Species come from gWildMonHeaders at runtime.")
    a("#ifndef GUARD_DATA_POKEDEX_HABITATS_H")
    a("#define GUARD_DATA_POKEDEX_HABITATS_H")
    a("")
    a("#define HAB_MAP_FRAME_TILES %d" % n_frame)
    a("#define HAB_MAP_SHEET_TILES %d" % n_map_sheet)
    a("#define HAB_OVERLAY_TILE_BASE %d   // + 0 empty, 1 dim, 2+mask rim, 18+mask glow (mask N1 E2 S4 W8)" % n_frame)
    a("#define HAB_OVERLAY_PAL %d" % OVERLAY_PAL)
    a("#define HAB_ROUTE_TILES %d" % n_route)
    a("#define HAB_GRID_X %d" % MH.GX)
    a("#define HAB_GRID_Y %d" % MH.GY)
    a("#define HAB_COLS %d" % MH.COLS)
    a("#define HAB_ROWS %d" % MH.ROWS)
    for k, (x, y) in MH.PLATE.items():
        a("#define HAB_PLATE_%s_X %d" % (k.upper(), x))
        a("#define HAB_PLATE_%s_Y %d" % (k.upper(), y))
    a("#define HAB_PLATE_W %d" % MH.PLATE_W)
    x, y, w, h = MH.CTA
    a("#define HAB_CTA_X %d\n#define HAB_CTA_Y %d\n#define HAB_CTA_W %d" % (x, y, w))
    x, y, w, h = MH.TIME_CHIP
    a("#define HAB_TIME_X %d\n#define HAB_TIME_Y %d" % (x, y))
    x, y, w, h = EM.NAME_PILL
    a("#define HAB_NAME_X %d\n#define HAB_NAME_Y %d\n#define HAB_NAME_W %d" % (x, y, w))
    a("#define HAB_TAB_X0 %d\n#define HAB_TAB_W %d\n#define HAB_TAB_PITCH %d" % (MH.TAB_X0, MH.TAB_W, MH.TAB_W + 4))
    a("#define HAB_ROW_Y0 %d\n#define HAB_ROW_PITCH %d\n#define HAB_ROWS_VISIBLE %d" % (MH.ROW_Y0, MH.ROW_PITCH, MH.ROWS_VISIBLE))
    a("#define HAB_CHIP_X %d\n#define HAB_SLOT_X0 %d\n#define HAB_SLOT_W %d\n#define HAB_SLOT_PITCH %d\n#define HAB_SLOT_N %d"
      % (MH.CHIP_X, MH.SLOT_X0, MH.SLOT_W, MH.SLOT_PITCH, MH.SLOT_N))
    a("#define HAB_WELL_DY %d\n#define HAB_WELL_H %d\n#define HAB_TRAY_Y %d" % (MH.WELL_DY, MH.WELL_H, MH.TRAY_Y))
    x, y, w, h = MH.SEG
    a("#define HAB_SEG_X %d\n#define HAB_SEG_Y %d" % (x, y))
    a("")
    a("static const u8 *const sHabZoneNames[] = {")
    a('    COMPOUND_STRING(""),')
    for z in ZONES:
        a('    COMPOUND_STRING("%s"),' % MH.ZONE_NAME[z])
    a("};")
    a("")
    for region in ("tosa", "tiksi"):
        hab, cells, grid = region_data(region, zones_by_id)
        R = region.capitalize()
        a("static const u8 sHabCells_%s[][2] = {" % R)
        for i in range(0, len(cells), 12):
            a("    " + " ".join("{%d, %d}," % c for c in cells[i:i + 12]))
        a("};")
        a("static const struct OrchidHabitat sHabitats_%s[] = {" % R)
        for (sid, z, nx, ny, c0, cn, name) in hab:
            a("    {%s, %d, %d, %d, %d, %d}, // %s" % (sid, z, nx, ny, c0, cn, name))
        a("};")
        a("static const u8 sHabZoneGrid_%s[HAB_ROWS][HAB_COLS] = {" % R)
        for row in grid:
            a("    {" + ",".join(str(v) for v in row) + "},")
        a("};")
        a("")
    a("#endif // GUARD_DATA_POKEDEX_HABITATS_H")
    with open(P("src", "data", "pokedex_habitats.h"), "w") as f:
        f.write("\n".join(L) + "\n")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    n_frame, n_sheet = export_map_sheet()
    n_route = export_route_sheet()
    export_bitmaps()
    write_header(n_frame, n_sheet, n_route)
    print("map frame tiles", n_frame, "sheet", n_sheet, "route tiles", n_route)
