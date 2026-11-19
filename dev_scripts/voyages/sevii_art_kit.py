"""
Helpers for the gTileset_SeviiIslands art additions (sevii_tileset.py art section; design-review mockup only).

  ent(tile, pal, st)        8x8 colour-index grid -> metatile entry; re-uses an identical tile (also h/v-flipped)
                            that already exists in gTileset_General, in a KEPT gTileset_Rustboro slot, or among
                            the new tiles, before spending a free slot (st.add_tiles)
  quad(img16, pal, st)      16x16 index grid -> 4 entries (TL, TR, BL, BR)
  meta(...)                 add_metatile wrapper that also de-duplicates identical (entries, attr) metatiles
  remap(tile, src_pal, dst_pal, fixed)  nearest-colour index remap (RGB distance), fixed {src idx: dst idx}
  grid(rows, legend)        ASCII art -> index rows
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import voyage_compose as vc      # noqa: E402

GEN_RB = ("gTileset_General", "gTileset_Rustboro")
T, H, V = 0x3FF, 0x400, 0x800


def E(tile, pal, h=False, v=False):
    return tile | (H if h else 0) | (V if v else 0) | (pal << 12)


def _flips(t):
    yield t, False, False
    yield [r[::-1] for r in t], True, False
    yield t[::-1], False, True
    yield [r[::-1] for r in t[::-1]], True, True


_INDEX = None


def _index(st):
    """{tuple(tile): tile number} for General tiles and the Rustboro tiles the Sevii copy keeps."""
    global _INDEX
    if _INDEX is None:
        st._ensure_free()
        sc = vc.scene(GEN_RB)
        free = set(st.FREE_TILES)
        idx = {}
        for i in range(sc.p.n):
            idx.setdefault(_key(sc.p.tile(i)), i)
        for i in range(sc.s.n):
            if i not in free:
                idx.setdefault(_key(sc.s.tile(i)), 512 + i)
        _INDEX = idx
    return _INDEX


def _key(t):
    return tuple(tuple(r) for r in t)


def ent(tile, pal, st, reuse=True):
    """-> metatile entry for an 8x8 index grid drawn with palette slot pal."""
    tile = [list(r) for r in tile]
    if not any(any(r) for r in tile):
        return E(0, pal)
    if reuse:
        idx = _index(st)
        for t, h, v in _flips(tile):
            if _key(t) in idx:
                return E(idx[_key(t)], pal, h, v)
    for t, h, v in _flips(tile):
        for k, have in st._TILES.items():
            if have == t:
                return E(512 + k, pal, h, v)
    return E(st.add_tiles([tile])[0], pal)


def quad(img, pal, st):
    """16x16 index grid -> [TL, TR, BL, BR] entries."""
    out = []
    for oy in (0, 8):
        for ox in (0, 8):
            out.append(ent([r[ox:ox + 8] for r in img[oy:oy + 8]], pal, st))
    return out


_META_BY_KEY = {}


def meta(st, label, entries, behaviour="MB_NORMAL", layer=0, coll=0, elev=0):
    """add_metatile, sharing one metatile id between identical (entries, behaviour, layer)."""
    key = (tuple(entries), behaviour, layer)
    if key in _META_BY_KEY:
        mid = _META_BY_KEY[key]
        return mid | (coll << 10) | (elev << 12)
    raw = st.add_metatile(label, entries, behaviour, layer, coll, elev)
    _META_BY_KEY[key] = raw & 0x3FF
    return raw


def tile_of(ts, i):
    """8x8 index grid of tile number i (>= 512: secondary) in a vanilla.Scene-like object."""
    return ts.p.tile(i) if i < 512 else ts.s.tile(i - 512)


def entry_tile(sc, e):
    """The 8x8 grid an entry shows (flips applied) in scene sc."""
    t = tile_of(sc, e & T)
    if e & H:
        t = [r[::-1] for r in t]
    if e & V:
        t = t[::-1]
    return [list(r) for r in t]


def split16(img):
    return [[r[ox:ox + 8] for r in img[oy:oy + 8]] for oy in (0, 8) for ox in (0, 8)]


def join16(tiles):
    """[TL, TR, BL, BR] 8x8 -> 16x16."""
    return [tiles[0][y] + tiles[1][y] for y in range(8)] + [tiles[2][y] + tiles[3][y] for y in range(8)]


def dist(a, b):
    # weighted RGB distance (green counts most, as the eye does)
    return 2 * (a[0] - b[0]) ** 2 + 4 * (a[1] - b[1]) ** 2 + 3 * (a[2] - b[2]) ** 2


def nearest_map(src_pal, dst_pal, fixed=None, allowed=None):
    """{src index: dst index} by nearest colour (index 0 stays 0)."""
    fixed = fixed or {}
    allowed = [i for i in (allowed or range(1, 16))]
    m = {0: 0}
    for i in range(1, 16):
        if i in fixed:
            m[i] = fixed[i]
        else:
            m[i] = min(allowed, key=lambda j: dist(src_pal[i], dst_pal[j]))
    return m


def remap(tile, m):
    return [[m[v] for v in r] for r in tile]


def grid(rows, legend):
    """ASCII rows -> index rows; legend {char: index}; '.' = 0."""
    out = []
    for r in rows:
        out.append([0 if c == "." else legend[c] if c in legend else int(c, 16) for c in r])
    return out
