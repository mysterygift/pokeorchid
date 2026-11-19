# Batch 8: Holon Leader Faba + Holon battle transition (design review, no game code changed)

**Changes since the last review (round 2):**
- Front pic A: the collar is now a plain symmetric stand-up high collar (no flap across the face).
- Visor enlarged on both sprites, per the user ("too narrow"):
  - Front: one rounded lime lens from brow (y6) to cheekbone (y11), bulging past the head on the near side, with a white nose-pad bump.
  - OW: a 4-row rounded lens, rows 16-19 of the stand frames. The side view is 4 rows too, and a stray back-of-head pixel was fixed.
- Re-rendered: `faba_front_compare.png` (v1 vs new A vs ref), battle intros 1x/x3, OW frames/candidates/walk GIF.
- Checks: `check_ow` npc_3 OK. Front silhouette growth is 57 px vs Maxie (collar + lens bulge), shrink 0.
- All questions are decided (bottom of this file).

Scripts are in `dev_scripts/voyages/faba/`. Run them with the scratchpad venv Python:
- `faba_ow.py` builds the OW sheet, the palette candidates and the walk GIF.
- `faba_front.py` builds the front pics (A and B), the compare sheet, the 1x line-up and the silhouette audit.
- `holon_transition.py` builds the logo tiles and tilemap and renders the transition frame by frame.
- Battle mocks come from `trainer_classes/battle_mock.py faba/faba_front.png <env> "Holon Leader Faba" <out>`.

Game-ready art in `faba/`:

| File | Contents |
|---|---|
| `faba_ow.png` | 144x32, npc_3 |
| `faba_ow_ownpal.png` + `npc_faba.pal` | Fallback with its own palette |
| `faba_front.png` | Variant A |
| `faba_front_chesthand.png` | Variant B |
| `holon_logo.png` + `holon_logo.bin` | Transition tiles + tilemap |

## 1. OW sprite: `faba_ow_frames_x6.png`, `faba_ow_walk.gif`, `faba_ow_palette_candidates.png`, `faba_ow_context_1x_3x.png`

**How it was built**
- **Body:** vanilla `scientist_1` (npc_3). It is the same base as the approved Holon Researcher, and it is a lab coat.
  - Arms, legs, feet and the 9-frame walk cycle are pixel-for-pixel vanilla.
  - The walk frames are bobbed and every change follows the bob.
- **Why the template wasn't scaled:** the user's template is 32x48 RPG-Maker frames. Halved to Gen 3 size, its head is about two-thirds of the body (row 2 of the candidates sheet).
  - So the template gives the design cues: the coat with collar wings flared beside the jaw, the glasses band, and the stand/A/stand/B timing.
  - Proportions come from vanilla, per the OW-proportions rule.
- **Head:** a bald dome after vanilla `balding_man`: warm-brown scalp outline, 2px highlight at the top left, pale side tufts.
  - The **lime visor is a 4-row rounded lens** (round 2; v1 was a 2-row band) across the eyes. The eyes stay at vanilla x6/x9 and show dark through it.
  - Grin, small chin goatee.
- **Collar:** white wings rise beside the jaw in front (lime inner neck). In the back view the collar is a white wall up to the ears, which is how the model sheet reads from behind.
- **Hands and legs:** hands are white gloves under 2-row lime cuffs; trousers and boots are white/lavender.
- **Palette: npc_3 (shared).** It has lavender greys 5-7 for the coat and lime 8-A for the visor and cuffs.
  - Its only gap: no gold and no blonde. Hair is pale grey (reads platinum), and the gold buttons are left off the OW (1px gold reads as dirt).
  - Other candidates rendered:
    - npc_green: lime + gold, but no greys, so the coat is flat white.
    - npc_white: gold + greys, but no green, so the visor goes gold.
    - npc_pink: the visor goes blue.
  - Fallback `npc_faba.pal` adds blonde hair. It costs one OBJ palette, like the Cynthia/School Kid ♀ exceptions.
- `kit.check_ow(npc_3)`: OK.

## 2. Front pic: `faba_front_compare.png`, `faba_front_1x_lineup.png`, `faba_front_silhouette.png`, `faba_battle_intro_*.png` (+`_x3`)

**How it was built**
- **Base:** vanilla `magma_leader_maxie`. It is Faba's build: tall, narrow, knee-length coat, high collar, and hand on the hip as in Faba's model-sheet front view.
  - The silhouette, legs and hip hand are vanilla.
  - Red cape + grey shirt become one white coat with lavender shading; the slacks become white/lavender trousers; the boots get gold soles.
