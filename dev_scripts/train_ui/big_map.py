"""
TOSA RAIL — bigger network on a scrolling virtual canvas (round 2).

Canvas 512x256 px (= one 64x32-tile BG2 text map, 2 screenblocks). The map viewport is the
240x112 strip between the fixed header (y 0..15) and the fixed tray (y 128..159).

Layers proposed for the scrolling version:
  BG0  text: header title, tray name/line/hints, messages, YES/NO          (fixed, prio 0)
  BG1  chrome: header band + tray art, std window frames                   (fixed, prio 0)
  BG2  diagram: tubes + station labels baked into tiles, 64x32 map          (scrolls, prio 1)
       BG2HOFS = camX, BG2VOFS = camY - 16
  BG3  grid: follows the pan 1:1 plus the usual 1px/4f diagonal drift      (prio 3)
  OBJ  nodes, ring, head (prio 1, in front of BG2), gold name pill (prio 2, BEHIND BG2 so the
       baked label text sits on top of it), edge chevrons; WIN0 = map viewport clips OBJs so
       nothing scrolls over the header/tray.

Camera rule (recommended): DEAD ZONE + RE-CENTRE. The camera holds still while the selected
station is inside a safe box; when the cursor lands outside it, the camera eases (16 frames,
ease-out, clamped to the canvas) to centre that station. Neighbour hops therefore don't move the
whole diagram, and a pan always leaves equal context on every side of the new station.
"""
from common import *
import station_map as M
from backdrop import GRID_PAL, grid_index

CW, CH = 512, 256
VX, VY, VW, VH = 0, 16, 240, 112           # map viewport on screen
SAFE = dict(l=48, r=48, t=24, b=32)        # dead-zone margins inside the viewport
CAM_EASE = 16                              # frames for a re-centre pan
RING_TRAVEL = 8

THEMES.setdefault("rail_forest", [(40, 104, 64), (72, 160, 88), (144, 208, 136), (216, 240, 200)])
LINE_THEME = {"coast": "rail_sea", "ridge": "orchid", "forest": "rail_forest", "grey": "rail_grey"}
LINE_LABEL = {"coast": "COAST", "ridge": "RIDGE", "forest": "FOREST"}

# name: (x, y, lines, label (anchor, dx, dy))   — all on 8px cell centres (8k+4)
STATIONS = {
    "TOSA PORT":     (36, 220, ("coast",), ("c", 0, 6)),
    "MARIS BAY":     (100, 220, ("coast",), ("c", 0, 6)),
    "VALE JUNCTION": (172, 172, ("coast", "ridge"), ("r", 6, 6)),
    "SALT FLATS":    (252, 172, ("coast",), ("c", 0, -18)),
    "KORU CITY":     (340, 172, ("coast", "forest"), ("l", -7, 6)),
    "CORAL END":     (452, 204, ("coast",), ("c", 0, 6)),
    "TELOK TOWN":    (172, 108, ("ridge", "forest"), ("r", 6, 6)),
    "ASHEN PASS":    (236, 44, ("ridge",), ("c", 0, 6)),
    "CINDER PEAK":   (332, 44, ("ridge",), ("c", 0, 6)),
    "GALE POINT":    (452, 76, ("ridge",), ("c", 0, 6)),
    "ELDER WOOD":    (44, 60, ("forest",), ("r", 8, -5)),
    "MOSS HOLLOW":   (100, 108, ("forest",), ("c", 0, -18)),
    "FERN GATE":     (268, 108, ("forest",), ("c", 0, -18)),
}
EDGES = [
    ("TOSA PORT", "MARIS BAY", "coast", []),
    ("MARIS BAY", "VALE JUNCTION", "coast", [(124, 220)]),
    ("VALE JUNCTION", "SALT FLATS", "coast", []),
    ("SALT FLATS", "KORU CITY", "coast", []),
    ("KORU CITY", "CORAL END", "coast", [(372, 204)]),
    ("VALE JUNCTION", "TELOK TOWN", "ridge", []),
    ("TELOK TOWN", "ASHEN PASS", "ridge", [(172, 76), (204, 44)]),
    ("ASHEN PASS", "CINDER PEAK", "ridge", []),
    ("CINDER PEAK", "GALE POINT", "ridge", [(420, 44)]),
    ("ELDER WOOD", "MOSS HOLLOW", "forest", [(44, 84), (68, 108)]),
    ("MOSS HOLLOW", "TELOK TOWN", "forest", []),
    ("TELOK TOWN", "FERN GATE", "forest", []),
    ("FERN GATE", "KORU CITY", "forest", [(308, 108), (340, 140)]),
]
STATE = dict(current="TOSA PORT",
             visited={"TOSA PORT", "MARIS BAY", "VALE JUNCTION", "SALT FLATS", "KORU CITY",
                      "TELOK TOWN", "MOSS HOLLOW", "ASHEN PASS"})


