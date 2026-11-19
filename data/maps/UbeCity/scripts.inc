# 1 "data/maps/UbeCity/scripts.pory"

# 2 "data/maps/UbeCity/scripts.pory"
UbeCity_MapScripts::
# 3 "data/maps/UbeCity/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, UbeCity_OnTransition
# 4 "data/maps/UbeCity/scripts.pory"
	.byte 0
# 5 "data/maps/UbeCity/scripts.pory"

# 6 "data/maps/UbeCity/scripts.pory"
UbeCity_OnTransition:
# 7 "data/maps/UbeCity/scripts.pory"
	setflag FLAG_VISITED_UBE_CITY
# 8 "data/maps/UbeCity/scripts.pory"
	end
# 9 "data/maps/UbeCity/scripts.pory"

# 10 "data/maps/UbeCity/scripts.pory"
UbeCity_EventScript_TownSign::
# 11 "data/maps/UbeCity/scripts.pory"
	msgbox UbeCity_Text_TownSign, MSGBOX_SIGN
# 12 "data/maps/UbeCity/scripts.pory"
	end
# 13 "data/maps/UbeCity/scripts.pory"

# 14 "data/maps/UbeCity/scripts.pory"
UbeCity_EventScript_Sign0::
# 15 "data/maps/UbeCity/scripts.pory"
	msgbox UbeCity_Text_Sign0, MSGBOX_SIGN
# 16 "data/maps/UbeCity/scripts.pory"
	end
# 17 "data/maps/UbeCity/scripts.pory"

# 18 "data/maps/UbeCity/scripts.pory"
UbeCity_Text_TownSign:
# 19 "data/maps/UbeCity/scripts.pory"
	.string "UBE CITY\n"
# 20 "data/maps/UbeCity/scripts.pory"
	.string "Home of SILPH CO.'s TIKSI branch.$"
# 21 "data/maps/UbeCity/scripts.pory"

# 22 "data/maps/UbeCity/scripts.pory"
UbeCity_Text_Sign0:
# 23 "data/maps/UbeCity/scripts.pory"
	.string "SILPH CO. TIKSI BRANCH\n"
# 24 "data/maps/UbeCity/scripts.pory"
	.string "Closed to visitors.$"
