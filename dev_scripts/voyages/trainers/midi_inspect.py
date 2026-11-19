"""Inspect a Standard MIDI File for m4a/mid2agb import (no mido needed).

Reports: format, ppqn, tempo map, time signature, length, every track's channels, program changes,
note range/count, controllers (vol 7, pan 10, expression 11, sustain 64, modulation 1), pitch bends,
markers (loop "[" / "]"), and the peak number of simultaneously sounding notes per channel and in
total (directsound budget check is done against a program->voice map given on the command line).

usage: midi_inspect.py FILE.mid [FILE2.mid ...]
"""
import struct
import sys
from collections import defaultdict

NOTE = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
GM = ["Acoustic Grand Piano", "Bright Acoustic Piano", "Electric Grand Piano", "Honky-tonk Piano", "Electric Piano 1",
      "Electric Piano 2", "Harpsichord", "Clavinet", "Celesta", "Glockenspiel", "Music Box", "Vibraphone", "Marimba",
      "Xylophone", "Tubular Bells", "Dulcimer", "Drawbar Organ", "Percussive Organ", "Rock Organ", "Church Organ",
      "Reed Organ", "Accordion", "Harmonica", "Tango Accordion", "Acoustic Guitar (nylon)", "Acoustic Guitar (steel)",
      "Electric Guitar (jazz)", "Electric Guitar (clean)", "Electric Guitar (muted)", "Overdriven Guitar",
      "Distortion Guitar", "Guitar Harmonics", "Acoustic Bass", "Electric Bass (finger)", "Electric Bass (pick)",
      "Fretless Bass", "Slap Bass 1", "Slap Bass 2", "Synth Bass 1", "Synth Bass 2", "Violin", "Viola", "Cello",
      "Contrabass", "Tremolo Strings", "Pizzicato Strings", "Orchestral Harp", "Timpani", "String Ensemble 1",
      "String Ensemble 2", "Synth Strings 1", "Synth Strings 2", "Choir Aahs", "Voice Oohs", "Synth Choir",
      "Orchestra Hit", "Trumpet", "Trombone", "Tuba", "Muted Trumpet", "French Horn", "Brass Section",
      "Synth Brass 1", "Synth Brass 2", "Soprano Sax", "Alto Sax", "Tenor Sax", "Baritone Sax", "Oboe",
      "English Horn", "Bassoon", "Clarinet", "Piccolo", "Flute", "Recorder", "Pan Flute", "Blown Bottle",
      "Shakuhachi", "Whistle", "Ocarina", "Lead 1 (square)", "Lead 2 (sawtooth)", "Lead 3 (calliope)",
      "Lead 4 (chiff)", "Lead 5 (charang)", "Lead 6 (voice)", "Lead 7 (fifths)", "Lead 8 (bass + lead)",
      "Pad 1 (new age)", "Pad 2 (warm)", "Pad 3 (polysynth)", "Pad 4 (choir)", "Pad 5 (bowed)", "Pad 6 (metallic)",
      "Pad 7 (halo)", "Pad 8 (sweep)", "FX 1 (rain)", "FX 2 (soundtrack)", "FX 3 (crystal)", "FX 4 (atmosphere)",
      "FX 5 (brightness)", "FX 6 (goblins)", "FX 7 (echoes)", "FX 8 (sci-fi)", "Sitar", "Banjo", "Shamisen", "Koto",
      "Kalimba", "Bagpipe", "Fiddle", "Shanai", "Tinkle Bell", "Agogo", "Steel Drums", "Woodblock", "Taiko Drum",
      "Melodic Tom", "Synth Drum", "Reverse Cymbal", "Guitar Fret Noise", "Breath Noise", "Seashore", "Bird Tweet",
      "Telephone Ring", "Helicopter", "Applause", "Gunshot"]


def nn(n):
    return f'{NOTE[n % 12]}{n // 12 - 1}'


def vlq(d, i):
    v = 0
    while True:
        b = d[i]; i += 1
        v = (v << 7) | (b & 0x7F)
        if not b & 0x80:
            return v, i


def parse(path):
    d = open(path, 'rb').read()
    assert d[:4] == b'MThd'
    hl = struct.unpack('>I', d[4:8])[0]
    fmt, ntr, div = struct.unpack('>HHH', d[8:14])
    i = 8 + hl
    tracks = []
    while i < len(d) and len(tracks) < ntr:
        assert d[i:i + 4] == b'MTrk', d[i:i + 4]
        ln = struct.unpack('>I', d[i + 4:i + 8])[0]
        tracks.append(d[i + 8:i + 8 + ln])
        i += 8 + ln
    evs = []
    for ti, t in enumerate(tracks):
        j, tick, run = 0, 0, None
        while j < len(t):
            dt, j = vlq(t, j)
            tick += dt
            st = t[j]
            if st == 0xFF:
                typ = t[j + 1]
                ln, j = vlq(t, j + 2)
                evs.append((tick, ti, 'meta', typ, t[j:j + ln])); j += ln
            elif st in (0xF0, 0xF7):
                ln, j = vlq(t, j + 1)
                evs.append((tick, ti, 'sysex', st, t[j:j + ln])); j += ln
            else:
                if st & 0x80:
                    run = st; j += 1
                else:
                    st = run
                hi, ch = st & 0xF0, st & 0x0F
                n = 1 if hi in (0xC0, 0xD0) else 2
                data = t[j:j + n]; j += n
                evs.append((tick, ti, hi, ch, bytes(data)))
    return fmt, ntr, div, evs


