"""Trainer-class sprite kit: kitbash Gen 3 trainer front pics (64x64) and OW sheets (144x32)
from vanilla art with palette remaps and ASCII pixel patches, then validate against Gen 3 limits.

Typical class script (classes/<id>.py):

    from kit import *
    f = load_front('sailor')              # vanilla base, indices + its own 16-colour palette
    print(f.dump(16, 0, 48, 30))          # see the pixels you are about to edit (one hex char per index)
    f.set_pal(9, (240, 240, 240))         # recolour a whole ramp slot
    f.remap({7: 9})                       # move pixels from slot 7 to slot 9
    f.patch(20, 10, '''
        ..FFF..
        .F111F.
    ''', {'F': 15, '1': 1})               # '.' = keep, '_' = transparent (0), mapped chars = palette index
    f.save_front('hawker_m')              # out/hawker_m_front.png (indexed, BGR555-rounded) + checks

    o = load_ow('fat_man')                # 9 frames, palette = one shared NPC palette
    o.to_npc_pal('npc_2', {...})          # optional: move to another shared palette by index map
    o.patch_frame(0, 0, 10, '''...''', key)
    o.save_ow('hawker_m', 'npc_2')        # out/hawker_m_ow.png + walk GIF + checks

Frame order (OW): 0 down, 1 up, 2 left, 3-4 walk down, 5-6 walk up, 7-8 walk left. Right = hflip(left).
"""
import os
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
FRONT_DIR = os.path.join(ROOT, 'graphics/trainers/front_pics')
OW_DIR = os.path.join(ROOT, 'graphics/object_events/pics/people')
NPC_PAL_DIR = os.path.join(ROOT, 'graphics/object_events/palettes')
OUT = os.path.join(os.path.dirname(__file__), 'out')
os.makedirs(OUT, exist_ok=True)

BG = (115, 197, 164)
HEX = '0123456789ABCDEF'


def rgb555(c):
    """Round a colour the way gbagfx does (to multiples of 8, BGR555)."""
    return tuple((v >> 3) << 3 for v in c)


def read_jasc(path):
    lines = open(path).read().split('\n')
    n = int(lines[2])
    return [tuple(int(v) for v in lines[3 + i].split()) for i in range(n)]


def npc_pal(name):
    """Shared NPC palette by name, or a custom one written to out/<name>.pal (JASC) for a cloned NPC
    that needs its own palette (costs an OBJ palette slot when on screen)."""
    p = os.path.join(NPC_PAL_DIR, name + '.pal')
    if not os.path.exists(p):
        p = os.path.join(OUT, name + '.pal')
    return read_jasc(p)


