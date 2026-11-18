import json,struct,glob,os
from collections import deque
lays={l['id']:l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if 'id' in l}
def attrs(ts):
    import re
    n=re.sub(r'(?<!^)(?=[A-Z])','_',ts.replace('gTileset_','')).lower()
    for b in ('primary','secondary'):
        p=f'data/tilesets/{b}/{n}/metatile_attributes.bin'
        if os.path.exists(p): return open(p,'rb').read()
for f in sorted(glob.glob('data/maps/*/map.json')):
    j=json.load(open(f))
    if j['layout'] not in ('LAYOUT_POKEMON_CENTER_1F','LAYOUT_LAVARIDGE_TOWN_POKEMON_CENTER_1F','LAYOUT_MART'): continue
    L=lays[j['layout']]; w,h=L['width'],L['height']; d=open(L['blockdata_filepath'],'rb').read()
    pa,sa=attrs(L['primary_tileset']),attrs(L['secondary_tileset'])
    cell=lambda x,y: struct.unpack_from('<H',d,2*(y*w+x))[0]
    def beh(m):
        a,i=(pa,m) if m<512 else (sa,m-512); return struct.unpack_from('<H',a,2*i)[0]&0xff
    npcs={(o['x'],o['y']):o for o in j.get('object_events',[]) if 'x' in o}
    warps=[(wp['x'],wp['y']) for wp in j['warp_events'] if (wp['x'],wp['y'])!=(0,0)]
    start=warps[0]
    seen={start}; q=deque([start])
    while q:
        x,y=q.popleft()
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx,ny=x+dx,y+dy
            if 0<=nx<w and 0<=ny<h and (nx,ny) not in seen and not (cell(nx,ny)>>10)&3 and (nx,ny) not in npcs:
                seen.add((nx,ny)); q.append((nx,ny))
    probs=[]
    for (x,y),o in npcs.items():
        if o.get('script','0x0') in ('0x0','NULL') : continue
        ok=False
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            if (x+dx,y+dy) in seen: ok=True
            ax,ay=x+dx,y+dy
            if 0<=ax<w and 0<=ay<h and beh(cell(ax,ay)&0x3ff)==0x80 and (x+2*dx,y+2*dy) in seen: ok=True
        if not ok: probs.append(f"{o['graphics_id'][14:]}@{x},{y}")
        if (cell(x,y)>>10)&3: probs.append(f"{o['graphics_id'][14:]} on blocked tile {x},{y}")
    # PC reachable
    for yy in range(h):
        for xx in range(w):
            if beh(cell(xx,yy)&0x3ff)==0x83 and (xx,yy+1) not in seen: probs.append(f'PC {xx},{yy} not usable')
    for wx,wy in warps:
        if (wx,wy) not in seen: probs.append(f'warp {wx},{wy} unreachable')
    print(f"{os.path.basename(os.path.dirname(f)):40s} reach={len(seen):3d} {'OK' if not probs else probs}")
