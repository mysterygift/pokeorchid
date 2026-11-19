#!/usr/bin/env python3
"""
Placeholder maps for every place on the Tosa region map that has no Tosa-built map yet
(user, 2026-11-18/19: sizes from the descriptions, big reserves, bigger routes, Pokemon Centres and
Marts in the towns, the hawker centre in Bura City, multi-floor Challenger's Trail and Mt. Batok,
Railway Tunnels on the train-station tileset, a rocky Faber Town).

Scale: ~40 metatiles per region-map square along a route (min 30 across), towns ~24-28, cities ~36,
reserves as big as the engine allows ((w + 15) * (h + 14) <= 10240). Each map is a readable stand-in:
a border (trees / rock / cave wall) with an opening on every side that touches another place on the
region map, dirt paths to the middle, terrain by theme, and a sign with the place's description
(region map tagger notes / TODO.md). Doors, cave mouths, exit mats and ladders are real warps, linked
by name (LINKS). No map connections yet; the open sides are where they go.

Station towns (dev_scripts/train_ui/tosa_stations.py) keep their station building as warp 0 and are
enlarged from their stock 15x12 clearing. Centre / Mart / hawker centre interiors are copies of
TelokTown_PokemonCenter_1F, TelokTown_Mart and HawkerCentreTest (their scripts are reused globally).

Safe to re-run: maps are created only if missing; station exteriors are enlarged only while still
stock. Maps you have edited are never touched.

usage: python3 dev_scripts/tosa_maps/placeholders.py
"""
import json
import os
import random
import re
import struct
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
P = lambda *p: os.path.join(ROOT, *p)
GROUP = "gMapGroup_TosaOverworld"
MAX_MAP_DATA = 10240                     # fieldmap.c: (width + 15) * (height + 14)

# ---------------------------------------------------------------- block values (metatile | collision << 10 | elevation << 12)
GRASS, TALL, PATH, SAND, SEA, SIGN = 0x3001, 0x300D, 0x31D9, 0x3124, 0x1170, 0x0403
TREE = {(0, 0): 0x05D4, (1, 0): 0x05D5, (0, 1): 0x05DC, (1, 1): 0x05DD}
TREE_STACK = {0: 0x05E4, 1: 0x05E5}
ROCK_TOP, ROCK_FACE = 0x046C, 0x0471                     # General mountain top / face (Route 106)
MOUTH = [[0x046C, 0x046C, 0x046C], [0x0471, 0x0471, 0x0471],
         [0x0474, 0x0464, 0x047D], [0x047C, 0x00A7, 0x0491]]   # cave mouth (Route 106), door at (1, 3)
CAVE_FLOOR, CAVE_WALL, CAVE_LADDER, CAVE_MAT = 0x3201, 0x0611, 0x3205, 0x3207
CAVE_FACE = 0x0619                                         # Granite Cave ledge face
# gTileset_UrbanPlatform (station tileset)
T_VOID, T_PAVE_A, T_PAVE_B, T_TRACK, T_WALL, T_WALLBASE = 0x0600, 0x320D, 0x320E, 0x060B, 0x0605, 0x0607

OUTDOOR = ("gTileset_General", "gTileset_TosaPort", [0x1D4, 0x1D5, 0x1DC, 0x1DD])
ROCKY = ("gTileset_General", "gTileset_TosaPort", [0x071] * 4)
CAVE = ("gTileset_General", "gTileset_Cave", [0x211] * 4)
SEA_TS = ("gTileset_General", "gTileset_TosaPort", [0x170] * 4)
TUNNEL = ("gTileset_Building", "gTileset_UrbanPlatform", [0x200] * 4)

TOWN, CITY, ROUTE, SEAR, UNDER = "MAP_TYPE_TOWN", "MAP_TYPE_CITY", "MAP_TYPE_ROUTE", "MAP_TYPE_OCEAN_ROUTE", "MAP_TYPE_UNDERGROUND"
RESERVE_TEXT = ("A sprawling nature reserve at the heart of the Tosa region, home to all manner of species. "
                "Pokémon Rangers watch over it; invasive species from other regions are a growing problem.")
CM = {"centre": True, "mart": True}

