# Batch 5: Cynthia, Holon Researcher, Cynthia music, Cynthia's team (design review only)

Nothing under data/ src/ include/ graphics/ sound/ was changed. The scripts and install-ready sprites are in
`dev_scripts/voyages/trainers/`, and the renders are in this folder. Python: scratchpad venv.

| Script (trainers/) | Writes |
|---|---|
| `cynthia.py` | `cynthia_front.png`, `cynthia_ow.png` (npc_blue), `cynthia_ow_ownpal.png` + `npc_cynthia.pal` (fallback); renders `cynthia_*` |
| `holon_researcher.py` | `holon_researcher_front.png` (+ `_greyslacks`), `holon_researcher_ow.png` (npc_3, + `_lighthair`); renders `holon_researcher_*` |
| `intro_textbox.py` | `intro_*_p1.png`, `intro_textbox_sheet.png`. Uses the real intro string and a port of `BreakSubStringAutomatic` |
| `midi_inspect.py`, `music_plan.py` | MIDI reports and the voice / directsound plan (tables below) |
| `cynthia_team.py` | Team legality check against the repo learnsets |
| `CREDITS.md` | lichen credit text and where it goes |

---

## Decided (user, 2026-11-19)
- Cynthia OW palette: npc_white (trainers/cynthia_ow.png regenerated with CHOSEN='npc_white').
- Holon Researcher front + OW tweak approved as drawn.
- Holon Researcher: BROWN trousers variant.
- Cynthia's team has held items (propose a set).
- Cynthia rematch: after the Holon Lake battle she moves to Changu City's Battle Lounge (a battle facility where you fight trainers from other regions/gyms) and becomes a Rotom Phone CALL contact; calling her arranges a rematch at the Lounge.
- Music loop/repeat markers: the user adds them themself after the songs are imported — import without inventing loop points.

## 1. Cynthia sprites (lichen)

- **Front pic.** Cut from 0,0 to 63,63 on the sheet. 13 colours plus transparency, re-indexed in the vanilla
  order: 1-4 skin ramp and outline, 5-7 hair, 8-11 coat greys, E white, F black. Slots 12-13 are unused.
  `kit.check_front`: OK. Bounding box x6-53, y2-62, with no edge pixels and the feet on y62 like vanilla adults.
  See `cynthia_front_x4.png` and `cynthia_battle_intro_lake_x3.png` (Orchid lake floor).
- **OW frame order.** lichen's 9 frames are already in vanilla order: 0 down, 1 up, 2 left, 3-4 walk down,
  5-6 walk up, 7-8 walk left. This is the sheet order that `overworld_ascending_frames` reads
  (`object_event_pic_tables.h`). They match the vanilla bounding boxes of beauty/lass (stand y11-30, walk y12-31).
  - **Alignment issue (minor).** In the left-walk frames 7-8 the head bobs 1px but the feet stay on y30.
    Vanilla walk frames move the whole body down to y31. This is not visible at 1x and was left as drawn.
- **Shared palette.** Lichen's OW uses 12 colours: vanilla skin and outline, a 4-shade hair ramp, a 3-shade
  coat ramp (blue-grey, navy, near-black) and black. No shared palette has both a gold ramp and a near-black
  ramp. All candidates are in `cynthia_ow_palette_candidates.png`.
  - **DECIDED: npc_white** (dull gold hair, grey coat). This was originally recommended as npc_blue ("black coat" row). It is built in Emerald since the trainer-classes merge.
    - With npc_blue, hair would move to 5-7, a brighter gold (255,222,74 / 213,172,32 / 131,98,0) than lichen's pale gold.
    - The cream hair highlight becomes white E.
    - The coat's blue-grey and navy both become A (65,57,98, dark purple-grey), and the near-black becomes F.
      The coat reads black with a faint purple sheen, and the blue-grey highlight on the hair clips is lost.
  - npc_white keeps the coat grey but turns the hair olive. npc_green keeps the hair close to lichen's but
    turns the coat olive. npc_2 makes the hair orange, and npc_1 makes it khaki.
  - The fallback is `cynthia_ow_ownpal.png`: exact colours on her own palette (`npc_cynthia.pal`). This is
    the same exception that School Kid ♀ got.
