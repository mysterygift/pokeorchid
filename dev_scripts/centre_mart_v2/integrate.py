#!/usr/bin/env python3
"""Install the v2 Pokemon Centre (5x5) and Pokemart (4x5) exteriors in every town.

Run plan.py first (it decides where each new building goes), then:

    python integrate.py            # dry run: report only
    python integrate.py --write    # apply

What it does
  * gTileset_General: new 8x8 tiles in slots freed by retiring the old Centre/Mart art (and
    tiles nothing on a map uses); 45 canonical metatiles (Centre 5x5 + Mart 4x5) over grass, plus
    variants where a town's ground under the building's transparent edges is not grass.
  * Layers: row 0 (the roof's back edge) is walkable where the ground behind it is, and its art is
    in the top layer, so the roof draws over a player walking behind the building. Every other row
    is COVERED (both layers under sprites), so a player standing in front draws over the facade.
  * Doors: Centre 1x2 animated door (bottom-middle), Mart 2x2 sliding double door. Door frames in
    graphics/door_anims/poke_center.png / poke_mart.png.
  * Centre arrow sign: two dedicated tiles animated by TilesetAnim_General (frames in
    data/tilesets/primary/general/anim/centre_arrow/).
  * Layouts: old 4x4 boxes replaced, warps moved (Mart gains a right-hand door warp), NPCs on new
    cells moved, a Mart signpost object (OBJ_EVENT_GFX_MART_SIGN) placed where plan.json says.
"""
import json
import os
import re
import struct
import sys
from collections import defaultdict

import numpy as np
from PIL import Image

from common import (HERE, ROOT, GEN, layouts, maps, read_grid, write_grid, behaviours, tset, attr_of,
                    meta_of, OLD_CENTRE_DOOR, OLD_MART_DOOR)

NORMAL, COVERED = 0, 1
ANIMATED = set(range(432, 462)) | set(range(464, 474)) | set(range(480, 490)) | set(range(496, 502)) | set(range(508, 512))
OLD_IDS = {0x048 + r * 8 + c for r in range(4) for c in range(4)} | {0x028 + r * 8 + c for r in range(4) for c in range(4)} | {0x02E}
GRASS_MT = 0x001
SIZE = {"centre": (5, 5), "mart": (4, 5)}
PAL = {"centre": 1, "mart": 0}
DOORS = {"centre": [(2, 4)], "mart": [(1, 4), (2, 4)]}
ARROW_TILES = [(7, 8), (8, 8)]            # Centre art, 8x8 tile coords holding the arrow panel
ARROW_WINDOW = (60, 65, 71, 71)           # x0, y0, x1, y1 (exclusive) of the scrolling area
ARROW_FRAMES = 16
DOOR_BITS = 0x0400                        # collision 1, elevation 0: vanilla bump-to-enter door
MB = behaviours()


def read_pal(i):
    lines = open(os.path.join(GEN, "palettes", f"{i:02d}.pal")).read().split("\n")[3:19]
    return [tuple(int(v) for v in l.split()) for l in lines]


def to_indices(rgba, pal):
    idx = {}
    for i, c in enumerate(pal):
        if i and c not in idx:
            idx[c] = i
    h, w = rgba.shape[:2]
    out = np.zeros((h, w), np.uint8)
    for y in range(h):
        for x in range(w):
            if rgba[y, x, 3]:
                out[y, x] = idx[tuple(int(v) for v in rgba[y, x, :3])]
    return out


def flips(t):
    return ((t, 0, 0), (t[:, ::-1], 1, 0), (t[::-1], 0, 1), (t[::-1, ::-1], 1, 1))


class Bank:
    def __init__(self, free, existing):
        self.free = list(free)
        self.lookup = {}                    # bytes -> (idx, h, v)
        self.new = {}                       # idx -> 8x8 array
        self.short = 0
        self.reused = 0
        for idx, t in existing.items():
            self.lookup.setdefault(t.tobytes(), (idx, 0, 0))

    def add(self, t):
        for v, hf, vf in flips(t):
            k = v.tobytes()
            if k in self.lookup:
                idx, h0, v0 = self.lookup[k]
                if idx not in self.new:
                    self.reused += 1
                return idx, hf ^ h0, vf ^ v0
        if not self.free:
            self.short += 1
            return 0, 0, 0
        idx = self.free.pop(0)
        self.lookup[t.tobytes()] = (idx, 0, 0)
        self.new[idx] = t
        return idx, 0, 0

    def take(self, t, idx):
        self.free.remove(idx)
        self.new[idx] = t


