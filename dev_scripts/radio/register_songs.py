"""
Registers the radio songs from songs.py (after import_radio_midi.py made their .mid + voicegroup).

Idempotent. For each song not yet registered:
  include/constants/songs.h   MUS_* after the last song; END_MUS and every PH_* move up
  sound/song_table.inc        a BGM entry before the PH_* songs (the index must equal the constant)
  sound/songs/midi/midi.cfg   mid2agb flags (own voicegroup)
  sound/voice_groups.inc      the song's voicegroup (+ voicegroup_radio_gm_drumset once)
  src/debug.c                 the debug sound test list
Then always:
  charmap.txt                 the MUS_* / PH_* / END_MUS block is rebuilt from songs.h (value order),
                              so the {MUS_...} text codes can never drift from the constants again
  src/data/radio_songs.h      the station song lists (radio_stations.h includes it)
Run dev_scripts/radio/song_lengths.py after a build to refresh the intro / loop frame counts.

usage: python3 dev_scripts/radio/register_songs.py
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from songs import SONGS        # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MIDI_FLAGS = "-E -R50 -G_{name} -V090"


def path(*p):
    return os.path.join(ROOT, *p)


def read(p):
    return open(path(p)).read()


def write(p, s):
    open(path(p), "w").write(s)


def songs_h():
    s = read("include/constants/songs.h")
    lines = s.split("\n")
    end_i = next(i for i, l in enumerate(lines) if re.match(r"#define END_MUS\b", l))
    last_i = max(i for i, l in enumerate(lines[:end_i]) if re.match(r"#define MUS_\w+\s+\d+", l))
    last_v = int(lines[last_i].split()[2])
    added = []
    for cfg in SONGS:
        name = cfg["song"].upper()
        if re.search(r"#define %s\b" % name, s):
            continue
        last_v += 1
        last_i += 1
        lines.insert(last_i, "#define %-27s %d" % (name, last_v))
        added.append(name)
    s = "\n".join(lines)
    s = re.sub(r"#define END_MUS(\s+)\d+", lambda m: "#define END_MUS%s%d" % (m.group(1), last_v), s)
    # PH_* follow END_MUS in order
    n = [last_v]

    def ph(m):
        n[0] += 1
        return "#define %s%s%d" % (m.group(1), m.group(2), n[0])
    s = re.sub(r"#define (PH_\w+)(\s+)\d+", ph, s)
    write("include/constants/songs.h", s)
    return added


def song_values():
    vals = {}
    for m in re.finditer(r"#define\s+((?:MUS|PH)_\w+|END_MUS)\s+(\d+)\b", read("include/constants/songs.h")):
        vals[m.group(1)] = int(m.group(2))
    return vals


def charmap():
    """Fix every MUS_* / PH_* / END_MUS value in place; add missing names after their predecessor."""
    vals = song_values()
    lines = read("charmap.txt").split("\n")
    pat = re.compile(r"^((?:MUS|PH)_\w+|END_MUS) = [0-9A-F]{2} [0-9A-F]{2}$")

    def fmt(n):
        return "%s = %02X %02X" % (n, vals[n] & 0xFF, vals[n] >> 8)
    where = {}
    for i, l in enumerate(lines):
        m = pat.match(l)
        if m and m.group(1) in vals:
            lines[i] = fmt(m.group(1))
            where[m.group(1)] = i
    # drop duplicates of END_MUS etc. never happen; insert missing ones in value order
    by_val = sorted(vals, key=lambda n: (vals[n], n.startswith("PH_"), n == "END_MUS"))
    for k, n in enumerate(by_val):
        if n in where:
            continue
        prev = next((by_val[j] for j in range(k - 1, -1, -1) if by_val[j] in where), None)
        at = where[prev] + 1
        # keep END_MUS / PH_TRAP_BLEND after the songs: insert before them if prev is a MUS_
        lines.insert(at, fmt(n))
        for key in where:
            if where[key] >= at:
                where[key] += 1
        where[n] = at
    # END_MUS and the first phoneme belong after the last song
    last_mus = max((where[n] for n in where if n.startswith("MUS_")))
    tail = [n for n in ("END_MUS", by_val[-1] and next(n for n in by_val if n.startswith("PH_"))) if where[n] < last_mus]
    if tail:
        moved = [lines[where[n]] for n in tail]
        for i in sorted((where[n] for n in tail), reverse=True):
            del lines[i]
        last = max(i for i, l in enumerate(lines) if l.startswith("MUS_") and pat.match(l))
        lines[last + 1:last + 1] = moved
    write("charmap.txt", "\n".join(lines))


def insert_after_last(p, line_re, new_lines, before_re=None):
    s = read(p)
    lines = s.split("\n")
    todo = [l for l in new_lines if l not in lines]
    if not todo:
        return
    stop = len(lines)
    if before_re:
        stop = next(i for i, l in enumerate(lines) if re.search(before_re, l))
    i = max(i for i, l in enumerate(lines[:stop]) if re.search(line_re, l))
    lines[i + 1:i + 1] = todo
    write(p, "\n".join(lines))


def tables(added):
    names = [c["song"] for c in SONGS]
    insert_after_last("sound/song_table.inc", r"^\tsong mus_\w+, MUSIC_PLAYER_BGM",
                      ["\tsong %s, MUSIC_PLAYER_BGM, 0" % n for n in names], before_re=r"^\tsong ph_")
    cfg = read("sound/songs/midi/midi.cfg").rstrip("\n").split("\n")
    have = {l.split(":")[0] for l in cfg}
    cfg += ["%s.mid: %s" % (n, MIDI_FLAGS.format(name=n)) for n in names if n + ".mid" not in have]
    write("sound/songs/midi/midi.cfg", "\n".join(cfg) + "\n")
    vg = ['.include "sound/voicegroups/drumsets/radio_gm.inc"'] + \
         ['.include "sound/voicegroups/%s.inc"' % n for n in names]
    s = read("sound/voice_groups.inc").rstrip("\n").split("\n")
    s += [l for l in vg if l not in s]
    write("sound/voice_groups.inc", "\n".join(s) + "\n")
    # debug sound test list: the BGM X-macro list ends with the last song (no trailing backslash)
    d = read("src/debug.c")
    m = re.search(r"#define SOUND_LIST_BGM.*?\n\n", d, re.S)
    block = m.group(0)
    have = set(re.findall(r"X\((MUS_\w+)\)", block))
    new = [n.upper() for n in names if n.upper() not in have]
    if new:
        body = block.rstrip("\n")
        body = body + " \\\n" + " \\\n".join("    X(%s)" % n for n in new)
        d = d.replace(block, body + "\n\n")
        write("src/debug.c", d)


def radio_songs():
    out = ["// Generated by dev_scripts/radio/register_songs.py from dev_scripts/radio/songs.py. Do not edit.",
           "// (MIDIs converted by import_radio_midi.py; lengths in radio_song_lengths.h)", ""]
    stations = []
    for cfg in SONGS:
        if cfg["station"] not in stations:
            stations.append(cfg["station"])
    for st in stations:
        var = "sSongs_" + st.split("_", 1)[1].title().replace("_", "")
        out.append("static const struct RadioSong %s[] =" % var)
        out.append("{")
        for cfg in SONGS:
            if cfg["station"] == st:
                out.append('    RADIO_SONG(%s, "%s"),' % (cfg["song"].upper(), cfg["title"]))
        out.append("};")
        out.append("")
    write("src/data/radio_songs.h", "\n".join(out))


def main():
    added = songs_h()
    tables(added)
    charmap()
    radio_songs()
    print("added %d songs: %s" % (len(added), ", ".join(added)))


if __name__ == "__main__":
    main()
