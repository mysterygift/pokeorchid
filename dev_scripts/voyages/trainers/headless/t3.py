from common import *
e = start()
try:
    print('flag lake', get_flag(e, 0x1AA), 'hide', get_flag(e, 0x1AB))
    warp(e, 21, 121, 0)
    e.frames(60)
    print('pos', pos(e), 'hide', get_flag(e, 0x1AB), 'song', song(e))
    e.shot('shots/c_cafe_before_flag.png')
    set_flag(e, 0x1AA)
    warp(e, 21, 121, 0)
    e.frames(60)
    print('pos', pos(e), 'hide', get_flag(e, 0x1AB))
    e.shot('shots/c_cafe_after_flag.png')
finally:
    e.close()
