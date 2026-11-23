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

## Rotom Phone (replaces the PokéNav) — approved 2026-11-17
Review page: https://claude.ai/artifact/VMCa72HNxA8greGsRFMW2a · mockups: `mock_phone.py`, `mock_quests.py`.

Home screen
- Start-menu entry **PHONE** takes POKéNAV's slot (new 16x16 Rotom Phone icon in `menu_icons.py`).
- Landscape Rotom phone over the BG3 grid; **always Rotom coral** (an object, not a gender-themed panel):
  bolt fin on top, tail spike below, Rotom-eye notch on the left bezel, diagonal screen glare.
- Status bar (location, signal, clock), 4 app tiles (32x32, colour field + white pictogram), gold pill
  around the selected tile + label, Rotom "Bzzt!" line in a bottom strip (normal font, 12px pitch).
- Apps: **MAP** (v1 = `FieldInitRegionMap`, no zoom), **CALL** (PokéNav Match Call via a new pokenav
  launch mode that returns to the phone), **QUESTS**, slot 4 = **RADIO** (see below).
- **Locked apps show a dimmed "?" tile** with a Rotom line; the grid stays 4 wide.
- Badge on QUESTS = number of quests in REWARD state; Rotom's eye glows/blinks while > 0.
- Rotom keeps its voice in the bottom strip.
- Contest Condition / Ribbons are dropped with the PokéNav main menu.

