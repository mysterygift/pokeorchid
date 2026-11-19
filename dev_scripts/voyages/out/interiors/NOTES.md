# Sevii interiors — FRLG → Emerald translation mockups (decision 8)

Script: `dev_scripts/voyages/frlg_interiors.py` (houses, harbour, driver) + `interiors_caves.py` (learned cave
autotiler). Re-run: `<venv python> dev_scripts/voyages/frlg_interiors.py [key ...]`. Nothing in data/ src/
include/ graphics/ changed; no tileset edited; every cell is an existing metatile of the named pair.
Every room is FRLG's size; warps, objects, signs and coord events sit on FRLG's cells; collision + elevation are
FRLG's (houses: hand-checked, walk diff in each `_spec.json`). Per room: `<name>.png`, `@2x.png`,
`_vs_frlg.png` (FRLG | Emerald), `_spec.json` (grid, warps, objects with Emerald gfx, walk diff, seams, sharing).

## Rooms

| Output | FRLG map(s) | Size | Emerald pair | Method |
|---|---|---|---|---|
| `sevii_harbor` | ONE..SEVEN_ISLAND_HARBOR (7) | 17x13 | General + IslandHarbor | **clone**: FRLG Island Harbor *is* Emerald's `LAYOUT_ISLAND_HARBOR` (Birth Island / Navel Rock harbour) |
| `sevii_house3` | 15 maps on LAYOUT_HOUSE3_FRLG: ONE_ISLAND_HOUSE1/2, TWO_ISLAND_HOUSE, CAPE_BRINK_HOUSE, THREE_ISLAND_HOUSE2-5, FOUR_ISLAND_HOUSE1/2, FIVE_ISLAND_HOUSE1/2, SIX_ISLAND_HOUSE, WATER_PATH_HOUSE2, SEVAULT_CANYON_HOUSE | 11x9 | Building + GenericBuilding | hand class map (= vanilla HOUSE2 furniture) |
| `six_island_water_path_house1` | WATER_PATH_HOUSE1 (LAYOUT_HOUSE4_FRLG) | 11x9 | Building + GenericBuilding | hand class map |
| `three_island_house1` | THREE_ISLAND_HOUSE1 | 11x9 | Building + GenericBuilding | hand; Lab display case → glass cabinet |
| `four_island_loreleis_house` | LORELEIS_HOUSE | 11x9 | Building + GenericBuilding | hand; carpet → wood + HOUSE1 orange rug, bed, dolls |
| `four_island_pokemon_day_care` | FOUR_ISLAND_POKEMON_DAY_CARE | 12x9 | Building + PokemonDayCare | vanilla Route 117 Day Care (same room) + FRLG lower half |
| `seven_island_house_room1` / `_room2` | SEVEN_ISLAND_HOUSE_ROOM1 / ROOM2 | 11x9 / 12x9 | Building + GenericBuilding | hand; Room2 = e-Reader room |
| `one_island_kindle_road_ember_spa` | KINDLE_ROAD_EMBER_SPA | 27x39 | General + Lavaridge | learned autotiler, set *lava* + Lavaridge hot-spring water, General waterfall |
| `mt_ember_summit_path_1f/2f/3f` | SUMMIT_PATH_1F/2F/3F | 15x18 / 48x46 / 15x11 | General + Lavaridge | learned, *lava* (Fiery Path / Magma Hideout rock) |
| `mt_ember_ruby_path_*` (8) | RUBY_PATH_1F, B1F, B1F_STAIRS, B2F, B2F_STAIRS, B3F, B4F, B5F (everything reachable from 1F) | 6x7 … 31x23 | General + Lavaridge | learned, *lava* |
| `three_island_dunsparce_tunnel` (+ `_dug_out`, `_dug_out_alt_rusturf`) | DUNSPARCE_TUNNEL (+ its DUG_OUT layout, used once the National Dex is on = always post-game) | 30x7 | General + Cave (alt: General + RusturfTunnel) | learned, *cave* (Granite) / *rusturf* |
| `six_island_dotted_hole_1f`, `_b1f`…`_b4f`, `_sapphire_room` | DOTTED_HOLE 1F, B1F-B4F, SAPPHIRE_ROOM | 16x11, 13x11, 16x15 | General + NavelRock | learned, *navel* (Emerald Navel Rock; trained also on Granite Cave — same metatile arrangement) |
| `seven_island_sevault_canyon_tanoby_key` (+ `_alt_rusturf`) | SEVAULT_CANYON_TANOBY_KEY | 15x16 | General + Cave (alt: RusturfTunnel) | learned |
| `seven_island_tanoby_ruins_monean_chamber` (+ `_alt_ruins`) and the other 6 chambers | TANOBY_RUINS_*_CHAMBER (7) | 23x17 | General + Cave | learned, *cave* (alt: Sealed Chamber / Regi-tomb set) |

Chamber shapes: same frame, maze differs — collision differs from Monean in Liptoo 8 cells, Weepth 2, Dilford 8,
Scufib 6, Rixy 10, Viapois 2; all 7 rendered with the same method. Dotted Hole B2F/B3F/B4F differ from B1F in
7/3/4 collision cells (rock lumps) plus their warps / braille sign text.

Sharing (no tileset is edited, so nothing changes for them): GenericBuilding — HOUSE1-4, Dewford Hall, Wanda's,
Pacifidlog / Fortree / Tunneler / Diving / Safari houses; PokemonDayCare — Route 117 Day Care only; IslandHarbor —
LAYOUT_ISLAND_HARBOR only; Lavaridge — Lavaridge Town, Jagged Pass, Fiery Path, Magma Hideout x8, Drake Base
Camp; Cave — Granite / Shoal / Seafloor / Cave of Origin / ruins / Orchid's Mt. Batok, Mt. Drake, Challenger's
Trail, Damp Path, Frigo, shrines; NavelRock — Navel Rock x7; RusturfTunnel — Rusturf Tunnel only.