def poly(e):
    a, b, _, way = e
    return [STATIONS[a][:2]] + list(way) + [STATIONS[b][:2]]


def group(e, visited):
    a, b, line, _ = e
    return line if (a in visited and b in visited) else "grey"


# ------------------------------------------------------------------ sprites
def interchange_sprite(on=True):
    im = new_sheet(16, 16)
    cv = Canvas(im)
    if on:
        disc(cv, 8, 8, 6, WHITE, INK, WHITE, PANEL_SHADE)
        ring(cv, 8, 8, 3, INK)
    else:
        disc(cv, 8, 8, 6, PANEL_DARK, INK, PANEL_SHADE, INK_SOFT)
        ring(cv, 8, 8, 3, INK)
    return KX.sheet_rgba(im)


def node_for(name, visited):
    on = name in visited
    if len(STATIONS[name][2]) > 1:
        return interchange_sprite(on)
    return M.node_sprite("on" if on else "off")


def ring_big():
    """Gold ring sized for interchange nodes too (r 6..9 on an 24x24 canvas -> 32x32 OBJ)."""
    im = new_sheet(24, 24)
    cv = Canvas(im)
    for y in range(24):
        for x in range(24):
            d = ((x + 0.5 - 12) ** 2 + (y + 0.5 - 12) ** 2) ** 0.5
            if 6.0 < d <= 9.0:
                if d > 8.0:
                    c = INK
                else:
                    s_ = (x + 0.5 - 12) + (y + 0.5 - 12)
                    c = SELECT_LIGHT if s_ < -6 else SELECT_DARK if s_ > 6 else SELECT
                cv.set(x, y, c)
    return KX.sheet_rgba(im)


def chevron_img(direction):
    """Gen 3 6x9 red chevron (kit.SMALL_ARROW points left) in any of 4 directions."""
    rows = SMALL_ARROW
    if direction == "right":
        rows = [r[::-1] for r in rows]
    elif direction in ("up", "down"):
        rows = ["".join(r[c] for r in SMALL_ARROW) for c in range(len(SMALL_ARROW[0]))]
        if direction == "down":
            rows = rows[::-1]
    im = Image.new("RGBA", (len(rows[0]), len(rows)), (0, 0, 0, 0))
    p = im.load()
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch in "OF":
                p[x, y] = (snap(ARROW_RED[0]) if ch == "F" else snap(ARROW_RED[1])) + (255,)
    return im


# ------------------------------------------------------------------ labels
def label_box(name):
    cx, cy, _, (anchor, dx, dy) = STATIONS[name]
    w = text_width(name, "small")
    tx = cx - w // 2 + dx if anchor == "c" else (cx + dx - w if anchor == "l" else cx + dx)
    ty = cy + dy - 1
    return tx, ty, (tx - 5, ty + 2, w + 9, 13)


# ------------------------------------------------------------------ static canvas (built once per state)
def fills(state):
    """Line masks per group on the canvas."""
    groups = {}
    for e in EDGES:
        groups.setdefault(group(e, state["visited"]), []).append(poly(e))
    return {g: M.line_masks(p, CW, CH) for g, p in groups.items()}


def base_canvas(state=STATE):
    out = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    for g in ("grey", "coast", "ridge", "forest"):
        f = fills(state).get(g)
        if f:
            KX.layer(out, lambda cv, f=f: M.draw_lines(cv, *f), LINE_THEME[g])

    def labels(cv):
        for n in STATIONS:
            tx, ty, _ = label_box(n)
            on = n in state["visited"]
            draw_text(cv, tx, ty, n, WHITE if on else INK_SOFT, INK, font="small")
    KX.layer(out, labels)
    for n, (x, y, _, _) in STATIONS.items():
        out.alpha_composite(node_for(n, state["visited"]), (x - 8, y - 8))
    x, y = STATIONS[state["current"]][:2]
    out.alpha_composite(M.head(), (x - 8, y - 8 - 14))
    return out


