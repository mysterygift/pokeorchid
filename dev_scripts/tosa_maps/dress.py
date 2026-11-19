#!/usr/bin/env python3
"""
Detail pass for the generated Tosa outdoor maps: turns the flat placeholder terrain into vanilla-style
Gen 3 ground, using only General-primary metatiles (so it works on any outdoor secondary).

  - paths become bordered dirt roads (Route 101 / Petalburg, 0x118 set; road="light" gives the pale
    0x1D0 grass path instead)
  - ponds are squared to the 2x2 grid and get banks (0x0B0 set, with the 0x002 lip on the grass below); sea next to sand gets a
    shoreline (0x11B set); open sea gets the odd rock
  - tree tops peek into the row above the tree line (0x1CE/0x1CF, 0x1C6/0x1C7 in tall grass)
  - routes / reserves get short one-way ledges and flower patches in open grass

apply() is used by towns.py on freshly rendered towns. Run as a script it dresses the placeholder
routes and landmarks in ROUTES, keeping the undressed blocks in dress_state.json so re-runs give the
same result; a map changed since it was dressed (e.g. in Porymap) is skipped.

usage: python3 dev_scripts/tosa_maps/dress.py [--only Name,Name]
"""
import hashlib
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import placeholders as PH        # noqa: E402

STATE = os.path.join(HERE, "dress_state.json")

E0C1, E1, E3 = 0x0400, 0x1000, 0x3000          # collision 1 elev 0 / elev 1 (water) / elev 3 (ground)
ROUTE_PATH = {"TL": 0x1D0, "T": 0x1D1, "TR": 0x1D2, "L": 0x1D8, "C": 0x1D9, "R": 0x1DA, "BL": 0x1E0, "B": 0x1E1, "BR": 0x1E2}
DIRT_PATH = {"TL": 0x118, "T": 0x119, "TR": 0x11A, "L": 0x120, "C": 0x121, "R": 0x122, "BL": 0x128, "B": 0x129, "BR": 0x12A}
POND = {"TL": 0x0B0, "T": 0x0B1, "TR": 0x0B2, "L": 0x0B8, "C": 0x0A1, "R": 0x0BA, "INL": 0x0C0, "INR": 0x0C2}
POND_LIP = 0x002
SHORE = {"S": 0x11C, "N": 0x12C, "E": 0x123, "W": 0x125, "NE": 0x145, "NW": 0x146,
         "dSE": 0x11B, "dSW": 0x11D, "dNE": 0x12B, "dNW": 0x12D}
SAND_IN = {"NW": 0x13D, "NE": 0x13E}
SEA, SAND, GRASS, TALL, FLOWER = 0x170, 0x124, 0x001, 0x00D, 0x004
ROCKS = ([[0x150, 0x151], [0x158, 0x159]], [[0x175, 0x176], [0x17D, 0x17E]])
LEDGE = (0x0D5, 0x087, 0x0D6)
TREE_TOP = {0x1D4: 0, 0x1D6: 0, 0x1E4: 0, 0x1E6: 0, 0x1D5: 1, 0x1D7: 1, 0x1E5: 1, 0x1E7: 1}
PEEK = {"G": (0x1CE, 0x1CF), "T": (0x1C6, 0x1C7)}

# what each id means when reading a map back (dressed or not)
CLASS = {}
for _ids, _c in ((ROUTE_PATH.values(), "P"), (DIRT_PATH.values(), "P"), (POND.values(), "Q"),
                 (SHORE.values(), "W"), ((SEA,), "W"), ((SAND,) + tuple(SAND_IN.values()), "S"),
                 ((GRASS, POND_LIP, 0x1CE, 0x1CF), "G"), ((TALL, 0x1C6, 0x1C7), "T")):
    for _i in _ids:
        CLASS[_i] = _c

