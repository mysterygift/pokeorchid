#!/usr/bin/env python3
"""Legality check for every Pokemon used in the Cold Storage test: the six trainers, Haru as a
battle partner and the test team the aide hands out. Uses this repo's own data:

  * each move must be in the species' level-up learnset (the P_LVL_UP_LEARNSETS generation) at or
    below the mon's level; level 0 entries are evolution moves and count for the evolved form
  * an evolved species must be at least the level its pre-evolution evolves at (EVO_LEVEL);
    stone / item evolutions have no minimum

    python3 dev_scripts/cold_storage_tileset/check_movesets.py      (no dependencies)
"""
import glob
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


def read(path):
    return open(os.path.join(ROOT, path)).read()


def const(name):
    return re.sub(r"[^A-Z0-9]+", "_", name.upper()).strip("_")


def learnsets():
    gen = re.search(r"#define P_LVL_UP_LEARNSETS\s+(\w+)", read("include/config/pokemon.h")).group(1)
    files = sorted(glob.glob(os.path.join(ROOT, "src/data/pokemon/level_up_learnsets/gen_*.h")))
    path = files[-1] if gen == "GEN_LATEST" else os.path.join(ROOT, f"src/data/pokemon/level_up_learnsets/{gen.lower()}.h")
    text = open(path).read() + read("src/data/pokemon/orchid_learnsets.h")
    arrays = {}
    for m in re.finditer(r"static const struct LevelUpMove (s\w+LevelUpLearnset)\[\] = \{(.*?)\};", text, re.S):
        arrays[m.group(1)] = [(int(lv), mv) for lv, mv in re.findall(r"LEVEL_UP_MOVE\(\s*(\d+),\s*MOVE_(\w+)\)", m.group(2))]
    return arrays, os.path.relpath(path, ROOT)


def species_info():
    """{SPECIES: (learnset array name, [(method, param, target)])}"""
    out = {}
    for path in glob.glob(os.path.join(ROOT, "src/data/pokemon/species_info/*.h")):
        text = open(path).read()
        for m in re.finditer(r"\[SPECIES_(\w+)\]\s*=\s*\{(.*?)\n    \},", text, re.S):
            body = m.group(2)
            ls = re.search(r"\.levelUpLearnset = (\w+)", body)
            evos = re.findall(r"\{(EVO_\w+),\s*(\w+),\s*SPECIES_(\w+)", body)
            if ls:
                out[m.group(1)] = (ls.group(1), evos)
    return out


def party_mons(path, wanted):
    """Yield (owner, species, level, [moves]) from a .party file for the trainers in `wanted`."""
    text = read(path)
    for block in re.split(r"^=== ", text, flags=re.M)[1:]:
        owner = block.split(" ===")[0]
        if not wanted(owner):
            continue
        for mon in re.split(r"\n\s*\n", block.split("\n", 1)[1]):
            lines = [ln.strip() for ln in mon.strip().split("\n") if ln.strip()]
            if not any(ln.startswith("Level:") for ln in lines):
                continue
            species = re.sub(r"\s*\(.*?\)", "", lines[0].split("@")[0]).strip()
            level = int(next(ln for ln in lines if ln.startswith("Level:")).split(":")[1])
            yield owner, const(species), level, [const(ln[2:]) for ln in lines if ln.startswith("- ")]


def script_mons(path):
    for m in re.finditer(r"givemon SPECIES_(\w+), (\d+)(.*)", read(path)):
        yield "TEST TEAM (aide)", m.group(1), int(m.group(2)), re.findall(r"move\d=MOVE_(\w+)", m.group(3))


def main():
    arrays, source = learnsets()
    info = species_info()
    pre_evo = {}
    for sp, (_, evos) in info.items():
        for method, param, target in evos:
            pre_evo.setdefault(target, []).append((sp, method, param))
    mons = list(party_mons("src/data/trainers.party", lambda o: o.startswith("TRAINER_COLD_STORAGE_")))
    mons += list(party_mons("src/data/battle_partners.party", lambda o: o == "PARTNER_HARU"))
    mons += list(script_mons("data/maps/ColdStorageTest/scripts.pory"))
    print(f"level-up learnsets: {source}")
    bad, last = 0, None
    for owner, sp, level, moves in mons:
        if owner != last:
            print(f"\n{owner}")
            last = owner
        problems = []
        if sp not in info:
            problems.append("unknown species")
        else:
            learn = arrays[info[sp][0]]
            for mv in moves:
                lv = [l for l, m in learn if m == mv]
                if not lv:
                    problems.append(f"{mv} is not a level-up move")
                elif min(lv) > level:
                    problems.append(f"{mv} is learned at Lv. {min(lv)}")
            mins = [int(p) for _, method, p in pre_evo.get(sp, []) if method == "EVO_LEVEL" and p.isdigit()]
            if pre_evo.get(sp) and mins and level < min(mins):
                problems.append(f"evolves at Lv. {min(mins)}")
            if len(moves) != len(set(moves)) or not 1 <= len(moves) <= 4:
                problems.append("bad move list")
        bad += bool(problems)
        how = ""
        if sp in pre_evo:
            src, method, p = pre_evo[sp][0]
            how = f"  [from {src.title()}: {method} {p}]"
        print(f"  {'FAIL' if problems else 'ok  '} {sp.title():<11} Lv. {level:<3} {', '.join(m.title().replace('_', ' ') for m in moves)}{how}")
        for p in problems:
            print(f"         -> {p}")
    print(f"\n{len(mons)} Pokemon checked, {bad} with problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
