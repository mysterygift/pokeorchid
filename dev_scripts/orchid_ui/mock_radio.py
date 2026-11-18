"""RADIO app + field 'now playing' toast mockups (Rotom Phone slot 4). usage: mock_radio.py OUT_DIR"""
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
kit.THEMES["teal"] = [(24, 104, 120), (48, 160, 168), (120, 208, 208), (200, 240, 240)]


class Sheet:
    def __init__(self, theme="teal", w=W, h=H):
        self.cols = list(kit.palette(theme))
        self.cols[0] = (1, 2, 3)
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


SCR, SCR_DEEP, SCR_GLARE = (40, 40, 52), (24, 24, 32), (56, 56, 72)
NEEDLE = ((248, 80, 0), (128, 32, 0))           # Gen 3 red (chevron colours)
LCD = (120, 232, 184)                            # tuner digits

# name, freq, region, accent (dark, face, light), tagline, now playing, songs available now?
STATIONS = [
    ("TOSA FM", 88.4, "Tosa", ((96, 48, 128), (152, 88, 184), (200, 152, 224)),
     "Home of Tosa's hits!", "Tosa Port", True),
    ("HOENN FM", 91.3, "Hoenn", ((32, 80, 136), (64, 128, 200), (136, 184, 232)),
     "Sun, sea and Route 104.", "Route 104", True),
    ("KANTO GOLD", 98.1, "Kanto", ((152, 40, 72), (216, 88, 112), (240, 152, 168)),
     "The classics, all day.", "Route 1", True),
    ("RADIO UNOVA", 105.2, "Unova", ((40, 40, 64), (96, 96, 120), (160, 160, 184)),
     "Big city sounds.", "Route 10", False),
    ("ABSOLUTE GALAR", 107.7, "Galar", ((136, 96, 24), (200, 152, 48), (240, 208, 120)),
     "Galar's biggest anthems.", "Motostoke", False),
]
F_MIN, F_MAX = 87.5, 108.0


def fx(f):
    return 14 + round((f - F_MIN) / (F_MAX - F_MIN) * 211)


def mini_note(cv, x, y, c):
    stamp(cv, x, y, ["..XXX", "..X.X", "..X.X", "XXX.X", "XXXXX", "XX..."][:0] or
          ["...XXX", "...XXX", "...X..", "...X..", ".XXX..", "XXXX..", ".XX..."], {"X": c})


