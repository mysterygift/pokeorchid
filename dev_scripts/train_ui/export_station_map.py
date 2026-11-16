"""
Export the ROM assets for the TOSA RAIL station map screen from network.json.

Reads   dev_scripts/train_ui/network.json
        include/constants/train_stations.h   (station ids + TRAIN_STATION_COUNT, validated)
        src/data/train_stations.h            (display names, validated)
Writes  graphics/train_map/bg.pal            JASC, 96 colours = BG palettes 0-5
        graphics/train_map/grid.png/.bin     BG3 grid tiles + 32x32 tilemap (pal 5)
        graphics/train_map/diagram.png/.bin  BG2 tube + label tiles + 64x32 tilemap (screenblock order)
        graphics/train_map/frame.png/.bin    BG1 header + tray tiles + 32x32 tilemap (pal 0)
        graphics/train_map/obj.pal           OBJ palette A: nodes.png, chevron.png, pill.png
        graphics/train_map/obj_lines.pal     OBJ palette B: legend.png, tray_line.png
        graphics/train_map/{nodes,chevron,pill,legend,tray_line}.png
        src/data/train_station_map.h         generated tables
        dev_scripts/train_ui/out/export_check_*.png  (decoded-from-export previews, 3x)

Fails (exit 1) on: id/count/name mismatch, off-grid nodes, non 0/45/90 runs, a cell holding both
label and tube pixels, a cell shared by two edges that isn't a station's centre cell (covered by
its node OBJ), > 512 diagram tiles, or non-opaque header/tray rows.

usage: python export_station_map.py
"""
import json
import os
import re
import struct
import sys

from common import *
import station_map as SM
from backdrop import GRID_PAL

NET = os.path.join(HERE, "network.json")
GFX = os.path.join(ROOT, "graphics", "train_map")
HDR = os.path.join(ROOT, "src", "data", "train_station_map.h")
CONST_H = os.path.join(ROOT, "include", "constants", "train_stations.h")
DATA_H = os.path.join(ROOT, "src", "data", "train_stations.h")

MAP_W, MAP_H = 64, 32                 # BG2 tilemap cells (512x256)
DIAGRAM_TILE_BUDGET = 512
HEADER_ROWS = (0, 15)
TRAY_ROWS = (128, 159)
TRAY_Y = 128
LEGEND_Y = 4                          # screen y of the 16x8 legend tube OBJs
LEGEND_RIGHT = 236                    # legend block ends here
TITLE = "TOSA RAIL"

# BG palette slots (fixed by the screen spec)
PAL_ORCHID, PAL_SEA, PAL_FOREST, PAL_GREY, PAL_SELECTED, PAL_GRID = range(6)
RAMPS = {   # ACCENT_DARK, ACCENT, ACCENT_LIGHT, ACCENT_PALE
    PAL_ORCHID: THEMES["orchid"],
    PAL_SEA: SM.SEA,
    PAL_FOREST: [(40, 104, 64), (72, 160, 88), (144, 208, 136), (216, 240, 200)],
    PAL_GREY: SM.GREY,
}
BACKDROP = GRID_PAL[1]                # BG palette 0 colour 0 = screen backdrop


def fail(msg):
    print("export_station_map: ERROR: " + msg, file=sys.stderr)
    sys.exit(1)


