"""
Five Isle Meadow Rocket Warehouse interior: design-review mockup (Sailor's Voyages / Sevii batch 3).

FRLG's FiveIsland_RocketWarehouse (29x27, gTileset_BuildingFrlg + gTileset_SilphCo) re-drawn in the vanilla
New Mauville pair (gTileset_General + gTileset_BikeShop, i.e. LAYOUT_NEW_MAUVILLE_INSIDE, read from git:
the Hoenn layouts were deleted from the working tree). Every cell is a metatile that New Mauville / the
Mauville Bike Shop already use; the walls follow New Mauville's own grammar (top rim 1F / face 27 / shadow
row 2F, internal rim 37, side walls 70/72, T-junctions 89/8A, pillar 88/90/91/98/A0, corridors 8B/8C/93/94/
8D/8E/95/96) so it reads like a vanilla Emerald interior. Crates (C0-C3) are solved by vanilla neighbour
frequency. The exit mat is the Bike Shop's green mat (0x218/0x220, the only exit mat in this pair).

FRLG plan kept: three rooms on top (cage store / table room / Gideon's lab), the wall between them and the
crate hall with three openings, the lab -> computer room -> exit room chain on the right with the two
openings into the hall. FRLG's spin-tile maze has no Emerald counterpart in this pair (New Mauville has no
spin tiles): the hall is a plain crate maze here (see the open questions in the spec report).

Nothing under data/ src/ include/ graphics/ is touched.
usage: <venv python> dev_scripts/voyages/rocket_warehouse_interior.py [--seams]
"""
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import voyage_compose as vc        # noqa: E402
import frlg_translate as ft        # noqa: E402
from PIL import Image              # noqa: E402

OUT = os.path.join(HERE, "out", "batch3")
BASE = os.path.join(OUT, "five_island_rocket_warehouse")
PAIR = ("gTileset_General", "gTileset_BikeShop")
W, H = 30, 28

# Rocket gfx is invisible in this build -> Emerald grunts (Magma, see open questions); FRLG facing kept.
_PEOPLE = "graphics/object_events/pics/people/"
vc.SPRITES.update({
    "grunt_m_down": (_PEOPLE + "team_magma/magma_member_m.png", 16, 32, 0, False),
    "grunt_m_right": (_PEOPLE + "team_magma/magma_member_m.png", 16, 32, 2, True),
    "grunt_f_up": (_PEOPLE + "team_magma/magma_member_f.png", 16, 32, 1, False),
    "grunt_f_left": (_PEOPLE + "team_magma/magma_member_f.png", 16, 32, 2, False),
    "admin_m_left": (_PEOPLE + "team_magma/magma_member_m.png", 16, 32, 2, False),
    "scientist_left": (_PEOPLE + "scientist_1.png", 16, 32, 2, False),
})


