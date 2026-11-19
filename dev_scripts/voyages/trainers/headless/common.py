import sys, os, struct, re
sys.path.insert(0, '/Users/arandavies/Development/pokemon-orchid/pokeorchid-voy-trainers/dev_scripts/mgba_headless')
S = os.path.dirname(os.path.abspath(__file__)); os.chdir(S)
from boot import boot, pos, warp, walk
ROOT = '/Users/arandavies/Development/pokemon-orchid/pokeorchid-voy-trainers'

DEC = {}
for line in open(os.path.join(ROOT, 'charmap.txt'), encoding='utf-8'):
    m = re.match(r"^'(.+?)'\s*=\s*([0-9A-F]{2})\s*$", line)
    if m and len(m.group(2)) == 2:
        DEC.setdefault(int(m.group(2), 16), m.group(1))
DEC[0x00] = ' '; DEC[0xFE] = '\\n'; DEC[0xFA] = '\\l'; DEC[0xFB] = '\\p'; DEC[0x39] = '<NBSP>'


def decode(b):
    out = ''
    for c in b:
        if c == 0xFF:
            break
        out += DEC.get(c, '{%02X}' % c)
    return out


FLAGS = 0x1270
VARS = 0x139C


def set_flag(e, flag, on=True):
    sb1 = e.r32('gSaveBlock1Ptr')
    a = sb1 + FLAGS + flag // 8
    v = e.r8(a)
    v = v | (1 << (flag % 8)) if on else v & ~(1 << (flag % 8))
    e.w8(a, v)


def get_flag(e, flag):
    sb1 = e.r32('gSaveBlock1Ptr')
    return bool(e.r8(sb1 + FLAGS + flag // 8) >> (flag % 8) & 1)


def song(e):
    hdr = e.r32('gMPlayInfo_BGM')
    for n in ('mus_orchid_vs_cynthia', 'mus_orchid_encounter_cynthia', 'mus_orchid_vs_trainer', 'mus_slateport'):
        if e.syms.get(n) == hdr:
            return n
    return hex(hdr)


def start(name='h'):
    e = boot(os.path.join(S, name))
    e.press('B', after=40)
    return e


def idle(e):
    return e.r8('sGlobalScriptContextStatus') == 2 and e.r8('sLockFieldControls') == 0
