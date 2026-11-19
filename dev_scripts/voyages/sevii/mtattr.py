"""Metatile behaviour / layout helpers for the Sevii build scripts (Emerald metatile_attributes = u16, behaviour bits 0-7)."""
import json, os, re, struct

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
P = lambda *p: os.path.join(ROOT, *p)
_MB, _ATTR, _LAYOUTS = None, {}, None


def mb():
    """name -> value and value -> name for enum MetatileBehavior."""
    global _MB
    if _MB is None:
        txt = open(P("include", "constants", "metatile_behaviors.h")).read()
        body = txt[txt.index("{") + 1:txt.index("}")]
        names, n = {}, 0
        for line in body.split("\n"):
            line = line.split("//")[0].strip().rstrip(",")
            if not line:
                continue
            if "=" in line:
                k, v = [s.strip() for s in line.split("=")]
                n = int(v, 0)
                line = k
            names[line] = n
            n += 1
        _MB = (names, {v: k for k, v in names.items()})
    return _MB


def tileset_attr_path(ts):
    txt = open(P("src", "data", "tilesets", "headers.h")).read()
    m = re.search(r"const struct Tileset %s =\s*\{(.*?)\};" % re.escape(ts), txt, re.S)
    sym = re.search(r"\.metatileAttributes = (\w+)", m.group(1)).group(1)
    mt = open(P("src", "data", "tilesets", "metatiles.h")).read()
    return P(re.search(r"%s\[\] = INCBIN_U16\(\"([^\"]+)\"\)" % sym, mt).group(1))


def attrs(ts):
    if ts not in _ATTR:
        d = open(tileset_attr_path(ts), "rb").read()
        _ATTR[ts] = struct.unpack("<%dH" % (len(d) // 2), d)
    return _ATTR[ts]


def layouts():
    global _LAYOUTS
    if _LAYOUTS is None:
        _LAYOUTS = {l["id"]: l for l in json.load(open(P("data", "layouts", "layouts.json")))["layouts"] if "id" in l}
    return _LAYOUTS


def reset():
    global _LAYOUTS
    _LAYOUTS = None
    _ATTR.clear()


class Layout:
    def __init__(self, layout_id=None, entry=None):
        L = entry or layouts()[layout_id]
        self.L, self.w, self.h = L, L["width"], L["height"]
        d = open(P(L["blockdata_filepath"]), "rb").read()
        self.cells = list(struct.unpack("<%dH" % (self.w * self.h), d))
        self.pa, self.sa = attrs(L["primary_tileset"]), attrs(L["secondary_tileset"])

    def raw(self, x, y):
        return self.cells[y * self.w + x]

    def mt(self, x, y):
        return self.raw(x, y) & 0x3FF

    def coll(self, x, y):
        return (self.raw(x, y) >> 10) & 3

    def elev(self, x, y):
        return self.raw(x, y) >> 12

    def beh(self, x, y):
        m = self.mt(x, y)
        a = self.pa[m] if m < 512 else self.sa[m - 512] if m - 512 < len(self.sa) else 0
        return a & 0xFF

    def behname(self, x, y):
        return mb()[1].get(self.beh(x, y), hex(self.beh(x, y)))

    def inside(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h

    def save(self):
        open(P(self.L["blockdata_filepath"]), "wb").write(struct.pack("<%dH" % len(self.cells), *self.cells))