# ------------------------------------------------------------------ FRLG reference (Silph Co metatiles)
def _silph_tileset():
    """gTileset_SilphCo has no tiles.png of its own: it borrows Condominiums' tiles + palettes (headers.h).
    Built here in memory so frlg_translate can draw the FRLG map without being edited."""
    t = object.__new__(ft.FTileset)
    gfx, meta = ft.tileset_dir("gTileset_Condominiums"), ft.tileset_dir("gTileset_SilphCo")
    t.sym = "gTileset_SilphCo"
    im = Image.open(os.path.join(gfx, "tiles.png"))
    t.w, t.px, t.n = im.width // 8, im.load(), (im.width // 8) * (im.height // 8)
    raw = open(os.path.join(meta, "metatiles.bin"), "rb").read()
    t.meta = [struct.unpack_from("<8H", raw, i * 16) for i in range(len(raw) // 16)]
    raw = open(os.path.join(meta, "metatile_attributes.bin"), "rb").read()
    t.attrs = list(struct.unpack("<%dI" % (len(raw) // 4), raw))
    t.pals = [ft._jasc(os.path.join(gfx, "palettes", "%02d.pal" % i)) for i in range(16)]
    return t


def frlg_map():
    if "gTileset_SilphCo" not in ft._TS:
        ft._TS["gTileset_SilphCo"] = _silph_tileset()
    return ft.load_map("FiveIsland_RocketWarehouse")


# ------------------------------------------------------------------ the grid
# One token per cell: 2 hex digits = metatile 0x2xx of gTileset_BikeShop (New Mauville), "cc" = crate
# (solved among C0-C3), "m1"/"m2" = Bike Shop exit mat halves (0x218 / 0x220).
# x:     0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29
GRID = """
        68 1F 1F 1F 1F 1F 99 9A 1F 1F 1F 99 9A 88 1F 1F 1F 1F 1F 6A 08 68 1F 1F 1F 1F 1F 1F 6A 08
        70 D6 D7 27 27 27 A1 A2 B2 B4 27 A1 A2 90 27 27 27 27 27 72 08 70 D6 D7 D4 D5 27 27 72 08
        70 DE DF 75 2F 2F A9 AA BA BC 2F A9 AA 90 75 2F 2F 2F 2F 72 08 70 DE DF DC DD 75 2F 72 08
        70 7D 10 10 cc cc 10 10 10 10 10 10 10 90 7D 10 10 10 10 72 08 70 7D C8 E4 E5 7D 10 72 08
        70 7D cc cc cc cc 10 cc cc 10 cc cc 10 90 7D 10 A3 A4 10 72 08 70 7D 10 7F 2F 7E 10 72 08
        70 7D cc cc 10 10 10 cc cc 10 cc cc 10 90 7D 10 AB AC 10 72 08 70 7D 10 10 10 10 10 72 08
        70 7D 10 10 10 10 10 10 10 10 10 10 10 90 7D 10 10 C8 10 72 08 70 7D 10 10 10 10 10 72 08
        70 7D 10 9E 37 37 37 9D 85 10 9E 37 37 91 87 9D 85 10 10 72 08 70 7D 10 9E 37 6F 37 8A 08
        70 7D 10 A6 27 27 27 A5 7D 10 A6 B3 B4 90 27 A5 7D 10 10 72 08 70 7D 10 A6 27 D6 D7 72 08
        70 7D 10 7F 2F 2F 2F 2F 7E 10 7F BB BC 98 75 2F 7E 10 10 72 08 70 7D 10 7F 2F EE DF 72 08
        70 7D 10 10 10 10 cc cc 10 10 10 10 10 A0 7D cc 10 10 10 72 08 70 7D 10 10 10 10 10 72 08
        70 7D 10 10 10 cc cc 10 10 10 10 10 10 7F 7E 10 10 10 10 72 08 70 7D 10 10 10 10 10 72 08
        70 7D 10 10 cc cc 10 10 10 10 10 10 10 10 10 10 10 10 10 72 08 89 79 37 9D 85 9E 37 8A 08
        70 7D 10 10 cc cc 10 10 10 10 10 10 cc cc 10 10 10 10 10 72 08 70 27 27 A5 7D A6 27 72 08
        70 7D 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 cc 10 72 08 70 75 2F 2F 7E 7F 2F 72 08
        70 7D 10 10 10 cc 10 10 10 10 cc cc 10 10 10 10 10 10 10 8C 1F 8B 7D 10 10 10 10 10 72 08
        70 7D 10 10 10 cc 10 cc 10 10 cc cc cc 10 10 10 10 cc 10 94 27 93 7D 10 10 10 10 10 72 08
        70 7D 10 10 10 cc 10 10 10 10 cc cc cc 10 10 10 10 cc 10 7F 2F 2F 7E 10 10 10 10 10 72 08
        70 7D 10 10 10 cc 10 10 10 10 10 10 cc 10 10 10 10 cc 10 8E 37 8D 85 10 10 10 10 10 72 08
        70 7D 10 10 10 cc 10 10 10 10 10 10 10 10 10 10 10 10 10 96 27 95 7D 10 10 10 10 10 72 08
        70 7D 10 10 10 cc 10 10 10 10 10 10 10 10 10 10 10 10 10 72 08 70 7D 10 cc cc 10 10 72 08
        70 7D 10 10 10 10 10 10 10 10 10 10 10 10 10 cc 10 10 10 8C 1F 8B 7D 10 cc cc 10 10 72 08
        70 7D 10 cc cc cc cc cc 10 10 10 10 10 10 10 10 10 10 10 94 27 93 7D 10 10 10 10 10 72 08
        70 7D 10 cc cc 10 10 10 10 10 10 10 10 10 10 cc 10 10 10 7F 2F 2F 7E 10 10 10 10 10 72 08
        70 cc 10 cc 10 10 cc cc cc cc cc cc cc cc cc cc 10 10 10 8E 37 8D 85 10 10 10 10 10 72 08
        70 cc cc 10 10 cc cc cc 10 10 10 10 10 10 10 10 10 10 cc 96 27 95 7D 10 10 10 10 10 72 08
        78 79 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 7A 08 70 7D 10 10 10 10 10 72 08
        80 27 27 27 27 27 27 27 27 27 27 27 27 27 27 27 27 27 27 82 08 70 7D 10 m1 m2 10 10 72 08
"""
CRATES = [0x2C0, 0x2C1, 0x2C2, 0x2C3]
MAT = {"m1": 0x218, "m2": 0x220}
LEGEND_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#$%&*+-=:;<>?@^~!"

# ------------------------------------------------------------------ events (FRLG coords -> this map)
# FRLG warp (24,25) -> MAP_FIVE_ISLAND_MEADOW warp 0 (Meadow door (12,21)); here both mat halves warp.
WARPS = [dict(x=24, y=27, dest_map="MAP_FIVE_ISLAND_MEADOW", dest_warp_id=0, frlg=(24, 25)),
         dict(x=25, y=27, dest_map="MAP_FIVE_ISLAND_MEADOW", dest_warp_id=0, frlg=(24, 25))]
OBJECTS = [  # (x, y, label, kind, sprite, FRLG source)
    (6, 6, "Grunt1", "npc", "grunt_f_up", "ROCKET_F (6,6) Grunt1"),
    (15, 11, "Grunt2", "npc", "grunt_m_down", "ROCKET_M (15,11) Grunt2"),
    (17, 15, "Grunt3", "npc", "grunt_m_right", "ROCKET_M (17,15) Grunt3"),
    (26, 11, "Admin2", "npc", "admin_m_left", "ROCKET_M (25,11) Admin2 (faced right); trigger (22-24,11) -> (25,11)"),
    (27, 16, "Admin1", "npc", "grunt_f_left", "ROCKET_F (27,16) Admin1"),
    (27, 4, "Gideon", "npc", "scientist_left", "SCIENTIST (27,4) Gideon = boss spot"),
    (4, 5, "UpGrade", "item", "item", "ITEM_BALL (4,5) Up-Grade"),
    (17, 4, "TM36", "item", "item", "ITEM_BALL (17,3) TM36, on the table (elevation 0) as in FRLG"),
    (1, 16, "Pearl", "item", "item", "ITEM_BALL (1,16) Pearl"),
    (8, 25, "BigPearl", "item", "item", "ITEM_BALL (8,25) Big Pearl"),
]
OTHER_MARKS = [
    (24, 27, "EXIT", "warp"), (25, 27, "EXIT", "warp"),
    (27, 2, "h:Nest", "note"), (7, 16, "h:Net", "note"),           # hidden items (FRLG same cells)
    (26, 8, "PC", "sign"), (27, 8, "PC", "sign"),                 # FRLG computer bg_event (26,11), facing east
    (4, 3, "cage", "sign"), (2, 4, "cage", "sign"), (7, 4, "cage", "sign"), (10, 4, "cage", "sign"),
    (6, 1, "cage", "sign"), (11, 1, "cage", "sign"),              # FRLG wall cages -> Mauville racks
    (25, 11, "trg", "note"),                                      # Admin2 trigger: the only way into room 2
    (1, 21, "spin maze -> plain crate hall", "note"),
    (23, 22, "spin tiles -> floor", "note"),
]


def parse():
    rows = [r.split() for r in GRID.strip("\n").splitlines()]
    assert len(rows) == H and all(len(r) == W for r in rows), [len(r) for r in rows]
    return rows


def spec():
    vc.check_size(W, H)
    rows = parse()
    legend, chars, auto = {}, {}, []
    for y, r in enumerate(rows):
        for x, t in enumerate(r):
            if t == "cc":
                auto.append((x, y, CRATES))
                t = "10"                                       # placeholder, solved below
            mid = MAT[t] if t in MAT else 0x200 + int(t, 16)
            if mid not in chars:
                chars[mid] = LEGEND_CHARS[len(chars)]
                legend[chars[mid]] = ("id", mid)
    marks = [m for m in OTHER_MARKS] + [(x, y, lab, kind, spr) for x, y, lab, kind, spr, _ in OBJECTS]
    return dict(size=(W, H), tileset=PAIR, ground=("id", 0x208),
                rows=["".join(chars[MAT[t] if t in MAT else 0x200 + int(t if t != "cc" else "10", 16)]
                              for t in r) for r in rows],
                legend=legend, auto=auto, marks=marks)


def report(g):
    shared_git = vc.pair_layouts(PAIR)
    return dict(
        pair=PAIR, size=(W, H), frlg=dict(map="FiveIsland_RocketWarehouse", layout="LAYOUT_FIVE_ISLAND_ROCKET_WAREHOUSE",
                                         size=(29, 27), pair=("gTileset_BuildingFrlg", "gTileset_SilphCo")),
        base_vanilla_layout="LAYOUT_NEW_MAUVILLE_INSIDE (git %s)" % vc.GIT_REF,
        secondary_users_working_tree=vc.sharing(PAIR[1]),
        secondary_users_vanilla=shared_git,
        warps=WARPS,
        objects=[dict(x=x, y=y, label=lab, gfx=spr, frlg=src) for x, y, lab, _k, spr, src in OBJECTS],
        hidden_items=[dict(x=27, y=2, item="ITEM_NEST_BALL"), dict(x=7, y=16, item="ITEM_NET_BALL")],
        metatiles=["0x%03X" % m for m in vc.metatile_ids(g)],
        seams=[(x, y, d, "0x%03X" % a, "0x%03X" % b) for x, y, d, a, b in vc.seams(g, PAIR)],
        open_questions=[
            "Spin-tile maze: New Mauville's pair has no spin tiles. Mockup = plain crate maze. Recommend keeping "
            "it plain (crates already force a route); alternative: Mauville's blue/green electric barriers "
            "(0x2B7/2BF/2C7/2CF, 0x2B6/2BE/2C6/2CE) with floor buttons 0x236/0x22E in the hall-to-exit-room "
            "corridors, scripted like NewMauville_Inside.",
            "Grunt gfx: Rocket sprites are invisible in this build; mockup uses Team Magma grunts. Recommend "
            "whichever team Orchid's Sevii story uses (or a new Orchid villain gfx later).",
            "Tileset: General+BikeShop is used by no working-tree map (New Mauville and the Bike Shop were deleted), "
            "so adding it back is risk-free; recommend reusing it as-is.",
            "Exit: Bike Shop green mat at the bottom of the exit room (2 warp cells) instead of New Mauville's "
            "wall door 0x276; recommend the mat (matches FRLG and the Meadow door).",
        ])


def main():
    sp = spec()
    g = vc.render(sp, BASE)
    fm = frlg_map()
    fm.report = dict(pair=PAIR)
    ft.side_by_side(fm, BASE)
    rep = report(g)
    keep = dict(sp)
    keep["report"] = rep
    json.dump(keep, open(BASE + "_spec.json", "w"), indent=0, default=str)
    s = rep["seams"]
    print("%s  %dx%d  metatiles=%d  seams=%d" % (BASE, W, H, len(rep["metatiles"]), len(s)))
    if "--seams" in sys.argv:
        for t in s:
            print("  seam", t)
    return g


if __name__ == "__main__":
    main()
