#!/usr/bin/env python3
"""
Inka Seawall: a short coastal route between Route 314 (west, open sea) and Inka City (east). The land
was reclaimed from the sea: a paved promenade along a concrete seawall, parkland behind it, and a
popular date spot, so it is full of couples and other trainers.

  - 40x30. West strip and everything south of the wall is sea (surfable, continuous with Route 314);
    a small beach at the west end to land on. Promenade (TosaPort cobble) rows 13-16, the pier slab
    (0x3B3 / 0x3B4 with bollards) rows 17-18 and the pier face (0x3B5) row 19 make the seawall.
    Inka's west road (its rows 18-19) meets promenade rows 14-15: connection offset -4.
  - park: shrub hedge along the promenade, the Lovers' Knot sculpture (TosaPort 2x2 statue), trees,
    flowers (dress.py), signs
  - 8 trainers in reused vanilla slots 10-17 (aliases keep the old names building), 2 NPCs,
    Route 314's water / fishing encounters
  - region map: cell (14, 14) becomes MAPSEC_INKA_SEAWALL (Route 314 shrinks to cells 8-13);
    connections Route 314 <-> Inka Seawall <-> Inka City replace Route 314 <-> Inka City

Re-runnable: it rewrites the map, the trainer entries and the region-map edit in place.
usage: python3 dev_scripts/tosa_maps/inka_seawall.py
"""
import json
import os
import re
import sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import placeholders as PH        # noqa: E402
import dress                     # noqa: E402
import towns as TW               # noqa: E402

P = PH.P
NAME, MAP_ID, LAYOUT, MAPSEC = "InkaSeawall", "MAP_INKA_SEAWALL", "LAYOUT_INKA_SEAWALL", "MAPSEC_INKA_SEAWALL"
W, H = 40, 30
CELL = (14, 14)
INKA_OFFSET = -4                  # Inka row r sits on our row r - 4
PROM = (13, 16)                   # promenade rows
LAND_X = 8                        # first land column (beach)
WALK_X = 12                       # promenade / seawall start
TOP, SLAB, FACE = 17, 18, 19      # seawall rows

COBBLE = TW.COBBLE
SLAB_TOP, SLAB_MID, BOLLARD, FACE_T = 0x33B3, 0x33B4, 0x07C7, 0x07B5
SLAB_TOP_L, SLAB_MID_L, FACE_L = 0x33B0, 0x07B1, 0x07B2
SHRUB, PLANTERS, POT = 0x0400 | 0x243, (0x0400 | 0x213, 0x0400 | 0x214), 0x0400 | 0x20B
STATUE = [[0x0400 | 0x246, 0x0400 | 0x247], [0x0400 | 0x256, 0x0400 | 0x257]]

