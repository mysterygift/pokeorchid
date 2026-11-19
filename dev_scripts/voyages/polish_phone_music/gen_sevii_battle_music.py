#!/usr/bin/env python3
"""Sevii battle music: FRLG battle songs re-voiced onto Hoenn (Emerald) instruments.

User decision (Wavebreak Voyages): "Sevii should use FR/LG battle music, but change the voicegroups to match
Hoenn music". For each FRLG song this writes
  sound/songs/midi/mus_orchid_sevii_<name>.mid   = the FRLG MIDI, every event kept (loop markers included),
                                                    drum-kit notes remapped from the FRLG kit to rs_drumset keys
  sound/voicegroups/sevii_<name>.inc             = a voicegroup whose slot N holds the closest *Emerald* voice
                                                    for what FRLG had in slot N (copied verbatim from a vanilla
                                                    Emerald voicegroup, so program numbers in the MIDI stay as-is)
and prints the mapping table + directsound polyphony check (m4a has 5 directsound channels).

CGB voices are only ever replaced by the same CGB channel kind (square 1 / square 2 / wave / noise), so channel
sharing between tracks is exactly as in the FRLG original. The victory songs need nothing: FRLG reused the R/S
victory themes (mus_rg_victory_wild.mid is byte-identical to mus_victory_wild.mid, the trainer one differs only by
a few CC values) and its rg_victory_* voicegroups are byte-identical to Emerald's, so Sevii keeps MUS_VICTORY_*.

usage: python3 gen_sevii_battle_music.py [--write]     (run from anywhere; paths are repo-relative)
"""
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
import smf  # noqa: E402

VG_DIR = os.path.join(REPO, 'sound', 'voicegroups')
MIDI_DIR = os.path.join(REPO, 'sound', 'songs', 'midi')
FILLER = 'voice_square_1 60, 0, 0, 2, 0, 0, 15, 0'

# FRLG drum kit key -> rs_drumset key (both kits start at key 36). FRLG has no hi-hats in the kit (it uses the noise
# channel), and no cowbell / triangle / Japanese percussion in rs_drumset, so those fold onto the nearest Hoenn piece.
DRUM_KEYS = {
    35: 36,                 # below the FRLG kit (silent garbage) -> kick
    36: 36,                 # kick -> rnd kick
    37: 38, 38: 38,         # sd90 solo snare -> rnd snare
    39: 39,                 # 909 clap
    40: 40, 42: 40,         # orchestra snare
    44: 38, 46: 38,         # rnd snare
    41: 41, 43: 43, 45: 45, 47: 47, 48: 48, 50: 50,     # ambient toms -> sc55 toms (same keys)
    49: 57, 52: 57, 57: 57, 59: 59, 60: 60,             # orchestra crashes
    53: 53,                 # ride bell -> bell
    54: 54,                 # tambourine
    55: 55,                 # trinity crash
    56: 53,                 # cowbell -> bell
    61: 64, 63: 64, 64: 64, 62: 62,                     # indian drum / congas -> congas
    80: 54, 81: 54, 82: 54, 83: 54,                     # triangle / jingle bell -> tambourine
    86: 53, 87: 36, 88: 62, 89: 62,                     # atarigane / taiko / kotsuzumi
}

