#!/usr/bin/env python3
"""
Ferry berth for the Tosa Port jetty: paints new art over the jetty at the bottom of Tosa Port,
turns it into metatiles appended to gTileset_TosaPort, and rewrites the layout to use them.

gTileset_TosaPort is a copy of gTileset_Slateport made for this (same metatile IDs 0x200-0x3AE,
Cold Storage included), so Slateport City / Routes 108-109 / South Tosa Reserve are untouched.
Slateport is nearly full (70 new tiles needed, 41 safely free), so the copy gives up art Tosa Port
never uses: tiles owned only by metatiles that are not on the Tosa Port map are reclaimed and
those metatiles are blanked (they show as empty in Porymap). Door, rough-water and balloon
animation tiles are always kept. NOTE: dev_scripts/cold_storage_tileset still patches
gTileset_Slateport; Tosa Port's copy of the Cold Storage art is whatever was there on 2026-11-17.

    python export_jetty.py               # patch tileset + Tosa Port (run on a clean tree only)
    python export_jetty.py --previews    # also write before/after previews to ./out
    python export_jetty.py --dry-run     # count tiles/metatiles, write nothing

Art (all in Slateport palette 6, the white cobble-path palette, except the ferry sign in 12):
  concrete slab deck, white kerbs with a dark outline, a pile-supported quay face with rubber
  fenders on the berth, side fenders, mooring bollards with lines to the ship, a steel gangway at
  the boarding warp (16,36), two lamp posts (heads on LAYER_NORMAL so they draw over the player),
  and a ferry pictogram sign beside the jetty entrance. The cobble path now runs straight onto
  the jetty (path corners at row 28 replaced by straight path tiles).

How it fits (512-tile secondary VRAM block):
  * art is drawn on a map-sized overlay; every 8x8 quadrant the overlay fully covers becomes a
    bottom-layer tile, partly covered quadrants keep the original bottom (water/grass) and put the
    art on the top layer
  * tiles dedupe flip-aware against each other AND against every tile Slateport already has
  * new tiles go into slots no metatile references (incl. 504-511, which Slateport's -num_tiles 504
    cut off; the copy builds all 512), then into reclaimed slots (see above)
  * metatiles are appended after the Cold Storage ones (0x3AF+); identical cells share one
"""
import json
import os
import struct
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "out")
PRIM = os.path.join(ROOT, "data", "tilesets", "primary", "general")
SEC = os.path.join(ROOT, "data", "tilesets", "secondary", "tosa_port")
LAYOUT = os.path.join(ROOT, "data", "layouts", "TosaPort", "map.bin")
MAP_JSON = os.path.join(ROOT, "data", "maps", "TosaPort", "map.json")
W, H = 38, 40

BASE_METATILES = 431        # 406 vanilla + 25 Cold Storage
KEEP_METATILES = {0x2DC, 0x393, 0x347, 0x3AA}   # doors, rough water, Cold Storage door (code)
KEEP_TILES = set(range(224, 228))                 # Slateport balloon animation writes here

# palette letters -> (palette slot, colour index); colours come from the .pal files untouched
P6 = dict(W=1, E=2, C=3, V=4, G=5, M=6, D=7, K=8, y=9, Q=11, A=13)
P12 = dict(D=1, K=2, B=3, b=4, G=7, W=10)

LAYER_NORMAL, LAYER_COVERED = 0, 1
MB_NORMAL = 0
WALK, BLOCK = 0x3000, 0x0400        # elevation 3 walkable / collision 1 elevation 0


# ------------------------------------------------------------------ tileset reading/rendering
def read_pal(path):
    v = list(map(int, open(path).read().split()[3:]))
    return [tuple(v[i:i + 3]) for i in range(0, 48, 3)]


