---
applyTo: "**/*.pory"
description: Write valid Poryscript (not pokeemerald assembly) in .pory map scripts
---

# Poryscript rules for `.pory` files

`.pory` files are **Poryscript**, compiled by `tools/poryscript/poryscript` into
`scripts.inc`. Full language reference: `docs/tutorials/poryscript.md`.
Command names and arguments come from the macros in `asm/macros/event.inc` and
`asm/macros/movement.inc`.

## Two modes in one file

1. **Inside a `raw` block** (between `` raw ` `` and the closing `` ` ``) the text is
   copied verbatim into the `.inc` file. Write plain pokeemerald assembly there:
   `Label::`, tab-indented `msgbox Text_Label, MSGBOX_NPC`, `goto_if_set FLAG_X, Dest`,
   `.string "...$"`, `.byte 0`, `end`. None of the rules below apply.
2. **Everywhere else** write Poryscript. Never emit assembly syntax there:
   no `Label::` / `Label:`, no `.string`, no `.byte`, no `$` string terminators,
   no space-separated arguments.

## Top-level statements (outside `raw`)

```
mapscripts TelokTown_MapScripts {
    MAP_SCRIPT_ON_TRANSITION {
        setflag(FLAG_VISITED_TELOK_TOWN)
    }
    MAP_SCRIPT_ON_FRAME_TABLE [
        VAR_TELOK_TOWN_STATE, 0: TelokTown_EventScript_Intro
    ]
}

script TelokTown_EventScript_Npc {
    lock
    faceplayer
    msgbox(format("Text here. {PLAYER} works.\pNew box."), MSGBOX_NPC)
    release
}

text TelokTown_Text_Sign {
    format("Telok Town\n“Where new journeys take root.”")
}

movement TelokTown_Movement_AideWalk {
    walk_left * 3
    face_down
}

mart TelokTown_Mart_Items {
    ITEM_POKE_BALL
    ITEM_POTION
}
```

- An empty map script header is `mapscripts Name_MapScripts {}`.
- Script names follow `MapName_EventScript_Thing`; text `MapName_Text_Thing`;
  movement `MapName_Movement_Thing`.
- `script` blocks end automatically; `end` / `return` are only needed to exit early.
  Use `script(local) Name { }` for scripts not referenced from other files.

## Commands

- Commands that take arguments use **parentheses with comma-separated args**:
  `setflag(FLAG_X)`, `setvar(VAR_X, 1)`, `playse(SE_PIN)`, `delay(24)`,
  `waitmovement(0)`, `applymovement(LOCALID_AIDE, TelokTown_Movement_AideWalk)`,
  `giveitem(ITEM_POTION)`, `trainerbattle_single(TRAINER_X, "Intro.", "Lose.")`.
- Commands with no arguments are bare: `lock`, `faceplayer`, `release`, `waitmessage`,
  `closemessage`, `waitse`, `end`.
- Command names are lowercase exactly as in `event.inc`: `playse` (not `playSE`),
  `applymovement` (not `applymovemment`), `playbgm`, `fadescreen`, `warp`.
- Inline text: `msgbox("Short text.", MSGBOX_NPC)` or, for anything that needs wrapping,
  `msgbox(format("Long text..."), MSGBOX_NPC)`. Do not hand-insert `\n` line breaks
  into `format()` text except for deliberate breaks; use `\p` for a new text box.
- Inline movement: `applymovement(OBJ_EVENT_ID_PLAYER, moves(walk_up * 2, face_left))`.
- Text placeholders are braces: `{PLAYER}`, `{RIVAL}`, `{STR_VAR_1}`. There is no `{var}`.

## Control flow (never `checkvar`/`compare` + `goto_if_*` outside `raw`)

```
if (flag(FLAG_X)) { ... } elif (!flag(FLAG_Y)) { ... } else { ... }
if (var(VAR_X) == 1 && var(VAR_Y) >= 2) { ... }
if (defeated(TRAINER_X)) { ... }
while (var(VAR_TEMP_0) < 3) { addvar(VAR_TEMP_0, 1) }
do { ... } while (flag(FLAG_X))
switch (var(VAR_RESULT)) {
    case 0: msgbox("A")
    case 1:
    case 2: msgbox("B or C")
    default: break
}
```

- Conditions must be `flag(...)`, `var(...) <op> value`, or `defeated(...)`, combined with
  `&&`, `||`, `!` and parentheses. Never write `if 0x1 goto ...` or `if VAR_X == 1`.
- Autovar commands can be the condition directly, comparing `VAR_RESULT` for you:
  `if (checkitem(ITEM_POTION))`, `if (yesnobox(...) == YES)`,
  `if (getpartysize() < 6)`, `if (specialvar(VAR_RESULT, GetSomething) == TRUE)`.
  The list is in `tools/poryscript/command_config.json`.
- Jumps: `goto(Label)`, `call(Label)`, `call_if_unset(FLAG_X, Label)` are fine, but prefer
  `if` blocks. `break` / `continue` work in loops and switches.
- Comments are `//` or `#`.
