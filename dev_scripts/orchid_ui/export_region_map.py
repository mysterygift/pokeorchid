"""
Tosa region map: ROM art + map data from the USER's art (dev_scripts/orchid_ui/ref/tosa_*.png).

The three 240x160 sources are rotated 180 deg (user request) before anything else. Square numbers
(from tosa_towns.png, numbered top-to-bottom / left-to-right on the ORIGINAL image) are kept, so
the user's names by number stay valid. Screen pixel = map-art pixel (unzoomed); cursor cell
(x, y) of the 28x15 grid = 8x8 px at (8 + 8x, 16 + 8y) (region_map.c MAPCURSOR_X/Y_MIN = 1, 2).

Writes:
  graphics/pokenav/region_map/map.png / map.pal / map.bin   Town Map, Fly map, PokeNav (affine,
        8bpp, 64x64-byte map, <= 256 tiles, no flips); pixel values 112+ (BG palettes 7-9)
  graphics/pokedex/region_map.png / .pal / .bin             dex AREA copy (text 8bpp, 32x32)
  src/data/region_map/region_map_layout.h                   cursor grid (Tosa sections only)
  src/data/region_map/region_map_sections.json               Tosa cells, placeholders, Hoenn off-grid
  dev_scripts/orchid_ui/ref/tosa_places.md                   placeholder table for renaming
  graphics/pokenav/region_map/brendan_icon.png, may_icon.png  map heads cut from the player OW sprites
  graphics/pokenav/region_map/orchid_frame.png / .bin        Orchid frame (header, map rim, tray + name pill)

What the format forces (everything else is the user's pixels):
  * only tile rows 2-16 (y 16-135 = the cursor grid) are kept; rows 0-1 and 17-19 (under the
    header / tray in every view) and the rest of the 512x512 affine map are one sea tile;
  * squares become full-cell opaque markers (one shared tile each for cities / landmarks), since
    the user's terrain under the 20 squares alone would push the map past the 256-tile limit.

usage: export_region_map.py
"""
import json
import os
import struct
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
REF = os.path.join(HERE, "ref")
P = lambda *p: os.path.join(ROOT, *p)
W, H = 240, 160
GX, GY = 8, 16
RED = (255, 0, 0)
PAL_BASE = 112                      # BG palette 7, colour 0

# Markers (Hoenn region-map reds, snapped to BGR555): city = full-cell red block,
# landmark = route-yellow cell with a small red dot.
CITY_DARK, CITY_FACE, CITY_HI = (144, 0, 0), (248, 56, 16), (248, 168, 16)
LM_GROUND, LM_EDGE = (240, 208, 80), (224, 160, 0)

TOSA_PORT, TELOK = 4, 10
# Placeholder kinds for the other 18 squares (user: "randomly set as cities/landmarks").
LANDMARKS = {3, 6, 7, 11, 15, 16, 18, 20}


def load(name):
    return Image.open(os.path.join(REF, name)).convert("RGB").rotate(180)


