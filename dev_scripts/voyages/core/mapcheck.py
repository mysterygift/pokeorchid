"""
Walkability check for the core voyage maps: ASCII collision dump + BFS on foot (elevation rules, one-way ledges,
no Surf) from an arrival cell to target cells.

usage: <venv python> mapcheck.py LAYOUT_ID [sx sy tx ty ...]  (prints the map, then reach for each target)
"""
import os
import sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import voyage_compose as vc   # noqa: E402

JUMP = {0x38: (1, 0), 0x39: (-1, 0), 0x3A: (0, -1), 0x3B: (0, 1)}


def load(lid):
    e, g = vc.raw_layout(lid)
    sc = vc.scene((e["primary_tileset"], e["secondary_tileset"]))

    def beh(v):
        m = v & 0x3FF
        return (sc.p.attrs[m] if m < 0x200 else sc.s.attrs[m - 0x200]) & 0xFF
    return g, beh


def reach(g, beh, start, blocked=()):
    h, w = len(g), len(g[0])
    z0 = g[start[1]][start[0]] >> 12
    seen = {(start, z0)}
    q = deque([(start, z0)])
    cells = {start}
    while q:
        (x, y), z = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < w and 0 <= ny < h) or (nx, ny) in blocked:
                continue
            v = g[ny][nx]
            b = beh(v)
            if b in JUMP and JUMP[b] == (dx, dy):
                nx, ny = nx + dx, ny + dy
                if not (0 <= nx < w and 0 <= ny < h):
                    continue
                v = g[ny][nx]
                b = beh(v)
            if (v >> 10) & 3 or b in vc.WATER_BEHAVIORS:
                continue
            tz = v >> 12
            if tz not in (0, 15) and z not in (0, 15) and tz != z:
                continue
            nz = z if tz in (0, 15) else tz
            if ((nx, ny), nz) not in seen:
                seen.add(((nx, ny), nz))
                cells.add((nx, ny))
                q.append(((nx, ny), nz))
    return cells


def dump(g, beh, marks=None):
    marks = marks or {}
    print("    " + "".join("%d" % (x % 10) for x in range(len(g[0]))))
    for y, row in enumerate(g):
        s = ""
        for x, v in enumerate(row):
            if (x, y) in marks:
                s += marks[(x, y)]
            elif beh(v) in vc.WATER_BEHAVIORS:
                s += "~"
            elif beh(v) in JUMP:
                s += "v^<>"[[0x3B, 0x3A, 0x39, 0x38].index(beh(v))]
            elif (v >> 10) & 3:
                s += "#"
            else:
                s += "%X" % (v >> 12)
        print("%3d %s" % (y, s))


if __name__ == "__main__":
    lid = sys.argv[1]
    g, beh = load(lid)
    nums = list(map(int, sys.argv[2:]))
    dump(g, beh)
    if nums:
        s = (nums[0], nums[1])
        r = reach(g, beh, s)
        for i in range(2, len(nums), 2):
            t = (nums[i], nums[i + 1])
            print("reach %s -> %s: %s" % (s, t, t in r))


def path(lid, start, goal, blocked=()):
    """Directions (UP/DOWN/LEFT/RIGHT) on foot from start to goal (same rules as reach), or None."""
    g, beh = load(lid)
    h, w = len(g), len(g[0])
    names = {(1, 0): "RIGHT", (-1, 0): "LEFT", (0, 1): "DOWN", (0, -1): "UP"}
    z0 = g[start[1]][start[0]] >> 12
    prev = {(start, z0): None}
    q = deque([(start, z0)])
    while q:
        (x, y), z = cur = q.popleft()
        if (x, y) == goal:
            out = []
            while prev[cur]:
                cur, d = prev[cur]
                out.append(d)
            return out[::-1]
        for (dx, dy), nm in names.items():
            nx, ny = x + dx, y + dy
            if not (0 <= nx < w and 0 <= ny < h) or (nx, ny) in blocked:
                continue
            v = g[ny][nx]
            b = beh(v)
            if b in JUMP and JUMP[b] == (dx, dy):
                nx, ny = nx + dx, ny + dy
                v = g[ny][nx]
                b = beh(v)
            if ((v >> 10) & 3 or b in vc.WATER_BEHAVIORS) and (nx, ny) != goal:
                continue
            tz = v >> 12
            if tz not in (0, 15) and z not in (0, 15) and tz != z and (nx, ny) != goal:
                continue
            nz = z if tz in (0, 15) else tz
            if ((nx, ny), nz) not in prev:
                prev[((nx, ny), nz)] = (cur, nm)
                q.append(((nx, ny), nz))
    return None
