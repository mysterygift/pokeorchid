#!/usr/bin/env python3
"""
Placeholder maps for the Tiksi routes (Route 401-410) and Tanoby Delta, laid out from the user's
Tiksi region-map tagging (dev_scripts/region_map_tagger/tags_tiksi.json) and terrain art.

Each map covers its section's bounding box on the region grid, s tiles per cell (as large as the
engine's map-size limit allows, up to 30):
  - cells of the route are open ground (grass, tall grass); the rest of the box is forest
  - a 2-wide path runs centre to centre between the route's cells, and out to an opening on every
    edge that touches another tagged place (connections are left to the user)
  - sea is traced from tiksi_terrain.png (8 px per cell), with a sand fringe, so coastal routes
    follow the user's coastline
  - dressed like the Tosa routes (dress.py): path / pond / shore edges, groves, ledges, flowers
  - a route sign quoting the tagger notes and one NPC each

Tanoby Delta nods to Sevii's Tanoby Ruins: a beach, then open water (Surf) with islets that each hold
a sealed stone chamber, the biggest at the centre. The chamber facade is FRLG's Tanoby art, ported by
port_tanoby.py into gTileset_TanobyDelta; everything else there is Emerald General. Maps edited since generation
(tiksi_routes.json hashes) are skipped unless --force.
usage: python3 dev_scripts/tiksi_maps/tiksi_routes.py [--force] [--only Route401,...]
"""
import hashlib
import json
import os
import random
import sys
from collections import OrderedDict, deque

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "dev_scripts", "tosa_maps"))
import placeholders as PH        # noqa: E402
import dress                     # noqa: E402
import towns as TW               # noqa: E402

P = PH.P
GROUP = "gMapGroup_Tiksi"
STATE = os.path.join(HERE, "tiksi_routes.json")
TAGS = P("dev_scripts", "region_map_tagger", "tags_tiksi.json")
TERRAIN = P("dev_scripts", "orchid_ui", "ref", "tiksi_terrain.png")
G = lambda s: "OBJ_EVENT_GFX_" + s

# name -> (section, music, npc gfx, npc line, extra)
ROUTES = OrderedDict([
    ("Route401", ("MAPSEC_ROUTE_401", "MUS_ROUTE104", "FISHERMAN",
                  "You came on that boat? Nobody comes to Tiksi on purpose. Furong's just east of here, if you need a bed.", {})),
    ("Route402", ("MAPSEC_ROUTE_402", "MUS_ROUTE110", "HIKER",
                  "Mt. Drake starts just north of here. Its peaks are higher than anything in Tosa.", {})),
    ("Route403", ("MAPSEC_ROUTE_403", "MUS_DESERT", "CAMPER",
                  "The shrine up north sits in the middle of a desert. The locals won't go near it.", {})),
    ("Route404", ("MAPSEC_ROUTE_404", "MUS_ROUTE110", "HIKER",
                  "Drake Base Camp is where climbers rest before Mt. Drake. Warm stew, cold nights.", {})),
    ("Route405", ("MAPSEC_ROUTE_405", "MUS_ROUTE120", "PICNICKER",
                  "Ube City is south of here. It's the only city in Tiksi. Silph Co. even has an office there!", {})),
    ("Route406", ("MAPSEC_ROUTE_406", "MUS_ROUTE120", "BUG_CATCHER",
                  "Tanglyn Town is at the east end. Have you seen the murals there? They're older than Tosa!", {})),
    ("Route407", ("MAPSEC_ROUTE_407", "MUS_ROUTE104", "LASS",
                  "Ube City's to the north and Furong Village is south. This road joins the two.", {})),
    ("Route408", ("MAPSEC_ROUTE_408", "MUS_ROUTE104", "SAILOR",
                  "This road follows the shore of the bay. On a calm day you can see right across the water.", {})),
    ("Route409", ("MAPSEC_ROUTE_409", "MUS_ROUTE113", "HEX_MANIAC",
                  "Feel that chill? Tiksi is warm everywhere else. The cold comes from the cave at the end of this route…", {"cold": True})),
    ("Route410", ("MAPSEC_ROUTE_410", "MUS_ROUTE120", "OLD_MAN",
                  "Hm? You found this path? Only us locals know about it. It leads down to the delta.", {"hidden": True})),
    ("TanobyDelta", ("MAPSEC_TANOBY_DELTA", "MUS_ROUTE119", "SCIENTIST_1",
                     "Nobody knows who built the ruin out there. Some say people came from across the sea, long before Tiksi had towns.", {"delta": True})),
])


