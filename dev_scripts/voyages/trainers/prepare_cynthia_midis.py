"""Prepare the user's two Cynthia MIDIs (ref/) for mid2agb and write them into sound/songs/midi/.

    python3 dev_scripts/voyages/trainers/prepare_cynthia_midis.py

Decisions (out/batch5_trainers/NOTES.md "Music", DECISIONS.md 19):
- vs_cynthia.mid -> mus_orchid_vs_cynthia.mid (11 tracks; NUM_TRACKS_BGM is raised 10 -> 12):
  * ch16 dropped (an exact copy of ch5), ch7 orchestra hits dropped.
  * ch5 synth bass stays program 38, which the song's own voicegroup maps to the programmable-wave channel.
  * ch6 steel drums stay program 114, mapped to the sc88pro xylophone (directsound) for the bell line.
  * ch9 strings, ch12 flute and ch14 distortion guitar never overlap and share one track; ch15 piano joins
    ch11's track after ch11 ends. Each merged segment re-sends its program, volume, pan, bend range and a
    centred pitch bend.
  * ch11 (a second square lead under ch2) is moved from program 80 to 82 so it plays on square channel 2
    instead of fighting ch2 for square channel 1.
  * RPN 0 (pitch-bend sensitivity: CC101 0, CC100 0, CC6 n) becomes CC20 n (mid2agb's BENDR); mid2agb
    ignores RPNs, so without this every bend would play at +/-2 semitones.
  * Drum key 49 (empty in rs_drumset) -> 57 (orchestra crash).
- encounter_cynthia.mid -> mus_orchid_encounter_cynthia.mid: one piano track; program 0 stays, because the
  song's own GM-numbered voicegroup puts the piano keysplit in slot 0 (vanilla voicegroups have a drumset there).
- Both: only notes, program changes, pitch bends and CC 1/7/10/20 are written. Every other controller is
  dropped (mid2agb gives CC 12-31 special meanings, and ignores 11/64/91/... anyway). Tempo and time
  signature events are kept. NO loop markers are added: the user places "[" / "]" after import.
"""
import os
import struct
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
REF = os.path.join(HERE, 'ref')
OUT = os.path.join(ROOT, 'sound', 'songs', 'midi')

KEEP_CC = {1, 7, 10, 20}


def vlq_read(d, i):
    v = 0
    while True:
        b = d[i]
        i += 1
        v = (v << 7) | (b & 0x7F)
        if not b & 0x80:
            return v, i


def vlq(v):
    out = [v & 0x7F]
    v >>= 7
    while v:
        out.append(0x80 | (v & 0x7F))
        v >>= 7
    return bytes(reversed(out))


def parse(path):
    """-> division, [ (tick, kind, a, data) ] where kind = 'meta' (a = type) or a status high nibble (a = channel)."""
    d = open(path, 'rb').read()
    hl = struct.unpack('>I', d[4:8])[0]
    _fmt, ntr, div = struct.unpack('>HHH', d[8:14])
    i, evs = 8 + hl, []
    for _ in range(ntr):
        ln = struct.unpack('>I', d[i + 4:i + 8])[0]
        t, j, tick, run = d[i + 8:i + 8 + ln], 0, 0, None
        i += 8 + ln
        while j < len(t):
            dt, j = vlq_read(t, j)
            tick += dt
            st = t[j]
            if st == 0xFF:
                typ = t[j + 1]
                n, j = vlq_read(t, j + 2)
                evs.append((tick, 'meta', typ, bytes(t[j:j + n])))
                j += n
            elif st in (0xF0, 0xF7):
                n, j = vlq_read(t, j + 1)
                j += n
            else:
                if st & 0x80:
                    run = st
                    j += 1
                else:
                    st = run
                hi = st & 0xF0
                n = 1 if hi in (0xC0, 0xD0) else 2
                evs.append((tick, hi, st & 0x0F, bytes(t[j:j + n])))
                j += n
    return div, evs


def track_chunk(events):
    """events: [(tick, order, raw bytes)] -> MTrk chunk (adds End of Track)."""
    out, last = bytearray(), 0
    for tick, _o, raw in sorted(events, key=lambda e: (e[0], e[1])):
        out += vlq(tick - last) + raw
        last = tick
    out += vlq(0) + b'\xFF\x2F\x00'
    return b'MTrk' + struct.pack('>I', len(out)) + bytes(out)


def write_midi(path, div, conductor, tracks):
    data = b'MThd' + struct.pack('>IHHH', 6, 1, 1 + len(tracks), div) + track_chunk(conductor)
    for t in tracks:
        data += track_chunk(t)
    open(path, 'wb').write(data)


def conductor_events(evs, name):
    out = [(0, 0, b'\xFF\x03' + vlq(len(name)) + name.encode())]
    for tick, kind, a, data in evs:
        if kind == 'meta' and a in (0x51, 0x58):      # tempo, time signature
            out.append((tick, 1, b'\xFF' + bytes([a]) + vlq(len(data)) + data))
    return out


