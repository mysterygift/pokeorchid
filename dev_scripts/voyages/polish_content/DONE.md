# Content polish: done (Sevii trainers, tower encounters, lake rocks, flag-gated doors)

Worktree `pokeorchid-pol-content` (base = the voyages index). Nothing committed or staged by me. The final normal
`make -j8` is clean (only the pre-existing heal_location.c unused-function and Mt. Ember "explicit waitstate" warnings),
and `grep gHarnessKeys pokeemerald.map` = 0.

**Everything is (re)applied by one idempotent script:** `apply_polish.py apply` (Pillow venv), which also runs
`apply_world.py`. Run it again after any `build_sevii.py` / `install_holon.py` re-export, since those regenerate the maps.
`apply_polish.py check` runs the sight-line check on its own.

## Merge note for the coordinator
Outside `polish_content/` I also changed two files in `dev_scripts/voyages/sevii/` (copied into this worktree from
pokeorchid-voyages). Your `--exclude='dev_scripts/voyages/*'` would skip them, so copy them over by hand:
- `sevii_flags.json` now lists both door flags.
- `build_sevii.py` `allocate_flags()` now keeps non-item entries, so a re-run doesn't drop the door flags.

## A. Post-game Sevii trainers (33)
- **Which NPCs:** 33 of build_sevii's ex-FRLG trainer NPCs, plus invented sea-route swimmers, are now
  `TRAINER_TYPE_NORMAL`. Each sits at its FRLG position with its FRLG sight (capped at 2–4).
- **Teams:** from each trainer's FRLG rematch team, evolved, Lv 58–68.
  - Isles 1–3: Lv 58–61. Isles 4–5: Lv 62–63. Isles 6–7: Lv 64–68.
  - Default movesets, no items, AI Basic Trainer, names ≤ 10 characters.
- **Lines:** short new intro and defeat lines. The post-battle line is the NPC's old flavour line.
- **Spread:**

  | Area | Trainers |
  |---|---|
  | Kindle Road | 6 |
  | Treasure Beach | 1 |
  | Bond Bridge | 3 |
  | Mt. Ember | 2 Rangers (Ranger OW) |
  | Sea Route A | 1 swimmer |
  | Memorial Pillar | 3 Bird Keepers |
  | Sea Route C | 2 swimmers |
  | Water Path | 4 |
  | Ruin Valley | 3 |
  | Sevault Canyon Entrance | 3 |
  | Sevault Canyon | 3 |
  | Tanoby Ruins | 2 |

  - Not used: the doubles (Mik & Kia and similar), the Crush Girls (no female Black Belt OW), and the Juggler, Tamer and Painter (no Emerald class). The Rocket grunts don't battle (a DECISIONS item).
  - Tommy is talk-only: he fishes off the shore, as in FRLG.
  - Amira now faces the beach (she used to face the sea).
- **Slots:** `TRAINER_SEVII_*` take vanilla slots 31–106, skipping rematch, Match Call, gym-roster
  (set_gym_trainers) and Gabby & Ty slots. The old names are aliased in the new "Wavebreak Voyages polish" block of
  opponents.h. The slot list is `SLOTS` in `trainers_spec.py`.
- **Sight check:** `check` walks every facing direction's sight line, with collision, objects and elevation.
  No stop cell is a warp, and none splits the map or cuts off an NPC or item: **0 problems**.

## B. Research Tower encounters
- **Tileset:** `gTileset_HolonLab` (headers.h) reuses Lab's tiles and palettes but has its own metatiles and attributes
  (`data/tilesets/secondary/holon_lab/`): Lab plus 0x29E, a copy of the lab floor 0x269 with
  `MB_INDOOR_ENCOUNTER`. gTileset_Lab itself is untouched.
- **2F layout:** now on that tileset. 54 floor cells around the four machines (x6–16, y4–10) are encounter floor. The
  stairs side (x17–19) and the head of research's room have none.
- **Wild table:** moved from 1F (lobby, vanilla layout, so no encounters) to `gHolonResearchTower_2F`, rate 10:
  Magnemite, Voltorb, Magneton, Castform, Electrode, Porygon2, plus Klink-δ, Klang-δ, Klinklang-δ, Beldum-δ, Metang-δ
  and Metagross-δ, Lv 55–62. I dropped Eevee-δ (it's the gift) and added Metagross-δ as a 1% slot.

## C. Holon Lake rocks
- Four `OBJ_EVENT_GFX_BREAKABLE_ROCK` with `EventScript_RockSmash`, on the shore at (9,23), (27,41), (44,26) and (62,24).
- The Holon reachability check still reports OK, and every rock is reachable on foot.

## D. Flag-gated doors
- **Flags:** `FLAG_SEVII_DOTTED_HOLE_OPEN` = 0x26B and `FLAG_SEVII_TANOBY_OPEN` = 0x26C (flags.h, sevii_flags.json).
  Unset = sealed exactly as before.
- **Ruin Valley:**
  - New metatile `METATILE_SeviiIslands_DottedDoor_Open` = 0x3D7, appended to gTileset_SeviiIslands with 4 new tiles
    (`-num_tiles 502`) and `MB_NON_ANIMATED_DOOR`. The art is the slab frame hollowed into a dark doorway
    (`shots/dotted_door_sealed_vs_open_tiles.png`).
  - `ON_LOAD` sets the metatile.
  - `ON_TRANSITION` moves the scientist off the doorstep to (26,25). He gets a new line.
  - The "sealed" sign script ends silently once the flag is set.
- **Tanoby Ruins:** TanobyDelta's door art is untouched, since the tileset is shared with Tiksi.
  - `ON_LOAD` clears the collision on the 7 door cells (`setmetatile 0x20A, FALSE`).
  - 7 coord triggers (`VAR_TEMP_1` 0, flag-checked) warp into the chambers.
  - The chambers' south-arrow exits lead back.
  - The sign is silent once the flag is set.

## Verification
- `check_sevii.py`: identical to the baseline (same 9 pre-existing FRLG notes).
- `check_sevii.py --world`: unchanged. Only Dotted Hole is unreachable, because it is sealed by default.
- **Headless** (`headless/run_polish.py` on `hbuild.sh` harness, user save copy, under the lock), **15/15 PASS** across separate runs,
  logs `shots/run_polish_*.log`:
  - **Trainer battles:**
    - Logan spots the player → battle vs slot 58.
    - Daryl spots the player → slot 92.
    - Stanly, talked to → slot 88.
    - Surfing on Sea Route A, swimmer Dylan spots the player → slot 65.
  - **Tower 2F wild battles:** Electrode, and Beldum-δ Lv55 (`tower_2f_wild.png`).
  - **Lake rocks:** two smashed, and the objects are removed. Neither smash rolled an encounter.
  - **Doors sealed by default:** Ruin Valley 0x3C0 with collision; Tanoby blocks UP.
  - **Doors after poking the flags:**
    - Ruin Valley shows 0x3D7. On arrival the player walks out, then goes into Dotted Hole 1F and back.
    - Tanoby: Monean in and out, and Dilford in.

## Known gaps
- Nothing in the game sets the two door flags yet (a story hook is for later).
- No lake rock-smash encounter was observed in the two smashes (it's random).
- Holon's `wild_delta.json` in the voyages tree still keys the tower table on 1F.
