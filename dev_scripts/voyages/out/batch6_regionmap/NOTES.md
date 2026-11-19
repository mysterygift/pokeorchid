# Sailor's Voyages, batch 6: region maps (Eon, Sevii, Holon, Newmoon, Fullmoon)

These are mockups and a plan only. Nothing under data/, src/, include/ or graphics/ was changed. The full code plan is in `dev_scripts/voyages/regionmap/IMPLEMENTATION.md`.

Regenerate (Pillow venv):
- `python dev_scripts/voyages/regionmap/eon_clouds.py`
- `python dev_scripts/voyages/regionmap/sevii.py`
- `python dev_scripts/voyages/regionmap/placeholders.py`

Every screen is drawn as Orchid's MAP v2 would draw it, using the real ROM art:
- **BG2:** the region map art
- **Header and tray:** the same kit drawing as the approved `mock_map.py`
- **OBJs:** nodes, gold ring cursor and player head, from the ROM sheets (`cursor_small.png`, `orchid_nodes.png`, `brendan_icon.png`)
- **Sizes:** 1x is 240x160; the `@3x` files are the 3x versions.

## Files
| File | What |
|---|---|
| `eon_dense_screen.png` / `@3x` | **Eon Island, chosen look.** Intro clouds packed densely over the vanilla Hoenn map, Southern Island clear |
| `eon_dense_bg2.png` / `@3x` | The BG2 picture alone, exactly what REGION_MAP_EON's tiles and tilemap hold |
| `eon_compare.png` / `@3x` | The source intro cloud sheet (stamp boxes marked), vanilla Hoenn, dense (chosen), and round 3's sparse clouds on sky |
| `eon_sky_*` | Round 3, kept for reference |
| `eon_rom_preview/eon_dense.{png,bin,pal}` | What the exporter would ship: 8bpp sheet, 64x64 u8 affine tilemap, 48-colour JASC palette. Plus `_sheet@3x.png` |
| `eon_budget.txt` | Tile and colour counts |
| `sevii_screens.png` / `@3x`, `sevii{123,45,67}_screen.png` | The three FRLG Sevii maps in MAP v2: header "SEVII ISLANDS" plus the sub-area, town discs and landmark diamonds, blue sea-route tubes for the invented straits, ring and head |
| `sevii{123,45,67}_cells@4x.png` | The proposed cursor grid. Black boxes = sections we build. Dashed blue = new strait sections. Red X = vanilla cells cleared (not built). Orange = FRLG switch button erased |
| `sevii_grid.json` | Section bboxes (go into `region_map_sections.json`), cleared sections, erased tilemap entries |
| `placeholders_screens.png` / `@3x`, `{holon,newmoon,fullmoon}_screen.png`, `_bg2.png` | Placeholder maps |
| `placeholders_budget.txt` | Shared-sheet tile count |

## Eon Island: the decision trail
1. **Round 1.** Procedural puff clouds, and a re-paletted intro *storm* cloud texture. The user picked the white Gen 3 look but wanted fewer, bigger clouds, baked into the BG with no sprites. They never were sprites: every round has been BG2 tiles only.
2. **Round 2.** Five drawn cumulus banks. Rejected: "looks even worse — just use existing tiles".
3. **Round 3.** The intro's `graphics/intro/scene_2/clouds.png` tiles as-is (big cloud plus wisps, mirrored only), sparse, on the intro sky colour. Verdict: "looks good for now", but it needs to be denser.
4. **Round 4 (decided).** Map as-is underneath, dense.
   - **How it's built:**
     - Big clouds sit on two staggered lattices, so they overlap into banks covering most of Hoenn, with scattered gaps showing bits of map and sea.
     - Nine wisps go on top.
     - Southern Island, a little sea and the player head stay clear.
     - 128 big clouds and 9 wisps are placed. 11 placements touching the clear window are dropped.
   - **Budget:**
     - Tiles: **125 unique 8x8 tiles of 256** (8000 B).
     - Colours: **23 of the 48-colour slot** (the vanilla Hoenn colours visible in the gaps plus the 3 intro cloud colours at 141-143).
     - Fits easily: vanilla Hoenn alone is 231 tiles.
   - **Hardware notes:**
     - The region map BG is affine, so it has no tile flips. Mirrored clouds are stored mirrored (42 distinct cloud tiles in all).
     - Round 3's sparse clouds over the map needed 258 tiles, over the limit. Dense coverage is cheaper, because cloud interiors dedupe and fewer map tiles show.
   - **Eon gets no node diamond.** It would cover the 6 px island; the ring and head mark it.

## Sevii
- **Art.** The FRLG art is unchanged apart from erasing FRLG's baked "switch map" button: 9 tiles per map, set to the sea tile by a tilemap edit.
- **Routes.** The FRLG art already draws Kindle Road, Bond Bridge, Water Path and the other land routes. Only the invented straits are drawn, as MAP v2 sea tubes.
- **Grid changes (Sevii 1-3):** Mt. Ember gets Kindle Road's top cell (2,3); Berry Forest gets Bond Bridge's west cell (14,12). FRLG only had them overlapping.
- **Cleared cells.** Sections we don't build are taken off the grid and their slots reused:
  - Resort Gorgeous, Water Labyrinth, Navel Rock (Sevii 4-5)
  - Outcast Island, Green Path, Trainer Tower, Birth Island (Sevii 6-7)
