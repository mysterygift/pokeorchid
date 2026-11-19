#!/usr/bin/env python3
"""
People and doors for the approved Tiksi towns (gen_tiksi_maps.py built the layouts; they stay as they are).

  - every house door without a warp gets an interior (shared vanilla house layouts) with its people;
    Mart doors get a Mart (copy of Telok's). The closed Silph office and Mural Hall stay sign-only.
  - NPCs from town_text.TIKSI, moved to the nearest tile the player can reach if the hint is blocked
  - each Regi cave gets a mouth in its town (the caves only had exits before) and a Regi Guardian
    beside it (TODO.md: guardians stand at the dungeon entrances). Drake Base Camp uses the Jagged
    Pass cave mound so it matches the ash slope; the others use the General cave mouth.

Idempotent: interiors are rewritten, the town's tiksi_people block in scripts.pory is replaced, and a
mouth is stamped only where its cells still hold the original blocks (recorded in tiksi_people.json).

usage: python3 dev_scripts/tiksi_maps/tiksi_people.py
"""
import json
import os
import re
import struct
import sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "dev_scripts", "tosa_maps"))
import placeholders as PH                         # noqa: E402
import towns as TW                                # noqa: E402
from town_text import TIKSI, G                    # noqa: E402

P = PH.P
GROUP = "gMapGroup_Tiksi"
STATE = os.path.join(HERE, "tiksi_people.json")
JAGGED_MOUND = [[0x0668, 0x0669, 0x066A], [0x0678, 0x0256, 0x067A], [0x0674, 0x025E, 0x0674]]   # Jagged Pass (16,18)
MOUND_DOOR = (1, 2)
MOUTH_DOOR = (1, 3)
CLOSED = {"UbeCity": [(22, 9)], "TanglynTown": [(5, 5), (6, 5)]}     # Silph office, Mural Hall (approved)
MART_DOOR = 0x041
# mouths moved elsewhere: where they were, and the approved map's blocks there (aefd62456c)
GONE = {("DrakeBaseCamp", "MtDrakeSummit"): ((9, 7), [[12913, 12913, 12913], [12913, 12913, 12913], [1657, 1657, 1657]]),
        ("DrakeBaseCamp", "RegolisShrine"): ((4, 7), [[1652, 1652, 1658], [1756, 1757, 1756], [1492, 1493, 1492]]),
        ("DrakeBaseCamp", "FerrumShrine"): ((23, 7), [[1815, 1494, 1493], [1817, 1500, 1501], [1493, 1492, 1493]])}
# cave folder, top-left of the stamp, kind, guardian graphics, guardian line
MOUTHS = {
    "FurongVillage": [("GavaniPath", (6, 13), "general", G("EXPERT_M"),
                       "I am the guardian of Gavani Path. The thunder giant has come home to its cave.\\pTiksi's elders swore to keep it from the people. Tread carefully in there.")],
    "DrakeBaseCamp": [],   # Regolis Shrine is entered from Route 403, Mt. Drake from its own maps (mt_drake.py)
    "TanglynTown": [("FrigoCave", (30, 2), "general", G("OLD_WOMAN"),
                     "Frigo Cave is colder than it has any right to be. The ice giant is back inside.\\pI have guarded this shore all my life. Don't make me regret letting you pass.")],
}


