# Sailor's Voyages, batch 3: Sevii Islands 4–7, translated from the real FRLG maps

These are mockups plus exportable map data. Nothing under data/, src/, include/ or graphics/ was changed, and nothing is committed.

Every outdoor map below is the **FRLG map itself**, read from git `8ee39561d7~1`. Each is redrawn cell for cell at the **same size** with `frlg_translate.py`, the same tool batch 2 uses, and keeps FRLG's events.

Per map:
- `<map>_vs_frlg.png`: FRLG on the left, Emerald on the right
- `<map>.png` / `@2x.png`
- `<map>_spec.json`: spec plus report

Marks are as in batch 2. Field-move objects are now drawn with their Emerald sprites (breakable rock, boulder, cut tree).

Regenerate with the Pillow venv:
- **Batch 3:** `python dev_scripts/voyages/mock_batch3.py`. Steps are `maps routes overview regionmap` (the default) plus `ice` and `probe`; add `[FrlgMapName ...] [--seams]` to limit or check.
- **Icefall Cave:** `icefall_translate.py`
- **Rocket Warehouse interior:** `rocket_warehouse_interior.py`
- **Interiors:** `frlg_interiors.py`, writing to `out/interiors/`, which has its own NOTES.md
- **Tileset sheets:** `sevii_art_sheets.py`, writing to `out/batch3/tileset/`
- **FRLG references:** `frlg_ref.py batch3`

## Decided (DECISIONS.md, applied here)
- **Faithful FRLG translations.** Islands are linked by FRLG harbours plus the ferry, and by **invented Surf routes**. Those routes are short, are walled on both long sides by 2x2 sea rocks, and have a connection at each end.
- **FRLG currents become plain sea.**
- **FRLG arrow warps are recreated.** Each warp cell gets a duplicate metatile with MB_*_ARROW_WARP in the Sevii tileset.
- **Proposed `gTileset_SeviiIslands`.** It is a copy of gTileset_Rustboro used only by the Sevii maps, so its additions never touch Route 116, Southern Island, Faraway Island or Ube City. It carries the cottage variants, the Two Island market stall, the ported Onix tails / Memorial Pillar / Dotted Hole entrance, the Rocket Warehouse and the arrow duplicates.
- **Lone rocks become Emerald boulders:** 0x0E0 on grass, 0x0E1 on rocky dirt, 0x0E2 on sand.
- **FRLG Rock Smash objects** become OBJ_EVENT_GFX_BREAKABLE_ROCK with EventScript_RockSmash.
- **Icefall Cave** uses the Shoal Cave ice look, with the 0x386 exit mat at the entrance.
- **"Tanoby Ruins" is kept**, deliberately. It is built on Tiksi's **gTileset_TanobyDelta** as-is (no edits), so **Tanoby Delta (Tiksi) and Tanoby Ruins (Sevii) share the same chamber art.**
- **Rocket Warehouse.** The exterior is recoloured Cold Storage tiles with an R logo. The interior is a New Mauville-tile placeholder.
- **Map ids** reuse the FRLG names.
- **Centres and Marts** clone TelokTown_PokemonCenter_1F / TelokTown_Mart.
- **Generic NPCs only.** There are no trainers in this pass.

## Geography
- **Region maps:** `sevii45_region_map@4x.png` and `sevii67_region_map@4x.png`.
- **Overview:** `overview.png` shows both region maps beside every map at 1/8 scale. Maps are placed by FRLG connection offsets, and the routes by their own offsets. The Six Island group is drawn 24 tiles further east so it doesn't cover Sevault Canyon.