QUESTS app (PSF Unbound Quest Menu, branch `unbound-quest-menu`, reskinned)
- Bag-style pill rows; selected row = gold palette swap; ★ favourite (Select); steps progress "2/5".
- State tags are pictograms, never words: ? new (PSF INACTIVE) / ! active / gift reward / ✓ done / padlock locked.
- Filter tabs under the header, L/R cycle All / New / Active / Reward / Done; Start = hidden A–Z toggle.
- Header count = completed / **unlocked** quests (don't reveal the total).
- **Locked quests are hidden** in the list; ?????? only for unreached steps inside a started quest.
- Tray: sprite in the icon well (item / mon / object), pin location pill, 2 description lines, Ⓐ Steps
  only on quests with subquests. Steps view: quest name header, segmented progress bar, B = back.
- Scrollbar hidden when everything fits.
- **New/updated quests: Rotom buzzes on the field** (phone icon + jingle) instead of PSF's message box.
- Gift pictogram: keep; redraw at 9x8 if it doesn't read in mGBA.
- Strings say Quests, not Missions; PSF/Skeli background art is not used.

RADIO app (slot 4) — approved 2026-11-17 · mockups: `mock_radio.py`
- Teal theme. LCD tuner (frequency, 88–108 scale, station markers, Gen 3 red needle OBJ), station card
  (region plate + name + tagline), now-playing tray with EQ bars. ←/→ tune (eased needle, crossfade), A on/off, B back.
- Stations play random songs from a region in the Gen 3 soundfont: TOSA FM 88.4, HOENN FM 91.3, KANTO GOLD 98.1,
  SINNOH SOUND 101.6 (added 2026-11-19), RADIO UNOVA 105.2, ABSOLUTE GALAR 107.7. **Town/route themes only** (no battle themes).
- Unlocks: Tosa, Hoenn, Kanto from the start; Sinnoh, Unova and Galar unlock through quests (no quest flags yet, so
  Sinnoh and Unova are open from the start for now).
- Music priority: battles/fanfares/cutscenes > script music (playbgm / fadenewbgm / savebgm / savedMusic; radio yields
  until fadedefaultbgm or the next map change with nothing saved) > radio (overrides map, night, surf, bike) > map music.
- **No signal** on underground and underwater map types: Rotom says "No signal…", map music plays.
- Rotation: each song plays its loop **twice**, ~1s fade, next from a shuffle bag (no repeats until all played);
  timer only runs while the radio song is playing; after a battle the next song starts.
- Field toast top-left (map-popup slot, station colour + station name + song title) when a song starts; queued behind
  the map-name popup.
- State = `VAR_RADIO_STATION` (0 = off), no save-block change. Loop lengths generated from MIDI loop markers.
- No quick toggle outside the phone for now.
- Hoenn + Kanto songs are already in the ROM. Sinnoh (10) + Unova (11) are GM MIDI rips converted by
  `dev_scripts/radio/import_radio_midi.py` (list: `songs.py`, registration: `register_songs.py`). Galar needs MIDIs.

CALL app — approved 2026-11-17 · mockups: `mock_call.py`
- Blue header (app header = the app's tile colour; QUESTS orchid, RADIO teal, MAP green — recommendation, not yet
  confirmed explicitly).
- Contact list: pill rows with the contact's OW head (people sheets: head at y 10–26 of the 16x32 frame), name,
  location; pictogram tags: home (Mom), Poké Ball = rematch, ! = new. Tray: location pill, status, profile.
- A opens the contact card (replaces PokéNav Call/Check/Cancel): trainer front pic on a dais (OW sprite at 2x for
  NPCs without one), name, location, profile, red "Wants a rematch!" strip; CALL / BACK buttons, CALL pre-selected.
- Ringing: round portrait, pulsing rings, "Calling…", B hangs up. Talking: standard Orchid dialogue box, header timer.
- Match-call data, rematch logic and messages unchanged; field interruptions stay, with a Rotom ringing icon.

MAP (region map) — v2, approved 2026-11-17
- User's terrain art unchanged; routes as 6px Gen 3 tubes on BG1 (gold visited, grey unvisited, blue sea);
  towns = disc nodes, landmarks = diamonds (OBJs, grey until visited); cursor = train-map gold ring; player head.
- **No rail view / no SELECT toggle. No name pill on the map. No "Town/City" type label** — the tray shows only the
  place name + a rail pictogram if the place has a Tosa Rail station (no Pokémon Center / Mart marks). Fly map = same screen, FLY header, "Ⓐ Fly here".
- Unvisited places shown greyed (nodes + routes), not hidden. User's Tosa terrain art kept exactly as is.

### Rotom Phone home: news ticker (approved 2026-11-17)
- The status-bar location text is removed. A newspaper pictogram is followed by a right-to-left scrolling headline strip, clipped at x 49–148 before the signal pips. Gold dots separate the headlines. The clock and signal are unchanged.
- Headlines come from a table `{ text, minBadges, maxBadges, flag, flagState }`. The eligible pool is built and shuffled once per phone open. The fallback line is "No news today, bzzt!".
- On hardware the strip is a wide text window on its own BG, scrolled with HOFS at 1px per frame and clipped with WIN0.

### Rotom Phone: implementation (2026-11-18, branch rotom-phone-impl)
- **Offline state (user request 2026-11-18):** until `FLAG_SYS_PHONE_ACTIVE` (was unused system flag 0x863) is set,
  the phone opens to an X-eyed Rotom face with empty signal bars and the clock only (no ticker, apps or strip).
  Mock: `mock_phone.py` 06_offline.png. Set the flag from the story script that switches the phone on.
- Home: `src/rotom_phone.c` (export_phone.py). The gold pill is an OBJ under the app tiles rather than a BG2 palette
  swap (the glare band crosses the slots, which would need more than 16 colours); it looks the same.
- CALL: `src/rotom_phone_call.c` is a standalone kit screen over the unchanged match-call data/logic (not a PokéNav
  mode). Contact heads come from a trainer-pic → overworld-sprite table (no data links trainers to OW sprites).
  No "new message" tag yet (there is no save data for it). Field calls show a buzzing Rotom Phone icon.
- QUESTS: `src/quests.c` (PSF port: data, save bits, script commands 0xe8-0xea, macros) + `src/rotom_phone_quests.c`.
  `startquest` / `rewardquest` / `completequest` / `unlockquest` / `completesubquest` buzz Rotom on the field.
  Quest content is placeholder (mockup samples + numbered quests) until real quests are written on dev.
- RADIO: `src/radio.c` + `src/rotom_phone_radio.c`; song lengths from `dev_scripts/radio/song_lengths.py`.
  Galar is stubbed (no songs, locked).
- MAP v2: `export_map_v2.py` + `RegionMap_LoadOrchidMapV2` in region_map.c. Placeholder places have no visited
  flags yet, so they stay grey. The Fly map cursor still moves freely (A only works on places you can fly to).
- PokéNav Condition / Ribbons retired behind `ORCHID_RETIRE_POKENAV_CONDITION_RIBBONS` (include/config/general.h).

## Pokédex HABITATS (2026-11-22 / 23)

Review page: https://claude.ai/artifact/DSMUW9W3u7BdwJ6APXue4b. Mock: `mock_habitats.py`; ROM art + data:
`export_habitats.py` → `graphics/pokedex/orchid/habitats_*`, `hab_*.png`, `src/data/pokedex_habitats.h`;
code: `src/pokedex_habitats.c` (START on the dex list).

Approved decisions:
- Region map view; the cursor hops habitat to habitat (sections with wild tables); the hovered habitat glows,
  its zone (Northern / Eastern / Southern / Western Tosa) is lit, other land dimmed (sea untouched), gold rim.
  Zones are set per area in the region map tagger (Habitat dropdown, `tags.json` "habitat"); Tiksi is one zone.
- "Ⓐ Route View" call to action above the route name. L / R switch region; the Tiksi tab appears once
  FLAG_VISITED_FURONG_VILLAGE is set. SELECT flips day / night (morning + day + evening share the day list).
- Seen → Captured → Catalogued. Captured = the caught flag (any acquisition); catalogued = caught a second time
  (`SaveBlock3.dexCatalogued`, set in `Cmd_trysetcaughtmondexflags`). One capture: category, HT/WT, AREA tab,
  level ranges. Two captures: dex description and encounter rates. Progress is per species, not per route.
- Icons: not seen = black silhouette, seen = greyscale, captured = colour + GREY Poké Ball, catalogued =
  colour + COLOUR Poké Ball (user 2026-11-23; replaced the gold book). The same balls mark list rows, the entry
  name pill, counts and map badges. A habitat badge needs both its day and night lists.
- A on a seen species opens its dex entry (B then returns to the list, not the route page).
- Wild tables: placeholders for every Tosa / Tiksi map (`dev_scripts/orchid_encounters/encounters.py`), day + night.

Day / night (OW_ENABLE_DNS) lives in `dev_scripts/orchid_dns/`: house windows, gym door, Pokémon Center upper
windows + door, Mart door only, station glass, Tosa Port jetty lamp bulbs. All on the TosaPort tileset; Telok
(Petalburg) and the Tiksi towns are not lit yet.
