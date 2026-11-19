# Holon stream: done

Worktree `pokeorchid-voy-holon` (detached from `voyages` bc3f480c7c). Nothing is committed. A clean `make` succeeds, and `grep gHarnessKeys pokeemerald.map` returns nothing.

Everything under data/ is regenerated from the approved batch-4 specs by `install_holon.py`, which needs the Pillow venv. The C wiring was done by hand; it is listed below.

## Arrival hook for core (`src/voyages.c`, HOLON entry)

- **Map:** `MAP_HOLON_MIRAGE_FOREST`.
- **Arrival point:** x 5, y 36. This is on the wooden jetty, facing left toward the Sailor.
  - Use `warp MAP_HOLON_MIRAGE_FOREST, 5, 36`. There is no warp event on the jetty.
- **Dock objects:**
  - Sailor `LOCALID_HOLON_SAILOR` at (3,36), elevation 4.
  - Boat `LOCALID_HOLON_BOAT` (`OBJ_EVENT_GFX_MR_BRINEYS_BOAT`) at (1,36).
- **Sailor script:** `HolonMirageForest_EventScript_Sailor` calls `Holon_SailorReturnPlaceholder`, which only shows a message. Swap it for core's common dock script after merging.

## What changed

### Tilesets

- **gTileset_Holon**, in `data/tilesets/secondary/holon/`.
  - It is the approved "full greens" draft, byte-identical to `out/batch4/gTileset_HolonDesat`.
  - It has 512 tiles (`-num_tiles 512`), 367 metatiles, palette 06 for the blue-grey rock and palette 07 for drained foliage.
  - It uses Fortree's anim callback, which is a no-op.
- **gTileset_General_Holon** is a struct in `headers.h` that uses General's tiles, metatiles and attributes and General's animation.
  - Only its palette array is new: `data/tilesets/primary/general_holon/palettes`, with the greens desaturated in 00-05.
  - `field_door.c` `GetDoorGraphics` treats it as General, so the Centre and Mart doors animate.
- Fortree, General and their palettes are untouched.

### Field-effect hook (`src/holon.c`, `include/holon.h`)

- On maps whose primary tileset is General_Holon, `FLDEFF_PAL_TAG_GENERAL_0` and `_1` load desaturated copies: `graphics/field_effects/palettes/general_{0,1}_holon.pal`.
- The hook is in `field_effect.c`, in the three palette loaders, and in `wild_encounter_ow.c` (the OW spawn animation).

### Sphere object

- New object graphic `OBJ_EVENT_GFX_HOLON_SPHERE`, 32x32. It has its own palette tag, `OBJ_EVENT_PAL_TAG_HOLON_SPHERE` (0x113A).
- The glow is a palette swap in two places:
  - `LoadObjectEventPalette` loads the glow palette whenever `HOLON_SPHERE_GLOW_FLAG` is set.
  - `callnative Holon_SetSphereGlow` updates it straight away.
- `Holon_EventScript_AwakenSphere` sets the flag and swaps the palette.

### Maps, in `gMapGroup_Holon` (appended last)

| Map | Notes |
|---|---|
| HolonMirageForest | 44x48 |
| HolonVillage | 72x72 |
| `_PokemonCenter_1F`, `_Mart` | Tosa clones |
| `_House1`..`_House7` | vanilla house layouts |
| `_RuinsHouse` | |
| HolonResearchTower_1F | WI 1F layout as-is |
| HolonResearchTower_2F | its own layout, with lab machines |
| HolonLake | 72x52 |

- **Connections:** coast ↔ village (∓12), village ↔ lake (0).
- **Heal location:** `HEAL_LOCATION_HOLON_VILLAGE`.
- **Signs and NPCs:** every NPC has a line, including the four "drained flora" lines.
- **Berry trees:** 9 trees, planted once on transition.
  - They reuse the ids of the deleted Route 102/104 trees. **Check this against Sevii.**
- **Gifts and statics:**
  - The Eevee gift is at Tower 2F, given by the head of research.
  - The shiny Gyarados static is on the lake at (40,44). It needs Surf, and it is forced shiny with `createmon … shinyMode`.

### Bridges

- Route 119's planks are drawn over sprites, so walkers have to be at elevation 4.
- Bridges with end posts: the posts are at 4, with a transition cell at 0 outside each one.
- Bridges without posts: the planks are at 4, so you can't surf under them.
- The coast jetty is a post-less bridge, so its planks are at 4 and the Sailor stands at elevation 4.

### MAPSECs

