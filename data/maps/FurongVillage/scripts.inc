# 1 "data/maps/FurongVillage/scripts.pory"

# 2 "data/maps/FurongVillage/scripts.pory"
FurongVillage_MapScripts::
# 3 "data/maps/FurongVillage/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, FurongVillage_OnTransition
# 4 "data/maps/FurongVillage/scripts.pory"
	.byte 0
# 5 "data/maps/FurongVillage/scripts.pory"

# 6 "data/maps/FurongVillage/scripts.pory"
FurongVillage_OnTransition:
# 7 "data/maps/FurongVillage/scripts.pory"
	setflag FLAG_VISITED_FURONG_VILLAGE
# 8 "data/maps/FurongVillage/scripts.pory"
	end
# 9 "data/maps/FurongVillage/scripts.pory"

# 10 "data/maps/FurongVillage/scripts.pory"
FurongVillage_EventScript_Sign0::
# 11 "data/maps/FurongVillage/scripts.pory"
	msgbox FurongVillage_Text_Sign0, MSGBOX_SIGN
# 12 "data/maps/FurongVillage/scripts.pory"
	end
# 13 "data/maps/FurongVillage/scripts.pory"

# 14 "data/maps/FurongVillage/scripts.pory"
FurongVillage_Text_Sign0:
# 15 "data/maps/FurongVillage/scripts.pory"
	.string "FURONG VILLAGE\n"
# 16 "data/maps/FurongVillage/scripts.pory"
	.string "A fishing village on TIKSI's shore.$"

FurongVillage_EventScript_TiksiNpc1::
# 23 "data/maps/FurongVillage/scripts.pory"
	msgbox FurongVillage_EventScript_TiksiNpc1_Text_0, MSGBOX_NPC
	return


FurongVillage_EventScript_TiksiNpc2::
# 27 "data/maps/FurongVillage/scripts.pory"
	msgbox FurongVillage_EventScript_TiksiNpc2_Text_0, MSGBOX_NPC
	return


FurongVillage_EventScript_TiksiNpc3::
# 31 "data/maps/FurongVillage/scripts.pory"
	msgbox FurongVillage_EventScript_TiksiNpc3_Text_0, MSGBOX_NPC
	return


FurongVillage_EventScript_TiksiGuardianGavaniPath::
# 35 "data/maps/FurongVillage/scripts.pory"
	msgbox FurongVillage_EventScript_TiksiGuardianGavaniPath_Text_0, MSGBOX_NPC
	return


FurongVillage_EventScript_TiksiNpc1_Text_0:
# 23 "data/maps/FurongVillage/scripts.pory"
	.string "A boat from Tosa? We don't get many of\n"
	.string "those. Not legal ones, anyhow.$"

FurongVillage_EventScript_TiksiNpc2_Text_0:
# 27 "data/maps/FurongVillage/scripts.pory"
	.string "Tiksi is a hard land. The sea feeds us\n"
	.string "and the mountain watches over us.$"

FurongVillage_EventScript_TiksiNpc3_Text_0:
# 31 "data/maps/FurongVillage/scripts.pory"
	.string "Are you from Tosa? Grandpa says Tosa\n"
	.string "people are soft. You look all right to\l"
	.string "me.$"

FurongVillage_EventScript_TiksiGuardianGavaniPath_Text_0:
# 35 "data/maps/FurongVillage/scripts.pory"
	.string "I am the guardian of Gavani Path. The\n"
	.string "thunder giant has come home to its\l"
	.string "cave.\p"
	.string "Tiksi's elders swore to keep it from the\n"
	.string "people. Tread carefully in there.$"
