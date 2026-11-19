"""Minimal Standard MIDI File reader/writer (no mido): keeps every event, running status expanded on write."""
import struct


def _vlq(d, i):
    v = 0
    while True:
        b = d[i]; i += 1
        v = (v << 7) | (b & 0x7F)
        if not b & 0x80:
            return v, i


def _wvlq(v):
    out = [v & 0x7F]
    v >>= 7
    while v:
        out.append((v & 0x7F) | 0x80)
        v >>= 7
    return bytes(reversed(out))


class Event:
    """kind: 'midi' (status, data bytes), 'meta' (type, data), 'sysex' (raw status, data). tick = absolute."""
    __slots__ = ('tick', 'kind', 'status', 'data', 'mtype')

    def __init__(self, tick, kind, status, data, mtype=None):
        self.tick, self.kind, self.status, self.data, self.mtype = tick, kind, status, bytearray(data), mtype

    @property
    def ch(self):
        return self.status & 0x0F

    @property
    def cmd(self):
        return self.status & 0xF0


def read(path):
    d = open(path, 'rb').read()
    assert d[:4] == b'MThd'
    hl = struct.unpack('>I', d[4:8])[0]
    fmt, ntrk, div = struct.unpack('>HHH', d[8:14])
    i = 8 + hl
    tracks = []
    for _ in range(ntrk):
        assert d[i:i + 4] == b'MTrk', d[i:i + 4]
        ln = struct.unpack('>I', d[i + 4:i + 8])[0]
        j, end = i + 8, i + 8 + ln
        tick, rs, evs = 0, None, []
        while j < end:
            dt, j = _vlq(d, j)
            tick += dt
            b = d[j]
            if b == 0xFF:
                mt = d[j + 1]
                l, k = _vlq(d, j + 2)
                evs.append(Event(tick, 'meta', 0xFF, d[k:k + l], mt))
                j = k + l
            elif b in (0xF0, 0xF7):
                l, k = _vlq(d, j + 1)
                evs.append(Event(tick, 'sysex', b, d[k:k + l]))
                j = k + l
            else:
                if b & 0x80:
                    rs = b; j += 1
                n = 1 if (rs & 0xF0) in (0xC0, 0xD0) else 2
                evs.append(Event(tick, 'midi', rs, d[j:j + n]))
                j += n
        tracks.append(evs)
        i = end
    return fmt, div, tracks


def write(path, fmt, div, tracks):
    out = bytearray(b'MThd' + struct.pack('>IHHH', 6, fmt, len(tracks), div))
    for evs in tracks:
        body, last = bytearray(), 0
        for e in evs:
            body += _wvlq(e.tick - last)
            last = e.tick
            if e.kind == 'meta':
                body += bytes([0xFF, e.mtype]) + _wvlq(len(e.data)) + e.data
            elif e.kind == 'sysex':
                body += bytes([e.status]) + _wvlq(len(e.data)) + e.data
            else:
                body += bytes([e.status]) + e.data
        out += b'MTrk' + struct.pack('>I', len(body)) + body
    open(path, 'wb').write(out)
