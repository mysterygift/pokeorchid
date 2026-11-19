"""
Sevii Islands region maps (REGION_MAP_SEVII123 / 45 / 67) as they would look in Orchid's MAP v2 screen.
MOCK only.

Art = the FRLG Sevii region maps already in the ROM (graphics/pokenav/region_map/map_sevii_*.png/.bin, the
same files gRegionMapInfos[REGION_MAP_SEVII*] loads). One tilemap edit is proposed: FRLG's baked map-switch
button (bottom right) is replaced by sea (ERASE). Everything else stays FRLG.

Overlays (all as the ROM would draw them in MAP v2):
  * nodes (OBJ discs / diamonds) for towns and single-cell landmarks
  * blue sea-route tubes (BG1, like Tosa's sea routes) for the invented island-to-island straits
  * cursor ring + player head, header "SEVII ISLANDS" + sub-area, tray = place name
The @4x "_cells" sheets show the proposed sRegionMapSections_Sevii* grid: every cell of every section we
build, outlined and labelled; dashed = new strait sections; struck-out = vanilla cells we clear.

usage: <venv python> dev_scripts/voyages/regionmap/sevii.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rm_common as C  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

SEA_C = ((40, 96, 184), (72, 152, 224), (152, 208, 248))     # mock_map.SEA_C (dark, face, light)

# Proposed grids. Vanilla FRLG cells unless noted. Strait sections reuse spare Sevii slots (renamed).
CLUSTERS = {
    "123": dict(
        sub="ISLES 1-3",
        towns={"MAPSEC_ONE_ISLAND": "One Island", "MAPSEC_TWO_ISLAND": "Two Island",
               "MAPSEC_THREE_ISLAND": "Three Island"},
        landmarks={"MAPSEC_MT_EMBER": "Mt. Ember", "MAPSEC_BERRY_FOREST": "Berry Forest"},
        routes={"MAPSEC_KINDLE_ROAD": "Kindle Road", "MAPSEC_TREASURE_BEACH": "Treasure Beach",
                "MAPSEC_CAPE_BRINK": "Cape Brink", "MAPSEC_BOND_BRIDGE": "Bond Bridge",
                "MAPSEC_THREE_ISLE_PORT": "Three Isle Port"},
        # cell moves: (2,3) Kindle Road -> Mt. Ember; (14,12) Bond Bridge -> Berry Forest
        moves={(2, 3): "MAPSEC_MT_EMBER", (14, 12): "MAPSEC_BERRY_FOREST"},
        straits={
            "MAPSEC_SEVII_ISLE_22": ("One-Two Strait", [(2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9)], ("MAPSEC_TREASURE_BEACH", "MAPSEC_TWO_ISLAND")),
            "MAPSEC_SEVII_ISLE_23": ("Two-Three Strait", [(10, 9), (11, 9), (12, 9), (13, 9), (13, 10), (13, 11), (13, 12)], ("MAPSEC_TWO_ISLAND", "MAPSEC_BERRY_FOREST")),
        },
        clear=[],
        cursor="MAPSEC_ONE_ISLAND", visited={"MAPSEC_ONE_ISLAND", "MAPSEC_TWO_ISLAND"},
        # strait ends -> the places they join (for tube end caps)
    ),
    "45": dict(
        sub="ISLES 4-5",
        towns={"MAPSEC_FOUR_ISLAND": "Four Island", "MAPSEC_FIVE_ISLAND": "Five Island"},
        landmarks={},
        routes={"MAPSEC_FIVE_ISLE_MEADOW": "Five Isle Meadow", "MAPSEC_MEMORIAL_PILLAR": "Memorial Pillar"},
        moves={},
        straits={
            "MAPSEC_SEVII_ISLE_24": ("Four-Five Strait", [(4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9), (9, 10), (9, 11), (10, 11), (11, 11), (12, 11), (13, 11), (14, 11), (15, 11)], ("MAPSEC_FOUR_ISLAND", "MAPSEC_FIVE_ISLAND")),
        },
        clear=["MAPSEC_RESORT_GORGEOUS", "MAPSEC_WATER_LABYRINTH", "MAPSEC_NAVEL_ROCK_FRLG"],
        cursor="MAPSEC_FIVE_ISLAND", visited={"MAPSEC_FOUR_ISLAND", "MAPSEC_FIVE_ISLAND"},
    ),
    "67": dict(
        sub="ISLES 6-7",
        towns={"MAPSEC_SIX_ISLAND": "Six Island", "MAPSEC_SEVEN_ISLAND": "Seven Island"},
        landmarks={"MAPSEC_CANYON_ENTRANCE": "Canyon Entrance"},
        routes={"MAPSEC_WATER_PATH": "Water Path", "MAPSEC_RUIN_VALLEY": "Ruin Valley",
                "MAPSEC_SEVAULT_CANYON": "Sevault Canyon", "MAPSEC_TANOBY_RUINS": "Tanoby Ruins"},
        moves={},
        straits={
            "MAPSEC_THREE_ISLE_PATH": ("Six-Seven Strait", [(16, 6), (15, 6), (14, 6), (13, 6), (12, 6), (11, 6), (10, 6), (9, 6), (8, 6), (7, 6), (6, 6), (6, 7)], ("MAPSEC_SIX_ISLAND", "MAPSEC_SEVEN_ISLAND")),
        },
        clear=["MAPSEC_OUTCAST_ISLAND", "MAPSEC_GREEN_PATH", "MAPSEC_TRAINER_TOWER", "MAPSEC_BIRTH_ISLAND_FRLG"],
        cursor="MAPSEC_SIX_ISLAND", visited={"MAPSEC_SIX_ISLAND"},
    ),
}
ERASE_BOX = (20, 12, 23, 15)            # map-cell box (x0, y0, x1, y1) holding FRLG's switch button


def proposed_grid(key, cl):
    rows = C.layout_rows(os.path.join(C.ROOT, "src", "data", "region_map", "region_map_layout_sevii%s.h" % key))
    g = [list(r) for r in rows]
    for y, r in enumerate(g):
        for x, s in enumerate(r):
            if s in cl["clear"]:
                g[y][x] = "MAPSEC_NONE"
    for (x, y), s in cl["moves"].items():
        g[y][x] = s
    for s, (_, cells, _j) in cl["straits"].items():
        for x, y in cells:
            assert g[y][x] == "MAPSEC_NONE", (key, s, x, y, g[y][x])
            g[y][x] = s
    return rows, g


def erased_art(key):
    """FRLG art with the switch button tiles replaced by the sea tile (a 64x64 u8 tilemap edit)."""
    sheet = Image.open(os.path.join(C.RM, "map_sevii_%s.png" % key))
    tm = bytearray(open(os.path.join(C.RM, "map_sevii_%s.bin" % key), "rb").read())
    from collections import Counter
    sea = Counter(tm[y * 64 + x] for y in range(20) for x in range(30)).most_common(1)[0][0]
    changed = []
    bx0, by0, bx1, by1 = ERASE_BOX
    for ty in range(by0 + 2, by1 + 2):                 # cell -> tile: +1 x, +2 y
        for tx in range(bx0 + 1, bx1 + 1):
            if tm[ty * 64 + tx] != sea:
                changed.append((tx, ty, tm[ty * 64 + tx]))
                tm[ty * 64 + tx] = sea
    return C.bg2_from(sheet, bytes(tm)), changed, sea


def tube_layer(cells_list, ends):
    """Sea tube through the cell centres (orthogonal steps), 5 px wide with dark rim, like MAP v2's tubes."""
    im = Image.new("RGBA", (C.W, C.H))
    d = ImageDraw.Draw(im)
    for cells in cells_list:
        pts = [C.cell_ctr(c) for c in cells]
        pts = [ends[cells][0]] + pts + [ends[cells][1]]
        for w, col in ((7, SEA_C[0]), (5, SEA_C[1])):
            d.line(pts, fill=col + (255,), width=w, joint="curve")
        d.line([(x - 1, y - 1) for x, y in pts], fill=SEA_C[2] + (255,), width=1)
    return im


