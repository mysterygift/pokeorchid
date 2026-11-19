# Sailor's Voyages, batch 2 (v2): Sevii Islands 1-3, translated from the real FRLG maps

These are mockups only. Nothing under data/, src/, include/ or graphics/ was changed.

v2 replaces the hand-composed v1. The v1 files are now:
- outputs: `out/batch2_v1/`
- specs: `specs_batch2_v1.py`
- renderer: `mock_batch2_v1.py`

Every map below is the **FRLG map itself**, read from git `8ee39561d7~1` (layout + map.json; the FRLG tilesets are still in data/tilesets). Each one is redrawn cell for cell in an Emerald tileset pair at the **same width and height**, with FRLG's events.

Each map has:
- `<map>_vs_frlg.png`: FRLG original on the left, translation on the right, same scale
- `<map>.png` / `@2x.png`: the translation with marks
- `<map>_spec.json`: the voyage_compose spec plus a report of buildings, caves, connections, warps and objects

Marks:
- blue = warp
- orange text = map connection, placed on the stretch of edge the neighbour covers
- yellow = NPC
- red = item ball
- pink double box = legendary / Pokémon object spot
- green = sign
- `h` = hidden item
- `smash` / `boulder` / `cut` = field-move objects (Emerald OBJ_EVENT_GFX_BREAKABLE_ROCK / PUSHABLE_BOULDER / CUTTABLE_TREE)

Regenerate (Pillow venv): `python dev_scripts/voyages/mock_batch2.py [FrlgMapName ...] [--seams]`. The tool is `frlg_translate.py`, documented in its docstring; batch 3 reuses it.

## Method (`frlg_translate.py`)
1. **Classify.** All 591 FRLG metatiles used by these 11 maps are sorted into 22 terrain classes. The heuristic uses:
   - the behaviour (MB_*), terrain and encounter bits
   - the collision each metatile has in the maps
   - colour fractions
   - `OVERRIDES` for the ones reviewed by eye: fence posts, pink cliff lips, boardwalk planks, cliffs standing in fast water, Berry Forest's autumn trees, the sandy road beyond an exit warp

   Review table: `out/frlg_translate/classes.png` (FRLG cell at 2x, class, Emerald cell) plus `classes.json`. Class counts: building 122, rock/cliff 98, sea 66, sea rock 46, grass 49, tree 45, path 45, sand 32, fence 21, pond 15, plank deck 12, ledges 14, flowers 6, signs 5, doors 4, waterfall 3, tall grass 2, stairs 2, cave 2, decor 2. **Unresolved: 0.**
2. **Buildings.** Building pieces come in every colour, so they are not classified directly. From each door warp, the tool floods the impassable cells above the door, splitting the area half-way to neighbouring doors.
   - **Footprint:** becomes ground.
   - **Stamp:** an Emerald/Orchid exterior goes in with **its door on FRLG's warp cell**: Orchid Centre / Mart / red-roof house (General primary), Mr. Briney's cottage for 5-wide houses, or the Pretty Petal shop.
   - **Leftovers:** impassable cells that belong to no door's building become rock.
3. **Seagallop harbours.** In FRLG each harbour is a south arrow warp at the end of a plank boardwalk, with the harbour building standing in the sea below it. The tool clears that building to sea and puts Southern Island's concrete ferry dock (the S.S. Tidal berth) there.
4. **Terrain.** The class grid goes through the voyage_compose autotilers:
   - beach shore for sand / sea
   - rock rim for land / sea (no grass lip under rock)
   - General rock massif for cliffs
   - Route 120 / 104 pond banks
   - 2x2 Petalburg Woods trees where they fit, 1-wide forest elsewhere
   - dirt-road 9-slice
   - ledges solved from vanilla neighbours
   - 0AF/0CF stairs
   - waterfalls: Route 119's General-primary falls; the pools they join become sea-type water. Every General pair has these cells; vanilla uses them on Routes 114 and 119, Meteor Falls, Ever Grande, Victory Road, Battle Frontier and Safari Zone
   - Route 104 pier planks for FRLG plank decks and bridges
   - Route 116's General cave mouth (09F over 0A7), or Jagged Pass's in Lavaridge
   - FRLG 1x1 sea rocks become Emerald 2x2 Route 104 rocks, kept at least 3 cells apart, so dense FRLG rock fields thin out
