SevenIsland_SevaultCanyon_House_MapScripts::
	.byte 0


SevenIsland_SevaultCanyon_House_EventScript_ChanseyDanceMan::
# 4 "data/maps/SevenIsland_SevaultCanyon_House/scripts.pory"
	msgbox SevenIsland_SevaultCanyon_House_EventScript_ChanseyDanceMan_Text_0, MSGBOX_NPC
	return


SevenIsland_SevaultCanyon_House_EventScript_Chansey::
# 8 "data/maps/SevenIsland_SevaultCanyon_House/scripts.pory"
	lock
# 9 "data/maps/SevenIsland_SevaultCanyon_House/scripts.pory"
	faceplayer
# 10 "data/maps/SevenIsland_SevaultCanyon_House/scripts.pory"
	waitse
# 11 "data/maps/SevenIsland_SevaultCanyon_House/scripts.pory"
	playmoncry SPECIES_CHANSEY, CRY_MODE_NORMAL
# 12 "data/maps/SevenIsland_SevaultCanyon_House/scripts.pory"
	msgbox SevenIsland_SevaultCanyon_House_EventScript_Chansey_Text_0
# 13 "data/maps/SevenIsland_SevaultCanyon_House/scripts.pory"
	waitmoncry
# 14 "data/maps/SevenIsland_SevaultCanyon_House/scripts.pory"
	release
	return


SevenIsland_SevaultCanyon_House_EventScript_ChanseyDanceMan_Text_0:
# 4 "data/maps/SevenIsland_SevaultCanyon_House/scripts.pory"
	.string "My Chansey loves to dance! Don't you,\n"
	.string "dear?$"

SevenIsland_SevaultCanyon_House_EventScript_Chansey_Text_0:
# 12 "data/maps/SevenIsland_SevaultCanyon_House/scripts.pory"
	.string "CHANSEY: Chaaansey!$"
