#!/usr/bin/env python3
"""
Second pass over the Tosa placeholder towns (dev_scripts/tosa_maps/placeholders.py made the first):
rebuilds each town / city / small landmark in town_text.TOWNS as a readable little place.

  - station towns get the Tosa Rail station building (station_art.py) with its two entrance tiles as
    warps 0 and 1 (the placeholder left warp 0 at the old 15x12 spot, away from the door)
  - roads from every region-map opening to a central plaza (cobbles in cities, dirt in towns)
  - Centre, Mart, hawker centre, decorative specials with a sign, and houses with real interiors
    (shared vanilla house layouts: no new layouts or tiles)
  - flowers by the houses, trees / ponds / rock by theme, a town sign, NPCs with lines from TODO.md
  - Centre / Mart / hawker interiors relinked, heal location moved to the new Centre door, and the
    town's FLAG_VISITED_* (the one region_map.c checks for its section) set on entry so Fly works

Every map it writes is recorded with a hash in towns_generated.json; a map edited since (e.g. in
Porymap) is skipped unless --force. Building pieces are cut once from live maps into kit_blocks.json.

usage: python3 dev_scripts/tosa_maps/towns.py [--force] [--only Name,Name]
"""
import hashlib
import json
import os
import random
import re
import sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import placeholders as PH                        # noqa: E402  helpers + block constants
from town_text import TOWNS, GYMS                # noqa: E402

P = PH.P
GROUP = PH.GROUP
KIT_PATH = os.path.join(HERE, "kit_blocks.json")
STATION_KIT = os.path.join(HERE, "station_kit.json")
GEN_PATH = os.path.join(HERE, "towns_generated.json")

# name: (source map, x, y, w, h, door offset or None, centre/mart sign offsets)
KIT_SRC = {
    "centre": ("InkaCity", 10, 20, 4, 4, (1, 2), [(2, 3), (3, 3)]),
    "mart": ("InkaCity", 23, 19, 4, 4, (1, 3), [(2, 3), (3, 3)]),
    "house_p": ("TosaPort", 4, 9, 4, 4, (1, 3), []),
    "house_r": ("TosaPort", 5, 16, 4, 4, (1, 3), []),
    "house_w": ("TosaPort", 16, 12, 6, 4, (2, 3), []),
    "hawker": ("BuraCity", 22, 9, 5, 4, (2, 3), []),
    "depot": ("TosaPort", 2, 2, 6, 5, None, []),
    "warehouse": ("TosaPort", 15, 4, 6, 5, None, []),
    "coldstore": ("TosaPort", 21, 5, 8, 5, None, []),      # its door is left without a warp
    "stall": ("TosaPort", 23, 11, 4, 5, None, []),
}
FLOWER = 0x3004
COBBLE = {"TL": 0x3208, "T": 0x3209, "TR": 0x320A, "L": 0x3210, "C": 0x3211, "R": 0x3212,
          "BL": 0x3218, "B": 0x3219, "BR": 0x321A}
DIRT = PH.PATH

# interior templates: layout, exit warps, NPC spots (x, y, movement)
INTERIORS = [
    ("LAYOUT_HOUSE1", [(3, 8), (4, 8)], [(6, 4, "WANDER_AROUND"), (2, 5, "FACE_RIGHT")]),
    ("LAYOUT_HOUSE2", [(3, 7), (4, 7)], [(4, 4, "FACE_RIGHT"), (7, 4, "FACE_LEFT")]),
    ("LAYOUT_HOUSE3", [(3, 7), (4, 7)], [(6, 3, "FACE_LEFT"), (3, 3, "FACE_RIGHT")]),
    ("LAYOUT_HOUSE4", [(3, 8), (4, 8)], [(6, 5, "FACE_RIGHT"), (2, 3, "LOOK_AROUND")]),
    ("LAYOUT_PACIFIDLOG_TOWN_HOUSE1", [(4, 8), (5, 8)], [(3, 5, "FACE_DOWN"), (6, 4, "FACE_LEFT")]),
    ("LAYOUT_PACIFIDLOG_TOWN_HOUSE2", [(4, 8), (5, 8)], [(3, 5, "FACE_DOWN"), (8, 6, "LOOK_AROUND")]),
    ("LAYOUT_ROUTE116_TUNNELERS_REST_HOUSE", [(4, 8), (5, 8)], [(6, 5, "FACE_RIGHT"), (3, 6, "LOOK_AROUND")]),
]
MOVES = {"wander": ("MOVEMENT_TYPE_WANDER_AROUND", 1), "look": ("MOVEMENT_TYPE_LOOK_AROUND", 0),
         "up": ("MOVEMENT_TYPE_FACE_UP", 0), "down": ("MOVEMENT_TYPE_FACE_DOWN", 0),
         "left": ("MOVEMENT_TYPE_FACE_LEFT", 0), "right": ("MOVEMENT_TYPE_FACE_RIGHT", 0)}


# ---------------------------------------------------------------- kit / bookkeeping
def load_kit():
    kit = json.load(open(KIT_PATH)) if os.path.exists(KIT_PATH) else {}
    changed = False
    for k, (src, x, y, w, h, door, signs) in KIT_SRC.items():
        if k not in kit:
            kit[k] = {"rows": PH.block_from(src, x, y, w, h), "door": door, "signs": signs, "from": [src, x, y]}
            changed = True
    if changed:
        json.dump(kit, open(KIT_PATH, "w"), indent=1)
    # vanilla Hoenn gym (General primary, so it works on any secondary): 6x5, animated door at (3,4)
    kit["gym"] = {"rows": [[0x31AA, 0x31AB, 0x31AB, 0x31AB, 0x31AB, 0x31AC],
                           [0x05B2, 0x05B3, 0x05B3, 0x05B3, 0x05B3, 0x05B4],
                           [0x05B8, 0x05B9, 0x05BA, 0x05B3, 0x05BB, 0x05BC],
                           [0x05C0, 0x05C1, 0x05C2, 0x05C5, 0x05C3, 0x05C4],
                           [0x31C8, 0x31C9, 0x05CA, 0x05CD, 0x05CB, 0x31CC]], "door": [3, 4], "signs": []}
    st = json.load(open(STATION_KIT))
    kit["station"] = {"rows": st["rows"], "door": st["door"], "door2": st["door2"], "signs": []}
    return kit


