# Delta stream: done (tier A, 57 species / 21 lines)

Uncommitted in the worktree `pokeorchid-voy-delta` (detached at bc3f480c7c). Clean `make -j8` build.
`grep gHarnessKeys pokeemerald.map` = 0. SaveBlock1 = 0x3D68 (15720 of 15872 bytes).

## What changed
| Area | Files |
|---|---|
| Generator (re-runnable, `--tiers AB` later) | `dev_scripts/voyages/delta/gen_delta.py`, `delta_text.py` (dex text + δ move patches). Run with the scratchpad venv python `-W ignore`; `--sheet` writes `shots/palettes_contact_sheet.png` |
| Species | `SPECIES_<X>_DELTA` = 1578–1634 in `include/constants/species.h` (between gen_delta markers, after LAOMEOW). The new file `src/data/pokemon/species_info/delta_families.h` is generated from each base block: δ types, the name "<Name>-δ", `.isDeltaSpecies = TRUE`, new natDex, category and description, δ palette and δ follower palette, δ level-up learnset, and evolutions retargeted to δ. Form and Mega tables are dropped. It keeps the same `#if P_FAMILY_*` / cross-evo guards as the base. Included from `species_info.h` after orchid_families.h |
| Struct | `include/pokemon.h`: `isDeltaSpecies:1` (padding4 7). Helpers in `pokemon.c`: `IsDeltaSpecies`, `GetDeltaBaseSpecies`, `GetDeltaSpecies`, backed by the generated `src/data/pokemon/delta_species.h` |
| Learnsets | `src/data/pokemon/delta_learnsets.h`: the base Gen-9 learnset plus 2–3 δ moves per line, marked `// δ`. A move the base already learns is skipped. Magikarp-δ gets only Iron Defense. Gallade-δ also gets Leaf Blade at 1. Teachable and egg moves point at the base |
| Graphics | `src/data/graphics/delta_pokemon.h` (included after `data/graphics/pokemon.h`). Every δ species gets new `graphics/pokemon/<x>/delta_gba.pal` (and `delta.pal` for the non-GBA twin) and `overworld_delta.pal` |
| Dex | National #1031–1087 (`NATIONAL_DEX_COUNT` = MILOTIC_DELTA); Tosa #220–276 (`HOENN_DEX_COUNT` updated); entries inserted after their base in the 3 `pokedex_orders.h` lists |
| Diploma | `HasAllHoennMons` (pokedex.c) skips δ species |
| Eggs | `daycare.c` `DetermineEggSpeciesAndParentSlots`: a δ father with the non-δ counterpart mother gives a δ egg. δ mother and δ × Ditto already worked through GetEggSpecies |
| Glyph | `charmap.txt` `'δ' = 18`; 9 patched `graphics/fonts/latin_*.png` (only cell 0x18 differs); `src/fonts.c` widths [0x18] = 6/6/5/4/5/5/4/5/4; `tools/poryscript/font_config.json` δ = 6 |
| Save | `include/global.h`: `NUM_DEX_FLAG_BYTES` reserves 1122 slots (tier A + B), so tier B won't shift the save again |
| Test | `test/daycare.c` "(Daycare) Orchid: either Delta parent passes Delta on to the Egg" |

## Palettes
- **Hand-made:** the 6 approved palettes (Gyarados, Eevee, Charizard, Dragonite, Gardevoir, Klinklang) are used as they are.
- **Overrides:** 11 species have hand-tuned family overrides: Ralts/Kirlia/Gallade (leaf gown, deep-green hair, pink horn), Flareon, Umbreon, Vibrava, Flygon, Klink/Klang (to match Klinklang), Sylveon and Milotic.
- **Automatic:** the other 40 are recoloured automatically. The largest hue family moves to the primary type colour and the second to the secondary type.
- **Followers:** follower palettes are mapped from each species' δ front palette (`transfer_palette`).
- **Icons:** the closest of the 6 shared icon palettes is chosen.
- **Shiny:** δ shinies use the base shiny palette (decision Q6). Change `.shinyPalette` in the generator if you want δ shinies.
- **Review sheets:** `shots/palettes_contact_sheet.png` and `shots/followers_contact_sheet.png`.

