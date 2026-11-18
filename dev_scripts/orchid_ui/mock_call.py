"""CALL app mockups (Rotom Phone): contact list, contact card, in-call. usage: mock_call.py OUT_DIR"""
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
import windows as Wn
from gamefont import draw_text, text_width

W, H = 240, 160
G = K.G


class Sheet:
    def __init__(self, theme="male", w=W, h=H):
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


X.SIL.update({
    "phone": [".XX.....", "XXX.....", "XXX.....", ".XX.....", ".XXX....", "..XXX.XX", "...XXXXX", "....XXX."],
    "rematch": ["..XXX..", ".XXXXX.", "XXXXXXX", "X..X..X", "XXXXXXX", ".XXXXX.", "..XXX.."],
    "new": ["XX", "XX", "XX", "XX", "..", "XX"],
    "home": ["...X...", "..XXX..", ".XXXXX.", "XXXXXXX", ".XX.XX.", ".XX.XX.", ".XXXXX."],
})
TAG = {"rematch": ((152, 40, 72), (216, 88, 112), (240, 152, 168)),
       "new": ((136, 96, 24), (200, 152, 48), (240, 208, 120)),
       "home": ((40, 104, 64), (72, 160, 88), (144, 208, 136))}

# name, OW sprite, front pic (None = OW only), location, state, profile, call line
CONTACTS = [
    ("MOM", "mom", None, "Tosa Port", "home", "Always happy to hear\nfrom you, dear!",
     "MOM: Are you eating properly?\nDon't forget to rest your POKéMON!"),
    ("FISHER BOON", "fisherman", "fisherman", "Tosa Pier", "rematch", "Fishes off Tosa Pier\nevery dawn.",
     "BOON: Oi! The Torpesquid are\nbiting tonight. Come battle me!"),
    ("LASS MEI", "lass", "lass", "Telok Town", None, "Collects cute POKéMON and\nkopi-shop stickers.",
     "MEI: I caught a Pinguin today!\nIt's sooo round. Bye-bye!"),
    ("HIKER ARJUN", "hiker", "hiker", "S. Tosa Reserve", "new", "Walks the Reserve trails.\nKnows every shortcut.",
     "ARJUN: Ho! I found a new trail\npast the Reserve gate!"),
    ("YOUNGSTER DANI", "youngster", "youngster", "Tosa Port", None, "Practises battling by the\nferry terminal.",
     "DANI: My team's way stronger now!\nYou'd better watch out!"),
    ("PICNICKER JO", "picnicker", "picnicker", "Telok Town", None, "Picnics by the river with\nher Iyepure.",
     "JO: The river's so pretty today.\nYou should come for a picnic!"),
]


def ow_head(name):
    im = Image.open(G("object_events", "pics", "people", name + ".png")).crop((0, 0, 16, 32))
    rgba = K.sheet_rgba(im)
    return rgba.crop((0, 10, 16, 26))


def front_pic(name):
    return K.sheet_rgba(Image.open(G("trainers", "front_pics", name + ".png")))


def tag(s, x, y, state):
    dk, fc, lt = TAG[state]
    c = s.c
    rounded_box(s.cv, x, y, 18, 12, 3, c(fc), INK, c(lt), c(dk))
    X.centred_sil(s.cv, x + 1, y + 1, 16, 10, state, WHITE, c(dk))


def header(s, title, right=None):
    cv = s.cv
    D.header_band(cv, 0, 239, round_left=False)
    rounded_box(cv, 4, 2, 14, 12, 3, ACCENT_LIGHT, INK, WHITE, ACCENT)
    X.centred_sil(cv, 5, 3, 13, 10, "phone", ACCENT_DARK, None)
    draw_text(cv, 23, 0, title, WHITE, ACCENT_DARK)
    if right:
        draw_text(cv, 236 - text_width(right, "narrow"), 0, right, WHITE, ACCENT_DARK, font="narrow")


def hint(cv, x, y, key, label):
    w = X.keypad(cv, x, y + 4, key)
    draw_text(cv, x + w + 3, y, label, INK_SOFT, PANEL_SHADE, font="narrow")
    return x + w + 3 + text_width(label, "narrow") + 8


ROW_Y, ROW_H, ROWS = 20, 18, 5


