"""
Shared composer for the Sailor's Voyages design-review mockups (post-game boat trips to secret islands).

Builds map mockups ONLY from metatiles that already exist in a chosen primary+secondary tileset pair, by
copying raw block values (metatile id + collision + elevation) out of layouts that use that same pair. No
tileset is touched, so no other map that shares a tileset can change. Wraps dev_scripts/tiksi_maps/compose.py
(not edited) and adds:

  * git fallback: layouts deleted from the working tree (most vanilla Hoenn maps) are read from git at
    GIT_REF (the commit before the Hoenn maps were deleted). Force the vanilla copy of a layout that still
    exists but was rebuilt by Orchid with an "@git" suffix: "LAYOUT_DEWFORD_TOWN@git".
  * base: start the grid from an existing layout instead of a single ground cell (edits / patches).
  * extra spec keys (applied in this order after base/ground):
        rows, legend           as compose.py ('.'/' ' = keep)
        fill:  [(x, y, w, h, ref)]               rectangle of one cell
        stamps: [(LAYOUT, sx, sy, w, h, dx, dy)] chunks (as compose.py)
        pstamps: [(LAYOUT, sx, sy, w, h, dx, dy)] chunks from a layout of ANY pair with the same primary;
                 every cell must be a primary metatile (< 0x200, the same art in every pair) -- e.g. the
                 Orchid Centre / Mart / red-roof house, which live in the General primary   (batch 2)
        cells: [(x, y, ref)]                     single cells
        rows_after                               as compose.py ('_' = ground cell)
        auto:  [(x, y, [ids])]                   cells solved by vanilla neighbour frequency (solve())
        post:  [(x, y, ref)]                     single cells applied last (seam fixes)
    A terrain mask can come first: mask (rows), mask_legend {char: ref}, mask_auto {char: [ids]};
    ring_classes() turns a land/sea mask into rim 'R' / sea-edge 'W' classes. edges (or edges_list) =
    dict(chars, water_chars, vocab, layouts[, kind="rock"]) tiles those chars from vanilla examples by
    their 8-neighbour class signature (learn_edges / autotile_edges); big_trees / tree_kit tile 2x2 trees.
    A ref is (LAYOUT, x, y) -> that layout's raw cell; ("id", metatile[, coll, elev]) -> the raw value of a
    cell that shows that metatile in some same-pair layout (for a primary-tileset id that the pair's layouts
    never use: any layout with the same primary); or ("raw", u16) -> a raw block value whose metatile id is
    checked to exist in the pair (use only values read from a same-pair layout).
  * marks: [(x, y, label, kind)]. kind is one of
        sailor, son, npc, boat, legendary, item, warp, sign, moved, note
    sailor/son/npc/boat/legendary/item also draw the real overworld sprite (see SPRITES), so the mockup
    reads like the game; every mark gets a small labelled box.
  * render(spec, out_base) -> writes <out_base>.png (1x) and <out_base>@2x.png, both with marks.
  * render_layout(layout_id, out_base, marks) for "before" pictures of untouched maps.
  * catalog(layout_id, path, scale) -> coordinate-gridded picture of a layout, to pick cells from.
  * check_size(w, h) asserts the engine limit (w+15)*(h+14) <= 10240 and even sizes.
  * sharing(secondary) -> ids of the working-tree layouts that use a secondary tileset.

Run with the scratchpad venv python (system python has no Pillow).
"""
import json
import os
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))   # holon stream copy lives in dev_scripts/voyages/holon/
sys.path.insert(0, os.path.join(ROOT, "dev_scripts", "tiksi_maps"))
import compose                                     # noqa: E402
import vanilla                                     # noqa: E402  (imported by compose)
from PIL import Image, ImageDraw                   # noqa: E402

GIT_REF = "1d1d50b3a2~1"     # last commit with the vanilla Hoenn layouts in data/layouts

_orig_raw_layout = compose.raw_layout
_GIT_JSON = None


def _git(path):
    return subprocess.run(["git", "-C", ROOT, "show", "%s:%s" % (GIT_REF, path)],
                          capture_output=True, check=True).stdout


def _git_raw_layout(layout_id):
    global _GIT_JSON
    if _GIT_JSON is None:
        _GIT_JSON = json.loads(_git("data/layouts/layouts.json"))
    for e in _GIT_JSON["layouts"]:
        if e.get("id") == layout_id:
            w, h = e["width"], e["height"]
            vals = struct.unpack("<%dH" % (w * h), _git(e["blockdata_filepath"])[:2 * w * h])
            return e, [list(vals[y * w:(y + 1) * w]) for y in range(h)]
    raise KeyError(layout_id)


def raw_layout(layout_id):
    """-> (layouts.json entry, rows of raw u16). Working tree first, then git; 'ID@git' forces git."""
    if layout_id in compose._LAYOUTS:
        return compose._LAYOUTS[layout_id]
    if layout_id.endswith("@git"):
        compose._LAYOUTS[layout_id] = _git_raw_layout(layout_id[:-4])
        return compose._LAYOUTS[layout_id]
    try:
        return _orig_raw_layout(layout_id)
    except KeyError:
        compose._LAYOUTS[layout_id] = _git_raw_layout(layout_id)
        return compose._LAYOUTS[layout_id]


compose.raw_layout = raw_layout     # compose.cell() now sees deleted vanilla layouts too

_SCENES = {}

