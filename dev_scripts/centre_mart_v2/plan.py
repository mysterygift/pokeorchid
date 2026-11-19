#!/usr/bin/env python3
"""Where does each town's new Centre (5x5) / Mart (4x5) + Mart signpost go?  -> plan.json + report.

The old buildings are 4x4. Each new box must contain the old door column, must not touch another
building, a warp, a sign or a trigger, and prefers plain ground (grass / sand / path). If no box
fits on plain ground, the cheapest box that overwrites scenery is used and listed as FORCED.
NPCs standing on new cells are moved (listed as MOVE).

    python plan.py
"""
import json
import os

from common import HERE, layouts, maps, read_grid, attr_of, behaviours, buildings, event_cells

MB = behaviours()
OK_BEH = {MB[n] for n in ("MB_NORMAL", "MB_TALL_GRASS", "MB_SAND", "MB_LONG_GRASS") if n in MB}


def main():
    L, M = layouts(), maps()
    by_layout = {}
    for mid, (p, js) in M.items():
        by_layout.setdefault(js["layout"], []).append((mid, p, js))
    live = {lid: L[lid] for lid in by_layout}
    blds = buildings(live)
    plan = []
    for lid in sorted({b["layout"] for b in blds}):
        e = L[lid]
        g = read_grid(e)
        H, W = len(g), len(g[0])
        evs, npcs = {}, set()
        for mid, p, js in by_layout[lid]:
            for c, k in event_cells(js).items():
                evs.setdefault(c, []).extend(k)
            for o in js.get("object_events") or []:
                npcs.add((o["x"], o["y"]))
        mine = [b for b in blds if b["layout"] == lid]
        old_all = {}
        for b in mine:
            bx, by, bw, bh = b["box"]
            for i in range(bw):
                for j in range(bh):
                    old_all[(bx + i, by + j)] = id(b)
        claimed = set()
        # Centres first (bigger), then Marts, then signs
        for b in sorted(mine, key=lambda b: b["kind"]):
            bx, by, bw, bh = b["box"]
            old = {c for c, k in old_all.items() if k == id(b)}

            def hard(x, y):
                if not (0 <= x < W and 0 <= y < H) or (x, y) in claimed:
                    return True
                if (x, y) in old_all and (x, y) not in old:
                    return True                         # another building's old box
                if (x, y) in old:
                    return False
                k = evs.get((x, y), [])
                return any(t != "object_events" for t in k)

            def free(x, y):
                if (x, y) in old:
                    return True
                v = g[y][x]
                return not ((v >> 10) & 3) and (attr_of(e, v & 0x3FF) & 0xFF) in OK_BEH

            def walkable(x, y):
                if not (0 <= x < W and 0 <= y < H):
                    return False
                return (x, y) in old or not ((g[y][x] >> 10) & 3)

            cands = []
            if b["kind"] == "centre":
                size, opts = (5, 5), [(nx, ny) for nx in (bx - 1, bx) for ny in (by - 1, by - 2, by)]
                fronts = lambda nx, ny: [(nx + 2, ny + 5)]
            else:
                size, opts = (4, 5), [(bx, ny) for ny in (by - 1, by)]
                fronts = lambda nx, ny: [(nx + 1, ny + 5), (nx + 2, ny + 5)]
            for nx, ny in opts:
                cells = [(nx + i, ny + j) for i in range(size[0]) for j in range(size[1])]
                if any(hard(*c) for c in cells + fronts(nx, ny)):
                    continue
                forced = [c for c in cells if not free(*c)] + [c for c in fronts(nx, ny) if not walkable(*c)]
                cost = 100 * len(forced) + sum(c not in old for c in cells) + (0 if ny == by - 1 else 2) + (nx != bx - 1)
                cands.append((cost, nx, ny, forced))
            if not cands:
                plan.append(dict(b, new=None))
                continue
            _, nx, ny, forced = min(cands)
            cells = {(nx + i, ny + j) for i in range(size[0]) for j in range(size[1])}
            claimed |= cells | set(fronts(nx, ny))
            entry = dict(b, new=(nx, ny, *size), forced=forced,
                         move=[c for c in sorted(npcs) if c in cells - old])
            plan.append(entry)
        for entry in plan:
            if entry["layout"] != lid or entry["kind"] != "mart" or not entry["new"]:
                continue
            nx, ny, _, _ = entry["new"]
            old = {c for c, k in old_all.items() if k == id(next(b for b in mine if b["box"] == entry["box"]))}
            entry["sign"] = None
            for sx, sy in ((nx + 4, ny + 4), (nx - 1, ny + 4), (nx + 4, ny + 3), (nx - 1, ny + 3)):
                ok = (0 <= sx < W and 0 <= sy + 1 < H and (sx, sy) not in claimed and (sx, sy) not in evs
                      and ((sx, sy) in old or (not ((g[sy][sx] >> 10) & 3)
                                               and (attr_of(e, g[sy][sx] & 0x3FF) & 0xFF) in OK_BEH))
                      and (sx, sy) not in {c for c, k in old_all.items() if c not in old})
                if ok:
                    entry["sign"] = (sx, sy)
                    claimed.add((sx, sy))
                    break
    for p in plan:
        tag = "C" if p["kind"] == "centre" else "M"
        print(f"{tag} {p['layout']:<36} old {tuple(p['box'][:2])} -> new {p['new'] and tuple(p['new'][:2])}"
              + (f"  sign {p.get('sign')}" if p["kind"] == "mart" else "")
              + (f"  FORCED {p['forced']}" if p.get("forced") else "")
              + (f"  MOVE {p['move']}" if p.get("move") else ""))
    print(sum(1 for p in plan if not p["new"]), "without room;", sum(1 for p in plan if p.get("forced")), "forced")
    json.dump(plan, open(os.path.join(HERE, "plan.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
