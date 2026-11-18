"""QUESTS app mockups (PSF Unbound Quest Menu data, Orchid kit look). usage: mock_quests.py OUT_DIR"""
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
from gamefont import draw_text, text_width

W, H = 240, 160


class Sheet:
    """P sheet whose first 16 entries are the Orchid kit roles; extra colours appended on demand."""
    def __init__(self):
        self.cols = list(kit.palette("orchid"))
        self.cols[0] = (1, 2, 3)          # key, never matched by c()
        self.im = Image.new("P", (W, H), 0)
        self.cv = Canvas(self.im)

    def c(self, rgb):
        rgb = snap(rgb)
        if rgb not in self.cols:
            self.cols.append(rgb)
        return self.cols.index(rgb)

    def rgba(self):
        flat = [v for c in self.cols for v in c]
        self.im.putpalette(flat + [0] * (768 - len(flat)))
        return K.sheet_rgba(self.im)


# ------------------------------------------------------------------ pictograms
X.SIL.update({
    "all": ["X.XXXXX", ".......", "X.XXXXX", ".......", "X.XXXXX"],
    "new": [".XXX.", "XX.XX", "...XX", "..XX.", "..X..", ".....", "..X.."],
    "active": ["XX", "XX", "XX", "XX", "..", "XX"],
    "reward": [".X...X.", "X.X.X.X", ".XXXXX.", "XXXXXXX", "XXX.XXX", "XXX.XXX", "XXX.XXX"],
    "done": ["......X", ".....XX", "X...XX.", "XX.XX..", ".XXX...", "..X...."],
    "locked": [".XXX.", "X...X", "X...X", "XXXXX", "XX.XX", "XXXXX"],
    "quest": ["XXXXXX", "X....X", "X.XX.X", "X....X", "X.XX.X", "XXXXXX"],
})
TAGS = {   # state -> (dark, face, light)
    "new": ((96, 96, 120), (144, 144, 160), (192, 192, 200)),
    "active": ((32, 80, 136), (64, 128, 200), (136, 184, 232)),
    "reward": ((152, 40, 72), (216, 88, 112), (240, 152, 168)),
    "done": ((40, 104, 64), (72, 160, 88), (144, 208, 136)),
    "locked": ((72, 72, 88), (112, 112, 128), (152, 152, 168)),
}
FILTERS = [("all", "All"), ("new", "New"), ("active", "Active"), ("reward", "Reward"), ("done", "Done")]
STAR = [
    "....k....",
    "...kyk...",
    "kkkkwykkk",
    "kwyyyyyyk",
    ".kyyyyyk.",
    "..kyyyk..",
    ".kyykyyk.",
    ".kykkkyk.",
    ".kk...kk.",
]

# Tosa sample quests: name, state, fav, subquests(done, total), sprite, location, text
QUESTS = [
    ("Lost Kopi Cups", "active", True, (2, 5), ("item", "soothe_bell"), "Tosa Port",
     "The kopi uncle lost his cups\naround the harbour. Find 5!"),
    ("Hawker's Recipe", "reward", False, None, ("item", "letter"), "Hawker Centre",
     "Return to Hawker Centre\nto receive your reward!"),
    ("Squid on the Pier", "active", True, (1, 3), ("mon", "torpesquid"), "Tosa Pier",
     "Torpesquid keep tangling the\nnets. Battle 3 at night."),
    ("Ferry Timetable", "done", False, None, ("item", "town_map"), "Tosa Port",
     "You delivered the new\ntimetable. Ferries run on time!"),
    ("Old Sea Chart", "new", False, None, ("item", "old_sea_map"), "Telok Town",
     "Talk to the old sailor in\nTelok Town to begin."),
    ("??????", "locked", False, None, None, "???", ""),
]
SUBS = [("Cup by the ferry gate", "done", "Tosa Port"), ("Cup in the fish market", "done", "Tosa Port"),
        ("Cup on the rail bridge", "active", "Reserve"), ("??????", "locked", "???"), ("??????", "locked", "???")]

ROW_Y, ROW_H, PILL_X, PILL_W, ROWS = 35, 16, 8, 218, 5
TRAY_Y = 114


