from common import *
e = start()
OPP = e.sym('gParties') + 600
try:
    set_flag(e, 0x1AA)
    warp(e, 21, 121, 0)
    e.frames(30)
    walk(e, 'UP', 3); print('pos', pos(e))
    e.shot('shots/d_cafe_room.png')
    walk(e, 'DOWN', 2); print('pos', pos(e))
    walk(e, 'RIGHT', 5); print('pos', pos(e))
    e.press('UP', hold=2, after=10)
    e.press('A', after=30)
    print('song at greeting', song(e))
    e.shot('shots/d_cynthia_greet.png')
    for i in range(12):
        e.press('A', after=40)
        print('  A', i, 'song', song(e))
        if i == 1:
            e.shot('shots/d_cynthia_wonderful.png')
        if e.r32(OPP + 0) != 0:
            break
    print('party created after', i, 'song', song(e))
    # wait for party creation, then swap slot 0 <-> 5 so Garchomp leads
    for f in range(400):
        if e.r32(OPP + 5 * 100) != 0:
            break
        e.frames(1)
    a, b = e.read(OPP, 100), e.read(OPP + 500, 100)
    e.write(OPP, b); e.write(OPP + 500, a)
    print('swapped at frame', f)
    for k in range(8):
        e.frames(15)
        e.shot('shots/d_transition_%02d.png' % k)
    print('song in transition', song(e))
    for k in range(40):
        if k == 14:
            e.press('B', after=10)
        e.frames(20)
        sp = struct.unpack('<H', e.read(e.sym('gBattleMons') + 140, 2))[0]
        txt = decode(e.read(e.sym('gDisplayedStringBattle'), 120))
        if k % 4 == 0:
            e.shot('shots/d_battle_%02d.png' % k)
        print(k, 'opp species', sp, 'song', song(e), repr(txt[:80]))
    for k in range(100):
        e.frames(10)
        t = decode(e.read(e.sym('gDisplayedStringBattle'), 60))
        if k == 2:
            e.shot('shots/d_sent_out.png')
        if 'What will' in t:
            break
        e.press('B', after=20)
    e.frames(30)
    e.shot('shots/d_battle_menu.png')
    e.press('A', after=30); e.shot('shots/d_fight_menu.png'); e.press('A', after=10)
    for k in range(120):
        e.frames(10)
        sp = struct.unpack('<H', e.read(e.sym('gBattleMons') + 140, 2))[0]
        txt = decode(e.read(e.sym('gDisplayedStringBattle'), 120))
        if k % 6 == 0 or sp == 947:
            print(k, sp, repr(txt[:70]))
        if sp == 947:
            e.frames(1)
            for j in range(6):
                e.shot('shots/d_mega_%d.png' % j); e.frames(40); e.shot('shots/d_mega.png'); print('MEGA'); break
finally:
    e.close()
