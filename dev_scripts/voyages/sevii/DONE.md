# Sevii stream: done (Wavebreak Voyages)

Worktree `pokeorchid-voy-sevii` (detached at bc3f480c7c). Nothing is committed. The clean `make -j8` build passes,
`grep gHarnessKeys pokeemerald.map` = 0, and there are no new warnings.

## Hand-off for the core stream: the voyage arrival point
- **Map:** `MAP_ONE_ISLAND_HARBOR`, the One Island harbour dock.
- **Cell:** x 8, y 4, in front of the ferry sailor (8,5). Mr. Briney's boat is at (8,7).
- **Warp id:** 1. This is a landing-only warp event on that cell, so `warp MAP_ONE_ISLAND_HARBOR, 1` works as well as `8, 4`.
- **Constants:** `include/constants/sevii.h` defines `SEVII_ARRIVAL_MAP` / `_WARP_ID` / `_X` / `_Y`.

  Fill the SEVII entry in `src/voyages.c` with `.arrivalMap = MAP_ONE_ISLAND_HARBOR, .arrivalX = 8, .arrivalY = 4`.
- **Other harbours:** every island harbour (`MAP_<N>_ISLAND_HARBOR`) uses the same landing cell and warp id 1. Three's harbour is reached from Three Isle Port.
- **Return voyage:** the ferry sailor's menu has no "home" option. The core stream owns that: add a case to `OneIsland_Harbor_EventScript_Sailor`, or put its own Sailor NPC on the dock.
- **`src/seagallop.c`:** `sSeag` still lands the FRLG harbours at (8,5). That's the sailor's cell in this layout, so change it to (8,4) if the fancy ferry scene is used.

## Regenerate
1. Export in a tree **without** these changes. The translator reads data/, so re-exporting on top of the installed maps gives different output. For example, use a scratch worktree at bc3f480c7c:
   `<venv> dev_scripts/voyages/sevii/frlg_translate.py export --out DIR`
2. Then run in this tree: `<venv> dev_scripts/voyages/sevii/build_sevii.py DIR`
   - It's idempotent: blocks are marked, and the flag allocation is kept in `sevii_flags.json`.
   - The `CONFIG` dict at the top holds the open-question switches.
3. Checks:
   - `python3 dev_scripts/voyages/sevii/check_sevii.py [--world]`
   - `view.py Map [x0 y0 x1 y1]` prints an ASCII view.
4. Headless:
   - Build the harness with `harness_test_build.sh <dir>/h <save copy>`. It patches `MonKnowsMove` so the party "knows" Surf, then reverts it; rebuild normally afterwards.
   - Run `<venv> emu_sevii.py <dir>/h [towns centre ferry ice surf ember stall gamecorner warehouse]` while holding `/tmp/voyages_mgba.lock`.

The scripts were copied from `pokeorchid-voyages/dev_scripts/voyages`, with ROOT moved one level deeper. The new ones are `build_sevii.py`, `check_sevii.py`, `emu_sevii.py`, `mtattr.py`, `reach_flags.py`, `sevii_text.py`, `view.py` and `harness_test_build.sh`.

## What changed
- **gTileset_SeviiIslands** (`data/tilesets/secondary/sevii_islands/`, `-num_tiles 498`):
  - Registered in headers.h, graphics.h, metatiles.h, `include/tilesets.h` and the metatile_labels.h `METATILE_SeviiIslands_*` block.
  - Uses the Rustboro animation callback.
  - `src/field_door.c`: the two Rustboro door entries are repeated for the Sevii copy. The Rocket Warehouse door has its own animation, `graphics/door_anims/sevii_rocket_warehouse.png` (Cold Storage frames recoloured with the R, palette 12).
  - No shared tileset was touched. Tanoby Ruins uses gTileset_TanobyDelta as it is.
