"""
TOSA RAIL station map — renderer shared by the stills (mock_station_map.py) and the
navigation GIF (anim_station_map.py).

Layers, bottom-up, like the GBA would draw them:
  BG3  scrolling grid (kit backdrop, own palette)
  BG2  map art: rail lines + header band + bottom tray. Line tiles are drawn ONCE with the
       kit ACCENT ramp; each line segment's cells pick a BG palette:
          pal 0 = orchid (RIDGE line, header, tray)   pal 1 = sea (COAST line)
          pal 2 = grey  (segment touching a station you have not visited)
       All node centres sit on 8px cell centres (8k+4) so a 6px line fits inside one cell
       row/column and two colours never share a cell (the junction cell is under its node OBJ).
  BG0  text: station labels, header title, tray name + hints (gold pill blitted behind
       the selected label, like the YES/NO pill)
  OBJ  station nodes (16x16), gold selection ring (16x16), player head (16x16)
  BG1  popups (dialogue + YES/NO, Orchid std frame)
"""
from common import *

# ------------------------------------------------------------------ palettes
SEA = [(24, 96, 120), (40, 152, 168), (120, 208, 208), (200, 240, 232)]
GREY = [(64, 64, 80), (96, 96, 112), (136, 136, 152), (176, 176, 184)]
THEMES.setdefault("rail_sea", SEA)
THEMES.setdefault("rail_grey", GREY)
LINE_THEME = {"coast": "rail_sea", "ridge": "orchid", "grey": "rail_grey"}
LINE_NAME = {"coast": "COAST LINE", "ridge": "RIDGE LINE"}

# ------------------------------------------------------------------ network (placeholder)
# name: (cx, cy, line, label placement)  — placement = (anchor, dx, dy)
#   anchor 'c' centred under/over the node, 'l' text ends left of node, 'r' text starts right.
STATIONS = {
    "TOSA PORT":     (28, 100, "coast", ("c", 0, 6)),
    "MARIS BAY":     (76, 100, "coast", ("c", 0, 6)),
    "VALE JUNCTION": (124, 76, "coast", ("r", 4, 6)),
    "KORU CITY":     (212, 76, "coast", ("c", -6, -18)),
    "TELOK TOWN":    (124, 44, "ridge", ("l", -9, -8)),
    "ASHEN PASS":    (196, 28, "ridge", ("c", 0, 6)),
}
ORDER = ["TOSA PORT", "MARIS BAY", "VALE JUNCTION", "KORU CITY", "TELOK TOWN", "ASHEN PASS"]
# edges: (a, b, line, waypoints between a and b) — 0 / 45 / 90 degree runs only
EDGES = [
    ("TOSA PORT", "MARIS BAY", "coast", []),
    ("MARIS BAY", "VALE JUNCTION", "coast", [(92, 100), (116, 76)]),
    ("VALE JUNCTION", "KORU CITY", "coast", []),
    ("VALE JUNCTION", "TELOK TOWN", "ridge", []),
    ("TELOK TOWN", "ASHEN PASS", "ridge", [(124, 36), (132, 28)]),
]

DEFAULT_STATE = dict(current="TOSA PORT",
                     visited={"TOSA PORT", "MARIS BAY", "VALE JUNCTION", "TELOK TOWN"})

TRAY_Y = 128
HEADER_H = 16


# ------------------------------------------------------------------ line art
def _dist_seg(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    L = dx * dx + dy * dy
    t = 0 if L == 0 else max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / L))
    qx, qy = ax + t * dx, ay + t * dy
    return ((px - qx) ** 2 + (py - qy) ** 2) ** 0.5


