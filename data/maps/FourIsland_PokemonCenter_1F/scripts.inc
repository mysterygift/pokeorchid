FourIsland_PokemonCenter_1F_MapScripts::
# 2 "data/maps/FourIsland_PokemonCenter_1F/scripts.pory"
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
# 3 "data/maps/FourIsland_PokemonCenter_1F/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, FourIsland_PokemonCenter_1F_MapScripts_MAP_SCRIPT_ON_TRANSITION
	.byte 0

FourIsland_PokemonCenter_1F_MapScripts_MAP_SCRIPT_ON_TRANSITION:
# 4 "data/maps/FourIsland_PokemonCenter_1F/scripts.pory"
	setrespawn HEAL_LOCATION_FOUR_ISLAND
	return


# 8 "data/maps/FourIsland_PokemonCenter_1F/scripts.pory"

# 9 "data/maps/FourIsland_PokemonCenter_1F/scripts.pory"
FourIsland_PokemonCenter_1F_EventScript_Nurse::
# 10 "data/maps/FourIsland_PokemonCenter_1F/scripts.pory"
	setvar VAR_0x800B, LOCALID_FOUR_ISLAND_NURSE
# 11 "data/maps/FourIsland_PokemonCenter_1F/scripts.pory"
	call Common_EventScript_PkmnCenterNurse
# 12 "data/maps/FourIsland_PokemonCenter_1F/scripts.pory"
	waitmessage
# 13 "data/maps/FourIsland_PokemonCenter_1F/scripts.pory"
	waitbuttonpress
# 14 "data/maps/FourIsland_PokemonCenter_1F/scripts.pory"
	release
# 15 "data/maps/FourIsland_PokemonCenter_1F/scripts.pory"
	end