- **98 maps in `gMapGroup_Sevii`**, appended after Tiksi. They are listed in `build_report.json`:
  - 86 exported maps
  - 7 Centres (TelokTown_PokemonCenter_1F clones). One Island's is the Net Center: MUS_RG_NET_CENTER and a technician.
  - 4 Marts (Three, Four, Six, Seven; TelokTown_Mart clones with a post-game stock)
  - the Joyful Game Corner: the deleted Mauville Game Corner room and scripts, restored from git `1d1d50b3a2^` as `LAYOUT_TWO_ISLAND_JOYFUL_GAME_CORNER`. Seven chatter NPCs got new lines; the coin/prize clerks, Starter-doll girl and 20-coin man are unchanged.

  Other map details:
  - FRLG layout ids are replaced in place in layouts.json. The FRLG House3/House4 folders became `SeviiHouse3/4`, because Emerald already has `data/layouts/House3`.
  - The scripts include block is `@ sevii-maps` in `data/event_scripts.s`, plus `data/scripts/sevii.inc`, which holds the ferry, market stall, Mart list and Ember Spa heal.
- **Warps:**
  - linked symmetrically
  - 21 second exit-mat warps added
  - Rocket Warehouse exit moved onto its moved mat
  - Mt. Ember's 3 FRLG arrow warps sit on shared Lavaridge ash, so they are plain warp events plus facing-checked coord triggers (`EDGE_WARPS`)
  - SeviiIslands arrow warps use the MB_*_ARROW_WARP duplicates
- **Connections:** as exported; the sea routes A–D join the clusters.
- **NPCs:**
  - No trainers: every former trainer is TRAINER_TYPE_NONE with a flavour line from `sevii_text.py`.
  - Removed: Moltres, Ruby, Sapphire, Blue, the e-Reader trainer, and Icefall Back's Lorelei/Rocket scene. All story coord triggers were dropped.
  - Kept: Ember Spa's heal trigger.
  - Mt. Ember's two grunts stepped off the Ruby Path mouth.
  - FRLG-only graphics are swapped: missing FRLG dolls became other Emerald dolls, and the Chansey uses `SPECIES(CHANSEY)`.
- **Layout fixes** (`fix_layouts`, counts in `build_report.json`):
  - Mt. Ember's ash 0x271 had come out solid, so walkable FRLG cells took FRLG's collision back (exterior 321 cells, summit 98).
  - Pond water the translator blocked was made surfable again (Berry Forest 19, Four Island 10, plus a few more).
  - Elevation-4 pier planks and the Memorial Pillar plaza became 3. They had cut the harbour docks off from every town.
  - Two closed passages were opened: Four Island (39,27) to the Icefall pond, and Six Island's dock edge (14,25) to the sea.
  - 8 walled-in items or NPCs moved to the nearest reachable cell.
  - Object elevations now match the cell they are talked from.
- **Default answers to the open questions** (each one flips in `CONFIG` / `build_sevii.py`):
  - **Dotted Hole door and the 7 Tanoby chamber doors are sealed.** The cell is impassable and has a "sealed" sign; the warps and maps stay linked. To re-open, set `seal_*` False and give those cells a door metatile with MB_NON_ANIMATED_DOOR: they are rock/facade in the translation.
  - **Two Island stall** is a pokemart of 30 rare items (the batch-3 list plus mints, Upgrade and Dragon Scale) at ×3.
    - The price comes from `VAR_SHOP_PRICE_MULTIPLIER` (was VAR_UNUSED_0x409B), read by a new `SeviiShopPrice()` in `src/shop.c`.
    - The stall script sets it to 3 and clears it after the shop closes.
  - **Rocket grunts** are Team Aqua sprites (`EXPORT_SWAP`) and don't battle.
  - **Water Path's pale path** keeps the export's port.
  - **Icefall's HM07 ball** gives ITEM_ICE_STONE instead (no free HM).
  - **The Dunsparce Tunnel** uses the dug-out layout, so both ends are joined.
- **Ferry:** the sailor in every harbour opens a 7-line menu: the other six islands (own cluster first) and "Stay here". The boat leaves (`Common_EventScript_FerryDepartIsland`), then the game warps to that harbour's (8,4).
- **Heal locations:** `HEAL_LOCATION_ONE…SEVEN_ISLAND` were updated in place: door +1, `LOCALID_<ISLAND>_NURSE`. Their `respawn_npc` survives the mapjson rewrite.
- **Flags:**
  - `FLAG_VISITED_ONE…SEVEN_ISLAND` = FLAG_UNUSED_0x264–0x26A, set on transition into each island town. The FRLG `#define FLAG_VISITED_TWO_ISLAND 0` was commented out.
  - `FLAG_WORLD_MAP_*_ISLAND` now alias the visited flags, ready for region_map.c.
  - 0x26B–0x27F are still free.
  - Item and hidden-item flags reuse unreachable vanilla flags; see the table below.