- **Ground mocks.** `cynthia_ow_ground_1x.png` and `_3x.png` show her on General grass 0x001 and sand 0x124.
  The walk cycle is in `cynthia_ow_walk.gif`.
- **Mugshot.** Champion entries use the mugshot transition (Wallace: `Mugshot: Yellow`, coords -8,7, rotation
  0x188). Cynthia's pic would need its own coords; these have not been mocked.

## 2. Holon Researcher (new class)

- **Front pic: tweak of `scientist_frlg.png`.** Emerald has no Scientist front pic. The silhouette is
  pixel-identical to vanilla (silhouette audit: grow 0 / shrink 0; OW mask diff 0).
  - Hair is recoloured from blue-grey to brown (176,120,80 / 128,80,48 / 72,40,24).
  - Shirt and tie are recoloured from pink to green (160,216,120 shirt, 64,144,72 tie). The navy strip next to
    the shirt now joins the tie, so the flask liquid also turns green.
  - The glasses get a thin warm top arc and lower rims, so the lenses read as rings instead of the vanilla
    browline bar.
  - Hair and trousers share one ramp, so the slacks turn brown as well. The variant `_greyslacks` puts the
    trousers on the coat greys instead.
- **OW: tweak of `scientist_1.png` (npc_3).** It already has brown hair, glasses and a green tie. The changes
  are a green collar and shirt (9) and a dark green tie (A) on all front and side frames.
  - npc_3 is the only shared palette with a white coat ramp, a green ramp and a brown ramp.
  - Variant `_lighthair`: npc_3's light brown is orange, so lighter hair reads as ginger. Not recommended.
- Renders: `holon_researcher_compare.png` (vanilla vs tweak: front 2x, all 9 OW frames + flip at 3x, card),
  `holon_researcher_face_x8.png`, `holon_researcher_ow_walk.gif`, and battle intros in `intro_textbox_sheet.png`.
- **Weak spot.** The round-glasses change is subtle at 64px, because the black bridge and temples stay vanilla.

### Class name: "Holon Researcher" vs `struct TrainerClass.name[13]` (include/data.h:152)
"Holon Researcher" is 16 characters + EOS = 17 bytes, so it does not fit the 13-byte initializer
(src/battle_main.c:298). These are the readers of `gTrainerClasses[].name` / `GetTrainerClassNameFromId`:

| Reader | Destination | Fits 16 chars? |
|---|---|---|
| battle_message.c:3057 `BattleStringGetOpponentClassByTrainerId` → `B_TXT_TRAINER1/2_CLASS`, `_NAME_WITH_CLASS` (3324-3345, 3471-3478), partner (3536-3605) | class + space + name built in the local `text[32]` (3114: max(32, 11, 11, ITEM_NAME_LENGTH 20)) → `gDisplayedStringBattle[425]` | yes: 16+1+10+EOS = 28 ≤ 32 |
| scrcmd.c:3036 `bufferTrainerClassName` | `gStringVarN[0x100]` | yes |
| battle_dome.c:4202 | `gStringVar1[0x100]` | yes (frontier classes only) |
| union_room.c:4455 | `trainerCardStrBuffer[12][15]` (include/union_room.h:130) | **no**, but it only sees union-room classes (`GetUnionRoomTrainerClass`), never this one |
| pokenav_match_call_list.c:414, pokenav_match_call_data.c:1089 | pointer, drawn clipped to 69 px FONT_NARROW | only rematch-table trainers |
| rotom_phone_call.c:228 `ContactName` | `gStringVar1` | only rematch contacts |
| test/battle/trainer_control.c:142 | reads `.ball` only | n/a |

**Widening to `name[17]` is safe.** It costs 4 bytes per class of ROM. No save data stores class names, and
trainerproc maps `Class:` to the constant, not the string.

**Text box.** The tree no longer prints "<CLASS> <NAME> would like to battle!". The real intro is
`"You are challenged by {B_TRAINER1_NAME_WITH_CLASS}!\p"` (battle_message.c:97), auto-broken at 208 px over
2 lines (battle_message.c:3724, line_break.c). The breaker balances line widths, so it splits the class:

