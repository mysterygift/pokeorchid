#!/usr/bin/env python3
"""Headless in-game check of the 5x5 Marts (dev_scripts/mgba_headless harness ROM).

    python ingame.py <harness rom base> <outdir> [all|door]

all : every Mart: warp onto the interior exit, walk out, check we stand in front of the new door,
      screenshot, walk back in.
door: Bura City: screenshots while the door opens, and with the player on the roof's back row.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(HERE, "..", "mgba_headless"))
from boot import boot, warp, pos, walk  # noqa: E402


def map_numbers():
    js = json.load(open(os.path.join(ROOT, "data", "maps", "map_groups.json")))
    out = {}
    for g, name in enumerate(js["group_order"]):
        for n, folder in enumerate(js[name]):
            out[folder] = (g, n)
    return out


def folders():
    out = {}
    for d in os.listdir(os.path.join(ROOT, "data", "maps")):
        p = os.path.join(ROOT, "data", "maps", d, "map.json")
        if os.path.exists(p):
            out[json.load(open(p))["id"]] = (d, json.load(open(p)))
    return out


def marts():
    """-> [(town map id, door (x, y), interior folder, interior exit warp index)]"""
    inst = json.load(open(os.path.join(HERE, "installed.json")))
    F = folders()
    rows = []
    for m in inst["marts"]:
        nx, ny = m["new"]
        door = (nx + 2, ny + 4)
        for mid, (folder, js) in F.items():
            if js["layout"] != m["layout"]:
                continue
            w = next(w for w in js["warp_events"] if (w["x"], w["y"]) == door)
            ifolder, ijs = F[w["dest_map"]]
            wi = next(i for i, iw in enumerate(ijs["warp_events"]) if iw["dest_map"] == mid)
            rows.append((mid, door, ifolder, wi))
    return rows


def settle(e):
    for _ in range(4):
        e.press("B", after=60)


def wait_idle(e, limit=600):
    for _ in range(limit // 10):
        if e.r8("sLockFieldControls") == 0:
            return
        e.frames(10)


def check_all(e, out):
    nums = map_numbers()
    bad = []
    for mid, door, ifolder, wi in marts():
        g, n = nums[ifolder]
        warp(e, g, n, wi)
        wait_idle(e)
        e.press("DOWN", hold=16, after=160)
        wait_idle(e)
        x, y, og, on = pos(e)
        e.shot(os.path.join(out, f"{mid}.png"), scale=1)
        out_ok = (x, y) == (door[0], door[1] + 1)
        e.press("UP", hold=16, after=160)
        wait_idle(e)
        back = pos(e)
        in_ok = (back[2], back[3]) == (g, n)
        print(f"{mid:<36} out at ({x},{y}) want ({door[0]},{door[1] + 1}) {'OK' if out_ok else 'FAIL'}"
              f"  re-enter {'OK' if in_ok else 'FAIL'}", flush=True)
        if not (out_ok and in_ok):
            bad.append(mid)
    print("BAD", bad)


def door(e, out):
    nums = map_numbers()
    mid, d, ifolder, wi = next(r for r in marts() if r[0] == "MAP_BURA_CITY")
    warp(e, *nums[ifolder], wi)
    wait_idle(e)
    e.press("DOWN", hold=16, after=160)
    wait_idle(e)
    print("front of Mart", pos(e))
    e.shot(os.path.join(out, "door_front.png"), scale=2)
    e.keys(1 << 6)                              # hold UP: bump the door, it slides open
    for k in range(6):
        e.frames(4)
        e.shot(os.path.join(out, f"door_open_{k}.png"), scale=2)
    e.keys(0)
    wait_idle(e)
    print("inside", pos(e))
    # behind the roof: out again, round the left side, onto the back row
    e.press("DOWN", hold=16, after=160)
    wait_idle(e)
    walk(e, "LEFT", 3)
    walk(e, "UP", 6)
    walk(e, "RIGHT", 3)
    e.press("DOWN", hold=16, after=40)
    e.frames(20)
    print("behind Mart", pos(e))
    e.shot(os.path.join(out, "behind.png"), scale=2)


def main():
    rom, out, mode = sys.argv[1], sys.argv[2], (sys.argv[3] if len(sys.argv) > 3 else "all")
    os.makedirs(out, exist_ok=True)
    e = boot(rom)
    settle(e)
    try:
        (check_all if mode == "all" else door)(e, out)
    finally:
        e.close()


if __name__ == "__main__":
    main()
