# Polish: Cynthia phone contact + Sevii battle music (2026-11-19)

Worktree `pokeorchid-pol-phone` (detached, on top of the staged voyages merge). Nothing committed, index untouched.
Final normal `make -j8` is clean (only the pre-existing `heal_location.c` unused-function warning) and
`grep -c gHarnessKeys pokeemerald.map` = 0.

## A. Cynthia in the Rotom Phone CALL list

- `MC_HEADER_CYNTHIA` (include/pokenav.h, after Wallace) + `sCynthiaMatchCallHeader` in src/pokenav_match_call_data.c:
  NPC type, enabled by `FLAG_CYNTHIA_BEATEN_AT_LAKE`, mapsec Changu City, name "Cynthia", desc "CHAMPION", one
  fallback line (PokéNav only). So she joins the list through the normal `MatchCall_GetEnabled` loop.
- src/rotom_phone_call.c (existing kit pieces only, no new art):
  - row head = `OBJ_EVENT_GFX_CYNTHIA`; card / ringing portrait = `TRAINER_PIC_CYNTHIA`;
  - profile "Sinnoh's Champion, relaxing / at the Battle Café.";
  - **Champion tag**: tray status text "Champion" in Champion gold (KIT_SELECT_DARK) like Mom's "Home"; while
    today's café rematch is open it becomes "Champion · rematch ready!" (rematch red), the row shows the existing
    rematch pictogram and the card the red strip "Rematch at the Café today!";
  - call text: 4 rotating openers (random start, then cycles each call; EWRAM, not saved) + an availability line from
    `IsCynthiaCafeRematchAvailable()` (same RTC-day rule as `Common_EventScript_CynthiaCafe`):
    "We haven't battled today yet. / Come find me at the café!" or "We've had our battle for today. / Come back to
    the café tomorrow!";
  - calling her from inside the café gives the standard "That TRAINER is close by" line.
- include/field_specials.h: prototype for `IsCynthiaCafeRematchAvailable`.

## B. Sevii battle music (FRLG songs, Hoenn voices)

Generator: `gen_sevii_battle_music.py` (+ `smf.py`, a tiny MIDI reader/writer). For each song it copies the FRLG
MIDI unchanged (loop markers kept, none added) except drum notes, and writes a voicegroup whose slot N is the closest
**vanilla Emerald** voice for what FRLG had in slot N, copied verbatim from a named Emerald voicegroup (so the MIDI's
program numbers stay as they are). CGB voices are only swapped for the same CGB channel (square1/square2/wave/noise),
so channel sharing is as in FRLG. Directsound peak is unchanged (≤5 in every song). Full per-slot table:
`mapping.md`.

| New song | From | Hoenn counterpart | What changes |
|---|---|---|---|
| MUS_ORCHID_SEVII_VS_WILD 565 | mus_rg_vs_wild | vs_wild | FRLG kit → rs_drumset; squares/wave lead get Emerald envelopes; organ + nylon guitar get Emerald envelopes |
| MUS_ORCHID_SEVII_VS_TRAINER 566 | mus_rg_vs_trainer | vs_trainer | rs_drumset (cowbell → bell, triangle → tambourine); square bass + leads, wave, e.piano, nylon get Emerald voices; guitars/brass/strings already identical |
| MUS_ORCHID_SEVII_ENCOUNTER_BOY 567 | mus_rg_encounter_boy | encounter_male | rs_drumset; organs → encounter_male organ; squares → Emerald squares |
| MUS_ORCHID_SEVII_ENCOUNTER_GIRL 568 | mus_rg_encounter_girl | encounter_girl | rs_drumset; organ/nylon/squares → Emerald voices |
| MUS_ORCHID_SEVII_ENCOUNTER_ROCKET 569 | mus_rg_encounter_rocket | encounter_magma | rs_drumset; organ/nylon/squares → Emerald; wave waveform 14 → Magma's waveform 16 |

- Victory themes: nothing to do. FRLG reused the R/S victory songs (`mus_rg_victory_wild.mid` is byte-identical to
  `mus_victory_wild.mid`, the trainer one differs by a few CC values) on byte-identical voicegroups, so Sevii keeps
  MUS_VICTORY_WILD / MUS_VICTORY_TRAINER.
