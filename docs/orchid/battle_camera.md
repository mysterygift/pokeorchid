# Battle camera (Mode 7 floor)

Orchid draws the battle environment as a perspective floor with a moving
camera, instead of the flat Gen 3 background. Code: `src/battle_mode7.c`.
Toggle: `B_MODE7_BATTLE_FLOOR` in `include/config/battle.h`.

## What the player sees

| Moment | Camera |
|---|---|
| Battle start | No split-screen slide. The camera pulls back from a rotated close-up while the letterbox opens; trainers and wild Pokémon wait as dark silhouettes and fade in when it lands. |
| Choosing an action | Slight orbit (~1.7°) around the centre of the battle. Opponents occasionally replay their send-out front animation (no cry). |
| "X used Y!" | Eases in on the attacker. |
| Move animation | Returns to the wide shot as the animation launches (animations use fixed battler coordinates). |
| A hit lands | Pushes in on the battler hit for ~50 frames. |
| Stat change | After the stat-change animation, focuses on that battler for ~60 frames. |

At rest the framing matches the classic backgrounds: platform ellipses
128x32 at (176,64) opponent and (64,117) player.

## How it works

- BG mode 1. The floor is affine BG2 (8bpp, 512x512, charblock 2,
  screenblock 26–27). BG0/BG1 stay text layers; BG3 is off.
- Every frame `ComputeLines` builds per-scanline BG2PA/PC/X/Y values;
  HBlank DMA0 streams them (`BattleMode7_VBlank`). Lines deeper than
  `M7_MAX_DEPTH` sample one flat texel ("haze") to hide texture repeats.
- The camera (`struct Mode7Camera`) is yaw (orbit about the platforms'
  midpoint) plus a lens: zoom about any screen point, and pan.
- Battler sprites (and trainers during the intro) are moved to stay on
  their platforms. Player-side sprites never move up, so back sprites stay
  hidden behind the text box.

### Falling back to the flat background

Some effects need text BG2/BG3 or DMA0: move backgrounds (`LoadMoveBg`),
battler-on-BG2 animations, scanline effects and terrain backgrounds. For
these the floor suspends to the classic 4bpp environment and resumes after
6 idle frames. The handoff hides BG2/BG3, loads the new background, and
only shows BG3 from the next VBlank (`BattleMode7_FinishBgLoad`), so
half-loaded VRAM is never displayed. Mode 7 also recovers by itself when a
menu (bag, party) re-initialises the battle video.

Not used in link or recorded battles, or for environments without a floor.

### Hooks in vanilla code

| File | Hook |
|---|---|
| `battle_main.c` | `BattleMode7_Update` (top of `BattleMainCB2`), `BattleMode7_VBlank`, `IsBattleInActionSelection`, wild-mon intro |
| `battle_intro.c` | `BattleIntroMode7` task, start after the classic slide |
| `battle_controllers.c`, `battle_gfx_sfx_util.c` | trainer silhouette intro (`SpriteCB_TrainerMode7Intro`) |
| `battle_script_commands.c` | focus on attack string, hit animation, stat-change animation |
| `battle_anim.c` | `ClearFocus` on animation launch, move-BG suspend, BG2 in the fade-to-BG blend |
| `battle_bg.c`, `scanline_effect.c` | terrain / scanline suspend |
| `battle_util2.c` | `BattleMode7_End` in `FreeBattleResources` |

## Tuning

All in `src/battle_mode7.c`:

| Define | Controls |
|---|---|
| `M7_INTRO_FRAMES`, `M7_INTRO_YAW`, `M7_INTRO_ZOOM` | intro fly-in length, start rotation, start zoom |
| `M7_SWAY_YAW`, `M7_SWAY_YAW_SPEED`, `M7_SWAY_ZOOM` | idle orbit amount, speed, breathing zoom |
| `M7_FOCUS_ZOOM`, `M7_FOCUS_YAW`, `M7_FOCUS_BODY_Y` | focus close-up |
| `M7_EASE_SHIFT`, `M7_EASE_SHIFT_FAST` | how quickly the camera eases (1/8, 1/4 per frame) |
| `M7_IDLE_ANIM_MIN`, `M7_IDLE_ANIM_RANGE` | how often idle front animations play |

The camera geometry (`M7_HORIZON`, `M7_HEIGHT`, `M7_FOCAL`, `M7_REST_*`,
platform positions in `include/battle_mode7.h`) is fitted to the classic
framing. Changing it means regenerating every floor.

## Environments

| Environment | Floor | At night |
|---|---|---|
| Grass | South Tosa Reserve: lalang meadow, stream, orchids (`orchid_grass`) | moonlit |
| Sand | East Coast beach: sea, foam line (`orchid_beach`) | foam catches the moon |
| Plain | HDB void deck: driveway, kerb, drain, puddles (`orchid_void_deck`) | fluorescent-lit tiles |
| Cave | limestone cave: darkness at the back, stalagmites, crystals, a patch of light from the roof (`orchid_cave`) | moonbeam; moss and crystals glow |
| Ruins | temple ruins: flagstones, steps to a laterite terrace, a fallen column; carved daises (`orchid_ruins`) | dais rims and glyphs glow |
| Office | CBD office: carpet tiles, desk banks, window light, walkway; round rugs (`orchid_office`) | monitors glow, desk lamps pool light |
| Mall | atrium: marble, shopfronts, granite band with brass, planters, spotlights; inlaid medallions (`orchid_mall`) | neon shop signs, spotlight pools |
| Jungle | rainforest: boardwalk, buttress roots, ferns, leaf litter, sun dapples; mossy clearings (`orchid_jungle`) | moonlight dapples, fireflies |
| Pond | Tosa Reservoir: reeds and lamp posts on the far bank, lily pads, glitter; pale shallows (`orchid_lake`) | moon path, lamp reflections |
| Long Grass | tall-grass test floor (`tall_grass/mode7_*`) | — |
| others | classic flat background | — |

