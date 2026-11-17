# Orchid UI — design notes

"Gen 5 layout, Gen 3 pixels." Black/White structure (round pocket wheel, pill rows,
flat patterned backdrops) drawn with Ruby/Sapphire/Emerald pixel rules (1px ink
outline, top-left light bevel, bottom-right shade, 3-step ramps, BGR555 colours).

Source of truth: `kit.py` (palette roles + primitives), `backdrop.py`, `windows.py`.
Screens: `bag_screen.py` (satchel bag BG). Mockups: `mock_bag.py`, `mock_review.py`.

## Status
- Design review in progress — **do not implement until the user approves the mockups.**

## Decisions so far
- Pocket-switch arrows in the bag header: small 6x9 Gen 3 chevrons (`kit.SMALL_ARROW`,
  original red.pal colours), not the 16x16 scroll indicators. (User request.)
- **No ▶ arrow cursor anywhere** — the gold pill alone marks the selection (bag list,
  context menus, YES/NO, start menu). (Review 1.)
- **Start menu rows get 16x16 icons** left of the label (`graphics/start_menu/menu_icons.png`,
  one shared OBJ palette). (Review 1.)
- **Shared windows use the Orchid (purple) theme for everyone**; gender themes only on
  player-owned screens like the bag. (Review 1, approved.)
- Satchel colours approved (tan leather, navy / rose flap). Flap must match body width;
  buckles sit on the body's sides facing outward with a small shoulder strap behind. (Review 1.)
- **Item art colour rule:** any item depiction (pocket icons, items peeking from the satchel,
  menu icons) uses Gen 3 item-icon saturation and perspective — derive ramps from
  `graphics/items/icon_palettes/*.pal`, don't invent colours. (Review 1.)

- **Unused list rows show the backdrop** (no ghost pills). (Review 2.)
- **Std window frame keeps the chunky 3px accent band.** (Review 2.)
- **BW-style scrollbar** (recessed track + gold thumb) replaces Gen 3's up/down list arrows. (Review 2.)
- **Description tray:** stitched seam stays; description text starts at tray y+2 with a
  **14px line pitch** so it clears the seam (FONT_NORMAL is 16px — implement via a
  text-printer line-pitch tweak or FONT_SHORT). (Review 2.)
- Context menus (USE / GIVE / TOSS) get **no icons**. (Review 2.)
- Poké Ball art: centre button must be small and round. (Review 2.)
- Orchid UI kit approved as the shared look. (Review 2.)

- **Backdrop = BW-style scrolling grid** on its own layer (BG3): near-black base with
  light 1px grid lines every 16px and faint minor lines at 8px (`backdrop.GRID_PAL`),
  scrolling diagonally down-right at 1px / 4 frames. Replaces the orchid-dot pattern
  kit-wide; screen art on BG2 leaves index 0 transparent so the grid shows through. (Review 3.)
- Poké Ball centre button sits on the band line (band bisects it). (Review 3.)

## Implementation notes (from review)
- **Pocket switching (L/R, D-pad ←/→):** the satchel sprite shakes (existing
  `ShakeBagSprite` affine wiggle) **and the gold selection circle moves along the ring
  from the old pocket button to the new one**; when it arrives, the new button shows its
  selected frame. Chained presses should retarget the circle smoothly. (User request.)
- Pill selection inside std windows (menus, YES/NO) needs a custom cursor routine that
  blits a pill into the window bitmap instead of printing the arrow glyph.
- List rows are BG2 art; highlight = per-cell palette swap (pal 0 normal, 1 selected).
  Unused rows are restored from a pill-free copy of the row tiles (backdrop only).
  Text windows stay transparent on pal 0.
- BG3 (free in the bag) holds the grid: 2x2 tiles + 32x32 map, own BG palette slot;
  scroll with BG3HOFS/VOFS from the bag's main callback. BG2 tile count must stay < 256
  if BG3's map goes at screenblock 28 (it overlaps charblock 3 from tile 256).
- Pocket-switch timing (see `anim_bag.py`): ring travels 12 frames ease-out; satchel shows
  the closed frame rising from y-5 for 6 frames with a decaying wiggle; list clears and
  pill rows wipe in over 16 frames, then text returns.
- New assets get new symbols — `menu.png`/`gBagScreen_Gfx` is shared with the Battle
  Pyramid bag and must stay.