# name, section, theme, (w, h), sign text, music, map type, extras
#   extras: cells (region squares, for split places), centre / mart / hawker, coast side, trees, tall,
#           mouths {key: side} (cave entrances), floor: {"mats": {key: x hint}, "ladders": {key: (fx, fy)}}
PLACES = [
    # station towns (map exists; enlarged around the station building, warp 0)
    ("MoongroveCity", "MAPSEC_MOONGROVE_CITY", "marsh", (36, 32), "Moongrove City: nestled in the mangroves. Gym leader Tork enjoys hunting for catfish.", None, CITY, dict(CM)),
    ("TimahCity", "MAPSEC_TIMAH_CITY", "city", (36, 32), "Timah City: in the tropical heart of the Tosa Reserve. Gym leader Hana cultivates orchids in her garden.", None, CITY, dict(CM, trees=6)),
    ("FaberTown", "MAPSEC_FABER_TOWN", "rocky", (28, 24), "Faber Town: nestled in the cliffs, reached by cable car or a treacherous climb. Meru, the town's leader, trains against Rock Pokémon.", None, TOWN, dict(CM, mouths={"batok_w": "W", "batok_e": "E"})),
    ("ChanguCity", "MAPSEC_CHANGU_CITY", "city", (36, 32), "Changu City: home of the Tosa region's airport.", None, CITY, dict(CM)),
    ("ChanguAirport", "MAPSEC_CHANGU_AIRPORT", "city", (36, 28), "Changu Airport: the Tosa region's international airport.", None, CITY, {}),
    ("InkaCity", "MAPSEC_INKA_CITY", "city", (36, 32), "Inka City: the region's logistics hub. Gym leader Frea runs a cold food distribution centre. Marlin Co. hides a secret.", None, CITY, dict(CM)),
    ("BuraCity", "MAPSEC_BURA_CITY", "city", (32, 28), "Bura City: a quiet stopover on the way between Changu and Juran.", None, CITY, dict(CM, hawker=True)),
    ("JuranCity", "MAPSEC_JURAN_CITY", "city", (36, 32), "Juran City.", None, CITY, dict(CM)),
    ("SenokoCity", "MAPSEC_SENOKO_CITY", "city", (36, 32), "Senoko City: Mo runs the national power grid and looks after the wind farms around town.", None, CITY, dict(CM)),
    ("PokemonLeague", "MAPSEC_PKMN_LEAGUE", "city", (32, 32), "Pokémon League.", None, CITY, dict(CM, mouths={"trail": "W"})),
    ("PoketopiaGate", "MAPSEC_POKETOPIA_GATE", "coast", (28, 24), "Pokétopia Gate: the way across to Pokétopia.", None, TOWN, {"coast": "S"}),
    ("CorralCity", "MAPSEC_CORRAL_CITY", "coast", (36, 32), "Corral City: the bustling beach city on Pokétopia, home to Marina's gym and a lovely marina.", None, CITY, dict(CM, coast="S")),
    # new towns
    ("WavebreakTown", "MAPSEC_WAVEBREAK_TOWN", "coast", (24, 24), "Wavebreak Town: a forgotten seaside town, home to Tosa's first port before Tosa Port opened.", "MUS_DEWFORD", TOWN, dict(CM, coast="W")),
    ("PinestampTown", "MAPSEC_PINESTAMP_TOWN", "town", (24, 22), "Pinestamp Town.", "MUS_OLDALE", TOWN, dict(CM, trees=10)),
    ("ChallengerGate", "MAPSEC_CHALLENGER_GATE", "city", (32, 32), "Challenger Gate: the last stop before Challenger's Trail and the Pokémon League.", "MUS_EVER_GRANDE", CITY, dict(CM, mouths={"trail": "E"})),
    # routes
    ("Route302", "MAPSEC_ROUTE_302", "route", (50, 30), "Route 302", "MUS_ROUTE104", ROUTE, {"mouths": {"batok": "E"}}),
    ("Route303", "MAPSEC_ROUTE_303", "route", (30, 50), "Route 303", "MUS_ROUTE104", ROUTE, {}),
    ("Route304", "MAPSEC_ROUTE_304", "route", (50, 30), "Route 304", "MUS_ROUTE104", ROUTE, {}),
    ("Route305", "MAPSEC_ROUTE_305", "route", (110, 64), "Route 305", "MUS_ROUTE119", ROUTE, {}),
    ("Route306", "MAPSEC_ROUTE_306", "route", (30, 40), "Route 306: a short, pleasant path for people commuting from Changu City to Changu Airport.", "MUS_ROUTE104", ROUTE, {"tall": 0.3}),
    ("Route307", "MAPSEC_ROUTE_307", "route", (30, 50), "Route 307", "MUS_ROUTE110", ROUTE, {"mouths": {"batok": "N"}}),
    ("Route308", "MAPSEC_ROUTE_308", "route", (70, 100), "Route 308", "MUS_ROUTE110", ROUTE, {}),
    ("Route309", "MAPSEC_ROUTE_309", "route", (120, 40), "Route 309", "MUS_ROUTE110", ROUTE, {}),
    ("Route310", "MAPSEC_ROUTE_310", "route", (40, 120), "Route 310", "MUS_ROUTE120", ROUTE, {}),
    ("Route311_West", "MAPSEC_ROUTE_311", "route", (50, 30), "Route 311 (west of the Damp Path)", "MUS_ROUTE113", ROUTE, {"cells": [(4, 8)], "mouths": {"damp": "E"}}),
    ("Route311_East", "MAPSEC_ROUTE_311", "route", (50, 30), "Route 311 (east of the Damp Path)", "MUS_ROUTE113", ROUTE, {"cells": [(6, 8)], "mouths": {"damp": "W"}}),
    ("Route312", "MAPSEC_ROUTE_312", "sea", (40, 140), "Route 312", "MUS_SURF", SEAR, {}),
    ("Route313", "MAPSEC_ROUTE_313", "sea", (120, 60), "Route 313", "MUS_SURF", SEAR, {}),
    ("Route314", "MAPSEC_ROUTE_314", "sea", (200, 30), "Route 314", "MUS_SURF", SEAR, {}),
    # landmarks
    ("MoongroveMarsh", "MAPSEC_MOONGROVE_MARSH", "marsh", (40, 40), "Moongrove Marsh: marshlands and mangroves around Moongrove City. Great for fishing up elusive Pokémon, and haunting ghosts come out at night.", "MUS_PETALBURG_WOODS", ROUTE, {}),
    ("PowerPlant", "MAPSEC_TOSA_POWER_PLANT", "town", (24, 20), "Power Plant: Senoko City's wind power plant.", "MUS_ROUTE110", ROUTE, {}),
    ("IndustrialPark", "MAPSEC_INDUSTRIAL_PARK", "city", (32, 28), "Industrial Park.", "MUS_ROUTE110", CITY, {}),
    ("AbandonedHouse", "MAPSEC_ABANDONED_HOUSE", "house", (20, 16), "Abandoned House: abandoned in the early days of the Tosa region. People in Moongrove spot lights here at night. It's haunted.", "MUS_ABANDONED_SHIP", ROUTE, {}),
    ("GalangalForest", "MAPSEC_GALANGAL_FOREST", "forest", (40, 40), "Galangal Forest: a range of medicinal plants grow here.", "MUS_PETALBURG_WOODS", ROUTE, {}),
    ("KantuFalls", "MAPSEC_KANTU_FALLS", "falls", (32, 32), "Kantu Falls: a beautiful series of waterfalls near Faber Town. Locals come once or twice a year to bathe in the mineral-rich waters.", "MUS_ROUTE119", ROUTE, {}),
    ("RailwayTunnels", "MAPSEC_RAILWAY_TUNNELS", "tunnel", (40, 30), "Railway Tunnels: dingy tunnels beneath Tosa Port railway station.", "MUS_SEALED_CHAMBER", UNDER, {}),
    ("DampPath", "MAPSEC_DAMP_PATH", "cave", (40, 24), "Damp Path: a wet, abandoned path through the hills of West Tosa. Filled with rowdy thugs and ne'er-do-wells now. And Zubat.", "MUS_SEALED_CHAMBER", UNDER, {"floor": {"mats": {"w": "w", "e": "e"}}}),
    ("SouthTosaReserve2", "MAPSEC_SOUTH_TOSA_RESERVE_2", "reserve", (90, 40), "South Tosa Reserve. " + RESERVE_TEXT, "MUS_SOUTHTOSARESERVE", ROUTE, {}),
    ("SouthTosaReserve3", "MAPSEC_SOUTH_TOSA_RESERVE_3", "reserve", (64, 80), "South Tosa Reserve. " + RESERVE_TEXT, "MUS_SOUTHTOSARESERVE", ROUTE, {}),
    ("NorthTosaReserve", "MAPSEC_NORTH_TOSA_RESERVE", "reserve", (40, 90), "North Tosa Reserve. " + RESERVE_TEXT, "MUS_SOUTHTOSARESERVE", ROUTE, {}),
    ("EastTosaReserve", "MAPSEC_EAST_TOSA_RESERVE", "reserve", (90, 80), "East Tosa Reserve. " + RESERVE_TEXT, "MUS_SOUTHTOSARESERVE", ROUTE, {}),
    # Mt. Batok: west climb Route 302 -> Faber Town, east descent Faber Town -> Route 307
    ("MtBatok_1F", "MAPSEC_MT_BATOK", "cave", (44, 32), "Mt. Batok 1F (from Route 302).", "MUS_MT_PYRE", UNDER, {"floor": {"mats": {"out": "w"}, "ladders": {"up": (0.8, 0.3)}}}),
    ("MtBatok_2F", "MAPSEC_MT_BATOK", "cave", (40, 32), "Mt. Batok 2F.", "MUS_MT_PYRE", UNDER, {"floor": {"ladders": {"down": (0.8, 0.3), "up": (0.2, 0.7)}}}),
    ("MtBatok_3F", "MAPSEC_MT_BATOK", "cave", (36, 28), "Mt. Batok 3F (to Faber Town).", "MUS_MT_PYRE", UNDER, {"floor": {"mats": {"out": "e"}, "ladders": {"down": (0.2, 0.3)}}}),
    ("MtBatok_East_2F", "MAPSEC_MT_BATOK", "cave", (40, 30), "Mt. Batok east 2F (from Faber Town).", "MUS_MT_PYRE", UNDER, {"floor": {"mats": {"out": "w"}, "ladders": {"down": (0.75, 0.35)}}}),
    ("MtBatok_East_1F", "MAPSEC_MT_BATOK", "cave", (40, 32), "Mt. Batok east 1F (to Route 307).", "MUS_MT_PYRE", UNDER, {"floor": {"mats": {"out": "e"}, "ladders": {"up": (0.25, 0.3)}}}),
    # Challenger's Trail (Victory Road): a mountain climb, Challenger Gate -> Pokemon League
    ("ChallengersTrail_1F", "MAPSEC_CHALLENGERS_TRAIL", "cave", (48, 44), "Challenger's Trail 1F: the final test before the Pokémon League.", "MUS_VICTORY_ROAD", UNDER, {"floor": {"mats": {"gate": "w", "cliffs": "e"}}}),
    ("ChallengersTrail_Cliffs", "MAPSEC_CHALLENGERS_TRAIL", "rocky", (40, 40), "Challenger's Trail: the open cliffs halfway up.", "MUS_VICTORY_ROAD", ROUTE, {"mouths": {"low": "S", "high": "N"}, "closed": True}),
    ("ChallengersTrail_2F", "MAPSEC_CHALLENGERS_TRAIL", "cave", (46, 40), "Challenger's Trail 2F.", "MUS_VICTORY_ROAD", UNDER, {"floor": {"mats": {"cliffs": "w"}, "ladders": {"up": (0.8, 0.25)}}}),
    ("ChallengersTrail_3F", "MAPSEC_CHALLENGERS_TRAIL", "cave", (46, 40), "Challenger's Trail 3F: the summit is near.", "MUS_VICTORY_ROAD", UNDER, {"floor": {"mats": {"league": "e"}, "ladders": {"down": (0.2, 0.25)}}}),
]
# warp links (map, key) <-> (map, key): both ends point at each other
LINKS = [
    (("Route302", "mouth:batok"), ("MtBatok_1F", "mat:out")),
    (("MtBatok_1F", "ladder:up"), ("MtBatok_2F", "ladder:down")),
    (("MtBatok_2F", "ladder:up"), ("MtBatok_3F", "ladder:down")),
    (("MtBatok_3F", "mat:out"), ("FaberTown", "mouth:batok_w")),
    (("FaberTown", "mouth:batok_e"), ("MtBatok_East_2F", "mat:out")),
    (("MtBatok_East_2F", "ladder:down"), ("MtBatok_East_1F", "ladder:up")),
    (("MtBatok_East_1F", "mat:out"), ("Route307", "mouth:batok")),
    (("Route311_West", "mouth:damp"), ("DampPath", "mat:w")),
    (("DampPath", "mat:e"), ("Route311_East", "mouth:damp")),
    (("ChallengerGate", "mouth:trail"), ("ChallengersTrail_1F", "mat:gate")),
    (("ChallengersTrail_1F", "mat:cliffs"), ("ChallengersTrail_Cliffs", "mouth:low")),
    (("ChallengersTrail_Cliffs", "mouth:high"), ("ChallengersTrail_2F", "mat:cliffs")),
    (("ChallengersTrail_2F", "ladder:up"), ("ChallengersTrail_3F", "ladder:down")),
    (("ChallengersTrail_3F", "mat:league"), ("PokemonLeague", "mouth:trail")),
]


