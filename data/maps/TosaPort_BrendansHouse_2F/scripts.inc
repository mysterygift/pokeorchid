TosaPort_BrendansHouse_2F_MapScripts::
	.byte 0


TosaPortStation_Attendant::
# 11 "data/maps/TosaPort_BrendansHouse_2F/scripts.pory"
	lock
# 12 "data/maps/TosaPort_BrendansHouse_2F/scripts.pory"
	faceplayer
# 13 "data/maps/TosaPort_BrendansHouse_2F/scripts.pory"
	call TosaRail_EventScript_OpenAllStations
# 14 "data/maps/TosaPort_BrendansHouse_2F/scripts.pory"
	giveitem ITEM_RAIL_CARD
# 15 "data/maps/TosaPort_BrendansHouse_2F/scripts.pory"
	usetrain
# 16 "data/maps/TosaPort_BrendansHouse_2F/scripts.pory"
	release
	end

