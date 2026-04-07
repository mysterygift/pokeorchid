# How to rename a town (maps, layouts, and display name)

Renaming a town touches **folder paths**, **generated assembly labels**, and sometimes **save-related constants**. Do it in one pass so `mapjson` and the linker never disagree about paths or symbol names.

This guide assumes the pokeemerald-expansion style layout used in Pokeorchid (`data/maps/`, `data/layouts/`, `tools/mapjson`).

## Pick a scope before you start

| Goal | What you change | Typical use |
|------|----------------|------------|
| **Player-facing name only** | `src/data/region_map/region_map_sections.json` (`name`), sign/dialogue strings | Same map IDs and engine symbols; minimal risk |
| **Folder + script symbols (recommended for “new town” identity)** | Map folders, `map.json` `"name"`, `map_groups.json`, layout folder + `layouts.json`, includes, references | Clean labels like `TelokTown_MapScripts` while keeping vanilla `MAP_*` / `LAYOUT_*` **ids** if you want save compatibility |
| **Full constant rename** | Everything above **plus** `MAP_*`, `MAPSEC_*`, `LAYOUT_*`, heal locations, C/asm references | Bigger diff; grep the whole tree |

Most hacks keep **`map.json` `"id"`** (e.g. `MAP_OLDALE_TOWN`) and **`layout` + layouts.json `"id"`** (e.g. `LAYOUT_OLDALE_TOWN`) **unchanged** so existing saves and internal tables still line up, while **`map.json` `"name"`** and **disk folders** use the new CamelCase name (e.g. `TelokTown`). That matches how `mapjson` wires headers to `Foo_MapScripts` / `Foo_MapEvents`.

---

## Step-by-step checklist

Work with **Porymap and the editor closed** for the folders you move, or reopen the project after renames.

### 1. Rename map folders under `data/maps/`

- Rename the town root folder, e.g. `data/maps/OldaleTown` → `data/maps/TelokTown`.
- Rename every **interior** folder the same way, e.g. `OldaleTown_Mart` → `TelokTown_Mart`, so naming stays consistent.

The name of each folder must eventually match the corresponding `"name"` field in that folder’s `map.json` (see step 3).

### 2. Update `data/maps/map_groups.json`

- Every string you changed on disk (e.g. `TelokTown`, `TelokTown_Mart`) must appear **exactly** in `map_groups.json` where the old names were.
- If this file says `TelokTown` but the folder is still `OldaleTown`, `mapjson` will error with a path like `data/maps//TelokTown/map.json` missing.

### 3. Edit each affected `map.json`

In **`data/maps/<MapFolder>/map.json`**:

- Set **`"name"`** to **`<MapFolder>`** (same spelling as the directory). `mapjson` uses this for generated labels: `<name>_MapScripts`, `<name>_MapEvents`, `<name>_MapConnections`, and includes paths in generated comments.
- **`"id"`**: change only if you are doing a **full** `MAP_*` rename and will update warps, connections, C code, and constants everywhere.
- **`"layout"`**: still points at the **layout id** in `data/layouts/layouts.json` (often unchanged for save compatibility).

If a map uses **`shared_scripts_map`** or **`shared_events_map`**, update those string values to the **new** map `name` of the shared target.

### 4. Layouts for the town

1. Rename **`data/layouts/<OldLayoutDir>`** to match your project convention (e.g. `TelokTown`).
2. Open **`data/layouts/layouts.json`**, find the layout entry used by the town:
   - Set **`"name"`** to the assembly symbol for that layout (e.g. `TelokTown_Layout`). This is what map headers reference from the layout table.
   - Set **`border_filepath`** and **`blockdata_filepath`** to the new paths under `data/layouts/<NewDir>/`.
   - **`"id"`** (e.g. `LAYOUT_OLDALE_TOWN`): often **left as-is** so save data and scripts that use the layout id by number still match. Rename only if you intend to chase every `LAYOUT_*` reference.

### 5. Regenerate layout headers (required after `layouts.json` edits)

From the repo root:

```shell
make -B include/constants/layouts.h data/layouts/layouts.inc data/layouts/layouts_table.inc
```

Stale `layouts.inc` / `layouts_table.inc` causes **undefined references** to the new `*_Layout` symbol or wrong `LAYOUT_*` linkage.

### 6. `data/event_scripts.s`

- Update **`.include`** paths for any map whose folder moved, e.g. `data/maps/TelokTown/scripts.inc` instead of `data/maps/OldaleTown/scripts.inc`.

Do **not** truncate shared script includes when resolving merge conflicts; missing labels in `.inc` files often show up as linker errors.

### 7. Warps, connections, and other maps

Search and fix references to the old **folder/`name`** or old **`MAP_*`** ids, depending on your scope:

- **`map.json` `connections`**: `"map"` must be a valid `MAP_*` constant.
- **Warp `dest_map`** in other maps’ `map.json` files must match the destination’s **`id`**, not the display folder name.
- **Scripts** that use `warp`, `map`, or map-specific event names must use the new symbols if you renamed `map.json` `"name"`.

### 8. World metadata (optional but common)

- **Region map popup / Town Map name**: `src/data/region_map/region_map_sections.json` — update the **`name`** field for the relevant `MAPSEC_*` entry.
- **Heal locations**: `src/data/heal_locations.json` if a Pokémon Center or heal tile pointed at the old map id.
- **Wild encounters**: `src/data/wild_encounters.json` (or project equivalent) if encounters key off map or section constants you changed.
- **C code**: e.g. `src/region_map.c` or debug features sometimes list `MAP_*` — update if you changed those constants.

### 9. Text and flags

- Signs, NPC dialogue, and `msgbox` strings are **independent** of `map.json` `"name"`; update them in the same change if the story should say the new town name.
- **Flags / vars** keyed by content rather than map name usually stay; if anything used the old map **folder name** in a label, rename consistently.

### 10. Verify with build and Porymap

```shell
make
```

Fix any remaining **undefined references** to `<OldName>_MapScripts` or layout symbols — that usually means a missed `map_groups.json` entry, wrong `map.json` `"name"`, or layout files not regenerated.

Reopen the Porymap project so it picks up the new paths.

---

## Quick reference: what must stay in sync

| Artifact | Rule |
|----------|------|
| `data/maps/<X>/` folder | `<X>` == `map.json` `"name"` |
| `map_groups.json` | Lists the same `<X>` strings as map folders |
| `layouts.json` | `name` matches the layout symbol; paths point at real `border.bin` / `map.bin` |
| Generated layout files | Rebuild after `layouts.json` changes |
| `event_scripts.s` | `.include` paths match new folders |

---

## Related

- [How to delete vanilla maps](how_to_delete_vanilla_maps.md) — inverse operation; same touch points (`map_groups.json`, layouts, `event_scripts.s`).
