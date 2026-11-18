"""Prove the trainer-class art landed in the BUILT ROM, without an emulator.

Run from dev_scripts/trainer_classes/ after `make`:  python verify_ingame.py

For every sprite in install.SPRITES this follows the same pointers the game follows, reading pokeemerald.gba
with addresses from `arm-none-eabi-nm pokeemerald.elf`:
- front pic:  gTrainerPicInfo[TRAINER_PIC_X].frontPic -> {imageData, paletteData}; imageData is smol-compressed,
              so the slice is decompressed with tools/compresSmol -d, then decoded as 8x8 4bpp tiles.
- class name: gTrainerClasses[TRAINER_CLASS_X].name decoded from the Gen 3 charset.
- overworld:  gObjectEventGraphicsInfoPointers[OBJ_EVENT_GFX_X] -> info.paletteTag + info.images; the palette is
              resolved through sObjectEventSpritePalettes by tag, as FindObjectEventPaletteIndexByTag does.
              9 frames of 16x32 (2x4 tiles) read from the images' data pointer.
Enum values come from parsing include/constants/*.h (cross-checked: every class name decoded from the ROM
must equal the expected string, which fails loudly if the parsed ordinal is off).

Each decoded sprite is compared pixel-for-pixel (indices) and colour-for-colour (BGR555) with its out/ source.
Writes out/ingame/<id>_front_rom.png, out/ingame/<id>_ow_rom.png and out/ingame/contact_sheet.png
(every front pic and all 9 OW frames, rendered from the ROM bytes with the ROM palettes).
"""
import os
import re
import struct
import subprocess
import sys
import tempfile
from PIL import Image, ImageDraw

from kit import ROOT, OUT, rgb555
from install import SPRITES, npc_palette

ROM = os.path.join(ROOT, 'pokeemerald.gba')
ELF = os.path.join(ROOT, 'pokeemerald.elf')
SMOL = os.path.join(ROOT, 'tools/compresSmol/compresSmol')
INGAME = os.path.join(OUT, 'ingame')
os.makedirs(INGAME, exist_ok=True)

# out id -> (TRAINER_PIC_*, TRAINER_CLASS_*, expected class name, OBJ_EVENT_GFX_*)
WIRING = {
    'tourist_m':         ('TOURIST_M',    'TOURIST',     'TOURIST',     'TOURIST_M'),
    'tourist_f':         ('TOURIST_F',    'TOURIST',     'TOURIST',     'TOURIST_F'),
    'hawker_m':          ('HAWKER_M',     'HAWKER',      'HAWKER',      'HAWKER_M'),
    'hawker_f':          ('HAWKER_F',     'HAWKER',      'HAWKER',      'HAWKER_F'),
    'delivery_m':        ('RIDER',        'RIDER',       'RIDER',       'RIDER'),
    'executive_m':       ('EXECUTIVE',    'EXECUTIVE',   'EXECUTIVE',   'EXECUTIVE'),
    'influencer_f':      ('INFLUENCER',   'INFLUENCER',  'INFLUENCER',  'INFLUENCER'),
    'getai_f':           ('SINGER',       'SINGER',      'SINGER',      'SINGER'),
    'nyonya_f':          ('NYONYA',       'NYONYA',      'NYONYA',      'NYONYA'),
    'dancer_f':          ('DANCER',       'DANCER',      'DANCER',      'DANCER'),
    'orchid_keeper_f':   ('ORCHIDIST',    'ORCHIDIST',   'ORCHIDIST',   'ORCHIDIST'),
    'recruit_m':         ('RECRUIT',      'RECRUIT',     'RECRUIT',     'RECRUIT'),
    'edit_sailor':       ('PORT_WORKER',  'PORT_WORKER', 'PORT WORKER', 'PORT_WORKER'),
    'edit_expert_m':     ('EXPERT_M',     'EXPERT',      'EXPERT',      'EXPERT_M'),
    'edit_black_belt':   ('BLACK_BELT',   'BLACK_BELT',  'BLACK BELT',  'BLACK_BELT'),
    'edit_school_kid_m': ('SCHOOL_KID_M', 'SCHOOL_KID',  'SCHOOL KID',  'SCHOOL_KID_M'),
    'edit_school_kid_f': ('SCHOOL_KID_F', 'SCHOOL_KID',  'SCHOOL KID',  'SCHOOL_KID_F'),
    'ranger_m':          ('POKEMON_RANGER_M', 'PKMN_RANGER', 'PKMN RANGER', 'POKEMON_RANGER_M'),
    'ranger_f':          ('POKEMON_RANGER_F', 'PKMN_RANGER', 'PKMN RANGER', 'POKEMON_RANGER_F'),
}
PAL_TAG_NONE = 0x11FF