def tag(s, x, y, state):
    cv, c = s.cv, s.c
    dk, fc, lt = TAGS[state]
    rounded_box(cv, x, y, 18, 12, 3, c(fc), INK, c(lt), c(dk))
    X.centred_sil(cv, x + 1, y + 1, 16, 10, state, WHITE, c(dk))


def star(s, x, y):
    cmap = {"k": INK, "y": s.c((248, 192, 48)), "w": s.c((248, 240, 168))}
    stamp(s.cv, x, y, STAR, cmap)


def header(s, title, count):
    cv = s.cv
    D.header_band(cv, 0, 239, round_left=False)
    rounded_box(cv, 4, 2, 14, 12, 3, ACCENT_LIGHT, INK, WHITE, ACCENT)
    X.centred_sil(cv, 5, 3, 13, 10, "quest", ACCENT_DARK, None)
    draw_text(cv, 23, 0, title, WHITE, ACCENT_DARK)
    if count:
        draw_text(cv, 236 - text_width(count), 0, count, WHITE, ACCENT_DARK)


def filter_tabs(s, sel):
    cv = s.cv
    X.keypad(cv, 4, 22, "L")
    for i, (key, _) in enumerate(FILTERS):
        x = 22 + i * 26
        if i == sel:
            rounded_box(cv, x, 18, 24, 14, 4, SELECT, INK, SELECT_LIGHT, SELECT_DARK)
            X.centred_sil(cv, x + 1, 19, 22, 12, key, INK, SELECT_DARK)
        else:
            rounded_box(cv, x, 18, 24, 14, 4, PANEL, INK, WHITE, PANEL_SHADE)
            X.centred_sil(cv, x + 1, 19, 22, 12, key, INK_SOFT, None)
    X.keypad(cv, 154, 22, "R")
    draw_text(cv, 174, 17, FILTERS[sel][1] + " (%d)" % [6, 1, 2, 1, 1][sel], WHITE, INK_SOFT, font="narrow")


def rows(s, items, cursor, scroll_frac=0.0, thumb_h=40):
    cv = s.cv
    for r in range(ROWS):
        y = ROW_Y + r * ROW_H
        if r >= len(items):
            continue
        name, state, fav, subs = items[r][:4]
        sel = r == cursor
        if sel:
            rounded_box(cv, PILL_X, y, PILL_W, 14, 4, SELECT, INK, SELECT_LIGHT, SELECT_DARK)
        else:
            rounded_box(cv, PILL_X, y, PILL_W, 14, 4, PANEL, INK, WHITE, PANEL_SHADE)
        if fav:
            star(s, PILL_X + 4, y + 2)
        ink = INK_SOFT if state == "locked" else INK
        draw_text(cv, PILL_X + 16, y - 1, name, ink, SELECT_DARK if sel else PANEL_SHADE)
        if subs:
            prog = "%d/%d" % subs
            draw_text(cv, PILL_X + PILL_W - 26 - text_width(prog, "small"), y - 1, prog, ink,
                      SELECT_DARK if sel else PANEL_SHADE, font="small")
        tag(s, PILL_X + PILL_W - 22, y + 1, state)
    if len(items) <= ROWS and thumb_h != 72:
        return
    # scroll track + gold thumb
    D.track(cv, 230, ROW_Y, 236, ROW_Y + ROWS * ROW_H - 3)
    ty = ROW_Y + 1 + round(scroll_frac * (ROWS * ROW_H - 5 - thumb_h))
    rounded_box(cv, 231, ty, 5, thumb_h, 1, SELECT, INK, SELECT_LIGHT, SELECT_DARK)


