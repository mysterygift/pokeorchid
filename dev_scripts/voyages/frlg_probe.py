"""
Feasibility probe for a FRLG -> Emerald metatile translation table (batch 3): every distinct metatile a
deleted FRLG layout uses (git 8ee39561d7~1, drawn with the FRLG tilesets still in data/tilesets), grouped by
kind, with use counts. Kind = a first guess from the metatile behaviour + collision + colour, then KIND_FIX
(hand-checked against the contact sheet).

usage: <venv python> dev_scripts/voyages/frlg_probe.py [LAYOUT_ID] [out_base]
       (default LAYOUT_FOUR_ISLAND -> out/batch3/four_island_metatile_probe.png/.txt)
"""
import collections
import json
import os
import re
import struct
import sys

from PIL import Image, ImageDraw

import frlg_ref as fr

HERE = os.path.dirname(os.path.abspath(__file__))
KINDS = ["water", "shore edge", "sand", "grass", "tall grass", "tree", "rock", "cliff", "ledge", "building",
         "path", "decor"]
_ENUM = [m.group(1) for m in re.finditer(r"^\s+(MB_\w+),", open(os.path.join(
    fr.ROOT, "include", "constants", "metatile_behaviors.h")).read(), re.M)]

def _ids(*a):
    return [int(x, 16) for x in " ".join(a).split()]


# hand corrections after reading the contact sheet (2026-11-19): {layout: {metatile id: kind}}
KIND_FIX = {"LAYOUT_FOUR_ISLAND": dict(
    [(m, "building") for m in _ids("029 02A 030 031 032 033 038 03B 286 287 2E3 2E4 2E6 2E7 2E5 028 02B 039 03A",
                                   "040 041 058 059 05A 05B 060 061 063 186 197 19F 28E 28F 291 292 295 296 297",
                                   "299 29B 29C 29D 2B8 2BA 2BB 048 049 04A 04B 050 051 052 053 187 18F 2A8 2A9",
                                   "2AA 2AB 2B0 2B1 2B2 2B3 2CB 2CC 2CD 2D3 2D4 2D5 2DB 2DC 2DD 062 289 28A 28B",
                                   "28C 28D 293 294 29A 2B9 2E8 2E9 2EA 2F0 2F1 2F2 281 282 285")]
    + [(m, "path") for m in _ids("2F3 2F4 2F5 2F6 2F7 089 091 2F8 2FA 1BD 1BE 1BF 2F9 0C5 0C6 0C7 0CD 0CE 0CF")]
    + [(m, "rock") for m in _ids("24C 24D 069 071 0BA 0BB 305")]
    + [(m, "decor") for m in _ids("002 169 004 161 2A0 2A1 2A2 2A3")]
    + [(m, "ledge") for m in _ids("17B 17C 17D 17E 17F")]
    + [(m, "shore edge") for m in _ids("1B3")]
    + [(m, "cliff") for m in _ids("070 072 073 075 079 07A 07B 07C 0A0 0A8 0A9 0B2 0B3 0B4 0B5 068 306")]
    + [(m, "tree") for m in _ids("0E6 0E8 0E9 0F8 0F9 016 017 01B 01E 01F 0EA 0F0 0F1 2BF")]
)}