def drake_base_camp_top(vals, w):
    """The user asked for the volcanic slope and its cave to go (Mt. Drake has its own maps now): rows
    0-9 become grass and trees matching the lower camp, with a dirt path north to Route 404 (its south
    opening lands on our x 13-16)."""
    import dress
    out = list(vals)
    for y in range(10):
        for x in range(w):
            out[y * w + x] = PH.GRASS
    tree_blocks = [(bx, by) for by in range(0, 10, 2) for bx in (0, 2, 26, 28)]
    tree_blocks += [(bx, 0) for bx in range(4, 12, 2)] + [(bx, 0) for bx in range(18, 26, 2)]
    tree_blocks += [(6, 4), (8, 4), (20, 2), (22, 6), (4, 8)]
    for bx, by in tree_blocks:
        for j in (0, 1):
            for i in (0, 1):
                out[(by + j) * w + bx + i] = PH.TREE[(i, j)]
    for bx in (0, 2, 26, 28):                       # trees stacked down the side columns overlap
        for by in range(0, 10, 2):
            for i in (0, 1):
                out[(by + 1) * w + bx + i] = PH.TREE_STACK[i]
    for x, y in [(x, y) for y in (5, 6) for x in range(18, 23)] + [(x, y) for y in (3, 4) for x in range(10, 13)]:
        out[y * w + x] = PH.TALL
    for y in range(0, 11):
        out[y * w + 14] = out[y * w + 15] = PH.PATH
    return dress.apply(out, w, len(out) // w, "dirt", [], "DrakeBaseCamp")


def read_layout(m, layouts):
    lay = layouts[m["layout"]]
    vals = PH.read_bin(P(lay["blockdata_filepath"]))
    return lay, vals


def door_cells(lay, vals):
    sec = re.sub(r"(?<!^)(?=[A-Z])", "_", lay["secondary_tileset"][9:]).lower()
    prim = attrs("primary", "general")
    secd = attrs("secondary", sec)
    beh = enum_behaviours()
    out = []
    for i, b in enumerate(vals):
        mt = b & 0x3FF
        a = prim[mt] if mt < 512 else secd[mt - 512]
        if "DOOR" in beh.get(a & 0xFF, ""):
            out.append((i % lay["width"], i // lay["width"], mt))
    return out


def attrs(kind, name):
    return PH.read_bin(P("data", "tilesets", kind, name, "metatile_attributes.bin"))


def enum_behaviours():
    src = open(P("include", "constants", "metatile_behaviors.h")).read()
    body = src[src.index("{") + 1:src.index("}")]
    out, v = {}, 0
    for tok in body.split(","):
        tok = re.sub(r"//.*", "", tok).strip()
        if not tok:
            continue
        if "=" in tok:
            n, val = tok.split("=")
            v = int(val.strip(), 0)
            n = n.strip()
        else:
            n = tok
        out[v] = n
        v += 1
    return out


def reachable(lay, vals, start):
    w, h = lay["width"], lay["height"]
    col = lambda x, y: (vals[y * w + x] >> 10) & 3
    el = lambda x, y: vals[y * w + x] >> 12
    seen, q = {start}, [start]
    while q:
        x, y = q.pop()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in seen and not col(nx, ny):
                e1, e2 = el(x, y), el(nx, ny)
                if e1 == e2 or e1 in (0, 15) or e2 in (0, 15):
                    seen.add((nx, ny))
                    q.append((nx, ny))
    return seen


def main():
    state = json.load(open(STATE)) if os.path.exists(STATE) else {}
    lj = json.load(open(P("data", "layouts", "layouts.json")), object_pairs_hook=OrderedDict)
    layouts = OrderedDict((l["id"], l) for l in lj["layouts"])
    mg_path = P("data", "maps", "map_groups.json")
    mg = json.load(open(mg_path), object_pairs_hook=OrderedDict)
    group = mg[GROUP]
    new_includes = []
    only = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
    for town, spec in TIKSI.items():
        if only and town not in only:
            continue
        mpath = P("data", "maps", town, "map.json")
        m = json.load(open(mpath), object_pairs_hook=OrderedDict)
        lay, vals = read_layout(m, layouts)
        w = lay["width"]
        const = m["id"][4:]
        st = state.setdefault(town, {})
        # --- cave mouths (stamped once; the original blocks are remembered)
        warps = [wv for wv in m["warp_events"] if not wv.get("_tiksi")]
        keep = []
        for wv in m["warp_events"]:
            dest_folder = TW.folder_of(wv["dest_map"]) if wv["dest_map"].startswith("MAP_") else None
            if dest_folder and (dest_folder in [c[0] for c in MOUTHS.get(town, [])] or
                                (town, dest_folder) in GONE or
                                dest_folder.startswith(town + "_House") or dest_folder == town + "_Mart"):
                continue                                   # rebuilt below
            keep.append(wv)
        m["warp_events"] = keep
        guardians = []
        # mouths that were moved elsewhere (mt_drake.py): put the approved blocks back
        for (t, cave), ((x0, y0), rows) in GONE.items():
            if t != town:
                continue
            for j, row in enumerate(rows):
                for i, v in enumerate(row):
                    vals[(y0 + j) * w + x0 + i] = v
            st.pop(cave, None)
            st.pop(cave + "@", None)
        for cave, (x0, y0), kind, gfx, line in MOUTHS.get(town, []):
            rows = JAGGED_MOUND if kind == "jagged" else PH.MOUTH
            door = MOUND_DOOR if kind == "jagged" else MOUTH_DOOR
            key = cave
            if key not in st:
                st[key] = [[vals[(y0 + j) * w + x0 + i] for i in range(len(rows[0]))] for j in range(len(rows))]
            st[key + "@"] = [x0, y0]
            for j, row in enumerate(rows):
                for i, v in enumerate(row):
                    vals[(y0 + j) * w + x0 + i] = v
            dx, dy = x0 + door[0], y0 + door[1]
            idx = len(m["warp_events"])
            m["warp_events"].append(OrderedDict([("x", dx), ("y", dy), ("elevation", 0),
                                                 ("dest_map", "MAP_" + PH.snake(cave)), ("dest_warp_id", "0")]))
            cj_path = P("data", "maps", cave, "map.json")
            cj = json.load(open(cj_path), object_pairs_hook=OrderedDict)
            cj["warp_events"][0].update(dest_map=m["id"], dest_warp_id=str(idx))
            PH.write_json(cj_path, cj)
            guardians.append((gfx, (dx + 2, dy + 1), line, cave))
        if town == "DrakeBaseCamp":
            vals = drake_base_camp_top(vals, w)
        PH.write_bin(P(lay["blockdata_filepath"]), vals)
        # --- doors without warps: houses and Marts
        centre = next(wv for wv in m["warp_events"] if wv["dest_map"].endswith("_POKEMON_CENTER_1F"))
        reach = reachable(lay, vals, (centre["x"], centre["y"] + 1))
        warped = {(wv["x"], wv["y"]) for wv in m["warp_events"]}
        doors = [(x, y, mt) for x, y, mt in door_cells(lay, vals)
                 if (x, y) not in warped and (x, y) not in CLOSED.get(town, [])]
        nh = 0
        for x, y, mt in sorted(doors, key=lambda d: (d[1], d[0])):
            idx = len(m["warp_events"])
            if mt == MART_DOOR:
                folder, im, ipory = PH.clone_mart(town, const, m["region_map_section"])
                for wv in im["warp_events"]:
                    wv["dest_warp_id"] = str(idx)
                im["music"] = m["music"]
                PH.write_json(P("data", "maps", folder, "map.json"), im)
                TW.write_pory(folder, ipory)
                dest = im["id"]
            else:
                folder = "%s_House%d" % (town, nh + 1)
                people = spec["houses"][nh] if nh < len(spec["houses"]) else []
                lid, exits, spots = TW.INTERIORS[(nh + 3) % len(TW.INTERIORS)]
                dest = "MAP_" + PH.snake(town) + "_HOUSE%d" % (nh + 1)
                objs, pory = [], "mapscripts %s_MapScripts {}\n" % folder
                for j, (g, text) in enumerate(people[:len(spots)]):
                    sx, sy, mv = spots[j]
                    label = "%s_EventScript_Npc%d" % (folder, j + 1)
                    objs.append(TW.obj(g, sx, sy, 3, "MOVEMENT_TYPE_" + mv, label, 1 if mv == "WANDER_AROUND" else 0))
                    pory += TW.msg(label, text, "MSGBOX_NPC")
                im = OrderedDict([
                    ("id", dest), ("name", folder), ("layout", lid), ("music", m["music"]),
                    ("region", m.get("region", "REGION_HOENN")), ("region_map_section", m["region_map_section"]),
                    ("requires_flash", False), ("weather", "WEATHER_NONE"), ("map_type", "MAP_TYPE_INDOOR"),
                    ("allow_cycling", False), ("allow_escaping", False), ("allow_running", False),
                    ("show_map_name", False), ("battle_scene", "MAP_BATTLE_SCENE_NORMAL"), ("connections", None),
                    ("object_events", objs),
                    ("warp_events", [OrderedDict([("x", ex), ("y", ey), ("elevation", 0), ("dest_map", m["id"]),
                                                  ("dest_warp_id", str(idx))]) for ex, ey in exits]),
                    ("coord_events", []), ("bg_events", [])])
                PH.write_json(P("data", "maps", folder, "map.json"), im)
                TW.write_pory(folder, pory)
                nh += 1
            m["warp_events"].append(OrderedDict([("x", x), ("y", y), ("elevation", 0), ("dest_map", dest),
                                                 ("dest_warp_id", "0")]))
            if folder not in group:
                group.append(folder)
                new_includes.append(folder)
        # --- NPCs and guardians
        warps_xy = [(wv["x"], wv["y"]) for wv in m["warp_events"]]
        avoid = warps_xy + [(x, y + 1) for x, y in warps_xy] + [(b["x"], b["y"]) for b in m["bg_events"]]
        taken = []
        objs = [o for o in m["object_events"] if not o["script"].startswith(town + "_EventScript_Tiksi")]

        def spot(hint):
            best = None
            for (x, y) in reach:
                if (x, y) in avoid or any(abs(x - a) + abs(y - b) < 2 for a, b in taken):
                    continue
                if any(abs(x - a) <= 1 and abs(y - b) <= 1 for a, b in warps_xy):
                    continue
                d = abs(x - hint[0]) + abs(y - hint[1])
                if best is None or d < best[0]:
                    best = (d, x, y)
            taken.append(best[1:])
            return best[1:]
        pory_block = ""
        people = [(g, hint, mv, text, "Npc%d" % (k + 1)) for k, (g, hint, mv, text) in enumerate(spec["npcs"])]
        people += [(g, hint, "down", line, "Guardian" + cave) for g, hint, line, cave in guardians]
        for g, hint, mv, text, tag in people:
            x, y = spot(hint)
            label = "%s_EventScript_Tiksi%s" % (town, tag)
            elev = (vals[y * w + x] >> 12) & 0xF
            objs.append(TW.obj(g, x, y, elev, mv, label))
            pory_block += TW.msg(label, text, "MSGBOX_NPC")
        m["object_events"] = objs
        PH.write_json(mpath, m)
        pory_path = P("data", "maps", town, "scripts.pory")
        pory = open(pory_path).read()
        start, end = "// --- tiksi_people.py (generated) ---", "// --- end tiksi_people.py ---"
        if start in pory:
            pory = pory[:pory.index(start)] + pory[pory.index(end) + len(end) + 1:]
        pory = pory.rstrip("\n") + "\n\n" + start + "\n" + pory_block + end + "\n"
        TW.write_pory(town, pory)
        print("%-14s houses %d  npcs %d  mouths %d  warps %d" % (town, nh, len(people), len(guardians), len(m["warp_events"])))
    PH.write_json(mg_path, mg)
    es_path = P("data", "event_scripts.s")
    es = open(es_path).read()
    missing = [f for f in group if ('data/maps/%s/scripts.inc' % f) not in es]
    if missing:
        lines = es.split("\n")
        at = max(i for i, l in enumerate(lines) if "data/maps/MtDrakeSummit/scripts.inc" in l or "@ tiksi-people" in l)
        lines[at + 1:at + 1] = ['\t.include "data/maps/%s/scripts.inc" @ tiksi-people' % f for f in missing]
        open(es_path, "w").write("\n".join(lines))
    json.dump(state, open(STATE, "w"), indent=1)


if __name__ == "__main__":
    main()
