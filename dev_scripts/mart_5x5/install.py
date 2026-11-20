#!/usr/bin/env python3
"""Replace every 4x5 v2 Poke Mart on the maps with the 5x5 Mart (art/mart.png).

    python install.py            # dry run: report the placements and the tile budget
    python install.py --write    # apply

* Finds each Mart by its 2x2 door pair (METATILE_General_Door_PokeMart / _Right) and grows the box
  by one column on the side with plain ground (SIDE overrides). The door ends up on one of the old
  door cells, so the ground in front of it is unchanged.
* gTileset_General: the old Mart's tiles and metatiles are recycled (plus tiles only unplaced
  metatiles still reference); 25 canonical metatiles over grass and per-town ground variants as in
  ../centre_mart_v2/integrate.py (row 0 top layer over sprites, rows 1-4 COVERED).
* Door: a 1x2 animated door (column 2, rows 3-4), like the Centre's. The second door warp is
  removed and warp ids pointing past it are renumbered in every map.
* Objects on the new column (the Mart signpost, NPCs) move: the signpost to the far side of the
  new front row when it can, anything else to the nearest free walkable cell.
"""
import json
import os
import re
import struct
import sys
from collections import defaultdict

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "centre_mart_v2"))
from common import ROOT, GEN, layouts, maps, read_grid, write_grid, behaviours, tset, attr_of, meta_of  # noqa: E402
from integrate import read_pal, to_indices, Bank, flips, ANIMATED, GRASS_MT, NORMAL, COVERED, DOOR_BITS, \
    save_indexed, open_door, door_glass  # noqa: E402

OLD_DOOR, OLD_DOOR_R = 0x097, 0x09D
W, H = 5, 5
DOOR = (2, 4)
PAL = 0
MB = behaviours()
PLAIN = (MB["MB_NORMAL"], MB["MB_TALL_GRASS"], MB["MB_SAND"])
SIDE = {"LAYOUT_BATTLE_FRONTIER_OUTSIDE_WEST": "R"}   # over a bench instead of half a tree
# Four Island: a house was laid over the old Mart's right half; the new Mart moves left over the
# stray cliff/door fragments and the old roof pieces left above the house become grass.
SPECIAL = {"LAYOUT_FOUR_ISLAND": dict(old=(21, 22), cells={(21 + i, 22 + j) for i in range(2) for j in range(5)}
                                      | {(23, 22), (24, 22)}, new=(18, 22), clear={(23, 22): 0x001, (24, 22): 0x001})}
# cells copied elsewhere before the Mart is drawn over them: {layout: [((from), (to)), ...]}
# (Timah's left flower planter is simply covered: the signpost takes that side)
MOVE_CELLS = {}
SIGN = "OBJ_EVENT_GFX_MART_SIGN"


