import sys
from common import *
MB=behaviours(); inv={v:k for k,v in MB.items()}
L,M=layouts(),maps()
lid=sys.argv[1]; e=L[lid]; g=read_grid(e)
x0,y0,x1,y1=map(int,sys.argv[2:6])
evs={}
for mid,(p,js) in M.items():
    if js['layout']==lid:
        for c,k in event_cells(js).items(): evs.setdefault(c,[]).extend(k)
print('     '+' '.join(f'{x:>5}' for x in range(x0,x1)))
for y in range(y0,y1):
    row=[]
    for x in range(x0,x1):
        v=g[y][x]; m=v&0x3FF; c=(v>>10)&3; b=attr_of(e,m)&0xFF
        tag=f"{m:03X}{'#' if c else ' '}{'E' if (x,y) in evs else ('t' if b==MB['MB_TALL_GRASS'] else ('.' if b==0 else '?'))}"
        row.append(tag)
    print(f'{y:>4} '+' '.join(row))
