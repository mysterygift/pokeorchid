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
TanglynTown_EventScript_Sign0::
# 11 "data/maps/TanglynTown/scripts.pory"
	msgbox TanglynTown_Text_Sign0, MSGBOX_SIGN
# 12 "data/maps/TanglynTown/scripts.pory"
	end
# 13 "data/maps/TanglynTown/scripts.pory"

# 14 "data/maps/TanglynTown/scripts.pory"
TanglynTown_EventScript_Sign1::
# 15 "data/maps/TanglynTown/scripts.pory"
	msgbox TanglynTown_Text_Sign1, MSGBOX_SIGN
# 16 "data/maps/TanglynTown/scripts.pory"
	end
# 17 "data/maps/TanglynTown/scripts.pory"

# 18 "data/maps/TanglynTown/scripts.pory"
TanglynTown_Text_Sign0:
# 19 "data/maps/TanglynTown/scripts.pory"
	.string "TANGLYN TOWN\n"
# 20 "data/maps/TanglynTown/scripts.pory"
	.string "A quiet coastal town filled\l"
# 21 "data/maps/TanglynTown/scripts.pory"
	.string "with ancient murals.$"
# 22 "data/maps/TanglynTown/scripts.pory"

# 23 "data/maps/TanglynTown/scripts.pory"
TanglynTown_Text_Sign1:
# 24 "data/maps/TanglynTown/scripts.pory"
	.string "TANGLYN MURAL HALL\n"
# 25 "data/maps/TanglynTown/scripts.pory"
	.string "Home of TIKSI's ancient murals.\l"
# 26 "data/maps/TanglynTown/scripts.pory"
	.string "(Closed for restoration.)$"

TanglynTown_EventScript_TiksiNpc1::
# 33 "data/maps/TanglynTown/scripts.pory"
	msgbox TanglynTown_EventScript_TiksiNpc1_Text_0, MSGBOX_NPC
	return


TanglynTown_EventScript_TiksiNpc2::
# 37 "data/maps/TanglynTown/scripts.pory"
	msgbox TanglynTown_EventScript_TiksiNpc2_Text_0, MSGBOX_NPC
	return


TanglynTown_EventScript_TiksiNpc3::
# 41 "data/maps/TanglynTown/scripts.pory"
	msgbox TanglynTown_EventScript_TiksiNpc3_Text_0, MSGBOX_NPC
	return


TanglynTown_EventScript_TiksiGuardianFrigoCave::
# 45 "data/maps/TanglynTown/scripts.pory"
	msgbox TanglynTown_EventScript_TiksiGuardianFrigoCave_Text_0, MSGBOX_NPC
	return


TanglynTown_EventScript_TiksiNpc1_Text_0:
# 33 "data/maps/TanglynTown/scripts.pory"
	.string "The murals in the hall show giants\n"
	.string "sealed away by Tiksi's ancestors. Five\l"
	.string "of them! Not three.$"

TanglynTown_EventScript_TiksiNpc2_Text_0:
# 37 "data/maps/TanglynTown/scripts.pory"
	.string "The murals are older than any record.\n"
	.string "Some say people from Sevii painted\l"
	.string "them.$"

TanglynTown_EventScript_TiksiNpc3_Text_0:
# 41 "data/maps/TanglynTown/scripts.pory"
	.string "Frigo Cave's off the north shore.\n"
	.string "Locals say it's colder inside than it\l"
	.string "has any right to be.$"

TanglynTown_EventScript_TiksiGuardianFrigoCave_Text_0:
# 45 "data/maps/TanglynTown/scripts.pory"
	.string "Frigo Cave is colder than it has any\n"
	.string "right to be. The ice giant is back\l"
	.string "inside.\p"
	.string "I have guarded this shore all my life.\n"
	.string "Don't make me regret letting you pass.$"
