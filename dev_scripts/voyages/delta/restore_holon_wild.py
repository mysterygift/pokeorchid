"""Swap the intended Delta species back into the Holon wild tables (src/data/wild_encounters.json),
per dev_scripts/voyages/holon/wild_delta.json. Only slots whose current species is the δ entry's base
species (same levels) are touched. Re-runnable."""
import json, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
P = os.path.join(ROOT, "src/data/wild_encounters.json")
wd = json.load(open(os.path.join(ROOT, "dev_scripts/voyages/holon/wild_delta.json")))["encounters"]
we = json.load(open(P, encoding="utf-8"))
by = {}
for g in we["wild_encounter_groups"]:
    for e in g["encounters"]:
        by[(e.get("map"), e.get("base_label"))] = e
n = 0
for d in wd:
    e = by[(d["map"], d["base_label"])]
    for k, v in d.items():
        if not k.endswith("_mons"):
            continue
        for want, cur in zip(v["mons"], e[k]["mons"]):
            if want["species"] != cur["species"] and want["species"] == cur["species"] + "_DELTA" \
                    and (want["min_level"], want["max_level"]) == (cur["min_level"], cur["max_level"]):
                cur["species"] = want["species"]
                n += 1
open(P, "w", encoding="utf-8").write(json.dumps(we, indent=2, ensure_ascii=False) + "\n")
print("restored %d Delta slots" % n)
