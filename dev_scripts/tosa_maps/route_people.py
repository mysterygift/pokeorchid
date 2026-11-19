#!/usr/bin/env python3
"""
A few NPCs on the Tosa placeholder routes, landmarks and dungeons (towns are done by towns.py).
Each person stands on a walkable tile near the middle of the map, away from warps and signs, with a
line drawn from TODO.md / the region map tagger notes. Re-running replaces only these NPCs (their
scripts are named <Map>_EventScript_Route*) and the generated block in scripts.pory.

usage: python3 dev_scripts/tosa_maps/route_people.py
"""
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import placeholders as PH        # noqa: E402
import towns as TW               # noqa: E402

P = PH.P
G = lambda s: "OBJ_EVENT_GFX_" + s
RANGER = "Rangers patrol the Tosa Reserve to protect the native Pokémon. Lately we spend most of our time tracking invasive species."
PEOPLE = {
    "Route302": [(G("YOUNGSTER"), "Mt. Batok's just east of here. The climb to Faber Town is no joke!"),
                 (G("LASS"), "Route 302's my favourite place to train. The wild Pokémon here are gentle.")],
    "Route303": [(G("CAMPER"), "Watch your step in the tall grass. You never know what'll jump out.")],
    "Route304": [(G("PICNICKER"), "I packed kaya toast for the walk. Want to share? …Oh, I already ate it.")],
    "Route305": [(G("HIKER"), "This route goes on forever! Good thing there are Pokémon Centres in every town."),
                 (G("BUG_CATCHER"), "I've seen Pokémon here that aren't in any of my books. Invasive, the Rangers said.")],
    "Route306": [(G("MAN_3"), "I walk to the airport every morning. It's a short, pleasant commute."),
                 (G("TOURIST_F"), "Is this the way to Changu City? My map's all in kilometres!")],
    "Route307": [(G("HIKER"), "The east side of Mt. Batok comes out just north of here. Took me all day.")],
    "Route308": [(G("CAMPER"), "I'm camping out to watch for rare Pokémon. Day three. Nothing yet.")],
    "Route309": [(G("PICNICKER"), "Such a long route! I keep stopping to look at the flowers.")],
    "Route310": [(G("BLACK_BELT"), "I run this route every morning. Builds the legs!")],
    "Route311_West": [(G("MAN_4"), "The Damp Path's crawling with thugs these days. Go round if you can.")],
    "Route311_East": [(G("WOMAN_2"), "You came through the Damp Path? Brave. Or foolish.")],
    "Route312": [(G("SWIMMER_M"), "The current's strong out here. Keep swimming!")],
    "Route313": [(G("SWIMMER_F"), "I'm swimming all the way to Pokétopia! …Eventually.")],
    "Route314": [(G("SAILOR"), "Ahoy! Tosa's waters are full of Pokémon you won't see anywhere else.")],
    "MoongroveMarsh": [(G("FISHERMAN"), "The catfish here are elusive. Tork says patience is everything."),
                       (G("HEX_MANIAC"), "Come back after dark… that's when the marsh ghosts come out to play.")],
    "GalangalForest": [(G("ORCHIDIST"), "Galangal Forest is full of medicinal plants. My grandmother made all her remedies from what grows here."),
                       (G("BUG_CATCHER"), "Shh! I'm stalking a rare Bug Pokémon. It's hiding in the galangal.")],
    "KantuFalls": [(G("OLD_WOMAN"), "Once or twice a year, the people of Faber Town come to bathe in the falls. The water's full of minerals."),
                   (G("TUBER_M"), "Brrr! The water's freezing… but I feel ten years younger!")],
    "RailwayTunnels": [(G("PORT_WORKER"), "These old tunnels run under Tosa Port station. We're not supposed to let anyone down here… but I won't tell.")],
    "DampPath": [(G("MANIAC"), "Oi, this is our path! Pay the toll or turn back!\\p…Just kidding. The Zubat are the real problem down here.")],
    "SouthTosaReserve2": [(G("POKEMON_RANGER_M"), RANGER)],
    "SouthTosaReserve3": [(G("POKEMON_RANGER_F"), RANGER)],
    "NorthTosaReserve": [(G("POKEMON_RANGER_M"), RANGER),
                         (G("SCIENTIST_1"), "Professor Palm asked me to count the Pokémon here. The numbers keep changing every year.")],
    "EastTosaReserve": [(G("POKEMON_RANGER_F"), RANGER),
                        (G("EXPERT_M"), "When I was a boy, every Pokémon in this reserve was native to Tosa. Not any more.")],
    "MtBatok_1F": [(G("HIKER"), "Mt. Batok goes up three floors to Faber Town. Mind the loose rocks!")],
    "MtBatok_2F": [(G("CAMPER"), "I think I'm lost. Is up this way?")],
    "MtBatok_3F": [(G("HIKER"), "Faber Town's just ahead. Meru climbs this every morning, you know.")],
    "MtBatok_East_2F": [(G("BLACK_BELT"), "I'm training on the mountain like Meru does. Ow, my toes.")],
    "MtBatok_East_1F": [(G("HIKER"), "This side of Mt. Batok comes out on Route 307.")],
    "ChallengersTrail_1F": [(G("MAN_3"), "Challenger's Trail. Only the best Trainers make it to the top.")],
    "ChallengersTrail_Cliffs": [(G("EXPERT_F"), "Halfway there. Don't look down!")],
    "ChallengersTrail_2F": [(G("WOMAN_5"), "My Pokémon are exhausted, but we're not giving up now!")],
    "ChallengersTrail_3F": [(G("MAN_3"), "The Pokémon League's just past this floor. Good luck!")],
}


