#!/usr/bin/env python3
"""Lit windows at night: give window glass its own light-blended palette colours (DNS .pla files).

The expansion's day/night system (OW_ENABLE_DNS) darkens outdoor maps at night, except palette colours listed
in the palette's .pla file: those "lights" blend toward the palette's colour 0 (when 0 is listed) instead. A
light index may only be used by things that should glow, so window glass has to get indices of its own:

  1. find glass pixels: small light-blue panes framed by dark pixels inside the listed window metatiles
     (houses), every glass-coloured pixel of "always" metatiles, and hand-drawn boxes on the big buildings
     ("masks": Centre, Mart, station, gym), where glass shares colours with the walls;
  2. per palette, give the glass colours light indices: unused indices first (checked across EVERY tileset
     the palette is drawn with); if there are fewer free indices than glass shades, shades are merged by
     brightness. The light index keeps its glass colour, so the day look is unchanged (bar merged shades);
  3. tiles that also appear outside windows are copied into free tile slots and only the window
     metatiles are pointed at the copies, so walls and paving never glow;
  4. write tiles.png, metatiles.bin, the palettes (colour 0 = LAMP) and their .pla.

    windows.py detect LAYOUT out.png PAIR   preview the glass found on one map (magenta)
    windows.py report PAIR                  dry run: glass per palette, free indices, tile copies
    windows.py apply PAIR                   write the changes (run once; re-running is a no-op once glass
                                            already sits on light indices)
"""
import json
import os
import struct
import sys

from PIL import Image

import dns_tool as T

ROOT = T.ROOT
LAMP = (248, 184, 56)        # colour 0 of a light palette = what its lights blend toward at night

CONFIG = {
    "tosa": {
        "primary": "gTileset_General", "secondary": "gTileset_TosaPort",
        # house windows / doors: detected as dark-framed panes
        "windows": [0x00B, 0x013, 0x021, 0x2D1, 0x2D9, 0x2DE],
        # panes with light frames: every glass-coloured pixel counts
        "always": [0x2BD, 0x2BF, 0x268],
        # (reference layout, building origin in metatiles, [(x0, y0, x1, y1, mode)]) in building pixels;
        # mode "glass" = glass-coloured pixels in the box, "light" = every pixel brighter than LIGHT_LUM
        "masks": [
            ("LAYOUT_CHANGU_CITY", (12, 17), [          # Pokémon Center (Orchid v2)
                # upper windows + arches; on the front face only the door (user, 2026-11-23)
                (8, 9, 22, 38, "glass"), (56, 9, 72, 38, "glass"), (30, 5, 37, 31, "glass"),
                (43, 5, 50, 31, "glass"), (31, 33, 49, 40, "glass"), (32, 64, 48, 79, "glass")]),
            ("LAYOUT_CHANGU_CITY", (28, 9), [           # Poké Mart (Orchid v2)
                (33, 66, 47, 79, "glass")]),       # only the door (user, 2026-11-23)
            ("LAYOUT_CHANGU_CITY", (20, 2), [           # station
                (9, 51, 24, 62, "glass"), (70, 51, 85, 62, "glass"), (33, 58, 37, 78, "glass"),
                (57, 58, 61, 78, "glass")]),
            ("LAYOUT_CHANGU_CITY", (12, 9), [           # gym
                (9, 50, 23, 56, "glass"), (26, 50, 40, 56, "glass"), (74, 50, 88, 56, "glass"),
                (48, 60, 63, 76, "glass")]),
        ],
    },
}
LIGHT_LUM = 150
MAX_PANE = 64          # px; bigger glass-coloured areas are walls / paving, not panes


def is_glass(c):
    r, g, b = c
    return b >= 150 and b - r >= 12 and b >= g and (r + g + b) >= 380


def lum(c):
    return 0.30 * c[0] + 0.59 * c[1] + 0.11 * c[2]


