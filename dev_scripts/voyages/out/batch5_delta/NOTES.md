# Batch 5: Delta Species (δ) design review

Review material only. No game files were changed. Scripts are in `dev_scripts/voyages/delta/` and run with the scratchpad venv Python:
`glyph.py`, `delta_table.py`, `wild_tables.py`, `palettes.py`, `ui_mocks.py` (run `glyph.py` first).

## Headline numbers

| | |
|---|---|
| Delta species | **91** in **35** lines. Tier A (core): 57 species / 21 lines. Tier B (optional): 34 species / 14 lines. |
| Sources | User list 21, TCG 65, extrapolated 5 (Leafeon/Glaceon/Sylveon-δ, Krabby-δ, Wingull-δ: these stages have no δ card) |
| Species IDs | SPECIES_LAOMEOW = 1577, NUM_SPECIES = 1578 today. With all 91: last δ = 1668, NUM_SPECIES = 1669. Headroom to the 11-bit limit (2047) = **378**. |
| National dex | #1031–#1121 (after NATIONAL_DEX_LAOMEOW = 1030) |
| Tosa dex | Laomeow is Tosa #219. Deltas become #220 onwards (all 91 → #220–#310) |
| Save cost | +12 bytes each for `dexSeen` and `dexCaught` (SaveBlock1). The last built `pokeemerald.elf` has gSaveblock1 = 0x3D50 (15696) of 15872, so 176 bytes are free and this fits. The build may be stale; the STATIC_ASSERT will confirm it. |
| Name length | All 91 names are ≤ 12 characters, counting "-δ" as 2. The longest are **Farfetch'd-δ, Charmander-δ, Charmeleon-δ, Feraligatr-δ = 12**. Correction to delta_requests.md: Farfetch'd-δ is 12 characters, not 11. 17 names are longer than 10 characters (see §5). |
| δ byte | **0x18** in charmap.txt (`'δ' = 18`). It is blank in all 9 Latin fonts, and Latin text never uses it. |

## 1. Delta list (`delta/delta_table.csv`, `delta_table.png`)
CSV columns: base constant, `SPECIES_X_DELTA`, name, character count, type1/type2, evolves-from (δ constant), base types, line, tier, home map, source, TCG card, confidence.

- **User lines (tier A):** Stantler (Psychic); Ralts/Kirlia/Gardevoir/Gallade (Grass); Dratini/Dragonair/Dragonite (Electric); Purrloin/Liepard and Glameow/Purugly (Fairy); Drifloon/Drifblim (Flying/Fire); Klink/Klang/Klinklang (Rock/Ice); Farfetch'd (Steel); Pancham/Pangoro (Psychic); Relicanth (Grass/Ground).
- **TCG tier A:** Larvitar, Bagon and Beldum lines (EX Delta Species); the Eevee family; Magikarp/Gyarados, Pichu line, Horsea line, Trapinch line, Meowth/Persian (Holon Phantoms); Charmander line (Crystal Guardians); Feebas/Milotic (Dragon Frontiers).
- **TCG tier B:** Pidgey, Psyduck, Oddish (with Bellossom), the 4 fossil lines (Holon Phantoms); Treecko, Krabby/Kingler, Wingull/Pelipper (Crystal Guardians); Swablu, Mareep, Totodile, Vulpix (Dragon Frontiers).
- **Where the TCG types come from:** the pkmncards.com δ listing (191 cards). The saved Bulbapedia Holon page confirms several: Magikarp δ is Metal, Gyarados δ Lightning/Metal, Anorith δ Metal, Armaldo δ Fighting/Metal, and Meowth δ dual Metal.
- **How TCG types become game types:** Lightning→Electric, Metal→Steel, Darkness→Dark, Colorless→Normal. Fighting stays Fighting, except Armaldo, which becomes Rock.
- **Confidence:**
  - *high*: a δ card with that type exists.
  - *med*: the game type is a judgement call. This covers Gloom/Vileplume (TCG Psychic can also mean Poison), Armaldo, and the Mareep line (Colorless).
  - *extrap*: no card exists for that stage.
  - *user*: the type is your choice; any TCG difference is noted in the CSV.
