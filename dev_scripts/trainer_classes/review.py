"""Build the round-1 review page (out/review.html) from out/*.png + classes/*.md.

usage: review.py   (run after every class script; regenerates battle mocks + line-ups)
"""
import base64
import html
import io
import os
import re
import subprocess
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
CLS = os.path.join(HERE, 'classes')
ROOT = os.path.abspath(os.path.join(HERE, '../..'))
sys.path.insert(0, HERE)
import kit  # noqa: E402

# id, class label, battle name, battle floor, vanilla front base (for the before/after), group
NEW = [
    ('tourist_m', 'TOURIST ♂', 'TOURIST GREG', 'orchid_beach'),
    ('tourist_f', 'TOURIST ♀', 'TOURIST HANNA', 'orchid_beach'),
    ('hawker_m', 'HAWKER ♂', 'HAWKER AH SENG', 'orchid_void_deck'),
    ('hawker_f', 'HAWKER ♀', 'HAWKER MDM LIM', 'orchid_void_deck'),
    ('delivery_m', 'RIDER', 'RIDER FARID', 'orchid_void_deck'),
    ('executive_m', 'EXECUTIVE', 'EXECUTIVE MARCUS', 'orchid_office'),
    ('influencer_f', 'INFLUENCER', 'INFLUENCER CHLOE', 'orchid_mall'),
    ('getai_f', 'SINGER', 'SINGER LILY', 'orchid_void_deck'),
    ('nyonya_f', 'NYONYA', 'NYONYA BEE LIAN', 'orchid_ruins'),
    ('dancer_f', 'CLASSICAL DANCER', 'DANCER PRIYA', 'orchid_mall'),
    ('orchid_keeper_f', 'ORCHID KEEPER', 'ORCHID KEEPER ANITA', 'orchid_jungle'),
    ('recruit_m', 'RECRUIT', 'RECRUIT DARREN', 'orchid_grass'),
]
EDITS = [
    ('edit_expert_m', 'Expert ♂ → Tai Chi Uncle', 'expert_m', 'expert_m', 'orchid_grass', 'EXPERT WEI MING', 'replace'),
    ('edit_school_kid_m', 'School Kid ♂ → Tosa uniform', 'school_kid_m', 'school_kid_m', 'orchid_grass', 'SCHOOL KID RYAN', 'replace'),
    ('edit_school_kid_f', 'School Kid ♀ → Tosa uniform', 'school_kid_f', None, 'orchid_grass', 'SCHOOL KID MEI', 'replace'),
    ('edit_sailor', 'Sailor → Port Worker', 'sailor', 'sailor', 'orchid_beach', 'PORT WORKER KUMAR', 'new'),
    ('edit_black_belt', 'Black Belt → recolour, no headband', 'black_belt', 'black_belt', 'orchid_grass', 'BLACK BELT RAZAK', 'replace'),
]
PY = sys.executable


