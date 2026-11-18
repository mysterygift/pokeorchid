"""MAP app / region map mockups: the user's Tosa art + Orchid kit + Tosa Rail line-map cues.
usage: mock_map.py OUT_DIR"""
import os
import struct
import sys

KIT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KIT)
from PIL import Image
import kit
from kit import *
import kit_ext as K
import system_ext as X
import dex_ext as D
from gamefont import draw_text, text_width

W, H = 240, 160
REF = os.path.join(KIT, "ref")
GX, GY = 8, 16                     # cursor grid origin (region_map.c)
MAP_Y0, MAP_Y1 = 16, 135
NAMES = {4: "Tosa Port", 10: "Telok Town", 1: "Town 01", 3: "Site 03", 7: "Site 07", 11: "Site 11",
         12: "Town 12", 9: "Town 09", 8: "Town 08", 13: "Town 13", 14: "Town 14", 17: "Town 17"}
LANDMARKS = {3, 6, 7, 11, 15, 16, 18, 20}
VISITED = {4, 10, 1, 3, 11, 12}
HERE_NODE = 4

ROUTE_C = ((216, 152, 40), (240, 200, 80), (248, 232, 152))      # dark, face, light
GREY_C = ((128, 128, 112), (176, 176, 160), (216, 216, 200))
SEA_C = ((40, 96, 184), (72, 152, 224), (152, 208, 248))
RAIL = {"COAST": ((24, 104, 120), (48, 160, 168), (120, 208, 208)),
        "RIDGE": ((96, 48, 128), (152, 88, 184), (200, 152, 224))}
kit.THEMES["map"] = kit.THEMES["leaf"]


def load(name):
    return Image.open(os.path.join(REF, name)).convert("RGB").rotate(180)