G = lambda s: "OBJ_EVENT_GFX_" + s
# slot, constant, name, class, pic, gender, music, double, party, [(gfx, x, y, facing, sight, intro, defeat, post, notenough)]
TRAINERS = [
    ("TRAINER_GRUNT_PETALBURG_WOODS", "TRAINER_AMIR_AND_NUR", "Amir & Nur", "Young Couple", "Young Couple", "Male", "Girl", True,
     [("Plusle", 34), ("Minun", 34)],
     [(G("MAN_3"), 17, 13, "down", 2, "AMIR: We come here every Friday. Nur says the sunset's better than any film.",
       "AMIR: Even losing is fine, as long as it's together.", "AMIR: Our Pokémon are a couple too. They copy everything we do.",
       "AMIR: A double battle needs two Pokémon. Come back with a partner for yours!"),
      (G("WOMAN_2"), 18, 13, "down", 2, "NUR: You'll battle us both? That's very brave. Or very lonely.",
       "NUR: Amir, you were supposed to protect me!", "NUR: Plusle and Minun cheer each other on. Like us. Mostly.",
       "NUR: We battle as a pair. You need two Pokémon to take us on.")]),
    ("TRAINER_MARCEL", "TRAINER_JUN_AND_HUI", "Jun & Hui", "Young Couple", "Young Couple", "Male", "Girl", True,
     [("Volbeat", 34), ("Illumise", 34)],
     [(G("BOY_2"), 31, 16, "up", 1, "JUN: Shh, we're watching the ships come in. Unless… you want a battle?",
       "JUN: We were distracted. By the view. Obviously.", "JUN: At night Volbeat and Illumise light up the whole seawall.",
       "JUN: Two of us, two of yours. Bring another Pokémon."),
      (G("GIRL_3"), 32, 16, "up", 1, "HUI: This is our anniversary! Make it a battle to remember!",
       "HUI: Well, we'll definitely remember it.", "HUI: Five years ago Jun asked me out right on this spot. He was so nervous.",
       "HUI: Come back with two Pokémon and we'll battle!")]),
    ("TRAINER_ALBERTO", "TRAINER_CHLOE", "Chloe", "Influencer", "Influencer", "Female", "Female", False,
     [("Delcatty", 34), ("Jynx", 35)],
     [(G("INFLUENCER"), 23, 16, "up", 3, "Golden hour on the seawall! Quick, battle me while the lighting's good!",
       "Ugh, my followers saw that live.", "Hashtag Inka Seawall, hashtag sunset, hashtag couple goals… I'm here alone, but the hashtags don't know that.", None)]),
    ("TRAINER_ED", "TRAINER_IMRAN", "Imran", "Triathlete", "Running Triathlete M", "Male", "Male", False,
     [("Ninjask", 34), ("Linoone", 34), ("Dodrio", 35)],
     [(G("RUNNING_TRIATHLETE_M"), 27, 14, "walklr", 3, "Morning run, evening run, I'm always on the seawall! Keep up!",
       "Out of breath… and out of Pokémon.", "Five laps from the beach to Inka every day. The couples keep getting in my way.", None)]),
    ("TRAINER_GRUNT_SEAFLOOR_CAVERN_4", "TRAINER_SITI", "Siti", "Beauty", "Beauty", "Female", "Female", False,
     [("Roselia", 35), ("Bellossom", 35)],
     [(G("BEAUTY"), 36, 13, "down", 2, "My date's late. Again. You'll have to do.",
       "Hmph. At least you showed up.", "If he isn't here by sunset, I'm giving these flowers to my Bellossom.", None)]),
    ("TRAINER_DECLAN", "TRAINER_HOCK_AND_LAN", "Hock & Lan", "Old Couple", "Old Couple", "Male", "Intense", True,
     [("Azumarill", 35), ("Dewgong", 36)],
     [(G("OLD_MAN"), 20, 9, "down", 2, "UNCLE HOCK: When we were young, this was all water. We courted on a sampan!",
       "UNCLE HOCK: Fifty years married and still learning.", "UNCLE HOCK: They filled in the sea so people had room to walk. Best thing Inka ever did.",
       "UNCLE HOCK: We battle side by side. You'll need two Pokémon."),
      (G("OLD_WOMAN"), 21, 9, "down", 2, "AUNTIE LAN: Don't go easy on us, dear. We certainly won't on you.",
       "AUNTIE LAN: Oh, well done! Your mother must be proud.", "AUNTIE LAN: Every evening we walk to the sculpture and back. Every single evening.",
       "AUNTIE LAN: Come back with two Pokémon, dear.")]),
    ("TRAINER_GRUNT_RUSTURF_TUNNEL", "TRAINER_YUKI", "Yuki", "Tourist", "Tourist F", "Female", "Female", False,
     [("Spinda", 33), ("Castform", 33), ("Pelipper", 34)],
     [(G("TOURIST_F"), 28, 7, "left", 3, "The guidebook says this is the most romantic spot in Tosa! …I came with my Pokémon.",
       "My Pokémon and I had a lovely time anyway.", "I came all the way from Johto for this sunset. Totally worth it.", None)]),
    ("TRAINER_GRUNT_WEATHER_INST_1", "TRAINER_FAIZ", "Faiz", "Rider", "Rider", "Male", "Male", False,
     [("Manectric", 34), ("Raichu", 34), ("Swellow", 35)],
     [(G("RIDER"), 14, 15, "right", 4, "Flower delivery for… a couple on the seawall. That narrows it down to everyone!",
       "Okay, okay, you win. Don't tell my customer I stopped.", "Valentine's week, I deliver here forty times a day.", None)]),
]
NPCS = [
    (G("FISHERMAN"), 21, 18, "down", "This seawall used to be open sea. My father fished from a boat right where I'm standing."
     "\\pNow I fish from the wall. Same fish, though."),
    (G("LASS"), 25, 10, "look", "Couples tie a ribbon on the Lovers' Knot and make a wish.\\pI tied three. Just to be safe."),
]
SIGNS = [
    ((12, 11), "INKA SEAWALL\nReclaimed from the sea for the people of Inka."),
    ((23, 8), "LOVERS' KNOT\nCouples who walk the seawall at sunset are said to stay together forever."),
]
STATUE_AT = (24, 6)


