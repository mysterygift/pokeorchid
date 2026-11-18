from gba import Emu
def boot(rom='cm'):
    e=Emu(rom+'.gba',rom+'.elf')
    e.frames(400); e.press('START',after=120); e.press('A',after=240); e.press('A',after=300)
    return e

def warp(e, group, num, warp=0):
    e.press('R','START',after=60); e.press('A',after=30); e.press('DOWN'); e.press('A',after=30)
    for _ in range(group): e.press('UP',after=6)
    e.press('A',after=20)
    for _ in range(num): e.press('UP',after=6)
    e.press('A',after=20)
    for _ in range(warp): e.press('UP',after=6)
    e.press('A',after=200)

def pos(e):
    import struct
    sb1=e.r32('gSaveBlock1Ptr'); x,y=struct.unpack('<hh',e.read(sb1,4)); g,n=e.read(sb1+4,2)
    return (x,y,g,n)

def walk(e, d, n):
    for _ in range(n):
        e.press(d, hold=16, after=4)
