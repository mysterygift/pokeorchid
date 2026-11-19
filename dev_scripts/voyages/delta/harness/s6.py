from common import *
import struct
e=start()
def bm(i):
    b=e.read(e.syms['gBattleMons']+140*i,0x30)
    return struct.unpack('<H',b[0:2])[0], list(b[0x22:0x25]), struct.unpack('<H',b[0x2A:0x2C])[0]
try:
    e.press('R','START',after=60); e.press('DOWN'); e.press('DOWN'); e.press('A',after=30)
    for _ in range(13): e.press('DOWN',after=6)
    shot(e,'f0_menu.png')
    e.press('A',after=600); shot(e,'f1_battle.png'); print(cb2(e))
    for _ in range(4):
        e.press('B',after=120)
    shot(e,'f2_battle.png')
    print('player', bm(0), 'enemy', bm(1))
    print('SPECIES_GYARADOS_DELTA expected', 'types ELECTRIC=14 STEEL=9')
finally:
    e.close()
strip('f_strip.png',cols=3)
