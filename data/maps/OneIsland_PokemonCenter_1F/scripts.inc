OneIsland_PokemonCenter_1F_MapScripts::
# 2 "data/maps/OneIsland_PokemonCenter_1F/scripts.pory"
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
# 3 "data/maps/OneIsland_PokemonCenter_1F/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, OneIsland_PokemonCenter_1F_MapScripts_MAP_SCRIPT_ON_TRANSITION
	.byte 0

OneIsland_PokemonCenter_1F_MapScripts_MAP_SCRIPT_ON_TRANSITION:
# 4 "data/maps/OneIsland_PokemonCenter_1F/scripts.pory"
	setrespawn HEAL_LOCATION_ONE_ISLAND
	return


OneIsland_PokemonCenter_1F_EventScript_NetTech::
# 9 "data/maps/OneIsland_PokemonCenter_1F/scripts.pory"
	msgbox OneIsland_PokemonCenter_1F_EventScript_NetTech_Text_0, MSGBOX_NPC
	return


# 12 "data/maps/OneIsland_PokemonCenter_1F/scripts.pory"

# 13 "data/maps/OneIsland_PokemonCenter_1F/scripts.pory"
OneIsland_PokemonCenter_1F_EventScript_Nurse::
# 14 "data/maps/OneIsland_PokemonCenter_1F/scripts.pory"
	setvar VAR_0x800B, LOCALID_ONE_ISLAND_NURSE
# 15 "data/maps/OneIsland_PokemonCenter_1F/scripts.pory"
	call Common_EventScript_PkmnCenterNurse
# 16 "data/maps/OneIsland_PokemonCenter_1F/scripts.pory"
	waitmessage
# 17 "data/maps/OneIsland_PokemonCenter_1F/scripts.pory"
	waitbuttonpress
# 18 "data/maps/OneIsland_PokemonCenter_1F/scripts.pory"
	release
# 19 "data/maps/OneIsland_PokemonCenter_1F/scripts.pory"
	end

OneIsland_PokemonCenter_1F_EventScript_NetTech_Text_0:
# 9 "data/maps/OneIsland_PokemonCenter_1F/scripts.pory"
	.string "This is the POKéMON NET CENTER. The\n"
	.string "network machine in the back links the\l"
	.string "Sevii Islands with Tosa. It's still being\l"
	.string "tuned, though!$"
