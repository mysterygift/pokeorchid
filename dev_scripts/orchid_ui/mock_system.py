"""
Save prompt + start menu polish mockups (shared windows -> Orchid theme; the player's name
uses the gender name colour, patched into SPARE_A/B of the std window palette).

States
  05 save card + "Would you like to save the game?" + YES/NO
  06 overwrite prompt          07 SAVING... (wobbling Poké Ball OBJ)     08 saved
  09 polished start menu       10 before/after sheet (approved vs polished, Safari, Pyramid)
usage: mock_system.py OUT_DIR
"""
import os
import sys
from PIL import Image
from kit import *
import kit_ext as K
import windows as Wn
import system_ext as X
from gamefont import draw_text, text_width

W, H = 240, 160
SAVE = dict(location="Tosa Port", name="KAITO", badges=1, dex=12, time="4:27")
MSG_CONFIRM = "Would you like to save the game?"
MSG_OVERWRITE = "There is already a saved file.\nIs it okay to overwrite it?"
MSG_SAVING = "SAVING…\nDON'T TURN OFF THE POWER."


def ball_at(msg):
    """Saving ball OBJ (16x16) sits right after the first message line."""
    return 16 + text_width(msg.split("\n")[0]) + 4, 119


# ================================================================== save prompt
def render_save(msg, yesno=None, ball=None, sparkles=False, gender="M", name=None, arrow=False):
    out = X.field_scene(show_player=False)          # the save card covers the player
    data = dict(SAVE, name=name or SAVE["name"])
    K.layer(out, lambda cv: X.save_card(cv, data), "orchid", **X.std_pal_kw(gender))
    X.message(out, msg, gender)
    if yesno is not None:
        X.yes_no(out, yesno)
    if ball is not None:
        out.alpha_composite(X.pokeball_frame(ball), ball_at(msg))
    if sparkles:
        for (dx, dy, big) in ((-5, -2, True), (17, -1, False), (16, 9, True)):
            X.sparkle(out, ball_at(msg)[0] + dx, ball_at(msg)[1] + dy, big)
    if arrow:
        last = msg.split("\n")[-1]
        X.down_arrow(out, 16 + text_width(last) + 3, 120 + 16 * msg.count("\n") + 6)
    return out


