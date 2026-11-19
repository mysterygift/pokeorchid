# Voyage region maps: implementation note (batch 6)

This is a plan only. No file under data/, src/, include/ or graphics/ has been changed. Mocks are in `../out/batch6_regionmap/` (see NOTES.md there). Line numbers are from `voyages` at df3fd8da67 and will drift.

Scripts in this folder (Pillow venv):
- `rm_common.py`: BG2 decoder, vanilla Hoenn art read from git `fead488d62^`, and the MAP v2 screen composer.
- `eon_clouds.py`: the Eon map. It writes `out/batch6_regionmap/eon_rom_preview/eon_dense.{png,bin,pal}` (chosen), i.e. what the exporter would ship.
- `sevii.py`: the proposed Sevii grids (the `CLUSTERS` dict), the switch-button erase, and the mocks. Its output is `sevii_grid.json`.
- `placeholders.py`: the Holon / Newmoon / Fullmoon placeholders.

When this is built, turn these into one exporter, `dev_scripts/voyages/export_region_maps.py`. It should write:
- the graphics
- the four new layout headers plus the three rewritten Sevii layouts
- the `orchid_map_v2_voyages.h` nodes and tubes
- the section JSON entries for the voyage block

## 0. What exists today (survey)

| Piece | Where | State for voyages |
|---|---|---|
| `enum RegionMapType` | include/region_map.h:9 | HOENN (= Tosa), KANTO, SEVII123/45/67, TIKSI |
| `gRegionMapInfos[]` | src/region_map.c:364 | Sevii entries exist with FRLG art: `map_sevii_*.png/.bin/.pal` plus dex copies in graphics/pokedex |
| `sRegionMapSections_Sevii*` | src/data/region_map/region_map_layout_sevii*.h | Vanilla FRLG grids, still compiled |
| `GetRegionMapType` | region_map.c:1206 | Switches on `GetRegionForSectionId`, and that function sends the **whole** Kanto+Sevii block to `REGION_TIKSI` (include/regions.h:14 `IsTiksiMapSec` = `[KANTO_MAPSEC_START, MAPSEC_SPECIAL_AREA)`). The Sevii branch is unreachable. |
| `FLAG_VISITED_TIKSI` | src/overworld.c:676 | Set on entering any `IsTiksiMapSec` section. A Sevii map would set it today. |
| Viewed-region override | region_map.c:753-778 | `sViewedRegionMapType`. The phone MAP's R key flips HOENN ⇄ TIKSI (field_region_map.c:185) when `CanSwitchRegionFromMap()` (:241): phone caller and `FLAG_VISITED_TIKSI`. |
| `GetRegionMapRegionName` | region_map.c:1259 | "TIKSI" or else "TOSA". Used in the MAP header (field_region_map.c:272) and the Rotom greeting (rotom_phone.c:627). |
| `GetRegionMapFallbackMapSec` | region_map.c:1267 | FURONG_VILLAGE or TOSA_PORT. Used when the section has width/height 0 or another region is being viewed. |
| MAP v2 `sOrchidRegionMapsV2` | region_map.c:2611 | Only HOENN and TIKSI. **`GetOrchidRegionMapV2()` falls back to the Tosa nodes and tubes for any other type**, so Tosa's discs would be drawn over the Sevii art. `ORCHID_MAP_MAX_NODES` (:89) only knows the two arrays. |
| Visited state (MAP v2) | `OrchidMapPlaceVisited` :2636 | `GetMapsecType == MAPSECTYPE_CITY_CANFLY`. The Sevii cases (:1556-1569) test `FLAG_WORLD_MAP_*_ISLAND`, which **are `0` in Emerald** (include/constants/flags.h:2394+), so the places always show grey. |
| Fly | `sFlyLocations` :2195, `sMapHealLocations` :437 | The Sevii rows exist with FRLG `MAP_*` / `HEAL_LOCATION_*_ISLAND` ids and 0 flags. Only the current `regionMapType` is shown. |
| `region_map_sections.json` | src/data/region_map | Sevii entries have **no x/y and width 0**: the Tiksi exporter zeroes the whole block. `MAPSEC_SOUTHERN_ISLAND` is also width 0: the Tosa exporter zeroes untagged Hoenn sections. |
| Tiksi exporter | dev_scripts/orchid_ui/export_region_map_tiksi.py:85 `kanto_block` = `[PALLET, SPECIAL_AREA)`; `update_sections` :144-158 | Free-slot allocator over the whole block. It also pops x/y on every block entry. |
| Tosa exporter | export_region_map.py:201 `update_sections` | Leaves the Kanto block alone. Zeroes any untagged Hoenn entry, Southern Island included. |
| Tagger | dev_scripts/region_map_tagger/index.html:182-186 | `kanto` = `[kantoStartId, MAPSEC_SPECIAL_AREA]` |
| Popups | src/map_name_popup.c:692 | `OW_POPUP_GENERATION == GEN_5` (config/overworld.h:118). Kanto-range ids map to theme 0 = `MAPPOPUP_THEME_BW_DEFAULT`, which is the theme every section uses. The text is `gRegionMapEntries[].name`. **Nothing to change** apart from the names. |
| Dex AREA | pokedex_area_screen.c:334-357, pokedex_area_region_map.c:15 | Draws `gRegionMapInfos[GetRegionMapType(current)].dexMap*`. It counts only encounters whose section has the same region-map type. The group `switch` at :343 handles only `MAP_GROUP_TOWNS_AND_ROUTES(_FRLG)`, `DUNGEONS(_FRLG)` and `SPECIAL_AREA(_FRLG)`; **maps in any other group are skipped**. |

