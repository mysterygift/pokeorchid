SevenIsland_SevaultCanyon_MapScripts::
	.byte 0


SevenIsland_SevaultCanyon_EventScript_Cyndy::
# 4 "data/maps/SevenIsland_SevaultCanyon/scripts.pory"
	msgbox SevenIsland_SevaultCanyon_EventScript_Cyndy_Text_0, MSGBOX_NPC
	return


SevenIsland_SevaultCanyon_EventScript_Evan::
# 8 "data/maps/SevenIsland_SevaultCanyon/scripts.pory"
	msgbox SevenIsland_SevaultCanyon_EventScript_Evan_Text_0, MSGBOX_NPC
	return


SevenIsland_SevaultCanyon_EventScript_Jackson::
# 12 "data/maps/SevenIsland_SevaultCanyon/scripts.pory"
	trainerbattle_single TRAINER_SEVII_JACKSON, SevenIsland_SevaultCanyon_Text_JacksonIntro, SevenIsland_SevaultCanyon_Text_JacksonDefeat
# 13 "data/maps/SevenIsland_SevaultCanyon/scripts.pory"
	msgbox SevenIsland_SevaultCanyon_Text_JacksonPost, MSGBOX_AUTOCLOSE
	return


SevenIsland_SevaultCanyon_EventScript_Katelyn::
# 29 "data/maps/SevenIsland_SevaultCanyon/scripts.pory"
	msgbox SevenIsland_SevaultCanyon_EventScript_Katelyn_Text_0, MSGBOX_NPC
	return


SevenIsland_SevaultCanyon_EventScript_Leroy::
# 33 "data/maps/SevenIsland_SevaultCanyon/scripts.pory"
	trainerbattle_single TRAINER_SEVII_LEROY, SevenIsland_SevaultCanyon_Text_LeroyIntro, SevenIsland_SevaultCanyon_Text_LeroyDefeat
# 34 "data/maps/SevenIsland_SevaultCanyon/scripts.pory"
	msgbox SevenIsland_SevaultCanyon_Text_LeroyPost, MSGBOX_AUTOCLOSE
	return


SevenIsland_SevaultCanyon_EventScript_Michelle::
# 50 "data/maps/SevenIsland_SevaultCanyon/scripts.pory"
	trainerbattle_single TRAINER_SEVII_MICHELLE, SevenIsland_SevaultCanyon_Text_MichelleIntro, SevenIsland_SevaultCanyon_Text_MichelleDefeat
# 51 "data/maps/SevenIsland_SevaultCanyon/scripts.pory"
	msgbox SevenIsland_SevaultCanyon_Text_MichellePost, MSGBOX_AUTOCLOSE
	return


SevenIsland_SevaultCanyon_EventScript_Lex::
# 67 "data/maps/SevenIsland_SevaultCanyon/scripts.pory"
	msgbox SevenIsland_SevaultCanyon_EventScript_Lex_Text_0, MSGBOX_NPC
	return


SevenIsland_SevaultCanyon_EventScript_Nya::
# 71 "data/maps/SevenIsland_SevaultCanyon/scripts.pory"
	msgbox SevenIsland_SevaultCanyon_EventScript_Nya_Text_0, MSGBOX_NPC
	return


SevenIsland_SevaultCanyon_EventScript_BlackBelt::
# 75 "data/maps/SevenIsland_SevaultCanyon/scripts.pory"
	msgbox SevenIsland_SevaultCanyon_EventScript_BlackBelt_Text_0, MSGBOX_NPC
	return


SevenIsland_SevaultCanyon_EventScript_RouteSign::
# 79 "data/maps/SevenIsland_SevaultCanyon/scripts.pory"
	msgbox SevenIsland_SevaultCanyon_EventScript_RouteSign_Text_0, MSGBOX_SIGN
	return


SevenIsland_SevaultCanyon_EventScript_Cyndy_Text_0:
# 4 "data/maps/SevenIsland_SevaultCanyon/scripts.pory"
	.string "The hot springs here are the best for\n"
	.string "sore muscles.$"

SevenIsland_SevaultCanyon_EventScript_Evan_Text_0:
# 8 "data/maps/SevenIsland_SevaultCanyon/scripts.pory"
	.string "It's lovely to meet a traveller from\n"
	.string "Tosa.$"

SevenIsland_SevaultCanyon_EventScript_Katelyn_Text_0:
# 29 "data/maps/SevenIsland_SevaultCanyon/scripts.pory"
	.string "Hiking all day is tiring, but the views\n"
	.string "make it worth it.$"

SevenIsland_SevaultCanyon_EventScript_Lex_Text_0:
# 67 "data/maps/SevenIsland_SevaultCanyon/scripts.pory"
	.string "Each island has its own character. Have\n"
	.string "you visited them all?$"

SevenIsland_SevaultCanyon_EventScript_Nya_Text_0:
# 71 "data/maps/SevenIsland_SevaultCanyon/scripts.pory"
	.string "A ferry hops between the islands from\n"
	.string "every harbour.$"

SevenIsland_SevaultCanyon_EventScript_BlackBelt_Text_0:
# 75 "data/maps/SevenIsland_SevaultCanyon/scripts.pory"
	.string "The ruins are south of here, past the\n"
	.string "canyon.$"

SevenIsland_SevaultCanyon_EventScript_RouteSign_Text_0:
# 79 "data/maps/SevenIsland_SevaultCanyon/scripts.pory"
	.string "SEVAULT CANYON\n"
	.string "Falling rocks. Climb with care.$"

SevenIsland_SevaultCanyon_Text_JacksonIntro::
# 16 "data/maps/SevenIsland_SevaultCanyon/scripts.pory"
	.string "Only the strong make it through Sevault\n"
	.string "Canyon!$"

SevenIsland_SevaultCanyon_Text_JacksonDefeat::
# 20 "data/maps/SevenIsland_SevaultCanyon/scripts.pory"
	.string "You're strong, all right.$"

SevenIsland_SevaultCanyon_Text_JacksonPost::
# 24 "data/maps/SevenIsland_SevaultCanyon/scripts.pory"
	.string "I packed so many snacks for this trip!$"

SevenIsland_SevaultCanyon_Text_LeroyIntro::
# 37 "data/maps/SevenIsland_SevaultCanyon/scripts.pory"
	.string "I came all the way here to train. Face\n"
	.string "me!$"

SevenIsland_SevaultCanyon_Text_LeroyDefeat::
# 41 "data/maps/SevenIsland_SevaultCanyon/scripts.pory"
	.string "My training isn't over.$"

SevenIsland_SevaultCanyon_Text_LeroyPost::
# 45 "data/maps/SevenIsland_SevaultCanyon/scripts.pory"
	.string "The sunsets out here are something\n"
	.string "special.$"

SevenIsland_SevaultCanyon_Text_MichelleIntro::
# 54 "data/maps/SevenIsland_SevaultCanyon/scripts.pory"
	.string "Only elite Trainers come this far.\n"
	.string "Battle!$"

SevenIsland_SevaultCanyon_Text_MichelleDefeat::
# 58 "data/maps/SevenIsland_SevaultCanyon/scripts.pory"
	.string "You're elite too.$"

SevenIsland_SevaultCanyon_Text_MichellePost::
# 62 "data/maps/SevenIsland_SevaultCanyon/scripts.pory"
	.string "A ferry hops between the islands from\n"
	.string "every harbour.$"