# name: (FRLG source song, FRLG voicegroup, Hoenn counterpart, midi.cfg flags, {slot: (emerald voicegroup, slot)})
SONGS = {
    'vs_wild': ('mus_rg_vs_wild', 'rg_vs_wild', 'vs_wild', '-E -R50 -G_sevii_vs_wild -V090 -P1', {
        0: ('vs_wild', 0),                  # FRLG kit -> rs_drumset
        4: ('vs_wild', 80),                 # square 2, 75% duty
        17: ('vs_trainer', 17),             # organ
        24: ('b_frontier', 24),             # nylon guitar, Emerald's usual envelope
        33: ('vs_wild', 33),                # fingered bass
        48: ('vs_wild', 48),                # strings
        80: ('vs_frontier_brain', 80),      # square 1, 25% duty (Emerald has this exact voice)
        81: ('vs_wild', 80),                # square 2, 75% duty
        82: ('vs_trainer', 90),             # wave lead, same waveform 7, Emerald envelope
        87: ('aqua_magma_hideout', 82),     # wave, waveform 6
        92: ('vs_wild', 4),                 # square 2, 50% duty
        126: ('vs_mew', 126),               # noise (open hat)
        127: ('vs_mew', 127),               # noise (closed hat)
    }),
    'vs_trainer': ('mus_rg_vs_trainer', 'rg_vs_trainer', 'vs_trainer', '-E -R50 -G_sevii_vs_trainer -V090 -P1', {
        0: ('vs_trainer', 0),
        3: ('vs_trainer', 81),              # wave, waveform 5
        5: ('vs_frontier_brain', 4),        # detuned e.piano
        17: ('vs_trainer', 17),             # organ
        21: ('petalburg', 56),              # accordion
        24: ('b_frontier', 24),             # nylon guitar
        29: ('b_pyramid', 29),              # overdrive guitar
        30: ('b_pyramid', 30),              # distortion guitar (high)
        33: ('vs_trainer', 6),              # square-2 bass, 75% duty
        48: ('vs_trainer', 48),             # strings
        56: ('vs_trainer', 56),             # trumpet
        60: ('vs_trainer', 60),             # french horn
        62: ('b_pyramid', 62),              # distortion guitar (low)
        81: ('vs_trainer', 5),              # square 1, 12.5% duty
        82: ('vs_trainer', 7),              # square 1, 75% duty
        120: ('vs_frontier_brain', 120),    # scream drive
        125: ('rs_sfx_1', 123),             # long noise
        126: ('vs_mew', 126),               # noise
        127: ('vs_frontier_brain', 127),    # noise
    }),
    'encounter_boy': ('mus_rg_encounter_boy', 'rg_encounter_boy', 'encounter_male', '-E -R50 -G_sevii_encounter_boy -V090', {
        0: ('encounter_male', 0),
        1: ('vs_trainer', 1),               # piano
        17: ('encounter_male', 17),         # organ
        18: ('encounter_male', 17),         # organ (FRLG's slow-attack copy)
        38: ('encounter_girl', 38),         # synth bass
        80: ('encounter_male', 82),         # square 2, 75% duty
        81: ('vs_trainer', 83),             # square 2, 25% duty
        126: ('encounter_magma', 126),      # noise
        127: ('vs_frontier_brain', 127),    # noise
    }),
    'encounter_girl': ('mus_rg_encounter_girl', 'rg_encounter_girl', 'encounter_girl', '-E -R50 -G_sevii_encounter_girl -V051', {
        0: ('encounter_girl', 0),
        1: ('encounter_girl', 1),           # piano
        17: ('aqua_magma_hideout', 17),     # organ
        24: ('b_frontier', 24),             # nylon guitar
        48: ('encounter_female', 48),       # strings
        80: ('vs_trainer', 6),              # square 2, 75% duty (bass)
        81: ('vs_trainer', 82),             # square 1, 50% duty
        126: ('encounter_magma', 126),      # noise
        127: ('vs_mew', 127),               # noise
    }),
    'encounter_rocket': ('mus_rg_encounter_rocket', 'rg_encounter_rocket', 'encounter_magma', '-E -R50 -G_sevii_encounter_rocket -V096', {
        0: ('encounter_magma', 0),
        17: ('encounter_aqua', 17),         # organ
        24: ('b_frontier', 24),             # nylon guitar
        38: ('encounter_magma', 38),        # synth bass
        80: ('vs_trainer', 82),             # square 1, 50% duty
        81: ('vs_trainer', 80),             # square 2, 50% duty
        83: ('encounter_magma', 83),        # wave (Emerald's evil-team waveform 16; FRLG had 14)
    }),
}


def load_vg(name):
    path = os.path.join(VG_DIR, name + '.inc')
    out = []
    for line in open(path):
        s = line.strip()
        if s.startswith('voice_') and not s.startswith('voice_group'):
            out.append(s)
    return out


def kind(voice):
    """'ds' for anything played on a directsound channel, else the CGB channel."""
    v = voice.split()[0]
    if v.startswith('voice_square_1'):
        return 'sq1'
    if v.startswith('voice_square_2'):
        return 'sq2'
    if v.startswith('voice_programmable_wave'):
        return 'wave'
    if v.startswith('voice_noise'):
        return 'noise'
    return 'ds'


def short(voice):
    m = re.search(r'DirectSoundWaveData_(\w+)', voice)
    if m:
        return m.group(1).replace('sc88pro_', '').replace('sd90_classical_', '').replace('sd90_special_', '')
    m = re.search(r'voicegroup_(\w+?)(_keysplit)?,', voice + ',')
    if voice.startswith('voice_keysplit'):
        return voice.split()[1].replace('voicegroup_', '').rstrip(',')
    k = kind(voice)
    p = [x.strip(',') for x in voice.split()[1:]]
    if k == 'sq1':
        return f'square1 duty{p[3]} env {",".join(p[4:])}'
    if k == 'sq2':
        return f'square2 duty{p[2]} env {",".join(p[3:])}'
    if k == 'wave':
        return f'wave {p[2].replace("ProgrammableWaveData_", "#")} env {",".join(p[3:])}'
    return f'noise env {",".join(p[3:])}'


def note_spans(tracks, voice_of):
    """[(start, end, kind)] for every note, kind from the track's current program."""
    spans = []
    for evs in tracks:
        prog, on = {}, {}
        for e in evs:
            if e.kind != 'midi':
                continue
            if e.cmd == 0xC0:
                prog[e.ch] = e.data[0]
            elif e.cmd == 0x90 and e.data[1] > 0:
                on[(e.ch, e.data[0])] = (e.tick, voice_of(prog.get(e.ch, 0)))
            elif e.cmd == 0x80 or (e.cmd == 0x90 and e.data[1] == 0):
                k = (e.ch, e.data[0])
                if k in on:
                    t0, v = on.pop(k)
                    spans.append((t0, max(e.tick, t0 + 1), v))
    return spans


