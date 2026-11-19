"""Holon Leader Faba: Gen 3 16x32 overworld sheet (9 frames, vanilla order).

Built on vanilla graphics/object_events/pics/people/scientist_1.png (npc_3, lab coat, same build as the
approved Holon Researcher) so arms, legs, feet and the walk cycle stay pixel-for-pixel Gen 3. From the
user's template (ref/faba_ow_template_sheet.png, 32x48 RPG-Maker frames) it takes the design cues that survive
the drop to 16x32: the white coat with the collar wings flared beside the jaw, the glasses band across the
eyes, the walk timing (stand, A, stand, B). Faba's own details come from ref/faba_model_sheet.png:
  - bald head after vanilla balding_man.png (warm-brown scalp outline, top-left highlight), pale side hair
  - lime visor = a big rounded lens, 4 rows brow-to-cheek, over both eyes (eyes at the vanilla x6/x9 show
    through as dark green; round 2 per user: v1's 2-row band was too narrow)
  - goatee + grin, very high white collar (wings beside the jaw in front, a wall behind the head in back view)
  - lime inner neck, white gloves under lime cuffs, white trousers, white boots
Everything is drawn in npc_3 indices (greys 5-7 + lime 8-A), then remapped for the other palette candidates.

Run: <venv python> dev_scripts/voyages/faba/faba_ow.py   (writes faba/ + out/batch8_faba/)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'trainer_classes')))
import kit  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

OUT = os.path.abspath(os.path.join(HERE, '..', 'out', 'batch8_faba'))
os.makedirs(OUT, exist_ok=True)

DOWN, UP, LEFT = (0, 3, 4), (1, 5, 6), (2, 7, 8)

# npc_3 slots: 1-3 skin, 4 warm outline, 5/6/7 lavender greys (coat; 5 = pale hair), 8/9/A lime,
# B/C/D brick browns (unused except D on nothing), E white, F black.  '_' clears, '.' keeps.
HEAD = {
    'down': '''
        _____444444_____
        ___F45333354F___
        __F5322222235F__
        __F5221111225F__
        __F521E111125F__
        _F23A999999A32F_
        _FA8EE8888889AF_
        _FA888A88A889AF_
        __FA99999999AF__
        __F3334EE4333F__
        ___4332552334___
    ''',
    'up': '''
        _____444444_____
        ___F43333334F___
        __F4322222234F__
        __F3221111223F__
        __F321E111123F__
        _F253211112352F_
        _F355322223553F_
        __F5555555555F__
        __7EEEEEEEEEE7__
        _7EEEEEEEEEEEE7_
        _7E5EEEEEEEE5E7_
    ''',
    'left': '''
        ______4444______
        ____4433333F____
        ___431111123F___
        ___41E1111223F__
        __41111111223F__
        __AAAAA112235F__
        _A8E889A32355F__
        _A888A9A34566F__
        _A9999A232566F__
        _4543333333F____
        __55543334F_____
    ''',
}
# collar / neck rows below and beside the head (y relative to a stand frame); '.' keeps the scientist body
COLLAR = {
    'down': (19, '''
        .7............7.
        .7E..........E7.
        .7EE........EE7.
        ..75E5A88A5E57..
    '''),
    'up': (22, '''
        ..756EEEEEE657..
    '''),
    'left': (19, '''
        ............7...
        ...........7E7..
        ..........7EE7..
        ....7A88EEEE7...
    '''),
}


def bob(fr):
    top = next(y for y in range(32) if any(fr.px[y]))
    return top - 11


def direction(i):
    return 'down' if i in DOWN else 'up' if i in UP else 'left'


def build():
    o = kit.load_ow('scientist_1')
    for i in range(9):
        fr = o.frame(i)
        dy = bob(fr)
        d = direction(i)
        # ---- body recolour (rows from the shoulders down) ----
        for y in range(21 + dy, 32):
            for x in range(16):
                v = fr.px[y][x]
                if v in (9, 10):                       # green tie -> closed coat front
                    fr.px[y][x] = 6 if v == 10 else 5
                elif v in (12, 13) and y >= 28 + dy:   # brown slacks -> white trousers / boots
                    fr.px[y][x] = 6 if v == 13 else 5
        # hands -> white gloves, sleeve end above -> lime cuff (2 rows)
        gl = [(x, y) for y in range(23 + dy, 32) for x in range(16) if fr.px[y][x] in (1, 2, 3, 4)]
        for x, y in gl:
            fr.px[y][x] = {1: 14, 2: 14, 3: 5, 4: 6}[fr.px[y][x]]
        cuffs = set()
        for x, y in gl:
            for k in (1, 2):
                yy = y - k
                if (x, yy) not in gl and fr.px[yy][x] in (5, 6, 7, 14):
                    cuffs.add((x, yy))
        for x, y in cuffs:
            fr.px[y][x] = {14: 8, 5: 8, 6: 8, 7: 9}[fr.px[y][x]]
        # ---- head ----
        for y in range(0, 21 + dy):
            for x in range(16):
                fr.px[y][x] = 0
        fr.patch(0, 11 + dy, HEAD[d])
        cy, art = COLLAR[d]
        fr.patch(0, cy + dy, art)
        o.set_frame(i, fr)
    return o


# ------------------------------------------------------------------ palette candidates
# role (npc_3 slot) -> slot in the candidate palette. npc_3 itself is the identity.
CANDIDATES = {
    'npc_3': {},
    # gold 5-7 for hair (and nothing else gold), lime 8-A visor/cuffs, coat has no greys: white + black only
    'npc_green': {5: 14, 6: 14, 7: 15, 8: 8, 9: 9, 10: 10},
    # gold 5-7 hair, greys B-D coat, no green: visor + cuffs go gold
    'npc_white': {5: 11, 6: 12, 7: 13, 8: 5, 9: 6, 10: 7},
    # greys B-D coat, blue 5-7 visor (no green)
    'npc_pink': {5: 11, 6: 12, 7: 13, 8: 8, 9: 9, 10: 10},
}
OWN_PAL = [kit.BG, (255, 213, 180), (255, 197, 148), (222, 148, 115), (123, 65, 65),
           (205, 205, 222), (156, 156, 189), (74, 74, 123),          # coat greys (npc_3)
           (184, 224, 48), (112, 168, 24), (40, 80, 16),              # Faba lime
           (240, 224, 152), (200, 160, 64), (120, 88, 32),            # pale-blonde hair / gold
           (255, 255, 255), (0, 0, 0)]


def remap_to(o, palname, roles):
    p = o.copy()
    p.pal = kit.npc_pal(palname) if palname != 'own' else list(OWN_PAL)
    p.remap(roles)
    return p


def own_variant(o):
    """Own palette: hair pale blonde (B), gold buttons/boot heels (C)."""
    p = o.copy()
    p.pal = list(OWN_PAL)
    for i in range(9):
        fr = p.frame(i)
        dy = bob(fr)
        for y in range(11 + dy, 21 + dy):          # hair: pale grey 5/6 in the head block -> blonde B/C
            for x in range(16):
                if fr.px[y][x] == 5:
                    fr.px[y][x] = 11
                elif fr.px[y][x] == 6 and y < 20 + dy:
                    fr.px[y][x] = 12
        p.set_frame(i, fr)
    return p


def label(im, text, pad=12):
    out = Image.new('RGB', (im.width, im.height + pad), (60, 60, 60))
    out.paste(im, (0, pad))
    ImageDraw.Draw(out).text((2, 0), text, fill=(255, 255, 255))
    return out


def vstack(ims, gap=6):
    out = Image.new('RGB', (max(i.width for i in ims), sum(i.height for i in ims) + gap * (len(ims) - 1)), (60, 60, 60))
    y = 0
    for i in ims:
        out.paste(i, (0, y)); y += i.height + gap
    return out


def hstack(ims, gap=8):
    out = Image.new('RGB', (sum(i.width for i in ims) + gap * (len(ims) - 1), max(i.height for i in ims)), (60, 60, 60))
    x = 0
    for i in ims:
        out.paste(i, (x, 0)); x += i.width + gap
    return out


def template_naive():
    """The template's 4x4 32x48 frames shrunk to 16x32 (half size, nearest) in Gen 3 frame order, to show
    why the template is used for design cues and not scaled: the head ends up a chibi 2/3 of the body."""
    t = Image.open(os.path.join(HERE, '..', 'ref', 'faba_ow_template_sheet.png')).convert('RGBA')
    # template rows: 0 down, 1 left, 2 right, 3 up; columns: stand, A, stand, B
    order = [(0, 0), (3, 0), (1, 0), (0, 1), (0, 3), (3, 1), (3, 3), (1, 1), (1, 3)]
    out = Image.new('RGBA', (144, 32), (0, 0, 0, 0))
    for k, (r, c) in enumerate(order):
        f = t.crop((c * 32, r * 48, c * 32 + 32, r * 48 + 48)).resize((16, 24), Image.NEAREST)
        out.paste(f, (k * 16, 8), f)
    bg = Image.new('RGBA', out.size, (232, 232, 232, 255))
    bg.alpha_composite(out)
    return bg.convert('RGB')


def main():
    o = build()
    res = []
    p = os.path.join(HERE, 'faba_ow.png'); o.to_image().save(p); res.append((p, kit.check_ow(o, 'npc_3')))
    kit.ow_gif(o, os.path.join(OUT, 'faba_ow_walk.gif'))
    kit.ow_preview(o, 6).save(os.path.join(OUT, 'faba_ow_frames_x6.png'))
    own = own_variant(o)
    own.to_image().save(os.path.join(HERE, 'faba_ow_ownpal.png'))
    kit.write_jasc(os.path.join(HERE, 'npc_faba.pal'), OWN_PAL)

    rows = [label(kit.ow_preview(kit.load_ow('scientist_1'), 4).convert('RGB'), 'vanilla scientist_1 (npc_3): body/arms/legs/walk base'),
            label(template_naive().resize((144 * 4, 32 * 4), Image.NEAREST), "user's template, naively halved (head too big: cues only)")]
    for name, roles in CANDIDATES.items():
        c = remap_to(o, name, roles)
        probs = kit.check_ow(c, name)
        rows.append(label(kit.ow_preview(c, 4).convert('RGB'), name + ('  (CHOSEN)' if name == 'npc_3' else '') + ('  ! ' + '; '.join(probs) if probs else '')))
    rows.append(label(kit.ow_preview(own, 4).convert('RGB'), 'own palette (npc_faba.pal): blonde hair + gold, costs 1 OBJ palette'))
    vstack(rows).save(os.path.join(OUT, 'faba_ow_palette_candidates.png'))

    # 1x / 3x in context next to the Holon Researcher on the lab floor colour
    hr = kit.Pic.from_png(os.path.join(HERE, '..', 'trainers', 'holon_researcher_ow.png'))
    floor = (200, 200, 208)
    strip = Image.new('RGB', (16 * 8 + 8, 36), floor)
    for k, (pic, f) in enumerate([(o, 0), (o, 1), (o, 2), (hr, 0), (hr, 2), (own, 0), (own, 2)]):
        im = pic.frame(f).render(1)
        strip.paste(im, (4 + k * 18, 2), im)
    hstack([strip, strip.resize((strip.width * 3, strip.height * 3), Image.NEAREST)]).save(os.path.join(OUT, 'faba_ow_context_1x_3x.png'))
    for pth, probs in res:
        print(('OK   ' if not probs else 'WARN ') + os.path.basename(pth), probs)
    return o


if __name__ == '__main__':
    main()
