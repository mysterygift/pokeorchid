"""Cynthia: cut lichen's sheet (ref/cynthia_sheet_by_lichen.png, CREDIT: "sprites by lichen") into a
Gen 3 trainer front pic (64x64, 16 colours, slot 0 transparent) and a 9-frame 144x32 OW sheet, fit the
OW to shared NPC palettes (candidates rendered side by side), validate with trainer_classes/kit.py.

Outputs:
  trainers/cynthia_front.png           64x64 indexed, own 16-colour palette (front pics own their palette)
  trainers/cynthia_ow.png              144x32 indexed, chosen shared NPC palette (CHOSEN below)
  trainers/cynthia_ow_ownpal.png       144x32 indexed, lichen's exact colours (fallback, own palette)
  trainers/npc_cynthia.pal             JASC for the fallback
  out/batch5_trainers/cynthia_*.png    review renders

Run: <venv python> dev_scripts/voyages/trainers/cynthia.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'trainer_classes')))
import kit  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

REF = os.path.join(HERE, '..', 'ref', 'cynthia_sheet_by_lichen.png')
OUT = os.path.join(HERE, '..', 'out', 'batch5_trainers')
os.makedirs(OUT, exist_ok=True)

FRONT_BG = (223, 206, 224)
OW_BG = (212, 188, 232)

# ---------------------------------------------------------------- front pic
# Palette laid out in the vanilla convention: 1-4 skin ramp + warm outline, then hair, then coat, E white, F black.
FRONT_PAL = [kit.BG,
             (248, 208, 184), (216, 160, 120), (189, 123, 98), (141, 83, 66),   # skin light..outline
             (242, 226, 186), (232, 192, 128), (171, 147, 99),                   # hair
             (131, 131, 139), (80, 80, 80), (57, 57, 57), (33, 33, 33),          # coat greys
             (0, 0, 0), (0, 0, 0),                                               # unused 12-13
             (255, 255, 255), (0, 0, 0)]


def cut_front(sheet):
    px = sheet.load()
    lut = {c: i for i, c in enumerate(FRONT_PAL) if i not in (0, 12, 13)}
    pic = kit.Pic(64, 64, None, FRONT_PAL)
    for y in range(64):
        for x in range(64):
            c = px[x, y]
            if c == FRONT_BG:
                continue
            pic.px[y][x] = lut[c]
    return pic


# ---------------------------------------------------------------- OW sheet
# lichen's OW colours by role
SRC = {
    'skin1': (255, 213, 180), 'skin2': (246, 189, 148), 'skin3': (222, 148, 115), 'outl': (123, 65, 65),
    'hairP': (247, 231, 200), 'hairY': (237, 209, 118), 'hairG': (195, 139, 80), 'hairO': (97, 101, 64),
    'coatB': (104, 129, 141), 'coatC': (77, 77, 102), 'coatN': (39, 39, 66), 'black': (0, 0, 0),
}
FIXED = {'skin1': 1, 'skin2': 2, 'skin3': 3, 'outl': 4, 'black': 15}

# Hand-picked role -> slot maps per shared palette (slots: 5-7, 8-A, B-D ramps, E white).
CANDIDATES = {
    # gold hair ramp 5-7 and the purple ramp 8-A darkest shade for the coat
    'npc_blue':  {'hairP': 14, 'hairY': 5, 'hairG': 6, 'hairO': 7, 'coatB': 9, 'coatC': 10, 'coatN': 15},
    # same, but the coat's blue-grey highlight also goes to the darkest purple: near-black coat
    'npc_blue (black coat)': {'hairP': 14, 'hairY': 5, 'hairG': 6, 'hairO': 7, 'coatB': 10, 'coatC': 10, 'coatN': 15},
    # dull gold 5-7 hair, grey B-D coat
    'npc_white': {'hairP': 14, 'hairY': 5, 'hairG': 6, 'hairO': 7, 'coatB': 12, 'coatC': 13, 'coatN': 15},
    # olive-gold 5-7 hair, coat has no dark ramp (dark olive 7 + black)
    'npc_green': {'hairP': 14, 'hairY': 5, 'hairG': 6, 'hairO': 7, 'coatB': 7, 'coatC': 7, 'coatN': 15},
    # saturated yellow 5-7 hair, coat dark brown D + black
    'npc_2':     {'hairP': 14, 'hairY': 5, 'hairG': 6, 'hairO': 7, 'coatB': 12, 'coatC': 13, 'coatN': 15},
    # tan B-D hair, navy 8-A coat
    'npc_1':     {'hairP': 14, 'hairY': 11, 'hairG': 12, 'hairO': 13, 'coatB': 9, 'coatC': 10, 'coatN': 15},
}
CHOSEN = 'npc_white'  # user 2026-11-19


def cut_ow_roles(sheet):
    """Return 9 frames as 144x32 grid of role names (None = transparent)."""
    px = sheet.load()
    inv = {v: k for k, v in SRC.items()}
    grid = [[None] * 144 for _ in range(32)]
    for y in range(32):
        for x in range(144):
            c = px[x, 64 + y]
            if c != OW_BG:
                grid[y][x] = inv[c]
    return grid


def ow_from_roles(grid, palname, roles):
    pal = kit.npc_pal(palname.split(' ')[0])
    m = dict(FIXED, **roles)
    pic = kit.Pic(144, 32, None, pal)
    for y in range(32):
        for x in range(144):
            r = grid[y][x]
            if r:
                pic.px[y][x] = m[r]
    return pic


def own_pal_ow(grid):
    order = ['skin1', 'skin2', 'skin3', 'outl', 'hairY', 'hairG', 'hairO', 'coatB', 'coatC', 'coatN',
             'hairP']
    pal = [kit.BG] + [SRC[k] for k in order] + [(0, 0, 0)] * 2 + [(255, 255, 255), (0, 0, 0)]
    m = {k: i + 1 for i, k in enumerate(order)}
    m['black'] = 15
    pic = kit.Pic(144, 32, None, pal)
    for y in range(32):
        for x in range(144):
            if grid[y][x]:
                pic.px[y][x] = m[grid[y][x]]
    return pic, pal


def ground_patch(kind):
    """3x3 metatiles of real General-tileset ground (grass 0x001 / sand 0x124), via voyage_compose."""
    sys.path.insert(0, os.path.join(HERE, '..'))
    import voyage_compose as vc
    mid = {'grass': 0x001, 'sand': 0x124}[kind]
    return vc.picture([[mid] * 3] * 3, ('gTileset_General', 'gTileset_Petalburg')).convert('RGB')


def ow_on_ground(pic, kind, frames=(0, 1, 2)):
    """Each frame standing on a 2x3-tile patch; the 16x32 sprite's feet rest on the bottom tile row."""
    W = 16 * 3 * len(frames) + 8 * (len(frames) - 1)
    out = Image.new('RGB', (W, 48), (40, 40, 40))
    patch = ground_patch(kind)
    for k, f in enumerate(frames):
        ox = k * (48 + 8)
        out.paste(patch, (ox, 0))
        spr = pic.frame(f).render(1)
        # 16x32 object event: sprite bottom = bottom of the metatile the NPC stands on (centre tile here)
        out.paste(spr, (ox + 16, 32 - 32), spr)
    return out