# ------------------------------------------------------------------ virtual (proposed) secondaries (batch 3)
# A proposed new secondary that is a COPY of an existing one plus additions, e.g. gTileset_SeviiIslands =
# gTileset_Rustboro + cottage variants / market stall / ported FRLG art, used only by the Sevii maps. Nothing
# is written to data/: the scene draws the base tileset and the module's extras on top. Cell lookups
# ("id" refs, stamps, the autotilers) run on the base pair (real_pair), so every existing id means the same
# metatile; new metatiles are placed with spec["vcells"] / spec["vstamps"] after everything else.
# module.extras() -> dict(base=<real secondary>, tiles=[8x8 lists of colour indices], palettes={slot: 16 rgb},
#                         metatiles=[(label, (8 tile entries), attr u16)])   (ids follow the base's)
# module.RAW {label: raw u16}, module.STAMPS {name: dict(cells=[[raw]], door=(dx, dy) or None)}
VIRTUAL_MODULES = {"gTileset_SeviiIslands": "sevii_tileset"}
_VIRTUAL = {}


def virtual(name):
    """The extras module of a virtual secondary (imported on first use), or None."""
    if name not in VIRTUAL_MODULES:
        return None
    if name not in _VIRTUAL:
        import importlib
        _VIRTUAL[name] = importlib.import_module(VIRTUAL_MODULES[name])
    return _VIRTUAL[name]


def real_pair(ts):
    """The pair whose layouts / metatile ids a (possibly virtual) pair copies."""
    ts = tuple(ts)
    mod = virtual(ts[1])
    return (ts[0], mod.extras()["base"]) if mod else ts


def scene(ts):
    ts = tuple(ts)
    if ts not in _SCENES:
        mod = virtual(ts[1])
        if not mod:
            _SCENES[ts] = vanilla.Scene(*ts)
        else:
            ex = mod.extras()
            sc = vanilla.Scene(ts[0], ex["base"])
            s_ = sc.s
            base_tile, extra = s_.tile, ex.get("tiles", {})      # {secondary tile index: 8x8} overrides
            s_.tile = lambda i, _b=base_tile, _e=extra: _e[i] if i in _e else _b(i)
            s_.n = max([s_.n] + [k + 1 for k in extra])
            for slot, pal in ex.get("palettes", {}).items():
                sc.pals[slot] = [tuple(c) for c in pal]
            for _lab, entries, attr in ex.get("metatiles", []):
                s_.metatiles.append(tuple(entries))
                s_.attrs.append(attr)
            _SCENES[ts] = sc
    return _SCENES[ts]


def _count(ts):
    sc = scene(ts)
    return len(sc.p.metatiles), len(sc.s.metatiles)


def ref_value(ref, ts):
    if ref[0] == "id":                      # ("id", metatile[, coll, elev]) -> an existing same-pair cell
        if ref[1] >= 0x200 or ref[1] in uses(ts):
            r = by_id(ref[1], ts, *ref[2:])
            return raw_layout(r[0])[1][r[2]][r[1]]
        return _prim_value(ref[1], ts, *ref[2:])
    if ref[0] == "raw":
        v = ref[1]
        mid = v & 0x3FF
        np_, ns = _count(ts)
        assert (mid < np_) if mid < 0x200 else (mid - 0x200 < ns), "metatile 0x%X not in %s" % (mid, ts)
        return v
    return compose.cell(ref, ts)


