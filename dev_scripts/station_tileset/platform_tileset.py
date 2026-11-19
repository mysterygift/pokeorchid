#!/usr/bin/env python3
"""
gTileset_UrbanPlatform: Tosa Rail platforms with the wall colour-coded by line (user: "important for
player navigation"). Same art as gTileset_UrbanInterior (export_tileset.py) and the same metatile ids
for everything the Tosa Port platform already uses, so a platform layout switches tileset unchanged:

    0x200        Void
    0x201-0x20A  shell, CENTRAL teal (pal 6)  = UrbanInterior's "tosa" shell
    0x20B-0x20F  track, platform edge, paving A/B, exit mat (pals 7, 8)
    0x210-0x219  shell, WEST purple (pal 9)   (UrbanInterior has the unused Telok brick here)
    0x21A-0x223  shell, EAST green (pal 11)
    0x224-0x22D  shell, POKETOPIA orange (pal 12)
    0x280-0x2AD  Pokemon Center escalators (pal 10), same ids so fldeff_escalator.c animates them

Shell order inside each block: Ceiling_Beam, Ceiling, Canopy_Beam, Canopy, Wall, Wall_Poster,
WallBase, Pillar_Canopy, Pillar_Wall, Pillar_Base (shell_id(line, i) below).
Concourses stay on gTileset_UrbanInterior (its slots 11-12 hold the concourse fixtures).

    python platform_tileset.py      # writes data/tilesets/secondary/urban_platform/
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import export_tileset as E  # noqa: E402

TS_DIR = os.path.join(E.ROOT, "data", "tilesets", "secondary", "urban_platform")

# line key -> (palette slot, theme name in E.THEMES, first shell metatile id)
LINES = {
    "central":   (6, "tosa", 0x201),
    "west":      (9, "west", 0x210),
    "east":      (11, "east", 0x21A),
    "poketopia": (12, "poketopia", 0x224),
}
SHELL = ["Ceiling_Beam", "Ceiling", "Canopy_Beam", "Canopy", "Wall", "Wall_Poster", "WallBase",
         "Pillar_Canopy", "Pillar_Wall", "Pillar_Base"]
CANOPY = (56, 64, 88)                                  # the neutral Tosa canopy for every line
E.THEMES.update(
    west=dict(wall=(136, 88, 176), wall_d=(96, 56, 136), wall_l=(184, 144, 216), canopy=CANOPY),
    east=dict(wall=(72, 152, 88), wall_d=(40, 104, 64), wall_l=(136, 200, 128), canopy=CANOPY),
    poketopia=dict(wall=(216, 120, 56), wall_d=(160, 80, 40), wall_l=(240, 176, 112), canopy=CANOPY),
)


def shell_id(line, name):
    return LINES[line][2] + SHELL.index(name)


def metatile_defs():
    t = {k: E.theme_colours(v[1]) for k, v in LINES.items()}
    draw = {
        "Ceiling_Beam": lambda t: E.draw_ceiling(t, True), "Ceiling": lambda t: E.draw_ceiling(t, False),
        "Canopy_Beam": lambda t: E.draw_canopy(t, True), "Canopy": lambda t: E.draw_canopy(t, False),
        "Wall": E.draw_wall, "Wall_Poster": E.draw_poster, "WallBase": E.draw_wall_base,
        "Pillar_Canopy": E.draw_pillar_canopy, "Pillar_Wall": E.draw_pillar_wall,
        "Pillar_Base": E.draw_pillar_base,
    }
    defs = [("Void", "central", E.draw_void, E.MB_NORMAL, E.LAYER_NORMAL)]
    for line in LINES:
        for name in SHELL:
            defs.append((name + "_" + line.capitalize(), line, lambda f=draw[name], c=t[line]: f(c),
                         E.MB_NORMAL, E.LAYER_COVERED))
        if line == "central":
            defs += [
                ("Track", "central", E.draw_track, E.MB_NORMAL, E.LAYER_COVERED),
                ("PlatformEdge", "central", E.draw_edge, E.MB_NORMAL, E.LAYER_NORMAL),
                ("Paving_A", "central", lambda: E.draw_paving(False), E.MB_NORMAL, E.LAYER_NORMAL),
                ("Paving_B", "central", lambda: E.draw_paving(True), E.MB_NORMAL, E.LAYER_NORMAL),
                ("ExitMat", "central", E.draw_exit_mat, E.MB_SOUTH_ARROW_WARP, E.LAYER_NORMAL),
            ]
    return defs


def main():
    E.TS_DIR = TS_DIR
    E.PALETTES.clear()
    E.PALETTES.update({6: E.shell_palette("tosa"), 7: E.PAL_TRACK, 8: E.PAL_PLATFORM,
                       9: E.shell_palette("west"), 11: E.shell_palette("east"),
                       12: E.shell_palette("poketopia")})
    E.THEME_PALS.update({k: (v[0], 7, 8) for k, v in LINES.items()})
    E.metatile_defs = metatile_defs
    E.add_concourse = lambda *a: None                   # concourse kit lives in UrbanInterior only
    bank, metatiles, attrs, labels = E.build()
    for line, (_, _, first) in LINES.items():           # the documented ids must hold
        assert labels.index("Wall_" + line.capitalize()) + E.SECONDARY_METATILE_BASE == shell_id(line, "Wall")
    assert labels.index("Track") + E.SECONDARY_METATILE_BASE == 0x20B
    E.write_tileset(bank, metatiles, attrs)
    print(f"urban_platform: {len(bank.tiles)} tiles / 512, {len(metatiles)} metatiles")
    return 0


if __name__ == "__main__":
    sys.exit(main())
