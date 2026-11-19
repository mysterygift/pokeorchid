SevenIsland_SevaultCanyon_Entrance_MapScripts::
	.byte 0


SevenIsland_SevaultCanyon_Entrance_EventScript_Miah::
# 4 "data/maps/SevenIsland_SevaultCanyon_Entrance/scripts.pory"
	trainerbattle_single TRAINER_SEVII_MIAH, SevenIsland_SevaultCanyon_Entrance_Text_MiahIntro, SevenIsland_SevaultCanyon_Entrance_Text_MiahDefeat
# 5 "data/maps/SevenIsland_SevaultCanyon_Entrance/scripts.pory"
	msgbox SevenIsland_SevaultCanyon_Entrance_Text_MiahPost, MSGBOX_AUTOCLOSE
	return


SevenIsland_SevaultCanyon_Entrance_EventScript_Eve::
# 21 "data/maps/SevenIsland_SevaultCanyon_Entrance/scripts.pory"
	msgbox SevenIsland_SevaultCanyon_Entrance_EventScript_Eve_Text_0, MSGBOX_NPC
	return


SevenIsland_SevaultCanyon_Entrance_EventScript_Jon::
# 25 "data/maps/SevenIsland_SevaultCanyon_Entrance/scripts.pory"
	msgbox SevenIsland_SevaultCanyon_Entrance_EventScript_Jon_Text_0, MSGBOX_NPC
	return


SevenIsland_SevaultCanyon_Entrance_EventScript_Nicolas::
# 29 "data/maps/SevenIsland_SevaultCanyon_Entrance/scripts.pory"
	trainerbattle_single TRAINER_SEVII_NICOLAS, SevenIsland_SevaultCanyon_Entrance_Text_NicolasIntro, SevenIsland_SevaultCanyon_Entrance_Text_NicolasDefeat
# 30 "data/maps/SevenIsland_SevaultCanyon_Entrance/scripts.pory"
	msgbox SevenIsland_SevaultCanyon_Entrance_Text_NicolasPost, MSGBOX_AUTOCLOSE
	return


SevenIsland_SevaultCanyon_Entrance_EventScript_Madeline::
# 46 "data/maps/SevenIsland_SevaultCanyon_Entrance/scripts.pory"
	trainerbattle_single TRAINER_SEVII_MADELINE, SevenIsland_SevaultCanyon_Entrance_Text_MadelineIntro, SevenIsland_SevaultCanyon_Entrance_Text_MadelineDefeat
# 47 "data/maps/SevenIsland_SevaultCanyon_Entrance/scripts.pory"
	msgbox SevenIsland_SevaultCanyon_Entrance_Text_MadelinePost, MSGBOX_AUTOCLOSE
	return


SevenIsland_SevaultCanyon_Entrance_EventScript_Mason::
# 63 "data/maps/SevenIsland_SevaultCanyon_Entrance/scripts.pory"
	msgbox SevenIsland_SevaultCanyon_Entrance_EventScript_Eve_Text_0, MSGBOX_NPC
	return


SevenIsland_SevaultCanyon_Entrance_EventScript_RouteSign::
# 67 "data/maps/SevenIsland_SevaultCanyon_Entrance/scripts.pory"
	msgbox SevenIsland_SevaultCanyon_Entrance_EventScript_RouteSign_Text_0, MSGBOX_SIGN
	return


SevenIsland_SevaultCanyon_Entrance_EventScript_Eve_Text_0:
# 21 "data/maps/SevenIsland_SevaultCanyon_Entrance/scripts.pory"
	.string "The canyon ahead is steep. Get ready\n"
	.string "for a climb!$"

SevenIsland_SevaultCanyon_Entrance_EventScript_Jon_Text_0:
# 25 "data/maps/SevenIsland_SevaultCanyon_Entrance/scripts.pory"
	.string "The Sevii Islands are so peaceful. I\n"
	.string "could stay here forever.$"

SevenIsland_SevaultCanyon_Entrance_EventScript_RouteSign_Text_0:
# 67 "data/maps/SevenIsland_SevaultCanyon_Entrance/scripts.pory"
	.string "SEVAULT CANYON ENTRANCE\n"
	.string "Tanoby Ruins lie beyond the canyon.$"

SevenIsland_SevaultCanyon_Entrance_Text_MiahIntro::
# 8 "data/maps/SevenIsland_SevaultCanyon_Entrance/scripts.pory"
	.string "A sweet scent drifts through the\n"
	.string "canyon...$"

SevenIsland_SevaultCanyon_Entrance_Text_MiahDefeat::
# 12 "data/maps/SevenIsland_SevaultCanyon_Entrance/scripts.pory"
	.string "How bitter...$"

SevenIsland_SevaultCanyon_Entrance_Text_MiahPost::
# 16 "data/maps/SevenIsland_SevaultCanyon_Entrance/scripts.pory"
	.string "The sunsets out here are something\n"
	.string "special.$"

SevenIsland_SevaultCanyon_Entrance_Text_NicolasIntro::
# 33 "data/maps/SevenIsland_SevaultCanyon_Entrance/scripts.pory"
	.string "Sevault Canyon is tough. Prove you're\n"
	.string "ready!$"

SevenIsland_SevaultCanyon_Entrance_Text_NicolasDefeat::
# 37 "data/maps/SevenIsland_SevaultCanyon_Entrance/scripts.pory"
	.string "You'll do fine in there.$"

SevenIsland_SevaultCanyon_Entrance_Text_NicolasPost::
# 41 "data/maps/SevenIsland_SevaultCanyon_Entrance/scripts.pory"
	.string "The canyon ahead is steep. Get ready\n"
	.string "for a climb!$"

SevenIsland_SevaultCanyon_Entrance_Text_MadelineIntro::
# 50 "data/maps/SevenIsland_SevaultCanyon_Entrance/scripts.pory"
	.string "Rangers patrol here. Let's see your\n"
	.string "skill!$"

SevenIsland_SevaultCanyon_Entrance_Text_MadelineDefeat::
# 54 "data/maps/SevenIsland_SevaultCanyon_Entrance/scripts.pory"
	.string "Impressive work.$"

SevenIsland_SevaultCanyon_Entrance_Text_MadelinePost::
# 58 "data/maps/SevenIsland_SevaultCanyon_Entrance/scripts.pory"
	.string "Hiking all day is tiring, but the views\n"
	.string "make it worth it.$"
