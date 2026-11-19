# Sailor's Voyages, batch 1: design-review mockups

These are mockups only. Nothing under data/, src/ or include/ was changed. Every cell is copied from an existing layout with the same primary + secondary tileset pair (or, for General-primary ids, from any layout that shares the primary), so no tileset is edited. Each map is drawn at 1x and @2x. Marks: yellow = Sailor/NPC, orange = Son, white = boat, blue = warp, pink = legendary, red = item ball, green = sign. Sprites are the real overworld PNGs.

To regenerate (Pillow venv): `python dev_scripts/voyages/mock_batch1.py [name ...]`. Specs are in `specs_batch1.py`; the shared tooling is in `voyage_compose.py`.

## Tileset change made during review
- **Newmoon does not use gTileset_Fallarbor**, at the user's request. Newmoon was first drafted on General + Fallarbor (Route 113 ash). Both Newmoon maps are now General + **Dewford**.
- **Fullmoon was never on Fallarbor.** It is General + Rustboro (exterior and interior), unchanged. The only Fallarbor render of Fullmoon was a throwaway palette test in the scratchpad.

---

## 1. Wavebreak Town patch: `wavebreak_before.png` / `wavebreak_after.png`
- **Size and pair:** 36x34 (unchanged), General + TosaPort. **60 layouts share TosaPort**: all Tosa towns and routes, Tiksi Routes 401-410, Mt. Drake faces, Inka Seawall, Frigo Cave exterior, and others. Only existing cells are reused.
- **History:** the user has hand-edited this map. `d76b8ea26f` holds their Porymap edits: resize 32x30 to 36x34, connections, and NPCs moved (the fisherman placed at 11,26 facing the sea). The later `6bafea671f` only swapped the Centre/Mart art. The patch therefore changes only the south-west corner.
- **Changes:**
  - **Beach:** x7-10, y28-30 is now sand (0x124). The shoreline steps out at y27 (11B/11C/13D) and back in at y31 (12C/145). Rows y32-33 and the Route 312 edge are untouched. Close-up: `wavebreak_beach_3x.png`.
  - **Other houses:** House 1 and House 3 are repainted purple like House 2; their doors and warps are unchanged.
  - **Hut:** a 4x4 copy of Wavebreak's red-roof General house (the same art as House 1), so it stands out from the purple houses. It sits at x12-15, y26-29 with the door at (13,29). Tosa Port's crates are at (16,27-28), on grass.
  - **Dock:** Mr. Briney's wooden dock from Route 104, drawn from the Rustboro metatiles; it needs the TosaPort addition below. It is pier columns only: the sea end at x3 (33D/345/335) and planks at x4-6 (26E/26D/276), rows y28-30.
    - Route 104's land-end column (32E/336/277) is left out because it carries that map's cliff rock. The planks start in the shore column x6 and run straight off the sand.
    - Rows y28-29 are walkable planks; y30 is the face with posts in the water (water behaviour). (7,30) becomes shore water (145) so the face meets water, not sand.
  - **Sea rocks:** three rock clumps cleared, at (0-1,28-29), (0-1,30-31) and (2-3,30-31).
  - **Fishermen** (OBJ_EVENT_GFX_FISHERMAN, Emerald asset, NPC_2 palette; rendered with it). Each faces the water and stands where nothing gets cut off:

    | Position | Facing | Status | Flavour |
    |---|---|---|---|
    | (11,26) | left | existing, unchanged | |
    | (11,10) | left | new | "The fish bite best under these trees at the north end. Shade on the water, see?" |
    | (11,17) | left | new | "Left my spare rods by the Centre. If they're gone, so's my luck." |
    | (8,30) | down | new, on the beach | "That old sailor's boat goes places my line never reaches. Wonder what bites out there." |

  - **Fish crates and rods** (proposed TosaPort metatiles, all solid except the rod tips):
    - A crate of fish over a crate stack at (11,27-28), beside the fisherman at (11,26).
    - A crate of fish at (11,11).
    - Upright rod pairs, 1x2, at (11,18-19) and (9,29-30). The rod top cell is passable and drawn over sprites; the base is solid.
    - A bucket next to each rod pair, at (11,20) and (10,30), solid. No bucket or pail metatile was found in General or TosaPort (the Slateport/Dewford/Lilycove sets were not searched); the nearest are TosaPort's market pots (0x20C, 0x21B/0x21C), which sit on cobble.
    - The beach and dock stay reachable from (12,30) via (11,29-30), (10,29), (9,29) and (8,28-29). The x11 shore strip was already blocked by the fisherman at (11,26), and its pockets open onto the grass at x12.