class Tileset:
    def __init__(self, d):
        self.dir = d
        self.img = Image.open(os.path.join(d, "tiles.png"))
        self.px = self.img.load()
        self.wt = self.img.size[0] // 8
        self.ntiles = self.wt * (self.img.size[1] // 8)
        self.pals = [read_pal(os.path.join(d, "palettes", f"{i:02d}.pal")) for i in range(16)]
        raw = open(os.path.join(d, "metatiles.bin"), "rb").read()
        self.metatiles = [list(struct.unpack_from("<8H", raw, i)) for i in range(0, len(raw), 16)]
        raw = open(os.path.join(d, "metatile_attributes.bin"), "rb").read()
        self.attrs = [struct.unpack_from("<H", raw, i)[0] for i in range(0, len(raw), 2)]

    def tile(self, t):
        x0, y0 = (t % self.wt) * 8, (t // self.wt) * 8
        return tuple(tuple(self.px[x0 + x, y0 + y] & 15 for x in range(8)) for y in range(8))


class Pair:
    def __init__(self):
        self.p, self.s = Tileset(PRIM), Tileset(SEC)
        self.pal = [self.p.pals[i] if i < 6 else self.s.pals[i] for i in range(16)]

    def tile(self, t):
        return self.p.tile(t) if t < 512 else self.s.tile(t - 512)

    def meta(self, m):
        return self.p.metatiles[m] if m < 512 else self.s.metatiles[m - 512]

    def attr(self, m):
        return self.p.attrs[m] if m < 512 else self.s.attrs[m - 512]

    def rgb(self, pal, i):
        return tuple(v // 8 * 8 for v in self.pal[pal][i])

    def render_entries(self, e, layers=(0, 1)):
        im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
        px = im.load()
        for layer in layers:
            for q in range(4):
                v = e[layer * 4 + q]
                t, hf, vf, pal = v & 0x3FF, (v >> 10) & 1, (v >> 11) & 1, v >> 12
                ti = self.tile(t)
                for y in range(8):
                    for x in range(8):
                        c = ti[7 - y if vf else y][7 - x if hf else x]
                        if c == 0 and layer == 1:
                            continue
                        px[(q % 2) * 8 + x, (q // 2) * 8 + y] = self.rgb(pal, c) + (255,)
        return im

    def render_map(self, grid):
        img = Image.new("RGBA", (len(grid[0]) * 16, len(grid) * 16))
        cache = {}
        for y, row in enumerate(grid):
            for x, v in enumerate(row):
                m = v & 0x3FF
                if m not in cache:
                    cache[m] = self.render_entries(self.meta(m))
                img.paste(cache[m], (x * 16, y * 16))
        return img


def load_grid():
    raw = open(LAYOUT, "rb").read()
    v = struct.unpack(f"<{len(raw) // 2}H", raw)
    return [list(v[i:i + W]) for i in range(0, len(v), W)]


# ------------------------------------------------------------------ the art
X0, X1 = 14 * 16, 25 * 16 + 8         # horizontal arm, west end .. east kerb
XV0 = 22 * 16 + 8                      # vertical arm west kerb
YV0, YH0, YS = 29 * 16, 35 * 16, 37 * 16
PATH_X0, PATH_X1 = 23 * 16, 25 * 16


class Overlay:
    def __init__(self):
        self.px = {}        # (x, y) -> (palette slot, colour index), bottom/covered art
        self.tpx = {}       # top-layer art drawn over sprites (lamp heads -> LAYER_NORMAL)

    def put(self, x, y, ch, pal=6, top=False):
        (self.tpx if top else self.px)[(x, y)] = (pal, (P6 if pal == 6 else P12)[ch])

    def stamp(self, art, x, y, flip=False, pal=6, top=False):
        for j, row in enumerate(art):
            if flip:
                row = row[::-1]
            for i, ch in enumerate(row):
                if ch != ".":
                    self.put(x + i, y + j, ch, pal, top)


def is_deck(x, y):
    return (XV0 <= x < X1 and YV0 <= y < YS) or (X0 <= x < X1 and YH0 <= y < YS)


def open_edge(x, y):
    """A non-deck pixel the deck needs an edge against; the path above the root is not one."""
    if is_deck(x, y):
        return False
    return not (y < YV0 and PATH_X0 <= x < PATH_X1)


def paint_deck(o):
    for y in range(YV0, YS):
        for x in range(X0, X1):
            if not is_deck(x, y):
                continue
            d, side = 99, None
            for r in range(1, 7):
                for dx, dy, s in ((-r, 0, "w"), (r, 0, "e"), (0, -r, "n"), (0, r, "s")):
                    if s == "s" and y + r >= YS:
                        if d > r:
                            d, side = r, "s"
                    elif open_edge(x + dx, y + dy) and d > r:
                        d, side = r, s
                for dx in (-r, r):
                    for dy in (-r, r):
                        if open_edge(x + dx, y + dy) and d > r:
                            d, side = r, "c"
                if d < 99:
                    break
            lx, ly = x % 16, y % 16
            c = "C"                                   # slab: seam, highlight, body
            if lx == 0 or ly == 0:
                c = "A"
            elif lx == 1 or ly == 1:
                c = "E"
            if PATH_X0 <= x < PATH_X1 and y - YV0 in (0, 1):
                c = "A" if y == YV0 else "C"          # joint where the cobble path meets the deck
            if side == "s":                           # cope lip over the quay face
                c = {1: "W", 2: "E", 3: "C"}.get(d, c)
            elif side:                                # kerb: outline, white cope, groove
                if d == 1:
                    c = "D"
                elif d in (2, 3):
                    c = "W" if side in "nw" else "E"
                elif d == 4:
                    c = "E"
                elif d == 5:
                    c = "C"
            o.put(x, y, c)


def paint_face(o):
    for x in range(X0, X1):
        lx = (x - X0) % 16
        for ly in range(16):
            c = None
            if ly == 0:
                c = "C"
            elif ly <= 4:
                c = "G" if lx == 0 else "A"
            elif ly == 5:
                c = "G"
            elif ly == 6:
                c = "M"
            elif ly <= 9:
                c = "K"
            if 8 <= ly <= 13 and lx in (3, 4, 5, 6):  # piles
                c = "CAGM"[lx - 3]
            if ly == 14 and lx in (2, 7):
                c = "W"                               # foam at the waterline
            if (x == X0 or x == X1 - 1) and ly <= 9:
                c = "D"
            if c:
                o.put(x, YS + ly, c)
    for fx in range(X0 + 9, X1 - 4, 16):              # rubber fenders on the berth face
        for y in range(YS - 1, YS + 9):
            for x in range(fx, fx + 5):
                c = "K"
                if x == fx:
                    c = "D"
                if x == fx + 1 and YS <= y <= YS + 6:
                    c = "M"
                if y == YS - 1:
                    c = "D"
                o.put(x, y, c)
    # side fenders (top-down), clear of the kerb bollards and lamp bases
    spots = [(X1, 30 * 16 + 4, 1), (X1, 32 * 16 + 4, 1), (X1, 34 * 16 + 4, 1), (X1, 36 * 16 + 4, 1),
             (XV0 - 1, 32 * 16 + 4, -1), (XV0 - 1, 34 * 16 - 2, -1), (X0 - 1, YH0 + 6, -1)]
    for x0, fy, s in spots:
        for y in range(fy, fy + 9):
            for k in range(3):
                o.put(x0 + s * k, y, "DKK"[k])


BOLLARD = [
    "...KKKK...",
    "..KEWWEK..",
    ".KEEECCAK.",
    ".KACCAAGK.",
    "..KGDDDK..",
    "...KMDK...",
    "...KMDK...",
    "..KGMDDK..",
    ".KDGDDDDK.",
    ".KKDDDDKK.",
    "..KKKKKK..",
]
LAMP_HEAD = [
    "KKKKKKK..",
    "KEEEEEEK.",
    "KDDDDDDDK",
    ".KWWWWK..",
    "..KyyK...",
]
SIGN = [
    ".KKKKKKKKKKKKKK.",
    "KBBBBBBBBBBBBBBK",
    "KBBBBBBWWBBBBBBK",
    "KBBBBBBWWBBBBBBK",
    "KBBBBWWWWWWBBBBK",
    "KBBWWWWWWWWWWWBK",
    "KBBBWWWWWWWWWBBK",
    "KBbbBbbBbbBbbBBK",
    "KBBBBBBBBBBBBBBK",
    ".KKKKKKKKKKKKKK.",
    "......KDGK......",
    "......KDGK......",
    "......KDGK......",
    "......KDGK......",
    ".....KKDGKK.....",
    "......KKKK......",
]
BERTH_BOLLARDS = [(14, 36), (20, 36), (24, 36)]
SIGN_AT = (21, 28)
EAST_LAMP, WEST_LAMP = (25, 31), (22, 33)       # base cells; heads sit in the row above
EAST_BOLLARD, WEST_BOLLARD = (25, 33), (22, 31)
GANGWAY = (16, 36)


def paint_props(o):
    for tx, ty in BERTH_BOLLARDS:
        o.stamp(BOLLARD, tx * 16 + 3, ty * 16 + 1)
    for sx, sy, dx in ((14 * 16 + 9, 36 * 16 + 8, 1), (20 * 16 + 6, 36 * 16 + 8, -1)):
        x, y = sx, sy                                  # mooring lines toward the ferry
        for i in range(10):
            o.put(x, y, "W")
            o.put(x, y + 1, "C")
            y += 1
            if i % 2:
                x += dx
    # kerb bollards sit inside the kerb cell, overhanging the water rather than the walkway
    o.stamp(BOLLARD, EAST_BOLLARD[0] * 16 + 1, EAST_BOLLARD[1] * 16 + 2)
    o.stamp(BOLLARD, WEST_BOLLARD[0] * 16 + 5, WEST_BOLLARD[1] * 16 + 2, True)
    # gangway: steel hinge plate with rivets, treads, white handrails on dark posts
    x0, y0 = GANGWAY[0] * 16 + 2, GANGWAY[1] * 16 + 9
    for y in range(y0, YS + 14):
        for x in range(x0, x0 + 12):
            if y < y0 + 2:
                c = "D" if y == y0 else ("C" if (x - x0) % 3 == 1 else "G")
            elif x in (x0, x0 + 11):
                c = "D"
            elif x in (x0 + 1, x0 + 10):
                c = "G"
            else:
                c = "A" if (y - y0) % 3 == 0 else "C"
            o.put(x, y, c)
    for x in (x0, x0 + 11):
        for y in range(y0 - 3, YS + 12):
            if (y - y0) % 5 == 0 or y == y0 - 3:
                for k in range(3):
                    o.put(x, y - k, "D")
        for y in range(y0 - 3, YS + 11):
            o.put(x, y - 3, "W")
    # lamp posts on the kerbs; the head row goes on the top layer (drawn over sprites)
    for (tx, ty), fl in ((EAST_LAMP, False), (WEST_LAMP, True)):
        pxl = tx * 16 + 3 if not fl else tx * 16 + 12
        base, top = ty * 16 + 13, (ty - 1) * 16 + 6
        for y in range(top, base):
            head = y < ty * 16
            o.put(pxl, y, "G", top=head)
            o.put(pxl + 1, y, "D", top=head)
        for x in range(pxl - 2, pxl + 4):
            o.put(x, base, "K")
            o.put(x, base - 1, "D")
        o.stamp(LAMP_HEAD, pxl - 8 if not fl else pxl, top - 2, flip=fl, top=True)
    o.stamp(SIGN, SIGN_AT[0] * 16, SIGN_AT[1] * 16, pal=12)


def edited_grid(grid):
    g = [r[:] for r in grid]

    def setm(x, y, m):
        g[y][x] = (g[y][x] & ~0x3FF) | m
    setm(23, 28, 0x210)                 # straight path edges instead of the rounded path end
    setm(24, 28, 0x212)
    for x in range(13, 27):
        setm(x, 37, 0x14E)              # old face -> plain water under the new face
    setm(22, 34, 0x14E)                 # old inner kerb corner
    return g


# ------------------------------------------------------------------ packing
def flips(t):
    h = tuple(tuple(reversed(r)) for r in t)
    v = tuple(reversed(t))
    return ((t, 0, 0), (h, 1, 0), (v, 0, 1), (tuple(reversed(h)), 1, 1))


class Bank:
    def __init__(self, pair, slots):
        self.lookup, self.new = {}, {}
        self.slots = list(slots)
        free = set(slots)
        for i in range(pair.s.ntiles):
            if i in free:
                continue
            t = pair.s.tile(i)
            self.lookup.setdefault(t, (512 + i, 0, 0))

    def add(self, t):
        for v, hf, vf in flips(t):
            if v in self.lookup:
                i, h0, v0 = self.lookup[v]
                return i, hf ^ h0, vf ^ v0
        if not self.slots:
            raise SystemExit(f"out of tile slots after {len(self.new)} new tiles")
        i = self.slots.pop(0)
        self.new[i] = t
        self.lookup[t] = (512 + i, 0, 0)
        return 512 + i, 0, 0


def free_slots(pair, grid):
    """Unreferenced slots first, then tiles only metatiles absent from Tosa Port use.
    Returns (slots, owners) where owners[tile] = metatiles to blank if that tile is reclaimed."""
    on_map = {v & 0x3FF for row in grid for v in row} | KEEP_METATILES
    # connected maps are drawn with Tosa Port's tilesets near the seam: keep their metatiles too
    layouts = {l["id"]: l for l in json.load(open(os.path.join(ROOT, "data", "layouts", "layouts.json")))["layouts"]
               if "id" in l}
    for c in json.load(open(MAP_JSON)).get("connections") or []:
        folder = "".join(w.capitalize() for w in c["map"][4:].split("_"))
        mj = os.path.join(ROOT, "data", "maps", folder, "map.json")
        if not os.path.exists(mj):
            raise SystemExit(f"can't find {mj} for connection {c['map']}")
        lay = layouts[json.load(open(mj))["layout"]]
        raw = open(os.path.join(ROOT, lay["blockdata_filepath"]), "rb").read()
        on_map |= {v & 0x3FF for v in struct.unpack(f"<{len(raw) // 2}H", raw)}
    refs = {}
    for i, e in enumerate(pair.s.metatiles):
        for v in e:
            t = v & 0x3FF
            if t >= 512:
                refs.setdefault(t - 512, set()).add(0x200 + i)
    unref = [t for t in range(1, 512) if t not in refs and t not in KEEP_TILES]
    spare = sorted((t for t, ms in refs.items() if t not in KEEP_TILES and not (ms & on_map)),
                   key=lambda t: (min(refs[t]), t))
    return unref + spare, {t: refs.get(t, set()) for t in unref + spare}


def build(pair, grid, o):
    g2 = edited_grid(grid)
    cells = sorted({(x // 16, y // 16) for x, y in list(o.px) + list(o.tpx)})
    slots, owners = free_slots(pair, grid)
    bank = Bank(pair, slots)
    metas, attrs, ids = [], [], {}
    existing = {(tuple(e), a): 0x200 + i
                for i, (e, a) in enumerate(zip(pair.s.metatiles, pair.s.attrs))}
    placed = {}
    for cx, cy in cells:
        orig = g2[cy][cx] & 0x3FF
        oe, oa = list(pair.meta(orig)), pair.attr(orig)
        e = oe[:]
        normal = False
        painted_total = 0
        for q in range(4):
            qx, qy = cx * 16 + (q % 2) * 8, cy * 16 + (q // 2) * 8
            quad = [(qx + x, qy + y) for y in range(8) for x in range(8)]
            base = [p for p in quad if p in o.px]
            head = [p for p in quad if p in o.tpx]
            painted = base
            painted_total += len(base)

            def tile_of(pts, what, src=None):
                src = src or o.px
                pals = {src[p][0] for p in pts}
                if len(pals) != 1:
                    raise SystemExit(f"cell {cx},{cy} q{q} {what}: mixed palettes {pals}")
                s = set(pts)
                t = tuple(tuple(src[(qx + x, qy + y)][1] if (qx + x, qy + y) in s else 0
                                for x in range(8)) for y in range(8))
                i, hf, vf = bank.add(t)
                return i | hf << 10 | vf << 11 | pals.pop() << 12

            if len(base) == 64:
                e[q] = tile_of(base, "bottom")
                e[4 + q] = tile_of(head, "top", o.tpx) if head else 0
            elif base or head:
                if oe[4 + q] & 0x3FF:
                    raise SystemExit(f"cell {cx},{cy} q{q}: art over an existing top tile "
                                     f"(metatile {orig:#x})")
                if base and head:
                    raise SystemExit(f"cell {cx},{cy} q{q}: lamp head over a partial quadrant")
                e[4 + q] = tile_of(base, "top") if base else tile_of(head, "top", o.tpx)
            if head:
                normal = True
        behaviour = MB_NORMAL if painted_total >= 64 else oa & 0xFF
        layer = LAYER_NORMAL if normal else LAYER_COVERED
        if not normal and (oa >> 12) & 0xF not in (LAYER_COVERED,) and painted_total < 256:
            # keep the original layer type where only a corner was touched and it had top art
            if any(oe[4 + q] & 0x3FF for q in range(4)):
                layer = (oa >> 12) & 0xF
        a = behaviour | layer << 12
        key = (tuple(e), a)
        if key in existing:
            mid = existing[key]
        elif key in ids:
            mid = ids[key]
        else:
            mid = 0x200 + BASE_METATILES + len(metas)
            ids[key] = mid
            metas.append(e)
            attrs.append(a)
        placed[(cx, cy)] = mid
    bank.blank = sorted(set().union(*(owners[t] for t in bank.new)) if bank.new else set())
    bank.nslots = len(slots)
    return g2, placed, metas, attrs, bank


def collision(g2, placed):
    blocked = set(BERTH_BOLLARDS) | {SIGN_AT}
    walk = {(18, 36)}                     # the old white post there is gone
    out = [r[:] for r in g2]
    for (x, y), mid in placed.items():
        v = (g2[y][x] & ~0x3FF) | mid
        if (x, y) in blocked:
            v = BLOCK | mid
        elif (x, y) in walk:
            v = WALK | mid
        out[y][x] = v
    return out


# ------------------------------------------------------------------ writing
def write_tiles(bank):
    im = Image.open(os.path.join(SEC, "tiles.png"))
    px = im.load()
    for i, t in bank.new.items():
        ox, oy = (i % 16) * 8, (i // 16) * 8
        for y in range(8):
            for x in range(8):
                px[ox + x, oy + y] = t[y][x]
    im.save(os.path.join(SEC, "tiles.png"), bits=4, optimize=False)


def append_metatiles(metas, attrs, blank):
    path = os.path.join(SEC, "metatiles.bin")
    raw = bytearray(open(path, "rb").read())
    for m in blank:                     # metatiles whose art was reclaimed -> empty
        raw[(m - 0x200) * 16:(m - 0x200) * 16 + 16] = bytes(16)
    open(path, "wb").write(raw)
    for name, fmt, rows in (("metatiles.bin", "<8H", metas), ("metatile_attributes.bin", "<H", attrs)):
        path = os.path.join(SEC, name)
        size = struct.calcsize(fmt)
        raw = open(path, "rb").read()
        assert len(raw) == BASE_METATILES * size, f"{name}: expected {BASE_METATILES} metatiles " \
            f"(run on a tree without the jetty already applied)"
        with open(path, "wb") as f:
            f.write(raw)
            for r in rows:
                f.write(struct.pack(fmt, *r) if fmt == "<8H" else struct.pack(fmt, r))


def write_grid(g):
    with open(LAYOUT, "wb") as f:
        for row in g:
            f.write(struct.pack(f"<{W}H", *row))


def move_ferry():
    d = json.load(open(MAP_JSON))
    for ob in d["object_events"]:
        if ob["graphics_id"] == "OBJ_EVENT_GFX_SS_TIDAL":
            ob["y"] = 39
    with open(MAP_JSON, "w") as f:
        json.dump(d, f, indent=2)
        f.write("\n")


# ------------------------------------------------------------------ previews
def sprite(png, palfile, w, h):
    im = Image.open(os.path.join(ROOT, png))
    pal = read_pal(os.path.join(ROOT, palfile)) if palfile else \
        [tuple(im.getpalette()[i * 3:i * 3 + 3]) for i in range(16)]
    src = im.crop((0, 0, w, h)).load()
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dst = out.load()
    for y in range(h):
        for x in range(w):
            i = src[x, y] & 15
            if i:
                dst[x, y] = tuple(v // 8 * 8 for v in pal[i]) + (255,)
    return out


def with_objects(img, ship_y):
    d = json.load(open(MAP_JSON))
    pics = {"OBJ_EVENT_GFX_SAILOR": "people/sailor.png", "OBJ_EVENT_GFX_SCIENTIST_2": "people/scientist_2.png",
            "OBJ_EVENT_GFX_OLD_MAN": "people/old_man.png", "OBJ_EVENT_GFX_FISHERMAN": "people/fisherman.png"}
    out = img.copy()
    obs = [(ob["y"], ob["x"], ob["graphics_id"]) for ob in d["object_events"]]
    obs.append((35, 17, "PLAYER"))
    for y, x, gid in sorted(obs):
        if gid == "OBJ_EVENT_GFX_SS_TIDAL":
            s = sprite("graphics/object_events/pics/misc/ss_tidal.png",
                       "graphics/object_events/palettes/ss_tidal.pal", 96, 40)
            y = ship_y
        elif gid == "PLAYER":
            s = sprite("graphics/object_events/pics/people/brendan/walking.png", None, 16, 32)
        elif gid in pics and os.path.exists(os.path.join(ROOT, "graphics/object_events/pics", pics[gid])):
            s = sprite("graphics/object_events/pics/" + pics[gid], None, 16, 32)
        else:
            continue
        out.alpha_composite(s, (x * 16 + 8 - s.width // 2, y * 16 + 16 - s.height))
    pad = Image.new("RGBA", (out.width, out.height + 64))
    pair = Pair()
    wt = pair.render_entries(pair.meta(0x14E))
    for tx in range(W):
        for ty in range(H, H + 4):
            pad.paste(wt, (tx * 16, ty * 16))
    pad.alpha_composite(out, (0, 0))
    return pad


def previews(before, ship_before):
    os.makedirs(OUT, exist_ok=True)
    pair = Pair()                                   # re-read: renders from the written files
    after = with_objects(pair.render_map(load_grid()), 39)
    before = with_objects(before, ship_before)
    for name, im in (("before", before), ("after", after)):
        im.crop((10 * 16, 22 * 16, 30 * 16, 40 * 16)).resize((960, 864), Image.NEAREST) \
            .save(os.path.join(OUT, f"{name}_area.png"))
    print("previews in", OUT)


def main(argv):
    pair = Pair()
    grid = load_grid()
    if len(pair.s.metatiles) != BASE_METATILES:
        raise SystemExit(f"TosaPort has {len(pair.s.metatiles)} metatiles, expected "
                         f"{BASE_METATILES}: already applied?")
    o = Overlay()
    paint_deck(o)
    paint_face(o)
    paint_props(o)
    g2, placed, metas, attrs, bank = build(pair, grid, o)
    final = collision(g2, placed)
    print(f"cells repainted: {len(placed)}; new metatiles: {len(metas)} "
          f"({BASE_METATILES} + {len(metas)} = {BASE_METATILES + len(metas)} / 512)")
    print(f"new tiles: {len(bank.new)} / {bank.nslots} available; "
          f"{len(bank.blank)} unused metatiles blanked: {' '.join(f'{m:#x}' for m in bank.blank)}")
    if "--dry-run" in argv:
        return 0
    before = pair.render_map(grid) if "--previews" in argv else None
    write_tiles(bank)
    append_metatiles(metas, attrs, bank.blank)
    write_grid(final)
    move_ferry()
    if before is not None:
        previews(before, 38)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