def report(path):
    fmt, ntr, div, evs = parse(path)
    out = [f'## {path.split("/")[-1]}', f'format {fmt}, {ntr} tracks, division {div} ppqn']
    tempos, sigs, markers, names, texts = [], [], [], defaultdict(list), []
    end = max(e[0] for e in evs)
    per_ch = defaultdict(lambda: {'tracks': set(), 'progs': [], 'notes': 0, 'lo': 127, 'hi': 0, 'cc': defaultdict(set),
                                  'bend': 0, 'vel': [127, 0]})
    for tick, ti, kind, a, data in evs:
        if kind == 'meta':
            if a == 0x51:
                tempos.append((tick, 60_000_000 / int.from_bytes(data, 'big')))
            elif a == 0x58:
                sigs.append((tick, f'{data[0]}/{2 ** data[1]}'))
            elif a in (0x06, 0x07):
                markers.append((tick, ti, data.decode('latin1')))
            elif a == 0x03:
                names[ti].append(data.decode('latin1'))
            elif a in (0x01,):
                texts.append((tick, ti, data.decode('latin1')))
        elif kind in (0x90, 0x80, 0xC0, 0xB0, 0xE0):
            c = per_ch[a]
            c['tracks'].add(ti)
            if kind == 0x90 and data[1] > 0:
                c['notes'] += 1; c['lo'] = min(c['lo'], data[0]); c['hi'] = max(c['hi'], data[0])
                c['vel'][0] = min(c['vel'][0], data[1]); c['vel'][1] = max(c['vel'][1], data[1])
            elif kind == 0xC0:
                c['progs'].append((tick, data[0]))
            elif kind == 0xB0:
                c['cc'][data[0]].add(data[1])
            elif kind == 0xE0:
                c['bend'] += 1
    # seconds via tempo map
    tm = sorted(tempos) or [(0, 120.0)]

    def secs(t):
        s, last_t, bpm = 0.0, 0, tm[0][1]
        for tt, b in tm:
            if tt > t:
                break
            s += (tt - last_t) / div * 60 / bpm
            last_t, bpm = tt, b
        return s + (t - last_t) / div * 60 / bpm
    bars = end / (div * 4)
    out.append(f'tempo: ' + ', '.join(f'{b:.1f} bpm @ tick {t}' for t, b in tm[:6]) + (' ...' if len(tm) > 6 else '')
               + f'  ({len(tm)} tempo events)')
    out.append(f'time signature: ' + (', '.join(f'{s} @ {t}' for t, s in sigs[:4]) or 'none (4/4 assumed)'))
    out.append(f'length: {end} ticks = {bars:.2f} bars of 4/4 = {secs(end):.1f} s')
    out.append(f'track names: ' + '; '.join(f'T{k}:{"/".join(v)}' for k, v in sorted(names.items())))
    out.append(f'markers: ' + (', '.join(f'{m!r} @ {t} (T{ti})' for t, ti, m in markers) or 'NONE'))
    if texts:
        out.append('text: ' + ', '.join(f'{m!r} @ {t}' for t, ti, m in texts[:8]))
    out.append('')
    out.append('| ch | tracks | program(s) | GM name | notes | range | vel | CCs (values seen) | bends |')
    out.append('|---|---|---|---|---|---|---|---|---|')
    for ch in sorted(per_ch):
        c = per_ch[ch]
        progs = sorted({p for _, p in c['progs']})
        gm = 'drums (ch10)' if ch == 9 else ', '.join(GM[p] for p in progs) or '-'
        ccs = '; '.join(f'{k}:{min(v)}-{max(v)}' if len(v) > 1 else f'{k}:{min(v)}' for k, v in sorted(c['cc'].items()))
        rng = f'{nn(c["lo"])}-{nn(c["hi"])} ({c["lo"]}-{c["hi"]})' if c['notes'] else '-'
        out.append(f'| {ch + 1} | {",".join(map(str, sorted(c["tracks"])))} | {",".join(map(str, progs)) or "-"} | {gm} '
                   f'| {c["notes"]} | {rng} | {c["vel"][0]}-{c["vel"][1]} | {ccs} | {c["bend"]} |')
    # polyphony per channel and total
    on = defaultdict(int)
    peak = defaultdict(int)
    tot, tpeak, tpeak_at = 0, 0, 0
    seq = []
    for tick, ti, kind, a, data in evs:
        if kind == 0x90 and data[1] > 0:
            seq.append((tick, 1, a))
        elif kind == 0x80 or (kind == 0x90 and data[1] == 0):
            seq.append((tick, 0, a))
    for tick, typ, ch in sorted(seq):   # offs before ons at the same tick
        if typ:
            on[ch] += 1; tot += 1
            peak[ch] = max(peak[ch], on[ch])
            if tot > tpeak:
                tpeak, tpeak_at = tot, tick
        else:
            on[ch] = max(0, on[ch] - 1); tot = max(0, tot - 1)
    out.append('')
    out.append('peak simultaneous notes per channel: ' + ', '.join(f'ch{c + 1}={peak[c]}' for c in sorted(peak))
               + f'; total peak {tpeak} @ tick {tpeak_at} (bar {tpeak_at / (div * 4) + 1:.1f})')
    return '\n'.join(out), per_ch, peak, (fmt, ntr, div, end, tm, markers)


if __name__ == '__main__':
    for p in sys.argv[1:]:
        print(report(p)[0])
        print()
