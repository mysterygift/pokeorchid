# Implementation brief — shared rules for every build stream

Source of truth for design: `DECISIONS.md` + each batch's `out/batch*/NOTES.md` (Decided sections) + plan
`/Users/arandavies/.claude/plans/enchanted-leaping-pie.md`. Mockup scripts/specs live in
`/Users/arandavies/Development/pokemon-orchid/pokeorchid-voyages/dev_scripts/voyages/` (UNTRACKED in git — read them by
absolute path; copy what you need into your worktree's `dev_scripts/voyages/<stream>/`).

## Worktrees and hand-off (no commits)
Each stream works in its own detached worktree cut from `voyages` (bc3f480c7c):
- core: ../pokeorchid-voy-core · delta: ../pokeorchid-voy-delta · trainers: ../pokeorchid-voy-trainers · sevii: ../pokeorchid-voy-sevii · holon: ../pokeorchid-voy-holon
Do NOT commit, push, or touch other worktrees (the main `pokeorchid` dev checkout and `pokeorchid-engine-dev` are the
user's). Leave all changes uncommitted; the coordinator merges via `git add -A && git diff --cached --binary`.
Build in your own worktree only (`make -j8`; tools/poryscript/poryscript and ignored build outputs are already copied).
Never run a full `make check`; targeted `make check TESTS=...` only if you add a test.

## Pre-allocated resources (don't take anything outside your list; ask the coordinator if short)
| Stream | Flags | Vars | Trainer IDs | Map group | Charmap |
|---|---|---|---|---|---|
| core | FLAG_UNUSED_0x02B–0x02F (voyage unlocks), 0x03A–0x03F (legendary hide/caught/defeated), 0x068, 0x0E9 | VAR_UNUSED_0x408B | — | new `gMapGroup_Voyages` appended after `gMapGroup_Tiksi` | — |
| delta | — | — | — | — | 'δ' at 0x18 |
| trainers | FLAG_UNUSED_0x1AA, 0x1AB, 0x1DA | VAR_UNUSED_0x4091 | next free reused vanilla slots from 23 (skip rematch/Match Call trainers; aliases per memory feedback-trainer-slot-reuse.md) | — | PH_* shift for new songs |
| sevii | FLAG_UNUSED_0x264–0x27F (visited/fly flags, events) | VAR_UNUSED_0x409B | — | new `gMapGroup_Sevii` | — |
| holon | FLAG_UNUSED_0x280–0x29F | VAR_UNUSED_0x409D | — | new `gMapGroup_Holon` | — |
Group order when merged: Voyages, Sevii, Holon (after Tiksi). Item-ball flags: reuse FLAG_ITEM_* of unreachable maps (memory feedback-trainer-slot-reuse.md), renamed + aliased; core
owns Latiasite/Latiosite. Item balls follow the user's rule: reuse FLAG_ITEM_* / FLAG_HIDDEN_ITEM_* of deleted/unreachable maps (renamed + aliased). Slices: sevii = FLAG_ITEM_* 0x3E8–0x44F, FLAG_HIDDEN_ITEM_* of unreachable maps, overflow FLAG_UNUSED_0x493–0x4BF; holon + core = FLAG_ITEM_* 0x450–0x492, overflow FLAG_UNUSED_0x4C0–0x4EF.

## Conventions
- Memory notes (read the ones your brief names): /Users/arandavies/.claude/projects/-Users-arandavies-Development-pokemon-orchid-pokeorchid/memory/
- Map scripts are Poryscript (`scripts.pory` → generated `scripts.inc`, both committed). Use `.pory` for new maps.
- Gotchas: same-second mtimes can leave stale scripts.inc (delete it); editing only map.bin may not rebuild maps.o
  (`rm build/emerald/data/maps.o`); heal_locations.json gets rewritten by mapjson; FRLG-only OW gfx are invisible in
  Emerald; obedience needs `callnative Script_SetPartyMetLevel` for handed-out test mons.
- Headless test harness: dev_scripts/mgba_headless (README); work on a COPY of
  /Users/arandavies/Development/pokemon-orchid/pokeorchid-engine-dev/pokeemerald.sav; `pkill -f mgba-rom-test-mac`
  before each run; rebuild normally afterwards (`grep gHarnessKeys pokeemerald.map` must be empty).
- Pillow venv: /private/tmp/claude-501/-Users-arandavies-Development-pokemon-orchid-pokeorchid/72fd3b53-a4f0-4cad-8c0a-22b751dccb01/scratchpad/venv/bin/python
- Finish with: a clean `make` build, your headless checks, and `dev_scripts/voyages/<stream>/DONE.md` in your worktree
  (what changed, files, verification evidence, known gaps).
