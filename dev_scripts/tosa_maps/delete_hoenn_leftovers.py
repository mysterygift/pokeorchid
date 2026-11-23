#!/usr/bin/env python3
"""
Second Hoenn deletion pass (designer, 2026-11-23: "you can get rid of those leftover hoenn maps").
The leftover vanilla Hoenn maps still place gTileset_General metatiles, which blocks reclaiming
General's palette colours / tiles (night-lit Centre, Mart and station windows). Builds on
delete_hoenn_maps.py (first pass, 2026-11-19) and reuses its machinery.

Deleted:
  * gMapGroup_TownsAndRoutes except the Orchid maps (TosaPort, TelokTown, SouthTosaReserve):
    Fortree, Dewford, Lavaridge, Fallarbor, Verdanturf, Pacifidlog, Routes 115-134, Underwater 124-129;
  * their interiors (IndoorDewford ... IndoorRoute124, incl. the Fallarbor / Verdanturf Battle Tents);
  * every gMapGroup_Dungeons map;
  * in gMapGroup_SpecialArea: the Safari Zone and the Hoenn places only the deleted harbours / routes
    led to (Faraway Island, Birth Island, Navel Rock, Trainer Hill).
Kept: Battle Frontier, IndoorDynamic (secret bases, link rooms, contest halls, SS Tidal, truck),
Southern Island (the Wavebreak voyage lands there, src/voyages.c), the Ever Grande League rooms and
every Orchid group / map. Any map an Orchid map still warps / connects to / names in its scripts is
kept (KEEP below, plus an abort if one is found that is not listed).

Same handling as the first pass, appending to its files instead of replacing them:
  * connections into deleted maps dropped, warps into them loop back to themselves;
  * MAP_ ids stay defined (mapjson "unused maps" enum); deleted maps' LOCALID_ ids are appended to
    include/constants/deleted_hoenn_maps.h (with their real values) unless a kept map defines them;
  * heal locations of deleted maps removed, aliased to Telok Town's Centre (HEAL_LOCATION_OLDALE_TOWN;
    Telok is the renamed Oldale) in include/constants/heal_location_aliases.h;
  * Fly table (src/region_map.c sMapHealLocations) entries naming a deleted map -> Telok Town;
  * gWildMonHeaders entries of deleted maps removed (other wild groups untouched);
  * layouts no remaining map uses are removed with their folders. Tilesets are never touched.
  * script labels still named by kept code after the deletion get stubs appended to
    data/scripts/deleted_hoenn_stubs.inc (STUBS below, taken from the link errors).

One-shot: run once from the repo root (python3 dev_scripts/tosa_maps/delete_hoenn_leftovers.py).
--dry-run prints the plan and the reference check without writing; --stubs-only just appends STUBS.
After running: rm build/emerald/data/*.d (stale deps name the deleted scripts.inc), then make.
"""
import glob
import json
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delete_hoenn_maps import ROOT, P, load, dump  # noqa: E402

KEEP_TOWNS_AND_ROUTES = {"TosaPort", "TelokTown", "SouthTosaReserve"}
DELETE_GROUPS = ["IndoorDewford", "IndoorLavaridge", "IndoorFallarbor", "IndoorVerdanturf",
                 "IndoorPacifidlog", "IndoorFortree", "IndoorRoute116", "IndoorRoute117",
                 "IndoorRoute119", "IndoorRoute121", "IndoorRoute123", "IndoorRoute124", "Dungeons"]
SPECIAL_AREA_DELETE = re.compile(r"^(SafariZone_|FarawayIsland_|BirthIsland_|NavelRock_|TrainerHill_)")
# Maps on the delete list that Orchid content really uses (found by the reference check). None so far.
KEEP = set()
# Never rewrite these (another engineer edits them).
HANDS_OFF = {"TosaPort"}
VANILLA = "expansion/1.17.2"
TELOK_MAP, TELOK_HEAL = "MAP_OLDALE_TOWN", "HEAL_LOCATION_OLDALE_TOWN"

# Labels from deleted maps' scripts that kept code (vanilla C / shared scripts) still names; from the
# link errors after the deletion. Scripts end, texts are empty - only dead paths reach them.
STUBS = [
    ("FarawayIsland_Interior_EventScript_HideMewWhenGrassCut", "script"),   # src/fldeff_cut.c
    ("IslandCave_EventScript_OpenRegiEntrance", "script"),                  # src/field_control_avatar.c
    ("Kecleon_Text_SomethingUnseeable", "text"),                            # data/scripts (Kecleon, Route 120)
    ("Kecleon_Text_UseDevonScopeMonAttacked", "text"),
    ("Kecleon_Text_WantToUseDevonScope", "text"),
    ("Route119_EventScript_ScottWonAtFortreeGymCall", "script"),            # src/field_control_avatar.c
    ("SkyPillar_Outside_EventScript_ClosedDoor", "script"),                 # src/field_control_avatar.c
    ("TrainerHill_Entrance_Text_ChallengeTime", "text"),                    # data/scripts/trainer_hill.inc
]