def screen_list(cursor=1):
    s = Sheet()
    cv = s.cv
    header(s, "CALL", "%d contacts" % len(CONTACTS))
    heads = []
    for r in range(ROWS):
        n, ow, pic, loc, state = CONTACTS[r][:5]
        y = ROW_Y + r * ROW_H
        sel = r == cursor
        if sel:
            rounded_box(cv, 8, y, 218, 16, 4, SELECT, INK, SELECT_LIGHT, SELECT_DARK)
        else:
            rounded_box(cv, 8, y, 218, 16, 4, PANEL, INK, WHITE, PANEL_SHADE)
        heads.append((ow, 12, y - 1))
        draw_text(cv, 33, y, n, INK, SELECT_DARK if sel else PANEL_SHADE)
        lw = text_width(loc, "narrow")
        draw_text(cv, 200 - lw, y, loc, INK_SOFT, SELECT_DARK if sel else PANEL_SHADE, font="narrow")
        if state:
            tag(s, 204, y + 2, state)
    D.track(cv, 230, ROW_Y, 236, ROW_Y + ROWS * ROW_H - 3)
    rounded_box(cv, 231, ROW_Y + 1, 5, 60, 1, SELECT, INK, SELECT_LIGHT, SELECT_DARK)
    # tray
    D.tray(cv, 114)
    c = CONTACTS[cursor]
    X.label_pill(cv, 8, 119, 14 + X.CAP_W + text_width(c[3], "narrow"), "pin")
    draw_text(cv, 8 + X.CAP_W + 4, 118, c[3], INK, PANEL_SHADE, font="narrow")
    status = {"rematch": "Ready for a rematch!", "new": "New message!", "home": "Home"}.get(c[4], "")
    if status:
        draw_text(cv, 236 - text_width(status, "narrow"), 118, status, s.c(TAG[c[4]][0]), PANEL_SHADE, font="narrow")
    draw_text(cv, 8, 130, c[5], INK, PANEL_SHADE, line_h=14)
    out = K.grid_frame(3)
    out.alpha_composite(s.rgba())
    for ow, x, y in heads:
        out.alpha_composite(ow_head(ow), (x, y + 1))
    return out


def screen_card(idx=1, button=0):
    c = CONTACTS[idx]
    s = Sheet()
    cv = s.cv
    header(s, "CALL")
    # portrait well (dais) left
    rounded_box(cv, 6, 20, 76, 92, 4, PANEL, INK, WHITE, PANEL_SHADE)
    disc(cv, 44, 62, 33, PANEL_SHADE, INK)
    disc(cv, 44, 62, 31, ACCENT_PALE, None)
    disc(cv, 43, 61, 26, WHITE, None)
    ring(cv, 44, 62, 32, ACCENT_LIGHT)
    # info panel right
    rounded_box(cv, 86, 20, 150, 92, 4, PANEL, INK, WHITE, PANEL_SHADE)
    draw_text(cv, 92, 20, c[0], INK, PANEL_SHADE)
    X.label_pill(cv, 92, 38, 14 + X.CAP_W + text_width(c[3], "narrow"), "pin")
    draw_text(cv, 92 + X.CAP_W + 4, 37, c[3], INK, PANEL_SHADE, font="narrow")
    cv.hline(92, 230, 55, PANEL_SHADE)
    cv.hline(92, 230, 56, WHITE)
    draw_text(cv, 92, 57, c[5], INK, PANEL_SHADE, line_h=14)
    # rematch strip
    if c[4] == "rematch":
        dk, fc, lt = TAG["rematch"]
        rounded_box(cv, 92, 92, 138, 15, 4, s.c(fc), INK, s.c(lt), s.c(dk))
        draw_text(cv, 98, 91, "Wants a rematch!", WHITE, s.c(dk), font="narrow")
    # buttons
    for i, (lab, key) in enumerate((("CALL", "phone"), ("BACK", None))):
        x = 8 + i * 116
        sel = i == button
        if sel:
            rounded_box(cv, x, 118, 108, 22, 5 if False else 4, SELECT, INK, SELECT_LIGHT, SELECT_DARK)
        else:
            rounded_box(cv, x, 118, 108, 22, 4, PANEL, INK, WHITE, PANEL_SHADE)
        if key:
            rounded_box(cv, x + 6, 122, 18, 14, 3, ACCENT, INK, ACCENT_LIGHT, ACCENT_DARK)
            X.centred_sil(cv, x + 7, 123, 17, 12, "phone", WHITE, ACCENT_DARK)
        else:
            X.b_disc(cv, x + 15, 129)
        draw_text(cv, x + 32, 121, lab, INK, SELECT_DARK if sel else PANEL_SHADE)
    hint(cv, 8, 144, "A", "Select")
    out = K.grid_frame(3)
    out.alpha_composite(s.rgba())
    if c[2]:
        p = front_pic(c[2])
        out.alpha_composite(p, (44 - 32, 62 - 34))
    else:
        out.alpha_composite(K.upscale(ow_head(c[1]), 2), (44 - 16, 62 - 16))
    return out