Excluded (decided earlier): Centres / Marts, Joyful Game Corner, Icefall Cave, Rocket Warehouse, Berry Forest,
Mt. Ember exterior. Not in the brief but reached by an outdoor warp: FIVE_ISLAND_RESORT_GORGEOUS_HOUSE (Selphy,
BuildingFrlg/Museum, 11x9), SEVEN_ISLAND_TRAINER_TOWER, ALTERING_CAVE (Emerald already has
LAYOUT_ALTERING_CAVE), LOST_CAVE (14 rooms), WATER_LABYRINTH, PATTERN_BUSH etc. are outdoor/other — left for a
later batch.

## Open questions (recommendation first)

1. **Harbours**: point all 7 maps at the existing `LAYOUT_ISLAND_HARBOR` (no new layout). Sailor moves from FRLG
   (8,6) to (8,5) and the boat from (8,9) to (8,7) (Birth Island's cells; FRLG's are pier / water in the Emerald
   room). *Recommend: yes.*
2. **House3 = vanilla LAYOUT_HOUSE2?** HOUSE2 is the same room minus FRLG's black bottom row (11x8). *Recommend
   the translated 11x9 (keeps FRLG door cell (4,7) and exterior warp ids); alternative: reuse HOUSE2 with the
   exit warp moved to row 7 — identical look.* All 15 maps share one layout as in FRLG.
3. **Exit mats**: FRLG 3-wide mat → Emerald 2-wide mat on x3-4 (x2-3 in WaterPath House1) with both halves
   warping (vanilla habit). *Recommend as drawn.*
4. **Lorelei's dolls**: Emerald has Pikachu / Jigglypuff / Meowth dolls (+ BIG_LAPRAS_DOLL 32x32); Wigglytuff,
   Seel, Slowpoke, Slowbro, Psyduck, Chansey, Nidoran♀/♂, Pidgeot, Fearow have no Emerald OW gfx (FRLG ones are
   invisible in this build). *Recommend: keep the 3 Emerald dolls + big Lapras, swap the rest for other Emerald
   dolls (or re-enable the FRLG Pokémon OW gfx).* Lorelei → Glacia gfx placeholder.
5. **Seven Island Room1/Room2** is the e-Reader trainer room (opens only via `setmaplayoutindex
   ..._DOOR_OPEN` when an e-Reader trainer is valid). *Recommend: drop Room2 and its warp; Room1 keeps a closed
   shelf wall.* Rendered anyway.
6. **Dunsparce Tunnel**: post-game the DUG_OUT layout is always used. Granite brown matches FRLG's colour but its
   rock mass is floor-coloured, so the tunnel reads poorly; Rusturf (Emerald's own dug-through tunnel) has the
   same raised-top structure and good contrast. *Recommend Rusturf (`_alt_rusturf`); also for Tanoby Key (its FRLG
   set is olive-green).* FRLG's rock-pile floor in the dug-out corridor is mostly solid and becomes rock mass —
   needs a hand pass for rock piles.
7. **Mt. Ember ladders**: Lavaridge has no ladder metatiles; mockup uses the wooden plank 0x2AE. *Recommend
   copying Cave's 0x23F / 0x217 ladder art recoloured into 2 free Lavaridge slots, or keep planks.* Rock stairs →
   Fiery Path plank stairs 0x2AF.
8. **Braille tablets / pedestals** (Ruby Path B4F/B5F, Dotted Hole rooms, Sapphire room): drawn as rocks / cracked
   floor (no braille slabs in Lavaridge / NavelRock). *Recommend: keep as sign events on rock lumps; or use Cave's
   Sealed Chamber braille pieces if those rooms move to General + Cave.* Ruby / Sapphire / Chansey OW gfx are
   FRLG-only (need gfx).
9. **Summit Path 2F** loses FRLG's decorative terraced crater (all solid → one flat plateau). *Recommend the user
   repaints it with Fiery Path plateau faces, as for the Mt. Ember exterior terraces (decision 6).*
10. **Tanoby chambers**: *Recommend General + Cave (brown ridge maze, main render)*; the Sealed-Chamber/ruins set
    (`_alt_ruins`) mixes in orange/purple ruin pieces. FRLG's yellow-brick back wall has no Cave equivalent.
11. **Dotted Hole** in Emerald Navel Rock cream instead of FRLG white-grey. *Recommend as is* (same tileset family).

## Remaining seams (unseen vanilla neighbour pairs, after the solver)
Houses 4-11 each (furniture next to different furniture than vanilla; all read fine), Lorelei 20 (bed on the
base row, rug next to the yellow table), Day Care 27 (lawn edges / table on lawn / black row; vanilla lawn has no
edge pieces). Caves: Ember Spa 103 (hot-spring water against cave rock never happens in vanilla — springs are
outdoors), Summit 2F 32, Ruby B3F 30, Dotted Hole 8-20 (NavelRock pairs learnt from Granite Cave count as unseen),
Tanoby 5-9, others ≤ 11. Exact cells in each `_spec.json` → `report.seams`.

Walk diffs vs FRLG: caves 0 (collision copied); houses 0 except Lorelei (0,2),(1,2),(0,3) solid under the 2-wide
bed (doll cells / dead corner) and Seven Room1 row 0 (unreachable wall row); harbour = Emerald's own walkway
(pier one row shorter, see Q1).
