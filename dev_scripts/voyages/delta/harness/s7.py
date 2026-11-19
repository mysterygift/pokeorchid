from common import *
import struct
e=start()
def bm(i):
    b=e.read(e.syms['gBattleMons']+140*i,0x30)
    return struct.unpack('<H',b[0:2])[0], list(b[0x22:0x25]), struct.unpack('<H',b[0x2A:0x2C])[0]
def lead():
    p=e.r32('gPlayerPartyPtr') if 'gPlayerPartyPtr' in e.syms else e.syms['gParties']
    return p
try:
    e.press('R','START',after=60); e.press('DOWN'); e.press('DOWN'); e.press('A',after=30)
    for _ in range(7): e.press('DOWN',after=6)
    e.press('A',after=60)  # Clear Pokerus (hacked: swap slot 0 and 2)
    e.press('R','START',after=60); e.press('DOWN'); e.press('DOWN'); e.press('A',after=30)
    for _ in range(13): e.press('DOWN',after=6)
    e.press('A',after=600)
    for _ in range(3): e.press('B',after=120)
    shot(e,'g0_battle.png'); print('player', bm(0), 'enemy', bm(1))
    e.write(e.syms['gBattleMons']+140+0x2A, struct.pack('<H',1))
    e.press('A',after=60); shot(e,'g1_fight.png')
    e.press('A',after=60)
    for i in range(40):
        e.press('A',after=90)
        if i%4==3: shot(e,'g2_%02d.png'%i)
        print(i, cb2(e))
finally:
    e.close()
strip('g_strip.png',cols=4)
