#!/usr/bin/env python3
"""Headless in-game check of the v2 Centre / Mart exteriors (dev_scripts/mgba_headless).

    python ingame.py <harness rom base> <outdir> [all|bura]

all : every Centre/Mart: warp onto the interior exit, walk out, check we stand in front of the new
      door, walk back in; Marts also enter through the right-hand door.
bura: screenshots in Bura City - player in front of the Centre, behind the Centre roof, the Mart
      signpost on several frames, the Centre arrow tiles on several frames.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "mgba_headless"))
from boot import boot, warp, pos, walk  # noqa: E402


def settle(e):
    # the JAXSON save opens on a nickname prompt; clear it
    for k in ("B", "B", "B", "B"):
        e.press(k, after=60)


def wait_idle(e, limit=600):
    for _ in range(limit // 10):
        if e.r8("sLockFieldControls") == 0:
            return
        e.frames(10)


def check_all(e, out):
    plan = json.load(open(os.path.join(HERE, "plan.json")))
    rows = json.load(open(os.path.join(HERE, "interiors.json")))
    doors = {}
    for p in plan:
        nx, ny, w, h = p["new"]
        doors.setdefault(p["layout"], []).append((p["kind"], nx + (2 if p["kind"] == "centre" else 1), ny + h - 1))
    layout_of = {}
    for g, n, wi, folder, dest in rows:
        js = json.load(open(os.path.join(HERE, "..", "..", "data", "maps", folder, "map.json")))
        layout_of[folder] = js
    bad = []
    for g, n, wi, folder, dest in rows:
        kind = "centre" if "PokemonCenter" in folder else "mart"
        warp(e, g, n, wi)
        wait_idle(e)
        e.press("DOWN", hold=16, after=160)
        wait_idle(e)
        x, y, og, on = pos(e)
        e.shot(os.path.join(out, f"{folder}_out.png"), scale=1)
        e.press("UP", hold=16, after=160)
        wait_idle(e)
        back = pos(e)
        ok = (back[2], back[3]) == (g, n)
        right = None
        if kind == "mart" and ok:
            e.press("DOWN", hold=16, after=160)
            wait_idle(e)
            e.press("RIGHT", hold=16, after=40)
            e.press("UP", hold=16, after=160)
            wait_idle(e)
            r = pos(e)
            right = (r[2], r[3]) == (g, n)
        print(f"{folder:<40} out at ({x},{y}) map {og}.{on}  re-enter {'OK' if ok else 'FAIL'}"
              + ("" if right is None else f"  right door {'OK' if right else 'FAIL'}"), flush=True)
        if not ok or right is False:
            bad.append(folder)
    print("BAD", bad)


def bura(e, out):
    rows = json.load(open(os.path.join(HERE, "interiors.json")))
    g, n, wi = next((r[0], r[1], r[2]) for r in rows if r[3] == "BuraCity_PokemonCenter_1F")
    warp(e, g, n, wi)
    wait_idle(e)
    e.press("DOWN", hold=16, after=160)
    wait_idle(e)
    print("front of Centre", pos(e))
    e.shot(os.path.join(out, "bura_centre_front.png"), scale=2)
    # arrow tiles: read VRAM tile 167-168 on several frames
    seen = set()
    for k in range(6):
        seen.add(bytes(e.read(0x06000000 + 167 * 32, 64)))
        e.frames(16)
    print("arrow tile states seen:", len(seen))
    # behind the roof: round the left side, then step down onto the back row
    walk(e, "LEFT", 3)
    walk(e, "UP", 6)
    walk(e, "RIGHT", 3)
    e.press("DOWN", hold=16, after=40)
    e.frames(20)
    print("behind Centre", pos(e))
    e.shot(os.path.join(out, "bura_centre_behind.png"), scale=2)
    # door opening: walk back round to the front and bump the door
    e.press("UP", hold=16, after=20)
    walk(e, "LEFT", 3)
    walk(e, "DOWN", 6)
    walk(e, "RIGHT", 3)
    e.keys(1 << 6)                              # hold UP
    for k in range(4):
        e.frames(5)
        e.shot(os.path.join(out, f"bura_centre_door_{k}.png"), scale=2)
    e.keys(0)
    g, n, wi = next((r[0], r[1], r[2]) for r in rows if r[3] == "BuraCity_Mart")
    warp(e, g, n, wi)
    wait_idle(e)
    e.press("DOWN", hold=16, after=160)
    wait_idle(e)
    print("front of Mart", pos(e))
    for k in range(4):
        e.shot(os.path.join(out, f"bura_mart_{k}.png"), scale=2)
        e.frames(14)


def main():
    rom, out, mode = sys.argv[1], sys.argv[2], (sys.argv[3] if len(sys.argv) > 3 else "all")
    os.makedirs(out, exist_ok=True)
    e = boot(rom)
    settle(e)
    try:
        (check_all if mode == "all" else bura)(e, out)
    finally:
        e.close()


if __name__ == "__main__":
    main()
