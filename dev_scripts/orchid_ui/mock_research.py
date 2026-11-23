"""
Palm's research tasks (round 1 mockups): Habitats progress turned into Professor Palm's field notes.

Tasks are computed from the dex (seen / captured / catalogued per habitat, day and night), so they track
themselves; the save only remembers which rewards were claimed. They live in the Rotom Phone's QUESTS app
under a new RESEARCH tab; Rotom buzzes in the field when one completes; the reward is claimed in the app
("Send to Palm") and research points raise a Research Rank.

usage: mock_research.py OUT_DIR
"""
import os
import sys

KIT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KIT)
from PIL import Image
import kit
from kit import *
import kit_ext as K
import system_ext as X
import dex_ext as D
import mock_quests as Q
import mock_habitats as MH
from gamefont import draw_text, text_width

W, H = 240, 160

X.SIL.update({
    "notes": ["..XXX..", "XX...XX", "X.XXX.X", "X.....X", "X.XXX.X", "X.....X", "X.XX..X", "XXXXXXX"],
})
CLIP = ["..kkk..", "kkwwwkk", "kwkkkwk", "kwwwwwk", "kwkkkwk", "kwwwwwk", "kwkkwwk", "kkkkkkk"]

RESEARCH_FILTERS = Q.FILTERS[:1] + [("notes", "Research")] + Q.FILTERS[1:]

# name, state, fav, (done, total), sprite, location, text
TASKS = [
    ("Western Tosa survey", "active", True, (4, 6), ("item", "town_map"), "Western Tosa",
     "Catalogue every species on\neach Western Tosa route. +40 RP"),
    ("Night watch: Western Tosa", "reward", False, None, ("item", "moon_stone"), "Western Tosa",
     "Send your notes to Palm to\nclaim the reward."),
    ("Southern Tosa survey", "active", False, (1, 9), ("item", "town_map"), "Southern Tosa",
     "Catalogue every species on\neach Southern Tosa route. +60 RP"),
    ("Request: marsh catfish", "new", False, None, ("mon", "barboach"), "Moongrove Marsh",
     "Palm wants a Barboach from\nthe marsh catalogued. +10 RP"),
    ("Request: reserve fighter", "done", False, None, ("mon", "tyrogue"), "South Tosa Reserve",
     "Tyrogue catalogued. Palm's\nthesis chapter 2 is done!"),
    ("??????", "locked", False, None, None, "???", ""),
]
STEPS = [("Telok Town", "done"), ("Route 311 East", "done"), ("Route 311 West", "active"),
         ("Damp Path", "done"), ("Wavebreak Town", "done"), ("Tosa Port", "new")]
RANKS = ["Field Assistant", "Junior Researcher", "Researcher", "Senior Researcher", "Palm's Partner"]


def research_tabs(s, sel):
    cv = s.cv
    X.keypad(cv, 4, 22, "L")
    for i, (key, _) in enumerate(RESEARCH_FILTERS):
        x = 18 + i * 23
        if i == sel:
            rounded_box(cv, x, 18, 21, 14, 4, SELECT, INK, SELECT_LIGHT, SELECT_DARK)
            X.centred_sil(cv, x + 1, 19, 19, 12, key, INK, SELECT_DARK)
        else:
            rounded_box(cv, x, 18, 21, 14, 4, PANEL, INK, WHITE, PANEL_SHADE)
            X.centred_sil(cv, x + 1, 19, 19, 12, key, INK_SOFT, None)
    X.keypad(cv, 18 + len(RESEARCH_FILTERS) * 23 + 2, 22, "R")
    lab = RESEARCH_FILTERS[sel][1]
    draw_text(cv, 236 - text_width(lab, "narrow"), 17, lab, WHITE, INK_SOFT, font="narrow")