# ------------------------------------------------------------------ detection
def detect(ts, info, w_px, h_px, blocks, w, cfg):
    col = lambda x, y: ts.pals[info[y][x][0]][info[y][x][1]]
    mid = lambda x, y: blocks[(y // 16) * w + x // 16] & 0x3FF
    wins, always = set(cfg["windows"]), set(cfg.get("always", []))
    seen, out = set(), set()
    for y0 in range(h_px):
        for x0 in range(w_px):
            if (x0, y0) in seen or not is_glass(col(x0, y0)) or mid(x0, y0) not in wins:
                continue
            comp, stack, border = [], [(x0, y0)], []
            seen.add((x0, y0))
            while stack:
                x, y = stack.pop()
                comp.append((x, y))
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if not (0 <= nx < w_px and 0 <= ny < h_px):
                        continue
                    if is_glass(col(nx, ny)):
                        if (nx, ny) not in seen:
                            seen.add((nx, ny))
                            stack.append((nx, ny))
                    else:
                        border.append(col(nx, ny))
            if len(comp) <= MAX_PANE and border and sum(lum(c) < 125 for c in border) / len(border) >= 0.6:
                out.update(c for c in comp if mid(*c) in wins)
    for y in range(h_px):
        for x in range(w_px):
            if mid(x, y) in always and is_glass(col(x, y)):
                out.add((x, y))
    return out


def layouts_of(cfg):
    L = json.load(open(os.path.join(ROOT, "data/layouts/layouts.json")))["layouts"]
    return [l["id"] for l in L if l.get("primary_tileset") == cfg["primary"]
            and l.get("secondary_tileset") == cfg["secondary"]]


def glass_by_metatile(cfg):
    """{metatile id: set((x, y))} glass pixels in metatile space, unioned over every layout of the pair."""
    out = {}
    for lid in layouts_of(cfg):
        ts, info, blocks, w = T.load_layout(lid)
        h_px, w_px = len(info), len(info[0])
        for (x, y) in detect(ts, info, w_px, h_px, blocks, w, cfg):
            out.setdefault(blocks[(y // 16) * w + x // 16] & 0x3FF, set()).add((x % 16, y % 16))
    for lid, (ox, oy), boxes in cfg.get("masks", []):
        ts, info, blocks, w = T.load_layout(lid)
        for (x0, y0, x1, y1, mode) in boxes:
            for y in range(y0, y1 + 1):
                for x in range(x0, x1 + 1):
                    mx, my = ox * 16 + x, oy * 16 + y
                    c = ts.pals[info[my][mx][0]][info[my][mx][1]]
                    if (mode == "glass" and is_glass(c)) or (mode == "light" and lum(c) >= LIGHT_LUM):
                        out.setdefault(blocks[(my // 16) * w + mx // 16] & 0x3FF, set()).add((mx % 16, my % 16))
    return out


# ------------------------------------------------------------------ tile-space mapping
def tile_of(ts, ent, x, y):
    """Topmost (entry slot, tile, pal, tx, ty) drawing metatile pixel (x, y)."""
    q = (y // 8) * 2 + x // 8
    for layer in (1, 0):
        e = ent[layer * 4 + q]
        t, hf, vf, pal = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1, e >> 12
        tile = ts.ptiles[t] if t < 512 else (ts.stiles[t - 512] if t - 512 < len(ts.stiles) else None)
        if tile is None:
            continue
        tx, ty = (7 - x % 8) if hf else x % 8, (7 - y % 8) if vf else y % 8
        if layer == 0 or tile[ty][tx]:
            return layer * 4 + q, t, pal, tx, ty
    return None


def primary_partners(cfg):
    """Secondary tilesets drawn with this primary (their metatiles also use palettes 0-5)."""
    L = json.load(open(os.path.join(ROOT, "data/layouts/layouts.json")))["layouts"]
    return sorted({l["secondary_tileset"] for l in L if l.get("primary_tileset") == cfg["primary"]})


def index_usage(cfg, ts):
    """used[pal] = set of colour indices drawn anywhere with that palette (primary pals: across all partners)."""
    used = [set() for _ in range(16)]

    def scan(tsx, metas):
        for ent in metas:
            for layer in range(2):
                for q in range(4):
                    e = ent[layer * 4 + q]
                    t, pal = e & 0x3FF, e >> 12
                    tile = tsx.ptiles[t] if t < 512 else (tsx.stiles[t - 512] if t - 512 < len(tsx.stiles) else None)
                    if tile is None:
                        continue
                    for row in tile:
                        used[pal].update(c for c in row if c or layer == 0)
    scan(ts, ts.pmeta + ts.smeta)
    for sec in primary_partners(cfg):
        if sec == cfg["secondary"]:
            continue
        try:
            other = T.Tilesets(cfg["primary"], sec)
        except SystemExit:
            continue
        for ent in other.smeta:          # only primary palettes matter from other secondaries
            for layer in range(2):
                for q in range(4):
                    e = ent[layer * 4 + q]
                    t, pal = e & 0x3FF, e >> 12
                    if pal >= T.NUM_PALS_IN_PRIMARY:
                        continue
                    tile = other.ptiles[t] if t < 512 else (other.stiles[t - 512] if t - 512 < len(other.stiles) else None)
                    if tile is None:
                        continue
                    for row in tile:
                        used[pal].update(c for c in row if c or layer == 0)
    return used


# ------------------------------------------------------------------ plan
def plan(key):
    cfg = CONFIG[key]
    ts = T.Tilesets(cfg["primary"], cfg["secondary"])
    gm = glass_by_metatile(cfg)
    # tile pixel -> glass, per (tile, pal)
    glass_px = {}                 # (t, pal) -> set((tx, ty))
    uses = {}                     # (t, pal) -> list of (metatile, slot) that draw glass with it
    for m, pix in gm.items():
        ent = ts.entries(m)
        for (x, y) in pix:
            r = tile_of(ts, ent, x, y)
            if r is None:
                continue
            slot, t, pal, tx, ty = r
            if pal == 0 or pal >= 13:
                continue          # palette 0 is never light-blended
            glass_px.setdefault((t, pal), set()).add((tx, ty))
            uses.setdefault((t, pal), set()).add((m, slot))
    # glass colour indices per palette
    shades = {}
    for (t, pal), pix in glass_px.items():
        tile = ts.ptiles[t] if t < 512 else ts.stiles[t - 512]
        for (tx, ty) in pix:
            shades.setdefault(pal, set()).add(tile[ty][tx])
    used = index_usage(cfg, ts)
    alloc = {}                    # pal -> {old idx: light idx}
    notes = []
    for pal, idxs in sorted(shades.items()):
        free = [i for i in range(1, 16) if i not in used[pal]]
        idxs = sorted(idxs, key=lambda i: lum(ts.pals[pal][i]))
        if not free:
            notes.append(f"pal {pal}: no free index, {len(idxs)} glass shades left unlit")
            continue
        if len(free) >= len(idxs):
            alloc[pal] = dict(zip(idxs, free))
        else:                     # merge shades into len(free) brightness bands
            k = len(free)
            alloc[pal] = {i: free[min(k - 1, n * k // len(idxs))] for n, i in enumerate(idxs)}
            notes.append(f"pal {pal}: {len(idxs)} glass shades merged into {k} light colour(s)")
    # tiles needing a copy: drawn by a non-window metatile slot or with another palette
    all_uses = {}
    for m in list(range(len(ts.pmeta))) + [512 + i for i in range(len(ts.smeta))]:
        for slot, e in enumerate(ts.entries(m)):
            all_uses.setdefault(e & 0x3FF, set()).add((m, slot, e >> 12))
    copies = {}
    for (t, pal), u in glass_px.items():
        if pal not in alloc:
            continue
        glass_slots = {(m, s) for (m, s) in uses[(t, pal)]}
        others = {(m, s) for (m, s, p) in all_uses.get(t, ()) if (m, s) not in glass_slots or p != pal}
        if others:
            copies[(t, pal)] = sorted(others)
    return ts, cfg, gm, glass_px, uses, shades, alloc, copies, notes


def report(key):
    ts, cfg, gm, glass_px, uses, shades, alloc, copies, notes = plan(key)
    print(f"glass metatiles: {len(gm)}  glass tiles: {len(glass_px)}  tiles to copy: {len(copies)}")
    for pal, m in sorted(alloc.items()):
        print(f"  pal {pal:2d}: " + ", ".join(f"{o}{ts.pals[pal][o]}->{n}" for o, n in sorted(m.items())))
    for n in notes:
        print("  NOTE", n)
    print("free tile slots:", len(free_tiles(ts, True)), "primary,", len(free_tiles(ts, False)), "secondary")


# ------------------------------------------------------------------ apply
def free_tiles(ts, primary):
    tiles = ts.ptiles if primary else ts.stiles
    ref = set()
    for ent in ts.pmeta + ts.smeta:
        for e in ent:
            ref.add(e & 0x3FF)
    base = 0 if primary else 512
    return [i for i in range(len(tiles)) if (base + i) not in ref and not any(any(r) for r in tiles[i]) and i]


def apply(key):
    ts, cfg, gm, glass_px, uses, shades, alloc, copies, notes = plan(key)
    for n in notes:
        print("NOTE", n)
    pimg = Image.open(os.path.join(ts.pd, "tiles.png"))
    simg = Image.open(os.path.join(ts.sd, "tiles.png"))
    pfree, sfree = free_tiles(ts, True), free_tiles(ts, False)
    pmeta = [list(e) for e in ts.pmeta]
    smeta = [list(e) for e in ts.smeta]

    def put(t, fn):
        img, i = (pimg, t) if t < 512 else (simg, t - 512)
        cols = img.size[0] // 8
        ox, oy = (i % cols) * 8, (i // cols) * 8
        for y in range(8):
            for x in range(8):
                v = fn(x, y, img.getpixel((ox + x, oy + y)))
                if v is not None:
                    img.putpixel((ox + x, oy + y), v)

    def get(t):
        img, i = (pimg, t) if t < 512 else (simg, t - 512)
        cols = img.size[0] // 8
        ox, oy = (i % cols) * 8, (i // cols) * 8
        return [[img.getpixel((ox + x, oy + y)) for x in range(8)] for y in range(8)]

    made = 0
    for (t, pal), pix in glass_px.items():
        if pal not in alloc:
            continue
        remap = alloc[pal]
        target = t
        if (t, pal) in copies:
            # primary metatiles can only reference primary tiles; secondary ones can use either sheet
            needs_primary = any(m < 512 for (m, s) in uses[(t, pal)])
            pool = pfree if (needs_primary or not sfree) else sfree
            if not pool:
                print(f"NOTE no free tile slot for tile {t:03X}; skipped")
                continue
            slot = pool.pop(0)
            target = slot if pool is pfree else 512 + slot
            src = get(t)
            put(target, lambda x, y, v: src[y][x])
            for (m, s) in uses[(t, pal)]:
                meta = pmeta if m < 512 else smeta
                e = meta[m if m < 512 else m - 512][s]
                meta[m if m < 512 else m - 512][s] = (e & ~0x3FF) | target
            made += 1
        put(target, lambda x, y, v: remap.get(v & 15) if (x, y) in pix and (v & 15) in remap else None)
    pimg.save(os.path.join(ts.pd, "tiles.png"))
    simg.save(os.path.join(ts.sd, "tiles.png"))
    for d, meta in ((ts.pd, pmeta), (ts.sd, smeta)):
        open(os.path.join(d, "metatiles.bin"), "wb").write(b"".join(struct.pack("<8H", *e) for e in meta))
    for pal, remap in alloc.items():
        d = ts.pd if pal < T.NUM_PALS_IN_PRIMARY else ts.sd
        p = os.path.join(d, "palettes", f"{pal:02d}.pal")
        cols = T.load_pal(p)
        cols[0] = LAMP
        for old, new in remap.items():
            if cols[new] == (0, 0, 0) or new not in remap.values() or True:
                cols[new] = cols[old] if list(remap.values()).count(new) == 1 else cols[new_shade(remap, new, cols)]
        with open(p, "w", newline="\r\n") as f:
            f.write("JASC-PAL\n0100\n16\n" + "".join(f"{r} {g} {b}\n" for r, g, b in cols))
        lights = sorted(set(remap.values()))
        with open(p[:-4] + ".pla", "w") as f:
            f.write("# Window glass lit at night (dev_scripts/orchid_dns/windows.py); 0 = lamp colour\n0\n")
            f.write("".join(f"{i}\n" for i in lights))
    print(f"copied {made} tiles; lit palettes {sorted(alloc)}")


def new_shade(remap, new, cols):
    """When several glass shades share one light index, keep the middle shade's colour."""
    olds = sorted((o for o, n in remap.items() if n == new), key=lambda o: lum(cols[o]))
    return olds[len(olds) // 2]


def detect_cmd(layout, png, key):
    cfg = CONFIG[key]
    ts, info, blocks, w = T.load_layout(layout)
    h_px, w_px = len(info), len(info[0])
    hits = detect(ts, info, w_px, h_px, blocks, w, cfg)
    gm = glass_by_metatile(cfg) if "--masks" in sys.argv else {}
    im = T.image(ts, info)
    for (x, y) in hits:
        im.putpixel((x, y), (255, 0, 255))
    for y in range(h_px):
        for x in range(w_px):
            if (x % 16, y % 16) in gm.get(blocks[(y // 16) * w + x // 16] & 0x3FF, ()):
                im.putpixel((x, y), (255, 0, 255))
    im.save(png)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "detect":
        detect_cmd(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == "report":
        report(sys.argv[2])
    elif cmd == "apply":
        apply(sys.argv[2])
