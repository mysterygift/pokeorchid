# Tosa Rail (trains) — scripting reference

Code: `src/train_travel.c` (access rules, journey cutscene), `src/train_station_map.c` (station picker),
`data/scripts/train.inc` (shared script), station table `src/data/train_stations.h`.
Stations: `TRAIN_STATION_TOSA_PORT` (platform `TosaPort_BrendansHouse_2F`) plus the test stations
`TrainTestEast/North` (shared attendant + debug station master in `data/maps/TrainTestEast/scripts.inc`).
The Tosa Port gatehouse `TosaPort_BrendansHouse_1F` has the paid area at the back left: through the fare
gates (x 4), then the down escalator (warp (1,4)) to the platform's up escalator (warp (1,7)).

Concourse kit (gTileset_UrbanInterior 0x2B0+, `dev_scripts/station_tileset/concourse.py`): concourse wall,
tactile guide strips and blister pads, fare gate cabinet + gate closed/open (for a north-south gate line)
+ glass fence (east-west run), ticket booth (a small building: roof, fascia drawn over sprites, facade,
counter = MB_COUNTER), seats, exit mats, 2-wide rear exit arch and the train `StationSign`. The floor is
the platform's staggered paving (Paving_A on even rows, Paving_B on odd rows; the stock PC escalator
metatiles assume the same), so every floor prop has an `_A` and a `_B` version; the painter picks by row.
`export_tileset.py --paint-tosa-port` repaints the gatehouse and the Tosa Port platform (overwrites
Porymap edits to those two layouts).

Fare gates: the gate tiles are solid. Their bg events (`TosaGateway_FareGateNorth/South`) set the gate's
x/y in `VAR_0x8004/5` and run `TosaGateway_FareGate`: no Rail Card → refusal message; otherwise it swaps
in `FareGate_Gate_Open_B`, hides the follower, walks the player two tiles in the direction they face and
swaps `FareGate_Gate_B` back. A new gate on an even row needs the `_A` ids instead. TEMP: the ticket
booth clerk gives a Rail Card if you have none.

## Macros (`asm/macros/event.inc`)

| Macro | What it does |
|---|---|
| `usetrain` | Full flow: checks for `ITEM_RAIL_CARD`, says "Where would you like to go?", opens the station map, then boards → departs → warps → arrives. **Returns only if the player cancels or can't ride**; on departure the script never resumes. |
| `settrainstation STATION, MODE` | Sets a station's access. Clobbers `VAR_0x8004`/`VAR_0x8005`. |

`MODE` values:
- `TRAIN_ACCESS_OPEN`: usable now, even if never visited. Also clears "closed".
- `TRAIN_ACCESS_CLOSED`: greyed out as "closed right now", even if visited.
- `TRAIN_ACCESS_LOCKED`: back to the default (usable once visited). Clears both override flags.

Minimal attendant:
```
MyStation_EventScript_Attendant::
	lock
	faceplayer
	usetrain
	release
	end
```

## Specials (for custom flows)

| Special | In | Out |
|---|---|---|
| `TrainStation_CountDestinations` | — | `VAR_RESULT` = number of stations you can reach from here. **Also marks the current station visited.** |
| `TrainStation_OpenMap` (+ `waitstate`) | — | `VAR_RESULT` and `VAR_0x8004` = the chosen station, or `TRAIN_STATION_NONE`. If a station was chosen, the train is parked at the platform when the screen fades back in. |
| `TrainTravel_Depart` (+ `waitstate`) | `VAR_0x8004` = destination, `VAR_0x8005` = `TRUE` to make the train pull in first (story moments), `FALSE` if it's already parked | Never returns (warps). |
| `TrainStation_SetAccess` | `VAR_0x8004` = station, `VAR_0x8005` = mode | — (what `settrainstation` calls) |
| `TrainStation_BufferName` | `VAR_0x8004` = station | `STR_VAR_1` = station name |

Scripted ride to a fixed destination, with no picker (e.g. a story trip):
```
	lock
	hidefollower
	setvar VAR_0x8004, TRAIN_STATION_TEST_EAST
	setvar VAR_0x8005, TRUE      @ train arrives on screen first
	special TrainTravel_Depart
	waitstate
	end
```

## Constants (`include/constants/train_stations.h`)

- `TRAIN_STATION_*`: station ids (indexes into `sTrainStations`). `TRAIN_STATION_NONE` = 0xFF.
- Flags `0x40–0x4F`: one `FLAG_TRAIN_UNLOCK_*` / `FLAG_TRAIN_CLOSED_*` pair per station. The spare
  `STATION_3..7` pairs are there to rename when you add real stations (8 stations max before you need more flags).
- `ITEM_RAIL_CARD` (repurposed Rainbow Pass) is required to ride.

## Station states

A station is **closed** if its CLOSED flag is set. Otherwise it is **open** if its town's `visitedFlag`
or its UNLOCK flag is set. Otherwise it is **unvisited** (greyed out, "not visited yet").

## Gotchas

- **Platform layout:** the player must be standing *south* of the track. The train stops with its door
  on the player's column, and the player walks north up to the station's `trackY` row to board.
- **Arrival:** the player is warped onto (`trackX`, `trackY`), hidden, and then steps one tile south.
  That tile must be walkable platform.
- **Visiting = using the attendant.** `CountDestinations` "visits" a station by setting its UNLOCK flag.
  So `TRAIN_ACCESS_LOCKED` on a station with `visitedFlag = 0` also wipes that visit. Give real stations a
  `FLAG_VISITED_*` so that LOCKED behaves as you'd expect.
- `usetrain` always passes `VAR_0x8005 = FALSE`, because the picker has already parked the train. If you
  want the pull-in, call the specials directly.
- `usetrain` calls `hidefollower` for you. Do the same if you call `TrainTravel_Depart` directly.

## Adding a station

1. Add an id in `include/constants/train_stations.h` and bump `TRAIN_STATION_COUNT`.
2. Add a row in `src/data/train_stations.h`: name, map, `trackX/Y` (map tile, no `MAP_OFFSET`),
   `visitedFlag`, and the unlock/closed flags.
3. Rename a spare flag pair in `include/constants/flags.h`.
4. Add the station's node, label and edges to `dev_scripts/train_ui/network.json`, then regenerate the map art:
   `python3 dev_scripts/train_ui/export_station_map.py` (needs Pillow). Never hand-edit the generated
   `graphics/train_map/*` or `src/data/train_station_map.h`.
5. Put an attendant that runs `usetrain` on the platform.