def build(spec):
    """spec -> grid of raw u16 (see module docstring)."""
    w, h = spec["size"]
    vts = tuple(spec["tileset"])
    ts = real_pair(vts)                      # lookups on the base pair; virtual additions go in last
    if "base" in spec:
        e, g0 = raw_layout(spec["base"])
        assert (e["primary_tileset"], e["secondary_tileset"]) == ts, (spec["base"], ts)
        ox, oy = spec.get("base_offset", (0, 0))
        fillv = ref_value(spec["ground"], ts) if "ground" in spec else 0
        g = [[fillv] * w for _ in range(h)]
        for y in range(len(g0)):
            for x in range(len(g0[0])):
                if 0 <= x + ox < w and 0 <= y + oy < h:
                    g[y + oy][x + ox] = g0[y][x]
    else:
        gv = ref_value(spec["ground"], ts)
        g = [[gv] * w for _ in range(h)]

    def put(x, y, v):
        if 0 <= x < w and 0 <= y < h:
            g[y][x] = v

    if "mask" in spec:     # terrain mask first: legend chars -> refs, mask_auto chars -> solved candidates
        mask = spec["mask"]
        edge_list = spec.get("edges_list") or ([spec["edges"]] if spec.get("edges") else [])
        auto_legend = dict(spec.get("mask_auto", {}))
        for edges in edge_list:
            for ch in edges["chars"]:
                auto_legend.pop(ch, None)
        apply_mask(g, mask, spec.get("mask_legend", {}), auto_legend, ts)
        for edges in edge_list:   # each: chars to tile, water_chars = the "true" class, vocab, layouts
            water = [[ch in edges["water_chars"] for ch in row] for row in mask]
            table = learn_edges(edges["layouts"], ts, {"rock": is_rock, "shore": shore_class}.get(edges.get("kind")))
            cells = [(x, y) for y, row in enumerate(mask) for x, ch in enumerate(row) if ch in edges["chars"]]
            left = autotile_edges(g, cells, water, table, set(edges["vocab"]), ts)
            if left:
                solve(g, {c: edges["vocab"] for c in left}, ts)
        if "big_trees" in spec:    # mask char tiled with 2x2 forest trees
            big_trees(g, mask, spec["big_trees"], ts, kit=spec.get("tree_kit", TREES_GENERAL))

    for y, row in enumerate(spec.get("rows", [])):
        for x, ch in enumerate(row):
            if ch not in ". ":
                put(x, y, ref_value(spec["legend"][ch], ts))
    for x, y, fw, fh, ref in spec.get("fill", []):
        v = ref_value(ref, ts)
        for j in range(fh):
            for i in range(fw):
                put(x + i, y + j, v)
    for lid, sx, sy, cw, chh, dx, dy in spec.get("stamps", []):
        for j in range(chh):
            for i in range(cw):
                put(dx + i, dy + j, ref_value((lid, sx + i, sy + j), ts))
    for lid, sx, sy, cw, chh, dx, dy in spec.get("pstamps", []):
        e, g0 = raw_layout(lid)
        assert e["primary_tileset"] == ts[0], (lid, e["primary_tileset"], ts)
        for j in range(chh):
            for i in range(cw):
                v = g0[sy + j][sx + i]
                assert v & 0x3FF < 0x200, "pstamp %s (%d,%d) = secondary metatile 0x%X" % (lid, sx + i, sy + j,
                                                                                           v & 0x3FF)
                put(dx + i, dy + j, v)
    for x, y, ref in spec.get("cells", []):
        put(x, y, ref_value(ref, ts))
    for y, row in enumerate(spec.get("rows_after", [])):
        for x, ch in enumerate(row):
            if ch not in ". ":
                put(x, y, ref_value(spec["ground"] if ch == "_" else spec["legend"][ch], ts))
    if spec.get("auto"):   # [(x, y, [candidate ids])] solved against everything placed so far
        solve(g, {(x, y): c for x, y, c in spec["auto"]}, ts)
    for x, y, ref in spec.get("post", []):
        put(x, y, ref_value(ref, ts))
    if vts != ts:                            # new metatiles of a virtual secondary
        mod = virtual(vts[1])
        n_meta = 0x200 + len(scene(vts).s.metatiles)
        for name, dx, dy in spec.get("vstamps", []):
            for j, row in enumerate(mod.STAMPS[name]["cells"]):
                for i, v in enumerate(row):
                    if v is not None:
                        put(dx + i, dy + j, v)
        for x, y, v in spec.get("vcells", []):
            v = mod.RAW[v] if isinstance(v, str) else v
            assert (v & 0x3FF) < n_meta, "metatile 0x%X not in %s" % (v & 0x3FF, vts[1])
            put(x, y, v)
    return g


def draw_grid(g, ts):
    sc = scene(ts)
    h, w = len(g), len(g[0])
    under = Image.new("RGBA", (w * 16, h * 16))
    over = Image.new("RGBA", (w * 16, h * 16), (0, 0, 0, 0))
    for y in range(h):
        for x in range(w):
            u, o = sc.metatile(g[y][x] & 0x3FF)
            under.paste(u, (x * 16, y * 16))
            over.paste(o, (x * 16, y * 16))
    return under, over


# ------------------------------------------------------------------ overworld sprites for the marks
# kind/name -> (png, frame w, frame h, frame index, hflip)
SPRITES = {
    "sailor": ("graphics/object_events/pics/people/sailor.png", 16, 32, 0, False),
    "sailor_up": ("graphics/object_events/pics/people/sailor.png", 16, 32, 1, False),
    "sailor_left": ("graphics/object_events/pics/people/sailor.png", 16, 32, 2, False),
    "sailor_right": ("graphics/object_events/pics/people/sailor.png", 16, 32, 2, True),
    "son": ("graphics/object_events/pics/people/little_boy.png", 16, 16, 0, False),
    "fisherman": ("graphics/object_events/pics/people/fisherman.png", 16, 32, 0, False),
    "boat": ("graphics/object_events/pics/misc/mr_brineys_boat.png", 32, 32, 0, False),
    "boat_up": ("graphics/object_events/pics/misc/mr_brineys_boat.png", 32, 32, 1, False),
    "boat_left": ("graphics/object_events/pics/misc/mr_brineys_boat.png", 32, 32, 2, False),
    "boat_right": ("graphics/object_events/pics/misc/mr_brineys_boat.png", 32, 32, 2, True),
    "ss_tidal": ("graphics/object_events/pics/misc/ss_tidal.png", 32, 40, 0, False),
    "item": ("graphics/object_events/pics/misc/ball_poke.png", 16, 32, 0, False),
    "latias": ("graphics/pokemon/latias/overworld.png", 32, 32, 0, False),
    "latios": ("graphics/pokemon/latios/overworld.png", 32, 32, 0, False),
    "darkrai": ("graphics/pokemon/darkrai/overworld.png", 32, 32, 0, False),
    "cresselia": ("graphics/pokemon/cresselia/overworld.png", 32, 32, 0, False),
    "cresselia_right": ("graphics/pokemon/cresselia/overworld.png", 32, 32, 2, True),
    # batch 2: generic townsfolk (Emerald graphics only; FRLG-only OW gfx are invisible in this build)
    "ss_tidal_left": ("graphics/object_events/pics/misc/ss_tidal.png", 32, 40, 1, False),
    "ss_tidal_right": ("graphics/object_events/pics/misc/ss_tidal.png", 32, 40, 1, True),
    "boy": ("graphics/object_events/pics/people/boy_1.png", 16, 32, 0, False),
    "woman": ("graphics/object_events/pics/people/woman_2.png", 16, 32, 0, False),
    "old_man": ("graphics/object_events/pics/people/old_man.png", 16, 32, 0, False),
    "old_woman": ("graphics/object_events/pics/people/old_woman.png", 16, 32, 0, False),
    "hiker": ("graphics/object_events/pics/people/hiker.png", 16, 32, 0, False),
    "swimmer": ("graphics/object_events/pics/people/swimmer_m.png", 16, 32, 0, False),
    "lass": ("graphics/object_events/pics/people/lass.png", 16, 32, 0, False),
    "camper": ("graphics/object_events/pics/people/camper.png", 16, 32, 0, False),
    "picnicker": ("graphics/object_events/pics/people/picnicker.png", 16, 32, 0, False),
    "man": ("graphics/object_events/pics/people/man_3.png", 16, 32, 0, False),
    "expert": ("graphics/object_events/pics/people/expert_m.png", 16, 32, 0, False),
    "beauty": ("graphics/object_events/pics/people/beauty.png", 16, 32, 0, False),
    "fisherman_left": ("graphics/object_events/pics/people/fisherman.png", 16, 32, 2, False),
    # field-move objects (Emerald graphics; the _frlg ones are invisible in this build)
    "breakable_rock": ("graphics/object_events/pics/misc/breakable_rock.png", 16, 16, 0, False),
    "pushable_boulder": ("graphics/object_events/pics/misc/pushable_boulder.png", 16, 16, 0, False),
    "cuttable_tree": ("graphics/object_events/pics/misc/cuttable_tree.png", 16, 16, 0, False),
}
_SPR = {}