def layout():
    code = [["G"] * W for _ in range(H)]
    raw = {}
    for y in range(H):
        for x in range(W):
            if x < LAND_X or y >= TOP or (x < WALK_X and y > PROM[1]):
                code[y][x] = "W"
            elif x < WALK_X:
                code[y][x] = "S"                     # landing beach
    for y in range(PROM[0], PROM[1] + 1):
        for x in range(WALK_X, W):
            code[y][x] = "C"
    for x in range(WALK_X, W):                       # the seawall
        raw[(x, TOP)] = SLAB_TOP_L if x == WALK_X else SLAB_TOP
        raw[(x, SLAB)] = SLAB_MID_L if x == WALK_X else (BOLLARD if (x - WALK_X) % 5 == 3 else SLAB_MID)
        raw[(x, FACE)] = FACE_L if x == WALK_X else FACE_T
        for y in (TOP, SLAB, FACE):
            code[y][x] = "R"
    # trees: top border, east edge outside the opening onto Inka's road
    for y in range(0, 2):
        for x in range(LAND_X, W):
            code[y][x] = "X"
    for y in range(0, PROM[0] - 1):
        for x in (W - 2, W - 1):
            code[y][x] = "X"
    # park furniture
    sx, sy = STATUE_AT
    for j in range(2):
        for i in range(2):
            raw[(sx + i, sy + j)] = STATUE[j][i]
            code[sy + j][sx + i] = "R"
    for x in range(WALK_X + 2, W - 2):               # hedge along the promenade, with gaps into the park
        if (x - WALK_X) % 7 not in (0, 1):
            raw[(x, PROM[0] - 1)] = SHRUB
            code[PROM[0] - 1][x] = "R"
    for k, x in enumerate(range(WALK_X + 3, W - 3, 9)):    # planters on the promenade's park side
        raw[(x, PROM[0])] = PLANTERS[k % 2]
    for (x, y), _ in SIGNS:
        raw[(x, y)] = PH.SIGN
        code[y][x] = "R"
    return code, raw


def render(code, raw):
    out = []
    isc = lambda x, y: x >= W or (0 <= x and 0 <= y < H and code[y][x] == "C" and (x, y) not in raw)
    for y in range(H):
        for x in range(W):
            if (x, y) in raw:
                out.append(raw[(x, y)])
                continue
            c = code[y][x]
            if c == "C":
                n, s, w_, e = isc(x, y - 1), isc(x, y + 1), isc(x - 1, y), isc(x + 1, y)
                k = ("T" if not n else "B" if not s else "") + ("L" if not w_ else "R" if not e else "")
                out.append(COBBLE[k or "C"])
            elif c == "X":
                bx, by = x // 2, y // 2
                tb = lambda bx_, by_: all(0 <= by_ * 2 + j < H and code[by_ * 2 + j][bx_ * 2 + i] == "X" for i in (0, 1) for j in (0, 1))
                if tb(bx, by):
                    out.append(PH.TREE_STACK[x % 2] if y % 2 and tb(bx, by + 1) else PH.TREE[(x % 2, y % 2)])
                else:
                    out.append(PH.GRASS)
            else:
                out.append({"G": PH.GRASS, "S": PH.SAND, "W": PH.SEA}[c])
    return out


