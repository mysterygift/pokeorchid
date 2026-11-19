"""
Map mockup composer for the Tiksi maps: builds a layout ONLY from metatiles that already exist in the
chosen tilesets, by copying cells / chunks out of existing layouts that use the same primary+secondary
pair. Nothing is drawn or added to a tileset, so no other map using it can change.

A spec is a dict:
  name, size (w, h), tileset (primary, secondary)
  ground: (LAYOUT, x, y)                         cell copied everywhere first
  legend: {char: (LAYOUT, x, y)}                 one cell per character in `rows`
  rows:   [str, ...]                             '.' = keep what is there; other chars from `legend`
  stamps: [(LAYOUT, sx, sy, w, h, dx, dy), ...]  chunks copied in order (after rows)
  marks:  [(x, y, label, kind)]                  mockup-only overlay: npc / warp / regi / sign / land
Raw u16 block values are copied, so collision + elevation travel with each metatile.

compose(spec) -> (grid, under_rgba, over_rgba); mockup(spec, path, scale) writes a PNG with the overlay.
"""
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "dev_scripts", "centre_mart"))
import vanilla                                   # noqa: E402  Scene renders metatiles from repo data
from PIL import Image, ImageDraw                 # noqa: E402

_LAYOUTS = {}


def raw_layout(layout_id):
    """-> (entry, rows of raw u16 block values)."""
    if layout_id not in _LAYOUTS:
        js = json.load(open(os.path.join(ROOT, "data", "layouts", "layouts.json")))
        for e in js["layouts"]:
            if e.get("id") == layout_id:
                w, h = e["width"], e["height"]
                raw = open(os.path.join(ROOT, e["blockdata_filepath"]), "rb").read()
                vals = struct.unpack("<%dH" % (w * h), raw[:2 * w * h])
                _LAYOUTS[layout_id] = (e, [list(vals[y * w:(y + 1) * w]) for y in range(h)])
                break
        else:
            raise KeyError(layout_id)
    return _LAYOUTS[layout_id]


def cell(ref, tileset):
    lid, x, y = ref
    e, g = raw_layout(lid)
    assert (e["primary_tileset"], e["secondary_tileset"]) == tuple(tileset), \
        "%s uses %s/%s, not %s" % (lid, e["primary_tileset"], e["secondary_tileset"], tileset)
    return g[y][x]


def compose(spec):
    w, h = spec["size"]
    ts = spec["tileset"]
    g = [[cell(spec["ground"], ts)] * w for _ in range(h)]
    for y, row in enumerate(spec.get("rows", [])):
        for x, ch in enumerate(row):
            if ch != "." and ch != " " and x < w and y < h:
                g[y][x] = cell(spec["legend"][ch], ts)
    for lid, sx, sy, cw, chh, dx, dy in spec.get("stamps", []):
        for j in range(chh):
            for i in range(cw):
                if 0 <= dx + i < w and 0 <= dy + j < h:
                    g[dy + j][dx + i] = cell((lid, sx + i, sy + j), ts)
    # rows_after: like rows, applied after the stamps (to patch seams); '_' = the ground cell
    for y, row in enumerate(spec.get("rows_after", [])):
        for x, ch in enumerate(row):
            if ch not in ". " and x < w and y < h:
                g[y][x] = cell(spec["ground"] if ch == "_" else spec["legend"][ch], ts)
    sc = vanilla.Scene(*ts)
    under = Image.new("RGBA", (w * 16, h * 16))
    over = Image.new("RGBA", (w * 16, h * 16), (0, 0, 0, 0))
    for y in range(h):
        for x in range(w):
            u, o = sc.metatile(g[y][x] & 0x3FF)
            under.paste(u, (x * 16, y * 16))
            over.paste(o, (x * 16, y * 16))
    return g, under, over


MARK_COLOURS = {"npc": (255, 220, 60), "warp": (80, 200, 255), "regi": (255, 80, 80), "sign": (200, 255, 120),
                "land": (255, 255, 255)}


def mockup(spec, path, scale=2, marks=True):
    g, under, over = compose(spec)
    im = under.copy()
    im.alpha_composite(over)
    im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
    if marks:
        d = ImageDraw.Draw(im)
        T = 16 * scale
        for x, y, label, kind in spec.get("marks", []):
            c = MARK_COLOURS.get(kind, (255, 255, 255))
            d.rectangle([x * T + 2, y * T + 2, x * T + T - 3, y * T + T - 3], outline=c + (255,), width=2)
            d.text((x * T + 3, y * T + T - 2), label, fill=c + (255,), stroke_width=2, stroke_fill=(0, 0, 0, 255))
    im.convert("RGB").save(path)
    return g


def write_blocks(spec, g, path):
    open(path, "wb").write(struct.pack("<%dH" % (len(g) * len(g[0])), *[v for r in g for v in r]))
