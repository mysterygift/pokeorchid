"""
Pixel-accurate mockups of the Orchid Pokédex HABITATS view (round 2).

Round 2 (user review 2026-11-22):
  * "Ⓐ Route View" call to action above the route name on the region map
  * Seen -> Captured -> Catalogued: one capture reveals measurements, area and levels; a second capture
    completes the dex entry and reveals the encounter rate. Catalogued = two captures.
  * Day / night: every habitat has day and night tables; SELECT flips the view between them.

MAP SCREEN (region overview)
    BG3  region map art (the dex AREA map: user's Tosa / Tiksi art + town / landmark markers)
    BG2  zone overlay: 8x8 cells alpha-blended dark outside the lit habitat zone, gold rim
         round the zone, gold glow on the hovered route (pulses)
    BG1  Orchid frame (header band, map rim, tray + name pill), zone plate, CTA pill
    BG0  text: region tabs, title, zone plate, route name + counts, CTA
    OBJ  caught badges on completed routes, compass, sun / moon chip, count pictograms
ROUTE PAGE (one habitat, one time of day)
    BG3  scrolling grid; BG1 method chips + icon wells + tray; BG0 text
    OBJ  32x32 party icons: unseen = black silhouette, seen = greyscale, captured / catalogued = colour,
         badges (ball = captured once, gold book = catalogued), red chevrons when rows scroll

usage: mock_habitats.py OUT_DIR
"""
import json
import os
import sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from kit import *
import kit as K
import kit_ext as KX
import dex_ext as D
from gamefont import draw_text, text_width
import region_tags as RT
import export_region_map as EM
import export_region_map_tiksi as ET

ROOT = KX.ROOT
W, H = 240, 160
GX, GY = 8, 16
COLS, ROWS = 28, 15
DIM_TO, DIM_K = (16, 16, 32), 0.5          # BLDALPHA-style darkening of land outside the zone

# ------------------------------------------------------------------ habitat zones
# Placeholder split; in the real build this is a per-area "habitat" field in the region map tagger.
ZONE_NAME = {"NORTH": "Northern Tosa", "EAST": "Eastern Tosa", "SOUTH": "Southern Tosa", "WEST": "Western Tosa"}
ZONE_OF = {}
for z, secs in {
    "NORTH": "KANTU_FALLS ROUTE_304 GALANGAL_FOREST ROUTE_305 ROUTE_303 TIMAH_CITY ROUTE_302 MT_BATOK FABER_TOWN "
             "NORTH_TOSA_RESERVE ROUTE_307 PINESTAMP_TOWN CHALLENGER_GATE CHALLENGERS_TRAIL PKMN_LEAGUE",
    "EAST": "EAST_TOSA_RESERVE SENOKO_CITY TOSA_POWER_PLANT ROUTE_309 BURA_CITY ROUTE_310 JURAN_CITY "
            "POKETOPIA_GATE CORRAL_CITY",
    "SOUTH": "CHANGU_CITY ROUTE_308 ROUTE_306 CHANGU_AIRPORT INDUSTRIAL_PARK INKA_CITY ROUTE_314 MOONGROVE_CITY "
             "MOONGROVE_MARSH RAILWAY_TUNNELS SOUTH_TOSA_RESERVE_1 SOUTH_TOSA_RESERVE_2 SOUTH_TOSA_RESERVE_3 "
             "ABANDONED_HOUSE",
    "WEST": "WAVEBREAK_TOWN ROUTE_311 DAMP_PATH OLDALE_TOWN ROUTE_312 ROUTE_313 TOSA_PORT",
}.items():
    for s in secs.split():
        ZONE_OF["MAPSEC_" + s] = z

# ------------------------------------------------------------------ encounter data
TIMES = ("day", "night")
METHODS = ["land_mons", "water_mons", "rock_smash_mons", "fishing_mons"]
METHOD_LABEL = {"land_mons": "Grass", "water_mons": "Surfing", "rock_smash_mons": "Rock Smash",
                "fishing_mons": "Fishing"}
SLOT_RATES = {"land_mons": [20, 20, 10, 10, 10, 10, 5, 5, 4, 4, 1, 1],
              "water_mons": [60, 30, 5, 4, 1], "rock_smash_mons": [60, 30, 5, 4, 1],
              "fishing_mons": [70, 30, 60, 20, 20, 40, 40, 15, 4, 1]}
ROD_OF_SLOT = ["Old Rod"] * 2 + ["Good Rod"] * 3 + ["Super Rod"] * 5


