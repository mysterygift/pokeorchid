# Voyages core stream: done

Worktree `../pokeorchid-voy-core` (detached from `voyages` bc3f480c7c). Nothing is committed. The final normal
`make -j8` is clean; `grep gHarnessKeys pokeemerald.map` returns 0.

## What changed
- **Voyage system**: `src/voyages.c`, `include/voyages.h`, `include/constants/voyages.h`, 4 specials appended to
  `data/specials.inc`, shared Sailor script `data/scripts/voyages.inc` (included in event_scripts.s).
  - `sVoyageDestinations[]` holds the passcode, unlock flag, arrival map/x/y and the legendary hide/caught flags.
    Codes are matched case-insensitively against gStringVar2 after `special EnterCode`.
  - `Voyage_CheckCode`: VAR_RESULT is the destination or VOYAGE_DEST_NONE, VAR_0x8005 says whether it was newly
    unlocked, and gStringVar1 holds the name.
  - `Voyage_BuildMenu`: pushes entries for `dynmultistack`. It lists only unlocked destinations, never the one
    you're at. Away from Wavebreak it lists only built ones. "Enter a code" appears only at Wavebreak; "Cancel"
    always does.
  - `Voyage_IsDestinationOpen`: for an unbuilt destination the Sailor says "too rough just now".
  - `Voyage_Depart` (waitstate): clears the destination's hide flags unless that legendary was caught, then runs
    DoSeagallopFerryScene.
  - **Hook for Sevii / Holon**: set `.arrivalMap/.arrivalX/.arrivalY` in their table entry. It is currently
    MAP_UNDEFINED.
  - `IsVoyageMapSec()` covers [MAPSEC_ONE_ISLAND, MAPSEC_SPECIAL_AREA) plus MAPSEC_EON_ISLAND. `IsTiksiMapSec`
    (include/regions.h) excludes these, so voyage maps never set FLAG_VISITED_TIKSI.
  - The Tiksi exporter's `kanto_block` now stops at MAPSEC_ONE_ISLAND, so Tiksi won't allocate or clear voyage
    slots.
- **Cutscene** (`src/seagallop.c`): VAR_0x8004 = SEAGALLOP_VOYAGE_OUTBOUND/INBOUND (200/201) switches to
  `graphics/seagallop/briney_boat.png`, which is Briney's boat side frame at 2x (64x64, NPC_3 palette). The wake
  is kept. Outbound travel is eastbound and inbound westbound, and the warp comes from `Voyage_SetArrivalWarp`.
  The FRLG Seagallop path is unchanged.
- **Flags**:

  | Flag | Use |
  |---|---|
  | 0x2B-0x2F | FLAG_VOYAGE_EON/SEVII/HOLON/NEWMOON/FULLMOON |
  | 0x3A-0x3D | FLAG_CAUGHT_VOYAGE_LATIAS/LATIOS/DARKRAI/CRESSELIA |
  | 0x3E/0x3F | FLAG_HIDE_EON_LATIAS/LATIOS |
  | 0x68 | FLAG_HIDE_NEWMOON_DARKRAI |
  | 0xE9 | FLAG_HIDE_FULLMOON_CRESSELIA |
  | 0x450 | FLAG_ITEM_EON_ISLAND_LATIASITE (was ROUTE_123_ULTRA_BALL, aliased) |
  | 0x451 | FLAG_ITEM_EON_ISLAND_LATIOSITE (was ROUTE_126_GREEN_SHARD, aliased) |

  Routes 123 and 126 can't be reached from Tosa Port (BFS). VAR_UNUSED_0x408B is not used.
- **Map sections** (region_map_sections.json, aliases added):
  - SOUTHERN_ISLAND becomes MAPSEC_EON_ISLAND "Eon Island".
  - NAVEL_ROCK_FRLG becomes MAPSEC_NEWMOON_ISLAND.
  - BIRTH_ISLAND_FRLG becomes MAPSEC_FULLMOON_ISLAND.

  Names are in title case, matching Orchid (the brief said "EON ISLAND"). No region-map art or layout was
  touched.
- **gTileset_TosaPort**: 12 metatiles were appended at 0x2E0-0x2EB and 15 tiles at local slots
  d1-d5, 107-10a, 125, 126, 135, 145, 155 and 165. Every one of those slots was all-zero and unreferenced. No
  palette was edited.
- **Wavebreak**: the patch was computed against HEAD and only the changed cells were written. It covers:
  - the SW beach, dock and props
  - the hut and the purple roofs
  - one extra fix, below
  - the hut door warp 6 at (13,29)
  - the dock Sailor and boat, hidden with FLAG_TEMP_1 before FLAG_SYS_GAME_CLEAR
  - three fishermen with the NOTES lines
