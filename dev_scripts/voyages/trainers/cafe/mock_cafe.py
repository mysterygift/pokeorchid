"""
Batch 7: Changu City café (Cynthia's post-game rematch spot; placeholder for a future Battle Lounge).
Design-review mockup only: nothing under data/ src/ include/ graphics/ is written.

  exterior: LAYOUT_CHANGU_CITY (44x38, General + TosaPort) patched in the free grass south-east of House 2
  interior: new 12x10 room on Building + OrchidCentre (the Orchid Pokemon Centre's café kit)

usage: <venv python> dev_scripts/voyages/cafe/mock_cafe.py
Writes dev_scripts/voyages/out/batch7_cafe/*.png (1x + @2x, labelled marks).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import voyage_compose as vc   # noqa: E402
import sprites as sp          # noqa: E402
from PIL import Image         # noqa: E402

OUT = os.path.join(HERE, "..", "out", "batch7_cafe")
TP = ("gTileset_General", "gTileset_TosaPort")
OC = ("gTileset_Building", "gTileset_OrchidCentre")
CHANGU = "LAYOUT_CHANGU_CITY"


def I(mid, *ce):
    return ("id", mid) + ce


def N(x, y, label, who, facing="down"):
    return (x, y, label, "npc", sp.key(who, facing))


# ------------------------------------------------------------------ exterior
# Existing events of MAP_CHANGU_CITY (data/maps/ChanguCity/map.json), drawn on both before and after.
EXISTING = [
    N(23, 13, "", "man_3"), N(39, 18, "", "tourist_f"), N(7, 15, "", "woman_4"), N(30, 16, "", "lass"),
    N(25, 7, "", "man_4"),
    (33, 13, "", "sign"),                                     # OBJ_EVENT_GFX_MART_SIGN object
    (22, 6, "Stn", "warp"), (23, 6, "", "warp"), (14, 21, "PC", "warp"), (30, 13, "Mart", "warp"),
    (31, 13, "", "warp"), (15, 13, "Gym", "warp"), (5, 21, "H1", "warp"), (26, 29, "H2", "warp"),
    (19, 21, "H3", "warp"), (25, 11, "H4", "warp"),
    (21, 34, "", "sign"), (15, 21, "", "sign"), (16, 21, "", "sign"), (32, 13, "", "sign"),
    (11, 13, "", "sign"), (5, 13, "", "sign"),
]

# Free today: x30-39, y25-29 (grass 001), between House 2 (x25-28) + its flower strip (x29) and the trees
# at x40-41. The road y30-31 runs x24-35 (east end 20A/21A at x35).
CAFE_X, CAFE_Y = 31, 26          # 4x4 building, door in its column 1 -> (32, 29)
TERRACE_X, TERRACE_Y = 35, 25    # Bura City market stall (4x5): orange awning, posts, pots, flower boxes
ROAD_END = 38                    # road y30-31 extended from x35 to x38 so the terrace sits on it


def exterior_spec(house="red"):
    """house='red': Changu House 3's red-roof General house (pstamp of primary metatiles 0x008-0x022).
    house='purple': House 2's purple TosaPort house (the alternative)."""
    src = (18, 18) if house == "red" else (25, 26)
    return dict(
        name="Changu City (café patch)", size=(44, 38), tileset=TP, base=CHANGU,
        stamps=[(CHANGU, src[0], src[1], 4, 4, CAFE_X, CAFE_Y),
                ("LAYOUT_BURA_CITY", 4, 7, 4, 5, TERRACE_X, TERRACE_Y)],
        cells=[(x, 30, (CHANGU, 30, 30)) for x in range(35, ROAD_END)]          # road top edge 209
        + [(x, 31, (CHANGU, 30, 31)) for x in range(35, ROAD_END)]             # road bottom edge 219
        + [(ROAD_END, 30, (CHANGU, 35, 30)), (ROAD_END, 31, (CHANGU, 35, 31)),   # east end 20A / 21A
           (30, 29, ("LAYOUT_BURA_CITY", 9, 11))],                              # café sign post (0x003)
        marks=EXISTING + [
            (32, 29, "CAFE", "warp"),
            (30, 29, "sign", "sign"),
            N(36, 28, "patron", "executive", "down"),
        ],
    )


# ------------------------------------------------------------------ interior
# Every cell is an existing metatile of LAYOUT_POKEMON_CENTER_1F (Building + OrchidCentre). Columns x8-11
# are the Centre's café corner (Centre x10-13) with the tablet PC (21D / trim 213) taken out.
INT_LEGEND = {
    "w": I(0x201), "1": I(0x202), "2": I(0x203), "p": I(0x205), "q": I(0x206), "m": I(0x207),
    "s": I(0x208), "t": I(0x209),
    "F": I(0x20A), "a": I(0x20B), "b": I(0x20C), "_": I(0x20E), "P": I(0x211), "Q": I(0x212),
    "S": I(0x214), "T": I(0x215),
    "f": I(0x216), "-": I(0x217), "E": I(0x21E), "U": I(0x21F),
    "g": I(0x220), ".": I(0x221), "<": I(0x222), "A": I(0x229), "B": I(0x22A), "C": I(0x22B),
    ",": I(0x22C), "/": I(0x22D), "o": I(0x22E),
    "x": I(0x243), "D": I(0x244), "~": I(0x234),
    "M": I(0x248), "N": I(0x249), "k": I(0x247), "K": I(0x24A),
}
INT_ROWS = [
    # 0         1
    # 012345678901
    "w12wpq12wmst",    # 0  two windows round the flower painting, menu board + cup shelf
    "Fab_PQab__ST",    # 1  wall trim (fern top at x0)
    "f--------E-U",    # 2  fern / wall foot / counter return 21E, urn 21F
    "g........ABC",    # 3  café counter 229 22A 22B
    ".........o,o",    # 4  counter stools
    ".xDx.xDx.~.~",    # 5  two tables (3 wide: stool, table, stool)
    ".~~~.~~~....",    # 6  table shadows
    "........xDx.",    # 7  Cynthia's table
    "kxDx....~~~k",    # 8  third table, ferns (as the Centre's corner fern 247/24A)
    "K~~~.MN....K",    # 9  exit mat
]


