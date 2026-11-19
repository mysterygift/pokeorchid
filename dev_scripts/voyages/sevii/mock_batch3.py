"""
Batch 3 (Sevii Islands 4-7): FAITHFUL translations of the FRLG maps (frlg_translate.py, same size, FRLG
events) on the proposed gTileset_SeviiIslands (sevii_tileset.py = Rustboro copy + additions), plus the
invented Surf routes 4<->5 and 6<->7 (sea_routes.py), region maps, overview. Icefall Cave rooms come from
icefall_translate.py (General + Cave, Shoal ice look) and the Rocket Warehouse interior from
rocket_warehouse_interior.py (General + BikeShop, New Mauville tiles); this script only places them in the
overview.

usage: <venv python> dev_scripts/voyages/mock_batch3.py [maps] [routes] [overview] [regionmap] [ice] [probe]
       [MapName ...] [--seams]       (no step names = maps routes overview regionmap)
  ice / probe = the pre-decision Icefall look comparison and the FRLG metatile probe (kept for the record)
FRLG reference renders: <venv python> dev_scripts/voyages/frlg_ref.py batch3   -> ref/frlg/
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import voyage_compose as vc   # noqa: E402
import frlg_translate as ft   # noqa: E402
import sea_routes as sr       # noqa: E402
from PIL import Image, ImageDraw   # noqa: E402

OUT = os.path.join(HERE, "out", "batch3")
ROOT = vc.ROOT
RM = os.path.join(ROOT, "graphics", "pokenav", "region_map")


# ------------------------------------------------------------------ region maps
def region_map(key):
    """map_sevii_<key>.png (8bpp tiles) + .bin (64x64 u8 map) -> 240x160 @4x with section boxes (as batch 2)."""
    t = Image.open(os.path.join(RM, "map_sevii_%s.png" % key))
    b = open(os.path.join(RM, "map_sevii_%s.bin" % key), "rb").read()
    cols = t.width // 8
    im = Image.new("P", (64 * 8, 64 * 8))
    im.putpalette(t.getpalette())
    for i, v in enumerate(b):
        im.paste(t.crop(((v % cols) * 8, (v // cols) * 8, (v % cols) * 8 + 8, (v // cols) * 8 + 8)),
                 ((i % 64) * 8, (i // 64) * 8))
    im = im.convert("RGB").crop((0, 0, 240, 160))
    src = open(os.path.join(ROOT, "src", "data", "region_map", "region_map_layout_sevii%s.h" % key)).read()
    rows = [re.findall(r"MAPSEC_\w+", r) for r in src.split("\n")[1:16]]
    S = 4
    big = im.resize((240 * S, 160 * S), Image.NEAREST)
    d = ImageDraw.Draw(big)
    secs = {}
    for y, r in enumerate(rows):
        for x, s in enumerate(r):
            if s != "MAPSEC_NONE":
                secs.setdefault(s, []).append((x, y))
                X, Y = (x + 1) * 8 * S, (y + 2) * 8 * S      # MAPCURSOR_X_MIN 1, MAPCURSOR_Y_MIN 2
                d.rectangle([X, Y, X + 8 * S - 1, Y + 8 * S - 1], outline=(200, 30, 30))
    for s, cells in secs.items():
        x, y = min(cells)
        d.text(((x + 1) * 8 * S + 2, (y + 2) * 8 * S + 2), s[7:].replace("_", " ").title(), fill=(0, 0, 0),
               stroke_width=2, stroke_fill=(255, 255, 255))
    for x in range(28):
        d.text(((x + 1) * 8 * S + 10, 2), str(x), fill=(40, 40, 120))
    for y in range(15):
        d.text((2, (y + 2) * 8 * S + 10), str(y), fill=(40, 40, 120))
    big.save(os.path.join(OUT, "sevii%s_region_map@4x.png" % key))
    return {s: sorted(c) for s, c in secs.items()}


# ------------------------------------------------------------------ ice room comparison
def ice():
    import specs_batch3 as sp
    outs = []
    for name in ("icefall_ice_coldstorage", "icefall_ice_shoal"):
        spec = sp.ALL[name]
        vc.check_size(*spec["size"])
        g = vc.render(spec, os.path.join(OUT, name))
        print("%-26s %3dx%-3d %s/%s" % (name, spec["size"][0], spec["size"][1], spec["tileset"][0][9:],
                                       spec["tileset"][1][9:]))
        if "--seams" in sys.argv:
            ss = vc.seams(g, spec["tileset"])
            print("   seams:", len(ss), " ".join("%d,%d%s:%03X/%03X" % s for s in ss[:40]))
        im = Image.open(os.path.join(OUT, name + "@2x.png")).convert("RGB")
        dr = ImageDraw.Draw(im)                # shortest solution, entry -> goal (review aid only)
        pts = [(x * 32 + 16, y * 32 + 16) for x, y in spec["route"]]
        dr.line(pts, fill=(255, 230, 40), width=3)
        for p in pts[1:]:
            dr.ellipse([p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4], fill=(255, 230, 40))
        outs.append((spec, im))
    pad, head = 16, 40
    W = sum(im.width for _, im in outs) + pad * (len(outs) + 1)
    H = max(im.height for _, im in outs) + head + pad
    sheet = Image.new("RGB", (W, H), (40, 40, 48))
    d = ImageDraw.Draw(sheet)
    x = pad
    for spec, im in outs:
        sheet.paste(im, (x, head))
        d.text((x, 6), spec["name"], fill=(255, 255, 255))
        d.text((x, 20), "%s + %s" % spec["tileset"], fill=(180, 200, 255))
        x += im.width + pad
    sheet.save(os.path.join(OUT, "icefall_ice_compare.png"))


# ------------------------------------------------------------------ FRLG metatile probe (Four Island)
def probe():
    import frlg_probe
    frlg_probe.main(os.path.join(OUT, "four_island_metatile_probe"), "LAYOUT_FOUR_ISLAND")


# ------------------------------------------------------------------ FRLG translations
# FRLG map -> pair. Both clusters are on the proposed Sevii-only Rustboro copy, so every edge connection
# (FRLG's and the invented sea routes) joins two maps with the same secondary.
MAPS = {
    "FourIsland": "sevii",
    "FiveIsland": "sevii", "FiveIsland_Meadow": "sevii", "FiveIsland_MemorialPillar": "sevii",
    "SixIsland": "sevii", "SixIsland_WaterPath": "sevii", "SixIsland_RuinValley": "sevii",
    "SevenIsland": "sevii", "SevenIsland_SevaultCanyon_Entrance": "sevii", "SevenIsland_SevaultCanyon": "sevii",
    "SevenIsland_TanobyRuins": "tanoby",       # Tiksi's Tanoby Delta tileset (shared art, used as-is)
}
BUILDING_CHOICE = {"FiveIsland_Meadow": {0: "rocket_warehouse"},
                   "SevenIsland_TanobyRuins": {i: "chamber" for i in range(7)}}
VSTAMPS = {}
EXTRA_MARKS = {}
ZOOM = {"FiveIsland_MemorialPillar": (0, 37, 17, 56)}

# invented Surf routes (user: keep sea routes between the islands, short, walled by sea rocks)
SEA_ROUTES = {
    # Four Island's south sea (x12-19) down, then east to Five Island's west sea (rows 6-13)
    "sevii_sea_route_c": sr.route_spec(
        "Sevii Sea Route C", (40, 22), corridor=[(2, 0, 8, 20), (2, 12, 38, 8)], islets=[(22, 14, 6, 4)],
        conns=[("up", -10, "MAP_FOUR_ISLAND", (2, 9)), ("right", 6, "MAP_FIVE_ISLAND", (12, 19))],
        marks=[(24, 15, "", "item", "item"), (5, 7, "", "npc", "swimmer"), (15, 17, "", "npc", "swimmer"),
               (34, 13, "", "npc", "swimmer")]),
    # Seven Island's east sea (rows 8-13) east to Six Island's south-west sea (rows 24-29)
    "sevii_sea_route_d": sr.route_spec(
        "Sevii Sea Route D", (40, 10), corridor=[(0, 2, 40, 6)],
        conns=[("left", -6, "MAP_SEVEN_ISLAND", (2, 7)), ("right", -22, "MAP_SIX_ISLAND", (2, 7))],
        marks=[(10, 4, "", "npc", "swimmer"), (26, 5, "", "npc", "swimmer")]),
}
SEA_ROUTE_NEIGHBOURS = {"MAP_FOUR_ISLAND": "FourIsland", "MAP_FIVE_ISLAND": "FiveIsland",
                        "MAP_SEVEN_ISLAND": "SevenIsland", "MAP_SIX_ISLAND": "SixIsland"}


def translate_maps(names, seams=False):
    grids = {}
    for n in names:
        fm = ft.load_map(n)
        spec = ft.translate(fm, MAPS[n], BUILDING_CHOICE.get(n), vstamps=VSTAMPS.get(n))
        spec["marks"] += EXTRA_MARKS.get(n, [])
        const = [m for m, nn in SEA_ROUTE_NEIGHBOURS.items() if nn == n]
        if const:
            gone = sr.clear_edge_rocks(spec, sr.island_openings(SEA_ROUTES).get(const[0], []))
            if gone:
                fm.report["sea_rocks_cleared_for_route"] = gone
        base = os.path.join(OUT, ft.snake(n))
        g = ft.render(spec, base)
        grids[n] = (g, spec["tileset"])
        ft.side_by_side(fm, base, zoom=ZOOM.get(n))
        ft.write_spec(spec, fm, base + "_spec.json")
        r = fm.report
        print("%-34s %3dx%-3d %-6s bld=%d caves=%d boulders=%d arrows=%d ported=%d rocks_cleared=%d" % (
            n, fm.w, fm.h, MAPS[n], len(r["buildings"]), len(r["caves"]), len(r.get("boulders", [])),
            len(r.get("arrow_warps", [])), r.get("ported_cells", 0), len(r.get("sea_rocks_cleared_for_route", []))))
        if seams:
            ss = vc.seams(g, spec["tileset"], ignore={0x001, 0x124, 0x170})
            print("   seams: %d" % len(ss))
    return grids


def sea_routes(grids):
    probs = []
    for key, spec in SEA_ROUTES.items():
        nb = {m: grids[n] for m, n in SEA_ROUTE_NEIGHBOURS.items() if n in grids}
        for m, o0, o1 in sr.autofit(spec, {m: nb[m] for _d, _o, m, _ab in spec["conns"]}):
            if o0 != o1:
                print("   %s: offset to %s moved %s -> %s" % (key, m[4:], o0, o1))
        g = vc.render(spec, os.path.join(OUT, key))
        probs += sr.check(spec, g, nb)
        print("%-34s %3dx%-3d sevii  conns=%s" % (key, spec["size"][0], spec["size"][1],
                                                  [(c[0], c[1], c[2][4:]) for c in spec["conns"]]))
    for p in probs:
        print("   ROUTE CHECK:", p)
    return probs


# overview: each cluster's FRLG connection chain laid out by its offsets; islands placed by region-map cell
# (~24 tiles per cell); sea routes placed at their connection offsets; warp-only maps drawn beside their door.
def overview_positions():
    P = {}
    P["FourIsland"] = (0, 0)
    P["sevii_sea_route_c"] = (P["FourIsland"][0] - SEA_ROUTES["sevii_sea_route_c"]["conns"][0][1], 40)
    P["FiveIsland"] = (P["sevii_sea_route_c"][0] + 40, P["sevii_sea_route_c"][1]
                       + SEA_ROUTES["sevii_sea_route_c"]["conns"][1][1])
    P["FiveIsland_Meadow"] = (P["FiveIsland"][0] + 24, P["FiveIsland"][1])
    P["FiveIsland_MemorialPillar"] = (P["FiveIsland_Meadow"][0] + 24, P["FiveIsland_Meadow"][1] + 20)
    P["four_island_icefall_cave_entrance"] = (52, -40)
    P["four_island_icefall_cave_1f"] = (86, -40)
    P["four_island_icefall_cave_b1f"] = (110, -40)
    P["four_island_icefall_cave_back"] = (138, -40)
    P["five_island_rocket_warehouse"] = (P["FiveIsland_Meadow"][0] - 2, P["FiveIsland_Meadow"][1] + 44)
    # cluster 6-7, to the right. Route D hangs off Seven Island's east edge; the Six Island group (Six, Water
    # Path, Ruin Valley) is drawn SIX_GAP tiles further east than Route D's far end so Ruin Valley doesn't
    # cover Sevault Canyon (in the game Route D's east edge meets Six Island directly).
    X0, Y0, SIX_GAP = 190, 60, 24
    rd = SEA_ROUTES["sevii_sea_route_d"]["conns"]
    P["SevenIsland"] = (X0, Y0)
    P["sevii_sea_route_d"] = (X0 + 24, Y0 - rd[0][1])
    P["SevenIsland_SevaultCanyon_Entrance"] = (X0, Y0 + 20)
    P["SevenIsland_SevaultCanyon"] = (X0 + 24, Y0 + 40)
    P["SevenIsland_TanobyRuins"] = (X0 + 24 - 48, Y0 + 120)
    P["SixIsland"] = (P["sevii_sea_route_d"][0] + 40 + SIX_GAP, P["sevii_sea_route_d"][1] + rd[1][1])
    P["SixIsland_WaterPath"] = (P["SixIsland"][0] + 24, P["SixIsland"][1] - 40)
    P["SixIsland_RuinValley"] = (P["SixIsland_WaterPath"][0] - 48, P["SixIsland_WaterPath"][1] + 80)
    return P


def overview():
    k = 2
    pos = overview_positions()
    ims = {}
    for n in pos:
        f = os.path.join(OUT, (ft.snake(n) if n in MAPS else n) + ".png")
        if os.path.exists(f):
            ims[n] = Image.open(f).convert("RGB")
    xs = [pos[n][0] for n in ims] + [pos[n][0] + ims[n].width // 16 for n in ims]
    ys = [pos[n][1] for n in ims] + [pos[n][1] + ims[n].height // 16 for n in ims]
    x0, y0 = min(xs), min(ys)
    ov = Image.new("RGB", ((max(xs) - x0) * k + 20, (max(ys) - y0) * k + 30), (98, 172, 224))
    d = ImageDraw.Draw(ov)
    for n, im in ims.items():
        px, py = pos[n]
        im = im.resize((im.width * k // 16, im.height * k // 16), Image.LANCZOS)
        X, Y = (px - x0) * k + 10, (py - y0) * k + 10
        ov.paste(im, (X, Y))
        d.rectangle([X, Y, X + im.width - 1, Y + im.height - 1], outline=(255, 255, 255))
        d.text((X + 3, Y + 3), n.replace("_", " "), fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
    d.text((10, ov.height - 16), "edge connections as FRLG + invented Sea Routes C / D; Icefall Cave and the "
                                 "Rocket Warehouse drawn beside their doors (warps only); Six Island group shifted east for legibility", fill=(0, 0, 0))
    rms = [Image.open(os.path.join(OUT, "sevii%s_region_map@4x.png" % k_)).convert("RGB") for k_ in ("45", "67")]
    h = ov.height // 2
    rms = [r.resize((int(r.width * h / r.height), h), Image.NEAREST) for r in rms]
    out = Image.new("RGB", (rms[0].width + ov.width + 10, ov.height), (255, 255, 255))
    out.paste(rms[0], (0, 0))
    out.paste(rms[1], (0, h))
    out.paste(ov, (rms[0].width + 10, 0))
    out.save(os.path.join(OUT, "overview.png"))


STEPS = ("maps", "routes", "overview", "regionmap", "ice", "probe")


def main(args):
    steps = [a for a in args if a in STEPS] or ["maps", "routes", "overview", "regionmap"]
    names = [a for a in args if not a.startswith("--") and a not in STEPS] or list(MAPS)
    os.makedirs(OUT, exist_ok=True)
    if "regionmap" in steps:
        for k in ("45", "67"):
            region_map(k)
    grids = {}
    if "maps" in steps or "routes" in steps:
        grids = translate_maps(names if "maps" in steps else list(SEA_ROUTE_NEIGHBOURS.values()),
                               "--seams" in args)
    if "routes" in steps:
        sea_routes(grids)
    if "overview" in steps:
        overview()
    if "ice" in steps:
        ice()
    if "probe" in steps:
        probe()


if __name__ == "__main__":
    main(sys.argv[1:])
