"""
Radio song list for import_radio_midi.py / register_songs.py.

song: MUS_* name in lower case (also the .mid / voicegroup name); src: the MIDI file name;
title: radio "now playing" title; station: RADIO_* station.
Optional per-song fixes (keys are source MIDI track numbers, or (track, channel) tuples):
  drop: parts to leave out; merge: [(a, b)] parts to play on one track; voice: {part: VOICES key};
  psg: {part: VOICES key} replaces the automatic square/wave choice; order: track order;
  loop: (start beat, end beat) overrides loop detection; levels: {part: volume factor}.
"""

SINNOH = "RADIO_SINNOH"
UNOVA = "RADIO_UNOVA"

SONGS = [
    # ---- Sinnoh ----
    dict(song="mus_dp_route202", src="Route_202.mid", title="Route 202", station=SINNOH),
    dict(song="mus_dp_route205", src="Pokemon_Diamond_Pearl_Route205.mid", title="Route 205", station=SINNOH),
    dict(song="mus_dp_route209", src="DPPt_-_Route_209.mid", title="Route 209", station=SINNOH),
    dict(song="mus_dp_route216", src="route-216-217.mid", title="Route 216", station=SINNOH),
    dict(song="mus_dp_route228", src="Pokemon_Pearl_Diamond_Route_228.mid", title="Route 228", station=SINNOH),
    dict(song="mus_dp_eterna_night", src="Eterna_City_Night_Pokemon_Diamond_Pearl.mid", title="Eterna City (Night)", station=SINNOH,
         drop=[7]),
    dict(song="mus_dp_hearthome", src="Pokemon DiamondPearlPlatinum - Hearthome City.mid", title="Hearthome City", station=SINNOH),
    dict(song="mus_dp_gts", src="GTS.mid", title="Global Terminal", station=SINNOH),
    dict(song="mus_dp_lake_cavern", src="VerityValorAucityCavern.mid", title="Lake Caverns", station=SINNOH),
    dict(song="mus_dp_underground", src="underground.mid", title="The Underground", station=SINNOH),
    # ---- Unova ----
    dict(song="mus_bw_nuvema", src="Nuvema_Town.mid", title="Nuvema Town", station=UNOVA),
    dict(song="mus_bw_route2", src="2nd_unova_route_theme_2.mid", title="Route 2", station=UNOVA),
    dict(song="mus_bw_castelia", src="hiunmidi.mid", title="Castelia City", station=UNOVA),
    dict(song="mus_bw_driftveil", src="Driftveil_City_BW.mid", title="Driftveil City", station=UNOVA,
         voice={2: "wave_bass", 10: "synbass"}),
    dict(song="mus_bw_route10", src="Route10.mid", title="Route 10", station=UNOVA),
    dict(song="mus_bw_victory_road", src="PKBW_VR_Kio.mid", title="Victory Road", station=UNOVA),
    dict(song="mus_bw_n_castle", src="PokemonBWtwo_NsCastle.mid", title="N's Castle", station=UNOVA,
         voice={1: "sq1_soft", 6: "sq2_soft", 4: "wave_bass"}),
    dict(song="mus_bw_alder", src="PKBW_AL_Kio_V1-1.mid", title="Alder's Theme", station=UNOVA),
    dict(song="mus_bw_cheren", src="CherenBW2.mid", title="Cheren's Theme", station=UNOVA),
    dict(song="mus_bw_white_treehollow", src="White_Tree_Hollow_Entrance.mid", title="White Treehollow", station=UNOVA),
    dict(song="mus_bw_entralink", src="entralink.mid", title="Entralink", station=UNOVA),
]
