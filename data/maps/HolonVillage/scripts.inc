HolonVillage_MapScripts::
# 2 "data/maps/HolonVillage/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, HolonVillage_MapScripts_MAP_SCRIPT_ON_TRANSITION
	.byte 0

HolonVillage_MapScripts_MAP_SCRIPT_ON_TRANSITION:
# 3 "data/maps/HolonVillage/scripts.pory"
	setflag FLAG_VISITED_HOLON_VILLAGE
# 4 "data/maps/HolonVillage/scripts.pory"
	call_if_unset FLAG_HOLON_BERRIES_PLANTED, HolonVillage_EventScript_PlantBerries
	return


HolonVillage_EventScript_PlantBerries::
# 9 "data/maps/HolonVillage/scripts.pory"
	setberrytree BERRY_TREE_ROUTE_104_SOIL_1, BERRY_ID_ORAN, BERRY_STAGE_BERRIES
# 10 "data/maps/HolonVillage/scripts.pory"
	setberrytree BERRY_TREE_ROUTE_104_ORAN_1, BERRY_ID_PECHA, BERRY_STAGE_BERRIES
# 11 "data/maps/HolonVillage/scripts.pory"
	setberrytree BERRY_TREE_ROUTE_104_CHERI_1, BERRY_ID_ORAN, BERRY_STAGE_BERRIES
# 12 "data/maps/HolonVillage/scripts.pory"
	setberrytree BERRY_TREE_ROUTE_104_SOIL_2, BERRY_ID_SITRUS, BERRY_STAGE_BERRIES
# 13 "data/maps/HolonVillage/scripts.pory"
	setberrytree BERRY_TREE_ROUTE_104_LEPPA, BERRY_ID_ORAN, BERRY_STAGE_BERRIES
# 14 "data/maps/HolonVillage/scripts.pory"
	setberrytree BERRY_TREE_ROUTE_104_ORAN_2, BERRY_ID_LUM, BERRY_STAGE_BERRIES
# 15 "data/maps/HolonVillage/scripts.pory"
	setberrytree BERRY_TREE_ROUTE_104_SOIL_3, BERRY_ID_PECHA, BERRY_STAGE_BERRIES
# 16 "data/maps/HolonVillage/scripts.pory"
	setberrytree BERRY_TREE_ROUTE_104_PECHA, BERRY_ID_ORAN, BERRY_STAGE_BERRIES
# 17 "data/maps/HolonVillage/scripts.pory"
	setberrytree BERRY_TREE_ROUTE_102_ORAN, BERRY_ID_PERSIM, BERRY_STAGE_BERRIES
# 18 "data/maps/HolonVillage/scripts.pory"
	setflag FLAG_HOLON_BERRIES_PLANTED
	return


HolonVillage_EventScript_Walkway::
# 22 "data/maps/HolonVillage/scripts.pory"
	goto_if_set FLAG_HOLON_POWER_SPOTS_HEALED, HolonVillage_EventScript_Walkway_1
# 25 "data/maps/HolonVillage/scripts.pory"
	msgbox HolonVillage_EventScript_Walkway_Text_1, MSGBOX_NPC
	return

HolonVillage_EventScript_Walkway_1:
# 23 "data/maps/HolonVillage/scripts.pory"
	msgbox HolonVillage_EventScript_Walkway_Text_0, MSGBOX_NPC
	return


HolonVillage_EventScript_FarmerNw::
# 30 "data/maps/HolonVillage/scripts.pory"
	goto_if_set FLAG_HOLON_POWER_SPOTS_HEALED, HolonVillage_EventScript_FarmerNw_1
# 33 "data/maps/HolonVillage/scripts.pory"
	msgbox HolonVillage_EventScript_FarmerNw_Text_1, MSGBOX_NPC
	return

HolonVillage_EventScript_FarmerNw_1:
# 31 "data/maps/HolonVillage/scripts.pory"
	msgbox HolonVillage_EventScript_FarmerNw_Text_0, MSGBOX_NPC
	return


HolonVillage_EventScript_FarmerSe::
# 38 "data/maps/HolonVillage/scripts.pory"
	goto_if_set FLAG_HOLON_POWER_SPOTS_HEALED, HolonVillage_EventScript_FarmerSe_1
# 41 "data/maps/HolonVillage/scripts.pory"
	msgbox HolonVillage_EventScript_FarmerSe_Text_1, MSGBOX_NPC
	return

HolonVillage_EventScript_FarmerSe_1:
# 39 "data/maps/HolonVillage/scripts.pory"
	msgbox HolonVillage_EventScript_FarmerSe_Text_0, MSGBOX_NPC
	return


HolonVillage_EventScript_Lass::
# 46 "data/maps/HolonVillage/scripts.pory"
	goto_if_set FLAG_HOLON_POWER_SPOTS_HEALED, HolonVillage_EventScript_Lass_1
# 49 "data/maps/HolonVillage/scripts.pory"
	msgbox HolonVillage_EventScript_Lass_Text_1, MSGBOX_NPC
	return

HolonVillage_EventScript_Lass_1:
# 47 "data/maps/HolonVillage/scripts.pory"
	msgbox HolonVillage_EventScript_Lass_Text_0, MSGBOX_NPC
	return


HolonVillage_EventScript_Mentor::
# 54 "data/maps/HolonVillage/scripts.pory"
	msgbox HolonVillage_EventScript_Mentor_Text_0, MSGBOX_NPC
	return


