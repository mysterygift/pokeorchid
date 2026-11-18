import sys, json
from boot import *
rom=sys.argv[1]
bl=json.load(open('bldgs.json'))
e=boot(rom)
bad=[]
for g,n,name in bl:
    warp(e,g,n,0)
    e.press('DOWN',hold=16,after=100); p1=pos(e)
    e.frames(20)
    e.press('UP',hold=16,after=120); p2=pos(e)
    e.shot(f'ex/{name}_in.png',scale=1)
    ok=(p2[2],p2[3])==(g,n)
    print(name, p1, p2, 'ENTER OK' if ok else 'ENTER FAIL', flush=True)
    if not ok: bad.append(name)
print('BAD',bad)
e.close()