def load_encounters():
    """{section: {time: {method: {species: {rate, lv}}}}}; base_label "_Night" = night, else day
    (the fallback table, used for morning / day / evening)."""
    enc = json.load(open(os.path.join(ROOT, "src/data/wild_encounters.json")))
    headers = [g for g in enc["wild_encounter_groups"] if g["label"] == "gWildMonHeaders"][0]["encounters"]
    sec_of = {}
    maps = os.path.join(ROOT, "data/maps")
    for d in os.listdir(maps):
        p = os.path.join(maps, d, "map.json")
        if os.path.exists(p):
            m = json.load(open(p))
            sec_of[m["id"]] = m.get("region_map_section")
    out = {}
    for h in headers:
        sec = sec_of.get(h["map"])
        if not sec:
            continue
        t = "night" if h.get("base_label", "").endswith("_Night") else "day"
        for meth in METHODS:
            if meth not in h:
                continue
            tab = out.setdefault(sec, {}).setdefault(t, {}).setdefault(meth, {})
            for i, mon in enumerate(h[meth]["mons"]):
                sp = mon["species"]
                if sp == "SPECIES_NONE":
                    continue
                e = tab.setdefault(sp, {"rate": {}, "lv": [99, 0]})
                key = ROD_OF_SLOT[i] if meth == "fishing_mons" else ""
                e["rate"][key] = e["rate"].get(key, 0) + SLOT_RATES[meth][i]
                e["lv"] = [min(e["lv"][0], mon["min_level"]), max(e["lv"][1], mon["max_level"])]
    return out


ENC = load_encounters()

# ------------------------------------------------------------------ sample save (made up)
def _set(names):
    return set("SPECIES_" + s for s in names.split())


CATALOGUED = _set("WOOPER LOTAD MAGIKARP GOLDEEN ZIGZAGOON POOCHYENA SKWOVET MAREEP STARLY GEODUDE")
CAPTURED = CATALOGUED | _set("CROAGUNK SHELLOS TYMPOLE BARBOACH LOMBRE NIDORAN_F NIDORAN_M WINGULL HOOTHOOT "
                             "MACHOP LILLIPUP DEWPIDER")
SEEN = CAPTURED | _set("GOOMY YANMA STUNFISK SURSKIT CORPHISH QUAGSIRE ELECTRIKE ABRA ROCKRUFF MANKEY "
                       "SPINARAK GASTLY SALANDIT")


def state(sp):
    if sp in CATALOGUED:
        return "catalogued"
    if sp in CAPTURED:
        return "captured"
    return "seen" if sp in SEEN else "unseen"


def species_of(sec, time=None):
    s = set()
    for t, by_m in ENC.get(sec, {}).items():
        if time in (None, t):
            for tab in by_m.values():
                s |= set(tab)
    return s


def counts(species):
    return (sum(1 for s in species if s in SEEN), sum(1 for s in species if s in CAPTURED),
            sum(1 for s in species if s in CATALOGUED), len(species))


def name_of(const):
    try:
        return D.species(const[8:])["name"]
    except Exception:
        return const[8:].replace("_", " ").title()[:10]


# ------------------------------------------------------------------ pictograms (kit roles)
PICTO = {
    "land_mons": [
        "...........", ".#.....#...", ".#..#..#.#.", "##..#.##.#.", "#.#.#.#..#.",
        "#.#.##.#.##", "..#.#..#.#.", ".#..#.#..#.", ".#.#..#.#..", "###########"],
    "water_mons": [
        "...........", "...###.....", "..#...#....", ".#..##.#...", "#..#..#....",
        "#..#...##..", ".#..###..##", "..##.......", ".##..##..##", "#..##..##.."],
    "rock_smash_mons": [
        "...........", "....####...", "...#....#..", "..#..#...#.", ".#..#.....#",
        ".#...#....#", "#.....#...#", "#.....#..#.", "#....#...#.", ".#########."],
    "fishing_mons": [
        ".........##", "........#..", ".......#...", "......#...#", ".....#....#",
        "....#.....#", "...#......#", "..#.....#.#", ".##......#.", "##........."],
}
EYE = ["..#####..", ".#.....#.", "#..###..#", "#..#+#..#", "#..###..#", ".#.....#.", "..#####.."]
BOOK = ["#########", "#+++#+++#", "#+++#+++#", "#+++#+++#", "#+++#+++#", "#+++#+++#", "#########"]
SUN = ["....#....", ".#.....#.", "...###...", "..#+++#..", "#.#+++#.#", "..#+++#..", "...###...",
       ".#.....#.", "....#...."]
MOON = ["...####..", "..##+....", ".##+.....", ".#++.....", ".#++.....", ".#++.....", ".##+.....",
        "..##+....", "...####.."]
A_BTN = ["..#####..", ".#+++++#.", "#+++#+++#", "#++#+#++#", "#++###++#", "#++#+#++#", "#+++++++#",
         ".#+++++#.", "..#####.."]