def line_masks(polys, w, h, fill_r=2.0, out_r=3.0):
    """Return (fill, outline) pixel sets for a group of polylines (pixel-centre distance)."""
    fill, outl = set(), set()
    for pts in polys:
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            for y in range(int(min(ay, by) - out_r - 1), int(max(ay, by) + out_r + 2)):
                for x in range(int(min(ax, bx) - out_r - 1), int(max(ax, bx) + out_r + 2)):
                    if not (0 <= x < w and 0 <= y < h):
                        continue
                    d = _dist_seg(x + 0.5, y + 0.5, ax, ay, bx, by)
                    if d <= fill_r:
                        fill.add((x, y))
                    elif d <= out_r:
                        outl.add((x, y))
    return fill, outl - fill


def draw_lines(cv, fill, outl):
    """Gen 3 tube: ink outline, light top/left edge, dark bottom/right edge (3-step ramp)."""
    for (x, y) in outl:
        cv.set(x, y, INK)
    for (x, y) in fill:
        up, left = (x, y - 1) not in fill, (x - 1, y) not in fill
        down, right = (x, y + 1) not in fill, (x + 1, y) not in fill
        if up or (left and not down):
            c = ACCENT_LIGHT
        elif down or right:
            c = ACCENT_DARK
        else:
            c = ACCENT
        cv.set(x, y, c)


def edge_poly(e, scale=1.0, origin=(0, 0)):
    a, b, _, way = e
    pts = [STATIONS[a][:2]] + way + [STATIONS[b][:2]]
    ox, oy = origin
    return [(ox + x * scale, oy + y * scale) for x, y in pts]


def edge_group(e, visited):
    a, b, line, _ = e
    return line if (a in visited and b in visited) else "grey"


def map_layer(out, state, scale=1.0, origin=(0, 0), fill_r=2.0, out_r=3.0):
    """Composite the rail lines (one palette per line group) onto `out`."""
    groups = {}
    for e in EDGES:
        groups.setdefault(edge_group(e, state["visited"]), []).append(edge_poly(e, scale, origin))
    for g in ("grey", "coast", "ridge"):
        if g not in groups:
            continue
        fill, outl = line_masks(groups[g], W, H, fill_r, out_r)
        KX.layer(out, lambda cv: draw_lines(cv, fill, outl), LINE_THEME[g])


# ------------------------------------------------------------------ chrome (BG2, orchid)
def train_glyph(cv, x, y):
    """12x12 header pictogram: train front (kit roles)."""
    rows = [
        "..OOOOOOOO..",
        ".OWWWWWWWWO.",
        "OWGGGGGGGGPO",
        "OWGGGGGGGGPO",
        "OWGGGGGGGGPO",
        "OPPPPPPPPPPO",
        "OPYPPPPPPYPO",
        "OPPPPPPPPPPO",
        ".OOOOOOOOOO.",
        "..O.O..O.O..",
        ".O...OO...O.",
        "OOOOOOOOOOOO",
    ]
    stamp(cv, x, y, rows, {"O": INK, "W": WHITE, "G": ACCENT_PALE, "P": PANEL_SHADE, "Y": SELECT})


def chrome(state, title="TOSA RAIL", legend=True):
    def fn(cv):
        # header band (dex style) + bottom tray (bag/dex style, stitched seam)
        band_face(cv)
        train_glyph(cv, 6, 2)
        tray(cv, TRAY_Y)
    return fn


def band_face(cv):
    cv.rect(0, 0, 239, HEADER_H - 2, ACCENT)
    cv.hline(0, 239, 0, ACCENT_LIGHT)
    cv.hline(0, 239, HEADER_H - 2, ACCENT_DARK)
    cv.hline(0, 239, HEADER_H - 1, INK)


def tray(cv, y0, y1=159, x0=0, x1=239):
    cv.rect(x0, y0, x1, y1, PANEL)
    cv.hline(x0, x1, y0, INK)
    cv.hline(x0, x1, y0 + 1, WHITE)
    cv.hline(x0, x1, y1, PANEL_SHADE)
    for x in range(x0 + 2, x1 - 1):
        if x % 4 < 2:
            cv.set(x, y0 + 3, PANEL_SHADE)


