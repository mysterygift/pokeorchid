"""Rotom Phone home-screen mockups (Orchid UI kit). usage: python3 mock_phone.py OUT_DIR"""
import os
import sys

KIT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KIT)
from PIL import Image, ImageDraw
import kit
from kit import snap, Canvas, rounded_box, disc
import kit_ext as K
import system_ext as X
import mock_system as MS
from gamefont import draw_text, text_width

W, H = 240, 160

# ---------------------------------------------------------------- one P sheet, colours added on demand
class Sheet:
    def __init__(self, w, h):
        self.cols = [(0, 0, 0)]
        self.im = Image.new("P", (w, h), 0)
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


INK = (40, 40, 64)
WHITE = (248, 248, 248)
# Rotom coral ramp (from the official art, snapped)
R_LIGHT, R_FACE, R_SHADE, R_DARK = (248, 152, 120), (232, 104, 80), (192, 72, 64), (136, 48, 48)
SCR, SCR_GLARE, SCR_DEEP = (40, 40, 52), (56, 56, 72), (24, 24, 32)
GOLD = ((216, 128, 32), (248, 208, 88), (248, 240, 168))   # kit SELECT_DARK / SELECT / SELECT_LIGHT
GREY_TXT = (168, 168, 184)

APPS = [  # name, (dark, face, light), Rotom line
    ("MAP", ((40, 104, 64), (72, 160, 88), (144, 208, 136)), "Bzzt! Where to? I'll pull\nup the TOSA map!"),
    ("CALL", ((32, 80, 136), (64, 128, 200), (136, 184, 232)), "Want to ring someone?\nI've got 12 contacts!"),
    ("QUESTS", ((96, 48, 128), (152, 88, 184), (200, 152, 224)), "2 new requests! People\nare counting on you, bzzt!"),
    ("RADIO", ((24, 104, 120), (48, 160, 168), (120, 208, 208)), "Tune in to TOSA FM!\n(App still downloading…)"),
]

# 16x16 silhouettes: '#' white, '=' tile-light, 'r' pin red
ICONS = {
    "MAP": [
        "................",
        "..........rrr...",
        ".........rrwrr..",
        ".##......rrrrr..",
        ".####.....rrr.#.",
        ".##=####...r###.",
        ".##===######=##.",
        ".##===##=###=##.",
        ".##===##==##=##.",
        ".##===##==##=##.",
        ".##===##==##=##.",
        ".##===##==##=##.",
        ".####=##==####..",
        "....######......",
        "................",
        "................",
    ],
    "CALL": [
        "................",
        ".###......#.....",
        "#####......#.#..",
        "#####...#..#..#.",
        "####.....#..#.#.",
        ".###......#.#.#.",
        ".###............",
        "..###...........",
        "...###..........",
        "....####...###..",
        ".....##########.",
        "......#########.",
        "........######..",
        "................",
        "................",
        "................",
    ],
    "QUESTS": [
        "................",
        ".....######.....",
        "..####====####..",
        "..##..####..##..",
        "..##........##..",
        "..##.#..===.##..",
        "..####......##..",
        "..##.#..===.##..",
        "..##........##..",
        "..##.#..===.##..",
        "..####......##..",
        "..##.#..===.##..",
        "..##........##..",
        "..############..",
        "................",
        "................",
    ],
    "RADIO": [
        "...........#....",
        "..........#.....",
        ".........#......",
        "........#.......",
        "..############..",
        ".##############.",
        ".#=.=.=.###..##.",
        ".#.=.=.=##.##.#.",
        ".#=.=.=.##.##.#.",
        ".#.=.=.=###..##.",
        ".##############.",
        ".##############.",
        "..##........##..",
        "................",
        "................",
        "................",
    ],
}


# ---------------------------------------------------------------- news ticker (replaces the location text)
# Mirrors the proposed C table: { text, minBadges, maxBadges, flag, flagState }. flag None = always eligible.
NEWS = [
    ("Rookie Trainers spotted leaving Tosa Port!",      0, 0, None, None),
    ("Ferry timetable back to normal after storm.",     0, 8, None, None),
    ("TOSA FM: new hits every hour, bzzt!",             0, 8, None, None),
    ("Local Trainer wins first Gym Badge!",             1, 1, None, None),
    ("Cold Storage reports a strange chill...",         2, 8, "FLAG_COLD_STORAGE_DONE", False),
    ("Tosa Rail adds extra trains for fans.",           3, 8, "FLAG_TOSA_RAIL_OPEN", True),
    ("Halfway there! Challenger holds 4 badges.",       4, 5, None, None),
    ("Tosa League braces for a new challenger!",        8, 8, None, None),
    ("A new Champion is crowned in Tosa!",              0, 8, "FLAG_SYS_GAME_CLEAR", True),
]
TICK_L, TICK_R = 49, 148          # clip window (WIN0 on hardware); signal pips start at 154
NEWS_ICON = ["#######", "#=====#", "#.###.#", "#.....#", "#.###.#", "#.....#", "#######"]