_BASE = {}


def base(state=STATE):
    k = id(state)
    if k not in _BASE:
        _BASE[k] = (base_canvas(state), fills(state))
    return _BASE[k]


# ------------------------------------------------------------------ camera
def clamp_cam(x, y):
    return max(0, min(CW - VW, int(round(x)))), max(0, min(CH - VH, int(round(y))))


def centre_on(name):
    x, y = STATIONS[name][:2]
    return clamp_cam(x - VW / 2, y - VH / 2)


def in_safe(name, cam):
    x, y = STATIONS[name][:2]
    sx, sy = x - cam[0], y - cam[1]
    return SAFE["l"] <= sx <= VW - SAFE["r"] and SAFE["t"] <= sy <= VH - SAFE["b"]


def next_cam(name, cam):
    """Dead zone + re-centre: keep the camera unless the station left the safe box."""
    return cam if in_safe(name, cam) else centre_on(name)


# ------------------------------------------------------------------ chevrons at line exits
def exits(fill_all, cam):
    """Where tubes cross the viewport edge -> list of (direction, screen x, screen y)."""
    cx, cy = cam
    out = []

    def runs(vals):
        vals = sorted(vals)
        res, start, prev = [], None, None
        for v in vals:
            if start is None:
                start = prev = v
            elif v == prev + 1:
                prev = v
            else:
                res.append((start + prev) / 2)
                start = prev = v
        if start is not None:
            res.append((start + prev) / 2)
        return res
    if cx + VW < CW:
        col = cx + VW - 1
        for y in runs([y for (x, y) in fill_all if x == col and cy <= y < cy + VH]):
            out.append(("right", VX + VW - 9, VY + int(y) - cy - 4))
    if cx > 0:
        for y in runs([y for (x, y) in fill_all if x == cx and cy <= y < cy + VH]):
            out.append(("left", VX + 3, VY + int(y) - cy - 4))
    if cy > 0:
        for x in runs([x for (x, y) in fill_all if y == cy and cx <= x < cx + VW]):
            out.append(("up", VX + int(x) - cx - 4, VY + 3))
    if cy + VH < CH:
        row = cy + VH - 1
        for x in runs([x for (x, y) in fill_all if y == row and cx <= x < cx + VW]):
            out.append(("down", VX + int(x) - cx - 4, VY + VH - 9))
    return out


_CHEV = {}


def draw_chevrons(out, cam, fill_all, bob=0):
    for d, x, y in exits(fill_all, cam):
        if d not in _CHEV:
            _CHEV[d] = chevron_img(d)
        dx, dy = {"right": (bob, 0), "left": (-bob, 0), "up": (0, -bob), "down": (0, bob)}[d]
        x = max(VX + 1, min(VX + VW - 8, x))
        y = max(VY + 1, min(VY + VH - 10, y))
        out.alpha_composite(_CHEV[d], (x + dx, y + dy))


# ------------------------------------------------------------------ header (legend or mini-map)
def legend_layer(out, x=96):
    for key in ("coast", "ridge", "forest"):
        f = M.line_masks([[(x + 3, 8), (x + 11, 8)]], W, H, 1.6, 2.6)
        KX.layer(out, lambda cv, f=f: M.draw_lines(cv, *f), LINE_THEME[key])
        tx, lab = x + 15, LINE_LABEL[key]
        KX.layer(out, lambda cv, tx=tx, lab=lab: draw_text(cv, tx, -2, lab, WHITE, ACCENT_DARK, font="small"))
        x = tx + text_width(lab, "small") + 6


