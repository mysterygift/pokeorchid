from common import *
e = start()
try:
    warp(e, 20, 9, 10)
    e.frames(30)
    print('warped', pos(e)); walk(e, 'LEFT', 2); e.press('UP', hold=2, after=20)
    print('at sign', pos(e))
    e.press('A', after=60); e.shot('shots/g_cafe_sign.png'); e.press('A', after=20); e.press('A', after=30)
    walk(e, 'RIGHT', 2)
    print('before door', pos(e))
    walk(e, 'UP', 1)
    e.frames(250)
    print('after door', pos(e))
    walk(e, 'UP', 5)
    e.frames(20)
    print('room pos', pos(e))
    e.shot('shots/g_cafe_walls.png')
    walk(e, 'RIGHT', 5); e.press('UP', hold=2, after=20)
    print('barista spot', pos(e))
    e.press('A', after=90)
    e.shot('shots/g_barista.png')
    e.press('A', after=30)
finally:
    e.close()
e = start()
try:
    e.press('R', 'START', after=60)
    for _ in range(6): e.press('DOWN', after=6)
    e.press('A', after=40)
    e.write(e.r32('sDebugMenuListData') + 736, struct.pack('<hh', 26, -1))
    for _ in range(5): e.press('DOWN', after=6)
    e.press('A', after=10)
    for k in range(200):
        e.frames(10)
        if 'challenged' in decode(e.read(e.sym('gDisplayedStringBattle'), 120)):
            break
    e.frames(150)
    e.shot('shots/f_researcher_intro.png')
finally:
    e.close()