def sprite(name):
    if name not in _SPR:
        path, fw, fh, fi, flip = SPRITES[name]
        im = Image.open(os.path.join(ROOT, path))
        im = im.crop((fi * fw, 0, fi * fw + fw, fh))
        rgba = im.convert("RGBA")
        if im.mode == "P":
            px, rp = im.load(), rgba.load()
            for y in range(im.height):
                for x in range(im.width):
                    if px[x, y] == 0:
                        rp[x, y] = (0, 0, 0, 0)
        if flip:
            rgba = rgba.transpose(Image.FLIP_LEFT_RIGHT)
        _SPR[name] = rgba
    return _SPR[name]


MARK_COLOURS = {"sailor": (255, 220, 60), "son": (255, 170, 60), "npc": (255, 220, 60), "boat": (255, 255, 255),
                "legendary": (255, 90, 200), "item": (255, 80, 80), "warp": (80, 200, 255),
                "sign": (200, 255, 120), "moved": (255, 140, 0), "note": (255, 255, 255),
                "conn": (255, 120, 40), "spot": (255, 90, 200), "ferry": (255, 255, 255), "field": (190, 190, 190)}
SPRITE_KINDS = {"sailor", "son", "npc", "boat", "legendary", "item", "ferry", "field"}


def _overlay(im, marks, scale):
    """Sprites first (at 1x before scaling would blur nothing, but we draw at final scale)."""
    T = 16 * scale
    for m in marks:
        x, y, label, kind = m[:4]
        spr = m[4] if len(m) > 4 else (kind if kind in SPRITES else None)
        if kind in SPRITE_KINDS and spr:
            s = sprite(spr)
            s = s.resize((s.width * scale, s.height * scale), Image.NEAREST)
            px = x * T + T // 2 - s.width // 2
            py = y * T + T - s.height
            im.alpha_composite(s, (px, py))
    d = ImageDraw.Draw(im)
    for m in marks:
        x, y, label, kind = m[:4]
        c = MARK_COLOURS.get(kind, (255, 255, 255)) + (255,)
        if kind == "note":
            d.text((x * T + 2, y * T + 2), label, fill=c, stroke_width=2, stroke_fill=(0, 0, 0, 255))
            continue
        if kind == "conn":      # map-edge connection: (x, y) is the label anchor, drawn as an arrow label
            d.text((x * T + 2, y * T + 2), label, fill=c, stroke_width=2, stroke_fill=(0, 0, 0, 255))
            continue
        if kind == "spot":      # empty landmark spot: dashed double box
            for k in (1, 4):
                d.rectangle([x * T + k, y * T + k, x * T + T - 1 - k, y * T + T - 1 - k], outline=c, width=1)
        bw = max(1, scale)
        d.rectangle([x * T + 1, y * T + 1, x * T + T - 2, y * T + T - 2], outline=c, width=bw)
        if label:
            d.text((x * T + 2, y * T + T - 1), label, fill=c, stroke_width=2, stroke_fill=(0, 0, 0, 255))


def picture(g, ts, marks=(), scale=1, grid=False):
    under, over = draw_grid(g, ts)
    im = under.copy()
    im.alpha_composite(over)
    im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
    if grid:
        d = ImageDraw.Draw(im)
        T = 16 * scale
        for x in range(len(g[0])):
            d.line([(x * T, 0), (x * T, im.height)], fill=(0, 0, 0, 70))
        for y in range(len(g)):
            d.line([(0, y * T), (im.width, y * T)], fill=(0, 0, 0, 70))
    if marks:
        _overlay(im, marks, scale)
    return im


def render(spec, out_base, grid=False):
    """Writes <out_base>.png and <out_base>@2x.png with marks; returns the grid."""
    g = build(spec)
    ts = tuple(spec["tileset"])
    marks = spec.get("marks", [])
    os.makedirs(os.path.dirname(out_base), exist_ok=True)
    picture(g, ts, marks, 1, grid).convert("RGB").save(out_base + ".png")
    picture(g, ts, marks, 2, grid).convert("RGB").save(out_base + "@2x.png")
    return g


def layout_spec(layout_id):
    e, g = raw_layout(layout_id)
    return dict(size=(e["width"], e["height"]), tileset=(e["primary_tileset"], e["secondary_tileset"]),
                base=layout_id)


