#!/usr/bin/env python3
"""Lit windows via a shared "window light" palette in a spare secondary slot.

General's palettes are full (the Battle Frontier, Sevii and every Orchid tileset draw with them), and window
glass shares colours with walls, so glass can't simply be marked as a light in place. Instead one spare
secondary palette slot (TosaPort 11) holds a WINDOW palette built so the windows of several buildings draw
identically by day:
    indices 1-10 = the colours General palettes 0, 1 and 5 share (whites, greys, glass blues, ink)
    11-14       = Pokémon Center reds (General pal 1)
    8, 15       = house wall yellows (General pal 5 13 / 14; house window tiles are copied with 13->8, 14->15)
Lights (.pla): whites and glass blues. The 8x8 entries of window metatiles that are mostly glass switch to
this palette; primary window metatiles are first copied into empty secondary metatile slots and the
secondary's maps repointed, so other tilesets never see the change.

    lightpal.py report JOB
    lightpal.py apply JOB      (run on a clean tileset: it isn't re-entrant)

Glass detection: windows.py (CONFIG[job["windows_cfg"]]).
"""
import json
import os
import struct
import sys

from PIL import Image

import dns_tool as T
import windows as W

ROOT = T.ROOT
JOBS = {
    "tosa_windows": {
        "windows_cfg": "tosa", "light_pal": 11, "base_pal": 1,
        # per source palette: index remap into the window palette (identity if absent); entries using an
        # index not in "allowed" can't be drawn with the window palette and stay as they are
        # pal 0 = the Mart door: its two glass blues aren't in the window palette, so they take its glass
        # blues (12 -> 9, 13 -> 10; a touch brighter by day)
        "sources": {5: {13: 8, 14: 15}, 1: {}, 0: {12: 9, 13: 10}},
        "allowed": set(range(1, 16)) - {0},
        "src_ok": {5: {2, 3, 4, 5, 6, 7, 10, 13, 14}, 1: set(range(1, 15)) - {8}, 0: {1, 2, 3, 4, 5, 6, 7, 9, 10, 12, 13}},
        "overrides": {8: (5, 13), 15: (5, 14)},          # window palette index <- (General palette, index)
        "lights": [1, 2, 3, 4, 9, 10],
        # gym windows stay dark (user: only half a pane lit); its door (0x1CD) is lit. Centre: upper windows
        # + door; Mart: door only (windows.py masks, user 2026-11-23)
        "exclude": [0x1C0, 0x1C1, 0x1C2, 0x1C3, 0x1C4],
        "min_glass": 0.6,
    },
}


def secondary_layouts(cfg):
    L = json.load(open(os.path.join(ROOT, "data/layouts/layouts.json")))["layouts"]
    return [l for l in L if l.get("secondary_tileset") == cfg["secondary"] and l.get("primary_tileset") == cfg["primary"]]


def placed_metatiles(layouts):
    used = set()
    for l in layouts:
        p = os.path.join(ROOT, l["blockdata_filepath"])
        if os.path.exists(p):
            used.update(b & 0x3FF for (b,) in struct.iter_unpack("<H", open(p, "rb").read()))
    return used


def tile_px(ts, t):
    return ts.ptiles[t] if t < 512 else ts.stiles[t - 512]


def plan(job_key):
    job = JOBS[job_key]
    cfg = W.CONFIG[job["windows_cfg"]]
    ts = T.Tilesets(cfg["primary"], cfg["secondary"])
    gm = W.glass_by_metatile(cfg)
    glass_n = {}
    for m, pix in gm.items():
        if m in job["exclude"]:
            continue
        ent = ts.entries(m)
        for (x, y) in pix:
            r = W.tile_of(ts, ent, x, y)
            if r and r[2] in job["sources"]:
                glass_n[(m, r[0])] = glass_n.get((m, r[0]), 0) + 1
    lights = set(job["lights"])
    slots = {}                                      # metatile -> {slot: (tile, src pal)}
    for (m, s), n in glass_n.items():
        e = ts.entries(m)[s]
        t, pal = e & 0x3FF, e >> 12
        px = tile_px(ts, t)
        used = {c for row in px for c in row if c}
        if not used <= job["src_ok"][pal]:
            continue
        remap = job["sources"][pal]
        lit = sum(1 for row in px for c in row if remap.get(c, c) in lights)
        if lit and n / lit >= job["min_glass"]:
            slots.setdefault(m, {})[s] = (t, pal)
    lays = secondary_layouts(cfg)
    used = placed_metatiles(lays)
    blank = [512 + i for i, e in enumerate(ts.smeta) if all((v & 0x3FF) == 0 for v in e) and (512 + i) not in used]
    return job, cfg, ts, slots, lays, blank