- Registration: songs.h 565-569, END_MUS 569, every PH_* +5 (songs.h and charmap.txt; a script checked every
  charmap MUS_/PH_ code against songs.h: 0 mismatches), song_table.inc, midi.cfg (FRLG's -V, `-P1` on the two vs
  songs like every Emerald battle theme), voice_groups.inc, debug.c sound list.
- Selection (src/pokemon.c): `GetBattleBGM` returns SEVII_VS_WILD / SEVII_VS_TRAINER (ordinary classes, the
  branch that used to fall back to MUS_VS_TRAINER) when `IsSeviiMapSec(gMapHeader.regionMapSectionId)`.
  `GetSeviiTrainerEncounterBGM()` (called from `PlayTrainerEncounterMusic`, battle_setup.c) maps approach music on
  Sevii with the trainer_tower.c grouping: female/girl/twins/cute → GIRL, suspicious/aqua/magma/dangerous → ROCKET,
  everything else → BOY. Off Sevii nothing changes. Sevii map music is untouched (FRLG).

## Verification (headless, harness ROM from `hbuild.sh`, copy of the engine-dev save)

Scripts: `hbuild.sh` (harness ROM; adds debug Script 1 = `callnative PlayTrainerEncounterMusic`, restored after),
`run.sh` (voyages lock + waits for GDB port 2345 to be free, since another session runs emulators without the lock),
`test_phone.py`, `test_music.py`; `emu_lib.py` / `e2e_lib.py` copied from the voyages e2e kit. Shots in `shots/`.

**Phone** (`test_phone.py`, shots 01-10):
- Flag clear: contacts = [Mr. Stone] only (01). Flag set: [Mr. Stone, Cynthia (special, mapsec 8, header 21)];
  her row has the OW head, "Changu City" and the rematch pictogram; tray "Champion · rematch ready!" + profile (02).
- Card: portrait, location pill, profile, red strip "Rematch at the Café today!" (03); ringing (04).
- Call 1: "CYNTHIA: Hello, JAXSON. / I'm at the Battle Café in Changu. ¶ The harbour breeze… ¶ We haven't battled
  today yet. / Come find me at the café!" (05-06).
- After poking `FLAG_CYNTHIA_CAFE_REMATCHED` + `VAR_CYNTHIA_CAFE_REMATCH_DAY` = today's RTC day (9820): no row
  pictogram, tray "Champion" in gold (07), no strip on the card (08), and call 2 rotated to the next opener
  ("Oh, JAXSON! I was just reading about Tosa's old legends…") ending "We've had our battle for today. / Come back
  to the café tomorrow!" (09-10).

**Music** (`test_music.py`, `shots/music_run.log`: 7/7), song read from `gMPlayInfo_BGM.songHeader`:
| Check | Song |
|---|---|
| wild battle on the boot map (Tiksi, control) | MUS_VS_WILD |
| wild battle on One Island (debug Start Wild Battle) (21) | MUS_ORCHID_SEVII_VS_WILD |
| Try Battle 26 (Holon Researcher, ordinary class) on One Island (22) | MUS_ORCHID_SEVII_VS_TRAINER |
| approach music, Calvin (Male), boot map (control) | MUS_ENCOUNTER_MALE |
| approach music on One Island: Calvin / Gabrielle (Female) / Shelly (Aqua) | SEVII_ENCOUNTER_BOY / _GIRL / _ROCKET |

After the One Island wild win the map song returned to MUS_RG_SEVII_123 (Sevii map music unchanged).

## Known gaps / for the user
- **Listen** (none of this was heard): the drum kit swap is the biggest change, especially SEVII_VS_TRAINER's
  53 cowbell hits now on rs "bell" and 57 triangle hits on tambourine, and SEVII_ENCOUNTER_ROCKET's wave line on
  Magma's waveform. Volumes are FRLG's -V values; rs_drumset may sit louder or quieter than the FRLG kit.
- Many FRLG voices were already identical to Emerald ones (same samples/envelopes), so the re-voiced songs are close
  to the originals apart from drums and envelopes; if the user wants a stronger Hoenn colour, swap slots in the
  `SONGS` table and rerun the generator.
- Pre-existing, not from this change: on the CALL talk screen, text after the first `\p` renders pale green in the
  headless renderer for every contact (Mr. Stone too, `shots/x_preexisting_mrstone_page2_text_colour.png`). Worth a
  look in mGBA.
- No Sevii trainers exist yet, so the encounter themes were exercised through `PlayTrainerEncounterMusic` from a
  harness-only debug script, not a real trainer's sight.