def peak_ds(spans):
    pts = []
    for a, b, v in spans:
        if v == 'ds':
            pts += [(a, 1), (b, -1)]
    cur = best = 0
    at = 0
    for t, d in sorted(pts, key=lambda x: (x[0], x[1])):
        cur += d
        if cur > best:
            best, at = cur, t
    over = 0
    cur, last = 0, 0
    for t, d in sorted(pts, key=lambda x: (x[0], x[1])):
        if cur > 5:
            over += t - last
        cur += d
        last = t
    return best, at, over


def main():
    write = '--write' in sys.argv
    report = []
    for name, (src, frlg_vg, counterpart, cfg, slots) in SONGS.items():
        frlg = load_vg(frlg_vg)
        fmt, div, tracks = smf.read(os.path.join(MIDI_DIR, src + '.mid'))

        # which programs does the song actually use?
        used = set()
        for evs in tracks:
            for e in evs:
                if e.kind == 'midi' and e.cmd == 0xC0:
                    used.add(e.data[0])
        missing = sorted(used - set(slots))
        assert not missing, f'{name}: no Hoenn voice chosen for FRLG programs {missing}'

        vg = [FILLER] * (max(slots) + 1)
        rows = []
        for slot in sorted(slots):
            sv, ss = slots[slot]
            hoenn = load_vg(sv)[ss]
            old = frlg[slot]
            assert kind(hoenn) == kind(old), f'{name} slot {slot}: {old} -> {hoenn} changes channel kind'
            if slot == 0:
                assert 'rs_drumset' in hoenn
            vg[slot] = hoenn
            rows.append((slot, short(old), short(hoenn), f'{sv}:{ss}', 'same' if hoenn == old else ''))

        # drum notes: FRLG kit -> rs_drumset keys (only while program 0 is selected on that channel)
        drum_hits = defaultdict(int)
        for evs in tracks:
            prog = {}
            for e in evs:
                if e.kind != 'midi':
                    continue
                if e.cmd == 0xC0:
                    prog[e.ch] = e.data[0]
                elif e.cmd in (0x80, 0x90, 0xA0) and prog.get(e.ch) == 0:
                    k = e.data[0]
                    assert k in DRUM_KEYS, f'{name}: FRLG drum key {k} has no rs_drumset mapping'
                    if e.cmd == 0x90 and e.data[1] > 0:
                        drum_hits[(k, DRUM_KEYS[k])] += 1
                    e.data[0] = DRUM_KEYS[k]

        before = peak_ds(note_spans(smf.read(os.path.join(MIDI_DIR, src + '.mid'))[2],
                                    lambda p: kind(frlg[p]) if p < len(frlg) else 'ds'))
        after = peak_ds(note_spans(tracks, lambda p: kind(vg[p])))

        out_mid = os.path.join(MIDI_DIR, f'mus_orchid_sevii_{name}.mid')
        out_vg = os.path.join(VG_DIR, f'sevii_{name}.inc')
        if write:
            smf.write(out_mid, fmt, div, tracks)
            with open(out_vg, 'w') as f:
                f.write(f'@ Generated by dev_scripts/voyages/polish_phone_music/gen_sevii_battle_music.py: FRLG {frlg_vg}\n')
                f.write(f'@ slots re-voiced with vanilla Emerald voices (Hoenn counterpart: {counterpart}).\n')
                f.write(f'voice_group sevii_{name}\n')
                for v in vg:
                    f.write(f'\t{v}\n')

        report.append(f'### MUS_ORCHID_SEVII_{name.upper()} (from {src}, Hoenn counterpart `{counterpart}`)\n')
        report.append(f'midi.cfg: `mus_orchid_sevii_{name}.mid: {cfg}`\n')
        report.append('| slot | FRLG voice | Hoenn voice | taken from | |\n|---|---|---|---|---|')
        for r in rows:
            report.append(f'| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |')
        if drum_hits:
            report.append('\nDrum keys (FRLG kit -> rs_drumset, hits): ' +
                          ', '.join(f'{a}->{b} ({n})' for (a, b), n in sorted(drum_hits.items())))
        report.append(f'\nDirectsound peak: FRLG {before[0]} (ticks over 5: {before[2]}), Sevii {after[0]} '
                      f'(ticks over 5: {after[2]}, peak at tick {after[1]})\n')
        print(f'{name}: {len(rows)} slots, ds peak {before[0]} -> {after[0]}, '
              f'{"written" if write else "dry run"}')
    with open(os.path.join(HERE, 'mapping.md'), 'w') as f:
        f.write('# Sevii battle music: FRLG slot -> Hoenn voice (generated)\n\n' + '\n'.join(report) + '\n')


if __name__ == '__main__':
    main()
