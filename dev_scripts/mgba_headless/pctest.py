import sys
from boot import *
from PIL import Image
rom=sys.argv[1] if len(sys.argv)>1 else 'cm'
e=boot(rom)
warp(e,2,2,0); print('warp',pos(e))
walk(e,'UP',5); walk(e,'RIGHT',3); walk(e,'UP',1); print('at pc',pos(e))
shots=[]
def s(n): e.shot(n,scale=1); shots.append(n)
s('p0.png')
e.press('A',after=90); s('p1.png')
e.press('A',after=60); s('p2.png')
e.press('B',after=60); s('p3.png')
e.press('B',after=60); s('p4.png')
walk(e,'DOWN',2); print('after',pos(e)); s('p5.png')
ims=[Image.open(f) for f in shots]
o=Image.new('RGB',(720,320));[o.paste(im,((i%3)*240,(i//3)*160)) for i,im in enumerate(ims)];o.resize((1440,640),0).save('pseq.png')
e.close()