## Debug
Debug menu → Give X → Pokémon (Basic/Complex) takes a species id: Ralts-δ = 1579, Magikarp-δ = 1617, Gyarados-δ = 1618 (Stantler-δ 1578 … Milotic-δ 1634, in `delta_table.csv` order).

## Verification
- **Targeted tests:**
  - `make check TESTS="(Daycare) Orchid"`: PASS. Six cases: δ mother, δ father × base Magikarp, base × base, Gallade-δ × Gardevoir, Gallade-δ × Ditto, Raichu-δ mother.
  - `TESTS="Species names fit"`: all 16 tests pass.
  - `TESTS="Species dex entries"`: PASS.
- **Headless mGBA:** run on a copy of the engine-dev save, with a harness-only hack of debug "Heal party" / "Clear Pokerus" (`harness/hack.py`, reverted). Shots are in `shots/`:
  - **party.png:** the δ glyph renders. "Gyarados-δ" fits the gold lead card (no clipping), and so do Charmeleon-δ and Farfetch'd-δ.
  - **summary_*.png:** Gyarados-δ shows ELECTR/STEEL, Tosa No. 260 and Wild Charge from the δ patch. Ralts-δ shows GRASS, No. 221.
  - **pc_box.png:** Gyarados-δ with ELECTR/STEEL.
  - **dex_list.png / dex_entry_gyarados_delta.png:** #259 Magikarp-δ and #260 Gyarados-δ, with the "Atrocious" category, the Holon text and the gold sprite.
  - **battle_*.png:** healthbox names. `gBattleMons[0/1]` = species 1618, types [14, 9] (Electric/Steel). Magikarp-δ = [9, 9] (Steel).
  - **evo_*.png:** Magikarp-δ Lv19 → Lv20 → "evolved into Gyarados-δ!" → learned Bite.
  - **follower_gyarados_delta.png:** the gold follower.

## Known gaps / notes
- **Existing saves:** the dex flag arrays grew, so `dexCaught` and every SaveBlock1 field after it shift.
  - Old saves (including the engine-dev save) show wrong Own counts and stray caught balls in the dex list. The seen/caught flags are misread.
  - This can't be avoided without a migration. Space is now reserved, so tier B won't shift the save again.
- **Learnsets follow Gen 9 only:** δ learnsets are generated from `level_up_learnsets/gen_9.h`. If `P_LVL_UP_LEARNSETS` changes, re-run the generator against that file.
- **Automatic palettes:** they are first passes, reviewed only on the contact sheets. The weak spots listed here
  before (Gyarados-δ follower, Drifloon-δ, Vibrava-δ) were fixed in the tier-B pass below.
- **Species checks keyed on base species don't apply:** abilities are kept (v1), and type-tied abilities stay. Checks such as Leek/Light Ball, Pikachu forms and Eevee-partner don't recognise δ.
- **Holon-only species:** they are not excluded from the diploma (none exist yet). Only δ species are skipped.
- **Truncation:** 10-character truncation (TV, contests, Battle Tower) drops the δ as accepted. The naming keyboard has no δ.
- **Not placed (tier A pass):** wild encounters, gifts and statics were the Holon stream's work; the Holon wild tables now use the Deltas (tier-B section).

# Tier B (34 species / 14 lines), polish pass in `pokeorchid-pol-delta`

Uncommitted (index untouched). Clean `make -j8`; `grep gHarnessKeys pokeemerald.map` = 0.

