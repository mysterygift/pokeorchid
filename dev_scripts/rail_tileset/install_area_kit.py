#!/usr/bin/env python3
"""Outdoor rail kit + level-crossing signage, installed into an area (secondary) tileset.

    python3 dev_scripts/rail_tileset/install_area_kit.py [SECONDARY ...] [--preview DIR] [--dry-run]

gTileset_General has no room left (the Centre/Mart rebuild reused the slots export_rails.py had
taken), so the kit lives in the secondary tileset of each area that has railway instead. The
user chose this on 2026-11-18. Default target: petalburg (Telok Town, Routes 102/103).

What one install adds to a secondary tileset:
  * Rails: the same pieces as export_rails.py (straights, 2x2 curves, buffers, foot crossings)
    on grass and on sand, palette 3 overlay in the top layer, layer COVERED.
  * Advance warning sign (2 metatiles) and boom barriers facing east and west: cabinet with
    the arm lowered (arm over grass or a 3-wide sand path: left edge, middle, right edge) or
    raised (two tiles of upright arm drawn over sprites). Palette 4, whose spare slots 3-5
    this script fills with yellow / dark yellow / black.
  * Labels METATILE_<Tileset>_Crossing* in include/constants/metatile_labels.h, for setmetatile
    (raise/lower a barrier from a script).

Everything is appended after the tileset's own tiles/metatiles at fixed bases (KITS), so a rerun
rewrites the same range. Rerunning after Porymap edits to the kit range overwrites them.
Needs Pillow.
"""
import math
import os
import re
import struct
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import art_crossing as AC  # noqa: E402
import export_rails as R  # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
GENERAL = os.path.join(ROOT, "data", "tilesets", "primary", "general")
LABELS = os.path.join(ROOT, "include", "constants", "metatile_labels.h")

# secondary dir name -> first kit tile slot / first kit metatile (both secondary-relative).
# Bases are the tileset's size before the kit went in; rows of 8 keep the Porymap picker tidy.
KITS = {
    # Petalburg's tiles.png holds 160 tiles, but vanilla metatiles 0x24A/0x24B (on no map) point
    # at tiles 288-307 past its end; starting at 320 keeps them pointing at blank tiles.
    "petalburg": {"tile_base": 320, "meta_base": 144},
}

GROUND = {"grass": 0x001, "sand": 0x121, "path_l": 0x120, "path_m": 0x121, "path_r": 0x122}
COVERED, NORMAL = 1, 0
MB_NORMAL = 0x00


# ------------------------------------------------------------------------------------ pieces
def crossing_pieces():
    """name -> 16x16 rows of palette-4 indices."""
    def idx(rows):
        return [[AC.LEGEND[ch] for ch in r] for r in rows]

    P = {}
    P["WarnTop"] = idx(AC.WARNING_SIGN[:16])
    P["WarnBottom"] = idx(AC.WARNING_SIGN[16:32])
    e = AC.lowered_strip()
    w = AC.hflip(e)
    P["E_Down"] = idx(AC.cell(e, 0, 0))
    P["W_Down"] = idx(AC.cell(w, 3, 0))
    for i in (1, 2, 3):
        P["E_Arm%d" % i] = idx(AC.cell(e, i, 0))
        P["W_Arm%d" % i] = idx(AC.cell(w, 3 - i, 0))
    e = AC.raised_column()
    w = AC.hflip(e)
    for side, c in (("E", e), ("W", w)):
        P[side + "_RaisedTop"] = idx(AC.cell(c, 0, 0))
        P[side + "_RaisedMid"] = idx(AC.cell(c, 0, 1))
        P[side + "_Up"] = idx(AC.cell(c, 0, 2))
    return P