# placeholder routes / landmarks this script dresses (towns are dressed by towns.py)
ROUTES = {n: "route" for n in ("Route302", "Route303", "Route304", "Route305", "Route306", "Route307", "Route308",
                               "Route309", "Route310", "Route311_West", "Route311_East")}
ROUTES.update({"Route312": "sea", "Route313": "sea", "Route314": "sea", "MoongroveMarsh": "marsh",
               "GalangalForest": "forest", "KantuFalls": "falls", "NorthTosaReserve": "route",
               "EastTosaReserve": "route", "ChallengersTrail_Cliffs": "rocky"})


def classify(vals):
    return ["O" if (v >> 10) & 3 and (v & 0x3FF) not in CLASS else CLASS.get(v & 0x3FF, "O") for v in vals]


def apply(vals, w, h, road="dirt", avoid=(), seed="", ledges=0, flowers=0, rocks=True, groves=0):
    """Return a dressed copy of the block list. `avoid`: event tiles to keep clear of new obstacles.
    Ledges / flower patches / rocks are placed only on undressed input (count > 0)."""
    rnd = random.Random("dress/" + seed)
    vals = _groves(list(vals), w, h, groves, rnd, list(avoid))
    cls = classify(vals)
    at = lambda x, y: cls[y * w + x]
    ok = lambda x, y: 0 <= x < w and 0 <= y < h

    def cell(x, y, edge):
        return at(x, y) if ok(x, y) else edge

    # sea that touches no sand but sits in land (e.g. a marsh pool drawn with the sea tile) -> pond
    for y in range(h):
        for x in range(w):
            if at(x, y) == "W" and _pondish(cls, w, h, x, y):
                cls[y * w + x] = "Q"
    _square_ponds(cls, w, h, set(avoid))

    # --- normalise water so every pond / shore cell has a tile
    changed = True
    while changed:
        changed = False
        for y in range(h):
            for x in range(w):
                c = at(x, y)
                if c == "W":
                    sn = [cell(x + dx, y + dy, "W") == "S" for dx, dy in ((0, -1), (0, 1), (1, 0), (-1, 0))]
                    if (sn[0] and sn[1]) or (sn[2] and sn[3]) or (sn[1] and (sn[2] or sn[3])):
                        cls[y * w + x] = "S"
                        changed = True
                elif c == "Q":
                    land = lambda dx, dy: cell(x + dx, y + dy, "Q") != "Q"
                    if land(-1, 0) and land(1, 0):
                        cls[y * w + x] = "G"
                        changed = True
    out = list(vals)
    for y in range(h):
        for x in range(w):
            c, i = at(x, y), y * w + x
            if c == "P":
                isp = lambda dx, dy: cell(x + dx, y + dy, "P") == "P"
                k = ("T" if not isp(0, -1) else "B" if not isp(0, 1) else "") + ("L" if not isp(-1, 0) else "R" if not isp(1, 0) else "")
                out[i] = E3 | (ROUTE_PATH if road == "light" else DIRT_PATH)[k or "C"]
            elif c == "Q":
                land = lambda dx, dy: cell(x + dx, y + dy, "Q") != "Q"
                n, wv, e = land(0, -1), land(-1, 0), land(1, 0)
                if n:
                    k = "TL" if wv else "TR" if e else "T"
                elif wv:
                    k = "L"
                elif e:
                    k = "R"
                elif land(-1, -1):
                    k = "INL"
                elif land(1, -1):
                    k = "INR"
                else:
                    k = "C"
                out[i] = E1 | POND[k]
            elif c == "W":
                sd = lambda dx, dy: cell(x + dx, y + dy, "W") == "S"
                n, s, e, wv = sd(0, -1), sd(0, 1), sd(1, 0), sd(-1, 0)
                k = ("NE" if n and e else "NW" if n and wv else "N" if n else "S" if s else "E" if e else "W" if wv else
                     "dSE" if sd(1, 1) else "dSW" if sd(-1, 1) else "dNE" if sd(1, -1) else "dNW" if sd(-1, -1) else None)
                out[i] = E1 | (SHORE[k] if k else SEA)
            elif c == "S":
                wt = lambda dx, dy: cell(x + dx, y + dy, "S") == "W"
                k = "NW" if wt(0, -1) and wt(-1, 0) else "NE" if wt(0, -1) and wt(1, 0) else None
                out[i] = E3 | (SAND_IN[k] if k else SAND)
            elif c == "G":
                out[i] = E3 | (POND_LIP if cell(x, y - 1, "G") == "Q" else GRASS)
            elif c == "T":
                out[i] = E3 | (POND_LIP if cell(x, y - 1, "T") == "Q" else TALL)
    # --- tree tops peek into the row above
    for y in range(h - 1):
        for x in range(w):
            c = cls[y * w + x]
            below = vals[(y + 1) * w + x] & 0x3FF
            if c in PEEK and below in TREE_TOP and (out[y * w + x] & 0x3FF) in (GRASS, TALL):
                out[y * w + x] = E3 | PEEK[c][TREE_TOP[below]]

    near = lambda x, y, r: any(abs(x - a) <= r and abs(y - b) <= r for a, b in avoid)
    plain = lambda x, y: ok(x, y) and cls[y * w + x] == "G" and (out[y * w + x] & 0x3FF) == GRASS
    walk = lambda x, y: ok(x, y) and cls[y * w + x] in ("G", "T", "P")

    # --- sea rocks well away from land and events
    if rocks:
        sea = [(x, y) for y in range(2, h - 3) for x in range(2, w - 3)
               if all(ok(x + dx, y + dy) and (out[(y + dy) * w + x + dx] & 0x3FF) == SEA for dx in range(-2, 4) for dy in range(-2, 4))]
        rnd.shuffle(sea)
        want, used = len(sea) // 260, []
        for x, y in sea:
            if want <= 0:
                break
            if near(x, y, 4) or any(abs(x - a) < 7 and abs(y - b) < 7 for a, b in used):
                continue
            if any((out[(y + dy) * w + x + dx] & 0x3FF) != SEA for dx in range(-2, 4) for dy in range(-2, 4)):
                continue
            rows = rnd.choice(ROCKS)
            for dy in range(2):
                for dx in range(2):
                    out[(y + dy) * w + x + dx] = E0C1 | rows[dy][dx]
            used.append((x, y))
            want -= 1

    # --- one-way ledges: short, with walkable ground all round, so they never cut a way off
    tries = 0
    while ledges > 0 and tries < 4000:
        tries += 1
        n = rnd.randint(3, 6)
        x, y = rnd.randrange(3, w - n - 3), rnd.randrange(4, h - 4)
        if not all(plain(x + k, y) for k in range(n)):
            continue
        if not all(walk(x + k, y + dy) for k in range(-1, n + 1) for dy in (-1, 1)) or not walk(x - 1, y) or not walk(x + n, y):
            continue
        if not all(plain(x + k, y + dy) for k in range(-1, n + 1) for dy in (-2, -1, 1, 2) if ok(x + k, y + dy) and cls[(y + dy) * w + x + k] != "T"):
            continue
        if any(near(x + k, y, 2) for k in range(n)):
            continue
        for k in range(n):
            out[y * w + x + k] = E0C1 | (LEDGE[0] if k == 0 else LEDGE[2] if k == n - 1 else LEDGE[1])
            cls[y * w + x + k] = "O"
        ledges -= 1

    # --- flower patches
    tries = 0
    while flowers > 0 and tries < 4000:
        tries += 1
        x, y = rnd.randrange(2, w - 4), rnd.randrange(2, h - 4)
        cells = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1), (x + 2, y), (x + 2, y + 1)][:rnd.randint(3, 6)]
        if not all(plain(cx, cy) for cx, cy in cells) or any(near(cx, cy, 1) for cx, cy in cells):
            continue
        for cx, cy in cells:
            if rnd.random() < 0.85:
                out[cy * w + cx] = E3 | FLOWER
                cls[cy * w + cx] = "O"
        flowers -= 1
    return out