# ------------------------------------------------------------------ input + validation
def load_network():
    net = json.load(open(NET))
    src = open(CONST_H).read()
    defs = dict((m.group(1), int(m.group(2), 0)) for m in
                re.finditer(r"#define\s+(TRAIN_STATION_\w+)\s+(\w+)", src) if re.match(r"^(0x[0-9A-Fa-f]+|\d+)$", m.group(2)))
    count = defs.pop("TRAIN_STATION_COUNT", None)
    if count is None:
        fail("TRAIN_STATION_COUNT not found in " + CONST_H)
    ids = {k: v for k, v in defs.items() if k != "TRAIN_STATION_NONE" and not k.startswith("TRAIN_STATION_STATE_")}
    if sorted(ids.values()) != list(range(count)):
        fail("station ids in %s are not 0..%d: %s" % (CONST_H, count - 1, ids))
    st = net["stations"]
    got = [s["id"] for s in st]
    if len(got) != len(set(got)):
        fail("duplicate station ids in network.json")
    if set(got) != set(ids):
        fail("network.json stations %s != constants %s" % (sorted(got), sorted(ids)))
    if len(st) != count:
        fail("network.json has %d stations, TRAIN_STATION_COUNT = %d" % (len(st), count))
    # display names from src/data/train_stations.h
    data = open(DATA_H).read()
    strings = dict(re.findall(r'static const u8 (\w+)\[\]\s*=\s*_\("([^"]*)"\)', data))
    names = {}
    heads = [m for m in re.finditer(r"\[(TRAIN_STATION_\w+)\]\s*=\s*\{", data) if m.group(1) != "TRAIN_STATION_COUNT"]
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(data)
        nm = re.search(r"\.name\s*=\s*(\w+)", data[m.end():end])
        if nm and nm.group(1) in strings:
            names[m.group(1)] = strings[nm.group(1)]
    for s in st:
        if names.get(s["id"]) != s["name"]:
            fail("%s: network.json name %r != src/data/train_stations.h %r" % (s["id"], s["name"], names.get(s["id"])))
    st.sort(key=lambda s: ids[s["id"]])
    for s in st:
        s["num"] = ids[s["id"]]
        if s["x"] % 8 != 4 or s["y"] % 8 != 4:
            fail("%s node (%d,%d) is not on a cell centre (8k+4)" % (s["id"], s["x"], s["y"]))
    lines = net["lines"]
    keys = [l["key"] for l in lines]
    if len(lines) > 4:
        fail("obj_lines.pal holds at most 4 lines")
    for l in lines:
        if l["bgPalette"] not in (PAL_ORCHID, PAL_SEA, PAL_FOREST):
            fail("line %s: bgPalette must be 0, 1 or 2" % l["key"])
    byid = {s["id"]: s for s in st}
    for e in net["edges"]:
        if e["a"] not in byid or e["b"] not in byid or e["a"] == e["b"]:
            fail("bad edge %s-%s" % (e["a"], e["b"]))
        if e["line"] not in keys:
            fail("edge %s-%s: unknown line %s" % (e["a"], e["b"], e["line"]))
        pts = edge_points(e, byid)
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            dx, dy = abs(bx - ax), abs(by - ay)
            if not (dx == 0 or dy == 0 or dx == dy):
                fail("edge %s-%s: run (%d,%d)->(%d,%d) is not 0/45/90 degrees" % (e["a"], e["b"], ax, ay, bx, by))
            for x, y in ((ax, ay), (bx, by)):
                if x % 8 != 4 or y % 8 != 4:
                    fail("edge %s-%s: waypoint (%d,%d) not on a cell centre" % (e["a"], e["b"], x, y))
    for s in st:
        s["lines"] = [i for i, l in enumerate(lines)
                      if any(e["line"] == l["key"] and s["id"] in (e["a"], e["b"]) for e in net["edges"])]
    return net, st, lines, byid


def edge_points(e, byid):
    a, b = byid[e["a"]], byid[e["b"]]
    return [(a["x"], a["y"])] + [tuple(p) for p in e["via"]] + [(b["x"], b["y"])]


# ------------------------------------------------------------------ palettes
def bg_palettes():
    pals = []
    for slot in (PAL_ORCHID, PAL_SEA, PAL_FOREST, PAL_GREY):
        THEMES["_x"] = RAMPS[slot]
        p = palette("_x")
        if slot == PAL_GREY:
            p[WHITE] = p[INK_SOFT]                    # greyed label text
        pals.append(p)
    sel = palette("orchid")
    sel[WHITE], sel[INK] = sel[INK], sel[SELECT_DARK]  # selected label: ink text, gold-dark shadow
    pals.append(sel)
    grid = [snap(c) for c in GRID_PAL] + [(0, 0, 0)] * (16 - len(GRID_PAL))
    pals.append(grid)
    for p in pals:
        p[0] = snap(BACKDROP)
    return pals


def obj_pal_a():
    return palette("orchid", spare_a=ARROW_RED[0], spare_b=ARROW_RED[1], key=(115, 197, 164))


OL_INK, OL_WHITE, OL_SHADE = 1, 2, 3          # obj_lines.pal; line i ramp at 4+3i: light, face, dark


def obj_pal_b(lines):
    p = [snap((115, 197, 164)), snap(K._NEUTRAL[INK]), snap(K._NEUTRAL[WHITE]), snap(K._NEUTRAL[PANEL_SHADE])]
    for l in lines:
        d, f, li, _ = RAMPS[l["bgPalette"]]
        p += [snap(li), snap(f), snap(d)]
    return p + [(0, 0, 0)] * (16 - len(p))


def p_image(w, h, pal):
    im = Image.new("P", (w, h), 0)
    flat = [v for c in pal[:16] for v in c]
    im.putpalette(flat + [0] * (48 - len(flat)))
    return im