5. **Events.** Warps, connections, signs, hidden items and objects are kept at FRLG positions. FRLG-only overworld graphics (the IS_FRLG block of object_event_graphics_info_pointers.h) are swapped via `GFX_SWAP`:

   | FRLG | Emerald |
   |---|---|
   | SWIMMER_*_WATER / _LAND | SWIMMER_M/F |
   | BATTLE_GIRL / BLACKBELT | BLACK_BELT |
   | CAMPER / PICNICKER / HIKER _FRLG | Emerald versions |
   | WOMAN_1/2/3_FRLG | WOMAN_2/5 |
   | LITTLE_BOY / GIRL _FRLG | LITTLE_BOY / GIRL |
   | BIKER | CYCLING_TRIATHLETE_M |
   | BILL | SCIENTIST_1 |
   | BREAKABLE_ROCK / PUSHABLE_BOULDER / CUTTABLE_TREE _FRLG | Emerald objects |
   | MOLTRES, DODUO | OBJ_EVENT_GFX_SPECIES(...) |

## How FRLG links these maps (from the map.json files)
- **Edge connections (kept as FRLG has them):**

  | Map | Direction | Neighbour | Offset |
  |---|---|---|---|
  | One Island | right | Kindle Road | -120 |
  | One Island | down | Treasure Beach | 0 |
  | Two Island | up | Cape Brink | +24 |
  | Three Island | left | Bond Bridge | 0 |
  | Three Island | down | Three Isle Port | 0 |

  Treasure Beach and Three Isle Port were added to the scope because FRLG connects them.
- **Warps only:**
  - Kindle Road's top stairs (11-12,6) lead to Mt. Ember exterior (28-29,48).
  - Mt. Ember (29,7) leads to the summit (9,15).
  - Mt. Ember's caves: Summit Path 1F (14,24) and 3F (39,19), and Ruby Path (42,39). These are out of scope.
  - Kindle Road's Ember Spa is a cave door at (15,58), not a building.
  - Bond Bridge (12-13,6) leads to Berry Forest (42-44,41).
  - Three Isle Port has two Dunsparce Tunnel caves, (16,4) and (38,5).
- **Between islands: none.** One, Two and Three are linked only by the Seagallop: the harbour warps One (12,18), Two (10,8) and Three Isle Port (12,13) lead to `*_HARBOR`. Those are FRLG's Island Harbor rooms; Emerald already has that layout as LAYOUT_ISLAND_HARBOR, used by BirthIsland_Harbor and NavelRock_Harbor.
- **Proposed in-cluster link (least invented):** keep FRLG's arrangement. Each harbour warp goes to a clone of LAYOUT_ISLAND_HARBOR with a ferry NPC who hops One ↔ Two ↔ Three. The Sailor's small boat waits on One Island's boardwalk, from Wavebreak. No sea routes: v1's Sea Routes A/B are dropped.

## Tileset pairs (2 for the whole cluster)
| Pair | Maps | Other layouts using the secondary |
|---|---|---|
| General + **Rustboro** | One Island, Kindle Road, Treasure Beach, Two Island, Cape Brink, Three Island, Bond Bridge, Three Isle Port, Berry Forest | 5: ROUTE116, SOUTHERN_ISLAND_EXTERIOR/INTERIOR, FARAWAY_ISLAND_ENTRANCE, UBE_CITY |
| General + **Lavaridge** | Mt. Ember exterior, Mt. Ember summit | 12: LAVARIDGE_TOWN, JAGGED_PASS, FIERY_PATH, MAGMA_HIDEOUT_x8, DRAKE_BASE_CAMP |

- **Rustboro** covers everything the edge-connected maps need: Route 104 coast, shore and sea rocks, Briney's pier planks for boardwalks and Bond Bridge, the Southern Island ferry dock, Briney's cottage and the Pretty Petal shop, Petalburg Woods trees, and Route 116's cave mouth.
- **Lavaridge** gives the ash floor, stairs and cave doors, as you asked ("Mt Chimney tiles for Mt Ember"). Mt. Ember is reached only by warps, so no edge has to match. Its walls use the General rock massif, because Lavaridge's own cliffs are thin terrace lines and FRLG's thick walls became unreadable with them.
- Every edge connection joins two Rustboro maps, so the General-only edge rule never comes into play.

