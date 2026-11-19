# 1 "data/maps/FurongVillage/scripts.pory"

# 2 "data/maps/FurongVillage/scripts.pory"
FurongVillage_MapScripts::
# 3 "data/maps/FurongVillage/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, FurongVillage_OnTransition
# 4 "data/maps/FurongVillage/scripts.pory"
	.byte 0
# 5 "data/maps/FurongVillage/scripts.pory"

# 6 "data/maps/FurongVillage/scripts.pory"
FurongVillage_OnTransition:
# 7 "data/maps/FurongVillage/scripts.pory"
	setflag FLAG_VISITED_FURONG_VILLAGE
# 8 "data/maps/FurongVillage/scripts.pory"
	end
# 9 "data/maps/FurongVillage/scripts.pory"

# 10 "data/maps/FurongVillage/scripts.pory"
FurongVillage_EventScript_Sign0::
# 11 "data/maps/FurongVillage/scripts.pory"
	msgbox FurongVillage_Text_Sign0, MSGBOX_SIGN
# 12 "data/maps/FurongVillage/scripts.pory"
	end
# 13 "data/maps/FurongVillage/scripts.pory"

# 14 "data/maps/FurongVillage/scripts.pory"
FurongVillage_Text_Sign0:
# 15 "data/maps/FurongVillage/scripts.pory"
	.string "FURONG VILLAGE\n"
# 16 "data/maps/FurongVillage/scripts.pory"
	.string "A fishing village on TIKSI's shore.$"