## 1. Section block split

```
0x58 MAPSEC_PALLET_TOWN (renamed REGOLIS_SHRINE) ... 0x8E MAPSEC_POWER_PLANT   = Tiksi   (55 ids; 20 used, 35 free)
0x8F MAPSEC_ONE_ISLAND ............................. 0xBF MAPSEC_EMBER_SPA     = Voyages (49 ids)
0xC0 MAPSEC_SPECIAL_AREA
```

- **include/regions.h**
  - Add `#define VOYAGE_MAPSEC_START MAPSEC_ONE_ISLAND` and `#define VOYAGE_MAPSEC_END MAPSEC_SPECIAL_AREA` (exclusive).
  - `IsTiksiMapSec`: `id >= KANTO_MAPSEC_START && id < VOYAGE_MAPSEC_START`. This alone fixes (d): `FLAG_VISITED_TIKSI` (overworld.c:676) is no longer set by voyage maps.
  - Add `IsVoyageMapSec(id)`: `id >= VOYAGE_MAPSEC_START && id < VOYAGE_MAPSEC_END`, or `id == MAPSEC_EON_ISLAND`.
- **constants**: `KANTO_MAPSEC_*` (region_map_sections.constants.json.txt:18-20) stay as they are; the popup code depends on them.

### Renames

Each rename keeps its enum slot. The old id goes into `region_map_section_aliases.h`, and names are title case like the rest of Orchid.

| Slot | New id | Name (≤16, `MAP_NAME_LENGTH`) | Region map |
|---|---|---|---|
| 0x49 SOUTHERN_ISLAND | `MAPSEC_EON_ISLAND` | Eon Island | EON |
| 0x8F-0x95 ONE…SIX_ISLAND | (keep ids) | One Island … Seven Island | SEVII123/45/67 |
| KINDLE_ROAD, TREASURE_BEACH, CAPE_BRINK, BOND_BRIDGE, THREE_ISLE_PORT, MT_EMBER, BERRY_FOREST | (keep) | Kindle Road, Treasure Beach, Cape Brink, Bond Bridge, Three Isle Port, Mt. Ember, Berry Forest | SEVII123 |
| FIVE_ISLE_MEADOW, MEMORIAL_PILLAR, ICEFALL_CAVE | (keep) | Five Isle Meadow, Memorial Pillar, Icefall Cave | SEVII45 |
| WATER_PATH, RUIN_VALLEY, CANYON_ENTRANCE, SEVAULT_CANYON, TANOBY_RUINS | (keep) | Water Path, Ruin Valley, Canyon Entrance, Sevault Canyon, Tanoby Ruins | SEVII67 |
| 0xA7 SEVII_ISLE_22 | `MAPSEC_ONE_TWO_STRAIT` | One-Two Strait | SEVII123 |
| 0xA8 SEVII_ISLE_23 | `MAPSEC_TWO_THREE_STRAIT` | Two-Three Strait | SEVII123 |
| 0xA9 SEVII_ISLE_24 | `MAPSEC_FOUR_FIVE_STRAIT` | Four-Five Strait | SEVII45 |
| 0xB5 THREE_ISLE_PATH | `MAPSEC_SIX_SEVEN_STRAIT` | Six-Seven Strait | SEVII67 |
| 0x9B RESORT_GORGEOUS | `MAPSEC_HOLON_VILLAGE` | Holon Village | HOLON |
| 0x9C WATER_LABYRINTH | `MAPSEC_MIRAGE_FOREST` | Mirage Forest | HOLON |
| 0x9F OUTCAST_ISLAND | `MAPSEC_RESEARCH_TOWER` | Research Tower | HOLON |
| 0xA0 GREEN_PATH | `MAPSEC_HOLON_LAKE` | Holon Lake | HOLON |
| 0xAA NAVEL_ROCK_FRLG | `MAPSEC_NEWMOON_ISLAND` | Newmoon Island | NEWMOON |
| 0xB7 BIRTH_ISLAND_FRLG | `MAPSEC_FULLMOON_ISLAND` | Fullmoon Island | FULLMOON |

