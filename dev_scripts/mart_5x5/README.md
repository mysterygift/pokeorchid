# 5x5 Poke Mart

Replaces the 4x5 v2 Mart (`../centre_mart_v2`), whose 16 px door straddled two metatiles, with a
5x5 Mart whose door sits inside the centre metatile.

| step | script | output |
|---|---|---|
| widen the art | `art.py` | `art/mart.png` (80x80, from `../centre_mart_v2/art/mart.png`) |
| install | `install.py [--write]` | General tiles/metatiles, ground variants, layouts, warps, signposts, sign events, door frames, label, `installed.json` |
| render check | `verify.py` | `out/verify.png` |
| in-game check | `ingame.py <harness rom> <outdir> all\|door` | exit/enter every Mart; Bura door frames |

Needs Pillow + numpy.

## Art
Each half grows 32 -> 40 px by repeating columns only where the art is periodic or flat: two more
glass stripes and a 2 px wider gutter on the roof, horizontal bands on the base, two more window
panes on the front. Corners, outlines, the centre tower and the door are untouched; the right-hand
window display keeps its own pixels (stretched the same way).

## Install
* Each Mart is found by its old 2x2 door pair and grows one column on the side with plain ground
  (`SIDE` forces a side). The new door (column 2) is one of the old door cells, so nothing in front
  of it changes. Four Island (house over the old Mart's right half) is moved 3 cells left (`SPECIAL`).
* Tiles: General was full. 15 duplicate tiles (incl. flipped copies) are merged in every metatile
  that sees General's tiles, which frees their slots without changing a pixel; the old Mart's tiles
  and tiles only unplaced metatiles reference are recycled. 8 slots are left afterwards.
* Metatiles: 25 canonical in General (door keeps 0x097). Ground variants go into the town's
  secondary; gTileset_TosaPort and gTileset_BattleFrontierOutsideWest were at 512, so unplaced,
  unlabelled metatiles there are recycled.
* Door: 1x2 animated door (`DOOR_SIZE_1x2`, `graphics/door_anims/poke_mart.png` 16x96).
  `METATILE_General_Door_PokeMart_Right` is gone; the second door warp is removed and warp ids past
  it renumbered (Changu Cafe, Wavebreak Sailor's Hut).
* Objects on the new column move (the signpost to the far side of the front row); the
  "read the Mart sign" bg events sit on the window display (front row, columns 3-4).
* Overwritten scenery: BF West bench, Lavaridge / Verdanturf / Six Island edge cells, Timah's left
  flower planter (the signpost takes that side).
