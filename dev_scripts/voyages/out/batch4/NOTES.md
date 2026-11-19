# Sailor's Voyages, batch 4: Holon, design-review mockups (round 2)

These are mockups only. Nothing under data/, src/, include/ or graphics/ was changed. The new tileset is a **draft** written to `out/batch4/gTileset_Holon/` (plus two palette variants, see Greens). The maps are rendered from those draft files, so what you see is what the game would load.

How the outdoor maps are built:
- Every cell is first composed in General + Fortree, copied from vanilla Route 119 / 120 / Fortree cells.
- It is then converted to General + gTileset_Holon: rock becomes its blue-grey copy, and the new pieces are placed.

Marks on the maps:
- yellow = NPC
- red = Holon Researcher trainer (Scientist1 sprite as a stand-in)
- pink = Cynthia (sprite by lichen, credit "sprites by lichen") and landmark spots
- blue = warp door
- orange text = connection
- grey = objects (berry trees, the sphere)

To regenerate (Pillow venv): `python dev_scripts/voyages/holon/mock_holon.py`. It also rewrites the draft tileset.

Scripts in `holon/`:
- `holon_tileset.py`: the tileset generator and all the new art
- `specs_holon.py`: the map specs
- `holon_kit.py`: helpers
- `mock_holon.py`: the renderer

Files in `out/batch4/`:
- `holon_coast`, `holon_village`, `holon_lake` (`.png` + `@2x`), in the recommended greens (primary + secondary desaturated, drained rings)
- `holon_tower_1f`, `holon_tower_2f`, `holon_ruins_house` (`.png` + `@2x`)
- `overview.png`
- `holon_new_art_4x.png`: every new piece at 4x, beside the vanilla art it is matched to
- `holon_lake_pillars_dormant@2x.png` / `_glow@2x.png`: the pillars in the map at 2x, sphere off and on
- `holon_palette06.png`: General 03 beside Holon 06
- Greens comparison:
  - `holon_village_green_{current,secondary,full}@2x.png`
  - `holon_lake_green_{current,secondary,full}@2x.png`
  - `holon_green_compare@2x.png`: GBA-camera crops, the three variants side by side

## Decided
- **Round 1 (2026-11-19):**
  - Holon outdoor maps are built from Route 119 / 120 pieces.
  - The Research Tower is the vanilla Weather Institute, with interiors ROUTE119_WEATHER_INSTITUTE_1F/2F (Building + Lab).
  - The three small domes round the tower are dropped.
- **Round 2 (user answers):**
  - **gTileset_Holon** = a Holon-only copy of gTileset_Fortree, used only by the three Holon outdoor maps.
  - **Blue-grey rocks:** in gTileset_Holon.
  - **Railway:** the existing Orchid rail kit pieces, copied in.
  - **Diamond-carved stones:** new art.
  - **Dead trees:** dropped.
  - **Lake pillars:** new 1x3 tiles.
  - **The sphere:** an object with a palette-swap glow.
  - **Carved domes:** stay sealed.
  - **Ruins-house interior, heal location and MAPSECs:** approved.
  - **Greens (user):** desaturated greens. Story beat: the researchers drain energy from the land through Power Spots, and it's hurting the flora.

## gTileset_Holon: what it is and what it touches
- **A copy, so nothing shared changes.**
  - Fortree's own files and its 4 layouts (FORTREE_CITY, ROUTE119, ROUTE120, FARAWAY_ISLAND_INTERIOR) are untouched.
  - gTileset_General (primary) is untouched; Holon metatiles only *reference* General tiles.
  - The rail kit's General palette-04 edit (crossing-sign colours in `install_area_kit.set_pal4`) is NOT needed: only the rail pieces are copied, and they use General palette 03 as it is.
- **Palettes (secondary slots 6-12):**

  | Slot | In Fortree | In gTileset_Holon |
  |---|---|---|
  | 06 | blank | **NEW "Holon rock"**: General 03 with slots 8-14 (outline + brown rock ramp) swapped for blue-grey of the same luminance: (48,48,72) and (224,232,240) (184,196,216) (152,164,192) (120,132,168) (88,100,136) (64,72,104). Grey and grass slots are as General 03, so the grass inside rock tiles still matches. |
  | 07 | blank | **NEW "drained foliage"**: General 02 with its green slots (1-4, 12-15) at about 45% saturation, nudged toward straw. Used only by the Power Spot rings. |
  | 08-11 | Fortree's | copied (green slots desaturated, see Greens) |
  | 12 | blank | **free** |

