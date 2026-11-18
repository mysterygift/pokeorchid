import sys, json
from boot import *
from PIL import Image
rom=sys.argv[1]
bl=json.load(open('bldgs.json'))
e=boot(rom)
res=[]
for g,n,name in bl:
    warp(e,g,n,0); p0=pos(e)
    ok_in = (p0[2],p0[3])==(g,n)
    e.press('DOWN',hold=16,after=100); p1=pos(e)
    e.frames(30)
    out = (p1[2],p1[3])!=(g,n)
    e.shot(f'ex/{name}_a.png',scale=1)
    walk(e,'DOWN',2); p2=pos(e)
    e.shot(f'ex/{name}_b.png',scale=1)
    moved = p2[:2]!=p1[:2]
    r=(name,ok_in,p0,out,p1,p2,moved); res.append(r); print(r, flush=True)
json.dump(res,open('exitall.json','w'))
e.close()