| Old section | New section |
|---|---|
| RESORT_GORGEOUS | MAPSEC_HOLON_VILLAGE |
| WATER_LABYRINTH | MAPSEC_MIRAGE_FOREST |
| OUTCAST_ISLAND | MAPSEC_RESEARCH_TOWER |
| GREEN_PATH | MAPSEC_HOLON_LAKE |

- Names are in title case, and the old ids are aliased.
- `overworld.c` is not touched, as the coordinator asked.

### Flags

| Flag | Id |
|---|---|
| `FLAG_VISITED_HOLON_VILLAGE` | 0x280 |
| `FLAG_VISITED_HOLON_LAKE` | 0x281 |
| `FLAG_HOLON_BERRIES_PLANTED` | 0x282 |
| `FLAG_HOLON_RECEIVED_EEVEE` | 0x283 |
| `FLAG_HOLON_HIDE_GYARADOS` | 0x284 |
| `FLAG_HOLON_SPHERE_GLOW` | 0x285 |

- Item flag 0x492 is renamed `FLAG_ITEM_HOLON_RUINS_HOUSE_STAR_PIECE`. Its old name, `SAFARI_ZONE_SOUTH_EAST_BIG_PEARL`, is aliased; the Safari Zone can't be reached.
- `VAR_UNUSED_0x409D` is not used.

### Wild encounters

- Holon tables are in `wild_encounters.json` with base species, in day and `_Night` variants.
- The intended Delta tables are in `wild_delta.json`.

## Placeholders

`swap_placeholders.py` rewrites the placeholders to the real names. Run it from the repo root; `--dry-run` previews the changes.

| Placeholder | Real name |
|---|---|
| Researcher OW `OBJ_EVENT_GFX_SCIENTIST_1` (trainer objects) | `OBJ_EVENT_GFX_HOLON_RESEARCHER` |
| `TODO_TRAINER_HOLON_RESEARCHER_1..6` (`include/constants/holon.h`, aliased to Space Center / Weather Inst. grunts) | IDO, CHRISTOPHE (coast 21,9 / 34,22); MATEO, HENRIK (lake 8,36 / 40,13); TOBIAS, KENJI (tower 2F 18,6 / 11,9). **Check this order against the trainers stream's levels.** |
| Cynthia: `OBJ_EVENT_GFX_WOMAN_2`, `call Holon_CynthiaPlaceholder`, flag 0 | `OBJ_EVENT_GFX_CYNTHIA`, `Common_EventScript_CynthiaHolonLake`, `FLAG_CYNTHIA_BEATEN_AT_LAKE` |
| `HOLON_SPHERE_GLOW_FLAG` = `FLAG_HOLON_SPHERE_GLOW` | `FLAG_CYNTHIA_BEATEN_AT_LAKE`, so the sphere glows once she's beaten |
| `SPECIES_EEVEE` (gift) | `SPECIES_EEVEE_DELTA` |
| `SPECIES_GYARADOS` and its OW (static) | `SPECIES_GYARADOS_DELTA` |
| Wild tables | the entries in `wild_delta.json` |
| Sailor dock script | core's common dock script (manual, not in the swap script) |

## Verification

- `check_holon.py`:
  - map sizes are OK
  - all warps are symmetric
  - all connections are symmetric
  - the flood-fill reaches every warp, NPC and sign on foot
  - only the boat, the lake island (sphere and pillars) and the Gyarados need Surf
- Headless run, under the lock, with harness-only debug flags 0x29D-0x29F for no encounters, no trainer sight and no collision. The log is `shots/headless_log.txt`, and there are 21 shots.
  - **Debug warps:** Centre door, Tower 1F, Tower 2F, Ruins house, House1 and Mart all land correctly.
  - **Centre heal:** HP 1 → 126/126.
  - **Walk:** village → coast → long grass → jetty → village → lake, all crossing the connections.
  - **Grass field-effect palette:** the GENERAL_1 palette that loads matches the Holon copy, not the vivid one.
  - **Sphere glow:** the OBJ palette is the glow palette after the flag is set.
  - **Eevee gift:** the flag is set.
- The harness scripts are in `headless/`.

## Known gaps

- The Tower land table (`gHolonResearchTower_1F`) can never trigger, because the Weather Institute floors have no encounter tiles.
- The Lake rock-smash table has no smash rocks placed.
- The 1F and 2F lab layouts are shared with vanilla `Route119_WeatherInstitute_*`; 1F is used as-is.
- The region-map cells, the Fly/visited state and `IsVoyageMapSec` belong to other streams.