def _groves(vals, w, h, count, rnd, avoid):
    """Clumps of 2-6 trees on the 2x2 grid in open grass, each kept only if no event is cut off."""
    T = PH.TREE
    bw, bh = w // 2, h // 2
    grass = lambda x, y: 0 <= x < w and 0 <= y < h and (vals[y * w + x] & 0x3FF) in (GRASS, TALL) and not (vals[y * w + x] >> 10) & 3
    clear = lambda bx, by: all(grass(bx * 2 + i, by * 2 + j) for i in range(-1, 3) for j in range(-1, 3)) and \
        not any(bx * 2 - 2 <= a <= bx * 2 + 3 and by * 2 - 2 <= b <= by * 2 + 3 for a, b in avoid)
    tries = 0
    while count > 0 and tries < 600:
        tries += 1
        bx, by = rnd.randrange(1, bw - 1), rnd.randrange(1, bh - 1)
        if not clear(bx, by):
            continue
        clump, edge = [(bx, by)], [(bx, by)]
        for _ in range(rnd.randint(1, 5)):
            cx, cy = rnd.choice(edge)
            nb = rnd.choice(((1, 0), (-1, 0), (0, 1), (0, -1), (1, 0)))
            c = (cx + nb[0], cy + nb[1])
            if c not in clump and 1 <= c[0] < bw - 1 and 1 <= c[1] < bh - 1 and clear(*c):
                clump.append(c)
                edge.append(c)
        new = list(vals)
        for cx, cy in clump:
            for j in (0, 1):
                for i in (0, 1):
                    new[(cy * 2 + j) * w + cx * 2 + i] = T[(i, j)]
        for cx, cy in clump:                     # a tree with a tree below overlaps it
            if (cx, cy + 1) in clump:
                for i in (0, 1):
                    new[(cy * 2 + 1) * w + cx * 2 + i] = PH.TREE_STACK[i]
        pts = [(a, b) for a, b in avoid if 0 <= a < w and 0 <= b < h]
        if same_links(vals, new, w, h, pts):
            vals = new
            count -= 1
    return vals