| Cluster | FRLG edge chain (kept exactly) | Added |
|---|---|---|
| 4–5 | Five Island → right Five Isle Meadow (0) → right Memorial Pillar (+20). Four Island has no edges. | **Sevii Sea Route C** (40x22): Four Island bottom (Four x12-19, offset −10) runs down then east to Five Island's west sea (rows 6-13, offset +6). It has an islet with an item. |
| 6–7 | Six Island → right Water Path (−40) → left Ruin Valley (+80); Seven Island → down Sevault Canyon Entrance (0) → right Sevault Canyon (+20) → down Tanoby Ruins (−48) | **Sevii Sea Route D** (40x10): Seven Island's east sea (rows 8-13, offset −6) runs east to Six Island's south-west sea (rows 24-29, offset −22). |

- **The route check passes** (`sea_routes.check`). Every opening cell is passable sea on both sides, and every other edge cell is rock or has no neighbour.
- **Sea rocks cleared** for the openings:
  - Four Island: (12,37) and (17,37)
  - Five Island: (1,6), (2,9) and (0,14)
- **Connections dropped in the export:** FRLG connections to maps outside scope (Five Island ↑ Water Labyrinth, Seven Island ↑ Trainer Tower, Water Path ← Green Path) are dropped, because they would break the build. They are listed in each map.json's `_export_notes`.

## Tileset pairs
| Pair | Maps | Other layouts using the secondary |
|---|---|---|
| General + **SeviiIslands** (proposed; Rustboro copy + additions) | Four, Five, Meadow, Memorial Pillar, Six, Water Path, Ruin Valley, Seven, Sevault Canyon Entrance, Sevault Canyon, Sea Routes C/D, **and all batch-2 Sevii maps** | Sevii maps only (by design) |
| General + **TanobyDelta** (Tiksi, unchanged) | Tanoby Ruins | TANOBY_DELTA (Tiksi) |
| General + **Cave** | Icefall Cave Entrance, 1F, B1F, Back | 74 layouts, including Orchid's Frigo Cave, which has the same blue ice-room look |
| General + **BikeShop** | Rocket Warehouse interior | none in the working tree (vanilla New Mauville / Bike Shop are deleted) |

- **Connection-edge rule:** every connection joins two SeviiIslands maps, except **Sevault Canyon ↔ Tanoby Ruins**. On that one, all cells within 7 rows and 8 columns of the shared edge are General primary on both sides. Checked: 0 secondary cells.
- **Batch 2:** every edge (including Sea Routes A/B) is SeviiIslands ↔ SeviiIslands, and Mt. Ember (Lavaridge) is warp-only, so there are no violations.

## gTileset_SeviiIslands budget (`tileset/budget.txt`; real files in `out/export/tilesets/sevii_islands/`)
**Freed space:**
- Rustboro uses 498 of 512 tiles and 365 of 512 metatiles.
- The copy keeps only the metatiles that Route 104, the Southern Island exterior and the Faraway Island entrance use. The other 272 ids stay but are blanked.
- That frees **401 tile slots**. Tile 0 and Rustboro's animation destinations 128-159 / 448-451 are kept.
- `check_kept()` asserts that every Rustboro cell the Sevii specs use keeps its art.

| Addition | Tiles | Metatiles | Palette | Close-up |
|---|---|---|---|---|
| Cottage variants v1-v3: weathered thatch roof, door moved left / right, flower box | 2 | 11 | 6 (new) | `tileset/cottage_variants@4x.png` |
| Two Island market stall (4x4, counter MB_COUNTER) | 24 | 14 | 6 | `tileset/market_stall@4x.png` |
| Memorial Pillar Onix-tail mounds (FRLG port) | 36 | 10 | General 3 | `tileset/onix_tails@4x.png` |
| Memorial Pillar + its sand plaza (FRLG port) | 43 | 17 | General 5 + 7 (new: FRLG primary pal 5) | `tileset/memorial_pillar@4x.png` |
| Ruin Valley Dotted Hole entrance: pillars, dotted door, mound, pale path (FRLG port) | 33 | 28 | 3, 5, 7 | `tileset/ruin_valley_dotted_hole@4x.png` |
| Rocket Warehouse exterior (6x5, Cold Storage recoloured, red R) | 26 | 17 | 12 (new) | `tileset/rocket_warehouse@4x.png` |
| Arrow-warp duplicates: 9 (plank, grass, path, dirt-road cells) | 0 | 9 | — | — |
| **Total** | **164** (237 free left) | **106** (471/512, 41 left) | 6, 7, 12 filled; 8-11 stay Rustboro's | |

