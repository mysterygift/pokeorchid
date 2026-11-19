"""
PROPOSED secondary tileset gTileset_SeviiIslands (design-review mockup only; nothing is written to data/).

= a COPY of gTileset_Rustboro (same metatile ids 0x200-0x36C, so every Sevii spec built on General + Rustboro
renders the same) used ONLY by the Sevii maps, plus additions that would otherwise have to go into a shared
vanilla tileset (Rustboro is also used by Route 116, Southern Island, Faraway Island, Ube City):

  * arrow-warp duplicates  FRLG's arrow warps (harbour boardwalks, Berry Forest / Bond Bridge exits): a copy
                           of the metatile drawn on the warp cell with MB_{N,S,E,W}_ARROW_WARP  (arrow())
  * art additions          cottage variants, Two Island market stall, Memorial Pillar's Onix tails (FRLG
                           port), Five Isle Meadow's Rocket Warehouse (Cold Storage exterior recoloured)
                           -- registered by the art section below (add_tiles / add_metatile / STAMPS)

voyage_compose.scene(("gTileset_General", "gTileset_SeviiIslands")) draws Rustboro + these extras
(voyage_compose.VIRTUAL_MODULES). New metatile ids follow Rustboro's last one, new tiles follow its tiles.
budget() reports what is left of the secondary limits (512 tiles, 512 metatiles, palette slots 6-12).
"""
import os
import re
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
BASE = "gTileset_Rustboro"
PRIMARY = "gTileset_General"
BASE_DIR = os.path.join(ROOT, "data", "tilesets", "secondary", "rustboro")
MB = re.findall(r"^\s+(MB_\w+)", open(os.path.join(ROOT, "include", "constants", "metatile_behaviors.h")).read(),
                re.M)

_TILES = {}          # {secondary tile index: 8x8 colour indices} new art, written into FREE tile slots
_PALS = {}           # {slot: [16 (r, g, b)]} replaced / filled palette slots (secondary slots 6-12)
_META = []           # (label, 8 tile entries, attr u16)
RAW = {}             # label -> raw block value (metatile id | collision << 10 | elevation << 12)
STAMPS = {}          # name -> dict(cells=[[raw or None]], door=(dx, dy) or None, note=str)
LABELS = {}          # label -> metatile id


def _base_counts():
    n_meta = os.path.getsize(os.path.join(BASE_DIR, "metatiles.bin")) // 16
    return n_meta


BASE_METATILES = _base_counts()