HolonVillage_EventScript_FarmerN::
# 58 "data/maps/HolonVillage/scripts.pory"
	goto_if_set FLAG_HOLON_POWER_SPOTS_HEALED, HolonVillage_EventScript_FarmerN_1
# 61 "data/maps/HolonVillage/scripts.pory"
	msgbox HolonVillage_EventScript_FarmerN_Text_1, MSGBOX_NPC
	return

HolonVillage_EventScript_FarmerN_1:
# 59 "data/maps/HolonVillage/scripts.pory"
	msgbox HolonVillage_EventScript_FarmerN_Text_0, MSGBOX_NPC
	return


HolonVillage_EventScript_TownSign::
# 66 "data/maps/HolonVillage/scripts.pory"
	msgbox HolonVillage_EventScript_TownSign_Text_0, MSGBOX_SIGN
	return


HolonVillage_EventScript_LakeSign::
# 70 "data/maps/HolonVillage/scripts.pory"
	msgbox HolonVillage_EventScript_LakeSign_Text_0, MSGBOX_SIGN
	return


HolonVillage_EventScript_FarmSign::
# 74 "data/maps/HolonVillage/scripts.pory"
	msgbox HolonVillage_EventScript_FarmSign_Text_0, MSGBOX_SIGN
	return


HolonVillage_EventScript_TowerSign::
# 78 "data/maps/HolonVillage/scripts.pory"
	msgbox HolonVillage_EventScript_TowerSign_Text_0, MSGBOX_SIGN
	return


HolonVillage_EventScript_Walkway_Text_0:
# 23 "data/maps/HolonVillage/scripts.pory"
	.string "Readings at the Power Spot are climbing\n"
	.string "back to normal. Faba's so-called\l"
	.string "tolerance... I should have checked his\l"
	.string "numbers.$"

HolonVillage_EventScript_Walkway_Text_1:
# 25 "data/maps/HolonVillage/scripts.pory"
	.string "A seasonal fluctuation, nothing more.\n"
	.string "The readings from the Power Spot are\l"
	.string "perfectly within tolerance.$"

HolonVillage_EventScript_FarmerNw_Text_0:
# 31 "data/maps/HolonVillage/scripts.pory"
	.string "Look at that! The leaves by the tower\n"
	.string "came up green this morning. Maybe the\l"
	.string "berries will set after all.$"

HolonVillage_EventScript_FarmerNw_Text_1:
# 33 "data/maps/HolonVillage/scripts.pory"
	.string "Third season the berries won't set.\n"
	.string "Leaves come up grey as ash, closer to\l"
	.string "that tower they get.$"

HolonVillage_EventScript_FarmerSe_Text_0:
# 39 "data/maps/HolonVillage/scripts.pory"
	.string "The soil's breathing again, I swear it.\n"
	.string "Gran was right about this land.$"

HolonVillage_EventScript_FarmerSe_Text_1:
# 41 "data/maps/HolonVillage/scripts.pory"
	.string "My gran said this soil grew anything.\n"
	.string "Now look at it. Power Spot, they call it...\l"
	.string "more like a drain.$"

HolonVillage_EventScript_Lass_Text_0:
# 47 "data/maps/HolonVillage/scripts.pory"
	.string "Have you seen the lake? The grass\n"
	.string "round the stone pillars is green again!$"

HolonVillage_EventScript_Lass_Text_1:
# 49 "data/maps/HolonVillage/scripts.pory"
	.string "The grass round the lake used to be so\n"
	.string "green. Now it's all washed out near\l"
	.string "those stone pillars.$"

HolonVillage_EventScript_Mentor_Text_0:
# 54 "data/maps/HolonVillage/scripts.pory"
	.string "That old house belonged to Holon's\n"
	.string "stone carvers. When the tower went up\l"
	.string "they left, and nobody's lived there\l"
	.string "since.$"

HolonVillage_EventScript_FarmerN_Text_0:
# 59 "data/maps/HolonVillage/scripts.pory"
	.string "Word is the tower's machines are off.\n"
	.string "Good riddance. We'll have a proper\l"
	.string "harvest yet.$"

HolonVillage_EventScript_FarmerN_Text_1:
# 61 "data/maps/HolonVillage/scripts.pory"
	.string "Farming's hard work, but nobody in Holon\n"
	.string "ever went hungry. Well... nobody used to.$"

HolonVillage_EventScript_TownSign_Text_0:
# 66 "data/maps/HolonVillage/scripts.pory"
	.string "Holon Village\n"
	.string "Welcome, travellers from across the\l"
	.string "sea.$"

HolonVillage_EventScript_LakeSign_Text_0:
# 70 "data/maps/HolonVillage/scripts.pory"
	.string "South: Holon Lake\n"
	.string "North: Holon Village$"

HolonVillage_EventScript_FarmSign_Text_0:
# 74 "data/maps/HolonVillage/scripts.pory"
	.string "Holon Farms\n"
	.string "Please leave the berry trees to the\l"
	.string "farmers.$"

HolonVillage_EventScript_TowerSign_Text_0:
# 78 "data/maps/HolonVillage/scripts.pory"
	.string "Holon Research Tower\n"
	.string "Studying the Power Spots and the Delta\l"
	.string "Species.$"