def render_layout(layout_id, out_base, marks=()):
    spec = layout_spec(layout_id)
    spec["marks"] = list(marks)
    return render(spec, out_base)


def catalog(layout_id, path, scale=2, region=None):
    """Gridded picture with x/y numbers every tile (region=(x, y, w, h) to crop)."""
    e, g = raw_layout(layout_id)
    ts = (e["primary_tileset"], e["secondary_tileset"])
    if region:
        rx, ry, rw, rh = region
        g = [row[rx:rx + rw] for row in g[ry:ry + rh]]
    else:
        rx = ry = 0
    im = picture(g, ts, (), scale, grid=True)
    pad = 14
    out = Image.new("RGBA", (im.width + pad, im.height + pad), (255, 255, 255, 255))
    out.paste(im, (pad, pad))
    d = ImageDraw.Draw(out)
    T = 16 * scale
    for x in range(len(g[0])):
        d.text((pad + x * T + 2, 1), str(rx + x), fill=(0, 0, 0, 255))
    for y in range(len(g)):
        d.text((0, pad + y * T + 2), str(ry + y), fill=(0, 0, 0, 255))
    out.convert("RGB").save(path)


def check_size(w, h):
    assert w % 2 == 0 and h % 2 == 0, "keep w, h even (%d x %d)" % (w, h)
    assert (w + 15) * (h + 14) <= 10240, "(w+15)*(h+14) = %d > 10240" % ((w + 15) * (h + 14))


def sharing(secondary):
    js = json.load(open(os.path.join(ROOT, "data", "layouts", "layouts.json")))
    return [e["id"] for e in js["layouts"] if e.get("secondary_tileset") == secondary]


def metatile_ids(g):
    return sorted({v & 0x3FF for row in g for v in row})


def write_blocks(g, path):
    open(path, "wb").write(struct.pack("<%dH" % (len(g) * len(g[0])), *[v for r in g for v in r]))


# ------------------------------------------------------------------ id lookup
def pair_layouts(ts, include_git=True):
    """Layout ids (working tree, then git-only vanilla) whose tileset pair is ts."""
    global _GIT_JSON
    ts = real_pair(ts)
    out = []
    js = json.load(open(os.path.join(ROOT, "data", "layouts", "layouts.json")))
    have = set()
    for e in js["layouts"]:
        if (e.get("primary_tileset"), e.get("secondary_tileset")) == ts:
            out.append(e["id"])
        have.add(e.get("id"))
    if include_git:
        if _GIT_JSON is None:
            _GIT_JSON = json.loads(_git("data/layouts/layouts.json"))
        for e in _GIT_JSON["layouts"]:
            if (e.get("primary_tileset"), e.get("secondary_tileset")) == ts:
                out.append(e["id"] if e["id"] not in have else e["id"] + "@git")
    return out


_USES = {}


def uses(ts):
    """{metatile id: {raw value: [(layout, x, y), ...]}} over every same-pair layout."""
    ts = tuple(ts)
    if ts not in _USES:
        d = {}
        for lid in pair_layouts(ts):
            try:
                e, g = raw_layout(lid)
            except Exception:
                continue
            for y, row in enumerate(g):
                for x, v in enumerate(row):
                    d.setdefault(v & 0x3FF, {}).setdefault(v, []).append((lid, x, y))
        _USES[ts] = d
    return _USES[ts]


def by_id(mid, ts, coll=None, elev=None):
    """A (LAYOUT, x, y) ref to an existing same-pair cell that shows metatile `mid` (most common raw
    collision/elevation, or the one asked for). Raises if no layout with this pair uses it."""
    vs = uses(ts).get(mid)
    if not vs:
        raise KeyError("metatile 0x%X is used by no %s layout" % (mid, ts))
    cands = [(len(locs), v) for v, locs in vs.items()
             if (coll is None or (v >> 10) & 3 == coll) and (elev is None or v >> 12 == elev)]
    if not cands:
        raise KeyError("0x%X with coll=%s elev=%s not found in %s" % (mid, coll, elev, ts))
    v = max(cands)[1]
    return vs[v][0]