def main(write):
    L, M = layouts(), maps()
    gen = tset("gTileset_General")
    pal = read_pal(PAL)
    art = np.array(Image.open(os.path.join(HERE, "art", "mart.png")).convert("RGBA"))
    ind = to_indices(art, pal)
    alpha = art[:, :, 3] > 0

    live = defaultdict(list)
    for mid, (p, js) in M.items():
        live[js["layout"]].append((mid, p, js))
    grids = {lid: read_grid(L[lid]) for lid in live if L[lid].get("primary_tileset") == "gTileset_General"}
    grids = {k: g for k, g in grids.items() if g is not None}

    # ------------------------------------------------------------ find the Marts + choose a side
    def events(lid):
        out = []
        for mid, p, js in live[lid]:
            for k in ("object_events", "warp_events", "bg_events", "coord_events"):
                for o in js.get(k) or []:
                    out.append((k, o, mid))
        return out

    def plain(lid, x, y):
        g = grids[lid]
        if not (0 <= y < len(g) and 0 <= x < len(g[0])):
            return False
        v = g[y][x]
        return not (v >> 10) & 3 and (attr_of(L[lid], v & 0x3FF) & 0xFF) in PLAIN

    marts = []
    for lid, g in grids.items():
        for y, row in enumerate(g):
            for x, v in enumerate(row):
                if (v & 0x3FF) == OLD_DOOR and x + 1 < len(row) and (row[x + 1] & 0x3FF) == OLD_DOOR_R:
                    marts.append(dict(layout=lid, old=(x - 1, y - 4)))
    for lid, sp in SPECIAL.items():
        marts.append(dict(layout=lid, old=sp["old"], special=sp))
    old_cells = defaultdict(set)
    for m in marts:
        bx, by = m["old"]
        old_cells[m["layout"]] |= m["special"]["cells"] if "special" in m else \
            {(bx + i, by + j) for i in range(4) for j in range(5)}

    for m in marts:
        lid, (bx, by) = m["layout"], m["old"]
        if "special" in m:
            nx, ny = m["new"] = m["special"]["new"]
            m["door"] = (nx + DOOR[0], ny + DOOR[1])
            m["side"], m["cost"], m["forced"] = "moved", {"moved": ([], [])}, ["moved"]
            continue
        ev = events(lid)
        cost = {}
        for side, cx in (("L", bx - 1), ("R", bx + 4)):
            hard, movable = [], []
            for cy in range(by, by + 5):
                if (cx, cy) in old_cells[lid]:
                    hard.append((cx, cy, "other mart"))
                elif not plain(lid, cx, cy):
                    hard.append((cx, cy, f"{grids[lid][cy][cx] & 0x3FF:03x}" if 0 <= cy < len(grids[lid]) and 0 <= cx < len(grids[lid][0]) else "edge"))
                for k, o, _ in ev:
                    if (o["x"], o["y"]) == (cx, cy):
                        (hard if k == "warp_events" else movable).append((cx, cy, o.get("graphics_id") or o.get("script")))
            cost[side] = (hard, movable)
        side = SIDE.get(lid) or min("LR", key=lambda s: (len(cost[s][0]), len(cost[s][1]), s != "L"))
        m["side"], m["cost"] = side, cost
        nx = bx - 1 if side == "L" else bx
        m["new"] = (nx, by)
        m["door"] = (nx + DOOR[0], by + DOOR[1])
        m["forced"] = cost[side][0]
    new_cells = defaultdict(set)
    for m in marts:
        nx, ny = m["new"]
        new_cells[m["layout"]] |= {(nx + i, ny + j) for i in range(W) for j in range(H)}
    for m in marts:
        print(f"{m['layout']:40s} old {m['old']} -> {m['side']} new {m['new']}"
              + (f"  FORCED over {m['forced']}" if m["forced"] else "")
              + (f"  moves {m['cost'][m['side']][1]}" if m["cost"][m["side"]][1] else ""))

    # ------------------------------------------------------------ what dies: metatiles
    sec_in, sec_out, prim_out = defaultdict(set), defaultdict(set), set()
    prim_in = set()
    for lid, g in grids.items():
        s = L[lid]["secondary_tileset"]
        for y, row in enumerate(g):
            for x, v in enumerate(row):
                mt = v & 0x3FF
                inside = (x, y) in old_cells[lid]
                if mt >= 0x200:
                    (sec_in if inside else sec_out)[s].add(mt)
                else:
                    (prim_in if inside else prim_out).add(mt)
        for v in struct.unpack("<4H", open(os.path.join(ROOT, L[lid]["border_filepath"]), "rb").read()[:8]):
            (prim_out if (v & 0x3FF) < 0x200 else sec_out[s]).add(v & 0x3FF)
    labels_h = open(os.path.join(ROOT, "include", "constants", "metatile_labels.h")).read()
    labelled = {int(v, 16) for n, v in re.findall(r"#define (METATILE_General_\w+)\s+(0x[0-9A-Fa-f]+)", labels_h)
                if not n.startswith("METATILE_General_Door_PokeMart")}
    keep_prim = prim_out | labelled | {0}
    dying_prim = sorted(prim_in - keep_prim)                  # old Mart canonical + primary variants
    spare_prim = sorted(m for m in range(1, 0x200) if m not in keep_prim and m not in prim_in
                        and not any(gen.meta[m]))              # blank, unplaced
    prim_pool = dying_prim + spare_prim
    dying_sec = {s: sorted(ids - sec_out[s]) for s, ids in sec_in.items()}

    # ------------------------------------------------------------ merge duplicate General tiles
    # Identical 8x8 tiles (incl. flipped copies) are merged into one slot in every metatile that
    # can see General's tiles, which frees the copies without changing a pixel on screen.
    tiles_im = Image.open(os.path.join(GEN, "tiles.png"))
    tpx = np.array(tiles_im)
    tw = tiles_im.width // 8
    n_rows = tpx.shape[0] // 8

    def tile_at(i):
        r, c = divmod(i, tw)
        return tpx[r * 8:(r + 1) * 8, c * 8:(c + 1) * 8].copy()

    general_secs = sorted({e["secondary_tileset"] for e in L.values()
                           if e.get("primary_tileset") == "gTileset_General" and str(e.get("secondary_tileset", "0")).startswith("gTileset_")})
    seen, remap = {}, {}
    for i in range(min(512, n_rows * tw)):
        if i in ANIMATED:
            continue
        t = tile_at(i)
        hit = next(((seen[v.tobytes()], h, vf) for v, h, vf in flips(t) if v.tobytes() in seen), None)
        if hit:
            remap[i] = hit
        else:
            seen[t.tobytes()] = i
    merged_secs = set()

    def merge(meta):
        changed = False
        for k, e in enumerate(meta):
            t = e & 0x3FF
            if t in remap:
                to, h, v = remap[t]
                meta[k] = (e & 0xF000) | to | ((e >> 10 & 1) ^ h) << 10 | ((e >> 11 & 1) ^ v) << 11
                changed = True
        return changed

    for mm in gen.meta:
        merge(mm)
    for s in general_secs:
        for mm in tset(s).meta:
            if merge(mm):
                merged_secs.add(s)
    print(f"merged {len(remap)} duplicate tiles: {sorted(remap)}")

    # ------------------------------------------------------------ what dies: tiles
    strict_ref, map_ref = set(), set()
    for mt in keep_prim:
        strict_ref |= {e & 0x3FF for e in gen.meta[mt]}
    map_ref |= strict_ref
    for mt in range(1, 0x200):
        if mt not in keep_prim and mt not in prim_in:
            strict_ref |= {e & 0x3FF for e in gen.meta[mt] if any(gen.meta[mt])}
    used_sec = defaultdict(set)
    for lid, g in grids.items():
        for row in g:
            for v in row:
                if (v & 0x3FF) >= 0x200:
                    used_sec[L[lid]["secondary_tileset"]].add(v & 0x3FF)
    for s in general_secs:                     # metatiles scripts place (labels) count as used
        used_sec[s] |= {int(v, 16) for v in re.findall(
            r"#define METATILE_" + s[len("gTileset_"):] + r"_\w+\s+(0x[0-9A-Fa-f]+)", labels_h)}
    for s in general_secs:
        st = tset(s)
        dead = set(dying_sec.get(s, []))
        for i, mm in enumerate(st.meta):
            if 0x200 + i in dead:
                continue
            refs = {e & 0x3FF for e in mm if (e & 0x3FF) < 0x200}
            strict_ref |= refs
            if 0x200 + i in used_sec[s] - dead:
                map_ref |= refs
    strict_free = [t for t in range(1, 512) if t not in strict_ref and t not in ANIMATED]
    lax_free = [t for t in range(1, 512) if t not in map_ref and t not in ANIMATED and t not in strict_free]
    free = [t for t in strict_free + lax_free if t // tw < n_rows]

    existing = {t: tile_at(t) for t in sorted(map_ref) if t // tw < n_rows and t not in ANIMATED and t not in free}
    bank = Bank(free, existing)

    def entry(x0, y0):
        idx, hf, vf = bank.add(ind[y0:y0 + 8, x0:x0 + 8].copy())
        return idx | hf << 10 | vf << 11 | PAL << 12

    grass = gen.meta[GRASS_MT][:4]

    def build_cell(cx, cy, ground):
        quads, opaque = [], True
        for q in range(4):
            x0, y0 = cx * 16 + (q & 1) * 8, cy * 16 + (q >> 1) * 8
            a = alpha[y0:y0 + 8, x0:x0 + 8]
            opaque &= bool(a.all())
            quads.append(entry(x0, y0) if a.any() else 0)
        if cy == 0:
            bottom, top, layer = list(ground), quads, NORMAL
        elif opaque:
            bottom, top, layer = quads, [0] * 4, COVERED
        else:
            bottom, top, layer = list(ground), quads, COVERED
        door = (cx, cy) == DOOR
        if door or (cx, cy + 1) == DOOR:
            assert opaque, ("door cells must be opaque", cx, cy)
        beh = MB["MB_ANIMATED_DOOR"] if door else MB["MB_NORMAL"]
        return tuple(bottom + top), beh | layer << 12, opaque

    canonical = {(cx, cy): build_cell(cx, cy, grass) for cy in range(H) for cx in range(W)}

    def ground_of(lid, x, y):
        if not plain(lid, x, y):
            return None
        return tuple(meta_of(L[lid], grids[lid][y][x] & 0x3FF)[:4])

    def old_ground(lid, x, y):
        """ground the old Mart drew under a transparent cell at (x, y), if it was one"""
        v = grids[lid][y][x] & 0x3FF
        mm = meta_of(L[lid], v)
        if any(mm[4:]) and (attr_of(L[lid], v) >> 12) in (NORMAL, COVERED) and mm[:4] != [0] * 4:
            return tuple(mm[:4])
        return None

    assignments = []
    for m in marts:
        lid = m["layout"]
        nx, ny = m["new"]
        cells = {}
        for cy in range(H):
            for cx in range(W):
                ent, at, opaque = canonical[(cx, cy)]
                if not opaque:
                    x, y = nx + cx, ny + cy
                    probes = []
                    if cy == 0:
                        probes.append((x, y - 1))
                    if cx == 0:
                        probes.append((x - 1, y))
                    if cx == W - 1:
                        probes.append((x + 1, y))
                    if cy == H - 1:
                        probes.append((x, y + 1))
                    probes += [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]
                    gnd = None
                    for px, py in probes:
                        if (px, py) in new_cells[lid]:
                            continue
                        gnd = ground_of(lid, px, py)
                        if gnd:
                            break
                    if gnd is None and (x, y) in old_cells[lid]:
                        gnd = old_ground(lid, x, y)
                    if gnd and gnd != tuple(grass):
                        c = build_cell(cx, cy, gnd)
                        ent, at = c[0], c[1]
                cells[(cx, cy)] = (ent, at)
        assignments.append((m, cells))

    # ------------------------------------------------------------ metatile ids
    pool = list(prim_pool)

    def take_prim():
        if not pool:
            raise SystemExit(f"out of primary metatile slots: {len(dying_prim)} recycled + {len(spare_prim)} spare, {len(prim_variants)} variants so far")
        return pool.pop(0)

    # keep the door on its old id so the label barely moves
    pool.remove(OLD_DOOR)
    ids = {}
    for cy in range(H):
        for cx in range(W):
            ids[(cx, cy)] = OLD_DOOR if (cx, cy) == DOOR else take_prim()
    content_to_prim = {(v[0], v[1]): ids[k] for k, v in canonical.items()}
    prim_variants, sec_variants = {}, defaultdict(dict)
    sec_pool = {s: list(v) for s, v in dying_sec.items()}
    _unplaced = {}

    def unplaced_sec(s):
        """metatiles of secondary s that no layout (live or not), border or label uses"""
        if s not in _unplaced:
            used = set()
            for e in L.values():
                if e.get("secondary_tileset") != s:
                    continue
                gg = grids.get(e["id"]) or read_grid(e)
                for row in gg or []:
                    used |= {v & 0x3FF for v in row}
                for v in struct.unpack("<4H", open(os.path.join(ROOT, e["border_filepath"]), "rb").read()[:8]):
                    used.add(v & 0x3FF)
            name = s[len("gTileset_"):]
            lab = {int(v, 16) for v in re.findall(r"#define METATILE_" + name + r"_\w+\s+(0x[0-9A-Fa-f]+)", labels_h)}
            n = len(tset(s).meta)
            cand = [0x200 + i for i in range(n) if 0x200 + i not in used and 0x200 + i not in lab]
            cand.sort(key=lambda m: any(tset(s).meta[m - 0x200]))      # blank ones first
            _unplaced[s] = cand
            print(f"  {s} is full: {len(cand)} unplaced metatiles to recycle")
        return _unplaced[s]

    placed = []
    for m, cells in assignments:
        s = L[m["layout"]]["secondary_tileset"]
        out = {}
        for k, content in cells.items():
            if content in content_to_prim:
                out[k] = content_to_prim[content]
            else:                       # ground variants live in the town's secondary (General is full)
                if content not in sec_variants[s]:
                    st = tset(s)
                    if sec_pool.get(s):
                        mid = sec_pool[s].pop(0)
                    elif len(st.meta) >= 512:   # secondary full: recycle a metatile no map places
                        mid = unplaced_sec(s).pop(0)
                    else:
                        mid = 0x200 + len(st.meta)
                        st.meta.append([0] * 8)
                        st.attr.append(0)
                    sec_variants[s][content] = mid
                out[k] = sec_variants[s][content]
        placed.append((m, out))

    print(f"\n{len(marts)} Marts; tiles: {len(strict_free)} free + {len(lax_free)} only on unplaced metatiles; "
          f"art needs {len(bank.new)} new, reuses {bank.reused}; {len(bank.free)} left; short {bank.short}")
    print(f"  lax slots used: {sorted(t for t in bank.new if t in lax_free)}")
    print(f"metatiles: 25 canonical, {len(prim_variants)} primary variants, "
          + ", ".join(f"{s}: {len(v)}" for s, v in sec_variants.items()))
    print(f"primary metatile pool: {len(dying_prim)} recycled + {len(spare_prim)} spare; {len(pool)} left")
    for s in sec_variants:
        print(f"  {s}: {len(tset(s).meta)} metatiles")
        assert len(tset(s).meta) <= 512, s
    if bank.short:
        raise SystemExit("NOT ENOUGH TILE SPACE")
    if not write:
        print("dry run; pass --write")
        return

    # ------------------------------------------------------------ write tilesets
    for idx, t in bank.new.items():
        r, c = divmod(idx, tw)
        tpx[r * 8:(r + 1) * 8, c * 8:(c + 1) * 8] = t
    out_im = Image.fromarray(tpx, "P")
    out_im.putpalette(tiles_im.getpalette())
    out_im.save(os.path.join(GEN, "tiles.png"), bits=4, optimize=False)
    for mt in dying_prim:
        gen.meta[mt], gen.attr[mt] = [0] * 8, 0
    for k, (ent, at, _) in canonical.items():
        gen.meta[ids[k]], gen.attr[ids[k]] = list(ent), at
    for (ent, at), mid in prim_variants.items():
        gen.meta[mid], gen.attr[mid] = list(ent), at
    gen.save()
    for s, d in sec_variants.items():
        st = tset(s)
        for (ent, at), mid in d.items():
            st.meta[mid - 0x200], st.attr[mid - 0x200] = list(ent), at
    for s, rest in sec_pool.items():
        st = tset(s)
        for mid in rest:
            st.meta[mid - 0x200], st.attr[mid - 0x200] = [0] * 8, 0
    for s in set(sec_variants) | set(sec_pool) | merged_secs:
        tset(s).save()

    # ------------------------------------------------------------ write maps
    by_layout = defaultdict(list)
    for m, out in placed:
        lid = m["layout"]
        g = grids[lid]
        bx, by = m["old"]
        nx, ny = m["new"]
        for (sx, sy), (tx, ty) in MOVE_CELLS.get(lid, []):
            g[ty][tx] = g[sy][sx]
        for (cx_, cy_), mt in m.get("special", {}).get("clear", {}).items():
            g[cy_][cx_] = mt | (g[cy_][cx_ + 1] & 0xF000)
        newc = {(nx + i, ny + j) for i in range(W) for j in range(H)}
        front = g[min(ny + H, len(g) - 1)][nx + DOOR[0]]
        elev = (front >> 12) & 0xF
        if elev in (0, 15):
            elev = 3
        for (cx, cy), mid in out.items():
            x, y = nx + cx, ny + cy
            if (cx, cy) == DOOR:
                bits = DOOR_BITS
            elif cy == 0:
                above = g[y - 1][x] if y > 0 else 0x0400
                behind_walkable = y > 0 and not ((above >> 10) & 3) and (x, y - 1) not in new_cells[lid]
                bits = (above & 0xF000) if behind_walkable else (elev << 12) | 0x0400
            else:
                bits = (elev << 12) | 0x0400
            g[y][x] = mid | bits
        by_layout[lid].append(m)

    removed = {}                                   # map id -> removed warp index
    for lid, ms in by_layout.items():
        write_grid(L[lid], grids[lid])
        for mid, path, js in live[lid]:
            changed = False
            warps = js.get("warp_events") or []
            taken = {(o["x"], o["y"]) for k in ("object_events", "warp_events", "bg_events", "coord_events")
                     for o in js.get(k) or []}
            for m in ms:
                bx, by = m["old"]
                nx, ny = m["new"]
                dl, dr = (bx + 1, by + 4), (bx + 2, by + 4)
                pair = [i for i, w in enumerate(warps) if (w["x"], w["y"]) in (dl, dr) and (w["x"], w["y"]) in old_cells[lid]]
                if pair:
                    keep = pair[0]
                    warps[keep]["x"], warps[keep]["y"] = m["door"]
                    for i in reversed(pair[1:]):
                        assert mid not in removed, "two Marts' warps removed in one map: renumbering needs a list"
                        removed[mid] = i
                        del warps[i]
                    changed = True
                newc = {(nx + i, ny + j) for i in range(W) for j in range(H)}
                for o in js.get("object_events") or []:
                    if (o["x"], o["y"]) not in newc:
                        continue
                    cands = []
                    if o.get("graphics_id") == SIGN:
                        cands = [(nx + W, ny + 4), (nx - 1, ny + 4)]
                    best = next((c for c in cands if c not in taken and plain(lid, *c) and c not in new_cells[lid]), None)
                    for r in range(1, 6):
                        if best:
                            break
                        for dy in range(-r, r + 1):
                            for dx in range(-r, r + 1):
                                c = (o["x"] + dx, o["y"] + dy)
                                if c not in taken and c not in new_cells[lid] and plain(lid, *c):
                                    best = c
                                    break
                            if best:
                                break
                    print(f"  {mid}: {o.get('graphics_id')} ({o['x']},{o['y']}) -> {best}")
                    taken.discard((o["x"], o["y"]))
                    if best:
                        o["x"], o["y"] = best
                        taken.add(best)
                    changed = True
                # "read the Mart sign" spots go on the window display: front row, columns 3-4
                shop = sorted((o for o in js.get("bg_events") or []
                               if o.get("script") == "Common_EventScript_ShowPokemartSign" and ny + 3 <= o["y"] <= ny + 4
                               and nx - 1 <= o["x"] <= nx + W), key=lambda o: o["x"])
                for o, x in zip(shop, (nx + 3, nx + 4)):
                    if (o["x"], o["y"]) != (x, ny + 4):
                        print(f"  {mid}: Mart sign event ({o['x']},{o['y']}) -> ({x},{ny + 4})")
                        o["x"], o["y"] = x, ny + 4
                        changed = True
                for k in ("bg_events", "coord_events"):
                    for o in js.get(k) or []:
                        if (o["x"], o["y"]) in newc and o not in shop:
                            print(f"  WARNING {mid}: {k} {o.get('script')} at ({o['x']},{o['y']}) now inside the Mart")
            if changed:
                with open(path, "w") as f:
                    json.dump(js, f, indent=2, ensure_ascii=False)
                    f.write("\n")

    # warp ids pointing past a removed warp shift down by one
    for mid2, (path, js) in maps().items():
        changed = False
        for w in js.get("warp_events") or []:
            if w.get("dest_map") in removed:
                i = int(w["dest_warp_id"])
                r = removed[w["dest_map"]]
                if i == r:
                    print(f"  WARNING {mid2}: warp into removed {w['dest_map']} warp {i}")
                if i > r:
                    w["dest_warp_id"] = str(i - 1) if isinstance(w["dest_warp_id"], str) else i - 1
                    changed = True
        if changed:
            with open(path, "w") as f:
                json.dump(js, f, indent=2, ensure_ascii=False)
                f.write("\n")
            print(f"  renumbered warps in {mid2}")

    # ------------------------------------------------------------ labels, door frames
    txt = open(os.path.join(ROOT, "include", "constants", "metatile_labels.h")).read()
    txt = re.sub(r"#define METATILE_General_Door_PokeMart\s+0x[0-9A-Fa-f]+",
                 f"#define METATILE_General_Door_PokeMart         0x{ids[DOOR]:03X}", txt)
    txt = re.sub(r"#define METATILE_General_Door_PokeMart_Right\s+0x[0-9A-Fa-f]+\n", "", txt)
    open(os.path.join(ROOT, "include", "constants", "metatile_labels.h"), "w").write(txt)
    door_frames(ind, pal)
    json.dump(dict(ids={f"mart_{k[0]}_{k[1]}": v for k, v in ids.items()},
                   marts=[dict(layout=m["layout"], new=m["new"], side=m["side"], forced=m["forced"]) for m in marts]),
              open(os.path.join(HERE, "installed.json"), "w"), indent=1)
    print("written")


def door_frames(ind, pal):
    """1x2 door (column 2, rows 3-4): the glass slides apart from the middle."""
    blues = [i for i, col in enumerate(pal) if i and col[2] > col[0] + 60]
    gy0, gy1, gx0, gx1 = door_glass(ind, 32, 48, 64, 80, blues)
    frames = []
    for half in (2, 4, 7):
        frames.append(open_door(ind[48:80, 32:48], (gy0 - 48, gy1 - 48), (gx0 + gx1) // 2 - 32,
                                min(half, (gx1 - gx0) // 2), 7, 6))
    save_indexed(np.concatenate(frames, axis=0), pal, os.path.join(ROOT, "graphics", "door_anims", "poke_mart.png"))


if __name__ == "__main__":
    if "--doors-only" in sys.argv:
        p = read_pal(PAL)
        door_frames(to_indices(np.array(Image.open(os.path.join(HERE, "art", "mart.png")).convert("RGBA")), p), p)
    else:
        main("--write" in sys.argv)