def legend_layer(out, x=150):
    """Header legend: a short tube in each line colour + its name (small font, white)."""
    for key, label in (("coast", "COAST"), ("ridge", "RIDGE")):
        fill, outl = line_masks([[(x + 3, 8), (x + 11, 8)]], W, H, 1.6, 2.6)
        KX.layer(out, lambda cv: draw_lines(cv, fill, outl), LINE_THEME[key])
        tx = x + 16
        KX.layer(out, lambda cv: draw_text(cv, tx, -3, label, WHITE, ACCENT_DARK, font="small"))
        x = tx + text_width(label, "small") + 8


# ------------------------------------------------------------------ OBJ sprites
def node_sprite(kind):
    """16x16 OBJ: 'on' (visited), 'off' (not visited)."""
    im = new_sheet(16, 16)
    cv = Canvas(im)
    if kind == "on":
        disc(cv, 8, 8, 5, WHITE, INK, WHITE, PANEL_SHADE)
        cv.set(6, 6, WHITE)
    else:
        disc(cv, 8, 8, 5, PANEL_DARK, INK, PANEL_SHADE, INK_SOFT)
    return KX.sheet_rgba(im)


def ring_sprite(kind="gold"):
    """16x16 OBJ: selection ring around a node (gold) or the 'denied' flash ring (grey)."""
    im = new_sheet(16, 16)
    cv = Canvas(im)
    face, light, dark = ((SELECT, SELECT_LIGHT, SELECT_DARK) if kind == "gold"
                         else (PANEL_DARK, PANEL_SHADE, INK_SOFT))
    for y in range(16):
        for x in range(16):
            d = ((x + 0.5 - 8) ** 2 + (y + 0.5 - 8) ** 2) ** 0.5
            if 5.0 < d <= 8.0:
                if d > 7.0:
                    c = INK
                else:
                    s_ = (x + 0.5 - 8) + (y + 0.5 - 8)          # <0 = top-left half
                    c = light if s_ < -4 else dark if s_ > 4 else face
                cv.set(x, y, c)
    return KX.sheet_rgba(im)


_HEAD = {}


def head():
    if "h" not in _HEAD:
        _HEAD["h"] = player_map_icon()
    return _HEAD["h"]


# ------------------------------------------------------------------ text helpers (BG0)
def label_box(name, small=True):
    """Return text x, y and pill rect for a station label."""
    cx, cy, _, (anchor, dx, dy) = STATIONS[name]
    font = "small"
    w = text_width(name, font)
    if anchor == "c":
        tx = cx - w // 2 + dx
    elif anchor == "l":
        tx = cx + dx - w
    else:
        tx = cx + dx
    ty = cy + dy - 1                     # small caps occupy rows ty+4 .. ty+11 (+ shadow)
    pill = (tx - 5, ty + 2, w + 9, 13)
    return tx, ty, pill


def labels_layer(out, state, cursor=None):
    def fn(cv):
        for n in STATIONS:
            tx, ty, (px, py, pw, ph) = label_box(n)
            if n == cursor:
                rounded_box(cv, px, py, pw, ph, 4, SELECT, INK, SELECT_LIGHT, SELECT_DARK)
                draw_text(cv, tx, ty, n, INK, SELECT_DARK, font="small")
            elif n in state["visited"]:
                draw_text(cv, tx, ty, n, WHITE, INK, font="small")
            else:
                draw_text(cv, tx, ty, n, INK_SOFT, INK, font="small")
    KX.layer(out, fn)


