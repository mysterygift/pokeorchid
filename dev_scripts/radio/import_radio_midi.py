"""
Radio MIDI importer: turns General MIDI rips into Gen 3 m4a-ready MIDIs plus a voicegroup each.

For every song in songs.py:
  * notes are grouped per (MIDI track, channel); exact duplicate parts are dropped and, if more than
    10 remain (the BGM player has 10 tracks), parts sharing a Gen 3 voice are merged;
  * CC11 expression is folded into CC7 volume (mid2agb ignores CC11); RPN pitch-bend range becomes
    CC20 (BENDR); every other controller is dropped (mid2agb gives several CCs m4a meanings);
  * GM programs map to vanilla Gen 3 instruments (VOICES below, envelopes copied from vanilla
    voicegroups). Up to two monophonic lead parts go to the square channels and one bass part to the
    wave channel, as the vanilla route themes do, so the 5 DirectSound channels are left for strings,
    piano and drums. GM drums (channel 10) use voicegroup_radio_gm_drumset (GM key layout);
  * the loop is the song's own repeat: either loop markers in the file, or the longest stretch that
    repeats note-for-note. Everything after the first repeat is cut and '[' / ']' markers are written,
    which mid2agb turns into the GOTO loop the radio counts (dev_scripts/radio/song_lengths.py).

Writes sound/songs/midi/<song>.mid and sound/voicegroups/<song>.inc and prints a report (track plan,
loop, DirectSound polyphony). Registering the songs (songs.h, song_table.inc, midi.cfg, ...) is
register_songs.py.

usage: python3 dev_scripts/radio/import_radio_midi.py [song ...]   (source MIDIs: dev_scripts/radio/midi_src/)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from midilib import Midi       # noqa: E402
from songs import SONGS        # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FILLER = "voice_square_1 60, 0, 0, 2, 0, 0, 15, 0"


def ds(sample, a, d, s, r, key=60):
    return "voice_directsound %d, 0, DirectSoundWaveData_%s, %d, %d, %d, %d" % (key, sample, a, d, s, r)


def ks(name):
    return "voice_keysplit voicegroup_%s_keysplit, keysplit_%s" % (name, name)


VOICES = {
    "piano": ks("piano"),
    "epiano": ds("sd90_classical_detuned_ep1_low", 255, 188, 128, 226),
    "strings": ks("strings"),
    "pizz": ds("sc88pro_pizzicato_strings", 255, 216, 0, 165),
    "harp": ds("sc88pro_harp", 255, 242, 51, 242),
    "timpani": ds("sc88pro_timpani", 255, 246, 0, 226),
    "trumpet": ks("trumpet"),
    "horn": ks("french_horn"),
    "tuba": ks("tuba"),
    "flute": ds("sc88pro_flute", 255, 127, 231, 127),
    "oboe": ds("sd90_classical_oboe", 255, 165, 154, 127),
    "shaku": ds("sd90_classical_shakuhachi", 255, 0, 255, 204),
    "whistle": ds("sd90_classical_whistle", 255, 0, 255, 127),
    "glock": ds("sc88pro_glockenspiel", 255, 165, 51, 242),
    "xylo": ds("sc88pro_xylophone", 255, 235, 0, 204),
    "tbell": ds("sc88pro_tubular_bell", 255, 165, 90, 216),
    "organ": ds("sc88pro_organ2", 255, 0, 255, 210),
    "church": ds("sc88pro_church_organ3_low", 255, 76, 154, 188),
    "accordion": ds("sc88pro_accordion", 255, 0, 255, 165),
    "nylon": ds("sc88pro_nylon_str_guitar", 255, 249, 25, 76),
    "overdrive": ds("sd90_classical_overdrive_guitar", 255, 0, 255, 127),
    "distortion": ds("sd90_classical_distortion_guitar_low", 255, 0, 255, 127),
    "fbass": ds("sc88pro_fingered_bass", 255, 253, 0, 149),
    "fretless": ds("sc88pro_fretless_bass", 255, 253, 0, 188),
    "slap": ds("sc88pro_slap_bass", 255, 235, 128, 99),
    "synbass": ds("sc88pro_synth_bass", 255, 252, 0, 115),
    "choir": ds("classical_choir_voice_ahhs", 255, 0, 255, 165),
    "taiko": ds("sc88pro_taiko", 255, 0, 255, 0),
    "tom": ds("unused_sc55_tom", 255, 210, 77, 204),
    "koto": ds("unknown_koto_low", 255, 0, 206, 242),
    "dsquare": ds("sc88pro_square_wave", 255, 0, 255, 127),
    "crash": ds("sc88pro_orchestra_cymbal_crash", 255, 246, 0, 216),
    "wind": ds("sc88pro_wind", 255, 0, 255, 127),
    "woodblock": ds("ethnic_flavours_hyoushigi", 255, 0, 206, 0),
    # PSG voices (two square channels, one wave channel)
    "sq1": "voice_square_1_alt 60, 0, 0, 2, 0, 1, 9, 1",
    "sq2": "voice_square_2_alt 60, 0, 2, 0, 1, 9, 1",
    "sq1_soft": "voice_square_1_alt 60, 0, 0, 1, 0, 1, 7, 1",
    "sq2_soft": "voice_square_2_alt 60, 0, 1, 0, 1, 7, 1",
    "sq1_pluck": "voice_square_1_alt 60, 0, 0, 2, 0, 2, 3, 1",
    "sq2_pluck": "voice_square_2_alt 60, 0, 2, 0, 2, 3, 1",
    "wave_bass": "voice_programmable_wave_alt 60, 0, ProgrammableWaveData_2, 0, 7, 15, 1",
    "wave_lead": "voice_programmable_wave_alt 60, 0, ProgrammableWaveData_1, 0, 7, 15, 1",
    "wave_reed": "voice_programmable_wave_alt 60, 0, ProgrammableWaveData_7, 0, 7, 15, 1",
    "drums": "voice_keysplit_all voicegroup_radio_gm_drumset",
}
# one-shot / decaying instruments: notes longer than this (beats) only hold a DirectSound channel
PLUCK_CAP = {"piano": 2, "epiano": 2, "harp": 2, "nylon": 2, "tbell": 2, "koto": 2, "timpani": 1.5,
             "pizz": 1, "xylo": 1, "glock": 1, "drums": 1.5, "taiko": 1, "tom": 1, "woodblock": 0.5}
PSG = {"sq1": 1, "sq2": 2, "sq1_soft": 1, "sq2_soft": 2, "sq1_pluck": 1, "sq2_pluck": 2,
       "wave_bass": 3, "wave_lead": 3, "wave_reed": 3}


def gm_voice(p):
    table = [
        (0, 3, "piano"), (4, 5, "epiano"), (6, 7, "piano"), (8, 10, "glock"), (11, 13, "xylo"),
        (14, 14, "tbell"), (15, 15, "harp"), (16, 18, "organ"), (19, 20, "church"), (21, 23, "accordion"),
        (24, 28, "nylon"), (29, 29, "overdrive"), (30, 30, "distortion"), (31, 31, "overdrive"),
        (32, 34, "fbass"), (35, 35, "fretless"), (36, 37, "slap"), (38, 39, "synbass"),
        (40, 44, "strings"), (45, 45, "pizz"), (46, 46, "harp"), (47, 47, "timpani"),
        (48, 51, "strings"), (52, 54, "choir"), (55, 55, "strings"), (56, 56, "trumpet"), (57, 57, "horn"),
        (58, 58, "tuba"), (59, 59, "trumpet"), (60, 60, "horn"), (61, 63, "trumpet"),
        (64, 71, "oboe"), (72, 76, "flute"), (77, 77, "shaku"), (78, 78, "whistle"), (79, 79, "flute"),
        (80, 87, "dsquare"), (88, 90, "strings"), (91, 91, "choir"), (92, 103, "strings"),
        (104, 106, "nylon"), (107, 107, "koto"), (108, 108, "xylo"), (109, 109, "oboe"), (110, 110, "strings"),
        (111, 111, "oboe"), (112, 113, "glock"), (114, 114, "xylo"), (115, 115, "woodblock"),
        (116, 116, "taiko"), (117, 118, "tom"), (119, 119, "crash"), (120, 120, "nylon"), (121, 122, "wind"),
        (123, 127, "glock"),
    ]
    for lo, hi, v in table:
        if lo <= p <= hi:
            return v
    return "piano"


# GM families that may move to a square channel (leads), in preference order
SQUARE_FAMILY = [(80, 87), (64, 67), (71, 71), (68, 70), (72, 79), (16, 23), (8, 10)]
BASS_FAMILY = (32, 39)


def family_rank(p, fams):
    for i, (lo, hi) in enumerate(fams):
        if lo <= p <= hi:
            return i
    return None


class Part:
    """One (source track, channel) note stream with its controllers."""

    def __init__(self, src, ch, name):
        self.src = src
        self.ch = ch
        self.name = name
        self.notes = []
        self.ctl = []       # events: prog / cc / bend
        self.drum = ch == 9

    def progs(self):
        return [e["prog"] for e in self.ctl if e["kind"] == "prog"]

    def main_prog(self):
        # program in force for most notes
        cur = 0
        counts = {}
        ps = sorted([e for e in self.ctl if e["kind"] == "prog"], key=lambda e: e["t"])
        j = 0
        for n in self.notes:
            while j < len(ps) and ps[j]["t"] <= n["t"]:
                cur = ps[j]["prog"]
                j += 1
            counts[cur] = counts.get(cur, 0) + 1
        return max(counts, key=counts.get) if counts else (ps[0]["prog"] if ps else 0)

    def poly_stats(self, notes=None):
        notes = notes if notes is not None else self.notes
        pts = sorted([(n["t"], 1) for n in notes] + [(n["t"] + n["dur"], -1) for n in notes])
        cur = mx = 0
        over = 0
        last = 0
        for t, d in pts:
            if cur > 1:
                over += t - last
            last = t
            cur += d
            mx = max(mx, cur)
        span = max(1, (pts[-1][0] - pts[0][0])) if pts else 1
        return mx, over / span


def load_parts(m):
    parts = []
    for ti, tr in enumerate(m.tracks):
        name = next((e["data"].decode("latin-1") for e in tr if e["kind"] == "meta" and e["type"] == 3), "")
        by = {}
        for e in tr:
            if e["kind"] in ("note", "prog", "cc", "bend"):
                p = by.get(e["ch"])
                if p is None:
                    p = by[e["ch"]] = Part(ti, e["ch"], name)
                (p.notes if e["kind"] == "note" else p.ctl).append(e)
        parts += [p for p in by.values() if p.notes]
    return parts


def tempo_and_meta(m):
    out = []
    for _, e in m.all_events():
        if e["kind"] == "meta" and e["type"] in (0x51, 0x58):
            out.append(e)
    out.sort(key=lambda e: e["t"])
    # collapse duplicate tempo events at the same tick (keep the last)
    res = {}
    for e in out:
        res[(e["t"], e["type"])] = e
    return sorted(res.values(), key=lambda e: e["t"])


def markers(m):
    return [(e["t"], e["data"].decode("latin-1").strip().lower()) for _, e in m.all_events()
            if e["kind"] == "meta" and e["type"] in (1, 6)]


def detect_loop(parts, ppqn, end):
    """Longest L such that some window [S+L, S+2L) repeats [S, S+L) note for note; minimal S."""
    q = max(1, ppqn // 12)
    keyset = set()
    allnotes = []
    for i, p in enumerate(parts):
        for n in p.notes:
            k = (round(n["t"] / q), n["key"], i)
            keyset.add(k)
            allnotes.append(k)
    if not allnotes:
        return None
    nbeats = end // ppqn + 2
    best = None
    for Lb in range(nbeats // 2, 7, -1):
        L = Lb * ppqn
        Lq = round(L / q)
        tot = [0] * (nbeats + 1)
        hit = [0] * (nbeats + 1)
        for (tq, key, i) in allnotes:
            t = tq * q
            if t < L:
                continue
            b = int(t // ppqn)
            tot[b] += 1
            if (tq - Lq, key, i) in keyset or (tq - Lq - 1, key, i) in keyset or (tq - Lq + 1, key, i) in keyset:
                hit[b] += 1
        # prefix sums
        pt = [0]
        ph = [0]
        for b in range(nbeats + 1):
            pt.append(pt[-1] + tot[b])
            ph.append(ph[-1] + hit[b])
        for Sb in range(0, nbeats - 2 * Lb + 2):
            a, z = Sb + Lb, min(nbeats, Sb + 2 * Lb)
            if z - a < Lb - 1:
                continue
            n = pt[z] - pt[a]
            if n < 16:
                continue
            if (ph[z] - ph[a]) / n >= 0.96:
                best = (Sb * ppqn, L)
                break
        if best:
            return best
    return None


def bar_ticks(m):
    for e in tempo_and_meta(m):
        if e["type"] == 0x58:
            num, den = e["data"][0], 2 ** e["data"][1]
            return int(m.ppqn * 4 * num / den)
    return m.ppqn * 4


def vol_events(part):
    """CC7 x CC11 / 127 at each change; RPN bend range -> CC20; pan kept."""
    out = []
    vol, expr = 100, 127
    rpn = [127, 127]
    for e in sorted(part.ctl, key=lambda e: e["t"]):
        if e["kind"] == "prog":
            out.append(dict(e))
        elif e["kind"] == "bend":
            out.append(dict(e))
        else:
            c, v = e["cc"], e["val"]
            if c == 7:
                vol = v
                out.append(dict(t=e["t"], kind="vol", val=vol * expr // 127))
            elif c == 11:
                expr = v
                out.append(dict(t=e["t"], kind="vol", val=vol * expr // 127))
            elif c == 10:
                out.append(dict(t=e["t"], kind="cc", cc=10, val=v))
            elif c == 101:
                rpn[0] = v
            elif c == 100:
                rpn[1] = v
            elif c == 6 and rpn == [0, 0]:
                out.append(dict(t=e["t"], kind="cc", cc=20, val=v))
    return out


def level_at(evs, t, default=100):
    lv = default
    for e in evs:
        if e["kind"] == "vol" and e["t"] <= t:
            lv = e["val"]
    return lv


def convert(cfg, midi_dir, verbose=True):
    m = Midi.load(os.path.join(midi_dir, cfg["src"]))
    parts = load_parts(m)
    rep = []
    # drop parts explicitly, then exact duplicates
    drop = set(cfg.get("drop", []))
    parts = [p for p in parts if (p.src, p.ch) not in drop and p.src not in drop]
    seen = {}
    uniq = []
    for p in parts:
        sig = tuple((n["t"], n["key"]) for n in p.notes)
        if sig in seen:
            rep.append("  dup  tr%d ch%d = tr%d ch%d (dropped)" % (p.src, p.ch, seen[sig].src, seen[sig].ch))
            continue
        seen[sig] = p
        uniq.append(p)
    parts = uniq
    for p in parts:
        p.evs = vol_events(p)
        p.prog = p.main_prog()
        p.voice = "drums" if p.drum else gm_voice(p.prog)
        p.mx, p.over = p.poly_stats()
    for key, v in cfg.get("voice", {}).items():
        for p in parts:
            if (p.src, p.ch) == key or p.src == key:
                p.voice = v
                p.forced = True

    # merge down to 10 output tracks
    groups = [[p] for p in parts]
    for a, b in cfg.get("merge", []):
        ga = next(g for g in groups if any((p.src, p.ch) == a or p.src == a for p in g))
        gb = next(g for g in groups if any((p.src, p.ch) == b or p.src == b for p in g))
        if ga is not gb:
            ga += gb
            groups.remove(gb)
    while len(groups) > 10:
        best = None
        for i in range(len(groups)):
            for j in range(i + 1, len(groups)):
                gi, gj = groups[i], groups[j]
                if gi[0].voice != gj[0].voice or gi[0].drum != gj[0].drum:
                    continue
                notes = [n for p in gi + gj for n in p.notes]
                mx, over = gi[0].poly_stats(notes)
                score = over + mx * 0.01
                if best is None or score < best[0]:
                    best = (score, i, j)
        if best is None:
            # merge the two smallest parts regardless of voice (smaller one takes the other's voice)
            groups.sort(key=lambda g: sum(len(p.notes) for p in g))
            best = (0, 0, 1)
        _, i, j = best
        rep.append("  merge %s + %s" % (["tr%d" % p.src for p in groups[i]], ["tr%d" % p.src for p in groups[j]]))
        groups[i] += groups[j]
        del groups[j]

    # PSG assignment
    def mono(g):
        mx, over = g[0].poly_stats([n for p in g for n in p.notes])
        return over < 0.03
    psg_cfg = cfg.get("psg")
    if psg_cfg is None:
        free_sq = ["sq1", "sq2"]
        wave_used = False
        for g in groups:
            if any(getattr(p, "forced", False) for p in g):
                v = g[0].voice
                if v in PSG:
                    if PSG[v] == 3:
                        wave_used = True
                    elif v.replace("_soft", "").replace("_pluck", "") in free_sq:
                        free_sq.remove(v.replace("_soft", "").replace("_pluck", ""))
        # bass -> wave
        if not wave_used:
            cands = [g for g in groups if not g[0].drum and len(g) == 1 and not getattr(g[0], "forced", False)
                     and family_rank(g[0].prog, [BASS_FAMILY]) is not None and mono(g)]
            if cands:
                g = max(cands, key=lambda g: len(g[0].notes))
                g[0].voice = "wave_bass"
        # leads -> squares
        cands = []
        for g in groups:
            p = g[0]
            if p.drum or len(g) > 1 or getattr(p, "forced", False) or p.voice in PSG:
                continue
            r = family_rank(p.prog, SQUARE_FAMILY)
            if len(set(gm_voice(x) for x in p.progs())) > 1:
                continue
            if r is None or not mono(g):
                continue
            cands.append((r, -len(p.notes), id(g), g))
        cands.sort()
        for _, _, _, g in cands[:len(free_sq)]:
            sq = free_sq.pop(0)
            r = family_rank(g[0].prog, SQUARE_FAMILY)
            g[0].voice = sq + ("_pluck" if r == 6 else "_soft" if r in (3, 4) else "")
    else:
        for key, v in psg_cfg.items():
            for g in groups:
                if any((p.src, p.ch) == key or p.src == key for p in g):
                    for p in g:
                        p.voice = v

    # order: as listed in cfg["order"] (source tracks), else PSG leads, melodic, bass, drums last
    def okey(g):
        p = g[0]
        if "order" in cfg and p.src in cfg["order"]:
            return (-1, cfg["order"].index(p.src))
        if p.drum:
            return (3, 0)
        if p.voice in PSG and PSG[p.voice] < 3:
            return (0, p.src)
        if p.voice.startswith("wave"):
            return (2, p.src)
        return (1, p.src)
    groups.sort(key=okey)

    # loop
    end = m.end_tick()
    bar = bar_ticks(m)
    mk = markers(m)
    loop = None
    lb = [t for t, s in mk if s in ("[", "loopstart", "begin loop", "loop start")]
    le = [t for t, s in mk if s in ("]", "loopend", "end loop", "loop end")]
    if "loop" in cfg:
        loop = (round(cfg["loop"][0] * m.ppqn), round((cfg["loop"][1] - cfg["loop"][0]) * m.ppqn))
        how = "config"
    elif lb and le:
        loop = (lb[0], le[0] - lb[0])
        how = "markers"
    else:
        loop = detect_loop([p for g in groups for p in g], m.ppqn, end)
        how = "repeat"
        if loop is None:
            first = min(n["t"] for g in groups for p in g for n in p.notes)
            last = max(n["t"] + n["dur"] for g in groups for p in g for n in p.notes)
            e2 = -(-last // bar) * bar
            loop = (first // bar * bar, e2 - first // bar * bar)
            how = "whole song"
    S, L = loop
    E = S + L

    # build output
    out = Midi()
    out.ppqn = m.ppqn
    cond = [dict(e) for e in tempo_and_meta(m) if e["t"] < E]
    cond.append(dict(t=S, kind="meta", type=6, data=b"["))
    cond.append(dict(t=E, kind="meta", type=6, data=b"]"))
    out.tracks.append(cond)
    slots = {}          # voice line -> program slot
    drum_slot = None
    tracks_rep = []
    ds_notes = []
    psg_scale = cfg.get("psg_level", 0.7)
    for ti, g in enumerate(groups):
        ch = ti
        tr = []
        single = len(g) == 1
        voice_for = {}

        def slot_for(v):
            line = VOICES[v]
            if line not in slots:
                slots[line] = len(slots)
            return slots[line]
        notes = []
        for p in g:
            for n in p.notes:
                if n["t"] >= E:
                    continue
                n2 = dict(n)
                n2["ch"] = ch
                n2["dur"] = min(n2["dur"], E - n2["t"])
                cap = PLUCK_CAP.get(p.voice)
                if cap and not cfg.get("no_cap"):
                    n2["dur"] = min(n2["dur"], int(cap * m.ppqn))
                if n2["dur"] <= 0:
                    continue
                if not single:      # bake the part's volume into velocity
                    n2["vel"] = max(1, min(127, n2["vel"] * level_at(p.evs, n["t"]) // 100))
                n2["_p"] = p
                notes.append(n2)
        p0 = g[0]
        base_voice = p0.voice
        # program changes inside a single part keep their own GM mapping unless forced/PSG
        prog_evs = []
        if single and not p0.drum and base_voice not in PSG and not getattr(p0, "forced", False):
            for e in p0.evs:
                if e["kind"] == "prog" and e["t"] < E:
                    prog_evs.append((e["t"], gm_voice(e["prog"])))
        if not prog_evs or prog_evs[0][0] > min(n["t"] for n in notes):
            prog_evs.insert(0, (0, base_voice))
        cur_voice = None
        state_at_S = {}
        for t, v in prog_evs:
            if v != cur_voice:
                tr.append(dict(t=t, kind="prog", ch=ch, prog=slot_for(v)))
                cur_voice = v
            if t <= S:
                state_at_S["prog"] = slot_for(v)
        level = 1.0
        if base_voice in PSG:
            level = psg_scale
        level *= cfg.get("levels", {}).get(p0.src, 1.0)
        if single:
            vol0 = 100
            for e in p0.evs:
                if e["t"] >= E:
                    continue
                if e["kind"] == "vol":
                    v = max(0, min(127, round(e["val"] * level)))
                    tr.append(dict(t=e["t"], kind="cc", ch=ch, cc=7, val=v))
                    if e["t"] <= S:
                        state_at_S["vol"] = v
                elif e["kind"] == "cc":
                    tr.append(dict(t=e["t"], kind="cc", ch=ch, cc=e["cc"], val=e["val"]))
                    if e["t"] <= S and e["cc"] == 10:
                        state_at_S["pan"] = e["val"]
                elif e["kind"] == "bend":
                    tr.append(dict(t=e["t"], kind="bend", ch=ch, val=e["val"]))
                    if e["t"] <= S:
                        state_at_S["bend"] = e["val"]
            if not any(e["kind"] == "cc" and e["cc"] == 7 for e in tr):
                v = round(vol0 * level)
                tr.append(dict(t=0, kind="cc", ch=ch, cc=7, val=v))
                state_at_S["vol"] = v
        else:
            v = round(100 * level)
            tr.append(dict(t=0, kind="cc", ch=ch, cc=7, val=v))
            state_at_S["vol"] = v
        # restate the loop-start state so the GOTO comes back to the right voice / volume
        if S > 0:
            if "prog" in state_at_S:
                tr.append(dict(t=S, kind="prog", ch=ch, prog=state_at_S["prog"]))
            if "vol" in state_at_S:
                tr.append(dict(t=S, kind="cc", ch=ch, cc=7, val=state_at_S["vol"]))
            tr.append(dict(t=S, kind="cc", ch=ch, cc=10, val=state_at_S.get("pan", 64)))
            if any(e["kind"] == "bend" for e in tr):
                tr.append(dict(t=S, kind="bend", ch=ch, val=state_at_S.get("bend", 8192)))
        for n in notes:
            n.pop("_p", None)
        tr += notes
        tr.sort(key=lambda e: e["t"])
        out.tracks.append(tr)
        if base_voice not in PSG:
            ds_notes += notes
        mx, over = p0.poly_stats(notes) if notes else (0, 0)
        tracks_rep.append("  T%-2d %-10s <- %s%s" % (
            ti + 1, base_voice, ", ".join("tr%d/ch%d %s(p%d)" % (p.src, p.ch + 1, p.name[:14], p.prog) for p in g),
            "  poly %d" % mx))

    # voicegroup
    vg_lines = [FILLER] * len(slots)
    for line, sl in slots.items():
        vg_lines[sl] = line
    name = cfg["song"]
    vg = "voice_group %s\n" % name + "".join("\t%s\n" % l for l in vg_lines)

    # DirectSound polyphony (tracks not on PSG)
    pts = sorted([(n["t"], 1) for n in ds_notes] + [(n["t"] + n["dur"], -1) for n in ds_notes])
    cur = mx = 0
    over5 = 0
    last = 0
    for t, d in pts:
        if cur > 5:
            over5 += t - last
        last = t
        cur += d
        mx = max(mx, cur)
    if verbose:
        print("== %s  (%s)" % (name, cfg["src"]))
        for r in rep:
            print(r)
        for r in tracks_rep:
            print(r)
        print("  loop %s: start beat %.2f, length %.2f beats (song %.1f beats)  DS poly max %d, >5 for %.0f%%"
              % (how, S / m.ppqn, L / m.ppqn, end / m.ppqn, mx, 100 * over5 / max(1, E)))
    return out, vg


# GM percussion key -> (drumset file, key in that kit), built from the RS and FRLG kits.
# RS has real hi-hats and toms, FRLG has the crash / ride / cowbell / triangle the RS kit lacks.
GM_DRUMS = {
    35: ("rs", 36), 36: ("rs", 36), 37: ("emerald_1", 75), 38: ("rs", 38), 39: ("rs", 39), 40: ("rs", 40),
    41: ("rs", 41), 42: ("rs", 42), 43: ("rs", 43), 44: ("rs", 42), 45: ("rs", 45), 46: ("rs", 46),
    47: ("rs", 47), 48: ("rs", 48), 49: ("frlg", 49), 50: ("rs", 50), 51: ("frlg", 53), 52: ("frlg", 52),
    53: ("frlg", 53), 54: ("rs", 54), 55: ("rs", 55), 56: ("frlg", 56), 57: ("rs", 57), 58: ("frlg", 57),
    59: ("frlg", 59), 60: ("frlg", 62), 61: ("frlg", 64), 62: ("frlg", 62), 63: ("frlg", 63),
    64: ("frlg", 64), 65: ("rs", 48), 66: ("rs", 47), 67: ("frlg", 86), 68: ("frlg", 86), 69: ("rs", 42),
    70: ("rs", 42), 75: ("emerald_1", 75), 76: ("emerald_1", 75), 77: ("emerald_1", 75),
    80: ("frlg", 80), 81: ("frlg", 81), 82: ("rs", 42), 83: ("frlg", 83),
}


def make_drumset():
    kits = {}
    for k in ("rs", "frlg", "emerald_1"):
        lines = open(os.path.join(ROOT, "sound", "voicegroups", "drumsets", k + ".inc")).read().split("\n")
        start = int(lines[0].split(",")[1])
        kits[k] = (start, [l.strip() for l in lines[1:] if l.strip()])
    out = ["@ GM percussion layout for the radio imports (dev_scripts/radio/import_radio_midi.py)",
           "voice_group radio_gm_drumset, 35"]
    for key in range(35, 84):
        line = FILLER
        if key in GM_DRUMS:
            kit, k2 = GM_DRUMS[key]
            start, ls = kits[kit]
            cand = ls[k2 - start]
            if "DirectSoundWaveData" in cand:
                line = cand
        out.append("\t" + line)
    open(os.path.join(ROOT, "sound", "voicegroups", "drumsets", "radio_gm.inc"), "w").write("\n".join(out) + "\n")


def main():
    make_drumset()
    midi_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi_src")
    only = set(sys.argv[1:])
    for cfg in SONGS:
        if only and cfg["song"] not in only:
            continue
        out, vg = convert(cfg, midi_dir)
        out.save(os.path.join(ROOT, "sound", "songs", "midi", cfg["song"] + ".mid"))
        open(os.path.join(ROOT, "sound", "voicegroups", cfg["song"] + ".inc"), "w").write(vg)


if __name__ == "__main__":
    main()
