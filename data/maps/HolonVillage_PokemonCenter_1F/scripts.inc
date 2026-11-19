# 1 "data/maps/HolonVillage_PokemonCenter_1F/scripts.pory"

# 2 "data/maps/HolonVillage_PokemonCenter_1F/scripts.pory"
HolonVillage_PokemonCenter_1F_MapScripts::
# 3 "data/maps/HolonVillage_PokemonCenter_1F/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, HolonVillage_PokemonCenter_1F_OnTransition
# 4 "data/maps/HolonVillage_PokemonCenter_1F/scripts.pory"
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
# 5 "data/maps/HolonVillage_PokemonCenter_1F/scripts.pory"
	.byte 0
# 6 "data/maps/HolonVillage_PokemonCenter_1F/scripts.pory"

# 7 "data/maps/HolonVillage_PokemonCenter_1F/scripts.pory"
HolonVillage_PokemonCenter_1F_OnTransition:
# 8 "data/maps/HolonVillage_PokemonCenter_1F/scripts.pory"
	setrespawn HEAL_LOCATION_HOLON_VILLAGE
# 9 "data/maps/HolonVillage_PokemonCenter_1F/scripts.pory"
	end
# 10 "data/maps/HolonVillage_PokemonCenter_1F/scripts.pory"

# 11 "data/maps/HolonVillage_PokemonCenter_1F/scripts.pory"
HolonVillage_PokemonCenter_1F_EventScript_Nurse::
# 12 "data/maps/HolonVillage_PokemonCenter_1F/scripts.pory"
	setvar VAR_0x800B, LOCALID_HOLON_VILLAGE_NURSE
# 13 "data/maps/HolonVillage_PokemonCenter_1F/scripts.pory"
	call Common_EventScript_PkmnCenterNurse
# 14 "data/maps/HolonVillage_PokemonCenter_1F/scripts.pory"
	waitmessage
# 15 "data/maps/HolonVillage_PokemonCenter_1F/scripts.pory"
	waitbuttonpress
# 16 "data/maps/HolonVillage_PokemonCenter_1F/scripts.pory"
	release
# 17 "data/maps/HolonVillage_PokemonCenter_1F/scripts.pory"
	end

HolonVillage_PokemonCenter_1F_EventScript_Visitor::
# 21 "data/maps/HolonVillage_PokemonCenter_1F/scripts.pory"
	msgbox HolonVillage_PokemonCenter_1F_EventScript_Visitor_Text_0, MSGBOX_NPC
	return


HolonVillage_PokemonCenter_1F_EventScript_Visitor_Text_0:
# 21 "data/maps/HolonVillage_PokemonCenter_1F/scripts.pory"
	.string "I'm only here to study the Delta\n"
	.string "Species. Your Pokémon Center works\l"
	.string "just like ours back home!$"
