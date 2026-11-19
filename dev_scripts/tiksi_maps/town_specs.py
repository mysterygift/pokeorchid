"""
Tiksi town mockups (round 1 design review). Each town only uses metatiles copied from existing layouts
that share its tileset pair (compose.py enforces this), so no tileset changes.

Lore: TODO.md (repo root) + region map tagger notes (tags_tiksi.json). Tiksi is "a rural harsh region
with rugged people who look after it"; the player arrives on a Team Torrent smuggling ship.

usage: town_specs.py <out_dir>
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import compose  # noqa: E402

DEW = "LAYOUT_DEWFORD_TOWN"

# ---------------------------------------------------------------- Furong Village
# "A fishing village near the route the player lands on when they make the trip to Tiksi in search of
# Matt" / "land in a small fishing village on Tiksi" (via one of Team Torrent's smuggling ships).
# Tileset gTileset_Dewford (shared: Dewford Town, Routes 105-107, Birth / Navel Rock exteriors).
# East = the sea (Furong sits on the inlet on the Tiksi map); exits west (Route 401) and north (Route 407).
FURONG = dict(
    name="Furong Village", slug="furong_village", size=(26, 20),
    tileset=("gTileset_General", "gTileset_Dewford"),
    ground=(DEW, 6, 12),
    legend={
        "w": (DEW, 12, 2),     # sea
        "e": (DEW, 11, 2),     # shore: sand | sea
        "R": (DEW, 14, 18),    # coastal scrub bush
        "g": (DEW, 0, 15),     # grass tuft under trees
    },
    # x0-17 land, x18 shoreline, x19-25 open sea (Furong is on the inlet; see the Tiksi map)
    rows=["." * 18 + "e" + "w" * 7] * 6 + [
          "..............R...ewwwwwww",
          "........R.........ewwwwwww",
          "..................ewwwwwww",
          "..................ewwwwwww",
          "..................ewwwwwww",
          "..................ewwwwwww",
          "....R.............ewwwwwww",
          ".................Rewwwwwww",
          "..................ewwwwwww",
          "......R...........ewwwwwww",
          "..............R...ewwwwwww",
          "..................ewwwwwww",
          "......RR.....R....ewwwwwww",
          "......RR.....R....ewwwwwww"],
    stamps=[
        # north treeline (Dewford forest block) with a gap at x8-10 for Route 407
        (DEW, 14, 0, 6, 2, 0, 0), (DEW, 14, 0, 2, 2, 6, 0), (DEW, 14, 0, 6, 2, 11, 0), (DEW, 14, 0, 1, 2, 17, 0),
        # west treeline, gap at y9-11 for Route 401
        (DEW, 14, 0, 2, 6, 0, 2), (DEW, 14, 0, 2, 1, 0, 8), (DEW, 14, 0, 2, 6, 0, 12),
        # south: scrubby treeline broken by boulders
        (DEW, 14, 0, 6, 2, 0, 18), (DEW, 14, 0, 5, 2, 8, 18), (DEW, 14, 0, 4, 2, 14, 18),
        # the landing jetty: Dewford's dock, doubled to reach deep water
        (DEW, 11, 9, 3, 2, 18, 11), (DEW, 12, 9, 2, 2, 21, 11), (DEW, 12, 9, 2, 2, 23, 11),
        # sea rocks off the point (Route 106 shares gTileset_Dewford)
        ("LAYOUT_ROUTE106", 8, 0, 4, 5, 20, 2), ("LAYOUT_ROUTE106", 5, 2, 2, 2, 23, 16),
        ("LAYOUT_ROUTE106", 8, 5, 2, 2, 20, 15),
        # Pokémon Centre
        (DEW, 1, 7, 4, 4, 3, 4),
        # fishers' huts
        (DEW, 7, 5, 4, 4, 10, 3), (DEW, 16, 11, 4, 4, 10, 12),
    ],
    marks=[(4, 7, "door", "warp"), (4, 9, "lands", "land"), (9, 0, "R407", "warp"), (0, 10, "R401", "warp"),
           (24, 11, "boat", "npc"), (17, 11, "", "sign")],
    notes="Rough landing village: sand, boulders, two fishers' huts, the Centre, and a jetty on the inlet where "
          "the smugglers' boat ties up. No Mart, no gym.",
)

LAV = "LAYOUT_LAVARIDGE_TOWN"
JAG = "LAYOUT_JAGGED_PASS"

# ---------------------------------------------------------------- Drake Base Camp
# Last stop before Mt. Drake: Regidrago at the peak, Registeel's Ferrum Shrine at its core, the finale vs
# Matt on top (TODO.md). No tagger note. Tileset gTileset_Lavaridge (shared by 14 maps: Lavaridge Town,
# Route 112, Mt. Chimney, Jagged Pass, Fiery Path, Magma Hideout...). The north band is Jagged Pass's lower
# slope: the trail up Mt. Drake. Exits: north = Mt. Drake trail, south = Route 402.
DRAKE = dict(
    name="Drake Base Camp", slug="drake_base_camp", size=(30, 24),
    tileset=("gTileset_General", "gTileset_Lavaridge"),
    ground=(LAV, 6, 18),
    legend={},
    rows=[],
    stamps=[
        # Mt. Drake: Jagged Pass's lower slope, trail up the middle
        (JAG, 0, 27, 30, 10, 0, 0),
        # camp buildings (Lavaridge): Pokémon Centre, supply Mart, two lodges
        (LAV, 8, 3, 4, 4, 5, 13), (LAV, 14, 2, 4, 4, 21, 13),
        (LAV, 11, 11, 4, 5, 10, 17), (LAV, 15, 11, 4, 5, 16, 17),
        # tall grass patches (Route 112 shares gTileset_Lavaridge)
        ("LAYOUT_ROUTE112", 26, 44, 4, 2, 3, 20), ("LAYOUT_ROUTE112", 26, 44, 4, 2, 22, 20),
        ("LAYOUT_ROUTE112", 26, 44, 3, 2, 12, 11), ("LAYOUT_ROUTE112", 26, 44, 3, 2, 18, 11),
        # side treelines (Jagged Pass foot)
        (JAG, 0, 38, 3, 8, 0, 10), (JAG, 0, 38, 3, 6, 0, 18), (JAG, 26, 38, 4, 8, 26, 10), (JAG, 26, 38, 4, 6, 26, 18),
    ],
    marks=[(15, 0, "Mt.Drake", "warp"), (6, 15, "door", "warp"), (6, 17, "lands", "land"), (14, 23, "R402", "warp")],
    notes="Climbers' camp at the foot of Mt. Drake: the trail starts at the top of the map. Centre, a supply "
          "Mart and two lodges for climbers. No gym.",
)

RUS = "LAYOUT_RUSTBORO_CITY"

# ---------------------------------------------------------------- Ube City
# "The Tiksi Region's only city. Home to the Silph Co.'s Tiksi branch" (tagger) + "Silph Co. Office: a
# remote sales office for Kanto's famous Silph Co. They've been struggling to break into the Tosa market"
# (TODO.md). Only city of a rural region -> a modest square, not a metropolis; Silph = a small office.
# Tileset gTileset_Rustboro (shared by 9 maps: Rustboro, Routes 104/116, Petalburg Woods, Southern Island...).
# Exits: north (Route 405) and east (Route 407).
UBE = dict(
    name="Ube City", slug="ube_city", size=(32, 28),
    tileset=("gTileset_General", "gTileset_Rustboro"),
    ground=(RUS, 14, 36),
    legend={"r": (RUS, 13, 40)},       # street paving
    # streets: north exit down to the fountain, fountain east to the exit
    rows=["." * 15 + "rr" + "." * 15] * 12 + ["." * 15 + "r" * 17] * 2 + ["." * 15 + "rr" + "." * 15] * 3,
    stamps=[
        # tree borders (Rustboro's own), gaps for the north and east exits
        (RUS, 11, 0, 6, 2, 0, 0), (RUS, 11, 0, 6, 2, 6, 0), (RUS, 11, 0, 3, 2, 12, 0),
        (RUS, 11, 0, 6, 2, 18, 0), (RUS, 11, 0, 6, 2, 24, 0), (RUS, 11, 0, 2, 2, 30, 0),
        (RUS, 37, 12, 2, 10, 0, 2), (RUS, 37, 12, 2, 10, 0, 12), (RUS, 37, 12, 2, 6, 0, 22),
        (RUS, 37, 12, 2, 10, 30, 2), (RUS, 37, 12, 2, 10, 30, 14), (RUS, 37, 12, 2, 4, 30, 24),
        (RUS, 11, 0, 6, 2, 2, 26), (RUS, 11, 0, 6, 2, 8, 26), (RUS, 11, 0, 6, 2, 14, 26),
        (RUS, 11, 0, 6, 2, 20, 26), (RUS, 11, 0, 4, 2, 26, 26),
        # Silph Co. Tiksi sales office: a modest two-storey block on the square
        (RUS, 24, 42, 6, 5, 18, 3),
        # Pokémon Centre and Mart facing the square
        (RUS, 15, 35, 4, 4, 5, 5), (RUS, 15, 42, 4, 4, 10, 5),
        # fountain in the square, lamps around it
        (RUS, 27, 38, 3, 3, 14, 13), (RUS, 19, 23, 1, 2, 12, 12), (RUS, 19, 23, 1, 2, 18, 12),
        (RUS, 19, 23, 1, 2, 12, 16), (RUS, 19, 23, 1, 2, 18, 16),
        # homes
        (RUS, 7, 34, 5, 5, 3, 19), (RUS, 28, 24, 5, 5, 23, 19), (RUS, 31, 39, 4, 8, 25, 2),
    ],
    marks=[(15, 0, "R405", "warp"), (31, 13, "R407", "warp"), (6, 7, "door", "warp"), (6, 9, "lands", "land"),
           (21, 7, "Silph", "sign")],
    notes="A small square: Centre, Mart, fountain, a couple of homes, and Silph Co.'s modest Tiksi sales office "
          "(not a tower: they're struggling to break in). No gym.",
)

LIL = "LAYOUT_LILYCOVE_CITY"

# ---------------------------------------------------------------- Tanglyn Town
# "A quiet coastal town filled with ancient murals" (tagger; no TODO.md entry). The murals can tie into the
# local myths that foretold the Regis' arrival (TODO.md). Tileset gTileset_Lilycove (shared by 10 maps:
# Lilycove, Routes 121-123, Safari Zone areas): its art museum = the Mural Hall. Exits: west (Route 406),
# south (Route 408).
TANGLYN = dict(
    name="Tanglyn Town", slug="tanglyn_town", size=(33, 28),
    tileset=("gTileset_General", "gTileset_Lilycove"),
    ground=(LIL, 46, 22),
    legend={},
    rows=[],
    stamps=[
        # the shore: Lilycove's east coast from its top edge (bluff, stairs down, beach, rocks, open sea)
        (LIL, 44, 0, 19, 28, 14, 0),
        # Mural Hall (Lilycove's art museum) on the west side of town
        (LIL, 7, 0, 11, 9, 1, 0),
        # Pokémon Centre and a home
        (LIL, 23, 11, 4, 4, 3, 12), (LIL, 10, 19, 4, 4, 8, 18),
        # trees: west edge (gap for Route 406) and south edge (gap for Route 408)
        (LIL, 0, 10, 2, 4, 0, 9), (LIL, 0, 10, 2, 4, 0, 18), (LIL, 0, 10, 2, 4, 0, 22),
        (LIL, 0, 10, 2, 4, 2, 24), (LIL, 0, 10, 2, 4, 4, 24), (LIL, 0, 10, 2, 4, 9, 24), (LIL, 0, 10, 2, 4, 11, 24),
    ],
    # seam: grass over the cut-off Lilycove house at x14 and the sea's west tip
    rows_after=["." * 14 + "_____"] * 2 + ["." * 14 + "_"] * 6,
    marks=[(0, 15, "R406", "warp"), (7, 27, "R408", "warp"), (4, 14, "door", "warp"), (4, 16, "lands", "land"),
           (6, 8, "murals", "sign")],
    notes="A quiet shore town above a rocky beach. Its art museum becomes the Mural Hall, home of the ancient "
          "murals that foretold the Regis' arrival. Centre and two homes. No gym, no Mart.",
)

TOWNS = [FURONG, DRAKE, UBE, TANGLYN]

if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for t in TOWNS:
        compose.mockup(t, os.path.join(out, "town_%s.png" % t["slug"]), scale=2)
        print(t["name"])
