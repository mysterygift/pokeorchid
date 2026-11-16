# Tosa Rail — design log

Mockups for train travel between visited stations. Uses the Orchid UI kit
(`ORCHID_UI_KIT`, default `../pokeorchid-satchel/dev_scripts/orchid_ui`; the kit is imported, not copied).
Review page: `out/review.html`. Rebuild everything with `PYTHON=<python with Pillow> ./build_all.sh`.

## Status
- **Approved after round 2** ("Use your suggestions"). Assets are exported by `export_station_map.py`
  from `network.json`; the asset ↔ C contract is in `IMPLEMENTATION.md`.
- Scope change during v1: the overworld train art is owned by the engine-side session
  (`graphics/train/train.png`). These scripts only *read* it for the storyboard and never write to `graphics/`.

## Decisions (user, round 1)
1. Unvisited stations: **names shown greyed** (not "???").
2. After the player alights, **the train leaves**.
3. **Layout A** (line diagram). Follow-up asked: how a bigger map looks and whether it pans to frame the
   selected station. Answered in round 2 below.
4. **The train is always parked** at the boarding platform when a station is picked (no arrive-first).
5. **The cursor skips greyed stations.** Shake + message only when nothing visited lies in that direction.
6. **Rides are free, but need the RAIL CARD key item.** The engine checks it before the map opens; the map
   UI itself is unchanged.

## Decisions (user, round 2 — "Use your suggestions")
1. Layout A, scrolling **dead zone + re-centre** camera.
2. **Red Gen 3 chevrons** on tube exits (no mini-map).
3. Station **labels baked into BG2** tiles (grey/selected = palette swaps).
4. **Cone D-pad picking:** nearest accessible station in a 90° cone, preferring a shared line.
5. Design the real network to fit a **512×256** canvas.

## Files
| File | Makes |
|---|---|
| `common.py` | kit import, 1x/3x still + GIF savers, ROM sprite loaders (Brendan, NPCs, region-map head), keypad A/B glyphs |
| `station_map.py` | map renderer: network data, line art, nodes/ring/head OBJs, tray, confirm popup, layout B |
| `mock_station_map.py` | stills `map_a_default`, `map_b_telok`, `map_c_confirm`, `map_d_denied`, `map_alt_list` (1x + 3x), `map_ab_3x.png` |
| `anim_station_map.py` | `map_nav_3x.gif` (cursor travel, denied shake, confirm) |
| `journey_scene.py` | mock platform scene (2 stations) + read-only loader for `graphics/train/train.png` |
| `anim_journey.py` | `journey_3x.gif`, `journey_storyboard.png`, `journey_timing.txt` |
| `big_map.py` | round 2: 13-station network on a 512x256 canvas, camera rule, edge chevrons, header mini-map option, BG2 budget |
| `mock_big_map.py` | `big_1_open`, `big_2_telok`, `big_3_koru`, `big_4_rule`, `big_5_minimap` (1x + 3x), `big_overview_2x.png`, `big_nav_3x.gif` |
| `review_page.py` | `out/review.html` (self-contained, round 2) |
| `network.json` | **source of truth** for the real station map (stations, lines, edges, label anchors) |
| `export_station_map.py` | ROM asset exporter → `graphics/train_map/*`, `src/data/train_station_map.h`, `out/export_check_*_3x.png` |
| `IMPLEMENTATION.md` | asset formats, palette roles, rects, timings, camera and cone rules for the C screen |

## Choices made
- **Line diagram, not region art.** Tubes at 0/45/90° on the kit grid backdrop (BG3). Each tube is 6px:
  1px ink outline, light top/left edge, face, dark bottom/right edge (Gen 3 three-step ramp).
- **Line colour = BG palette swap.** Tube tiles are drawn once with the kit ACCENT roles. Each segment's
  cells pick pal 0 orchid (RIDGE line), pal 1 sea (COAST line) or pal 2 grey (segment touching an unvisited
  station). Visited state therefore costs no extra tiles.
- **Node centres on 8px cell centres (8k+4)** so a 6px tube fits inside one cell row or column, and two
  line colours never share a cell. The junction cell is covered by the node OBJ.
- **States:** visited node = white disc. Unvisited = grey disc, greyed name (INK_SOFT) and grey track, and
  the cursor skips it. Selection = gold ring OBJ on the node + gold pill behind the name (no ▶).
  Current station = region-map player head (`graphics/pokenav/region_map/brendan_icon.png`) above the node.
- **Labels in the small font** (white with INK shadow) directly on the grid. The tray uses the normal font for the name
  and the small font for the line name and hints.
- **Tray** = bag/dex tray (stitched seam, text clears it). Hint row uses the ROM's own `{A_BUTTON}`/`{B_BUTTON}`
  glyphs from `graphics/fonts/keypad_icons.png`, recoloured to the kit (accent cap, white letter).
- **Header** = dex-style accent band: train-front pictogram + "TOSA RAIL" + line legend (COAST / RIDGE).
  The legend tubes must be OBJs, because their cells sit in the orchid-palette band.
- **Confirm** = standard Orchid dialogue box + std-frame YES/NO, gold pill on the choice (approved kit rule).
- **Denied input:** D-pad toward a direction that only has unvisited stations. The ring shakes
  (+2,+2,0,-2,-2,0 ×2 = 12 frames), a grey ring blinks on the target (4 on / 4 off, 36 frames), the failure
  buzzer plays, and the tray shows "You haven't been to X yet. / Visit it on foot first." until the next input.