- **Repainted details:**
  - Bald scalp with pale-blonde tufts.
  - Big rounded lime lens (round 2) from brow to cheek, eyes visible, glint, white nose-pad bump.
  - Long nose, toothy grin, pale moustache and goatee, lime inner collar.
  - Collar (round 2, after user feedback): a symmetric stand-up high collar rising behind the jaw to ear height on both sides (outer edges vertical at x26/x43, white outer face, lavender inner face behind the jaw, throat shadow where the lapel line meets it, gold star pin on the right). The v1 flap that swept in front of and behind the face is gone (`faba/faba_front_v1.png` kept for the compare).
  - Long lime cuffs over white gloves.
  - Two gold buttons, two gold U-pocket trims.
- **Palette:** 16 slots. 1-4 skin, 5-7 coat lavender, 8-A lime, B-D gold/blonde, E white, F black.
- **Checks:**
  - `check_front` flags 5 pixels on the bottom edge. They are Maxie's own boot row (vanilla does the same).
  - Silhouette audit vs Maxie: growth 55 px (was 131 in v1), all of it the collar and the visor bulge; shrink 0. No limb grows past vanilla.
- **Variant B** moves the free hand to the chest (the official-art gesture) and hides the other behind the back.
  - It is drawn white-on-white over the coat and reads weaker at 1x. **A is recommended.**
- **Battle mocks:** on `building` (what Tower 2F gives today, `MAP_BATTLE_SCENE_NORMAL`) and on `orchid_office`.

## 3. Holon battle transition (B_TRANSITION_HOLON): `holon_logo_sheet.png`, `holon_transition_keyframes_x2.png`, `holon_transition.gif`

**Art**
- Same format as `team_aqua.png` + `.bin`:
  - 64x96 4bpp tileset. **62 tiles of 96** (Aqua uses 82).
  - 32x32 u16 tilemap (2048 bytes), palette 15.
- The logo is mirror-symmetric, so one quadrant is drawn and h/v-flipped. `holon_transition.py` decodes the saved files back to the screen and asserts a match.
- Drawn only in the existing `evil_team.pal` indices (black 1, greys 2-5, white 15), so the palette Aqua/Magma already load is **reused unchanged**.
- The design reads at GBA scale:
  - a black 6-point star, points up and down as on the card
  - a white disc with a grey rim and black outline
  - a jagged light-grey lightning ring (white core, grey glow, dark rim)

**Timing (simulated from the vanilla state functions):**
1. The generic intro: 3 grey flashes, 48 frames.
2. Aqua_Init/SetGfx.
3. PatternWeave_Blend1/Blend2: BG0 alpha 0→16, then the field under the logo 16→0, while the per-scanline sine weave amplitude decays 64→0.
4. FinishAppear.
5. FramesCountdown 60.
6. PatternWeave_CircularMask closes to black.

That is **217 frames ≈ 3.6 s**, the same as Aqua. The GIF is every 3rd frame, over the Holon Lake sphere screenshot (e2e 35b).

**Implementation (later, after approval)**
- Copy `faba/holon_logo.{png,bin}` to `graphics/battle_transitions/holon.{png,bin}`.
- In `src/battle_transition.c`:
  - `sHolon_Tileset/Tilemap` with INCGFX like Aqua (lines ~305).
  - `Holon_Init` = Aqua_Init with the Holon tileset; it still loads `sEvilTeam_Palette`.
  - `Holon_SetGfx` = Aqua_SetGfx with the Holon tilemap.
  - `sHolon_Funcs[]` = {Holon_Init, Holon_SetGfx, PatternWeave_Blend1, PatternWeave_Blend2, PatternWeave_FinishAppear, FramesCountdown, PatternWeave_CircularMask}.
  - `[B_TRANSITION_HOLON] = Task_Holon` in `sTasks_Main` (next to `[B_TRANSITION_AQUA] = Task_Aqua`, line 361). `sTasks_Intro` already defaults every transition to `Task_Intro`, so it needs no edit.
- Add `B_TRANSITION_HOLON` to the `enum BattleTransition` in `include/battle_transition.h`, before the count.
- **Selection:** in `GetTrainerBattleTransition` (src/battle_setup.c:914), after the mugshot check, return it for `TRAINER_CLASS_HOLON_RESEARCHER` and `TRAINER_CLASS_HOLON_LEADER`.
  - It is selected by class, like Aqua/Magma: one line, and it covers all 6 researchers + Faba.
  - Do not give Faba a `Mugshot:`, because the mugshot check runs first.