def tray_text(out, name, hint=True, message=None):
    def fn(cv):
        if message:
            draw_text(cv, 8, TRAY_Y + 2, message, INK, PANEL_SHADE, line_h=14)
            return
        line = STATIONS[name][2]
        # line stub + node pictogram (picture, not a label)
        draw_text(cv, 26, TRAY_Y + 1, name, INK, PANEL_SHADE)
        draw_text(cv, 26, TRAY_Y + 15, LINE_NAME[line], INK_SOFT, PANEL_SHADE, font="small")
        if hint:
            x = 239 - 8 - (8 + 3 + text_width("DEPART", "small") + 8 + 8 + 3 + text_width("CANCEL", "small"))
            y = TRAY_Y + 20
            x = draw_button(cv, x, y, "A") + 3
            x = draw_text(cv, x, y - 4, "DEPART", INK, PANEL_SHADE, font="small") + 8
            x = draw_button(cv, x, y, "B") + 3
            draw_text(cv, x, y - 4, "CANCEL", INK, PANEL_SHADE, font="small")
    KX.layer(out, fn)
    if not message:
        # tray pictogram: tube stub in the line's colour with a node on it
        line = STATIONS[name][2]
        fill, outl = line_masks([[(6, TRAY_Y + 11), (20, TRAY_Y + 11)]], W, H, 2.0, 3.0)
        KX.layer(out, lambda cv: draw_lines(cv, fill, outl), LINE_THEME[line])
        out.alpha_composite(node_sprite("on"), (13 - 8, TRAY_Y + 11 - 8))


# ------------------------------------------------------------------ popups (BG1, orchid)
def confirm_popup(out, dest, yes=True):
    def fn(cv):
        Wn.dialogue_box(cv, 2, 15, 27, 4)
        draw_text(cv, 16, 120, "Take the train to\n%s?" % dest, INK, PANEL_SHADE)
        Wn.std_frame(cv, 23, 9, 5, 4)
        Wn.selection_bar(cv, 23 * 8 + 2, (9 if yes else 11) * 8 + 1, 36, 14)
        draw_text(cv, 23 * 8 + 8, 72, "YES", INK, PANEL_SHADE)
        draw_text(cv, 23 * 8 + 8, 88, "NO", INK, PANEL_SHADE)
    KX.layer(out, fn)


# ------------------------------------------------------------------ frame renderer
def render(state=DEFAULT_STATE, cursor="MARIS BAY", scroll=0, ring_at=None, ring_dx=0,
           deny=None, tray_msg=None, popup=None, head_dy=0, show_pill=True):
    """
    cursor:  station under the gold ring (its label gets the gold pill).
    ring_at: (x, y) override for the ring centre while it travels between stations.
    deny:    greyed station the player just tried to move to (grey flash ring on it).
    """
    out = KX.grid_frame(scroll)
    map_layer(out, state)
    KX.layer(out, chrome(state))
    KX.layer(out, lambda cv: draw_text(cv, 22, -1, "TOSA RAIL", WHITE, ACCENT_DARK))
    legend_layer(out)
    labels_layer(out, state, cursor if (show_pill and ring_at is None) else None)
    # OBJ: nodes, ring, head
    for n, (cx, cy, _, _) in STATIONS.items():
        out.alpha_composite(node_sprite("on" if n in state["visited"] else "off"), (cx - 8, cy - 8))
    if deny:
        cx, cy = STATIONS[deny][:2]
        out.alpha_composite(ring_sprite("grey"), (cx - 8, cy - 8))
    if cursor or ring_at:
        rx, ry = ring_at or STATIONS[cursor][:2]
        out.alpha_composite(ring_sprite("gold"), (int(rx) - 8 + ring_dx, int(ry) - 8))
    cx, cy = STATIONS[state["current"]][:2]
    out.alpha_composite(head(), (cx - 8, cy - 8 - 13 + head_dy))
    tray_text(out, cursor, message=tray_msg)
    if popup:
        popup(out)
    return out


