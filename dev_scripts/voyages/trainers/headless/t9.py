from common import *
for mode in ('available', 'done_today'):
    e = start()
    try:
        set_flag(e, 0x1AA)
        warp(e, 21, 121, 0)
        e.frames(30)
        sb1 = e.r32('gSaveBlock1Ptr')
        day = struct.unpack('<h', e.read(e.sym('gLocalTime'), 2))[0]
        if mode == 'done_today':
            set_flag(e, 0x1DA)
            e.w16(sb1 + VARS + (0x4091 - 0x4000) * 2, day & 0xFFFF)
        walk(e, 'UP', 1); walk(e, 'RIGHT', 5); e.press('UP', hold=2, after=20)
        e.press('A', after=90)
        e.press('A', after=90)
        print(mode, 'rtc day', day, pos(e))
        e.shot('shots/k_%s.png' % mode)
    finally:
        e.close()