COMPASS = [".....n.....", ".....n.....", "....nnn....", "....nnn....", "..w..#..e..", "wwwww#eeeee",
           "..w..#..e..", "....sss....", "....sss....", ".....s.....", ".....s....."]


def stamp_rows(cv, x, y, rows, cmap):
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if cmap.get(ch) is not None:
                cv.set(x + c, y + r, cmap[ch])


def compass(cv, x, y, zone):
    lit = zone[0].lower() if zone else None
    cmap = {k: (SELECT if k == lit else INK_SOFT) for k in "nesw"}
    cmap["#"] = INK
    stamp_rows(cv, x, y, COMPASS, cmap)


def grey_ball(cv, x, y):
    """First catch: the caught ball in greys (same 8x8 vanilla shape, kit roles)."""
    im = Image.open(os.path.join(ROOT, "graphics", "pokedex", "caught_ball.png"))
    px = im.load()
    m = {15: INK, 11: PANEL_DARK, 1: WHITE}
    for yy in range(5, 13):
        for xx in range(8):
            if px[xx, yy] in m:
                cv.set(x + xx, y + yy - 5, m[px[xx, yy]])


def badge(cv, x, y, st):
    """captured once = grey ball, catalogued = colour ball."""
    if st == "catalogued":
        D.caught_ball(cv, x, y)
    elif st == "captured":
        grey_ball(cv, x, y)


def counts_row(tc, x, y, c3, font="narrow", total=True):
    """eye seen, grey ball captured, colour ball catalogued, then "/total" once; returns end x."""
    s, c, k, n = c3
    for icon, val in (("eye", s), ("captured", c), ("catalogued", k)):
        if icon == "eye":
            stamp_rows(tc, x, y + 4, EYE, {"#": INK, "+": WHITE})
        else:
            badge(tc, x, y + 4, icon)
        txt = "%d" % val
        draw_text(tc, x + 11, y, txt, INK, PANEL_SHADE, font=font)
        x += 11 + text_width(txt, font) + 5
    if total:
        txt = "/%d" % n
        draw_text(tc, x - 2, y, txt, INK_SOFT, PANEL_SHADE, font=font)
        x += text_width(txt, font)
    return x


# ------------------------------------------------------------------ icons
def icon_folder(const):
    base = const[8:].lower()
    g = lambda *p: os.path.join(ROOT, "graphics", "pokemon", *p)
    if os.path.exists(g(base, "icon.png")):
        return base
    if "_" in base:
        b, rest = base.split("_", 1)
        for cand in (rest, rest + "n", rest.rstrip("n")):
            if os.path.exists(g(b, cand, "icon.png")):
                return os.path.join(b, cand)
        return b
    return base


def icon_pal_index(const):
    import re
    try:
        b = D._species_blocks()[const[8:]]
    except KeyError:
        return 0
    m = re.search(r"\.iconPalIndex\s*=\s*(?:P_GBA_STYLE_SPECIES_ICONS\s*\?\s*\d+\s*:\s*)?(\d)", b)
    return int(m.group(1)) if m else 0


def icon(const, st, frame=0):
    im = KX.mon_icon(icon_folder(const), frame, icon_pal_index(const))
    if st in ("captured", "catalogued"):
        return im
    px = im.load()
    for y in range(32):
        for x in range(32):
            r, g, b, a = px[x, y]
            if not a:
                continue
            if st == "unseen":
                px[x, y] = (24, 24, 40, 255)
            else:   # greyscale OBJ palette = luminance of the species' icon palette, lifted a little
                l = 0.30 * r + 0.59 * g + 0.11 * b
                v = snap((int(40 + l * 0.82),) * 3)[0]
                px[x, y] = (v, v, v, 255)
    return im


# ------------------------------------------------------------------ map screen
def is_sea(im, cx, cy):
    px = im.load()
    x0, y0 = GX + cx * 8, GY + cy * 8
    blue = sum(1 for j in range(8) for i in range(8)
               if px[x0 + i, y0 + j][2] > px[x0 + i, y0 + j][0] + 40 and px[x0 + i, y0 + j][2] >= px[x0 + i, y0 + j][1])
    return blue >= 40


def cell_zones(tags, im):
    own = {}
    for a in tags.placed():
        z = ZONE_OF.get(a.id)
        if z:
            for c in a.cells:
                own[c] = z
    out = {}
    pts = list(own.items())
    for cy in range(ROWS):
        for cx in range(COLS):
            if (cx, cy) in own:
                out[(cx, cy)] = own[(cx, cy)]
            elif is_sea(im, cx, cy):
                out[(cx, cy)] = None
            else:
                out[(cx, cy)] = min(pts, key=lambda p: (p[0][0] - cx) ** 2 + (p[0][1] - cy) ** 2)[1]
    return out


