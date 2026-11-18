#!/usr/bin/env python3
"""Generate the placeholder trainer battle theme (mus_orchid_vs_trainer.mid).

Original composition, written as data so it is easy to tweak and regenerate.
Plays on the vanilla vs_trainer voicegroup (see sound/voicegroups/vs_trainer.inc):
  0  drumset (rs: 36 kick, 38 snare, 42 closed hat, 46 open hat, 55 crash)
  48 strings, 56 trumpet, 80 square lead, 81 wave bass, 82 square harmony

Layout: 4-bar intro, then a 16-bar loop (A: Em C D B x2, B: Am Em C D Am Em B B).
Directsound budget is 5 channels: strings x2 + trumpet + up to 2 drums.

Usage: python3 gen_orchid_vs_trainer.py <out.mid>
"""
import struct
import sys

PPQN = 24          # mid2agb's native clock: 16th = 6 ticks
S = 6              # one 16th note in ticks
BAR = 16           # 16ths per bar
TEMPO_BPM = 168

NOTE_BASE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def n(name):
    """'F#5' -> MIDI note number (C4 = 60)."""
    if name is None:
        return None
    pitch = NOTE_BASE[name[0]]
    rest = name[1:]
    while rest and rest[0] in "#b":
        pitch += 1 if rest[0] == "#" else -1
        rest = rest[1:]
    return pitch + 12 * (int(rest) + 1)


# ---- harmony -------------------------------------------------------------
CHORDS = {
    "Em": ("E", "G", "B"),
    "C": ("C", "E", "G"),
    "D": ("D", "F#", "A"),
    "B": ("B", "D#", "F#"),
    "Am": ("A", "C", "E"),
}
INTRO_GROOVE = ["Em", "Em"]
SECTION_A = ["Em", "C", "D", "B", "Em", "C", "D", "B"]
SECTION_B = ["Am", "Em", "C", "D", "Am", "Em", "B", "B"]
LOOP = SECTION_A + SECTION_B


def chord_note(root_name, octave):
    """Voice a chord tone so it sits at or above the octave's C."""
    return n(f"{root_name}{octave}")


# ---- melody (note, length in 16ths); None = rest -------------------------
INTRO_LEAD = (
    # bar 1: chromatic tumble down from B5
    [(f, 1) for f in ["B5", "A#5", "A5", "G#5", "G5", "F#5", "F5", "E5",
                      "D#5", "D5", "C#5", "C5", "B4", "A#4", "A4", "G#4"]]
    # bar 2: hits then a run up into the groove
    + [("E5", 2), (None, 2), ("E5", 2), (None, 2),
       ("F#5", 2), ("G5", 2), ("A5", 2), ("B5", 2)]
    # bars 3-4: lead rests while the groove sets up
    + [(None, 32)]
)

LEAD_A = [
    ("E5", 2), ("B4", 2), ("E5", 2), ("F#5", 2), ("G5", 4), ("F#5", 2), ("E5", 2),
    ("G5", 6), ("E5", 2), ("C5", 4), ("E5", 2), ("G5", 2),
    ("A5", 4), ("G5", 2), ("F#5", 2), ("D5", 4), ("F#5", 2), ("A5", 2),
    ("B5", 8), ("A5", 2), ("G5", 2), ("F#5", 2), ("D#5", 2),
    ("E5", 2), ("B4", 2), ("E5", 2), ("F#5", 2), ("G5", 2), ("A5", 2), ("B5", 4),
    ("C6", 4), ("B5", 2), ("A5", 2), ("G5", 4), ("E5", 4),
    ("F#5", 2), ("G5", 2), ("A5", 4), ("D6", 4), ("C6", 2), ("A5", 2),
    ("B5", 12), ("D#5", 2), ("F#5", 2),
]