def minimap(out, cam, state, sel, x0=203, y0=0):
    """Option 2: 32x16 OBJ in the header, canvas at 1/16 + a gold viewport box (15x7 OBJ)."""
    im = Image.new("RGBA", (34, 16), (0, 0, 0, 0))
    p = im.load()
    ink = snap((40, 40, 64)) + (255,)
    face = snap((24, 24, 32)) + (255,)
    for y in range(16):
        for x in range(34):
            edge = x in (0, 33) or y in (0, 15)
            p[x, y] = ink if edge else face
    cols = {"coast": THEMES["rail_sea"][1], "ridge": THEMES["orchid"][2], "forest": THEMES["rail_forest"][2],
            "grey": THEMES["rail_grey"][1]}
    for e in EDGES:
        c = snap(cols[group(e, state["visited"])]) + (255,)
        pts = poly(e)
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            n = int(max(abs(bx - ax), abs(by - ay)) // 4) + 1
            for i in range(n + 1):
                xx = 1 + int((ax + (bx - ax) * i / n) / 16)
                yy = int((ay + (by - ay) * i / n) / 16)
                if 0 < xx < 33 and 0 < yy < 15:
                    p[xx, yy] = c
    for n, (sx, sy, _, _) in STATIONS.items():
        xx, yy = 1 + sx // 16, sy // 16
        if 0 < yy < 15:
            p[xx, yy] = (snap((248, 248, 248)) if n in state["visited"] else snap((112, 112, 136))) + (255,)
    # viewport box (separate 16x8 OBJ in the ROM)
    gold = snap((248, 208, 88)) + (255,)
    bx, by = 1 + cam[0] // 16, cam[1] // 16
    for x in range(bx, bx + 15):
        for y in (by, by + 7):
            if 0 <= x < 34 and 0 <= y < 16:
                p[x, y] = gold
    for y in range(by, by + 8):
        for x in (bx, bx + 14):
            if 0 <= x < 34 and 0 <= y < 16:
                p[x, y] = gold
    out.alpha_composite(im, (x0, y0))


# ------------------------------------------------------------------ tray
def tray_text(out, name, message=None):
    lines = STATIONS[name][2]

    def fn(cv):
        if message:
            draw_text(cv, 8, M.TRAY_Y + 2, message, INK, PANEL_SHADE, line_h=14)
            return
        draw_text(cv, 26, M.TRAY_Y + 1, name, INK, PANEL_SHADE)
        draw_text(cv, 26, M.TRAY_Y + 15, " + ".join(LINE_LABEL[l] for l in lines) + (" LINES" if len(lines) > 1 else " LINE"),
                  INK_SOFT, PANEL_SHADE, font="small")
        x = 239 - 8 - (8 + 3 + text_width("DEPART", "small") + 8 + 8 + 3 + text_width("CANCEL", "small"))
        y = M.TRAY_Y + 20
        x = draw_button(cv, x, y, "A") + 3
        x = draw_text(cv, x, y - 4, "DEPART", INK, PANEL_SHADE, font="small") + 8
        x = draw_button(cv, x, y, "B") + 3
        draw_text(cv, x, y - 4, "CANCEL", INK, PANEL_SHADE, font="small")
    KX.layer(out, fn)
    if not message:
        f = M.line_masks([[(6, M.TRAY_Y + 11), (20, M.TRAY_Y + 11)]], W, H, 2.0, 3.0)
        KX.layer(out, lambda cv: M.draw_lines(cv, *f), LINE_THEME[lines[0]])
        spr = interchange_sprite() if len(lines) > 1 else M.node_sprite("on")
        out.alpha_composite(spr, (13 - 8, M.TRAY_Y + 11 - 8))


# ------------------------------------------------------------------ frame
def grid(cam, drift):
    out = Image.new("RGBA", (W, H))
    px = out.load()
    for y in range(H):
        for x in range(W):
            px[x, y] = GRID_PAL[grid_index(x + cam[0] - drift, y + cam[1] - VY - drift)] + (255,)
    return out


_RING = {}


def render(cursor, cam, state=STATE, drift=0, ring_at=None, ring_dx=0, deny=None, message=None,
           popup=None, header="legend", bob=0, show_safe=False):
    """cam = (camX, camY) canvas offset of the viewport. ring_at = canvas coords while travelling."""
    bimg, fl = base(state)
    fill_all = set()
    for f, _ in fl.values():
        fill_all |= f
    out = grid(cam, drift)
    out.alpha_composite(bimg.crop((cam[0], cam[1], cam[0] + VW, cam[1] + VH)), (VX, VY))
    # selected label: gold pill OBJ behind BG2 + label cells palette-swapped to ink text
    if ring_at is None and cursor:
        tx, ty, (px_, py, pw, ph) = label_box(cursor)
        ox, oy = VX - cam[0], VY - cam[1]

        def pill(cv):
            rounded_box(cv, px_ + ox, py + oy, pw, ph, 4, SELECT, INK, SELECT_LIGHT, SELECT_DARK)
            draw_text(cv, tx + ox, ty + oy, cursor, INK, SELECT_DARK, font="small")
        KX.layer(out, pill)
    if deny:
        x, y = STATIONS[deny][:2]
        out.alpha_composite(M.ring_sprite("grey"), (x - cam[0] - 8, y - cam[1] + VY - 8))
    if "r" not in _RING:
        _RING["r"] = ring_big()
    rx, ry = ring_at or STATIONS[cursor][:2]
    out.alpha_composite(_RING["r"], (int(round(rx)) - cam[0] - 12 + ring_dx, int(round(ry)) - cam[1] + VY - 12))
    draw_chevrons(out, cam, fill_all, bob)
    if show_safe:
        def box(cv):
            x0, y0 = VX + SAFE["l"], VY + SAFE["t"]
            x1, y1 = VX + VW - SAFE["r"], VY + VH - SAFE["b"]
            for x in range(x0, x1 + 1):
                if x % 4 < 2:
                    cv.set(x, y0, SELECT)
                    cv.set(x, y1, SELECT)
            for y in range(y0, y1 + 1):
                if y % 4 < 2:
                    cv.set(x0, y, SELECT)
                    cv.set(x1, y, SELECT)
        KX.layer(out, box)
    # fixed chrome (BG1) — covers anything that scrolled under it
    KX.layer(out, M.chrome(state))
    KX.layer(out, lambda cv: draw_text(cv, 22, -1, "TOSA RAIL", WHITE, ACCENT_DARK))
    if header == "legend":
        legend_layer(out)
    else:
        minimap(out, cam, state, cursor)
    tray_text(out, cursor, message)
    if popup:
        popup(out)
    return out


# ------------------------------------------------------------------ overview + budget
def overview(frames, path, k=2):
    """Whole canvas with the viewport of each framing outlined."""
    from PIL import ImageDraw
    bimg, _ = base()
    g = Image.new("RGBA", (CW, CH))
    px = g.load()
    for y in range(CH):
        for x in range(CW):
            px[x, y] = GRID_PAL[grid_index(x, y)] + (255,)
    g.alpha_composite(bimg)
    big = KX.upscale(g.convert("RGB"), k)
    sheet = Image.new("RGB", (big.size[0] + 32, big.size[1] + 40), (28, 28, 36))
    sheet.paste(big, (16, 30))
    d = ImageDraw.Draw(sheet)
    d.text((16, 8), "Virtual canvas 512x256 (BG2 64x32 tiles). Boxes = the 240x112 map viewport of each framing.",
           fill=(230, 230, 240))
    colours = [(240, 200, 80), (120, 220, 240), (240, 120, 160), (160, 240, 140)]
    for i, (label, cam) in enumerate(frames):
        c = colours[i % len(colours)]
        x0, y0 = 16 + cam[0] * k, 30 + cam[1] * k
        d.rectangle((x0, y0, x0 + VW * k - 1, y0 + VH * k - 1), outline=c, width=3)
        d.text((x0 + 6, y0 + 4), label, fill=c)
    sheet.save(path)


def budget(state=STATE):
    """Tile count of BG2 (tubes + baked labels) and label/tube cell conflicts."""
    im = new_sheet(CW, CH)
    cv = Canvas(im)
    fl = fills(state)
    for f, o in fl.values():
        M.draw_lines(cv, f, o)
    for n in STATIONS:
        tx, ty, _ = label_box(n)
        draw_text(cv, tx, ty, n, WHITE, INK, font="small")
    tiles, tm = to_tiles(im)
    tube_cells = set()
    for f, o in fl.values():
        for (x, y) in f | o:
            tube_cells.add((x // 8, y // 8))
    conflicts = []
    label_tiles = 0
    for n in STATIONS:
        tx, ty, _ = label_box(n)
        w = text_width(n, "small")
        cells = {(x // 8, y // 8) for x in range(tx, tx + w) for y in range(ty + 3, ty + 13)}
        label_tiles += len(cells)
        if cells & tube_cells:
            conflicts.append(n)
    return dict(tiles=len(tiles), label_cells=label_tiles, conflicts=conflicts,
                map_bytes=64 * 32 * 2)