def file_hash(*paths):
    hsh = hashlib.sha1()
    for p in paths:
        if os.path.exists(p):
            hsh.update(open(p, "rb").read())
    return hsh.hexdigest()


def map_paths(name, layout_dir=None):
    out = [P("data", "maps", name, "map.json")]
    if layout_dir:
        out.append(P("data", "layouts", layout_dir, "map.bin"))
    return out


def visited_flags():
    """mapsec -> FLAG_VISITED_* from GetMapsecType in region_map.c, through the section aliases."""
    alias = dict(re.findall(r"#define\s+(MAPSEC_\w+)\s+(MAPSEC_\w+)",
                            open(P("include", "constants", "region_map_section_aliases.h")).read()))
    src = open(P("src", "region_map.c")).read()
    out = {}
    for sec, flag in re.findall(r"case (MAPSEC_\w+):\s*(?://[^\n]*)?\s*return FlagGet\((FLAG_VISITED_\w+)\)", src):
        out[alias.get(sec, sec)] = flag
    return out


# ---------------------------------------------------------------- planning one town
class Town:
    def __init__(self, name, spec, kit, grid, mapjson):
        self.name, self.spec, self.kit = name, spec, kit
        self.w, self.h = spec["size"]
        assert self.w % 2 == 0 and self.h % 2 == 0 and (self.w + 15) * (self.h + 14) <= PH.MAX_MAP_DATA, name
        self.rnd = random.Random(name + "/towns")
        self.cv = PH.Canvas(self.w, self.h, "G")
        self.theme = spec["theme"]
        self.road = spec.get("road", "cobble")
        self.station = mapjson is not None and any(
            wv["dest_map"].endswith("_STATION") for wv in mapjson.get("warp_events", []))
        cells = [c for c, s in grid.items() if s == mapjson_sec(mapjson, name)]
        self.opens = PH.openings(cells, grid, self.w, self.h) if cells else {}
        for side in spec.get("mouths", {}).values():
            self.opens.pop(side, None)
        if spec.get("coast"):
            self.opens.pop(spec["coast"], None)
        self.warps = OrderedDict()          # key -> (x, y)
        self.fronts = []                    # door-front tiles (keep NPCs and trees off)
        self.buildings = []                 # (kind, x, y, w, h, door_xy, key)
        self.signs = []                     # (x, y, script, facing)
        self.npcs = []

    # -- helpers
    def free(self, x0, y0, x1, y1, ok=("G",)):
        if x0 < 0 or y0 < 0 or x1 >= self.w or y1 >= self.h:
            return False
        return all(self.cv.t[yy][xx] in ok and (xx, yy) not in self.cv.raw
                   for yy in range(y0, y1 + 1) for xx in range(x0, x1 + 1))

    def mark(self, x0, y0, x1, y1, code):
        for yy in range(y0, y1 + 1):
            for xx in range(x0, x1 + 1):
                if self.cv.ok(xx, yy):
                    self.cv.t[yy][xx] = code

    def stamp(self, rows, x0, y0):
        self.cv.stamp(x0, y0, rows)
        self.mark(x0, y0, x0 + len(rows[0]) - 1, y0 + len(rows) - 1, "B")

    # -- stages
    def frame(self):
        w, h, cv = self.w, self.h, self.cv
        wall = "R" if self.theme == "rocky" else "X"
        gap = {(side, pos + k) for side, ps in self.opens.items() for pos in ps for k in range(-2, 4)}
        for by in range(h // 2):
            for bx in range(w // 2):
                edge = [e for cond, e in ((by == 0, ("N", bx * 2)), (by == h // 2 - 1, ("S", bx * 2)),
                                         (bx == 0, ("W", by * 2)), (bx == w // 2 - 1, ("E", by * 2))) if cond]
                if edge and not any(e in gap for e in edge):
                    cv.rect(bx * 2, by * 2, bx * 2 + 1, by * 2 + 1, wall)
        self.hub = ((w // 2) & ~1, self.spec.get("hub_y", (h * 2 // 5) & ~1))
        if self.station:
            st = self.kit["station"]["rows"]
            sx = self.hub[0] - 2                                     # entrance (2,4)-(3,4) on the hub column
            for pos in self.opens.get("N", []):
                if abs(pos - self.hub[0]) < 8:
                    sx = pos + 6 if pos + 12 < w else pos - 10
            self.st_xy = (sx, 2)
            self.hub = (sx + 2, max(self.hub[1], 12))

    def seg(self, x0, y0, x1, y1, keep=False):
        x0, x1 = max(0, min(x0, x1)), min(self.w - 1, max(x0, x1))
        y0, y1 = max(0, min(y0, y1)), min(self.h - 1, max(y0, y1))
        self.cv.rect(x0, y0, x1, y1, "P")
        self.segs.append([x0, y0, x1, y1, keep])

    def seg_path(self, a, b, keep=False):
        """Same shape as Canvas.path: along a's row to b's column, then along b's column."""
        (ax, ay), (bx, by) = a, b
        self.seg(min(ax, bx), ay, max(ax, bx) + 1, ay + 1, keep)
        self.seg(bx, min(ay, by), bx + 1, max(ay, by) + 1, keep)

    def roads(self):
        cv, (hx, hy) = self.cv, self.hub
        self.segs, self.conn_ends, self.conn_cells = [], [], set()
        for side, poss in self.opens.items():
            for pos in poss:
                start = {"N": (pos, 0), "S": (pos, self.h - 2), "W": (0, pos), "E": (self.w - 2, pos)}[side]
                if side in "WE":
                    self.seg_path(start, self.hub, True)
                else:
                    self.seg_path(self.hub, start, True)
        # a street grid (high street through the hub, more every 8 rows, side streets every 12 columns),
        # split at every junction so prune() can drop the pieces no building uses
        limit = self.h - 5 - (10 if self.spec.get("coast") == "S" else 0)
        rows, yy = [hy], hy + 8
        while yy <= limit:
            rows.append(yy & ~1)
            yy += 8
        if len(rows) == 1 and limit - hy >= 7:
            rows.append(limit & ~1)
        vxs = [hx + k * 12 for k in range(-3, 4) if 4 <= hx + k * 12 <= self.w - 7]
        xs = sorted(set([4] + vxs + [(self.w - 7) & ~1]))
        for yy in rows:
            for a, b in zip(xs, xs[1:]):
                self.seg(a, yy, b + 1, yy + 1)
        for vx in vxs:
            for a, b in zip(rows, rows[1:]):
                self.seg(vx, a, vx + 1, b + 1)
        self.seg(hx - 3, hy - 2, hx + 4, hy + 3, True)                 # plaza
        self.plaza = len(self.segs) - 1
        if self.station:
            sx, sy = self.st_xy
            self.seg_path((sx + 2, sy + 5), self.hub, True)            # under the entrance down to the plaza
        # coast: sea band and beach (roads stop at the sand)
        side = self.spec.get("coast")
        if side:
            band = 6 if side in "NS" else 5
            for yy in range(self.h):
                for xx in range(self.w):
                    dd = {"S": self.h - 1 - yy, "N": yy, "W": xx, "E": self.w - 1 - xx}[side]
                    if dd < band:
                        cv.t[yy][xx] = "W"
                    elif dd < band + 3:
                        cv.t[yy][xx] = "S"

    def mouths(self):
        cv, (hx, hy) = self.cv, self.hub
        rocky = self.theme == "rocky"
        for key, side in self.spec.get("mouths", {}).items():
            mx, my = {"N": (hx + 4, 5), "S": (hx - 6, self.h - 5), "W": (5, hy - 4), "E": (self.w - 6, hy - 4)}[side]
            cv.rect(mx - 3, my - 4, mx + 3, my + 1, "R")
            self.seg(mx - 1, my + 1, mx + 1, my + 2, True)
            cv.stamp(mx - 1, my - 3, PH.MOUTH)
            self.mark(mx - 1, my - 3, mx + 1, my, "B")
            self.warps["mouth:" + key] = (mx, my)
            self.fronts.append((mx, my + 1))
            if side in "NS":
                self.seg_path((mx, my + 1), self.hub, True)
            else:
                self.seg_path((mx, my + 1), (hx, my + 1), True)
                self.seg_path((hx, my + 1), self.hub, True)
            # rock shoulders read as a cliff face rather than a blob
            cv.rect(mx - 3, my - 4, mx + 3, my - 4, "R")

    def place_station(self):
        if not self.station:
            return
        st = self.kit["station"]
        sx, sy = self.st_xy
        self.stamp(st["rows"], sx, sy)
        self.warps["station"] = (sx + st["door"][0], sy + st["door"][1])
        self.warps["station2"] = (sx + st["door2"][0], sy + st["door2"][1])
        self.fronts += [(sx + 2, sy + 5), (sx + 3, sy + 5)]
        self.buildings.append(("station", sx, sy, 6, 5, self.warps["station"], "station"))

    def place(self, kind, key, near):
        """Greedy: the spot whose door joins a road with the shortest walk, nearest `near`."""
        b = self.kit[kind]
        rows, door = b["rows"], b["door"]
        bw, bh = len(rows[0]), len(rows)
        best = None
        for y0 in range(2, self.h - bh - 3):
            for x0 in range(2, self.w - bw - 2):
                if not self.free(x0, y0, x0 + bw - 1, y0 + bh - 1):
                    continue
                if not self.free(x0 - 1, y0 - 1, x0 + bw, y0 + bh - 1, ("G", "m", "F", "P")):
                    continue
                if door is None:
                    # decorative: needs road within 2 rows below, footprint clear
                    fx = x0 + bw // 2 - 1
                    conn = self.connect_len(fx, y0 + bh, 3)
                else:
                    fx = x0 + door[0]
                    conn = self.connect_len(fx, y0 + bh, 7)
                if conn is None:
                    continue
                dist = abs(fx - near[0]) + abs(y0 + bh - near[1])
                score = conn * 3 + dist * 0.35 + self.rnd.random() * 2.5
                if best is None or score < best[0]:
                    best = (score, x0, y0, fx)
        if best is None:
            print("  %s: no room for %s" % (self.name, kind))
            return None
        _, x0, y0, fx = best
        self.stamp(rows, x0, y0)
        for yy in range(y0 - 1, y0 + bh + 1):
            for xx in range(x0 - 1, x0 + bw + 1):
                if self.cv.ok(xx, yy) and self.cv.t[yy][xx] == "G":
                    self.cv.t[yy][xx] = "m"
        yy = y0 + bh
        while self.cv.ok(fx, yy) and not (self.cv.t[yy][fx] == "P" and self.cv.t[yy][fx + 1] == "P"):
            self.cv.t[yy][fx] = self.cv.t[yy][fx + 1] = "P"
            self.conn_cells |= {(fx, yy), (fx + 1, yy)}
            yy += 1
        self.conn_ends.append((fx, yy))
        self.conn_cells |= {(fx, y0 + bh), (fx + 1, y0 + bh)}
        dxy = (x0 + door[0], y0 + door[1]) if door else None
        if dxy:
            self.warps[key] = dxy
            self.fronts.append((dxy[0], y0 + bh))
        for (sx, sy) in b.get("signs", []):
            script = "Common_EventScript_ShowPokemonCenterSign" if kind == "centre" else "Common_EventScript_ShowPokemartSign"
            self.signs.append((x0 + sx, y0 + sy, script, "BG_EVENT_PLAYER_FACING_NORTH"))
        self.buildings.append((kind, x0, y0, bw, bh, dxy, key))
        return self.buildings[-1]

    def connect_len(self, fx, fy, limit):
        for k in range(limit + 1):
            yy = fy + k
            if not self.cv.ok(fx + 1, yy):
                return None
            a, b = self.cv.t[yy][fx], self.cv.t[yy][fx + 1]
            if a == "P" and b == "P":
                return k
            if a not in ("G", "m") or b not in ("G", "m") or (fx, yy) in self.cv.raw or (fx + 1, yy) in self.cv.raw:
                return None
        return None

    def buildings_pass(self):
        hx, hy = self.hub
        nh = 0
        self.special_signs = []
        for n, item in enumerate(self.spec["buildings"]):
            kind, text = (item, None) if isinstance(item, str) else item
            if kind == "centre":
                near, key = (hx - 8, hy + 6), "centre"
            elif kind == "mart":
                near, key = (hx + 8, hy + 6), "mart"
            elif kind == "hawker":
                near, key = (hx + 10, hy - 2), "hawker"
            elif kind == "gym":
                near, key = (hx + 9, hy - 3), "gym"
            elif kind.startswith("house"):
                near = (self.rnd.randrange(4, self.w - 4), self.rnd.randrange(4, self.h - 4))
                key = "house:%d" % nh
                nh += 1
            else:
                near, key = (hx + self.rnd.choice((-10, 10)), hy - 6), "special:%d" % n
            got = self.place(kind, key, near)
            if got and kind == "gym":
                _, x0, y0, bw, bh, _, _ = got
                for sx in (x0 - 1, x0 + bw):
                    if self.cv.ok(sx, y0 + bh - 1) and self.cv.t[y0 + bh - 1][sx] == "m":
                        self.cv.t[y0 + bh - 1][sx] = "N"
                        self.signs.append((sx, y0 + bh - 1, self.name + "_EventScript_GymSign", "BG_EVENT_PLAYER_FACING_ANY"))
                        break
            if got and text:
                _, x0, y0, bw, bh, _, _ = got
                self.signs.append((x0 + 1, y0 + bh - 1, self.name + "_EventScript_Sign%d" % n, "BG_EVENT_PLAYER_FACING_NORTH"))
                self.special_signs.append((n, text))
            if got is None and kind.startswith("house"):
                nh -= 1
        self.n_houses = nh

    def prune(self):
        """Keep only the road pieces on the way from the plaza to a door, exit, cave or the station."""
        segs = self.segs
        inside = lambda sg, x, yy: sg[0] <= x <= sg[2] and sg[1] <= yy <= sg[3]
        need = {i for i, sg in enumerate(segs) if sg[4]}
        for (x, yy) in self.conn_ends:
            for i, sg in enumerate(segs):
                if inside(sg, x, yy) or inside(sg, x + 1, yy):
                    need.add(i)
        touch = lambda a, b: not (a[2] < b[0] - 0 or b[2] < a[0] or a[3] < b[1] or b[3] < a[1])
        parent, queue = {self.plaza: None}, [self.plaza]
        while queue:
            i = queue.pop(0)
            for j in range(len(segs)):
                if j not in parent and touch(segs[i], segs[j]):
                    parent[j] = i
                    queue.append(j)
        keep = set()
        for i in need:
            while i is not None and i not in keep and i in parent:
                keep.add(i)
                i = parent[i]
        cells = set(self.conn_cells)
        for i in keep:
            x0, y0, x1, y1, _ = segs[i]
            cells |= {(x, yy) for x in range(x0, x1 + 1) for yy in range(y0, y1 + 1)}
        for yy in range(self.h):
            for x in range(self.w):
                if self.cv.t[yy][x] == "P" and (x, yy) not in cells:
                    self.cv.t[yy][x] = "G"

    def decorate(self):
        cv, rnd = self.cv, self.rnd
        # flowers either side of house fronts
        for kind, x0, y0, bw, bh, dxy, key in self.buildings:
            if kind.startswith("house") or kind in ("centre", "mart"):
                for xx in (x0 - 1, x0 + bw):
                    for yy in (y0 + bh - 2, y0 + bh - 1):
                        if cv.ok(xx, yy) and cv.t[yy][xx] == "m" and rnd.random() < 0.8:
                            cv.t[yy][xx] = "F"
        # ponds (marsh)
        made = 0
        for _ in range(60):
            if made >= self.spec.get("ponds", 0):
                break
            cx, cy = rnd.randrange(5, self.w - 5), rnd.randrange(5, self.h - 5)
            r = rnd.randint(2, 3)
            if self.free(cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2):
                cv.blob(rnd, cx, cy, r, "W", ("P", "B", "m", "F", "X", "R", "S"))
                made += 1
        # rock outcrops (rocky)
        if self.theme == "rocky":
            for _ in range(self.w * self.h // 40):
                bx, by = rnd.randrange(2, self.w // 2 - 2), rnd.randrange(2, self.h // 2 - 2)
                if self.free(bx * 2 - 1, by * 2 - 1, bx * 2 + 2, by * 2 + 2):
                    cv.rect(bx * 2, by * 2, bx * 2 + 1, by * 2 + 1, "R")
        # trees on open grass, never next to a road / building front
        dens = self.spec.get("trees", 0.1)
        for by in range(1, self.h // 2 - 1):
            for bx in range(1, self.w // 2 - 1):
                x, yy = bx * 2, by * 2
                if self.free(x - 1, yy - 1, x + 2, yy + 2, ("G", "X", "m", "F")) and self.free(x, yy, x + 1, yy + 1) \
                        and rnd.random() < dens and not any(abs(fx - x) < 3 and abs(fy - yy) < 3 for fx, fy in self.fronts):
                    cv.rect(x, yy, x + 1, yy + 1, "X")
        # town sign beside the main road in
        self.town_sign()

    def town_sign(self):
        cv = self.cv
        cands = []
        for side, poss in self.opens.items():
            for pos in poss:
                cands.append({"S": (pos - 1, self.h - 4), "N": (pos - 1, 3), "W": (3, pos - 1), "E": (self.w - 4, pos - 1)}[side])
        cands.append((self.hub[0] - 4, self.hub[1] - 3))
        for (x, yy) in cands:
            for dx, dy in ((0, 0), (-1, 0), (0, -1), (1, 0), (0, 1), (-2, 0), (2, 0)):
                xx, y2 = x + dx, yy + dy
                if cv.ok(xx, y2) and cv.t[y2][xx] in ("G", "m") and (xx, y2) not in cv.raw:
                    cv.t[y2][xx] = "N"
                    self.signs.insert(0, (xx, y2, self.name + "_EventScript_TownSign", "BG_EVENT_PLAYER_FACING_ANY"))
                    return

    def walkable(self, x, yy):
        return self.cv.ok(x, yy) and (x, yy) not in self.cv.raw and self.cv.t[yy][x] in ("G", "P", "m", "S")

    def place_npcs(self):
        hx, hy = self.hub
        taken = []
        bykey = {k: (d[0], d[1] + 2) if d else (x0 + bw // 2, y0 + bh + 1)
                 for kind, x0, y0, bw, bh, d, k in self.buildings}
        if self.station:
            bykey["station"] = (self.warps["station"][0] + 2, self.warps["station"][1] + 2)
        for k, (mx, my) in self.warps.items():
            if k.startswith("mouth:"):
                bykey[k] = (mx + 2, my + 2)
        avoid = list(self.warps.values()) + self.fronts + [(s[0], s[1]) for s in self.signs]
        for gfx, where, move, text in self.spec.get("npcs", []):
            if where == "plaza":
                target = (hx + self.rnd.randint(-3, 3), hy + self.rnd.randint(-2, 2))
            elif where in ("coast", "pond"):
                want = "S" if where == "coast" else "W"
                pts = [(x, yy) for yy in range(self.h) for x in range(self.w) if self.cv.t[yy][x] == want]
                target = self.rnd.choice(pts) if pts else (hx, hy)
            elif where == "exit":
                ends = [{"S": (p, self.h - 5), "N": (p, 4), "W": (4, p), "E": (self.w - 5, p)}[s]
                        for s, ps in self.opens.items() for p in ps]
                target = self.rnd.choice(ends) if ends else (hx, hy + 4)
            elif where == "any":
                target = (self.rnd.randrange(4, self.w - 4), self.rnd.randrange(4, self.h - 4))
            else:
                target = bykey.get(where, (hx, hy))
            best = None
            for yy in range(3, self.h - 3):
                for x in range(3, self.w - 3):
                    if not self.walkable(x, yy):
                        continue
                    if any(abs(x - ax) <= 1 and abs(yy - ay) <= 1 for ax, ay in avoid):
                        continue
                    if any(abs(x - ax) + abs(yy - ay) < 3 for ax, ay in taken):
                        continue
                    dd = abs(x - target[0]) + abs(yy - target[1]) + self.rnd.random()
                    if best is None or dd < best[0]:
                        best = (dd, x, yy)
            if best:
                taken.append(best[1:])
                self.npcs.append((gfx, best[1], best[2], move, text))

    def render(self):
        cv, out = self.cv, []
        cob = self.road == "cobble"
        isp = lambda x, yy: (not cv.ok(x, yy)) or (cv.t[yy][x] == "P" and (x, yy) not in cv.raw)
        for yy in range(self.h):
            for x in range(self.w):
                if (x, yy) in cv.raw:
                    out.append(cv.raw[(x, yy)])
                    continue
                c = cv.t[yy][x]
                if c == "P":
                    if not cob:
                        out.append(DIRT)
                        continue
                    n, s, w_, e = isp(x, yy - 1), isp(x, yy + 1), isp(x - 1, yy), isp(x + 1, yy)
                    k = ("T" if not n else "B" if not s else "") + ("L" if not w_ else "R" if not e else "")
                    out.append(COBBLE[k or "C"])
                    continue
                if c == "F":
                    out.append(FLOWER)
                    continue
                if c in ("m", "B"):
                    c = "G"
                out.append(None)
                out[-1] = c
        # trees / rock / plain codes through the placeholder renderer
        tmp = PH.Canvas(self.w, self.h, "G")
        for yy in range(self.h):
            for x in range(self.w):
                v = out[yy * self.w + x]
                tmp.t[yy][x] = v if isinstance(v, str) else "?"
        final = []
        for yy in range(self.h):
            for x in range(self.w):
                v = out[yy * self.w + x]
                if not isinstance(v, str):
                    final.append(v)
                    continue
                if v == "X":
                    bx = x // 2
                    tb = lambda bx_, by_: all(tmp.ok(bx_ * 2 + i, by_ * 2 + j) and tmp.t[by_ * 2 + j][bx_ * 2 + i] == "X"
                                              for i in (0, 1) for j in (0, 1))
                    if tb(bx, yy // 2):
                        final.append(PH.TREE_STACK[x % 2] if yy % 2 and tb(bx, yy // 2 + 1) else PH.TREE[(x % 2, yy % 2)])
                    else:
                        final.append(PH.GRASS)
                    continue
                if v == "R":
                    final.append(PH.ROCK_TOP if yy == 0 or tmp.t[yy - 1][x] != "R" else PH.ROCK_FACE)
                    continue
                final.append({"G": PH.GRASS, "T": PH.TALL, "S": PH.SAND, "W": PH.SEA, "N": PH.SIGN, "?": PH.GRASS}[v])
        return final


def mapjson_sec(m, name):
    return m["region_map_section"] if m else None


# ---------------------------------------------------------------- writing
def obj(gfx, x, yy, elev, move, script, rng=None):
    mt, r = MOVES.get(move, (move, 0))
    if rng is not None:
        r = rng
    return OrderedDict([("graphics_id", gfx), ("x", x), ("y", yy), ("elevation", elev), ("movement_type", mt),
                        ("movement_range_x", r), ("movement_range_y", r), ("trainer_type", "TRAINER_TYPE_NONE"),
                        ("trainer_sight_or_berry_tree_id", "0"), ("script", script), ("flag", "0")])


def msg(label, text, kind):
    t = text.replace('"', "'")
    parts = t.split("\\p")
    body = "\\p".join(parts)
    if "\n" in body:                                      # sign headers keep their own line break
        head, rest = body.split("\n", 1)
        return '\nscript %s {\n    msgbox(format("%s\\n%s"), %s)\n}\n' % (label, head, rest, kind)
    return '\nscript %s {\n    msgbox(format("%s"), %s)\n}\n' % (label, body, kind)


def main():
    force = "--force" in sys.argv
    only = None
    if "--only" in sys.argv:
        only = set(sys.argv[sys.argv.index("--only") + 1].split(","))
    kit = load_kit()
    patch_gym_trainers()
    grid = PH.region_cells()
    flags = visited_flags()
    gen = json.load(open(GEN_PATH)) if os.path.exists(GEN_PATH) else {}
    lj_path = P("data", "layouts", "layouts.json")
    lj = json.load(open(lj_path), object_pairs_hook=OrderedDict)
    layouts = OrderedDict((l["id"], l) for l in lj["layouts"])
    mg_path = P("data", "maps", "map_groups.json")
    mg = json.load(open(mg_path), object_pairs_hook=OrderedDict)
    heal_path = P("src", "data", "heal_locations.json")
    heal = json.load(open(heal_path), object_pairs_hook=OrderedDict)
    new_includes = []

    for name, spec in TOWNS.items():
        if only and name not in only:
            continue
        mpath = P("data", "maps", name, "map.json")
        m = json.load(open(mpath), object_pairs_hook=OrderedDict)
        lay = layouts[m["layout"]]
        ldir = os.path.dirname(lay["blockdata_filepath"]).split("/")[-1]
        rec = gen.get(name)
        if rec and rec != file_hash(*map_paths(name, ldir)) and not force:
            print("skip %s (edited since generated; --force to overwrite)" % name)
            continue
        t = Town(name, spec, kit, grid, m)
        t.frame()
        t.roads()
        t.mouths()
        t.place_station()
        t.buildings_pass()
        t.prune()
        t.decorate()
        t.place_npcs()
        if t.station:                                    # station entrances are always warps 0 and 1
            t.warps = OrderedDict([(k, t.warps[k]) for k in ("station", "station2")] +
                                  [(k, v) for k, v in t.warps.items() if k not in ("station", "station2")])
        blocks = t.render()
        PH.write_bin(P(lay["blockdata_filepath"]), blocks)
        lay["width"], lay["height"] = t.w, t.h
        lay["secondary_tileset"] = "gTileset_TosaPort"
        lay["primary_tileset"] = "gTileset_General"
        PH.write_bin(P(lay["border_filepath"]), [0x1D4, 0x1D5, 0x1DC, 0x1DD] if t.theme != "rocky" else [0x071] * 4)
        const = PH.snake(name) if not m["id"].startswith("MAP_") else m["id"][4:]
        # warps: keep the station's (it already points at <Town>_Station warp 0), rebuild the rest
        keys = list(t.warps.keys())
        warps = []
        for k in keys:
            x, yy = t.warps[k]
            wv = OrderedDict([("x", x), ("y", yy), ("elevation", 0), ("dest_map", "X"), ("dest_warp_id", "X")])
            if k in ("station", "station2"):
                st = next(o for o in m["warp_events"] if o["dest_map"].endswith("_STATION"))
                wv.update(dest_map=st["dest_map"], dest_warp_id="0")
            warps.append(wv)
        # mouth links: keep whatever the placeholder linked them to (match by destination order)
        old_mouths = [wv for wv in m["warp_events"] if "MT_BATOK" in wv["dest_map"] or "CHALLENGERS_TRAIL" in wv["dest_map"]]
        mouth_keys = [k for k in keys if k.startswith("mouth:")]
        assert len(old_mouths) == len(mouth_keys), (name, old_mouths, mouth_keys)
        order = {"FaberTown": {"mouth:batok_w": "MT_BATOK_3F", "mouth:batok_e": "MT_BATOK_EAST_2F"}}
        for k in mouth_keys:
            want = order.get(name, {}).get(k)
            src = next(wv for wv in old_mouths if want is None or wv["dest_map"].endswith(want))
            warps[keys.index(k)].update(dest_map=src["dest_map"], dest_warp_id=src["dest_warp_id"])
            # the far end points back at our new index
            fm = folder_of(src["dest_map"])
            fj = json.load(open(P("data", "maps", fm, "map.json")), object_pairs_hook=OrderedDict)
            fj["warp_events"][int(src["dest_warp_id"])]["dest_warp_id"] = str(keys.index(k))
            PH.write_json(P("data", "maps", fm, "map.json"), fj)
        # station interior: both exit tiles return to warp 0
        if t.station:
            sm = folder_of(warps[0]["dest_map"])
            sj = json.load(open(P("data", "maps", sm, "map.json")), object_pairs_hook=OrderedDict)
            for wv in sj["warp_events"]:
                if wv["dest_map"] == m["id"]:
                    wv["dest_warp_id"] = "0"
            PH.write_json(P("data", "maps", sm, "map.json"), sj)
        # Centre / Mart / hawker interiors
        group = mg[GROUP]
        for key, suffix in (("centre", "_PokemonCenter_1F"), ("mart", "_Mart"), ("hawker", "_HawkerCentre")):
            if key not in t.warps:
                continue
            folder = name + suffix
            ij = json.load(open(P("data", "maps", folder, "map.json")), object_pairs_hook=OrderedDict)
            idx = keys.index(key)
            for wv in ij["warp_events"]:
                if wv["dest_map"] == m["id"]:
                    wv["dest_warp_id"] = str(idx)
            warps[idx].update(dest_map=ij["id"], dest_warp_id="0")
            PH.write_json(P("data", "maps", folder, "map.json"), ij)
            if key == "centre":
                hid = "HEAL_LOCATION_" + const
                for e in heal["heal_locations"]:
                    if e["id"] == hid:
                        e["x"], e["y"] = t.warps["centre"][0], t.warps["centre"][1] + 1
        # gym (placeholder interior: vanilla Dewford Gym room, leader + guide)
        if "gym" in t.warps:
            write_gym(name, m, keys.index("gym"), warps, group, new_includes, gen)
        # houses
        houses_txt = spec.get("houses", [])
        interiors = []
        for i in range(t.n_houses):
            folder = "%s_House%d" % (name, i + 1)
            tpl = INTERIORS[(i + sum(map(ord, name))) % len(INTERIORS)]
            if spec.get("house_layout"):
                tpl = next(x for x in INTERIORS if x[0] == spec["house_layout"])
            lid, exits, spots = tpl
            idx = keys.index("house:%d" % i)
            iid = "MAP_" + PH.snake(name) + "_HOUSE%d" % (i + 1)
            warps[idx].update(dest_map=iid, dest_warp_id="0")
            people = houses_txt[i] if i < len(houses_txt) else []
            objs, pory = [], "mapscripts %s_MapScripts {}\n" % folder
            for j, (gfx, text) in enumerate(people[:len(spots)]):
                sx, sy, mv = spots[j]
                label = "%s_EventScript_Npc%d" % (folder, j + 1)
                objs.append(obj(gfx, sx, sy, 3, "MOVEMENT_TYPE_" + mv, label, 1 if mv == "WANDER_AROUND" else 0))
                pory += msg(label, text, "MSGBOX_NPC")
            ij = OrderedDict([
                ("id", iid), ("name", folder), ("layout", lid), ("music", m["music"]),
                ("region", m.get("region", "REGION_HOENN")), ("region_map_section", m["region_map_section"]),
                ("requires_flash", False), ("weather", "WEATHER_NONE"), ("map_type", "MAP_TYPE_INDOOR"),
                ("allow_cycling", False), ("allow_escaping", False), ("allow_running", False),
                ("show_map_name", False), ("battle_scene", "MAP_BATTLE_SCENE_NORMAL"), ("connections", None),
                ("object_events", objs),
                ("warp_events", [OrderedDict([("x", ex), ("y", ey), ("elevation", 0), ("dest_map", m["id"]),
                                              ("dest_warp_id", str(idx))]) for ex, ey in exits]),
                ("coord_events", []), ("bg_events", [])])
            PH.write_json(P("data", "maps", folder, "map.json"), ij)
            write_pory(folder, pory)
            if folder not in group:
                group.append(folder)
                new_includes.append(folder)
            interiors.append(folder)
            gen[folder] = file_hash(P("data", "maps", folder, "map.json"))
        # remove houses from an earlier run that no longer exist
        k = t.n_houses + 1
        while os.path.isdir(P("data", "maps", "%s_House%d" % (name, k))):
            stale = "%s_House%d" % (name, k)
            for f in os.listdir(P("data", "maps", stale)):
                os.remove(P("data", "maps", stale, f))
            os.rmdir(P("data", "maps", stale))
            if stale in group:
                group.remove(stale)
            gen.pop(stale, None)
            k += 1
        bad = [(keys[i], wv) for i, wv in enumerate(warps) if "X" in (wv["dest_map"], wv["dest_warp_id"])]
        assert not bad, (name, bad)
        # events + scripts
        objs, pory_npcs = [], ""
        for j, (gfx, x, yy, move, text) in enumerate(t.npcs):
            label = "%s_EventScript_Npc%d" % (name, j + 1)
            elev = (blocks[yy * t.w + x] >> 12) & 0xF
            objs.append(obj(gfx, x, yy, elev, move, label))
            pory_npcs += msg(label, text, "MSGBOX_NPC")
        bg = [OrderedDict([("type", "sign"), ("x", x), ("y", yy), ("elevation", 0), ("player_facing_dir", face),
                           ("script", script)]) for x, yy, script, face in t.signs]
        m["object_events"] = objs
        m["warp_events"] = warps
        m["coord_events"] = []
        m["bg_events"] = bg
        PH.write_json(mpath, m)
        flag = flags.get(m["region_map_section"])
        pory = "mapscripts %s_MapScripts {\n" % name
        if flag:
            pory += "    MAP_SCRIPT_ON_TRANSITION {\n        setflag(%s)\n    }\n" % flag
        pory += "}\n"
        pory += msg(name + "_EventScript_TownSign", spec["sign"], "MSGBOX_SIGN")
        if name in GYMS and "gym" in t.warps:
            gy = GYMS[name]
            pory += msg(name + "_EventScript_GymSign", "%s Pokémon Gym\nLeader: %s. %s-type Pokémon." % (
                spec["sign"].split("\n")[0], gy["name"], gy["type"]), "MSGBOX_SIGN")
        for n, text in t.special_signs:
            pory += msg("%s_EventScript_Sign%d" % (name, n), text, "MSGBOX_SIGN")
        pory += pory_npcs
        write_pory(name, pory)
        gen[name] = file_hash(*map_paths(name, ldir))
        print("%-16s %dx%d  warps %d  houses %d  npcs %d%s" % (name, t.w, t.h, len(warps), t.n_houses, len(objs),
                                                             "" if flag else "  (no fly flag for its section)"))

    lj["layouts"] = list(layouts.values())
    PH.write_json(lj_path, lj)
    PH.write_json(mg_path, mg)
    with open(heal_path, "w") as f:
        json.dump(heal, f, indent=2, ensure_ascii=False)
        f.write("\n")
    if new_includes:
        es_path = P("data", "event_scripts.s")
        es = open(es_path).read()
        lines = es.split("\n")
        group_set = set(mg[GROUP])
        last = max(i for i, l in enumerate(lines)
                   if re.match(r'\s*\.include "data/maps/(\w+)/scripts.inc"', l)
                   and re.match(r'\s*\.include "data/maps/(\w+)/scripts.inc"', l).group(1) in group_set
                   and re.match(r'\s*\.include "data/maps/(\w+)/scripts.inc"', l).group(1) not in new_includes)
        add = ['\t.include "data/maps/%s/scripts.inc"' % f for f in new_includes
               if ('data/maps/%s/scripts.inc' % f) not in es]
        lines[last + 1:last + 1] = add
        open(es_path, "w").write("\n".join(lines))
    json.dump(gen, open(GEN_PATH, "w"), indent=1, sort_keys=True)


GYM_LAYOUT = ("LAYOUT_DEWFORD_TOWN_GYM", [(5, 27), (6, 27)], (4, 3), (5, 24))


def write_gym(name, m, idx, warps, group, new_includes, gen):
    gy = GYMS[name]
    folder = name + "_Gym"
    iid = "MAP_" + PH.snake(name) + "_GYM"
    lid, exits, (lx, ly), (gx, gyy) = GYM_LAYOUT
    warps[idx].update(dest_map=iid, dest_warp_id="0")
    town = m["region_map_section"]
    objs = [obj(gy["gfx"], lx, ly, 3, "down", folder + "_EventScript_Leader"),
            obj("OBJ_EVENT_GFX_MAN_2", gx, gyy, 3, "down", folder + "_EventScript_Guide")]
    ij = OrderedDict([
        ("id", iid), ("name", folder), ("layout", lid), ("music", "MUS_GYM"),
        ("region", m.get("region", "REGION_HOENN")), ("region_map_section", town),
        ("requires_flash", False), ("weather", "WEATHER_NONE"), ("map_type", "MAP_TYPE_INDOOR"),
        ("allow_cycling", False), ("allow_escaping", False), ("allow_running", False),
        ("show_map_name", False), ("battle_scene", "MAP_BATTLE_SCENE_GYM"), ("connections", None),
        ("object_events", objs),
        ("warp_events", [OrderedDict([("x", ex), ("y", ey), ("elevation", 0), ("dest_map", m["id"]),
                                      ("dest_warp_id", str(idx))]) for ex, ey in exits]),
        ("coord_events", []), ("bg_events", [])])
    PH.write_json(P("data", "maps", folder, "map.json"), ij)
    badge = gy["badge"]
    q = lambda t: t.replace('"', "'")
    pory = "mapscripts %s_MapScripts {}\n" % folder
    pory += """
script %(f)s_EventScript_Leader {
    trainerbattle_single(%(c)s, %(f)s_Text_Intro, %(f)s_Text_Defeat, %(f)s_EventScript_Defeated, NO_MUSIC)
    msgbox(%(f)s_Text_Post, MSGBOX_AUTOCLOSE)
}

script %(f)s_EventScript_Defeated {
    setflag(%(badge)s)
    msgbox(format("{PLAYER} received the %(n)s Gym Badge!\\p(Placeholder Gym: the badge flag is set.)"))
    release
}

script %(f)s_EventScript_Guide {
    msgbox(format("Hey, Challenger! This is the Gym of %(n)s, who uses %(ty)s-type Pokémon.\\pThe Gym's still being fitted out. For now it's just you, %(n)s and this empty hall!"), MSGBOX_NPC)
}

text %(f)s_Text_Intro {
    format("%(intro)s")
}

text %(f)s_Text_Defeat {
    format("%(defeat)s")
}

text %(f)s_Text_Post {
    format("%(post)s")
}
""" % dict(f=folder, c=gy["const"], badge=badge, n=gy["name"], ty=gy["type"], intro=q(gy["intro"]),
           defeat=q(gy["defeat"]), post=q(gy["post"]))
    write_pory(folder, pory)
    if folder not in group:
        group.append(folder)
        new_includes.append(folder)
    gen[folder] = file_hash(P("data", "maps", folder, "map.json"))


def patch_gym_trainers():
    """Rename the vanilla gym-leader slots to the Tosa leaders and give them placeholder teams."""
    oph = P("include", "constants", "opponents.h")
    src = open(oph).read()
    aliases = []
    for town, gy in GYMS.items():
        slot, const = gy["slot"], gy["const"]
        src = re.sub(r"#define %s(\s+)(\d+)" % slot, lambda mm: "#define %s%s%s" % (
            const, " " * max(1, len(slot) + len(mm.group(1)) - len(const)), mm.group(2)), src)
        aliases.append("#define %-37s %s" % (slot, const))
    block = ("// Orchid: the vanilla gym-leader slots were reused for the Tosa Gym Leaders (placeholder teams).\n"
             + "\n".join(aliases) + "\n")
    marker = "// Orchid: the vanilla gym-leader slots"
    if marker in src:
        start = src.index(marker)
        end = src.index("\n\n", start) + 1
        src = src[:start] + block + src[end:]
    else:
        anchor = "// NOTE: Because each Trainer uses a flag"
        src = src.replace(anchor, block + "\n" + anchor)
    open(oph, "w").write(src)
    tp = P("src", "data", "trainers.party")
    party = open(tp).read()
    for town, gy in GYMS.items():
        body = ["=== %s ===" % gy["const"], "Name: %s" % gy["name"], "Class: Leader", "Pic: %s" % gy["pic"],
                "Gender: %s" % gy["gender"], "Music: %s" % gy["gender"], "Double Battle: No", "AI: Basic Trainer", ""]
        for sp, lv in gy["party"]:
            body += [sp, "Level: %d" % lv, ""]
        new = "\n".join(body) + "\n"
        for head in ("=== %s ===" % gy["slot"], "=== %s ===" % gy["const"]):
            if head in party:
                i = party.index(head)
                j = party.find("\n=== ", i + 4)
                j = len(party) if j < 0 else j + 1
                party = party[:i] + new + party[j:]
                break
        else:
            raise SystemExit("no trainers.party entry for " + gy["slot"])
    open(tp, "w").write(party)


def folder_of(map_id):
    for f in os.listdir(P("data", "maps")):
        mj = P("data", "maps", f, "map.json")
        if os.path.exists(mj) and f[0].isupper():
            try:
                if json.load(open(mj)).get("id") == map_id:
                    return f
            except ValueError:
                pass
    raise KeyError(map_id)


def write_pory(folder, text):
    open(P("data", "maps", folder, "scripts.pory"), "w").write(text)
    stale = P("data", "maps", folder, "scripts.inc")
    if os.path.exists(stale):
        os.remove(stale)


if __name__ == "__main__":
    main()