def neighbours(g, cell, own):
    x, y = cell
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= ny < len(g) and 0 <= nx < len(g[0]) and g[ny][nx] not in ("MAPSEC_NONE", own):
            yield (nx, ny)


def frame_sub(out, sub):
    def fn(cv):
        w = C.text_width(sub, "narrow")
        C.draw_text(cv, C.W - 6 - w, 1, sub, C.WHITE, C.ACCENT_DARK, font="narrow")
    C.K.layer(out, fn, "map")


def cells_sheet(key, cl, art, rows, g):
    S = 4
    big = art.convert("RGB").resize((C.W * S, C.H * S), Image.NEAREST)
    d = ImageDraw.Draw(big)
    names = dict(cl["towns"], **cl["landmarks"], **cl["routes"])
    names.update({s: v[0] for s, v in cl["straits"].items()})
    secs = C.sections_of(g)
    for y, r in enumerate(rows):                        # cleared vanilla cells: red X
        for x, s in enumerate(r):
            if s != "MAPSEC_NONE" and g[y][x] == "MAPSEC_NONE":
                X, Y = C.cell_px((x, y))
                d.line([X * S, Y * S, (X + 8) * S - 1, (Y + 8) * S - 1], fill=(220, 40, 40), width=2)
                d.line([(X + 8) * S - 1, Y * S, X * S, (Y + 8) * S - 1], fill=(220, 40, 40), width=2)
                d.text((X * S + 2, (Y + 8) * S - 12), s[7:].lower()[:10], fill=(220, 40, 40))
    for s, cells in secs.items():
        strait = s in cl["straits"]
        col = (40, 90, 220) if strait else (0, 0, 0) if s in names else (150, 150, 150)
        for c in cells:
            X, Y = C.cell_px(c)
            box = [X * S, Y * S, (X + 8) * S - 1, (Y + 8) * S - 1]
            if strait:
                for i in range(0, 8 * S, 6):
                    d.line([box[0] + i, box[1], min(box[0] + i + 2, box[2]), box[1]], fill=col, width=2)
                    d.line([box[0] + i, box[3], min(box[0] + i + 2, box[2]), box[3]], fill=col, width=2)
                    d.line([box[0], box[1] + i, box[0], min(box[1] + i + 2, box[3])], fill=col, width=2)
                    d.line([box[2], box[1] + i, box[2], min(box[1] + i + 2, box[3])], fill=col, width=2)
            else:
                d.rectangle(box, outline=col, width=2)
        x, y = min(cells, key=lambda c: (c[1], c[0]))
        X, Y = C.cell_px((x, y))
        label = names.get(s, s[7:].title() + " (not built)")
        d.text((X * S + 3, Y * S + 3), label, fill=(0, 0, 0) if not strait else (20, 40, 160),
               stroke_width=2, stroke_fill=(255, 255, 255))
    for x in range(28):
        d.text(((x + 1) * 8 * S + 10, 2), str(x), fill=(40, 40, 120))
    for y in range(15):
        d.text((2, (y + 2) * 8 * S + 10), str(y), fill=(40, 40, 120))
    d.rectangle([C.cell_px(ERASE_BOX[:2])[0] * S, C.cell_px(ERASE_BOX[:2])[1] * S,
                 C.cell_px(ERASE_BOX[2:])[0] * S, C.cell_px(ERASE_BOX[2:])[1] * S], outline=(255, 140, 0), width=2)
    d.text((C.cell_px(ERASE_BOX[:2])[0] * S + 3, C.cell_px(ERASE_BOX[:2])[1] * S + 3),
           "FRLG switch button\nerased (tilemap)", fill=(160, 70, 0), stroke_width=2, stroke_fill=(255, 255, 255))
    big.save(os.path.join(C.OUT, "sevii%s_cells@4x.png" % key))


