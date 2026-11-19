# Region maps + end-to-end check: done (2026-11-19)

Worktree `pokeorchid-voyages` (branch `voyages`). Nothing is committed. The final normal `make -j8` is clean: only the
pre-existing `heal_location.c` unused-function warning, and `grep -c gHarnessKeys pokeemerald.map` = 0.

## Part 1: region maps (regionmap/IMPLEMENTATION.md + the user's decisions)
- **Exporter:** `dev_scripts/voyages/export_region_maps.py` (Pillow venv). It is idempotent and writes:
  - Eon art: `map_eon.*`, the dense intro clouds over vanilla Hoenn, 125 tiles.
  - The shared placeholder sheet `map_voyage_placeholder.*` (123 tiles) and `map_{holon,newmoon,fullmoon}.bin`.
  - Dex AREA tilemaps `graphics/pokedex/region_map_{eon,holon,newmoon,fullmoon}.bin`. These reuse the BG tiles and palette.
  - FRLG's switch-map button erased from the Sevii region-map and Dex tilemaps.
  - The cursor grids: the Sevii grids are rebuilt from vanilla in git HEAD, plus `region_map_layout_voyages.h`.
  - `orchid_map_v2_voyages.h`, holding the nodes, the blue strait tubes and the strait cursor cell lists.
  - `orchid_frame_voyages.png`: Tosa's frame sheet plus 2 new tube end-cap shapes.
  - The voyage-block x/y/w/h in `region_map_sections.json`.
    - Interiors with no cell of their own borrow their parent's bbox: Icefall → Four Island, Ember Spa → Kindle Road, Rocket Warehouse → Meadow, Dotted Hole → Ruin Valley, Tanoby Key/chambers → Tanoby Ruins.
- **include/region_map.h:**
  - Adds `REGION_MAP_EON/HOLON/NEWMOON/FULLMOON` and `REGION_MAP_COUNT`.
  - Adds `IsVoyageRegionMapType()`, `GetRegionMapSubAreaName()` and `IsSeviiMapSec()`.
- **src/region_map.c:**
  - `GetVoyageRegionMapType()` is a switch over the voyage sections, checked first in `GetRegionMapType`. Region stays `REGION_TOSA`.
  - New `gRegionMapInfos` entries, guarded by a STATIC_ASSERT that every type has one.
  - New `GetMapSecIdAt` cases.
  - Header names: "SEVII ISLANDS", "EON ISLAND", "HOLON", "NEWMOON ISLAND", "FULLMOON ISLAND".
  - The sub-label "ISLES 1-3", "ISLES 4-5" or "ISLES 6-7" is drawn right-aligned in the narrow font.
  - Per-type fallback sections: One / Four / Seven Island, Eon, Mirage Forest, Newmoon, Fullmoon.
  - Strait cursor special case: progress along the sea-route map indexes the cell list, so the L-shaped straits work.
  - Eon Island is always `MAPSECTYPE_ROUTE`.
  - MAP v2 table entries for all 7 voyage types. Eon has no node.
- **Fly:** Sevii uses the `FLAG_WORLD_MAP_*_ISLAND` aliases, i.e. the Sevii stream's visited flags. The cursor only moves on the current cluster's grid, so you can Fly only within a cluster.
- **Fix:** `sMapHealLocations` rows for the six renamed slots pointed at FRLG maps. They now point at Holon Village (heal location), Mirage Forest, Research Tower, Holon Lake, Newmoon and Fullmoon.
- **Fix:** Holon Village turns gold or becomes flyable once `FLAG_VISITED_HOLON_VILLAGE` is set.
- **field_region_map.c:** in a voyage, R does not switch regions and no hint is shown. The sub-label is printed.
- **FLAG_VISITED_TIKSI:** `IsTiksiMapSec` already excluded the voyage sections (core stream).
- **Exporter guards:**
  - Tiksi: `kanto_block` already stops at ONE_ISLAND.
  - Tosa `export_region_map.py`: `VOYAGE_KEEP = {MAPSEC_EON_ISLAND}`.
  - Tagger: `kantoEnd` = ONE_ISLAND − 1, and voyage sections are hidden in both modes. Verified by reading the code only; the exporters were not re-run.