MAP_TOK = re.compile(r"\bMAP_[A-Z0-9_]+\b")


def vanilla_map_names():
    out = subprocess.run(["git", "show", VANILLA + ":data/maps/map_groups.json"], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout
    mg = json.loads(out)
    return {n for g in mg["group_order"] for n in mg[g]}


def script_text(name):
    d = P("data", "maps", name)
    files = [f for f in glob.glob(d + "/*.inc") if os.path.basename(f) not in
             ("events.inc", "header.inc", "connections.inc")] + glob.glob(d + "/*.pory")
    return "".join(open(f, errors="ignore").read() for f in files)


def refs_of(m, ids):
    """Deleted-map ids a map warps / connects to or names in its scripts."""
    r = {w["dest_map"] for w in m.get("warp_events", []) if w["dest_map"] in ids}
    r |= {c["map"] for c in (m.get("connections") or []) if c["map"] in ids}
    r |= {t for t in MAP_TOK.findall(script_text(m["name"])) if t in ids}
    return r


def append_defines(path, guard_end, title, pairs, skip):
    """Append '#define name value' lines before the include guard's #endif (skipping names already
    in the file or in skip)."""
    text = open(path).read()
    have = set(re.findall(r"#define\s+(\w+)", text))
    new = [(k, v) for k, v in pairs if k not in have and k not in skip]
    if not new:
        return 0
    block = ["", "// " + title] + ["#define %-48s %s" % (k, v) for k, v in new] + [""]
    i = text.rindex(guard_end)
    text = text[:i].rstrip("\n") + "\n" + "\n".join(block) + "\n" + text[i:]
    open(path, "w").write(text)
    return len(new)


def append_stubs(stubs):
    path = P("data", "scripts", "deleted_hoenn_stubs.inc")
    text = open(path).read()
    have = set(re.findall(r"^(\w+)::", text, re.M))
    add = []
    for label, kind in stubs:
        if label in have:
            continue
        body = {"script": "\tend", "text": '\t.string "$"', "movement": "\tstep_end"}[kind]
        add.append("%s::\n%s\n" % (label, body))
    if add:
        if "delete_hoenn_leftovers" not in text:
            text = text.rstrip("\n") + "\n\n@ Second pass (dev_scripts/tosa_maps/delete_hoenn_leftovers.py).\n"
        text = text.rstrip("\n") + "\n\n" + "\n".join(add)
        open(path, "w").write(text)
    return len(add)


def main():
    dry = "--dry-run" in sys.argv
    stubs_only = "--stubs-only" in sys.argv
    if stubs_only:
        print("stubs appended:", append_stubs(STUBS))
        return
    mg = load(P("data", "maps", "map_groups.json"))
    maps = {}
    for f in glob.glob(P("data", "maps", "*", "map.json")):
        m = load(f)
        maps[m["name"]] = m

    doomed = {n for n in mg.get("gMapGroup_TownsAndRoutes", []) if n not in KEEP_TOWNS_AND_ROUTES}
    for g in DELETE_GROUPS:
        doomed |= set(mg.get("gMapGroup_" + g, []))
    doomed |= {n for n in mg.get("gMapGroup_SpecialArea", []) if SPECIAL_AREA_DELETE.match(n)}
    doomed -= KEEP
    doomed &= set(maps)
    if not doomed:
        print("nothing to delete (already run?)")
        return
    ids = {maps[n]["id"]: n for n in doomed}
    kept = [n for n in maps if n not in doomed]

    # reference check: an Orchid map (not in vanilla) that still uses a deleted map aborts the run
    vanilla = vanilla_map_names()
    orchid_refs, vanilla_refs = {}, {}
    for n in kept:
        r = refs_of(maps[n], ids)
        if r:
            (vanilla_refs if n in vanilla else orchid_refs)[n] = sorted(r)
    for n, r in sorted(vanilla_refs.items()):
        print("  kept vanilla map %s -> deleted %s (warps loop / connections drop)" % (n, r))
    if orchid_refs:
        for n, r in sorted(orchid_refs.items()):
            print("  ORCHID map %s uses deleted %s" % (n, r))
        sys.exit("Orchid maps use maps on the delete list: add them to KEEP")
    for g in ["gMapGroup_TosaRail", "gMapGroup_TosaOverworld", "gMapGroup_Tiksi", "gMapGroup_Voyages",
              "gMapGroup_Holon", "gMapGroup_Sevii", "gMapGroup_TrainTest", "gMapGroup_IndoorDynamic",
              "gMapGroup_IndoorEverGrande"]:
        assert not doomed & set(mg.get(g, [])), "would delete maps of " + g
    assert not doomed & ({"SouthernIsland_Exterior", "SouthernIsland_Interior"} | KEEP_TOWNS_AND_ROUTES)
    assert not any(n.startswith("BattleFrontier_") for n in doomed)
    by_group = {g: [n for n in mg[g] if n in doomed] for g in mg["group_order"]}
    print("deleting %d maps:" % len(doomed))
    for g, ns in by_group.items():
        if ns:
            print("  %s (%d/%d): %s" % (g, len(ns), len(mg[g]), " ".join(ns)))
    if dry:
        return

    # remaining maps: drop connections, loop warps
    for name in kept:
        m = maps[name]
        changed = False
        conns = m.get("connections") or []
        keep = [c for c in conns if c["map"] not in ids]
        if len(keep) != len(conns):
            m["connections"] = keep or None
            changed = True
        for i, w in enumerate(m.get("warp_events", [])):
            if w["dest_map"] in ids:
                w["dest_map"], w["dest_warp_id"] = m["id"], str(i)
                changed = True
        if changed:
            assert name not in HANDS_OFF, name
            dump(P("data", "maps", name, "map.json"), m)

    # map groups, layouts, script includes, folders
    used_layouts = {maps[n]["layout"] for n in kept}
    for g in list(mg["group_order"]):
        mg[g] = [n for n in mg[g] if n not in doomed]
        if not mg[g]:
            mg["group_order"].remove(g)
            del mg[g]
    dump(P("data", "maps", "map_groups.json"), mg)
    lj = load(P("data", "layouts", "layouts.json"))
    gone = [l for l in lj["layouts"] if l.get("id") not in used_layouts and
            any(maps[n]["layout"] == l.get("id") for n in doomed)]
    lj["layouts"] = [l for l in lj["layouts"] if l not in gone]
    dump(P("data", "layouts", "layouts.json"), lj)
    kept_dirs = {os.path.dirname(l[k]) for l in lj["layouts"] if l for k in ("blockdata_filepath", "border_filepath")}
    for l in gone:
        d = os.path.dirname(l["blockdata_filepath"])
        if d not in kept_dirs and os.path.isdir(P(d)):
            shutil.rmtree(P(d))
    es = open(P("data", "event_scripts.s")).read().split("\n")
    es = [ln for ln in es if not any('data/maps/%s/' % n in ln for n in doomed)]
    open(P("data", "event_scripts.s"), "w").write("\n".join(es))
    for n in doomed:
        shutil.rmtree(P("data", "maps", n))

    # heal locations -> Telok Town
    hp = P("src", "data", "heal_locations.json")
    heal = load(hp)
    removed = [h["id"] for h in heal["heal_locations"] if h["map"] in ids or h.get("respawn_map") in ids]
    heal["heal_locations"] = [h for h in heal["heal_locations"] if h["id"] not in removed]
    dump(hp, heal)

    # wild encounters: drop the deleted maps' gWildMonHeaders entries
    wp = P("src", "data", "wild_encounters.json")
    wild = load(wp)
    dropped = 0
    for grp in wild["wild_encounter_groups"]:
        if grp.get("label") != "gWildMonHeaders":
            continue
        before = len(grp["encounters"])
        grp["encounters"] = [e for e in grp["encounters"] if e.get("map") not in ids]
        dropped += before - len(grp["encounters"])
    dump(wp, wild)

    # LOCALIDs of the deleted maps (real values) unless a kept map still defines the name
    kept_lids = {o["local_id"] for n in kept for o in maps[n].get("object_events", []) if o.get("local_id")}
    lids = {}
    for n in sorted(doomed):
        for i, o in enumerate(maps[n].get("object_events", [])):
            if o.get("local_id"):
                lids.setdefault(o["local_id"], i + 1)
    n_lid = append_defines(P("include", "constants", "deleted_hoenn_maps.h"), "#endif",
                           "Second pass (delete_hoenn_leftovers.py): leftover Hoenn maps' local ids.",
                           sorted(lids.items()), kept_lids)
    n_heal = append_defines(P("include", "constants", "heal_location_aliases.h"), "#endif",
                            "Second pass (delete_hoenn_leftovers.py): leftover Hoenn heal locations -> Telok Town.",
                            [(h, TELOK_HEAL) for h in sorted(removed)], set())

    # Fly table: entries naming a deleted map fly to Telok Town
    rp = P("src", "region_map.c")
    rc = open(rp).read()
    i = rc.index("static const u8 sMapHealLocations[][3] =")
    j = rc.index("};", i)
    tab = rc[i:j]
    fly = 0
    for mid in ids:
        old = "MAP_GROUP(%s), MAP_NUM(%s)" % (mid, mid)
        if old in tab:
            tab = tab.replace(old, "MAP_GROUP(%s), MAP_NUM(%s)" % (TELOK_MAP, TELOK_MAP))
            fly += 1
    for hid in removed:
        tab = tab.replace(hid + "}", TELOK_HEAL + "}")
    open(rp, "w").write(rc[:i] + tab + rc[j:])

    n_stub = append_stubs(STUBS)
    print("layouts removed %d, heal locations removed %d (%s), wild entries dropped %d, "
          "localids added %d, heal aliases added %d, fly entries redirected %d, stubs added %d"
          % (len(gone), len(removed), ", ".join(removed), dropped, n_lid, n_heal, fly, n_stub))
    print("layouts removed:", " ".join(l["id"] for l in gone))


if __name__ == "__main__":
    main()