def save_png(im, path):
    im.save(path, bits=4, optimize=False)


def write_jasc(path, pal):
    with open(path, "w", newline="\n") as f:
        f.write("JASC-PAL\r\n0100\r\n%d\r\n" % len(pal))
        for c in pal:
            f.write("%d %d %d\r\n" % c)


def write_tilemap(path, entries):
    with open(path, "wb") as f:
        for (t, hf, vf, pal) in entries:
            f.write(struct.pack("<H", (t & 0x3FF) | (hf << 10) | (vf << 11) | (pal << 12)))


# ------------------------------------------------------------------ diagram (BG2)
def label_geom(s):
    anchor, dx, dy = s["label"]
    w = text_width(s["name"], "small")
    if anchor == "c":
        tx = s["x"] - w // 2 + dx
    elif anchor == "l":
        tx = s["x"] + dx - w
    else:
        tx = s["x"] + dx
    ty = s["y"] + dy - 1
    pw = ((w + 10 + 7) // 8) * 8                     # pill = whole 8px OBJ pieces, >= 5px margin
    px = tx - (pw - w) // 2
    return tx, ty, w, px, pw


def build_diagram(net, st, lines, byid):
    CW, CH = net["canvas"]
    if (CW, CH) != (512, 256):
        fail("canvas must be 512x256 (one 64x32 BG2 map)")
    im = p_image(CW, CH, bg_palettes()[0])
    cv = Canvas(im)
    edge_px = []
    fill_all, out_all = set(), set()
    for e in net["edges"]:
        f, o = SM.line_masks([edge_points(e, byid)], CW, CH)
        edge_px.append(f | o)
        fill_all |= f
        out_all |= o
    SM.draw_lines(cv, fill_all, out_all - fill_all)
    tube_img = im.copy()
    for s in st:
        tx, ty, w, px, pw = label_geom(s)
        if tx < 0 or tx + w > CW or ty < 0 or ty + 16 > CH:
            fail("%s label off the canvas" % s["id"])
        draw_text(cv, tx, ty, s["name"], WHITE, INK, font="small")
    # cell attribution
    ipx, tpx = im.load(), tube_img.load()
    label_cells = {}
    for s in st:
        tx, ty, w, _, _ = label_geom(s)
        cells = set()
        for y in range(ty, ty + 16):
            for x in range(tx - 1, tx + w + 1):
                if 0 <= x < CW and 0 <= y < CH and ipx[x, y] != tpx[x, y]:
                    cells.add((x // 8, y // 8))
        label_cells[s["id"]] = sorted(cells, key=lambda c: (c[1], c[0]))
    edge_cells = [sorted({(x // 8, y // 8) for (x, y) in pxs}, key=lambda c: (c[1], c[0])) for pxs in edge_px]
    node_cells = {(s["x"] // 8, s["y"] // 8) for s in st}
    all_label = {c: sid for sid, cs in label_cells.items() for c in cs}
    owner = {}
    for i, cs in enumerate(edge_cells):
        for c in cs:
            if c in all_label:
                fail("cell %s holds both label (%s) and tube pixels (edge %d)" % (c, all_label[c], i))
            if c in owner and c not in node_cells:
                fail("cell %s is shared by edges %d and %d and is not a station centre cell" % (c, owner[c], i))
            owner.setdefault(c, i)
    for sid, cs in label_cells.items():
        for c in cs:
            if all_label[c] != sid:
                fail("labels %s and %s share cell %s" % (sid, all_label[c], c))
    tiles, tm = to_tiles(im)
    if len(tiles) > DIAGRAM_TILE_BUDGET:
        fail("diagram uses %d tiles > %d" % (len(tiles), DIAGRAM_TILE_BUDGET))
    line_pal = {l["key"]: l["bgPalette"] for l in lines}
    entries = []
    for i, (t, hf, vf) in enumerate(tm):
        c = (i % MAP_W, i // MAP_W)
        pal = PAL_ORCHID
        if c in owner:
            pal = line_pal[net["edges"][owner[c]]["line"]]
        entries.append((t, hf, vf, pal))
    sb = []
    for block in (0, 1):
        for y in range(MAP_H):
            for x in range(block * 32, block * 32 + 32):
                sb.append(entries[y * MAP_W + x])
    return dict(img=im, tiles=tiles, entries=entries, sb=sb, label_cells=label_cells,
                edge_cells=edge_cells, fill_all=fill_all)


# ------------------------------------------------------------------ frame (BG1)
def legend_layout(lines):
    widths = [15 + text_width(l["name"], "small") for l in lines]
    total = sum(widths) + 6 * (len(lines) - 1)
    x = LEGEND_RIGHT - total
    xs = []
    for w in widths:
        xs.append(x)
        x += w + 6
    return xs


def build_frame(lines):
    im = p_image(256, 256, bg_palettes()[0])
    cv = Canvas(im)
    cv.rect(0, 0, 255, 13, ACCENT)
    cv.hline(0, 255, 0, ACCENT_LIGHT)
    cv.hline(0, 255, 14, ACCENT_DARK)
    cv.hline(0, 255, 15, INK)
    SM.train_glyph(cv, 6, 2)
    title_end = draw_text(cv, 22, -1, TITLE, WHITE, ACCENT_DARK)
    xs = legend_layout(lines)
    if xs and xs[0] < title_end + 8:
        fail("legend collides with the title")
    for x, l in zip(xs, lines):
        draw_text(cv, x + 15, -2, l["name"], WHITE, ACCENT_DARK, font="small")
    SM.tray(cv, TRAY_Y, 159, 0, 255)
    px = im.load()
    for (y0, y1) in (HEADER_ROWS, TRAY_ROWS):
        for y in range(y0, y1 + 1):
            for x in range(240):
                if px[x, y] == 0:
                    fail("frame pixel (%d,%d) is transparent; header/tray must be opaque" % (x, y))
    for y in range(16, 128):
        for x in range(256):
            if px[x, y]:
                fail("frame row %d not transparent" % y)
    tiles, tm = to_tiles(im)
    return im, tiles, [(t, hf, vf, PAL_ORCHID) for (t, hf, vf) in tm], xs


# ------------------------------------------------------------------ OBJ sheets
def _ring(cv, oy, face, light, dark, rim):
    for y in range(16):
        for x in range(16):
            d = ((x + 0.5 - 8) ** 2 + (y + 0.5 - 8) ** 2) ** 0.5
            if 4.6 < d <= 8.0:
                if d > 7.0 or d <= 5.6:
                    c = rim
                else:
                    s_ = (x + 0.5 - 8) + (y + 0.5 - 8)
                    c = light if s_ < -4 else dark if s_ > 4 else face
                cv.set(x, oy + y, c)


def build_nodes():
    pal = obj_pal_a()
    im = p_image(16, 16 * 6, pal)
    cv = Canvas(im)
    disc(cv, 8, 8, 5, WHITE, INK, WHITE, PANEL_SHADE)                       # 0 visited
    cv.set(6, 6, WHITE)
    disc(cv, 8, 24, 5, PANEL_DARK, INK, PANEL_SHADE, INK_SOFT)               # 1 grey
    disc(cv, 8, 40, 6, WHITE, INK, WHITE, PANEL_SHADE)                       # 2 interchange
    ring(cv, 8, 40, 3, INK)
    disc(cv, 8, 56, 6, PANEL_DARK, INK, PANEL_SHADE, INK_SOFT)               # 3 interchange grey
    ring(cv, 8, 56, 3, INK)
    _ring(cv, 64, SELECT, SELECT_LIGHT, SELECT_DARK, INK)                    # 4 gold ring
    _ring(cv, 80, PANEL_DARK, PANEL_SHADE, INK_SOFT, INK)                    # 5 grey ring
    return im, pal


def build_chevron():
    """16x16 frames (DEVIATION from 8x8: the approved 6x9 chevron does not fit 8x8).
    frame 0 = right, art x 5..10, y 4..12 ; frame 1 = down, art x 4..12, y 5..10."""
    pal = obj_pal_a()
    im = p_image(16, 32, pal)
    cv = Canvas(im)
    cmap = {"O": SPARE_B, "F": SPARE_A}
    stamp(cv, 5, 4, SMALL_ARROW, cmap, hflip=True)
    down = ["".join(r[c] for r in SMALL_ARROW) for c in range(len(SMALL_ARROW[0]))][::-1]
    stamp(cv, 4, 16 + 5, down, cmap)
    return im, pal


def build_pill():
    pal = obj_pal_a()
    wide = p_image(24, 16, pal)
    rounded_box(Canvas(wide), 0, 1, 24, 14, 4, SELECT, INK, SELECT_LIGHT, SELECT_DARK)
    im = p_image(8, 48, pal)
    for i in range(3):
        im.paste(wide.crop((i * 8, 0, i * 8 + 8, 16)), (0, i * 16))
    return im, pal


def _remap_lines(src, dst, oy, line_i):
    """Kit-role drawing -> obj_lines.pal indices."""
    m = {INK: OL_INK, WHITE: OL_WHITE, PANEL_SHADE: OL_SHADE}
    if line_i is not None:
        m.update({ACCENT_LIGHT: 4 + 3 * line_i, ACCENT: 5 + 3 * line_i, ACCENT_DARK: 6 + 3 * line_i})
    sp, dp = src.load(), dst.load()
    for y in range(src.size[1]):
        for x in range(src.size[0]):
            v = sp[x, y]
            if v:
                dp[x, oy + y] = m[v]


def build_legend(lines):
    pal = obj_pal_b(lines)
    im = p_image(16, 8 * len(lines), pal)
    for i in range(len(lines)):
        t = new_sheet(16, 8)
        f, o = SM.line_masks([[(3, 4), (11, 4)]], 16, 8, 1.6, 2.6)
        SM.draw_lines(Canvas(t), f, o)
        _remap_lines(t, im, 8 * i, i)
    return im, pal


def build_tray_line(lines):
    pal = obj_pal_b(lines)
    im = p_image(16, 16 * (len(lines) + 1), pal)
    for i in range(len(lines) + 1):
        t = new_sheet(16, 16)
        cv = Canvas(t)
        if i < len(lines):
            f, o = SM.line_masks([[(3, 8), (13, 8)]], 16, 16, 2.0, 3.0)
            SM.draw_lines(cv, f, o)
            disc(cv, 8, 8, 5, WHITE, INK, WHITE, PANEL_SHADE)
            cv.set(6, 6, WHITE)
            _remap_lines(t, im, 16 * i, i)
        else:
            disc(cv, 8, 8, 6, WHITE, INK, WHITE, PANEL_SHADE)       # interchange: ringed node, no tube
            ring(cv, 8, 8, 3, INK)
            _remap_lines(t, im, 16 * i, None)
    return im, pal


# ------------------------------------------------------------------ header (.h)
def c_header(st, lines, net, D, legend_xs):
    L = ["// Generated by dev_scripts/train_ui/export_station_map.py from dev_scripts/train_ui/network.json",
         "// do not edit — change network.json and rerun the exporter.",
         "",
         "#define TRAIN_MAP_CANVAS_W %d" % net["canvas"][0],
         "#define TRAIN_MAP_CANVAS_H %d" % net["canvas"][1],
         "#define TRAIN_MAP_LINE_COUNT %d" % len(lines),
         "#define TRAIN_MAP_EDGE_COUNT %d" % len(net["edges"]),
         "",
         "struct TrainMapStation { u16 x, y; u8 lineMask; bool8 interchange; s16 labelX, labelY; u8 labelW; u16 labelCellsStart; u8 labelCellsCount; };",
         "struct TrainMapEdge { u8 a, b, line; u16 cellsStart; u16 cellsCount; };",
         "",
         "static const u8 *const sTrainMapLineNames[TRAIN_MAP_LINE_COUNT] = { %s };"
         % ", ".join('(const u8[])_("%s")' % l["name"] for l in lines),
         ""]
    cells, rows = [], []
    for s in st:
        _, ty, _, px, pw = label_geom(s)
        lc = D["label_cells"][s["id"]]
        mask = sum(1 << i for i in s["lines"])
        rows.append("    [%s] = { .x = %d, .y = %d, .lineMask = 0x%02X, .interchange = %s, .labelX = %d, .labelY = %d, "
                    ".labelW = %d, .labelCellsStart = %d, .labelCellsCount = %d },"
                    % (s["id"], s["x"], s["y"], mask, "TRUE" if len(s["lines"]) > 1 else "FALSE",
                       px, ty, pw, len(cells), len(lc)))
        cells += [y * MAP_W + x for (x, y) in lc]
    L.append("static const struct TrainMapStation sTrainMapStations[TRAIN_STATION_COUNT] =\n{")
    L += rows
    L.append("};\n")
    L.append("// tilemap cell index = y*64 + x (canvas tile coords, NOT screenblock order)")
    L.append("static const u16 sTrainMapLabelCells[] =\n{")
    L += ["    " + ", ".join(str(v) for v in cells[i:i + 16]) + "," for i in range(0, len(cells), 16)]
    L.append("};\n")
    key_i = {l["key"]: i for i, l in enumerate(lines)}
    ecells, erows = [], []
    for e, cs in zip(net["edges"], D["edge_cells"]):
        erows.append("    { .a = %s, .b = %s, .line = %d, .cellsStart = %d, .cellsCount = %d },"
                     % (e["a"], e["b"], key_i[e["line"]], len(ecells), len(cs)))
        ecells += [y * MAP_W + x for (x, y) in cs]
    L.append("static const struct TrainMapEdge sTrainMapEdges[TRAIN_MAP_EDGE_COUNT] =\n{")
    L += erows
    L.append("};\n")
    L.append("// tube cells for each edge, same indexing")
    L.append("static const u16 sTrainMapEdgeCells[] =\n{")
    L += ["    " + ", ".join(str(v) for v in ecells[i:i + 16]) + "," for i in range(0, len(ecells), 16)]
    L.append("};\n")
    L.append("// screen x of each legend tube OBJ (y = header)")
    L.append("static const u8 sTrainMapLegendX[TRAIN_MAP_LINE_COUNT] = { %s };" % ", ".join(str(x) for x in legend_xs))
    L.append("#define TRAIN_MAP_LEGEND_Y %d" % LEGEND_Y)
    return "\n".join(L) + "\n"


# ------------------------------------------------------------------ decode-from-export check
def decode_tiles(png):
    im = Image.open(png)
    px = im.load()
    n = (im.size[0] // 8) * (im.size[1] // 8)
    per = im.size[0] // 8
    return [[px[(i % per) * 8 + x, (i // per) * 8 + y] for y in range(8) for x in range(8)] for i in range(n)]


def read_pal(path):
    v = open(path).read().split()
    n = int(v[2])
    nums = list(map(int, v[3:3 + 3 * n]))
    return [tuple(nums[i:i + 3]) for i in range(0, len(nums), 3)]


def read_map(path):
    d = open(path, "rb").read()
    return [struct.unpack("<H", d[i:i + 2])[0] for i in range(0, len(d), 2)]


def draw_bg(out, tiles, cells, pals, w_cells, scroll=(0, 0), opaque=False):
    """cells = row-major list of u16 entries (w_cells wide). Draws a 240x160 BG view."""
    ox, oy = scroll
    h_cells = len(cells) // w_cells
    W_, H_ = w_cells * 8, h_cells * 8
    p = out.load()
    for sy in range(160):
        for sx in range(240):
            x, y = (sx + ox) % W_, (sy + oy) % H_
            e = cells[(y // 8) * w_cells + x // 8]
            t, hf, vf, pl = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1, e >> 12
            tx, ty = x % 8, y % 8
            if hf:
                tx = 7 - tx
            if vf:
                ty = 7 - ty
            v = tiles[t][ty * 8 + tx]
            if v or opaque:
                p[sx, sy] = pals[pl * 16 + v] + (255,)


def sb_to_rowmajor(sb):
    out = [0] * (64 * 32)
    for block in (0, 1):
        for y in range(32):
            for x in range(32):
                out[y * 64 + block * 32 + x] = sb[block * 1024 + y * 32 + x]
    return out


def obj(out, png, pal, frame, fh, x, y, hflip=False, vflip=False):
    im = Image.open(png)
    fw = im.size[0]
    fr = im.crop((0, frame * fh, fw, frame * fh + fh))
    if hflip:
        fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
    if vflip:
        fr = fr.transpose(Image.FLIP_TOP_BOTTOM)
    rgba = Image.new("RGBA", fr.size, (0, 0, 0, 0))
    sp, dp = fr.load(), rgba.load()
    for yy in range(fr.size[1]):
        for xx in range(fr.size[0]):
            if sp[xx, yy]:
                dp[xx, yy] = pal[sp[xx, yy]] + (255,)
    out.alpha_composite(rgba, (x, y))


def export_check(st, lines, net, D, legend_xs, cam, cursor, accessible, path):
    """Rebuild a frame purely from the exported files, applying the runtime palette rules."""
    pals = read_pal(os.path.join(GFX, "bg.pal"))
    oa = read_pal(os.path.join(GFX, "obj.pal"))
    ob = read_pal(os.path.join(GFX, "obj_lines.pal"))
    out = Image.new("RGBA", (240, 160), pals[0] + (255,))
    # BG3 grid
    draw_bg(out, decode_tiles(os.path.join(GFX, "grid.png")), read_map(os.path.join(GFX, "grid.bin")), pals, 32,
            scroll=(cam[0] % 256, (cam[1] - 16) % 256))
    # BG2 diagram with runtime palette rules
    cells = sb_to_rowmajor(read_map(os.path.join(GFX, "diagram.bin")))
    byid = {s["id"]: s for s in st}
    for e, cs in zip(net["edges"], D["edge_cells"]):
        if not (e["a"] in accessible and e["b"] in accessible):
            for (x, y) in cs:
                i = y * 64 + x
                cells[i] = (cells[i] & 0x0FFF) | (PAL_GREY << 12)
    for s in st:
        p = PAL_SELECTED if s["id"] == cursor else (PAL_ORCHID if s["id"] in accessible else PAL_GREY)
        for (x, y) in D["label_cells"][s["id"]]:
            i = y * 64 + x
            cells[i] = (cells[i] & 0x0FFF) | (p << 12)
    # pill OBJs (prio 2) go under BG2: draw them first
    s = byid[cursor]
    _, ty, _, px, pw = label_geom(s)
    pill = os.path.join(GFX, "pill.png")
    for i in range(pw // 8):
        fr = 0 if i == 0 else (2 if i == pw // 8 - 1 else 1)
        obj(out, pill, oa, fr, 16, px + 8 * i - cam[0], ty - cam[1] + 16)
    draw_bg(out, decode_tiles(os.path.join(GFX, "diagram.png")), cells, pals, 64, scroll=(cam[0], (cam[1] - 16) % 256))
    # nodes + ring (prio 1)
    nodes = os.path.join(GFX, "nodes.png")
    for s in st:
        inter = len(s["lines"]) > 1
        fr = (2 if inter else 0) + (0 if s["id"] in accessible else 1)
        obj(out, nodes, oa, fr, 16, s["x"] - 8 - cam[0], s["y"] - 8 - cam[1] + 16)
    s = byid[cursor]
    obj(out, nodes, oa, 4, 16, s["x"] - 8 - cam[0], s["y"] - 8 - cam[1] + 16)
    # chevrons (cell rule from IMPLEMENTATION.md)
    chev = os.path.join(GFX, "chevron.png")
    for side, x, y in chevrons_cell_rule(D["edge_cells"], cam):
        if side == "right":
            obj(out, chev, oa, 0, 16, 226, y - 8)
        elif side == "left":
            obj(out, chev, oa, 0, 16, -2, y - 8, hflip=True)
        elif side == "down":
            obj(out, chev, oa, 1, 16, x - 8, 113)
        else:
            obj(out, chev, oa, 1, 16, x - 8, 14, vflip=True)
    # BG1 frame (prio 0, opaque header/tray) hides map OBJs under it
    draw_bg(out, decode_tiles(os.path.join(GFX, "frame.png")), read_map(os.path.join(GFX, "frame.bin")), pals, 32)
    # header/tray OBJs (prio 0)
    for i, x in enumerate(legend_xs):
        obj(out, os.path.join(GFX, "legend.png"), ob, i, 8, x, LEGEND_Y)
    trf = len(lines) if len(s["lines"]) > 1 else s["lines"][0]
    obj(out, os.path.join(GFX, "tray_line.png"), ob, trf, 16, 5, 131)
    # BG0 text stand-in (what the C side prints)
    lay = new_sheet(240, 160)
    cv = Canvas(lay)
    draw_text(cv, 24 + 2, 128 + 1, s["name"], INK, PANEL_SHADE)
    names = [lines[i]["name"] for i in s["lines"]]
    draw_text(cv, 24 + 2, 144, " + ".join(names) + (" LINES" if len(names) > 1 else " LINE"), INK_SOFT, PANEL_SHADE, font="small")
    x = 136 + 6
    x = draw_button(cv, x, 148, "A") + 3
    x = draw_text(cv, x, 144, "DEPART", INK, PANEL_SHADE, font="small") + 8
    x = draw_button(cv, x, 148, "B") + 3
    draw_text(cv, x, 144, "CANCEL", INK, PANEL_SHADE, font="small")
    out.alpha_composite(KX.sheet_rgba(lay))
    KX.upscale(out.convert("RGB"), 3).save(path)


def chevrons_cell_rule(edge_cells, cam):
    """Per side, per edge: a tube cell on the last visible cell column/row whose neighbour just
    outside the viewport is a cell of the same edge -> one chevron at that cell's centre."""
    cx, cy = cam
    vis_c0, vis_c1 = cx // 8, (cx + 239) // 8
    vis_r0, vis_r1 = cy // 8, (cy + 111) // 8
    res = []
    for cs in edge_cells:
        s = set(cs)
        for side, (dc, dr) in (("right", (1, 0)), ("left", (-1, 0)), ("down", (0, 1)), ("up", (0, -1))):
            hits = []
            for (c, r) in cs:
                if not (vis_c0 <= c <= vis_c1 and vis_r0 <= r <= vis_r1):
                    continue
                if side == "right" and c != vis_c1 or side == "left" and c != vis_c0:
                    continue
                if side == "down" and r != vis_r1 or side == "up" and r != vis_r0:
                    continue
                if (c + dc, r + dr) in s:
                    hits.append((c, r))
            if hits:
                c, r = hits[len(hits) // 2]
                res.append((side, c * 8 + 4 - cx, r * 8 + 4 - cy + 16))
    return res


# ------------------------------------------------------------------ main
def main():
    net, st, lines, byid = load_network()
    os.makedirs(GFX, exist_ok=True)
    pals = bg_palettes()
    write_jasc(os.path.join(GFX, "bg.pal"), [c for p in pals for c in p])
    # grid
    g = p_image(16, 16, pals[PAL_GRID])
    from backdrop import grid_index
    gp = g.load()
    for y in range(16):
        for x in range(16):
            gp[x, y] = grid_index(x, y)
    save_png(g, os.path.join(GFX, "grid.png"))
    write_tilemap(os.path.join(GFX, "grid.bin"),
                  [((y & 1) * 2 + (x & 1), 0, 0, PAL_GRID) for y in range(32) for x in range(32)])
    # diagram
    D = build_diagram(net, st, lines, byid)
    save_png(tiles_to_image(D["tiles"], p_image(8, 8, pals[0]), per_row=16), os.path.join(GFX, "diagram.png"))
    write_tilemap(os.path.join(GFX, "diagram.bin"), D["sb"])
    # frame
    fim, ftiles, fentries, legend_xs = build_frame(lines)
    save_png(tiles_to_image(ftiles, p_image(8, 8, pals[0]), per_row=16), os.path.join(GFX, "frame.png"))
    write_tilemap(os.path.join(GFX, "frame.bin"), fentries)
    # OBJ
    nodes, pa = build_nodes()
    save_png(nodes, os.path.join(GFX, "nodes.png"))
    save_png(build_chevron()[0], os.path.join(GFX, "chevron.png"))
    save_png(build_pill()[0], os.path.join(GFX, "pill.png"))
    leg, pb = build_legend(lines)
    save_png(leg, os.path.join(GFX, "legend.png"))
    save_png(build_tray_line(lines)[0], os.path.join(GFX, "tray_line.png"))
    write_jasc(os.path.join(GFX, "obj.pal"), pa)
    write_jasc(os.path.join(GFX, "obj_lines.pal"), pb)
    # header
    open(HDR, "w", newline="\n").write(c_header(st, lines, net, D, legend_xs))
    # checks rendered back from the exported files
    ensure_out()
    acc = {"TRAIN_STATION_TEST_WEST", "TRAIN_STATION_TEST_EAST"}

    def centre(sid):
        s = byid[sid]
        return (max(0, min(512 - 240, s["x"] - 120)), max(0, min(256 - 112, s["y"] - 56)))
    export_check(st, lines, net, D, legend_xs, centre("TRAIN_STATION_TEST_WEST"), "TRAIN_STATION_TEST_WEST", acc,
                 os.path.join(OUT, "export_check_west_3x.png"))
    export_check(st, lines, net, D, legend_xs, centre("TRAIN_STATION_TEST_EAST"), "TRAIN_STATION_TEST_EAST", acc,
                 os.path.join(OUT, "export_check_east_3x.png"))
    export_check(st, lines, net, D, legend_xs, centre("TRAIN_STATION_TEST_NORTH"), "TRAIN_STATION_TEST_NORTH",
                 acc | {"TRAIN_STATION_TEST_NORTH"}, os.path.join(OUT, "export_check_north_3x.png"))
    print("diagram: %d tiles (budget %d), frame: %d tiles, label cells: %d, edge cells: %d"
          % (len(D["tiles"]), DIAGRAM_TILE_BUDGET, len(ftiles),
             sum(len(v) for v in D["label_cells"].values()), sum(len(c) for c in D["edge_cells"])))
    print("legend x:", legend_xs, "y:", LEGEND_Y)
    for s in st:
        _, ty, w, px, pw = label_geom(s)
        print("%-26s node (%d,%d) lines %s label pill x=%d y=%d w=%d" % (s["id"], s["x"], s["y"], s["lines"], px, ty, pw))
    print("ok")


if __name__ == "__main__":
    main()