def _square_ponds(cls, w, h, avoid):
    """Ponds on the 2x2 grid (like vanilla's rectangular ponds): a block is water when at least two of
    its cells are, never over events, paths or obstacles; blocks with under two water neighbours dry up."""
    bw, bh = w // 2, h // 2
    cells = lambda bx, by: [(bx * 2 + i, by * 2 + j) for j in (0, 1) for i in (0, 1)]
    wet = {}
    for by in range(bh):
        for bx in range(bw):
            cs = cells(bx, by)
            n = sum(cls[y * w + x] == "Q" for x, y in cs)
            if n and all(cls[y * w + x] in ("Q", "G", "T") and (x, y) not in avoid for x, y in cs):
                wet[(bx, by)] = n >= 2
            elif n:
                wet[(bx, by)] = None             # mixed with something solid: leave as drawn
    for _ in range(2):
        for (bx, by), v in list(wet.items()):
            if v and sum(bool(wet.get((bx + dx, by + dy))) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))) < 2:
                wet[(bx, by)] = False
    for (bx, by), v in wet.items():
        if v is None:
            continue
        for x, y in cells(bx, by):
            if v:
                cls[y * w + x] = "Q"
            elif cls[y * w + x] == "Q":
                cls[y * w + x] = "G"


def _pondish(cls, w, h, x0, y0):
    """True if the sea component holding (x0, y0) touches no sand and no map edge."""
    seen, stack = {(x0, y0)}, [(x0, y0)]
    while stack:
        x, y = stack.pop()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < w and 0 <= ny < h):
                return False
            c = cls[ny * w + nx]
            if c == "S":
                return False
            if c == "W" and (nx, ny) not in seen:
                seen.add((nx, ny))
                stack.append((nx, ny))
        if len(seen) > 400:
            return False
    return True