def main():
    lj = json.load(open(P("data", "layouts", "layouts.json")))
    layouts = {l["id"]: l for l in lj["layouts"] if "id" in l}
    for name, people in PEOPLE.items():
        mpath = P("data", "maps", name, "map.json")
        m = json.load(open(mpath), object_pairs_hook=PH.OrderedDict)
        lay = layouts[m["layout"]]
        w, h = lay["width"], lay["height"]
        vals = PH.read_bin(P(lay["blockdata_filepath"]))
        water = m["map_type"] == "MAP_TYPE_OCEAN_ROUTE"
        avoid = [(wv["x"], wv["y"]) for wv in m["warp_events"]] + [(b["x"], b["y"]) for b in m["bg_events"]]
        rnd = random.Random(name)
        cx, cy = w // 2, h // 2
        objs = [o for o in m["object_events"] if not o["script"].startswith(name + "_EventScript_Route")]
        taken = [(o["x"], o["y"]) for o in objs]
        block = ""
        for k, (gfx, text) in enumerate(people):
            tx, ty = cx + rnd.randint(-8, 8), cy + rnd.randint(-6, 6)
            best = None
            for y in range(2, h - 2):
                for x in range(2, w - 2):
                    v = vals[y * w + x]
                    if (v >> 10) & 3:
                        continue
                    if water != ((v & 0x3FF) == (PH.SEA & 0x3FF)):
                        continue
                    if any(abs(x - a) <= 2 and abs(y - b) <= 2 for a, b in avoid + taken):
                        continue
                    d = abs(x - tx) + abs(y - ty)
                    if best is None or d < best[0]:
                        best = (d, x, y)
            if not best:
                print("  %s: nowhere for %s" % (name, gfx))
                continue
            _, x, y = best
            taken.append((x, y))
            label = "%s_EventScript_Route%d" % (name, k + 1)
            objs.append(TW.obj(gfx, x, y, (vals[y * w + x] >> 12) & 0xF, "look" if k % 2 else "wander", label))
            block += TW.msg(label, text, "MSGBOX_NPC")
        m["object_events"] = objs
        PH.write_json(mpath, m)
        pory_path = P("data", "maps", name, "scripts.pory")
        pory = open(pory_path).read()
        start, end = "// --- route_people.py (generated) ---", "// --- end route_people.py ---"
        if start in pory:
            pory = pory[:pory.index(start)] + pory[pory.index(end) + len(end) + 1:]
        if block:
            pory = pory.rstrip("\n") + "\n\n" + start + "\n" + block + end + "\n"
        TW.write_pory(name, pory)
        print("%-24s %d" % (name, len(people)))


if __name__ == "__main__":
    main()