def sheet(ts, start, count, path, cols=16, scale=2):
    """Metatile sheet with hex ids; ids no same-pair layout uses are dimmed."""
    sc = scene(ts)
    used = uses(ts)
    rows = (count + cols - 1) // cols
    T = 16 * scale
    im = Image.new("RGBA", (cols * (T + 4), rows * (T + 12)), (255, 255, 255, 255))
    d = ImageDraw.Draw(im)
    for k in range(count):
        mid = start + k
        u, o = sc.metatile(mid)
        t = u.copy()
        t.alpha_composite(o)
        t = t.resize((T, T), Image.NEAREST)
        if mid not in used:
            t = Image.blend(t, Image.new("RGBA", t.size, (255, 255, 255, 255)), 0.6)
        x, y = (k % cols) * (T + 4), (k // cols) * (T + 12)
        im.paste(t, (x, y + 11))
        d.text((x, y), "%03X" % mid, fill=(0, 0, 0, 255))
    im.convert("RGB").save(path)


def _prim_value(mid, ts, coll=None, elev=None):
    """Primary-tileset metatile that no layout of this pair uses: take its raw value from a layout that
    shares the primary (the metatile lives in the primary, so it is the same art in every pair)."""
    global _GIT_JSON
    if _GIT_JSON is None:
        _GIT_JSON = json.loads(_git("data/layouts/layouts.json"))
    js = json.load(open(os.path.join(ROOT, "data", "layouts", "layouts.json")))
    pairs = {(e.get("primary_tileset"), e.get("secondary_tileset"))
             for e in js["layouts"] + _GIT_JSON["layouts"] if "primary_tileset" in e}
    for p in sorted(pairs, key=str):
        if p[0] == ts[0] and p != tuple(ts):
            try:
                r = by_id(mid, p, coll, elev)
            except KeyError:
                continue
            return raw_layout(r[0])[1][r[2]][r[1]]
    raise KeyError("primary metatile 0x%X used nowhere" % mid)


def idmap(layout_id, path, region=None, scale=3):
    """Like catalog() but prints each cell's metatile id (hex) and collision (* = solid) on it."""
    e, g = raw_layout(layout_id)
    ts = (e["primary_tileset"], e["secondary_tileset"])
    rx, ry, rw, rh = region or (0, 0, e["width"], e["height"])
    g2 = [row[rx:rx + rw] for row in g[ry:ry + rh]]
    im = picture(g2, ts, (), scale, grid=True)
    pad = 16
    out = Image.new("RGBA", (im.width + pad, im.height + pad), (255, 255, 255, 255))
    out.paste(im, (pad, pad))
    d = ImageDraw.Draw(out)
    T = 16 * scale
    for x in range(rw):
        d.text((pad + x * T + 2, 2), str(rx + x), fill=(0, 0, 0, 255))
    for y in range(rh):
        d.text((0, pad + y * T + 2), str(ry + y), fill=(0, 0, 0, 255))
        for x in range(rw):
            v = g2[y][x]
            t = "%03X%s" % (v & 0x3FF, "*" if (v >> 10) & 3 else "")
            d.text((pad + x * T + 1, pad + y * T + 1), t, fill=(255, 255, 255, 255), stroke_width=1,
                   stroke_fill=(0, 0, 0, 255))
    out.convert("RGB").save(path)


# ------------------------------------------------------------------ seam checker
_ADJ = {}


def adjacency(ts):
    """{(a, b, dir): count} metatile-id pairs seen side by side in vanilla/working layouts: dir 'E' = b is east
    of a, 'S' = b is south of a. Pairs of two primary ids are learnt from every layout with the same
    primary; pairs involving a secondary id only from layouts with exactly this pair."""
    ts = real_pair(ts)
    if ts in _ADJ:
        return _ADJ[ts]
    global _GIT_JSON
    if _GIT_JSON is None:
        _GIT_JSON = json.loads(_git("data/layouts/layouts.json"))
    js = json.load(open(os.path.join(ROOT, "data", "layouts", "layouts.json")))
    have = {e.get("id") for e in js["layouts"]}
    ids = [(e["id"], (e["primary_tileset"], e["secondary_tileset"])) for e in js["layouts"]
           if "primary_tileset" in e]
    ids += [(e["id"] if e["id"] not in have else e["id"] + "@git", (e["primary_tileset"], e["secondary_tileset"]))
            for e in _GIT_JSON["layouts"] if "primary_tileset" in e]
    adj = {}
    for lid, p in ids:
        if p[0] != ts[0]:
            continue
        same = p == ts
        try:
            g = raw_layout(lid)[1]
        except Exception:
            continue
        h, w = len(g), len(g[0])
        for y in range(h):
            for x in range(w):
                a = g[y][x] & 0x3FF
                for dx, dy, d in ((1, 0, "E"), (0, 1, "S")):
                    if x + dx < w and y + dy < h:
                        b = g[y + dy][x + dx] & 0x3FF
                        if same or (a < 0x200 and b < 0x200):
                            adj[(a, b, d)] = adj.get((a, b, d), 0) + 1
    _ADJ[ts] = adj
    return adj


def seams(g, ts, ignore=()):
    """Cells whose east or south neighbour pair never occurs in any comparable layout:
    [(x, y, 'E'|'S', a, b)]. `ignore` = metatile ids to skip (e.g. plain ground that goes with anything)."""
    adj = adjacency(ts)
    out = []
    h, w = len(g), len(g[0])
    for y in range(h):
        for x in range(w):
            a = g[y][x] & 0x3FF
            for dx, dy, d in ((1, 0, "E"), (0, 1, "S")):
                if x + dx < w and y + dy < h:
                    b = g[y + dy][x + dx] & 0x3FF
                    if a != b and a not in ignore and b not in ignore and (a, b, d) not in adj:
                        out.append((x, y, d, a, b))
    return out


def neighbours(mid, ts, d):
    """Metatiles seen to the d ('N','S','E','W') of `mid`, most common first is not tracked: a sorted set."""
    adj = adjacency(ts)
    if d == "E":
        return sorted(b for a, b, dd in adj if a == mid and dd == "E")
    if d == "S":
        return sorted(b for a, b, dd in adj if a == mid and dd == "S")
    if d == "W":
        return sorted(a for a, b, dd in adj if b == mid and dd == "E")
    return sorted(a for a, b, dd in adj if b == mid and dd == "S")


def solve(g, auto, ts, rounds=12, fixed_raw=None):
    """Fill the cells in `auto` ({(x, y): [candidate metatile ids]}) with the candidates that fit their
    neighbours best, by vanilla pair frequency (iterated conditional modes; each cell maximises the sum of
    log(count + 0.01) over its 4 neighbours). Writes raw values (taken from existing same-pair / same-primary
    cells via ("id", mid)) into g in place and returns the list of cells that still have an unseen pair."""
    import math
    adj = adjacency(ts)
    h, w = len(g), len(g[0])
    cur = {k: v[0] for k, v in auto.items()}

    def mid(x, y):
        return cur[(x, y)] if (x, y) in cur else g[y][x] & 0x3FF

    def score(x, y, m):
        sc = 0.0
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < w and 0 <= ny < h):
                continue
            n = mid(nx, ny)
            if dx == 1:
                c = adj.get((m, n, "E"), 0)
            elif dx == -1:
                c = adj.get((n, m, "E"), 0)
            elif dy == 1:
                c = adj.get((m, n, "S"), 0)
            else:
                c = adj.get((n, m, "S"), 0)
            sc += math.log(c + 0.01)
        return sc

    for _ in range(rounds):
        changed = 0
        for (x, y), cands in auto.items():
            best = max(cands, key=lambda m: score(x, y, m))
            if best != cur[(x, y)]:
                cur[(x, y)] = best
                changed += 1
        if not changed:
            break
    for (x, y), m in cur.items():
        g[y][x] = ref_value(("id", m), ts)
    bad = [(x, y) for (x, y) in auto if score(x, y, cur[(x, y)]) < -4]
    return bad