def regions(vals, w, h, points):
    """Label of the dry, walkable region each point sits in (ledges count as walls, to be safe)."""
    dry = lambda v: not (v >> 10) & 3 and CLASS.get(v & 0x3FF) not in ("Q", "W")
    lab, out = {}, []
    for p in points:
        if p in lab:
            out.append(lab[p])
            continue
        x0, y0 = p
        if not (0 <= x0 < w and 0 <= y0 < h):
            out.append(None)
            continue
        # a start on a solid tile (a door, a sign) joins the region of any dry neighbour
        if not dry(vals[y0 * w + x0]):
            nb = [lab[q] for q in ((x0 + 1, y0), (x0 - 1, y0), (x0, y0 + 1), (x0, y0 - 1)) if q in lab]
            if nb:
                lab[p] = nb[0]
                out.append(nb[0])
                continue
        stack, seen, found = [p], {p}, None
        while stack:
            x, y = stack.pop()
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in seen and dry(vals[ny * w + nx]):
                    if (nx, ny) in lab:
                        found = lab[(nx, ny)]
                        continue
                    seen.add((nx, ny))
                    stack.append((nx, ny))
        label = found or p
        for q in seen:
            lab[q] = label
        out.append(label)
    return out


def same_links(a, b, w, h, points):
    """True if every pair of points connected in `a` is still connected in `b`."""
    ra, rb = regions(a, w, h, points), regions(b, w, h, points)
    return all(rb[i] == rb[j] for i in range(len(points)) for j in range(i) if ra[i] == ra[j])


def events_of(m):
    return ([(e["x"], e["y"]) for e in m.get("warp_events") or []] + [(e["x"], e["y"]) for e in m.get("object_events") or []]
            + [(e["x"], e["y"]) for e in m.get("bg_events") or []] + [(e["x"], e["y"]) for e in m.get("coord_events") or []])


def main():
    only = None
    if "--only" in sys.argv:
        only = set(sys.argv[sys.argv.index("--only") + 1].split(","))
    state = json.load(open(STATE)) if os.path.exists(STATE) else {}
    layouts = {l["id"]: l for l in json.load(open(PH.P("data", "layouts", "layouts.json")))["layouts"] if "id" in l}
    for name, theme in ROUTES.items():
        if only and name not in only:
            continue
        m = json.load(open(PH.P("data", "maps", name, "map.json")))
        lay = layouts[m["layout"]]
        w, h = lay["width"], lay["height"]
        path = PH.P(lay["blockdata_filepath"])
        cur = PH.read_bin(path)
        digest = hashlib.sha1(open(path, "rb").read()).hexdigest()
        st = state.get(name)
        if st and digest != st["dressed"]:
            print("%-24s changed since it was dressed: skipped" % name)
            continue
        base = [int(st["base"][k:k + 4], 16) for k in range(0, len(st["base"]), 4)] if st else cur
        area = w * h
        land = theme not in ("sea",)
        out = apply(base, w, h, "dirt", events_of(m), name,
                    ledges=area // 450 if theme == "route" else 0,
                    flowers=area // 260 if land and theme != "rocky" else 0,
                    groves=area // 300 if theme in ("route", "marsh") else 0)
        ev = [(e["x"], e["y"] + 1) for e in m.get("warp_events") or []] + [(e["x"], e["y"]) for e in m.get("object_events") or []]
        if not same_links(base, out, w, h, ev):
            print("%-24s dressing would cut a way through: skipped" % name)
            continue
        PH.write_bin(path, out)
        state[name] = {"base": "".join("%04x" % v for v in base),
                       "dressed": hashlib.sha1(open(path, "rb").read()).hexdigest()}
        print("%-24s dressed (%dx%d)" % (name, w, h))
    json.dump(state, open(STATE, "w"), indent=0)


if __name__ == "__main__":
    main()