### Choosing a floor for a map

Underground maps already use the cave floor, and surfing on a pond uses the
lake. For everything else, set the map's **battle scene** (Porymap: Header tab
> Battle scene, or `"battle_scene"` in `map.json`):

| Battle scene | Environment |
|---|---|
| `MAP_BATTLE_SCENE_CAVE` | Cave |
| `MAP_BATTLE_SCENE_RUINS` | Ruins |
| `MAP_BATTLE_SCENE_OFFICE` | Office |
| `MAP_BATTLE_SCENE_BEACH` | Sand (beach) |
| `MAP_BATTLE_SCENE_JUNGLE` | Jungle |
| `MAP_BATTLE_SCENE_MALL` | Mall |
| `MAP_BATTLE_SCENE_LAKE` | Pond (lake) |

A location scene applies to every battle on the map (wild, trainer, surfing),
for the graphics and for Secret Power / Nature Power / Camouflage. Gym leader,
champion, Frontier and legendary battles keep their own backgrounds.

### Night

Each Orchid floor has a second palette, `palette_night.pal`, over the same
tiles. `IsBattleNight()` (`src/battle_bg.c`) picks it when `GetTimeOfDay()` is
`TIME_NIGHT` (the RTC clock; evening still uses the day palette). Features meant
for night use palette slots that are dull or hidden by day (lamps, monitors,
neon, fireflies, glyphs) and light up in the night palette, so night costs no
extra tiles. `GetBattleEnvironmentPalette()` is the one place both the floor
and the flat fallback get their palette from.

### Adding or editing a floor

1. Add a theme to `tools/orchid/battle_envs.py`, then run
   `python3 tools/orchid/battle_envs.py all`. This writes, per environment,
   `mode7_floor.png` (512x512 source art), the runtime `mode7_tiles.bin` /
   `mode7_map.bin`, a classic `tiles.png` / `map.bin` / `palette.pal` /
   `palette_night.pal` rendered from the floor through the rest camera, and
   regenerates `src/data/battle_mode7_floors.h`. A theme returns its day
   palette and a night palette (`night_of()` grades the day palette and takes
   per-slot glow overrides).
2. Map the environment to its floor in `GetFloor` (`src/battle_mode7.c`),
   and point its `gBattleEnvironmentInfo` entry at the new background and
   palette (`src/data/battle_environment.h`, `src/data/graphics/battle_environment.h`).

Rules the generator enforces or assumes:

- At most 256 unique 8x8 tiles (no flips on affine BGs). Stamp the same
  platform design under both battlers at the same `(x % 8, y % 8)` so the
  tiles are shared; use tile-aligned decals and repeating bands.
- Only palette row 2 (indices 33–47). Rows 3–4 keep the original
  environment colours for the intro "entry" art.
- No single-pixel detail or checker dithers: they shimmer as the camera
  moves. Use solid bands and 2x2 marks. Draw upright detail (grass) about
  3x tall in texture space so it survives the perspective squash.
- Column 0 stays plain ground; the haze samples texel (4, 8).
- The tile budget is tight: the two platforms alone cost ~150-200 tiles.
  Background patterns must repeat in step with the platform offset
  (112, -192) so both platforms sit on the same pattern (e.g. stones 56 wide,
  32 or 48 tall), and scenery should be stamps at 8-aligned origins on plain
  ground (`blob`, `fill_rect`, `decals_on_plain`). Only about 23 screen rows of
  the far floor (v 40-146) and the strip left of the opponent (u 124-250,
  v 146-272) are visible at rest; put each place's landmarks there.

Hand-painted floors: edit `mode7_floor.png`, then
`python3 tools/orchid/mode7_floor.py convert <png> <dir>`.

## Performance

The GBA has no hardware divide. Keep all per-frame and per-scanline maths
32-bit: one 64-bit division per scanline halved the frame rate. Check after
changes by comparing play-time frames against emulator frames (60 fps =
equal).

## Testing

Debug menu (R + Start) → Party → **Debug Battle: Day…** / **Debug Battle:
Night…** runs the showcase battle on any floor (map default, grass, beach,
void deck, cave, ruins, office, mall, jungle, lake) with the time forced.

Debug menu (R + Start) → Party → Start Debug Battle runs a showcase:
Blaziken, Gardevoir and Swampert vs a Lv 38 smart-AI team. It covers
physical, special and status moves, stat drops, KOs, switching,
Earthquake's screen shake and Surf's background swap. Debug battles skip
the obedience check.

## Known limitations

- One frame of plain floor colour while the background swaps to a flat
  move background (e.g. Surf). There is no spare VRAM or heap to prepare it
  off-screen.
- The level-up stats box draws on BG2 and may not show while the floor is up.
- Battler sprites don't scale with the focus zoom.