# ------------------------------------------------------------------ terrain masks
def ring_classes(mask, land_chars, sea_chars="~", land_diag=False):
    """From a mask (list of str), mark land cells 4-adjacent (8-adjacent with land_diag) to sea as 'R' (rim)
    and sea cells 8-adjacent to land as 'W' (sea edge). Returns a new list of str (other cells unchanged)."""
    h, w = len(mask), len(mask[0])
    out = [list(r) for r in mask]
    for y in range(h):
        for x in range(w):
            c = mask[y][x]
            nb = [mask[y + dy][x + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1)
                  if (dx or dy) and 0 <= x + dx < w and 0 <= y + dy < h]
            nb4 = [mask[y + dy][x + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                   if 0 <= x + dx < w and 0 <= y + dy < h]
            if c in land_chars and any(n in sea_chars for n in (nb if land_diag else nb4)):
                out[y][x] = "R"
            elif c in sea_chars and any(n in land_chars for n in nb):
                out[y][x] = "W"
    return ["".join(r) for r in out]


def ring_multi(mask, coasts, sea_chars="~"):
    """Several coast types in one mask (batch 2). coasts = [(land_chars, land_mark, sea_mark), ...] in
    priority order: a land cell 4-adjacent to sea becomes land_mark (None = leave it), a sea cell 8-adjacent
    to that land becomes sea_mark (first coast that claims it wins). E.g. rock rim 'R'/'W' for grass and
    beach 'S'/'w' for sand in the same map."""
    h, w = len(mask), len(mask[0])
    out = [list(r) for r in mask]
    for y in range(h):
        for x in range(w):
            c = mask[y][x]
            nb8 = [mask[y + dy][x + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1)
                   if (dx or dy) and 0 <= x + dx < w and 0 <= y + dy < h]
            nb4 = [mask[y + dy][x + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                   if 0 <= x + dx < w and 0 <= y + dy < h]
            for land, lm, sm in coasts:
                if c in land and lm and any(n in sea_chars for n in nb4):
                    out[y][x] = lm
                    break
                if c in sea_chars and sm and any(n in land for n in nb8):
                    out[y][x] = sm
                    break
    return ["".join(r) for r in out]


def apply_mask(g, mask, legend, auto_legend, ts):
    """Write mask cells: legend chars -> refs; auto_legend chars -> candidate lists solved by solve().
    Returns the solve() report."""
    auto = {}
    for y, row in enumerate(mask):
        for x, ch in enumerate(row):
            if ch in auto_legend:
                auto[(x, y)] = auto_legend[ch]
            elif ch in legend:
                g[y][x] = ref_value(legend[ch], ts)
    return solve(g, auto, ts) if auto else []


# ------------------------------------------------------------------ learned edge autotiler
WATER_BEHAVIORS = {0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x18, 0x1A, 0x22, 0x2A, 0x2C, 0x2D}


def is_water(mid, ts):
    sc = scene(ts)
    ts_, i = (sc.p, mid) if mid < 0x200 else (sc.s, mid - 0x200)
    return i < len(ts_.attrs) and (ts_.attrs[i] & 0xFF) in WATER_BEHAVIORS


_NB8 = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))


def _sig(wgrid, x, y):
    h, w = len(wgrid), len(wgrid[0])
    own = wgrid[y][x]
    return (own,) + tuple(wgrid[y + dy][x + dx] if 0 <= x + dx < w and 0 <= y + dy < h else own
                          for dx, dy in _NB8)


def _reduce(sig):
    """Blob-style reduction: a diagonal only matters when both orthogonals beside it match the centre."""
    own, nw, n, ne, w, e, sw, s, se = sig
    keep = lambda d, a, b: d if (a == own and b == own) else own  # noqa: E731
    return (own, keep(nw, n, w), n, keep(ne, n, e), w, e, keep(sw, s, w), s, keep(se, s, e))


# General-primary rock massif / cliff pieces (Southern Island, Faraway Island, Route 120 gorge)
ROCK_IDS = set(range(0x06A, 0x07E)) | {0x088, 0x089, 0x08A, 0x090, 0x091, 0x093, 0x094, 0x0A9}


def is_rock(mid, ts):
    return mid in ROCK_IDS


SAND_IDS = {0x124, 0x13D, 0x13E}


def shore_class(mid, ts):
    """True = water, False = beach sand, None = anything else (cells next to it are not learnt from)."""
    if is_water(mid, ts):
        return True
    return False if mid in SAND_IDS else None


