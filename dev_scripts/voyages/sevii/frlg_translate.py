"""
FRLG -> Emerald map translator for design-review mockups (Sailor's Voyages, Sevii Islands).

The FRLG maps were deleted from Orchid (git FRLG_REF is the last commit that has them; the FRLG tilesets
are still in data/tilesets). FRLG tilesets need the FRLG primary, so their cells cannot be copied into an
Emerald map. This tool instead re-draws an FRLG map cell for cell in an Emerald tileset pair:

  1. classify  every FRLG metatile into a terrain class (CLASSES) from its behaviour (MB_*), terrain /
               encounter bits, the collision it has in the maps, and its look (colour fractions).
               OVERRIDES fixes the ones the heuristic gets wrong; `classes` writes a review table.
  2. context   per map: warps -> building footprints (flood over building cells from each door), bridge
               cells (walkable between water), sign bg_events -> sign cells.
  3. render    the class grid becomes a voyage_compose spec at the SAME width / height: water / shore /
               rock rim / rock massif / pond edges by the learned autotilers, 2x2 trees, 9-slice paths,
               ledges, stairs, bridges, fences solved from vanilla neighbours; buildings stamped from
               Emerald / Orchid exteriors with the door on FRLG's warp cell (PAIRS[...]["buildings"]).
  4. events    warps, connections, signs, objects, hidden items carried over as marks; FRLG-only overworld
               graphics (the IS_FRLG block of object_event_graphics_info_pointers.h) swapped for Emerald
               look-alikes (GFX_SWAP).

usage (scratchpad venv python, see voyage_compose):
  frlg_translate.py classes MAP [MAP ...]                  -> out/frlg_translate/classes.png + classes.json
  frlg_translate.py MAP[:PAIR] [MAP[:PAIR] ...] [--out DIR] -> DIR/<map>.png, @2x, _vs_frlg.png, _spec.json
  frlg_translate.py export [--out DIR]                      -> REAL map data for every Sevii map (export_maps.py):
                                                             layouts/<F>/map.bin+border.bin, layouts.json,
                                                             maps/<Map>/map.json, tilesets/sevii_islands/
  MAP is the FRLG map folder name without _Frlg (OneIsland, OneIsland_KindleRoad, MtEmber_Exterior ...).
  PAIR is a key of PAIRS (default: DEFAULT_PAIR, or the batch's per-map choice passed in by its script).

Library use (batch scripts): fmap = load_map(name); spec = translate(fmap, pair_key, extra=...);
vc.render(spec, out_base); side_by_side(fmap, out_base). The spec is a plain voyage_compose spec, so a
batch can patch it (extra stamps / marks) before rendering.

If something is missing from git, clone pret/pokefirered to PFR_CLONE and it is read from there.
"""
import json
import os
import re
import struct
import subprocess
import sys
from collections import Counter, deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import voyage_compose as vc            # noqa: E402
from PIL import Image, ImageDraw       # noqa: E402

ROOT = vc.ROOT
FRLG_REF = "8ee39561d7~1"              # last commit with the FRLG maps ("Removed FRLG maps ..." is 8ee39561d7)
PFR_CLONE = os.path.abspath(os.path.join(ROOT, "..", "pokefirered-ref"))
OUT = os.path.join(HERE, "out", "frlg_translate")
MB = re.findall(r"^\s+(MB_\w+)", open(os.path.join(ROOT, "include", "constants", "metatile_behaviors.h")).read(),
                re.M)


# ================================================================================================ sources
def _git(path):
    r = subprocess.run(["git", "-C", ROOT, "show", "%s:%s" % (FRLG_REF, path)], capture_output=True)
    if r.returncode == 0:
        return r.stdout
    p = os.path.join(PFR_CLONE, path.replace("_Frlg", ""))
    if os.path.exists(p):
        return open(p, "rb").read()
    raise FileNotFoundError(path)


_LAYOUTS = None


def frlg_layouts():
    global _LAYOUTS
    if _LAYOUTS is None:
        _LAYOUTS = {e["id"]: e for e in json.loads(_git("data/layouts/layouts.json"))["layouts"] if "id" in e}
    return _LAYOUTS