def main():
    os.makedirs(C.OUT, exist_ok=True)
    report = {}
    shots = []
    for key, cl in CLUSTERS.items():
        art, changed, sea = erased_art(key)
        rows, g = proposed_grid(key, cl)
        secs = C.sections_of(g)
        # nodes: towns = discs, single-cell landmarks = diamonds
        nodes = []
        for s in cl["towns"]:
            nodes.append((secs[s][0], False, s in cl["visited"]))
        for s in cl["landmarks"]:
            if len(secs.get(s, [])) == 1:
                nodes.append((secs[s][0], True, s in cl["visited"]))
        ends = {}
        tubes = []
        for s, (_, cells, (ja, jb)) in cl["straits"].items():
            a = min(secs[ja], key=lambda c: abs(c[0] - cells[0][0]) + abs(c[1] - cells[0][1]))
            b = min(secs[jb], key=lambda c: abs(c[0] - cells[-1][0]) + abs(c[1] - cells[-1][1]))
            t = tuple(cells)
            ends[t] = (C.cell_ctr(a), C.cell_ctr(b))
            tubes.append(t)
        cur = secs[cl["cursor"]][0]
        names = dict(cl["towns"], **cl["landmarks"], **cl["routes"])
        scr = C.screen(art, "SEVII ISLANDS", names[cl["cursor"]], nodes, cursor=cur, here=cur,
                       tubes=tube_layer(tubes, ends))
        frame_sub(scr, cl["sub"])
        C.save(scr, "sevii%s_screen" % key)
        shots.append(scr)
        cells_sheet(key, cl, art, rows, g)
        report[key] = {
            "erased_tiles": [list(c) for c in changed], "sea_tile": sea,
            "sections": {s: {"name": dict(names, **{k: v[0] for k, v in cl["straits"].items()}).get(s, "(not built)"),
                             "bbox": [min(x for x, _ in c), min(y for _, y in c),
                                      max(x for x, _ in c) - min(x for x, _ in c) + 1,
                                      max(y for _, y in c) - min(y for _, y in c) + 1],
                             "cells": len(c)} for s, c in sorted(secs.items())},
            "cleared": sorted(set(s for r in rows for s in r if s != "MAPSEC_NONE") - set(secs)),
        }
    strip = Image.new("RGB", (C.W * 3 + 16, C.H), (40, 40, 48))
    for i, im in enumerate(shots):
        strip.paste(im.convert("RGB"), (i * (C.W + 8), 0))
    C.save(strip, "sevii_screens")
    json.dump(report, open(os.path.join(C.OUT, "sevii_grid.json"), "w"), indent=1)
    for k, r in report.items():
        print("sevii%s erased %d tiles; sections:" % (k, len(r["erased_tiles"])))
        for s, v in r["sections"].items():
            print("   %-28s %-18s bbox %s" % (s, v["name"], v["bbox"]))
        print("   cleared:", r["cleared"])


if __name__ == "__main__":
    main()