def free_primary_tiles(cfg, ts):
    """Primary tiles no placed metatile of ANY layout on this primary references (placed.py)."""
    import placed
    _, _, used_ptiles, _ = placed.placed_usage(cfg["primary"])
    # also keep every tile referenced by any primary metatile (unplaced metatiles stay intact)
    for ent in ts.pmeta:
        for e in ent:
            if (e & 0x3FF) < 512:
                used_ptiles.add(e & 0x3FF)
    return [t for t in range(1, 512) if t not in used_ptiles]


def report(job_key):
    job, cfg, ts, slots, lays, blank = plan(job_key)
    print("metatiles to light:", " ".join(f"{m:03X}{'*' if m < 512 else ''}" for m in sorted(slots)))
    print("entries:", sum(len(v) for v in slots.values()), "primary to copy:", len([m for m in slots if m < 512]),
          "empty secondary slots:", len(blank))
    remapped = {(t, p) for v in slots.values() for (t, p) in v.values() if job["sources"][p]}
    print("tiles needing a remapped copy:", len(remapped), "free primary tiles:", len(free_primary_tiles(cfg, ts)))


def apply(job_key):
    job, cfg, ts, slots, lays, blank = plan(job_key)
    smeta = [list(e) for e in ts.smeta]
    attr_p = open(os.path.join(ts.pd, "metatile_attributes.bin"), "rb").read()
    attr_path = os.path.join(ts.sd, "metatile_attributes.bin")
    attr_s = bytearray(open(attr_path, "rb").read())
    asz = len(attr_s) // len(ts.smeta)
    # remapped tile copies (into free primary tiles: usable from secondary metatiles)
    free = free_primary_tiles(cfg, ts)
    pimg = Image.open(os.path.join(ts.pd, "tiles.png"))
    cols = pimg.size[0] // 8
    copy_of = {}
    for v in slots.values():
        for (t, p) in v.values():
            remap = job["sources"][p]
            if not remap or (t, p) in copy_of:
                continue
            if not free:
                raise SystemExit("out of free primary tiles")
            dst = free.pop(0)
            src = tile_px(ts, t)
            ox, oy = (dst % cols) * 8, (dst // cols) * 8
            for y in range(8):
                for x in range(8):
                    pimg.putpixel((ox + x, oy + y), remap.get(src[y][x], src[y][x]))
            copy_of[(t, p)] = dst
    pimg.save(os.path.join(ts.pd, "tiles.png"))
    remap_mt = {}
    for m, ss in sorted(slots.items()):
        if m < 512:
            if not blank:
                raise SystemExit("no empty secondary metatile slot left")
            new = blank.pop(0)
            ent = list(ts.pmeta[m])
            i = new - 512
            attr_s[i * asz:(i + 1) * asz] = attr_p[m * asz:(m + 1) * asz]
            remap_mt[m] = new
        else:
            new, ent = m, smeta[m - 512]
        for s, (t, p) in ss.items():
            tile = copy_of.get((t, p), t)
            e = ent[s]
            ent[s] = (e & 0x0C00) | tile | (job["light_pal"] << 12)
        smeta[new - 512] = ent
    open(os.path.join(ts.sd, "metatiles.bin"), "wb").write(b"".join(struct.pack("<8H", *e) for e in smeta))
    open(attr_path, "wb").write(attr_s)
    n = 0
    for l in lays:
        p = os.path.join(ROOT, l["blockdata_filepath"])
        if not os.path.exists(p):
            continue
        cells = [b for (b,) in struct.iter_unpack("<H", open(p, "rb").read())]
        out = [(b & ~0x3FF) | remap_mt[b & 0x3FF] if (b & 0x3FF) in remap_mt else b for b in cells]
        if out != cells:
            open(p, "wb").write(struct.pack(f"<{len(out)}H", *out))
            n += 1
    base = T.load_pal(os.path.join(ts.pd, "palettes", f"{job['base_pal']:02d}.pal"))
    colsw = list(base)
    for i, (sp, si) in job["overrides"].items():
        colsw[i] = T.load_pal(os.path.join(ts.pd, "palettes", f"{sp:02d}.pal"))[si]
    colsw[0] = W.LAMP
    dst = os.path.join(ts.sd, "palettes", f"{job['light_pal']:02d}.pal")
    with open(dst, "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n16\n" + "".join(f"{r} {g} {b}\n" for r, g, b in colsw))
    with open(dst[:-4] + ".pla", "w") as f:
        f.write("# lit glass (orchid_dns/lightpal.py)\n0\n")  # gbagfx reads 64-char lines: keep it short
        f.write("".join(f"{i}\n" for i in job["lights"]))
    print(f"lit {len(slots)} metatiles ({sum(len(v) for v in slots.values())} entries; {len(remap_mt)} copied from "
          f"the primary; {len(copy_of)} remapped tiles), updated {n} maps")


if __name__ == "__main__":
    {"report": report, "apply": apply}[sys.argv[1]](sys.argv[2])