def enum_values(path, first, last):
    """Ordinals of a plain C enum (no explicit values) from `first` up to and including `last`."""
    src = re.sub(r'//[^\n]*|/\*.*?\*/', '', open(path).read(), flags=re.S)
    start = src.index(first + ',')
    end = src.index(last, start)
    names = [n.strip() for n in src[start:end + len(last)].split(',')]
    names = [n for n in names if n]
    for n in names:
        assert re.fullmatch(r'[A-Z0-9_]+', n), f'unexpected enum token {n!r} in {path}'
    return {n: i for i, n in enumerate(names)}


PICS = enum_values(os.path.join(ROOT, 'include/constants/trainers.h'), 'TRAINER_PIC_NONE', 'TRAINER_PIC_COUNT')
CLASSES = enum_values(os.path.join(ROOT, 'include/constants/trainers.h'), 'TRAINER_CLASS_PKMN_TRAINER_1', 'TRAINER_CLASS_COUNT')
GFX = enum_values(os.path.join(ROOT, 'include/constants/event_objects.h'), 'OBJ_EVENT_GFX_BRENDAN_NORMAL', 'NUM_OBJ_EVENT_GFX')

rom = open(ROM, 'rb').read()
syms, by_addr = {}, {}
for line in subprocess.run(['arm-none-eabi-nm', '-S', '--defined-only', ELF],
                           capture_output=True, text=True, check=True).stdout.splitlines():
    parts = line.split()
    if len(parts) == 4:
        addr, size, name = int(parts[0], 16), int(parts[1], 16), parts[3]
        syms[name] = (addr, size)
        by_addr[addr] = (name, size)


def rd(addr, n):
    off = addr - 0x08000000
    assert 0 <= off and off + n <= len(rom), hex(addr)
    return rom[off:off + n]


def u32(addr):
    return struct.unpack('<I', rd(addr, 4))[0]


def u16(addr):
    return struct.unpack('<H', rd(addr, 2))[0]


def palette(addr):
    out = []
    for i in range(16):
        c = u16(addr + 2 * i)
        out.append(((c & 31) << 3, ((c >> 5) & 31) << 3, ((c >> 10) & 31) << 3))
    return out