def main(write):
    plan = json.load(open(os.path.join(HERE, "plan.json")))
    if any(p["new"] is None for p in plan):
        raise SystemExit("plan.json has buildings without a placement")
    L, M = layouts(), maps()
    gen = tset("gTileset_General")
    pals = {0: read_pal(0), 1: read_pal(1)}
    art = {k: np.array(Image.open(os.path.join(HERE, "art", f"{k}.png")).convert("RGBA")) for k in SIZE}
    ind = {k: to_indices(art[k], pals[PAL[k]]) for k in SIZE}
    alpha = {k: art[k][:, :, 3] > 0 for k in SIZE}

    live = {}
    for mid, (p, js) in M.items():
        live.setdefault(js["layout"], []).append((mid, p, js))
    grids = {lid: read_grid(L[lid]) for lid in live if L[lid].get("primary_tileset") == "gTileset_General"}
    grids = {k: g for k, g in grids.items() if g is not None}

    # ---------------------------------------------------------------- what dies
    old_cells = defaultdict(set)
    for p in plan:
        bx, by, bw, bh = p["box"]
        old_cells[p["layout"]] |= {(bx + i, by + j) for i in range(bw) for j in range(bh)}
    sec_used_in_box, sec_used_out = defaultdict(set), defaultdict(set)
    prim_used = set()
    for lid, g in grids.items():
        s = L[lid]["secondary_tileset"]
        for y, row in enumerate(g):
            for x, v in enumerate(row):
                m = v & 0x3FF
                inside = (x, y) in old_cells[lid]
                if m >= 0x200:
                    (sec_used_in_box if inside else sec_used_out)[s].add(m)
                elif not inside:
                    prim_used.add(m)
        for v in struct.unpack("<4H", open(os.path.join(ROOT, L[lid]["border_filepath"]), "rb").read()[:8]):
            (prim_used if (v & 0x3FF) < 0x200 else sec_used_out[s]).add(v & 0x3FF)
    dying_sec = {s: sorted(ids - sec_used_out[s]) for s, ids in sec_used_in_box.items()}
    labels = open(os.path.join(ROOT, "include", "constants", "metatile_labels.h")).read()
    labelled = {int(v, 16) for v in re.findall(r"#define METATILE_General_\w+\s+(0x[0-9A-Fa-f]+)", labels)}
    labelled -= {OLD_CENTRE_DOOR, OLD_MART_DOOR}
    keep_prim = (prim_used | labelled) - OLD_IDS
    prim_pool = sorted(m for m in range(1, 0x200) if m not in keep_prim)

    # ---------------------------------------------------------------- free tiles
    strict_ref, map_ref = set(), set()
    for m in keep_prim:
        strict_ref |= {e & 0x3FF for e in gen.meta[m]}
    map_ref |= strict_ref
    secs = {L[lid]["secondary_tileset"] for lid in grids}
    used_sec_ids = defaultdict(set)
    for lid, g in grids.items():
        for row in g:
            for v in row:
                if (v & 0x3FF) >= 0x200:
                    used_sec_ids[L[lid]["secondary_tileset"]].add(v & 0x3FF)
    for s in secs:
        st = tset(s)
        dead = set(dying_sec.get(s, []))
        for i, m in enumerate(st.meta):
            if 0x200 + i in dead:
                continue
            refs = {e & 0x3FF for e in m if (e & 0x3FF) < 0x200}
            strict_ref |= refs
            if 0x200 + i in used_sec_ids[s] - dead:
                map_ref |= refs
    strict_free = [t for t in range(1, 512) if t not in strict_ref and t not in ANIMATED]
    lax_free = [t for t in range(1, 512) if t not in map_ref and t not in ANIMATED and t not in strict_free]
    free = strict_free + lax_free

    tiles_im = Image.open(os.path.join(GEN, "tiles.png"))
    assert tiles_im.mode == "P"
    tpx = np.array(tiles_im)
    tw = tiles_im.width // 8

    def tile_at(i):
        r, c = divmod(i, tw)
        return tpx[r * 8:(r + 1) * 8, c * 8:(c + 1) * 8].copy()

    existing = {t: tile_at(t) for t in sorted(map_ref) if t < 512 and t not in ANIMATED and t not in free
                and (t // tw) * 8 < tpx.shape[0]}
    bank = Bank(free, existing)

    # arrow: two dedicated, adjacent slots
    pair = next(t for t in strict_free if t + 1 in strict_free)
    arrow_slots = [pair, pair + 1]
    for (tx, ty), slot in zip(ARROW_TILES, arrow_slots):
        bank.take(ind["centre"][ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8].copy(), slot)
    arrow_cells = {}                       # (tx, ty) -> slot

    for (tx, ty), slot in zip(ARROW_TILES, arrow_slots):
        arrow_cells[(tx, ty)] = slot

    def entry_for(kind, x0, y0):
        t = ind[kind][y0:y0 + 8, x0:x0 + 8]
        if kind == "centre" and (x0 // 8, y0 // 8) in arrow_cells:
            return arrow_cells[(x0 // 8, y0 // 8)] | PAL[kind] << 12
        idx, hf, vf = bank.add(t.copy())
        return idx | hf << 10 | vf << 11 | PAL[kind] << 12

    grass = gen.meta[GRASS_MT][:4]

    def build_cell(kind, cx, cy, ground):
        """-> (8 entries, attribute)."""
        quads, opaque, empty = [], True, []
        for q in range(4):
            x0, y0 = cx * 16 + (q & 1) * 8, cy * 16 + (q >> 1) * 8
            a = alpha[kind][y0:y0 + 8, x0:x0 + 8]
            opaque &= bool(a.all())
            empty.append(not a.any())
            quads.append(None if not a.any() else entry_for(kind, x0, y0))
        art_entries = [q or 0 for q in quads]
        if cy == 0:
            bottom, top, layer = list(ground), art_entries, NORMAL           # roof back edge over sprites
        elif opaque:
            bottom, top, layer = art_entries, [0] * 4, COVERED
        else:
            bottom, top, layer = list(ground), art_entries, COVERED
        beh = MB["MB_ANIMATED_DOOR"] if (cx, cy) in DOORS[kind] else MB["MB_NORMAL"]
        if (cx, cy) in DOORS[kind] or (cx, cy + 1) in DOORS[kind]:
            assert opaque, (kind, cx, cy, "door cells must be opaque")
        return tuple(bottom + top), beh | layer << 12, opaque

    canonical = {}
    for kind, (w, h) in SIZE.items():
        for cy in range(h):
            for cx in range(w):
                canonical[(kind, cx, cy)] = build_cell(kind, cx, cy, grass)

    # ---------------------------------------------------------------- per-town plan
    def ground_of(lid, x, y):
        """bottom layer of a walkable, plain cell, or None"""
        g = grids[lid]
        if not (0 <= y < len(g) and 0 <= x < len(g[0])):
            return None
        v = g[y][x]
        if (v >> 10) & 3:
            return None
        e = L[lid]
        if (attr_of(e, v & 0x3FF) & 0xFF) not in (MB["MB_NORMAL"], MB["MB_TALL_GRASS"], MB["MB_SAND"]):
            return None
        return tuple(meta_of(e, v & 0x3FF)[:4])

    new_cells = defaultdict(set)
    for p in plan:
        nx, ny, w, h = p["new"]
        new_cells[p["layout"]] |= {(nx + i, ny + j) for i in range(w) for j in range(h)}

    prim_variants, sec_variants = {}, defaultdict(dict)   # content -> metatile id
    assignments = []                                      # (plan entry, {(cx, cy): content})
    for p in plan:
        lid, kind = p["layout"], p["kind"]
        nx, ny, w, h = p["new"]
        cells = {}
        for cy in range(h):
            for cx in range(w):
                ent, at, opaque = canonical[(kind, cx, cy)]
                if not opaque:
                    x, y = nx + cx, ny + cy
                    probes = []
                    if cy == 0:
                        probes.append((x, y - 1))
                    if cx == 0:
                        probes.append((x - 1, y))
                    if cx == w - 1:
                        probes.append((x + 1, y))
                    if cy == h - 1:
                        probes.append((x, y + 1))
                    probes += [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]
                    gnd = None
                    for px_, py_ in probes:
                        if (px_, py_) in new_cells[lid] or (px_, py_) in old_cells[lid]:
                            continue
                        gnd = ground_of(lid, px_, py_)
                        if gnd:
                            break
                    if gnd and gnd != tuple(grass):
                        content = build_cell(kind, cx, cy, gnd)
                        ent, at = content[0], content[1]
                cells[(cx, cy)] = (ent, at)
        assignments.append((p, cells))

    # ---------------------------------------------------------------- metatile ids
    ids = {}
    pool = list(prim_pool)

    def take_prim():
        if not pool:
            raise SystemExit("out of primary metatile slots")
        return pool.pop(0)

    for kind, (w, h) in SIZE.items():
        for cy in range(h):
            for cx in range(w):
                ids[(kind, cx, cy)] = take_prim()
    canon_content = {ids[k]: (v[0], v[1]) for k, v in canonical.items()}
    content_to_prim = {(v[0], v[1]): ids[k] for k, v in canonical.items()}
    sec_pool = {s: list(v) for s, v in dying_sec.items()}
    placed = []                                            # (p, {(cx, cy): metatile id})
    for p, cells in assignments:
        s = L[p["layout"]]["secondary_tileset"]
        out = {}
        for (cx, cy), content in cells.items():
            if content in content_to_prim:
                out[(cx, cy)] = content_to_prim[content]
                continue
            if all((e & 0x3FF) < 0x200 for e in content[0]):
                mid = take_prim()
                content_to_prim[content] = mid
                prim_variants[content] = mid
                out[(cx, cy)] = mid
            else:
                if content not in sec_variants[s]:
                    st = tset(s)
                    if sec_pool.get(s):
                        mid = sec_pool[s].pop(0)
                    else:
                        mid = 0x200 + len(st.meta)
                        st.meta.append([0] * 8)
                        st.attr.append(0)
                    sec_variants[s][content] = mid
                out[(cx, cy)] = sec_variants[s][content]
        placed.append((p, out))

    # ---------------------------------------------------------------- report
    print(f"buildings: {sum(p['kind'] == 'centre' for p in plan)} Centres, {sum(p['kind'] == 'mart' for p in plan)} Marts")
    print(f"tiles: {len(strict_free)} free + {len(lax_free)} only used by unplaced metatiles; "
          f"new art used {len(bank.new)}, reused {bank.reused} existing tile patterns; {len(bank.free)} left")
    lax_used = sorted(t for t in bank.new if t in lax_free)
    print(f"  slots taken from unplaced secondary metatiles: {lax_used}")
    print(f"metatiles: {len(ids)} canonical, "
          f"{len(prim_variants)} primary variants, " + ", ".join(f"{s}: {len(v)}" for s, v in sec_variants.items()))
    print(f"primary metatile slots left: {len(pool)}")
    print(f"arrow tiles: {arrow_slots}")
    print("Centre door", hex(ids[('centre', 2, 4)]), "Mart doors", hex(ids[('mart', 1, 4)]), hex(ids[('mart', 2, 4)]))
    if bank.short:
        raise SystemExit(f"NOT ENOUGH TILE SPACE: {bank.short} short")
    if not write:
        print("dry run; pass --write")
        return

    # ---------------------------------------------------------------- write tilesets
    for idx, t in bank.new.items():
        r, c = divmod(idx, tw)
        tpx[r * 8:(r + 1) * 8, c * 8:(c + 1) * 8] = t
    out = Image.fromarray(tpx, "P")
    out.putpalette(tiles_im.getpalette())
    out.save(os.path.join(GEN, "tiles.png"), bits=4, optimize=False)
    for m in prim_pool:
        gen.meta[m], gen.attr[m] = [0] * 8, 0
    for mid, (ent, at) in canon_content.items():
        gen.meta[mid], gen.attr[mid] = list(ent), at
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
    for s in set(sec_variants) | set(sec_pool):
        tset(s).save()

    # ---------------------------------------------------------------- write maps
    map_edits = defaultdict(list)
    for p, out_ids in placed:
        lid, kind = p["layout"], p["kind"]
        g = grids[lid]
        nx, ny, w, h = p["new"]
        bx, by, bw, bh = p["box"]
        H, W = len(g), len(g[0])
        front = g[min(ny + h, H - 1)][nx + DOORS[kind][0][0]]
        elev = (front >> 12) & 0xF
        if elev in (0, 15):
            elev = 3
        # leftovers of the old box become the ground in front of the old building
        fill = g[min(by + bh, H - 1)][bx + 1]
        for i in range(bw):
            for j in range(bh):
                c = (bx + i, by + j)
                if c not in new_cells[lid]:
                    g[c[1]][c[0]] = fill
        for (cx, cy), mid in out_ids.items():
            x, y = nx + cx, ny + cy
            if (cx, cy) in DOORS[kind]:
                bits = DOOR_BITS
            elif cy == 0:
                above = g[y - 1][x] if y > 0 else 0x0400
                behind_walkable = y > 0 and not ((above >> 10) & 3) and (x, y - 1) not in new_cells[lid]
                bits = (above & 0xF000) if behind_walkable else (elev << 12) | 0x0400
            else:
                bits = (elev << 12) | 0x0400
            g[y][x] = mid | bits
        map_edits[lid].append((p, elev))

    sign_ids = []
    for lid, items in map_edits.items():
        write_grid(L[lid], grids[lid])
        for mid, path, js in live[lid]:
            changed = False
            warps = js.get("warp_events") or []
            for p, elev in items:
                nx, ny, w, h = p["new"]
                ox, oy = p["door"]
                dx, dy = DOORS[p["kind"]][0]
                for wi, wv in enumerate(list(warps)):
                    if (wv["x"], wv["y"]) == (ox, oy):
                        wv["x"], wv["y"] = nx + dx, ny + dy
                        changed = True
                        if p["kind"] == "mart":
                            rx, ry = nx + DOORS["mart"][1][0], ny + DOORS["mart"][1][1]
                            if not any((o["x"], o["y"]) == (rx, ry) for o in warps):
                                warps.append(dict(wv, x=rx, y=ry))
                # NPCs on new cells: nearest free walkable cell
                taken = {(o["x"], o["y"]) for k in ("object_events", "warp_events", "bg_events", "coord_events")
                         for o in js.get(k) or []}
                for o in js.get("object_events") or []:
                    if (o["x"], o["y"]) in new_cells[lid] and tuple((o["x"], o["y"])) in {tuple(c) for c in p.get("move", [])}:
                        best = None
                        for r in range(1, 6):
                            for ddx in range(-r, r + 1):
                                for ddy in range(-r, r + 1):
                                    c = (o["x"] + ddx, o["y"] + ddy)
                                    if c in taken or c in new_cells[lid]:
                                        continue
                                    if ground_of(lid, *c) is None:
                                        continue
                                    best = c
                                    break
                                if best:
                                    break
                            if best:
                                break
                        print(f"  {mid}: NPC {o.get('script')} ({o['x']},{o['y']}) -> {best}")
                        o["x"], o["y"] = best
                        taken.add(best)
                        changed = True
                if p["kind"] == "mart" and p.get("sign"):
                    sx, sy = p["sign"]
                    objs = js.setdefault("object_events", [])
                    if not any(o.get("graphics_id") == "OBJ_EVENT_GFX_MART_SIGN" and (o["x"], o["y"]) == (sx, sy) for o in objs):
                        objs.append({"graphics_id": "OBJ_EVENT_GFX_MART_SIGN", "x": sx, "y": sy, "elevation": elev,
                                     "movement_type": "MOVEMENT_TYPE_NONE", "movement_range_x": 0,
                                     "movement_range_y": 0, "trainer_type": "TRAINER_TYPE_NONE",
                                     "trainer_sight_or_berry_tree_id": "0", "script": "0x0", "flag": "0"})
                        changed = True
                        sign_ids.append(mid)
            if changed:
                with open(path, "w") as f:
                    json.dump(js, f, indent=2, ensure_ascii=False)
                    f.write("\n")

    # ---------------------------------------------------------------- labels
    txt = open(os.path.join(ROOT, "include", "constants", "metatile_labels.h")).read()
    txt = re.sub(r"#define METATILE_General_Door_PokeCenter\s+0x[0-9A-Fa-f]+",
                 f"#define METATILE_General_Door_PokeCenter       0x{ids[('centre', 2, 4)]:03X}", txt)
    txt = re.sub(r"#define METATILE_General_Door_PokeMart\s+0x[0-9A-Fa-f]+",
                 f"#define METATILE_General_Door_PokeMart         0x{ids[('mart', 1, 4)]:03X}", txt)
    right = f"#define METATILE_General_Door_PokeMart_Right   0x{ids[('mart', 2, 4)]:03X}"
    if "METATILE_General_Door_PokeMart_Right" in txt:
        txt = re.sub(r"#define METATILE_General_Door_PokeMart_Right\s+0x[0-9A-Fa-f]+", right, txt)
    else:
        txt = re.sub(r"(#define METATILE_General_Door_PokeMart\s+0x[0-9A-Fa-f]+\n)", r"\1" + right + "\n", txt)
    open(os.path.join(ROOT, "include", "constants", "metatile_labels.h"), "w").write(txt)

    door_frames(ind, pals)
    arrow_frames(ind, pals, arrow_slots)
    json.dump(dict(arrow_slots=arrow_slots, ids={f"{k[0]}_{k[1]}_{k[2]}": v for k, v in ids.items()}),
              open(os.path.join(HERE, "installed.json"), "w"), indent=1)
    print("signs placed in:", ", ".join(sign_ids))
    print("written")


def save_indexed(arr, pal, path):
    im = Image.fromarray(arr.astype(np.uint8), "P")
    im.putpalette([v for c in pal for v in c])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path, bits=4, optimize=False)


def open_door(cut, gap_rows, centre_x, half, dark, floor):
    """Slide the door glass apart: pixels within `half` of centre_x in gap_rows become the dark
    interior (the bottom two rows the floor)."""
    out = cut.copy()
    y0, y1 = gap_rows
    for y in range(y0, y1):
        for x in range(out.shape[1]):
            if centre_x - half <= x < centre_x + half:
                out[y, x] = floor if y >= y1 - 2 else dark
    return out


def door_glass(ind, x0, x1, y0, y1, glass):
    """-> bounds of the door panel: the glass, extended down to the dark sill (outline index 7)."""
    sub = ind[y0:y1, x0:x1]
    ys, xs = np.where(np.isin(sub, glass))
    gy0, gy1, gx0, gx1 = ys.min() + y0, ys.max() + y0 + 1, xs.min() + x0, xs.max() + x0 + 1
    cx = (gx0 + gx1) // 2
    while gy1 < y1 and ind[gy1, cx] != 7:
        gy1 += 1
    return gy0, gy1, gx0, gx1


def door_frames(ind, pals):
    # Centre: glass is palette-1 blues (9, 10) in the door cell (column 2, row 4)
    c = ind["centre"]
    gy0, gy1, gx0, gx1 = door_glass(c, 32, 48, 64, 80, (9, 10))
    frames = []
    for k, half in enumerate((2, 4, 7)):
        f = open_door(c[48:80, 32:48], (gy0 - 48, gy1 - 48), (gx0 + gx1) // 2 - 32, min(half, (gx1 - gx0) // 2), 8, 7)
        frames.append(f)
    save_indexed(np.concatenate(frames, axis=0), pals[1], os.path.join(ROOT, "graphics", "door_anims", "poke_center.png"))
    # Mart: 2x2 door, columns 1-2, rows 3-4; glass is palette-0 blues
    m = ind["mart"]
    blues = [i for i, col in enumerate(pals[0]) if i and col[2] > col[0] + 60]
    gy0, gy1, gx0, gx1 = door_glass(m, 16, 48, 64, 80, blues)
    frames = []
    for half in (3, 6, 9):
        f = open_door(m[48:80, 16:48], (gy0 - 48, gy1 - 48), (gx0 + gx1) // 2 - 16, min(half, (gx1 - gx0) // 2), 7, 6)
        frames.append(f)
    save_indexed(np.concatenate(frames, axis=0), pals[0], os.path.join(ROOT, "graphics", "door_anims", "poke_mart.png"))


def arrow_frames(ind, pals, slots):
    c = ind["centre"]
    x0, y0, x1, y1 = ARROW_WINDOW
    win = c[y0:y1, x0:x1]
    bg = 7
    strip = np.full((y1 - y0, ARROW_FRAMES), bg, np.uint8)
    strip[:, :x1 - x0] = win
    d = os.path.join(GEN, "anim", "centre_arrow")
    for k in range(ARROW_FRAMES):
        f = c[64:72, 56:72].copy()
        rolled = np.roll(strip, -k, axis=1)[:, :x1 - x0]
        f[y0 - 64:y1 - 64, x0 - 56:x1 - 56] = rolled
        save_indexed(f, pals[1], os.path.join(d, f"{k}.png"))


if __name__ == "__main__":
    if "--doors-only" in sys.argv:
        pals = {0: read_pal(0), 1: read_pal(1)}
        art = {k: np.array(Image.open(os.path.join(HERE, "art", f"{k}.png")).convert("RGBA")) for k in SIZE}
        door_frames({k: to_indices(art[k], pals[PAL[k]]) for k in SIZE}, pals)
    else:
        main("--write" in sys.argv)