def write_jasc(path, pal):
    with open(path, 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n%d\n' % len(pal))
        for c in pal:
            f.write('%d %d %d\n' % tuple(rgb555(c)))


NPC_PALS = ['npc_1', 'npc_2', 'npc_3', 'npc_4', 'npc_white', 'npc_blue', 'npc_green', 'npc_pink']


class Pic:
    def __init__(self, w, h, px=None, pal=None):
        self.w, self.h = w, h
        self.px = px if px is not None else [[0] * w for _ in range(h)]
        self.pal = list(pal) if pal else [BG] + [(0, 0, 0)] * 15

    @classmethod
    def from_png(cls, path):
        im = Image.open(path)
        assert im.mode == 'P', f'{path} is not indexed'
        flat = im.getpalette()
        pal = [tuple(flat[i * 3:i * 3 + 3]) for i in range(16)]
        data = list(im.getdata()) if not hasattr(im, 'get_flattened_data') else list(im.get_flattened_data())
        px = [data[y * im.width:(y + 1) * im.width] for y in range(im.height)]
        return cls(im.width, im.height, px, pal)

    def copy(self):
        return Pic(self.w, self.h, [r[:] for r in self.px], self.pal)

    # ---- palette ----
    def set_pal(self, slot, rgb):
        self.pal[slot] = tuple(rgb)

    def remap(self, mapping, region=None):
        """Change pixel indices: mapping {old: new}. region=(x0,y0,x1,y1) inclusive limits the change."""
        x0, y0, x1, y1 = region or (0, 0, self.w - 1, self.h - 1)
        for y in range(y0, y1 + 1):
            row = self.px[y]
            for x in range(x0, x1 + 1):
                if row[x] in mapping:
                    row[x] = mapping[row[x]]

    def used(self):
        return sorted({v for r in self.px for v in r})

    # ---- pixels ----
    def get(self, x, y):
        return self.px[y][x]

    def put(self, x, y, i):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[y][x] = i

    def fill(self, x0, y0, x1, y1, i):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.put(x, y, i)

    def clear(self, x0, y0, x1, y1):
        self.fill(x0, y0, x1, y1, 0)

    def patch(self, x, y, art, key=None):
        """Stamp ASCII art at (x, y). '.' keeps the pixel, '_' = transparent, hex digits 0-F map to
        that palette index directly, other chars go through key. Leading/trailing blank lines and
        common indentation are stripped."""
        key = key or {}
        lines = [l for l in art.split('\n')]
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
        ind = min(len(l) - len(l.lstrip()) for l in lines if l.strip())
        for dy, line in enumerate(lines):
            for dx, ch in enumerate(line[ind:]):
                if ch in ' .':
                    continue
                if ch == '_':
                    v = 0
                elif ch in key:
                    v = key[ch]
                elif ch in HEX:
                    v = HEX.index(ch)
                else:
                    raise ValueError(f'unmapped char {ch!r}')
                self.put(x + dx, y + dy, v)

    def blit(self, src, sx0, sy0, sx1, sy1, dx, dy, transparent=True, flip=False):
        """Copy a region of another Pic (same palette layout) to (dx, dy)."""
        for y in range(sy0, sy1 + 1):
            for x in range(sx0, sx1 + 1):
                v = src.px[y][sx1 - (x - sx0) if flip else x]
                if transparent and v == 0:
                    continue
                self.put(dx + x - sx0, dy + y - sy0, v)

    def shift(self, x0, y0, x1, y1, dx, dy):
        """Move a region by (dx, dy), clearing what it leaves behind."""
        tmp = self.copy()
        self.clear(x0, y0, x1, y1)
        self.blit(tmp, x0, y0, x1, y1, x0 + dx, y0 + dy)

    def outline(self, color=15, region=None, only_on=(0,)):
        """Add a 1px outline in `color` around non-transparent pixels (into transparent pixels)."""
        x0, y0, x1, y1 = region or (0, 0, self.w - 1, self.h - 1)
        src = self.copy()
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if src.px[y][x] not in only_on:
                    continue
                for ax, ay in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + ax, y + ay
                    if 0 <= nx < self.w and 0 <= ny < self.h and src.px[ny][nx] not in (0,) and src.px[ny][nx] != color:
                        self.px[y][x] = color
                        break

    def dump(self, x0=0, y0=0, x1=None, y1=None):
        """Hex dump of a region with column/row rulers, '.' for transparent."""
        x1 = self.w - 1 if x1 is None else x1
        y1 = self.h - 1 if y1 is None else y1
        head = '    ' + ''.join(str((x // 10) % 10) for x in range(x0, x1 + 1))
        head2 = '    ' + ''.join(str(x % 10) for x in range(x0, x1 + 1))
        rows = [head, head2]
        for y in range(y0, y1 + 1):
            rows.append(f'{y:3d} ' + ''.join('.' if self.px[y][x] == 0 else HEX[self.px[y][x]] for x in range(x0, x1 + 1)))
        return '\n'.join(rows)

    def pal_str(self):
        return '\n'.join(f'{HEX[i]}: {c}' for i, c in enumerate(self.pal))

    # ---- output ----
    def to_image(self):
        im = Image.new('P', (self.w, self.h))
        flat = []
        for c in self.pal:
            flat += list(rgb555(c))
        im.putpalette(flat + [0] * (768 - len(flat)))
        im.putdata([v for r in self.px for v in r])
        return im

    def render(self, scale=1, bg=None):
        im = self.to_image().convert('RGBA')
        if bg is not None:
            b = Image.new('RGBA', im.size, bg)
            mask = Image.new('L', im.size, 0)
            mask.putdata([0 if v == 0 else 255 for r in self.px for v in r])
            b.paste(im, (0, 0), mask)
            im = b
        else:
            data = list(im.getdata())
            flat = [v for r in self.px for v in r]
            im.putdata([(0, 0, 0, 0) if flat[i] == 0 else data[i] for i in range(len(data))])
        if scale != 1:
            im = im.resize((self.w * scale, self.h * scale), Image.NEAREST)
        return im

    # ---- OW frames ----
    def frame(self, i):
        f = Pic(16, 32, [r[i * 16:(i + 1) * 16] for r in self.px], self.pal)
        return f

    def set_frame(self, i, f):
        for y in range(32):
            self.px[y][i * 16:(i + 1) * 16] = f.px[y][:16]

    def patch_frame(self, i, x, y, art, key=None):
        f = self.frame(i)
        f.patch(x, y, art, key)
        self.set_frame(i, f)

    def frames(self, idx=range(9)):
        return [self.frame(i) for i in idx]

    # ---- saving with checks ----
    def save_front(self, name):
        problems = check_front(self)
        p = os.path.join(OUT, f'{name}_front.png')
        self.to_image().save(p)
        self.render(4, (232, 232, 232)).save(os.path.join(OUT, f'{name}_front_x4.png'))
        return p, problems

    def save_ow(self, name, palname):
        problems = check_ow(self, palname)
        p = os.path.join(OUT, f'{name}_ow.png')
        self.to_image().save(p)
        ow_preview(self).save(os.path.join(OUT, f'{name}_ow_x6.png'))
        ow_gif(self, os.path.join(OUT, f'{name}_ow_walk.gif'))
        return p, problems


def load_front(name):
    return Pic.from_png(os.path.join(FRONT_DIR, name + '.png'))


def load_ow(name, sub=None):
    p = os.path.join(OW_DIR, (sub + '/' if sub else '') + name + '.png')
    pic = Pic.from_png(p)
    if pic.w > 144:  # keep only the 9 walking frames
        pic = Pic(144, 32, [r[:144] for r in pic.px], pic.pal)
    return pic


def blank_ow(palname):
    return Pic(144, 32, None, npc_pal(palname))


def check_front(pic):
    probs = []
    if (pic.w, pic.h) != (64, 64):
        probs.append(f'size {pic.w}x{pic.h} != 64x64')
    if len(pic.used()) > 16:
        probs.append('more than 16 indices')
    if rgb555(pic.pal[0]) != rgb555(BG):
        probs.append(f'slot 0 is {pic.pal[0]} not transparent mint')
    seen = {}
    for i, c in enumerate(pic.pal):
        if i in pic.used() and i:
            k = rgb555(c)
            if k in seen:
                probs.append(f'slots {seen[k]} and {i} round to the same colour {k}')
            seen[k] = i
    # touching the frame edge reads as cropped in battle
    edge = [v for v in pic.px[0] + pic.px[63] + [r[0] for r in pic.px] + [r[63] for r in pic.px] if v]
    if edge:
        probs.append(f'{len(edge)} pixels on the 64x64 edge (ok only if vanilla base also does)')
    return probs


def check_ow(pic, palname):
    probs = []
    want = npc_pal(palname)
    if [rgb555(c) for c in pic.pal[:16]] != [rgb555(c) for c in want]:
        probs.append(f'palette differs from shared {palname}')
    if (pic.w, pic.h) != (144, 32):
        probs.append(f'size {pic.w}x{pic.h} != 144x32')
    for i in range(9):
        f = pic.frame(i)
        if any(f.px[y][x] for y in range(0, 6) for x in range(16)):
            probs.append(f'frame {i}: pixels above y6 (vanilla people keep rows 0-9 mostly empty)')
    return probs


def ow_preview(pic, scale=6):
    """All 9 frames + a right-facing (flipped) stand frame on light grey, scaled."""
    frames = pic.frames()
    right = frames[2].render(1, (232, 232, 232)).transpose(Image.FLIP_LEFT_RIGHT)
    tiles = [f.render(1, (232, 232, 232)) for f in frames] + [right]
    out = Image.new('RGBA', (len(tiles) * 18, 32), (200, 200, 200, 255))
    for i, t in enumerate(tiles):
        out.paste(t, (i * 18, 0))
    return out.resize((out.width * scale, out.height * scale), Image.NEAREST)


def ow_gif(pic, path, scale=4):
    """Walk cycle in all four directions: stand, A, stand, B."""
    seqs = [(0, 3, 0, 4), (1, 5, 1, 6), (2, 7, 2, 8)]
    fr = []
    for k in range(4):
        row = []
        for s in seqs:
            row.append(pic.frame(s[k]).render(1, (232, 232, 232)))
        row.append(pic.frame(seqs[2][k]).render(1, (232, 232, 232)).transpose(Image.FLIP_LEFT_RIGHT))
        img = Image.new('RGBA', (4 * 20, 32), (232, 232, 232, 255))
        for j, r in enumerate(row):
            img.paste(r, (j * 20 + 2, 0))
        fr.append(img.resize((img.width * scale, img.height * scale), Image.NEAREST).convert('P', palette=Image.ADAPTIVE))
    fr[0].save(path, save_all=True, append_images=fr[1:], duration=170, loop=0)


def compare(name, base_front=None, base_ow=None, scale=4):
    """Side-by-side vanilla base vs new, front + OW, written to out/<name>_compare.png."""
    parts = []
    if base_front:
        parts.append(load_front(base_front).render(scale, (232, 232, 232)))
    nf = os.path.join(OUT, f'{name}_front.png')
    if os.path.exists(nf):
        parts.append(Pic.from_png(nf).render(scale, (232, 232, 232)))
    if base_ow:
        parts.append(ow_preview(load_ow(base_ow), scale))
    no = os.path.join(OUT, f'{name}_ow.png')
    if os.path.exists(no):
        parts.append(ow_preview(Pic.from_png(no), scale))
    W = max(p.width for p in parts[:2] + [Image.new('RGBA', (1, 1))]) * 2 + 8
    W = max(W, max(p.width for p in parts))
    H = 0
    rows = []
    if base_front or os.path.exists(nf):
        rows.append(parts[:2] if base_front else parts[:1])
    rows += [[p] for p in parts[len(rows[0]) if rows else 0:]]
    H = sum(max(p.height for p in r) + 8 for r in rows)
    out = Image.new('RGBA', (W, H), (70, 70, 70, 255))
    y = 0
    for r in rows:
        x = 0
        for p in r:
            out.paste(p, (x, y)); x += p.width + 8
        y += max(p.height for p in r) + 8
    path = os.path.join(OUT, f'{name}_compare.png')
    out.save(path)
    return path


def report(name, results):
    for p, probs in results:
        print(('OK   ' if not probs else 'WARN ') + os.path.relpath(p, ROOT))
        for pr in probs:
            print('     - ' + pr)
