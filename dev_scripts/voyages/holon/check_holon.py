"""
Static checks for the installed Holon maps: warp symmetry, map sizes, connection symmetry, and a flood-fill
reachability check (on foot, then with Surf) from each map's entry points to every warp, object and sign.

usage: python3 dev_scripts/voyages/holon/check_holon.py
"""
import json
import os
import re
import struct
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
P = lambda *a: os.path.join(ROOT, *a)   # noqa: E731

MG = json.load(open(P("data", "maps", "map_groups.json")))
MAPS = MG["gMapGroup_Holon"]
LAYOUTS = {e["id"]: e for e in json.load(open(P("data", "layouts", "layouts.json")))["layouts"] if "id" in e}
MB = dict((n, int(v, 0)) for n, v in re.findall(r"^\s+(MB_\w+)(?:\s*=\s*(\w+))?", "", re.M))


def behaviours():
    txt = open(P("include", "constants", "metatile_behaviors.h")).read()
    names = re.findall(r"^\s+(MB_\w+),", txt, re.M)
    return {n: i for i, n in enumerate(names)}


BEH = behaviours()
SURF = {BEH[n] for n in BEH if n in ("MB_POND_WATER", "MB_OCEAN_WATER", "MB_DEEP_WATER", "MB_SEMI_DEEP_WATER",
                                     "MB_SOOTOPOLIS_DEEP_WATER", "MB_INTERIOR_DEEP_WATER", "MB_NO_SURFACING",
                                     "MB_EASTWARD_CURRENT", "MB_WESTWARD_CURRENT", "MB_NORTHWARD_CURRENT",
                                     "MB_SOUTHWARD_CURRENT", "MB_WATERFALL")}


def tileset_dir(sym):
    hdr = open(P("src", "data", "tilesets", "headers.h")).read()
    m = re.search(r"const struct Tileset %s =\s*\{.*?\.metatileAttributes = (\w+)," % sym, hdr, re.S)
    mt = open(P("src", "data", "tilesets", "metatiles.h")).read()
    m2 = re.search(r"%s\[\] = INCBIN_U16\(\"([^\"]+)\"\)" % m.group(1), mt)
    return P(m2.group(1))