## 4. Class, placement, music

**Class: `TRAINER_CLASS_HOLON_LEADER` = `"Holon{NBSP}Leader"`**
- 12 chars, which fits the widened [17] field; the NBSP keeps "Holon Leader Faba" on one line.
- Prize 20 and BALL_MASTER, like Aqua/Magma Leader (src/battle_main.c:313).
- Pics/OW: `TRAINER_PIC_HOLON_LEADER_FABA`, `OBJ_EVENT_GFX_FABA` (npc_3, PALSLOT_NPC_3 as the researcher uses).

**Trainer slot:** reuse a vanilla ID with an alias (rule: overwrite vanilla slots, never Haru).
- Thematic pick: **slot 32 `TRAINER_SHELLY_WEATHER_INSTITUTE`** (the old Weather Institute 2F boss), aliased `TRAINER_HOLON_FABA`.
- The vanilla `Route119_WeatherInstitute_2F` map still references it. Check that the map is unreachable in Orchid before reusing it; otherwise use any unreachable grunt slot.

**Placement on Research Tower 2F** (20x11; checked against the layout's collision):
- **(11,6), facing down,** in the corridor in front of the orange specimen tank, centred between the two round drain machines.
- Researchers Tobias (18,6) and Kenji (11,9) already guard the approach. Kenji at (11,9) faces up toward him, as if reporting to him.
- `TRAINER_TYPE_NONE`, talk-to boss battle (`trainerbattle_single` with intro/defeat texts, then the post-script).
- **No stair blocker is needed.** 2F is the top floor and a dead end: the only exit is the stairs (17,1), and the head of research's office (x0-3) is reachable by rows 9-10 as well as row 6.
- Hide him with `FLAG_HOLON_FABA_DEFEATED` after the scene.

**Music**
- Battle: `MUS_VS_AQUA_MAGMA_LEADER`. It is a one-line case for `TRAINER_CLASS_HOLON_LEADER` in `GetBattleBGM` (src/pokemon.c ~5167).
- Encounter: `Music: Aqua` (MUS_ENCOUNTER_AQUA, sinister) rather than the researchers' `Intense`.
- A custom Faba/Aether theme could later go through the Cynthia MIDI pipeline. That costs +1-2 songs, which shifts the PH_* songs, and the tracks/DS budget has to be checked again.

## 5. Team (Lv 70-72, between Kenji 67-68 and Cynthia 70-74). All constants checked to exist.

| Mon | Lv | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Hypno | 70 | Leftovers | Insomnia | Calm | Psychic, Focus Blast, Nasty Plot, Hypnosis |
| Claydol | 70 | Light Clay | Levitate | Bold | Reflect, Light Screen, Earth Power, Psychic |
| Bruxish | 71 | Life Orb | Dazzling | Jolly | Psychic Fangs, Aqua Jet, Crunch, Ice Fang |
| Leafeon-δ (Grass/Steel) | 71 | Sitrus Berry | Leaf Guard | Adamant | Leaf Blade, Iron Head, X-Scissor, Swords Dance |
| Jolteon-δ (Electric/Steel) | 71 | Expert Belt | Volt Absorb | Timid | Thunderbolt, Flash Cannon, Shadow Ball, Volt Switch |
| **Metagross-δ** (Electric/Steel), ace | 72 | Weakness Policy | Clear Body | Adamant | Wild Charge, Meteor Mash, Zen Headbutt, Bullet Punch |

- The first three are Faba's USUM Psychic core. The three Deltas are "Power Spot-charged" Tower species.
- The Eeveelutions tie into the Eevee-δ the Tower gives away; Metagross-δ is the Tower's flagship (Ido has a Lv 63 one).
- IVs 31, no EVs, 4 Full Restores, AI Basic Trainer (same as Cynthia).
- Weak to Dark/Ghost/Fire/Ground overall. Bruxish's Dazzling stops priority.

## 6. Story beat (Faba is the one draining the Power Spots)

**Before** (on talk):
> Ah, the tourist. You've seen the fields? Wilted, yes. A small price.
> Every Power Spot on Holon flows into these machines. With that energy, my Delta Pokémon will rival any legend!
> I am Holon Leader Faba, and no child is pulling the plug!

**Defeat:**
> Impossible! My calculations were flawless!

**After:**
> Fine! Shut the machines down! The Power Spots will refill... eventually. But Holon WILL remember Faba!

Then he exits: fade, `removeobject`, set the flag.

**What changes after `FLAG_HOLON_FABA_DEFEATED`:**
- The machine sign text becomes "The round machine is silent. The stored energy is draining back into the ground."
- Researcher post-texts change.
- **The drained rings heal** around the Tower and the lake pillar island. Cheapest way: the rings use only palette 07 ("drained foliage", batch 4), so on Holon outdoor maps load the healthy General-02 greens into slot 7 when the flag is set (one palette swap, 0 tiles, 0 metatiles). The rest of Holon stays desaturated as its look.
- The farmer and researcher NPC lines in the village get after-versions.
- The sphere glow stays tied to the Cynthia event as built. Optionally it could glow brighter here.

## Decisions (user, 2026-11-19)

1. **OW palette: npc_3** (shared). `npc_faba.pal` / `faba_ow_ownpal.png` are unused fallbacks.
2. **Front pose: A** (hand on hip). Variant B is dropped.
3. **Visor:** too narrow in v1. **Enlarged** on the front pic and the OW to a big rounded lens from brow to cheek, wider than the head on the near side, with a nose-pad bump. Done this round; see it in review.
4. **Tower 2F battle background: office.** Set `battle_scene` to `MAP_BATTLE_SCENE_OFFICE` (orchid_office) in HolonResearchTower_2F/map.json. This affects Tobias/Kenji too.
5. **Transition: B_TRANSITION_HOLON for all 7** (Faba + the 6 Holon Researchers), selected by class in `GetTrainerBattleTransition`. **Plain greyscale**: evil_team.pal is reused, with no new palette.
6. **Music:** battle `MUS_VS_AQUA_MAGMA_LEADER` (class case in `GetBattleBGM`), encounter `Music: Aqua`.
7. **Team:** as proposed (Hypno, Claydol, Bruxish, Leafeon-δ, Jolteon-δ, Metagross-δ; Lv 70-72; items, natures and moves per the table).
8. **Story:**
   - The head of research gives the **Eevee-δ only after Faba's defeat** (gate her offer on `FLAG_HOLON_FABA_DEFEATED`, with a "not now" line before).
   - **The drained rings heal** after his defeat, through the palette-07 swap on Holon outdoor maps.
9. **Trainer slot: 32 (`TRAINER_SHELLY_WEATHER_INSTITUTE`)**, aliased `TRAINER_HOLON_FABA`, once Route119_WeatherInstitute_2F is confirmed unreachable in Orchid. Check this at implementation.

Still open, decide at implementation: whether Faba leaves the map or stays as a sulking NPC after the battle (draft: he leaves, `removeobject` + flag).

## Open questions (round 1, all answered above)

1. **OW palette:** npc_3 (recommended: shared, matches the Holon Researcher; pale-grey hair, no gold), or the own palette `npc_faba.pal` (blonde hair; costs one OBJ palette on 2F)?
2. **Front pose:** A, hand on hip, as on the model sheet (recommended), or B, hand at the chest from the official art (weaker white-on-white)? If you want the hunched official-art pose for real, it needs a redraw from a different base.
3. **Visor size:** front visor at 3 rows and OW at 2 rows, as drawn? Or a bigger, rounder lens?
4. **Battle background on Tower 2F:** switch the map to `MAP_BATTLE_SCENE_OFFICE` (orchid_office, recommended: lab/office floor), or keep `building`? This affects the researchers too.
5. **Transition:** use it for Faba + all 6 Holon Researchers by class (recommended)? Keep the greyscale evil_team palette, or add a tint (e.g. lime crackle via one new 16-colour palette)?
6. **Trainer slot:** slot 32 (Shelly, Weather Institute) aliased `TRAINER_HOLON_FABA`, if that map is unreachable (recommended)?
7. **Music:** vs Aqua/Magma Leader + Aqua encounter now (recommended), or a custom Faba theme later?
8. **Team:** as proposed (3 USUM + 3 Deltas, Lv 70-72), or all Deltas?
9. **Eevee-δ gift:** keep it available any time (as built), or have the head of research give it only after Faba's defeat, as thanks (recommended: better story beat, no new map work)?
10. **After defeat:** heal the drained rings via the palette-07 swap (recommended)? Faba leaves the map, or stays as a sulking NPC?
