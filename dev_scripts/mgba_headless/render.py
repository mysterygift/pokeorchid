"""Minimal GBA mode-0 renderer (text BGs + regular/affine-as-regular OBJs, priorities, no blending/windows)."""
import struct
from PIL import Image

SIZES = {(0, 0): (8, 8), (0, 1): (16, 16), (0, 2): (32, 32), (0, 3): (64, 64),
         (1, 0): (16, 8), (1, 1): (32, 8), (1, 2): (32, 16), (1, 3): (64, 32),
         (2, 0): (8, 16), (2, 1): (8, 32), (2, 2): (16, 32), (2, 3): (32, 64)}


def col(pal, i):
    c = pal[2 * i] | (pal[2 * i + 1] << 8)
    return ((c & 31) << 3, ((c >> 5) & 31) << 3, ((c >> 10) & 31) << 3)


def render(io, reg, vram, pal, oam):
    h16 = lambda b, o: struct.unpack_from('<H', b, o)[0]
    dispcnt = h16(reg, 0)
    mode = dispcnt & 7
    layers = []  # (prio, order, pixels dict)
    W, H = 240, 160
    back = col(pal, 0)
    # BG
    for bg in range(4):
        if not (dispcnt >> (8 + bg)) & 1:
            continue
        if mode == 1 and bg == 3 or mode == 2 and bg < 2 or mode > 2:
            continue
        cnt = h16(reg, 8 + 2 * bg)
        prio = cnt & 3
        cbase = ((cnt >> 2) & 3) * 0x4000
        bpp8 = (cnt >> 7) & 1
        sbase = ((cnt >> 8) & 31) * 0x800
        size = cnt >> 14
        hofs = h16(reg, 0x10 + 4 * bg) & 511
        vofs = h16(reg, 0x12 + 4 * bg) & 511
        affine = (mode == 1 and bg == 2) or (mode == 2)
        px = [None] * (W * H)
        if affine:
            continue  # not rendered
        tw = 512 if size & 1 else 256
        th = 512 if size & 2 else 256
        for y in range(H):
            yy = (y + vofs) % th
            for x in range(W):
                xx = (x + hofs) % tw
                blk = (xx // 256) + ((yy // 256) * (2 if tw == 512 else 1))
                se = h16(vram, sbase + blk * 0x800 + (((yy % 256) // 8) * 32 + (xx % 256) // 8) * 2)
                t = se & 0x3FF
                fx = (xx & 7) ^ (7 if se & 0x400 else 0)
                fy = (yy & 7) ^ (7 if se & 0x800 else 0)
                if bpp8:
                    a = cbase + t * 64 + fy * 8 + fx
                    if a >= 0x10000:
                        continue
                    c = vram[a]
                    if c:
                        px[y * W + x] = col(pal, c)
                else:
                    a = cbase + t * 32 + fy * 4 + fx // 2
                    if a >= 0x10000:
                        continue
                    c = (vram[a] >> ((fx & 1) * 4)) & 15
                    if c:
                        px[y * W + x] = col(pal, (se >> 12) * 16 + c)
        layers.append((prio, 1, bg, px))
    # OBJ
    if dispcnt & 0x1000:
        map1d = dispcnt & 0x40
        objs = [[None] * (W * H) for _ in range(4)]
        for i in range(127, -1, -1):
            a0, a1, a2 = struct.unpack_from('<HHH', oam, i * 8)
            aff = a0 & 0x100
            if not aff and a0 & 0x200:
                continue
            shape = a0 >> 14
            if shape == 3:
                continue
            sz = a1 >> 14
            w, h = SIZES[(shape, sz)]
            dbl = aff and (a0 & 0x200)
            y0 = a0 & 255
            x0 = a1 & 511
            if y0 >= 160:
                y0 -= 256
            if x0 >= 240:
                x0 -= 512
            if dbl:
                x0 += w // 2
                y0 += h // 2
            bpp8 = a0 & 0x2000
            hf = (not aff) and (a1 & 0x1000)
            vf = (not aff) and (a1 & 0x2000)
            tile = a2 & 0x3FF
            prio = (a2 >> 10) & 3
            palb = (a2 >> 12) * 16
            mode_ = (a0 >> 10) & 3
            if mode_ == 2:
                continue  # obj window
            for yy in range(h):
                sy = y0 + yy
                if not 0 <= sy < H:
                    continue
                ty = (h - 1 - yy) if vf else yy
                for xx in range(w):
                    sx = x0 + xx
                    if not 0 <= sx < W:
                        continue
                    tx = (w - 1 - xx) if hf else xx
                    if bpp8:
                        tn = tile + ((ty // 8) * (w // 8) * 2 if map1d else (ty // 8) * 32) + (tx // 8) * 2
                        addr = 0x10000 + (tn & 0x3FF) * 32 + (ty & 7) * 8 + (tx & 7)
                        c = vram[addr] if addr < 0x18000 else 0
                        if c:
                            objs[prio][sy * W + sx] = col(pal, 256 + c)
                    else:
                        tn = tile + ((ty // 8) * (w // 8) if map1d else (ty // 8) * 32) + (tx // 8)
                        addr = 0x10000 + (tn & 0x3FF) * 32 + (ty & 7) * 4 + (tx & 7) // 2
                        c = (vram[addr] >> ((tx & 1) * 4)) & 15 if addr < 0x18000 else 0
                        if c:
                            objs[prio][sy * W + sx] = col(pal, 256 + palb + c)
        for p in range(4):
            layers.append((p, 0, -1, objs[p]))
    layers.sort(key=lambda l: (-l[0], -l[1], -l[2]))  # draw back to front
    img = Image.new('RGB', (W, H), back)
    data = list(img.getdata())
    for _, _, _, px in layers:
        for i, c in enumerate(px):
            if c is not None:
                data[i] = c
    img.putdata(data)
    return img
