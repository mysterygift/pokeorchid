"""
PROPOSED (not applied) additions to gTileset_TosaPort for the Wavebreak beach, batch 1:
  * Mr. Briney's wooden dock (Route 104, gTileset_Rustboro metatiles 0x33D 0x26E 0x32E / 0x345 0x26D 0x336 /
    0x335 0x276 0x277): 9 metatiles copied as they are, 5 Rustboro secondary tiles; every entry uses palettes
    0-5, which come from gTileset_General, so the colours are identical in TosaPort (no palette work).
  * crates on sand: TosaPort's own crate tiles (as in 0x32E / 0x336) over sand (General 0x124's tiles) instead
    of the market cobble: 2 metatiles, 0 new tiles.
  * crate of fish: the crate with an open top holding two silver fish: 1 metatile, 2 new tiles (palette 7).
  * fishing-rod pair stuck upright in the sand, 1x2: 2 metatiles, 4 new tiles (palette 7, right half = hflip).
  * bucket (pail) on sand, 3/4 view: 1 metatile, 4 new tiles (palette 12 for the blue water; light from the
    upper left, so not mirrored).
Nothing here writes to data/; mockups draw these with render(). Numbers for NOTES.md: plan().

Palette 7 of TosaPort (the crate palette) is used for all new art: 3 (200,200,216) / 4 (144,136,160) /
5 (64,72,104) silver-grey fish and outline, 6 (248,248,216) highlight / float white, 7 (216,200,144) and
9 (136,112,72) wood, 8 (168,160,104) sand shadow, 10 (232,56,32) float red.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import voyage_compose as vc   # noqa: E402
from PIL import Image, ImageDraw   # noqa: E402

TP = ("gTileset_General", "gTileset_TosaPort")
RB = ("gTileset_General", "gTileset_Rustboro")
DOCK_IDS = [0x33D, 0x26E, 0x32E, 0x345, 0x26D, 0x336, 0x335, 0x276, 0x277]
# Route 104 x11-14 y51-53: sea end / plank / plank / land end; rows: top planks, middle planks, front face
DOCK_ROWS = [[0x33D, 0x26E, 0x26E, 0x32E], [0x345, 0x26D, 0x26D, 0x336], [0x335, 0x276, 0x276, 0x277]]


def _fish_crate_top():
    """16x8 open crate top with two fish (left half / right half become two tiles)."""
    g = [[0] * 16 for _ in range(8)]
    g[0] = [0] + [5] * 13 + [0, 0]
    for y in range(1, 7):
        g[y] = [5] + [9] * 13 + [5, 0 if y < 5 else 4]
    g[7] = [5] + [7] * 13 + [5, 4]
    for y, x in ((2, 3), (3, 9), (5, 4), (6, 11), (2, 12)):   # a little ice / scale glint in the box
        g[y][x] = 8
    fish = [[None, 4, 3, 3, 3, 3, None, 4],
            [4, 5, 6, 6, 3, 3, 4, 4],
            [None, 4, 4, 4, 4, 4, None, 4]]
    for j, row in enumerate(fish):                          # fish A, head left
        for i, c in enumerate(row):
            if c is not None:
                g[2 + j][2 + i] = c
    for j, row in enumerate(fish):                          # fish B, head right (mirrored)
        for i, c in enumerate(reversed(row)):
            if c is not None:
                g[4 + j][5 + i] = c
    return g


def _rods_left():
    """8x32 left half of the 1x2 rod pair (the right half is its mirror)."""
    g = [[0] * 8 for _ in range(32)]
    for x in range(2, 7):
        g[31][x] = 8                                        # dug-in sand shadow
    for x in range(3, 6):
        g[30][x] = 8
    for y in range(8, 31):
        g[y][4] = 9                                         # rod
        if y >= 10:
            g[y][5] = 5                                     # its shaded side
    g[6][3] = g[7][3] = 9                                   # bent tip
    for y in range(7, 12):
        g[y][2] = 3                                         # line
    g[12][2] = 10                                           # float: red top, white belly, dark tip
    for x in (1, 2, 3):
        g[13][x] = 10
        g[14][x] = 6
    g[15][2] = 5
    g[22][5] = g[22][6] = 4                                 # reel
    g[23][5] = 4
    g[23][6] = 5
    return g


BUCKET = [   # 16x16, palette 7 indices ('.' = transparent), drawn after TosaPort's market pots 0x20C / 0x21B:
    # oval rim seen from above (rows 2-7, ~40%) with teal water (back edge in shadow) and a fish tail inside,
    # lit lip on the left / front, body narrowing to the base, right side darker, handle lying back behind
    # the rim (rows 0-1), soft shadow on the sand below and to the right
    "....55555555....",
    "...5........5...",
    "...5555555555...",
    "..566666333345..",
    ".56FFFFFFFFFF45.",
    ".56EEEEE34EEE45.",
    ".56EEEEEE3EEE45.",
    "..566666333345..",
    "..563333333445..",
    "..563333333445..",
    "..544444444445..",
    "...5633333445.4.",
    "...5633333445.4.",
    "....55555555.4..",
    ".....44444444...",
    "................",
]


# The art above is written in palette-7 indices; palette 7 has no blue, so the bucket is stored in TosaPort
# palette 12 (existing; greys + blues): outline 5->1 (64,72,104), light 3->8 (184,192,208), mid 4->7
# (136,144,168), lip highlight 6->10 (248,248,248), water E->4 (104,160,208), water in shadow F->3 (64,112,160)
BUCKET_PAL = 12
_TO_PAL12 = {3: 8, 4: 7, 5: 1, 6: 10, 0xE: 4, 0xF: 3}


def _bucket():
    g = []
    for row in BUCKET:
        row = row.replace(" ", ".")[:16].ljust(16, ".")
        g.append([0 if c == "." else _TO_PAL12[int(c, 16)] for c in row])
    return g


def _bucket_left():
    """8x16 left half of a pail seen in 3/4 view (right half = mirror): handle arc, rim ellipse from
    above with water inside, metal body with a band, sand shadow."""
    g = [[0] * 8 for _ in range(16)]
    for x in range(4, 8):
        g[0][x] = 5                                         # handle arc
    g[1][3] = 5
    g[2][2] = 5
    for x in range(3, 8):
        g[3][x] = 5                                         # back of the rim
    g[4][2] = 5
    g[4][3] = 4
    for y in (4, 5, 6):
        for x in range(3 if y == 4 else 3, 8):
            g[y][x] = 3                                     # water surface
    g[5][1] = g[6][1] = 5
    g[5][2] = g[6][2] = 4
    g[5][6] = 6                                             # glint on the water
    g[7][1] = 5
    for x in range(2, 8):
        g[7][x] = 6                                         # lit front lip of the rim
    for y in range(8, 14):
        g[y][1] = 5
        g[y][2] = 4
        for x in range(3, 8):
            g[y][x] = 3
    for x in range(2, 8):
        g[10][x] = 4                                        # band
        g[14][x] = 5                                        # base
        g[15][x] = 8                                        # shadow on the sand
    g[14][1] = 5
    return g


def _split(g, w8, h8):
    return [[[row[x * 8:(x + 1) * 8] for row in g[y * 8:(y + 1) * 8]] for x in range(w8)] for y in range(h8)]


_ft = _split(_fish_crate_top(), 2, 1)
_rt = _split(_rods_left(), 1, 4)
_bt = _split(_bucket(), 2, 2)
NEW_TILES = {"fish_l": _ft[0][0], "fish_r": _ft[0][1],
             "rod_a": _rt[0][0], "rod_b": _rt[1][0], "rod_c": _rt[2][0], "rod_d": _rt[3][0],
             "bucket_a": _bt[0][0], "bucket_b": _bt[0][1], "bucket_c": _bt[1][0], "bucket_d": _bt[1][1]}
_ot = _split(_bucket_left(), 1, 2)     # first, side-on bucket (rejected), kept for the comparison only
OLD_TILES = {"oldbucket_a": _ot[0][0], "oldbucket_b": _ot[1][0]}

_tp = vc.scene(TP)
SAND = list(_tp.p.metatiles[0x124][:4])         # General sand, bottom layer


def E(tile, pal, h=0, v=0):
    return (tile, pal, h, v)


# name -> (8 entries: 4 bottom + 4 top; tile = int (vanilla index in TosaPort's own numbering) or str (new),
#          layer: 1 = covered (both layers under sprites), 0 = normal (top layer over sprites), collision)
def _crate(top_pair, front_pair):
    return [E(t & 0x3FF, t >> 12) for t in SAND] + [E(top_pair[0], 7), E(top_pair[1], 7),
                                                     E(front_pair[0], 7), E(front_pair[1], 7)]


PROPOSED = {
    "crate_sand": (_crate((0x28A, 0x28B), (0x29A, 0x29B)), 1, 1),
    "crates_stacked_sand": (_crate((0x29A, 0x29B), (0x29A, 0x29B)), 1, 1),
    "fish_crate_sand": (_crate(("fish_l", "fish_r"), (0x29A, 0x29B)), 1, 1),
    "rods_top": ([E(t & 0x3FF, t >> 12) for t in SAND] + [E("rod_a", 7), E("rod_a", 7, 1), E("rod_b", 7),
                                                         E("rod_b", 7, 1)], 0, 0),
    "bucket_sand": ([E(t & 0x3FF, t >> 12) for t in SAND] + [E("bucket_a", BUCKET_PAL), E("bucket_b", BUCKET_PAL),
                                                           E("bucket_c", BUCKET_PAL), E("bucket_d", BUCKET_PAL)],
                    1, 1),
    "rods_base": ([E(t & 0x3FF, t >> 12) for t in SAND] + [E("rod_c", 7), E("rod_c", 7, 1), E("rod_d", 7),
                                                          E("rod_d", 7, 1)], 1, 1),
}


OLD = {"bucket_old_sand": ([E(t & 0x3FF, t >> 12) for t in SAND] + [
    E("oldbucket_a", 7), E("oldbucket_a", 7, 1), E("oldbucket_b", 7), E("oldbucket_b", 7, 1)], 1, 1)}


def render(name):
    """-> (under, over) 16x16 RGBA of a proposed metatile, or of a dock metatile ('dock_33D' etc.)."""
    if name.startswith("dock_"):
        return vc.scene(RB).metatile(int(name[5:], 16))
    entries, layer, _ = PROPOSED[name] if name in PROPOSED else OLD[name]
    under = Image.new("RGBA", (16, 16), (0, 0, 0, 255))
    over = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for k, (t, pal, hf, vf) in enumerate(entries):
        if isinstance(t, str):
            tile = NEW_TILES[t] if t in NEW_TILES else OLD_TILES[t]
        else:
            ts, i = (_tp.p, t) if t < 512 else (_tp.s, t - 512)
            tile = ts.tile(i)
        q, top = k & 3, k >= 4
        dst = (over if (top and layer == 0) else under).load()
        for y in range(8):
            for x in range(8):
                ci = tile[7 - y if vf else y][7 - x if hf else x]
                if ci == 0 and top:
                    continue
                dst[(q & 1) * 8 + x, (q >> 1) * 8 + y] = _tp.pals[pal][ci] + (255,)
    return under, over


def plan():
    """Counts for NOTES.md."""
    rb = vc.scene(RB)
    dock_tiles = sorted({e & 0x3FF for m in DOCK_IDS for e in rb.s.metatiles[m - 0x200] if e & 0x3FF >= 512})
    ref = {e & 0x3FF for m in _tp.s.metatiles for e in m if e & 0x3FF >= 512}
    free_tiles = [t for t in range(_tp.s.n) if t + 512 not in ref and t != 0]
    used = vc.uses(TP)
    free_mt = [i + 0x200 for i, m in enumerate(_tp.s.metatiles)
               if all((e & 0x3FF) == 0 for e in m) and i + 0x200 not in used]
    return dict(dock_metatiles=len(DOCK_IDS), dock_tiles=dock_tiles, new_tiles=len(NEW_TILES),
                new_metatiles=len(PROPOSED), tiles_total=_tp.s.n, free_tiles=free_tiles,
                metatiles_total=len(_tp.s.metatiles), free_metatiles=free_mt)


def closeup(path, scale=4):
    """Vanilla crates beside the proposed props and the dock, labelled, at `scale`."""
    sand_u, _ = _tp.metatile(0x124)
    items = [("0x32E vanilla", [[_tp.metatile(0x32E)]]), ("0x336 vanilla", [[_tp.metatile(0x336)]]),
             ("crate on sand", [[render("crate_sand")]]), ("stack on sand", [[render("crates_stacked_sand")]]),
             ("fish crate", [[render("fish_crate_sand")]]),
             ("fish over stack", [[render("fish_crate_sand")], [render("crates_stacked_sand")]]),
             ("rods 1x2", [[render("rods_top")], [render("rods_base")]]),
             ("bucket (pal 12)", [[render("bucket_sand")]]),
             ("0x21B pot", [[_tp.metatile(0x21B)]]),
             ("Briney dock", [[render("dock_%03X" % m) for m in row] for row in DOCK_ROWS])]
    T = 16 * scale
    W = sum(max(max(len(r) for r in cells) * T, 7 * len(label)) + 20 for label, cells in items) + 20
    H = 3 * T + 60
    im = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(im)
    x = 20
    for label, cells in items:
        for j, row in enumerate(cells):
            for i, (u, o) in enumerate(row):
                c = Image.new("RGBA", (16, 16))
                c.paste(sand_u, (0, 0))
                c.alpha_composite(u)
                c.alpha_composite(o)
                im.paste(c.resize((T, T), Image.NEAREST), (x + i * T, 40 + j * T))
        d.text((x, 10), label, fill=(0, 0, 0))
        x += max(max(len(r) for r in cells) * T, 7 * len(label)) + 20
    im.save(path)


if __name__ == "__main__":
    print(plan())
    closeup(os.path.join(HERE, "out", "batch1", "tosaport_addition_closeup_4x.png"))
