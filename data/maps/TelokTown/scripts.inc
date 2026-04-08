# 1 "data/maps/TelokTown/scripts.pory"

# 2 "data/maps/TelokTown/scripts.pory"
TelokTown_MapScripts::
# 3 "data/maps/TelokTown/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, TelokTown_OnTransition
# 4 "data/maps/TelokTown/scripts.pory"
	.byte 0
# 5 "data/maps/TelokTown/scripts.pory"

# 6 "data/maps/TelokTown/scripts.pory"
TelokTown_OnTransition:
# 7 "data/maps/TelokTown/scripts.pory"
	setflag FLAG_VISITED_TELOK_TOWN
# 8 "data/maps/TelokTown/scripts.pory"
	end
# 9 "data/maps/TelokTown/scripts.pory"

# 10 "data/maps/TelokTown/scripts.pory"
TelokTown_EventScript_TownSign::
# 11 "data/maps/TelokTown/scripts.pory"
	msgbox TelokTown_Text_TownSign, MSGBOX_SIGN
# 12 "data/maps/TelokTown/scripts.pory"
	end
# 13 "data/maps/TelokTown/scripts.pory"

# 14 "data/maps/TelokTown/scripts.pory"
TelokTown_EventScript_ExistentialMan::
# 15 "data/maps/TelokTown/scripts.pory"
	lock
# 16 "data/maps/TelokTown/scripts.pory"
	faceplayer
# 17 "data/maps/TelokTown/scripts.pory"
	msgbox TelokTown_Text_SavingMyProgress, MSGBOX_NPC
# 18 "data/maps/TelokTown/scripts.pory"
	delay 60
# 19 "data/maps/TelokTown/scripts.pory"
	msgbox TelokTown_Text_WaitWhat, MSGBOX_NPC
# 20 "data/maps/TelokTown/scripts.pory"
	release
# 21 "data/maps/TelokTown/scripts.pory"
	end
# 22 "data/maps/TelokTown/scripts.pory"

# 23 "data/maps/TelokTown/scripts.pory"
TelokTown_Text_SavingMyProgress:
# 24 "data/maps/TelokTown/scripts.pory"
	.string "I want to take a rest, so I'm saving my\n"
# 25 "data/maps/TelokTown/scripts.pory"
	.string "progress.$"
# 26 "data/maps/TelokTown/scripts.pory"

# 27 "data/maps/TelokTown/scripts.pory"
TelokTown_Text_WaitWhat:
# 28 "data/maps/TelokTown/scripts.pory"
	.string "Wait, what am I talking about?$"
# 29 "data/maps/TelokTown/scripts.pory"

# 30 "data/maps/TelokTown/scripts.pory"
TelokTown_Text_TownSign:
# 31 "data/maps/TelokTown/scripts.pory"
	.string "Telok Town\n"
# 32 "data/maps/TelokTown/scripts.pory"
	.string "“Where new journeys take root.”$"