def squares():
    """{number: (cx, cy)} with numbers from the ORIGINAL image order, cells on the rotated map."""
    orig = Image.open(os.path.join(REF, "tosa_towns.png")).convert("RGB")
    px = orig.load()
    found = []
    for y in range(0, H, 8):
        for x in range(0, W, 8):
            if px[x, y] == RED and px[x + 7, y + 7] == RED:
                found.append((x, y))
    out = {}
    for n, (x, y) in enumerate(found, 1):
        nx, ny = W - 8 - x, H - 8 - y              # 180 deg: the 8x8 block's new top-left
        out[n] = ((nx - GX) // 8, (ny - GY) // 8)
    return out


def route_cells_between(a, b):
    """Route cells on the straight line between squares a and b of the rotated routes image."""
    rt = load("tosa_routes.png").load()
    (ax, ay), (bx, by) = a, b
    cells = []
    if ax == bx:
        for cy in range(min(ay, by) + 1, max(ay, by)):
            cells.append((ax, cy))
    elif ay == by:
        for cx in range(min(ax, bx) + 1, max(ax, bx)):
            cells.append((cx, ay))
    ok = []
    for cx, cy in cells:
        x0, y0 = GX + cx * 8, GY + cy * 8
        n = sum(1 for i in range(8) for j in range(8) if rt[x0 + i, y0 + j][0] > 200 and rt[x0 + i, y0 + j][2] < 130)
        if n >= 12:
            ok.append((cx, cy))
    return ok


def city_tile():
    t = [[CITY_FACE] * 8 for _ in range(8)]
    for i in range(8):
        t[0][i] = t[7][i] = t[i][0] = t[i][7] = CITY_DARK
    for i in range(1, 7):
        t[1][i] = CITY_HI
    t[1][1] = t[2][1] = CITY_HI
    return t


def landmark_tile():
    t = [[LM_GROUND] * 8 for _ in range(8)]
    for i in range(8):
        t[0][i] = t[7][i] = LM_EDGE
    for y in range(2, 6):
        for x in range(2, 6):
            t[y][x] = CITY_FACE
    for i in range(2, 6):
        t[2][i] = CITY_DARK if False else t[2][i]
    t[2][2] = t[2][5] = t[5][2] = t[5][5] = LM_GROUND
    t[2][3] = t[2][4] = CITY_HI
    return t


def map_art():
    im = load("tosa_routes.png")
    px = im.load()
    sq = squares()
    for n, (cx, cy) in sq.items():
        t = landmark_tile() if n in LANDMARKS else city_tile()
        x0, y0 = GX + cx * 8, GY + cy * 8
        for y in range(8):
            for x in range(8):
                px[x0 + x, y0 + y] = t[y][x]
    return im


def sea_tile(im):
    px = im.load()
    # a pure-sea tile from the rotated art (the stripes repeat every 4 rows)
    for ty in range(17, 20):
        for tx in range(30):
            t = tuple(px[tx * 8 + x, ty * 8 + y] for y in range(8) for x in range(8))
            if set(t) <= {(152, 208, 248), (160, 176, 248)}:
                return t
    raise SystemExit("no sea tile")


def build_tiles(im):
    """Tiles + 30x20 cell list for the kept area (rows 2-16), sea elsewhere."""
    px = im.load()
    sea = sea_tile(im)
    tiles, index = [sea], {sea: 0}
    cells = []
    for ty in range(20):
        for tx in range(30):
            if 2 <= ty <= 16:
                t = tuple(px[tx * 8 + x, ty * 8 + y] for y in range(8) for x in range(8))
            else:
                t = sea
            if t not in index:
                index[t] = len(tiles)
                tiles.append(t)
            cells.append(index[t])
    return tiles, cells


def palette_of(tiles):
    cols = []
    for t in tiles:
        for c in t:
            if c not in cols:
                cols.append(c)
    assert len(cols) <= 47, len(cols)
    return cols


def write_png8(path, tiles, cols):
    per = 16
    rows = (len(tiles) + per - 1) // per
    im = Image.new("P", (per * 8, rows * 8), 0)
    flat = [0, 0, 0] * PAL_BASE + [c for rgb in [(0, 0, 0)] + cols for c in rgb]
    im.putpalette(flat + [0] * (768 - len(flat)))
    px = im.load()
    for i, t in enumerate(tiles):
        ox, oy = (i % per) * 8, (i // per) * 8
        for j, c in enumerate(t):
            px[ox + j % 8, oy + j // 8] = PAL_BASE + 1 + cols.index(c)
    im.save(path)


def write_jasc48(path, cols):
    pal = [(0, 0, 0)] + cols
    pal += [(0, 0, 0)] * (48 - len(pal))
    with open(path, "w", newline="\n") as f:
        f.write("JASC-PAL\n0100\n48\n")
        for c in pal:
            f.write("%d %d %d\n" % c)


PLACE_NAMES = {}


def place_name(n):
    return ("Site %02d" if n in LANDMARKS else "Town %02d") % n


def update_sections(sq, reserve):
    path = P("src", "data", "region_map", "region_map_sections.json")
    data = json.load(open(path))
    secs = data["map_sections"]
    ids = [s["id"] for s in secs]
    kanto0, kanto1 = ids.index("MAPSEC_PALLET_TOWN"), ids.index("MAPSEC_SPECIAL_AREA")
    tosa = {
        "MAPSEC_TOSA_PORT": (sq[TOSA_PORT], 1, 1),
        "MAPSEC_OLDALE_TOWN": (sq[TELOK], 1, 1),
        "MAPSEC_SOUTH_TOSA_RESERVE": (min(reserve), 1 + max(c[1] for c in reserve) - min(c[1] for c in reserve)
                                      if reserve[0][0] == reserve[-1][0] else 1, None),
    }
    rx, ry = min(reserve)
    rw = max(c[0] for c in reserve) - rx + 1
    rh = max(c[1] for c in reserve) - ry + 1
    for i, s in enumerate(secs):
        if s["id"].startswith("MAPSEC_TOSA_PH_"):
            continue
        if s["id"] == "MAPSEC_TOSA_PORT":
            s.update(x=sq[TOSA_PORT][0], y=sq[TOSA_PORT][1], width=1, height=1)
        elif s["id"] == "MAPSEC_OLDALE_TOWN":
            s.update(x=sq[TELOK][0], y=sq[TELOK][1], width=1, height=1)
        elif s["id"] == "MAPSEC_SOUTH_TOSA_RESERVE":
            s.update(x=rx, y=ry, width=rw, height=rh)
        elif not (kanto0 <= i < kanto1) and "x" in s:
            # vanilla Hoenn section: off the Tosa grid (no cell, nothing drawn or highlighted)
            s.pop("x", None)
            s.pop("y", None)
            s["width"] = 0
            s["height"] = 0
    secs[:] = [s for s in secs if not s["id"].startswith("MAPSEC_TOSA_PH_")]
    for n in sorted(sq):
        if n in (TOSA_PORT, TELOK):
            continue
        cx, cy = sq[n]
        secs.append({"id": "MAPSEC_TOSA_PH_%02d" % n, "name": place_name(n), "x": cx, "y": cy, "width": 1, "height": 1})
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    return secs


def write_layout(secs):
    grid = [["MAPSEC_NONE"] * 28 for _ in range(15)]
    for s in secs:
        if s["id"] in ("MAPSEC_TOSA_PORT", "MAPSEC_OLDALE_TOWN", "MAPSEC_SOUTH_TOSA_RESERVE") or s["id"].startswith("MAPSEC_TOSA_PH_"):
            for y in range(s["y"], s["y"] + s["height"]):
                for x in range(s["x"], s["x"] + s["width"]):
                    grid[y][x] = s["id"]
    L = ["// GENERATED by dev_scripts/orchid_ui/export_region_map.py (Tosa, from the user's art).",
         "static const mapsec_u8_t sRegionMap_MapSectionLayout[MAP_HEIGHT][MAP_WIDTH] = {"]
    for row in grid:
        L.append("    {" + ", ".join(row) + "},")
    L.append("};")
    open(P("src", "data", "region_map", "region_map_layout.h"), "w").write("\n".join(L) + "\n")


def write_places_md(sq, reserve):
    L = ["# Tosa region map places", "",
         "Generated by `dev_scripts/orchid_ui/export_region_map.py` from the user's art (`ref/tosa_*.png`,",
         "rotated 180 deg). Square numbers are the user's (original image order). Cells are on the 28x15",
         "region-map cursor grid. Rename a placeholder by editing its `name` in",
         "`src/data/region_map/region_map_sections.json` (and here).", "",
         "| # | Cell | MAPSEC | Name | Kind |", "|---|---|---|---|---|"]
    for n in sorted(sq):
        cx, cy = sq[n]
        if n == TOSA_PORT:
            row = (n, cx, cy, "MAPSEC_TOSA_PORT", "Tosa Port", "town")
        elif n == TELOK:
            row = (n, cx, cy, "MAPSEC_OLDALE_TOWN", "Telok Town", "town")
        else:
            row = (n, cx, cy, "MAPSEC_TOSA_PH_%02d" % n, place_name(n) + " (placeholder)", "landmark" if n in LANDMARKS else "city/town")
        L.append("| %d | (%d,%d) | `%s` | %s | %s |" % row)
    L += ["", "South Tosa Reserve (`MAPSEC_SOUTH_TOSA_RESERVE`): route cells %s, between #%d and #%d." %
          (", ".join("(%d,%d)" % c for c in reserve), TOSA_PORT, TELOK), "",
          "Markers: towns / cities = full-cell red block; landmarks = small red dot on a route-yellow cell."]
    open(os.path.join(REF, "tosa_places.md"), "w").write("\n".join(L) + "\n")


def player_heads():
    """16x16 map heads cut from the protagonists' overworld sprites (walking.png frame 0, facing
    down, rows 8-23 = hair to collar), keeping their own palettes (object_events/palettes)."""
    for gender in ("brendan", "may"):
        src = Image.open(P("graphics", "object_events", "pics", "people", gender, "walking.png"))
        pal = []
        for line in open(P("graphics", "object_events", "palettes", gender + ".pal")).read().split("\n")[3:19]:
            pal.append(tuple(int(v) for v in line.split()))
        head = src.crop((0, 8, 16, 24))
        out = Image.new("P", (16, 16), 0)
        out.putdata(list(head.getdata()))
        out.putpalette([c for rgb in pal for c in rgb] + [0] * (768 - 48))
        out.save(P("graphics", "pokenav", "region_map", gender + "_icon.png"), transparency=0)


# ---- Orchid frame for the Town Map / Fly map (BG1, palette slot 1, charbase 3 tiles)
FRAME_PAL_SLOT = 1
NAME_PILL = (6, 140, 116, 14)         # fits "South Tosa Reserve" (101 px, FONT_NORMAL) + 6 px margins


def frame_art():
    import sys
    sys.path.insert(0, HERE)
    from kit import new_sheet, Canvas, rounded_box, to_tiles, write_tilemap, TRANSPARENT, INK, \
        ACCENT, ACCENT_DARK, ACCENT_LIGHT, PANEL, WHITE, PANEL_SHADE
    import dex_ext as D
    im = new_sheet(W, H, "orchid", spare_a=D.BALL_RED)
    cv = Canvas(im)
    D.header_band(cv, 0, W - 1, round_left=False)
    rounded_box(cv, 2, 17, 236, 118, 4, TRANSPARENT, INK, ACCENT_DARK, ACCENT_LIGHT)
    for y in range(16, 136):
        for x in (0, 1, 238, 239):
            cv.set(x, y, ACCENT)
    D.tray(cv, 136)
    x, y, w, h = NAME_PILL
    rounded_box(cv, x, y, w, h, 4, PANEL, INK, WHITE, PANEL_SHADE)
    tiles, tm = to_tiles(im)
    assert len(tiles) <= 256, len(tiles)
    from kit import tiles_to_image
    sheet = tiles_to_image(tiles, im)
    pal = D.dex_palette("orchid")
    flat = [c for rgb in pal for c in rgb]
    sheet.putpalette(flat + [0] * (768 - len(flat)))
    sheet.save(P("graphics", "pokenav", "region_map", "orchid_frame.png"), transparency=0)
    cells = [None] * (32 * 32)
    for i, item in enumerate(tm):
        cells[(i // 30) * 32 + i % 30] = item
    write_tilemap(P("graphics", "pokenav", "region_map", "orchid_frame.bin"), cells, pal_num=FRAME_PAL_SLOT)
    return len(tiles)


def export():
    sq = squares()
    reserve = route_cells_between(sq[TOSA_PORT], sq[TELOK])
    art = map_art()
    tiles, cells = build_tiles(art)
    assert len(tiles) <= 256, len(tiles)
    cols = palette_of(tiles)
    # --- affine map (Town Map / Fly / PokeNav): 64x64 bytes
    write_png8(P("graphics", "pokenav", "region_map", "map.png"), tiles, cols)
    write_jasc48(P("graphics", "pokenav", "region_map", "map.pal"), cols)
    amap = bytearray(64 * 64)
    for i, t in enumerate(cells):
        amap[(i // 30) * 64 + i % 30] = t
    open(P("graphics", "pokenav", "region_map", "map.bin"), "wb").write(bytes(amap))
    # --- dex AREA copy: text mode, 32x32 u16 entries (no flips used), same tiles / palette
    write_png8(P("graphics", "pokedex", "region_map.png"), tiles, cols)
    write_jasc48(P("graphics", "pokedex", "region_map.pal"), cols)
    tmap = bytearray()
    for y in range(32):
        for x in range(32):
            t = cells[y * 30 + x] if (x < 30 and y < 20) else 0
            tmap += struct.pack("<H", t)
    open(P("graphics", "pokedex", "region_map.bin"), "wb").write(bytes(tmap))
    player_heads()
    print("frame tiles", frame_art())
    secs = update_sections(sq, reserve)
    write_layout(secs)
    write_places_md(sq, reserve)
    return sq, reserve, len(tiles), len(cols)


if __name__ == "__main__":
    sq, reserve, nt, nc = export()
    print("tiles", nt, "colours", nc, "reserve", reserve)
    for n in sorted(sq):
        print(n, sq[n])