## What changed
| Area | Change |
|---|---|
| Generator | `gen_delta.py` now defaults to `--tiers AB`. Rows are sorted A-then-B, so tier-A ids/dex numbers are unchanged (re-running `--tiers A` alone still reproduces tier A byte for byte). New `Normal` type colour (Mareep line). |
| Species | `SPECIES_PIDGEY_DELTA` … `SPECIES_NINETALES_DELTA` = 1635–1668 (NUM_SPECIES 1669), CSV order. Megas/G-Max forms dropped as in tier A; Gloom-δ evolves to Vileplume-δ (Leaf Stone) and Bellossom-δ (Sun Stone). |
| Dex | National #1088–1121 (`NATIONAL_DEX_COUNT` = NINETALES_DELTA), Tosa #277–310 (`HOENN_DEX_COUNT` 311), each inserted after its base in the 3 order lists. Dex text + categories for all 34 in `delta_text.py`. |
| Moves | `LINE_MOVES` for the 14 lines (2–3 δ STAB moves each). `SPECIES_MOVES`: Pidgeot-δ Steel Wing / Kingler-δ Iron Head / Cradily-δ Flash Cannon as evolution (Lv 0) moves; the Oddish line changes type per stage (Oddish/Bellossom Water, Gloom/Vileplume Psychic). |
| Save | No shift: `NUM_DEX_FLAG_BYTES` stays 141 (1122 reserved slots = exactly 1121 + 1). New `STATIC_ASSERT(POKEMON_SLOTS_NUMBER <= ORCHID_DEX_FLAG_SLOTS)` in `src/save.c` guards it. SaveBlock1 = 0x3CE8 in this merged tree (unchanged by tier B; only the dex arrays depend on the species count, `USE_DEXNAV_SEARCH_LEVELS` is FALSE). |
| Holon wild | `restore_holon_wild.py` swapped the 46 fallback slots (26 distinct tier-B species, day + night tables) in `src/data/wild_encounters.json` back to the Deltas in `holon/wild_delta.json`. Only the 7 Holon tables; no other diffs vs `wild_delta.json`. |
| Eggs/followers | Covered by the generator as in tier A (`delta_species.h` pairs; `overworld_delta.pal` per species). |

## Palettes
- Hand overrides added (contact sheet checked): Psyduck (amber), Kabuto/Kabutops (gold shell), Anorith (steel, blue fins),
  Swablu/Altaria (teal + aqua cotton), Krabby (charcoal shell, orange glow, matching Kingler-δ steel), Mareep line
  (white wool, one pinkish-beige skin, silver orb). The other tier-B palettes are automatic.
- Tier-A fixes: Vibrava-δ blossom-pink wings + leaf-green frames; Drifloon-δ/Drifblim-δ hot-air balloons (Fire envelope,
  sky-blue X/streamers); Gyarados-δ follower now gold (`FOLLOWER_OVERRIDES`).
- Followers: still `transfer_palette` by default; `FOLLOWER_OVERRIDES` (Gyarados, Kabuto, Oddish, Lileep) and
  `FOLLOWER_FAMILY` (Psyduck, hue-family transfer) for the ones that barely moved. A full HSV transfer was tried and
  rejected (worse on most tier-A followers).
- Sheets: `shots/palettes_contact_sheet.png` (all 91), `shots/followers_contact_sheet.png` (base | plain transfer | final).

## Verification
- Tests: `(Daycare) Orchid` PASS; `Species names fit` 16/16; `Species dex entries` PASS.
- Headless (harness `harness_b/`: `build_b.sh <save copy>` + `s1_summary.py`, `s2_holon_wild.py`, `s3_evolve.py`; debug.c restored from backup), shots in `shots_tierB/`:
  - `dex_pidgeot_delta.png`: Tosa #279 Pidgeot-δ, ELECTR/STEEL, "Bird", tier-B text, steel sprite.
  - `summary_pidgeot_strip.png`: party with Feraligatr-δ, Kabuto-δ, Ampharos-δ, Vileplume-δ, Wingull-δ; Pidgeot-δ summary ELECTR/STEEL, No. 279, Discharge (δ).
  - `holon_wild_strip.png` + `holon_wild_log.txt`: Holon Mirage Forest grass, 1st encounter = wild Ninetales-δ Lv56 (species 1668, `gBattleMons` types PSYCHIC); player Pidgeot-δ types [ELECTRIC, STEEL].
  - `evolve_strip.png`: Kabuto-δ Lv39 → Lv40 → "evolving" → Kabutops-δ (gold), learns Slash.
  - `follower_pidgeot_delta.png`: steel Pidgeot-δ follower.
- Known: icon palettes are the nearest of the 6 shared ones (Pidgeot-δ icon stays orange). Pelipper-δ and Wingull-δ
  are mostly white birds, so their δ change (blue → yellow trim) is modest.
