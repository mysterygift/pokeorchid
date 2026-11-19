#!/usr/bin/env python3
"""
Imports the user's "Sinjoh Ruins" MIDI (16 channels) as MUS_SINJOH_RUINS for Tanoby Delta.

The BGM player has 10 tracks, so the arrangement is folded to 10 MIDI channels:
  0 lead piano / e. piano      1 e. piano accompaniment (source channels 1 and 2)
  3 e. piano / piano / strings / trumpet                 4 e. piano / piano
  5 piano / trumpet / brass    6 strings / flute         7 harp       8 timpani
  9 drums, plus the "Gunshot" noise part as a closed hi-hat (key 81 -> 42); "Applause" is dropped
 10 strings (source channels 10-13)
Loop markers "[" / "]" move to the conductor track. The voicegroup (sound/voicegroups/sinjoh_ruins.inc)
is General MIDI ordered like Tosa Port's, so each MIDI program maps to its own slot.

usage: <venv>/python dev_scripts/music/import_sinjoh_ruins.py SOURCE.mid   (needs mido)
"""
import os
import sys

import mido

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT_MID = os.path.join(ROOT, "sound", "songs", "midi", "mus_sinjoh_ruins.mid")
OUT_VG = os.path.join(ROOT, "sound", "voicegroups", "sinjoh_ruins.inc")
MERGE = {2: 1, 11: 10, 12: 10, 13: 10, 14: 9}
DROP = {15}
DRUM_KEYS = {(14, 81): 42}
VOICES = {   # GM program -> voice line (others as in Tosa Port's voicegroup)
    4: "\tvoice_keysplit voicegroup_piano_keysplit, keysplit_piano",
    46: "\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_harp, 255, 242, 51, 242",
    47: "\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_timpani, 255, 246, 0, 226",
    61: "\tvoice_keysplit voicegroup_french_horn_keysplit, keysplit_french_horn",
}


def main(src):
    mid = mido.MidiFile(src)
    events = {}                              # out channel -> [(abs time, msg)]
    conductor = []
    for track in mid.tracks:
        now = 0
        for msg in track:
            now += msg.time
            if msg.is_meta:
                if msg.type in ("set_tempo", "time_signature", "key_signature") or \
                        (msg.type == "marker" and msg.text in ("[", "]")):
                    conductor.append((now, msg))
                continue
            if not hasattr(msg, "channel"):
                continue
            ch = msg.channel
            if ch in DROP:
                continue
            out = MERGE.get(ch, ch)
            if out != ch and msg.type == "program_change":
                continue                     # merged parts share the target channel's instrument
            if msg.type in ("note_on", "note_off") and (ch, msg.note) in DRUM_KEYS:
                msg = msg.copy(note=DRUM_KEYS[(ch, msg.note)])
            if msg.type == "control_change" and out != ch:
                continue                     # keep the target channel's own volume / pan
            events.setdefault(out, []).append((now, msg.copy(channel=out)))
    new = mido.MidiFile(type=1, ticks_per_beat=mid.ticks_per_beat)

    def to_track(items, name):
        tr = mido.MidiTrack()
        tr.append(mido.MetaMessage("track_name", name=name, time=0))
        last = 0
        for t, msg in sorted(items, key=lambda e: (e[0], 0 if getattr(e[1], "type", "") == "note_off" or
                                                    (getattr(e[1], "type", "") == "note_on" and e[1].velocity == 0) else 1)):
            tr.append(msg.copy(time=t - last))
            last = t
        tr.append(mido.MetaMessage("end_of_track", time=0))
        return tr

    new.tracks.append(to_track(conductor, "Sinjoh Ruins"))
    for ch in sorted(events):
        new.tracks.append(to_track(events[ch], "ch%d" % ch))
    assert len(events) <= 10, sorted(events)
    new.save(OUT_MID)

    base = open(os.path.join(ROOT, "sound", "voicegroups", "tosa_port.inc")).read().split("\n")
    assert base[0].strip() == "voice_group tosa_port"
    lines = ["voice_group sinjoh_ruins"] + base[1:]
    for prog, line in VOICES.items():
        lines[1 + prog] = line
    open(OUT_VG, "w").write("\n".join(lines))
    print("mus_sinjoh_ruins.mid: %d tracks, channels %s; voicegroup sinjoh_ruins" % (len(new.tracks), sorted(events)))


if __name__ == "__main__":
    main(sys.argv[1])