def blend(c, to, k):
    return tuple(int(c[i] * (1 - k) + to[i] * k) for i in range(3))


def edge(px, x0, y0, cx, cy, inside, colour):
    for (dx, dy) in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        if not inside(cx + dx, cy + dy):
            for t in range(8):
                x = x0 + (t if dy else (0 if dx < 0 else 7))
                y = y0 + (t if dx else (0 if dy < 0 else 7))
                px[x, y] = colour


def map_layer(region, zone, hover, glow, tags):
    if region == "tosa":
        im = EM.map_art(tags).convert("RGB")
        zones = cell_zones(tags, im)
    else:
        im = ET.map_art(tags.nodes()).convert("RGB")
        zones = None
    px = im.load()
    gold, gold_d, gold_l = K._NEUTRAL[SELECT], K._NEUTRAL[SELECT_DARK], K._NEUTRAL[SELECT_LIGHT]
    hov = set(hover.cells) if hover else set()
    for cy in range(ROWS):
        for cx in range(COLS):
            x0, y0 = GX + cx * 8, GY + cy * 8
            inzone = zones is None or zones[(cx, cy)] in (zone, None)
            for j in range(8):
                for i in range(8):
                    p = px[x0 + i, y0 + j]
                    if not inzone:
                        p = blend(p, DIM_TO, DIM_K)
                    elif (cx, cy) in hov:
                        p = blend(p, gold_l, 0.55 * glow)
                    px[x0 + i, y0 + j] = p
            if zones is not None and inzone and zones[(cx, cy)]:
                edge(px, x0, y0, cx, cy,
                     lambda x, y: not (0 <= x < COLS and 0 <= y < ROWS) or zones[(x, y)] in (zone, None), gold)
            if (cx, cy) in hov:
                edge(px, x0, y0, cx, cy, lambda x, y: (x, y) in hov, gold_d)
    return im.convert("RGBA")


PLATE = {"tosa": (6, 20), "tiksi": (122, 100)}
PLATE_W, PLATE_H = 112, 28
CTA = (6, 124, 76, 13)          # "Ⓐ Route View" pill, just above the tray's name pill
TAB_X0, TAB_W = 11, 40
TIME_CHIP = (214, 2, 22, 12)


def tab_cells(n):
    return [(TAB_X0 + k * (TAB_W + 4), 1) for k in range(n)]


def draw_map_frame(cv, region="tosa", n_tabs=2):
    """BG1 art of the map screen (also exported to the ROM by export_habitats.py). Tab pills are drawn
    in the normal palette; the selected one is a palette-1 (gold) swap of its cells."""
    ox, oy = PLATE[region]
    D.header_band(cv, 0, W - 1, round_left=False)
    rounded_box(cv, 2, 17, 236, 118, 4, TRANSPARENT, INK, ACCENT_DARK, ACCENT_LIGHT)
    for y in range(16, 136):
        for x in (0, 1, 238, 239):
            cv.set(x, y, ACCENT)
    D.tray(cv, 136)
    x, y, w, h = EM.NAME_PILL
    rounded_box(cv, x, y, w, h, 4, PANEL, INK, WHITE, PANEL_SHADE)
    rounded_box(cv, ox, oy, PLATE_W, PLATE_H, 4, PANEL, INK, WHITE, PANEL_SHADE)
    cv.hline(ox + 4, ox + PLATE_W - 5, oy + 13, PANEL_SHADE)
    cx_, cy_, cw, ch = CTA
    rounded_box(cv, cx_, cy_, cw, ch, 4, ACCENT, INK, ACCENT_LIGHT, ACCENT_DARK)
    tx, ty, tw, th = TIME_CHIP
    rounded_box(cv, tx, ty, tw, th, 4, PANEL, INK, WHITE, PANEL_SHADE)
    if n_tabs > 1:
        for (x, y) in tab_cells(n_tabs):
            D.tab_pill(cv, x, y, TAB_W)


