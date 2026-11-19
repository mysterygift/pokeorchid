"""Cynthia music import plan: map each MIDI channel/program of the user's two MIDIs onto vanilla m4a voices
and measure the directsound (DS) load against m4a's 5-channel mixer (src/m4a.c: 5 << SOUND_MODE_MAXCHN_SHIFT)
and the BGM player's 10 tracks (sound/music_player_table.inc NUM_TRACKS_BGM).

Prints markdown (pasted into out/batch5_trainers/NOTES.md). No files are changed.
usage: music_plan.py
"""
import os
from collections import defaultdict

import midi_inspect as mi

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, '..', 'ref')

# GM program -> (voice used in our voicegroup, source voicegroup slot, DS?)  'drop' = not imported
VOICE = {
    0: ('piano keysplit (voicegroup_piano_keysplit)', 'vs_champion 1 / vs_frontier_brain 1', True),
    1: ('piano keysplit', 'vs_champion 1', True),
    30: ('sd90_classical_distortion_guitar_high', 'vs_frontier_brain 30', True),
    38: ('sc88pro_synth_bass', 'vs_frontier_brain 38 / vs_elite_four 38', True),
    39: ('drop (exact double of ch5)', '-', None),
    44: ('strings keysplit (no tremolo sample)', 'vs_champion 48', True),
    47: ('sc88pro_timpani', 'vs_champion 47', True),
    48: ('strings keysplit', 'vs_champion 48', True),
    52: ('classical_choir_voice_ahhs', 'rg_vs_champion / b_pike', True),
    55: ('trumpet keysplit stab (no orchestra-hit sample)', 'vs_champion 56', True),
    60: ('french horn keysplit', 'vs_champion 60', True),
    62: ('trumpet keysplit (no synth-brass sample)', 'vs_champion 56', True),
    73: ('sc88pro_flute', 'vs_champion 73', True),
    80: ('square_1 lead (PSG)', 'vs_champion 82 / vs_frontier_brain 80', False),
    114: ('square_2 bell-like (PSG); alt DS sc88pro_xylophone', 'vs_champion 83 / encounter_champion 13', False),
    'drums': ('rs_drumset: 36 kick, 38 snare, 46 open hat all DS; 49 is EMPTY in rs (remap 49->57 crash)', 'vs_champion 0', True),
}


def plan(path, drop_channels=()):
    fmt, ntr, div, evs = mi.parse(path)
    prog = defaultdict(int)
    active = {}       # (ch, note) -> is_ds
    timeline = []
    for tick, ti, kind, a, data in sorted(evs, key=lambda e: (e[0], 0 if e[2] in (0x80, 0xC0) or (e[2] == 0x90 and e[4][1] == 0) else 1)):
        if kind == 0xC0:
            prog[a] = data[0]
        elif kind in (0x80, 0x90):
            if a in drop_channels:
                continue
            key = (a, data[0])
            if kind == 0x90 and data[1] > 0:
                p = 'drums' if a == 9 else prog[a]
                v = VOICE.get(p)
                active[key] = bool(v and v[2])
            else:
                active.pop(key, None)
            timeline.append((tick, sum(1 for v in active.values() if v), sum(1 for v in active.values() if not v)))
    end = max(e[0] for e in evs)
    over = defaultdict(int)
    peak = (0, 0)
    for (t0, ds, _), (t1, _, _) in zip(timeline, timeline[1:] + [(end, 0, 0)]):
        if ds > 5:
            over[ds] += t1 - t0
        if ds > peak[0]:
            peak = (ds, t0)
    return div, end, peak, over


def main():
    print('### Program -> voice map\n')
    print('| MIDI program | GM | m4a voice | copy from |')
    print('|---|---|---|---|')
    for p, (v, src, ds) in VOICE.items():
        gm = 'drums' if p == 'drums' else mi.GM[p]
        print(f'| {p} | {gm} | {v}{"" if ds is None else (" (DS)" if ds else " (PSG)")} | {src} |')
    for name, drops in (('vs_cynthia.mid', (15,)), ('encounter_cynthia.mid', ())):
        div, end, peak, over = plan(os.path.join(REF, name), drops)
        tot = sum(over.values())
        print(f'\n**{name}** (dropping ch{",".join(str(c + 1) for c in drops) or " none"}): DS peak {peak[0]} notes at bar '
              f'{peak[1] / (div * 4) + 1:.1f}; time with >5 DS notes = {100 * tot / end:.1f}% of the song '
              + ', '.join(f'{k} notes {100 * v / end:.1f}%' for k, v in sorted(over.items())))


if __name__ == '__main__':
    main()
