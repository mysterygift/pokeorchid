# Wavebreak Voyages — status / handoff (2026-11-19 ~17:05)

Plan: /Users/arandavies/.claude/plans/enchanted-leaping-pie.md · Decisions (source of truth): DECISIONS.md · Worktree: ../pokeorchid-voyages (branch `voyages`, from engine-dev; nothing committed; no data/src/include edits yet — Phase 1 design review only).
Pillow venv: /private/tmp/claude-501/-Users-arandavies-Development-pokemon-orchid-pokeorchid/72fd3b53-a4f0-4cad-8c0a-22b751dccb01/scratchpad/venv/bin/python (scratchpad may be wiped — recreate with `python3 -m venv … && pip install pillow`).

## Batches (mockups, all under out/)
| Batch | Folder | State |
|---|---|---|
| 1 Wavebreak hut/dock/props, hut interior, Eon, Newmoon, Fullmoon | out/batch1 | DONE, all decided |
| 2 Sevii 1–3 (FRLG translations, frlg_translate.py) | out/batch2 (v1 kept in batch2_v1) | DONE; re-rendered with rock/sea-route fixes 16:39 |
| 3 Sevii 4–7 + gTileset_SeviiIslands art + interiors | out/batch3, out/batch3/tileset, out/interiors | IN PROGRESS: maps rendered 16:40, tileset art sheets 16:48 (cottages, stall, Onix tails, Rocket Warehouse, Dotted Hole door, Memorial Pillar, Tanoby chambers, budget.txt); interiors helper translating Sevii interiors (14 done by 17:00, incl. unrequested Dotted Hole 1F + Monean Chamber — flag). Waiting for its final report + NOTES. |
| 4 Holon (coast, village, tower 1F/2F, lake, ruins) + gTileset_Holon | out/batch4 | DONE, all decided (round 2) |
| 5 Delta species + δ glyph | out/batch5_delta | DONE, all recs approved |
| 5 Cynthia + Holon Researcher + music | out/batch5_trainers, trainers/ | DONE, final team approved |
| 6 Region maps (Eon clouds, Sevii, placeholders) | out/batch6_regionmap, regionmap/IMPLEMENTATION.md | DONE, decided |
| 7 Changu Battle Café | out/batch7_cafe, cafe/ | DONE, decided (variant A, Battle Café, red roof, barista greets) |

## Review page
Draft v1 published: https://claude.ai/artifact/HcwTeXWHV1Y8BbjaVVxGrX — rebuild with `python3 dev_scripts/voyages/build_review.py`, copy review/ to the scratchpad (Artifact root must be under the session dirs or scratchpad), republish the same scratchpad index.html path (or pass `url` from a new conversation). Add open questions to OPEN in build_review.py.

## Phase 2 (implementation) — started after the user's go ("when limits reset you can start implementing")
voyages fast-forwarded to engine-dev bc3f480c7c. Rules: IMPLEMENT_BRIEF.md. Streams (detached worktrees, uncommitted; coordinator merges by staged diff into voyages):
- core: ../pokeorchid-voy-core — voyage system, ferry cutscene, Wavebreak hut/dock, Eon, Newmoon, Fullmoon, legendaries
- delta: ../pokeorchid-voy-delta — tier-A Delta species + δ glyph
- trainers: ../pokeorchid-voy-trainers — Cynthia, Holon Researcher, music, Battle Café
- sevii: ../pokeorchid-voy-sevii — gTileset_SeviiIslands + all Sevii maps/interiors (defaults for the 6 open Qs, flippable)
- holon: ../pokeorchid-voy-holon — gTileset_Holon + General_Holon palettes copy + Holon maps (placeholders for trainer/Delta deps)
core owns IsVoyageMapSec (overworld.c). Remaining after merges: swap placeholders (Researcher teams → Deltas, Holon wild → Deltas, Cynthia script hook), region maps stream (regionmap/IMPLEMENTATION.md), voyage table hooks for Sevii/Holon arrivals.
Headless mGBA lock: /tmp/voyages_mgba.lock (mkdir lock; never pkill other runs).