"Holon Research Tower" is 20 characters, too long for `MAP_NAME_LENGTH`. Hence "Research Tower".

The renamed slots are referenced only by `sMapHealLocations`, `regions.c` and the FRLG layout headers, so the aliases keep everything compiling.

**Spare voyage slots after this (21):**
- ROCKET_WAREHOUSE, TRAINER_TOWER, TRAINER_TOWER_2, DOTTED_HOLE, LOST_CAVE, PATTERN_BUSH, ALTERING_CAVE_FRLG, TANOBY_CHAMBERS, TANOBY_KEY
- MONEAN / LIPTOO / WEEPTH / DILFORD / SCUFIB / RIXY / VIAPOIS_CHAMBER
- EMBER_SPA, plus the 0x61-0x64 / 0x70-0x8E Kanto ids, which are Tiksi's, not ours

Suggested uses: Ember Spa (Kindle Road's cave door), Dotted Hole, Tanoby Chambers, extra Holon areas, and more straits.

## 2. Region and region-map type for each voyage section (regions.c)

Replace `sKantoSubregionMapsecs` with one table. It is the single source of truth, and the exporter writes it:

```c
struct VoyageMapSec { mapsec_u8_t mapsec; u8 region; u8 regionMapType; };
static const struct VoyageMapSec sVoyageMapSecs[] = {
    { MAPSEC_EON_ISLAND,      REGION_TOSA,  REGION_MAP_EON },
    { MAPSEC_ONE_ISLAND,      REGION_KANTO, REGION_MAP_SEVII123 },   // see Q5 (KANTO = FRLG battle music)
    ...
    { MAPSEC_HOLON_VILLAGE,   REGION_TOSA,  REGION_MAP_HOLON },
    { MAPSEC_NEWMOON_ISLAND,  REGION_TOSA,  REGION_MAP_NEWMOON },
    { MAPSEC_FULLMOON_ISLAND, REGION_TOSA,  REGION_MAP_FULLMOON },
};
const struct VoyageMapSec *GetVoyageMapSec(u32 mapSecId);   // NULL if not a voyage section
```

- **`GetRegionForSectionId`** (regions.h):
  - If `IsVoyageMapSec` and the table has the section, return `.region`.
  - Otherwise, a section in the voyage block that is not in the table returns `REGION_TOSA`.
  - Then the Tiksi test, then Tosa.
- **`GetKantoSubregion`**: drop it, or keep it as a wrapper over the table. Its only caller is `GetRegionMapType`.

## 3. include/region_map.h

```c
enum RegionMapType {
    REGION_MAP_HOENN, REGION_MAP_KANTO, REGION_MAP_SEVII123, REGION_MAP_SEVII45, REGION_MAP_SEVII67,
    REGION_MAP_TIKSI,
    REGION_MAP_EON, REGION_MAP_HOLON, REGION_MAP_NEWMOON, REGION_MAP_FULLMOON,   // Orchid voyages
    REGION_MAP_COUNT
};
static inline bool32 IsVoyageRegionMapType(enum RegionMapType t)
{ return t >= REGION_MAP_SEVII123 && t != REGION_MAP_TIKSI; }   // SEVII*, EON, HOLON, NEWMOON, FULLMOON
```

`sViewedRegionMapType` stores type + 1 in a u8, which is still fine.

## 4. src/region_map.c

1. **`GetRegionMapType`** (:1206): check the voyage table first, so that Holon's slots (they are in the old Sevii block) never reach the Kanto path:
   ```c
   const struct VoyageMapSec *v = GetVoyageMapSec(mapSecId);
   if (v != NULL) return v->regionMapType;
   if (GetRegionForSectionId(mapSecId) == REGION_TIKSI) return REGION_MAP_TIKSI;
   return REGION_MAP_HOENN;
   ```
   `REGION_MAP_KANTO` then becomes unreachable. Leave it in place, because the FRLG code references it.
2. **Graphics** (:330-425): add `gRegionMapInfos[REGION_MAP_EON/HOLON/NEWMOON/FULLMOON]`.
   - Eon: `map_eon.png/.pal/.bin` from `eon_clouds.py`. The sheet is padded to 16 tiles per row, so it needs `INCGFX_U32(..., ".8bpp.smol", "-num_tiles 125 -Wnum_tiles")` (the dense look; the exporter checks this, as the Tiksi one does).
   - Holon, Newmoon and Fullmoon share one sheet and one palette (`map_voyage_placeholder.png/.pal`, 123 tiles) and each has its own `.bin`. Their three `.regionMapGfx` / `.regionMapPalette` pointers are the same symbols.
   - Dex AREA copies: Eon `graphics/pokedex/region_map_eon.*`, the same picture as a 30x20 u16 tilemap (exporter pattern: `export_region_map_tiksi.write_dex`). The placeholders get a shared `region_map_voyage_placeholder.*`.
   - Sevii keeps its existing `map_sevii_*` and `region_map_sevii*` files. Apply **one tilemap edit** to each `map_sevii_*.bin`: the 9 tiles of FRLG's baked "switch map" button, cells (20-22, 12-14) = BG tiles x 21-23, y 14-16, are set to the sea tile, index 0. `sevii_grid.json` lists them. The dex copies have the same button; erase it there too.
3. **Layouts**:
   - Rewrite `region_map_layout_sevii123/45/67.h` from `sevii.py` `CLUSTERS`. Use `mapsec_u8_t` to match the Tiksi header.
   - Add `region_map_layout_eon.h`: one cell, (12,14) = `MAPSEC_EON_ISLAND`.
   - Add `region_map_layout_holon.h`: Holon Village (14,6), Mirage Forest (9,9), Research Tower (14,4), Holon Lake (15,10).
   - Add `region_map_layout_newmoon.h`: Newmoon Island (12,7).
   - Add `region_map_layout_fullmoon.h`: Fullmoon Island (13,7).
   - Add the matching cases to `GetMapSecIdAt` (:1229).

   The Sevii changes against the vanilla FRLG grids:
   - **123**:
     - (2,3) Kindle Road becomes `MT_EMBER`, so Mt. Ember gets a cell. FRLG overlaps it with Kindle Road's top cell.
     - (14,12) Bond Bridge becomes `BERRY_FOREST`, so Berry Forest gets a cell. FRLG overlaps it with Bond Bridge.
     - One-Two Strait: (2..8, 9).
     - Two-Three Strait: (10..13, 9) then (13, 10..12).
   - **45**:
     - RESORT_GORGEOUS, WATER_LABYRINTH and NAVEL_ROCK_FRLG are cleared: not built, and their slots are reused.
     - Four-Five Strait: (4..9, 4), (9, 5..11), (10..15, 11).
     - Icefall Cave keeps sharing Four Island's cell. Its entrance is on the Four Island map, and the cursor uses the escape warp.
   - **67**:
     - OUTCAST_ISLAND, GREEN_PATH, TRAINER_TOWER and BIRTH_ISLAND_FRLG are cleared.
     - Six-Seven Strait: (7..16, 6) then (6, 6..7).
4. **Section entries** (`region_map_sections.json`): x/y/width/height equal the bbox of the grid cells. These are the values `sevii.py` prints, and the exporter writes them:

   | Section | x,y,w,h |
   |---|---|
   | One Island | 1,8,1,1 |
   | Treasure Beach | 1,9,1,2 |
   | Kindle Road | 2,4,1,5 |
   | Mt. Ember | 2,3,1,1 |
   | Two Island | 9,9,1,1 |
   | Cape Brink | 9,7,1,2 |
   | Berry Forest | 14,12,1,1 |
   | Bond Bridge | 15,12,3,1 |
   | Three Island | 18,12,1,1 |
   | Three Isle Port | 18,13,2,1 |
   | One-Two Strait | 2,9,7,1 |
   | Two-Three Strait | 10,9,4,4 |
   | Four Island / Icefall Cave | 3,4,1,1 |
   | Five Island | 16,11,1,1 |
   | Five Isle Meadow | 17,11,1,2 |
   | Memorial Pillar | 18,12,1,3 |
   | Four-Five Strait | 4,4,12,8 |
   | Six Island | 17,5,1,1 |
   | Water Path | 18,3,1,5 |
   | Ruin Valley | 16,7,2,2 |
   | Seven Island | 5,8,1,1 |
   | Canyon Entrance | 5,9,1,1 |
   | Sevault Canyon | 6,9,1,3 |
   | Tanoby Ruins | 3,12,7,1 |
   | Six-Seven Strait | 6,6,11,2 |
   | Eon Island | 12,14,1,1 |
   | Holon Village / Mirage Forest / Research Tower / Holon Lake | 14,6 / 9,9 / 14,4 / 15,10 (all 1x1) |
   | Newmoon Island | 12,7,1,1 |
   | Fullmoon Island | 13,7,1,1 |

   - FRLG had Bond Bridge at x 13 and Meadow at y 10 / h 3; those values disagree with FRLG's own grid. The table uses the grid.
   - **L-shaped straits**: `InitMapBasedOnPlayerLocation` scales the player position into the bbox, so it can land on a sea cell that is not part of the strait. Add a case beside ROUTE_114 / ROUTE_126 (:1414): progress along the map's long axis maps to an index into the strait's cell list. Alternatively, keep every strait straight (Q4).
5. **`GetRegionMapRegionName`** (:1259): switch on `GetViewedRegionMapType()`:
   - SEVII* → "SEVII ISLANDS"
   - EON → "EON ISLAND"
   - HOLON → "HOLON"
   - NEWMOON → "NEWMOON ISLAND"
   - FULLMOON → "FULLMOON ISLAND"
   - TIKSI → "TIKSI"
   - otherwise "TOSA"

   The Rotom greeting "up the FULLMOON ISLAND map!" is 148 px in FONT_NORMAL; WIN_ROTOM is 168 px, so it fits.

   The MAP header also needs the sub-area: SEVII* → "ISLES 1-3" / "4-5" / "6-7", right-aligned in the narrow font (mock). Add `GetRegionMapSubAreaName()` and print it in `PrintTitleWindowText` (field_region_map.c:268) at `DISPLAY_WIDTH - 6 - width`. That spot is free, because the switch hint is off in voyages (§6).
6. **`GetRegionMapFallbackMapSec`** (:1267), per viewed type:

   | Type | Fallback |
   |---|---|
   | SEVII123 | ONE_ISLAND |
   | SEVII45 | FOUR_ISLAND |
   | SEVII67 | SEVEN_ISLAND |
   | EON | EON_ISLAND |
   | HOLON | MIRAGE_FOREST (the dock) |
   | NEWMOON | NEWMOON_ISLAND |
   | FULLMOON | FULLMOON_ISLAND |

   Pick the harbour where the Sailor or ferry lands.
7. **MAP v2** (:2563-2700):
   - New generated header `orchid_map_v2_voyages.h` with nodes, tubes and components per type, in the same format as `orchid_map_v2_tiksi.h`:

     | Type | Nodes | Tubes |
     |---|---|---|
     | Sevii123 | One/Two/Three Island discs; Mt. Ember and Berry Forest diamonds | 2 straits |
     | Sevii45 | Four/Five discs | 1 strait |
     | Sevii67 | Six/Seven discs; Canyon Entrance diamond | 1 strait |
     | Holon | village disc; 3 diamonds | none |
     | Newmoon / Fullmoon | 1 diamond each | none |
     | Eon | **no node**: the 16x16 diamond would hide the 6 px island; ring and head only (mock) | none |

     The FRLG art already bakes land routes (yellow/blue strips). Only the invented straits get BG1 sea tubes (`sea = TRUE`, blue once both ends are visited).
   - Tube tiles: `export_map_v2.py` builds a frame sheet per region (`orchid_frame_tiksi.png` pattern). Generate `orchid_frame_voyages.png` with the straight, corner and end sea-tube tiles the straits need.
   - Add `sOrchidRegionMapsV2[REGION_MAP_SEVII123…FULLMOON]`. Change the fallback in `GetOrchidRegionMapV2()` to `if (nodes == NULL && nodeCount == 0)`, and add a static `{0}` "empty" entry so a type without nodes draws **nothing** instead of Tosa's.
   - Extend `ORCHID_MAP_MAX_NODES` (:89) with the new arrays. The largest is Sevii123 with 5 nodes, so the 32-bit visited mask is fine.
   - `OrchidMapPlaceVisited`: needs real flags (§9).
8. **Fly / heal**: see §9.

## 5. Eon map art (decided, round 4: intro clouds, dense, Hoenn map as-is underneath)

- **Source.** `graphics/intro/scene_2/clouds.png`, the intro's passing-cloud OBJ sheet. Its palette is its own PNG palette, the same as `sClouds_Pal`. Only colours 9-11 are used.
- **Stamps.** The sheet's 8x8 tiles are copied unchanged as four stamps: the big cloud (4x4 tiles) plus three wisp strips.
- **Placement.** Big clouds sit on two staggered lattices of the BG tile grid: every 3 tiles across and every 2 rows, odd rows shifted, alternate ones mirrored. The second lattice is offset one tile right and one down and drawn behind.
  - Together they overlap into banks that hide most of Hoenn: landmass, routes and town markers.
  - A deterministic few are left out, so scattered bits of map and sea show through.
  - Wisps go on top.
- **Clear window.** Stamps that would touch the window round Southern Island (px 88-135 x 112-135, top corners stepped) are dropped, so the island, a bit of sea and the player icon stay clear.
- **Hoenn underneath.** The vanilla Hoenn map is used as-is (user, round 4). The cloud pixels are composited into the map tiles at export time. The round-3 "sky between sparse clouds" look is still rendered for reference.
- **Budget.** See §10.
- **No flips.** Affine BG2 cannot flip tiles, so mirrored clouds are stored mirrored. That is 42 distinct cloud tiles including the mirrored ones; the sheet has 32.
- **Hidden rows.** The rows under the header and tray (BG rows 0-1 and 17-19) are filled with the most common visible tile, so they cost nothing.
- **Hoenn art source.** The exporter reads the vanilla Hoenn art from git (`fead488d62^:graphics/pokenav/region_map/map.png/.bin/.pal`), because `map.png` is now Tosa.
  - **Recommendation:** commit a copy as `graphics/pokenav/region_map/map_hoenn_vanilla.*` and drop the git dependency.
- **Runtime cost: none.** There is no OBJ and no extra BG layer: `LoadRegionMapGfx` loads it exactly like any other region map.

## 6. Phone R switching (d)

- `CanSwitchRegionFromMap()` (field_region_map.c:241) becomes:
  ```c
  return callback == CB2_ReturnToRotomPhone && FlagGet(FLAG_VISITED_TIKSI)
      && !IsVoyageRegionMapType(GetRegionMapType(gMapHeader.regionMapSectionId));
  ```
  In a voyage destination the phone map shows only where you are, with no hint and no R.
- The flip at :189 stays HOENN ⇄ TIKSI, so voyage maps never enter the cycle.
- Alternative (Q6): from a voyage, R cycles here → Tosa → Tiksi → here.

## 7. Exporters (e)

- `export_region_map_tiksi.py`:
  - `kanto_block()` (:85) must end at `ids.index("MAPSEC_ONE_ISLAND")`. Use a shared constant, e.g. `region_tags.VOYAGE_START = "MAPSEC_ONE_ISLAND"`, never renamed.
  - Effects: `update_sections` stops popping x/y on Sevii entries; the free list (:144) can only offer Tiksi slots; `assert free` fires once Tiksi's 35 free slots are gone, instead of eating voyage slots.
- `export_region_map.py` (Tosa), `update_sections` (:201):
  - Its "reserved for Tiksi" range `kanto0..kanto1` already covers the voyage block. Leave that as it is.
  - Add `KEEP = {"MAPSEC_EON_ISLAND"}`, so Southern Island's x/y/w/h survives instead of being zeroed (:231).
- `region_map_tagger/index.html:183`: `kantoEnd` should become the index of `MAPSEC_ONE_ISLAND`, exclusive, so the Tiksi tagger cannot paint voyage sections.
- `server.py`: nothing to change.
- A new `dev_scripts/voyages/export_region_maps.py` owns the voyage block entries in `region_map_sections.json` and the alias lines. Write aliases cumulatively, using `write_aliases`' merge rules, so the other two exporters keep them.

## 8. Pokédex AREA and popups

- **Popups**: the GEN_5 popup takes the name from `gRegionMapEntries`. Kanto-range ids fall back to theme 0 = BW default, the same theme as everywhere else in Orchid. Only the names (§1) need changing.
- **Dex AREA**: it shows the current region type's map and only that type's encounters. So Holon's Delta wild mons show on the Holon placeholder while you stand in Holon, and in Tosa they show as "area unknown". That is vanilla behaviour, the same as Kanto/Sevii in FRLG. Eon has no wild table (Latias and Latios are static), so its AREA page is empty.
- **Bug to fix with the maps**: `FindMapsWithMon`'s group switch (pokedex_area_screen.c:343) ignores any group other than TownsAndRoutes, Dungeons or SpecialArea, with or without the `_FRLG` suffix. New voyage map groups would never show. The same applies to Orchid's existing Tiksi / Overworld / TosaRail groups.
  - Fix: add a `default:` that calls `SetAreaHasMon` when the section has a cell on the grid (width > 0), and `SetSpecialMapHasMon` otherwise.

## 9. Flags, Fly and heal locations

- The FRLG flags `FLAG_WORLD_MAP_ONE_ISLAND` … `_SEVEN_ISLAND` are `0` (flags.h:2405+). Point them at 7 free system flags, e.g. `FLAG_UNUSED_0x8E3`, `0x8E5`-`0x8EA` (check with the other agents first), and set them in each island's `OnTransition`.
- `GetMapsecType`, `sFlyLocations` and `OrchidMapPlaceVisited` then work unchanged.
- Holon Village, Newmoon and Fullmoon need `GetMapsecType` cases plus a flag each if they should show gold. Otherwise they stay grey except while you are there.
- `sMapHealLocations` rows for the Sevii slots (:520-563) point at FRLG `MAP_*` ids that do not exist. Rewrite them for the built maps; voyage centres get `HEAL_LOCATION_*` entries.
- Fly inside a cluster works through the wall Town Map with the Poké Rider (Q7). The phone never flies. You can never fly out of a voyage map, because the fly map only shows the current type.

## 10. GBA budgets (region map BG2)

BG2 is affine 8bpp:
- tiles: ≤ 256, because tilemap entries are u8
- charblock 2: 256 × 64 B = 16 KB
- tilemap: 64x64 u8 = 4 KB, screenblock 28
- palette: **48 colours** at `BG_PLTT_ID(7)`, indices 112-159 (`LoadRegionMapGfx` :803)
- no tile flips

| Map | Tiles | Colours |
|---|---|---|
| Vanilla Hoenn | 231 | 29 |
| Tosa | 250 (`-num_tiles 250`) | — |
| Tiksi | 219 | — |
| **Eon (dense, chosen)** | **125** (8000 B) | 23: vanilla 113-140 subset + intro cloud 141-143 |
| Eon round 3 (sky, sparse) | 44 | 9 |
| Eon round 3 (map, sparse) | 258: **over the limit**. Sparse clouds leave more unique map tiles visible than dense ones do | 30 |
| Sevii 1-3 / 4-5 / 6-7 (FRLG, unchanged) | 64 / 32 / 64 | ≤ 25 |
| Holon + Newmoon + Fullmoon (shared sheet) | 123 together | 6 of the vanilla `map.pal` |

- BG1 (MAP v2 frame and tubes) is 4bpp in charblock 3, with palettes 1 and 4-6.
- New sea-tube tiles: about 6 straight, corner and end shapes, appended after the 16 frame tiles (`ORCHID_MAP_FRAME_TILES`).
- Dex AREA copies are 8bpp text-BG tiles with a 30x20 u16 map, so the same counts apply.

## 11. Test plan (headless mGBA, after building)

- Warp to each voyage map. Check:
  - `FLAG_VISITED_TIKSI` stays clear
  - the phone MAP header shows the right region and sub-area, with the cursor and head on the right cell
  - no R hint is shown
  - the popup name is correct
- Check the strait cursor along a long map.
- Open the wall Town Map on One Island (fly icons).
- Dex AREA for a Holon δ species while in Holon and while in Tosa.
- Re-run `export_region_map_tiksi.py` and `export_region_map.py`, then diff `region_map_sections.json`. Voyage entries and Eon must be unchanged.