LEAD_B = [
    ("C6", 4), ("B5", 2), ("A5", 2), ("E5", 4), ("A5", 4),
    ("G5", 6), ("F#5", 2), ("E5", 8),
    ("E5", 2), ("G5", 2), ("C6", 4), ("B5", 2), ("C6", 2), ("D6", 4),
    ("D6", 8), ("C6", 4), ("A5", 4),
    ("A5", 2), ("B5", 2), ("C6", 4), ("E6", 4), ("D6", 2), ("C6", 2),
    ("B5", 6), ("A5", 2), ("G5", 4), ("E5", 4),
    ("F#5", 4), ("G5", 4), ("A5", 4), ("B5", 4),
    ("D#6", 8), ("B5", 4), (None, 4),
]


class Track:
    def __init__(self):
        self.events = []  # (tick, order, bytes)

    def add(self, tick, data, order=1):
        self.events.append((tick, order, bytes(data)))

    def note(self, tick, pitch, length, vel, gate=None, ch=0):
        gate = length if gate is None else gate
        self.add(tick, [0x90 | ch, pitch, vel], order=2)
        self.add(tick + gate, [0x80 | ch, pitch, 0], order=0)

    def setup(self, program, volume, pan, ch=0):
        self.add(0, [0xC0 | ch, program], order=0)
        self.add(0, [0xB0 | ch, 7, volume], order=0)
        self.add(0, [0xB0 | ch, 10, pan], order=0)

    def meta(self, tick, kind, data):
        self.add(tick, [0xFF, kind, len(data)] + list(data), order=0)

    def encode(self, end_tick):
        self.meta(end_tick, 0x2F, b"")
        out = bytearray()
        last = 0
        for tick, _, data in sorted(self.events, key=lambda e: (e[0], e[1])):
            out += varlen(tick - last) + data
            last = tick
        return b"MTrk" + struct.pack(">I", len(out)) + out


def varlen(value):
    buf = [value & 0x7F]
    value >>= 7
    while value:
        buf.insert(0, (value & 0x7F) | 0x80)
        value >>= 7
    return bytes(buf)


def write_line(track, start_tick, line, vel, gate_ratio=0.9, transpose=0):
    tick = start_tick
    for name, length in line:
        ticks = length * S
        if name is not None:
            gate = max(1, int(ticks * gate_ratio)) if ticks > S else ticks - 1
            track.note(tick, n(name) + transpose, ticks, vel, gate)
        tick += ticks
    return tick