# ------------------------------------------------------------------ alternative layout B
def render_list(state=DEFAULT_STATE, cursor="MARIS BAY", scroll=0):
    """Layout B: station list on the left (pill rows), mini line diagram in a well on the right."""
    out = KX.grid_frame(scroll)
    KX.layer(out, chrome(state))
    KX.layer(out, lambda cv: draw_text(cv, 22, -1, "TOSA RAIL", WHITE, ACCENT_DARK))
    legend_layer(out)
    # list rows (BG2 pills; gold = palette swap; greyed rows = disabled face)
    X0, RW, Y0 = 4, 116, 20
    rows = []
    for i, n in enumerate(ORDER):
        y = Y0 + i * 17
        rows.append((n, y))

    def pills(cv):
        for n, y in rows:
            if n == cursor:
                rounded_box(cv, X0, y, RW, 15, 4, SELECT, INK, SELECT_LIGHT, SELECT_DARK)
            elif n in state["visited"]:
                rounded_box(cv, X0, y, RW, 15, 4, PANEL, INK, WHITE, PANEL_SHADE)
            else:
                rounded_box(cv, X0, y, RW, 15, 4, PANEL_DARK, INK, PANEL_SHADE, INK_SOFT)
    KX.layer(out, pills)
    # line colour cap on each pill (palette per line)
    for n, y in rows:
        g = STATIONS[n][2] if n in state["visited"] else "grey"
        fill, outl = line_masks([[(X0 + 7, y + 7.5), (X0 + 7, y + 7.5)]], W, H, 2.2, 3.2)
        KX.layer(out, lambda cv: draw_lines(cv, fill, outl), LINE_THEME[g])

    def names(cv):
        for n, y in rows:
            fg, sh = (INK, PANEL_SHADE) if n in state["visited"] else (INK_SOFT, PANEL_DARK)
            if n == cursor:
                sh = SELECT_DARK
            draw_text(cv, X0 + 15, y - 1, n, fg, sh, font="narrow")
    KX.layer(out, names)
    for n, y in rows:
        if n == state["current"]:
            out.alpha_composite(head(), (X0 + RW - 18, y - 1))
    # mini map well
    WX, WY, WW, WH = 126, 20, 110, 102

    def well(cv):
        rounded_box(cv, WX, WY, WW, WH, 4, PANEL_DARK, INK, INK_SOFT, PANEL_SHADE)
    KX.layer(out, well)
    # re-show the grid inside the well (it is a window onto BG3)
    grid = KX.grid_frame(scroll)
    out.paste(grid.crop((WX + 2, WY + 2, WX + WW - 2, WY + WH - 2)), (WX + 2, WY + 2))
    s = 0.56
    xs = [v[0] for v in STATIONS.values()]
    ys = [v[1] for v in STATIONS.values()]
    org = (WX + WW / 2 - s * (min(xs) + max(xs)) / 2, WY + WH / 2 + 4 - s * (min(ys) + max(ys)) / 2)
    groups = {}
    for e in EDGES:
        groups.setdefault(edge_group(e, state["visited"]), []).append(edge_poly(e, s, org))
    for g in ("grey", "coast", "ridge"):
        if g in groups:
            fill, outl = line_masks(groups[g], W, H, 1.0, 2.0)
            KX.layer(out, lambda cv: draw_lines(cv, fill, outl), LINE_THEME[g])

    def dots(cv):
        for n, (x, y, _, _) in STATIONS.items():
            mx, my = org[0] + x * s, org[1] + y * s
            if n == cursor:
                ring(cv, mx, my, 6.0, INK)
                ring(cv, mx, my, 5.0, SELECT, 2.0)
            disc(cv, mx, my, 3.0, WHITE if n in state["visited"] else PANEL_DARK, INK)
    KX.layer(out, dots)
    cx, cy = STATIONS[state["current"]][:2]
    out.alpha_composite(head(), (int(org[0] + cx * s) - 8, int(org[1] + cy * s) - 18))
    tray_text(out, cursor)
    return out


# ------------------------------------------------------------------ budget helpers
def bg2_art_index_image(state=DEFAULT_STATE):
    """The BG2 art as one indexed image (palette-agnostic) for tile counting."""
    im = new_sheet(W, H)
    cv = Canvas(im)
    groups = {}
    for e in EDGES:
        groups.setdefault(edge_group(e, state["visited"]), []).append(edge_poly(e))
    for g, polys in groups.items():
        draw_lines(cv, *line_masks(polys, W, H))
    chrome(state)(cv)
    return im
