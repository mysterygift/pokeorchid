# Sailor's Voyages, batch 2: Sevii Islands 1-3 design-review mockups

These are mockups only. Nothing under data/, src/, include/ or graphics/ was changed. Every cell is copied from an existing layout with the same primary + secondary pair, or is a General-primary metatile, which shows the same art in every General pair. That covers the new Orchid Centre, Mart and red-roof house, the sea, sand, grass, trees, rock and ponds. No tileset is edited.

Each map is drawn at 1x and @2x. Marks:
- yellow = Sailor / NPC
- white = boat / ferry
- blue = warp
- pink double box = empty landmark spot
- red = item ball
- green = sign
- orange text = map connection

Sprites are the real overworld PNGs, Emerald graphics only.

To regenerate (Pillow venv): `python dev_scripts/voyages/mock_batch2.py [name ...] [--seams]`. Specs are in `specs_batch2.py`; the shared tooling is `voyage_compose.py`. Batch 2 added `pstamps`, `ring_multi()`, sprites and the `conn`/`spot` mark kinds to `voyage_compose.py`; batch 1 still renders unchanged.

## Geography
- **Region map:** `sevii123_region_map@4x.png` renders `map_sevii_123.png/.bin` with the section boxes from `region_map_layout_sevii123.h`.
  - Kindle Road runs north from One Island (cell 1,8) up column 2.
  - Two Island is at (9,9), with Cape Brink at (9,7-8).
  - Bond Bridge runs from (14-17,12) to Three Island at (18,12).
  - Mt. Ember and Berry Forest have no cell of their own.
- **Overview:** `overview.png` puts the region map beside every mockup at 1/4 scale, placed by its connection offsets.
- **FRLG references:** `frlg_ref.py` renders the deleted FRLG layouts (from git `8ee39561d7~1`, using the FRLG tilesets still in data/tilesets) into `ref/frlg/`. They are reference only; FRLG cells cannot be copied into an Emerald pair.
- **Scale:** FRLG's Sevii maps use about 24 tiles per region cell. The sea routes are shorter than that (One to Two is 7 cells, about 170 tiles in FRLG) so Surfing stays short.

## Tileset pairs (one secondary per cluster leg)
| Maps | Pair | Other layouts using the secondary |
|---|---|---|
| One Island, Kindle Road | General + **Rustboro** | 5: ROUTE116, SOUTHERN_ISLAND_EXTERIOR/INTERIOR, FARAWAY_ISLAND_ENTRANCE, UBE_CITY (batch 1 Eon / Fullmoon too) |
| Mt. Ember, Mt. Ember summit | General + **Lavaridge** | 12: LAVARIDGE_TOWN, JAGGED_PASS, FIERY_PATH, MAGMA_HIDEOUT_1F/2F_1R/2F_2R/2F_3R/3F_1R/3F_2R/3F_3R/4F, DRAKE_BASE_CAMP |
| Two Island, Cape Brink, Sea Routes A + B | General + **Dewford** | 4: DEWFORD_TOWN, BIRTH_ISLAND_EXTERIOR, NAVEL_ROCK_EXTERIOR, FURONG_VILLAGE (batch 1 Newmoon too) |
| Three Island, Bond Bridge, Berry Forest | General + **Fortree** | 4: FORTREE_CITY, ROUTE119, ROUTE120, FARAWAY_ISLAND_INTERIOR |

Two seams cross a change of secondary: Kindle Road / Mt. Ember, and Sea Route B / Bond Bridge. On both, the shared edge rows are built from General-primary cells only (sand, trees, rock, sea), so the two sides match.

All sizes are even and satisfy (w+15)*(h+14) <= 10240.

---

## 1. One Island: `one_island.png` (32x28, General + Rustboro)
- **Layout:** a town on a grass plateau, ringed by General rock massif and Petalburg Woods trees.
  - **Pokémon Net Center:** a second Centre exterior at the top, in the spot of FRLG's big building.
  - **Pokémon Centre:** below it.
  - **Houses:** a red-roof house, and Mr. Briney's Route 104 cottage as a second house.
  - **Beach:** to the east, running into Sea Route A.
  - **South coast:** a rock rim into the sea.