def main(out_path):
    intro_bars = 4
    loop_start = intro_bars * BAR * S
    loop_end = loop_start + len(LOOP) * BAR * S

    conductor = Track()
    us_per_beat = int(60_000_000 / TEMPO_BPM)
    conductor.meta(0, 0x51, us_per_beat.to_bytes(3, "big"))
    conductor.meta(0, 0x58, bytes([4, 2, 24, 8]))
    conductor.meta(loop_start, 0x06, b"[")
    conductor.meta(loop_end, 0x06, b"]")

    # --- lead (square 2) ---
    lead = Track()
    lead.setup(80, 100, 64)
    t = write_line(lead, 0, INTRO_LEAD, 110)
    t = write_line(lead, t, LEAD_A, 108)
    write_line(lead, t, LEAD_B, 112)

    # --- harmony: 16th arpeggios (square 1) ---
    harm = Track()
    harm.setup(82, 58, 40)
    bars = ["Em", "Em"] + INTRO_GROOVE + LOOP
    for i, chord in enumerate(bars):
        if i < 2:
            continue  # intro bars 1-2 belong to the lead
        root, third, fifth = CHORDS[chord]
        lo = 3 if root in ("A", "B") else 4
        r = chord_note(root, lo)
        tones = [r, r + (n(f"{third}4") - n(f"{root}4")) % 12,
                 r + (n(f"{fifth}4") - n(f"{root}4")) % 12]
        pattern = [tones[0], tones[1], tones[2], tones[1]]
        for step in range(BAR):
            harm.note((i * BAR + step) * S, pattern[step % 4], S, 92, S - 1)

    # --- bass: driving octave 8ths (wave) ---
    bass = Track()
    bass.setup(81, 120, 64)
    # intro bar 1: long low E; bar 2 shadows the lead hits
    bass.note(0, n("E2"), BAR * S, 110, BAR * S - 2)
    t = BAR * S
    for name, length in [("E2", 2), (None, 2), ("E2", 2), (None, 2),
                         ("F#2", 2), ("G2", 2), ("A2", 2), ("B2", 2)]:
        if name:
            bass.note(t, n(name), length * S, 110, length * S - 3)
        t += length * S
    for i, chord in enumerate(INTRO_GROOVE + LOOP):
        root = CHORDS[chord][0]
        low = n(f"{root}2")
        bar_tick = (2 + i) * BAR * S
        for step in range(8):
            pitch = low if step % 2 == 0 else low + 12
            bass.note(bar_tick + step * 2 * S, pitch, 2 * S, 112, 2 * S - 4)

    # --- strings: two-note pads (3rd + 5th) through the loop ---
    strings = Track()
    strings.setup(48, 62, 88)
    for i, chord in enumerate(LOOP):
        _, third, fifth = CHORDS[chord]
        bar_tick = loop_start + i * BAR * S
        for name in (third, fifth):
            pitch = n(f"{name}4")
            if pitch < n("E4"):
                pitch += 12
            strings.note(bar_tick, pitch, BAR * S, 80, BAR * S - 2)

    # --- trumpet: unison hits in the intro, doubles the B melody an octave down ---
    trumpet = Track()
    trumpet.setup(56, 84, 64)
    t = BAR * S
    for name, length in [("E4", 2), (None, 2), ("E4", 2), (None, 2),
                         ("F#4", 2), ("G4", 2), ("A4", 2), ("B4", 2)]:
        if name:
            trumpet.note(t, n(name), length * S, 100, length * S - 2)
        t += length * S
    b_start = loop_start + len(SECTION_A) * BAR * S
    write_line(trumpet, b_start, LEAD_B, 96, transpose=-12)

    # --- drums ---
    drums = Track()
    drums.setup(0, 96, 64)
    KICK, SNARE, CHAT, OHAT, CRASH = 36, 38, 42, 46, 55
    # intro bar 1: snare roll, bar 2: hits with the band
    for step in range(BAR):
        drums.note(step * S, SNARE, S, 50 + step * 4, S - 1)
    t = BAR * S
    for step, (name, length) in enumerate([(1, 2), (0, 2), (1, 2), (0, 2),
                                           (1, 2), (1, 2), (1, 2), (1, 2)]):
        if name:
            drums.note(t, SNARE if step < 4 else KICK, length * S, 110, S)
        t += length * S

    def groove(bar_tick, crash=False, fill=False):
        for step in range(BAR):
            tick = bar_tick + step * S
            if crash and step == 0:
                drums.note(tick, CRASH, 4 * S, 110, 4 * S)
            elif step % 2 == 0 and not (crash and step < 4):
                drums.note(tick, OHAT if step == 14 else CHAT, S, 70, S - 1)
            if step in (0, 6, 8, 10):
                drums.note(tick, KICK, S, 118, S - 1)
            if fill and step >= 12:
                drums.note(tick, SNARE, S, 90 + (step - 12) * 8, S - 1)
            elif step in (4, 12):
                drums.note(tick, SNARE, S, 112, S - 1)

    bars = INTRO_GROOVE + LOOP
    for i in range(len(bars)):
        bar_tick = (2 + i) * BAR * S
        loop_bar = i - len(INTRO_GROOVE)
        crash = i == 0 or loop_bar in (0, 8)
        fill = i == 1 or loop_bar in (7, 15)
        groove(bar_tick, crash=crash, fill=fill)

    tracks = [conductor, lead, harm, bass, strings, trumpet, drums]
    with open(out_path, "wb") as f:
        f.write(b"MThd" + struct.pack(">IHHH", 6, 1, len(tracks), PPQN))
        for track in tracks:
            f.write(track.encode(loop_end))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "mus_orchid_vs_trainer.mid")