def tags():
    t = json.load(open(TAGS))
    names = {a["key"]: a for a in t["areas"]}
    grid = {(x, y): names[k]["id"] for y, row in enumerate(t["grid"]) for x, k in enumerate(row) if k}
    notes = {names[k]["id"]: (names[k]["name"], names[k].get("notes") or "") for k in names}
    return grid, notes


def cell_size(cols, rows):
    for s in range(30, 9, -2):
        if (cols * s + 15) * (rows * s + 14) <= PH.MAX_MAP_DATA:
            return s
    raise SystemExit("too big")


def sea_mask(cells_box, s, w, h):
    from PIL import Image
    im = Image.open(TERRAIN).convert("RGB")
    px = im.load()
    (cx0, cy0) = cells_box
    out = set()
    for y in range(h):
        for x in range(w):
            ix = 8 + 8 * cx0 + int(x * 8 / s)
            iy = 16 + 8 * cy0 + int(y * 8 / s)
            r, g, b = px[min(ix, im.width - 1), min(iy, im.height - 1)]
            if b > 180 and b > r + 30 and b > g:
                out.add((x, y))
    return out


def sea_cell(cx, cy):
    """True if region-grid cell (cx, cy) of the terrain art is at least half sea."""
    from PIL import Image
    px = Image.open(TERRAIN).convert("RGB").load()
    n = 0
    for j in range(8):
        for i in range(8):
            r, g, b = px[8 + 8 * cx + i, 16 + 8 * cy + j]
            n += b > 180 and b > r + 30 and b > g
    return n >= 32


RUIN_TEXT = ("An ancient stone chamber. Strange carvings cover the sealed doorway."
             "\\pIt's said the delta's ruins were built by people who came from across the sea.")


FACADE = [[0x0400 | (0x200 + r * 3 + c) for c in range(3)] for r in range(4)]   # gTileset_TanobyDelta