- **Harbour:**
  - **Ferry berth:** the Southern Island concrete dock (the S.S. Tidal berth), copied whole from SOUTHERN_ISLAND_EXTERIOR. Its gangway stairs come down the rim at (16-17,19).
  - **Sailor's boat:** waits off the west end of the dock.
- **Warps:**

  | Warp | Position | Leads to |
  |---|---|---|
  | Net Center | (20,7) | interior |
  | Centre | (20,14) | clone of TelokTown_PokemonCenter_1F |
  | Red-roof house | (10,6) | house interior |
  | Briney cottage | (11,14) | house interior |
  | Ferry berth | (16,21) | ferry script tile (not a warp) |

- **Objects:**

  | Object | Graphic | Position | Facing |
  |---|---|---|---|
  | Sailor | SAILOR | (12,23), on the dock | left |
  | Boat | MR_BRINEYS_BOAT | (9,23) | right, bow to the dock |
  | Ferry | SS_TIDAL | (14,26) | |
  | NPCs | generic townsfolk | 3 | |
  | Signs | | (14,7), (14,16) | |

- **Connections:**
  - North: Kindle Road. Kindle's x0 is One Island's x4 (offset 4), and the path is at x16-17.
  - East: Sea Route A (offset 0).
  - South: sea only; see question 3.

## 2. Kindle Road: `kindle_road.png` (28x96, General + Rustboro)
- **Layout, south to north:**
  - forest-flanked path from One Island
  - beach strip with sea rocks
  - a grassy terrace with tall grass, two one-way ledges at y56 and y63 and a tree line
  - a Surf-only stretch (y31-44)
  - a second beach strip
  - the sandy foot of Mt. Ember
- **Coast and rock:** a rock massif wall on the west all the way up. Route 104 shore and sea rocks on the east.
- **Ember Spa:** a red-roof house with a sign at the north end. The door is at (5,6) and the sign at (8,6).
- **Objects:** 6 generic NPCs: fisherman, old woman, camper, picnicker, swimmer, hiker.
- **Connections:**
  - South: One Island (offset -4). Rows 94-95 repeat One Island's top row exactly.
  - North: Mt. Ember (offset -1). Row 0 is Mt. Ember's bottom row without its outer rock columns.

## 3. Mt. Ember: `mt_ember.png` (30x48), summit: `mt_ember_summit.png` (24x24), General + Lavaridge
- **Exterior:**
  - **Slope:** Jagged Pass rows 0-39, unchanged: ash terraces, ash trees, stairs.
  - **Foot:** rows 40-47 are a new forest-flanked foot that opens onto Kindle Road's sand.
  - **To the summit:** the top stairs at (13-14,5) warp to the summit, as Jagged Pass's do to Mt. Chimney.
  - **Ruby Path:** Jagged Pass's cave door at (16,18) is marked "Ruby Path (closed)".
  - **NPCs:** a hiker and an expert.
  - **Connection:** south to Kindle Road (offset +1).
- **Summit:**
  - **Source:** a crop of Mt. Chimney (x8-31, y0-23): the lava crater, the ash rim terraces, and the stairs at (17,22). Those stairs are the warp back to (13,5) on the exterior.
  - **Meteorite machine:** removed by copying two plain neighbour cells over it.
  - **Legendary spot:** (12,12) on the plateau in front of the crater is marked and left empty.