- **Conflicts between the TCG sets:** Tyranitar and Salamence are Fire/Steel in EX Delta Species but Lightning or Water as Dragon Frontiers ex. I used EX Delta Species, the Holon set. The TCG has Ralts/Gardevoir δ as Fire or Psychic/Metal, but your Grass choice stands.
- **No legendaries included** (Latias/Latios/Rayquaza/Mewtwo/Deoxys δ exist in the TCG). No δ Megas.
- The scripts check that no Delta keeps its base typing; none does.

## 2. Holon's Pokémon (plain wild encounters, no new species)
Magnemite, Magneton, Voltorb, Electrode (EX Delta Species) and Castform (Holon Phantoms). Magnezone was never a Holon's card. They appear in the Research Tower table and as one 1% Castform slot at the Lake.

## 3. Wild tables (`delta/wild_tables.csv`, `wild_tables.png`)
**Levels:** the Elite Four are Lv 46–55 and Wallace is Lv 55–58. The Tiksi Regi Guardians are 52–55. Holon therefore runs **Lv 50–65**: Coast 50–58, Village 52–58, Tower 55–60, Lake 55–65 (where Cynthia is fought).

| Map | Delta share (by encounter rate) | Notes |
|---|---|---|
| Mirage Forest coast | land 45%, surf 35%, rods 30/60/55% | Mostly Crystal Guardians / Dragon Frontiers Deltas: Wingull-δ, Swablu-δ, Flaaffy-δ, Treecko-δ, 1% Charmander-δ/Totodile-δ. Night: Drifloon-δ, Vulpix-δ, Ninetales-δ. Super rod: Relicanth-δ 15%. |
| Holon village | land **56%** (day and night), canals 6%, rods 70/80/60% | Day: Glameow-δ, Farfetch'd-δ, Stantler-δ, Pancham-δ, Ralts-δ. Night: Purrloin-δ, Liepard-δ, Drifloon-δ/Drifblim-δ. 1%: Larvitar-δ, Bagon-δ, Pupitar-δ, Shelgon-δ. Fishing for the Dratini-δ line. |
| Research Tower | δ 36%, Holon's 60%, normal 4% | Klink-δ line, Beldum-δ/Metang-δ, 1% Eevee-δ, Porygon2. |
| Holon Lake | **99–100%** | Pidgeotto/Pikachu/Meowth/Gloom/Trapinch lines. Rock Smash on the stone domes gives the 4 fossil Deltas. Surf: Psyduck/Seadra/Kingdra/Gyarados-δ. Rods: Magikarp/Horsea/Feebas/Milotic-δ. 1% Castform is the only non-Delta. |

The time-of-day split uses OW_TIME_OF_DAY_ENCOUNTERS, which is on. The base table is the TIME_MORNING fallback; `_Night` tables override it. The Tower and water tables are the same at all times.

Coverage check (in the script): every δ family has a wild member or a gift. 26 δ species are obtained only by evolving or breeding (listed on the PNG).

Suggested extras:
- **Eevee-δ Lv 50 as a gift** from a Holon Researcher in the Tower. It has 8 evolutions, and 1% wild alone is a grind.
- **Shiny Gyarados-δ Lv 65** as a static encounter at the Lake. This nods to Holon Phantoms' "Shining Gyarados" and the Lake of Rage.

## 4. Palettes (`palettes_2x.png`, proposed `.pal` files in `delta/palettes/`)
The six examples use the repo's GBA front pics and palettes. Only the palette changes; colours are snapped to 5-bit.

| Delta | Recolour |
|---|---|
| Gyarados-δ | Gold body, steel belly |
| Eevee-δ | Steel fur |
| Charizard-δ | Yellow body, steel wings, blue tail flame |
| Dragonite-δ | Lemon body, blue wings, white belly |
| Gardevoir-δ | Leaf-green gown, deep green hair, pink horn |
| Klinklang-δ | Ice-blue gears, rocky small gear |

