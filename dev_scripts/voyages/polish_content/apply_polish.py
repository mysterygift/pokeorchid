#!/usr/bin/env python3
"""
Content polish for the Wavebreak Voyages maps (Sevii trainers, Sevii flag-gated doors, Holon Research Tower
encounters, Holon Lake smash rocks). Idempotent; run from anywhere AFTER build_sevii.py / install_holon.py
(they regenerate the maps and would drop these edits):

  python3 dev_scripts/voyages/polish_content/apply_polish.py check      # sight-line / corridor check only
  python3 dev_scripts/voyages/polish_content/apply_polish.py apply      # write everything (then `make`)

The tileset art for the opened Dotted Hole door and the Holon lab encounter floor are installed by
`apply` too (tiles.png / metatiles / attributes: see install_* below).
"""
import json
import os
import re
import struct
import sys
from collections import deque, OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "dev_scripts", "voyages", "sevii"))
sys.path.insert(0, HERE)
import mtattr as MA          # noqa: E402
import check_sevii as C      # noqa: E402
from trainers_spec import T, SLOTS  # noqa: E402

P = lambda *p: os.path.join(ROOT, *p)
DIRS = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}


def jload(p):
    return json.load(open(p), object_pairs_hook=OrderedDict)


def jdump(p, d):
    s = json.dumps(d, indent=2, ensure_ascii=False) + "\n"
    open(p, "w").write(s)


def facing(movement):
    mv = movement.replace("MOVEMENT_TYPE_", "")
    if "SEQUENCE" in mv or mv in ("LOOK_AROUND", "WANDER_AROUND") or mv.startswith("ROTATE"):
        return list(DIRS)
    return [d for d in DIRS if d in mv.split("_")] or list(DIRS)


# ------------------------------------------------------------------ sight-line check
def components(m, L, objs, starts):
    """label cells reachable from each start; returns {start: component id}"""
    comp, cid = {}, 0
    for s in starts:
        if s in comp or not L.inside(*s):
            continue
        q = deque([s])
        comp[s] = cid
        while q:
            x, y = q.popleft()
            for dx, dy in DIRS.values():
                n = (x + dx, y + dy)
                if n in comp or not L.inside(*n) or L.coll(*n) or n in objs:
                    continue
                e1, e2 = L.elev(x, y), L.elev(*n)
                w1, w2 = C.is_water(L.beh(x, y)), C.is_water(L.beh(*n))
                if not (e1 == e2 or e1 in (0, 15) or e2 in (0, 15) or w1 != w2):
                    continue
                comp[n] = cid
                q.append(n)
        cid += 1
    return comp


def check_sight(verbose=True):
    """For every trainer: walk each facing direction's sight line. The trainer may end up standing on any cell
    of it (next to the player). That cell must not be a warp, and blocking it must not cut any entry / NPC /
    item off from the rest of the map."""
    bad = 0
    for tr in T:
        m = jload(P("data", "maps", tr["folder"], "map.json"))
        L = MA.Layout(m["layout"])
        lab = "%s_EventScript_%s" % (tr["folder"], tr["label"])
        idx = [i for i, o in enumerate(m["object_events"]) if o["script"] == lab]
        assert len(idx) == 1, (lab, idx)
        o = m["object_events"][idx[0]]
        mv = tr["over"].get("movement", o["movement_type"])
        warps = {(w["x"], w["y"]) for w in m["warp_events"]}
        others = {(p["x"], p["y"]) for j, p in enumerate(m["object_events"]) if j != idx[0]}
        targets = [(p["x"], p["y"]) for j, p in enumerate(m["object_events"]) if j != idx[0]]
        starts = sorted(warps)
        for c in m.get("connections") or []:
            d = c["direction"]
            edge = [(x, 0) for x in range(L.w)] if d == "up" else [(x, L.h - 1) for x in range(L.w)] if d == "down" \
                else [(0, y) for y in range(L.h)] if d == "left" else [(L.w - 1, y) for y in range(L.h)]
            starts += [p for p in edge if not L.coll(*p)][:1]
        base = components(m, L, others, starts)
        base_parts = len({base.get(s) for s in starts if s in base})
        problems = []
        line_len = {}
        for d in facing(mv):
            dx, dy = DIRS[d]
            cells = []
            x, y = o["x"], o["y"]
            for k in range(tr["sight"]):
                x, y = x + dx, y + dy
                if not L.inside(x, y) or L.coll(x, y) or (x, y) in others:
                    break
                ce = L.elev(x, y)          # the game's sight test fails on an elevation mismatch too
                if ce not in (0, 15) and ce != o["elevation"]:
                    break
                cells.append((x, y))
            line_len[d] = len(cells)
            for k, (sx, sy) in enumerate(cells[:-1] if len(cells) > 1 else []):
                if (sx, sy) in warps:
                    problems.append("%s: stop cell %s is a warp" % (d, (sx, sy)))
                comp = components(m, L, others | {(sx, sy)}, starts)
                parts = len({comp.get(s) for s in starts if s in comp})
                lost = [tg for tg in targets if C.reachable_from({c for c in base}, L, *tg)
                        and not C.reachable_from({c for c in comp}, L, *tg)]
                if parts > base_parts or lost:
                    problems.append("%s: standing on %s splits the map (parts %d->%d, cut off %s)" % (
                        d, (sx, sy), base_parts, parts, lost[:3]))
        bad += bool(problems)
        if verbose or problems:
            print("%-36s %-9s (%d,%d) %-22s sight=%d lines=%s %s" % (
                tr["folder"], tr["label"], o["x"], o["y"], mv[14:], tr["sight"],
                ",".join("%s%d" % (d[0], n) for d, n in line_len.items()), "OK" if not problems else ""))
            for p in problems:
                print("      !! " + p)
    print("%d trainers, %d with sight-line problems" % (len(T), bad))
    return bad


