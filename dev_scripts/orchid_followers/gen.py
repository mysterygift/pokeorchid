"""Build 192x32 follower sheets from ASCII frames. Frames: downA downB upA upB leftA leftB."""
import sys, importlib.util
from PIL import Image
def readpal(p):
    l=open(p).read().split('\n')[3:19]; return [tuple(int(v) for v in x.split()) for x in l]
def build(art, pal, out, xoff, bottom=29):
    cmap=art.CMAP
    im=Image.new('P',(192,32),0)
    flat=[]; [flat.extend(c) for c in pal]; im.putpalette(flat)
    px=im.load()
    for f,fr in enumerate(art.frames()):
        rows=[r for r in fr.strip('\n').split('\n')]
        rows=[r.split()[-1] if ' ' in r.strip() else r.strip() for r in rows]
        top=bottom-len(rows)+1
        for y,r in enumerate(rows):
            for x,ch in enumerate(r):
                if ch=='.': continue
                px[f*32+xoff+x, top+y]=cmap[ch]
    if getattr(art,'AUTO_OUTLINE',False):
        o=cmap['o']; src=im.copy(); sp=src.load()
        for y in range(32):
            for x in range(192):
                if sp[x,y]: continue
                fx=x//32
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny=x+dx,y+dy
                    if 0<=ny<32 and fx*32<=nx<fx*32+32 and sp[nx,ny] and sp[nx,ny]!=o:
                        px[x,y]=o; break
    im.save(out)
if __name__=='__main__':
    name, artfile, pal, out, xoff = sys.argv[1:6]
    spec=importlib.util.spec_from_file_location(name, artfile); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    build(m, readpal(pal), out, int(xoff))
