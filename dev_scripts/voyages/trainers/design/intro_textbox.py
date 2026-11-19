"""Battle-intro mocks with the REAL intro string and the REAL automatic line breaker.

The game does not print "<CLASS> <NAME>\\nwould like to battle!" any more: expansion's intro is
sText_Trainer1WantsToBattle = "You are challenged by {B_TRAINER1_NAME_WITH_CLASS}!\\p" (src/battle_message.c:97),
and BattleStringExpandPlaceholders runs BreakStringAutomatic(dst, 208 px, 2 lines, FONT_NORMAL, SHOW_SCROLL_PROMPT)
(src/battle_message.c:3724, src/line_break.c). break_auto() below is a port of BreakSubStringAutomatic, including
its quirk of comparing word *length* (chars) instead of width when counting lines.

Writes out/batch5_trainers/intro_<tag>_pN.png (240x160) + a contact sheet intro_textbox_sheet.png (2x).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TC = os.path.abspath(os.path.join(HERE, '..', '..', 'trainer_classes'))
UI = os.path.abspath(os.path.join(HERE, '..', '..', 'orchid_ui'))
sys.path = [UI] + [p for p in sys.path if os.path.abspath(p or '.') != HERE]

from PIL import Image, ImageDraw  # noqa: E402
import kit_ext as K  # noqa: E402
import battle_ext as BX  # noqa: E402
import mock_battle as M  # noqa: E402
from gamefont import text_width  # noqa: E402

OUT = os.path.join(HERE, '..', 'out', 'batch5_trainers')
MAXW, LINES, PROMPT = 208, 2, 8
NB = '\u00a0'   # stands for {NBSP}


def break_auto(s, maxw=MAXW, font='normal'):
    words = s.split(' ')
    wid = [text_width(w.replace(NB, ' '), font) for w in words]   # NBSP (charmap 0x39) never splits
    sp = text_width(' ', font)
    total = sum(wid) + sp * (len(words) - 1) + PROMPT
    if total <= maxw:
        return [s.replace(NB, ' ')]
    # line count (the C code compares word length in chars here, not width)
    cur, lines = 0, 1
    for i, w in enumerate(words):
        if i + 1 == len(words):
            cur += PROMPT
        if cur + len(w) > maxw:
            lines += 1
            cur = wid[i]
        else:
            cur += wid[i] + sp
    if cur > maxw:
        lines += 1
    while True:
        target = total // lines
        out = [[words[0]]]
        cur = wid[0]
        ok = True
        for i in range(1, len(words)):
            if cur + sp + wid[i] + PROMPT > maxw or cur > target:
                if len(out) == lines:
                    lines += 1
                    ok = False
                    break
                out.append([words[i]])
                cur = wid[i]
            else:
                out[-1].append(words[i])
                cur += sp + wid[i]
        if ok:
            return [' '.join(l).replace(NB, ' ') for l in out]


def scene(front_png, env):
    def intro_scene(env=env, trainer=None, player_back='brendan', trainer_dx=0):
        out = BX.environment(env)
        K.place(out, K.sprite_rgba(front_png), BX.ENEMY_C[0], BX.ENEMY_C[1])
        back = K.sprite_rgba(K.G('trainers', 'back_pics', player_back + '.png'), 0, 64)
        K.place(out, back, 80, 80)
        return out
    return intro_scene


def pages(front_png, env, text, tag):
    M.intro_scene = scene(front_png, env)
    lines = break_auto(text)
    ims = []
    for k in range(0, len(lines), LINES):
        page = lines[k:k + LINES]
        img = M.render(mode='msg', msg='\n'.join(page), intro=True, env=env)
        p = os.path.join(OUT, f'intro_{tag}_p{k // LINES + 1}.png')
        img.save(p)
        ims.append(img)
    widths = [text_width(l, 'normal') for l in lines]
    return lines, widths, ims


CASES = [
    # tag, front, env, string
    ('cynthia', 'cynthia_front.png', 'orchid_lake', 'You are challenged by Champion Cynthia!'),
    ('holon_short', 'holon_researcher_front.png', 'orchid_grass', 'You are challenged by Holon Researcher Ido!'),
    ('holon_long', 'holon_researcher_front.png', 'orchid_grass', 'You are challenged by Holon Researcher Christophe!'),
    ('holon_nbsp_long', 'holon_researcher_front.png', 'orchid_grass', 'You are challenged by Holon' + NB + 'Researcher Christophe!'),
    ('researcher_long', 'holon_researcher_front.png', 'orchid_grass', 'You are challenged by Researcher Christophe!'),
    ('holon_sentout', 'holon_researcher_front.png', 'orchid_grass', 'Holon Researcher Christophe sent out Pikachu!'),
]


def main():
    rows = []
    for tag, front, env, text in CASES:
        lines, widths, ims = pages(os.path.join(HERE, front), env, text, tag)
        print(f'{tag:16s} {len(lines)} line(s)  ' + ' | '.join(f'{l!r} {w}px' for l, w in zip(lines, widths)))
        rows.append((f'{tag}: ' + ' / '.join(f'{w}px' for w in widths) + f'  (max {MAXW})', ims))
    S = 2
    W = max(len(ims) for _, ims in rows) * (240 * S + 8)
    H = len(rows) * (160 * S + 16)
    sheet = Image.new('RGB', (W, H), (50, 50, 50))
    d = ImageDraw.Draw(sheet)
    for r, (lab, ims) in enumerate(rows):
        y = r * (160 * S + 16)
        d.text((4, y + 2), lab, fill=(255, 255, 255))
        for c, im in enumerate(ims):
            sheet.paste(im.convert('RGB').resize((240 * S, 160 * S), Image.NEAREST), (c * (240 * S + 8), y + 14))
    sheet.save(os.path.join(OUT, 'intro_textbox_sheet.png'))


if __name__ == '__main__':
    main()