## Merge log
- delta → voyages (applied staged diff, excluding dev_scripts/voyages/*, then rsync of the stream's dev_scripts/voyages/delta/). 
- trainers → voyages (same method). Combined `make -j8` clean, no harness code.
- core → voyages: conflicts in layouts.json + specials.inc (both-side appends) resolved by keeping both; combined build clean. Worktrees voy-delta/trainers/core removed after merge (disk was full); patches kept in scratchpad (*.patch).
- holon → voyages: conflicts map_groups.json/layouts.json/event_objects.h (appends, kept both). swap_placeholders.py run (Cynthia/Researcher/Delta names), HOLON arrival = MAP_HOLON_MIRAGE_FOREST (5,36), coast Sailor → Voyage_EventScript_Sailor, researcher teams swapped to Deltas (23 mons), 26 tier-B Delta refs in Holon wild tables fell back to base species. Combined build clean.
- sevii → voyages: conflicts event_scripts.s/map_groups.json/layouts.json (kept both; group order Voyages, Holon, Sevii) + wild_encounters.json merged as JSON (41 Sevii tables added). SEVII arrival = MAP_ONE_ISLAND_HARBOR (8,4); One Island harbour ferryman got a "Wavebreak & beyond" option → Voyage_EventScript_Sailor. Combined build clean. All stream worktrees removed (patches in scratchpad).
FINAL STEP (user go): commit voyages + merge into engine-dev once polish + region maps are done (check engine-dev's uncommitted Porymap edits first).
REGION MAPS + E2E: done (e2e/DONE.md), all checks passed.
POLISH RUNNING in snapshot worktrees (base tree 279810baf50b = voyages index; merge back with `git -C <wt> add -A && git -C <wt> diff --cached --binary 279810baf50bbe7b1f7bf62fa282d3513882d000 > p.patch`, then `git apply --3way` in voyages): ../pokeorchid-pol-delta (tier-B Deltas + weak recolours + Holon wild restore), ../pokeorchid-pol-phone (Cynthia phone contact + Sevii Hoenn-voiced battle music), ../pokeorchid-pol-content (Sevii trainers slots 31+, tower encounters, lake rocks, flag-gated doors).
MERGED (all polish + Holon/Sinnoh region maps) into voyages; combined build clean. Call-fix headless check running.
OLD PENDING MERGES (apply after the Holon region-map agent finishes in voyages): scratchpad/pol_delta.patch (tier-B Deltas; scripts in scratchpad/pol_delta_scripts → rsync to dev_scripts/voyages/delta/). pol-delta worktree removed. scratchpad/pol_phone.patch (Cynthia phone + MUS_ORCHID_SEVII_* 565-569; docs in scratchpad/pol_phone_scripts → dev_scripts/voyages/polish_phone_music/). pol-phone worktree removed.
scratchpad/pol_content.patch (33 Sevii trainers slots 31–106, Research Tower 2F encounters via gTileset_HolonLab copy, 4 lake smash rocks, flag-gated doors 0x26B/0x26C; docs scratchpad/pol_content_scripts → dev_scripts/voyages/polish_content/, plus copy build_sevii.py + sevii_flags.json into dev_scripts/voyages/sevii/). pol-content worktree removed. NOTE: Faba can't use slot 32 (now TRAINER_SEVII_FINN) — pick the next free slot after 106.
FIX (in voyages, unbuilt yet): src/rotom_phone_call.c PrintTalkTimer saves/restores text colours (call-screen page-2 pale-green text bug). Verify headless with a 2-page call after merges.
HOLON REGION MAP: user art ref/holon_region_*.png; cells Coast (15,13), Village (11,11), Tower (9,3), Lake (3,15); agent installing in voyages.
FABA: approved by the user, build agent running in voyages (slot after 106; leaves after defeat). Then: Sinnoh routes redraw (Gen 3 thin gold route lines) — user said yes; start after Faba finishes (same checkout), then commit voyages + merge into engine-dev.
FABA (old note): mockup agent → out/batch8_faba (sprites, team, placement); implement after approval, then merge.
QUEUED POLISH (original list) (user, after the region-map/E2E agent finishes — same checkout): (1) tier-B Deltas (34; fill Holon wild fallbacks), (2) Cynthia Rotom Phone CALL contact after the lake, (3) basic post-game Sevii trainers, (4) Research Tower wild encounters, (5) Sevii music status → finish re-voicing, (6) Dotted Hole + Tanoby chamber seals → flag-gated doors (FLAG_SEVII_DOTTED_HOLE_OPEN / FLAG_SEVII_TANOBY_OPEN from Sevii's free 0x26B–0x27F; ON_LOAD setmetatile door + hide sign when set; default sealed) — user approved.
- region maps implemented (export_region_maps.py + C) and the end-to-end headless run passed: see e2e/DONE.md (2026-11-19). Left: Sevii battle music re-voicing (fallback = Emerald tracks), Dex AREA on-screen check.
Merge method: `git -C <wt> add -A && git -C <wt> diff --cached --binary > X.patch; git apply --3way --exclude='dev_scripts/voyages/*' X.patch; rsync <wt>/dev_scripts/voyages/<stream>/`.
Known: Pokédex seen/caught arrays grew → old saves misread dex flags (save migration needed if the user wants it).

## Next steps
1. When batch 3 reports: check its renders (Sevii 4–7 vs FRLG, tileset sheets, budget — 512 tiles / palettes), send to the user, collect open questions.
2. Publish ONE design review page (Artifact) covering all batches: renders, tileset + sharing lists, DECISIONS.md summary, remaining open questions. Wait for the user's explicit approval.
3. Then Phase 2 implementation per plan (2a voyage system → 2b maps → 2c legendaries → 2d Delta → 2e Cynthia/Researcher/café → 2f region maps), verify headless in mGBA, targeted tests only.