- **Metatiles:** 367 of 512.
  - Fortree's 285 at 0x200-0x31C, unchanged, plus 3 blank slots.
  - **79 new at 0x320-0x36E**, listed in `gTileset_Holon/holon_metatiles.json`:

    | Range | What | New tiles |
    |---|---|---|
    | 0x320-0x344 | 37 blue-grey rock copies: Route 120 ridge / spikes / mounds, General cliff and boulders, the Ancient Tomb dome, and the Weather Institute cells that carry its rock face. Palette 03 -> 06 in the entries. | 0 |
    | 0x345-0x353 | 15 drained-foliage copies: grass, tall grass, long grass and its edge, 1-wide trees, peeks, flowers. Palette 02 -> 07. | 0 |
    | 0x354-0x359 | rail H / HW / HE, plus drained twins | rail kit tiles |
    | 0x35A-0x35D | carved stone top / bottom, plus drained twins | new |
    | 0x35E-0x360 | pillar top / mid / base | new |
    | 0x361-0x36C | 3x2 plinth, plus drained twins | new |
    | 0x36D-0x36E | sealed dome door: arch + slab | new |

- **Tiles:** 55 new tiles in total (rails + all new art).
  - They fill Fortree's blank tail slots 493-511 first, then slots no metatile references.
  - 276 unreferenced slots remain.
  - Wiring needs `-num_tiles 512` in graphics.h.
- **Layers:**
  - Rails, stone bottom, pillar base and plinth: COVERED (grass or water bottom layer, art on top).
  - Stone top, pillar top and pillar middle: NORMAL, so a player behind them (or surfing past) is hidden, like a tree top.
  - Pillar top / middle keep the water behaviour (surfable); the base is solid.
- **Sphere:** an object, not tiles. 32x32 OBJ sprite (`holon_tileset.sphere_sprite`). Its two 16-colour OBJ palettes (dormant blue-grey / glowing cyan) share the same indices, so the glow is a palette-tag swap at run time.
- **Art rules followed:**
  - Light from the top-left; Gen 3 3/4 view.
  - Tops seen from above: the stone and pillar-capital slabs (5-6 rows), the plinth top with a socket ring. Each has a dark lip row in the material's dark shade, then the front band.
  - Front faces lit-left / dark-right, with a checker dither only at the two ramp steps.
  - Incised diamonds: upper-left walls dark, lower-right walls light.
  - Outline dark on the shadow side; shadows cast down-right on the grass.
  - The domes keep the vanilla Ancient Tomb dome's own dithering; only the palette changes. The slab that seals the door is shaded with the same ramp: shadow under the arch, lit left jamb, dithered step to the shadow side.

## Greens (story: the Power Spots drain the land)
Three looks are rendered: `*_green_*@2x.png` and `holon_green_compare@2x.png`.

1. **current:** vanilla greens.
2. **secondary-only:** gTileset_Holon's greens desaturated (slots 06: 6,7,15; 08: 15; 09: 1-4,15; 10: 9,10,15; 11: 1-4,10,15). Cheap, but plain grass, trees and long grass live in General palette 02, so they stay vivid. Rock-edge grass and long-grass edges no longer match: the visible seams in the compare image.
3. **primary + secondary (recommended):** as 2, plus a **Holon-only primary, gTileset_GeneralHolon**.
   - It shares General's tiles, metatiles, attributes and animation callback; the struct points at General's own arrays. Only its palette array is new: General 00-05 with greens desaturated (00/01/04/05: slot 15; 02: slots 1-4, 12-15; 03: slots 6, 7, 15). ROM cost is about 192 bytes of palettes.
   - The colour change: saturation down about 35%, hue nudged about 10% toward olive, value kept, so ramps and dithering still read. Non-greens (water, roofs, skin, outlines) are untouched.
   - It affects only what Holon maps draw from the primary: grass, trees, paths' grass edges and the Centre / Mart / house stamps' grass corners. Sprites use OBJ palettes and are unaffected.
   - All three Holon outdoor maps use the same pair (General_Holon + Holon), so their connections stay seamless.
   - **Caveat:** field-effect sprites (tall- / long-grass rustle, footprints) use fixed OBJ palettes and would stay vivid. Either accept it, or load a desaturated field-effect palette on Holon maps (small C hook).
- **Drained rings round the Power Spots** (rendered in every variant). Foliage cells near the Research Tower (centre (36,36), full to r 9.5, thinning to r 17) and the pillar island (centre (25,26), full to r 6.5, thinning to r 12) swap to their palette-07 twins.
  - The thinning is a 4x4 ordered dither of whole cells, which reads as dying patches.
  - It costs 15 metatile copies plus drained twins of the grass-bottomed new pieces, and 0 tiles.
  - The Weather Institute's own grass corners use Fortree palette 08, so they stay at the normal desaturated green: a faint lighter-green halo at its foot.

**NPC flavour lines** (suggested):
- Farmer, NW field: "Third season the berries won't set. Leaves come up grey as ash, closer to that tower they get."
- Farmer, SE field: "My gran said this soil grew anything. Now look at it. Power Spot, they call it... more like a drain."
- Lass by the Centre: "The grass round the lake used to be so green. Now it's all washed out near those stone pillars."
- Researcher on the walkway (brushing it off): "A seasonal fluctuation, nothing more. The readings from the Power Spot are perfectly within tolerance."