- **New warp:** (13,29) leads to MAP_WAVEBREAK_TOWN_SAILORS_HUT, warp 0.
- **New objects** (shown after the Champion):

  | Object | Graphic | Position | Facing |
  |---|---|---|---|
  | Sailor | OBJ_EVENT_GFX_SAILOR | (4,29), on the dock | down |
  | Boat | OBJ_EVENT_GFX_MR_BRINEYS_BOAT | (4,31) | up, bow to the dock as on Route 104 |

- **Reachability:** every existing warp (Centre 14,23; Mart 26-27,23; houses 20,13 / 14,15 / 28,15), sign and NPC is untouched. The fisherman stays at (11,26) and still faces water at (10,26).

## Tileset addition: gTileset_TosaPort (approved, NOT applied yet)
Generator: `tileset_addition_batch1.py`. Close-up: `tosaport_addition_closeup_4x.png`, at 4x, with vanilla crates 0x32E/0x336 and pot 0x21B beside the proposed pieces. When applied, metatiles go into free slots only; no existing metatile or tile moves or changes. The pattern is `dev_scripts/cold_storage_tileset/export_exterior.py`.

**Pieces needed:**

| Piece | New metatiles | New tiles | Palettes | Collision / behaviour |
|---|---|---|---|---|
| Briney dock: Rustboro 0x33D, 0x26E, 0x345, 0x26D, 0x335, 0x276, copied as they are | 6 | 5 (Rustboro secondary tiles 0x230, 0x231, 0x240, 0x241, 0x250) | 0, 2, 4, 5 only: General's, so the colours are identical in TosaPort | planks walkable; sea end and face are water (MB_OCEAN_WATER), the boat's berth. Values from Route 104. |
| Crate on sand | 1 | 0 | crate tiles 0x28A, 0x28B, 0x29A, 0x29B on palette 7, over General sand 0x124 | solid, covered |
| Crate stack on sand | 1 | 0 | as above | solid, covered |
| Crate of fish | 1 | 2 (open crate top with two silver fish, 3/4 view) | palette 7 | solid, covered |
| Fishing rods, upright pair, 1x2 | 2 | 4 (left half drawn; the right half reuses it h-flipped) | palette 7 | base solid; top passable, layer normal so the tips draw over the player |
| Bucket (pail), Gen 3 3/4 view after the market pots 0x20C/0x21B: oval rim from above (~40% of the height) with blue water and a fish tail, handle lying back behind the rim, body narrowing to the base, lit from the upper left, shadow on the sand | 1 | 4 (shading is asymmetric, so no mirroring; sand bottom layer reused) | **palette 12**: palette 7 has no blue | solid, covered |
| **Total** | **12** | **15** | | |

Route 104's land-end column (0x32E/0x336/0x277) is not needed: +3 metatiles, 0 tiles, if the user wants it anyway.

**Room in gTileset_TosaPort:**
- **Metatiles:** metatiles.bin has 512 entries, the full secondary table. 124 of them are all-zero and unused by any layout: 0x202, 0x204, 0x230-0x231, 0x234, 0x238-0x239, 0x23C, 0x240-0x255 (part), 0x258-0x25D, 0x2E0-0x2EF, 0x2F2-0x2F7, 0x304-0x30F, 0x371-0x375, 0x389-0x395 (part), and more.
- **Tiles:** tiles.png holds 512 tiles, also full. 17 slots are referenced by no metatile and can be overwritten: 209-213, 263-266, 293, 294, 309, 325, 341, 357, 373, 389. 15 are needed, leaving 2.
- The station art at 0x3D0-0x3ED and its tiles are in use and untouched.

**Palette plan:**
- **No palette edits.** The dock uses only primary palettes (General 0-5), the same in every pair.
- **New art reuses TosaPort palette 7,** the existing crate palette, with only colours it already has:
  - 3 (200,200,216), 4 (144,136,160), 5 (64,72,104): silver fish, outline and eye
  - 6 (248,248,216): highlight / float white
  - 7 (216,200,144), 9 (136,112,72): wood / rod
  - 8 (168,160,104): sand shadow
  - 10 (232,56,32): float red
- **The bucket uses TosaPort palette 12** (existing; it has both greys and blues): 1 (64,72,104) outline, 7 (136,144,168) and 8 (184,192,208) metal, 10 (248,248,248) lip, 4 (104,160,208) and 3 (64,112,160) water.
- No free palette slot is needed.