def tray(s, loc, text, extra=None):
    cv = s.cv
    D.tray(cv, TRAY_Y)
    disc(cv, 20, 137, 16, PANEL_SHADE, None)
    disc(cv, 20, 137, 15, WHITE, INK)
    disc(cv, 20.5, 137.5, 13, PANEL, None)
    ring(cv, 20, 137, 14, PANEL_SHADE)
    cv.vline(40, TRAY_Y + 6, H - 6, PANEL_SHADE)
    cv.vline(41, TRAY_Y + 6, H - 6, WHITE)
    X.label_pill(cv, 46, TRAY_Y + 5, 10 + X.CAP_W + text_width(loc, "narrow"), "pin")
    draw_text(cv, 46 + X.CAP_W + 4, TRAY_Y + 4, loc, INK, PANEL_SHADE, font="narrow")
    if extra == "A":
        w = text_width("Steps", "narrow")
        X.keypad(cv, 236 - w - 12, TRAY_Y + 8, "A")
        draw_text(cv, 236 - w, TRAY_Y + 4, "Steps", INK_SOFT, PANEL_SHADE, font="narrow")
    elif extra:
        draw_text(cv, 236 - text_width(extra, "narrow"), TRAY_Y + 4, extra, INK_SOFT, PANEL_SHADE, font="narrow")
    draw_text(cv, 47, TRAY_Y + 16, text, INK, PANEL_SHADE, line_h=14)


def sprite_in_well(out, spr):
    if not spr:
        return
    kind, name = spr
    if kind == "item":
        im = K.item_icon(name)
        out.alpha_composite(im, (20 - 12, 137 - 12))
    else:
        im = K.mon_icon(name, 0, 0)
        out.alpha_composite(im, (20 - 16, 137 - 20))


def screen_list(sel_filter=0, cursor=0, items=None, scroll=0.0):
    items = items if items is not None else QUESTS
    s = Sheet()
    header(s, "QUESTS", "4/12")
    filter_tabs(s, sel_filter)
    rows(s, items, cursor, scroll)
    q = items[cursor]
    extra = "A" if q[3] else None
    tray(s, q[5], q[6], extra)
    out = K.grid_frame(3)
    out.alpha_composite(s.rgba())
    sprite_in_well(out, q[4])
    return out


def screen_subs(cursor=2):
    s = Sheet()
    cv = s.cv
    header(s, "Lost Kopi Cups", "2/5")
    # progress strip instead of filter tabs
    X.keypad(cv, 4, 22, "B")
    draw_text(cv, 16, 17, "Back", WHITE, INK_SOFT, font="narrow")
    rounded_box(cv, 52, 19, 184, 12, 3, PANEL_DARK, INK, PANEL_SHADE, PANEL_DARK)
    fill = round(180 * 2 / 5)
    rounded_box(cv, 54, 21, fill, 8, 2, s.c((72, 160, 88)), INK, s.c((144, 208, 136)), s.c((40, 104, 64)))
    for k in range(1, 5):
        x = 54 + round(180 * k / 5)
        cv.vline(x, 21, 28, INK_SOFT)
    items = [(n, st, False, None) for n, st, _ in SUBS]
    rows(s, items, cursor, 0.0, thumb_h=72)
    tray(s, SUBS[cursor][2], "Kopi uncle says he heard\nclinking under the rail bridge.", "Step 3 of 5")
    out = K.grid_frame(3)
    out.alpha_composite(s.rgba())
    sprite_in_well(out, ("item", "soothe_bell"))
    return out


def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    shots = {
        "10_quests_all": screen_list(0, 0),
        "11_quests_reward": screen_list(3, 0, [QUESTS[1]]),
        "12_quests_mon": screen_list(0, 2),
        "13_quests_subs": screen_subs(2),
    }
    for k, im in shots.items():
        im.save(os.path.join(outdir, k + ".png"))
        K.upscale(im.convert("RGB"), 3).save(os.path.join(outdir, "x3_" + k + ".png"))
    # GIF: cursor down the list, R to Reward filter, back to All, A into steps
    frames = []
    for cur in [0, 0, 1, 2, 3, 4]:
        frames += [screen_list(0, cur, scroll=cur / 8)] * 8
    frames += [screen_list(3, 0, [QUESTS[1]])] * 14
    frames += [screen_list(0, 0)] * 8
    frames += [screen_subs(c) for c in (0, 0, 1, 1, 2, 2)] * 1
    frames += [screen_subs(2)] * 20
    big = [K.upscale(f.convert("RGB"), 2) for f in frames]
    big[0].save(os.path.join(outdir, "quests.gif"), save_all=True, append_images=big[1:], duration=80, loop=0)


if __name__ == "__main__":
    main(sys.argv[1])