## Maps (sizes, pairs, objects)
- **Mirage Forest coast:** 44x48, General_Holon + Holon.
  - Jetty of Route 119 bridge planks over calm water.

    | Object | Position | Facing |
    |---|---|---|
    | Sailor | (3,36) | left |
    | Boat | (1,36) | bow to the jetty |

  - **Ruins clearing:** an old railway (rail kit HW, H…, HE at x13-25, y9) and four carved stones at (15,4-5), (23,4-5), (15,11-12), (23,11-12), with blue-grey mounds and boulders.
  - Researcher trainers at (21,9) and (34,22); a lass at (16,31).
  - East edge goes to the village west edge, offset +12.
- **Holon Village:** 72x72.
  - Poké Ball plan: tree ring, river canal running north-south, two octagonal ring canals, a dirt ring path, the walkway with Route 119 bridges, the Weather Institute (door (35,36)) against its now blue-grey rock face.
  - Buildings and doors:

    | Building | Door(s) |
    |---|---|
    | Centre | (6,35) |
    | Mart | (10,35), (11,35) |
    | H1 | (23,7) |
    | H2 | (15,15) |
    | H3 | (43,7) |
    | H4 | (5,25) |
    | H5 | (63,27) |
    | H6 | (59,55) |
    | H7 | (21,63) |
    | Holon Ruins house | (55,15) |

  - 4 crop fields with berry trees.
  - NPCs: farmers (25,14), (46,7) and (62,44); lass (9,37); mentor (56,16); researcher (36,39).
  - Connections: west edge to the coast (-12); south edge to the lake (0).
- **Research Tower 1F:** WEATHER_INSTITUTE_1F as it is (20x13, Building + Lab).
  - Exits (9,12) and (10,12); stairs (17,1).
  - Researchers at (14,2), (5,4) and (15,5); a visitor at (2,11).
- **Research Tower 2F:** WEATHER_INSTITUTE_2F (20x11).
  - The middle desks become Birch's two round machines, at (8,7) and (13,7), and an orange tank at (10,4).
  - Stairs (17,1); trainers (18,6) and (11,9); NPCs (6,6) and the head of research (2,6).
- **Holon Lake:** 72x52.
  - Blue-grey Route 120 ridge down a land strip into the lake, breaking into spikes.
  - **Pillars** in the water at (24,17-19), (16,31-33) and (33,31-33): a triangle round the island.
  - **Plinth** at (23-25, 25-26) with the **sphere object** at (24,25).
  - **Cynthia** at (24,35) on the south peninsula, facing up.
  - **Sealed domes** at (5,6) and (59,42): door cells (7,8-9) and (61,44-45), solid.
  - Marsh puddles in long grass on the west shore.
  - Researcher trainers at (8,36) and (40,13); mentor at (16,45).
  - North edge goes to the village (0).
- **Holon Ruins house:** 10x9, Building + GenericBuilding, base LAYOUT_HOUSE1 (shared by the 14 GenericBuilding layouts; nothing edited).
  - Stripped to bare boards: rug, table, chairs and plants taken out, using existing floor/wall cells. The cabinet, bookshelf and window are left.
  - A lore item at (4,5); exits (3,8) and (4,8), back to village door (55,15).
  - GenericBuilding's chairs and jars carry rug / green-floor backgrounds, so they can't stand on bare boards. More "dust" would need a few new cells.
- **Heal location:** HEAL_LOCATION_HOLON_VILLAGE at the Centre door (6,35), respawning in front of it at (6,36).
- **Proposed MAPSECs:** MAPSEC_HOLON_MIRAGE_FOREST (coast), MAPSEC_HOLON_VILLAGE (village, tower 1F/2F, ruins house, Centre/Mart), MAPSEC_HOLON_LAKE. Each needs a placeholder region-map cell.

Holon Researcher trainers: 6 in total (coast 2, lake 2, tower 2F 2).

## Open questions (recommendation first)
1. **Greens:** primary + secondary (gTileset_GeneralHolon palettes + Holon 06/08-11), recommended. Or secondary-only, which is cheaper but leaves grass/rock and long-grass seams.
2. **Drained rings:** keep them as rendered (palette 07, 15 metatile copies, 0 tiles)? Optionally also a desaturated field-effect OBJ palette on Holon maps.
3. **Sphere glow trigger:** swap to the glowing palette when Cynthia is beaten / the event fires (recommended). Or a slow 2-palette pulse while active.
4. **Ruins house dressing:** bare as shown (recommended, 0 new art). Or 2-3 new GenericBuilding-copy cells: dust piles, a tipped chair on boards.

## Known seams (round 1, unchanged)
- Tree-on-sand along the coast.
- Weather Institute stamp edges.
- Pond-staircase corner pairs that are rare in vanilla.