def screen(sel=1, on=True, eq=0, tune_x=None):
    s = Sheet()
    cv, c = s.cv, s.c
    st = STATIONS[sel]
    dk, fc, lt = st[3]
    # header
    D.header_band(cv, 0, 239, round_left=False)
    rounded_box(cv, 4, 2, 14, 12, 3, ACCENT_LIGHT, INK, WHITE, ACCENT)
    stamp(cv, 7, 4, ["....X.", "...X..", "XXXXXX", "X.X.XX", "XX.XXX", "XXXXXX", "X....X"],
          {"X": ACCENT_DARK})
    draw_text(cv, 23, 0, "RADIO", WHITE, ACCENT_DARK)
    # on/off switch pill
    if on:
        rounded_box(cv, 200, 2, 36, 12, 4, SELECT, INK, SELECT_LIGHT, SELECT_DARK)
        draw_text(cv, 210, -1, "ON", INK, SELECT_DARK, font="narrow")
        disc(cv, 229, 7.5, 3.5, WHITE, INK)
    else:
        rounded_box(cv, 200, 2, 36, 12, 4, PANEL_DARK, INK, PANEL_SHADE, INK_SOFT)
        disc(cv, 206, 7.5, 3.5, WHITE, INK)
        draw_text(cv, 213, -1, "OFF", WHITE, INK_SOFT, font="narrow")

    # tuner display (dark LCD panel)
    rounded_box(cv, 4, 20, 232, 58, 4, c(SCR), INK, c(SCR_GLARE), c(SCR_DEEP))
    # frequency digits
    f = "%.1f" % st[1]
    on_c = c(LCD) if on else c((88, 96, 104))
    draw_text(cv, 12, 20, f, on_c, c(SCR_DEEP))
    draw_text(cv, 14 + text_width(f), 22, "MHz", c((88, 160, 128)) if on else c((72, 80, 88)), None, font="small")
    draw_text(cv, 228 - text_width(st[0]), 20, st[0], WHITE if on else c((120, 120, 136)), c(SCR_DEEP))
    # scale
    for k in range(0, 42):
        fr = F_MIN + k * 0.5
        x = fx(fr)
        tall = abs(fr - round(fr)) < 0.01 and int(round(fr)) % 4 == 0
        cv.vline(x, 60 - (6 if tall else 3), 60, c((88, 96, 112)))
    cv.hline(10, 229, 61, c((88, 96, 112)))
    for i, s2 in enumerate(STATIONS):
        x = fx(s2[1])
        dot = s2[3][1] if (i == sel) else (88, 96, 112)
        disc(cv, x, 47.5, 2.5, c(dot), INK if i == sel else None)
    for fr in (88, 92, 96, 100, 104, 108):
        lab = str(fr)
        draw_text(cv, fx(fr) - text_width(lab, "small") // 2, 61, lab, c((120, 128, 144)), None, font="small")
    # needle
    nx = tune_x if tune_x is not None else fx(st[1])
    cv.vline(nx, 40, 63, c(NEEDLE[0]))
    cv.vline(nx + 1, 40, 63, c(NEEDLE[1]))
    cv.rect(nx - 1, 38, nx + 2, 40, c(NEEDLE[0]))

    # station card
    rounded_box(cv, 4, 82, 232, 30, 4, PANEL, INK, WHITE, PANEL_SHADE)
    rounded_box(cv, 8, 86, 48, 22, 3, c(fc), INK, c(lt), c(dk))       # region plate
    draw_text(cv, 32 - text_width(st[2], "narrow") // 2, 89, st[2], WHITE, c(dk), font="narrow")
    draw_text(cv, 62, 81, st[0], INK, PANEL_SHADE)
    draw_text(cv, 62, 95, st[4], INK_SOFT, PANEL_SHADE, font="narrow")
    if not st[6]:
        draw_text(cv, 228 - text_width("needs import", "small"), 81, "needs import", c((216, 88, 112)), None, font="small")

    # now playing tray
    D.tray(cv, 116)
    disc(cv, 20, 139, 16, PANEL_SHADE, None)
    disc(cv, 20, 139, 15, WHITE, INK)
    disc(cv, 20.5, 139.5, 13, PANEL, None)
    # equaliser bars in the well
    heights = [[4, 8, 6, 10, 5], [7, 5, 10, 6, 8], [9, 6, 4, 8, 10], [5, 10, 7, 4, 6]][eq % 4] if on else [1] * 5
    for k, hgt in enumerate(heights):
        x = 11 + k * 4
        cv.rect(x, 145 - hgt, x + 2, 145, c(fc) if on else PANEL_SHADE)
        cv.hline(x, x + 2, 145 - hgt, c(lt) if on else PANEL_SHADE)
    cv.vline(40, 122, 154, PANEL_SHADE)
    cv.vline(41, 122, 154, WHITE)
    if on:
        draw_text(cv, 47, 118, "Now playing", INK_SOFT, PANEL_SHADE, font="narrow")
        mini_note(cv, 47, 137, c(fc))
        draw_text(cv, 56, 132, st[5], INK, PANEL_SHADE)
    else:
        draw_text(cv, 47, 118, "Radio off", INK_SOFT, PANEL_SHADE, font="narrow")
        draw_text(cv, 47, 132, "Map music plays.", INK, PANEL_SHADE)
    # hints
    cv.set(0, 0, 0)
    x = 236 - text_width("Tune", "narrow")
    draw_text(cv, x, 118, "Tune", INK_SOFT, PANEL_SHADE, font="narrow")
    X.chevron  # (chevrons drawn as OBJ below)
    X.keypad(cv, 236 - text_width("On/Off", "narrow") - 12, 140, "A")
    draw_text(cv, 236 - text_width("On/Off", "narrow"), 136, "On/Off", INK_SOFT, PANEL_SHADE, font="narrow")
    out = K.grid_frame(3)
    out.alpha_composite(s.rgba())
    D.chevron(out, x - 16, 126)
    D.chevron(out, x - 7, 126, right=True)
    return out


def field_toast(sel=3, slide=0):
    """On the field: map-popup-style card top-left when a new song starts."""
    out = X.field_scene()
    st = STATIONS[sel]
    s = Sheet("teal")
    cv, c = s.cv, s.c
    dk, fc, lt = st[3]
    y0 = -28 + slide
    w = 12 + 26 + max(text_width(st[0], "narrow"), text_width(st[5])) + 8
    rounded_box(cv, 2, y0 + 2, w, 28, 4, PANEL, INK, WHITE, PANEL_SHADE)
    rounded_box(cv, 6, y0 + 6, 20, 20, 3, c(fc), INK, c(lt), c(dk))
    stamp(cv, 11, y0 + 9, ["...XXXX", "...XXXX", "...X..X", "...X..X", ".XXX.XX", "XXXX.XX", ".XX...."],
          {"X": WHITE})
    draw_text(cv, 31, y0 + 1, st[0], INK_SOFT, PANEL_SHADE, font="narrow")
    draw_text(cv, 31, y0 + 13, st[5], INK, PANEL_SHADE)
    out.alpha_composite(s.rgba())
    return out


def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    shots = {"20_radio_hoenn": screen(1), "21_radio_unova": screen(3), "22_radio_off": screen(1, on=False),
             "23_field_toast": field_toast(3, 28)}
    for k, im in shots.items():
        im.save(os.path.join(outdir, k + ".png"))
        K.upscale(im.convert("RGB"), 3).save(os.path.join(outdir, "x3_" + k + ".png"))
    frames = [screen(1, eq=k // 3) for k in range(18)]
    # tune right: needle sweeps 91.3 -> 98.1 -> 105.2
    for a, b, nxt in ((1, 2, 2), (2, 3, 3)):
        x0, x1 = fx(STATIONS[a][1]), fx(STATIONS[b][1])
        for k in range(8):
            frames.append(screen(a if k < 4 else b, eq=k, tune_x=round(x0 + (x1 - x0) * (1 - (1 - (k + 1) / 8) ** 2))))
        frames += [screen(nxt, eq=k // 3) for k in range(12)]
    frames += [screen(3, on=False)] * 10 + [screen(3, eq=k // 3) for k in range(12)]
    for k in range(0, 29, 4):
        frames.append(field_toast(3, k))
    frames += [field_toast(3, 28)] * 20
    big = [K.upscale(f.convert("RGB"), 2) for f in frames]
    big[0].save(os.path.join(outdir, "radio.gif"), save_all=True, append_images=big[1:], duration=66, loop=0)


if __name__ == "__main__":
    main(sys.argv[1])
