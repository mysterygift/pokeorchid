"""
Ice-floor puzzle check for the Icefall Cave mockups (batch 3).

Same rules and the same guarantee as dev_scripts/cold_storage_tileset/test_map.py's --solve (that solver is
hard-wired to the Cold Storage grid, its boss scene and its key/console states, so its BFS is restated here
for a plain room): on ice you keep sliding until the next cell is not walkable; you stop on the first non-ice
cell. The room passes only if the goal is reachable AND, from every reachable state, both the goal and the
entry are still reachable (no softlock, the way out always exists -- the lesson from Cold Storage).

Grid chars:  ~ ice   . floor (non-slip)   o single non-slip spot in the ice   B boulder / ice block
             E entry (walkable floor cell the warp drops you on)   G goal (ladder / hatch cell, floor)
usage: <venv python> dev_scripts/voyages/ice_puzzle.py      -> prints the check for specs_batch3.ICE_GRID
"""
from collections import deque

WALK = set(".oEG~")
ICE = set("~")
DIRS = {"N": (0, -1), "S": (0, 1), "W": (-1, 0), "E": (1, 0)}


def _cell(grid, x, y):
    return grid[y][x] if 0 <= y < len(grid) and 0 <= x < len(grid[0]) else "#"


def moves(grid, pos):
    for d, (dx, dy) in DIRS.items():
        p = (pos[0] + dx, pos[1] + dy)
        if _cell(grid, *p) not in WALK:
            continue
        while _cell(grid, *p) in ICE:
            q = (p[0] + dx, p[1] + dy)
            if _cell(grid, *q) not in WALK:
                break
            p = q
        yield d, p


def find(grid, ch):
    return [(x, y) for y, r in enumerate(grid) for x, c in enumerate(r) if c == ch]


def solve(grid):
    """-> dict(states, route (shortest entry->goal, one letter per input), back (goal->entry), stuck)."""
    entry, goals = find(grid, "E")[0], set(find(grid, "G"))
    prev, order = {entry: None}, deque([entry])
    while order:
        s = order.popleft()
        for d, n in moves(grid, s):
            if n not in prev:
                prev[n] = (s, d)
                order.append(n)

    def route(t):
        out = []
        while prev[t]:
            t, d = prev[t]
            out.append(d)
        return "".join(out[::-1])

    rev = {}
    for s in prev:
        for _, n in moves(grid, s):
            rev.setdefault(n, set()).add(s)

    def can_reach(targets):
        good, q = set(targets) & set(prev), deque(set(targets) & set(prev))
        while q:
            s = q.popleft()
            for p in rev.get(s, ()):
                if p not in good:
                    good.add(p)
                    q.append(p)
        return good

    to_goal, to_entry = can_reach(goals), can_reach({entry})
    stuck = [s for s in prev if s not in to_goal or s not in to_entry]
    reached = [g for g in goals if g in prev]
    best = min(reached, key=lambda g: len(route(g))) if reached else None
    back = None
    if best:                                   # shortest way back out from the goal
        p2, q = {best: None}, deque([best])
        while q:
            s = q.popleft()
            for d, n in moves(grid, s):
                if n not in p2:
                    p2[n] = (s, d)
                    q.append(n)
        t, out = entry, []
        while p2.get(t):
            t, d = p2[t]
            out.append(d)
        back = "".join(out[::-1])
    return dict(states=len(prev), route=route(best) if best else None, back=back, stuck=stuck)


def report(grid, name=""):
    r = solve(grid)
    ok = r["route"] is not None and not r["stuck"]
    print("%s ice check: %s | reachable cells %d | stuck %d | in %s (%d inputs) | out %s (%d inputs)" % (
        name, "PASS" if ok else "FAIL", r["states"], len(r["stuck"]), r["route"], len(r["route"] or ""),
        r["back"], len(r["back"] or "")))
    return ok, r


if __name__ == "__main__":
    import specs_batch3 as sp
    report(sp.ICE_GRID, "Icefall Cave ice room")
