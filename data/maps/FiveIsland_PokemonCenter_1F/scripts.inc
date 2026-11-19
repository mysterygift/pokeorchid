FiveIsland_PokemonCenter_1F_MapScripts::
# 2 "data/maps/FiveIsland_PokemonCenter_1F/scripts.pory"
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
# 3 "data/maps/FiveIsland_PokemonCenter_1F/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, FiveIsland_PokemonCenter_1F_MapScripts_MAP_SCRIPT_ON_TRANSITION
	.byte 0

FiveIsland_PokemonCenter_1F_MapScripts_MAP_SCRIPT_ON_TRANSITION:
# 4 "data/maps/FiveIsland_PokemonCenter_1F/scripts.pory"
	setrespawn HEAL_LOCATION_FIVE_ISLAND
	return


# 8 "data/maps/FiveIsland_PokemonCenter_1F/scripts.pory"

# 9 "data/maps/FiveIsland_PokemonCenter_1F/scripts.pory"
FiveIsland_PokemonCenter_1F_EventScript_Nurse::
# 10 "data/maps/FiveIsland_PokemonCenter_1F/scripts.pory"
	setvar VAR_0x800B, LOCALID_FIVE_ISLAND_NURSE
# 11 "data/maps/FiveIsland_PokemonCenter_1F/scripts.pory"
	call Common_EventScript_PkmnCenterNurse
# 12 "data/maps/FiveIsland_PokemonCenter_1F/scripts.pory"
	waitmessage
# 13 "data/maps/FiveIsland_PokemonCenter_1F/scripts.pory"
	waitbuttonpress
# 14 "data/maps/FiveIsland_PokemonCenter_1F/scripts.pory"
	release
# 15 "data/maps/FiveIsland_PokemonCenter_1F/scripts.pory"
	end
