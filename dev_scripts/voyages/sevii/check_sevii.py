#!/usr/bin/env python3
"""
Static checks for the Sevii maps (gMapGroup_Sevii), reach.py-style. Run from anywhere, plain python3:

  sizes      (w+15)*(h+14) <= 10240 (fieldmap.c)
  warps      every warp's destination exists and points back at the same doorway (exceptions listed)
  reach      flood fill per map from every warp / connection edge / landing: every warp, NPC (talkable from a
             neighbouring cell, or across a counter), item ball, sign and hidden item reachable. Water counts as
             walkable (post-game: Surf), as do Rock Smash / Strength / Cut objects; ledges count both ways.
  connections  each connection has a matching reverse with the negated offset
"""
import json
import os
import sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mtattr as MA     # noqa: E402

P = MA.P
GROUP = "gMapGroup_Sevii"
# one-way by design: Dotted Hole's wrong-way warps drop you back on 1F; harbour landing warps (id 1) are arrival only
ONE_WAY = {("SixIsland_DottedHole_B%dF" % n) for n in (1, 2, 3, 4)}
FIELD_OBJ = ("BREAKABLE_ROCK", "PUSHABLE_BOULDER", "CUTTABLE_TREE", "ITEM_BALL")


def load():
    groups = json.load(open(P("data", "maps", "map_groups.json")))
    maps = {}
    for f in groups[GROUP]:
        maps[f] = json.load(open(P("data", "maps", f, "map.json")))
    allmaps = {}
    for g, v in groups.items():
        if g == "group_order":
            continue
        for f in v:
            try:
                allmaps[json.load(open(P("data", "maps", f, "map.json")))["id"]] = f
            except FileNotFoundError:
                pass
    return maps, allmaps


def is_water(beh):
    n = MA.mb()[1].get(beh, "")
    return any(k in n for k in ("WATER", "OCEAN", "POND", "WATERFALL", "CURRENT", "SEAWEED")) and "PUDDLE" not in n


def flood(m, L):
    """Cells reachable from the map's entries (warps, landing cells, connection edges)."""
    objs = {(o["x"], o["y"]) for o in m["object_events"]
            if not any(k in o["graphics_id"] for k in FIELD_OBJ[:3]) and o["graphics_id"] != "OBJ_EVENT_GFX_MR_BRINEYS_BOAT"}
    starts = [(w["x"], w["y"]) for w in m["warp_events"]]
    for c in m.get("connections") or []:
        d = c["direction"]
        edge = [(x, 0) for x in range(L.w)] if d == "up" else [(x, L.h - 1) for x in range(L.w)] if d == "down" else \
            [(0, y) for y in range(L.h)] if d == "left" else [(L.w - 1, y) for y in range(L.h)]
        starts += [p for p in edge if not L.coll(*p)]

    def passable(x, y):
        return L.inside(x, y) and not L.coll(x, y) and (x, y) not in objs

    seen = set()
    q = deque()
    for s in starts:
        if L.inside(*s) and s not in seen:
            seen.add(s)
            q.append(s)
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if (nx, ny) in seen or not passable(nx, ny):
                continue
            e1, e2 = L.elev(x, y), L.elev(nx, ny)
            w1, w2 = is_water(L.beh(x, y)), is_water(L.beh(nx, ny))
            if not (e1 == e2 or e1 in (0, 15) or e2 in (0, 15) or w1 != w2):
                continue
            seen.add((nx, ny))
            q.append((nx, ny))
    return seen, objs


def reachable_from(seen, L, x, y, counter_ok=True):
    names = MA.mb()[0]
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if (x + dx, y + dy) in seen:
            return True
        if counter_ok and L.inside(x + dx, y + dy) and L.beh(x + dx, y + dy) == names["MB_COUNTER"] \
                and (x + 2 * dx, y + 2 * dy) in seen:
            return True
    return False