## 4. Two Island: `two_island.png` (40x24), Cape Brink: `cape_brink.png` (24x32), General + Dewford
- **Two Island:** built like vanilla Dewford: sand ground, Dewford's 1-wide trees, rock to the north-east.
  - **Joyful Game Corner:** Dewford Town Hall (5x4, the biggest Dewford house). The door is at (11,5) and its sign at (15,5).
  - **Centre and Mart:** they sit on a small lawn (x17-29, y3-8), because the Mart's corner cells are grass-only in the primary. Centre door (20,7); Mart doors (26,7) and (27,7); sign (23,7).
  - **Houses:** Dewford houses with doors at (10,14) and (28,15).
  - **Town sign:** (16,19).
  - **Harbour:** Dewford's wooden pier on the east beach, at (35-37,16-17). It has a fisherman and no ferry; see question 4.
  - **NPCs:** 4.
  - **Connections:**
    - West: Sea Route A (offset -4).
    - North: Cape Brink (offset +8, opening at x16-21).
    - East: Sea Route B (offset 0).
- **Cape Brink:**
  - **Layout:** a grass cape with a rock rim into the sea, a Dewford house at the tip (door at 11,9) and a cross-shaped pond. The pond uses the General pond set with Route 120 banks, learnt by the autotiler.
  - **Below the pond:** tall grass between 2x2 trees, then Dewford trees and the sand road down to Two Island.
  - **NPCs:** 2.
  - **Connection:** south to Two Island (offset -8). Rows 28-31 repeat Two Island's top row (x8-31).

## 5. Three Island: `three_island.png` (32x32), Bond Bridge: `bond_bridge.png` (64x20), Berry Forest: `berry_forest.png` (36x36), General + Fortree
- **Three Island:** a Fortree-style forest town.
  - **Treehouses:** two Fortree treehouses up in the trees. Doors are at (6,3) and (24,3), with ladders down to y6.
  - **Centre and Mart:** Centre door (15,12); Mart doors (21,12) and (22,12).
  - **Houses:** two red-roof houses (the General primary house, as on Route 119), doors at (5,19) and (21,20).
  - **Roads, signs, NPCs:** dirt roads, 2 signs, 3 NPCs.
  - **Connections:**
    - West: Bond Bridge (offset +4). The road at rows 13-14 meets Bond Bridge's rows 9-10.
    - South: the road exits at x14-15 toward Three Isle Port; see question 3.
- **Bond Bridge:** Route 119's log bridge, 34 cells long, over the open sea at rows 9-10.
  - **Bridge pieces:** 211/219 west end, 210/218 over water, 215/21D east end.
  - **West landing:** a sandy islet with a gap in the forest, the Berry Forest entrance (warps at 8-9,4), and a sign.
  - **East end:** a beach, then a forest road into Three Island.
  - **Sea rocks and NPCs:** sea rocks on both sides; a swimmer and a fisherman on the bridge, and a lass.
  - **Connections:**
    - West: Sea Route B (offset -28; arrive by Surf).
    - East: Three Island (offset -4).
- **Berry Forest:**
  - **Layout:** a maze of 2x2 Petalburg Woods trees on a 2x2 block grid, with tall-grass pockets, flower patches and a small pond.
  - **Exit:** warps at (17-18,35), back to Bond Bridge.
  - **Items:** 4 item balls; 2 are labelled "berry".
  - **Berry trees:** a "berry tree?" note marks one spot. They would be objects; see question 7.

## 6. Sea routes: `sea_route_a.png` (80x28), `sea_route_b.png` (64x48), General + Dewford
- **Why routes:** the region map spacing is too wide to join the towns' edges directly. One to Two is 7 cells, and Two to Bond Bridge is 5 cells across and 3 down.
- **Content:** open sea with Route 104 sea rocks, small grassy islets with a rock rim and 2x2 trees, swimmers, and an item ball on an islet.
- **Sea Route A:**
  - West: One Island (offset 0). Its rock headland in rows 0-8 continues One Island's north-east rock.
  - East: Two Island (offset +4).
- **Sea Route B:**
  - West: Two Island (offset 0). Rows 0-5 are rock.
  - East: Bond Bridge (offset +28).
  - The region map's islet south-east of Two Island (cell 10-11,11) is the 12x12 grassy island.