def squares():
    orig = Image.open(os.path.join(REF, "tosa_towns.png")).convert("RGB")
    px = orig.load()
    found = []
    for y in range(0, H, 8):
        for x in range(0, W, 8):
            if px[x, y] == (255, 0, 0) and px[x + 7, y + 7] == (255, 0, 0):
                found.append((x, y))
    out = {}
    for n, (x, y) in enumerate(found, 1):
        nx, ny = W - 8 - x, H - 8 - y
        out[n] = ((nx - GX) // 8, (ny - GY) // 8)
    return out


def classify():
    """{cell: 'land'|'sea'} route cells from the user's routes layer."""
    rt = load("tosa_routes.png").load()
    cells = {}
    for cy in range(15):
        for cx in range(28):
            x0, y0 = GX + cx * 8, GY + cy * 8
            land = sea = 0
            for j in range(8):
                for i in range(8):
                    p = rt[x0 + i, y0 + j]
                    if p[0] > 200 and p[2] < 130 and p != (255, 0, 0):
                        land += 1
                    elif p == (72, 152, 224):
                        sea += 1
            if land >= 12:
                cells[(cx, cy)] = "land"
            elif sea >= 12:
                cells[(cx, cy)] = "sea"
    return cells


def components(cells, nodes):
    """Route components split at nodes -> {cell: set(node numbers touched)}."""
    node_at = {v: k for k, v in nodes.items()}
    seen, out = set(), {}
    for start in cells:
        if start in seen or start in node_at:
            continue
        comp, touched, stack = [], set(), [start]
        seen.add(start)
        while stack:
            c = stack.pop()
            comp.append(c)
            for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (c[0] + d[0], c[1] + d[1])
                if n in node_at:
                    touched.add(node_at[n])
                elif n in cells and n not in seen:
                    seen.add(n)
                    stack.append(n)
        for c in comp:
            out[c] = touched
    return out


def tube_layer(cells, nodes, rails=False):
    """RGBA overlay: 6px Gen 3 tubes along route cells (train-map style)."""
    comp = components(cells, nodes)
    node_cells = set(nodes.values())
    allc = set(cells) | node_cells
    groups = {}
    for c, kind in cells.items():
        touched = comp.get(c, set())
        ok = touched and touched <= VISITED
        groups.setdefault(SEA_C if kind == "sea" and ok else ROUTE_C if ok else GREY_C, set()).add(c)
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for ramp, group in sorted(groups.items(), key=lambda kv: kv[0] != GREY_C):
        mask = set()
        for (cx, cy) in group:
            x0, y0 = GX + cx * 8, GY + cy * 8
            for j in range(1, 7):
                for i in range(1, 7):
                    mask.add((x0 + i, y0 + j))
            for d in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                n = (cx + d[0], cy + d[1])
                if n in allc:
                    for j in range(1, 7):
                        for k in (7, 8) if d[0] > 0 or d[1] > 0 else (0, -1):
                            if d[0]:
                                mask.add((x0 + k, y0 + j))
                            else:
                                mask.add((x0 + j, y0 + k))
        px = out.load()
        dk, fc, lt = ramp
        for (x, y) in mask:
            if not (MAP_Y0 <= y <= MAP_Y1 and 0 <= x < W):
                continue
            edge = any((x + a, y + b) not in mask for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if edge:
                col = (40, 40, 64)
            elif (x - 1, y) not in mask or (x, y - 1) not in mask or (x - 1, y - 1) not in mask:
                col = lt
            elif (x + 1, y) not in mask or (x, y + 1) not in mask or (x + 1, y + 1) not in mask:
                col = dk
            else:
                col = fc
            px[x, y] = snap(col) + (255,)
    return out


def ctr(cell):
    return GX + cell[0] * 8 + 3.5, GY + cell[1] * 8 + 3.5


def rail_layer(nodes):
    """Placeholder rail overlay (SELECT): 4px line-coloured tubes node to node, L-shaped."""
    lines = {"COAST": [12, 11, 10, 4, 3, 1], "RIDGE": [10, 9, 8, 13]}
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = out.load()
    for name, seq in lines.items():
        dk, fc, lt = RAIL[name]
        mask = set()
        for a, b in zip(seq, seq[1:]):
            (ax, ay), (bx, by) = ctr(nodes[a]), ctr(nodes[b])
            ax, ay, bx, by = int(ax), int(ay), int(bx), int(by)
            pts = [(ax, ay), (bx, ay), (bx, by)] if name == "RIDGE" else [(ax, ay), (ax, by), (bx, by)]
            for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
                for x in range(min(x1, x2) - 3, max(x1, x2) + 3):
                    for y in range(min(y1, y2) - 3, max(y1, y2) + 3):
                        mask.add((x, y))
        for (x, y) in mask:
            if not (MAP_Y0 <= y <= MAP_Y1 and 0 <= x < W):
                continue
            edge = any((x + a, y + b) not in mask for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if edge:
                col = (40, 40, 64)
            elif (x, y - 1) not in mask or (x - 1, y) not in mask:
                col = lt
            elif (x, y + 1) not in mask or (x + 1, y) not in mask:
                col = dk
            else:
                col = fc
            px[x, y] = snap(col) + (255,)
    return out


def head():
    d = K.G("pokenav", "region_map")
    raw = open(os.path.join(d, "brendan_icon.gbapal"), "rb").read()
    pal = []
    for i in range(16):
        v = struct.unpack_from("<H", raw, i * 2)[0]
        pal.append(((v & 31) << 3, ((v >> 5) & 31) << 3, ((v >> 10) & 31) << 3))
    return K.sheet_rgba(Image.open(os.path.join(d, "brendan_icon.png")), pal)


RAIL_NODES = {12, 11, 10, 4, 3, 1, 9, 8, 13}


def node_layer(nodes, cursor, rails=False):
    s = Image.new("P", (W, H), 0)
    s.putpalette([c for rgb in kit.palette("map") for c in rgb] + [0] * (768 - 48))
    cv = Canvas(s)
    for n, cell in nodes.items():
        if rails and n not in RAIL_NODES:
            continue
        x, y = ctr(cell)
        vis = n in VISITED
        if n in LANDMARKS:
            face = WHITE if vis else PANEL_DARK
            stamp(cv, int(x) - 3, int(y) - 3, ["...k...", "..kwk..", ".kwwwk.", "kwwwwwk", ".kwwws.", "..kss..", "...k..."]
                  if vis else ["...k...", "..kmk..", ".kmmmk.", "kmmmmmk", ".kmmmk.", "..kmk..", "...k..."],
                  {"k": INK, "w": WHITE, "s": PANEL_SHADE, "m": PANEL_DARK})
        else:
            disc(cv, x, y, 4.6, WHITE if vis else PANEL_DARK, INK)
            if vis:
                cv.set(int(x) + 1, int(y) + 1, PANEL_SHADE)
                cv.set(int(x) + 2, int(y), PANEL_SHADE)
    if cursor is not None:
        x, y = ctr(nodes[cursor])
        ring(cv, x, y, 7.2, INK, 1.0)
        ring(cv, x, y, 6.2, SELECT, 1.2)
        ring(cv, x, y, 5.2, SELECT_DARK, 0.6)
    return K.sheet_rgba(s)


def name_pill(out, nodes, n):
    x, y = ctr(nodes[n])
    name = NAMES.get(n, "???")
    w = text_width(name, "narrow") + 10
    px = int(x) - w // 2
    px, py = int(x) + 9, int(y) - 7
    if px + w > W - 4:
        px = int(x) - 9 - w

    def fn(cv):
        rounded_box(cv, px, py, w, 13, 4, SELECT, INK, SELECT_LIGHT, SELECT_DARK)
        draw_text(cv, px + 5, py - 2, name, INK, SELECT_DARK, font="narrow")
    K.layer(out, fn, "map")


X.SIL.update({
    "map": ["XX.XX.XX", "XX.XX.XX", "XX.XX.XX", "XX.XX.XX", "XX.XX.XX", "XX.XX.XX"],
    "pc": ["..XXX..", "..XXX..", "XXXXXXX", "XXXXXXX", "XXXXXXX", "..XXX..", "..XXX.."],
    "mart": ["X......", "XXXXXXX", ".XXXXXX", ".XXXXX.", ".X...X."],
    "rail": [".XXXXX.", "XX...XX", "XXXXXXX", "X.XXX.X", "XXXXXXX", ".X...X."],
    "fly": ["X.....X", "XX...XX", "XXX.XXX", ".XXXXX.", "...X...", "..XXX.."],
})
CHIPS = {4: ["rail"], 10: ["rail"], 9: ["rail"]}   # rail station mark only


def frame(out, nodes, cursor, rails, fly=False):
    s = Image.new("P", (W, H), 0)
    s.putpalette([c for rgb in kit.palette("map") for c in rgb] + [0] * (768 - 48))
    cv = Canvas(s)
    D.header_band(cv, 0, 239, round_left=False)
    rounded_box(cv, 4, 2, 14, 12, 3, ACCENT_LIGHT, INK, WHITE, ACCENT)
    X.centred_sil(cv, 5, 3, 13, 10, "fly" if fly else "map", ACCENT_DARK, None)
    draw_text(cv, 23, 0, "FLY" if fly else "TOSA", WHITE, ACCENT_DARK)
    # thin ink rim under header / over tray, tray
    D.tray(cv, 136, seam=False)
    name = NAMES.get(cursor, "???")
    draw_text(cv, 8, 138, name, INK, PANEL_SHADE)
    cx = 236
    for key in reversed(CHIPS.get(cursor, [])):
        cx -= 20
        rounded_box(cv, cx, 141, 18, 14, 3, ACCENT, INK, ACCENT_LIGHT, ACCENT_DARK)
        X.centred_sil(cv, cx + 1, 142, 17, 12, key, WHITE, ACCENT_DARK)
    if fly:
        X.keypad(cv, cx - 58, 146, "A")
        draw_text(cv, cx - 46, 141, "Fly here", INK_SOFT, PANEL_SHADE, font="narrow")
    out.alpha_composite(K.sheet_rgba(s))


def render(cursor=HERE_NODE, rails=False, fly=False):
    nodes = squares()
    cells = classify()
    for c in nodes.values():
        cells.pop(c, None)
    out = Image.new("RGBA", (W, H))
    out.paste(load("tosa_terrain.png").convert("RGBA"))
    if rails:
        out.alpha_composite(Image.new("RGBA", (W, H), (24, 24, 32, 150)))
        out.alpha_composite(rail_layer(nodes))
    else:
        out.alpha_composite(tube_layer(cells, nodes))
    out.alpha_composite(node_layer(nodes, cursor, rails))
    hx, hy = ctr(nodes[HERE_NODE])
    out.alpha_composite(head(), (int(hx) - 8, int(hy) - 19))
    frame(out, nodes, cursor, rails, fly)
    return out


def before():
    im = load("tosa_terrain.png").convert("RGBA")
    for n in ("tosa_routes.png", "tosa_towns.png"):
        im.alpha_composite(load(n).convert("RGBA"))
    return im


def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    shots = {"40_map_here": render(4), "41_map_telok": render(10), "42_map_fly": render(12, fly=True),
             "43_map_before": before()}
    for k, im in shots.items():
        im.save(os.path.join(outdir, k + ".png"))
        K.upscale(im.convert("RGB"), 3).save(os.path.join(outdir, "x3_" + k + ".png"))


if __name__ == "__main__":
    main(sys.argv[1])