The Tanoby port (41 tiles, 28 metatiles) was dropped after the user's decision; `PORT_TANOBY = False` in `sevii_art_pieces.py`.

## Per map (all FRLG size)
| Map | Size | Buildings: stamp (door = FRLG warp) | Other |
|---|---|---|---|
| Four Island | 48x40 | Centre (18,20); Mart (22,26); Day-Care = red-roof house (12,13); house1 cottage_v3 (25,14); Lorelei's house = Pretty Petal building (33,23); house2 cottage (25,26); harbour dock (10,28) | Icefall Cave mouth (38,12) across the L-shaped pond (Surf); breakable rock (5,11); harbour arrow S |
| Five Island | 24x20 | Centre (18,6); houses (12,6), (22,9); harbour dock (12,14) | arrow S |
| Five Isle Meadow | 24x40 | **Rocket Warehouse** (12,21) | Rocket Warehouse interior: `five_island_rocket_warehouse*` (30x28, New Mauville tiles) |
| Memorial Pillar | 24x60 | — | the pillar and the two Onix-tail mounds are **ported FRLG art**; 7 grey boulders 0x0E0; 3x crop in `_vs_frlg` |
| Six Island | 24x30 | Centre (11,11); Mart (20,11); house cottage_v3 (16,17); harbour dock (11,23) | arrow S |
| Water Path | 24x100 | cottage_v2 (5,13); cottage_v3 (11,19) | its pale-path strip (FRLG 0x0C4-0x0CF) is plain grass here (ported only in Ruin Valley) |
| Ruin Valley | 48x40 | — | Dotted Hole entrance **ported** (x22-26, y20-25), door warp (24,24); 9 brown boulders 0x0E1 |
| Seven Island | 24x20 | Centre (12,3); Mart (5,9); house cottage (11,9); harbour dock (16,13) | arrow S |
| Sevault Canyon Entrance | 24x40 | — | — |
| Sevault Canyon | 24x80 | house cottage_v3 (14,61) | Tanoby Key cave (7,17); 6 breakable rocks |
| Tanoby Ruins | 144x20 | 7 chambers = Tanoby Delta's 5x5 facade + mound chunk, door on FRLG's warp | 3 sand boulders 0x0E2 |
| Sea Route C / D | 40x22 / 40x10 | — | swimmers; item on Route C's islet |

**Icefall Cave** (`four_island_icefall_cave_*`, General + Cave, by icefall_translate.py):
- **Rooms:** Entrance 30x36, 1F 20x20, B1F 24x20, Back 25x26.
- **Walk check:** the reachable cells match FRLG exactly from every entry, with 0 stuck states.
- **Ice check:** `ice_puzzle`-style. B1F's ice field passes: 2 inputs in, 4 out, 0 stuck.
- **Whole cave:** 613 states, none of which can't get back out.

**Interiors** (`out/interiors/`, by frlg_interiors.py):
- 7 harbours are clones of the existing LAYOUT_ISLAND_HARBOR.
- Houses are on Building + GenericBuilding; the Day-Care is on PokemonDayCare.
- Ember Spa, Summit Path and Ruby Path are on General + Lavaridge.
- Dunsparce Tunnel, Tanoby Key and all 7 Tanoby chambers are on General + Cave.
- Dotted Hole 1F-B4F and the Sapphire Room are on General + NavelRock.

