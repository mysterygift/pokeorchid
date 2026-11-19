"""
Batch 2 (Sevii Islands 1-3), v2: FAITHFUL translations of the FRLG maps with frlg_translate.py (same size,
same layout, FRLG events). v1 (hand-composed) is kept in out/batch2_v1/ for comparison.

usage: <venv python> dev_scripts/voyages/mock_batch2.py [MapName ...] [--seams]
       -> out/batch2/<map>.png, @2x, <map>_vs_frlg.png, <map>_spec.json, overview.png, sevii123_region_map@4x.png
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import voyage_compose as vc      # noqa: E402
import frlg_translate as ft      # noqa: E402
import sea_routes as sr          # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

OUT = os.path.join(HERE, "out", "batch2")
RM = os.path.join(vc.ROOT, "graphics", "pokenav", "region_map")

# FRLG map -> Emerald pair. Cluster 1-3 is General + Rustboro (Route 104 coast, Briney's pier planks for
# FRLG's boardwalks and Bond Bridge, Petalburg Woods trees for Berry Forest, Route 116's cave mouth).
# Mt. Ember is General + Lavaridge (user: "use Mt Chimney tiles for Mt Ember"); it is reached only by
# warps, so no edge has to match.
MAPS = {
    "OneIsland": "sevii",
    "OneIsland_KindleRoad": "sevii",
    "OneIsland_TreasureBeach": "sevii",
    "MtEmber_Exterior": "lavaridge",
    "MtEmber_Summit": "lavaridge",
    "TwoIsland": "sevii",
    "TwoIsland_CapeBrink": "sevii",
    "ThreeIsland": "sevii",
    "ThreeIsland_BondBridge": "sevii",
    "ThreeIsland_Port": "sevii",
    "ThreeIsland_BerryForest": "sevii",
}
# forced building stamps {map: {warp index: name}} (defaults: ft.choose_building)
BUILDING_CHOICE = {
    "TwoIsland": {0: "flowershop", 1: "house"},
}
# Berry Forest's autumn trees come in many pieces; every impassable cell of that tileset is a tree
ft.override_impassable("BerryForest", "T", ["ThreeIsland_BerryForest"])
# extra stamps: One Island's harbour dock (stamped at One Island's bottom row) continues into the top
# rows of Treasure Beach, which FRLG also draws there
EXTRA_PSTAMPS = {}
EXTRA_STAMPS = {"OneIsland_TreasureBeach": [(ft.SI_EXT, 10, 22, 9, 3, 8, 0)]}
# virtual stamps of the proposed gTileset_SeviiIslands (sevii_tileset.py): Two Island's market stall back at
# FRLG's spot (a rare-goods shop; the clerk stands behind the counter)
VSTAMPS = {"TwoIsland": [("market_stall", 27, 1)]}
MOVE_MARKS = {"TwoIsland": {(28, 4): (28, 3)}}
# 3x detail crops under the side-by-side (map cells x0, y0, x1, y1)
ZOOM = {"TwoIsland_CapeBrink": (6, 17, 17, 30)}
# extra marks per map (Sailor + boat at One Island's harbour walkway; harbour = FRLG's Seagallop warp)
EXTRA_MARKS = {
    "OneIsland": [(11, 17, "Sailor", "sailor", "sailor_right"), (9, 17, "boat", "boat", "boat_right")],
}


def region_map():
    t = Image.open(os.path.join(RM, "map_sevii_123.png"))
    b = open(os.path.join(RM, "map_sevii_123.bin"), "rb").read()
    cols = t.width // 8
    im = Image.new("P", (512, 512))
    im.putpalette(t.getpalette())
    for i, v in enumerate(b):
        im.paste(t.crop(((v % cols) * 8, (v // cols) * 8, (v % cols) * 8 + 8, (v // cols) * 8 + 8)),
                 ((i % 64) * 8, (i // 64) * 8))
    im = im.convert("RGB").crop((0, 0, 240, 160))
    src = open(os.path.join(vc.ROOT, "src", "data", "region_map", "region_map_layout_sevii123.h")).read()
    rows = [re.findall(r"MAPSEC_\w+", r) for r in src.split("\n")[1:16]]
    S = 4
    big = im.resize((240 * S, 160 * S), Image.NEAREST)
    d = ImageDraw.Draw(big)
    secs = {}
    for y, r in enumerate(rows):
        for x, s in enumerate(r):
            if s != "MAPSEC_NONE":
                secs.setdefault(s, []).append((x, y))
                X, Y = (x + 1) * 8 * S, (y + 2) * 8 * S
                d.rectangle([X, Y, X + 8 * S - 1, Y + 8 * S - 1], outline=(200, 30, 30))
    for s, cells in secs.items():
        x, y = min(cells)
        d.text(((x + 1) * 8 * S + 2, (y + 2) * 8 * S + 2), s[7:].replace("_", " ").title(), fill=(0, 0, 0),
               stroke_width=2, stroke_fill=(255, 255, 255))
    big.save(os.path.join(OUT, "sevii123_region_map@4x.png"))


# overview: each island's FRLG connection chain laid out by its offsets (map tiles); the three islands
# are not edge-connected in FRLG (Seagallop only), so their groups are placed by region-map cell (~24 tiles
# per cell, as FRLG's Sevii maps).
CELL = 24


def overview_positions():
    P = {}
    # One Island at its cell (1,8); Kindle Road to its right with offset -120; Treasure Beach below (0)
    P["OneIsland"] = (1 * CELL, 8 * CELL)
    P["OneIsland_KindleRoad"] = (P["OneIsland"][0] + 24, P["OneIsland"][1] - 120)
    P["OneIsland_TreasureBeach"] = (P["OneIsland"][0], P["OneIsland"][1] + 20)
    # Mt. Ember (warp from Kindle Road's top) drawn above Kindle Road, summit (warp) to its right
    P["MtEmber_Exterior"] = (P["OneIsland_KindleRoad"][0] - 16, P["OneIsland_KindleRoad"][1] - 56)
    P["MtEmber_Summit"] = (P["MtEmber_Exterior"][0] + 60, P["MtEmber_Exterior"][1])
    # Two Island at (9,9); Cape Brink above, offset 24 (Cape x = Two x + 24)
    P["TwoIsland"] = (8 * CELL, 9 * CELL)
    P["TwoIsland_CapeBrink"] = (P["TwoIsland"][0] + 24, P["TwoIsland"][1] - 40)
    # Three Island at (18,12); Bond Bridge to its left (offset 0), Port below (0); Berry Forest by warp
    P["ThreeIsland"] = (18 * CELL, 11 * CELL)
    P["ThreeIsland_BondBridge"] = (P["ThreeIsland"][0] - 96, P["ThreeIsland"][1])
    P["ThreeIsland_Port"] = (P["ThreeIsland"][0], P["ThreeIsland"][1] + 40)
    P["ThreeIsland_BerryForest"] = (P["ThreeIsland_BondBridge"][0] - 20, P["ThreeIsland_BondBridge"][1] - 50)
    # invented sea routes at their connection offsets (Route B's east end meets Three Isle Port in the game;
    # the Three Island group stays at its region-map cell here so Bond Bridge doesn't cover Two Island)
    ca = SEA_ROUTES["sevii_sea_route_a"]["conns"]
    P["sevii_sea_route_a"] = (P["OneIsland_KindleRoad"][0] + 24, P["OneIsland_KindleRoad"][1] - ca[0][1])
    P["TwoIsland"] = (P["sevii_sea_route_a"][0] + 40, P["sevii_sea_route_a"][1] - ca[1][1])
    P["TwoIsland_CapeBrink"] = (P["TwoIsland"][0] + 24, P["TwoIsland"][1] - 40)
    cb = SEA_ROUTES["sevii_sea_route_b"]["conns"]
    P["sevii_sea_route_b"] = (P["TwoIsland"][0] + cb[0][1], P["TwoIsland"][1] + 20)
    return P


def overview(sizes):
    rm = Image.open(os.path.join(OUT, "sevii123_region_map@4x.png")).convert("RGB")
    k = 2
    pos = overview_positions()
    xs = [p[0] for p in pos.values()] + [pos[n][0] + sizes[n][0] for n in pos]
    ys = [p[1] for p in pos.values()] + [pos[n][1] + sizes[n][1] for n in pos]
    x0, y0 = min(xs), min(ys)
    ov = Image.new("RGB", ((max(xs) - x0) * k + 20, (max(ys) - y0) * k + 20), (98, 172, 224))
    d = ImageDraw.Draw(ov)
    for n, (px, py) in pos.items():
        im = Image.open(os.path.join(OUT, ft.snake(n) + ".png")).convert("RGB")
        im = im.resize((im.width * k // 16, im.height * k // 16), Image.LANCZOS)
        X, Y = (px - x0) * k + 10, (py - y0) * k + 10
        ov.paste(im, (X, Y))
        d.rectangle([X, Y, X + im.width - 1, Y + im.height - 1], outline=(255, 255, 255))
        d.text((X + 3, Y + 3), n.replace("_", " "), fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
    d.text((10, ov.height - 16), "edge connections as FRLG + invented Sevii Sea Routes A / B (walled by sea "
                                 "rocks); harbours = ferry", fill=(0, 0, 0))
    s = ov.height / rm.height
    rm2 = rm.resize((int(rm.width * s), ov.height), Image.NEAREST)
    out = Image.new("RGB", (rm2.width + ov.width + 10, ov.height), (255, 255, 255))
    out.paste(rm2, (0, 0))
    out.paste(ov, (rm2.width + 10, 0))
    out.save(os.path.join(OUT, "overview.png"))


# invented Surf routes (user 2026-11-19: keep sea routes between the islands, walled by sea rocks). v1's Sea
# Routes A / B were drawn for v1's hand-made islands; these are rebuilt in the same style to meet the FRLG-size
# islands' real sea edges. (direction, offset, neighbour, opening along that edge in route coordinates)
SEA_ROUTES = {
    # Kindle Road's east coast (rows 125-132, beside One Island) -> Two Island's west sea (rows 3-10)
    "sevii_sea_route_a": sr.route_spec(
        "Sevii Sea Route A", (40, 12), corridor=[(0, 2, 40, 8)], islets=[(16, 4, 6, 4)],
        conns=[("left", -123, "MAP_ONE_ISLAND_KINDLE_ROAD", (2, 9)), ("right", -1, "MAP_TWO_ISLAND", (2, 9))],
        marks=[(18, 5, "", "item", "item"), (8, 6, "", "npc", "swimmer"), (30, 3, "", "npc", "swimmer")]),
    # Two Island's south-west sea (x4-11) down, then east to Three Isle Port's west sea (rows 10-17)
    "sevii_sea_route_b": sr.route_spec(
        "Sevii Sea Route B", (36, 22), corridor=[(2, 0, 8, 20), (2, 12, 34, 8)], islets=[(20, 14, 6, 4)],
        conns=[("up", -2, "MAP_TWO_ISLAND", (2, 9)), ("right", 2, "MAP_THREE_ISLAND_PORT", (12, 19))],
        marks=[(22, 15, "", "item", "item"), (5, 6, "", "npc", "swimmer"), (14, 17, "", "npc", "swimmer"),
               (30, 13, "", "npc", "swimmer")]),
}
SEA_ROUTE_NEIGHBOURS = {"MAP_ONE_ISLAND_KINDLE_ROAD": "OneIsland_KindleRoad", "MAP_TWO_ISLAND": "TwoIsland",
                        "MAP_THREE_ISLAND_PORT": "ThreeIsland_Port"}


def sea_routes(grids, routes=SEA_ROUTES, nbrs=SEA_ROUTE_NEIGHBOURS, out=None):
    """Render the invented routes and check every opening against the rendered islands."""
    out = out or OUT
    probs = []
    for key, spec in routes.items():
        nb = {m: grids[n] for m, n in nbrs.items() if n in grids}
        for m, o0, o1 in sr.autofit(spec, {m: nb[m] for _d, _o, m, _ab in spec["conns"]}):
            if o0 != o1:
                print("   %s: offset to %s moved %s -> %s (island sea rock in the way)" % (key, m[4:], o0, o1))
        g = vc.render(spec, os.path.join(out, key))
        probs += sr.check(spec, g, {m: grids[n] for m, n in nbrs.items() if n in grids})
        print("%-24s %3dx%-3d sevii     conns=%s" % (key, spec["size"][0], spec["size"][1],
                                                     [(c[0], c[1], c[2][4:]) for c in spec["conns"]]))
    for p in probs:
        print("   ROUTE CHECK:", p)
    return probs


def main(args):
    names = [a for a in args if not a.startswith("--")] or list(MAPS)
    os.makedirs(OUT, exist_ok=True)
    region_map()
    sizes, grids = {}, {}
    for n in names:
        fm = ft.load_map(n)
        spec = ft.translate(fm, MAPS[n], BUILDING_CHOICE.get(n), vstamps=VSTAMPS.get(n))
        mv = MOVE_MARKS.get(n, {})
        spec["marks"] = [((mv[(m[0], m[1])] + tuple(m[2:])) if (m[0], m[1]) in mv else m) for m in spec["marks"]]
        spec["marks"] += EXTRA_MARKS.get(n, [])
        spec["stamps"] += EXTRA_STAMPS.get(n, [])
        const = [m for m, nn in SEA_ROUTE_NEIGHBOURS.items() if nn == n]
        if const:                           # clear island sea rocks in front of a sea-route opening
            gone = sr.clear_edge_rocks(spec, sr.island_openings(SEA_ROUTES).get(const[0], []))
            if gone:
                fm.report["sea_rocks_cleared_for_route"] = gone
                print("   %s: sea rocks cleared for a route opening at %s" % (n, gone))
        base = os.path.join(OUT, ft.snake(n))
        g = ft.render(spec, base)
        grids[n] = (g, spec["tileset"])
        ft.side_by_side(fm, base, zoom=ZOOM.get(n))
        ft.write_spec(spec, fm, base + "_spec.json")
        r = fm.report
        print("%-24s %3dx%-3d %-9s buildings=%d caves=%d rocks_dropped=%d" % (
            n, fm.w, fm.h, MAPS[n], len(r["buildings"]), len(r["caves"]), len(r.get("rocks_dropped", []))))
        if "--seams" in args:
            ss = vc.seams(g, spec["tileset"], ignore={0x001, 0x124, 0x170, 0x271})
            print("   seams: %d" % len(ss))
    if all(n in grids for n in SEA_ROUTE_NEIGHBOURS.values()):
        sea_routes(grids)
    for n in MAPS:
        fm = ft.load_map(n)
        sizes[n] = (fm.w, fm.h)
    for key, spec in SEA_ROUTES.items():
        sizes[key] = tuple(spec["size"])
    if not [a for a in args if not a.startswith("--")]:
        print("classes:", ft.classes_png(list(MAPS)))      # review table with this batch's overrides
    if all(os.path.exists(os.path.join(OUT, ft.snake(n) + ".png")) for n in MAPS):
        overview(sizes)


if __name__ == "__main__":
    main(sys.argv[1:])
