# CB2 minigame teardown and heap safety

Succinct notes from debugging a full-screen `SetMainCallback2` minigame that uses BG0, `InitWindows`, and `CopyWindowToVram`, then returns via `CB2_ReturnToField` / `CB2_ReturnToFieldContinueScript*`.

## Symptoms you might see

- `malloc.c` assert: `block->magic == MALLOC_SYSTEM_ID` inside `Free` / `FreeInternal`
- Illegal opcode or jump to a nonsense address (`0x01FEFFFE`, `0xE3A0C000`, etc.) shortly after exit

Those often mean **heap metadata is already wrong**; the failing `Free` is where the runtime notices it, not necessarily where corruption started.

## Things that bite

### 1. DMA3 and window GFX

`CopyWindowToVram(..., COPYWIN_FULL)` queues **`LoadBgTiles` DMA from `gWindows[id].tileData`**. If you **`Free` that buffer while a transfer is still pending**, you can corrupt the heap. Waiting on `IsDma3ManagerBusyWithBgCopy()` is sometimes necessary—but **it can read idle while you still hit malloc asserts** if the real problem is bad headers or a bogus pointer, not a busy queue.

### 2. `FreeAllWindowBuffers` scans every slot

It frees **all** `gWindowBgTilemapBuffers[]` and **every** `gWindows[i].tileData` for `i < WINDOWS_MAX`. Any **stale or garbage non-NULL `tileData`** becomes `Free(garbage)` → assert or worse. Prefer **`RemoveWindow(id)`** when you only own one window—or be sure no other slot is polluted.

### 3. BG tilemap pointer vs. freed WRAM

If you free the BG tilemap buffer that **`SetBgTilemapBuffer`** still references, later tilemap/DMA helpers can touch freed memory. **`UnsetBgTilemapBuffer(bg)`** before (or in tight coordination with) freeing that allocation.

### 4. Wholesale heap reset on return to the overworld

`ReturnToFieldLocal` runs **`MoveSaveBlocks_ResetHeap` → `InitHeap(gHeap, HEAP_SIZE)`** early in the return sequence. That **reinitialises the entire malloc arena** without walking each block.

So for minigame allocations that **only** live until that return:

- You may **avoid per-block `Free`** if `Free` keeps tripping on bad magic (corruption or inconsistent state).
- You **must** clear **global pointers** into the old heap (`gWindowBgTilemapBuffers`, `gWindows[].tileData`, `sGpuBgConfigs2` tilemap via `UnsetBgTilemapBuffer`) so nothing dereferences them **before** `InitHeap` and before overworld `InitWindows` runs.

### 5. Tasks and `DestroyTask`

Avoid **`DestroyTask(taskId)`** from inside the same task that **`RunTasks`** is iterating unless you follow the same patterns as vanilla screens that do it deliberately. **`ResetTasks()`** in `ResumeMap` clears tasks after the handoff.

**Never call `ResetTasks()` from inside a task function** that `RunTasks` is currently executing (including from a helper that init code runs mid-task). It wipes `gTasks[]` while the CPU is still “inside” that task’s stack frame; the first run may appear fine, the next can stick on a black fade or corrupt state. Defer full init with **`SetMainCallback2`** to a small loader CB2 that calls **`ResetTasks()`** first, then your real init — see **`CB2_LoadTypeRpsGfx`** in **`src/type_rps_minigame.c`**.

### 6. `ResetBgsAndClearDma3BusyFlags`

After heavy BG/window use, clearing DMA busy bookkeeping matches patterns in **roulette** (`FreeRoulette`) and similar screens. Call when you tear down before returning to field.

## Recommended handoff pattern (when `Free` is unsafe)

Rough order used successfully in `src/type_rps_minigame.c`:

1. `SetVBlankCallback(NULL)` (and clear blend regs etc. as needed).
2. `DeactivateAllTextPrinters()`.
3. `UnsetBgTilemapBuffer` for BGs you owned.
4. NULL out `gWindowBgTilemapBuffers[]`; `memset` `gWindows` and set `window.bg = 0xFF` for all slots (or equivalent dummy state).
5. `ResetBgsAndClearDma3BusyFlags(0)` (or appropriate flag).
6. `SetMainCallback2` to your return CB2 (`CB2_ReturnToField`, `CB2_ReturnToFieldContinueScriptPlayMapMusic`, etc.).

## Vanilla references

- **Roulette exit:** `FreeRoulette` in `src/roulette.c` — `FreeAllWindowBuffers`, `UnsetBgTilemapBuffer`, `ResetBgsAndClearDma3BusyFlags`, then return CB2.
- **Diploma exit:** `src/diploma.c` — `FreeAllWindowBuffers` then `CB2_ReturnToFieldFadeFromBlack` (still uses `Free` because heap is consistent there).
- **Return pipeline:** `ReturnToFieldLocal` / `InitHeap` in `src/overworld.c`, `src/load_save.c`.

## If crashes persist

