"""
Location pill with a weather cap: the left cap's colour + white symbol follow the current overworld weather.
Approved 2026-11-17; export_system.py builds the caps and ramps from STYLES.
usage: mock_weather_pill.py OUT_DIR
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mock_start_v2 as V  # noqa: E402  (sets up the kit path)
from PIL import Image, ImageDraw  # noqa: E402
import kit  # noqa: E402
from kit import *  # noqa: E402,F401
import kit_ext as K  # noqa: E402
import system_ext as X  # noqa: E402
from gamefont import draw_text, text_width  # noqa: E402
import mock_system as M  # noqa: E402

# key: (label, (dark, face, light), symbol rows, weathers it covers)
STYLES = {
    "clear": ("Clear", ((48, 120, 48), (88, 176, 72), (160, 216, 120)), [
        "....X....",
        ".X.....X.",
        "...XXX...",
        "..XXXXX..",
        "X.XXXXX.X",
        "..XXXXX..",
        "...XXX...",
        ".X.....X.",
        "....X....",
    ], "NONE, SUNNY, SUNNY_CLOUDS (normal outdoor weather)"),
    "sun": ("Harsh sun", ((152, 40, 40), (224, 72, 48), (248, 152, 96)), [
        ".....X.....",
        ".X...X...X.",
        "..X.....X..",
        "....XXX....",
        "...XXXXX...",
        "XX.XXXXX.XX",
        "...XXXXX...",
        "....XXX....",
        "..X.....X..",
        ".X...X...X.",
        ".....X.....",
    ], "DROUGHT"),
    "rain": ("Rain", ((32, 64, 144), (56, 112, 216), (120, 176, 248)), [
        "...X...",
        "..XXX..",
        "..XXX..",
        ".XXXXX.",
        "XXXXXXX",
        "XXXXXXX",
        ".XXXXX.",
        "..XXX..",
    ], "RAIN, DOWNPOUR"),
    "storm": ("Thunderstorm", ((40, 40, 104), (72, 72, 168), (136, 136, 224)), [
        "...XXXX",
        "..XXXX.",
        ".XXXX..",
        "XXXXXXX",
        "...XXX.",
        "..XXX..",
        "..XX...",
        ".XX....",
        ".X.....",
    ], "RAIN_THUNDERSTORM"),
    "snow": ("Snow", ((56, 128, 184), (104, 184, 232), (184, 224, 248)), [
        "....X....",
        ".X..X..X.",
        "..X.X.X..",
        "...XXX...",
        "XXXXXXXXX",
        "...XXX...",
        "..X.X.X..",
        ".X..X..X.",
        "....X....",
    ], "SNOW"),
    "fog": ("Mist / fog", ((88, 88, 104), (144, 144, 160), (200, 200, 208)), [
        ".XXXXXX...",
        "..........",
        "...XXXXXXX",
        "..........",
        "XXXXXXX...",
        "..........",
        "..XXXXXX..",
    ], "FOG_HORIZONTAL, FOG_DIAGONAL, FOG"),
    "smog": ("Toxic smog", ((88, 32, 112), (136, 56, 160), (192, 120, 216)), [
        "..XXXXX..",
        ".XXXXXXX.",
        "XX..X..XX",
        "XX..X..XX",
        ".XXXXXXX.",
        "..XX.XX..",
        "..X.X.X..",
    ], "THICK_SMOG"),
    "sand": ("Sandstorm", ((112, 72, 32), (176, 128, 72), (224, 184, 120)), [
        "XXXXXX.X..",
        "......XX..",
        ".XXXXXXX.X",
        ".........X",
        "XXXXXXXXX.",
        ".......X..",
        "..XXXXX..X",
    ], "SANDSTORM"),
    "ash": ("Volcanic ash", ((56, 48, 48), (104, 96, 96), (160, 152, 144)), [
        "..XXX....",
        ".XXXXXXX.",
        "XXXXXXXXX",
        ".XXXXXXX.",
        ".........",
        "X..X..X..",
        ".X..X..X.",
    ], "VOLCANIC_ASH"),
    "cloud": ("Overcast", ((72, 88, 104), (112, 136, 152), (168, 192, 200)), [
        "...XXX....",
        "..XXXXX.X.",
        ".XXXXXXXXX",
        "XXXXXXXXXX",
        "XXXXXXXXXX",
        ".XXXXXXXX.",
    ], "SHADE"),
    "water": ("Underwater", ((24, 96, 112), (40, 152, 160), (104, 208, 208)), [
        "......XXX.",
        ".....X...X",
        ".....X...X",
        "..XX..XXX.",
        ".X..X.....",
        ".X..X.....",
        "..XX....X.",
        ".......X.X",
        "........X.",
    ], "UNDERWATER, UNDERWATER_BUBBLES"),
    "indoor": ("Indoors (unchanged)", None, None, "indoor / underground maps keep the purple pin"),
}
ORDER = list(STYLES)


def weather_pill(out, key, loc="Tosa Port", x=8, y=9):
    label, ramp, rows, _ = STYLES[key]
    w = X.CAP_W + 4 + text_width(loc) + 7
    if ramp:
        kit.THEMES["wx"] = [kit.snap(ramp[0]), kit.snap(ramp[1]), kit.snap(ramp[2]), kit.snap(ramp[2])]
        X.SIL["wx"] = rows
        theme, sil = "wx", "wx"
    else:
        theme, sil = "orchid", "pin"

    def fn(cv):
        rounded_box(cv, x, y, w, 14, 4, PANEL, INK, WHITE, PANEL_SHADE)
        X.recolour_cap(cv, x, y, x + X.CAP_W - 1, y + 13, ACCENT, ACCENT_LIGHT, ACCENT_DARK)
        X.centred_sil(cv, x + 1, y + 1, X.CAP_W - 1, 12, sil, WHITE, ACCENT_DARK)
        draw_text(cv, x + X.CAP_W + 4, y - 1, loc, INK, PANEL_SHADE)
    K.layer(out, fn, theme)


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    # 1) swatch sheet: every style at 4x on the field green
    sc, cw, ch = 4, 120, 30
    cols = 3
    rows_n = (len(ORDER) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (cw * sc + 16) + 16, rows_n * (ch * sc + 40) + 16), (28, 28, 36))
    d = ImageDraw.Draw(sheet)
    for i, k in enumerate(ORDER):
        tile = X.field_scene(show_player=False).crop((0, 0, cw, ch))
        weather_pill(tile, k, x=6, y=8)
        px = 16 + (i % cols) * (cw * sc + 16)
        py = 16 + (i // cols) * (ch * sc + 40)
        d.text((px, py), STYLES[k][0] + "  -  " + STYLES[k][3], fill=(230, 230, 240))
        sheet.paste(K.upscale(tile.convert("RGB"), sc), (px, py + 16))
    sheet.save(os.path.join(out_dir, "weather_pills.png"))

    # 2) in context with the v2 start menu (rain + harsh sun)
    for k in ("rain", "clear", "smog"):
        im = X.field_scene("brendan")
        weather_pill(im, k)
        V.start_v2(im, M.NORMAL, 2, "M", "KAITO", "B")
        K.upscale(im.convert("RGB"), 3).save(os.path.join(out_dir, "weather_menu_%s.png" % k))


if __name__ == "__main__":
    main(sys.argv[1])
