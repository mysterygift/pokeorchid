# 1 "data/maps/TanglynTown/scripts.pory"

# 2 "data/maps/TanglynTown/scripts.pory"
TanglynTown_MapScripts::
# 3 "data/maps/TanglynTown/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, TanglynTown_OnTransition
# 4 "data/maps/TanglynTown/scripts.pory"
	.byte 0
# 5 "data/maps/TanglynTown/scripts.pory"

# 6 "data/maps/TanglynTown/scripts.pory"
TanglynTown_OnTransition:
# 7 "data/maps/TanglynTown/scripts.pory"
	setflag FLAG_VISITED_TANGLYN_TOWN
# 8 "data/maps/TanglynTown/scripts.pory"
	end
# 9 "data/maps/TanglynTown/scripts.pory"

# 10 "data/maps/TanglynTown/scripts.pory"
TanglynTown_EventScript_TownSign::
# 11 "data/maps/TanglynTown/scripts.pory"
	msgbox TanglynTown_Text_TownSign, MSGBOX_SIGN
# 12 "data/maps/TanglynTown/scripts.pory"
	end
# 13 "data/maps/TanglynTown/scripts.pory"

# 14 "data/maps/TanglynTown/scripts.pory"
TanglynTown_EventScript_Sign0::
# 15 "data/maps/TanglynTown/scripts.pory"
	msgbox TanglynTown_Text_Sign0, MSGBOX_SIGN
# 16 "data/maps/TanglynTown/scripts.pory"
	end
# 17 "data/maps/TanglynTown/scripts.pory"

# 18 "data/maps/TanglynTown/scripts.pory"
TanglynTown_Text_TownSign:
# 19 "data/maps/TanglynTown/scripts.pory"
	.string "TANGLYN TOWN\n"
# 20 "data/maps/TanglynTown/scripts.pory"
	.string "A quiet coastal town filled\l"
# 21 "data/maps/TanglynTown/scripts.pory"
	.string "with ancient murals.$"
# 22 "data/maps/TanglynTown/scripts.pory"

# 23 "data/maps/TanglynTown/scripts.pory"
TanglynTown_Text_Sign0:
# 24 "data/maps/TanglynTown/scripts.pory"
	.string "TANGLYN MURAL HALL\n"
# 25 "data/maps/TanglynTown/scripts.pory"
	.string "Home of TIKSI's ancient murals.\l"
# 26 "data/maps/TanglynTown/scripts.pory"
	.string "(Closed for restoration.)$"