def main():
    sheet = Image.open(REF).convert('RGB')

    front = cut_front(sheet)
    fprobs = kit.check_front(front)
    fp = os.path.join(HERE, 'cynthia_front.png')
    front.to_image().save(fp)
    front.render(4, (232, 232, 232)).save(os.path.join(OUT, 'cynthia_front_x4.png'))

    grid = cut_ow_roles(sheet)
    renders = []
    for name, roles in CANDIDATES.items():
        o = ow_from_roles(grid, name, roles)
        probs = kit.check_ow(o, name.split(' ')[0])
        renders.append((name, o, probs))
        if name == CHOSEN:
            op = os.path.join(HERE, 'cynthia_ow.png')
            o.to_image().save(op)
            kit.ow_gif(o, os.path.join(OUT, 'cynthia_ow_walk.gif'))
            kit.ow_preview(o, 4).save(os.path.join(OUT, 'cynthia_ow_frames_x4.png'))
            chosen = o
    own, ownpal = own_pal_ow(grid)
    own.to_image().save(os.path.join(HERE, 'cynthia_ow_ownpal.png'))
    kit.write_jasc(os.path.join(HERE, 'npc_cynthia.pal'), ownpal)

    # ---- palette candidate sheet (lichen original first), frames 0,1,2 at 4x on light grey
    S = 4
    rows = [('lichen original (own colours)', own, [])] + renders
    lab_h = 12
    row_h = 32 * S + lab_h + 6
    sheet_img = Image.new('RGB', (9 * 16 * S + 10 * 2 + 200, row_h * len(rows)), (60, 60, 60))
    d = ImageDraw.Draw(sheet_img)
    for r, (name, o, probs) in enumerate(rows):
        y = r * row_h
        d.text((4, y + 1), name + ('' if not probs else '  !' + '; '.join(probs)), fill=(255, 255, 255))
        prev = kit.ow_preview(o, S).convert('RGB')
        sheet_img.paste(prev, (4, y + lab_h))
    sheet_img.save(os.path.join(OUT, 'cynthia_ow_palette_candidates.png'))

    # ---- OW on grass and sand, 1x and 3x
    g = ow_on_ground(chosen, 'grass')
    s = ow_on_ground(chosen, 'sand')
    both = Image.new('RGB', (g.width, 48 * 2 + 4), (40, 40, 40))
    both.paste(g, (0, 0)); both.paste(s, (0, 52))
    both.save(os.path.join(OUT, 'cynthia_ow_ground_1x.png'))
    both.resize((both.width * 3, both.height * 3), Image.NEAREST).save(os.path.join(OUT, 'cynthia_ow_ground_3x.png'))

    print('front', fp, front.used(), fprobs or 'OK')
    for name, o, probs in renders:
        print('ow', name, probs or 'OK')


if __name__ == '__main__':
    main()