## Per map (all same size as FRLG)
| Map | Size | Buildings (door = FRLG warp) | Other |
|---|---|---|---|
| One Island | 24x20 | Centre (14,5) = FRLG's Pokémon Net Center building; house1 (19,9) cottage; house2 (8,11) cottage; harbour (12,18) dock | Sailor + boat added on the boardwalk; Bill → SCIENTIST_1 |
| Kindle Road | 24x140 | — | Ember Spa cave door (15,58); 15 Rock Smash rocks; 3 item balls; 140 FRLG sea-rock cells thinned to 2x2 rocks |
| Treasure Beach | 24x40 | — | One Island's dock continues into its top rows (as FRLG draws the harbour there); 8 hidden items |
| Mt. Ember exterior | 57x54 | — | 3 cave mouths; summit warp; Strength boulders / Rock Smash; Team Rocket pair |
| Mt. Ember summit | 19x22 | — | Moltres spot (9,6) marked; 4 boulders |
| Two Island | 48x20 | Centre (21,7); house (33,9) red-roof; Joyful Game Corner (39,9) Pretty Petal shop; harbour (10,8) dock | yellow market stall (no door) became rock bits |
| Cape Brink | 24x40 | house (12,16) cottage | **waterfall** at (11-13, 23-25) is Emerald's real animated MB_WATERFALL from Route 119 (General primary): lip 0BB/0B3/0BC, body 0B9, splash 02C/034/03C on the pool's top row; both pools it joins become sea-type water like Route 119's river; 3x crop under the side-by-side; 2 hidden items |
| Three Island | 24x40 | Centre (14,27); Mart (18,12); houses at (3,31), (4,6), (12,6), (13,19) cottage and (12,12) red-roof | biker gang + Doduo kept |
| Bond Bridge | 96x20 | — | FRLG's bridge is a short plank bridge (Route 104 planks); Berry Forest warps (12-13,6) |
| Three Isle Port | 48x20 | harbour (12,13) dock | 2 Dunsparce Tunnel caves |
| Berry Forest | 57x47 | — | yellow trees → Petalburg Woods trees; 3 exit warps (42-44,41); 15 hidden berries |

## Known seams (`--seams`)
- **What they are:** mostly rock-massif pieces in pairs vanilla never uses (075/07B, 075/120 ...).
  - The cause: FRLG's 1-2-cell cliff lines drawn with the General massif.
  - Also: 2x2 trees against rock, and fence ends.
- **Counts per map:** 37 (summit) to 455 (Berry Forest, mostly tree edges).
- **How they look:** they read fine at mockup scale (see the `_vs_frlg` PNGs). Fix by hand in Porymap when building.

## Decisions from v1 that still apply
- Centre and Mart interiors: clones of TelokTown_PokemonCenter_1F / TelokTown_Mart.
- The Sailor's boat (MR_BRINEYS_BOAT) waits at One Island.
- The ferry stand-in is the S.S. Tidal sprite: OBJ_EVENT_GFX_SEAGALLOP is FRLG-only.
- No legendary in scope. The Moltres spot is marked only.

## Review round 1 changes (2026-11-19)
These are applied in `frlg_translate.py` / `mock_batch2.py`, which now cover batches 2 and 3.

- **Pair:**
  - Every Sevii map that was on General + Rustboro is now on General + **gTileset_SeviiIslands**. That is a proposed Sevii-only copy of Rustboro (`sevii_tileset.py`), with the same metatile ids plus additions. Budget and close-ups are in `out/batch3/NOTES.md` and `out/batch3/tileset/`.
  - Mt. Ember stays on Lavaridge.
- **Cottage variants:** Briney-cottage houses rotate through `cottage`, `cottage_v1`, `_v2` and `_v3`, per map:
  - One Island: v1 (19,9), v2 (8,11)
  - Three Island: v3 (3,31), cottage (4,6), v1 (12,6), v2 (13,19)
  - Cape Brink: v3 (12,16)
- **Two Island market stall** is back at FRLG's spot. It is the 4x4 `market_stall` stamp at (27,1), and the clerk moves to (28,3) behind the counter. The proposed rare-goods stock list is in `out/batch3/NOTES.md`.
- **Arrow warps:** FRLG's arrow warps are kept on duplicate metatiles with MB_*_ARROW_WARP, labelled "(arrow S/N)" on the warp marks.
  - Harbours: One (12,18), Two (10,8), Three Isle Port (12,13).
  - Kindle Road → Mt. Ember (11-12,6).
  - Bond Bridge → Berry Forest (12-13,6).
  - Berry Forest exits (42-44,41).
  - Mt. Ember's arrow warps (28-29,48), (29,7) and the summit (9,15) sit on the shared Lavaridge tileset. They are listed but not duplicated; see question A.
