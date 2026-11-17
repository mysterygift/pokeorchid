"""Storyboard for the post-catch dex page: battle -> registered page -> exit. usage: postcatch_dex.py OUT_DIR"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import mock_dex as M
import mock_battle as B
import kit_ext as KX
from gamefont import draw_text
OUT = sys.argv[1]
ZIG = 11       # ENTRIES index of Zigzagoon (caught in the mock battle)
enemy = B.default_enemy()

def fade_black(im, k):
    im = im.convert('RGB')
    return Image.blend(im, Image.new('RGB', im.size, (0, 0, 0)), k)

frames = []
b1 = B.render(mode="msg", msg="Gotcha!\nZigzagoon was caught!", enemy=enemy, enemy_visible=False, ball=True, show_boxes=("plr",))
b2 = B.render(mode="msg", msg="Zigzagoon's data was added\nto the POKéDEX.", enemy=enemy, enemy_visible=False, ball=True, show_boxes=("plr",))
frames.append(("1  Battle: catch message", b1))
frames.append(("2  'data was added to the POKéDEX.'", b2))
frames.append(("3  Palette fade to black (16 frames)", fade_black(b2, 0.6)))
reg = M.render_registered(ZIG)
frames.append(("4  Page fades in; cry plays", fade_black(reg, 0.5)))
frames.append(("5  Registered page (NEW pulses)", reg))
frames.append(("6  NEW pill pulse frame", M.render_registered(ZIG, pulse=True)))
stage = M.E_DAIS_C[1] + int(M.E_DAIS_IN * 0.55) + 3
spr = M.D.mon_pic('zigzagoon')
y0 = stage - M.D.sprite_bottom(spr) + 32
frames.append(("7  A/B: BG darkens, pic glides to centre", M.render_registered(ZIG, fade=0.5, sprite_pos=((M.E_DAIS_C[0] + 120) // 2, (y0 + 80) // 2), show_ui_obj=False)))
frames.append(("8  ...then the nickname prompt (vanilla)", M.render_registered(ZIG, fade=1.0, sprite_pos=(120, 80), show_ui_obj=False)))

# sheet: hero (registered page, 3x) on top, storyboard (1x... 2x) below
S = 2
cols = 4
cw, ch = 240 * S, 160 * S
sheet = Image.new('RGB', (cols * (cw + 12) + 12, 160 * 3 + 24 + 2 * (ch + 30) + 12), (24, 24, 32))
hero = KX.upscale(reg.convert('RGB'), 3)
sheet.paste(hero, (12, 12))
d = ImageDraw.Draw(sheet)
from PIL import ImageFont
FONT = ImageFont.load_default(size=17)
notes = ["Post-catch dex page - Orchid",
         "- Same body as INFO (dais, number/name + ball, category,",
         "  types, HT/WT, footprint, description in the tray).",
         "- Header: no tabs; gold NEW pill + 'Registered to the POKeDEX!'.",
         "- NEW pill pulses (pal 1 swap) instead of vanilla's header flicker.",
         "- In: battle palette-fades out, page palette-fades in, cry.",
         "- Out (A/B): BLDY darken on BG, pic glides to the centre",
         "  (vanilla SpriteCB_SlideCaughtMonToCenter), then nickname.",
         "- Budget: entry sheet + 1 header variant tilemap; OBJ = the",
         "  battle sprite (as vanilla) + 2 type icons; BG pal 0-2."]
for i, t in enumerate(notes):
    d.text((12 + 720 + 24, 20 + i * 24), t, fill=(230, 230, 240), font=FONT)
y = 12 + 480 + 12
for i, (cap, im) in enumerate(frames):
    x = 12 + (i % cols) * (cw + 12)
    yy = y + (i // cols) * (ch + 30)
    sheet.paste(im.convert('RGB').resize((cw, ch), Image.NEAREST), (x, yy + 18))
    d.text((x, yy + 2), cap, fill=(230, 230, 240), font=FONT)
sheet.save(os.path.join(OUT, 'postcatch_mock.png'))
print('ok', sheet.size)
