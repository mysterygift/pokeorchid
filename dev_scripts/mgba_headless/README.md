# mgba_headless — drive the ROM without a GUI

Headless mGBA (`tools/mgba/mgba-rom-test-mac -g`, no Lua in that build) + a GDB-RSP client.

- `harness_build.sh <worktree> <outdir>/<name> <save.sav>` builds a *harness ROM*: it patches
  `ReadKeys` to OR in a RAM global `gHarnessKeys` (input injection) and `ReadFlash` to read the save
  from a copy embedded in the ROM at 0x1F00000 (the runner can't load .sav files), builds, copies
  `<name>.gba/.elf` out, reverts the two source files, then embeds the save. Rebuild normally after.
- `gba.py` `Emu(rom, elf)`: `frames(n)` is frame-exact (breakpoint on `VBlankIntr`), `press('A')`,
  `r8/r16/r32/read/write` (symbols from `arm-none-eabi-nm`, statics included), `shot(png)` renders
  mode-0 BGs + OBJs from VRAM/OAM/palette and the `sGpuRegBuffer` shadow registers (no blending).
- `boot.py`: `boot(name)` title → CONTINUE → overworld; `warp(e, group, num, warp)` via the debug
  menu; `walk(e, 'UP', n)`; `pos(e)` = (x, y, mapGroup, mapNum).
- `exitall.py` / `enterall.py`: leave/re-enter every Centre and Mart (list in `bldgs.json`).
  `pctest.py`: use the Centre PC. `reach.py` (run from the repo root, plain python): flood-fill
  check that every interior NPC, PC and warp is reachable.

Needs Python with Pillow. Kill leftovers with `pkill -f mgba-rom-test-mac` (GDB port 2345).
Never point it at the user's real .sav in place; copy it.
