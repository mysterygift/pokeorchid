"""Holon Researcher (new class, unique to Holon): a tweaked Scientist after the EX Delta Species
"Holon Scientist" card (ref/holon_scientist_card.png): brown hair, round glasses, white lab coat,
green shirt + darker green tie.

Bases (no redraw, silhouette kept):
  front: graphics/trainers/front_pics/scientist_frlg.png  (Emerald has no Scientist trainer pic)
  OW:    graphics/object_events/pics/people/scientist_1.png (npc_3; already brown hair + green tie)

Outputs (trainers/): holon_researcher_front.png (+ variant _greyslacks), holon_researcher_ow.png (npc_3)
Renders (out/batch5_trainers/): compare sheet, OW frames, silhouette audit, battle intro.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TC = os.path.abspath(os.path.join(HERE, '..', '..', 'trainer_classes'))
sys.path.insert(0, TC)
import kit  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

OUT = os.path.join(HERE, '..', 'out', 'batch5_trainers')
os.makedirs(OUT, exist_ok=True)

HAIR = {6: (176, 120, 80), 7: (128, 80, 48), 10: (72, 40, 24)}     # light / mid / dark brown
SHIRT = {8: (160, 216, 120), 9: (64, 144, 72)}                       # shirt light green, tie/shadow green
TORSO = (26, 17, 40, 35)


def front(slacks='brown'):
    f = kit.load_front('scientist_frlg')
    # torso: the navy shirt-shadow/tie strip (10) becomes the tie green (9) before 10 turns brown
    f.remap({10: 9}, TORSO)
    if slacks == 'grey':
        # trousers onto the coat greys, keeping the darkest step for creases
        f.remap({6: 12, 7: 11}, (26, 35, 47, 61))
    for s, c in HAIR.items():
        f.set_pal(s, c)
    for s, c in SHIRT.items():
        f.set_pal(s, c)
    # round glasses: vanilla lenses (x30-32 / x36-37, rows 12-13) keep their glare; add a thin top arc
    # (warm outline 4, over the brow row) and a lower rim on row 14 so each lens reads as a ring
    # instead of the vanilla browline bar. Lens positions and the black bridge/temples are vanilla.
    f.patch(28, 11, '''
        ..444...44..
        .FEEDF.FEDF.
        .4EDD4.4DD4.
        ..444...44..
    ''')
    return f


def ow(light_hair=False):
    o = kit.load_ow('scientist_1')
    G, T = 9, 10        # npc_3: 9 mid green (shirt), A dark green (tie)
    for i in range(9):
        fr = o.frame(i)
        # find the bob (walk frames are 1px lower): stand frames have the hair top at y11
        top = next(y for y in range(32) if any(fr.px[y]))
        dy = top - 11
        if i in (0, 3, 4):            # front views: collar row + shirt beside the tie, tie dark green
            for x in range(16):
                if fr.px[22 + dy][x] == 4 and 5 <= x <= 10:
                    fr.px[22 + dy][x] = G
            for y in range(23 + dy, 26 + dy):
                for x in (7, 8):
                    if fr.px[y][x] in (9, 10):
                        fr.px[y][x] = T
            for x in (6, 9):
                if fr.px[23 + dy][x] == 7:
                    fr.px[23 + dy][x] = G
        if i in (2, 7, 8):            # side views: the tie column beside the arm
            for y in range(22 + dy, 26 + dy):
                for x in range(3, 7):
                    if fr.px[y][x] == 9:
                        fr.px[y][x] = G
                    elif fr.px[y][x] == 10:
                        fr.px[y][x] = T
        # optional hair: lighter brown — dark base (13) -> mid (12), highlight (12) -> light (11).
        # npc_3's light step (205,98,74) is orange, so this reads ginger; default keeps vanilla hair.
        if not light_hair:
            o.set_frame(i, fr)
            continue
        # (glasses frames also use 13: front views stop above them at row 16, side views keep x<8)
        for y in range(11 + dy, 20 + dy):
            for x in range(16):
                if i in (0, 3, 4) and y > 16 + dy:
                    continue
                if i in (2, 7, 8) and y > 16 + dy and x < 8:
                    continue
                v = fr.px[y][x]
                if v == 12:
                    fr.px[y][x] = 11
                elif v == 13:
                    fr.px[y][x] = 12
        o.set_frame(i, fr)
    return o


def label(im, text, pad=12):
    out = Image.new('RGB', (im.width, im.height + pad), (60, 60, 60))
    out.paste(im, (0, pad))
    ImageDraw.Draw(out).text((2, 0), text, fill=(255, 255, 255))
    return out


def hstack(ims, gap=8, bg=(60, 60, 60)):
    out = Image.new('RGB', (sum(i.width for i in ims) + gap * (len(ims) - 1), max(i.height for i in ims)), bg)
    x = 0
    for i in ims:
        out.paste(i, (x, 0)); x += i.width + gap
    return out


def vstack(ims, gap=8, bg=(60, 60, 60)):
    out = Image.new('RGB', (max(i.width for i in ims), sum(i.height for i in ims) + gap * (len(ims) - 1)), bg)
    y = 0
    for i in ims:
        out.paste(i, (0, y)); y += i.height + gap
    return out


def main():
    results = []
    fa = front('brown')
    fb = front('grey')
    p = os.path.join(HERE, 'holon_researcher_front.png'); fa.to_image().save(p); results.append((p, kit.check_front(fa)))
    p = os.path.join(HERE, 'holon_researcher_front_greyslacks.png'); fb.to_image().save(p); results.append((p, kit.check_front(fb)))
    o = ow()
    o2 = ow(light_hair=True)
    o2.to_image().save(os.path.join(HERE, 'holon_researcher_ow_lighthair.png'))
    p = os.path.join(HERE, 'holon_researcher_ow.png'); o.to_image().save(p); results.append((p, kit.check_ow(o, 'npc_3')))
    kit.ow_gif(o, os.path.join(OUT, 'holon_researcher_ow_walk.gif'))

    van_f = kit.load_front('scientist_frlg')
    van_o = kit.load_ow('scientist_1')
    card = Image.open(os.path.join(HERE, '..', 'ref', 'holon_scientist_card.png')).convert('RGB')
    art = card.crop((22, 40, 222, 160))           # card illustration window (approx.)
    fronts = hstack([label(van_f.render(2, (232, 232, 232)).convert('RGB'), 'vanilla scientist_frlg'),
                     label(fa.render(2, (232, 232, 232)).convert('RGB'), 'tweak (brown slacks)'),
                     label(fb.render(2, (232, 232, 232)).convert('RGB'), 'variant: grey slacks'),
                     label(art, 'card ref')])
    ows = vstack([label(kit.ow_preview(van_o, 3).convert('RGB'), 'vanilla scientist_1 (npc_3) - all 9 frames + right (flip)'),
                  label(kit.ow_preview(o, 3).convert('RGB'), 'Holon Researcher OW (npc_3): green collar/shirt + dark green tie'),
                  label(kit.ow_preview(o2, 3).convert('RGB'), 'variant: lighter hair (npc_3 has no neutral brown: reads ginger)')])
    vstack([fronts, ows]).save(os.path.join(OUT, 'holon_researcher_compare.png'))

    # face close-up 6x: vanilla vs new
    crop = (22, 2, 46, 30)
    hstack([label(van_f.render(1, (232, 232, 232)).convert('RGB').crop(crop).resize((24 * 8, 28 * 8), Image.NEAREST), 'vanilla'),
            label(fa.render(1, (232, 232, 232)).convert('RGB').crop(crop).resize((24 * 8, 28 * 8), Image.NEAREST), 'round glasses / brown hair')]
           ).save(os.path.join(OUT, 'holon_researcher_face_x8.png'))

    for p, probs in results:
        print(('OK   ' if not probs else 'WARN ') + os.path.relpath(p, HERE), probs)


if __name__ == '__main__':
    main()
