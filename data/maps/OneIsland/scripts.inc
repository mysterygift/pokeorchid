OneIsland_MapScripts::
# 2 "data/maps/OneIsland/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, OneIsland_MapScripts_MAP_SCRIPT_ON_TRANSITION
	.byte 0

OneIsland_MapScripts_MAP_SCRIPT_ON_TRANSITION:
# 3 "data/maps/OneIsland/scripts.pory"
	setflag FLAG_VISITED_ONE_ISLAND
	return


OneIsland_EventScript_BILL::
# 8 "data/maps/OneIsland/scripts.pory"
	msgbox OneIsland_EventScript_BILL_Text_0, MSGBOX_NPC
	return


OneIsland_EventScript_OldMan::
# 12 "data/maps/OneIsland/scripts.pory"
	msgbox OneIsland_EventScript_OldMan_Text_0, MSGBOX_NPC
	return


OneIsland_EventScript_BaldingMan::
# 16 "data/maps/OneIsland/scripts.pory"
	msgbox OneIsland_EventScript_BaldingMan_Text_0, MSGBOX_NPC
	return


OneIsland_EventScript_IslandSign::
# 20 "data/maps/OneIsland/scripts.pory"
	msgbox OneIsland_EventScript_IslandSign_Text_0, MSGBOX_SIGN
	return


OneIsland_EventScript_PokemonNetCenterSign::
# 25 "data/maps/OneIsland/scripts.pory"
	msgbox OneIsland_EventScript_PokemonNetCenterSign_Text_0, MSGBOX_SIGN
	return


OneIsland_EventScript_BILL_Text_0:
# 8 "data/maps/OneIsland/scripts.pory"
	.string "I'm visiting an old friend who runs the\n"
	.string "Net Center. He's always tinkering with\l"
	.string "the network machine.$"

OneIsland_EventScript_OldMan_Text_0:
# 12 "data/maps/OneIsland/scripts.pory"
	.string "One Island is the gateway to the Sevii\n"
	.string "Islands. Ferries for all seven islands\l"
	.string "leave from the harbour.$"

OneIsland_EventScript_BaldingMan_Text_0:
# 16 "data/maps/OneIsland/scripts.pory"
	.string "Kindle Road runs north from here to Mt.\n"
	.string "Ember. The hot springs on the way are\l"
	.string "wonderful.$"

OneIsland_EventScript_IslandSign_Text_0:
# 20 "data/maps/OneIsland/scripts.pory"
	.string "ONE ISLAND\n"
	.string "Where the warm sea meets the Kindle\l"
	.string "Road.$"

OneIsland_EventScript_PokemonNetCenterSign_Text_0:
# 25 "data/maps/OneIsland/scripts.pory"
	.string "POKéMON NET CENTER\n"
	.string "Healing and long-distance links for\l"
	.string "travellers.$"