# ---------------------------------------------------------------- helpers
def snake(name):
    return re.sub(r"(?<=[a-z])(?=[A-Z])", "_", name).upper()   # MtBatok_1F -> MT_BATOK_1F


def read_bin(path):
    d = open(path, "rb").read()
    return list(struct.unpack(f"<{len(d) // 2}H", d))


def write_bin(path, vals):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "wb").write(struct.pack(f"<{len(vals)}H", *vals))


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def load_layouts():
    return {l["id"]: l for l in json.load(open(P("data", "layouts", "layouts.json")))["layouts"]}


def block_from(map_name, x, y, w, h):
    """Block values of a w x h rectangle of an existing map's layout."""
    lay = load_layouts()[json.load(open(P("data", "maps", map_name, "map.json")))["layout"]]
    v = read_bin(P(lay["blockdata_filepath"]))
    W = lay["width"]
    return [[v[(y + j) * W + x + i] for i in range(w)] for j in range(h)]


def region_cells():
    tags = json.load(open(P("dev_scripts", "region_map_tagger", "tags.json")))
    by_id = {a["key"]: a["id"] for a in tags["areas"]}
    return {(x, y): by_id.get(k, k) for y, row in enumerate(tags["grid"]) for x, k in enumerate(row) if k}


def openings(cells, grid, w, h):
    xs, ys = [c[0] for c in cells], [c[1] for c in cells]
    x0, y0, bw, bh = min(xs), min(ys), max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
    me, out = set(cells), {}
    for (cx, cy) in cells:
        for side, (dx, dy) in (("N", (0, -1)), ("S", (0, 1)), ("W", (-1, 0)), ("E", (1, 0))):
            n = (cx + dx, cy + dy)
            if n in me or n not in grid:
                continue
            pos = int((cx - x0 + 0.5) / bw * w) if side in "NS" else int((cy - y0 + 0.5) / bh * h)
            out.setdefault(side, []).append(pos & ~1)
    return out


