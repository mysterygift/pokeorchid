## Decided (user, 2026-11-19)
- Recolour variant A (deep-red walls, charcoal floor).
- Name: Battle Café. Red-roof exterior. Barista just welcomes you (no shop).

# Batch 7: Changu City café (Cynthia rematch spot): design-review mockup

After Cynthia is beaten at Holon Lake (post-game), she moves to a café in Changu City and can be rematched there. The café is a simple placeholder for the future Battle Lounge.

This is a mockup only. Nothing under data/, src/, include/ or graphics/ was changed. Every cell is copied from an existing layout with the same tileset pair, so no tileset is edited.

- **To regenerate:** `<venv python> dev_scripts/voyages/cafe/mock_cafe.py`
- **Sprites:** `cafe/sprites.py` draws the real overworld sprites with their in-game palettes.
- **Marks:** yellow = NPC, blue = warp, green = sign, pink = Cynthia.
- **Cynthia's sprite:** she is drawn as a dark silhouette because her overworld sprite does not exist yet.
- **Base branch:** ChanguCity and gTileset_OrchidCentre exist on **engine-dev** (this worktree), not on `dev`. Build the café there.

## 1. Exterior: `changu_before*.png`, `changu_after*.png` (+ `_gba@2x` 15x10-tile camera crops)
- **Size and pair:** LAYOUT_CHANGU_CITY, 44x38 (unchanged), General + TosaPort. **60 layouts share TosaPort**: every Tosa town and route, Tiksi Routes 401-410, the Mt. Drake faces, Inka Seawall, Frigo Cave exterior, Changu Airport and others. Only existing cells are reused.
- **Hand-edited map:** the user edits this map in Porymap (`d76b8ea26f`, `6bafea671f`). The patch only touches free grass at x30-38, y25-31, east of House 2. No existing cell outside that box changes.
- **Changes:**

  | Cells | What | Source |
  |---|---|---|
  | x31-34, y26-29 | **Café building**, 4x4. The red-roof house, door at **(32,29)** | Changu House 3 (18,18), primary metatiles 0x008-0x022 |
  | x35-38, y25-29 | **Terrace**: orange market-stall awning on posts, two pots, two flower boxes, cobble floor | Bura City market stall (4,7), 0x215-0x217 / 0x21D-0x21F / 0x23D-0x2DF / 0x20C / 0x213 |
  | x35-38, y30-31 | Road extended 3 tiles east under the terrace. The east end (20A/21A) moves from x35 to x38 | Changu's own road cells |
  | (30,29) | Café sign post (0x003) | Bura City (9,11) |

- **Alternative:** `changu_after_purple*.png` uses the purple TosaPort house (a copy of House 2) instead. See open question 2.
- **New warp:** index **10** at (32,29), elevation 0, leads to MAP_CHANGU_CITY_CAFE warp 0. The door is the animated house door (bump to enter), like H1-H4.
- **New bg_event:** a sign at (30,29), player facing north.
- **Optional object:** a terrace patron, OBJ_EVENT_GFX_EXECUTIVE at (36,28), facing down, standing still.
- **Reachability:**
  - Every existing warp is untouched: Station 22-23,6; PC 14,21; Mart 30-31,13; Gym 15,13; H1 5,21; H2 26,29; H3 19,21; H4 25,11.
  - All 7 signs, 5 NPCs and the Mart sign object are untouched. Nothing existing stood in x30-38, y25-31.
  - The café door opens onto the road at (32,30). The terrace opens onto the road at (36-37,29).
  - The grass at x30 and x39, and the y25 strip below the flower beds (x31-33, y21-24), stay walkable.
- **Seams** (`vc.seams` reports pairs that never occur side by side in vanilla): the house's east wall touches the awning posts at x34|x35, and the flower box at (38,29) sits on the road end at (38,30). Both look clean in the crops. A 1-tile gap between the house and the terrace would push the terrace into the tree line at x40.

