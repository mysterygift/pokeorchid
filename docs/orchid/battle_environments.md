# Battle environments

Battles use the classic flat Gen 3 background (BG3, 4bpp tiles + 64x32 map,
three palettes at BG palette 2-4). The Mode 7 "3D" floor and battle camera
that used to sit on top of this were removed; the Orchid environments below
remain as flat placeholders until proper background art is drawn.

## Orchid environments

Each lives in `graphics/battle_environment/orchid_<name>/` as `tiles.png`,
`map.bin`, `palette.pal` and `palette_night.pal`, and is wired up in
`src/data/graphics/battle_environment.h` and `src/data/battle_environment.h`.

| Environment | Folder |
|---|---|
| Grass | `orchid_grass` |
| Sand (beach) | `orchid_beach` |
| Plain (HDB void deck) | `orchid_void_deck` |
| Cave | `orchid_cave` |
| Ruins | `orchid_ruins` |
| Office | `orchid_office` |
| Mall | `orchid_mall` |
| Jungle | `orchid_jungle` |
| Pond (lake) | `orchid_lake` |

To redraw one, replace its `tiles.png`, `map.bin` and palettes in place (same
format as the vanilla environments in that folder's siblings).

## Choosing an environment for a map

Underground maps use the cave, and surfing on a pond uses the lake. For
anything else, set the map's **battle scene** (Porymap: Header tab > Battle
scene, or `"battle_scene"` in `map.json`):

| Battle scene | Environment |
|---|---|
| `MAP_BATTLE_SCENE_CAVE` | Cave |
| `MAP_BATTLE_SCENE_RUINS` | Ruins |
| `MAP_BATTLE_SCENE_OFFICE` | Office |
| `MAP_BATTLE_SCENE_BEACH` | Sand (beach) |
| `MAP_BATTLE_SCENE_JUNGLE` | Jungle |
| `MAP_BATTLE_SCENE_MALL` | Mall |
| `MAP_BATTLE_SCENE_LAKE` | Pond (lake) |

A location scene applies to every battle on the map (wild, trainer, surfing),
for the graphics and for Secret Power / Nature Power / Camouflage. Gym leader,
champion, Frontier and legendary battles keep their own backgrounds.

## Night

Each Orchid environment has a second palette, `palette_night.pal`, over the
same tiles. `IsBattleNight()` (`src/battle_bg.c`) picks it when
`GetTimeOfDay()` is `TIME_NIGHT` (evening still uses the day palette).
`GetBattleEnvironmentPalette()` is where the palette is chosen.

## Testing

Debug menu (R + Start) → Party → **Debug Battle: Day…** / **Debug Battle:
Night…** runs the showcase battle on any environment with the time forced.
Start Debug Battle runs the showcase party (Blaziken, Gardevoir, Swampert vs a
Lv 38 smart-AI team); debug battles skip the obedience check.