# ------------------------------------------------------------------ trainers
ALIAS_HEAD = "// Wavebreak Voyages polish: vanilla slots reused for the post-game Sevii trainers"


def install_trainers():
    assert len(SLOTS) >= len(T), "need %d slots" % len(T)
    oh = P("include", "constants", "opponents.h")
    txt = open(oh).read()
    aliases = []
    for (num, old), tr in zip(SLOTS, T):
        new = tr["const"]
        if re.search(r"#define %s\s+%d\b" % (new, num), txt):
            aliases.append((old, new))
            continue
        assert re.search(r"#define %s\s+%d\s*\n" % (old, num), txt), (old, num)
        txt = re.sub(r"#define %s(\s+)%d\s*\n" % (old, num),
                     lambda mm: "#define %-36s %d\n" % (new, num), txt, count=1)
        aliases.append((old, new))
    block = ALIAS_HEAD + " (dev_scripts/voyages/polish_content).\n" + \
        "".join("#define %-38s %s\n" % (old, new) for old, new in aliases)
    txt = re.sub(r"\n" + re.escape(ALIAS_HEAD) + r".*?\n\n", "\n", txt, flags=re.S)
    anchor = "// NOTE: Because each Trainer uses a flag"
    i = txt.index(anchor)
    txt = txt[:i] + block + "\n" + txt[i:]
    open(oh, "w").write(txt)

    tp = P("src", "data", "trainers.party")
    party = open(tp).read()
    for (num, old), tr in zip(SLOTS, T):
        body = ("=== %s ===\nName: %s\nClass: %s\nPic: %s\nGender: %s\nMusic: %s\nDouble Battle: No\n"
                "AI: Basic Trainer\n\n" % (tr["const"], tr["name"], tr["cls"], tr["pic"], tr["gender"], tr["music"]))
        body += "\n".join("%s\nLevel: %d\n" % (s, lv) for s, lv in tr["party"]) + "\n"
        pat = re.compile(r"=== (%s|%s) ===\n.*?(?=\n=== |\Z)" % (re.escape(old), re.escape(tr["const"])), re.S)
        assert pat.search(party), old
        party = pat.sub(lambda mm: body.rstrip("\n") + "\n", party, count=1)
    open(tp, "w").write(party)


def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def install_trainer_maps():
    by_map = OrderedDict()
    for tr in T:
        by_map.setdefault(tr["folder"], []).append(tr)
    for folder, trs in by_map.items():
        mp = P("data", "maps", folder, "map.json")
        m = jload(mp)
        sp = P("data", "maps", folder, "scripts.pory")
        s = open(sp).read()
        for tr in trs:
            lab = "%s_EventScript_%s" % (folder, tr["label"])
            o = next(o for o in m["object_events"] if o["script"] == lab)
            o["trainer_type"] = "TRAINER_TYPE_NORMAL"
            o["trainer_sight_or_berry_tree_id"] = str(tr["sight"])
            if "gfx" in tr["over"]:
                o["graphics_id"] = tr["over"]["gfx"]
            if "movement" in tr["over"]:
                o["movement_type"] = tr["over"]["movement"]
            pre = "%s_Text_%s" % (folder, tr["label"])
            mm = re.search(r"script %s \{\n(.*?)\n\}\n" % re.escape(lab), s, re.S)
            assert mm, lab
            if "trainerbattle" in mm.group(1):
                continue
            fm = re.search(r'msgbox\(format\("(.*)"\), MSGBOX_NPC\)', mm.group(1), re.S)
            post = fm.group(1) if fm else "..."
            new = ("script %s {\n    trainerbattle_single(%s, %sIntro, %sDefeat)\n"
                   "    msgbox(%sPost, MSGBOX_AUTOCLOSE)\n}\n\n"
                   "text %sIntro {\n    format(\"%s\")\n}\n\ntext %sDefeat {\n    format(\"%s\")\n}\n\n"
                   "text %sPost {\n    format(\"%s\")\n}\n" % (
                       lab, tr["const"], pre, pre, pre, pre, esc(tr["intro"]), pre, esc(tr["defeat"]), pre, post))
            s = s[:mm.start()] + new + s[mm.end():]
        open(sp, "w").write(s)
        jdump(mp, m)
        inc = P("data", "maps", folder, "scripts.inc")
        if os.path.exists(inc):
            os.remove(inc)          # poryscript regenerates it (avoids a same-second stale .inc)


# ------------------------------------------------------------------ main
def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "check":
        sys.exit(1 if check_sight() else 0)
    if cmd == "apply":
        install_trainers()
        install_trainer_maps()
        import apply_world
        apply_world.main()
        check_sight(verbose=False)


if __name__ == "__main__":
    main()
