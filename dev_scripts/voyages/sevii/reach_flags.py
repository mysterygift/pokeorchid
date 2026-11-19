#!/usr/bin/env python3
"""
Find vanilla FLAG_ITEM_* (0x3E8-0x44F) and FLAG_HIDDEN_ITEM_* flags that are safe to reuse for Sevii items:
their map can't be reached from MAP_TOSA_PORT (BFS over connections, warps, and every MAP_* named in a reachable
map's scripts or in data/scripts/*), nothing reachable or in src/ names them, and they aren't already aliased.
usage: python3 dev_scripts/voyages/sevii/reach_flags.py [--json]
"""
import glob, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
P = lambda *p: os.path.join(ROOT, *p)
MAPRE = re.compile(r"\bMAP_[A-Z0-9_]+\b")
FLAGRE = re.compile(r"\bFLAG_[A-Z0-9_]+\b")
SKIP = {"MAP_DYNAMIC", "MAP_UNDEFINED", "MAP_NONE"}


def maps():
    out = {}
    for mj in glob.glob(P("data", "maps", "*", "map.json")):
        j = json.load(open(mj))
        if "id" in j:
            out[j["id"]] = (os.path.dirname(mj), j)
    return out


def script_text(folder):
    t = ""
    for f in ("scripts.pory", "scripts.inc"):
        if os.path.exists(os.path.join(folder, f)):
            t += open(os.path.join(folder, f)).read()
    return t


def reachable(M, extra_seeds=()):
    common = "".join(open(f).read() for f in glob.glob(P("data", "scripts", "*.inc")) + glob.glob(P("data", "scripts", "*.pory")))
    seeds = {"MAP_TOSA_PORT", *extra_seeds} | (set(MAPRE.findall(common)) & set(M))
    seen, todo = set(), list(seeds)
    while todo:
        m = todo.pop()
        if m in seen or m not in M:
            continue
        seen.add(m)
        folder, j = M[m]
        nxt = [c["map"] for c in j.get("connections") or []] + [w["dest_map"] for w in j.get("warp_events", [])]
        nxt += MAPRE.findall(script_text(folder))
        todo += [n for n in nxt if n not in SKIP]
    return seen


def flag_defs():
    vals, aliases = {}, set()
    for line in open(P("include", "constants", "flags.h")):
        m = re.match(r"#define (FLAG_(?:ITEM|HIDDEN_ITEM)_[A-Z0-9_]+)\s+(.+?)\s*(//.*)?$", line)
        if not m:
            continue
        name, val = m.group(1), m.group(2)
        if re.match(r"^FLAG_[A-Z0-9_]+$", val):
            aliases.add(name); aliases.add(val)
            continue
        h = re.match(r"\(FLAG_HIDDEN_ITEMS_START \+ (0x[0-9A-Fa-f]+)\)", val)
        vals[name] = 0x1F4 + int(h.group(1), 16) if h else int(val, 16) if val.startswith("0x") else None
    return vals, aliases


def main(quiet=False):
    M = maps()
    R = reachable(M)
    used = set()
    for m in R:
        folder, j = M[m]
        used |= set(FLAGRE.findall(json.dumps(j) + script_text(folder)))
    for f in glob.glob(P("src", "**", "*.c"), recursive=True) + glob.glob(P("src", "**", "*.h"), recursive=True) + \
            glob.glob(P("data", "scripts", "*")) + glob.glob(P("data", "*.s")):
        try:
            used |= set(FLAGRE.findall(open(f, errors="ignore").read()))
        except IsADirectoryError:
            pass
    vals, aliases = flag_defs()
    items = sorted((v, n) for n, v in vals.items() if n.startswith("FLAG_ITEM_") and v and 0x3E8 <= v <= 0x44F
                   and n not in used and n not in aliases)
    hidden = sorted((v, n) for n, v in vals.items() if n.startswith("FLAG_HIDDEN_ITEM_") and v
                    and n not in used and n not in aliases)
    res = {"reachable": sorted(R), "items": [[hex(v), n] for v, n in items], "hidden": [[hex(v), n] for v, n in hidden]}
    if quiet:
        pass
    elif "--json" in sys.argv:
        print(json.dumps(res, indent=1))
    else:
        print("reachable maps:", len(R), "of", len(M))
        print("free item flags:", len(items), " free hidden flags:", len(hidden))
    return res


if __name__ == "__main__":
    main()