def _draw(p, s, mid):
    """One 16x16 FRLG metatile (both layers)."""
    pals = p.pals[:7] + s.pals[7:13] + p.pals[13:]
    ts, i = (p, mid) if mid < 640 else (s, mid - 640)
    im = Image.new("RGB", (16, 16))
    px = im.load()
    if i >= len(ts.meta):
        return im, 0
    for k, ent in enumerate(ts.meta[i]):
        t, hf, vf, pal = ent & 0x3FF, (ent >> 10) & 1, (ent >> 11) & 1, ent >> 12
        tt, ti = (p, t) if t < 640 else (s, t - 640)
        if ti >= tt.n:
            continue
        ox, oy = (ti % tt.w) * 8, (ti // tt.w) * 8
        q = k & 3
        bx, by = (q & 1) * 8, (q >> 1) * 8
        for y in range(8):
            for x in range(8):
                ci = tt.px[ox + (7 - x if hf else x), oy + (7 - y if vf else y)] & 15
                if ci == 0 and k >= 4:
                    continue
                px[bx + x, by + y] = pals[pal][ci]
    return im, ts.attrs[i]


def _colour_kind(im, solid):
    """Rough colour heuristic for MB_NORMAL cells."""
    n = {"blue": 0, "green": 0, "dkgreen": 0, "sand": 0, "brown": 0, "grey": 0, "other": 0}
    for r, g, b in im.getdata():
        if b > r + 30 and b > g:
            n["blue"] += 1
        elif g > r + 20 and g > b + 20:
            n["dkgreen" if g < 140 else "green"] += 1
        elif r > 180 and g > 160 and b < 150:
            n["sand"] += 1
        elif r > g + 15 and g > b:
            n["brown"] += 1
        elif abs(r - g) < 20 and abs(g - b) < 20:
            n["grey"] += 1
        else:
            n["other"] += 1
    top = max(n, key=n.get)
    if n["blue"] > 200:
        return "water"
    if n["blue"] > 40:
        return "shore edge"
    if top in ("green", "dkgreen") and solid and n["dkgreen"] > 60:
        return "tree"
    if top == "brown":
        return "cliff" if solid else "path"
    if top == "sand":
        return "sand"
    if top in ("green", "dkgreen"):
        return "grass" if not solid else "decor"
    return "building" if solid else "decor"


def classify(beh, solid, im):
    name = _ENUM[beh] if beh < len(_ENUM) else "MB_%d" % beh
    if "WATER" in name or "WATERFALL" in name or name in ("MB_SEAWEED", "MB_DIVE"):
        return ("water" if _colour_kind(im, solid) == "water" else "shore edge"), name
    if name in ("MB_TALL_GRASS", "MB_LONG_GRASS"):
        return "tall grass", name
    if name.startswith("MB_JUMP"):
        return "ledge", name
    if "DOOR" in name or "WARP" in name or "COUNTER" in name or "PC" in name:
        return "building", name
    if name in ("MB_SAND", "MB_DEEP_SAND", "MB_FOOTPRINTS"):
        return "sand", name
    return _colour_kind(im, solid), name


def probe(layout_id, out_base):
    js = json.loads(fr._git("data/layouts/layouts.json"))
    e = next(x for x in js["layouts"] if x.get("id") == layout_id)
    w, h = e["width"], e["height"]
    vals = struct.unpack("<%dH" % (w * h), fr._git(e["blockdata_filepath"])[:2 * w * h])
    p, s = fr.FTileset(e["primary_tileset"]), fr.FTileset(e["secondary_tileset"])
    count = collections.Counter(v & 0x3FF for v in vals)
    solid = {}
    for v in vals:
        solid.setdefault(v & 0x3FF, (v >> 10) & 3 != 0)
    fix = KIND_FIX.get(layout_id, {})
    rows = []
    for mid in sorted(count):
        im, attr = _draw(p, s, mid)
        kind, bname = classify(attr & 0x1FF, solid[mid], im)
        kind = fix.get(mid, kind)
        rows.append((kind, mid, count[mid], bname, solid[mid], im))
    groups = collections.OrderedDict((k, [r for r in rows if r[0] == k]) for k in KINDS)
    # contact sheet: one band per kind
    S, cols, cw, chh = 3, 12, 16 * 3 + 30, 16 * 3 + 22
    bands = [(k, g) for k, g in groups.items() if g]
    H = sum(22 + ((len(g) + cols - 1) // cols) * chh for _, g in bands) + 30
    sheet = Image.new("RGB", (cols * cw + 10, H), (255, 255, 255))
    d = ImageDraw.Draw(sheet)
    d.text((5, 5), "%s: %d distinct FRLG metatiles (%d primary %s, %d secondary %s), %d cells" % (
        layout_id, len(count), sum(1 for m in count if m < 640), e["primary_tileset"],
        sum(1 for m in count if m >= 640), e["secondary_tileset"], w * h), fill=(0, 0, 0))
    y = 26
    for k, g in bands:
        d.text((5, y + 4), "%s  (%d metatiles, %d cells)" % (k.upper(), len(g), sum(r[2] for r in g)),
               fill=(160, 0, 0))
        y += 22
        for i, (kind, mid, n, bname, sol, im) in enumerate(g):
            X, Y = 5 + (i % cols) * cw, y + (i // cols) * chh
            sheet.paste(im.resize((48, 48), Image.NEAREST), (X, Y))
            d.text((X, Y + 49), "%03X x%d%s" % (mid, n, "*" if sol else ""), fill=(0, 0, 0))
        y += ((len(g) + cols - 1) // cols) * chh
    sheet.save(out_base + ".png")
    with open(out_base + ".txt", "w") as f:
        f.write("%s  %dx%d  %s + %s\n" % (layout_id, w, h, e["primary_tileset"], e["secondary_tileset"]))
        f.write("distinct metatiles: %d (primary %d, secondary %d)\n\n" % (
            len(count), sum(1 for m in count if m < 640), sum(1 for m in count if m >= 640)))
        f.write("%-11s %5s %6s\n" % ("kind", "tiles", "cells"))
        for k, g in groups.items():
            f.write("%-11s %5d %6d\n" % (k, len(g), sum(r[2] for r in g)))
        f.write("\nid   cells solid behaviour  kind\n")
        for kind, mid, n, bname, sol, im in sorted(rows, key=lambda r: (KINDS.index(r[0]), r[1])):
            f.write("%03X %5d %s %-28s %s\n" % (mid, n, "*" if sol else " ", bname, kind))
    return groups


def main(out_base=None, layout_id="LAYOUT_FOUR_ISLAND"):
    out_base = out_base or os.path.join(HERE, "out", "batch3", layout_id[7:].lower() + "_metatile_probe")
    groups = probe(layout_id, out_base)
    print(layout_id, " ".join("%s=%d" % (k, len(g)) for k, g in groups.items()),
          "total=%d" % sum(len(g) for g in groups.values()))


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[1] if len(a) > 1 else None, a[0] if a else "LAYOUT_FOUR_ISLAND")