## Known seams (from `mock_batch2.py --seams`, cell pairs never seen side by side in vanilla)
- **Trees against rock:** 2x2 trees directly against the rock massif (One Island, Kindle Road, Mt. Ember foot) or the rock rim (islets). Vanilla puts a grass column between them.
- **Islet coasts:** a few rim / sea-edge corners on the small islets, and the north coasts have no grass lip.
- **Bridge:** the bridge ends meet the beach-shore cells (Bond Bridge).
- **Two Island:** Dewford tree trunks sit directly above the Game Corner roof.

They look acceptable at mockup scale; fix them cell by cell when building for real. Two kinds of fix were made during review:
- Bond Bridge's shore beside the bridge ends is now beach rather than rim.
- The narrow 2-wide pond in Berry Forest was removed.

## Open questions (recommendation first)
1. **Net Center.** The mockup has two Centre exteriors, as asked. In FRLG, One Island's Pokémon Center *is* the Net Center (Celio's machine is inside), so FRLG has no separate building.
   - **Recommendation:** keep one Centre labelled Pokémon Net Center, with Celio inside, and turn the second building into a house.
2. **Ferry stand-in.** OBJ_EVENT_GFX_SEAGALLOP exists but sits inside the IS_FRLG block, so it is invisible in this build. The mockup shows OBJ_EVENT_GFX_SS_TIDAL at the One Island berth.
   - **Recommendation:** use the S.S. Tidal sprite for the cluster ferry. The alternative is to enable the Seagallop graphics outside IS_FRLG.
3. **Treasure Beach and Three Isle Port.** Both are on the region map but out of scope.
   - One Island's south edge is sea; Three Island's south road ends at the map edge.
   - **Recommendation:** leave both as stubs now (close Three Island's road with trees if the Port is never built), and add them in a later batch.
4. **Ferry berths on Two and Three Island.** Only One Island got the ferry dock. Two Island's harbour is a small wooden pier; Three Island has no harbour, because the Fortree pair has no pier, and FRLG's lives at Three Isle Port.
   - **Recommendation:** the 1-3 ferry stops only at One Island. If Three Island needs a berth, build Three Isle Port on Dewford or Rustboro.
5. **Mt. Ember slope.** The slope is Jagged Pass rows 0-39, almost unchanged, so players will recognise it.
   - **Recommendation:** accept it as the "same volcano family" look, and repaint the terrace layout in Porymap when building.
   - The alternative is a new slope built from Mt. Chimney's lower switchbacks.
6. **Summit Path.** FRLG reaches the summit through a 3-floor cave. The mockup warps straight from the top stairs to the summit.
   - **Recommendation:** use the direct warp. Ruby Path stays a closed cave door.
7. **Berry Forest berries.** Berry trees are objects (berry tree gfx on soft soil), not metatiles.
   - **Recommendation:** use item balls with berries now, and add real berry-tree objects later if wanted.
8. **Three Island style.** Fortree treehouses replace FRLG's houses. This was chosen for the Fortree pair's log bridge and forest.
   - **Recommendation:** keep it. The alternative is Three Island on Petalburg (Telok's brown-roof houses), which has no bridge, so Bond Bridge would need its own pair and a General-only seam.
9. **Sea route length.** The routes are 80 and 64 tiles, short of FRLG's ~24 tiles per cell.
   - **Recommendation:** keep them short.
10. **Map ids.** Proposed: MAP_ONE_ISLAND, MAP_ONE_ISLAND_KINDLE_ROAD, MAP_MT_EMBER_EXTERIOR, MAP_MT_EMBER_SUMMIT, MAP_TWO_ISLAND, MAP_TWO_ISLAND_CAPE_BRINK, MAP_THREE_ISLAND, MAP_THREE_ISLAND_BOND_BRIDGE, MAP_THREE_ISLAND_BERRY_FOREST, MAP_SEVII_SEA_ROUTE_A/B.
    - Most of these layout ids still exist in layouts.json as FRLG entries whose files are deleted. Reuse the ids with new map.bin files, or delete those entries first.
    - The sea routes need new MAPSEC cells between the islands on `region_map_layout_sevii123.h`.
