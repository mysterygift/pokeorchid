# Centre / Mart exteriors v2

Replaces the 4x4 shophouse Centre / convenience Mart exteriors (dev_scripts/centre_mart) with the
supplied sheet art: a 5x5 Pokemon Centre and a 4x5 Poke Mart, plus a rotating Mart signpost.

| step | script | output |
|---|---|---|
| fit art to the grid + palettes | `art.py` | `art/centre.png` (80x80, General pal 1), `art/mart.png` (64x80, pal 0) |
| choose placements | `plan.py` | `plan.json` (new boxes, forced cells, NPC moves, sign cells) |
| install | `integrate.py [--write]` | General tiles/metatiles, town variants, layouts, warps, NPCs, signs, door frames, arrow frames, labels |
| signpost sprite | `sign.py` | `graphics/object_events/pics/misc/mart_sign.png` |
| render check | `verify.py` | `out/verify.png` |
| in-game check | `ingame.py <harness rom> <outdir> all\|bura` | exit/enter every building, screenshots |

Needs Pillow + numpy.

## Art
* The supplied art is made exactly mirror-symmetric (left half mirrored) so the right half reuses
  tiles with h-flip; only the Centre's arrow sign and the Mart's window display keep their own
  right-hand pixels. Mart: one pixel column inside each outline dropped (66 -> 64 px wide).
* Colours snapped to the existing General palettes 1 (Centre) and 0 (Mart). Those palettes are
  shared with houses in a dozen town tilesets, so they cannot change. The Centre loses one red
  shade (5 -> 4) and its dark window blue becomes slate.
* The 1-2 px ground gap under each door is filled with the base outline colour: door animations
  redraw the door cells without the ground layer, so door cells must be opaque.

## Layers / collision
* Row 0 (roof back edge): art in the top layer (over sprites) on the town's ground; walkable when
  the cell behind it is, so the roof hides a player walking behind the building.
* Rows 1-4: COVERED (both layers under sprites), solid; a player in front draws over the facade.
* Doors: vanilla bump-to-enter (collision 1, elevation 0, MB_ANIMATED_DOOR). Centre door is a 1x2
  animated door (`METATILE_General_Door_PokeCenter`); the Mart is a 2x2 sliding double door
  (`METATILE_General_Door_PokeMart` / `_Right`, `DOOR_SIZE_2x2_LEFT/RIGHT`) with a warp on each cell.

## Tile budget
General had 95 usable 8x8 slots; the art needs exactly 95. Some came from vanilla tiles that only
unplaced metatiles in Hoenn secondaries (Petalburg, Rustboro, Lilycove, Battle Frontier, ...)
referenced; those unplaced metatiles now draw garbage in Porymap. No slots are left in General.

## Arrow animation
Tiles 167-168 hold the Centre sign's arrow panel; `QueueAnimTiles_General_CentreArrow`
(src/tileset_anims.c) scrolls the arrow left through 16 frames (every 8 vblanks).
If `integrate.py` is re-run on a fresh tree it may choose a different pair: check `installed.json`.

## Signpost
`OBJ_EVENT_GFX_MART_SIGN`: 16x32 inanimate object on the shared npc_1 palette: a 14x10x4 board
drawn in 3/4 overhead projection (top face always visible), 8 frames per half turn. Placed on a free cell
beside each Mart's front row; not placed at Battle Frontier West, Lavaridge, Verdanturf (no room).

## Forced placements (legacy Hoenn maps)
Battle Frontier East, Fallarbor, Fortree, Lavaridge, Pacifidlog, Verdanturf have no plain ground
for the bigger boxes; the cheapest box overwrote scenery there (see `plan.json` "forced").