## 2. Fisherman's hut interior: `sailor_hut_int.png`
- **Layout:** the vanilla LAYOUT_ROUTE104_MR_BRINEYS_HOUSE (Mr. Briney's cottage), taken unchanged from git (`1d1d50b3a2~1`). It was deleted from the working tree with the Hoenn maps, so it needs restoring as a new layout, e.g. LAYOUT_WAVEBREAK_TOWN_SAILORS_HUT (copy its map.bin and border.bin).
- **Size and pair:** 12x9, Building + GenericBuilding. **14 layouts share GenericBuilding:** HOUSE1-4, DEWFORD_TOWN_HALL, VERDANTURF_TOWN_WANDAS_HOUSE, PACIFIDLOG_TOWN_HOUSE1/2, FORTREE_CITY_HOUSE1/2, ROUTE116_TUNNELERS_REST_HOUSE, FORTREE_CITY_DECORATION_SHOP, ROUTE124_DIVING_TREASURE_HUNTERS_HOUSE, SAFARI_ZONE_REST_HOUSE.
- **Warps:** (5,8) and (6,8) lead to Wavebreak warp 6 at (13,29).
- **Objects:**

  | Object | Graphic | Position | Notes |
  |---|---|---|---|
  | Sailor | OBJ_EVENT_GFX_SAILOR | (5,4) | Briney's old spot; hidden while he waits at the dock |
  | Son | OBJ_EVENT_GFX_LITTLE_BOY | (9,5) | on the cushion by the table |

## 3. Eon Island = Southern Island: `eon_ext.png`, `eon_int.png` (as is, no tile edits)
- **Sizes and pair:** exterior 33x30 (odd width, vanilla), interior 27x24. Both are General + Rustboro. **5 layouts share Rustboro:** ROUTE116, SOUTHERN_ISLAND_EXTERIOR, SOUTHERN_ISLAND_INTERIOR, FARAWAY_ISLAND_ENTRANCE, UBE_CITY.
- **Exterior:**
  - The small boat replaces the S.S. Tidal object at the same spot, (13,25), facing up, with its bow on the dock face as on Route 104.
  - The Sailor reuses LOCALID_SOUTHERN_ISLAND_SAILOR at (13,23) on the gangway, with a new script.
  - The big concrete ferry dock stays.
  - Warps (14,5) and (15,5) lead to the interior; the sign is at (16,7).
- **Interior:**
  - **Lati spot (decided: Latias and Latios on separate visits, picked by time of day, replacing VAR_ROAMER_POKEMON):** the Lati lands at (13,11), over the Eon stone, where vanilla LatiApproach ends. The player stands at (13,12), and the trigger is the bg event at (13,11).
  - **Mega stones:** item balls on the bank flower patches, Latiasite (ITEM_LATIASITE) at (8,8) and Latiosite (ITEM_LATIOSITE) at (18,8).
  - **Exits:** (13,18) and (14,18).
- **Script note:** the Lati script needs FLAG_ENABLE_SHIP_SOUTHERN_ISLAND set, or it shows only the sign text.

## 4. Fullmoon Island: `fullmoon_ext.png`, `fullmoon_int.png`
- **Pair:** General + Rustboro for both maps, shared with the 5 layouts listed for Eon Island.
- **Exterior (32x24):**
  - The island follows the Platinum shape: forest to the north, a terrace on the west, a dock notch at bottom-left, and a flower meadow at bottom-right.
  - **Rim:** the Southern/Faraway rock rim drops straight into the sea. It was learned from those two maps, with the grass lip 0x002 on the north coast.
  - **Trees:** 1-wide General forest (0C6/016).
  - **Pier:** Route 104's wooden pier at x10-13, y15-17; the land end is at x13.
  - **Ledge:** a one-way ledge (0D5/087/0D6) at y17 stands in for Platinum's inner terrace.
  - **Warps:** (20,6) and (21,6), at Southern Island's dark forest-path cells, lead to the interior.
  - **Objects:**

    | Object | Position | Facing |
    |---|---|---|
    | Sailor | (11,16), on the pier | down |
    | Boat | (11,18) | up |

- **Interior (24x20):**
  - A ring of 2x2 Petalburg Woods trees around a clearing, with flowers and an irregular pond in Southern Island's pond set.
  - **Cresselia:** OBJ_EVENT_GFX_SPECIES(CRESSELIA) at (11,7) on the west bank, facing the pond.
  - **Exits:** Southern Island interior's tree path, with warps at (12,14) and (13,14).

## 5. Newmoon Island: `newmoon_ext.png`, `newmoon_int.png` (+ `*_shade_sim@2x.png`)
- **Pair:** General + **Dewford** for both maps. **Dewford is shared by** DEWFORD_TOWN (Orchid), BIRTH_ISLAND_EXTERIOR, NAVEL_ROCK_EXTERIOR and FURONG_VILLAGE; in git also Routes 105-107. Cells come from vanilla Dewford Town (git), Routes 105/107, Southern/Faraway Island (rim and rock) and Route 104 (shore).
- **Exterior (32x26):**
  - **Terrain:** sand ground with Dewford's dark 1-wide trees (243/239/23A) to the north-west. There are two rock plateaus (the General rock massif, auto-tiled from Southern Island, Faraway Island and Route 120) and General boulders (0E2).
  - **Rim:** the same rock rim into the sea as Fullmoon.
  - **Shape:** the island runs off the top edge, as Southern Island does, because the rock rim has no north-facing edge for sand.
  - **Dock:** a bay at the bottom right, with Dewford's wooden pier at x16-19, y15-16.
  - **Warps:** (10,6) and (11,6), at the forest gap, lead to the interior.
  - **Objects:**

    | Object | Position | Facing |
    |---|---|---|
    | Sailor | (18,15), at the pier tip | right |
    | Boat | (20,15) | left, bow to the pier |

- **Interior (28x22):**
  - A ring of Dewford trees around a sand clearing, a rock crater wall with a gap at x13-14 y13-14, and a pond with sand-shore edges in the middle.
  - **Darkrai:** OBJ_EVENT_GFX_SPECIES(DARKRAI) at (13,10), standing in the pond.
  - **Exits:** (13,21) and (14,21).
- **Darker than Fullmoon, without editing palettes:**
  - The content is bare sand, rock and boulders, with darker 1-wide trees and no flowers or grass.
  - The map header weather should be WEATHER_SHADE (or WEATHER_FOG_HORIZONTAL, as on Mt. Pyre). `*_shade_sim@2x.png` is a rough preview of the shade; the real effect is a run-time palette tint. Day/night (OW_ENABLE_DNS) is off in this repo.

## Known seams (the `seams()` checker in voyage_compose)
These are pairs of cells that never sit side by side in vanilla:
- **Fullmoon exterior:** the north lip 0x002 sits directly above forest 0C6.
- **Newmoon:** sand (0x124) sits directly against rock-rim and rock-massif edges. In vanilla that rock always borders grass or the sea.
- **Wavebreak:** the house touches sand. The proposed dock, crate and rod cells are overlays, so the checker does not see them.

They look acceptable at mockup scale. Fix them cell by cell when the maps are built for real.

## Decided (user, after review)
1. **Wavebreak dock:**
   - Mr. Briney's wooden dock (Route 104) replaces the concrete jetty, at the user's request. It needs an additive TosaPort tileset change.
   - More fishermen go along the west shore, with crates of fish, fishing rods and buckets (proposed metatiles). See "Tileset addition".
2. **Sailor:** the voyage Sailor is a new object. The existing sailor NPC at (12,18) stays as he is.
3. **Hut:** uses the red-roof house (House 1's original art) so it stands out.
   - House 1 (x19-22, y10-13) and House 3 (x27-30, y12-15) are repainted as House 2's purple TosaPort house (a 4x4 metatile copy), so the hut is the only red roof.
   - Doors stay in column 1, so the warps at (20,13) and (28,15) are unchanged.
4. **Eon Island:** Latias and Latios come on separate visits, chosen by time of day. Item balls go on the banks at (8,8) and (18,8).
5. **Eon dock:** the S.S. Tidal's concrete dock stays, with the small boat at the gangway (13,25).
6. **Newmoon pair:** General + Dewford, with WEATHER_SHADE in the header.
7. **Newmoon shape:** the island runs off the top edge of the map, as Southern Island does.
8. **Fullmoon terraces:** a single one-way ledge stands in for the inner terraces.
9. **Map ids:**
   - MAP_WAVEBREAK_TOWN_SAILORS_HUT, a new layout restored from LAYOUT_ROUTE104_MR_BRINEYS_HOUSE
   - MAP_FULLMOON_ISLAND and MAP_FULLMOON_ISLAND_INTERIOR
   - MAP_NEWMOON_ISLAND and MAP_NEWMOON_ISLAND_INTERIOR
   - Eon Island reuses MAP_SOUTHERN_ISLAND_EXTERIOR and MAP_SOUTHERN_ISLAND_INTERIOR.