- **New group gMapGroup_Voyages** (after Tiksi):
  - WavebreakTown_SailorsHut: Briney's house from git
  - NewmoonIsland and NewmoonIsland_Interior: WEATHER_SHADE
  - FullmoonIsland and FullmoonIsland_Interior

  Generators: `build_core_maps.py` (tileset + layouts) and `build_core_events.py` (events, scripts and
  registration). `mapcheck.py` handles collision dumps and walking paths. `make_boat_sprite.py` makes the
  cutscene boat.
- **Eon** (SouthernIsland_*): the boat replaces the S.S. Tidal, and the vanilla Sailor runs the voyage script.
  - Inside, `gettimeofday` gives Latios at TIME_NIGHT and Latias otherwise, with the vanilla fly-in cutscene.
  - Battles use setwildbattle Lv70 and BattleSetup_StartLegendaryBattle. The Champion is Lv55-58.
  - The Latiasite (8,8) and Latiosite (18,8) balls use FLAG_TEMP_3/4. They appear only after their Lati is
    caught, and they appear right after the catch.

## Deviations (needed for the maps to work; the mockups were never walked)
1. **Wavebreak tree removed.** With the hut on x12-15 y26-29, the user's 2x2 tree at x16-17 y30-31 walled in the
   hut door; only the Route 312 edge led in. That tree is gone, and 6 cells at x16-17 y29-31 are now grass with
   crown peeks.
2. **Dock elevation.** Route 104's pier planks are at elevation 4 and were changed to 3 at Wavebreak and
   Fullmoon.
3. **Fullmoon access.** Cell (13,14) became grass, because the rim autotiler had cut off the pier.
4. **Newmoon plateau.** It is trimmed from x10-15 to x10-14 so the pier's land end connects.
5. **Newmoon entrances.** General+Dewford has no sand or forest-gap metatile with a warp behaviour. The
   entrance (10,6)/(11,6) and exit (13,21)/(14,21) are therefore coord triggers that `warp`, and arrival is at
   (10,7) and (13,20).
6. **Darkrai position.** Darkrai is at (13,13) in the crater gap, not (13,10) in the pond. An object on water
   takes the water's elevation and can't be talked to from shore.
7. **Sailor placement.** After the Champion the Sailor waits at the dock and his hut copy is hidden, following
   the approved NOTES. Before that, the hut Sailor gives the flavour/refusal line and the Son has lines for both
   states.

## Verification (headless, copy of the JAXSON save; shots in shots/)
- Hut: the Sailor refuses before game clear (01) and the Son speaks (02). Before game clear the dock has no
  Sailor or boat (03, 06). After clear the hut Sailor is gone (04) and the dock pair appears (05).
- Codes: "WRONGCODE" is rejected (13). `souldew` works in lower case (14), as do NightMare, LUNARWING,
  seagallop and Delta. Re-entering SOULDEW gives "already charted" (17).
- Menus:
  - At the start it shows only Enter a code and Cancel (11).
  - It then grows with each code (15, 16).
  - The island menus offer only built destinations (62, 63).
  - Sevii gives "too rough" (18).
- Voyages: Wavebreak to Eon (20-22), Eon to Wavebreak (45), Wavebreak to Newmoon (50/51), Newmoon to Fullmoon
  (55/56), Fullmoon to Newmoon, Newmoon to Wavebreak, Eon to Fullmoon. Each one has the boat cutscene and lands
  at the dock.
- Eon:
  - In the evening, Latias Lv70 (32) is caught, which sets CAUGHT_LATIAS and HIDE_LATIAS; the Latiasite ball
    appears (33) and is taken, setting its item flag.
  - With the RTC at 23h, Latios Lv70 appears (42). After fleeing it is hidden and the trigger shows the sign.
  - Sail home and back: the hide flag is cleared and Latios returns (46). After it faints it is hidden again.
- Darkrai: flee, then it returns after the next voyage, then faints. Cresselia: caught, and it stays gone on a
  later voyage. FLAG_VISITED_TIKSI stays 0 on Eon, Newmoon and Fullmoon.
- The test ROM came from `harness_test_build.sh`: a temporary patch gives 5 Master Balls on arrival, and
  src/voyages.c is restored afterwards.

## Known gaps
- Newmoon's WEATHER_SHADE and the cutscene can't be judged for colour: the renderer has no blending. Not
  checked in the real emulator.
- Fullmoon's pond is Southern Island's walkable puddle set (MB_PUDDLE), as in the mock.
- No region-map art, cursor cells or Fly entries for Eon, Newmoon or Fullmoon; their sections have width 0, so
  the map falls back. These belong to the region-map stream.
- The disk is nearly full (about 2.7 GB free, and briefly ENOSPC). I deleted my scratch harness ROMs. The JSON
  diffs are minimal and keep the existing formatting.
