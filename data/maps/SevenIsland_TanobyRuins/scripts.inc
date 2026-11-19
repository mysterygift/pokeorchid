SevenIsland_TanobyRuins_MapScripts::
# 2 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	map_script MAP_SCRIPT_ON_LOAD, SevenIsland_TanobyRuins_MapScripts_MAP_SCRIPT_ON_LOAD
	.byte 0

SevenIsland_TanobyRuins_MapScripts_MAP_SCRIPT_ON_LOAD:
# 3 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	goto_if_set FLAG_SEVII_TANOBY_OPEN, SevenIsland_TanobyRuins_MapScripts_MAP_SCRIPT_ON_LOAD_1
	return

SevenIsland_TanobyRuins_MapScripts_MAP_SCRIPT_ON_LOAD_1:
# 4 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	setmetatile 120, 10, 0x20A, FALSE
# 5 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	setmetatile 103, 10, 0x20A, FALSE
# 6 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	setmetatile 88, 8, 0x20A, FALSE
# 7 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	setmetatile 44, 11, 0x20A, FALSE
# 8 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	setmetatile 32, 9, 0x20A, FALSE
# 9 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	setmetatile 12, 15, 0x20A, FALSE
# 10 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	setmetatile 11, 6, 0x20A, FALSE
	return


SevenIsland_TanobyRuins_EventScript_Brandon::
# 16 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	trainerbattle_single TRAINER_SEVII_BRANDON, SevenIsland_TanobyRuins_Text_BrandonIntro, SevenIsland_TanobyRuins_Text_BrandonDefeat
# 17 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	msgbox SevenIsland_TanobyRuins_Text_BrandonPost, MSGBOX_AUTOCLOSE
	return


SevenIsland_TanobyRuins_EventScript_Benjamin::
# 33 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	msgbox SevenIsland_TanobyRuins_EventScript_Benjamin_Text_0, MSGBOX_NPC
	return


SevenIsland_TanobyRuins_EventScript_Edna::
# 37 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	msgbox SevenIsland_TanobyRuins_EventScript_Edna_Text_0, MSGBOX_NPC
	return


SevenIsland_TanobyRuins_EventScript_Clifford::
# 41 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	trainerbattle_single TRAINER_SEVII_CLIFFORD, SevenIsland_TanobyRuins_Text_CliffordIntro, SevenIsland_TanobyRuins_Text_CliffordDefeat
# 42 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	msgbox SevenIsland_TanobyRuins_Text_CliffordPost, MSGBOX_AUTOCLOSE
	return


SevenIsland_TanobyRuins_EventScript_Sealed::
# 58 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	goto_if_set FLAG_SEVII_TANOBY_OPEN, SevenIsland_TanobyRuins_EventScript_Sealed_2
# 61 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	msgbox SevenIsland_TanobyRuins_EventScript_Sealed_Text_0, MSGBOX_SIGN
	return

SevenIsland_TanobyRuins_EventScript_Sealed_2:
	end


SevenIsland_TanobyRuins_EventScript_EnterChamber_120_10::
# 67 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	goto_if_set FLAG_SEVII_TANOBY_OPEN, SevenIsland_TanobyRuins_EventScript_EnterChamber_120_10_1
	return

SevenIsland_TanobyRuins_EventScript_EnterChamber_120_10_1:
# 68 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	warp MAP_SEVEN_ISLAND_TANOBY_RUINS_MONEAN_CHAMBER, 0
	return


SevenIsland_TanobyRuins_EventScript_EnterChamber_103_10::
# 73 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	goto_if_set FLAG_SEVII_TANOBY_OPEN, SevenIsland_TanobyRuins_EventScript_EnterChamber_103_10_1
	return

SevenIsland_TanobyRuins_EventScript_EnterChamber_103_10_1:
# 74 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	warp MAP_SEVEN_ISLAND_TANOBY_RUINS_LIPTOO_CHAMBER, 0
	return


