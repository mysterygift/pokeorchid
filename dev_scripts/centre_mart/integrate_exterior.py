#!/usr/bin/env python3
"""Replace the vanilla Pokemon Centre / Pokemart exteriors with the new ones in every town.

Both buildings keep the vanilla 4x4 footprint, so no map is re-laid-out. What changes:

  * gTileset_General (primary): new 8x8 tiles go into tile slots that are freed by retiring the
    vanilla building art and metatiles no General map uses. The 32 building metatiles are
    rewritten (same ids, plus one spare id for the Mart's bottom-left, which used to be shared
    with the Centre).
  * Town secondary tilesets: where a town draws the building over non-grass ground it has its own
    copies of some building metatiles. Those are rebuilt with the town's ground kept underneath.
  * Layouts: the 16 cells of every building are re-pointed. The Centre's bottom row becomes a
    walkable covered walkway and its door moves up one tile, so the door warp moves up too.
  * The Mart door animation frames (graphics/door_anims/poke_mart.png).

Run once on a tree that still has the vanilla buildings:

    python integrate_exterior.py            # dry run: report only
    python integrate_exterior.py --write    # apply
"""
import json
import os
import re
import struct
import sys
from collections import Counter, defaultdict

from PIL import Image

import exterior4
import inventory
import vanilla
from vanilla import ROOT

NORMAL, COVERED = 0, 1
GEN = os.path.join(ROOT, "data", "tilesets", "primary", "general")
CENTRE_IDS = [[0x048, 0x049, 0x04A, 0x04B], [0x050, 0x051, 0x052, 0x053],
              [0x058, 0x059, 0x05A, 0x05B], [0x060, 0x061, 0x062, 0x063]]
MART_SPARE = 0x02E                       # unused primary metatile: the Mart's own bottom-left
MART_IDS = [[0x028, 0x029, 0x02A, 0x02B], [0x030, 0x031, 0x032, 0x033],
            [0x038, 0x039, 0x03A, 0x03B], [MART_SPARE, 0x041, 0x042, 0x043]]
OLD_IDS = {m for rows in CENTRE_IDS + MART_IDS for m in rows}   # incl. the spare: re-runs stay idempotent
GRASS = [0x002 | 2 << 12, 0x003 | 2 << 12, 0x003 | 2 << 12, 0x002 | 2 << 12]
# tile ranges the General tileset animations overwrite every few frames (src/tileset_anims.c)
ANIMATED_TILES = set(range(432, 462)) | set(range(464, 474)) | set(range(480, 490)) | set(range(496, 502)) | set(range(508, 512))


def behaviours():
    text = open(os.path.join(ROOT, "include", "constants", "metatile_behaviors.h")).read()
    names = re.findall(r"^\s*(MB_\w+)\s*,", text[text.index("enum"):], re.M)
    return {n: i for i, n in enumerate(names)}


def labelled_general_ids():
    text = open(os.path.join(ROOT, "include", "constants", "metatile_labels.h")).read()
    return {int(v, 16) for v in re.findall(r"#define METATILE_General_\w+\s+(0x[0-9A-Fa-f]+)", text)}


