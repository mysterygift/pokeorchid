"""
Round 3: the REAL Tosa Rail network from the region map tagger (dev_scripts/region_map_tagger/tags.json),
drawn with the approved round 2 renderer (big_map.py: 512x256 canvas, dead zone + re-centre camera,
chevrons, labels baked into BG2).

Lines and stops are the user's (tagger Rail tab). Node positions follow the stations' region-map cells
(roughly 2.5x across, 2.4x down), hand-snapped to cell centres so every run is 0/45/90 deg.
Corral City is ticked as a station but isn't on any line; the mock extends the Pokétopia Line to it
(question for the user).

Writes out/r3_*.png (1x + 3x) and out/r3_overview_2x.png; prints the BG2 budget.
usage: ORCHID_UI_KIT=../orchid_ui python mock_tosa_network.py
"""
import os

from common import *
import big_map as B
import station_map as M

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

THEMES.setdefault("rail_sun", [(168, 72, 16), (232, 128, 48), (248, 184, 104), (252, 224, 184)])
LINE_THEME = {"west": "orchid", "central": "rail_sea", "east": "rail_forest", "poketopia": "rail_sun",
              "grey": "rail_grey"}
LINE_LABEL = {"west": "WEST", "central": "CENTRAL", "east": "EAST", "poketopia": "POKéTOPIA"}
LINE_ORDER = ("west", "central", "east", "poketopia")


def c(cx, cy):
    """canvas cell -> pixel centre (8k+4)"""
    return cx * 8 + 4, cy * 8 + 4


# name: (x, y, lines, label (anchor, dx, dy)) — region cell in the comment
STATIONS = {
    "TOSA PORT":      (*c(3, 22),  ("west",),                       ("c", 0, 6)),     # (7,12)
    "MOONGROVE CITY": (*c(9, 22),  ("west",),                       ("r", 7, 6)),     # (9,12)
    "TIMAH CITY":     (*c(13, 3),  ("west",),                       ("c", 0, -18)),     # (11,4)
    "FABER TOWN":     (*c(23, 3),  ("west",),                       ("c", 0, -18)),   # (15,4)
    "CHANGU CITY":    (*c(23, 12), ("west", "central", "east"),     ("l", -8, 6)),    # (15,8)
    "CHANGU AIRPORT": (*c(23, 17), ("central",),                    ("r", 7, -6)),    # (15,10)
    "INKA CITY":      (*c(23, 27), ("central",),                    ("c", 0, 6)),     # (15,14)
    "BURA CITY":      (*c(38, 12), ("central",),                    ("c", 0, -18)),    # (21,8)
    "JURAN CITY":     (*c(43, 22), ("central", "poketopia"),        ("r", 8, -18)),    # (23,12)
    "SENOKO CITY":    (*c(56, 8),  ("east",),                       ("c", 0, 6)),     # (27,6)
    "POKéMON LEAGUE": (*c(43, 3),  ("east",),                       ("c", 0, 6)),     # (23,4)
    "POKéTOPIA GATE": (*c(51, 27), ("poketopia",),                  ("c", 0, 6)),   # (26,14)
    "CORRAL CITY":    (*c(59, 27), ("poketopia",),                  ("c", -6, -18)),    # (27,14)
}
EDGES = [
    ("TOSA PORT", "MOONGROVE CITY", "west", []),
    ("MOONGROVE CITY", "TIMAH CITY", "west", [c(9, 7)]),
    ("TIMAH CITY", "FABER TOWN", "west", []),
    ("FABER TOWN", "CHANGU CITY", "west", []),
    ("CHANGU CITY", "BURA CITY", "central", []),
    ("BURA CITY", "JURAN CITY", "central", [c(43, 17)]),
    ("JURAN CITY", "INKA CITY", "central", [c(38, 27)]),
    ("INKA CITY", "CHANGU AIRPORT", "central", []),
    ("CHANGU AIRPORT", "CHANGU CITY", "central", []),
    ("CHANGU CITY", "SENOKO CITY", "east", [c(27, 8)]),
    ("SENOKO CITY", "POKéMON LEAGUE", "east", [c(51, 3)]),
    ("JURAN CITY", "POKéTOPIA GATE", "poketopia", [c(46, 25), c(48, 27)]),
    ("POKéTOPIA GATE", "CORRAL CITY", "poketopia", []),
]
EARLY = dict(current="TOSA PORT", visited={"TOSA PORT"})
MID = dict(current="CHANGU CITY",
           visited={"TOSA PORT", "MOONGROVE CITY", "TIMAH CITY", "FABER TOWN", "CHANGU CITY", "CHANGU AIRPORT",
                    "INKA CITY", "BURA CITY"})
LATE = dict(current="JURAN CITY", visited=set(STATIONS) - {"POKéMON LEAGUE"})

B.STATIONS, B.EDGES, B.LINE_THEME, B.LINE_LABEL = STATIONS, EDGES, LINE_THEME, LINE_LABEL
B.STATE = EARLY