def _jasc(path):
    v = open(path).read().split()[3:]
    return [tuple(int(c) // 8 * 8 for c in v[i * 3:i * 3 + 3]) for i in range(len(v) // 3)]


def tileset_dir(sym):
    """gTileset_SeviiIslands123 -> data/tilesets/secondary/sevii_islands_123_frlg (and similar)."""
    name = sym.replace("gTileset_", "")
    snake = re.sub(r"(?<=[a-z])(?=[A-Z0-9])|(?<=[0-9])(?=[A-Z])", "_", name).lower().replace("__", "_")
    for kind in ("primary", "secondary"):
        for cand in (snake, snake + "_frlg", snake.replace("_frlg", "") + "_frlg"):
            p = os.path.join(ROOT, "data", "tilesets", kind, cand)
            if os.path.isdir(p):
                return p
    raise FileNotFoundError(sym)


class FTileset:
    """FRLG tileset: metatiles + u32 attributes (behaviour bits 0-8, terrain 9-13, encounter 24-26,
    layer 29-30)."""

    def __init__(self, sym):
        d = tileset_dir(sym)
        self.sym = sym
        im = Image.open(os.path.join(d, "tiles.png"))
        self.w, self.px, self.n = im.width // 8, im.load(), (im.width // 8) * (im.height // 8)
        raw = open(os.path.join(d, "metatiles.bin"), "rb").read()
        self.meta = [struct.unpack_from("<8H", raw, i * 16) for i in range(len(raw) // 16)]
        raw = open(os.path.join(d, "metatile_attributes.bin"), "rb").read()
        self.attrs = list(struct.unpack("<%dI" % (len(raw) // 4), raw))
        self.pals = [_jasc(os.path.join(d, "palettes", "%02d.pal" % i)) for i in range(16)]


_TS = {}


def ftileset(sym):
    if sym not in _TS:
        _TS[sym] = FTileset(sym)
    return _TS[sym]


class FScene:
    """FRLG primary (640 metatiles, palettes 0-6) + secondary (palettes 7-12)."""

    def __init__(self, primary, secondary):
        self.p, self.s = ftileset(primary), ftileset(secondary)
        self.pals = self.p.pals[:7] + self.s.pals[7:13] + self.p.pals[13:]
        self.cache = {}

    def _ts(self, mid):
        return (self.p, mid) if mid < 640 else (self.s, mid - 640)

    def attr(self, mid):
        ts, i = self._ts(mid)
        return ts.attrs[i] if i < len(ts.attrs) else 0

    def key(self, mid):
        """Stable id across maps: ('General_Frlg' | secondary name, metatile id)."""
        return ("General_Frlg" if mid < 640 else self.s.sym.replace("gTileset_", ""), mid)

    def image(self, mid):
        if mid in self.cache:
            return self.cache[mid]
        ts, i = self._ts(mid)
        im = Image.new("RGB", (16, 16))
        px = im.load()
        if i < len(ts.meta):
            for k, ent in enumerate(ts.meta[i]):
                t, hf, vf, pal = ent & 0x3FF, (ent >> 10) & 1, (ent >> 11) & 1, ent >> 12
                tt, ti = (self.p, t) if t < 640 else (self.s, t - 640)
                if ti >= tt.n:
                    continue
                ox, oy = (ti % tt.w) * 8, (ti // tt.w) * 8
                q = k & 3
                for y in range(8):
                    for x in range(8):
                        ci = tt.px[ox + (7 - x if hf else x), oy + (7 - y if vf else y)] & 15
                        if ci == 0 and k >= 4:
                            continue
                        px[(q & 1) * 8 + x, (q >> 1) * 8 + y] = self.pals[pal][ci]
        self.cache[mid] = im
        return im


class FrlgMap:
    def __init__(self, name):
        self.name = name
        self.json = json.loads(_git("data/maps/%s_Frlg/map.json" % name))
        e = frlg_layouts()[self.json["layout"]]
        self.layout = e
        self.w, self.h = e["width"], e["height"]
        vals = struct.unpack("<%dH" % (self.w * self.h), _git(e["blockdata_filepath"])[:2 * self.w * self.h])
        self.raw = [list(vals[y * self.w:(y + 1) * self.w]) for y in range(self.h)]
        self.scene = FScene(e["primary_tileset"], e["secondary_tileset"])

    def mid(self, x, y):
        return self.raw[y][x] & 0x3FF

    def coll(self, x, y):
        return (self.raw[y][x] >> 10) & 3

    def picture(self, scale=1):
        im = Image.new("RGB", (self.w * 16, self.h * 16))
        for y in range(self.h):
            for x in range(self.w):
                im.paste(self.scene.image(self.mid(x, y)), (x * 16, y * 16))
        return im.resize((im.width * scale, im.height * scale), Image.NEAREST) if scale != 1 else im


_MAPS = {}


def load_map(name):
    if name not in _MAPS:
        _MAPS[name] = FrlgMap(name)
    return _MAPS[name]


# ================================================================================================ classes
# char: (meaning, Emerald representative shown in the class table: ("id", m) or a note)
CLASSES = {
    "~": ("sea (ocean / fast current)", 0x170),
    "q": ("pond water", 0x0A1),
    "|": ("waterfall (lip 0BB/0B3/0BC, body 0B9, splash 02C/034/03C)", 0x0B9),
    "s": ("sand / beach", 0x124),
    ".": ("grass", 0x001),
    "g": ("tall grass", 0x00D),
    "f": ("flowers", 0x004),
    "p": ("path (sandy road)", 0x121),
    "T": ("tree (2x2 where possible)", 0x1D4),
    "M": ("rock wall / cliff (autotiled)", 0x07C),
    "v": ("ledge, jump south", 0x087),
    "<": ("ledge, jump west", 0x085),
    ">": ("ledge, jump east", 0x086),
    "h": ("stairs", 0x0AF),
    "b": ("bridge / boardwalk", "pair"),
    "k": ("wooden deck / bridge planks", "pair"),
    "r": ("sea rock (2x2 Emerald rock placed)", 0x150),
    "B": ("building (stamped)", "stamp"),
    "D": ("door (stamped)", "stamp"),
    "n": ("sign", 0x003),
    "F": ("fence", 0x149),
    "o": ("small rock / boulder", 0x0E2),
    "d": ("other decor (impassable)", 0x0E2),
    "c": ("cave mouth (stamped)", "stamp"),
    "x": ("UNRESOLVED", None),
}
WATER_MB = {"MB_OCEAN_WATER", "MB_FAST_WATER", "MB_DEEP_WATER", "MB_SEMI_DEEP_WATER", "MB_INTERIOR_DEEP_WATER",
            "MB_SOOTOPOLIS_DEEP_WATER", "MB_NO_SURFACING", "MB_EASTWARD_CURRENT", "MB_WESTWARD_CURRENT",
            "MB_NORTHWARD_CURRENT", "MB_SOUTHWARD_CURRENT"}

# (tileset name, metatile id) -> class: fixes after reviewing classes.png. Batch scripts may add more.
OVERRIDES = {}


def _ov(ts, ids, cls):
    for m in ids:
        OVERRIDES[(ts, m)] = cls


# reviewed on classes.png (Sevii 1-3): fence posts / bollards / railings, pink lattice railings
_ov("General_Frlg", [0x0D6, 0x0D7, 0x0E6, 0x0E7, 0x0E8, 0x0E9, 0x0EC, 0x0F0, 0x0F4, 0x0F8, 0x0F9], "F")
_ov("SeviiIslands123", range(0x324, 0x32F), "F")
_ov("SeviiIslands123", [0x32F], "~")                 # cliff foot in the shallows (Cape Brink's north edge)
_ov("General_Frlg", [0x0DB, 0x0DC, 0x0DD], "p")      # sandy road beyond an exit warp (impassable, still road)
_ov("SeviiIslands123", [0x318, 0x319, 0x31A, 0x31B, 0x31D, 0x31E, 0x31F], "M")   # grass over a pink cliff lip
_ov("SeviiIslands123", [0x2B9, 0x2BC], "d")          # trash cans
# wooden walkways to the Seagallop harbours (+ the harbour roof edge at the map's bottom row) -> deck
_ov("General_Frlg", range(0x1BD, 0x1C8), "k")
_ov("SeviiIslands123", [0x2B4, 0x2B5, 0x2B6, 0x2F0, 0x2F1, 0x2F2], "k")
# rock cliffs standing in (fast) sea water: rock, so the rim autotiler draws a cliff coast
_ov("General_Frlg", [0x265, 0x26B, 0x26C, 0x270, 0x272, 0x274], "M")
# freestanding decorative boulders (user, 2026-11-19: "freestanding rocks ... should just be continuous terrain"):
# class 'o' -> Emerald's fixed one-cell boulder for the ground around it (BOULDERS), not a rock-massif piece.
# FRLG's Rock Smash rocks are objects (BREAKABLE_ROCK_FRLG), never metatiles: they stay objects.
_ov("General_Frlg", [0x0AF, 0x0B7], "o")             # brown boulders on sand / dirt (Kindle Road, Ruin Valley)
_ov("SeviiIslands45", [0x309, 0x30A], "o")           # grey boulders on grass (Memorial Pillar)
_ov("SeviiIslands123", [0x357], "o")                 # boulders on Mt. Ember's ash


# Emerald General-primary one-cell boulders (raw values copied from vanilla layouts by ("id", m)):
#   0x0E0 grey boulder on grass        (Routes 111/112/115/118, Faraway Island interior)
#   0x0E1 brown boulder on rocky dirt  (Routes 113/116, Faraway Island entrance)
#   0x0E2 boulder on sand              (Dewford, Route 106, Route 111 desert, Navel Rock exterior)
BOULDERS = {"grass": 0x0E0, "dirt": 0x0E1, "sand": 0x0E2}
_BOULDER_GROUND = {".": "grass", "g": "grass", "f": "grass", "L": "grass", "s": "sand", "S": "sand",
                   "p": "dirt", "M": "dirt", "h": "dirt"}
_BOULDER_WEAK = {"M", "h"}       # rock / stairs only decide when no floor cell touches the boulder


def boulder_for(grid, x, y, floor):
    """(metatile, ground name, flagged) for a boulder at (x, y): majority ground class of the 8 neighbours.
    flagged = the pair draws that ground with a non-General cell (e.g. Lavaridge ash), so the closest
    General boulder is used and the cell is listed for review."""
    c = Counter()
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            nx, ny = x + dx, y + dy
            if (dx or dy) and 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and grid[ny][nx] in _BOULDER_GROUND:
                c[_BOULDER_GROUND[grid[ny][nx]]] += 0.01 if grid[ny][nx] in _BOULDER_WEAK else 1
    ground = c.most_common(1)[0][0] if c else "dirt"
    key = {"grass": ".", "sand": "s", "dirt": "p"}[ground]
    fid = floor.get(key)
    flagged = fid is not None and fid >= 0x200
    if flagged:
        ground = "dirt"
    return BOULDERS[ground], ground, flagged


def override_impassable(tileset, cls, names):
    """Every metatile of `tileset` that is impassable in these maps -> cls (e.g. all of Berry Forest's
    yellow trees -> 'T')."""
    for k, c in main_coll([load_map(n) for n in names]).items():
        if k[0] == tileset and c:
            OVERRIDES[k] = cls


def colour_fracs(im):
    """Fractions of a 16x16 metatile's pixels in rough colour buckets."""
    c = Counter()
    for r, g, b in im.convert("RGB").get_flattened_data() if hasattr(im, "get_flattened_data") else im.getdata():
        if min(r, g, b) > 150 and max(r, g, b) - min(r, g, b) < 50:
            c["light"] += 1
        elif b > r + 25 and b > g + 5:
            c["blue"] += 1
        elif g > r + 12 and g > b + 8:
            c["green"] += 1
        elif r > 175 and g > 150 and b < 150 and r - b > 50:
            c["sand"] += 1
        elif r > g + 30 and r > b + 30 and r > 150 and g < 120:
            c["red"] += 1
        elif abs(r - g) < 22 and abs(g - b) < 26 and r > 150:
            c["light"] += 1
        elif abs(r - g) < 25 and abs(g - b) < 30:
            c["grey"] += 1
        elif r >= g >= b - 10 and r > b + 15:
            c["brown"] += 1
        else:
            c["other"] += 1
    return {k: v / 256.0 for k, v in c.items()}


def info(scene, mid, coll):
    a = scene.attr(mid)
    return dict(mb=MB[a & 0x1FF] if (a & 0x1FF) < len(MB) else "MB_%X" % (a & 0x1FF),
                terrain=(a >> 9) & 31, enc=(a >> 24) & 7, coll=coll, col=colour_fracs(scene.image(mid)))


def auto_class(i):
    """Heuristic class from behaviour + collision + colour. See CLASSES. Building pieces are not
    recognised here (they come in every colour): class_grid() floods impassable cells from each door
    instead, and impassable cells left over become rock 'M'."""
    mb, col, coll = i["mb"], i["col"], i["coll"]
    g = lambda k: col.get(k, 0.0)        # noqa: E731
    water_mb = mb in WATER_MB or (i["terrain"] == 2 and mb not in ("MB_POND_WATER", "MB_NORMAL"))
    if water_mb and coll:
        return "r" if g("grey") + g("light") > 0.06 else "~"
    if water_mb:
        return "~"
    if mb == "MB_POND_WATER":
        return "q"
    if mb == "MB_WATERFALL":
        return "|"
    if mb == "MB_TALL_GRASS":
        return "g"
    if mb == "MB_JUMP_SOUTH":
        return "v"
    if mb == "MB_JUMP_WEST":
        return "<"
    if mb == "MB_JUMP_EAST":
        return ">"
    if mb == "MB_ROCK_STAIRS":
        return "h"
    if mb == "MB_NON_ANIMATED_DOOR" and g("brown") + g("grey") + g("other") > 0.4 and g("light") < 0.2:
        return "c"
    if "DOOR" in mb:
        return "D"
    if mb in ("MB_SIGNPOST", "MB_POKEMON_CENTER_SIGN", "MB_POKEMART_SIGN"):
        return "n"
    if mb in ("MB_SAND", "MB_SHALLOW_WATER"):
        return "s"
    if coll == 0:                        # walkable ground (arrow warps included)
        if g("red") > 0.06 and g("green") > 0.25:
            return "f"
        if g("green") > 0.55:
            return "."
        if g("brown") > 0.35 and g("sand") < 0.3 and g("green") < 0.2:
            return "k"
        if g("sand") > 0.4:
            return "p"
        if g("blue") > 0.4:
            return "~"
        if g("brown") + g("grey") + g("light") > 0.6:
            return "p"
        return "."
    # impassable
    if g("green") > 0.5 or (g("green") + g("sand") > 0.65 and g("green") > 0.2):
        return "T"
    if g("blue") > 0.45 or g("red") > 0.12 or g("other") > 0.25:
        return "B"
    if g("brown") + g("grey") > 0.5:
        return "M"
    return "B"


_CLASS_CACHE = {}


def metatile_class(scene, mid, coll):
    k = scene.key(mid)
    if k in OVERRIDES:
        return OVERRIDES[k]
    ck = (k, coll)
    if ck not in _CLASS_CACHE:
        _CLASS_CACHE[ck] = auto_class(info(scene, mid, coll))
    return _CLASS_CACHE[ck]


def main_coll(fmaps):
    """{(tileset key, mid): most common collision in these maps}."""
    c = {}
    for fm in fmaps:
        for y in range(fm.h):
            for x in range(fm.w):
                c.setdefault(fm.scene.key(fm.mid(x, y)), Counter())[fm.coll(x, y)] += 1
    return {k: v.most_common(1)[0][0] for k, v in c.items()}


def class_grid(fm):
    """Per-cell class (list of lists of chars) with map context applied."""
    g = [[metatile_class(fm.scene, fm.mid(x, y), fm.coll(x, y)) for x in range(fm.w)] for y in range(fm.h)]
    water = set("~q")
    # bridges: walkable non-water cells with water on both sides (E-W or N-S), in a run
    for y in range(fm.h):
        for x in range(fm.w):
            if g[y][x] in ".ps" and fm.coll(x, y) == 0:
                ns = 0 < y < fm.h - 1 and g[y - 1][x] in water | {"b"} and g[y + 1][x] in water | {"b"}
                ew = 0 < x < fm.w - 1 and g[y][x - 1] in water | {"b"} and g[y][x + 1] in water | {"b"}
                if ns or ew:
                    g[y][x] = "b"
    for b in fm.json.get("bg_events", []):
        if b["type"] == "sign":
            g[b["y"]][b["x"]] = "n"
    return g


# ================================================================================================ table
def classes_png(names, path=None, only=None):
    """Review table: every FRLG metatile used by these maps at 2x, its class, and the Emerald cell drawn
    for that class (General + Rustboro scene for the representative)."""
    path = path or os.path.join(OUT, "classes.png")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fms = [load_map(n) for n in names]
    seen = {}
    for fm in fms:
        for y in range(fm.h):
            for x in range(fm.w):
                k = fm.scene.key(fm.mid(x, y))
                if k not in seen:
                    seen[k] = (fm, fm.mid(x, y))
                seen.setdefault(("n", k), Counter())[fm.coll(x, y)] += 1
    keys = sorted(k for k in seen if k[0] != "n")
    if only:
        keys = [k for k in keys if metatile_class(seen[k][0].scene, seen[k][1],
                                                  seen[("n", k)].most_common(1)[0][0]) in only]
    esc = vc.scene(("gTileset_General", "gTileset_Rustboro"))
    cols, cw, ch = 12, 118, 44
    rows = (len(keys) + cols - 1) // cols
    im = Image.new("RGB", (cols * cw, rows * ch + 30), (255, 255, 255))
    d = ImageDraw.Draw(im)
    d.text((4, 4), "FRLG metatile (2x) -> class -> Emerald cell.  * = impassable in the maps.  "
                   "Sevii 1-3 maps: " + ", ".join(names), fill=(0, 0, 0))
    table = {}
    counts = Counter()
    for n, k in enumerate(keys):
        fm, mid = seen[k]
        coll = seen[("n", k)].most_common(1)[0][0]
        cl = metatile_class(fm.scene, mid, coll)
        counts[cl] += 1
        i = info(fm.scene, mid, coll)
        table["%s:%03X" % k] = dict(cls=cl, mb=i["mb"], coll=coll, override=k in OVERRIDES)
        X, Y = (n % cols) * cw + 2, (n // cols) * ch + 30
        im.paste(fm.scene.image(mid).resize((32, 32), Image.NEAREST), (X, Y))
        rep = CLASSES[cl][1]
        if isinstance(rep, int):
            u, o = esc.metatile(rep)
            t = u.copy()
            t.alpha_composite(o)
            im.paste(t.convert("RGB").resize((32, 32), Image.NEAREST), (X + 80, Y))
        else:
            d.rectangle([X + 80, Y, X + 111, Y + 31], outline=(160, 160, 160))
            d.text((X + 82, Y + 10), str(rep)[:5], fill=(120, 120, 120))
        colr = (200, 0, 0) if cl == "x" else (0, 0, 160) if k in OVERRIDES else (0, 0, 0)
        tag = "P" if k[0] == "General_Frlg" else "".join(ch for ch in k[0] if ch.isupper() or ch.isdigit())
        d.text((X + 35, Y), "%s %03X%s" % (tag, mid, "*" if coll else ""), fill=(0, 0, 0))
        d.text((X + 35, Y + 12), "[%s]" % cl, fill=colr)
        d.text((X + 35, Y + 24), i["mb"][3:12].lower(), fill=(90, 90, 90))
    im.save(path)
    json.dump(dict(classes={c: CLASSES[c][0] for c in CLASSES}, counts=counts, table=table),
              open(path.replace(".png", ".json"), "w"), indent=1, sort_keys=True)
    return counts, len(keys)


# ================================================================================================ pairs
G = "gTileset_General"
R104 = "LAYOUT_ROUTE104@git"
LAVA_TOWN = "LAYOUT_LAVARIDGE_TOWN"
JAGGED = "LAYOUT_JAGGED_PASS@git"
SI_EXT = "LAYOUT_SOUTHERN_ISLAND_EXTERIOR"

# Building stamps: name -> (layout, sx, sy, w, h, door_dx, door_dy). General-primary ones (pstamp) work in
# every General pair; the others only in their own pair.
BUILDINGS_PRIMARY = {
    "centre": (LAVA_TOWN, 8, 3, 5, 5, 2, 4),
    "mart": (LAVA_TOWN, 14, 2, 4, 5, 1, 4),
    "house": (LAVA_TOWN, 11, 12, 4, 4, 1, 3),
}
# Per pair: which classes need pair-specific cells, which building stamps exist, and the floor / rock
# vocabularies. "rock" = (kind, vocab, training layouts) for the wall autotiler.
PAIRS = {
    "rustboro": dict(
        tileset=(G, "gTileset_Rustboro"),
        floor={"s": 0x124, "p": None, ".": 0x001, "g": 0x00D, "f": 0x004},
        bridge=((R104, 12, 51), (R104, 12, 52)),          # Route 104 pier planks: upper row, lower row
        stairs=(0x0AF, 0x0CF),
        cave=("LAYOUT_ROUTE116@git", 47, 7, 1, 2, 0, 1),   # General-primary cave mouth 09F over 0A7
        harbor=(SI_EXT, 10, 21, 9, 4),                     # Southern Island's ferry dock (S.S. Tidal berth)
        buildings=dict(BUILDINGS_PRIMARY, cottage=(R104, 15, 47, 5, 4, 2, 3),
                       flowershop=(R104, 3, 15, 7, 4, 3, 3)),
    ),
    "lavaridge": dict(
        tileset=(G, "gTileset_Lavaridge"),
        floor={"s": 0x271, "p": 0x271, ".": 0x001, "g": 0x00D, "f": 0x004},
        bridge=None,
        stairs=(0x2AE, 0x2AF),
        cave=(JAGGED, 16, 17, 1, 2, 0, 1),               # 256 over 25E, door on the lower cell
        lava_rock=False,                                 # Lavaridge cliffs are thin terrace lines; FRLG walls read better as the General rock massif
        buildings=dict(BUILDINGS_PRIMARY),
    ),
    "dewford": dict(tileset=(G, "gTileset_Dewford"), floor={"s": 0x124, "p": None, ".": 0x001, "g": 0x00D,
                                                            "f": 0x004},
                    bridge=None, stairs=(0x0AF, 0x0CF), cave=None,
                    buildings=dict(BUILDINGS_PRIMARY, hall=("LAYOUT_DEWFORD_TOWN", 1, 0, 5, 4, 2, 3),
                                   dhouse=("LAYOUT_DEWFORD_TOWN", 16, 11, 4, 4, 1, 3))),
    "fortree": dict(tileset=(G, "gTileset_Fortree"), floor={"s": 0x124, "p": None, ".": 0x001, "g": 0x00D,
                                                            "f": 0x004},
                    bridge=(("LAYOUT_ROUTE119@git", 22, 84), ("LAYOUT_ROUTE119@git", 22, 85)),
                    stairs=(0x0AF, 0x0CF), cave=None, buildings=dict(BUILDINGS_PRIMARY)),
}
# PROPOSED gTileset_SeviiIslands = a Sevii-only copy of Rustboro + additions (sevii_tileset.py): same ids, plus
# cottage variants, market stall, Onix tails, Rocket Warehouse, arrow-warp duplicates (virtual: vstamps / vcells)
PAIRS["sevii"] = dict(PAIRS["rustboro"], tileset=(G, "gTileset_SeviiIslands"), virtual="sevii_tileset",
                      cottage_variants=("cottage", "cottage_v1", "cottage_v2", "cottage_v3"))
# Tanoby Ruins on Tiksi's gTileset_TanobyDelta (FRLG chamber facade already ported by port_tanoby.py; used
# as-is, no edits). Everything else in that pair is General primary; each chamber = Tanoby Delta's 5x5 facade
# + rock-mound chunk (x7-11, y13-17, door at +2,+4) stamped with its door on FRLG's warp cell.
PAIRS["tanoby"] = dict(tileset=(G, "gTileset_TanobyDelta"),
                       floor={"s": 0x124, "p": None, ".": 0x001, "g": 0x00D, "f": 0x004},
                       bridge=None, stairs=(0x0AF, 0x0CF), cave=None,
                       buildings=dict(BUILDINGS_PRIMARY, chamber=("LAYOUT_TANOBY_DELTA", 7, 13, 5, 5, 2, 4)))
DEFAULT_PAIR = "rustboro"

# vocabularies (General primary)
RIM = [0x002, 0x073, 0x075, 0x07B, 0x07C, 0x07D, 0x089, 0x074, 0x07A, 0x0A9, 0x079]
SEA_EDGE = [0x170, 0x180, 0x181, 0x189, 0x190, 0x192, 0x198, 0x19A, 0x15A, 0x15B, 0x171, 0x172, 0x174]
SHORE = [0x170, 0x11B, 0x11C, 0x11D, 0x123, 0x125, 0x12B, 0x12C, 0x12D, 0x13D, 0x13E, 0x145, 0x146, 0x124]
POND = [0x0A1, 0x0B0, 0x0B1, 0x0B2, 0x0B3, 0x0B8, 0x0B9, 0x0BA, 0x0BB, 0x0C0, 0x0C2, 0x0C3, 0x0C4]
FOREST = [0x0C6, 0x0C7, 0x016, 0x017, 0x00E, 0x00F]
FENCE = [0x149, 0x14A, 0x14B, 0x14C, 0x14D]
LEDGES = {"v": [0x0D5, 0x087, 0x0D6, 0x08F], "<": [0x085, 0x095, 0x0FE, 0x106], ">": [0x086, 0x096, 0x0FF, 0x107]}
RIM_TRAIN = [SI_EXT, "LAYOUT_FARAWAY_ISLAND_ENTRANCE"]
SHORE_TRAIN = [R104, "LAYOUT_DEWFORD_TOWN@git", "LAYOUT_ROUTE105", "LAYOUT_ROUTE107"]
ROCK_TRAIN = [SI_EXT, "LAYOUT_FARAWAY_ISLAND_ENTRANCE", "LAYOUT_ROUTE120", R104]
POND_TRAIN = ["LAYOUT_ROUTE120@git", R104, "LAYOUT_ROUTE119@git"]
# Lavaridge cliffs: impassable secondary cells of Jagged Pass / Mt. Chimney / Route 112 that are not trees
LAVA_TREES = set(range(0x2B0, 0x2E0)) | {0x2E2, 0x2E3}
LAVA_TRAIN = [JAGGED, "LAYOUT_MT_CHIMNEY@git", "LAYOUT_ROUTE112@git"]


def lava_rock_ids():
    out = set()
    for lid in LAVA_TRAIN:
        for row in vc.raw_layout(lid)[1]:
            for v in row:
                m = v & 0x3FF
                if (v >> 10) & 3 and 0x200 <= m and m not in LAVA_TREES and m not in (0x25E, 0x256):
                    out.add(m)
    return sorted(out)


# ================================================================================================ GFX swap
def frlg_only_gfx():
    """OBJ_EVENT_GFX_* names inside the IS_FRLG block (invisible in an Emerald build)."""
    src = open(os.path.join(ROOT, "src", "data", "object_events", "object_event_graphics_info_pointers.h")).read()
    out, on = set(), False
    for line in src.splitlines():
        if line.strip().startswith("#if IS_FRLG"):
            on = True
        elif line.strip().startswith("#endif") and on:
            on = False
        elif on:
            m = re.search(r"\[(OBJ_EVENT_GFX_\w+)\]", line)
            if m:
                out.add(m.group(1))
    return out


# FRLG-only gfx -> Emerald look-alike (OBJ_EVENT_GFX_ name, mockup sprite key)
GFX_SWAP = {
    "SWIMMER_F_WATER": ("SWIMMER_F", "swimmer"), "SWIMMER_M_WATER": ("SWIMMER_M", "swimmer"),
    "SWIMMER_F_LAND": ("SWIMMER_F", "swimmer"), "SWIMMER_M_LAND": ("SWIMMER_M", "swimmer"),
    "CAMPER_FRLG": ("CAMPER", "camper"), "PICNICKER_FRLG": ("PICNICKER", "picnicker"),
    "HIKER_FRLG": ("HIKER", "hiker"), "BATTLE_GIRL": ("BLACK_BELT", "expert"), "BLACKBELT": ("BLACK_BELT", "expert"),
    "BREAKABLE_ROCK_FRLG": ("BREAKABLE_ROCK", None), "PUSHABLE_BOULDER_FRLG": ("PUSHABLE_BOULDER", None),
    "CUTTABLE_TREE_FRLG": ("CUTTABLE_TREE", None), "WOMAN_1_FRLG": ("WOMAN_2", "woman"),
    "WOMAN_2_FRLG": ("WOMAN_2", "woman"), "WOMAN_3_FRLG": ("WOMAN_5", "woman"), "BEAUTY_FRLG": ("BEAUTY", "beauty"),
    "SAILOR_FRLG": ("SAILOR", "sailor"), "LITTLE_BOY_FRLG": ("LITTLE_BOY", "son"),
    "LITTLE_GIRL_FRLG": ("LITTLE_GIRL", "lass"), "TUBER_F_FRLG": ("TUBER_F", "swimmer"),
    "FISHER": ("FISHERMAN", "fisherman"), "BILL": ("SCIENTIST_1", "man"), "OLD_MAN_1": ("OLD_MAN", "old_man"),
    "BALDING_MAN": ("MAN_3", "man"), "CLERK": ("MART_EMPLOYEE", "man"), "SUPER_NERD": ("MANIAC", "man"),
    "BOY": ("BOY_1", "boy"), "MAN": ("MAN_3", "man"), "BIKER": ("CYCLING_TRIATHLETE_M", "man"),
    "ROCKET_M": ("ROCKET_M", "man"), "MOLTRES": ("SPECIES(MOLTRES)", None), "DODUO": ("SPECIES(DODUO)", None),
}


# field-move objects -> mockup sprite key (voyage_compose.SPRITES)
FIELD_OBJECTS = {"BREAKABLE_ROCK": "breakable_rock", "PUSHABLE_BOULDER": "pushable_boulder",
                 "CUTTABLE_TREE": "cuttable_tree"}


def swap_gfx(gid):
    g = gid.replace("OBJ_EVENT_GFX_", "")
    if g in GFX_SWAP:
        return GFX_SWAP[g]
    return (g, "man")


# ================================================================================================ translate
def _components(grid, cells, ok):
    """4-connected flood from cells over grid cells where ok(char)."""
    h, w = len(grid), len(grid[0])
    seen, q = set(), deque(cells)
    while q:
        x, y = q.popleft()
        if (x, y) in seen or not (0 <= x < w and 0 <= y < h) or not ok(grid[y][x]):
            continue
        seen.add((x, y))
        q.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
    return seen


def _building_cells(fm, grid, x0, y0, rx=6, up=7, doors=()):
    """Building footprint for a door at (x0, y0): 4-connected impassable cells (plus the door) reached
    from the cell above the door, inside x0-rx..x0+rx, y0-up..y0, skipping trees, sea and primary-tileset
    rock (cliffs next to buildings stay cliffs)."""
    lo, hi = x0 - rx, x0 + rx               # split the box half-way to other doors on nearby rows
    for dx_, dy_ in doors:
        if (dx_, dy_) != (x0, y0) and abs(dy_ - y0) <= 3:
            if dx_ < x0:
                lo = max(lo, (dx_ + x0) // 2 + 1)
            elif dx_ > x0:
                hi = min(hi, (dx_ + x0 - 1) // 2)
    out, q = set(), deque([(x0, y0), (x0, y0 - 1)])
    while q:
        x, y = q.popleft()
        if (x, y) in out or not (0 <= x < fm.w and 0 <= y < fm.h) or not lo <= x <= hi or not (y0 - up <= y <= y0):
            continue
        c = grid[y][x]
        door = (x, y) == (x0, y0) or c == "D"
        prim_rock = c == "M" and fm.mid(x, y) < 640
        if not door and (fm.coll(x, y) == 0 or c in "T~qrwF" or prim_rock):
            continue
        out.add((x, y))
        q.extend([(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)])
    return out


def _flood(fm, grid, starts, x0, x1, y0, y1, ok):
    out, q = set(), deque(starts)
    while q:
        x, y = q.popleft()
        if (x, y) in out or not (0 <= x < fm.w and 0 <= y < fm.h) or not (x0 <= x <= x1 and y0 <= y <= y1):
            continue
        if not ok(x, y):
            continue
        out.add((x, y))
        q.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
    return out


def _ground_of(grid, cells):
    """Most common walkable ground class around a set of cells."""
    c = Counter()
    for x, y in cells:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if (nx, ny) not in cells and 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and grid[ny][nx] in ".spgf":
                c[grid[ny][nx]] += 1
    return c.most_common(1)[0][0] if c else "."


def choose_building(dest, fw, pair):
    d = dest.upper()
    b = PAIRS[pair]["buildings"]
    if "POKEMON_CENTER" in d:
        return "centre"
    if "MART" in d:
        return "mart"
    if fw >= 7 and "flowershop" in b:
        return "flowershop"
    if fw >= 5 and "cottage" in b:
        return "cottage"
    if fw >= 5 and "hall" in b:
        return "hall"
    return "house"


def translate(fm, pair=DEFAULT_PAIR, building_choice=None, label=None, vstamps=None):
    """FrlgMap -> voyage_compose spec (same size), plus fm.report (dict) of what was done.
    building_choice: {warp index: building name} to force a stamp (a name of the virtual tileset's STAMPS
    works on a virtual pair). vstamps: [(STAMPS name, x, y)] extra virtual stamps (footprint cleared to ground)."""
    cfg = PAIRS[pair]
    ts = cfg["tileset"]
    grid = class_grid(fm)
    W, H = fm.w, fm.h
    report = dict(map=fm.name, size=(W, H), pair=ts, unresolved=[], buildings=[], caves=[])
    stamps, pstamps, cells, marks = [], [], [], []
    building_choice = building_choice or {}
    vmod = vc.virtual(ts[1]) if cfg.get("virtual") else None
    vst, vcells, arrows = [], [], []
    n_cottage = sum(ord(c) for c in fm.name)          # variant rotation differs per map, stable across runs
    for name, vx, vy in vstamps or []:
        rows = vmod.STAMPS[name]["cells"]
        gnd = _ground_of(grid, {(vx + i, vy + j) for j in range(len(rows)) for i in range(len(rows[0]))})
        for j in range(len(rows)):
            for i in range(len(rows[0])):
                grid[vy + j][vx + i] = gnd
        vst.append((name, vx, vy))
        report.setdefault("vstamps", []).append((name, vx, vy))
    # FRLG arrow warps (harbour boardwalks, forest exits ...): kept as arrow warps on a duplicate metatile
    for wv in fm.json.get("warp_events", []):
        b = MB[fm.scene.attr(fm.mid(wv["x"], wv["y"])) & 0x1FF]
        if b.endswith("_ARROW_WARP"):
            arrows.append((wv["x"], wv["y"], b.split("_")[1][0]))

    # ---- buildings and caves from warps
    for wi, wv in enumerate(fm.json.get("warp_events", [])):
        x, y, dest = wv["x"], wv["y"], wv["dest_map"]
        cl = grid[y][x]
        lbl = dest.replace("MAP_", "").replace(snake(fm.name).upper() + "_", "")[:14].lower()
        if "HARBOR" in dest and cl != "D":
            # FRLG Seagallop harbour: a south arrow warp at the end of a boardwalk, the harbour building
            # below it standing in the sea. -> clear that building to sea and put the pair's ferry dock there
            comp = _flood(fm, grid, [(x, y + 1)], x - 5, x + 5, y + 1, y + 8,
                          lambda cx, cy: fm.coll(cx, cy) or grid[cy][cx] in "kB")
            for cx, cy in comp:
                grid[cy][cx] = "~"
            if cfg.get("harbor"):
                lid, sx, sy, bw, bh = cfg["harbor"]
                e_ = vc.raw_layout(lid)[0]
                same = (e_["primary_tileset"], e_["secondary_tileset"]) == vc.real_pair(ts)
                (stamps if same else pstamps).append((lid, sx, sy, bw, bh, x - bw // 2, y + 1))
            report["buildings"].append(dict(warp=(x, y), dest=dest, footprint=len(comp), stamp="harbor dock"))
            marks.append((x, y, "harbor", "warp"))
            continue
        if cl == "D" or wi in building_choice:
            comp = _building_cells(fm, grid, x, y, doors=[(w_["x"], w_["y"]) for w_ in fm.json["warp_events"]])
            if not comp:
                marks.append((x, y, lbl, "warp"))
                continue
            xs = [c[0] for c in comp]
            ys = [c[1] for c in comp]
            fw = max(xs) - min(xs) + 1
            name = building_choice.get(wi) or choose_building(dest, fw, pair)
            if vmod and name == "cottage" and cfg.get("cottage_variants"):
                name = cfg["cottage_variants"][n_cottage % len(cfg["cottage_variants"])]
                n_cottage += 1
            if vmod and name in vmod.STAMPS:
                vrows = vmod.STAMPS[name]["cells"]
                lid, sx, sy, bw, bh = None, 0, 0, len(vrows[0]), len(vrows)
                ddx, ddy = vmod.STAMPS[name]["door"]
            else:
                lid, sx, sy, bw, bh, ddx, ddy = cfg["buildings"][name]
            gnd = _ground_of(grid, comp)
            # building pieces that the door split left beside this footprint belong to a building too
            extra = _components(grid, [(cx + dx_, cy) for cx, cy in comp for dx_ in (-1, 1)],
                                lambda c: c == "B")
            for cx, cy in comp | extra:
                grid[cy][cx] = gnd
            dx, dy = x - ddx, y - ddy
            ch = (lid, sx, sy, bw, bh, dx, dy)
            if lid is None:
                vst.append((name, dx, dy))
            else:
                (pstamps if name in BUILDINGS_PRIMARY else stamps).append(ch)
            for j in range(bh):                         # don't let the autotilers see the stamp area as rock
                for i in range(bw):
                    if 0 <= dx + i < W and 0 <= dy + j < H and grid[dy + j][dx + i] in "BDMTx":
                        grid[dy + j][dx + i] = gnd
            report["buildings"].append(dict(warp=(x, y), dest=dest, footprint=(min(xs), min(ys), fw,
                                                                               max(ys) - min(ys) + 1),
                                            stamp=name, at=(dx, dy, bw, bh)))
            marks.append((x, y, lbl, "warp"))
        else:
            marks.append((x, y, lbl, "warp"))
            if cl in "Mc" and cfg.get("cave"):
                lid, sx, sy, bw, bh, ddx, ddy = cfg["cave"]
                e_ = vc.raw_layout(lid)[0]
                same = (e_["primary_tileset"], e_["secondary_tileset"]) == vc.real_pair(ts)
                (stamps if same else pstamps).append((lid, sx, sy, bw, bh, x - ddx, y - ddy))
                for j in range(bh):
                    grid[y - ddy + j][x - ddx] = "M"        # rock around it stays continuous
                report["caves"].append((x, y, dest))
    # leftover building-looking cells not part of any door's building: impassable scenery -> rock;
    # a door cell with no building -> ground
    for y in range(H):
        for x in range(W):
            if grid[y][x] == "B":
                grid[y][x] = "M"
            elif grid[y][x] == "D":
                grid[y][x] = _ground_of(grid, {(x, y)})

    # ---- sea rocks: FRLG 1x1 rocks -> Emerald 2x2 Route 104 rocks where 4 sea cells fit
    covered, anchors = set(), []
    for _l, _sx, _sy, bw, bh, dx, dy in stamps + pstamps:     # never over a stamped building / chamber / dock
        covered.update((dx + i, dy + j) for i in range(bw) for j in range(bh))
    for y in range(H):
        for x in range(W):
            if grid[y][x] != "r" or (x, y) in covered:
                continue
            if any(abs(ax_ - x) <= 2 and abs(ay_ - y) <= 2 for ax_, ay_ in anchors):
                report.setdefault("rocks_merged", []).append((x, y))      # 2x2 rocks: keep them apart
                continue
            for ax, ay in ((x, y), (x - 1, y), (x, y - 1), (x - 1, y - 1)):
                cs = [(ax + i, ay + j) for i in (0, 1) for j in (0, 1)]
                if all(0 <= cx < W and 0 <= cy < H and grid[cy][cx] in "~r" and (cx, cy) not in covered
                       for cx, cy in cs):
                    pstamps.append((R104, 7, 48, 2, 2, ax, ay))
                    covered.update(cs)
                    anchors.append((ax, ay))
                    break
            else:
                report.setdefault("rocks_dropped", []).append((x, y))
    for y in range(H):
        for x in range(W):
            if grid[y][x] == "r":
                grid[y][x] = "~"
    # ---- freestanding boulders: Emerald's fixed boulder for the surrounding ground
    boulder_cells = []
    for y in range(H):
        for x in range(W):
            if grid[y][x] == "o":
                bid, gname, flagged = boulder_for(grid, x, y, cfg["floor"])
                boulder_cells.append((x, y, ("id", bid)))
                report.setdefault("boulders", []).append((x, y, "%03X" % bid, gname + (" (flag)" if flagged else "")))
    # ---- waterfalls: Emerald's General-primary waterfall as drawn on Route 119 (x17-19, y25-29): lip row
    # 0BB 0B3.. 0BC, body 0B9, splash 02C 034.. 03C on the first water row below; the pools it joins
    # become sea-type water (as Route 119's river) so their colour matches the falls
    falls_post = []
    fcells = {(x, y) for y in range(H) for x in range(W) if grid[y][x] == "|"}
    while fcells:
        comp = _components(grid, [next(iter(fcells))], lambda c: c == "|")
        fcells -= comp
        xs, ys = [c[0] for c in comp], [c[1] for c in comp]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        row = lambda l, m, r: [(x, l if x == x0 else r if x == x1 else m) for x in range(x0, x1 + 1)]   # noqa: E731
        falls_post += [(x, y0, ("id", m)) for x, m in row(0x0BB, 0x0B3, 0x0BC)]
        falls_post += [(x, y, ("id", 0x0B9)) for y in range(y0 + 1, y1 + 1) for x in range(x0, x1 + 1)]
        pools = _components(grid, [(x, y) for x in range(x0, x1 + 1) for y in (y0 - 1, y1 + 1)],
                            lambda c: c in "q~")
        for cx, cy in pools:
            grid[cy][cx] = "~"
        if y1 + 1 < H and all(grid[y1 + 1][x] == "~" for x in range(x0, x1 + 1)):
            falls_post += [(x, y1 + 1, ("id", m)) for x, m in row(0x02C, 0x034, 0x03C)]
        report.setdefault("waterfalls", []).append((x0, y0, x1, y1))
    # ---- a pair with no bridge art: FRLG's "bridge" cells (walkable between water: sand spits, corners) -> sand
    if not cfg.get("bridge"):
        for y in range(H):
            for x in range(W):
                if grid[y][x] == "b":
                    grid[y][x] = "s"
    # ---- mask chars for the autotilers
    mask = ["".join(r) for r in grid]
    # sea coasts: sand -> beach shore, other land -> rock rim; ponds: pond banks
    land_rim = ".gfpThvn<>Fodc"
    mk = vc.ring_multi(mask, [("s", "S", "w"), (land_rim, "R", "W"), ("M", "K", "W")], sea_chars="~")
    mk = vc.ring_multi(mk, [(".gfpsTM", "L", "Q")], sea_chars="q")
    fl = cfg["floor"]
    legend = {"~": ("id", 0x170, 0, 1), "q": ("id", 0x0A1, 0, 1), "|": ("id", 0x0B9),
              ".": ("id", fl["."]), "g": ("id", fl["g"]), "f": ("id", fl["f"]), "s": ("id", fl["s"]),
              "S": ("id", fl["s"]), "L": ("id", fl["."]), "p": ("id", fl["p"] or fl["."]),
              "T": ("id", fl["."]), "n": ("id", 0x003), "o": ("id", 0x0E2), "d": ("id", 0x0E2),
              "k": ("id", 0x170, 0, 1), "c": ("id", fl["s"]), "x": ("id", fl["."]), "b": ("id", 0x170, 0, 1),
              "h": ("id", fl["."]), "v": ("id", fl["."]), "<": ("id", fl["."]), ">": ("id", fl["."]),
              "F": ("id", fl["."]), "M": ("id", fl["s"]), "K": ("id", fl["s"])}
    edges = [dict(kind="shore", chars="Sw", water_chars="~Wwbkq|", vocab=SHORE, layouts=SHORE_TRAIN),
             dict(chars="RW", water_chars="~Wwbk|", vocab=RIM + SEA_EDGE, layouts=RIM_TRAIN),
             dict(chars="K", water_chars="~Wwbk|", vocab=[m for m in RIM if m != 0x002], layouts=RIM_TRAIN),
             dict(chars="LQ", water_chars="qQ", vocab=POND + [0x001, 0x002], layouts=POND_TRAIN)]
    if cfg.get("lava_rock"):
        edges.append(dict(kind="lava", chars="M", water_chars="M", vocab=lava_rock_ids(), layouts=LAVA_TRAIN))
    else:
        edges.append(dict(kind="rock", chars="M", water_chars="M", vocab=sorted(vc.ROCK_IDS), layouts=ROCK_TRAIN))

    # ---- discrete cells
    auto = []
    for y in range(H):
        for x in range(W):
            c = grid[y][x]
            if c in LEDGES:
                auto.append((x, y, LEDGES[c]))
            elif c == "F":
                auto.append((x, y, FENCE))
            elif c == "h":
                run_l = x > 0 and grid[y][x - 1] == "h"
                cells.append((x, y, ("id", cfg["stairs"][1 if run_l else 0])))
            elif c in "bk":
                if cfg.get("bridge"):
                    up = y > 0 and grid[y - 1][x] in "bk"
                    cells.append((x, y, cfg["bridge"][1 if up else 0]))
                else:
                    cells.append((x, y, ("id", 0x05E)))
            elif c == "x":
                report["unresolved"].append((x, y, "%03X" % fm.mid(x, y)))
    p_cells = []
    if fl["p"] is None:     # dirt road 9-slice from the path class
        DIRT = {"TL": 0x118, "T": 0x119, "TR": 0x11A, "L": 0x120, "C": 0x121, "R": 0x122, "BL": 0x128,
                "B": 0x129, "BR": 0x12A}
        pe = lambda x, y: not (0 <= x < W and 0 <= y < H) or grid[y][x] in "pnhbD"   # noqa: E731
        for y in range(H):
            for x in range(W):
                if grid[y][x] == "p":
                    k = ("T" if not pe(x, y - 1) else "B" if not pe(x, y + 1) else "") + \
                        ("L" if not pe(x - 1, y) else "R" if not pe(x + 1, y) else "")
                    p_cells.append((x, y, ("id", DIRT[k or "C"])))

    # ---- nothing drawn by cells / auto / tree fill may land on a stamped building
    under = set()
    for name, vx, vy in vst:
        rows = vmod.STAMPS[name]["cells"]
        under.update((vx + i, vy + j) for j in range(len(rows)) for i in range(len(rows[0])))
    if vmod:                                            # FRLG art ported cell by cell (Onix tails ...)
        vcells += [(x, y, v) for (m, x, y), v in getattr(vmod, "PORTED_CELLS", {}).items() if m == fm.name]
        report["ported_cells"] = len(vcells)
    for _l, _sx, _sy, bw, bh, dx, dy in stamps + [p_ for p_ in pstamps if p_[0] != R104]:
        under.update((dx + i, dy + j) for i in range(bw) for j in range(bh))
    cells = [c for c in cells + boulder_cells if (c[0], c[1]) not in under]
    p_cells = [c for c in p_cells if (c[0], c[1]) not in under]
    auto = [a for a in auto if (a[0], a[1]) not in under]
    # ---- trees: 2x2 where they fit, the rest 1-wide forest
    spec = dict(name=label or fm.name, size=(W, H), tileset=ts, ground=("id", 0x170, 0, 1),
                mask=mk, mask_legend=legend, edges_list=edges, big_trees="T",
                stamps=stamps, pstamps=pstamps, cells=p_cells + cells, auto=auto, marks=marks,
                post=falls_post)
    spec["vstamps"], spec["vcells"], spec["arrow_warps"] = vst, vcells, arrows
    report["arrow_warps"] = arrows
    adir = {(x, y): d for x, y, d in arrows}
    for i, m in enumerate(marks):
        if m[3] == "warp" and (m[0], m[1]) in adir:
            marks[i] = (m[0], m[1], m[2] + " (arrow %s)" % adir[(m[0], m[1])]) + tuple(m[3:])
    spec["_tree_fill"] = [(x, y) for y in range(H) for x in range(W) if grid[y][x] == "T" and (x, y) not in under]
    # ---- events
    for o in fm.json.get("object_events", []):
        gid, spr = swap_gfx(o.get("graphics_id", ""))
        kind = "item" if "ITEM_BALL" in gid else "npc"
        if gid.startswith("SPECIES"):
            marks.append((o["x"], o["y"], gid[8:-1].title(), "spot"))
        elif spr is None and gid in FIELD_OBJECTS:
            marks.append((o["x"], o["y"], "", "field", FIELD_OBJECTS[gid]))
        elif spr is None:
            marks.append((o["x"], o["y"], gid[:6].lower(), "note"))
        else:
            marks.append((o["x"], o["y"], "", kind, "item" if kind == "item" else spr))
    for b in fm.json.get("bg_events", []):
        if b["type"] == "sign":
            marks.append((b["x"], b["y"], "", "sign"))
        elif b["type"] == "hidden_item":
            marks.append((b["x"], b["y"], "h", "note"))
    for c in fm.json.get("connections") or []:
        marks.append(_conn_mark(c, W, H))
    report["connections"] = [(c["direction"], c["offset"], c["map"]) for c in fm.json.get("connections") or []]
    report["warps"] = [(w["x"], w["y"], w["dest_map"]) for w in fm.json.get("warp_events", [])]
    spec["object_events"] = [dict(graphics_id="OBJ_EVENT_GFX_" + swap_gfx(o.get("graphics_id", ""))[0],
                                  x=o["x"], y=o["y"],
                                  script="EventScript_RockSmash" if "BREAKABLE_ROCK" in o.get("graphics_id", "")
                                  else o.get("script"))
                             for o in fm.json.get("object_events", [])]
    report["objects"] = [(o["x"], o["y"], o.get("graphics_id"), swap_gfx(o.get("graphics_id", ""))[0])
                         for o in fm.json.get("object_events", [])]
    report["classes"] = Counter(c for r in grid for c in r)
    fm.report = report
    fm.grid = grid
    return spec


def _conn_mark(c, W, H):
    """Label inside the stretch of edge the neighbour actually covers (offset = its position along it)."""
    m = c["map"].replace("MAP_", "").title().replace("_", " ")
    d, o = c["direction"], c["offset"]
    if d in ("up", "down"):
        return (min(W - 6, max(0, o) + 1), 0 if d == "up" else H - 1, ("^ " if d == "up" else "v ") + m, "conn")
    y = min(H - 1, max(0, o) + 2)
    return (0, y, "< " + m, "conn") if d == "left" else (max(0, W - 9), y, m + " >", "conn")


# ---------------------------------------------------------------------------- build with the extra passes
_LAVA_SET = set()


def build(spec):
    """vc.build plus: 1-wide forest for tree cells big_trees could not fill; Lavaridge rock learner."""
    global _LAVA_SET
    edges = spec.get("edges_list", [])
    lava = [e for e in edges if e.get("kind") == "lava"]
    if lava:
        _LAVA_SET = set(lava[0]["vocab"])
        for e in lava:
            e["kind"] = "rock"
        vc_is_rock = vc.is_rock
        vc.is_rock = lambda m, t: m in _LAVA_SET          # used by learn_edges for kind="rock"
        try:
            g = vc.build(spec)
        finally:
            vc.is_rock = vc_is_rock
            for e in lava:
                e["kind"] = "lava"
    else:
        g = vc.build(spec)
    ts = vc.real_pair(spec["tileset"])
    big = {vc.ref_value(("id", m), ts) & 0x3FF for m in vc.TREES_GENERAL[:6]}
    rest = {(x, y): FOREST for x, y in spec.get("_tree_fill", []) if g[y][x] & 0x3FF not in big}
    if rest:
        vc.solve(g, rest, ts)
    mod = vc.virtual(spec["tileset"][1])
    if mod and hasattr(mod, "arrow"):                   # arrow-warp duplicate of whatever is drawn there
        for x, y, d in spec.get("arrow_warps", []):
            g[y][x] = mod.arrow(g[y][x], d)
    return g


def render(spec, out_base):
    g = build(spec)
    ts = tuple(spec["tileset"])
    os.makedirs(os.path.dirname(out_base), exist_ok=True)
    marks = spec.get("marks", [])
    vc.picture(g, ts, marks, 1).convert("RGB").save(out_base + ".png")
    vc.picture(g, ts, marks, 2).convert("RGB").save(out_base + "@2x.png")
    return g


def side_by_side(fm, out_base, scale=1, zoom=None):
    """<out_base>_vs_frlg.png: FRLG original (left) | translation (right), same scale, with a label bar.
    zoom=(x0, y0, x1, y1) in map cells adds a 3x crop of that region of both underneath."""
    a = fm.picture(scale)
    b = Image.open(out_base + (".png" if scale == 1 else "@2x.png")).convert("RGB")
    if zoom:
        x0, y0, x1, y1 = zoom
        box = tuple(v * 16 * scale for v in (x0, y0, x1 + 1, y1 + 1))
        za = a.crop(box).resize(((x1 - x0 + 1) * 48, (y1 - y0 + 1) * 48), Image.NEAREST)
        zb = b.crop(box).resize(za.size, Image.NEAREST)
        top = side_by_side_pair(a, b, fm)
        im = Image.new("RGB", (max(top.width, za.width * 2 + 12), top.height + za.height + 18), (255, 255, 255))
        im.paste(top, (0, 0))
        im.paste(za, (0, top.height + 18))
        im.paste(zb, (za.width + 12, top.height + 18))
        ImageDraw.Draw(im).text((2, top.height + 3), "3x crop, cells (%d,%d)-(%d,%d): FRLG | Emerald" % zoom,
                                fill=(0, 0, 0))
        im.save(out_base + "_vs_frlg.png")
        return
    side_by_side_pair(a, b, fm).save(out_base + "_vs_frlg.png")


def side_by_side_pair(a, b, fm):
    im = Image.new("RGB", (a.width + b.width + 12, max(a.height, b.height) + 16), (255, 255, 255))
    im.paste(a, (0, 16))
    im.paste(b, (a.width + 12, 16))
    d = ImageDraw.Draw(im)
    d.text((2, 2), "FRLG %s (%dx%d)" % (fm.name, fm.w, fm.h), fill=(0, 0, 0))
    d.text((a.width + 14, 2), "Emerald %s/%s" % tuple(t[9:] for t in fm.report["pair"]), fill=(0, 0, 0))
    return im


def write_spec(spec, fm, path):
    keep = {k: v for k, v in spec.items() if not k.startswith("_") and k not in ("mask_legend", "edges_list")}
    keep["report"] = {k: (dict(v) if isinstance(v, Counter) else v) for k, v in fm.report.items()}
    json.dump(keep, open(path, "w"), indent=0, default=str)


def run(names, pairs=None, out=None):
    out = out or OUT
    pairs = pairs or {}
    res = {}
    for n in names:
        fm = load_map(n)
        spec = translate(fm, pairs.get(n, DEFAULT_PAIR))
        base = os.path.join(out, snake(n))
        g = render(spec, base)
        side_by_side(fm, base)
        write_spec(spec, fm, base + "_spec.json")
        res[n] = (fm, spec, g)
        print("%-26s %3dx%-3d %-10s unresolved=%d buildings=%d" % (n, fm.w, fm.h, pairs.get(n, DEFAULT_PAIR),
                                                                   len(fm.report["unresolved"]),
                                                                   len(fm.report["buildings"])))
    return res


def snake(n):
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", n).lower()


if __name__ == "__main__":
    args = sys.argv[1:]
    outdir = None
    if "--out" in args:
        i = args.index("--out")
        outdir = args[i + 1]
        del args[i:i + 2]
    if args and args[0] == "export":            # real map data for implementation (export_maps.py)
        import export_maps
        export_maps.main(args[1:] + (["--out", outdir] if outdir else []))
        sys.exit(0)
    if args and args[0] == "classes":
        only = None
        if "--only" in args:
            i = args.index("--only")
            only = args[i + 1]
            del args[i:i + 2]
        print(classes_png(args[1:], os.path.join(OUT, "classes_%s.png" % "".join("%02X" % ord(c) for c in only))
                          if only else None, only))
    else:
        names, pairs = [], {}
        for a in args:
            n, _, p = a.partition(":")
            names.append(n)
            if p:
                pairs[n] = p
        run(names, pairs, outdir)