## 2. Interior: `cafe_int.png`, `cafe_int@2x.png`, `cafe_int@4x.png`
- **Layout:** new LAYOUT_CHANGU_CITY_CAFE, **12x10**. The engine check is (12+15)*(10+14) = 648, well within the limit.
- **Pair:** Building + **gTileset_ChanguCafe**, a new secondary used only by this layout. It is a café-only copy of **gTileset_OrchidCentre**, the Orchid Pokémon Centre's café kit; see "Café tileset" below. Today **2 layouts** use OrchidCentre: LAYOUT_POKEMON_CENTER_1F (all 16 Centres) and LAYOUT_LAVARIDGE_TOWN_POKEMON_CENTER_1F. Neither changes. The plain-colour render `cafe_int*.png` shows the room on the untouched OrchidCentre, for reference.
- **Border:** reuse `data/layouts/PokemonCenter_1F/border.bin`.
- **Built from:** only existing Centre metatiles (36 ids).
  - **Café corner:** columns x8-11 are the Centre's café corner (Centre columns x10-13):
    - Menu board 207, cup shelf 208/209, counter return 21E and coffee urn 21F.
    - Counter 229/22A/22B, which is MB_COUNTER, with stools 22E.
    - The tablet PC (21D / 213) and the shadow it casts (222/22D) are left out.
  - **Wall:** two windows (202/203) on either side of the Centre's flower painting (205/206).
  - **Plants:** the fern (20A/216/220) at the top left, and corner ferns 247/24A at both bottom corners.
  - **Tables:** four, each built from stool 243, table 244 and stool 243, with a shadow row of 234.
  - **Exit mat:** 248/249.
- **Warps:** (5,9) and (6,9), elevation 3, both lead to MAP_CHANGU_CITY warp 10.
- **Objects:**

  | Object | Graphic | Position | Facing | Notes |
  |---|---|---|---|---|
  | Barista | OBJ_EVENT_GFX_CLERK | (10,2) | down | Behind the counter. Talk across it from (10,4) |
  | Businessman | OBJ_EVENT_GFX_EXECUTIVE | (1,5) | right | A meeting at table 1 |
  | Businesswoman | OBJ_EVENT_GFX_WOMAN_5 | (3,5) | left | Same meeting |
  | Tourist | OBJ_EVENT_GFX_GENTLEMAN | (1,8) | right | Alone at table 3 |
  | **Cynthia** | **OBJ_EVENT_GFX_CYNTHIA (to be added)** | **(10,7)** | left | On the far stool of table 4, facing the empty seat (8,7). Hidden until she is beaten at Holon Lake. Talk to her from (10,6), (11,7) or (10,8) |

  Table 2 (x5-7, y5) is left empty, so the room does not feel full.
- **Seams:** the window, painting and trim stand side by side in a new order, and the fern touches the stool at x0|x1. Each was checked at 4x and looks clean.

## Café tileset: gTileset_ChanguCafe (user decision: own copy; floors and walls only)
Generator: `cafe/changu_cafe_tileset.py`. Comparison: `cafe_int_recolour_compare@2x.png` (original | A | B). Single renders: `cafe_int_A*.png` and `cafe_int_B*.png`. Proposed palette files: `gTileset_ChanguCafe_{A,B}_palettes/06.pal, 11.pal`.

**The copy:**
- **Source:** gTileset_OrchidCentre, the secondary paired with gTileset_Building.
- **Tiles:** the same as the source, with no tile changes. The tileset header can point `.tiles` at `gTilesetTiles_OrchidCentre` instead of duplicating its 174 tiles. If a separate `tiles.png` is preferred, copy it unchanged.
- **Metatile ids:** every id keeps its meaning.

**Palette slots changed (in the copy only):**

| Slot | Change | Used by |
|---|---|---|
| **6** | indices 2-7 recoloured | floor, floor shadows, and the floor around the mat |
| **11** | new; free in OrchidCentre (all black, unused) | the walls: a copy of pal 7 with the wall colours changed |

- **Slot 6** is used only by floor-type tiles in this kit. The mat's reds (11-13) and the outline (1) are left as they are.
- **Slot 7 is NOT edited.** The counter, stools, tables, windows, menu board and shelf also use it, so they keep their exact colours.