def base_canvas(state):
    """big_map.base_canvas with four line groups instead of its fixed three."""
    out = Image.new("RGBA", (B.CW, B.CH), (0, 0, 0, 0))
    fl = B.fills(state)
    for g in ("grey",) + LINE_ORDER:
        if g in fl:
            KX.layer(out, lambda cv, f=fl[g]: M.draw_lines(cv, *f), LINE_THEME[g])

    def labels(cv):
        for n in STATIONS:
            tx, ty, _ = B.label_box(n)
            draw_text(cv, tx, ty, n, WHITE if n in state["visited"] else INK_SOFT, INK, font="small")
    KX.layer(out, labels)
    for n, (x, y, _, _) in STATIONS.items():
        out.alpha_composite(B.node_for(n, state["visited"]), (x - 8, y - 8))
    x, y = STATIONS[state["current"]][:2]
    out.alpha_composite(M.head(), (x - 8, y - 8 - 14))
    return out


def legend_layer(out, x=84):
    for key in LINE_ORDER:
        f = M.line_masks([[(x + 3, 8), (x + 11, 8)]], W, H, 1.6, 2.6)
        KX.layer(out, lambda cv, f=f: M.draw_lines(cv, *f), LINE_THEME[key])
        tx, lab = x + 15, LINE_LABEL[key]
        KX.layer(out, lambda cv, tx=tx, lab=lab: draw_text(cv, tx, -2, lab, WHITE, ACCENT_DARK, font="small"))
        x = tx + text_width(lab, "small") + 5


def legend_pips(out, x=104):
    """Header option A: keep the TOSA RAIL title, legend = colour pips only (the tray names the line)."""
    for key in LINE_ORDER:
        f = M.line_masks([[(x + 3, 8), (x + 13, 8)]], W, H, 1.6, 2.6)
        KX.layer(out, lambda cv, f=f: M.draw_lines(cv, *f), LINE_THEME[key])
        x += 20


HEADER = {"mode": "named"}           # "named" = option B (no title text), "pips" = option A
_draw_text = B.draw_text


def _draw_text_no_title(cv, x, y, text, *a, **k):
    if HEADER["mode"] == "named" and text == "TOSA RAIL":
        return x
    return _draw_text(cv, x, y, text, *a, **k)


def header_legend(out):
    if HEADER["mode"] == "pips":
        legend_pips(out)
    else:
        legend_layer(out, x=22)


def tray_text(out, name, message=None):
    """big_map.tray_text, but interchanges list the line names without " LINES" so 3 lines clear the hints."""
    lines = STATIONS[name][2]

    def fn(cv):
        if message:
            draw_text(cv, 8, M.TRAY_Y + 2, message, INK, PANEL_SHADE, line_h=14)
            return
        draw_text(cv, 26, M.TRAY_Y + 1, name, INK, PANEL_SHADE)
        sub = " + ".join(LINE_LABEL[l] for l in lines) if len(lines) > 1 else LINE_LABEL[lines[0]] + " LINE"
        draw_text(cv, 26, M.TRAY_Y + 15, sub, INK_SOFT, PANEL_SHADE, font="small")
        x = 239 - 8 - (8 + 3 + text_width("DEPART", "small") + 8 + 8 + 3 + text_width("CANCEL", "small"))
        y = M.TRAY_Y + 20
        x = draw_button(cv, x, y, "A") + 3
        x = draw_text(cv, x, y - 4, "DEPART", INK, PANEL_SHADE, font="small") + 8
        x = draw_button(cv, x, y, "B") + 3
        draw_text(cv, x, y - 4, "CANCEL", INK, PANEL_SHADE, font="small")
    KX.layer(out, fn)
    if not message:
        f = M.line_masks([[(6, M.TRAY_Y + 11), (20, M.TRAY_Y + 11)]], W, H, 2.0, 3.0)
        KX.layer(out, lambda cv: M.draw_lines(cv, *f), LINE_THEME[lines[0]])
        spr = B.interchange_sprite() if len(lines) > 1 else M.node_sprite("on")
        out.alpha_composite(spr, (13 - 8, M.TRAY_Y + 11 - 8))


B.base_canvas, B.legend_layer, B.tray_text, B.draw_text = base_canvas, header_legend, tray_text, _draw_text_no_title


def save(name, im):
    im.convert("RGB").save(os.path.join(OUT, name + ".png"))
    KX.upscale(im.convert("RGB"), 3).save(os.path.join(OUT, name + "_3x.png"))


def main():
    shots = []
    HEADER["mode"] = "pips"
    save("r3_0_header_pips", B.render("CHANGU CITY", B.centre_on("CHANGU CITY"), state=MID))
    HEADER["mode"] = "named"
    for tag, state, cursor in (("r3_1_early", EARLY, "TOSA PORT"), ("r3_2_changu", MID, "CHANGU CITY"),
                               ("r3_3_juran", LATE, "JURAN CITY"), ("r3_4_timah", MID, "TIMAH CITY")):
        cam = B.centre_on(cursor)
        save(tag, B.render(cursor, cam, state=state))
        shots.append((tag[3:], cam))
    B.STATE = MID
    B.base.__defaults__ = (MID,)
    B.overview(shots, os.path.join(OUT, "r3_overview_2x.png"))
    for st in (EARLY, MID):
        print("budget", B.budget(st))


if __name__ == "__main__":
    main()