- **Dex AREA:** `pokedex_area_screen.c` gets a `default:` case for custom map groups. Caves and indoor maps get a marker; everything else gets the glow. This also fixes Tosa Rail, Overworld and Tiksi. It is build-verified only and was not checked on screen.
- **Sevii battle music:** see "Sevii music" below.

## Part 2: headless run (scripts run1-4 in this folder, logs run*.log, screenshots in shots/)
The harness is `hbuild.sh`. It sets debug flags 0x29D (no sight), 0x29E (no wild) and 0x29F (no collision), builds from a copy of the engine-dev save, and restores the config files afterwards.

What I saw on screen:
- **Codes:** all 5 work, including in lower case.
- **Voyages:** every destination and back worked: Eon, Sevii (home via One Island's "Wavebreak & beyond"), Holon (Mirage Forest jetty), Newmoon and Fullmoon.
- **Sevii maps:**
  - The FRLG art shows with the cursor, nodes, blue/grey strait tubes and the sub-labels.
  - The cursor follows One-Two, Four-Five (L-shape: Five end and the corner) and Six-Seven.
- **Other maps:** Eon shows the clouds with the head over Southern Island. Holon, Newmoon and Fullmoon show their placeholders.
- **R switch:** the hint shows on Tosa and is absent on the voyage maps.
- **FLAG_VISITED_TIKSI:** stays 0 after every voyage.
- **Holon:**
  - Researcher Ido leads with δ species 1594, and the trainer intro reads "Holon Researcher".
  - I walked coast → village → lake. A wild Persian-δ / Raichu-δ appeared; non-Deltas also occur, as in the tables.
  - Cynthia: the encounter song 563 played, then vs song 564 against Spiritomb.
  - After the win, `FLAG_CYNTHIA_BEATEN_AT_LAKE` is set and she is gone. The sphere's palette changed from plain to glow (screenshots 35b and 40b).
  - The Changu Battle Café shows her (hide flag clear).

Test-only shortcuts:
- Lead party level poked to 100 (no exp prompts).
- Wins forced by setting the foe to 1 HP.
- Debug warps for the Sevii islands.
- Old save: Dex flags are misread after the Delta change (expected).

## Sevii music
- **In the repo:** all 75 FRLG songs, each on its own FRLG voicegroup (`sound/voicegroups/rg_*.inc`, `midi.cfg -G_rg_*`). Sevii maps already use them:

  | Song | Voicegroup |
  |---|---|
  | MUS_RG_SEVII_123 | `_rg_pewter` |
  | MUS_RG_SEVII_45 | `_rg_sevii_45` |
  | MUS_RG_SEVII_67 | `_rg_sevii_67` |
  | MUS_RG_SEVII_ROUTE | `_rg_sevii_route` |
  | MUS_RG_SEVII_CAVE (Mt. Ember / caves) | `_rg_mt_moon` |
  | MUS_RG_SEVII_DUNGEON | `_rg_viridian_forest` |
  | MUS_RG_NET_CENTER | `_rg_poke_center` |

  Also present: MUS_RG_ROUTE3 / FUCHSIA / VIRIDIAN_FOREST / ROCKET_HIDEOUT / GAME_CORNER, the battle songs MUS_RG_VS_WILD / VS_TRAINER / VS_GYM_LEADER, MUS_RG_VICTORY_WILD / VICTORY_TRAINER, and MUS_RG_ENCOUNTER_*.
- **Implemented:** `GetBattleBGM` routes Sevii trainer battles to Emerald's MUS_VS_TRAINER (Sevii has no trainers yet). Wild battles keep MUS_VS_WILD. This is the "closest Emerald track" fallback. I did not use REGION_KANTO, because that also changes evolution, daycare and region checks.
- **Left:** re-voicing FRLG vs_wild, vs_trainer, the victory songs and the encounters onto Hoenn voicegroups.
  - Each song needs every program remapped from its rg_* voicegroup to a Hoenn voicegroup (new `-G` plus program remap), then a listening pass by the user.
  - About 6-8 songs at roughly 1-2 h each; the map songs too if wanted, about 6 more.
  - Then point GetBattleBGM's Sevii branch at the new song ids.