**Recommendation: recolour.** If Deltas keep normal colours, they look identical to the base species everywhere a name isn't shown (sprite, follower, dex pic), and in battle the player has nothing to read the type from. A recolour also costs only 1–2 new `.pal` files per species. The UI mocks already use the gold Gyarados-δ; the in-context look reads well.

## 5. δ glyph + UI (`glyph_closeup.png`, `ui_overview.png`, `ui_*_1x/3x.png`)
- **Free bytes:** F8, F9 and FC are not free; they are control prefixes. In the Latin fonts, these codes are only mapped to kana and have blank glyphs:
  - 0x18, 0x1F
  - 0x2F–0x33
  - 0x3B–0x4F
  - 0x5E–0x67
  - 0x69–0x76
  - 0x78
  - 0x87–0x9F

  0x37 is excluded because it is CHAR_BARD_WORD_DELIMIT. **Use 0x18**, the vanilla Japanese ね slot, also commented as the unused â.
- **Glyph:** built from each font's own 'o' bowl, plus an S-hook up to the 'd' ascender, with the vanilla drop-shadow rule. It covers all 9 Latin fonts: normal, short (+COPY_1..3), narrow, narrower, small, small_narrow, small_narrower, short_narrow, short_narrower. The width equals 'o' (6/6/5/4/5/5/4/5/4).
- **Casing:** the game uses mixed case, "Gyarados-δ" (expansion `speciesName` and the Orchid UI); "GYARADOS-δ" never appears.
- **Fit results** (font picked by the ROM's own fit rules; full list in `delta/ui_fit_report.json`):

| Screen | Rule | Gyarados-δ (10 chars) | 12-character names |
|---|---|---|---|
| Battle healthbox | small chain, 55px | small, 50px | small_narrower, 46px |
| Party slot | small chain, 50px | small, exactly 50px | small_narrower, 46px |
| Summary header | normal chain, 54px at Lv 2 digits | narrow, 50px | narrower, 46px |
| PC info | normal if ≤ 66px, else narrow | normal, 59px | narrow, 59/76px |
| Pokédex list | narrow chain, 85px | narrow | narrow, up to 59px |

  Nothing clips. Expansion already ships 12-character species names (e.g. Crabominable), so the fit code is already exercised.
- **Party lead slot:** in the mock, "Gyarados-δ" at exactly 50px runs into the gold card's right border (`ui_party_3x.png`). Check this in the emulator. If it clips, give the lead slot a fit width of about 45.
- **10-character truncation (VANILLA_POKEMON_NAME_LENGTH / MON_DATA_NICKNAME10):** this happens on TV shows (tv.c, global.tv.h), contest winners and museum paintings (contest.c), daycare mail (daycare.c `GetMonNicknameVanilla`), and Battle Tower records and interviews (battle_tower.c, global.h). The 17 names longer than 10 characters lose the δ in those places ("Charmeleon-δ" becomes "Charmeleon", "Gardevoir-δ" becomes "Gardevoir-"). No main UI screen truncates.

## 6. Implementation notes (no code)
1. **`include/constants/species.h`:** `SPECIES_<X>_DELTA` enum entries after SPECIES_LAOMEOW, before SPECIES_CUSTOM_END.
2. **`include/constants/pokedex.h`:**
   - `NATIONAL_DEX_<X>_DELTA` after NATIONAL_DEX_LAOMEOW.
   - The `NATIONAL_DEX_COUNT` line in the P_GEN_9 branch points at the last δ.
   - `F(<X>_DELTA)` after `F(LAOMEOW)` in FOREACH_SPECIES_IN_HOENN_DEX_ORDER.
3. **New file `src/data/pokemon/species_info/delta_families.h`**, `#include`d after orchid_families.h in `species_info.h`.
   - Generate it with a script (e.g. `delta/gen_species.py`). C can't copy another designated initializer at compile time.
   - Copy the base block, then change `.types`, `.speciesName` (`_("Gyarados-δ")`), `.natDexNum`, `.description` (new δ dex text), `.palette`/`.shinyPalette` and `.evolutions` (targets become `_DELTA`).
   - **Drop** `.formSpeciesIdTable`/`.formChangeTable`, so there are no Megas, G-Max or cosplay forms.
   - Keep the pic, icon, footprint, cry, learnset pointers and abilities.
   - Wrap each entry in the same `#if P_FAMILY_*` guards as its base.
   - Optionally add an `isDeltaSpecies:1` bit to `struct SpeciesInfo` (`include/pokemon.h`). The dex and summary could use it for a δ badge, and the egg rule could use it.
4. **Graphics (`src/data/graphics/pokemon.h`):** `gMonPalette_<X>Delta` / `gMonShinyPalette_<X>Delta` via `INCGFX_U16("graphics/pokemon/<x>/delta_gba.pal", ".gbapal")` plus a non-GBA twin. Followers (OW_FOLLOWERS_ENABLED) need a recoloured `overworld_delta.pal` too, or they show base colours. Icons can only use the 6 shared icon palettes: either pick the closest `iconPalIndex` or accept base-coloured icons (see Q6).
5. **Evolutions:**
   - Base species stay as they are. Each δ evolves only into δ.
   - Copy the conditions as they are: Eevee stones/friendship/location, Pangoro's Dark-in-party, Kirlia→Gallade with a Dawn Stone on a male.
   - Stantler-δ drops its Wyrdeer evolution (Psyshield Bash ×20); Farfetch'd (Kanto) has none.
6. **Text / tools:**
   - `charmap.txt`: `'δ' = 18`.
   - The 9 `graphics/fonts/latin_*.png`: δ at cell (8,1), which is 0x18. Patched copies are in `delta/fonts/`.
   - `src/fonts.c`: width `[0x18]` in all 9 width tables (values are in `delta/fonts/widths.json`).
   - `tools/poryscript/font_config.json`: δ widths for auto line-wrapping.
   - The naming-screen keyboard has no δ, so players can't type it. Choosing the default name still restores "Gyarados-δ".
7. **Learnsets:** the δ entries point at the base `s<X>LevelUpLearnset` / `TeachableLearnset` / `EggMoveLearnset`. Nothing new is needed unless Q4 adds moves.
8. **Eggs:** `GetEggSpecies()` (daycare.c:475) walks back through the evolution tables. A δ mother therefore already hatches the δ base form (Gyarados-δ → Magikarp-δ, Gallade-δ → Ralts-δ, Raichu-δ → Pichu-δ).
   - **Recommended rule: either δ parent → δ egg.** In `DetermineEggSpeciesAndParentSlots` (daycare.c:917), after `fatherEggSpecies` is set: if the father is δ and `GetEggSpecies(father)` is the δ twin of the mother's egg species, use the δ species. δ × Ditto → δ.
   - Alternative: the Gen 7+ regional-form rule, where only the mother passes on Delta, or the father if he holds an Everstone.
9. **Dex completion:** `HasAllHoennMons()` (pokedex.c:5534) loops over `HOENN_DEX_COUNT - 1`. Appending Deltas makes the Tosa diploma require all of them (see Q8).
10. **Testing:** targeted `TESTS=` only (for example a species-data or daycare test). Use the mGBA headless bridge for the δ glyph and the party lead slot.

## Open questions (recommendation first)
## Decided (user, 2026-11-19): every recommendation below accepted as written
Tier A (57 species / 21 lines) now, tier B later; Dragonite-δ pure Electric; Ralts line pure Grass; 2–3 δ STAB level-up moves per line; keep type-tied abilities for v1; recolour palettes; either δ parent → δ egg; Deltas kept in the Tosa list but excluded from the diploma count; accept 10-char truncation; δ at byte 0x18 with the drawn glyph; Eevee-δ gift + shiny Gyarados-δ static encounter (and remaining Qs per their recommendations).

1. **Scope:** ship tier A (57 species / 21 lines) first, and tier B later or never? *Recommend: tier A now.* Tier B's fossils, starters and Dragon Frontiers lines can follow once tier A plays well.
2. **Steel on final stages:** your lines currently have no Steel. In EX Delta Species, Dragonite δ is Lightning/Metal. Keep Dragonite-δ pure Electric? *Recommend yes; your call wins.* For the TCG lines I kept the TCG's "+ Steel on the final stage" pattern.
3. **Ralts line:** Gardevoir-δ / Gallade-δ pure Grass (your list), or Grass/Fairy and Grass/Fighting? *Recommend pure Grass.* It's simpler, and Delta replaces both types.
4. **STAB moves:** copying learnsets means Gyarados-δ learns no Electric moves and Charizard-δ no Electric moves until TMs. *Recommend a small per-line "δ move patch": 2–3 level-up moves of the new type.* Otherwise the typing is cosmetic in battle.
5. **Type-tied abilities** (Blaze/Torrent/Overgrow on the δ starters, Swift Swim, etc.): keep them or swap them? *Recommend keep for v1.* List the swaps on the next review if you want them.
6. **Recolour** (§4): *recommend yes.*
   - Shiny Deltas: *recommend the base shiny palette.* The alternative is a second hand-made palette.
   - Icons stay base-coloured (only 6 icon palettes): accept? *Recommend accept.*
   - Followers need a δ overworld palette too: *recommend yes.*
7. **Eggs** (§6.8): either δ parent → δ (*recommended*), or the mother/Everstone rule?
8. **Dex placement:** Deltas at the end of the Tosa dex mean the Tosa diploma needs all 91. *Recommend: keep them in the Tosa list but exclude Deltas (and Holon-only Pokémon) from the diploma count*, or give Deltas their own "HOLON" dex mode later.
9. **10-character truncation** (TV, contest painting, daycare mail, Battle Tower record): accept that 17 names lose the δ there? *Recommend accept.* Widening those save structs costs save space, and most of those features are vanilla leftovers.
10. **δ byte 0x18 and the glyph shape:** approve, or redraw the hook (for example a rounder top on the normal font)?
11. **Gifts:** Eevee-δ from a Holon Researcher at the Tower, and a shiny Gyarados-δ static at the Lake: *recommend both.*
12. **Wild levels** 50–65 with base forms kept (Larvitar-δ/Bagon-δ at 52, Dratini-δ at 55): OK as post-game flavour, or evolve them to match the level? *Recommend keep.* It's rare-slot flavour, as in vanilla post-game areas.
13. **Stantler-δ → Wyrdeer-δ and Farfetch'd-δ → Sirfetch'd-δ:** *recommend no, as already proposed:* they stay single-stage. Blocking Wyrdeer means leaving the evolution out of the δ entry.

## PNGs
- `delta_table.png`: all 91 Deltas with δ / base types, tier, home map, source, TCG card, confidence
- `wild_tables.png`: the 4 Holon maps, every table and slot, δ / Holon's / normal share, gifts, coverage check
- `palettes_2x.png`: 6 normal vs Delta front pics at 2x, with swatches
- `glyph_closeup.png`: δ next to o d a e 6 D in all 9 fonts at 6x, and "Gyarados-δ" / "Farfetch'd-δ" at 3x
- `ui_overview.png`: all UI mocks at 1x with 3x zooms of the name areas
- `ui_battle_gyarados_{1x,3x}.png`: Gyarados-δ (gold palette) vs Kingdra-δ
- `ui_battle_12char_{1x,3x}.png`: Charmeleon-δ vs Farfetch'd-δ
- `ui_summary_gyarados_{1x,3x}.png`, `ui_summary_12char_{1x,3x}.png`
- `ui_party_{1x,3x}.png`: Gyarados-δ lead, Charmeleon-δ, Farfetch'd-δ, Kingdra-δ
- `ui_pc_gyarados_{1x,3x}.png`, `ui_pc_12char_{1x,3x}.png`
- `ui_dex_list_{1x,3x}.png`: Tosa list #216–#224 with Deltas from #220