# Café-only copy of the interior secondary with recoloured floor/walls (see changu_cafe_tileset.py).
import types                                  # noqa: E402
import changu_cafe_tileset as cct             # noqa: E402
CAFE_TS = {"A": "gTileset_ChanguCafe", "B": "gTileset_ChanguCafeB"}
for _v, _name in CAFE_TS.items():
    vc.VIRTUAL_MODULES[_name] = "changu_cafe_tileset"
    vc._VIRTUAL[_name] = types.SimpleNamespace(extras=lambda _v=_v: cct.extras(_v))


def cafe_pair(variant):
    """(Building, gTileset_ChanguCafe[B]) with the wall entries repointed to pal 11. -> (pair, changed ids)."""
    ts = ("gTileset_Building", CAFE_TS[variant])
    return ts, cct.patch(vc.scene(ts))


def interior_spec(tileset=OC):
    rows = INT_ROWS
    assert all(len(r) == 12 for r in rows), [len(r) for r in rows]
    cyn = sp.silhouette("woman_5", "left")
    return dict(
        name="Changu City café", size=(12, 10), tileset=tileset, ground=I(0x221), rows=rows, legend=INT_LEGEND,
        marks=[
            N(10, 2, "barista", "clerk", "down"),
            N(1, 5, "biz", "executive", "right"), N(3, 5, "biz", "woman_5", "left"),
            N(1, 8, "tourist", "gentleman", "right"),
            (10, 7, "Cyn", "legendary", cyn),
            (5, 9, "exit", "warp"), (6, 9, "", "warp"),
        ],
    )


def crop(path_in, path_out, box, scale):
    im = Image.open(path_in).crop(box)
    im.resize((im.width * scale, im.height * scale), Image.NEAREST).save(path_out)


def main():
    os.makedirs(OUT, exist_ok=True)
    vc.render_layout(CHANGU, os.path.join(OUT, "changu_before"), EXISTING)
    for house in ("red", "purple"):
        spec = exterior_spec(house)
        g = vc.render(spec, os.path.join(OUT, "changu_after" + ("" if house == "red" else "_purple")))
        bad = vc.seams(g, TP, ignore={0x001})
        print("exterior %-6s seams: %s" % (house, [s for s in bad if 28 <= s[0] <= 40 and 23 <= s[1] <= 32]))
    # GBA-camera crops (240x160 = 15x10 tiles) around the café, before/after, @2x
    box = (25 * 32, 22 * 32, 40 * 32, 32 * 32)
    for nm in ("changu_before", "changu_after", "changu_after_purple"):
        crop(os.path.join(OUT, nm + "@2x.png"), os.path.join(OUT, nm + "_gba@2x.png"), box, 1)

    spec = interior_spec()
    vc.check_size(*spec["size"])
    g = vc.render(spec, os.path.join(OUT, "cafe_int"))
    print("interior seams:", vc.seams(g, OC, ignore={0x221}))
    print("interior metatiles:", " ".join("%03X" % m for m in vc.metatile_ids(g)))
    crop(os.path.join(OUT, "cafe_int.png"), os.path.join(OUT, "cafe_int@4x.png"), (0, 0, 192, 160), 4)

    # recoloured café tileset: variants A (charcoal floor, deep-red walls) and B (charcoal, red accents)
    for v in ("A", "B"):
        ts, changed = cafe_pair(v)
        print("variant %s: wall metatiles repointed to pal %d: %s" % (v, cct.WALL_SLOT,
                                                                     " ".join("%03X" % m for m in changed)))
        vc.render(interior_spec(ts), os.path.join(OUT, "cafe_int_%s" % v))
        pd = os.path.join(OUT, "gTileset_ChanguCafe_%s_palettes" % v)
        os.makedirs(pd, exist_ok=True)
        for slot, cols in cct.extras(v)["palettes"].items():
            open(os.path.join(pd, "%02d.pal" % slot), "w", newline="").write(cct.jasc(cols))
    # before / after side by side @2x
    ims = [Image.open(os.path.join(OUT, n + "@2x.png")) for n in ("cafe_int", "cafe_int_A", "cafe_int_B")]
    sheet = Image.new("RGB", (sum(i.width for i in ims) + 32, ims[0].height), (255, 255, 255))
    x = 0
    for i in ims:
        sheet.paste(i, (x, 0))
        x += i.width + 16
    sheet.save(os.path.join(OUT, "cafe_int_recolour_compare@2x.png"))


if __name__ == "__main__":
    main()