Then assume **heap corruption during the minigame** (buffer overflow in text, wrong window size, bad tile copy). The teardown above avoids **asserting on exit**; it does not fix the original writer bug—track that with mgba logs, hardware breakpoints, or narrowing which screen update last touched the heap.

## Case study: Type RPS minigame (`src/type_rps_minigame.c`)

Full-screen CB2 menu with BG0, a text window, compressed OBJ sheets, and **three Pokémon front sprites** via `CreateMonPicSprite_Affine` / `CreateMonPicSprite` (`src/trainer_pokemon_sprites.c`).

### Symptoms observed

- Severe **slowdown** after opening the menu several times, then **illegal opcode** in the emulator (e.g. warnings like `Illegal opcode: e7702e18`).
- Same class of failure as other heap issues: malloc metadata or control flow goes wrong once the heap is exhausted or corrupted.

### Root cause (mon pic subsystem vs `ResetSpriteData`)

- Those APIs **`Alloc`** decompressed frame buffers and register each pic in a small global table **`sSpritePics`** (capacity **`PICS_COUNT`**, 8 slots in vanilla).
- **`ResetSpriteData()`** resets **`gSprites`** and tile bookkeeping; it does **not** free those **`Alloc`**s and does **not** clear **`sSpritePics`**.
- If you only call **`ResetSpriteData()`** on **re-enter** the minigame, stale **`sSpritePics`** entries can still look “active”. **`CreateMonPicSprite*`** then fails to find a free slot (returns **`0xFFFF`**), and/or you leak the previous **`Alloc`** blocks every time sprites were reset without going through **`FreeAndDestroyMonPicSprite`**. Repeated use exhausts the pool and the heap → slowdown → crash.

### Fix pattern (init + exit)

1. **On init** (same screen setup as starter choose): after **`ResetSpriteData()`**, call **`ResetAllPicSprites()`** (`include/trainer_pokemon_sprites.h`). This clears the pic tracking slots so new mon pics can be created. Match the order used in **`src/starter_choose.c`** when bringing up that full-screen scene (`ResetSpriteData` then `ResetAllPicSprites`).
2. **On exit** (before `SetMainCallback2` to the field): for each mon pic sprite you created, call **`FreeAndDestroyMonPicSprite(spriteId)`** so the **`Alloc`**d buffers are **`Free`**d and **`sSpritePics`** stays consistent. Do not rely on **`ResetSpriteData()`** alone to release mon pic memory.
3. **`ResetAllPicSprites()`** by itself only zeroes the tracking structs; it does **not** call **`Free`** on orphaned frame buffers. Prefer the pair: **`FreeAndDestroyMonPicSprite`** on teardown, then **`ResetAllPicSprites`** on the next init if you also use **`ResetSpriteData()`** without having freed every pic.

### DMA before dropping window state

If the screen used **`CopyWindowToVram(..., COPYWIN_FULL)`**, wait for BG tile DMA to finish before NULLing window/BG state, e.g. **`while (IsDma3ManagerBusyWithBgCopy()) ;`** immediately before your abandon-window / handoff sequence (see §1). The Type RPS exit path does this before **`TypeRpsAbandonWindowStateForReturn()`**.

### Takeaway for future similar menus

Any CB2 UI that uses **`CreateMonPicSprite` / `CreateMonPicSprite_Affine`** must treat the **pic subsystem** as a separate lifecycle from **`ResetSpriteData()`**: clear slots on entry with **`ResetAllPicSprites()`**, release allocations on exit with **`FreeAndDestroyMonPicSprite`**, and keep the usual window/DMA teardown rules from §1–§6.

### `PlayCry_Normal` and `Task_DuckBGMForPokemonCry`

**`PlayCry_Normal`** ducks map BGM and creates **`Task_DuckBGMForPokemonCry`** (`src/sound.c`) to restore volume after the cry ends. **`StopCryAndClearCrySongs()`** stops the cry player but **does not remove that task**. If you **`SetMainCallback2`** to the field (or any screen that **`ResetTasks`**) while the duck task is still registered, behaviour is undefined and you can see **illegal opcode / jumped to invalid address**-class failures.

Before returning to field from a CB2 minigame that used **`PlayCry_Normal`**, either:

- Stop the cry **and** find **`Task_DuckBGMForPokemonCry`** with **`FindTaskIdByFunc`**, **`m4aMPlayVolumeControl(&gMPlayInfo_BGM, TRACKS_ALL, 256)`**, then **`DestroyTask`** (same idea as test clean-up in **`src/battle_main.c`** near **`Task_DuckBGMForPokemonCry`**), or  
- Use a cry API that does not start the duck task (e.g. **`PlayCry_NormalNoDucking`**) if BGM ducking is not desired.

Also keep the **recommended handoff order** in this doc: **`SetVBlankCallback(NULL)` first**, then text/DMA/window teardown, then **`SetMainCallback2`**—see **`src/type_rps_minigame.c`** **`PHASE_FADE_OUT`** after the cry/duck fix.