def render_map(region="tosa", hover_id="MAPSEC_ROUTE_311", tabs=("TOSA", "TIKSI"), glow=1.0, tags=None,
               time="day", cta_lit=True):
    tags = tags or (RT.Tags(region="tosa") if region == "tosa" else ET.load_tags())
    hover = next(a for a in tags.placed() if a.id == hover_id)
    zone = ZONE_OF.get(hover_id, "NORTH") if region == "tosa" else None
    out = map_layer(region, zone, hover, glow, tags)
    pal = D.dex_palette("orchid")
    sel = D.selected(pal)
    tab_sel = 0 if region == "tosa" else 1
    ox, oy = PLATE[region]
    cx_, cy_, cw, ch = CTA
    tx, ty, tw, th = TIME_CHIP

    # BG1 frame
    art = new_sheet(W, H, "orchid", spare_a=D.BALL_RED)
    draw_map_frame(Canvas(art), region, len(tabs))
    out.alpha_composite(KX.sheet_rgba(art, pal))
    if len(tabs) > 1:
        x, y = tab_cells(len(tabs))[tab_sel]
        t = new_sheet(W, H, "orchid")
        D.tab_pill(Canvas(t), x, y, TAB_W)
        out.alpha_composite(KX.sheet_rgba(t, sel))

    # BG0 text + small OBJ pictograms
    txt = new_sheet(W, H, "orchid", spare_a=D.BALL_RED)
    tc = Canvas(txt)
    if len(tabs) > 1:
        for k, ((x, y), lab) in enumerate(zip(tab_cells(len(tabs)), tabs)):
            draw_text(tc, x + (TAB_W - text_width(lab, "narrow")) // 2, y - 1, lab, INK,
                      PANEL_SHADE if k != tab_sel else SELECT_DARK, font="narrow")
        title, tcx = "HABITATS", 156
    else:
        title, tcx = "TOSA HABITATS", 112
    draw_text(tc, tcx - text_width(title) // 2, 0, title, WHITE, ACCENT_DARK)
    stamp_rows(tc, tx + 7, ty + 2, SUN if time == "day" else MOON,
               {"#": SELECT_DARK if time == "day" else INK, "+": SELECT if time == "day" else INK_SOFT})
    # zone plate
    zsp = set()
    for a in tags.placed():
        if region != "tosa" or ZONE_OF.get(a.id) == zone:
            zsp |= species_of(a.id)
    zname = ZONE_NAME[zone] if region == "tosa" else "Tiksi"
    draw_text(tc, ox + 16, oy - 1, zname, INK, PANEL_SHADE)
    compass(tc, ox + 3, oy + 2, zone)
    counts_row(tc, ox + 4, oy + 13, counts(zsp))
    # CTA: Ⓐ Route View
    stamp_rows(tc, cx_ + 3, cy_ + 2, A_BTN, {"#": INK, "+": WHITE if cta_lit else PANEL_SHADE})
    draw_text(tc, cx_ + 15, cy_ - 2, "Route View", WHITE, ACCENT_DARK, font="narrow")
    # tray: route name + route counts
    x, y, w, h = EM.NAME_PILL
    draw_text(tc, x + 6, y - 1, hover.name, INK, PANEL_SHADE)
    counts_row(tc, 128, 140, counts(species_of(hover_id)))
    out.alpha_composite(KX.sheet_rgba(txt, pal))

    # OBJ: badge on every habitat where everything (day + night) is catalogued (colour ball) / captured (grey)
    obj = new_sheet(W, H, "orchid", spare_a=D.BALL_RED)
    oc = Canvas(obj)
    for a in tags.placed():
        sp = species_of(a.id)
        if not sp:
            continue
        cx, cy = a.node_cell
        if all(x in CATALOGUED for x in sp):
            badge(oc, GX + cx * 8, GY + cy * 8 - 3, "catalogued")
        elif all(x in CAPTURED for x in sp):
            badge(oc, GX + cx * 8, GY + cy * 8 - 3, "captured")
    out.alpha_composite(KX.sheet_rgba(obj, pal))
    if len(tabs) > 1:
        D.chevron(out, TAB_X0 - 6, 8)
        D.chevron(out, TAB_X0 + len(tabs) * (TAB_W + 4) + 2, 8, right=True)
    return out


# ------------------------------------------------------------------ route page
ROW_Y0, ROW_PITCH, ROWS_VISIBLE = 20, 27, 4
CHIP_X, CHIP_W = 3, 19
SLOT_X0, SLOT_W, SLOT_PITCH, SLOT_N = 25, 33, 35, 6
WELL_DY, WELL_H = 3, 23
TRAY_Y = 129
SEG = (200, 2, 36, 12)           # [sun | moon] toggle in the header


def route_rows(sec, time):
    rows = []
    for m in METHODS:
        tab = ENC.get(sec, {}).get(time, {}).get(m)
        if not tab:
            continue
        sps = sorted(tab, key=lambda s: -sum(tab[s]["rate"].values()))
        for k in range(0, len(sps), SLOT_N):
            rows.append((m, sps[k:k + SLOT_N], k == 0))
    return rows


LOCK = [".kkk.", "k...k", "k...k", "kkkkk", "kk.kk", "kkkkk"]
QMARK = ["..kkkk..", ".kk..kk.", ".....kk.", "....kk..", "...kk...", "...kk...", "........", "...kk..."]
RARE_PCT = 5      # a slot share at or below this (any method) counts as rare


def is_rare(sec, time, m, sp):
    e = ENC[sec][time][m][sp]
    return max(e["rate"].values()) <= RARE_PCT


def render_route(sec, cursor=(0, 0), time="day", frame=0, grid_scroll=0, top=0, tags=None, locked=(), rare_q=False):
    """locked: methods the player can't use yet (no Surf / no rod): padlock on the chip, wells greyed with a
    padlock, no icons. rare_q: unseen rare species show a "?" instead of their silhouette."""
    tags = tags or RT.Tags(region="tosa")
    area = next(a for a in tags.placed() if a.id == sec)
    pal = D.dex_palette("orchid")
    sel = D.selected(pal)
    out = KX.grid_frame(grid_scroll)
    rows = route_rows(sec, time)
    vis = list(enumerate(rows))[top:top + ROWS_VISIBLE]
    ry = lambda r: ROW_Y0 + (r - top) * ROW_PITCH

    art = new_sheet(W, H, "orchid", spare_a=D.BALL_RED)
    cv = Canvas(art)
    D.header_band(cv, 0, W - 1, round_left=False)
    sx, sy, sw, sh = SEG
    rounded_box(cv, sx, sy, sw, sh, 4, PANEL, INK, WHITE, PANEL_SHADE)
    cv.vline(sx + sw // 2, sy + 1, sy + sh - 2, INK)
    for r, (m, sps, first) in vis:
        y0 = ry(r)
        if first:
            rounded_box(cv, CHIP_X, y0 + WELL_DY, CHIP_W, WELL_H, 3, ACCENT, INK, ACCENT_LIGHT, ACCENT_DARK)
        for k in range(len(sps)):
            if (r, k) != cursor:
                if m in locked:
                    rounded_box(cv, SLOT_X0 + k * SLOT_PITCH, y0 + WELL_DY, SLOT_W, WELL_H, 3, PANEL_DARK, INK, PANEL_SHADE, PANEL_DARK)
                else:
                    D.well(cv, SLOT_X0 + k * SLOT_PITCH, y0 + WELL_DY, SLOT_W, WELL_H)
    D.tray(cv, TRAY_Y)
    out.alpha_composite(KX.sheet_rgba(art, pal))
    # gold palette swaps: selected well + selected half of the time toggle
    g = new_sheet(W, H, "orchid")
    gc = Canvas(g)
    r, k = cursor
    rounded_box(gc, SLOT_X0 + k * SLOT_PITCH, ry(r) + WELL_DY, SLOT_W, WELL_H, 3, SELECT, INK, SELECT_LIGHT, SELECT_DARK)
    half = (sx, sy, sw // 2 + 1, sh) if time == "day" else (sx + sw // 2, sy, sw - sw // 2, sh)
    rounded_box(gc, *half, 4, SELECT, INK, SELECT_LIGHT, SELECT_DARK)
    out.alpha_composite(KX.sheet_rgba(g, sel))

    txt = new_sheet(W, H, "orchid", spare_a=D.BALL_RED)
    tc = Canvas(txt)
    title = area.name
    tw = text_width(title)
    tcx = 106
    draw_text(tc, tcx - tw // 2, 0, title, WHITE, ACCENT_DARK)
    compass(tc, 4, 2, ZONE_OF.get(sec))
    stamp_rows(tc, sx + 4, sy + 2, SUN, {"#": SELECT_DARK if time == "day" else INK_SOFT,
                                          "+": SELECT_LIGHT if time == "day" else PANEL_SHADE})
    stamp_rows(tc, sx + sw // 2 + 5, sy + 2, MOON, {"#": INK if time == "night" else INK_SOFT,
                                                    "+": SELECT_LIGHT if time == "night" else PANEL_SHADE})
    for r2, (m, sps, first) in vis:
        if first:
            stamp_rows(tc, CHIP_X + 4, ry(r2) + WELL_DY + 6, PICTO[m], {"#": WHITE})
            if m in locked:      # padlock tab on the chip's lower edge
                rounded_box(tc, CHIP_X + 4, ry(r2) + WELL_DY + WELL_H - 6, 11, 9, 2, PANEL, INK, WHITE, PANEL_SHADE)
                stamp_rows(tc, CHIP_X + 7, ry(r2) + WELL_DY + WELL_H - 5, LOCK, {"k": INK})
    # tray: selected species, gated by how many times it has been captured
    m, sps, _ = rows[r]
    sp = sps[k]
    st = state(sp)
    e = ENC[sec][time][m][sp]
    name = name_of(sp) if st != "unseen" else "?????"
    draw_text(tc, 8, TRAY_Y + 2, name, INK, PANEL_SHADE)
    badge(tc, 12 + text_width(name), TRAY_Y + 7, st)      # grey ball = caught once, colour = catalogued
    if m == "fishing_mons":
        rod, pct = max(e["rate"].items(), key=lambda kv: kv[1])
        rate = "%s %d%%" % (rod, pct) if st == "catalogued" else "%s ?%%" % rod
    else:
        rate = "%s %d%%" % (METHOD_LABEL[m], sum(e["rate"].values())) if st == "catalogued" else METHOD_LABEL[m] + " ?%"
    if st in ("captured", "catalogued"):
        lv = "Lv.%d" % e["lv"][0] if e["lv"][0] == e["lv"][1] else "Lv.%d-%d" % tuple(e["lv"])
    else:
        lv = "Lv.?"
    if m in locked:
        rate, lv = {"water_mons": "Needs Surf", "fishing_mons": "Needs a Super Rod",
                    "rock_smash_mons": "Needs Rock Smash"}.get(m, "Locked"), ""
    stamp_rows(tc, 8, TRAY_Y + 18, PICTO[m], {"#": INK_SOFT})
    draw_text(tc, 22, TRAY_Y + 14, rate + "   " + lv, INK_SOFT, PANEL_SHADE, font="narrow")
    c3 = counts(species_of(sec, time))
    counts_row(tc, 160, TRAY_Y + 2, c3, total=False)
    tot = "%d species" % c3[3]
    draw_text(tc, 234 - text_width(tot, "narrow"), TRAY_Y + 15, tot, INK_SOFT, PANEL_SHADE, font="narrow")
    out.alpha_composite(KX.sheet_rgba(txt, pal))
    D.chevron(out, tcx - tw // 2 - 10, 8)
    D.chevron(out, tcx + tw // 2 + 10, 8, right=True)
    if top + ROWS_VISIBLE < len(rows):       # more rows below / above: small red chevrons, rotated
        _vchev(out, 233, TRAY_Y - 5, down=True)
    if top > 0:
        _vchev(out, 233, ROW_Y0 + 2, down=False)

    # OBJ icons + badges (captured / catalogued icons bob; selected one always animates)
    for r2, (m2, sps2, _) in vis:
        for k2, sp2 in enumerate(sps2):
            st2 = state(sp2)
            f = frame if st2 in ("captured", "catalogued") or ((r2, k2) == (r, k) and st2 != "unseen") else 0
            x0, y0 = SLOT_X0 + k2 * SLOT_PITCH, ry(r2) + WELL_DY
            if m2 in locked:
                lk = new_sheet(W, H, "orchid")
                stamp_rows(Canvas(lk), x0 + SLOT_W // 2 - 2, y0 + WELL_H // 2 - 3, LOCK, {"k": INK_SOFT})
                out.alpha_composite(KX.sheet_rgba(lk, pal))
                continue
            if rare_q and st2 == "unseen" and is_rare(sec, time, m2, sp2):
                qm = new_sheet(W, H, "orchid")
                stamp_rows(Canvas(qm), x0 + SLOT_W // 2 - 4, y0 + WELL_H // 2 - 4, QMARK, {"k": INK})
                out.alpha_composite(KX.sheet_rgba(qm, pal))
                continue
            out.alpha_composite(icon(sp2, st2, f), (x0, y0 + WELL_H - 30))
            b = new_sheet(W, H, "orchid", spare_a=D.BALL_RED)
            bc = Canvas(b)
            badge(bc, x0 + SLOT_W - 10, y0 + WELL_H - 10, st2)
            out.alpha_composite(KX.sheet_rgba(b, pal))
    return out


def _vchev(out, cx, cy, down=True):
    """The kit's 6x9 red chevron turned to point down / up (scroll hint)."""
    tmp = Image.new("RGBA", (12, 12), (0, 0, 0, 0))
    D.chevron(tmp, 6, 6, right=True)
    tmp = tmp.rotate(-90 if down else 90)
    out.alpha_composite(tmp, (cx - 6, cy - 6))


# ------------------------------------------------------------------ dex entry, gated by captures
def render_entry_states(species="WOOPER"):
    """INFO tab for one species: seen / captured once / catalogued."""
    import mock_dex as MD
    out = []
    for st in ("seen", "captured", "catalogued"):
        MD.ENTRIES[0] = {"num": 194, "const": species, "seen": True, "caught": st != "seen"}

        def body(tc, _ac, sp, st=st):
            if st == "captured":
                y = MD.DESC_Y
                draw_text(tc, MD.DESC_X, y, "Catch one more to catalogue it.", INK_SOFT, PANEL_SHADE)
            elif st == "catalogued":
                draw_text(tc, MD.DESC_X, MD.DESC_Y, sp["desc"], INK, PANEL_SHADE, line_h=MD.DESC_PITCH)
        im = MD.render_entry(entry_index=0, body=body if st != "seen" else None)
        if st == "captured":           # name-pill ball goes grey until the second capture
            g = new_sheet(W, H, "orchid")
            gc = Canvas(g)
            rounded_box(gc, MD.E_X + MD.E_W - 16, MD.E_NAME_Y + 2, 10, 10, 0, PANEL, PANEL, PANEL, PANEL)
            grey_ball(gc, MD.E_X + MD.E_W - 15, MD.E_NAME_Y + 3)
            im.alpha_composite(KX.sheet_rgba(g, D.dex_palette("orchid")))
        out.append(im)
    return out


# ------------------------------------------------------------------ output
def save(im, path, k=3):
    KX.upscale(im.convert("RGB"), k).save(path)


def gif(frames, path, ms, k=3):
    fr = [KX.upscale(f.convert("RGB"), k) for f in frames]
    fr[0].save(path, save_all=True, append_images=fr[1:], duration=ms, loop=0)


def write_data(out, tags):
    rows = []
    for a in tags.placed():
        sp = species_of(a.id)
        if not sp:
            continue
        day, night = species_of(a.id, "day"), species_of(a.id, "night")
        rows.append({"id": a.id, "name": a.name, "zone": ZONE_OF.get(a.id, "?"), "species": len(sp),
                     "day_only": sorted(name_of(x) for x in day - night),
                     "night_only": sorted(name_of(x) for x in night - day),
                     "methods": sorted({METHOD_LABEL[m] for t in ENC[a.id].values() for m in t})})
    json.dump(rows, open(os.path.join(out, "habitats.json"), "w"), indent=1)
    return rows


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    tags = RT.Tags(region="tosa")
    MARSH = "MAPSEC_MOONGROVE_MARSH"
    save(render_map("tosa", MARSH, tags=tags), os.path.join(out, "map_south.png"))
    save(render_map("tosa", "MAPSEC_ROUTE_311", tags=tags, time="night"), os.path.join(out, "map_west_night.png"))
    save(render_map("tosa", "MAPSEC_ROUTE_302", tabs=("TOSA",), tags=tags), os.path.join(out, "map_single.png"))
    save(render_map("tiksi", "MAPSEC_ROUTE_401"), os.path.join(out, "map_tiksi.png"))
    # route page: find a species of each state in the marsh by day for the stills
    rows = route_rows(MARSH, "day")
    want = {}
    for r, (m, sps, _) in enumerate(rows):
        for k, sp in enumerate(sps):
            want.setdefault(state(sp), (r, k))
    for st in ("unseen", "seen", "captured", "catalogued"):
        if st in want:
            r, k = want[st]
            top = max(0, r - ROWS_VISIBLE + 1)
            save(render_route(MARSH, (r, k), "day", top=top, tags=tags), os.path.join(out, "route_%s.png" % st))
    nrows = route_rows(MARSH, "night")
    night_only = species_of(MARSH, "night") - species_of(MARSH, "day")
    cur = next(((r, k) for r, (m, sps, _) in enumerate(nrows) for k, sp in enumerate(sps) if sp in night_only), (0, 0))
    save(render_route(MARSH, cur, "night", tags=tags), os.path.join(out, "route_night.png"))
    for n, im in enumerate(render_entry_states("WOOPER")):
        save(im, os.path.join(out, "entry_%d.png" % n))
    # motion: map hops (CTA pulses), route page day -> night flip
    hops = ["MAPSEC_ROUTE_311", "MAPSEC_ROUTE_313", "MAPSEC_ROUTE_314", "MAPSEC_SOUTH_TOSA_RESERVE_1", MARSH]
    frames = []
    for h in hops:
        for i, g in enumerate((1.0, 0.75, 0.5, 0.75)):
            frames.append(render_map("tosa", h, glow=g, tags=tags, cta_lit=i < 2))
    gif(frames, os.path.join(out, "map_cursor.gif"), 140)
    frames = []
    for t, cur2 in (("day", (0, 0)), ("day", (0, 1)), ("night", (0, 1)), ("night", (0, 2)), ("night", (1, 0))):
        for f in (0, 1, 0, 1):
            frames.append(render_route(MARSH, cur2, t, frame=f, grid_scroll=len(frames), tags=tags))
    gif(frames, os.path.join(out, "route_daynight.gif"), 160)
    print(len(write_data(out, tags)), "habitats with wild tables")
