"""
Swap the Holon stream's placeholders for the real names once the trainers + delta streams are merged.

  trainers stream: OBJ_EVENT_GFX_HOLON_RESEARCHER, TRAINER_HOLON_IDO/CHRISTOPHE/MATEO/HENRIK/TOBIAS/KENJI,
                   OBJ_EVENT_GFX_CYNTHIA + Common_EventScript_CynthiaHolonLake + FLAG_CYNTHIA_BEATEN_AT_LAKE
  delta stream:    SPECIES_<BASE>_DELTA (Eevee-δ gift, shiny Gyarados-δ static, wild tables)

Idempotent. Run from the repo root of the merged tree:  python3 dev_scripts/voyages/holon/swap_placeholders.py
(--dry-run prints what would change). Afterwards rebuild; include/constants/holon.h keeps only the comment block.
"""
import json
import os
import re
import sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
P = lambda *a: os.path.join(ROOT, *a)   # noqa: E731
DRY = "--dry-run" in sys.argv

TRAINERS = {"TODO_TRAINER_HOLON_RESEARCHER_1": "TRAINER_HOLON_IDO",
            "TODO_TRAINER_HOLON_RESEARCHER_2": "TRAINER_HOLON_CHRISTOPHE",
            "TODO_TRAINER_HOLON_RESEARCHER_3": "TRAINER_HOLON_MATEO",
            "TODO_TRAINER_HOLON_RESEARCHER_4": "TRAINER_HOLON_HENRIK",
            "TODO_TRAINER_HOLON_RESEARCHER_5": "TRAINER_HOLON_TOBIAS",
            "TODO_TRAINER_HOLON_RESEARCHER_6": "TRAINER_HOLON_KENJI"}
TRAINER_MAPS = ["HolonMirageForest", "HolonLake", "HolonResearchTower_2F"]


def edit(path, fn):
    old = open(path).read()
    new = fn(old)
    if new != old:
        print(("would edit " if DRY else "edit ") + os.path.relpath(path, ROOT))
        if not DRY:
            open(path, "w").write(new)
            if path.endswith("scripts.pory"):
                inc = os.path.join(os.path.dirname(path), "scripts.inc")
                if os.path.exists(inc):
                    os.remove(inc)


def swap_pory(s):
    for a, b in TRAINERS.items():
        s = s.replace(a, b)
    s = s.replace("SPECIES_EEVEE,", "SPECIES_EEVEE_DELTA,").replace("SPECIES_EEVEE\n", "SPECIES_EEVEE_DELTA\n")
    s = s.replace("givemon SPECIES_EEVEE, 50", "givemon SPECIES_EEVEE_DELTA, 50")
    s = re.sub(r"\bSPECIES_GYARADOS\b(?!_)", "SPECIES_GYARADOS_DELTA", s)
    # Cynthia: the trainers stream's common script replaces the placeholder stub
    s = s.replace("\tcall Holon_CynthiaPlaceholder\n", "\tgoto Common_EventScript_CynthiaHolonLake\n")
    return s


def swap_json(s):
    j = json.loads(s, object_pairs_hook=OrderedDict)
    for o in j.get("object_events") or []:
        if o.get("graphics_id") == "OBJ_EVENT_GFX_SCIENTIST_1" and o.get("trainer_type") == "TRAINER_TYPE_NORMAL":
            o["graphics_id"] = "OBJ_EVENT_GFX_HOLON_RESEARCHER"
        if o.get("local_id") == "LOCALID_HOLON_CYNTHIA":
            o["graphics_id"] = "OBJ_EVENT_GFX_CYNTHIA"
            o["script"] = "Common_EventScript_CynthiaHolonLake"
            o["flag"] = "FLAG_CYNTHIA_BEATEN_AT_LAKE"
        if o.get("local_id") == "LOCALID_HOLON_GYARADOS":
            o["graphics_id"] = "OBJ_EVENT_GFX_SPECIES_SHINY(GYARADOS_DELTA)"
    return json.dumps(j, indent=2, ensure_ascii=False) + "\n"


def swap_header(s):
    s = re.sub(r"#define TODO_TRAINER_HOLON_RESEARCHER_\d\s+\w+\s*//[^\n]*\n", "", s)
    s = s.replace("#define HOLON_SPHERE_GLOW_FLAG            FLAG_HOLON_SPHERE_GLOW",
                  "#define HOLON_SPHERE_GLOW_FLAG            FLAG_CYNTHIA_BEATEN_AT_LAKE")
    return s


def swap_wild():
    delta = json.load(open(os.path.join(HERE, "wild_delta.json")), object_pairs_hook=OrderedDict)["encounters"]
    by = {e["base_label"]: e for e in delta}
    wp = P("src", "data", "wild_encounters.json")

    def fn(s):
        wj = json.loads(s, object_pairs_hook=OrderedDict)
        grp = wj["wild_encounter_groups"][0]
        grp["encounters"] = [by.get(e.get("base_label"), e) for e in grp["encounters"]]
        return json.dumps(wj, indent=2, ensure_ascii=False) + "\n"
    edit(wp, fn)


def main():
    for m in os.listdir(P("data", "maps")):
        if not m.startswith("Holon"):
            continue
        edit(P("data", "maps", m, "scripts.pory"), swap_pory)
        edit(P("data", "maps", m, "map.json"), swap_json)
    edit(P("include", "constants", "holon.h"), swap_header)
    swap_wild()


if __name__ == "__main__":
    main()
