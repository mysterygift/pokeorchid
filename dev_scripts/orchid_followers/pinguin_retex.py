"""Pinguin follower: Piplup's follower body + walk cycle recoloured into Pinguin's
battle palette, with a smaller hand-drawn head (crest, eyes, beak) on top."""
import sys
from PIL import Image
src, pal, out = sys.argv[1:4]
im = Image.open(src); px = im.load()
cols = [tuple(int(v) for v in l.split()) for l in open(pal).read().split('\n')[3:19]]
W,L,M,D,O,B,p,r,R,K,Y = 1,2,4,7,8,11,9,10,12,14,5
BASE = {1:K, 2:W, 3:K, 4:M, 5:M, 6:W, 7:W, 8:L, 10:K, 11:O, 9:B, 12:L}
COLLAR = {2:p, 4:R, 5:r, 6:p, 9:r, 12:r}   # first row under the head = red neckerchief
CH = {'o':K,'W':W,'L':L,'M':M,'O':O,'B':B,'r':r,'R':R,'p':p,'Y':Y}
HEAD_DOWN = """
....o.o....
...oroRo...
..oorrRoo..
.oWWWWWWLo.
oWWWWWWWWLo
oWoMWWWMoLo
oWoWOOBWoLo
oLWWWBWWLLo
.oLWWWWWLo.
..oLLLLLo..
"""
HEAD_UP = """
....o.o....
...oRoRo...
..oorrRoo..
.oWWWWWWLo.
oWWWWWWWLMo
oWWWWWWWLMo
oLWWWWWLLMo
oLLWWWLLMMo
.oLLLLLMMo.
..oMMMMMo..
"""
HEAD_LEFT = """
......o.o...
.....oroRo..
....oorrRoo.
...oWWWWWLo.
..oWWWWWWLMo
..oWoMWWWLMo
oOOBoMWWWLMo
.ooBWWWWLLMo
...oLWWWLMo.
....oLLLMo..
"""
heads = [(HEAD_DOWN,10)]*2 + [(HEAD_UP,10)]*2 + [(HEAD_LEFT,9)]*2
o = Image.new('P', im.size, 0); o.putpalette([c for t in cols for c in t]); op = o.load()
for y in range(24, im.height):
    for x in range(im.width):
        v = px[x, y]
        if v: op[x, y] = (COLLAR if y == 24 else BASE).get(v, BASE[v])
for f, (art, x0) in enumerate(heads):
    rows = art.strip('\n').split('\n')
    top = 24 - len(rows)
    for dy, row in enumerate(rows):
        for dx, c in enumerate(row):
            if c != '.': op[f*32 + x0 + dx, top + dy] = CH[c]
o.save(out)