SevenIsland_TanobyRuins_EventScript_EnterChamber_88_8::
# 79 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	goto_if_set FLAG_SEVII_TANOBY_OPEN, SevenIsland_TanobyRuins_EventScript_EnterChamber_88_8_1
	return

SevenIsland_TanobyRuins_EventScript_EnterChamber_88_8_1:
# 80 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	warp MAP_SEVEN_ISLAND_TANOBY_RUINS_WEEPTH_CHAMBER, 0
	return


SevenIsland_TanobyRuins_EventScript_EnterChamber_44_11::
# 85 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	goto_if_set FLAG_SEVII_TANOBY_OPEN, SevenIsland_TanobyRuins_EventScript_EnterChamber_44_11_1
	return

SevenIsland_TanobyRuins_EventScript_EnterChamber_44_11_1:
# 86 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	warp MAP_SEVEN_ISLAND_TANOBY_RUINS_DILFORD_CHAMBER, 0
	return


SevenIsland_TanobyRuins_EventScript_EnterChamber_32_9::
# 91 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	goto_if_set FLAG_SEVII_TANOBY_OPEN, SevenIsland_TanobyRuins_EventScript_EnterChamber_32_9_1
	return

SevenIsland_TanobyRuins_EventScript_EnterChamber_32_9_1:
# 92 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	warp MAP_SEVEN_ISLAND_TANOBY_RUINS_SCUFIB_CHAMBER, 0
	return


SevenIsland_TanobyRuins_EventScript_EnterChamber_12_15::
# 97 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	goto_if_set FLAG_SEVII_TANOBY_OPEN, SevenIsland_TanobyRuins_EventScript_EnterChamber_12_15_1
	return

SevenIsland_TanobyRuins_EventScript_EnterChamber_12_15_1:
# 98 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	warp MAP_SEVEN_ISLAND_TANOBY_RUINS_RIXY_CHAMBER, 0
	return


SevenIsland_TanobyRuins_EventScript_EnterChamber_11_6::
# 103 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	goto_if_set FLAG_SEVII_TANOBY_OPEN, SevenIsland_TanobyRuins_EventScript_EnterChamber_11_6_1
	return

SevenIsland_TanobyRuins_EventScript_EnterChamber_11_6_1:
# 104 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	warp MAP_SEVEN_ISLAND_TANOBY_RUINS_VIAPOIS_CHAMBER, 0
	return


SevenIsland_TanobyRuins_EventScript_Benjamin_Text_0:
# 33 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	.string "I've climbed every hill in the Sevii\n"
	.string "Islands. Some twice!$"

SevenIsland_TanobyRuins_EventScript_Edna_Text_0:
# 37 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	.string "I heard strange cries from inside the\n"
	.string "ruins once.$"

SevenIsland_TanobyRuins_EventScript_Sealed_Text_0:
# 61 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	.string "The chamber's entrance is sealed by a\n"
	.string "fall of rock.\n"
	.string "Nothing gets through for now.$"

SevenIsland_TanobyRuins_Text_BrandonIntro::
# 20 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	.string "The ruins hold secrets. You won't take\n"
	.string "them!$"

SevenIsland_TanobyRuins_Text_BrandonDefeat::
# 24 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	.string "Crumbled like old stone.$"

SevenIsland_TanobyRuins_Text_BrandonPost::
# 28 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	.string "I heard strange cries from inside the\n"
	.string "ruins once.$"

SevenIsland_TanobyRuins_Text_CliffordIntro::
# 45 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	.string "A gentleman's battle among the ruins?$"

SevenIsland_TanobyRuins_Text_CliffordDefeat::
# 49 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	.string "Splendid, simply splendid.$"

SevenIsland_TanobyRuins_Text_CliffordPost::
# 53 "data/maps/SevenIsland_TanobyRuins/scripts.pory"
	.string "I've spent my life exploring these\n"
	.string "ruins. The chambers have been closed\l"
	.string "off by rockfalls lately.$"