def rank_header(s, title, rank, rp):
    """QUESTS header with the Research Rank in place of the quest count: rank stars + RP."""
    cv = s.cv
    D.header_band(cv, 0, 239, round_left=False)
    rounded_box(cv, 4, 2, 14, 12, 3, ACCENT_LIGHT, INK, WHITE, ACCENT)
    X.centred_sil(cv, 5, 3, 13, 10, "notes", ACCENT_DARK, None)
    draw_text(cv, 23, 0, title, WHITE, ACCENT_DARK)
    txt = "%d RP" % rp
    x = 236 - text_width(txt, "narrow")
    draw_text(cv, x, 0, txt, WHITE, ACCENT_DARK, font="narrow")
    for k in range(5):
        stamp(cv, x - 12 - (4 - k) * 10, 3, Q.STAR,
              {"k": INK, "y": s.c((248, 192, 48)) if k < rank else ACCENT_LIGHT,
               "w": s.c((248, 240, 168)) if k < rank else ACCENT_PALE})


def tray_reward(s, loc, text, reward_cta):
    Q.tray(s, loc, text, None)
    if reward_cta:
        cv = s.cv
        w = text_width("Send to Palm", "narrow")
        X.keypad(cv, 236 - w - 12, Q.TRAY_Y + 8, "A")
        draw_text(cv, 236 - w, Q.TRAY_Y + 4, "Send to Palm", INK_SOFT, PANEL_SHADE, font="narrow")


def screen_list(cursor=0, items=None):
    items = items if items is not None else TASKS
    s = Q.Sheet()
    rank_header(s, "QUESTS", 2, 140)
    research_tabs(s, 1)
    Q.rows(s, items, cursor)
    t = items[cursor]
    if t[1] == "reward":
        tray_reward(s, t[5], t[6], True)
    else:
        Q.tray(s, t[5], t[6], "A" if t[3] else None)
    out = K.grid_frame(3)
    out.alpha_composite(s.rgba())
    Q.sprite_in_well(out, t[4])
    return out


def screen_steps(cursor=2):
    s = Q.Sheet()
    cv = s.cv
    Q.header(s, "Western Tosa survey", "4/6")
    X.keypad(cv, 4, 22, "B")
    draw_text(cv, 16, 17, "Back", WHITE, INK_SOFT, font="narrow")
    rounded_box(cv, 52, 19, 184, 12, 3, PANEL_DARK, INK, PANEL_SHADE, PANEL_DARK)
    fill = round(180 * 4 / 6)
    rounded_box(cv, 54, 21, fill, 8, 2, s.c((72, 160, 88)), INK, s.c((144, 208, 136)), s.c((40, 104, 64)))
    for k in range(1, 6):
        cv.vline(54 + round(180 * k / 6), 21, 28, INK_SOFT)
    items = [(n, st, False, None) for n, st in STEPS[:5]]
    Q.rows(s, items, cursor, 0.0, thumb_h=72)
    # tray: habitat pill + the habitat's own counts, step number
    Q.tray(s, STEPS[cursor][0], "Catalogue all 14 species,\nday and night: 9 done.", "Step 3 of 6")
    out = K.grid_frame(3)
    out.alpha_composite(s.rgba())
    Q.sprite_in_well(out, ("item", "town_map"))
    return out


def popup(out, lines, icon=None, title=None):
    """Orchid message panel over the app (kit window, accent band)."""
    s = Q.Sheet()
    cv = s.cv
    x0, y0, w, h = 24, 46, 192, 68
    rounded_box(cv, x0, y0, w, h, 4, PANEL, INK, WHITE, PANEL_SHADE)
    if title:
        rounded_box(cv, x0 + 6, y0 - 7, text_width(title) + 14, 14, 4, ACCENT, INK, ACCENT_LIGHT, ACCENT_DARK)
        draw_text(cv, x0 + 13, y0 - 8, title, WHITE, ACCENT_DARK)
    tx = x0 + (40 if icon else 10)
    for k, line in enumerate(lines):
        draw_text(cv, tx, y0 + 10 + k * 14, line, INK, PANEL_SHADE)
    if icon:
        D.well(cv, x0 + 8, y0 + 18, 26, 26)
    out.alpha_composite(s.rgba())
    if icon:
        im = K.item_icon(icon)
        out.alpha_composite(im, (x0 + 9, y0 + 19))
    return out