- **Sea Routes A / B restored** (`sevii_sea_route_a/b*`, `sea_routes.py`). v1's routes were drawn for v1's hand-made islands, so these are rebuilt in v1's style (open sea, Route 104 rocks, a grassy islet with an item, swimmers). Each corridor is walled on both long sides by 2x2 sea rocks:
  - **A** (40x12): Kindle Road's east coast (left, offset −123) to Two Island's west sea (right, −1).
  - **B** (36x22): Two Island's south-west sea (up, −2), then down and east to Three Isle Port's west sea (right, +2).
  - **Check:** `sea_routes.check` passes. Every opening is passable sea on both sides, and nothing leaks outside the corridors.
  - **Sea rocks cleared** in front of the openings:
    - Kindle Road: (22,122), (22,125), (20,128), (22,130), (22,133)
    - Two Island: (0,4), (9,17), (12,18)
    - Three Isle Port: (0,12)
- **Freestanding rocks** (the user: "should just be continuous terrain"). FRLG's decorative one-cell boulders become Emerald's fixed General boulders, matched to the ground around them. FRLG's Rock Smash rocks were already objects; they stay objects and are now drawn with the Emerald breakable-rock sprite (OBJ_EVENT_GFX_BREAKABLE_ROCK, EventScript_RockSmash in the export).

| Map | Fixed boulders (cells) | Breakable-rock objects |
|---|---|---|
| Kindle Road | 0x0E1 (rocky dirt): (9,8) (13,10) (10,11). 0x0E2 (sand): (14,52) (12,57) (11,65) (13,68) (17,69) (16,70) (19,76) (15,79) (7,121). These were rock-massif chips before. | (8,104) (11,95) (12,96) (10,95) (9,105) (15,75) (9,84) (15,74) (15,73) (18,111) (10,86) (9,110) (18,112) |
| Mt. Ember exterior | 0x0E1, **flagged**: the ground is Lavaridge ash, which has no ash boulder, so 0x0E1 is the closest. Cells: (28,0) (30,1) (28,7) (31,8) (27,9) (31,10) (36,12) (34,13) (37,13) (40,13) (31,14) (34,15) (35,15) (40,15) (27,16) (36,16) (39,16) (18,17) (32,17) | (29,41) (30,42) (34,14) (36,15) (18,39) (19,40) |
| Mt. Ember summit | 0x0E1, **flagged** (ash): 27 cells around the crater, (7,8) … (12,15); full list in `mt_ember_summit_spec.json` → report.boulders | — |
| other batch-2 maps | — | — (Cut trees / Strength boulders also now drawn with their Emerald sprites) |

- **Batch 2 follow-ups (connection-edge rule):** none. Every edge connection now joins two SeviiIslands maps, including the sea routes, and Mt. Ember (Lavaridge) is reached by warps only.
- **Implementation export:** `frlg_translate.py export` writes real layouts and map.json files for every Sevii map. See out/batch3/NOTES.md, "Implementation".

## Decided (DECISIONS.md)
1. **Island link.** FRLG harbours plus the ferry (Briney's boat via the Seagallop ferry scene), **and** the invented sea routes, kept walled by sea rocks.
2. **Arrow warps** recreated with MB_*_ARROW_WARP duplicates in gTileset_SeviiIslands.
3. **Net Center.** One Centre on One Island (= Net Center).
4. **House art.** Cottages liked; slight variants added to the Sevii tileset.
5. **Joyful Game Corner.** The exterior is the Pretty Petal building; the interior is a Mauville Game Corner layout clone with NPC scripts tweaked at build time.
6. **Mt. Ember terraces** left as translated; the user repaints them later.
7. **Market stall** put back, as a rare-goods shop.
8. **Fast currents** become plain sea (invented routes between them).
9. **2x2 sea rocks** accepted.
10. **Out-of-scope interiors** translated from FRLG the same way. See `out/interiors/`: harbours, houses, Ember Spa, Summit/Ruby Path, Dunsparce Tunnel.
11. **Map ids** reuse the FRLG names.

## Open questions (recommendation first)
A. **Mt. Ember's arrow warps** sit on the shared Lavaridge tileset, so a duplicate metatile there would change a vanilla tileset.
   - **Recommendation:** make those three warp cells plain warps. Jagged Pass → Mt. Chimney does the same with its stairs.
   - The alternative is a Sevii-only Lavaridge copy.
B. **Mt. Ember boulders on ash** use 0x0E1, the rocky-dirt boulder, because Lavaridge has no ash boulder. Accept, or let the user's terrace repaint (decision 6) cover them.