def base_tile_count():
    """Tiles Rustboro really uses: 1 + the highest secondary tile index any of its metatiles references."""
    raw = open(os.path.join(BASE_DIR, "metatiles.bin"), "rb").read()
    hi = -1
    for i in range(len(raw) // 2):
        e = struct.unpack_from("<H", raw, i * 2)[0]
        t = e & 0x3FF
        if t >= 512:
            hi = max(hi, t - 512)
    return hi + 1


TILE_BASE = base_tile_count()
# Rustboro City's own art (Devon Corp., gym, school, city houses ...) is used by no other layout of the pair, and
# never by a Sevii map. The Sevii copy keeps those metatile ids (blanked) and frees their tiles for new art:
# FREE_TILES = tiles referenced only by metatiles that appear in no General + Rustboro layout except
# LAYOUT_RUSTBORO_CITY, plus the unused tail after TILE_BASE.
CITY_ONLY_LAYOUTS = ("LAYOUT_RUSTBORO_CITY",)


def _free_tiles():
    import voyage_compose as vc
    sc = vc.vanilla.Scene(PRIMARY, BASE)
    keep_meta = set()
    for lid in vc.pair_layouts((PRIMARY, BASE)):
        if lid.replace("@git", "") in CITY_ONLY_LAYOUTS:
            continue
        try:
            g = vc.raw_layout(lid)[1]
        except Exception:
            continue
        keep_meta.update(v & 0x3FF for row in g for v in row if v & 0x3FF >= 0x200)
    used, kept = set(), set()
    for i, ents in enumerate(sc.s.metatiles):
        ts_ = {e & 0x3FF for e in ents if e & 0x3FF >= 512}
        used |= ts_
        if 0x200 + i in keep_meta:
            kept |= ts_
    dropped_meta = [0x200 + i for i in range(len(sc.s.metatiles)) if 0x200 + i not in keep_meta]
    free = sorted(t - 512 for t in used - kept) + list(range(TILE_BASE, 512))
    return free, dropped_meta


FREE_TILES, DROPPED_METATILES = None, None


def _ensure_free():
    global FREE_TILES, DROPPED_METATILES
    if FREE_TILES is None:
        FREE_TILES, DROPPED_METATILES = _free_tiles()


def extras():
    return dict(base=BASE, tiles=_TILES, palettes=_PALS, metatiles=_META)


def _scene_if_built():
    import voyage_compose as vc
    return vc._SCENES.get((PRIMARY, "gTileset_SeviiIslands"))


def add_tiles(tiles):
    """Store new 8x8 tiles (8 rows of 8 colour indices 0-15) in free tile slots; -> their tile numbers for
    metatile entries (512 + secondary index). Identical tiles are stored once."""
    _ensure_free()
    out = []
    for t in tiles:
        t = [list(r) for r in t]
        for k, v in _TILES.items():
            if v == t:
                out.append(512 + k)
                break
        else:
            free = [i for i in FREE_TILES if i not in _TILES]
            assert free, "gTileset_SeviiIslands is out of tiles"
            _TILES[free[0]] = t
            out.append(512 + free[0])
    sc = _scene_if_built()
    if sc is not None:
        sc.s.n = max(sc.s.n, max(_TILES) + 1)
    return out


def add_metatile(label, entries, behaviour="MB_NORMAL", layer=0, coll=0, elev=0):
    """New secondary metatile. entries = 8 tile entries (tile | hflip << 10 | vflip << 11 | pal << 12),
    bottom layer first. layer: 0 normal, 1 covered, 2 split. -> raw block value."""
    if label in LABELS:
        return RAW[label]
    attr = MB.index(behaviour) | (layer << 12)
    _META.append((label, tuple(entries), attr))
    mid = 0x200 + BASE_METATILES + len(_META) - 1
    LABELS[label] = mid
    RAW[label] = mid | (coll << 10) | (elev << 12)
    sc = _scene_if_built()
    if sc is not None:                      # scene already drawn once: keep it in step
        sc.s.metatiles.append(tuple(entries))
        sc.s.attrs.append(attr)
    return RAW[label]


ARROWS = {"N": "MB_NORTH_ARROW_WARP", "S": "MB_SOUTH_ARROW_WARP", "E": "MB_EAST_ARROW_WARP",
          "W": "MB_WEST_ARROW_WARP"}


def arrow(base_raw, direction):
    """Arrow-warp duplicate of the metatile in base_raw (any General / Rustboro id): same art and layer,
    behaviour MB_<dir>_ARROW_WARP, walkable. -> raw block value."""
    import voyage_compose as vc
    mid = base_raw & 0x3FF
    label = "arrow_%s_%03X" % (direction, mid)
    if label in LABELS:
        return RAW[label]
    sc = vc.scene((PRIMARY, BASE))
    ts, i = (sc.p, mid) if mid < 0x200 else (sc.s, mid - 0x200)
    entries, layer = ts.metatiles[i], (ts.attrs[i] >> 12) & 3
    return add_metatile(label, entries, ARROWS[direction], layer, coll=0, elev=(base_raw >> 12) & 0xF)


def budget():
    """Secondary budget after the additions (engine: 512 tiles, 512 metatiles; palettes 6-12 secondary)."""
    _ensure_free()
    return dict(base_tiles=TILE_BASE, freed_city_tiles=len(FREE_TILES) - (512 - TILE_BASE),
                dropped_city_metatiles=len(DROPPED_METATILES), new_tiles=len(_TILES),
                tiles_left=len(FREE_TILES) - len(_TILES),
                base_metatiles=BASE_METATILES, new_metatiles=len(_META),
                metatiles_left=512 - BASE_METATILES - len(_META),
                palettes_changed=sorted(_PALS), metatiles=[m[0] for m in _META])


# ============================================================================================ art additions
# (filled in by the art section: cottage variants, market stall, Onix tails, Rocket Warehouse)
# The art lives in sevii_art_pieces.py (helpers: sevii_art_kit.py; review sheets: sevii_art_sheets.py).
# register() appends tiles / metatiles / palettes / STAMPS here in a fixed order, so ids are deterministic.
import sevii_art_pieces as _art      # noqa: E402

# Batch 3b: more room for the FRLG landmark ports -- see sevii_art_pieces.free_policy(): only the metatiles of the
# layouts the Sevii specs / translator draw from (Route 104, Southern Island exterior, Faraway Island entrance) are
# kept; tiles referenced by no kept metatile (incl. the ~220 blank / unreferenced Rustboro slots) are free, except the
# Rustboro tile-animation destinations. check_kept() asserts the cells the Sevii specs name keep all their art.
import sys as _sys                   # noqa: E402
_art.free_policy(_sys.modules[__name__])
_art.register(_sys.modules[__name__])
PORTED = _art.PORTED                 # {("General_Frlg", FRLG metatile id): raw} -- substitute every such cell
PORTED_CELLS = _art.PORTED_CELLS     # {(FRLG map name, x, y): raw} -- whole ported formations, cell by cell