def patch_trainers():
    oph = P("include", "constants", "opponents.h")
    src = open(oph).read()
    aliases = []
    for slot, const, *_ in TRAINERS:
        src = re.sub(r"#define %s(\s+)(\d+)" % slot, lambda mm: "#define %s%s%s" % (
            const, " " * max(1, len(slot) + len(mm.group(1)) - len(const)), mm.group(2)), src)
        aliases.append("#define %-37s %s" % (slot, const))
    marker = "// Orchid: vanilla slots 10-17 were reused for the Inka Seawall trainers."
    block = marker + "\n" + "\n".join(aliases) + "\n"
    if marker in src:
        start = src.index(marker)
        src = src[:start] + block + src[src.index("\n\n", start) + 1:]
    else:
        anchor = "// NOTE: Because each Trainer uses a flag"
        src = src.replace(anchor, block + "\n" + anchor)
    open(oph, "w").write(src)
    tp = P("src", "data", "trainers.party")
    party = open(tp).read()
    for slot, const, name, cls, pic, gender, music, double, mons, _ in TRAINERS:
        assert len(name) <= 10, name
        body = ["=== %s ===" % const, "Name: %s" % name, "Class: %s" % cls, "Pic: %s" % pic, "Gender: %s" % gender,
                "Music: %s" % music, "Double Battle: %s" % ("Yes" if double else "No"), "AI: Basic Trainer", ""]
        for sp, lv in mons:
            body += [sp, "Level: %d" % lv, ""]
        new = "\n".join(body) + "\n"
        for head in ("=== %s ===" % slot, "=== %s ===" % const):
            if head in party:
                i = party.index(head)
                j = party.find("\n=== ", i + 4)
                j = len(party) if j < 0 else j + 1
                party = party[:i] + new + party[j:]
                break
        else:
            raise SystemExit("no trainers.party entry for " + slot)
    open(tp, "w").write(party)


def trainer_obj(gfx, x, y, facing, sight, script):
    mv = {"down": "MOVEMENT_TYPE_FACE_DOWN", "up": "MOVEMENT_TYPE_FACE_UP", "left": "MOVEMENT_TYPE_FACE_LEFT",
          "right": "MOVEMENT_TYPE_FACE_RIGHT", "walklr": "MOVEMENT_TYPE_WALK_LEFT_AND_RIGHT"}[facing]
    o = TW.obj(gfx, x, y, 3, mv, script, 2 if facing == "walklr" else 0)
    o["trainer_type"] = "TRAINER_TYPE_NORMAL"
    o["trainer_sight_or_berry_tree_id"] = str(sight)
    return o


def pory_text(label, text):
    return 'text %s {\n    format("%s")\n}\n\n' % (label, text.replace('"', "'"))


