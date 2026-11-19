"""MUS_ORCHID_ENCOUNTER_HOLON: the DPPt "Encounter (Team Galactic)" rip (ref/encounter_team_galactic.mid, a
GM-sequenced 48 ppqn rip, tracks SEQ_EYE_GINGA / Track: 0x...) prepared for mid2agb, plus its GM-numbered voicegroup.

    python3 dev_scripts/voyages/trainers/holon_encounter_music.py

Writes sound/songs/midi/mus_orchid_encounter_holon.mid and sound/voicegroups/mus_orchid_encounter_holon.inc.
Same approach as prepare_cynthia_midis.py / gen_cynthia_voicegroups.py: voicegroup slot = MIDI program, every
voice copied verbatim from a vanilla Emerald voicegroup (noted per slot).

Source layout (9 bars of 4/4 at 110 bpm; bar 1 is the intro, bars 2-9 the loop body):
  ch1, ch2, ch3, ch5  organ (19) / trumpet (56) lines that swap programs per section
  ch4                 bass (35 fretless / 37 slap / 39 synth)
  ch6                 glockenspiel arpeggios (bars 1-5)
  ch7                 clavinet riff (bars 2-9)
  ch8                 detuned double of ch2 (bars 5-9) + one piano note in bar 1   -> DROPPED
  ch10                drums (GS kit)

GBA budget (m4a: 5 directsound channels + square1 / square2 / wave / noise):
  T1 ch1 lead         square 1   (19 -> slot 85 50% duty, 56 -> slot 80 75% duty, so the organ/trumpet swap
                                  still changes colour)
  T2 ch2, T3 ch3,
  T5 ch5              directsound organ2 (19) / trumpet keysplit (56)
  T4 ch4 bass         wave channel (35 -> wave 16 sine-ish, 37 -> wave 5, 39 -> wave 3 saw)
  T6 ch6 glock        directsound glockenspiel (bars 1-5 only)
  T7 ch7 clavinet     square 2 (12.5% duty, fast decay: closest PSG colour to a clav)
  T8 ch10 kit         directsound rs_drumset: kick 36, snare 40 -> 38 (rnd snare), clap 39, toms 41-48;
                      key 31 (sticks, once in the intro) dropped: rs_drumset starts at 36
  T9 ch10 hats/tamb   noise channel, like MUS_ENCOUNTER_AQUA: 42/44/54 -> slot 127 key 76 (short), 46 -> slot 126
                      key 79 (open)
  => at most 5 directsound notes (ch2, ch3, ch5, glock, one drum) at any time.

Also: ticks halved to 24 ppqn (note-offs rounded down, never shorter than 1); only notes, programs, pitch bends and
CC 7/10 are kept; RPN 0 bend range (12 semitones in every channel) becomes CC20 (mid2agb BENDR); SysEx / GS meta
junk dropped. Loop: "[" at bar 2 (24 ppqn tick 96) and "]" at the end of bar 9 (tick 864), as marker meta events
on the conductor track; every track re-sends its program / volume / pan / bend range / bend at the loop start.
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import prepare_cynthia_midis as pc  # noqa: E402  (parse / vlq / track_chunk / channel_stream helpers)

ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SRC = os.path.join(HERE, '..', 'ref', 'encounter_team_galactic.mid')
OUT_MID = os.path.join(ROOT, 'sound', 'songs', 'midi', 'mus_orchid_encounter_holon.mid')
NAME = 'mus_orchid_encounter_holon'

LOOP_START, LOOP_END = 96, 864           # 24 ppqn: bar 2 .. end of bar 9
KEEP_CC = {7, 10, 20}

HATS = {42: (127, 76), 44: (127, 76), 54: (127, 76), 46: (126, 79)}   # GS key -> (noise slot, noise key)
DRUM_KEYS = {40: 38}                     # electric snare -> rs rnd_snare
DRUM_DROP = {31}

# output track -> (source channel 0-based, program remap)
TRACKS = [
    (0, {19: 85, 56: 80}),               # T1 lead on square 1
    (1, None),                           # T2 organ / trumpet (DS)
    (2, None),                           # T3 organ / trumpet (DS)
    (3, None),                           # T4 bass (wave)
    (4, None),                           # T5 organ / trumpet (DS)
    (5, None),                           # T6 glockenspiel (DS)
    (6, None),                           # T7 clavinet (square 2)
]

FILL = 'voice_square_1 60, 0, 0, 2, 0, 0, 15, 0'
VOICES = {
    0: 'voice_keysplit_all voicegroup_rs_drumset',                                                   # encounter_aqua 0
    7: 'voice_square_2 60, 0, 0, 0, 2, 4, 1',                                                        # clavinet -> vs_trainer 4
    9: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_glockenspiel, 255, 204, 51, 242',       # route119 9
    19: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_organ2, 255, 0, 255, 165',             # church organ -> encounter_aqua 17
    35: 'voice_programmable_wave_alt 60, 0, ProgrammableWaveData_16, 0, 7, 15, 0',                   # fretless -> encounter_magma 83
    37: 'voice_programmable_wave_alt 60, 0, ProgrammableWaveData_5, 0, 7, 15, 2',                    # slap -> vs_trainer 81
    39: 'voice_programmable_wave_alt 60, 0, ProgrammableWaveData_3, 0, 7, 15, 0',                    # synth bass -> encounter_aqua 83
    56: 'voice_keysplit voicegroup_trumpet_keysplit, keysplit_trumpet',                              # encounter_aqua 56
    80: 'voice_square_1 60, 0, 0, 3, 0, 1, 7, 1',                                                    # lead, trumpet parts -> vs_trainer 7
    85: 'voice_square_1 60, 0, 0, 2, 0, 1, 7, 1',                                                    # lead, organ parts -> vs_trainer 82
    126: 'voice_noise_alt 60, 0, 0, 0, 1, 7, 1',                                                     # open hat -> encounter_aqua 126
    127: 'voice_noise_alt 60, 0, 0, 0, 1, 0, 0',                                                     # closed hat / tambourine -> encounter_aqua 127
}


def halve(stream):
    """48 -> 24 ppqn. Note-offs round down but never onto/before their own note-on."""
    out, on = [], {}
    for t, o, k, d in stream:
        if k == 0x90 and d[1]:
            nt = t // 2
            on[d[0]] = nt
            out.append((nt, o, k, d))
        elif k == 0x90:
            nt = max(t // 2, on.pop(d[0], -1) + 1)
            out.append((nt, o, k, d))
        else:
            out.append((t // 2, o, k, d))
    return out


def loop_state(stream, prog_remap):
    """Program / CC7 / CC10 / CC20 / bend in force at LOOP_START (events at that tick included)."""
    st = {'prog': None, 7: None, 10: None, 20: None, 'bend': bytes([0x00, 0x40])}
    for t, _o, k, d in stream:
        if t > LOOP_START:
            break
        if k == 0xC0:
            st['prog'] = d[0]
        elif k == 0xB0 and d[0] in (7, 10, 20):
            st[d[0]] = d[1]
        elif k == 0xE0:
            st['bend'] = d
    ev = []
    if st['prog'] is not None:
        p = st['prog']
        ev.append((LOOP_START, 1, 0xC0, bytes([prog_remap.get(p, p) if prog_remap else p])))
    for cc in (7, 10, 20):
        if st[cc] is not None:
            ev.append((LOOP_START, 1, 0xB0, bytes([cc, st[cc]])))
    ev.append((LOOP_START, 1, 0xE0, st['bend']))
    return ev


def melodic(evs, ch, prog_remap):
    stream = halve([e for e in pc.channel_stream(evs, ch) if not (e[2] == 0xB0 and e[3][0] not in KEEP_CC)])
    # drop setup events sitting exactly on the loop start (re-sent as one snapshot below)
    body = [e for e in stream if not (e[0] == LOOP_START and e[2] in (0xB0, 0xC0, 0xE0))]
    body += loop_state(stream, None)
    body = [e for e in body if e[0] <= LOOP_END]
    return pc.to_raw(body, len(TRACK_OUT), prog_remap)


def drums(evs):
    stream = halve(pc.channel_stream(evs, 9))
    kit, noise, last_noise_prog = [], [], None
    kit.append((0, 1, 0xC0, bytes([0])))
    for e in stream:
        t, o, k, d = e
        if t > LOOP_END:
            continue
        if k == 0xB0 and d[0] in (7, 10):
            kit.append(e)
            noise.append(e)
        elif k == 0x90:
            key = d[0]
            if key in DRUM_DROP:
                continue
            if key in HATS:
                slot, nkey = HATS[key]
                if d[1] and slot != last_noise_prog:
                    noise.append((t, 1, 0xC0, bytes([slot])))
                    last_noise_prog = slot
                noise.append((t, o, k, bytes([nkey, d[1]])))
            else:
                kit.append((t, o, k, bytes([DRUM_KEYS.get(key, key), d[1]])))
    # intro fill: a kick starting while a snare/tom still sounds would be the 6th directsound note (glock + 3 lines)
    drop, on_at = set(), {}
    for t, o, k, d in sorted(kit, key=lambda e: (e[0], e[1])):
        if k == 0x90:
            if d[1]:
                if d[0] == 36 and t < LOOP_START and on_at:
                    drop.add(t)
                on_at[d[0]] = t
            else:
                on_at.pop(d[0], None)
    kept, skip_off = [], 0
    for e in sorted(kit, key=lambda e: (e[0], e[1])):
        if e[2] == 0x90 and e[3][0] == 36:
            if e[3][1] and e[0] in drop:
                skip_off += 1
                continue
            if not e[3][1] and skip_off:
                skip_off -= 1
                continue
        kept.append(e)
    kit = kept
    # after the jump back, the noise program left over from bar 9 must be replaced by the one in force at bar 2
    progs = [d[0] for t, o, k, d in noise if k == 0xC0 and t <= LOOP_START]
    noise = [e for e in noise if not (e[0] == LOOP_START and e[2] == 0xC0)]
    if progs:
        noise.append((LOOP_START, 1, 0xC0, bytes([progs[-1]])))
    kit.append((LOOP_START, 1, 0xC0, bytes([0])))
    return kit, noise


TRACK_OUT = []


def build():
    div, evs = pc.parse(SRC)
    assert div == 48, div
    for ch, remap in TRACKS:
        TRACK_OUT.append(melodic(evs, ch, remap))
    kit, noise = drums(evs)
    TRACK_OUT.append(pc.to_raw(kit, len(TRACK_OUT)))
    TRACK_OUT.append(pc.to_raw(noise, len(TRACK_OUT)))
    cond = [(0, 0, b'\xFF\x03' + pc.vlq(len('Encounter Holon')) + b'Encounter Holon')]
    for tick, kind, a, data in evs:
        if kind == 'meta' and a in (0x51, 0x58):
            cond.append((tick // 2, 1, b'\xFF' + bytes([a]) + pc.vlq(len(data)) + data))
    cond.append((LOOP_START, 2, b'\xFF\x06\x01['))
    cond.append((LOOP_END, 2, b'\xFF\x06\x01]'))
    # write with ppqn 24
    data = b'MThd' + struct.pack('>IHHH', 6, 1, 1 + len(TRACK_OUT), 24) + pc.track_chunk(cond)
    for t in TRACK_OUT:
        data += pc.track_chunk(t)
    open(OUT_MID, 'wb').write(data)
    lines = [f'voice_group {NAME}'] + ['\t' + VOICES.get(i, FILL) for i in range(128)]
    open(os.path.join(ROOT, 'sound', 'voicegroups', NAME + '.inc'), 'w').write('\n'.join(lines) + '\n')
    return len(TRACK_OUT)


if __name__ == '__main__':
    print(OUT_MID, build(), 'tracks')
