"""Rebuild ONLY gTileset_OrchidCentre and the two Centre 1F layouts from centre_interior.py.

Unlike integrate_interior.py --write this does not touch map events, scripts, the Mart or the
tileset wiring, so hand edits to the Centre maps (NPC positions, scripts) are kept.

    python rebuild_centre.py            # dry run: compare against the files in the repo
    python rebuild_centre.py --write
"""
import os
import sys
import tempfile
import filecmp

import centre_interior
import integrate_interior as ii


def build():
    c_main, c_lava = centre_interior.build(), centre_interior.build(back_door=True)
    cp = c_main["palettes"]
    ts = ii.Tileset("orchid_centre", [cp[k] for k in ("centre_floor", "centre_wall", "centre_furniture",
                                                       "centre_decor", "vanilla_pokemon_center")])
    rows = ts.paint(c_main["base"], c_main["top"], ii.CW, ii.CH, ii.centre_info(False))
    lrows = ts.paint(c_lava["base"], c_lava["top"], ii.CW, ii.CH, ii.centre_info(True))
    return ts, rows, lrows


def main(write):
    ts, rows, lrows = build()
    print(f"OrchidCentre: {len(ts.bank.tiles)} tiles, {len(ts.meta)} metatiles")
    real_dir, real_root = ts.dir, ii.ROOT
    if not write:
        tmp = tempfile.mkdtemp()
        ts.dir = os.path.join(tmp, "ts")
        ii.ROOT = tmp
        os.makedirs(os.path.join(tmp, "data", "layouts", "PokemonCenter_1F"))
        os.makedirs(os.path.join(tmp, "data", "layouts", "LavaridgeTown_PokemonCenter_1F"))
    ts.save()
    ii.save_layout("PokemonCenter_1F", rows, ts.void)
    ii.save_layout("LavaridgeTown_PokemonCenter_1F", lrows, ts.void)
    if not write:
        pairs = [(os.path.join(ts.dir, f), os.path.join(real_dir, f))
                 for f in ("tiles.png", "metatiles.bin", "metatile_attributes.bin")]
        pairs += [(os.path.join(tmp, "data", "layouts", d, f), os.path.join(real_root, "data", "layouts", d, f))
                  for d in ("PokemonCenter_1F", "LavaridgeTown_PokemonCenter_1F") for f in ("map.bin", "border.bin")]
        for a, b in pairs:
            print(("same    " if filecmp.cmp(a, b, shallow=False) else "DIFFERS ") + os.path.relpath(b, real_root))
        print("dry run; pass --write to apply")
    else:
        print("written")


if __name__ == "__main__":
    main("--write" in sys.argv)