def region_map():
    # region_map_sections.json: Route 314 gives up its east cell
    rp = P("src", "data", "region_map", "region_map_sections.json")
    rs = json.load(open(rp), object_pairs_hook=OrderedDict)
    secs = rs["map_sections"]
    r314 = next(s for s in secs if s["id"] == "MAPSEC_ROUTE_314")
    r314["width"] = CELL[0] - r314["x"]
    secs[:] = [s for s in secs if s["id"] != MAPSEC] + [OrderedDict([
        ("id", MAPSEC), ("name", "Inka Seawall"), ("x", CELL[0]), ("y", CELL[1]), ("width", 1), ("height", 1)])]
    with open(rp, "w") as f:
        f.write(json.dumps(rs, indent=2, ensure_ascii=False) + "\n")
    # cursor grid header
    lp = P("src", "data", "region_map", "region_map_layout.h")
    lines = open(lp).read().split("\n")
    rows = [i for i, l in enumerate(lines) if l.strip().startswith("{MAPSEC_")]
    row = lines[rows[CELL[1]]]
    cells = re.findall(r"MAPSEC_\w+", row)
    assert cells[CELL[0]] in ("MAPSEC_ROUTE_314", MAPSEC), cells[CELL[0]]
    cells[CELL[0]] = MAPSEC
    lines[rows[CELL[1]]] = row[:row.index("{")] + "{" + ", ".join(cells) + "},"
    open(lp, "w").write("\n".join(lines))
    # the tagger
    tp = P("dev_scripts", "region_map_tagger", "tags.json")
    raw = open(tp).read()
    t = json.loads(raw, object_pairs_hook=OrderedDict)
    if not any(a["key"] == MAPSEC for a in t["areas"]):
        t["areas"].append(OrderedDict([("key", MAPSEC), ("id", MAPSEC), ("originalId", MAPSEC), ("name", "Inka Seawall"),
                                       ("origName", "Inka Seawall"), ("kind", "route"), ("notes", ""), ("kanto", False)]))
    t["grid"][CELL[1]][CELL[0]] = MAPSEC
    t["mapAssign"][NAME] = MAPSEC
    indent = 2 if raw.startswith("{\n  \"") else None
    with open(tp, "w") as f:
        f.write(json.dumps(t, indent=indent, ensure_ascii=False) + ("\n" if raw.endswith("\n") else ""))


def set_connections(name, conns):
    p = P("data", "maps", name, "map.json")
    m = json.load(open(p), object_pairs_hook=OrderedDict)
    dirs = {d for d, _, _ in conns}
    m["connections"] = [c for c in (m.get("connections") or []) if c["direction"] not in dirs] + \
        [OrderedDict([("map", mp), ("offset", off), ("direction", d)]) for d, mp, off in conns]
    PH.write_json(p, m)


