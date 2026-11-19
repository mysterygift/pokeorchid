"""
Minimal Standard MIDI File reader/writer for the radio importer (no third-party deps).

Event = dict(t=abs_tick, kind=..., ...):
  kind 'note'  : ch, key, vel, dur        (note on/off pairs folded into one event)
  kind 'cc'    : ch, cc, val
  kind 'prog'  : ch, prog
  kind 'bend'  : ch, val (0..16383)
  kind 'chpress' / 'keypress': ch, val (, key)
  kind 'meta'  : type, data (bytes)
  kind 'sysex' : data
"""
import struct


def _vlq(data, i):
    v = 0
    while True:
        b = data[i]
        i += 1
        v = (v << 7) | (b & 0x7F)
        if not b & 0x80:
            return v, i


def _enc_vlq(v):
    out = [v & 0x7F]
    v >>= 7
    while v:
        out.append(0x80 | (v & 0x7F))
        v >>= 7
    return bytes(reversed(out))


class Midi:
    def __init__(self):
        self.fmt = 1
        self.ppqn = 96
        self.tracks = []   # list of list of events (abs ticks)

    @classmethod
    def load(cls, path):
        m = cls()
        data = open(path, "rb").read()
        if data[:4] == b"RIFF":     # RMID wrapper
            j = data.find(b"MThd")
            data = data[j:]
        assert data[:4] == b"MThd", path
        hl = struct.unpack(">I", data[4:8])[0]
        m.fmt, ntrk, div = struct.unpack(">HHH", data[8:14])
        if div & 0x8000:
            raise ValueError("SMPTE timing unsupported")
        m.ppqn = div
        i = 8 + hl
        for _ in range(ntrk):
            while i < len(data) and data[i:i + 4] != b"MTrk":
                i += 1
            if i >= len(data):
                break
            ln = struct.unpack(">I", data[i + 4:i + 8])[0]
            m.tracks.append(cls._parse_track(data[i + 8:i + 8 + ln]))
            i += 8 + ln
        return m

    @staticmethod
    def _parse_track(d):
        evs = []
        on = {}
        t = 0
        i = 0
        status = 0
        while i < len(d):
            dt, i = _vlq(d, i)
            t += dt
            if i >= len(d):
                break
            b = d[i]
            if b & 0x80:
                status = b
                i += 1
            if status == 0xFF:
                typ = d[i]
                ln, i = _vlq(d, i + 1)
                data = d[i:i + ln]
                i += ln
                if typ == 0x2F:
                    evs.append(dict(t=t, kind="end"))
                    break
                evs.append(dict(t=t, kind="meta", type=typ, data=bytes(data)))
                status = 0
                continue
            if status in (0xF0, 0xF7):
                ln, i = _vlq(d, i)
                evs.append(dict(t=t, kind="sysex", data=bytes(d[i:i + ln]), st=status))
                i += ln
                status = 0
                continue
            hi = status & 0xF0
            ch = status & 0x0F
            if hi in (0xC0, 0xD0):
                a = d[i]
                i += 1
                if hi == 0xC0:
                    evs.append(dict(t=t, kind="prog", ch=ch, prog=a))
                else:
                    evs.append(dict(t=t, kind="chpress", ch=ch, val=a))
                continue
            a, b2 = d[i], d[i + 1]
            i += 2
            if hi == 0x90 and b2 > 0:
                key = (ch, a)
                if key in on:       # retrigger: close the previous one
                    e = on.pop(key)
                    e["dur"] = t - e["t"]
                e = dict(t=t, kind="note", ch=ch, key=a, vel=b2, dur=0)
                on[key] = e
                evs.append(e)
            elif hi == 0x80 or hi == 0x90:
                e = on.pop((ch, a), None)
                if e is not None:
                    e["dur"] = t - e["t"]
            elif hi == 0xB0:
                evs.append(dict(t=t, kind="cc", ch=ch, cc=a, val=b2))
            elif hi == 0xE0:
                evs.append(dict(t=t, kind="bend", ch=ch, val=a | (b2 << 7)))
            elif hi == 0xA0:
                evs.append(dict(t=t, kind="keypress", ch=ch, key=a, val=b2))
        for e in on.values():
            e["dur"] = max(1, t - e["t"])
        return [e for e in evs if e["kind"] != "end"]

    def all_events(self):
        for ti, tr in enumerate(self.tracks):
            for e in tr:
                yield ti, e

    def end_tick(self):
        end = 0
        for _, e in self.all_events():
            end = max(end, e["t"] + e.get("dur", 0))
        return end

    def save(self, path):
        out = bytearray(b"MThd" + struct.pack(">IHHH", 6, 1, len(self.tracks), self.ppqn))
        for tr in self.tracks:
            raw = []    # (t, order, bytes)
            for e in tr:
                k = e["kind"]
                if k == "note":
                    raw.append((e["t"], 2, bytes([0x90 | e["ch"], e["key"], max(1, e["vel"])])))
                    raw.append((e["t"] + max(1, e["dur"]), 0, bytes([0x80 | e["ch"], e["key"], 0])))
                elif k == "cc":
                    raw.append((e["t"], 1, bytes([0xB0 | e["ch"], e["cc"], e["val"]])))
                elif k == "prog":
                    raw.append((e["t"], 1, bytes([0xC0 | e["ch"], e["prog"]])))
                elif k == "bend":
                    raw.append((e["t"], 1, bytes([0xE0 | e["ch"], e["val"] & 0x7F, e["val"] >> 7])))
                elif k == "meta":
                    raw.append((e["t"], 1, bytes([0xFF, e["type"]]) + _enc_vlq(len(e["data"])) + e["data"]))
            raw.sort(key=lambda r: (r[0], r[1]))
            body = bytearray()
            t = 0
            for rt, _, b in raw:
                body += _enc_vlq(rt - t) + b
                t = rt
            body += b"\x00\xFF\x2F\x00"
            out += b"MTrk" + struct.pack(">I", len(body)) + body
        open(path, "wb").write(out)