def saving_gif(path):
    """SAVING...: ball wobbles like a capture (3 rocks), then clicks + sparkles = saved."""
    frames = []
    seq = []
    for k in range(3):                                   # one rock = 24 GBA frames
        for f in range(24):
            import math
            seq.append(("rock", 30 * math.sin(f / 24 * 2 * math.pi)))
        seq += [("rock", 0)] * 10
    seq += [("click", 0)] * 8
    seq += [("saved", 0)] * 70
    for i in range(0, len(seq), 2):
        kind, ang = seq[i]
        if kind == "saved":
            im = render_save(SAVE["name"] + " saved the game.", ball=0, sparkles=(i // 8) % 2 == 0 or i > len(seq) - 40)
        else:
            im = render_save(MSG_SAVING, ball=round(ang / 15) * 15, sparkles=(kind == "click"))
        frames.append(K.upscale(im.convert("RGB"), 2))
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=33, loop=0, optimize=False)


# ================================================================== start menu
NORMAL = ["POKéDEX", "POKéMON", "BAG", "POKéNAV", "PLAYER", "SAVE", "OPTION", "EXIT"]
SAFARI = ["RETIRE", "POKéDEX", "POKéMON", "BAG", "PLAYER", "OPTION", "EXIT"]
PYRAMID = ["POKéMON", "BAG", "PLAYER", "REST", "RETIRE"]
MX, MW = 20, 9                          # approved: window tiles x 20..28


def start_menu(out, entries, cursor, gender="M", name="KAITO", polished=True, bob=-1):
    n = len(entries)

    def fn(cv):
        Wn.std_frame(cv, MX, 1, MW, n * 2)
        for i, e in enumerate(entries):
            y = 8 + i * 16
            if i == cursor:
                Wn.selection_bar(cv, MX * 8 + 2, y + 1, MW * 8 - 4, 14)
            if e == "PLAYER":
                if polished:
                    draw_text(cv, MX * 8 + 22, y, name, SPARE_A, SPARE_B)
                else:
                    draw_text(cv, MX * 8 + 22, y, name, INK, PANEL_SHADE)
            else:
                draw_text(cv, MX * 8 + 22, y, e, INK, PANEL_SHADE)
    K.layer(out, fn, "orchid", **X.std_pal_kw(gender))
    for i, e in enumerate(entries):
        sel = i == cursor
        muted = 0.0 if (sel or not polished) else 0.35
        dy = bob if (sel and polished) else 0
        out.alpha_composite(X.menu_icon(e, muted), (MX * 8 + 4, 8 + i * 16 + dy))


def chip_location(out, loc="Tosa Port"):
    def fn(cv):
        Wn.std_frame(cv, 1, 1, 10, 2)
        X.label_pill(cv, 8, 9, 80, "pin")
        draw_text(cv, 8 + X.CAP_W + 4, 8, loc, INK, PANEL_SHADE)
    K.layer(out, fn, "orchid")


def chip_safari(out, balls=30):
    def fn(cv):
        Wn.std_frame(cv, 1, 1, 11, 4)
        draw_text(cv, 36, 8, "SAFARI BALLS", INK, PANEL_SHADE, font="narrow")
        draw_text(cv, 36, 22, "×%d" % balls, INK, PANEL_SHADE)
        # recessed icon well behind the item icon
        disc(cv, 20, 23.5, 12, PANEL, INK, PANEL_SHADE, WHITE)
    K.layer(out, fn, "orchid")
    out.alpha_composite(K.item_icon("safari_ball"), (8, 12))


def chip_pyramid(out, floor=3):
    def fn(cv):
        Wn.std_frame(cv, 1, 1, 12, 4)
        draw_text(cv, 8, 6, "Battle Pyramid", INK, PANEL_SHADE)
        # 7 floor pips: cleared = gold, current = gold ring, ahead = recessed
        for k in range(7):
            cx, cy = 12 + k * 9, 29.5
            if k < floor - 1:
                disc(cv, cx, cy, 3.6, SELECT, INK, SELECT_LIGHT, SELECT_DARK)
            elif k == floor - 1:
                disc(cv, cx, cy, 3.6, ACCENT, INK, ACCENT_LIGHT, ACCENT_DARK)
            else:
                disc(cv, cx, cy, 3.6, PANEL_SHADE, INK, PANEL_DARK, WHITE)
        draw_text(cv, 75, 22, "Floor %d" % floor, INK, PANEL_SHADE, font="narrow")
    K.layer(out, fn, "orchid")


def render_start(entries=NORMAL, cursor=2, gender="M", polished=True, chip="location", name=None):
    out = X.field_scene("brendan" if gender == "M" else "may")
    name = name or ("KAITO" if gender == "M" else "MAY")
    if polished and chip == "location":
        chip_location(out)
    elif chip == "safari":
        chip_safari(out)
    elif chip == "pyramid":
        chip_pyramid(out)
    start_menu(out, entries, cursor, gender, name, polished)
    return out


# ================================================================== parts
def parts():
    from PIL import ImageDraw
    sc = 4
    out = Image.new("RGBA", (1000, 1000), (28, 28, 36, 255))
    d = ImageDraw.Draw(out)

    def put(img, x, y, cap):
        d.text((x, y), cap, fill=(230, 230, 240))
        out.paste(K.upscale(img, sc), (x, y + 14))
        return y + 14 + img.size[1] * sc + 14

    y = 10
    card = render_save(MSG_CONFIRM, 0).crop((0, 0, 128, 96))
    y2 = put(card, 10, y, "Save card: std window 14x10, location band + label pills (accent cap, white pictogram)")
    # pictograms
    pic = Image.new("RGBA", (5 * 22, 16), (0, 0, 0, 0))

    def pics(cv):
        for k, key in enumerate(["pin", "player", "badge", "dex", "clock"]):
            rounded_box(cv, k * 22, 1, 18, 14, 3, ACCENT, INK, ACCENT_LIGHT, ACCENT_DARK)
            X.centred_sil(cv, k * 22 + 1, 2, 16, 12, key, WHITE, ACCENT_DARK)
    K.layer(pic, pics, "orchid")
    put(pic, 540, y, "Pictograms: location / player / badges / caught / time")
    balls = Image.new("RGBA", (6 * 18, 16), (0, 0, 0, 0))
    for k, a in enumerate((-30, -15, 0, 15, 30)):
        balls.alpha_composite(X.pokeball_frame(a), (k * 18, 0))
    X.sparkle(balls, 5 * 18, 0, True)
    X.sparkle(balls, 5 * 18 + 8, 8, False)
    put(balls, 540, y + 120, "Saving ball OBJ 16x16 (start-menu icon palette): 5 tilt frames + sparkle")
    y = y2
    m = render_start().crop((150, 0, 240, 150))
    put(m, 10, y, "Polished start menu: muted resting icons, lifted selection, name colour")
    chip = render_start().crop((0, 0, 90, 34))
    put(chip, 440, y, "Location chip (std window 10x2)")
    s = render_start(SAFARI, 0, "F", chip="safari").crop((0, 0, 98, 50))
    put(s, 440, y + 180, "Safari chip: real safari_ball item icon in a well")
    return out


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    up = lambda im, name: K.upscale(im, 3).save(os.path.join(out_dir, name))
    up(render_save(MSG_CONFIRM, yesno=0), "state_05.png")
    up(render_save(MSG_OVERWRITE, yesno=0), "state_06.png")
    up(render_save(MSG_SAVING, ball=-30), "state_07.png")
    up(render_save(SAVE["name"] + " saved the game.", ball=0, sparkles=True), "state_08.png")
    up(render_start(), "state_09.png")
    sheet = X.sheet_grid([
        ("Approved (review 1)", render_start(polished=False, chip=None)),
        ("Polished: muted resting icons, lifted selection, name colour, location chip", render_start()),
        ("Polished, Safari Zone (female): RETIRE row + SAFARI BALLS chip", render_start(SAFARI, 0, "F", chip="safari")),
        ("Polished, Battle Pyramid: REST / RETIRE rows + floor chip", render_start(PYRAMID, 3, chip="pyramid")),
    ], 2)
    sheet.save(os.path.join(out_dir, "state_10.png"))
    # parts.png = options parts on top of save / start-menu parts (each cropped to content)
    import mock_options
    from PIL import ImageChops
    ims = []
    for im in (mock_options.parts(), parts()):
        bg = Image.new("RGBA", im.size, (28, 28, 36, 255))
        x0, y0, x1, y1 = ImageChops.difference(im.convert("RGB"), bg.convert("RGB")).getbbox()
        ims.append(im.crop((0, 0, max(x1 + 10, 600), y1 + 10)))
    sheet = Image.new("RGBA", (max(i.size[0] for i in ims), sum(i.size[1] for i in ims)), (28, 28, 36, 255))
    sheet.paste(ims[0], (0, 0))
    sheet.paste(ims[1], (0, ims[0].size[1]))
    sheet.save(os.path.join(out_dir, "parts.png"))
    saving_gif(os.path.join(out_dir, "saving.gif"))


if __name__ == "__main__":
    main(sys.argv[1])
