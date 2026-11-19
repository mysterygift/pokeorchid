"""Write the GM-numbered voicegroups for the two Cynthia songs (slot = General MIDI program).

    python3 dev_scripts/voyages/trainers/gen_cynthia_voicegroups.py

Every voice is copied from a vanilla voicegroup (noted per slot); unused slots hold the usual square filler.
"""
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
FILL = 'voice_square_1 60, 0, 0, 2, 0, 0, 15, 0'

VS = {
    0: 'voice_keysplit_all voicegroup_rs_drumset',                                                   # vs_champion 0
    1: 'voice_keysplit voicegroup_piano_keysplit, keysplit_piano',                                   # vs_champion 1
    30: 'voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_distortion_guitar_high, 255, 165, 154, 165',  # vs_frontier_brain 30
    38: 'voice_programmable_wave_alt 60, 0, ProgrammableWaveData_7, 0, 7, 15, 2',                    # synth bass on the wave channel (vs_champion 81)
    44: 'voice_keysplit voicegroup_strings_keysplit, keysplit_strings',                              # tremolo strings -> strings (vs_champion 48)
    47: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_timpani, 255, 246, 0, 226',            # vs_champion 47
    48: 'voice_keysplit voicegroup_strings_keysplit, keysplit_strings',                              # vs_champion 48
    52: 'voice_directsound 60, 0, DirectSoundWaveData_classical_choir_voice_ahhs, 255, 0, 255, 0',   # rg_vs_champion 52
    60: 'voice_keysplit voicegroup_french_horn_keysplit, keysplit_french_horn',                      # vs_champion 60
    62: 'voice_keysplit voicegroup_trumpet_keysplit, keysplit_trumpet',                              # synth brass -> trumpet (vs_champion 56)
    73: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_flute, 255, 0, 255, 165',              # vs_champion 73
    80: 'voice_square_1 60, 0, 0, 2, 0, 1, 7, 1',                                                    # square lead, square channel 1 (vs_champion 82)
    82: 'voice_square_2 60, 0, 2, 0, 1, 7, 1',                                                       # 2nd square lead, square channel 2 (vs_champion 80)
    114: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_xylophone, 255, 235, 0, 204',         # steel drums -> xylophone (encounter_champion 13)
}
ENCOUNTER = {
    0: 'voice_keysplit voicegroup_piano_keysplit, keysplit_piano',                                   # grand piano (vs_champion 1)
}


def write(name, slots):
    lines = [f'voice_group {name}'] + ['\t' + slots.get(i, FILL) for i in range(128)]
    open(os.path.join(ROOT, 'sound', 'voicegroups', name + '.inc'), 'w').write('\n'.join(lines) + '\n')


if __name__ == '__main__':
    write('mus_orchid_vs_cynthia', VS)
    write('mus_orchid_encounter_cynthia', ENCOUNTER)
    print('ok')
