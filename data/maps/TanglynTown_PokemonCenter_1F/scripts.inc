# 1 "data/maps/TanglynTown_PokemonCenter_1F/scripts.pory"

# 2 "data/maps/TanglynTown_PokemonCenter_1F/scripts.pory"
TanglynTown_PokemonCenter_1F_MapScripts::
# 3 "data/maps/TanglynTown_PokemonCenter_1F/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, TanglynTown_PokemonCenter_1F_OnTransition
# 4 "data/maps/TanglynTown_PokemonCenter_1F/scripts.pory"
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
# 5 "data/maps/TanglynTown_PokemonCenter_1F/scripts.pory"
	.byte 0
# 6 "data/maps/TanglynTown_PokemonCenter_1F/scripts.pory"

# 7 "data/maps/TanglynTown_PokemonCenter_1F/scripts.pory"
TanglynTown_PokemonCenter_1F_OnTransition:
# 8 "data/maps/TanglynTown_PokemonCenter_1F/scripts.pory"
	setrespawn HEAL_LOCATION_TANGLYN_TOWN
# 9 "data/maps/TanglynTown_PokemonCenter_1F/scripts.pory"
	end
# 10 "data/maps/TanglynTown_PokemonCenter_1F/scripts.pory"

# 11 "data/maps/TanglynTown_PokemonCenter_1F/scripts.pory"
TanglynTown_PokemonCenter_1F_EventScript_Nurse::
# 12 "data/maps/TanglynTown_PokemonCenter_1F/scripts.pory"
	setvar VAR_0x800B, LOCALID_TANGLYN_TOWN_NURSE
# 13 "data/maps/TanglynTown_PokemonCenter_1F/scripts.pory"
	call Common_EventScript_PkmnCenterNurse
# 14 "data/maps/TanglynTown_PokemonCenter_1F/scripts.pory"
	waitmessage
# 15 "data/maps/TanglynTown_PokemonCenter_1F/scripts.pory"
	waitbuttonpress
# 16 "data/maps/TanglynTown_PokemonCenter_1F/scripts.pory"
	release
# 17 "data/maps/TanglynTown_PokemonCenter_1F/scripts.pory"
	end