def b64(im_or_path, scale=1):
    im = Image.open(im_or_path) if isinstance(im_or_path, str) else im_or_path
    if scale != 1:
        im = im.convert('RGBA').resize((im.width * scale, im.height * scale), Image.NEAREST)
    buf = io.BytesIO()
    im.save(buf, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()


def b64file(path):
    mime = 'image/gif' if path.endswith('.gif') else 'image/png'
    return f'data:{mime};base64,' + base64.b64encode(open(path, 'rb').read()).decode()


def battle(id_, env, who):
    src = os.path.join(OUT, f'{id_}_front.png')
    dst = os.path.join(OUT, f'{id_}_battle.png')
    subprocess.run([PY, os.path.join(HERE, 'battle_mock.py'), src, env, who, dst], check=True,
                   capture_output=True)
    return dst


def trans(path):
    """Indexed PNG -> RGBA with slot 0 transparent."""
    p = kit.Pic.from_png(path)
    return p.render(1)


def ow_strip(path, frames=(0, 2, 1), flip_last=True):
    p = kit.Pic.from_png(path)
    ims = [p.frame(i).render(1) for i in frames]
    if flip_last:
        ims.append(p.frame(2).render(1).transpose(Image.FLIP_LEFT_RIGHT))
    out = Image.new('RGBA', (len(ims) * 18 - 2, 32), (0, 0, 0, 0))
    for i, im in enumerate(ims):
        out.alpha_composite(im, (i * 18, 0))
    return out.crop((0, 6, out.width, 32))


def md(id_):
    p = os.path.join(CLS, id_ + '.md')
    return open(p).read() if os.path.exists(p) else ''


def md_html(text):
    """Tiny markdown: headings dropped, bullets -> list, **bold**, `code`."""
    out, inlist = [], False
    for line in text.strip().split('\n'):
        s = line.strip()
        if not s or s.startswith('#'):
            if inlist:
                out.append('</ul>'); inlist = False
            continue
        s = html.escape(s)
        s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
        s = re.sub(r'`(.+?)`', r'<code>\1</code>', s)
        if s.startswith(('- ', '* ')):
            if not inlist:
                out.append('<ul>'); inlist = True
            out.append(f'<li>{s[2:]}</li>')
        else:
            if inlist:
                out.append('</ul>'); inlist = False
            out.append(f'<p>{s}</p>')
    if inlist:
        out.append('</ul>')
    return '\n'.join(out)


def lineup_fronts(ids):
    ims = [trans(os.path.join(OUT, f'{i}_front.png')) for i in ids if os.path.exists(os.path.join(OUT, f'{i}_front.png'))]
    out = Image.new('RGBA', (len(ims) * 60 + 4, 64), (0, 0, 0, 0))
    for k, im in enumerate(ims):
        out.alpha_composite(im, (k * 60 - 2, 0))
    return out


def lineup_ow(ids, vanilla=('youngster', 'lass', 'man_3', 'woman_2')):
    ims = []
    for v in vanilla:
        ims.append(('v', kit.load_ow(v).frame(0).render(1)))
    pb = os.path.join(ROOT, 'graphics/object_events/pics/people/brendan/walking.png')
    if os.path.exists(pb):
        ims.insert(0, ('v', kit.Pic.from_png(pb).frame(0).render(1)))
    for i in ids:
        p = os.path.join(OUT, f'{i}_ow.png')
        if os.path.exists(p):
            ims.append(('n', kit.Pic.from_png(p).frame(0).render(1)))
    out = Image.new('RGBA', (len(ims) * 18 + 6, 26), (0, 0, 0, 0))
    x = 0
    for k, (kind, im) in enumerate(ims):
        if kind == 'n' and ims[k - 1][0] == 'v':
            x += 6
        out.alpha_composite(im.crop((0, 6, 16, 32)), (x, 0))
        x += 18
    return out.crop((0, 0, x, 26))


def class_card(id_, label, who, env):
    f = os.path.join(OUT, f'{id_}_front.png')
    o = os.path.join(OUT, f'{id_}_ow.png')
    if not os.path.exists(f):
        return f'<article class="card missing"><h3>{html.escape(label)}</h3><p>Not drawn yet.</p></article>'
    bt = battle(id_, env, who)
    parts = [f'<article class="card" id="{id_}">',
             f'<header><h3>{html.escape(label)}</h3><span class="id">{id_}</span></header>',
             '<div class="cols">',
             f'<figure class="battle"><img class="px" style="--w:240px" src="{b64(bt)}" alt="{html.escape(label)} battle intro mock">'
             f'<figcaption>Battle intro, 240×160 shown 2×</figcaption></figure>',
             '<div class="side">',
             f'<figure class="front"><img class="px" style="--w:64px" src="{b64(trans(f))}" alt="front pic">'
             f'<figcaption>Front pic 64×64, 3×</figcaption></figure>']
    if os.path.exists(o):
        parts.append(f'<figure class="ow"><img class="px" style="--w:70px" src="{b64(ow_strip(o))}" alt="overworld stand frames">'
                     f'<figcaption>OW stand ↓ ← ↑ →, 4×</figcaption></figure>')
        gif = os.path.join(OUT, f'{id_}_ow_walk.gif')
        if os.path.exists(gif):
            parts.append(f'<figure class="walk"><img class="pxg" src="{b64file(gif)}" alt="walk cycle">'
                         f'<figcaption>Walk cycle</figcaption></figure>')
    parts.append('</div></div>')
    notes = md(id_)
    if notes:
        parts.append(f'<div class="notes">{md_html(notes)}</div>')
    parts.append('</article>')
    return '\n'.join(parts)


LANDS = {'replace': ('Replaces vanilla GFX', 'Same job: the vanilla class keeps its name and gets these sprites.'),
         'new': ('New class + sprites', 'Different job: added as its own class, front pic and OW; the vanilla class stays.')}


def edit_card(id_, label, base_front, base_ow, env, who, lands):
    f = os.path.join(OUT, f'{id_}_front.png')
    if not os.path.exists(f):
        return f'<article class="card missing"><h3>{html.escape(label)}</h3><p>Not drawn yet.</p></article>'
    notes = md(id_)
    m = re.search(r'base[^:]*:\s*`?([a-z_]+)', notes, re.I)
    bf = base_front or (m.group(1) if m else None)
    bt = battle(id_, env, who)
    tag, why = LANDS[lands]
    parts = [f'<article class="card edit" id="{id_}">',
             f'<header><h3>{html.escape(label)}</h3><span class="land {lands}">{tag}</span><span class="id">{id_}</span></header>',
             f'<p class="why">{why}</p>',
             '<div class="cols"><div class="pair">']
    if bf and os.path.exists(os.path.join(kit.FRONT_DIR, bf + '.png')):
        parts.append(f'<figure><img class="px" style="--w:64px" src="{b64(kit.load_front(bf).render(1))}" alt="vanilla"><figcaption>Vanilla</figcaption></figure>')
    parts.append(f'<figure><img class="px" style="--w:64px" src="{b64(trans(f))}" alt="edit"><figcaption>Orchid edit</figcaption></figure>')
    o = os.path.join(OUT, f'{id_}_ow.png')
    if os.path.exists(o):
        if base_ow:
            parts.append(f'<figure><img class="px" style="--w:70px" src="{b64(ow_strip(os.path.join(kit.OW_DIR, base_ow + ".png")))}" alt="vanilla OW"><figcaption>Vanilla OW</figcaption></figure>')
        parts.append(f'<figure><img class="px" style="--w:70px" src="{b64(ow_strip(o))}" alt="edit OW"><figcaption>Edit OW</figcaption></figure>')
    parts.append('</div>')
    parts.append(f'<figure class="battle sm"><img class="px" style="--w:240px" src="{b64(bt)}" alt="battle mock"></figure></div>')
    if notes:
        parts.append(f'<div class="notes">{md_html(notes)}</div>')
    parts.append('</article>')
    return '\n'.join(parts)


def build():
    tpl = open(os.path.join(HERE, 'review_template.html')).read()
    ids = [c[0] for c in NEW]
    lf = lineup_fronts(ids)
    lo = lineup_ow(ids)
    page = tpl
    page = page.replace('{{LINEUP_FRONTS}}', f'<img class="px" style="--w:{lf.width}px" src="{b64(lf)}" alt="all new front pics at 1x">')
    page = page.replace('{{LINEUP_OW}}', f'<img class="px" style="--w:{lo.width}px" src="{b64(lo)}" alt="overworld line-up with vanilla NPCs">')
    import review_text as T
    page = page.replace('{{INTRO}}', T.INTRO)
    page = page.replace('{{SUGGESTIONS}}', T.SUGGESTIONS)
    page = page.replace('{{QUESTIONS}}', T.QUESTIONS)
    toc = ' '.join(f'<a href="#{c[0]}">{html.escape(c[1])}</a>' for c in NEW)
    page = page.replace('{{TOC}}', f'<nav class="toc">{toc}</nav>')
    page = page.replace('{{CLASSES}}', '\n'.join(class_card(*c) for c in NEW))
    page = page.replace('{{EDITS}}', '\n'.join(edit_card(*e) for e in EDITS))
    dst = os.path.join(OUT, 'review.html')
    open(dst, 'w').write(page)
    print(dst, f'{len(page) // 1024} KB')


if __name__ == '__main__':
    build()
