from common import *

def try_battle(e, tid, tag):
    e.press('R', 'START', after=60)
    for _ in range(6): e.press('DOWN', after=6)
    e.press('A', after=40)
    p = e.r32('sDebugMenuListData')
    e.write(p + 736, struct.pack('<hh', tid, -1))
    for _ in range(5): e.press('DOWN', after=6)
    e.press('A', after=10)
    seen = None
    for k in range(200):
        e.frames(10)
        t = decode(e.read(e.sym('gDisplayedStringBattle'), 120))
        if 'challenged' in t:
            e.frames(30)
            e.shot('shots/f_%s_intro.png' % tag)
            seen = t
            break
    print(tag, 'trainer', e.r16(e.sym('gTrainerBattleParameter') + 2), 'song', song(e), repr(seen))
    for k in range(60):
        t = decode(e.read(e.sym('gDisplayedStringBattle'), 120))
        if 'What will' in t:
            break
        e.press('B', after=20)
    e.frames(20)
    e.shot('shots/f_%s_field.png' % tag)

# 1) exterior + café walls
e = start()
try:
    warp(e, 20, 9, 10)
    e.frames(30)
    print('exterior pos', pos(e))
    walk(e, 'DOWN', 1)
    e.frames(20)
    e.shot('shots/g_changu_exterior.png')
    walk(e, 'UP', 1)   # bump the door -> café
    e.frames(120)
    print('after door', pos(e))
    walk(e, 'UP', 5)
    e.frames(20)
    print('room pos', pos(e))
    e.shot('shots/g_cafe_walls.png')
    walk(e, 'RIGHT', 5); walk(e, 'UP', 1)
    e.press('A', after=60)
    e.shot('shots/g_barista.png')
    e.press('A', after=30)
finally:
    e.close()
# 2) Holon Researcher (Christophe, 26) intro text
e = start()
try:
    try_battle(e, 26, 'researcher')
finally:
    e.close()
# 3) Lake Cynthia (23) via Try Battle: music
e = start()
try:
    try_battle(e, 23, 'cynthia_lake')
finally:
    e.close()