def main():
    maps, allmaps = load()
    ids = {m["id"]: f for f, m in maps.items()}
    bad = 0
    report = []
    for f, m in maps.items():
        L = MA.Layout(m["layout"])
        size = (L.w + 15) * (L.h + 14)
        probs = []
        if size > 10240:
            probs.append("size %dx%d -> %d > 10240" % (L.w, L.h, size))
        # warps
        for i, w in enumerate(m["warp_events"]):
            B = allmaps.get(w["dest_map"])
            if B is None:
                probs.append("warp %d -> missing %s" % (i, w["dest_map"]))
                continue
            if f.endswith("_Harbor") and i == 1:
                continue
            bm = maps.get(B) or json.load(open(P("data", "maps", B, "map.json")))
            j = int(w["dest_warp_id"])
            if j >= len(bm["warp_events"]):
                probs.append("warp %d -> %s id %d out of range" % (i, B, j))
                continue
            back = bm["warp_events"][j]
            mine = [k for k, v in enumerate(m["warp_events"])
                    if abs(v["x"] - w["x"]) + abs(v["y"] - w["y"]) <= 1 and v["dest_map"] == w["dest_map"]]
            if back["dest_map"] != m["id"] or int(back["dest_warp_id"]) not in mine:
                if f not in ONE_WAY:
                    probs.append("warp %d (%d,%d) -> %s[%d] does not point back (it goes to %s[%s])" % (
                        i, w["x"], w["y"], B, j, back["dest_map"], back["dest_warp_id"]))
        # connections
        for c in m.get("connections") or []:
            B = ids.get(c["map"])
            if B is None:
                probs.append("connection to non-Sevii/missing %s" % c["map"])
                continue
            opp = {"up": "down", "down": "up", "left": "right", "right": "left"}[c["direction"]]
            rev = [r for r in maps[B].get("connections") or [] if r["map"] == m["id"] and r["direction"] == opp]
            if not rev or int(rev[0]["offset"]) != -int(c["offset"]):
                probs.append("connection %s %s %s has no matching reverse" % (c["direction"], c["offset"], c["map"]))
        # reach: every entry (warp / connection edge) must be in ONE walkable component (Surf allowed)
        parts = []
        for w in m["warp_events"]:
            s1, _ = flood(dict(m, warp_events=[w], connections=None), L)
            parts.append(("warp (%d,%d)" % (w["x"], w["y"]), s1 - {(w["x"], w["y"])} or {(w["x"], w["y"])}))
        for c0 in m.get("connections") or []:
            s1, _ = flood(dict(m, warp_events=[], connections=[c0]), L)
            if s1:
                parts.append(("edge %s" % c0["direction"], s1))
        sealed_cells = {(b["x"], b["y"]) for b in m["bg_events"] if b.get("script", "").endswith("_Sealed")}
        parts = [(n, s) for n, s in parts if not (len(s) == 1 and next(iter(s)) in sealed_cells)]
        groups = []
        for n, s in parts:
            hit = [gp for gp in groups if gp[1] & s]
            names, cells = [n], set(s)
            for gp in hit:
                groups.remove(gp)
                names += gp[0]
                cells |= gp[1]
            groups.append((names, cells))
        if len(groups) > 1:
            probs.append("entries split into %d walkable parts: %s" % (len(groups), [gp[0] for gp in groups]))
        seen, objs = flood(m, L)
        for i, w in enumerate(m["warp_events"]):
            if (w["x"], w["y"]) not in seen and not reachable_from(seen, L, w["x"], w["y"], False):
                sealed = any(b.get("script", "").endswith("_Sealed") and (b["x"], b["y"]) == (w["x"], w["y"])
                             for b in m["bg_events"])
                if not sealed:
                    probs.append("warp %d (%d,%d) unreachable" % (i, w["x"], w["y"]))
        for o in m["object_events"]:
            if o["script"] in ("0x0", "NULL") or "BOAT" in o["graphics_id"]:
                continue
            if not reachable_from(seen, L, o["x"], o["y"]):
                probs.append("%s @%d,%d unreachable" % (o["graphics_id"][14:], o["x"], o["y"]))
        for b in m["bg_events"]:
            if b["type"] == "hidden_item":
                if (b["x"], b["y"]) not in seen and not reachable_from(seen, L, b["x"], b["y"]):
                    probs.append("hidden %s @%d,%d unreachable" % (b["item"], b["x"], b["y"]))
            elif not reachable_from(seen, L, b["x"], b["y"]) and (b["x"], b["y"]) not in seen:
                probs.append("sign %s @%d,%d unreachable" % (b["script"].split("_EventScript_")[-1], b["x"], b["y"]))
        bad += bool(probs)
        report.append((f, L.w, L.h, size, len(seen), probs))
        print("%-40s %3dx%-3d size=%5d reach=%5d %s" % (f, L.w, L.h, size, len(seen), "OK" if not probs else probs))
    print("\n%d maps, %d with problems" % (len(maps), bad))
    json.dump(report, open(os.path.join(HERE, "check_report.json"), "w"), indent=1)
    return bad


