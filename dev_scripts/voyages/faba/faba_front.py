"""Holon Leader Faba: Gen 3 trainer front pic (64x64, 16 colours, slot 0 transparent).

Base: graphics/trainers/front_pics/magma_leader_maxie.png. Maxie already has Faba's build and the pose of
Faba's model-sheet front view (tall, narrow, knee-length coat, one hand on the hip, high collar), so the
silhouette, legs and hip hand stay vanilla. Repainted: red cape + grey shirt -> one white lab coat, dark slacks
-> white trousers and boots, red hair -> bald scalp with pale-blonde side tufts, glasses -> lime visor, plus a
goatee and grin, the huge collar wings, lime cuffs over white gloves, gold U-pocket trims/buttons/heels/star.
Variant B raises the hanging hand to the chest (official-art gesture).

Palette (vanilla convention): 1-4 skin + warm outline, 5-7 coat lavender shades, 8-A lime, B-D gold/hair,
E white, F black.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'trainer_classes')))
import kit  # noqa: E402

PAL = {
    5: (208, 208, 224), 6: (152, 152, 184), 7: (88, 88, 128),     # coat shading (lavender, like the official art)
    8: (192, 232, 64), 9: (128, 184, 24), 10: (56, 104, 16),       # lime visor / cuffs / inner collar
    11: (232, 200, 104), 12: (168, 128, 48), 13: (240, 232, 184),  # gold light, gold dark, pale-blonde hair
}


def base():
    f = kit.load_front('magma_leader_maxie')
    o = f.copy()
    for y in range(64):
        for x in range(64):
            v = o.px[y][x]
            if not v or v in (1, 2, 3, 4, 14, 15):
                continue
            legs = (y >= 49) or (y >= 47 and v in (5, 7, 8, 11))
            if legs:      # slacks + shoes -> white trousers/boots, lavender shading
                f.px[y][x] = {5: 14, 7: 5, 8: 6, 11: 7, 6: 5, 9: 14}.get(v, v)
            elif y >= 12:  # red cape + grey shirt -> one white coat
                f.px[y][x] = {12: 14, 13: 5, 10: 6, 6: 14, 7: 5, 8: 6, 11: 7, 9: 14, 5: 14}.get(v, v)
    for s_, c in PAL.items():
        f.set_pal(s_, c)
    return f


# Head, stamped at x=27, y=1 ('.' keep, '_' clear): bald dome lit from the upper left, pale-blonde tufts
# (D/C) at the temple and behind the ear, 3-row lime visor (eyes dark through it, white glint), long nose,
# sly grin with moustache, pale goatee, lime inner collar under the chin.
HEAD = '''
    _____444444______
    ___442111123F____
    __4211EE11223F___
    __421111122DDF___
    _4D21111122DDCF__
    _4D211111222DDCF_
    _43211111222DDCF_
    A9EE888888898A3CF
    A88FA898FA89A23CF
    _A9999999999A33F_
    __41122222232334F
    __D4EEE4D2234F___
    ___DD4DDC334F____
    ____DDC4A98A_____
    _____A988889A____
'''
# Collar: the right half stands up behind the head like a wall (gold star pin), the left half folds out into
# a pointed wing over the shoulder, as in the official art. Stamped at x=17, y=3.
# Collar (round 2, user: "just high collars"): a stand-up funnel collar rising behind the jaw to ear height on
# both sides, mirror-symmetric about the body axis (x 34.5): outer edge a clean vertical line at x26 / x43,
# white outer face, lighter lavender inner face visible behind the jaw, throat shadow at the bottom where the
# coat's lapel line meets it. The head is drawn on top, so the collar only shows around/behind it.
COLLAR = [
    (26, 9, 'FFF'), (26, 10, 'FE5'), (26, 11, 'FE55'), (26, 12, 'FE55'), (26, 13, 'FEE55'),
    (26, 14, 'FEE555'), (26, 15, 'F5EE556'), (27, 16, 'F5EE556'), (28, 17, 'FF'),
    (41, 9, 'FF'), (41, 10, '5EF'), (40, 11, '55EF'), (40, 12, '55EF'), (39, 13, '55EBF'),
    (38, 14, '555EEF'), (37, 15, '655EE5F'), (36, 16, '655EE5F'), (40, 17, 'FF'),
]


# Visor (round 2, user: v1 too narrow): one big rounded lime lens from the brow (y6) to the cheekbone (y11),
# bulging past the head on the near side (x26), eyes dark through it, white glint top-left, white nose-pad
# bump at the bottom centre. Runs (x, y, chars) stamped over the head.
LENS = [
    (28, 6, 'A' * 10),
    (27, 7, 'A8EE' + '8' * 7 + '9A'),
    (26, 8, 'A8E' + '8888' + '9' + '8888' + '9A'),
    (26, 9, 'A888FA898FA89A'),
    (26, 10, 'A9' + '88888' + '9' + '8888' + '9A'),
    (27, 11, 'A999AEEA999A'), (40, 8, '3'),
]


ARM_B = [
    (30, 20, 'FFF'), (29, 21, 'FEEEF'), (28, 22, 'FEE5EF'), (28, 23, 'F5E56F'), (27, 24, 'FA866F'),
    (26, 25, 'FA889F'), (25, 26, 'F8889F'), (24, 27, 'F8889F'), (23, 28, 'F8899F'), (22, 29, 'F889AF'),
    (22, 30, 'FE56F'), (22, 31, 'F556F'), (23, 32, 'FF'),
]


def gloves_and_cuffs(f, glove_box, cuff_box):
    x0, y0, x1, y1 = glove_box
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            v = f.px[y][x]
            if v in (1, 2, 3, 4):
                f.px[y][x] = {1: 14, 2: 14, 3: 5, 4: 6}[v]
    x0, y0, x1, y1 = cuff_box
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            v = f.px[y][x]
            if v in (14, 5, 6, 7):
                f.px[y][x] = {14: 8, 5: 9, 6: 9, 7: 10}[v]


def build(variant='A'):
    f = base()
    f.clear(18, 0, 47, 15)
    for x, y, run in COLLAR:
        f.patch(x, y, run)
    f.patch(27, 1, HEAD.replace('_', '.'))
    for x, y, run in LENS:
        f.patch(x, y, run)
    # inside of the collar: close the gaps between the wings, jaw and shoulders with lavender shadow
    for y in range(11, 19):
        xs = [x for x in range(18, 48) if f.px[y][x]]
        for x in range(min(xs), max(xs)):
            if not f.px[y][x]:
                f.px[y][x] = 6
    # hands -> white gloves; long lime cuffs on the forearms
    gloves_and_cuffs(f, (39, 33, 46, 40), (41, 28, 47, 33))     # hip hand (viewer's right)
    if variant == 'A':
        gloves_and_cuffs(f, (20, 41, 26, 44), (21, 40, 25, 40))  # hanging hand (viewer's left)
    else:
        # B: the hanging hand goes behind the back; the forearm crosses the chest, glove curled at the
        # collar (official-art gesture). Elbow tucked at the coat edge, lime cuff along the forearm.
        for y in range(41, 45):
            for x in range(20, 27):
                if f.px[y][x] in (1, 2, 3, 4):
                    f.px[y][x] = 0
        f.patch(21, 41, '''
            F6F
            .F
        ''')
        for x, y, run in ARM_B:
            f.patch(x, y, run)
    # gold: two coat buttons, two U-shaped pocket trims, boot heels
    f.patch(29, 19, '''
        BC
        CC
    ''', {'B': 11, 'C': 12})
    f.patch(29, 25, '''
        BC
        CC
    ''', {'B': 11, 'C': 12})
    for (px, py) in ((31, 35), (31, 41)):
        f.patch(px, py, '''
            B....B
            C....C
            .CBBC.
        ''', {'B': 11, 'C': 12})
    # boots: gold soles/heels (the darkest boot shade on the last rows)
    for y in range(60, 63):
        for x in range(16, 48):
            if f.px[y][x] == 7:
                f.px[y][x] = 12
    return f


def label(im, text, pad=12):
    from PIL import Image, ImageDraw
    out = Image.new('RGB', (im.width, im.height + pad), (60, 60, 60))
    out.paste(im, (0, pad))
    ImageDraw.Draw(out).text((2, 0), text, fill=(255, 255, 255))
    return out


def main():
    import runpy
    from PIL import Image
    OUT = os.path.abspath(os.path.join(HERE, '..', 'out', 'batch8_faba'))
    os.makedirs(OUT, exist_ok=True)
    res = []
    pics = {}
    for v, name in (('A', 'faba_front.png'), ('B', 'faba_front_chesthand.png')):
        f = build(v)
        pics[v] = f
        p = os.path.join(HERE, name)
        f.to_image().save(p)
        res.append((p, kit.check_front(f), len(f.used())))
    # compare sheet: Maxie base, A, B, official art
    art = Image.open(os.path.join(HERE, '..', 'ref', 'faba_official.webp')).convert('RGBA')
    art = art.resize((art.width * 256 // art.height, 256), Image.LANCZOS)
    bg = Image.new('RGBA', art.size, (232, 232, 232, 255)); bg.alpha_composite(art)
    tiles = [label(kit.load_front('magma_leader_maxie').render(4, (232, 232, 232)).convert('RGB'), 'base: magma_leader_maxie'),
             label(kit.Pic.from_png(os.path.join(HERE, 'faba_front_v1.png')).render(4, (232, 232, 232)).convert('RGB'), 'old A (v1): flap collar, thin visor'),
             label(pics['A'].render(4, (232, 232, 232)).convert('RGB'), 'new A: high collar + big visor'),
             label(bg.convert('RGB'), 'ref')]
    W = sum(t.width for t in tiles) + 8 * 3
    sheet = Image.new('RGB', (W, max(t.height for t in tiles)), (60, 60, 60))
    x = 0
    for t in tiles:
        sheet.paste(t, (x, 0)); x += t.width + 8
    sheet.save(os.path.join(OUT, 'faba_front_compare.png'))
    # 1x strip next to vanilla bosses for scale
    strip = Image.new('RGB', (64 * 5 + 16, 64), (232, 232, 232))
    for k, im in enumerate([kit.load_front('magma_leader_maxie'), kit.load_front('aqua_leader_archie'), pics['A'], pics['B'],
                            kit.Pic.from_png(os.path.join(HERE, '..', 'trainers', 'holon_researcher_front.png'))]):
        r = im.render(1)
        strip.paste(r, (k * 66, 0), r)
    strip.save(os.path.join(OUT, 'faba_front_1x_lineup.png'))
    # silhouette audit vs Maxie (kit's silhouette.py, pointed at this folder)
    kit.OUT = HERE
    sys.argv = ['silhouette.py', os.path.join(OUT, 'faba_front_silhouette.png'),
                'faba:magma_leader_maxie', 'faba_front_chesthand:magma_leader_maxie']
    tmp = os.path.join(HERE, 'faba_front_chesthand_front.png')       # silhouette.py wants <id>_front.png
    pics['B'].to_image().save(tmp)
    try:
        runpy.run_path(os.path.join(HERE, '..', '..', 'trainer_classes', 'silhouette.py'))
    finally:
        os.remove(tmp)
    for p, probs, n in res:
        print(('OK   ' if not probs else 'WARN ') + os.path.basename(p), n, 'indices', probs)


if __name__ == '__main__':
    main()
