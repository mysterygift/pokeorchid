from common import *
e=start()
try:
    p=pos(e); print('pos',p)
    # reload map: debug warp to the current map (warp 0)
    warp(e, p[2], p[3], 0); e.frames(120); print('pos',pos(e))
    walk(e,'DOWN',2); e.frames(60); shot(e,'i0_follow.png')
    walk(e,'LEFT',2); e.frames(60); shot(e,'i1_follow.png')
finally:
    e.close()
strip('i_strip.png',cols=2)