def tiles_to_px(data, wt, ht):
    """4bpp tiles (row-major, wt x ht tiles) -> rows of palette indices."""
    w, h = wt * 8, ht * 8
    px = [[0] * w for _ in range(h)]
    for t in range(wt * ht):
        tx, ty = t % wt, t // wt
        for y in range(8):
            for x in range(8):
                b = data[t * 32 + y * 4 + x // 2]
                px[ty * 8 + y][tx * 8 + x] = (b >> 4) if x & 1 else (b & 15)
    return px


def charset(raw):
    s = []
    for b in raw:
        if b == 0xFF:
            break
        if 0xBB <= b <= 0xD4:
            s.append(chr(ord('A') + b - 0xBB))
        elif 0xD5 <= b <= 0xEE:
            s.append(chr(ord('a') + b - 0xD5))
        elif 0xA1 <= b <= 0xAA:
            s.append(chr(ord('0') + b - 0xA1))
        else:
            s.append({0x00: ' ', 0x1B: 'é', 0xAD: '.', 0xB5: '♂', 0xB6: '♀', 0x53: 'PK', 0x54: 'MN'}.get(b, '?'))
    return ''.join(s)


def smol_decompress(addr):
    name, size = by_addr[addr]
    with tempfile.TemporaryDirectory() as d:
        src, dst = os.path.join(d, 'x.smol'), os.path.join(d, 'x.4bpp')
        open(src, 'wb').write(rd(addr, size))
        subprocess.run([SMOL, '-d', src, dst], check=True, capture_output=True)
        return name, open(dst, 'rb').read()


def load_src(path):
    im = Image.open(path)
    flat = im.getpalette()
    data = list(im.get_flattened_data() if hasattr(im, 'get_flattened_data') else im.getdata())
    px = [data[y * im.width:(y + 1) * im.width] for y in range(im.height)]
    return px, [rgb555(tuple(flat[i * 3:i * 3 + 3])) for i in range(16)]


def to_image(px, pal, transparent_bg=None):
    h, w = len(px), len(px[0])
    im = Image.new('RGB', (w, h))
    im.putdata([pal[i] if (i or transparent_bg is None) else transparent_bg for row in px for i in row])
    return im


def sprite_palettes():
    """sObjectEventSpritePalettes: {tag: palette data address}, terminated by OBJ_EVENT_PAL_TAG_NONE."""
    base, _ = syms['sObjectEventSpritePalettes']
    out, i = {}, 0
    while True:
        ptr, tag = u32(base + 8 * i), u16(base + 8 * i + 4)
        if tag == PAL_TAG_NONE:
            return out
        out.setdefault(tag, ptr)
        i += 1


def main():
    failures, rows = [], []
    spal = sprite_palettes()
    pic_info, _ = syms['gTrainerPicInfo']
    cls_tab, _ = syms['gTrainerClasses']
    gfx_ptrs, _ = syms['gObjectEventGraphicsInfoPointers']
    for sid, name, mode, npc in SPRITES:
        pic_c, cls_c, cls_name, gfx_c = WIRING[sid]
        rep = [f'{sid}:']
        # front pic
        front = u32(pic_info + 8 * PICS['TRAINER_PIC_' + pic_c])
        img_ptr, pal_ptr = u32(front), u32(front + 4)
        sym, data = smol_decompress(img_ptr)
        fpx = tiles_to_px(data, 8, 8)
        fpal = palette(pal_ptr)
        # 'ow' entries keep the vanilla front pic, so compare against graphics/ instead of out/
        front_src = (os.path.join(ROOT, 'graphics/trainers/front_pics', name + '.png') if mode == 'ow'
                     else os.path.join(OUT, sid + '_front.png'))
        spx, spal_src = load_src(front_src)
        ok_px, ok_pal = fpx == spx, fpal == spal_src
        rep.append(f'front {sym} px={"ok" if ok_px else "DIFF"} pal={"ok" if ok_pal else "DIFF"}')
        if not (ok_px and ok_pal):
            failures.append(f'{sid} front')
        # class name: struct TrainerClass { u8 name[13]; u8 money; u16 ball; } = 16 bytes; 12 chars max
        cls_addr = cls_tab + 16 * CLASSES['TRAINER_CLASS_' + cls_c]
        rom_name = charset(rd(cls_addr, 13))
        rep.append(f'class "{rom_name}"')
        if rom_name != cls_name:
            failures.append(f'{sid} class name {rom_name!r} != {cls_name!r}')
        # overworld
        info = u32(gfx_ptrs + 4 * GFX['OBJ_EVENT_GFX_' + gfx_c])
        tag, images = u16(info + 2), u32(info + 0x1C)
        frame_ptr, frame_size = u32(images), u16(images + 4)
        assert frame_size == 256, frame_size
        img_sym = by_addr.get(frame_ptr, ('?', 0))
        frames = [tiles_to_px(rd(frame_ptr + 256 * f, 256), 2, 4) for f in range(9)]
        opx = [sum((frames[f][y] for f in range(9)), []) for y in range(32)]
        opal = palette(spal[tag])
        sopx, _ = load_src(os.path.join(OUT, sid + '_ow.png'))
        ok_opx, ok_opal = opx == sopx, opal == npc_palette(npc)
        if img_sym[1] and img_sym[1] != 9 * 256:
            failures.append(f'{sid} OW sheet is {img_sym[1]} bytes, not 9 frames')
        rep.append(f'OW {img_sym[0]} tag=0x{tag:04X} pal={by_addr.get(spal[tag], ("?",))[0]} '
                   f'px={"ok" if ok_opx else "DIFF"} pal={"ok" if ok_opal else "DIFF"}')
        if not (ok_opx and ok_opal):
            failures.append(f'{sid} OW')
        print(' '.join(rep))
        fim = to_image(fpx, fpal)
        oim = to_image(opx, opal)
        fim.save(os.path.join(INGAME, sid + '_front_rom.png'))
        oim.save(os.path.join(INGAME, sid + '_ow_rom.png'))
        rows.append((sid, mode, pic_c, cls_c, rom_name, gfx_c, fim, oim))
    contact_sheet(rows)
    if failures:
        print('FAIL:', *failures, sep='\n  ')
        sys.exit(1)
    print(f'all {len(rows)} sprites match their out/ sources in the ROM')


def contact_sheet(rows):
    O = 3                              # front x2 (128px), OW x3 (48x96 per frame)
    cw, ch = 10 + 128 + 10 + 9 * 16 * O + 10, 128 + 44
    sheet = Image.new('RGB', (cw * 2, ch * ((len(rows) + 1) // 2) + 30), (40, 40, 48))
    d = ImageDraw.Draw(sheet)
    d.text((10, 8), 'Orchid trainer classes, decoded from pokeemerald.gba (front pic x2, OW frames 0-8 x3)',
           fill=(255, 255, 255))
    for i, (sid, mode, pic_c, cls_c, name, gfx_c, fim, oim) in enumerate(rows):
        x0, y0 = (i % 2) * cw, 30 + (i // 2) * ch
        sheet.paste(fim.resize((128, 128), Image.NEAREST), (x0 + 10, y0 + 22))
        sheet.paste(oim.resize((144 * O, 32 * O), Image.NEAREST), (x0 + 148, y0 + 22 + 16))
        d.text((x0 + 10, y0 + 6), f'{name}  [{mode}]  {sid}', fill=(255, 230, 120))
        d.text((x0 + 148, y0 + 22 + 16 + 32 * O + 6),
               f'TRAINER_PIC_{pic_c}\nOBJ_EVENT_GFX_{gfx_c}', fill=(190, 190, 200))
    sheet.save(os.path.join(INGAME, 'contact_sheet.png'))
    print('wrote', os.path.relpath(os.path.join(INGAME, 'contact_sheet.png'), ROOT))


if __name__ == '__main__':
    main()