- **Map sections** (exact ids from regionmap/IMPLEMENTATION.md):
  - SEVII_ISLE_22/23/24 and THREE_ISLE_PATH were renamed to ONE_TWO / TWO_THREE / FOUR_FIVE / SIX_SEVEN_STRAIT, with aliases in region_map_section_aliases.h.
  - Sea routes A–D use them in that order. Dunsparce Tunnel moved to THREE_ISLE_PORT.
  - Sevii names are in title case.
  - x/y/width/height are **not** set; that is the region-map stream's job.
  - overworld.c / IsTiksiMapSec were not touched.
- **Wild encounters:** 41 `gSevii_*` tables (Emerald) plus the Dunsparce Tunnel.
  - Built from FRLG's FireRed/LeafGreen tables, alternating slots between versions.
  - Unevolved species are evolved, and levels are mapped into 55–68. Old Rod stays Magikarp.
  - Towns with water, Ruby Path B4F/B5F and the four straits borrow their neighbours' tables.
  - Sealed or story-only maps have none.

## Verification
- **Static** (`check_sevii.py`, `check_report.json`):
  - All 98 maps fit (w+15)*(h+14) ≤ 10240; Tanoby Ruins is the largest at 5406.
  - Every warp has a matching return warp, except Dotted Hole's deliberate fall-back warps and the harbour landing warps.
  - Every connection has its reverse.
  - Flood fill: every warp, NPC, item ball and hidden item is reachable. The leftovers are decorations: Lorelei's shelf dolls, the Day-Care pen Pokémon, and one Rocket Warehouse cage sign.
  - Entry splits remain only where FRLG has them, i.e. multi-floor dungeons joined through other floors (Icefall, Ruby Path, Mt. Ember's upper ledge via Summit Path, the Dunsparce east mouth).
  - `--world`: from the One Island dock, every warp in the cluster is reachable except the sealed Dotted Hole.
- **Headless** (shots and results_*.json in `shots/`): **23/23 PASS**.
  - **Towns:** debug-warped into all 7 island towns; FLAG_VISITED was set for each.
  - **Centre:** the Net Center nurse healed (lead HP 1 → 126), and the exit lands at (14,6).
  - **Ferry:** the arrival warp lands at (8,4). The ferry went One → Four Island harbour, then out onto Four Island.
  - **Icefall B1F:** one UP press slid the player from (17,14) to (17,10).
  - **Surf:** off Two Island's dock into One-Two Strait (Sea Route A), and across it to Kindle Road. A wild Lv59 Tentacruel appeared on the way: `wild_sea_route_a_tentacruel_lv59.png`.
  - **Mt. Ember:** the edge warps work in both directions with Kindle Road.
  - **Market stall:** Ability Capsule costs ₽300000 (3 × 100000), and the multiplier is back to 0 afterwards.
  - **Joyful Game Corner:** in and out.
  - **Rocket Warehouse:** the door animation plays and leads into the interior.

## Known gaps
- **Seams:** the translation seams noted in the batch NOTES (massif pairs, trees against rock) are still there, and Mt. Ember's terraces still need the user's repaint.
- **Moved items:** a few walled-in items/NPCs were moved rather than reopening FRLG's paths (Meadow, Berry Forest pond pocket, Four Island). See `build_report.json` → `relocated`.
- **Region map:** Sevii sections have no x/y yet, so the region map falls back. The Fly table and heal rows in region_map.c are for the region-map stream.
- **Hidden items** are no longer underfoot (Emerald style: face the tile).
- **Day-Care man** has flavour text only; there's no Four Island Day-Care function.

## Reused flags (old vanilla name → kept as an alias)
| Sevii flag | Vanilla slot (alias) |
|---|---|
| FLAG_HIDDEN_ITEM_SEVII_FIVE_ISLAND_MEMORIAL_PILLAR_BIG_PEARL | FLAG_HIDDEN_ITEM_ROUTE_105_BIG_PEARL |
| FLAG_HIDDEN_ITEM_SEVII_FIVE_ISLAND_MEMORIAL_PILLAR_BLUK_BERRY | FLAG_HIDDEN_ITEM_ROUTE_113_ETHER |
| FLAG_HIDDEN_ITEM_SEVII_FIVE_ISLAND_MEMORIAL_PILLAR_RAZZ_BERRY | FLAG_HIDDEN_ITEM_LAVARIDGE_TOWN_ICE_HEAL |
| FLAG_HIDDEN_ITEM_SEVII_FIVE_ISLAND_MEMORIAL_PILLAR_SITRUS_BERRY | FLAG_HIDDEN_ITEM_ROUTE_111_STARDUST |
| FLAG_HIDDEN_ITEM_SEVII_FIVE_ISLAND_ROCKET_WAREHOUSE_NEST_BALL | FLAG_HIDDEN_ITEM_ROUTE_114_CARBOS |
| FLAG_HIDDEN_ITEM_SEVII_FIVE_ISLAND_ROCKET_WAREHOUSE_NET_BALL | FLAG_HIDDEN_ITEM_LILYCOVE_CITY_HEART_SCALE |
| FLAG_HIDDEN_ITEM_SEVII_FOUR_ISLAND_PEARL | FLAG_HIDDEN_ITEM_FALLARBOR_TOWN_NUGGET |
| FLAG_HIDDEN_ITEM_SEVII_FOUR_ISLAND_ULTRA_BALL | FLAG_HIDDEN_ITEM_VICTORY_ROAD_1F_ULTRA_BALL |
| FLAG_HIDDEN_ITEM_SEVII_MT_EMBER_EXTERIOR_FIRE_STONE | FLAG_HIDDEN_ITEM_ROUTE_113_TM_DOUBLE_TEAM |
| FLAG_HIDDEN_ITEM_SEVII_MT_EMBER_EXTERIOR_ULTRA_BALL | FLAG_HIDDEN_ITEM_ROUTE_104_POTION |
| FLAG_HIDDEN_ITEM_SEVII_ONE_ISLAND_TREASURE_BEACH_BIG_PEARL | FLAG_HIDDEN_ITEM_GRANITE_CAVE_B2F_EVERSTONE_2 |
| FLAG_HIDDEN_ITEM_SEVII_ONE_ISLAND_TREASURE_BEACH_PEARL | FLAG_HIDDEN_ITEM_LILYCOVE_CITY_PP_UP |
| FLAG_HIDDEN_ITEM_SEVII_ONE_ISLAND_TREASURE_BEACH_PEARL_2 | FLAG_HIDDEN_ITEM_ROUTE_104_SUPER_POTION |
| FLAG_HIDDEN_ITEM_SEVII_ONE_ISLAND_TREASURE_BEACH_STARDUST | FLAG_HIDDEN_ITEM_ROUTE_106_STARDUST |
| FLAG_HIDDEN_ITEM_SEVII_ONE_ISLAND_TREASURE_BEACH_STARDUST_2 | FLAG_HIDDEN_ITEM_ROUTE_114_REVIVE |
| FLAG_HIDDEN_ITEM_SEVII_ONE_ISLAND_TREASURE_BEACH_STAR_PIECE | FLAG_HIDDEN_ITEM_GRANITE_CAVE_B2F_EVERSTONE_1 |
| FLAG_HIDDEN_ITEM_SEVII_ONE_ISLAND_TREASURE_BEACH_ULTRA_BALL | FLAG_HIDDEN_ITEM_ROUTE_116_SUPER_POTION |
| FLAG_HIDDEN_ITEM_SEVII_ONE_ISLAND_TREASURE_BEACH_ULTRA_BALL_2 | FLAG_HIDDEN_ITEM_ROUTE_106_HEART_SCALE |
| FLAG_HIDDEN_ITEM_SEVII_SEVEN_ISLAND_SEVAULT_CANYON_CHERI_BERRY | FLAG_HIDDEN_ITEM_ROUTE_109_REVIVE |
| FLAG_HIDDEN_ITEM_SEVII_SEVEN_ISLAND_SEVAULT_CANYON_ENTRANCE_RAWST_BERRY | FLAG_HIDDEN_ITEM_ROUTE_109_GREAT_BALL |
| FLAG_HIDDEN_ITEM_SEVII_SEVEN_ISLAND_TANOBY_RUINS_HEART_SCALE | FLAG_HIDDEN_ITEM_ROUTE_104_HEART_SCALE |
| FLAG_HIDDEN_ITEM_SEVII_SEVEN_ISLAND_TANOBY_RUINS_HEART_SCALE_2 | FLAG_HIDDEN_ITEM_ROUTE_105_HEART_SCALE |
| FLAG_HIDDEN_ITEM_SEVII_SEVEN_ISLAND_TANOBY_RUINS_HEART_SCALE_3 | FLAG_HIDDEN_ITEM_ROUTE_115_HEART_SCALE |
| FLAG_HIDDEN_ITEM_SEVII_SEVEN_ISLAND_TANOBY_RUINS_HEART_SCALE_4 | FLAG_HIDDEN_ITEM_ROUTE_109_HEART_SCALE_1 |
| FLAG_HIDDEN_ITEM_SEVII_SIX_ISLAND_LEPPA_BERRY | FLAG_HIDDEN_ITEM_ROUTE_110_GREAT_BALL |
| FLAG_HIDDEN_ITEM_SEVII_SIX_ISLAND_WATER_PATH_ASPEAR_BERRY | FLAG_HIDDEN_ITEM_ROUTE_110_REVIVE |
| FLAG_HIDDEN_ITEM_SEVII_SIX_ISLAND_WATER_PATH_ORAN_BERRY | FLAG_HIDDEN_ITEM_ROUTE_110_FULL_HEAL |
| FLAG_HIDDEN_ITEM_SEVII_SIX_ISLAND_WATER_PATH_PINAP_BERRY | FLAG_HIDDEN_ITEM_ROUTE_111_PROTEIN |
| FLAG_HIDDEN_ITEM_SEVII_THREE_ISLAND_BERRY_FOREST_ASPEAR_BERRY | FLAG_HIDDEN_ITEM_LILYCOVE_CITY_POKE_BALL |
| FLAG_HIDDEN_ITEM_SEVII_THREE_ISLAND_BERRY_FOREST_BLUK_BERRY | FLAG_HIDDEN_ITEM_PETALBURG_WOODS_TINY_MUSHROOM_1 |
| FLAG_HIDDEN_ITEM_SEVII_THREE_ISLAND_BERRY_FOREST_CHERI_BERRY | FLAG_HIDDEN_ITEM_ROUTE_106_POKE_BALL |
| FLAG_HIDDEN_ITEM_SEVII_THREE_ISLAND_BERRY_FOREST_CHESTO_BERRY | FLAG_HIDDEN_ITEM_ROUTE_109_ETHER |
| FLAG_HIDDEN_ITEM_SEVII_THREE_ISLAND_BERRY_FOREST_LUM_BERRY | FLAG_HIDDEN_ITEM_VICTORY_ROAD_B2F_ELIXIR |
| FLAG_HIDDEN_ITEM_SEVII_THREE_ISLAND_BERRY_FOREST_NANAB_BERRY | FLAG_HIDDEN_ITEM_PETALBURG_WOODS_TINY_MUSHROOM_2 |
| FLAG_HIDDEN_ITEM_SEVII_THREE_ISLAND_BERRY_FOREST_ORAN_BERRY | FLAG_HIDDEN_ITEM_ROUTE_104_POKE_BALL |
| FLAG_HIDDEN_ITEM_SEVII_THREE_ISLAND_BERRY_FOREST_PECHA_BERRY | FLAG_HIDDEN_ITEM_ROUTE_110_POKE_BALL |
| FLAG_HIDDEN_ITEM_SEVII_THREE_ISLAND_BERRY_FOREST_PERSIM_BERRY | FLAG_HIDDEN_ITEM_JAGGED_PASS_GREAT_BALL |
| FLAG_HIDDEN_ITEM_SEVII_THREE_ISLAND_BERRY_FOREST_PINAP_BERRY | FLAG_HIDDEN_ITEM_JAGGED_PASS_FULL_HEAL |
| FLAG_HIDDEN_ITEM_SEVII_THREE_ISLAND_BERRY_FOREST_RAWST_BERRY | FLAG_HIDDEN_ITEM_ROUTE_117_REPEL |
| FLAG_HIDDEN_ITEM_SEVII_THREE_ISLAND_BERRY_FOREST_RAZZ_BERRY | FLAG_HIDDEN_ITEM_PETALBURG_WOODS_POTION |
| FLAG_HIDDEN_ITEM_SEVII_THREE_ISLAND_BERRY_FOREST_WEPEAR_BERRY | FLAG_HIDDEN_ITEM_PETALBURG_WOODS_POKE_BALL |
| FLAG_HIDDEN_ITEM_SEVII_THREE_ISLAND_BOND_BRIDGE_MAX_REPEL | FLAG_HIDDEN_ITEM_VICTORY_ROAD_B2F_MAX_REPEL |
| FLAG_HIDDEN_ITEM_SEVII_THREE_ISLAND_BOND_BRIDGE_PEARL | FLAG_HIDDEN_ITEM_ROUTE_104_ANTIDOTE |
| FLAG_HIDDEN_ITEM_SEVII_THREE_ISLAND_BOND_BRIDGE_STARDUST | FLAG_HIDDEN_ITEM_ROUTE_108_RARE_CANDY |
| FLAG_HIDDEN_ITEM_SEVII_THREE_ISLAND_DUNSPARCE_TUNNEL_NUGGET | FLAG_HIDDEN_ITEM_ROUTE_113_NUGGET |
| FLAG_HIDDEN_ITEM_SEVII_THREE_ISLAND_PP_UP | FLAG_HIDDEN_ITEM_ROUTE_111_RARE_CANDY |
| FLAG_HIDDEN_ITEM_SEVII_TWO_ISLAND_CAPE_BRINK_PP_MAX | FLAG_HIDDEN_ITEM_ROUTE_109_HEART_SCALE_2 |
| FLAG_HIDDEN_ITEM_SEVII_TWO_ISLAND_CAPE_BRINK_RARE_CANDY | FLAG_HIDDEN_ITEM_PETALBURG_CITY_RARE_CANDY |
| FLAG_ITEM_SEVII_FIVE_ISLAND_MEADOW_MAX_POTION | FLAG_ITEM_ROUTE_116_X_SPECIAL |
| FLAG_ITEM_SEVII_FIVE_ISLAND_MEADOW_PP_UP | FLAG_ITEM_ROUTE_104_PP_UP |
| FLAG_ITEM_SEVII_FIVE_ISLAND_MEMORIAL_PILLAR_METAL_COAT | FLAG_ITEM_ROUTE_105_IRON |
| FLAG_ITEM_SEVII_FIVE_ISLAND_ROCKET_WAREHOUSE_BIG_PEARL | FLAG_ITEM_ROUTE_106_PROTEIN |
| FLAG_ITEM_SEVII_FIVE_ISLAND_ROCKET_WAREHOUSE_PEARL | FLAG_ITEM_ROUTE_110_RARE_CANDY |
| FLAG_ITEM_SEVII_FIVE_ISLAND_ROCKET_WAREHOUSE_TM36 | FLAG_ITEM_ROUTE_109_PP_UP |
| FLAG_ITEM_SEVII_FIVE_ISLAND_ROCKET_WAREHOUSE_UPGRADE | FLAG_ITEM_ROUTE_110_DIRE_HIT |
| FLAG_ITEM_SEVII_FOUR_ISLAND_ICEFALL_CAVE_1F_ICE_STONE | FLAG_ITEM_ROUTE_111_HP_UP |
| FLAG_ITEM_SEVII_FOUR_ISLAND_ICEFALL_CAVE_1F_ULTRA_BALL | FLAG_ITEM_NEW_MAUVILLE_ULTRA_BALL |
| FLAG_ITEM_SEVII_FOUR_ISLAND_ICEFALL_CAVE_B1F_FULL_RESTORE | FLAG_ITEM_VICTORY_ROAD_B1F_FULL_RESTORE |
| FLAG_ITEM_SEVII_FOUR_ISLAND_ICEFALL_CAVE_B1F_NEVER_MELT_ICE | FLAG_ITEM_ROUTE_112_NUGGET |
| FLAG_ITEM_SEVII_FOUR_ISLAND_STARDUST | FLAG_ITEM_ROUTE_111_STARDUST |
| FLAG_ITEM_SEVII_FOUR_ISLAND_STAR_PIECE | FLAG_ITEM_ROUTE_111_TM_SANDSTORM |
| FLAG_ITEM_SEVII_MT_EMBER_EXTERIOR_DIRE_HIT | FLAG_ITEM_ROUTE_114_RARE_CANDY |
| FLAG_ITEM_SEVII_MT_EMBER_EXTERIOR_FIRE_STONE | FLAG_ITEM_ROUTE_113_SUPER_REPEL |
| FLAG_ITEM_SEVII_MT_EMBER_EXTERIOR_ULTRA_BALL | FLAG_ITEM_ROUTE_113_MAX_ETHER |
| FLAG_ITEM_SEVII_ONE_ISLAND_KINDLE_ROAD_CARBOS | FLAG_ITEM_ROUTE_114_PROTEIN |
| FLAG_ITEM_SEVII_ONE_ISLAND_KINDLE_ROAD_ETHER | FLAG_ITEM_ROUTE_116_ETHER |
| FLAG_ITEM_SEVII_ONE_ISLAND_KINDLE_ROAD_MAX_REPEL | FLAG_ITEM_LILYCOVE_CITY_MAX_REPEL |
| FLAG_ITEM_SEVII_SEA_ROUTE_A_PEARL | FLAG_ITEM_ROUTE_116_HP_UP |
| FLAG_ITEM_SEVII_SEA_ROUTE_B_STAR_PIECE | FLAG_ITEM_ROUTE_117_GREAT_BALL |
| FLAG_ITEM_SEVII_SEA_ROUTE_C_BIG_PEARL | FLAG_ITEM_ROUTE_123_RARE_CANDY |
| FLAG_ITEM_SEVII_SEVEN_ISLAND_SEVAULT_CANYON_HOUSE_LUCKY_PUNCH | FLAG_ITEM_ROUTE_116_REPEL |
| FLAG_ITEM_SEVII_SEVEN_ISLAND_SEVAULT_CANYON_KINGS_ROCK | FLAG_ITEM_ROUTE_115_TM_FOCUS_PUNCH |
| FLAG_ITEM_SEVII_SEVEN_ISLAND_SEVAULT_CANYON_MAX_ELIXIR | FLAG_ITEM_AQUA_HIDEOUT_B1F_MAX_ELIXIR |
| FLAG_ITEM_SEVII_SEVEN_ISLAND_SEVAULT_CANYON_NUGGET | FLAG_ITEM_ROUTE_115_IRON |
| FLAG_ITEM_SEVII_SIX_ISLAND_RUIN_VALLEY_FULL_RESTORE | FLAG_ITEM_PETALBURG_CITY_ETHER |
| FLAG_ITEM_SEVII_SIX_ISLAND_RUIN_VALLEY_HP_UP | FLAG_ITEM_PETALBURG_CITY_MAX_REVIVE |
| FLAG_ITEM_SEVII_SIX_ISLAND_RUIN_VALLEY_SUN_STONE | FLAG_ITEM_RUSTBORO_CITY_X_DEFEND |
| FLAG_ITEM_SEVII_SIX_ISLAND_WATER_PATH_DRAGON_SCALE | FLAG_ITEM_MOSSDEEP_CITY_NET_BALL |
| FLAG_ITEM_SEVII_SIX_ISLAND_WATER_PATH_ELIXIR | FLAG_ITEM_VICTORY_ROAD_1F_MAX_ELIXIR |
| FLAG_ITEM_SEVII_THREE_ISLAND_BERRY_FOREST_FULL_HEAL | FLAG_ITEM_METEOR_FALLS_1F_1R_FULL_HEAL |
| FLAG_ITEM_SEVII_THREE_ISLAND_BERRY_FOREST_MAX_ELIXIR | FLAG_ITEM_METEOR_FALLS_1F_1R_MOON_STONE |
| FLAG_ITEM_SEVII_THREE_ISLAND_BERRY_FOREST_MAX_ETHER | FLAG_ITEM_RUSTURF_TUNNEL_MAX_ETHER |
| FLAG_ITEM_SEVII_THREE_ISLAND_ZINC | FLAG_ITEM_METEOR_FALLS_1F_1R_TM_IRON_TAIL |
| FLAG_ITEM_SEVII_TWO_ISLAND_REVIVE | FLAG_ITEM_ABANDONED_SHIP_ROOMS_2_1F_REVIVE |