def main():
    code, raw = layout()
    blocks = render(code, raw)
    events = [xy for xy, _ in SIGNS] + [(x, y) for *_, people in TRAINERS for (_, x, y, *__) in people] + \
        [(x, y) for _, x, y, _, _ in NPCS]
    blocks = dress.apply(blocks, W, H, "dirt", events, NAME, flowers=5, groves=5, rocks=False)
    PH.write_bin(P("data", "layouts", NAME, "map.bin"), blocks)
    PH.write_bin(P("data", "layouts", NAME, "border.bin"), PH.SEA_TS[2])

    lj_path = P("data", "layouts", "layouts.json")
    lj = json.load(open(lj_path), object_pairs_hook=OrderedDict)
    lj["layouts"] = [l for l in lj["layouts"] if l.get("id") != LAYOUT] + [OrderedDict([
        ("id", LAYOUT), ("name", NAME + "_Layout"), ("width", W), ("height", H),
        ("primary_tileset", "gTileset_General"), ("secondary_tileset", "gTileset_TosaPort"),
        ("border_filepath", "data/layouts/%s/border.bin" % NAME),
        ("blockdata_filepath", "data/layouts/%s/map.bin" % NAME), ("layout_version", "emerald")])]
    PH.write_json(lj_path, lj)

    objs, pory = [], "mapscripts %s_MapScripts {}\n\n" % NAME
    for k, (xy, text) in enumerate(SIGNS):
        pory += TW.msg("%s_EventScript_Sign%d" % (NAME, k + 1), text, "MSGBOX_SIGN")
    for slot, const, name, cls, pic, gender, music, double, mons, people in TRAINERS:
        for (gfx, x, y, facing, sight, intro, defeat, post, notenough) in people:
            who = re.sub(r"\W", "", (intro.split(":")[0] if double else name).title())
            label = "%s_EventScript_%s" % (NAME, who)
            objs.append(trainer_obj(gfx, x, y, facing, sight, label))
            t = "%s_Text_%s" % (NAME, who)
            if double:
                pory += ("script %s {\n    trainerbattle_double(%s, %sIntro, %sDefeat, %sNotEnough)\n"
                         "    msgbox(%sPost, MSGBOX_AUTOCLOSE)\n}\n\n") % (label, const, t, t, t, t)
            else:
                pory += ("script %s {\n    trainerbattle_single(%s, %sIntro, %sDefeat)\n"
                         "    msgbox(%sPost, MSGBOX_AUTOCLOSE)\n}\n\n") % (label, const, t, t, t)
            pory += pory_text(t + "Intro", intro) + pory_text(t + "Defeat", defeat) + pory_text(t + "Post", post)
            if double:
                pory += pory_text(t + "NotEnough", notenough)
    for k, (gfx, x, y, move, text) in enumerate(NPCS):
        label = "%s_EventScript_Npc%d" % (NAME, k + 1)
        objs.append(TW.obj(gfx, x, y, 3, move, label))
        pory += TW.msg(label, text, "MSGBOX_NPC")

    m = OrderedDict([
        ("id", MAP_ID), ("name", NAME), ("layout", LAYOUT), ("music", "MUS_ROUTE104"),
        ("region", "REGION_HOENN"), ("region_map_section", MAPSEC), ("requires_flash", False),
        ("weather", "WEATHER_SUNNY"), ("map_type", "MAP_TYPE_ROUTE"), ("allow_cycling", True),
        ("allow_escaping", False), ("allow_running", True), ("show_map_name", True),
        ("battle_scene", "MAP_BATTLE_SCENE_NORMAL"), ("connections", None),
        ("object_events", objs), ("warp_events", []), ("coord_events", []),
        ("bg_events", [OrderedDict([("type", "sign"), ("x", x), ("y", y), ("elevation", 0),
                                    ("player_facing_dir", "BG_EVENT_PLAYER_FACING_ANY"),
                                    ("script", "%s_EventScript_Sign%d" % (NAME, k + 1))])
                       for k, ((x, y), _) in enumerate(SIGNS)])])
    PH.write_json(P("data", "maps", NAME, "map.json"), m)
    TW.write_pory(NAME, pory)
    set_connections(NAME, [("left", "MAP_ROUTE314", 0), ("right", "MAP_INKA_CITY", INKA_OFFSET)])
    set_connections("Route314", [("right", MAP_ID, 0)])
    set_connections("InkaCity", [("left", MAP_ID, -INKA_OFFSET)])

    mg_path = P("data", "maps", "map_groups.json")
    mg = json.load(open(mg_path), object_pairs_hook=OrderedDict)
    if NAME not in mg[PH.GROUP]:
        mg[PH.GROUP].append(NAME)
        PH.write_json(mg_path, mg)
    es_path = P("data", "event_scripts.s")
    es = open(es_path).read()
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % NAME
    if inc not in es:
        anchor = '\t.include "data/maps/InkaCity/scripts.inc"\n'
        assert anchor in es
        open(es_path, "w").write(es.replace(anchor, anchor + inc))

    we_path = P("src", "data", "wild_encounters.json")
    we = json.load(open(we_path), object_pairs_hook=OrderedDict)
    enc = we["wild_encounter_groups"][0]["encounters"]
    enc[:] = [e for e in enc if e.get("map") != MAP_ID]
    src = next(e for e in enc if e.get("map") == "MAP_ROUTE314")
    entry = OrderedDict([("map", MAP_ID), ("base_label", "g" + NAME)])
    for k in ("water_mons", "fishing_mons"):
        entry[k] = json.loads(json.dumps(src[k]), object_pairs_hook=OrderedDict)
    enc.insert(enc.index(src) + 1, entry)
    with open(we_path, "w") as f:
        json.dump(we, f, indent=2, ensure_ascii=False)
        f.write("\n")

    patch_trainers()
    region_map()
    print("%s %dx%d: %d trainers, %d NPCs" % (NAME, W, H, len(TRAINERS), len(NPCS)))


if __name__ == "__main__":
    main()