- "You are challenged by Holon / Researcher Ido!" (143 / 83 px)
- "You are challenged by Holon / Researcher Christophe!" (143 / 122 px)
- With `{NBSP}` (charmap 0x39, 3 px like a space) in the class string, "Holon{NBSP}Researcher" can't split:
  "You are challenged by / Holon Researcher Christophe!" (112 / 153 px). A 10-character name still fits.
- "Holon Researcher Christophe / sent out Pikachu!" (149 / 92 px)
- Cynthia: "You are challenged by / Champion Cynthia!"

All of these are in `intro_textbox_sheet.png`. `cynthia_battle_intro_lake*.png` still uses battle_mock.py's
old "would like to battle!" line and is kept only for the scene.

## 3. Music (inspection only, nothing imported)

**encounter_cynthia.mid**
- Format 1, 2 tracks (conductor "Champion Cynthia" + "Piano"), **256 ppqn**, 160 bpm.
- Meter: 3/4, with 5/4 at tick 3072 (bar 5), 3/4 at 4352, and 5/4 at 17408 (~bar 23). Length 22017 ticks ≈ 32 s.
- One channel, program 0 (Grand Piano): 471 notes, A#1-G6, velocity 65-127.
- Controllers: CC7 100, then a fade 127→2 from tick 19488 to 21816. CC10 51, CC91 60.
- **No loop markers.** 253 of 315 onsets fall off the 24-ppqn grid (humanised playing). No bar-level repeat was
  found, so the loop has to be picked by ear.
- Peak 5 simultaneous notes. The piano keysplit is directsound (DS), so that is exactly the 5-channel limit.