# picker layout, 8 per row: (kind, piece, ground, layer, label) or None for an empty slot
def layout():
    rows = []
    rail = ["H", "V", "HX", "VX", "HW", "HE", "VN", "VS"]
    rows.append([("rail", p, "grass", COVERED, None) for p in rail])
    rows.append([("rail", p, "sand", COVERED, None) for p in rail])
    for cy in (0, 1):
        rows.append([("rail", "%s%s%d%d" % (s, n, cx, cy), "grass", COVERED, None)
                     for s, n in (("E", "S"), ("W", "S"), ("E", "N"), ("W", "N")) for cx in (0, 1)])

    def x(piece, ground, layer, label):
        return ("cross", piece, ground, layer, label)

    rows.append([x("WarnTop", "grass", NORMAL, "CrossingSign_Top"), None,
                 x("E_RaisedTop", "grass", NORMAL, "CrossingBarrierE_RaisedTop"), None, None,
                 x("W_RaisedTop", "grass", NORMAL, "CrossingBarrierW_RaisedTop"), None, None])
    rows.append([x("WarnBottom", "grass", COVERED, "CrossingSign_Bottom"), None,
                 x("E_RaisedMid", "grass", NORMAL, "CrossingBarrierE_RaisedMid"), None, None,
                 x("W_RaisedMid", "grass", NORMAL, "CrossingBarrierW_RaisedMid"), None, None])
    rows.append([None, None, x("E_Up", "grass", COVERED, "CrossingBarrierE_Up"), None, None,
                 x("W_Up", "grass", COVERED, "CrossingBarrierW_Up"), None, None])
    for ground, gl in (("grass", "Grass"), ("path_l", "PathLeft"), ("path_m", "PathMid"), ("path_r", "PathRight")):
        row = [x("E_Down", "grass", COVERED, "CrossingBarrierE_Down") if ground == "grass" else None]
        row += [x("E_Arm%d" % i, ground, COVERED, "CrossingBarrierE_Arm%d_%s" % (i, gl)) for i in (1, 2, 3)]
        row += [x("W_Arm%d" % i, ground, COVERED, "CrossingBarrierW_Arm%d_%s" % (i, gl)) for i in (3, 2, 1)]
        row += [x("W_Down", "grass", COVERED, "CrossingBarrierW_Down") if ground == "grass" else None]
        rows.append(row)
    return rows


# ------------------------------------------------------------------------------------ packing
class Bank:
    """Flip-aware tile bank writing into secondary slots tile_base, tile_base+1, ..."""

    def __init__(self, base):
        self.base, self.tiles, self.lut = base, [], {}

    def add(self, t, pal):
        t = tuple(tuple(r) for r in t)
        if all(c == 0 for r in t for c in r):
            return 0
        if t not in self.lut:
            idx = 512 + self.base + len(self.tiles)
            if idx >= 1024:
                raise SystemExit("secondary tileset is out of tile slots")
            self.tiles.append(t)
            h = tuple(r[::-1] for r in t); v = tuple(t[::-1]); hv = tuple(r[::-1] for r in v)
            for f, bits in ((t, 0), (h, 0x400), (v, 0x800), (hv, 0xC00)):
                self.lut.setdefault(f, idx | bits)
        return self.lut[t] | (pal << 12)


def quads(p):
    return [[row[qx * 8:qx * 8 + 8] for row in p[qy * 8:qy * 8 + 8]] for qy in (0, 1) for qx in (0, 1)]