def channel_stream(evs, ch):
    """Source channel -> list of (tick, order, kind, data) with RPN 0 turned into CC20 and other CCs dropped.
    order: 0 = note off, 1 = controller/program/bend, 2 = note on (so offs and setup precede ons at a tick)."""
    out, rpn = [], [127, 127]
    for tick, kind, a, data in evs:
        if kind == 'meta' or a != ch:
            continue
        if kind == 0xB0:
            cc, val = data[0], data[1]
            if cc == 101:
                rpn[0] = val
            elif cc == 100:
                rpn[1] = val
            elif cc == 6 and rpn == [0, 0]:
                out.append((tick, 1, 0xB0, bytes([20, val])))
            elif cc in KEEP_CC:
                out.append((tick, 1, 0xB0, data))
        elif kind == 0x90:
            out.append((tick, 2 if data[1] else 0, 0x90, data))
        elif kind == 0x80:
            out.append((tick, 0, 0x90, bytes([data[0], 0])))
        elif kind in (0xC0, 0xE0):
            out.append((tick, 1, kind, data))
    return out


def state_at(stream, tick):
    """Program / CC7 / CC10 / CC20 in force on a source channel just before `tick`."""
    st = {'prog': 0, 7: 100, 10: 64, 20: 2}
    for t, _o, kind, data in stream:
        if t >= tick:
            break
        if kind == 0xC0:
            st['prog'] = data[0]
        elif kind == 0xB0 and data[0] in (7, 10, 20):
            st[data[0]] = data[1]
    return st


def notes_window(stream):
    ons = [t for t, _o, k, d in stream if k == 0x90 and d[1]]
    return min(ons), max(ons)


def segment(stream, start, end, first):
    """Events of one source channel for ticks [start, end). A note that starts inside keeps its note-off even
    if it falls after `end`. Unless this is the track's first segment, the channel state is re-sent at start."""
    out, open_notes = [], set()
    for t, o, k, d in stream:
        if k == 0x90 and d[1] == 0 and d[0] in open_notes:
            out.append((t, o, k, d))
            open_notes.discard(d[0])
        elif start <= t < end:
            if k == 0x90 and d[1]:
                open_notes.add(d[0])
            if not (k == 0x90 and d[1] == 0):
                out.append((t, o, k, d))
    if not first:
        st = state_at(stream, start)
        out += [(start, 1, 0xC0, bytes([st['prog']])), (start, 1, 0xB0, bytes([7, st[7]])),
                (start, 1, 0xB0, bytes([10, st[10]])), (start, 1, 0xB0, bytes([20, st[20]])),
                (start, 1, 0xE0, bytes([0x00, 0x40]))]
    return out


def to_raw(events, ch, remap_prog=None, remap_key=None):
    out = []
    for t, o, k, d in events:
        if k == 0xC0 and remap_prog:
            d = bytes([remap_prog.get(d[0], d[0])])
        if k == 0x90 and remap_key:
            d = bytes([remap_key.get(d[0], d[0]), d[1]])
        out.append((t, o, bytes([k | ch]) + d))
    return out


def vs_cynthia():
    div, evs = parse(os.path.join(REF, 'vs_cynthia.mid'))
    src = {c: channel_stream(evs, c) for c in range(16)}
    # output tracks: list of source channels (0-based), merged in time order
    layout = [[0], [1], [2], [3], [4], [5], [7], [8, 11, 13], [9], [10, 14], [12]]   # ch7 (6) and ch16 (15) dropped
    tracks = []
    for out_ch, group in enumerate(layout):
        wins = sorted((notes_window(src[c]) + (c,) for c in group))
        evs_out = []
        for idx, (lo, hi, c) in enumerate(wins):
            start = 0 if idx == 0 else lo
            end = wins[idx + 1][0] if idx + 1 < len(wins) else 1 << 30
            if idx + 1 < len(wins):
                assert hi < wins[idx + 1][0], f'ch{c + 1} overlaps ch{wins[idx + 1][2] + 1}'
            evs_out += segment(src[c], start, end, idx == 0)
        prog = {80: 82} if group[0] == 10 else None          # ch11: square lead 2
        key = {49: 57} if group == [9] else None             # drums
        tracks.append(to_raw(evs_out, out_ch, prog, key))
    write_midi(os.path.join(OUT, 'mus_orchid_vs_cynthia.mid'), div, conductor_events(evs, 'vs Cynthia'), tracks)
    return len(tracks)


def encounter_cynthia():
    div, evs = parse(os.path.join(REF, 'encounter_cynthia.mid'))
    stream = channel_stream(evs, 0)
    write_midi(os.path.join(OUT, 'mus_orchid_encounter_cynthia.mid'), div,
               conductor_events(evs, 'Encounter Cynthia'), [to_raw(stream, 0)])
    return 1


if __name__ == '__main__':
    print('mus_orchid_vs_cynthia.mid:', vs_cynthia(), 'tracks')
    print('mus_orchid_encounter_cynthia.mid:', encounter_cynthia(), 'track')
