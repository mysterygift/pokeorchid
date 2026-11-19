SixIsland_PokemonCenter_1F_MapScripts::
# 2 "data/maps/SixIsland_PokemonCenter_1F/scripts.pory"
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
# 3 "data/maps/SixIsland_PokemonCenter_1F/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, SixIsland_PokemonCenter_1F_MapScripts_MAP_SCRIPT_ON_TRANSITION
	.byte 0

SixIsland_PokemonCenter_1F_MapScripts_MAP_SCRIPT_ON_TRANSITION:
# 4 "data/maps/SixIsland_PokemonCenter_1F/scripts.pory"
	setrespawn HEAL_LOCATION_SIX_ISLAND
	return


# 8 "data/maps/SixIsland_PokemonCenter_1F/scripts.pory"

# 9 "data/maps/SixIsland_PokemonCenter_1F/scripts.pory"
SixIsland_PokemonCenter_1F_EventScript_Nurse::
# 10 "data/maps/SixIsland_PokemonCenter_1F/scripts.pory"
	setvar VAR_0x800B, LOCALID_SIX_ISLAND_NURSE
# 11 "data/maps/SixIsland_PokemonCenter_1F/scripts.pory"
	call Common_EventScript_PkmnCenterNurse
# 12 "data/maps/SixIsland_PokemonCenter_1F/scripts.pory"
	waitmessage
# 13 "data/maps/SixIsland_PokemonCenter_1F/scripts.pory"
	waitbuttonpress
# 14 "data/maps/SixIsland_PokemonCenter_1F/scripts.pory"
	release
# 15 "data/maps/SixIsland_PokemonCenter_1F/scripts.pory"
	end