class Canvas:
    def __init__(self, w, h, fill):
        self.w, self.h = w, h
        self.t = [[fill] * w for _ in range(h)]
        self.raw = {}
        self.warps = OrderedDict()                       # key -> (x, y, elevation)

    def ok(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h

    def set(self, x, y, v):
        if self.ok(x, y) and (x, y) not in self.raw:
            self.t[y][x] = v

    def rect(self, x0, y0, x1, y1, v):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.set(x, y, v)

    def blob(self, rnd, cx, cy, r, v, keep=()):
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r + rnd.randint(-r, r) and self.ok(x, y) \
                        and self.t[y][x] not in keep:
                    self.set(x, y, v)

    def stamp(self, x0, y0, rows):
        for j, row in enumerate(rows):
            for i, v in enumerate(row):
                if self.ok(x0 + i, y0 + j):
                    self.raw[(x0 + i, y0 + j)] = v

    def path(self, a, b, code="P"):
        (ax, ay), (bx, by) = a, b
        for x in range(min(ax, bx), max(ax, bx) + 2):
            self.set(x, ay, code); self.set(x, ay + 1, code)
        for y in range(min(ay, by), max(ay, by) + 2):
            self.set(bx, y, code); self.set(bx + 1, y, code)


def render(cv, theme):
    def tree_block(bx, by):
        x, y = bx * 2, by * 2
        return all(cv.ok(x + i, y + j) and cv.t[y + j][x + i] == "X" for i in (0, 1) for j in (0, 1))
    code = {"G": GRASS, "T": TALL, "P": PATH, "S": SAND, "W": SEA, "N": SIGN, "F": CAVE_FLOOR, "C": CAVE_WALL,
            "L": CAVE_LADDER, "M": CAVE_MAT, "V": T_VOID, "K": T_TRACK, "B": T_WALLBASE, "Q": T_WALL}
    out = []
    for y in range(cv.h):
        for x in range(cv.w):
            if (x, y) in cv.raw:
                out.append(cv.raw[(x, y)]); continue
            c = cv.t[y][x]
            if c == "X":
                bx, by = x // 2, y // 2
                if tree_block(bx, by):
                    out.append(TREE_STACK[x % 2] if y % 2 and tree_block(bx, by + 1) else TREE[(x % 2, y % 2)])
                    continue
                c = "G"
            if c == "C":                                     # cave wall: raised rock, bumpy face on its lower edge
                out.append(CAVE_FACE if y + 1 >= cv.h or cv.t[y + 1][x] != "C" else CAVE_WALL); continue
            if c == "R":                                     # rock: top face where nothing rocky is above
                out.append(ROCK_TOP if y == 0 or cv.t[y - 1][x] != "R" else ROCK_FACE); continue
            if c == "A":                                     # station paving, offset bricks by row
                out.append(T_PAVE_A if y % 2 == 0 else T_PAVE_B); continue
            out.append(code[c])
    return out


def trees_where(cv, pred, code="X"):
    for by in range(cv.h // 2):
        for bx in range(cv.w // 2):
            if pred(bx, by):
                cv.rect(bx * 2, by * 2, bx * 2 + 1, by * 2 + 1, code)


# ---------------------------------------------------------------- one map
def build(name, theme, w, h, opens, extras, station_door, blocks):
    rnd = random.Random(name)
    cave, sea, tunnel, rocky = theme == "cave", theme == "sea", theme == "tunnel", theme == "rocky"
    base = {"cave": "F", "sea": "W", "tunnel": "V", "rocky": "P"}.get(theme, "G")
    cv = Canvas(w, h, base)
    cx, cy = (w // 2) & ~1, (h // 2) & ~1
    hub = (cx, cy)
    if sea:
        for _ in range(max(1, w * h // 900)):
            cv.blob(rnd, rnd.randrange(4, w - 4), rnd.randrange(4, h - 4), rnd.randint(1, 3), "S")
        cv.set(cx, cy, "S")
        return cv, hub
    if tunnel:                                           # maintenance walkways between track runs
        for y in range(3, h - 3, 7):
            cv.rect(2, y, w - 3, y, "Q"); cv.rect(2, y + 1, w - 3, y + 1, "B"); cv.rect(2, y + 2, w - 3, y + 2, "K")
            cv.rect(2, y + 3, w - 3, y + 4, "A")
        for x in range(4, w - 4, 12):                    # cross passages
            cv.rect(x, 3, x + 1, h - 4, "A")
        cv.rect(cx - 1, cy - 1, cx + 2, cy + 2, "A")
        return cv, hub
    wall = {"cave": "C", "rocky": "R"}.get(theme, "X")
    closed = extras.get("closed")
    gap = set()
    if not closed:
        for side, poss in opens.items():
            for pos in poss:
                for k in range(-2, 4):
                    gap.add((side, pos + k))
    for by in range(h // 2):
        for bx in range(w // 2):
            edge = [e for cond, e in ((by == 0, ("N", bx * 2)), (by == h // 2 - 1, ("S", bx * 2)),
                                     (bx == 0, ("W", by * 2)), (bx == w // 2 - 1, ("E", by * 2))) if cond]
            if edge and (cave or not any(e in gap for e in edge)):
                cv.rect(bx * 2, by * 2, bx * 2 + 1, by * 2 + 1, wall)
    if station_door is not None:
        hub = (station_door[0], max(cy, station_door[1] + 3))
    if not cave and not closed:
        for side, poss in opens.items():
            for pos in poss:
                start = {"N": (pos, 0), "S": (pos, h - 2), "W": (0, pos), "E": (w - 2, pos)}[side]
                cv.path(start, hub, "S" if rocky else "P") if side in "WE" else cv.path(hub, start, "S" if rocky else "P")
    keep = ("P", "X", "C", "R", "S")
    if theme in ("route", "reserve", "marsh", "forest"):
        n = {"route": w * h // 120, "reserve": w * h // 90, "marsh": w * h // 160, "forest": w * h // 140}[theme]
        for _ in range(int(n * extras.get("tall", 1))):
            cv.blob(rnd, rnd.randrange(3, w - 3), rnd.randrange(3, h - 3), rnd.randint(2, 4), "T", keep)
    clumps = {"reserve": w * h // 260, "forest": w * h // 50, "route": w * h // 400}.get(theme, extras.get("trees", 0))
    if clumps:
        spots = [(rnd.randrange(1, w // 2 - 1), rnd.randrange(1, h // 2 - 1)) for _ in range(clumps)]
        rad = 1 if theme == "forest" else 0
        trees_where(cv, lambda bx, by: any(abs(bx - sx) + abs(by - sy) <= rad for sx, sy in spots)
                    and all(cv.t[by * 2 + j][bx * 2 + i] not in ("P", "S") for i in (0, 1) for j in (0, 1)))
    if rocky:                                            # rock outcrops (2x2) and a little grass
        for _ in range(w * h // 70):
            bx, by = rnd.randrange(2, w // 2 - 2), rnd.randrange(2, h // 2 - 2)
            if all(cv.t[by * 2 + j][bx * 2 + i] == "P" for i in (0, 1) for j in (0, 1)) and \
                    (abs(bx * 2 - hub[0]) > 4 or abs(by * 2 - hub[1]) > 4):
                cv.rect(bx * 2, by * 2, bx * 2 + 1, by * 2 + 1, "R")
        for _ in range(w * h // 300):
            cv.blob(rnd, rnd.randrange(3, w - 3), rnd.randrange(3, h - 3), 2, "G", ("R", "S"))
    if theme in ("reserve", "marsh"):
        for _ in range(max(1, w * h // (300 if theme == "marsh" else 900))):
            cv.blob(rnd, rnd.randrange(5, w - 5), rnd.randrange(5, h - 5), rnd.randint(2, 4), "W", keep)
    if theme == "coast":
        side = extras["coast"]
        band = 6 if side in "NS" else 5
        for y in range(h):
            for x in range(w):
                d = {"S": h - 1 - y, "N": y, "W": x, "E": w - 1 - x}[side]
                if d < band:
                    cv.set(x, y, "W")
                elif d < band + 3:
                    cv.set(x, y, "S")
    if theme == "falls":
        for y in range(2, h - 2):
            cv.rect(cx - 3, y, cx + 2, y, "W"); cv.set(cx - 4, y, "S"); cv.set(cx + 3, y, "S")
        cv.blob(rnd, cx, 6, 6, "W", ("X",))
    if cave:
        for _ in range(w * h // 120):
            bx, by = rnd.randrange(2, w // 2 - 2), rnd.randrange(2, h // 2 - 2)
            if abs(bx * 2 - cx) > 3 or abs(by * 2 - cy) > 3:
                cv.rect(bx * 2, by * 2, bx * 2 + 1, by * 2 + 1, "C")
        fl = extras.get("floor", {})
        for key, hint in fl.get("mats", {}).items():     # exit mats on the bottom wall
            mx = {"w": 6, "e": w - 7, "c": cx}[hint]
            cv.rect(mx - 2, h - 6, mx + 2, h - 3, "F")
            cv.set(mx, h - 2, "M")
            cv.warps["mat:" + key] = (mx, h - 2, 3)
            cv.path((mx, h - 4), (cx, cy), "F")
        for key, (fx, fy) in fl.get("ladders", {}).items():
            lx, ly = int(fx * (w - 8)) + 4, int(fy * (h - 8)) + 4
            cv.rect(lx - 2, ly - 2, lx + 2, ly + 2, "F")
            cv.set(lx, ly, "L")
            cv.warps["ladder:" + key] = (lx, ly, 3)
            cv.path((lx, ly + 1), (cx, cy), "F")
    # cave mouths (outdoor) and buildings
    for key, side in extras.get("mouths", {}).items():
        mx, my = {"N": (cx + 4, 5), "S": (cx - 6, h - 5), "W": (5, cy - 4), "E": (w - 6, cy - 4)}[side]
        cv.rect(mx - 3, my - 4, mx + 3, my + 2, "S" if rocky else "P")
        cv.stamp(mx - 1, my - 3, MOUTH)
        cv.warps["mouth:" + key] = (mx, my, 0)
        cv.path((mx, my + 1), hub, "S" if rocky else "P")
    return cv, hub


def place_building(cv, rows, door_off, at, key, signs_off=()):
    x0, y0 = at[0] - door_off[0], at[1] - door_off[1]
    cv.rect(x0 - 1, y0 - 1, x0 + len(rows[0]), y0 + len(rows) + 1, "P" if cv.t[at[1]][at[0]] != "S" else "S")
    cv.stamp(x0, y0, rows)
    cv.warps[key] = (at[0], at[1], 0)
    return [(at[0] + dx, at[1] + dy) for dx, dy in signs_off]


def place_sign(cv, hub, under):
    x, y = hub[0] + 3, hub[1] + 2
    cv.rect(x - 1, y - 1, x + 1, y + 1, under)
    if under not in ("F", "A"):
        cv.set(x, y, "N")
    return x, y


# ---------------------------------------------------------------- interiors
def clone_centre(town, const, mapsec):
    folder = town + "_PokemonCenter_1F"
    m = json.load(open(P("data", "maps", "TelokTown_PokemonCenter_1F", "map.json")), object_pairs_hook=OrderedDict)
    nurse = "LOCALID_%s_NURSE" % const
    keep = []
    for o in m["object_events"]:
        if o.get("local_id", "").endswith("_NURSE"):
            keep.append(OrderedDict(o, local_id=nurse, script="%s_EventScript_Nurse" % folder))
        elif o.get("script") == "Common_EventScript_OrchidCafe":
            keep.append(o)
    m.update(id="MAP_%s_POKEMON_CENTER_1F" % const, name=folder, region_map_section=mapsec, object_events=keep,
             warp_events=[OrderedDict(wv, dest_map="MAP_" + const, dest_warp_id="X")
                          for wv in m["warp_events"] if wv["dest_map"] == "MAP_OLDALE_TOWN"])
    pory = "\n".join([
        "raw `", "%s_MapScripts::" % folder,
        "\tmap_script MAP_SCRIPT_ON_TRANSITION, %s_OnTransition" % folder,
        "\tmap_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume", "\t.byte 0", "",
        "%s_OnTransition:" % folder, "\tsetrespawn HEAL_LOCATION_%s" % const, "\tend", "",
        "%s_EventScript_Nurse::" % folder, "\tsetvar VAR_0x800B, %s" % nurse,
        "\tcall Common_EventScript_PkmnCenterNurse", "\twaitmessage", "\twaitbuttonpress", "\trelease", "\tend", "`", ""])
    return folder, m, pory, nurse


def clone_mart(town, const, mapsec):
    folder = town + "_Mart"
    m = json.load(open(P("data", "maps", "TelokTown_Mart", "map.json")), object_pairs_hook=OrderedDict)
    clerk = [OrderedDict((k, v) for k, v in o.items() if k != "local_id") for o in m["object_events"]
             if o.get("script", "").endswith("_Clerk")]
    m.update(id="MAP_%s_MART" % const, name=folder, region_map_section=mapsec, object_events=clerk,
             warp_events=[OrderedDict(wv, dest_map="MAP_" + const, dest_warp_id="X") for wv in m["warp_events"]])
    return folder, m, "mapscripts %s_MapScripts {}\n" % folder


def clone_hawker(town, const, mapsec):
    folder = town + "_HawkerCentre"
    m = json.load(open(P("data", "maps", "HawkerCentreTest", "map.json")), object_pairs_hook=OrderedDict)
    m.update(id="MAP_%s_HAWKER_CENTRE" % const, name=folder, region_map_section=mapsec,
             warp_events=[OrderedDict(wv, dest_map="MAP_" + const, dest_warp_id="X") for wv in m["warp_events"]])
    return folder, m, "mapscripts %s_MapScripts {}\n" % folder


# ---------------------------------------------------------------- main
CURRENT = [None]


def main():
    grid = region_cells()
    centre_blk = block_from("SlateportCity", 18, 16, 4, 4)       # door (1, 2); signs right of the door, a row down
    mart_blk = block_from("SlateportCity", 12, 23, 4, 4)         # door (1, 3); signs right of the door
    house_blk = block_from("PetalburgCity", 5, 2, 5, 4)          # Wally's house, door (2, 3)
    station_blk = block_from("TosaPort", 8, 2, 7, 6)             # gatehouse, door (3, 5)
    cobbles = block_from("TosaPort", 10, 8, 2, 1)[0]
    lj_path = P("data", "layouts", "layouts.json")
    lj = json.load(open(lj_path), object_pairs_hook=OrderedDict)
    layouts = OrderedDict((l["id"], l) for l in lj["layouts"])
    mg_path = P("data", "maps", "map_groups.json")
    mg = json.load(open(mg_path), object_pairs_hook=OrderedDict)
    group = list(mg.get(GROUP, []))
    heal_path = P("src", "data", "heal_locations.json")
    heal = json.load(open(heal_path), object_pairs_hook=OrderedDict)
    maps, pending, made, upgraded, skipped = {}, {}, [], [], []

    for name, mapsec, theme, (w, h), text, music, mtype, extras in PLACES:
        CURRENT[0] = name
        assert w % 2 == 0 and h % 2 == 0 and (w + 15) * (h + 14) <= MAX_MAP_DATA, name
        mpath = P("data", "maps", name, "map.json")
        station = os.path.exists(mpath)
        if station:
            m = json.load(open(mpath), object_pairs_hook=OrderedDict)
            lay = layouts[m["layout"]]
            if not (lay["width"] == 15 and lay["height"] == 12 and len(m["warp_events"]) == 1):
                skipped.append(name)
                continue
        cells = extras.get("cells") or [c for c, s in grid.items() if s == mapsec]
        opens = openings(cells, grid, w, h) if cells else {}
        for side in extras.get("mouths", {}).values():   # a cave mouth replaces that side's opening
            opens.pop(side, None)
        door = None
        if station:
            dx = (w // 2) & ~1
            for pos in opens.get("N", []):
                if abs(pos - dx) < 7:
                    dx = pos + 10 if pos + 14 < w else pos - 10
            door = (dx, 7)
        cv, hub = build(name, theme, w, h, opens, extras, door, None)
        signs = []
        if station:                                      # station building first: warp 0
            cv.stamp(door[0] - 3, 2, station_blk)
            cv.raw[(door[0] - 1, door[1] + 1)], cv.raw[(door[0], door[1] + 1)] = cobbles
            cv.path((door[0], door[1] + 2), hub)
            cv.warps = OrderedDict([("station", (door[0], door[1], 0))] + list(cv.warps.items()))
        clamp = lambda v, lo, hi: max(lo, min(hi, v))
        bottom = h - (12 if extras.get("coast") == "S" else 5)   # stay above the sand / sea band
        row = clamp(hub[1] + 6, (door[1] + 6) if station else 6, bottom)
        cxl = clamp(hub[0] - 7, 4 if extras.get("coast") != "W" else 11, w - 14)
        cxr = clamp(hub[0] + 6, cxl + 8, w - 6)
        if extras.get("centre"):
            signs += place_building(cv, centre_blk, (1, 2), (cxl, row), "centre", ((1, 1), (2, 1)))
            cv.path((cxl, row + 2), hub)
        if extras.get("mart"):
            signs += place_building(cv, mart_blk, (1, 3), (cxr, row), "mart", ((1, 0), (2, 0)))
            cv.path((cxr, row + 1), hub)
        if extras.get("hawker"):
            hx, hy = (w - 8, clamp(hub[1] - 2, 7, bottom))
            place_building(cv, house_blk, (2, 3), (hx, hy), "hawker")
            cv.path((hx, hy + 1), hub)
        if theme == "house":
            cv.stamp(hub[0] - 2, hub[1] - 4, block_from("TosaPort", 4, 9, 4, 4))
        tiles = {"cave": CAVE, "sea": SEA_TS, "tunnel": TUNNEL, "rocky": ROCKY}.get(theme, OUTDOOR)
        under = {"cave": "F", "tunnel": "A", "rocky": "P"}.get(theme, "G")
        sign = None if theme == "sea" else place_sign(cv, hub, under)
        lid = m["layout"] if station else "LAYOUT_" + snake(name)
        write_bin(P("data", "layouts", name, "map.bin"), render(cv, theme))
        write_bin(P("data", "layouts", name, "border.bin"), tiles[2])
        layouts[lid] = OrderedDict([("id", lid), ("name", name + "_Layout"), ("width", w), ("height", h),
                                    ("primary_tileset", tiles[0]), ("secondary_tileset", tiles[1]),
                                    ("border_filepath", f"data/layouts/{name}/border.bin"),
                                    ("blockdata_filepath", f"data/layouts/{name}/map.bin"),
                                    ("layout_version", "emerald")])
        bg = []
        if sign:
            bg.append(OrderedDict([("type", "sign"), ("x", sign[0]), ("y", sign[1]), ("elevation", 0),
                                   ("player_facing_dir", "BG_EVENT_PLAYER_FACING_ANY"),
                                   ("script", name + "_EventScript_PlaceholderSign")]))
        for i, (sx, sy) in enumerate(signs):
            bg.append(OrderedDict([("type", "sign"), ("x", sx), ("y", sy), ("elevation", 0),
                                   ("player_facing_dir", "BG_EVENT_PLAYER_FACING_NORTH"),
                                   ("script", "Common_EventScript_ShowPokemonCenterSign" if i < 2 and extras.get("centre")
                                    else "Common_EventScript_ShowPokemartSign")]))
        if station:
            m["map_type"] = mtype
            upgraded.append(name)
        else:
            outdoor = theme not in ("cave", "tunnel")
            m = OrderedDict([
                ("id", "MAP_" + snake(name)), ("name", name), ("layout", lid), ("music", music),
                ("region", "REGION_HOENN"), ("region_map_section", mapsec), ("requires_flash", False),
                ("weather", "WEATHER_SUNNY" if outdoor else "WEATHER_NONE"), ("map_type", mtype),
                ("allow_cycling", True), ("allow_escaping", not outdoor), ("allow_running", True),
                ("show_map_name", True), ("battle_scene", "MAP_BATTLE_SCENE_NORMAL"), ("connections", None),
                ("object_events", []), ("warp_events", []), ("coord_events", []), ("bg_events", [])])
            made.append(name)
            if name not in group:
                group.append(name)
        m["bg_events"] = bg
        keep_station = m["warp_events"][:1] if station else []
        m["warp_events"] = keep_station + [OrderedDict([("x", x), ("y", y), ("elevation", e), ("dest_map", "X"),
                                                        ("dest_warp_id", "X")])
                                           for k, (x, y, e) in list(cv.warps.items())[1 if station else 0:]]
        maps[name] = (m, list(cv.warps.keys()))
        pory = "mapscripts %s_MapScripts {}\n" % name
        if sign:
            pory += '\nscript %s_EventScript_PlaceholderSign {\n    msgbox(format("%s Placeholder map."), MSGBOX_SIGN)\n}\n' % (
                name, text.replace('"', "'"))
        pending[name] = pory
        # interiors for Centre / Mart / hawker centre
        const = snake(name)
        for key, fn in (("centre", clone_centre), ("mart", clone_mart), ("hawker", clone_hawker)):
            if key not in cv.warps:
                continue
            res = fn(name, const, mapsec)
            folder, im, ipory = res[0], res[1], res[2]
            idx = list(cv.warps.keys()).index(key)
            for wv in im["warp_events"]:
                wv["dest_warp_id"] = str(idx)
            m["warp_events"][idx].update(dest_map=im["id"], dest_warp_id="0")
            maps[folder] = (im, None)
            pending[folder] = ipory
            if folder not in group:
                group.append(folder)
            if key == "centre":
                hx, hy = cv.warps["centre"][:2]
                hid = "HEAL_LOCATION_" + const
                heal["heal_locations"] = [e for e in heal["heal_locations"] if e["id"] != hid] + [OrderedDict([
                    ("id", hid), ("map", "MAP_" + const), ("x", hx), ("y", hy + 1),
                    ("respawn_map", im["id"]), ("respawn_npc", res[3])])]

    # links
    for (ma, ka), (mb, kb) in LINKS:
        if ma not in maps or mb not in maps:
            continue                                     # one end was edited by hand: leave both alone
        (A, akeys), (B, bkeys) = maps[ma], maps[mb]
        ia, ib = akeys.index(ka), bkeys.index(kb)
        A["warp_events"][ia].update(dest_map=B["id"], dest_warp_id=str(ib))
        B["warp_events"][ib].update(dest_map=A["id"], dest_warp_id=str(ia))
    for name, (m, _) in maps.items():
        bad = [w for w in m["warp_events"] if w["dest_map"] == "X" or w["dest_warp_id"] == "X"]
        assert not bad, "%s: unlinked warps %s" % (name, bad)
        write_json(P("data", "maps", name, "map.json"), m)
        pory = P("data", "maps", name, "scripts.pory")
        stock = "mapscripts %s_MapScripts {}\n" % name
        if not os.path.exists(pory) or open(pory).read() == stock or name in made or name in upgraded \
                or name not in [p[0] for p in PLACES]:
            open(pory, "w").write(pending[name])
            stale = P("data", "maps", name, "scripts.inc")
            if os.path.exists(stale):                    # same-second mtime would fool make
                os.remove(stale)

    lj["layouts"] = list(layouts.values())
    write_json(lj_path, lj)
    if GROUP not in mg["group_order"]:
        mg["group_order"].insert(mg["group_order"].index("gMapGroup_TosaRail") + 1, GROUP)
    mg[GROUP] = group
    write_json(mg_path, mg)
    with open(heal_path, "w") as f:
        json.dump(heal, f, indent=2, ensure_ascii=False)
        f.write("\n")
    es_path = P("data", "event_scripts.s")
    es = open(es_path).read()
    anchor = '\t.include "data/maps/TrainTestNorth/scripts.inc"\n'
    add = "".join('\t.include "data/maps/%s/scripts.inc"\n' % m for m in group if ('data/maps/%s/scripts.inc' % m) not in es)
    open(es_path, "w").write(es.replace(anchor, anchor + add))
    print("created %d, enlarged %d station exteriors, interiors %d, skipped (edited) %s"
          % (len(made), len(upgraded), len([g for g in group if g not in made]), skipped))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("while building", CURRENT[0])
        raise