## Boulders vs breakable rocks (batch 3)
| Map | Fixed boulders | Breakable rocks |
|---|---|---|
| Memorial Pillar | 0x0E0 at (5,40) (12,40) (4,43) (7,44) (15,44) (3,47) (8,48) | — |
| Ruin Valley | 0x0E1 at (17,11) (33,11) (14,12) (34,14) (31,16) (34,18) (33,20) (31,22) (35,22) | — |
| Tanoby Ruins | 0x0E2 at (32,4) (43,6) (106,7) | — |
| Four Island | — | (5,11) |
| Sevault Canyon | — | (3,41) (7,44) (12,47) (15,46) (16,47) (11,31) |

## Two Island market stall: proposed stock (rare items, high prices)
All constants exist in include/constants/items.h.
- **Vanilla prices:** I_PRICE is GEN_LATEST, so these are Gen 9 prices.
- **Stall prices:** a Mart sells at the item's own `.price`, so the stall prices need a per-shop markup. See question 2.

| Item | Vanilla | Stall |
|---|---|---|
| ITEM_ABILITY_CAPSULE | 100,000 | 150,000 |
| ITEM_ABILITY_PATCH | 250,000 | 250,000 |
| ITEM_BOTTLE_CAP / ITEM_GOLD_BOTTLE_CAP | 20,000 / 60,000 | 40,000 / 120,000 |
| ITEM_PP_MAX | 10,000 | 30,000 |
| ITEM_RARE_CANDY | 10,000 | 25,000 |
| ITEM_EXP_CANDY_XL | 10,000 | 20,000 |
| ITEM_LUCKY_EGG | 10,000 | 50,000 |
| ITEM_DESTINY_KNOT | 20,000 | 40,000 |
| ITEM_ADAMANT_MINT / ITEM_TIMID_MINT (+ other mints) | 20,000 | 30,000 |
| ITEM_LINKING_CORD | 8,000 | 20,000 |
| ITEM_DUSK_STONE / SHINY_STONE / DAWN_STONE / ICE_STONE | 3,000 | 10,000 |
| ITEM_RAZOR_CLAW / ITEM_RAZOR_FANG | 15,000 | 25,000 |
| ITEM_KINGS_ROCK / ITEM_METAL_COAT / ITEM_PRISM_SCALE | 10,000 / 3,000 / 3,000 | 20,000 / 12,000 / 15,000 |
| ITEM_PROTECTOR / ELECTIRIZER / MAGMARIZER / REAPER_CLOTH / DUBIOUS_DISC / UPGRADE / DRAGON_SCALE | treasure price | 20,000 |

## Implementation: real map data (`frlg_translate.py export`)
**Command:** `<venv python> dev_scripts/voyages/frlg_translate.py export [--out DIR]` (code in `export_maps.py`; default `out/export/`). It re-runs every builder (batch 2, batch 3, routes, Icefall, interiors, Rocket Warehouse) and writes the following.

**Layouts:**
- **Files:** `layouts/<Folder>/map.bin` + `border.bin`, holding the raw u16 blocks (metatile | collision << 10 | elevation << 12) exactly as rendered.
- **Entries:** `layouts.json`, with entries for those layouts (66). FRLG layout ids are reused; new ones are LAYOUT_SEVII_SEA_ROUTE_A-D and LAYOUT_FIVE_ISLAND_ROCKET_WAREHOUSE.

**Maps:** `maps/<Map>/map.json` (86 maps). Each is FRLG's map.json with these changes:
- FRLG-only graphics are swapped. Pokémon become `OBJ_EVENT_GFX_SPECIES(X)`, Rocket becomes Aqua (placeholder), Cooltrainers become MAN_4 / WOMAN_5, and BREAKABLE_ROCK_FRLG becomes BREAKABLE_ROCK.
- Moved objects are applied: the stall clerk goes to (28,3), and the harbour sailor and boat go to (8,5) and (8,7).
- Sea-route connections are added in both directions.
- Connections to unbuilt maps are dropped.
- `_export_notes` lists what still needs hands. The one FRLG-only sprite left is BLUE in one map.