def build_delta(name, grid, sec):
    """Tanoby Delta, after Sevii's Tanoby Ruins: the river from Route 410 reaches a beach, then open water
    (Surf) with islets, each holding a sealed stone chamber. The chamber facade is the FRLG Tanoby art
    (gTileset_TanobyDelta, dev_scripts/tiksi_maps/port_tanoby.py) set into an Emerald rock mound; sand,
    sea, shore and rocks are Emerald General tiles."""
    w, h = 44, 36
    cv = PH.Canvas(w, h, "W")
    mx = (w // 2) & ~1
    cv.rect(0, 0, w - 1, 7, "X")                     # forest along the top, the way in from Route 410
    cv.rect(mx - 8, 2, mx + 9, 7, "G")
    cv.rect(mx - 10, 8, mx + 11, 10, "S")            # the beach
    for y in range(0, 10):
        cv.set(mx, y, "P"); cv.set(mx + 1, y, "P")
    signs = [((mx + 3, 5), "Tanoby Delta\nA river delta with a mysterious ruin at its centre.")]
    cv.set(mx + 3, 5, "N")

    def islet(cx, cy, rx, ry, big):
        for y in range(cy - ry, cy + ry + 1):
            for x in range(cx - rx, cx + rx + 1):
                d = ((x - cx) / (rx + 0.5)) ** 2 + ((y - cy) / (ry + 0.5)) ** 2
                if d <= 1:
                    cv.set(x, y, "G" if big and d < 0.35 else "S")
        # rock mound with the chamber facade set into it; the facade's bottom row stands on the sand
        fy = cy - 1                                  # facade bottom row
        side = 2 if big else 1
        cv.rect(cx - 1 - side, fy - 4 - (1 if big else 0), cx + 1 + side, fy - 1, "R")
        cv.stamp(cx - 1, fy - 3, FACADE)
        signs.append(((cx, fy), RUIN_TEXT))

    islet(mx + 1, 23, 7, 5, True)                    # the central ruin
    for cx, cy in ((9, 18), (35, 17), (10, 30), (34, 30)):
        islet(cx, cy, 3, 3, False)
    blocks = PH.render(cv, "route")
    return dict(blocks=blocks, w=w, h=h, s=w, hub=(mx, 5), sign=None, signs=signs, secondary="gTileset_TanobyDelta",
                opens=[("N", (0, 0), (mx, 0), "MAPSEC_ROUTE_410")], cells={(0, 0)}, box=(0, 0, 1, 1))


def build(name, sec, extra, grid):
    if extra.get("delta"):
        return build_delta(name, grid, sec)
    cells = sorted(c for c, s_ in grid.items() if s_ == sec)
    xs, ys = [c[0] for c in cells], [c[1] for c in cells]
    cx0, cy0 = min(xs), min(ys)
    cols, rows = max(xs) - cx0 + 1, max(ys) - cy0 + 1
    s = cell_size(cols, rows)
    w, h = cols * s, rows * s
    rnd = random.Random("tiksi/" + name)
    cv = PH.Canvas(w, h, "X")
    local = {(x - cx0, y - cy0) for x, y in cells}
    centre = lambda c: (c[0] * s + s // 2 - 1, c[1] * s + s // 2 - 1)
    # open ground inside the route's cells (a 2-tile forest rim stays on the outer edges)
    for (lx, ly) in local:
        for y in range(ly * s, ly * s + s):
            for x in range(lx * s, lx * s + s):
                if 2 <= x < w - 2 and 2 <= y < h - 2:
                    cv.t[y][x] = "G"
    # openings: every edge of a route cell that touches another tagged place
    opens = []
    for (lx, ly) in local:
        for d, (dx, dy) in (("N", (0, -1)), ("S", (0, 1)), ("W", (-1, 0)), ("E", (1, 0))):
            n = (lx + dx + cx0, ly + dy + cy0)
            if (lx + dx, ly + dy) in local or n not in grid:
                continue
            mx, my = centre((lx, ly))
            edge = {"N": (mx, 0), "S": (mx, h - 2), "W": (0, my), "E": (w - 2, my)}[d]
            opens.append((d, (lx, ly), edge, grid[n]))
    # path: spanning tree over the cells from the most central one
    hub = min(local, key=lambda c: abs(c[0] - (cols - 1) / 2) + abs(c[1] - (rows - 1) / 2))
    seen, q, links = {hub}, deque([hub]), []
    while q:
        c = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (c[0] + dx, c[1] + dy)
            if n in local and n not in seen:
                seen.add(n)
                q.append(n)
                links.append((c, n))
    hidden = extra.get("hidden")
    for a, b in links:
        cv.path(centre(a), centre(b))
    for d, c, edge, _ in opens:
        mx, my = centre(c)
        if d in "NS":
            for y in range(min(my, edge[1]), max(my, edge[1]) + 2):
                cv.set(mx, y, "P"); cv.set(mx + 1, y, "P")
        else:
            for x in range(min(mx, edge[0]), max(mx, edge[0]) + 2):
                cv.set(x, my, "P"); cv.set(x, my + 1, "P")
    # tall grass, scattered trees (dense along a hidden route)
    keep = ("P", "X", "W", "S", "R")
    area = sum(1 for row in cv.t for c in row if c == "G")
    for _ in range(area // (110 if not hidden else 400)):
        cv.blob(rnd, rnd.randrange(3, w - 3), rnd.randrange(3, h - 3), rnd.randint(2, 4), "T", keep)
    if hidden:                                   # forest closes in on the path
        for by in range(h // 2):
            for bx in range(w // 2):
                x, y = bx * 2, by * 2
                if all(cv.ok(x + i, y + j) and cv.t[y + j][x + i] in ("G", "T") for i in (0, 1) for j in (0, 1)) and \
                        not any(cv.ok(x + i, y + j) and cv.t[y + j][x + i] == "P" for i in range(-2, 4) for j in range(-2, 4)):
                    cv.rect(x, y, x + 1, y + 1, "X")
    # sea from the art, sand fringe on the land side (never over the path)
    sea = sea_mask((cx0, cy0), s, w, h)
    # a shoreline band along any side of a route cell whose neighbouring cell in the art is mostly sea
    for (lx, ly) in local:
        for (dx, dy) in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if (lx + dx, ly + dy) in local or not sea_cell(cx0 + lx + dx, cy0 + ly + dy):
                continue
            band = max(4, s // 5)
            for k in range(band):
                for t in range(s):
                    x = lx * s + (t if dx == 0 else (s - 1 - k if dx > 0 else k))
                    y = ly * s + (t if dy == 0 else (s - 1 - k if dy > 0 else k))
                    sea.add((x, y))
    for (x, y) in sea:
        if cv.t[y][x] != "P":
            cv.t[y][x] = "W"
    for y in range(h):
        for x in range(w):
            if cv.t[y][x] in ("G", "T", "X") and any((x + dx, y + dy) in sea for dx in (-2, -1, 0, 1, 2) for dy in (-2, -1, 0, 1, 2)):
                cv.t[y][x] = "S"
    # sign and NPC near the hub
    hx, hy = centre(hub)
    sign = None
    for dx, dy in ((3, 3), (-3, 3), (3, -3), (-3, -3), (4, 0), (-4, 0)):
        x, y = hx + dx, hy + dy
        if cv.ok(x, y) and cv.t[y][x] in ("G", "T", "S"):
            cv.t[y][x] = "N"
            sign = (x, y)
            break
    blocks = PH.render(cv, "route")
    return dict(blocks=blocks, w=w, h=h, s=s, hub=(hx, hy), sign=sign, signs=[], opens=opens, cells=local,
                box=(cx0, cy0, cols, rows))


def npc_spot(b, w, h, near, avoid):
    best = None
    for y in range(3, h - 3):
        for x in range(3, w - 3):
            v = b[y * w + x]
            if (v >> 10) & 3 or (v & 0x3FF) not in (0x001, 0x00D, 0x124):
                continue
            if any(abs(x - a) + abs(y - c) < 3 for a, c in avoid):
                continue
            d = abs(x - near[0]) + abs(y - near[1])
            if best is None or d < best[0]:
                best = (d, x, y)
    return best[1:]


def main():
    force = "--force" in sys.argv
    only = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
    grid, notes = tags()
    state = json.load(open(STATE)) if os.path.exists(STATE) else {}
    lj_path = P("data", "layouts", "layouts.json")
    lj = json.load(open(lj_path), object_pairs_hook=OrderedDict)
    mg_path = P("data", "maps", "map_groups.json")
    mg = json.load(open(mg_path), object_pairs_hook=OrderedDict)
    es_path = P("data", "event_scripts.s")
    es = open(es_path).read()
    for name, (sec, music, gfx, line, extra) in ROUTES.items():
        if only and name not in only:
            continue
        mpath, bpath = P("data", "maps", name, "map.json"), P("data", "layouts", name, "map.bin")
        if name in state and not force:
            cur = hashlib.sha1((open(mpath).read() + open(bpath, "rb").read().hex()).encode()).hexdigest() \
                if os.path.exists(mpath) and os.path.exists(bpath) else None
            if cur != state[name]:
                print("%-12s edited since generated: skipped (--force to rebuild)" % name)
                continue
        r = build(name, sec, extra, grid)
        w, h = r["w"], r["h"]
        title, note = notes[sec]
        events = [r["sign"]] if r["sign"] else []
        events += [xy for xy, _ in r["signs"]]
        nx, ny = npc_spot(r["blocks"], w, h, (r["hub"][0] - 3, r["hub"][1] + 1), events)
        events.append((nx, ny))
        blocks = dress.apply(r["blocks"], w, h, "dirt", events, name, ledges=0 if extra.get("delta") else w * h // 600,
                             flowers=w * h // 300, groves=0, rocks=True)
        old_conn = json.load(open(mpath)).get("connections") if os.path.exists(mpath) else None
        PH.write_bin(bpath, blocks)
        PH.write_bin(P("data", "layouts", name, "border.bin"), PH.OUTDOOR[2])
        lid = "LAYOUT_" + PH.snake(name)
        lj["layouts"] = [l for l in lj["layouts"] if l.get("id") != lid] + [OrderedDict([
            ("id", lid), ("name", name + "_Layout"), ("width", w), ("height", h),
            ("primary_tileset", "gTileset_General"), ("secondary_tileset", r.get("secondary", "gTileset_TosaPort")),
            ("border_filepath", "data/layouts/%s/border.bin" % name),
            ("blockdata_filepath", "data/layouts/%s/map.bin" % name), ("layout_version", "emerald")])]
        text = title + ("\n" + note if note else "")
        pory = "mapscripts %s_MapScripts {}\n\n" % name
        bg = []
        if r["sign"]:
            pory += TW.msg(name + "_EventScript_Sign", text, "MSGBOX_SIGN")
            bg.append(OrderedDict([("type", "sign"), ("x", r["sign"][0]), ("y", r["sign"][1]), ("elevation", 0),
                                   ("player_facing_dir", "BG_EVENT_PLAYER_FACING_ANY"), ("script", name + "_EventScript_Sign")]))
        for k, ((sx, sy), stext) in enumerate(r["signs"]):
            label = "%s_EventScript_Sign%d" % (name, k + 1)
            pory += TW.msg(label, stext, "MSGBOX_SIGN")
            bg.append(OrderedDict([("type", "sign"), ("x", sx), ("y", sy), ("elevation", 0),
                                   ("player_facing_dir", "BG_EVENT_PLAYER_FACING_ANY"), ("script", label)]))
        pory += TW.msg(name + "_EventScript_Npc1", line, "MSGBOX_NPC")
        m = OrderedDict([
            ("id", "MAP_" + PH.snake(name)), ("name", name), ("layout", lid), ("music", music),
            ("region", "REGION_HOENN"), ("region_map_section", sec), ("requires_flash", False),
            ("weather", "WEATHER_SUNNY"), ("map_type", "MAP_TYPE_ROUTE"), ("allow_cycling", True),
            ("allow_escaping", False), ("allow_running", True), ("show_map_name", True),
            ("battle_scene", "MAP_BATTLE_SCENE_NORMAL"), ("connections", old_conn),
            ("object_events", [TW.obj(G(gfx), nx, ny, 3, "look", name + "_EventScript_Npc1")]),
            ("warp_events", []), ("coord_events", []), ("bg_events", bg)])
        PH.write_json(mpath, m)
        TW.write_pory(name, pory)
        if name not in mg[GROUP]:
            mg[GROUP].append(name)
        inc = '\t.include "data/maps/%s/scripts.inc" @ tiksi-routes\n' % name
        if inc not in es:
            lines = [l for l in es.split("\n") if "@ tiksi" in l]
            anchor = lines[-1] + "\n"
            es = es.replace(anchor, anchor + inc)
        state[name] = hashlib.sha1((open(mpath).read() + open(bpath, "rb").read().hex()).encode()).hexdigest()
        print("%-12s %3dx%-3d (%d px/cell, %dx%d cells) opens %s" % (
            name, w, h, r["s"], r["box"][2], r["box"][3], [(d, notes[n][0]) for d, _, _, n in r["opens"]]))
    PH.write_json(lj_path, lj)
    PH.write_json(mg_path, mg)
    open(es_path, "w").write(es)
    json.dump(state, open(STATE, "w"), indent=1)


if __name__ == "__main__":
    main()
