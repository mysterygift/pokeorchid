# Wavebreak Voyages — consolidated user decisions (review round 1, 2026-11-19)

Per-batch details live in out/batch*/NOTES.md "Decided" sections; this file is the cross-cutting summary.

## Voyage system
1. Transit: Emerald's ferry cutscene (`DoSeagallopFerryScene`, src/seagallop.c) with the ferry sprite swapped for Mr. Briney's small boat.
2. Passcodes are case-insensitive. Codes: SOULDEW (Eon), SEAGALLOP (Sevii), DELTA (Holon), NIGHTMARE (Newmoon), LUNARWING (Fullmoon).
3. Sevii: generic NPCs only in this pass (no trainers).

## Wavebreak
- Red-roof hut (only red roof; other 3 houses purple), Briney's wooden dock, extra fishermen, fish crates, rods, 3/4-view buckets with blue water (TosaPort addition, 12 metatiles / 15 tiles).

## Eon / moons
- Eon = Southern Island maps; Latias day / Latios night; mega stone after a catch; fainted legendary returns next voyage.
- Newmoon General+Dewford + WEATHER_SHADE (never Fallarbor); Fullmoon General+Rustboro.

## Sevii
4. One Centre on One Island (= Net Center).
5. Joyful Game Corner exterior = Pretty Petal flower shop building; interior = Mauville Game Corner layout with tweaked NPC scripts.
6. Mt. Ember terraces: the user repaints them later.
7. Sea rocks: 2x2 Emerald rocks, accepted.
8. Interiors (Ember Spa, Summit/Ruby Path, Dunsparce Tunnel, harbours, houses): translate the FRLG layouts the same way.
9. Map ids reuse FRLG names (MAP_ONE_ISLAND, MAP_ONE_ISLAND_KINDLE_ROAD, …).
10. Icefall entrance uses cave exit mat 0x386. Icefall ice = Shoal Cave look.
11. "Tanoby Ruins" kept (deliberate reference despite Tiksi's Tanoby Delta).
- Also: invented sea routes kept (walled by sea rocks), FRLG currents → plain sea, arrow warps recreated, gTileset_SeviiIslands (Rustboro copy) with cottage variants, Two Island market stall (rare items, high prices), Memorial Pillar Onix tails ported, Rocket Warehouse from recoloured Cold Storage tiles + R logo, interior placeholder from New Mauville tiles, Cape Brink waterfall, lone rocks → General boulders 0x0E0/0x0E1/0x0E2, smash rocks → breakable-rock objects.

## Region maps
12. Unbuilt FRLG scenery stays drawn as decoration.
13. Cursor special-case for the L-shaped straits.
14. Phone R region-switch disabled during a voyage.
15. Header "SEVII ISLANDS" + "ISLES 1-3" sub-label.
- Eon: dense intro clouds over Hoenn (approved), no place marker, player head over Southern Island. Sevii: FRLG battle music re-voiced to Hoenn voicegroups; Fly only within the current cluster; section names approved. Holon/Newmoon/Fullmoon placeholders.

## Holon
- All outdoor maps on gTileset_Holon (Fortree copy, Route 119/120 look; no shared palettes touched); Weather Institute = Research Tower (ext + 1F/2F); blue-grey rocks; existing Orchid rail tiles; diamond-carved stones; lake pillars + sphere (palette-swap glow); sealed carved domes, nicely dithered; no dead trees; no three small domes; ruins interior, heal location, region-map sections approved.
- Round 2 art approved (blue-grey rock copies, sealed carved domes, 1x3 lake pillars, carved standing stones, sphere object + OBJ palette-swap glow, Orchid rail kit).
- Greens: primary + secondary desaturated — Holon-only General copy (palettes 0-5 only) + desaturated Fortree-copy foliage; drained grass rings around the Research Tower and the lake pillar island. Grass-rustle/footprint field effects load desaturated palette copies on Holon maps (small code hook).

## Cynthia / Holon Researcher
16. Cynthia: Platinum team, NEWER (modern) movesets, held items, Garchomp can Mega Evolve (Garchompite; trainer mega). FINAL team approved as in trainers/cynthia_team.py (Lv 70-74, natures, IV 31, 4 Full Restores; Togekiss Life Orb, Lucario King's Rock).
17. Champion mugshot transition.
18. Widen TrainerClass.name to [17]; "Holon{NBSP}Researcher".
19. vs Cynthia: NUM_TRACKS_BGM 10→12, synth bass to wave channel, drop orchestra hits, xylophone for the bell line. No loop markers — the user adds them after import.
20. Holon Researcher: brown slacks, vanilla dark-brown OW hair, glasses as drawn.
21. Credit lichen under "Other Credits" in root CREDITS.md.
- Cynthia OW palette npc_white. After she's beaten at Holon Lake she moves to a café in Changu City (placeholder for a future Battle Lounge) where she can be rematched.
- Changu café: own tileset gTileset_ChanguCafe (copy of OrchidCentre); recolour variant A (deep-red walls, charcoal floor) approved; exterior patch as mocked (red-roof café + awning terrace, x30-38 y25-31). Name: "BATTLE CAFÉ" (sign). Red roof. Barista only greets you ("Welcome to the Battle Café!"), no shop.

## Delta species
- All recommendations accepted: tier A (57 species / 21 lines) first; δ = byte 0x18; recolours; δ STAB moves; either-parent δ eggs; excluded from diploma; Eevee-δ gift + shiny Gyarados-δ static.

## Round 2 (2026-11-19, during implementation)
- Save: no migration — the user starts a fresh save (Pokédex layout grew for Deltas).
- Sailor waits at the Wavebreak dock after the Champion; his Son stays in the hut (current behaviour, confirmed).
- Polish queued: tier-B Deltas, Cynthia Rotom Phone contact, basic post-game Sevii trainers, Research Tower wild encounters, Sevii music status/re-voicing; Dotted Hole / Tanoby chamber seals become flag-gated doors (approved).
- When everything (incl. region maps) is done: commit `voyages` and merge it into engine-dev (user's explicit go).
- NEW (user): Holon Leader Faba — boss battle at the top of the Holon Research Tower. Gen 3 OW sprite (from the user's template sheet ref/faba_ow_template_sheet.png) + trainer front pic, refs in ref/faba_*. Mockups first (out/batch8_faba), then implement before the engine-dev merge.
- Holon region map: user art (ref/holon_region_terrain.png + routes); cells Mirage Forest (15,13), Holon Village (11,11), Research Tower (9,3), Holon Lake (3,15).
- Newmoon/Fullmoon region map (user): convert the Gen 4 Sinnoh map into Gen 3 style — matching Gen 3 maps' colour banding, route look and colours — then mask everything except Newmoon + Fullmoon (top-left islands) with the Eon-style intro clouds. Shared by both islands. Needs the Sinnoh image saved to disk (not yet available).
- Faba (user): OW npc_3; front pose A with a plain high stand-up collar (no flaps across the face) and a WIDER visor covering more of the face like the reference (front + OW); Tower 2F uses the office battle background; Holon logo transition (plain greyscale) for Faba + all 6 Researchers; music Aqua/Magma Leader battle + Aqua encounter; team 3 USUM + 3 Deltas Lv 70–72; Eevee-δ gift only after Faba's defeat; drained rings heal (palette swap) after his defeat; trainer slot 32 (Shelly) if unreachable.
