"""
Newmoon / Fullmoon region map (REGION_MAP_SINNOH, user request 2026-11-19): the Gen 4 Sinnoh Town Map
(ref/sinnoh_map_gen4.png, 216x168) redrawn as a Gen 3 region map, then masked with the Eon map's baked intro
clouds (eon_clouds.py) so only Newmoon + Fullmoon (the two islets at the top left) and a little sea show.

Conversion (convert()):
  * the whole Sinnoh map is scaled by 5/7 (168 px -> the 120 px map window, tile rows 2-16) and centred;
  * land / sea / route / town / lake are classified from the DS colours; the DS relief shades (dark rim green
    .. ochre highland) become an elevation field, blurred and banded into Hoenn's five greens (snapped to
    BGR555 like the Tosa / Tiksi / Holon art); a 1-2 px dark green rim follows the coast;
  * routes: the DS 8 px route grid is mapped cell -> cell onto the 8 px region-map grid (connectivity kept),
    drawn Hoenn-style: whole cells in the route yellows, banded by the same elevation field; route cells over
    the sea get Hoenn's blue sea-route stripes;
  * towns / cities: vanilla Hoenn marker tiles (blue disc / red pill) on the mapped cell; lakes = inland water;
  * sea = Hoenn's striped sea tile.
Masking (masked()): eon_clouds.dense_place lattices + wisps over the converted map, with a clear window round
the two islets. BG2 is affine 8bpp: <= 256 tiles, no flips (counted by the caller).

usage: <venv python> dev_scripts/voyages/regionmap/sinnoh_moons.py   (writes previews + the 3x compare to
       dev_scripts/voyages/regionmap/shots_sinnoh/; export_region_maps.py ships the masked map)
"""
import math
import os
import random
import sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rm_common as C  # noqa: E402
import eon_clouds as E  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

SRC = os.path.join(HERE, "..", "ref", "sinnoh_map_gen4.png")
SHOTS = os.path.join(HERE, "shots_sinnoh")
W, H = 240, 160
SCALE = 5 / 7                    # 168 px -> 120 px (tile rows 2-16)
OX, OY = 40, 16                  # where the source's top-left lands (154 x 120 px)

# Gen 3 colours (vanilla Hoenn map, snapped to BGR555 = the Tosa / Tiksi / Holon art's values)
GREENS = [(0, 112, 0), (56, 168, 8), (96, 208, 0), (168, 232, 48), (208, 248, 120)]
YELLOWS = [(224, 160, 0), (232, 184, 56), (240, 208, 80), (232, 224, 112)]
SEA = [(152, 208, 248), (160, 176, 248)]
SEA_ROUTE = [(72, 152, 224), (40, 128, 224)]

CITY = {(240, 103, 103), (191, 55, 55), (248, 159, 159)}
TOWN = {(111, 135, 248), (71, 95, 208), (159, 183, 240)}
BORDER = {(224, 224, 224), (175, 175, 175), (248, 248, 248), (216, 216, 159)}
LAKE = {(95, 240, 208)}
MARK = {(143, 208, 39), (167, 232, 71), (95, 159, 8)}           # small green landmark icons
LEVEL = {(87, 143, 8): 0.0, (111, 175, 47): 1.0, (135, 200, 71): 1.6, (159, 216, 95): 2.4,
         (143, 159, 31): 2.9, (208, 191, 71): 3.7}

# the islets (source px bboxes), left = Newmoon (west of Fullmoon, as in DPPt)
ISLETS = {"MAPSEC_NEWMOON_ISLAND": (4, 11, 18, 31), "MAPSEC_FULLMOON_ISLAND": (28, 11, 43, 31)}


def kind(p):
    if p in CITY:
        return "city"
    if p in TOWN:
        return "town"
    if p in LAKE:
        return "lake"
    if p in BORDER or p in MARK:
        return "mark"
    if p in LEVEL:
        return "land"
    if p[0] >= 240 and 140 <= p[1] <= 215 and p[2] < 130:
        return "route"
    if p[2] > p[0] and p[2] >= p[1] - 8:
        return "sea"
    return "land"


def load_src():
    im = Image.open(SRC).convert("RGB")
    px = im.load()
    K = [[kind(px[x, y]) for x in range(im.width)] for y in range(im.height)]
    return im, px, K