def learn_edges(layouts, ts, classify=None):
    """{reduced signature: {id: count}} from layouts (any pair with the same primary for primary ids).
    classify(mid, ts) -> bool splits cells in two classes (default is_water; is_rock for rock masses)."""
    classify = classify or is_water
    table = {}
    for lid in layouts:
        e, g = raw_layout(lid)
        lts = (e["primary_tileset"], e["secondary_tileset"])
        wg = [[classify(v & 0x3FF, lts) for v in row] for row in g]
        for y in range(len(g)):
            for x in range(len(g[0])):
                m = g[y][x] & 0x3FF
                if m >= 0x200 and lts != tuple(ts):
                    continue
                sg = _sig(wg, x, y)
                if None in sg:
                    continue
                d = table.setdefault(_reduce(sg), {})
                d[m] = d.get(m, 0) + 1
    return table


def autotile_edges(g, cells, water, table, vocab, ts):
    """For each (x, y) in cells, pick the most frequent vocab id for its reduced land/water signature
    (water = grid of bools for the target map). Unseen signatures fall back to the orthogonal-only
    signature, then are left for solve(). Returns the cells that could not be resolved."""
    left = []
    for (x, y) in cells:
        sig = _reduce(_sig(water, x, y))
        cand = {m: c for m, c in table.get(sig, {}).items() if m in vocab}
        if not cand:
            own, nw, n, ne, w, e, sw, s, se = sig
            loose = [k for k in table if (k[0], k[2], k[4], k[5], k[7]) == (own, n, w, e, s)]
            for k in loose:
                for m, c in table[k].items():
                    if m in vocab:
                        cand[m] = cand.get(m, 0) + c
        if cand:
            g[y][x] = ref_value(("id", max(cand, key=cand.get)), ts)
        else:
            left.append((x, y))
    return left


# 2x2 tree sets: top-left, top-right, bottom-left/right when another tree is below, bottom-left/right on
# open ground, crown peeks over the ground cell above, ground
TREES_GENERAL = (0x1D4, 0x1D5, 0x1DC, 0x1DD, 0x1DC, 0x1DD, 0x1CE, 0x1CF, 0x001)   # Petalburg Woods
TREES_ASH = (0x26D, 0x26E, 0x275, 0x276, 0x20C, 0x20D, 0x204, 0x205, 0x218)       # Route 113 (Fallarbor)


def big_trees(g, mask, ch, ts, peek=True, ground=None, kit=TREES_GENERAL):
    """Tile the `ch` cells of mask with 2x2 forest trees (kit, default the General primary's 1D4 1D5 /
    1DC 1DD as in Petalburg Woods / Southern Island interior; TREES_ASH for Route 113's ash trees), greedy
    from the top-left. Cells left over (not part of a full 2x2) become `ground` (default the kit's ground).
    With peek, a ground cell right above a tree gets the crown peek, as dress.py does."""
    h, w = len(mask), len(mask[0])
    used = [[False] * w for _ in range(h)]
    TL, TR, BL, BR, BLe, BRe, PLi, PRi, GR = kit
    TL, TR, BL, BR, BLe, BRe = (ref_value(("id", m), ts) for m in (TL, TR, BL, BR, BLe, BRe))
    ground = ground or ("id", GR)
    for y in range(h):
        for x in range(w):
            if used[y][x] or mask[y][x] != ch:
                continue
            if x + 1 < w and y + 1 < h and all(mask[y + j][x + i] == ch and not used[y + j][x + i]
                                               for i in (0, 1) for j in (0, 1)):
                g[y][x], g[y][x + 1], g[y + 1][x], g[y + 1][x + 1] = TL, TR, BL, BR
                for i in (0, 1):
                    for j in (0, 1):
                        used[y + j][x + i] = True
    gv = ref_value(ground or ("id", 0x001), ts)
    for y in range(h):
        for x in range(w):
            if mask[y][x] == ch and not used[y][x]:
                g[y][x] = gv
    # a tree with another tree right below uses the overlapping bottom; otherwise the open-ground bottom
    for y in range(h - 1):
        for x in range(w - 1):
            if g[y][x] == BL and g[y][x + 1] == BR:
                below = g[y + 1][x] if y + 1 < h else None
                if below != TL:
                    g[y][x], g[y][x + 1] = BLe, BRe
    if peek:
        PL, PR = ref_value(("id", PLi), ts), ref_value(("id", PRi), ts)
        gid = GR
        for y in range(1, h):
            for x in range(w - 1):
                if g[y][x] == TL and g[y][x + 1] == TR and g[y - 1][x] & 0x3FF == gid \
                        and g[y - 1][x + 1] & 0x3FF == gid:
                    g[y - 1][x], g[y - 1][x + 1] = PL, PR
    return used


def small_trees(mask, ch, body, top, bottom):
    """1-wide tree cells (Dewford style): `bottom` where the cell below is not ch (trunk on the ground),
    `top` where the cell above is not ch (crown over the ground), else `body`.
    Returns [(x, y, ref)] for spec['cells']."""
    h, w = len(mask), len(mask[0])
    out = []
    for y in range(h):
        for x in range(w):
            if mask[y][x] != ch:
                continue
            up = y > 0 and mask[y - 1][x] == ch
            dn = y + 1 < h and mask[y + 1][x] == ch
            if not dn and y + 1 < h:
                m = bottom                       # trunk on the ground (also a lone row of trees)
            elif not up and y > 0:
                m = top                          # crown over the ground above
            else:
                m = body
            out.append((x, y, ("id", m)))
    return out