**vs_cynthia.mid**
- Format 1, 18 tracks (conductor + "System Setup" + CH#1-16), **480 ppqn**, 4/4.
- Tempo 171 → 166 (t4800) → 162 (t5040) → 185 bpm from t5760 (bar 4) to the end.
- 144000 ticks = 75 bars = 97.7 s. Markers are only 'Setup' @0 and 'Start' @1920. There is a GM-reset sysex.
- **Loop found:** bars 69-75 are exact repeats of bars 9-15 (bar 68 ≈ bar 8 at 97%). That gives
  **"[" at bar 8 (tick 13440) and "]" at bar 68 (tick 128640)**: a 60-bar body. The rest is a repeat plus a
  CC11 fade, and can be cut.
- 16 channels:

| ch | program | notes | range | notes |
|---|---|---|---|---|
| 1, 3 | 48 strings (44 tremolo bars 63-70) | 173 / 143 | G#3-E6 / B1-A5 | RPN bend range 12, later 4; 69 bends (intro swoop bar 3.5, bar 67) |
| 2 | 52 choir → 80 square lead (bar 11) → 52 (63) → 80 (71) | 125 | G#4-D#6 | main lead |
| 4 | 52 choir → 60 French horn (bar 16) | 55 | B3-D#5 | octave below ch2 |
| 5 | 38 synth bass 1 | 587 | B0-C#3 | peak 2 notes |
| 6 | 114 steel drums | 178 | G#3-G#6 | |
| 7 | 55 orchestra hit | 51 | F#2-G#5 | stabs, bars 4-68 |
| 8 | 47 timpani | 170 | G#2-D#3 | |
| 9 | 48 strings | 104 | C#3-E4 | bars 16.6-32 only |
| 10 | drums | 1116 | keys 36 kick, 38 snare, 46 open hat, 49 crash ×4, 57 crash ×3 | |
| 11 | 80 square lead | 92 | G4-G#6 | harmony to ch2, bars 24-56 |
| 12 | 73 flute | 28 | G#5-A#6 | bars 32-38 |
| 13 | 62 synth brass | 18 | G#3-F5 | bars 32-39 |
| 14 | 30 distortion guitar | 38 | F2-A6 | bars 56-61, 132 bends, bend range 10 |
| 15 | 1 bright piano | 32 | D5-D#7 | bars 56-58 |
| 16 | 39 synth bass 2 | 587 | | **an exact copy of ch5** at velocity 41-59 |

### Voice map (from `music_plan.py`)

| GM program | m4a voice | Copy from |
|---|---|---|
| 0, 1 piano | piano keysplit (DS) | vs_champion 1 |
| 30 distortion guitar | sd90_classical_distortion_guitar_high (DS) | vs_frontier_brain 30 |
| 38 synth bass | sc88pro_synth_bass (DS), **or programmable wave (PSG, recommended)** | vs_frontier_brain 38 / vs_champion 81 |
| 44, 48 strings | strings keysplit (DS); there is no tremolo sample | vs_champion 48 |
| 47 timpani | sc88pro_timpani (DS) | vs_champion 47 |
| 52 choir | classical_choir_voice_ahhs (DS) | rg_vs_champion / b_pike |
| 55 orchestra hit | no sample: trumpet stab, or drop | vs_champion 56 |
| 60 French horn | French horn keysplit (DS) | vs_champion 60 |
| 62 synth brass | trumpet keysplit (DS) | vs_champion 56 |
| 73 flute | sc88pro_flute (DS) | vs_champion 73 |
| 80 square lead | square_1 / square_2 (PSG) | vs_champion 80/82 |
| 114 steel drums | no sample: sc88pro_xylophone (DS), or a square (PSG) | encounter_champion 13 |
| drums | rs_drumset: 36, 38 and 46 are DS. **Key 49 is empty in rs**, so remap it to 57 (crash) | vs_champion 0 |

### Limits checked
- **Tracks.** The BGM player has **10 tracks** (`NUM_TRACKS_BGM`, sound/music_player_table.inc). m4a silently
  drops song tracks past that (src/m4a.c:590).
  - Dropping ch16 and merging the non-overlapping channels into shared tracks gives 12:
    9+12+14 (strings → flute → guitar), 13 alone, and 15 after bar 56 on ch11's track.
  - To reach 10, either raise `NUM_TRACKS_BGM` to 12 (2 × 0x50 bytes of RAM; the engine maximum is 16), or
    also drop ch7 (orchestra hits) and ch13 (18 synth-brass notes).
- **Directsound (≤5 at once).** Measured from note on/off, ch16 dropped:
  - With every melodic voice on DS: peak 12 at bar 58, more than 5 for 12.4% of the song.
  - Bass on the wave channel: 4.4%.
  - Plus orchestra hits dropped: 4.3%, peak 8 (bar 17).
  - Plus ch3 strings thinned at climaxes: 0.1%.
  - When the limit is exceeded, m4a steals voices, which you hear as dropouts in the loud bars 17 and 56-62.
- **Encounter:** 5 DS at peak, within budget.

### What must change in the MIDIs before import
1. **Loop markers** ("[" / "]" text or marker events on the conductor track, which mid2agb reads in midi.cpp):
   - vs: "[" at 13440 and "]" at 128640. Delete everything after 128640, including the CC11 fade.
   - encounter: by ear. Suggested start is "[" at 3072 (bar 5, first 5/4 bar), and "]" at 17408 (before the
     closing 5/4 bars). Delete the CC7 fade from 19488.
2. **Bend range.** mid2agb ignores RPN 100/101/6. Insert **CC20 (BENDR)**:
   - 12 at tick 1800 on ch1-4, and 4 at about tick 120300-120940 where the RPN changes.
   - 10 on ch14.
   - Without these, every bend plays at ±2 semitones.
3. **Programs.**
   - Slot 0 of every vanilla voicegroup is a **drumset**, so the encounter's program 0 piano would play drums.
     Either change it to 1, or give each song its own voicegroup with GM-numbered slots. That is the user's
     existing pattern (mus_sinjoh_ruins_test.inc), and it needs no other program edits.
   - vs ch12/13 start on program 0 but change before their first note, so they are fine.
4. **Cut ch16** (an exact duplicate of ch5), merge or drop channels to fit the track budget, and remap drum key
   49 → 57.
5. **ppqn.** No re-save is needed. mid2agb rescales any division to 24 clocks/beat (`ConvertTimes`).
   - The encounter's humanised timing snaps to about 16 ms.
   - Sub-clock drum notes become 1-clock notes.
   - Use `-X` (48 clocks/beat) if the swing matters.
6. **Volume.** CC7 is 100 on most channels, and ch1-3 rise to 119-127 in the bar-61 crescendo. CC11 only
   carries the end fade, which is trimmed anyway.
   - Suggested midi.cfg lines, matching vanilla: `-E -R50 -G_<own vg> -V080 -P1` for vs
     (vs_champion uses -V080 -P1) and `-V076` for the encounter (encounter_champion).
   - GM-reset sysex, CC0/32/71/74/91/93/94 and the RPNs are ignored by mid2agb, so they are harmless.

## 4. Cynthia's team: DECIDED (checked by `trainers/cynthia_team.py`)

User decisions (DECISIONS.md 16):
- Platinum species with **modern movesets**. Trainer moves need not be learnable in Orchid; every move, item
  and ability constant was checked to exist in include/constants/{moves,items,abilities}.h, and none are missing.
- Held items, levels 70-74, and Mega Garchomp.
- Mega: `ITEM_GARCHOMPITE` = 333 exists. `CanMegaEvolve` (src/battle_util.c:8578) checks for the Mega Ring
  only on the player's side, so an opponent mega-evolves just by holding the stone, once per trainer, like
  the Guardians' `Tyranitar @ Tyranitarite`. Mega Garchomp's ability becomes Sand Force.

| Mon | Lv | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Spiritomb | 70 | Leftovers | Pressure | Calm | Shadow Ball, Dark Pulse, Will-O-Wisp, Psychic |
| Roserade | 70 | Black Sludge | Natural Cure | Modest | Energy Ball, Sludge Bomb, Shadow Ball, Toxic Spikes |
| Togekiss | 72 | Life Orb | Serene Grace | Modest | Air Slash, Dazzling Gleam, Aura Sphere, Thunder Wave |
| Lucario | 72 | King's Rock | Inner Focus | Timid | Aura Sphere, Flash Cannon, Dragon Pulse, Nasty Plot |
| Milotic | 70 | Sitrus Berry | Marvel Scale | Bold | Scald, Ice Beam, Recover, Mirror Coat |
| Garchomp | 74 | Garchompite (Mega) | Rough Skin → Sand Force | Jolly | Earthquake, Dragon Claw, Stone Edge, Fire Fang |

Other settings:
- All IVs 31, no EVs (like Wallace and Steven).
- Bag: 4 Full Restores.
- `Class: Champion`, `Mugshot: Yellow` (placeholder colour), `AI: Basic Trainer`.
- Natures are my proposal. `Nature:` is valid trainers.party syntax (trainers.party:53).
- `cynthia_team.py` prints the ready `trainers.party` block. `Pic: Cynthia` and `Music:` need the new
  TRAINER_PIC_CYNTHIA and the encounter-music constant at implementation.
- Rematch: after her first defeat she moves to a café in Changu City and can be rematched there.

---

## Decisions (all questions closed; see dev_scripts/voyages/DECISIONS.md 16-21)

1. Cynthia's OW palette: **npc_white** (`cynthia_ow.png` regenerated). The hair is dull gold and the coat grey.
2. Cynthia's walk frames 7-8: left as drawn.
3. Champion mugshot transition: **yes**. Coords are tuned at implementation.
4. Holon Researcher slacks: **brown**.
5. Holon Researcher OW hair: **vanilla dark brown**.
6. Glasses: **as drawn**.
7. Class name: **widen `TrainerClass.name` to [17]** and use **"Holon{NBSP}Researcher"**.
8. vs Cynthia tracks: **raise `NUM_TRACKS_BGM` 10 → 12**.
9. vs Cynthia directsound: **synth bass on the wave channel, orchestra hits dropped**.
10. Steel drums: **xylophone** (DS) for the bell line.
11. Loop markers: **the user adds them after import** for both songs. The analysed points above are for reference.
12. Team levels: **70-74**.
13. Held items: **yes**, including Garchompite (Mega Garchomp).
14. Movesets: **modern** (the table above).
15. Rematch: **in a Changu City café** after the Holon Lake win (placeholder for a future Battle Lounge).
16. Credit: **lichen under "Other Credits" in the root CREDITS.md** (text in `trainers/CREDITS.md`).