**metatiles.bin (in the copy):** every entry that draws a wall tile with pal 7 now uses pal 11.
- The wall tiles are secondary tiles 2-3 (wall face and ceiling band) and 32-35 (dado trim).
- The entries changed are in metatiles 0x201-0x215 and 0x24B-0x24C. Window, painting, menu and shelf entries in those metatiles stay on pal 7.
- Furniture is untouched, as the user asked.

**No other map changes colour:**
- gTileset_OrchidCentre (its palettes, metatiles and tiles), gTileset_Building and every Centre map stay as they are.
- Only LAYOUT_CHANGU_CITY_CAFE points at gTileset_ChanguCafe.
- The exterior keeps its existing colours.

**Variants:**

| | Floor | Walls | Trim |
|---|---|---|---|
| **A (recommended)** | charcoal (72,72,80), lighter diamond (88-104) | deep red (136,32,40), shade (112,24,32), dark band (64,32,32) | warm cream band, charcoal dado rail |
| **B** | charcoal, with deep-red diamond centres (104,32,40) | charcoal (88,88,96) | deep-red band, cream dots |

**Recommendation: A.** Red walls over a dark floor read as a lounge, and keep the sprites readable on the floor. B is darker overall, and its red floor dots get busy around the tables.

## Flavour lines (drafts)
- **Sign:** "LAYOVER CAFÉ / Kopi, kaya toast and a seat between flights."
- **Barista:** "Welcome to the Layover! Our kopi's strong enough to get you through any delayed flight."
- **Businessman:** "We flew in from Lumiose this morning. If this deal doesn't close by tonight, I'm on the red-eye home."
- **Businesswoman:** "Synergise, innovate, leverage... I just wanted a kaya toast in peace."
- **Tourist:** "That blonde lady in the corner has been here every day since she came back from Holon Lake. Is she someone famous?"
- **Cynthia, before the rematch:** "Ah, it's you. The coffee here is wonderful, but I was hoping you'd come by. Shall we have another battle?"
- **Cynthia, after:** "Splendid. I think I'll stay in Changu a little longer."
- **Terrace patron:** "Best seat in Changu. You can watch the planes come in over the rooftops."

## Open questions, with recommendations
1. **Café name.** I recommend **"Layover Café"**: it fits an airport city, and a "lounge" fits the Battle Lounge later. Other options: Departure Lounge Café, Changu Coffee House, Kopi & Co.
2. **Building colour.** I recommend **red** (`changu_after`). Changu already has three purple houses, and House 2 sits right next door. Red with the orange awning reads as a shopfront, not a home. Purple (`changu_after_purple`) blends in more. Red is also House 3's colour, but House 3 is across town.
3. **Barista.** I recommend OBJ_EVENT_GFX_CLERK, which wears an apron, running the existing `Common_EventScript_OrchidCafe` shop (Kopi, Steamed Bao, Kaya Toast). That gives Cynthia's challengers somewhere to stock up before the rematch.
4. **Cynthia's overworld sprite.** OBJ_EVENT_GFX_CYNTHIA needs a new 16x32 OW asset; none exists in the expansion. She is shown "seated" on a stool cell, facing the table, as the patrons are. Gen 3 has no sitting frames, so she would stand on the stool and turn to the player when talked to. **Rematch rule:** I recommend once per day, with a daily flag cleared like the other daily events. Her visibility flag should be set when she is beaten at Holon Lake.
5. **Map ids.** I recommend MAP_CHANGU_CITY_CAFE / LAYOUT_CHANGU_CITY_CAFE now. Rename them when the Battle Lounge replaces the room. The exterior warp index (10) and the door stay the same either way.
6. **Terrace patron.** Keep him or drop him? I recommend keeping him: he signals "café" from the street. He is flavour only.
7. **Music.** I recommend keeping Changu's MUS_SLATEPORT inside, or the Pokémon Centre theme, rather than a new track for a placeholder room.
8. **Recolour variant.** I recommend A (deep-red walls, charcoal floor). Pick A or B. Each palette can be tuned in `changu_cafe_tileset.py` VARIANTS.
9. **Bigger room?** 12x10 holds 4 tables. If the Battle Lounge needs room for spectators, it can grow to the Centre's 14x10 by repeating the floor columns.
