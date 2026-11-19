"""Shared helpers for the v2 Centre / Mart exteriors (5x5 Centre, 4x5 Mart + signpost)."""
import glob
import json
import os
import re
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
GEN = os.path.join(ROOT, "data", "tilesets", "primary", "general")

OLD_CENTRE_DOOR, OLD_MART_DOOR = 0x059, 0x041


def layouts():
    js = json.load(open(os.path.join(ROOT, "data", "layouts", "layouts.json")))
    return {e["id"]: e for e in js["layouts"] if "id" in e}


def maps():
    out = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "data", "maps", "*", "map.json"))):
        js = json.load(open(p))
        out[js["id"]] = (p, js)
    return out


def read_grid(e):
    w, h = e["width"], e["height"]
    raw = open(os.path.join(ROOT, e["blockdata_filepath"]), "rb").read()
    if len(raw) != w * h * 2:
        return None
    b = struct.unpack(f"<{w * h}H", raw)
    return [[b[y * w + x] for x in range(w)] for y in range(h)]


def write_grid(e, g):
    with open(os.path.join(ROOT, e["blockdata_filepath"]), "wb") as f:
        f.write(struct.pack(f"<{e['width'] * e['height']}H", *[c for row in g for c in row]))


def behaviours():
    text = open(os.path.join(ROOT, "include", "constants", "metatile_behaviors.h")).read()
    names = re.findall(r"^\s*(MB_\w+)\s*,", text[text.index("enum"):], re.M)
    return {n: i for i, n in enumerate(names)}


def tileset_dir(sym):
    H = open(os.path.join(ROOT, "src", "data", "tilesets", "headers.h")).read()
    M = open(os.path.join(ROOT, "src", "data", "tilesets", "metatiles.h")).read()
    m = re.search(r"const struct Tileset " + sym + r"\s*=\s*\{(.*?)\};", H, re.S)
    ms = re.search(r"\.metatiles\s*=\s*(\w+)", m.group(1)).group(1)
    p = re.search(ms + r'\[\]\s*=\s*INCBIN_U16\("([^"]+)"\)', M).group(1)
    return os.path.join(ROOT, os.path.dirname(p))


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


_sets = {}


def tset(sym):
    if sym not in _sets:
        _sets[sym] = Set(GEN if sym == "gTileset_General" else tileset_dir(sym))
    return _sets[sym]


def attr_of(e, mid):
    s = tset("gTileset_General") if mid < 0x200 else tset(e["secondary_tileset"])
    i = mid if mid < 0x200 else mid - 0x200
    return s.attr[i] if i < len(s.attr) else 0


def meta_of(e, mid):
    s = tset("gTileset_General") if mid < 0x200 else tset(e["secondary_tileset"])
    i = mid if mid < 0x200 else mid - 0x200
    return s.meta[i] if i < len(s.meta) else [0] * 8


def event_cells(js):
    cells = {}
    for kind in ("object_events", "warp_events", "coord_events", "bg_events"):
        for ev in js.get(kind) or []:
            cells.setdefault((ev["x"], ev["y"]), []).append(kind)
    return cells


def buildings(L):
    """Every old Centre / Mart: by door metatile. -> list of dicts."""
    out = []
    for lid, e in L.items():
        if e.get("primary_tileset") != "gTileset_General":
            continue
        g = read_grid(e)
        if g is None:
            continue
        for y, row in enumerate(g):
            for x, v in enumerate(row):
                m = v & 0x3FF
                if m == OLD_CENTRE_DOOR:
                    out.append(dict(layout=lid, kind="centre", door=(x, y), box=(x - 1, y - 2, 4, 4)))
                elif m == OLD_MART_DOOR:
                    out.append(dict(layout=lid, kind="mart", door=(x, y), box=(x - 1, y - 3, 4, 4)))
    return out