- **Leftover art.** Their art (paths, the Birth Island triangle) stays visible as scenery; see Q3.
- **Strait slots:** Sevii Isle 22/23/24 and Three Isle Path, renamed One-Two / Two-Three / Four-Five / Six-Seven Strait.

## Placeholders (Holon, Newmoon, Fullmoon)
- **Contents:**
  - Vanilla region-map sea tile.
  - One flat island silhouette each:
    - Holon: an irregular big island with Village (disc) and Mirage Forest / Research Tower / Holon Lake (diamonds).
    - Newmoon: a crescent.
    - Fullmoon: a round island.
  - A small baked "PLACEHOLDER" tag.
- **Budget.** All three share one sheet (123 tiles) and the vanilla palette (6 colours).

## Map-name popups and the Pokédex AREA screen
- **Popups:** need no code. Orchid uses the GEN_5 black popup, and Kanto-range sections already fall back to the default theme. Only the section names change (title case, ≤16 characters; "Research Tower", not "Holon Research Tower").
- **Dex AREA** shows the region the player is standing in:
  - Holon's δ wild mons appear on the Holon placeholder only while in Holon.
  - Eon has no wild table, so its page is empty.
  - **Bug found:** the AREA screen skips encounters from any map group other than TownsAndRoutes, Dungeons or SpecialArea (with or without the `_FRLG` suffix). New voyage groups would never show, and neither do Orchid's Tiksi / Overworld / TosaRail groups today. The fix is in IMPLEMENTATION §8.

## Key findings from the code survey
1. Today the whole Kanto+Sevii block resolves to REGION_TIKSI, so:
   - a Sevii map would set FLAG_VISITED_TIKSI and show the Tiksi map
   - the Sevii branch of `GetRegionMapType` is dead
   - **Fix:** split the block at MAPSEC_ONE_ISLAND. 0x58-0x8E stays Tiksi (35 slots still free); 0x8F-0xBF becomes voyages.
2. The Tiksi exporter zeroes x/y on every block entry, and its free-slot allocator walks into the Sevii ids. The Tosa exporter zeroes untagged Southern Island. Both need the guard in IMPLEMENTATION §7, and so does the tagger's `kantoEnd`.
3. The MAP v2 table falls back to **Tosa's nodes and tubes** for any region type without its own entry. Without new entries, the Sevii art would get Tosa discs on top.
4. `FLAG_WORLD_MAP_*_ISLAND` are `0` in Emerald, so the Sevii fly points and visited (gold) state never turn on until they are pointed at real flags.

## Decided (user, 2026-11-19)
- Eon Island: no place marker (no diamond); opening the map shows the player head over Southern Island's spot on the clouded Hoenn map. Dense round 4 clouds.
- Sevii battles use the FRLG battle music, re-voiced onto Hoenn (Emerald) voicegroups so they match Hoenn music.
- Fly only works within the current Sevii cluster (1-3 / 4-5 / 6-7).
- Section names as proposed are right.
- Unbuilt FRLG scenery stays drawn as decoration; L-strait cursor special-case yes; phone R switching disabled during a voyage; header keeps the "ISLES 1-3" sub-label; Eon density approved; Holon/Newmoon/Fullmoon placeholders fine.

## Open questions (recommendation first)
1. **Eon density.** Is round 4 dense enough? The budget leaves room for more: 125/256 tiles. Raise `gap_every` to hide more, lower it to show more.
2. **Eon node.** No diamond on Eon Island (ring + head only), so the tiny island stays visible. The alternative is the usual landmark diamond.
3. **Unbuilt FRLG scenery on the Sevii maps** (Outcast Island's path, Trainer Tower, Birth Island's triangle, Navel Rock):
   - **Recommendation:** leave it as decoration with no cursor cell.
   - The alternative is to paint those tiles to sea: tilemap edits only, no new tiles.
4. **Strait shape.** The L-shaped straits (Two-Three, Four-Five, Six-Seven) need a small cursor special-case so the head follows the route.
   - **Recommendation:** add the special-case (IMPLEMENTATION §4.4).
   - The alternative is to draw them straight.
   - Four-Five is long on the region map (19 cells). The actual sea route map can still be short, because the cursor only scales.
5. **Battle music in Sevii.**
   - **Recommendation:** Sevii sections report REGION_KANTO, so `GetBattleBGM` plays the FRLG trainer and wild themes (MUS_RG_VS_TRAINER / MUS_RG_VS_WILD).
   - The alternative is REGION_TOSA (Orchid's music).
   - Holon, Eon and the moons stay Tosa in either case.
6. **Phone R in a voyage.**
   - **Recommendation:** disabled. The map shows only where you are, with no switch hint.
   - The alternative is to cycle here → Tosa → Tiksi.
7. **Fly inside a Sevii cluster** from the wall Town Map with the Poké Rider:
   - **Recommendation:** allow it within the cluster only (FRLG behaviour). The phone never flies, and you can never fly out of a voyage.
   - The alternative is no Sevii fly points at all, ferry only.
8. **Section names.** "One-Two Strait" style names for the invented sea routes, and "Holon Village" / "Mirage Forest" / "Research Tower" / "Holon Lake": are these OK, or do you have your own names?
9. **Sub-area label.** Should the header read "SEVII ISLANDS" plus "ISLES 1-3" right-aligned (as mocked), or just "SEVII ISLANDS"?
