# Stream "trainers" — done (2026-11-19)

Worktree `pokeorchid-voy-trainers` (detached, from `voyages` bc3f480c7c). Nothing committed. Clean `make -j8`
(normal build, `grep gHarnessKeys pokeemerald.map` = 0). Only pre-existing warning: heal_location.c unused function.

## What changed

### 1. Holon Researcher class
- `TRAINER_CLASS_HOLON_RESEARCHER` = `"Holon{NBSP}Researcher"`, prize 15, Ultra Ball (src/battle_main.c).
- `struct TrainerClass.name` widened 13 → 17 (include/data.h). Readers checked (see batch5 NOTES table): battle
  strings use `text[32]` / gDisplayedStringBattle, scrcmd/battle_dome use gStringVarN, union room only sees union
  classes, match call / Rotom CALL only rematch contacts. No save data stores class names.
- `TRAINER_PIC_HOLON_RESEARCHER` (brown slacks) and `OBJ_EVENT_GFX_HOLON_RESEARCHER` (npc_3, dark-brown hair).
- In battle the engine joins class + name with NBSP too, so the intro reads
  "You are challenged by / Holon Researcher Christophe!" (class + name never split; shot 12).

### 2. Cynthia
- `TRAINER_PIC_CYNTHIA` (mugshot coords -4,7, scale 0x188), `OBJ_EVENT_GFX_CYNTHIA` (npc_white, PALSLOT_NPC_1).
- Trainers (class Champion, `Mugshot: Yellow`, 4 Full Restores, AI Basic Trainer, final team from cynthia_team.py:
  natures, IV 31, items, Garchomp @ Garchompite):
  - slot 23 `TRAINER_CYNTHIA_LAKE` (alias `TRAINER_GRUNT_MT_PYRE_1`)
  - slot 24 `TRAINER_CYNTHIA_CAFE` (alias `TRAINER_GRUNT_MT_PYRE_2`)
- `GetBattleBGM` (src/pokemon.c) returns `MUS_ORCHID_VS_CYNTHIA` for both IDs.
- lichen credited in root CREDITS.md → "Other Credits" → "Pokémon Orchid Sprite Credits".
- Install script: `install_sprites.py` (design/ → graphics/, 16-colour, OW palette checked against npc_3 / npc_white).