def news_pool(badges, flags=()):
    out = []
    for text, lo, hi, flag, state in NEWS:
        if not lo <= badges <= hi:
            continue
        if flag is not None and (flag in flags) != state:
            continue
        out.append(text)
    return out


def draw_ticker(s, offset, pool):
    cv, c = s.cv, s.c
    kit.stamp(cv, 38, 34, NEWS_ICON, {"#": c(WHITE), "=": c((224, 72, 56)), ".": c(SCR_DEEP)})
    keep = s.im.crop((0, 31, W, 45))                   # restore everything outside the clip after drawing
    gap = 14
    x = TICK_R - offset
    loop = sum(text_width(t, "small") + gap for t in pool)
    x = TICK_R - (offset % loop) if loop else x
    for rep in range(3):
        for t in pool:
            if x > TICK_R:
                break
            draw_text(cv, x, 31, t, c(WHITE), c(SCR_DEEP), font="small")
            x += text_width(t, "small")
            cv.rect(x + gap // 2 - 1, 38, x + gap // 2, 39, c(GOLD[1]))   # gold dot between headlines
            x += gap
    clipped = s.im.copy()
    s.im.paste(keep, (0, 31))
    s.im.paste(clipped.crop((TICK_L, 31, TICK_R + 1, 45)), (TICK_L, 31))


def silhouette_mask():
    m = Image.new("1", (W, H), 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle((20, 24, 219, 137), radius=8, fill=1)
    # lightning-bolt fin (top, right of centre) and tail spike (bottom)
    d.polygon([(131, 25), (136, 12), (128, 13), (151, 1), (147, 11), (157, 10), (150, 25)], fill=1)
    d.polygon([(137, 136), (155, 136), (150, 157)], fill=1)
    return m


def draw_shell(s, eye=False):
    cv, c = s.cv, s.c
    m = silhouette_mask().load()
    inside = lambda x, y: 0 <= x < W and 0 <= y < H and m[x, y]
    for y in range(H):
        for x in range(W):
            if not inside(x, y):
                continue
            if not all(inside(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                cv.set(x, y, c(INK))
            elif not inside(x - 1, y - 1) or not inside(x, y - 2):
                cv.set(x, y, c(R_LIGHT))
            elif not inside(x + 1, y + 1) or not inside(x, y + 2):
                cv.set(x, y, c(R_SHADE))
            else:
                cv.set(x, y, c(R_FACE))
    # bezel inner step + screen
    rounded_box(cv, 28, 30, 184, 102, 4, c(R_SHADE), c(R_DARK), c(R_SHADE), c(R_LIGHT))
    rounded_box(cv, 30, 32, 180, 98, 3, c(SCR), c(SCR_DEEP), c(SCR), c(SCR), bevel=False)
    # diagonal glare band (like the official art), 1 step lighter
    for y in range(33, 129):
        for x in range(31, 209):
            if 150 < x + (y - 33) * 0.6 - 0 < 196 and cv.get(x, y) == c(SCR):
                cv.set(x, y, c(SCR_GLARE))
    # left notch = Rotom's eye/camera
    disc(cv, 30, 80.5, 6, c(R_FACE), c(INK))
    disc(cv, 30, 80.5, 3.5, c(SCR_DEEP), c(R_DARK))
    disc(cv, 30, 80.5, 1.5, c((120, 200, 248)) if eye else c((64, 72, 96)), None)
    if eye:
        cv.set(29, 79, c(WHITE))


def draw_phone(s, cursor, badge=0, eye=False, tick=0, pool=None):
    cv, c = s.cv, s.c
    draw_shell(s, eye)
    # status bar
    draw_ticker(s, tick, pool if pool is not None else news_pool(1))
    draw_text(cv, 170, 31, "4:27", c(WHITE), c(SCR_DEEP), font="small")
    for k in range(3):                                   # signal pips
        cv.rect(154 + k * 3, 41 - 2 * k, 155 + k * 3, 42, c(WHITE))
    cv.hline(36, 203, 45, c(SCR_DEEP))

    # app grid
    for i, (name, (dk, fc, lt), _) in enumerate(APPS):
        colx = 38 + i * 42
        sel = i == cursor
        if sel:
            rounded_box(cv, colx - 1, 49, 40, 48, 4, c(GOLD[1]), c(INK), c(GOLD[2]), c(GOLD[0]))
        tx, ty = colx + 5, 52
        rounded_box(cv, tx, ty, 29, 29, 4, c(fc), c(INK), c(lt), c(dk))
        rows = ICONS[name]
        for yy, row in enumerate(rows):
            for xx, ch in enumerate(row):
                px, py = tx + 7 + xx, ty + 7 + yy
                if ch == "#":
                    cv.set(px + 1, py + 1, c(dk)) if rows[yy + 1 if yy + 1 < 16 else yy][min(xx + 1, 15)] not in "#" else None
                    cv.set(px, py, c(WHITE))
                elif ch == "=":
                    cv.set(px, py, c(lt))
                elif ch == "r":
                    cv.set(px, py, c((224, 72, 56)))
                elif ch == "w":
                    cv.set(px, py, c(WHITE))
        if name == "QUESTS" and badge:
            disc(cv, tx + 27, ty + 2, 4, c((224, 72, 56)), c(INK))
            draw_text(cv, tx + 25, ty - 6, str(badge), c(WHITE), None, font="small")
        lab = name
        lw = text_width(lab, "small")
        draw_text(cv, colx + 19 - lw // 2, 81, lab, c(INK) if sel else c(GREY_TXT),
                  c(GOLD[0]) if sel else c(SCR_DEEP), font="small")

    # Rotom speech strip
    rounded_box(cv, 35, 100, 170, 28, 3, c(SCR_DEEP), c(SCR_DEEP), c(SCR_DEEP), c(SCR_DEEP), bevel=False)
    draw_text(cv, 40, 98, APPS[cursor][2], c(WHITE), c((88, 88, 104)), line_h=12)


# ---------------------------------------------------------------- offline (before FLAG_SYS_PHONE_ACTIVE)
# User request 2026-11-18: until a story flag switches the phone on, opening it shows Rotom's face
# with X eyes, empty signal bars and the clock; no ticker, apps or speech strip.
PIP_EMPTY = (88, 88, 104)
X_EYE = ['##............##',
         '###..........###',
         '.###........###.',
         '..###......###..',
         '...###....###...',
         '....###..###....',
         '.....######.....',
         '......####......',
         '......####......',
         '.....######.....',
         '....###..###....',
         '...###....###...',
         '..###......###..',
         '.###........###.',
         '###..........###',
         '##............##']
MOUTH = ['#......##......##......##',
         '.#....#..#....#..#....#..',
         '..#..#....#..#....#..#...',
         '...##......##......##....']


def draw_phone_offline(s, clock="4:27"):
    cv, c = s.cv, s.c
    draw_shell(s, False)
    draw_text(cv, 170, 31, clock, c(WHITE), c(SCR_DEEP), font="small")
    for k in range(3):                                   # empty signal pips
        cv.rect(154 + k * 3, 41 - 2 * k, 155 + k * 3, 42, c(PIP_EMPTY))
    cv.hline(36, 203, 45, c(SCR_DEEP))
    for ex in (90, 134):                                 # X eyes, shaded down-right
        kit.stamp(cv, ex + 1, 63, X_EYE, {"#": c(SCR_DEEP)})
        kit.stamp(cv, ex, 62, X_EYE, {"#": c(WHITE)})
    kit.stamp(cv, 109, 93, MOUTH, {"#": c(SCR_DEEP)})
    kit.stamp(cv, 108, 92, MOUTH, {"#": c(WHITE)})


def offline_frame(scroll=0, clock="4:27"):
    s = Sheet(W, H)
    draw_phone_offline(s, clock)
    out = K.grid_frame(scroll)
    out.alpha_composite(s.rgba())
    return out


def phone_layer(cursor, badge=0, eye=False, tick=0, pool=None):
    s = Sheet(W, H)
    draw_phone(s, cursor, badge, eye, tick, pool)
    return s.rgba()


def frame(cursor=0, scroll=0, badge=2, eye=True, tick=TICK_R - TICK_L - 2, pool=None):
    out = K.grid_frame(scroll)
    out.alpha_composite(phone_layer(cursor, badge, eye, tick, pool))
    return out


# ---------------------------------------------------------------- start menu with PHONE
PHONE_ICON = [
    ".........kk.....",
    "........kok.....",
    ".......kork.....",
    "..kkkkkkrkkkkk..",
    ".koooooooooooRk.",
    ".kokkkkkkkkkkRk.",
    "kkkkdddddddmkRk.",
    "kmkkddddddmdkRk.",
    "kkkkdddddmddkRk.",
    ".kokddddmdddkRk.",
    ".kokkkkkkkkkkRk.",
    ".krRRRRRRRRRRRk.",
    "..kkkkkkkRkkkk..",
    ".........kRk....",
    "..........k.....",
    "................",
]
_orig_icon = X.menu_icon


def menu_icon(name, muted=0.0):
    if name != "PHONE":
        return _orig_icon(name, muted)
    import menu_icons as MI
    im = Image.new("P", (16, 16), 0)
    kit.stamp(Canvas(im), 0, 0, PHONE_ICON, MI.CMAP)
    pal = list(MI.PALETTE)
    if muted:
        pal = [snap(tuple(int(v + (g - v) * muted) for v, g in zip(cc, (184, 184, 200)))) for cc in pal]
        pal[1] = MI.PALETTE[1]
    return K.sheet_rgba(im, pal)


X.menu_icon = menu_icon


def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    entries = ["POKéDEX", "POKéMON", "BAG", "PHONE", "PLAYER", "SAVE", "OPTION", "EXIT"]
    MS.render_start(entries, cursor=3).save(os.path.join(outdir, "00_start.png"))
    offline_frame().save(os.path.join(outdir, "06_offline.png"))
    for i in range(4):
        frame(i, badge=2, eye=(i == 2)).save(os.path.join(outdir, "%02d_home_%s.png" % (i + 1, APPS[i][0].lower())))
    # GIF: slide up from the start menu, then cursor walks the apps
    frames = []
    start = MS.render_start(entries, cursor=3)
    for f in range(8):
        frames.append(start)
    n = 14
    for f in range(n + 1):
        t = f / n
        e = 1 - (1 - t) ** 3
        dy = round(H * (1 - e))
        out = K.grid_frame(f // 4)
        ph = phone_layer(0, 2, False)
        out.alpha_composite(ph.crop((0, 0, W, H - dy)), (0, dy)) if dy < H else None
        frames.append(out)
    seq = [0] * 20 + [1] * 20 + [2] * 24 + [3] * 20 + [2] * 10 + [1] * 10 + [0] * 20
    for k, cur in enumerate(seq):
        frames.append(frame(cur, scroll=(n + k) // 4, badge=2, eye=(cur == 2 and (k // 6) % 2 == 0), tick=40 + k * 3))
    # news states: the same strip with 0 badges, 4 badges, and after the credits
    states = [("0 badges", news_pool(0)), ("4 badges, rail open", news_pool(4, {"FLAG_TOSA_RAIL_OPEN"})),
              ("Champion", news_pool(8, {"FLAG_SYS_GAME_CLEAR", "FLAG_TOSA_RAIL_OPEN", "FLAG_COLD_STORAGE_DONE"}))]
    pick = ["Rookie", "Halfway", "A new Champion"]          # lead each strip with the headline that state unlocks
    states = [(n, sorted(pl, key=lambda t, w=w: not t.startswith(w))) for (n, pl), w in zip(states, pick)]
    strip = Image.new("RGB", (W, 18 * len(states)), (0, 0, 0))
    for k, (_, pool) in enumerate(states):
        strip.paste(frame(0, pool=pool).convert("RGB").crop((0, 29, W, 47)), (0, 18 * k))
    strip.save(os.path.join(outdir, "05_news_states.png"))
    big = [K.upscale(fr.convert("RGB"), 2) for fr in frames]
    big[0].save(os.path.join(outdir, "phone.gif"), save_all=True, append_images=big[1:], duration=50, loop=0)
    for p in os.listdir(outdir):
        if p.endswith(".png") and not p.startswith("x3_"):
            K.upscale(Image.open(os.path.join(outdir, p)).convert("RGB"), 3).save(os.path.join(outdir, "x3_" + p))


if __name__ == "__main__":
    main(sys.argv[1])
