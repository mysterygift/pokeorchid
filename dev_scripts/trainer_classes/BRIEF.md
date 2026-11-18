# Orchid trainer classes — art brief (round 1 mockups)

Pokémon Orchid is a Pokémon Emerald (pokeemerald-expansion) ROM hack set in the Tosa region, based on
Singapore. Round 1 = mockups for design review. Round 2 wired every drawn sprite into the game:

- `install.py` copies `out/<id>_front.png` / `out/<id>_ow.png` into `graphics/` as 16-colour PNGs (new
  classes get new files; same-job edits overwrite the vanilla PNG after saving it as `<name>-og.png`).
  Re-run it after changing any class script, then `make`.
- `verify_ingame.py` (after `make`) reads `pokeemerald.gba` through the game's own tables and checks each
  front pic, class name, OW sheet and OW palette against `out/`; writes `out/ingame/contact_sheet.png`.
- New classes: TRAINER_CLASS_ TOURIST HAWKER RIDER EXECUTIVE INFLUENCER SINGER NYONYA DANCER ORCHIDIST
  RECRUIT PORT_WORKER. Pics/OWs: TOURIST_M/F, HAWKER_M/F, RIDER, EXECUTIVE, INFLUENCER, SINGER, NYONYA,
  DANCER, ORCHIDIST, RECRUIT, PORT_WORKER (TRAINER_PIC_* and OBJ_EVENT_GFX_*), plus OBJ_EVENT_GFX_SCHOOL_KID_F
  (own palette, OBJ_EVENT_PAL_TAG_NPC_SCHOOL_KID_F). Replaced in place: Expert M, Black Belt (OW now npc_4),
  School Kid M (front + OW), School Kid F (front).
- The FRLG shared palettes npc_blue/pink/green/white are now built in Emerald mode too (they were behind
  `#if IS_FRLG`), so Emerald-mode NPCs can use them.

Python with Pillow: `/private/tmp/claude-501/-Users-arandavies-Development-pokemon-orchid-pokeorchid/7eef0c81-b2a1-425c-b458-29de04c3c661/scratchpad/venv/bin/python`
(system Pythons have no Pillow). Run scripts from `dev_scripts/trainer_classes/` as single plain
commands (compound shell commands with `cd … &&` may be refused in this worktree).

## Tools
- `kit.py` — read its docstring. `load_front(name)` / `load_ow(name)` load vanilla art as palette
  indices; `dump()` prints a region as hex (one char per palette index) with rulers; `set_pal`,
  `remap`, `patch` (ASCII art; `.` keep, `_` transparent, `0-F` index, or a key dict), `blit`,
  `shift`, `fill`, `clear`; `save_front(id)` / `save_ow(id, npc_pal)` write indexed PNGs + previews
  to `out/` and return Gen 3 limit checks; `compare(id, base_front, base_ow)` writes a
  vanilla-vs-new sheet; `report()` prints checks.
- `detail.py out.png name …` zooms vanilla front pics with their palette strip; `owview.py` zooms OW sheets.
- `out/ref/*.png` contact sheets of vanilla front pics.
- Vanilla art: `graphics/trainers/front_pics/*.png` (64x64), `graphics/object_events/pics/people/*.png`
  (144x32 = 9 frames of 16x32; some sheets are wider — `load_ow` keeps the first 9).
  The `_frlg` files are FireRed/LeafGreen art: also fine as bases.

## Gen 3 trainer front pic rules (measured from vanilla)
- 64x64, one 16-colour palette, slot 0 transparent mint (115,197,164). Vanilla convention:
  1-4 skin ramp light→dark (4/5 often the warm brown skin outline), material ramps of 2-3 shades,
  E white, F black. Most use 15-16 slots. Colours round to multiples of 8.
- Full body, feet resting on y≈61-62, top of head y≈1-8. Adults are ~5-5.5 heads tall, kids ~4.
  Width 30-55 px. No pixels on the outer 64x64 edge.
- Outline: black on the outer silhouette, but **selective outlining**: edges against light areas
  and all interior lines use the darkest shade of the local material (dark green on a green dress,
  brown on skin). Black inside the figure only for deep creases, hair mass and shoes.
- Light from the upper left: highlights on the left/top, shadow on the right and under chin, brim,
  sleeves. 2-3 tone clumped shading, almost no dithering (only big cloth areas, sparingly).
- Faces: 3/4 view, eyes ~2x3 dark with optional 1px highlight, small brows, 1-3 px mouth. Keep the
  base sprite's face if the character type allows — faces are the hardest part to redraw.
- Keep the base's pose, proportions and anatomy. Redraw clothing, hair, headwear and props.
  Big readable props (camera, wok, lion head, phone) carry the class at battle size.
- Must read at 1x on a GBA screen. Check `*_front_x4.png` and the 1x PNG.

## Gen 3 overworld (NPC) rules
Read `/Users/arandavies/.claude/projects/-Users-arandavies-Development-pokemon-orchid-pokeorchid/memory/reference-gen3-ow-sprite-proportions.md`
(measured from vanilla Brendan/May; the user rejected freehand OW sprites before). Key points:
- **Start from a vanilla NPC sheet of similar build and keep silhouette, face layout, arms and feet
  pixel-for-pixel; repaint only hair, headwear, clothing, and add small props.** Don't draw from scratch.
- 9 frames: 0 down, 1 up, 2 left, 3-4 walk down, 5-6 walk up, 7-8 walk left (right = flip of left).
  Walk frames = stand bobbed down 1px with arm swing and one lifted foot. Every change must be
  applied consistently to all 9 frames (and to the bobbed ones 1px lower).
- **Palette: NPCs use one of the shared palettes, not their own.** `save_ow(id, pal)` checks the
  sheet palette equals one of: npc_1 npc_2 npc_3 npc_4 npc_white npc_blue npc_green npc_pink
  (`graphics/object_events/palettes/*.pal`). All share skin 1-3, outline 4, white E, black F and
  have three 3-shade ramps in 5-7, 8-A, B-D. Pick the palette whose ramps fit the outfit; if the
  base sheet is on a different palette, remap indices into the new one.
- Darker skin on OW (shared palettes only have one skin ramp): shift the skin one step darker
  (2 = highlight, 3 = base, 4 = shadow/outline) or use a brown ramp (npc_2 B-D, npc_white 5-7) —
  check it reads as skin, not mud.
- Pitfalls the user caught before: eyes too far apart, oversized heads, black interior lines, dotty
  1px highlights (read as dirt), diagonal straps on the back view (drop them from the back).

## Representation
Singapore is multicultural (Chinese, Malay, Indian, Eurasian, expats). Cultural classes must be
respectful, celebratory depictions — like Gen 2's Kimono Girl — never caricature. Skin tones in
the front pic palette should match the character (front pics have their own palette).

## Deliverables per class `<id>`
- `classes/<id>.py` — builds both sprites from vanilla bases, runnable on its own.
- `out/<id>_front.png` (64x64 indexed), `out/<id>_ow.png` (144x32 indexed, shared NPC palette),
  previews, and `out/<id>_compare.png`.
- `classes/<id>.md` — 5-10 lines: class name (≤12 chars, Gen 3 class names are short caps like
  HIKER, PKMN BREEDER), bases used, NPC palette, design choices, weak spots you know of, open
  questions for the user.