def attrs(sym):
    b = open(tileset_dir(sym), "rb").read()
    return list(struct.unpack("<%dH" % (len(b) // 2), b))


def layout(lid):
    e = LAYOUTS[lid]
    w, h = e["width"], e["height"]
    b = open(P(e["blockdata_filepath"]), "rb").read()
    v = struct.unpack("<%dH" % (w * h), b[:2 * w * h])
    pa, sa = attrs(e["primary_tileset"]), attrs(e["secondary_tileset"])

    def beh(x, y):
        m = v[y * w + x] & 0x3FF
        a = pa[m] if m < 512 else sa[m - 512]
        return a & 0xFF
    return w, h, v, beh


def mj(folder):
    return json.load(open(P("data", "maps", folder, "map.json")))


def folder_of(mid):
    for f in MAPS:
        if mj(f)["id"] == mid:
            return f
    return None


def check_warps():
    bad = 0
    for f in MAPS:
        j = mj(f)
        for i, w in enumerate(j["warp_events"]):
            g = folder_of(w["dest_map"])
            if g is None:
                print("  warp %s#%d -> %s (outside Holon)" % (f, i, w["dest_map"]))
                continue
            dj = mj(g)
            k = int(w["dest_warp_id"])
            if k >= len(dj["warp_events"]):
                print("  BAD warp %s#%d -> %s#%d (no such warp)" % (f, i, g, k)); bad += 1; continue
            back = dj["warp_events"][k]
            if back["dest_map"] != j["id"]:
                print("  BAD warp %s#%d -> %s#%d, which leads to %s" % (f, i, g, k, back["dest_map"])); bad += 1
            elif not any(int(back["dest_warp_id"]) == ii and ww["x"] == j["warp_events"][ii]["x"]
                         for ii, ww in enumerate(j["warp_events"]) if ii == int(back["dest_warp_id"])):
                pass
            # pairs: the return warp must land on a warp of ours that goes back to g
            r = j["warp_events"][int(back["dest_warp_id"])]
            if r["dest_map"] != dj["id"]:
                print("  BAD return %s#%d lands on %s#%s which leads to %s" % (g, k, f, back["dest_warp_id"], r["dest_map"])); bad += 1
    print("warps: %s" % ("OK" if not bad else "%d problems" % bad))
    return bad


def check_connections():
    bad = 0
    opp = {"left": "right", "right": "left", "up": "down", "down": "up"}
    for f in MAPS:
        j = mj(f)
        for c in j["connections"] or []:
            g = folder_of(c["map"])
            back = [d for d in (mj(g)["connections"] or []) if d["map"] == j["id"] and d["direction"] == opp[c["direction"]]]
            if len(back) != 1 or back[0]["offset"] != -c["offset"]:
                print("  BAD connection %s %s %+d -> %s" % (f, c["direction"], c["offset"], g)); bad += 1
    print("connections: %s" % ("OK" if not bad else "%d problems" % bad))
    return bad


def check_sizes():
    for f in MAPS:
        e = LAYOUTS[mj(f)["layout"]]
        w, h = e["width"], e["height"]
        assert (w + 15) * (h + 14) <= 10240, (f, w, h)
    print("sizes: OK ((w+15)*(h+14) <= 10240)")


def walk_ok(v, w, beh, a, b, surf):
    (x0, y0), (x1, y1) = a, b
    c0, c1 = v[y0 * w + x0], v[y1 * w + x1]
    if (c1 >> 10) & 3:
        return False
    water0, water1 = beh(x0, y0) in SURF, beh(x1, y1) in SURF
    if water1 and not surf:
        return False
    e0, e1 = c0 >> 12, c1 >> 12
    if water0 != water1 and surf:
        return True               # surf on / off
    return e0 in (0, 15) or e1 in (0, 15) or e0 == e1


def flood(lid, starts, surf):
    w, h, v, beh = layout(lid)
    seen = set(starts)
    q = deque(starts)
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in seen and walk_ok(v, w, beh, (x, y), (nx, ny), surf):
                seen.add((nx, ny))
                q.append((nx, ny))
    return seen, (w, h, v, beh)


ENTRY = {"HolonMirageForest": [(5, 36)], "HolonLake": [(30, 0), (31, 0)]}


def check_reach():
    problems = 0
    for f in MAPS:
        j = mj(f)
        lid = j["layout"]
        starts = list(ENTRY.get(f, []))
        if not starts:     # interiors / village: the tile in front of the first warp (or the coast edge)
            w0 = j["warp_events"][0]
            starts = [(w0["x"], w0["y"] - 1)] if f != "HolonVillage" else [(0, 38), (0, 39)]
            if f != "HolonVillage" and j["map_type"] == "MAP_TYPE_INDOOR":
                starts = [(w0["x"], w0["y"] - 1)]
        foot, (w, h, v, beh) = flood(lid, starts, False)
        surf, _ = flood(lid, starts, True)
        # objects stand on their own tile: blocked by them, so test the 4 neighbours (talking range)
        npc_tiles = {(o["x"], o["y"]) for o in j["object_events"]}

        counter = BEH.get("MB_COUNTER")

        def near(xy, region):
            x, y = xy
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (x + dx, y + dy)
                if n in region and n not in npc_tiles:
                    return True
                # talking across a counter (Centre nurse, Mart clerk)
                if 0 <= n[0] < w and 0 <= n[1] < h and beh(*n) == counter and (x + 2 * dx, y + 2 * dy) in region:
                    return True
            return False
        targets = [("warp", (wv["x"], wv["y"])) for wv in j["warp_events"]]
        targets += [("obj " + o["graphics_id"][14:], (o["x"], o["y"])) for o in j["object_events"]]
        targets += [("sign", (b["x"], b["y"])) for b in j["bg_events"]]
        if f == "HolonVillage":
            targets += [("edge S", (30, 71)), ("edge S", (31, 71))]
        if f == "HolonMirageForest":
            targets += [("edge E", (43, 26)), ("edge E", (43, 27))]
        out = []
        for kind, xy in targets:
            if xy in foot or near(xy, foot):
                continue
            if xy in surf or near(xy, surf):
                out.append("%s%s (Surf)" % (kind, xy))
            else:
                out.append("%s%s UNREACHABLE" % (kind, xy))
                problems += 1
        print("%-32s foot %4d tiles%s" % (f, len(foot), ("; " + ", ".join(out)) if out else ""))
    print("reachability: %s" % ("OK" if not problems else "%d unreachable" % problems))
    return problems


def main():
    check_sizes()
    bad = check_warps() + check_connections() + check_reach()
    return bad


if __name__ == "__main__":
    raise SystemExit(1 if main() else 0)
