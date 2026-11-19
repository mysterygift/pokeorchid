# Holon Leader Faba: done (2026-11-19)

This was done straight in `pokeorchid-voyages` (branch `voyages`). Nothing is committed. The final normal `make -j8` is clean. Its only warnings are the existing heal_location.c unused function and the Mt. Ember waitstate. `grep gHarnessKeys pokeemerald.map` returns 0.

## What changed

### Art
`install_faba.py` (Pillow venv) installs the art as 4-bit, 16-colour files and checks the palettes:
- `graphics/trainers/front_pics/holon_leader_faba.png`: pose A.
- `graphics/object_events/pics/people/faba.png`: palette is exactly npc_3.
- `graphics/battle_transitions/holon.png` + `.bin`: the logo uses indices {0,1,3,4,5,15} of `evil_team.pal`, and the palette is reused.

### Class, pic, OW
- **Class:** `TRAINER_CLASS_HOLON_LEADER` = `"Holon{NBSP}Leader"`, prize 20, Master Ball (src/battle_main.c).
- **Trainer pic:** `TRAINER_PIC_HOLON_LEADER_FABA` (src/data/graphics/trainers.h).
- **OW:** `OBJ_EVENT_GFX_FABA` uses npc_3 / PALSLOT_NPC_3, the same as the Holon Researcher. It is added after HOLON_SPHERE, and its graphics info, pic table and pointer follow Cynthia's.

### Trainer
- **Slot 107:** `TRAINER_HOLON_FABA`, which was Hex Maniac **Tammy** (Route 121).
  - Slots 23–106 were already taken; slot 32 (Shelly) went to the Sevii polish.
  - Tammy is not in a rematch, Match Call or gym table.
  - `#define TRAINER_TAMMY TRAINER_HOLON_FABA` is aliased in opponents.h, so Route121 still builds.
- **trainers.party:** the team from NOTES §5, with items, abilities, natures, moves and IV 31.
  - The Deltas are written as `SPECIES_*_DELTA`.
  - 4 Full Restores, AI Basic Trainer (the same as Cynthia), `Music: Aqua`.
- **No `Mugshot:`.** The mugshot check runs before the class check, so a mugshot would replace the Holon transition (NOTES §3).

### Music
In `GetBattleBGM`, `case TRAINER_CLASS_HOLON_LEADER` returns `MUS_VS_AQUA_MAGMA_LEADER`. The encounter music is `MUS_ENCOUNTER_AQUA`, set by the trainer's `Music: Aqua`.

### Transition
- `B_TRANSITION_HOLON` is added before `B_TRANSITION_COUNT`.
- `Task_Holon`, `sHolon_Funcs`, `Holon_Init` and `Holon_SetGfx` copy Aqua's code with the Holon tileset and tilemap. They reuse `sEvilTeam_Palette`.
- `GetTrainerBattleTransition` returns it for `TRAINER_CLASS_HOLON_RESEARCHER` and `TRAINER_CLASS_HOLON_LEADER`.

### Flags
- `FLAG_HOLON_FABA_DEFEATED` 0x286: hides Faba and unlocks the Eevee-δ gift.
- `FLAG_HOLON_POWER_SPOTS_HEALED` 0x287: heals the drained rings.

### Ring heal
- `Holon_LoadHealedRingsPalette` (src/holon.c) is called at the end of `LoadSecondaryTilesetPalette` (fieldmap.c).
- On gTileset_Holon maps, once the flag is set, it loads General_Holon palette 02 into BG slot 7. That is the same green as the grass round the rings, so the drained twins blend back in and the rest of Holon stays desaturated.
- To use vivid General 02 instead, change one array in that function.

### Research Tower 2F
- **map.json:**
  - `battle_scene` is `MAP_BATTLE_SCENE_OFFICE`.
  - Faba is appended last, so the local ids of the other objects don't shift: `LOCALID_HOLON_FABA` at (11,6), facing down, `TRAINER_TYPE_NONE`, flag `FLAG_HOLON_FABA_DEFEATED`.
- **scripts.pory:**
  - `trainerbattle_single` with the NOTES intro and defeat lines, then the continue script `…_FabaDefeated`. It shows the "Holon WILL remember Faba!" line, sets both flags, then fades and runs `removeobject`.
  - The head of research gives the "not now / stop Faba" line until the flag is set, then makes a thank-you offer.
  - These lines get after-versions: the machine sign (NOTES text), Tobias, Kenji and the lab NPC.
- **HolonVillage/scripts.pory:** the walkway researcher, the three farmers and the lass get after-versions, gated on the healed flag.

## Verification
Headless run: `headless/hbuild.sh` builds the harness ROM. It is polish_content's harness, but it restores each patched file from a cp backup instead of `git checkout`. `headless/run_faba.py` ran on a copy of the engine-dev save, under the lock. Result: **20/20 PASS**, log in `shots/run_faba.log`.

| Step | Result | Shots |
|---|---|---|
| Village before the battle | BG palette 7 = 07.pal (drained) | 01 |
| Faba before the battle | at (11,6) | 02 |
| Head of research before | "not now" line, no Eevee | 03 |
| Tobias | Task_Holon ran; trainer 29; "Holon Researcher Tobias"; office environment | 04_* |
| Faba encounter | song 419 (`MUS_ENCOUNTER_AQUA`) during the intro text; Task_Holon ran; trainer 107 | 05_* |
| Faba battle intro | "You are challenged by Holon Leader Faba!"; office environment (36); lead `SPECIES_HYPNO`; battle song 483 (`MUS_VS_AQUA_MAGMA_LEADER`) | 06 |
| After the win | both flags set, object removed | 08 |
| Eevee-δ | given (flag 0x283) | 09, 09b |
| Tower 2F re-entered | Faba stays hidden | |
| Village + Lake after | palette 7 = General_Holon 02 | 10 vs 01, 11 |

- The transition shot renders BG0 only. The renderer has no blending and reads WIN0 from sGpuRegBuffer, but the weave sets it per scanline.
- The harness ROM was deleted afterwards.

## Known gaps
- **install_holon.py overwrites these edits.** It regenerates HolonResearchTower_2F (map.json + scripts.pory) and HolonVillage/scripts.pory. If it is re-run, re-apply the edits above. They are self-contained blocks marked "Wavebreak Voyages" / `Faba` / `FLAG_HOLON_POWER_SPOTS_HEALED`.
- Faba has no mugshot, by design.
- The sphere glow is still tied to Cynthia.
- Only the lead's species was read from gBattleMons. The other five came from trainers.party, which compiled without error.
- Not checked in the headless run:
  - the Lv / items in battle
  - how the full 3.6 s transition looks with blending (check in mGBA)