def src_of(x, y):
    """target px -> source px (nearest, pixel centres), or None outside the source."""
    sx, sy = math.floor((x - OX + 0.5) / SCALE), math.floor((y - OY + 0.5) / SCALE)
    return (sx, sy) if 0 <= sx < 216 and 0 <= sy < 168 else None


def bfs_fill(val, known, w, h):
    """nearest-known fill of a 2D float field."""
    q = deque((x, y) for y in range(h) for x in range(w) if known[y][x])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not known[ny][nx]:
                known[ny][nx] = True
                val[ny][nx] = val[y][x]
                q.append((nx, ny))


def blur(f, w, h, r):
    out = [[0.0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            s = n = 0
            for j in range(-r, r + 1):
                for i in range(-r, r + 1):
                    xx, yy = x + i, y + j
                    if 0 <= xx < w and 0 <= yy < h:
                        s += f[yy][xx]
                        n += 1
            out[y][x] = s / n
    return out


def sea_px(x, y, ramp=SEA):
    # Hoenn's sea tile: light rows 0-1, dark row 2, light row 3 ... (stripes repeat every 4 rows)
    return ramp[1] if y % 4 in (2, 3) else ramp[0]


def vanilla_markers():
    """{'town': 8x8 RGB rows, 'city': 8x8} copied from the vanilla Hoenn map (Oldale / Fortree)."""
    sheet, tmap, rows = C.vanilla_hoenn()
    v = C.bg2_from(sheet, tmap).convert("RGB")
    secs = C.sections_of(rows)
    out = {}
    for k, s in (("town", "MAPSEC_OLDALE_TOWN"), ("city", "MAPSEC_FORTREE_CITY")):
        cx, cy = secs[s][0]
        x0, y0 = C.cell_px((cx, cy))
        out[k] = [[tuple(c // 8 * 8 for c in v.getpixel((x0 + i, y0 + j))) for i in range(8)] for j in range(8)]
    return out


def components(mask, w, h):
    """4-connected components of a bool grid -> (label grid, [sizes])."""
    lab = [[-1] * w for _ in range(h)]
    sizes = []
    for y in range(h):
        for x in range(w):
            if mask[y][x] and lab[y][x] < 0:
                n, q = 0, deque([(x, y)])
                lab[y][x] = len(sizes)
                while q:
                    cx, cy = q.popleft()
                    n += 1
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < w and 0 <= ny < h and mask[ny][nx] and lab[ny][nx] < 0:
                            lab[ny][nx] = len(sizes)
                            q.append((nx, ny))
                sizes.append(n)
    return lab, sizes


def thin(mask, w, h):
    """Zhang-Suen thinning (route bands -> 1 px centrelines)."""
    m = [row[:] for row in mask]
    changed = True
    while changed:
        changed = False
        for step in (0, 1):
            kill = []
            for y in range(1, h - 1):
                for x in range(1, w - 1):
                    if not m[y][x]:
                        continue
                    p = [m[y - 1][x], m[y - 1][x + 1], m[y][x + 1], m[y + 1][x + 1], m[y + 1][x], m[y + 1][x - 1],
                         m[y][x - 1], m[y - 1][x - 1]]
                    b = sum(p)
                    a = sum(1 for i in range(8) if not p[i] and p[(i + 1) % 8])
                    if not (2 <= b <= 6 and a == 1):
                        continue
                    if step == 0 and (p[0] and p[2] and p[4] or p[2] and p[4] and p[6]):
                        continue
                    if step == 1 and (p[0] and p[2] and p[6] or p[0] and p[4] and p[6]):
                        continue
                    kill.append((x, y))
            for x, y in kill:
                m[y][x] = False
            changed = changed or bool(kill)
    return m


def tcell(sx, sy):
    """source px -> target screen tile."""
    return int((OX + (sx + 0.5) * SCALE) // 8), int((OY + (sy + 0.5) * SCALE) // 8)


def convert():
    """-> (RGB 240x160 Gen 3 map, {mapsec: screen tile of the islet}, route cells, marker cells)."""
    im, px, K = load_src()
    sw, sh = im.width, im.height
    solid = [[K[y][x] != "sea" for x in range(sw)] for y in range(sh)]
    lab, sizes = components(solid, sw, sh)
    main = {i for i, n in enumerate(sizes) if n >= 400}      # Sinnoh's landmasses; the rest are islets
    is_main = lambda x, y: lab[y][x] in main
    routeK = {"route", "city", "town", "mark"}
    rmask = [[K[y][x] in routeK and is_main(x, y) for x in range(sw)] for y in range(sh)]

    def over_sea(x, y):
        # a route band drawn over open water: sea 6 px out on both sides (left/right or up/down)
        sea = lambda xx, yy: not (0 <= xx < sw and 0 <= yy < sh) or K[yy][xx] == "sea"
        return (sea(x - 6, y) and sea(x + 6, y)) or (sea(x, y - 6) and sea(x, y + 6))
    water = [[rmask[y][x] and over_sea(x, y) for x in range(sw)] for y in range(sh)]
    # elevation at source res: DS shade -> level, routes / markers / lakes filled from the nearest land
    lev = [[LEVEL.get(px[x, y], 0.0) for x in range(sw)] for y in range(sh)]
    known = [[K[y][x] == "land" and px[x, y] in LEVEL for x in range(sw)] for y in range(sh)]
    bfs_fill(lev, known, sw, sh)
    lev = blur(lev, sw, sh, 2)

    out = Image.new("RGB", (W, H))
    o = out.load()
    land = [[False] * W for _ in range(H)]
    el = [[0.0] * W for _ in range(H)]
    lake = [[False] * W for _ in range(H)]
    small = [[False] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            s = src_of(x, y)
            if s is None:
                continue
            sx, sy = s
            small[y][x] = solid[sy][sx] and not is_main(sx, sy)
            land[y][x] = solid[sy][sx] and not water[sy][sx]
            lake[y][x] = K[sy][sx] == "lake"
            el[y][x] = lev[sy][sx]
    for y in range(1, H - 1):                       # lone specks
        for x in range(1, W - 1):
            if land[y][x] and not any(land[y + j][x + i] for i, j in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                land[y][x] = False
    dist = [[0 if not land[y][x] else 99 for x in range(W)] for y in range(H)]
    q = deque((x, y) for y in range(H) for x in range(W) if not land[y][x])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and dist[ny][nx] > dist[y][x] + 1:
                dist[ny][nx] = dist[y][x] + 1
                q.append((nx, ny))
    rnd = random.Random(4)
    noise = [[rnd.random() for _ in range(W)] for _ in range(H)]
    noise = blur(blur(noise, W, H, 2), W, H, 2)
    elev = lambda x, y: el[y][x] + (noise[y][x] - 0.5) * 2.2 + min(dist[y][x], 8) * 0.12

    for y in range(H):
        for x in range(W):
            if lake[y][x]:
                o[x, y] = sea_px(x, y, SEA_ROUTE)
            elif land[y][x]:
                d = dist[y][x]
                if small[y][x]:                     # islets: 1 px rim, a lighter heart (Southern Island-like)
                    o[x, y] = GREENS[0 if d <= 1 else 1 if d <= 2 else 2]
                    continue
                o[x, y] = GREENS[0 if d <= 2 else max(1 if d > 3 else 0, min(4, int(elev(x, y))))]
            else:
                o[x, y] = sea_px(x, y)

    # routes (v2, user: "thin Gen 3 route lines, towns not bunched"):
    #   DS route bands -> centrelines -> the 8 px cells they pass through; towns placed first and nudged apart;
    #   the cell set is thinned to 1-cell lines (towns fixed) and re-joined 4-way; each cell then gets a
    #   vanilla Hoenn route tile (land) or sea-route tile (water)
    skel = thin(rmask, sw, sh)
    land_cells = {(x // 8, y // 8) for y in range(OY, OY + 120) for x in range(W) if land[y][x]}
    land_n = lambda t: sum(land[t[1] * 8 + j][t[0] * 8 + i] for j in range(8) for i in range(8)) \
        if 0 <= t[0] < 30 and 2 <= t[1] <= 16 else 0
    rcells, water_hits = set(), {}
    for y in range(sh):
        for x in range(sw):
            if skel[y][x]:
                t = tcell(x, y)
                rcells.add(t)
                water_hits[t] = water_hits.get(t, 0) + (1 if water[y][x] else -1)
    # islets are places, not routes
    islets, islet_cells = {}, set()
    for m, (x0, y0, x1, y1) in ISLETS.items():
        best = {}
        for sy in range(y0, y1):
            for sx in range(x0, x1):
                if solid[sy][sx]:
                    t = tcell(sx, sy)
                    best[t] = best.get(t, 0) + 1
        islets[m] = max(best, key=best.get)
        islet_cells |= set(best)
    rcells -= islet_cells
    # towns / cities: one marker per DS marker blob (cities first), nudged until no two touch (8-neighbourhood)
    blobs = []
    for k in ("city", "town"):
        mk_mask = [[K[y][x] == k for x in range(sw)] for y in range(sh)]
        mlab, msz = components(mk_mask, sw, sh)
        for i, n in enumerate(msz):
            if n < 12:
                continue
            pts = [(x, y) for y in range(sh) for x in range(sw) if mlab[y][x] == i]
            blobs.append((k, sum(p[0] for p in pts) / n, sum(p[1] for p in pts) / n))
    markers = {}
    for k, cx, cy in blobs:
        want = tcell(cx, cy)
        ok = lambda t: (land_n(t) >= 24 and t not in islet_cells
                        and all(max(abs(t[0] - u[0]), abs(t[1] - u[1])) >= 2 for u in markers))
        cands = sorted(((tx, ty) for tx in range(want[0] - 3, want[0] + 4) for ty in range(want[1] - 3, want[1] + 4)),
                       key=lambda t: (abs(t[0] - want[0]) + abs(t[1] - want[1]), t not in rcells))
        for t in cands:
            if ok(t):
                markers[t] = k
                break
        else:
            print("!! no room for a %s near %s" % (k, want))

    def bfs_link(a, targets):
        """shortest 4-way path over land cells from cell a to any target cell (inclusive)."""
        prev, q = {a: None}, deque([a])
        while q:
            c = q.popleft()
            if c in targets and c != a:
                path = []
                while c is not None:
                    path.append(c)
                    c = prev[c]
                return path
            for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (c[0] + d[0], c[1] + d[1])
                if n not in prev and (n in land_cells or n in targets) and n not in islet_cells:
                    prev[n] = c
                    q.append(n)
        return []
    rcells |= set(markers)
    for t in markers:                          # nudged towns join the nearest route
        if not any((t[0] + d[0], t[1] + d[1]) in rcells for d in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            rcells |= set(bfs_link(t, rcells - {t}))
    rcells = thin_cells(rcells, set(markers))
    rcells = join4(rcells, land_cells)
    sea_route = {t for t in rcells if t not in land_cells or (water_hits.get(t, 0) > 0 and land_n(t) < 40)}

    tiles = vanilla_route_tiles()
    for (tx, ty) in rcells:
        if not (2 <= ty <= 16) or (tx, ty) in markers:
            continue
        if (tx, ty) in sea_route:
            t = tiles["sea"][(tx * 7 + ty * 3) % len(tiles["sea"])]
        else:
            # vanilla land route tiles, sorted dark -> light; the local elevation picks one (blobs follow relief)
            e = sum(elev(tx * 8 + i, ty * 8 + j) for j in range(8) for i in range(8)) / 64
            n = len(tiles["land"])
            t = tiles["land"][max(0, min(n - 1, int((e - 1.0) / 3.0 * n) + (tx * 5 + ty * 3) % 3 - 1))]
        for j in range(8):
            for i in range(8):
                o[tx * 8 + i, ty * 8 + j] = t[j][i]
    mk = vanilla_markers()
    for (tx, ty), k in markers.items():
        if 2 <= ty <= 16:
            for j in range(8):
                for i in range(8):
                    o[tx * 8 + i, ty * 8 + j] = mk[k][j][i]
    return out, islets, rcells, markers


def thin_cells(cells, keep):
    """Zhang-Suen on the 30x20 cell grid (cells in `keep` never removed) -> 1-cell-wide lines."""
    m = [[(x, y) in cells for x in range(32)] for y in range(22)]
    changed = True
    while changed:
        changed = False
        for step in (0, 1):
            kill = []
            for y in range(1, 21):
                for x in range(1, 31):
                    if not m[y][x] or (x, y) in keep:
                        continue
                    p = [m[y - 1][x], m[y - 1][x + 1], m[y][x + 1], m[y + 1][x + 1], m[y + 1][x], m[y + 1][x - 1],
                         m[y][x - 1], m[y - 1][x - 1]]
                    b = sum(p)
                    a = sum(1 for i in range(8) if not p[i] and p[(i + 1) % 8])
                    if not (2 <= b <= 6 and a == 1):
                        continue
                    if step == 0 and (p[0] and p[2] and p[4] or p[2] and p[4] and p[6]):
                        continue
                    if step == 1 and (p[0] and p[2] and p[6] or p[0] and p[4] and p[6]):
                        continue
                    kill.append((x, y))
            for x, y in kill:
                m[y][x] = False
            changed = changed or bool(kill)
    return {(x, y) for y in range(22) for x in range(32) if m[y][x]}


def join4(cells, land_cells):
    """diagonal-only steps -> add the corner cell (land preferred) so every line is 4-connected."""
    cells = set(cells)
    for (x, y) in sorted(cells):
        for dx in (1, -1):
            n = (x + dx, y + 1)
            a, b = (x + dx, y), (x, y + 1)
            if n in cells and a not in cells and b not in cells:
                cells.add(a if (a in land_cells or b not in land_cells) else b)
    return cells


def vanilla_route_tiles():
    """Vanilla Hoenn region-map route tiles, snapped to BGR555: 'land' = all-yellow tiles sorted dark -> light,
    'sea' = all-blue sea-route tiles."""
    sheet, tmap, rows = C.vanilla_hoenn()
    v = C.bg2_from(sheet, tmap).convert("RGB")
    secs = C.sections_of(rows)
    land, sea, seen = [], [], set()
    for s, cells in secs.items():
        if "ROUTE" not in s:
            continue
        for c in cells:
            x0, y0 = C.cell_px(c)
            t = tuple(tuple(tuple(ch // 8 * 8 for ch in v.getpixel((x0 + i, y0 + j))) for i in range(8)) for j in range(8))
            if t in seen:
                continue
            seen.add(t)
            cols = {p for r in t for p in r}
            if cols <= set(YELLOWS):
                land.append(t)
            elif cols <= set(SEA_ROUTE):
                sea.append(t)
    lum = lambda t: sum(sum(p) for r in t for p in r)
    land.sort(key=lum)
    assert land and sea, (len(land), len(sea))
    return {"land": land, "sea": sea}


# ------------------------------------------------------------------ clouds
def clear_window(islets):
    """px rectangle left clear: the islets' bbox (source ISLETS scaled) + a little sea, stopping short of the
    mainland's west coast (target x 72+)."""
    x0 = min(v[0] for v in ISLETS.values())
    y0 = min(v[1] for v in ISLETS.values())
    x1 = max(v[2] for v in ISLETS.values())
    y1 = max(v[3] for v in ISLETS.values())
    tx0, ty0 = int(OX + x0 * SCALE) - 6, int(OY + y0 * SCALE) - 6
    tx1, ty1 = int(OX + x1 * SCALE) + 6, int(OY + y1 * SCALE) + 6
    return (tx0, max(OY, ty0), min(tx1, 72), ty1)


def masked(rgb, islets):
    """rgb Gen 3 map -> 'P' image (palette: index 112 + 1.. = map colours, 141-144 clouds) with the Eon
    clouds baked over everything but the islets' window."""
    cols = []
    for c in rgb.getdata():
        if c not in cols:
            cols.append(c)
    assert len(cols) <= 28, len(cols)                  # 113..140; 141-143 clouds, 144 sky (eon_clouds)
    im = Image.new("P", (W, H))
    pal = [0] * 768
    for i, c in enumerate(cols):
        pal[(113 + i) * 3:(113 + i) * 3 + 3] = list(c)
    im.putpalette(pal)
    idx = {c: 113 + i for i, c in enumerate(cols)}
    im.putdata([idx[c] for c in rgb.getdata()])
    win = clear_window(islets)
    old = (E.WINDOW, E.WINDOW_CUT, E.WINDOW_CUT2)
    wx0, wy0, wx1, wy1 = win
    E.WINDOW = win
    E.WINDOW_CUT = (wx1 - 6, wy0, wx1, wy0 + 6)        # stepped corners, like Eon's window
    E.WINDOW_CUT2 = (wx0, wy1 - 6, wx0 + 6, wy1)
    try:
        place = cover_land(rgb, list(E.DENSE))
        out = E.build(im, "map", place)
    finally:
        E.WINDOW, E.WINDOW_CUT, E.WINDOW_CUT2 = old
    return out


def cover_land(rgb, place):
    """Eon's lattice leaves holes (it drops every stamp touching the clear window); Sinnoh's mainland comes
    right up to the islets, so add stamps greedily until no land pixel outside the window shows."""
    sea = set(SEA) | set(SEA_ROUTE)
    rp = rgb.load()
    shapes = {}
    for name in E.STAMPS:
        for mir in (False, True):
            st = E.stamp_img(name, mir)
            sp = st.load()
            shapes[(name, mir)] = [(x, y) for y in range(st.height) for x in range(st.width) if sp[x, y] in E.CLOUD_REMAP]

    def covered_by(pl):
        cov = set()
        for name, tx, ty, mir in pl:
            if E.fits(name, tx, ty, mir):
                cov.update((tx * 8 + x, ty * 8 + y) for x, y in shapes[(name, mir)])
        return cov
    cov = covered_by(place)
    todo = {(x, y) for y in range(OY, OY + 120) for x in range(W)
            if rp[x, y] not in sea and (x, y) not in cov and not E.in_window(x, y)}
    cands = [(n, tx, ty, m) for (n, m) in shapes for ty in range(0, 17) for tx in range(-3, 30)
             if E.fits(n, tx, ty, m)]
    while todo:
        best, gain = None, 0
        for c in cands:
            n, tx, ty, m = c
            g = sum((tx * 8 + x, ty * 8 + y) in todo for x, y in shapes[(n, m)])
            if g > gain:
                best, gain = c, g
        if best is None:
            break
        place.append(best)
        n, tx, ty, m = best
        todo -= {(tx * 8 + x, ty * 8 + y) for x, y in shapes[(n, m)]}
    if todo:
        print("!! land left uncovered:", len(todo))
    return place


def screen(bg2, islets, here):
    names = {"MAPSEC_NEWMOON_ISLAND": "Newmoon Island", "MAPSEC_FULLMOON_ISLAND": "Fullmoon Island"}
    cell = lambda t: (t[0] - 1, t[1] - 2)
    return C.screen(bg2, "SINNOH", names[here], [], cursor=cell(islets[here]), here=cell(islets[here]))


def main():
    os.makedirs(SHOTS, exist_ok=True)
    rgb, islets, rcells, markers = convert()
    src = Image.open(SRC).convert("RGB")
    # side by side at 3x: source | v1 (route blocks, kept as shots_sinnoh/sinnoh_gen3_v1_blocks.png) | current
    # conversion (whole 240x160 BG; tile rows 0-1 / 17-19 sit under the frame)
    pad = 12
    panels = [("Gen 4 source (216x168)", src)]
    old = os.path.join(SHOTS, "sinnoh_gen3_v1_blocks.png")
    if os.path.exists(old):
        panels.append(("old: v1 route blocks", Image.open(old).convert("RGB")))
    view = rgb.copy()
    ImageDraw.Draw(view).rectangle([0, 16, W - 1, 135], outline=(255, 0, 255))
    panels.append(("new: Gen 3 route tiles (frame window magenta)", view))
    strip = Image.new("RGB", (sum(p.width for _, p in panels) + pad * (len(panels) + 1), max(src.height, H) + 22),
                      (40, 40, 48))
    d = ImageDraw.Draw(strip)
    x = pad
    for label, p in panels:
        strip.paste(p, (x, 18))
        d.text((x, 3), label, fill=(255, 255, 255))
        x += p.width + pad
    strip.resize((strip.width * 3, strip.height * 3), Image.NEAREST).save(os.path.join(SHOTS, "sinnoh_compare@3x.png"))
    rgb.save(os.path.join(SHOTS, "sinnoh_gen3_unmasked.png"))
    m = masked(rgb, islets)
    tiles, _ = E.to_rom(m)
    m.convert("RGB").save(os.path.join(SHOTS, "sinnoh_masked_bg2.png"))
    for here in islets:
        scr = screen(m, islets, here)
        scr.convert("RGB").resize((W * 3, H * 3), Image.NEAREST).save(
            os.path.join(SHOTS, "mock_%s@3x.png" % here[7:].lower()))
    print("islets (screen tiles)", islets, "route cells", len(rcells), "markers", len(markers),
          "masked tiles", len(tiles), "colours", len(set(rgb.getdata())))


if __name__ == "__main__":
    main()