### 3. Holon Researchers (slots 25-30, aliases for the old vanilla names in opponents.h)
`TRAINER_HOLON_IDO` 25, `_CHRISTOPHE` 26, `_MATEO` 27, `_HENRIK` 28, `_TOBIAS` 29, `_KENJI` 30; Lv 62-68; BASE species
for now. Intended Delta teams: `researcher_teams_delta.txt` (one line per mon to swap after the Delta merge).
Not placed on any map (Holon maps are the holon stream's).

### 4. Music
- `MUS_ORCHID_ENCOUNTER_CYNTHIA` 563, `MUS_ORCHID_VS_CYNTHIA` 564, END_MUS 564, every PH_* +2 in songs.h.
- charmap.txt: the MUS_TOSA_PORT..PH_NURSE_SOLO block regenerated from songs.h. **It was already wrong on the
  base** (MUS_ORCHID_VS_TRAINER missing, END_MUS/PH_* off by 1-3); now every code matches songs.h.
- song_table.inc, midi.cfg (`-E -R50 -G_<own vg> -V080 -P1` vs, `-V076` encounter), voice_groups.inc, debug.c sound list.
- `NUM_TRACKS_BGM` 10 → 12 (sound/music_player_table.inc; +0xA0 IWRAM, now 87.2%).
- `prepare_cynthia_midis.py` (ref/*.mid → sound/songs/midi/): vs = 11 tracks (ch16 duplicate + ch7 orchestra hits
  dropped; ch9+12+14 and ch11+15 merged with state re-sent per segment; ch11 → program 82 = square channel 2);
  RPN bend range → CC20 BENDR; drum key 49 → 57; only notes/programs/bends/CC1/7/10/20 kept. Encounter: one piano
  track. **No loop markers** (user adds them).
- `gen_cynthia_voicegroups.py`: GM-numbered voicegroups `mus_orchid_vs_cynthia` (synth bass 38 = programmable wave,
  steel drums 114 = sc88pro xylophone, choir, strings, horn, flute, squares 80/82, rs_drumset at 0) and
  `mus_orchid_encounter_cynthia` (piano keysplit at slot 0).

### 5. Scripts + Battle Café
- `data/scripts/cynthia.pory` (+ generated .inc, included from event_scripts.s):
  - `Common_EventScript_CynthiaHolonLake`: encounter music → speech + yes/no → `trainerbattle_no_intro` →
    `FLAG_CYNTHIA_BEATEN_AT_LAKE` → fade + `removeobject VAR_LAST_TALKED`. **For the holon stream:** give her
    object `script: Common_EventScript_CynthiaHolonLake`, `flag: FLAG_CYNTHIA_BEATEN_AT_LAKE`.
  - `Common_EventScript_CynthiaCafe`: rematch once per RTC day.
- Flags/var (my allocation): `FLAG_CYNTHIA_BEATEN_AT_LAKE` 0x1AA, `FLAG_HIDE_CHANGU_CAFE_CYNTHIA` 0x1AB (set/cleared
  by the café's ON_TRANSITION from the lake flag), `FLAG_CYNTHIA_CAFE_REMATCHED` 0x1DA,
  `VAR_CYNTHIA_CAFE_REMATCH_DAY` 0x4091.
- Daily rule: Orchid never sets FLAG_SYS_CLOCK_SET, so VAR_DAYS never updates. Two small specials in
  src/field_specials.c (`IsCynthiaCafeRematchAvailable`, `SetCynthiaCafeRematchDay`, appended to specials.inc)
  read the RTC day directly.
- Exterior: `cafe/patch_changu_exterior.py` changed 45 cells, all inside x30-38 y25-31 of
  data/layouts/ChanguCity/map.bin: the red-roof house, Bura stall terrace, road extension, and a sign post. It
  refuses to run if the box was hand-edited. ChanguCity map.json gets warp 10 (32,29) → café, sign (30,29)
  "BATTLE CAFÉ", and the terrace patron (36,28). New scripts are in scripts.pory/.inc.
- Interior: `MAP_CHANGU_CITY_CAFE` (appended to gMapGroup_TosaOverworld = 21.121, MUS_SLATEPORT) on
  `LAYOUT_CHANGU_CITY_CAFE` 12x10 (`cafe/build_cafe_layout.py`; collision copied from the Centre).
  - Objects: barista ("Welcome to the Battle Café!"), businessman, businesswoman, tourist (line changes after the
    lake flag), and Cynthia at (10,7).
  - Exit mat warps go to Changu warp 10.
- Tileset `gTileset_ChanguCafe` (data/tilesets/secondary/changu_cafe, `cafe/install_cafe_tileset.py`): a copy of
  OrchidCentre with variant A pal 6/11. Wall entries in metatiles 0x201-0x215 and 0x24B-0x24C use pal 11.
  OrchidCentre itself is untouched.

## Verification (headless, harness ROM, user save copy; scripts in `headless/`, shots in `shots/`)
- Café: Cynthia hidden without the lake flag; present after poking it (03/04). Exterior, sign, door → café, variant-A
  room and barista line all checked (01, 02, 05, 06).
- Real café rematch:
  - `gMPlayInfo_BGM.songHeader` = mus_orchid_encounter_cynthia during "Wonderful…", then mus_orchid_vs_cynthia
    from the transition on.
  - The mugshot transition runs (08). The renderer can't scale affine OBJs, so the pic shows unscaled.
  - Intro reads "You are challenged by / Champion Cynthia!" (09).
  - With the party poked so Garchomp leads: "Garchomp has Mega Evolved into Mega Garchomp!", and
    gBattleMons[1].species = 947 (11).
- Try Battle 23 (lake ID): song = mus_orchid_vs_cynthia (14). Try Battle 26: one-line class + name (12/13); song
  mus_orchid_vs_trainer.
- Rematch rule: offered when not yet won; "Come back tomorrow" when flag 0x1DA is set and the var = today's RTC day
  (9820) (15/16).

## Known gaps
- No Holon Lake map exists yet, so `Common_EventScript_CynthiaHolonLake` is built but has not been run in game.
- The Holon Researcher OW has not been seen in game; no map uses it yet. It uses the same pipeline as Cynthia's OW,
  which was seen. Its front pic was seen in battle.
- The mugshot scale and coords (-4,7,0x188) can't be judged with the headless renderer. Check them in mGBA.
- Music balance has not been listened to: directsound overflow is about 4% in bars 17 and 56-62, as analysed in the
  NOTES. Loop markers are for the user.
- The Rotom Phone CALL contact for Cynthia (mentioned in batch5 NOTES) was not in this brief and was not done.
- Researcher teams use base species until the Delta merge.