**Tileset:** `tilesets/sevii_islands/` holds the proposed gTileset_SeviiIslands as real files:
- tiles.png (Rustboro plus the new tiles in the freed slots)
- palettes 00-15
- metatiles.bin and metatile_attributes.bin
- labels.json

Export this **after** the maps, because the arrow duplicates are added while the maps build; the command does that.

**Manifest:** `manifest.json` gives each map's kind, layout, pair and notes.

**Still to do by hand when building:**
- headers and graphics.h / metatiles.h entries for gTileset_SeviiIslands, plus Rustboro's tile animations for the copy
- the Rocket Warehouse door animation (src/field_door.c, palette 12)
- map_groups.json entries
- the new region-map sections MAPSEC_SEVII_SEA_ROUTE_A-D
- the reverse connections in islands that already exist
- scripts: FRLG script labels are kept as placeholders
- the second exit-mat warp in houses (noted per map)
- item flags for the route items (reuse unreachable vanilla flags)
- Centre / Mart / Game Corner clones

## Known seams
- **Outdoor:** the same kinds as batch 2 (massif piece pairs, trees against rock). They read fine at mockup scale.
- **Tanoby Ruins:** the chunk's top rock row meets the sea with no sand between them, as in Tanoby Delta.
- **Icefall Cave:** water against floor, boulders on plain floor, ladder pieces in rock faces.
- **Interiors:** listed per room in `out/interiors/NOTES.md`.

## Open questions (recommendation first)
1. **Extra dungeon interiors.** The interiors pass translated everything FRLG links from these maps, including the full Ruby Path (8 floors), Dotted Hole B1F-B4F plus the Sapphire Room, and all 7 Tanoby chambers.
   - **Recommendation:** keep Ruby Path 1F only, with its deeper floors sealed (no Ruby / Sapphire quest in scope).
   - Also keep Dotted Hole 1F only, with the door sealed (a "sealed" sign), and keep 2 Tanoby chambers (Monean + Viapois), closing the others.
   - Or keep all of it as optional post-game dungeons. They cost nothing in tilesets, just map slots.
2. **Stall prices.** A Mart can't price per shop.
   - **Recommendation:** a small engine change, a "price multiplier" var read by the shop (e.g. ×2 at the stall) so the item table stays vanilla.
   - Alternatively, sell through a scripted menu.
3. **Rocket team.** Rocket objects are exported as Team Aqua sprites. The Icefall mockup uses Aqua and the Rocket Warehouse mockup uses Magma.
   - **Recommendation:** pick Orchid's Sevii villain team once, then swap in one pass (EXPORT_SWAP in export_maps.py).
4. **Water Path's pale path** (FRLG mint path tiles) is plain grass here. Ruin Valley uses the ported mint path.
   - **Recommendation:** port it on Water Path too. The cells are already in the tileset, so it costs no tiles.
5. **Tanoby chamber facade.** The big Monean chamber in FRLG sits on a stepped plateau and uses a second facade bottom (33C-33E). The translation uses Tanoby Delta's single facade for all 7. Accept.
6. **Out-of-scope neighbours** (Water Labyrinth / Resort Gorgeous, Green Path / Outcast Island / Pattern Bush / Altering Cave, Trainer Tower, Lost Cave).
   - **Recommendation:** later batch.
   - Until then, the FRLG connections are dropped and those edges are closed by the existing FRLG rock / sea.
7. **Lorelei's house** got the Pretty Petal building, chosen for its 7-wide footprint.
   - **Recommendation:** accept, or give it a cottage variant for a homelier look.
8. **Proposed gTileset_SeviiIslands.** Approve creating it: a copy of Rustboro with 272 city-only metatiles blanked and the additions above, with 41 metatiles left.
   - Its tile animations, the Rocket door animation and palette slots 6/7/12 are the only engine-side work.

## Pre-decision record (kept)
`icefall_ice_compare.png` (Cold Storage vs Shoal look; the user chose Shoal) and `four_island_metatile_probe.*` (the translation-feasibility probe).