def read_u16(path):
    b = open(path, "rb").read()
    return list(struct.unpack("<%dH" % (len(b) // 2), b))


def write_u16(path, vals):
    open(path, "wb").write(struct.pack("<%dH" % len(vals), *vals))


def camel(name):
    return "".join(p.capitalize() for p in name.split("_"))


def install(sec, dry=False):
    cfg = KITS[sec]
    d = os.path.join(ROOT, "data", "tilesets", "secondary", sec)
    tb, mb = cfg["tile_base"], cfg["meta_base"]
    gmeta = read_u16(os.path.join(GENERAL, "metatiles.bin"))
    meta = read_u16(os.path.join(d, "metatiles.bin"))
    attr = read_u16(os.path.join(d, "metatile_attributes.bin"))
    assert len(attr) * 8 == len(meta), "metatile_attributes.bin is not u16 per metatile"
    # nothing outside the kit may use kit tiles
    for i in range(min(mb, len(meta) // 8)):
        for e in meta[i * 8:i * 8 + 8]:
            t = e & 0x3FF
            if t >= 512 + tb:
                raise SystemExit("metatile 0x%03X uses tile %d inside the kit range" % (0x200 + i, t - 512))

    rails = R.build_pieces()
    cross = crossing_pieces()
    bank = Bank(tb)
    rows = layout()
    n_meta = len(rows) * 8
    meta = meta[:mb * 8]
    meta += [0] * (mb * 8 - len(meta)) + [0] * (n_meta * 8)
    attr = attr[:mb]
    attr += [0] * (mb - len(attr)) + [0] * n_meta
    labels = []
    for r, row in enumerate(rows):
        for c, slot in enumerate(row):
            mid = mb + r * 8 + c
            if slot is None:
                continue
            kind, piece, ground, layer, label = slot
            g = GROUND[ground]
            top = [bank.add(q, R.PAL if kind == "rail" else AC.PAL)
                   for q in quads(rails[piece] if kind == "rail" else cross[piece])]
            meta[mid * 8:mid * 8 + 4] = gmeta[g * 8:g * 8 + 4]
            meta[mid * 8 + 4:mid * 8 + 8] = top
            attr[mid] = MB_NORMAL | (layer << 12)
            if label:
                labels.append((label, 0x200 + mid))

    # tiles.png: keep the tileset's own tiles, then the kit
    png = os.path.join(d, "tiles.png")
    old = Image.open(png)
    assert old.mode == "P" and old.width == 128, (old.mode, old.size)
    total = tb + len(bank.tiles)
    im = Image.new("P", (128, math.ceil(total / 16) * 8), 0)
    im.putpalette(old.getpalette())
    keep = old.crop((0, 0, 128, min(old.height, math.ceil(tb / 16) * 8)))
    im.paste(keep, (0, 0))
    px = im.load()
    if tb % 16:   # clear the part of a shared row that belongs to the kit
        for t in range(tb, (tb // 16 + 1) * 16):
            for y in range(8):
                for x in range(8):
                    px[(t % 16) * 8 + x, (t // 16) * 8 + y] = 0
    for i, t in enumerate(bank.tiles):
        s = tb + i
        for y in range(8):
            for x in range(8):
                px[(s % 16) * 8 + x, (s // 16) * 8 + y] = t[y][x]

    print("%s: %d tiles at slots %d-%d, %d metatiles at 0x%03X-0x%03X"
          % (sec, len(bank.tiles), tb, total - 1, n_meta, 0x200 + mb, 0x200 + mb + n_meta - 1))
    if dry:
        return
    im.save(png, bits=4, optimize=False)
    set_num_tiles(sec, total)
    write_u16(os.path.join(d, "metatiles.bin"), meta)
    write_u16(os.path.join(d, "metatile_attributes.bin"), attr)
    write_labels(camel(sec), labels)


def set_num_tiles(sec, total):
    """graphics.h builds secondary tiles with -num_tiles N: anything past N never reaches the ROM."""
    path = os.path.join(ROOT, "src", "data", "tilesets", "graphics.h")
    src = open(path).read()
    pat = re.compile(r'(secondary/%s/tiles\.png", "[^"]*", "-num_tiles )(\d+)' % re.escape(sec))
    m = pat.search(src)
    if not m:
        raise SystemExit("no -num_tiles entry for %s in graphics.h" % sec)
    if int(m.group(2)) != total:
        src = src[:m.start(2)] + str(total) + src[m.end(2):]
        open(path, "w").write(src)


def write_labels(ts, labels):
    src = open(LABELS).read()
    begin = "// gTileset_%s: rail + level-crossing kit (dev_scripts/rail_tileset/install_area_kit.py)\n" % ts
    end = "// end %s rail kit\n" % ts
    w = max(len("METATILE_%s_%s" % (ts, n)) for n, _ in labels) + 1
    block = begin + "".join("#define %-*s0x%03X\n" % (w, "METATILE_%s_%s" % (ts, n), v) for n, v in labels) + end
    if begin in src:
        a = src.index(begin)
        b = src.index(end, a) + len(end)
        src = src[:a] + block + src[b:]
    else:
        # insert alphabetically among the "// gTileset_X" sections
        pos = None
        for m in re.finditer(r"^// gTileset_(\w+)\n", src, re.M):
            if m.group(1) > ts:
                pos = m.start()
                break
        if pos is None:
            pos = src.rindex("#endif")
        src = src[:pos] + block + "\n" + src[pos:]
    open(LABELS, "w").write(src)


def set_pal4(dry=False):
    path = os.path.join(GENERAL, "palettes", "04.pal")
    lines = open(path).read().split("\n")
    for k, (r, g, b) in AC.PAL4_EXTRA.items():
        lines[3 + k] = "%d %d %d" % (r, g, b)
    if not dry:
        open(path, "w").write("\n".join(lines))


def main(argv):
    dry = "--dry-run" in argv
    secs = [a for a in argv if not a.startswith("--") and a in KITS] or ["petalburg"]
    for a in argv:
        if not a.startswith("--") and a not in KITS and (argv.index(a) == 0 or argv[argv.index(a) - 1] != "--preview"):
            raise SystemExit("no KITS entry for %s: add its tile/metatile base first" % a)
    set_pal4(dry)
    for s in secs:
        install(s, dry)
    if "--preview" in argv and not dry:
        import preview_area_kit
        out = argv[argv.index("--preview") + 1]
        for s in secs:
            preview_area_kit.render(s, KITS[s]["meta_base"], len(layout()), out)
    print("dry run, nothing written" if dry else "done")


if __name__ == "__main__":
    main(sys.argv[1:])
