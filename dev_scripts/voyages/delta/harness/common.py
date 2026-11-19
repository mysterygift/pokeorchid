import sys, os
sys.path.insert(0,'/Users/arandavies/Development/pokemon-orchid/pokeorchid-voy-delta/dev_scripts/mgba_headless')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from boot import *
from PIL import Image
SHOTS=[]
def start():
    e=boot('dh')
    e.press('B',after=60); e.press('START',after=60); e.press('A',after=60)
    for _ in range(4): e.press('B',after=40)
    e.frames(60)
    e.press('R','START',after=60); e.press('DOWN'); e.press('DOWN'); e.press('A',after=30)
    e.press('DOWN'); e.press('DOWN'); e.press('A',after=60); e.frames(60)
    return e
def shot(e,name):
    e.shot(name); SHOTS.append(name)
def strip(out, cols=3):
    ims=[Image.open(f) for f in SHOTS]
    w,h=ims[0].size; rows=(len(ims)+cols-1)//cols
    o=Image.new('RGB',(w*cols,h*rows))
    for i,im in enumerate(ims): o.paste(im,((i%cols)*w,(i//cols)*h))
    o.save(out)
def cb2(e):
    a=e.r32(e.syms['gMain']+4)
    for k,v in e.syms.items():
        if v==a or v==a-1: return k
    return hex(a)