class Set:
    """A tileset's metatiles + attributes, editable."""

    def __init__(self, d):
        self.dir = d
        raw = open(os.path.join(d, "metatiles.bin"), "rb").read()
        self.meta = [list(struct.unpack_from("<8H", raw, i * 16)) for i in range(len(raw) // 16)]
        raw = open(os.path.join(d, "metatile_attributes.bin"), "rb").read()
        self.attr = list(struct.unpack(f"<{len(raw) // 2}H", raw))
        self.dirty = False

    def save(self):
        with open(os.path.join(self.dir, "metatiles.bin"), "wb") as f:
            for m in self.meta:
                f.write(struct.pack("<8H", *m))
        with open(os.path.join(self.dir, "metatile_attributes.bin"), "wb") as f:
            f.write(struct.pack(f"<{len(self.attr)}H", *self.attr))


def flips(tile):
    h = tuple(tuple(reversed(r)) for r in tile)
    v = tuple(reversed(tile))
    return ((tile, 0, 0), (h, 1, 0), (v, 0, 1), (tuple(reversed(h)), 1, 1))


class Bank:
    """New 8x8 tiles, deduplicated with flips, each given a free primary tile slot."""

    def __init__(self, free):
        self.free, self.lookup, self.tiles, self.short = list(free), {}, {}, 0

    def add(self, tile):
        for variant, hf, vf in flips(tile):
            if variant in self.lookup:
                idx, h0, v0 = self.lookup[variant]
                return idx, hf ^ h0, vf ^ v0
        if not self.free:
            self.short += 1
            idx = 10000 + self.short
        else:
            idx = self.free.pop(0)
        self.lookup[tile] = (idx, 0, 0)
        self.tiles[idx] = tile
        return idx, 0, 0


def quadrant(art, cx, cy, q, pals):
    """-> None (empty) or (entry-without-tile, tile, opaque). pals: [(slot, colour list)]."""
    x0, y0 = cx * 16 + (q & 1) * 8, cy * 16 + (q >> 1) * 8
    px = [[art.px[y0 + y][x0 + x] for x in range(8)] for y in range(8)]
    cols = {c for r in px for c in r}
    if cols == {None}:
        return None
    opaque = None not in cols
    cols.discard(None)
    for slot, pal in pals:
        if cols <= set(pal):
            idx = {c: i for i, c in enumerate(pal) if c is not None}   # duplicates: highest index
            return slot, tuple(tuple(0 if c is None else idx[c] for c in r) for r in px), opaque
    raise ValueError(f"cell ({cx},{cy}) quadrant {q}: no palette holds {sorted(cols)}")


def main(write):
    MB = behaviours()
    L, M = inventory.layouts(), inventory.maps()
    gen = Set(GEN)
    sec_sets = {}

    def sec(sym):
        if sym not in sec_sets:
            sec_sets[sym] = Set(vanilla.tileset_dir(sym))
        return sec_sets[sym]

    # ---- every layout paired with General, and metatile use
    grids, use_primary, use_sec = {}, Counter(), defaultdict(Counter)
    for lid, e in L.items():
        if e["primary_tileset"] != "gTileset_General" or not os.path.exists(os.path.join(ROOT, e["blockdata_filepath"])):
            continue
        if inventory.blocks(e) is None:
            continue
        grids[lid] = inventory.blocks(e)
        border = struct.unpack("<4H", open(os.path.join(ROOT, e["border_filepath"]), "rb").read()[:8])
        for v in [c for row in grids[lid] for c in row] + list(border):
            m = v & 0x3FF
            (use_primary if m < 0x200 else use_sec[e["secondary_tileset"]])[m] += 1

    # ---- building occurrences
    occ = []
    for lid, g in grids.items():
        for y, row in enumerate(g):
            for x, v in enumerate(row):
                if (v & 0x3FF) in (0x061, 0x041):
                    occ.append(dict(layout=lid, x=x, y=y, bx=x - 1, by=y - 3,
                                    kind="centre" if (v & 0x3FF) == 0x061 else "mart",
                                    secondary=L[lid]["secondary_tileset"]))
    cells_of = defaultdict(set)                       # layout -> {(x, y)} covered by buildings
    for o in occ:
        for cy in range(4):
            for cx in range(4):
                cells_of[o["layout"]].add((o["bx"] + cx, o["by"] + cy))
    stray = Counter()
    for lid, g in grids.items():
        for y, row in enumerate(g):
            for x, v in enumerate(row):
                if (v & 0x3FF) in OLD_IDS and (x, y) not in cells_of[lid]:
                    stray[(lid, v & 0x3FF)] += 1
    if stray:
        print("building metatiles outside known buildings:", dict(stray))

    # ---- old town variants that die with this change
    old_variants = defaultdict(set)
    for o in occ:
        g = grids[o["layout"]]
        for cy in range(4):
            for cx in range(4):
                m = g[o["by"] + cy][o["bx"] + cx] & 0x3FF
                if m >= 0x200:
                    old_variants[o["secondary"]].add(m)
    pool = {}
    for sym, ids in old_variants.items():
        outside = Counter()
        for lid, g in grids.items():
            if L[lid]["secondary_tileset"] != sym:
                continue
            for y, row in enumerate(g):
                for x, v in enumerate(row):
                    if (v & 0x3FF) in ids and (x, y) not in cells_of[lid]:
                        outside[v & 0x3FF] += 1
        pool[sym] = sorted(i for i in ids if not outside[i])

    # ---- free primary tiles
    labelled = labelled_general_ids()
    retired = {m for m in range(0x200) if m not in use_primary and m not in labelled} | OLD_IDS
    old_build_tiles = set()
    for m in OLD_IDS:
        for k, e in enumerate(gen.meta[m]):
            if (e >> 12) in (0, 1) and (e & 0x3FF):
                old_build_tiles.add(e & 0x3FF)
    referenced = set()
    for m, e in enumerate(gen.meta):
        if m not in retired:
            referenced |= {x & 0x3FF for x in e}
    general_secs = {L[lid]["secondary_tileset"] for lid in grids}
    for sym in general_secs:
        try:
            s = sec(sym)
        except FileNotFoundError:
            continue
        dead = set(pool.get(sym, []))
        for i, e in enumerate(s.meta):
            if 0x200 + i not in dead:
                referenced |= {x & 0x3FF for x in e if (x & 0x3FF) < 512}
    free = [t for t in range(1, 512) if t not in referenced and t not in ANIMATED_TILES]
    bank = Bank(free)

    # ---- art -> per-cell metatiles
    art = {"centre": exterior4.centre(), "mart": exterior4.mart()}
    pals = {"centre": [(1, exterior4.PAL1)], "mart": [(0, exterior4.PAL0), (1, exterior4.PAL1)]}

    def entry(t):
        slot, tile, _ = t
        idx, hf, vf = bank.add(tile)
        return idx | hf << 10 | vf << 11 | slot << 12

    def is_ground(e):
        return (e & 0x3FF) != 0 and (e & 0x3FF) not in old_build_tiles

    def build_cell(kind, cx, cy, old_bottom, neighbour_bottom):
        """-> (8 entries, attribute). old_bottom / neighbour_bottom: bottom layers to take ground from."""
        a = art[kind]
        two_layer = kind == "centre" and cy >= 2
        bottom, top = [0] * 4, [0] * 4
        for q in range(4):
            u = quadrant(a["under"], cx, cy, q, pals[kind])
            ov = quadrant(a["over"], cx, cy, q, pals[kind])
            if two_layer:
                assert u and u[2], (kind, cx, cy, q)
                bottom[q] = entry(u)
                top[q] = entry(ov) if ov else 0
                continue
            if u and u[2]:
                bottom[q] = entry(u)
                continue
            ground = None
            for cand in [old_bottom[q]] + [old_bottom[k] for k in range(4)] + \
                        ([neighbour_bottom[q]] if neighbour_bottom else []):
                if is_ground(cand):
                    ground = cand
                    break
            bottom[q] = ground if ground is not None else GRASS[q]
            top[q] = entry(u) if u else 0
        beh = 0
        if kind == "centre" and (cx, cy) == (1, 2):
            beh = MB["MB_NON_ANIMATED_DOOR"]
        if kind == "mart" and (cx, cy) == (1, 3):
            beh = MB["MB_ANIMATED_DOOR"]
        layer = COVERED if (kind == "mart" and cy == 3) else NORMAL
        return tuple(bottom + top), beh | layer << 12

    ids = {"centre": CENTRE_IDS, "mart": MART_IDS}
    canonical = {}
    for kind in ("centre", "mart"):
        for cy in range(4):
            for cx in range(4):
                canonical[(kind, cx, cy)] = build_cell(kind, cx, cy, GRASS, None)

    # ---- per-town cells
    def bottom_of(lid, x, y):
        g = grids[lid]
        if not (0 <= y < len(g) and 0 <= x < len(g[0])):
            return None
        m = g[y][x] & 0x3FF
        ts = gen if m < 0x200 else sec(L[lid]["secondary_tileset"])
        i = m if m < 0x200 else m - 0x200
        return ts.meta[i][:4] if i < len(ts.meta) else None

    plans, variant_need = [], defaultdict(dict)        # sym -> {content: None}
    for o in occ:
        lid, kind = o["layout"], o["kind"]
        cells = {}
        for cy in range(4):
            for cx in range(4):
                x, y = o["bx"] + cx, o["by"] + cy
                nb = bottom_of(lid, x - 1, y) if cx == 0 else bottom_of(lid, x + 1, y) if cx == 3 else None
                content = build_cell(kind, cx, cy, bottom_of(lid, x, y), nb)
                cells[(cx, cy)] = content
                if content != canonical[(kind, cx, cy)]:
                    variant_need[o["secondary"]][content] = None
        plans.append((o, cells))

    # ---- write metatiles
    for m in retired - OLD_IDS:
        gen.meta[m], gen.attr[m] = [0] * 8, 0
    for (kind, cx, cy), (ent, at) in canonical.items():
        gen.meta[ids[kind][cy][cx]], gen.attr[ids[kind][cy][cx]] = list(ent), at
    report = []
    for sym, need in variant_need.items():
        s = sec(sym)
        slots = list(pool.get(sym, []))
        for content in need:
            if slots:
                mid = slots.pop(0)
            else:
                mid = 0x200 + len(s.meta)
                if mid >= 0x400:
                    raise RuntimeError(f"{sym}: no metatile slots left")
                s.meta.append([0] * 8), s.attr.append(0)
            s.meta[mid - 0x200], s.attr[mid - 0x200] = list(content[0]), content[1]
            need[content] = mid
        for mid in slots:                              # dead variants nobody needs any more
            s.meta[mid - 0x200], s.attr[mid - 0x200] = [0] * 8, 0
        s.dirty = True
        report.append(f"{sym}: {len(need)} town variants ({len(s.meta)} metatiles)")

    # ---- layouts + warps
    changed_layouts, warp_moves = set(), []
    for o, cells in plans:
        lid, kind, g = o["layout"], o["kind"], grids[o["layout"]]
        door_bits = g[o["y"]][o["x"]] & 0xFC00
        for (cx, cy), content in cells.items():
            x, y = o["bx"] + cx, o["by"] + cy
            mid = ids[kind][cy][cx] if content == canonical[(kind, cx, cy)] else variant_need[o["secondary"]][content]
            bits = g[y][x] & 0xFC00
            if kind == "centre":
                if cy == 3 or (cx, cy) == (1, 2):
                    bits = door_bits                    # walkway + door: walkable at the door's elevation
                else:
                    bits = (bits & 0xF000) | 0x0400
            g[y][x] = mid | bits
        changed_layouts.add(lid)
        if kind == "centre":
            for mid_, (path, js) in M.items():
                if js["layout"] != lid:
                    continue
                for wi, w in enumerate(js.get("warp_events") or []):
                    if (w["x"], w["y"]) == (o["x"], o["y"]):
                        warp_moves.append((path, wi, o["x"], o["y"]))

    print(f"buildings: {sum(o['kind'] == 'centre' for o in occ)} Centres, {sum(o['kind'] == 'mart' for o in occ)} Marts "
          f"in {len(changed_layouts)} layouts")
    print(f"primary tiles: {len(free)} free, {len(bank.tiles)} used by the new art, {len(bank.free)} left")
    print(f"primary metatiles retired (unused, unlabelled): {len(retired - OLD_IDS)}")
    for r in report:
        print("  " + r)
    if bank.short:
        raise SystemExit(f"NOT ENOUGH TILE SPACE: {bank.short} tiles short")
    if not write:
        print("dry run; pass --write to apply")
        return

    im = Image.open(os.path.join(GEN, "tiles.png"))
    assert im.mode == "P"
    px, tw = im.load(), im.width // 8
    for idx, tile in bank.tiles.items():
        for y in range(8):
            for x in range(8):
                px[(idx % tw) * 8 + x, (idx // tw) * 8 + y] = tile[y][x]
    im.save(os.path.join(GEN, "tiles.png"), bits=4, optimize=False)
    gen.save()
    for s in sec_sets.values():
        if s.dirty:
            s.save()
    for lid in changed_layouts:
        e, g = L[lid], grids[lid]
        with open(os.path.join(ROOT, e["blockdata_filepath"]), "wb") as f:
            f.write(struct.pack(f"<{e['width'] * e['height']}H", *[c for row in g for c in row]))
    for path, warp, x, y in warp_moves:
        js = json.load(open(path))
        w = js["warp_events"][warp]
        assert (w["x"], w["y"]) == (x, y), (path, w)
        w["y"] = y - 1
        with open(path, "w") as f:
            json.dump(js, f, indent=2, ensure_ascii=False)
            f.write("\n")
    door_frames(art["mart"])
    print("written")


def door_frames(mart):
    """graphics/door_anims/poke_mart.png: three 16x32 frames (the tile above the door + the door),
    sliding open. All eight tiles of a frame use tileset palette 0."""
    pal = exterior4.PAL0
    idx = {c: i for i, c in reversed(list(enumerate(pal))) if c is not None}
    a = mart["under"]
    dx = exterior4.M_DOOR_COL * 16
    dark, floor = exterior4.GREYS["K"], exterior4.GREYS["k"]
    im = Image.new("P", (16, 96), 0)
    flat = [(0, 0, 0)] + [c for c in pal[1:]]
    im.putpalette([v for c in flat for v in c])
    px = im.load()
    for f, half in enumerate((2, 4, 7)):                 # half-width of the opening
        for y in range(32):
            for x in range(16):
                c = a.px[32 + y][dx + x]
                if y >= 17 and y <= 30 and 8 - half <= x <= 7 + half and 1 <= x <= 14:
                    c = floor if y >= 28 else dark
                px[x, f * 32 + y] = idx[c]
    im.save(os.path.join(ROOT, "graphics", "door_anims", "poke_mart.png"), bits=4, optimize=False)


if __name__ == "__main__":
    main("--write" in sys.argv)