def screen_calling(idx=1, phase=0, talking=True):
    c = CONTACTS[idx]
    s = Sheet()
    cv = s.cv
    header(s, "CALL", "0:%02d" % (4 + phase // 10) if talking else "Calling…")
    # pulsing rings round the portrait
    cx, cy = 120, 58
    if not talking:
        for k in range(3):
            r = 30 + ((phase * 2 + k * 8) % 24)
            if cy - r > 17:
                ring(cv, cx, cy, r, ACCENT_LIGHT if r < 40 else ACCENT)
    disc(cv, cx, cy, 30, ACCENT, INK)
    disc(cv, cx, cy, 27, WHITE, INK)
    disc(cv, cx - 1, cy - 1, 25, ACCENT_PALE, None)
    nw = text_width(c[0])
    rounded_box(cv, cx - nw // 2 - 8, 92, nw + 16, 14, 4, PANEL, INK, WHITE, PANEL_SHADE)
    draw_text(cv, cx - nw // 2, 91, c[0], INK, PANEL_SHADE)
    if not talking:
        dots = "Calling" + "." * (1 + (phase // 6) % 3)
        draw_text(cv, cx - text_width("Calling...", "narrow") // 2, 106, dots, WHITE, INK_SOFT, font="narrow")
    # hang-up hint
    out = K.grid_frame(3)
    out.alpha_composite(s.rgba())
    if c[2]:
        p = front_pic(c[2]).crop((8, 2, 56, 50))
        mask = Image.new("L", p.size, 0)
        mp = mask.load()
        for y in range(48):
            for x in range(48):
                if (x - 23.5) ** 2 + (y - 23.5) ** 2 <= 24.5 ** 2:
                    mp[x, y] = 255
        p2 = Image.new("RGBA", p.size, (0, 0, 0, 0))
        p2.paste(p, (0, 0), Image.composite(p.split()[3], mask, mask).point(lambda v: 255 if v > 0 else 0))
        out.alpha_composite(p2, (cx - 24, cy - 24))
    if talking:
        def fn(cv2):
            Wn.dialogue_box(cv2, 2, 15, 27, 4)
            draw_text(cv2, 16, 120, c[6], INK, PANEL_SHADE)
        K.layer(out, fn, "male")
    else:
        def fn2(cv2):
            hint(cv2, 96, 140, "B", "Hang up")
        K.layer(out, fn2, "male")
    return out


def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    shots = {"30_call_list": screen_list(1), "31_call_card": screen_card(1), "32_call_ringing": screen_calling(1, 6, False),
             "33_call_talk": screen_calling(1, 0, True)}
    for k, im in shots.items():
        im.save(os.path.join(outdir, k + ".png"))
        K.upscale(im.convert("RGB"), 3).save(os.path.join(outdir, "x3_" + k + ".png"))
    frames = [screen_list(0)] * 10 + [screen_list(1)] * 14 + [screen_card(1)] * 16
    frames += [screen_calling(1, k, False) for k in range(36)]
    frames += [screen_calling(1, k, True) for k in range(0, 40, 2)]
    big = [K.upscale(f.convert("RGB"), 2) for f in frames]
    big[0].save(os.path.join(outdir, "call.gif"), save_all=True, append_images=big[1:], duration=66, loop=0)


if __name__ == "__main__":
    main(sys.argv[1])