if __name__ == "__main__" and "--world" not in sys.argv:
    sys.exit(1 if main() else 0)


def world():
    """Whole-cluster reachability: walkable parts of every map linked by warps and connections, from the arrival
    dock (MAP_ONE_ISLAND_HARBOR warp 1). Lists warps that can't be reached at all (sealed doors excepted)."""
    maps, allmaps = load()
    ids = {m["id"]: f for f, m in maps.items()}
    parts = {}
    for f, m in maps.items():
        L = MA.Layout(m["layout"])
        nodes = [("w", i) for i in range(len(m["warp_events"]))] + [("c", c["direction"], c["map"]) for c in m.get("connections") or []]
        cells = {}
        for n in nodes:
            if n[0] == "w":
                w = m["warp_events"][n[1]]
                s, _ = flood(dict(m, warp_events=[w], connections=None), L)
                s = (s - {(w["x"], w["y"])}) or {(w["x"], w["y"])}
            else:
                s, _ = flood(dict(m, warp_events=[], connections=[c for c in m["connections"] if (c["direction"], c["map"]) == n[1:]]), L)
            cells[n] = s
        comp = {}
        for n in nodes:
            comp[n] = n
        for a in nodes:
            for b in nodes:
                if a < b and cells[a] & cells[b]:
                    ra, rb = a, b
                    while comp[ra] != ra:
                        ra = comp[ra]
                    while comp[rb] != rb:
                        rb = comp[rb]
                    comp[rb] = ra

        def root(n, comp=comp):
            while comp[n] != n:
                n = comp[n]
            return n
        parts[f] = (nodes, root)
    start = ("OneIsland_Harbor", parts["OneIsland_Harbor"][1](("w", 1)))
    seen, q = {start}, [start]
    while q:
        f, r = q.pop()
        nodes, root = parts[f]
        m = maps[f]
        for n in nodes:
            if root(n) != r:
                continue
            if n[0] == "w":
                w = m["warp_events"][n[1]]
                B = ids.get(w["dest_map"])
                if B:
                    nxt = (B, parts[B][1](("w", int(w["dest_warp_id"]))))
            else:
                B = ids.get(n[2])
                opp = {"up": "down", "down": "up", "left": "right", "right": "left"}[n[1]]
                nxt = (B, parts[B][1](("c", opp, m["id"]))) if B else None
            if B and nxt not in seen:
                seen.add(nxt)
                q.append(nxt)
    # ferry: every harbour sailor reaches every other harbour's landing
    for f in maps:
        if f.endswith("_Harbor"):
            for g in maps:
                if g.endswith("_Harbor") and (g, parts[g][1](("w", 1))) not in seen and any(s[0] == f for s in seen):
                    seen.add((g, parts[g][1](("w", 1))))
                    q.append((g, parts[g][1](("w", 1))))
        while q:
            f2, r = q.pop()
            nodes, root = parts[f2]
            m = maps[f2]
            for n in nodes:
                if root(n) != r:
                    continue
                if n[0] == "w":
                    w = m["warp_events"][n[1]]
                    B = ids.get(w["dest_map"])
                    nxt = (B, parts[B][1](("w", int(w["dest_warp_id"])))) if B else None
                else:
                    B = ids.get(n[2])
                    opp = {"up": "down", "down": "up", "left": "right", "right": "left"}[n[1]]
                    nxt = (B, parts[B][1](("c", opp, m["id"]))) if B else None
                if nxt and nxt not in seen:
                    seen.add(nxt)
                    q.append(nxt)
    missing = []
    for f, m in maps.items():
        nodes, root = parts[f]
        sealed = {(b["x"], b["y"]) for b in m["bg_events"] if b.get("script", "").endswith("_Sealed")}
        for n in nodes:
            if n[0] == "w" and (f, root(n)) not in seen:
                w = m["warp_events"][n[1]]
                if (w["x"], w["y"]) not in sealed:
                    missing.append("%s warp %d (%d,%d)" % (f, n[1], w["x"], w["y"]))
    print("world: %d map parts reached from the One Island dock; unreachable warps: %s" % (len(seen), missing or "none"))
    return missing


if __name__ == "__main__" and "--world" in sys.argv:
    world()