def screen_claim():
    out = screen_list(1)
    dim = Image.new("RGBA", (W, H), (8, 8, 16, 110))
    out.alpha_composite(dim)
    return popup(out, ["Palm sent 5 Ultra Balls", "and 30 research points!", "Night watch filed."], "ultra_ball",
                 "FIELD NOTES")


def screen_rank():
    out = screen_list(1)
    out.alpha_composite(Image.new("RGBA", (W, H), (8, 8, 16, 110)))
    s = Q.Sheet()
    cv = s.cv
    x0, y0, w, h = 24, 40, 192, 80
    rounded_box(cv, x0, y0, w, h, 4, PANEL, INK, WHITE, PANEL_SHADE)
    rounded_box(cv, x0 + 6, y0 - 7, text_width("RANK UP") + 14, 14, 4, SELECT, INK, SELECT_LIGHT, SELECT_DARK)
    draw_text(cv, x0 + 13, y0 - 8, "RANK UP", INK, SELECT_DARK)
    for k in range(5):
        stamp(cv, x0 + 56 + k * 16, y0 + 10, Q.STAR,
              {"k": INK, "y": s.c((248, 192, 48)) if k < 3 else PANEL_SHADE,
               "w": s.c((248, 240, 168)) if k < 3 else PANEL})
    t = "Researcher"
    draw_text(cv, x0 + (w - text_width(t)) // 2, y0 + 22, t, INK, PANEL_SHADE)
    for k, line in enumerate(["Palm: \"The habitat data", "is changing everything!\""]):
        draw_text(cv, x0 + 12, y0 + 40 + k * 14, line, INK_SOFT, PANEL_SHADE, font="narrow")
    out.alpha_composite(s.rgba())
    return out


# ------------------------------------------------------------------ Habitats integration
def stamp_clip(out, x, y):
    s = Q.Sheet()
    stamp(s.cv, x, y, CLIP, {"k": INK, "w": s.c((248, 240, 168))})
    out.alpha_composite(s.rgba())


def screen_habitats_map():
    """Map: a clipboard marks habitats with an open Palm request; the zone plate counts become survey progress."""
    out = MH.render_map("tosa", "MAPSEC_MOONGROVE_MARSH", tags=MH.RT.Tags(region="tosa"))
    tags = MH.RT.Tags(region="tosa")
    for a in tags.placed():
        if a.id in ("MAPSEC_MOONGROVE_MARSH", "MAPSEC_ROUTE_314"):
            cx, cy = a.node_cell
            stamp_clip(out, MH.GX + cx * 8 + 8, MH.GY + cy * 8 - 6)
    return out


def screen_habitats_route():
    """Route page: requested species get a clipboard on their well; the tray says what Palm wants."""
    out = MH.render_route("MAPSEC_MOONGROVE_MARSH", (3, 0), "day", top=1, tags=MH.RT.Tags(region="tosa"))
    rows = MH.route_rows("MAPSEC_MOONGROVE_MARSH", "day")
    for r, (m, sps, _) in enumerate(rows):
        for k, sp in enumerate(sps):
            if sp == "SPECIES_BARBOACH" and 1 <= r < 1 + MH.ROWS_VISIBLE:
                x0 = MH.SLOT_X0 + k * MH.SLOT_PITCH
                y0 = MH.ROW_Y0 + (r - 1) * MH.ROW_PITCH + MH.WELL_DY
                stamp_clip(out, x0 + 2, y0 + 2)
    # tray second line replaced by the request
    s = Q.Sheet()
    cv = s.cv
    cv.rect(6, MH.TRAY_Y + 13, 158, MH.TRAY_Y + 29, PANEL)
    stamp(cv, 8, MH.TRAY_Y + 18, CLIP, {"k": INK, "w": s.c((248, 240, 168))})
    draw_text(cv, 20, MH.TRAY_Y + 14, "Palm: catalogue this one", INK_SOFT, PANEL_SHADE, font="narrow")
    out.alpha_composite(s.rgba())
    return out


def screen_buzz():
    """Field: Rotom's buzz toast (existing QUEST_MENU_BUZZ) announcing a finished task."""
    shot = os.path.join(os.path.dirname(KIT), "..", "graphics", "pokedex", "orchid")  # unused path guard
    base = K.grid_frame(0)
    try:
        ow = Image.open(os.environ.get("RESEARCH_OW_SHOT", "")).convert("RGBA").resize((W, H), Image.NEAREST)
        base = ow
    except Exception:
        pass
    s = Q.Sheet()
    cv = s.cv
    msg = "Bzzt! Field notes updated!"
    w = text_width(msg, "narrow") + 34
    x0 = (W - w) // 2
    rounded_box(cv, x0, 4, w, 18, 4, s.c((232, 96, 64)), INK, s.c((248, 160, 128)), s.c((168, 56, 40)))
    rounded_box(cv, x0 + 3, 7, 12, 12, 4, WHITE, INK, WHITE, PANEL_SHADE)
    X.centred_sil(cv, x0 + 3, 8, 12, 10, "notes", s.c((168, 56, 40)), None)
    draw_text(cv, x0 + 20, 4, msg, WHITE, s.c((168, 56, 40)), font="narrow")
    sub = "Night watch: Western Tosa"
    sw = text_width(sub, "narrow") + 12
    rounded_box(cv, (W - sw) // 2, 24, sw, 14, 4, PANEL, INK, WHITE, PANEL_SHADE)
    draw_text(cv, (W - sw) // 2 + 6, 23, sub, INK, PANEL_SHADE, font="narrow")
    base.alpha_composite(s.rgba())
    return base


def save(im, path):
    K.upscale(im.convert("RGB"), 3).save(path)


if __name__ == "__main__" and len(sys.argv) == 2:
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    save(screen_list(0), os.path.join(out, "r1_list.png"))
    save(screen_list(3), os.path.join(out, "r2_request.png"))
    save(screen_steps(2), os.path.join(out, "r3_steps.png"))
    save(screen_list(1), os.path.join(out, "r4_reward.png"))
    save(screen_claim(), os.path.join(out, "r5_claim.png"))
    save(screen_rank(), os.path.join(out, "r6_rank.png"))
    save(screen_habitats_map(), os.path.join(out, "r7_hab_map.png"))
    save(screen_habitats_route(), os.path.join(out, "r8_hab_route.png"))
    save(screen_buzz(), os.path.join(out, "r9_buzz.png"))
    print("ok")


# ------------------------------------------------------------------ Habitats round 4 (user 2026-11-23)
def habitats_extras(out):
    """Locked rows (no Surf / rod yet) and rare unseen species shown as "?"."""
    tags = MH.RT.Tags(region="tosa")
    marsh = "MAPSEC_MOONGROVE_MARSH"
    rows = MH.route_rows(marsh, "day")
    water = next(r for r, (m, _, f) in enumerate(rows) if m == "water_mons")
    save(MH.render_route(marsh, (water, 1), "day", top=1, tags=tags, locked={"water_mons", "fishing_mons"}),
         os.path.join(out, "h1_locked.png"))
    save(MH.render_route(marsh, (0, 5), "day", tags=tags, rare_q=True), os.path.join(out, "h2_rare.png"))


if __name__ == "__main__" and len(sys.argv) > 2 and sys.argv[2] == "extras":
    habitats_extras(sys.argv[1])
