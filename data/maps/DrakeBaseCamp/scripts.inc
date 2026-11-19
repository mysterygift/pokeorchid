# 1 "data/maps/DrakeBaseCamp/scripts.pory"

# 2 "data/maps/DrakeBaseCamp/scripts.pory"
DrakeBaseCamp_MapScripts::
# 3 "data/maps/DrakeBaseCamp/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, DrakeBaseCamp_OnTransition
# 4 "data/maps/DrakeBaseCamp/scripts.pory"
	.byte 0
# 5 "data/maps/DrakeBaseCamp/scripts.pory"

# 6 "data/maps/DrakeBaseCamp/scripts.pory"
DrakeBaseCamp_OnTransition:
# 7 "data/maps/DrakeBaseCamp/scripts.pory"
	setflag FLAG_VISITED_DRAKE_BASE_CAMP
# 8 "data/maps/DrakeBaseCamp/scripts.pory"
	end
# 9 "data/maps/DrakeBaseCamp/scripts.pory"

# 10 "data/maps/DrakeBaseCamp/scripts.pory"
DrakeBaseCamp_EventScript_TownSign::
# 11 "data/maps/DrakeBaseCamp/scripts.pory"
	msgbox DrakeBaseCamp_Text_TownSign, MSGBOX_SIGN
# 12 "data/maps/DrakeBaseCamp/scripts.pory"
	end
# 13 "data/maps/DrakeBaseCamp/scripts.pory"

# 14 "data/maps/DrakeBaseCamp/scripts.pory"
DrakeBaseCamp_Text_TownSign:
# 15 "data/maps/DrakeBaseCamp/scripts.pory"
	.string "DRAKE BASE CAMP\n"
# 16 "data/maps/DrakeBaseCamp/scripts.pory"
	.string "The last stop before MT. DRAKE.$"