- **Cursor travel:** ring slides 8 frames, ease-out. The pill and tray update when it arrives (same idea as the
  bag's pocket ring).
- **Layout B (alternative):** pill list in line order (line-coloured cap, greyed rows, head on the
  current row) + mini diagram in a recessed well. Kept as the fallback for a larger network.
- **Network (placeholder):** COAST line TOSA PORT – MARIS BAY – VALE JUNCTION – KORU CITY. RIDGE branch
  VALE JUNCTION – TELOK TOWN – ASHEN PASS. Visited in the mockups: TOSA PORT, MARIS BAY, VALE JUNCTION, TELOK TOWN.

## Journey storyboard
- Fixed camera. Scene rows: 0 canopy (the name board hangs here so a parked train doesn't hide it),
  1–2 wall, 3 track, 4 platform edge (boarding row), 5–9 paving.
- Train from `graphics/train/train.png` (64x256: rear car, boarding car shut, loco, boarding car open),
  shown as [0][1][2] left→right. Door at x 88–103 from the train's left edge. Train top = track row y + 16 − 64.
  `trainX = playerTileX*16 − 88`.
- Engine timings used as given: door 12f (shut→open swap at frame 6), player step 16f, depart 80f ease-in
  (to left edge x = 240), arrive 96f ease-out (from x = −192), settle 16f. The other beats (idle 40, door
  hold 8, hide 8, wait 24, fade 16, black 16, fade-in 16, wait 20, alight appear 8, leave wait 30, end 60) are
  proposals, listed in `out/journey_timing.txt`. Ease curves here are quadratic; the C curves may differ.
- Boarding: the player walks 1 tile north from the edge row into the open door (drawn over the train), then
  is hidden. Alighting is the reverse, facing down.

## Budget (map screen)
- BG2 art: 23 unique 4bpp tiles (lines + header + tray, flip-deduped).
- BG palettes: 0 orchid, 1 sea, 2 grey, 3 grid; 13–15 text and frames unchanged.
- OBJ: 6 nodes + gold ring + grey ring + head = 9 OAM (16x16), +2 for the legend tubes. 2 OBJ palettes.
- The gold name pill is blitted into the BG0 text window like the YES/NO pill (custom cursor routine).

## Round 2 — bigger map (scrolling)
- **Placeholder network:** 13 stations, 3 lines, 3 interchanges, on a 512x256 canvas.
  COAST (teal): TOSA PORT – MARIS BAY – VALE JUNCTION – SALT FLATS – KORU CITY – CORAL END.
  RIDGE (purple): VALE JUNCTION – TELOK TOWN – ASHEN PASS – CINDER PEAK – GALE POINT.
  FOREST (green, `rail_forest` theme): ELDER WOOD – MOSS HOLLOW – TELOK TOWN – FERN GATE – KORU CITY.
  Interchanges use a ringed node; the tray lists every line ("RIDGE + FOREST LINES").
- **Viewport** = the 240x112 strip between the fixed header (y 0–15) and the fixed tray (y 128–159).
- **Camera rule: dead zone + re-centre.** The dead zone is 48px in from the left and right, 24 from the
  top, and 32 from the bottom (so the label under a node fits). While the selected station is inside it,
  the camera holds. When it lands outside, the camera eases 16 frames (ease-out) to centre that station,
  clamped to the canvas. The ring travels 8 frames at the same time. On open, the camera centres on the
  cursor (clamped). Why: neighbour hops don't move the diagram; a full re-centre gives context on every side.
- **Off-screen hint: red Gen 3 chevrons on tube exits** (6x9 `SMALL_ARROW`, rotated for up/down) wherever
  a tube crosses the viewport edge, bobbing 1px every 16 frames. The alternative, a 32x16 header mini-map
  at 1/16 with a gold viewport box, was mocked and not recommended: too small, and it displaces the legend.
- **Layers:** BG0 fixed text; BG1 fixed chrome (header band, tray, window frames); BG2 the diagram
  (64x32 map, `BG2HOFS = camX`, `BG2VOFS = camY − 16`); BG3 grid following the pan + drift. OBJs at
  priority 1 (nodes, ring, head, chevrons); gold name pill OBJ at priority 2 behind BG2 so the baked
  label text draws on top. WIN0 = the map viewport, with OBJs only inside.
- **Labels baked into BG2 tiles** at screen open. Greyed = pal 3 (WHITE role set to the INK_SOFT colour);
  selected = pal 4 (WHITE set to INK, INK set to SELECT_DARK). No label cell may contain tube pixels;
  `big_map.budget()` checks this (0 conflicts).
- **Budget:** 187 unique BG2 tiles (tubes + labels, of which 176 are label cells), 4 KB tilemap. BG pals
  0 orchid, 1 sea, 2 forest, 3 grey, 4 selected label, 5 grid; 13–15 as usual. OAM about 27 (13 nodes,
  ring, grey ring, head, pill ×2, ≤6 chevrons, 3 legend tubes).
- **Limits:** a text BG is at most 512x512 (64x64 map) without streaming, which fits about 40 stations at
  this density. Recommend designing the real network to fit 512x256.
- Journey storyboard rebuilt with the final `graphics/train/train.png` (read-only); parked at start, leaves after alighting.

## Open questions (round 2, with recommendations) — see review page
1. Camera: dead zone + re-centre vs always centre → dead zone + re-centre.
2. More-map hint: chevrons vs header mini-map → chevrons.
3. Labels baked into BG2 vs OBJ text → baked into BG2.
4. D-pad picking on a big network → nearest visited station in a 90° cone, preferring the same line.
5. Canvas size for the real network → fit 512x256; 512x512 only if needed; split into regions beyond that.
