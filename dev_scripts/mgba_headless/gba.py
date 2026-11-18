"""Headless GBA harness: mgba-rom-test -g (GDB stub) + RSP client + key injection + screen renderer.

Usage (python with Pillow):
    from gba import Emu
    e = Emu(rom, elf_map)       # starts emulator
    e.frames(60); e.press('A'); e.shot('x.png')
Keys are injected through the ROM global gHarnessKeys (ORed into REG_KEYINPUT in ReadKeys).
"""
import socket, subprocess, time, struct, os, re

KEYS = dict(A=1, B=2, SELECT=4, START=8, RIGHT=16, LEFT=32, UP=64, DOWN=128, R=256, L=512)
RUNNER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools', 'mgba', 'mgba-rom-test-mac')


def load_syms(elf):
    syms = {}
    out = subprocess.run(['arm-none-eabi-nm', elf], capture_output=True, text=True).stdout
    for line in out.splitlines():
        parts = line.split()
        if len(parts) == 3:
            syms.setdefault(parts[2], int(parts[0], 16))
    return syms


def _unrle(d):
    out = []
    i = 0
    while i < len(d):
        if d[i] == '*':
            out.append(out[-1] * (ord(d[i + 1]) - 29))
            i += 2
        else:
            out.append(d[i])
            i += 1
    return ''.join(out)


class Emu:
    def __init__(self, rom, mapfile, port=2345, savestate=None):
        self.syms = load_syms(mapfile)
        args = [RUNNER, '-g']
        if savestate:
            args += ['-t', savestate]
        args.append(rom)
        self.proc = subprocess.Popen(args, cwd=os.path.dirname(os.path.abspath(rom)),
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(100):
            try:
                self.s = socket.create_connection(('127.0.0.1', port))
                break
            except OSError:
                time.sleep(0.1)
        self.s.settimeout(10)
        self.buf = b''
        self.cmd('?')
        self.running = False

    # --- RSP ---
    def _send(self, data):
        pkt = b'$' + data.encode() + b'#' + ('%02x' % (sum(data.encode()) & 0xff)).encode()
        self.s.sendall(pkt)

    def _recv(self):
        while True:
            m = re.search(rb'\$([^#]*)#..', self.buf)
            if m:
                self.buf = self.buf[m.end():]
                self.s.sendall(b'+')
                return _unrle(m.group(1).decode())
            self.buf += self.s.recv(65536)

    def cmd(self, data):
        self._send(data)
        return self._recv()

    def stop(self):
        if self.running:
            self.s.sendall(b'\x03')
            self._recv()
            self.running = False

    def go(self):
        if not self.running:
            self._send('c')
            self.running = True

    def read(self, addr, n):
        self.stop()
        out = b''
        while n:
            k = min(n, 0x100)
            r = self.cmd('m%x,%x' % (addr, k))
            out += bytes.fromhex(r)
            addr += k
            n -= k
        return out

    def write(self, addr, data):
        self.stop()
        assert self.cmd('M%x,%x:%s' % (addr, len(data), data.hex())) == 'OK'

    def sym(self, name):
        return self.syms[name]

    def r8(self, a): return self.read(self._a(a), 1)[0]
    def r16(self, a): return struct.unpack('<H', self.read(self._a(a), 2))[0]
    def r32(self, a): return struct.unpack('<I', self.read(self._a(a), 4))[0]
    def w16(self, a, v): self.write(self._a(a), struct.pack('<H', v))
    def w8(self, a, v): self.write(self._a(a), bytes([v]))

    def _a(self, a):
        if isinstance(a, str):
            name, _, off = a.partition('+')
            return self.syms[name] + (int(off, 0) if off else 0)
        return a

    # --- time ---
    def vcount(self):
        return self.r32('gMain+0x20')  # vblankCounter1? fallback below

    def frames(self, n):
        """Run exactly n frames: breakpoint on ReadKeys (once per frame)."""
        self.stop()
        if not getattr(self, '_bp', False):
            a = self.syms['VBlankIntr'] & ~1
            r = self.cmd('Z0,%x,2' % a)
            assert r == 'OK', r
            self._bp = True
        for _ in range(n):
            self._send('c')
            self._recv()

    def frame_counter(self):
        return self.r32(self.syms['gMain'] + 0x24)

    def keys(self, mask):
        self.w16('gHarnessKeys', mask)

    def press(self, *names, hold=4, after=12):
        mask = 0
        for nm in names:
            mask |= KEYS[nm]
        self.keys(mask)
        self.frames(hold)
        self.keys(0)
        self.frames(after)

    def close(self):
        try:
            self.proc.kill()
        except Exception:
            pass

    # --- render ---
    def shot(self, path, scale=2):
        from render import render
        io = self.read(0x04000000, 0x60)
        regbuf = self.read(self.syms['sGpuRegBuffer'], 0x60) if 'sGpuRegBuffer' in self.syms else io
        vram = self.read(0x06000000, 0x18000)
        pal = self.read(0x05000000, 0x400)
        oam = self.read(0x07000000, 0x400)
        img = render(io, regbuf, vram, pal, oam)
        if scale != 1:
            img = img.resize((240 * scale, 160 * scale), 0)
        img.save(path)
        return path
