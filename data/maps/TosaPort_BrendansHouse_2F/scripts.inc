TosaPort_BrendansHouse_2F_MapScripts::
	.byte 0


TosaPortStation_Attendant::
# 9 "data/maps/TosaPort_BrendansHouse_2F/scripts.pory"
	lock
# 10 "data/maps/TosaPort_BrendansHouse_2F/scripts.pory"
	faceplayer
# 11 "data/maps/TosaPort_BrendansHouse_2F/scripts.pory"
	checkitem ITEM_RAIL_CARD
# 12 "data/maps/TosaPort_BrendansHouse_2F/scripts.pory"
	compare VAR_RESULT, FALSE
	goto_if_eq TosaPortStation_Attendant_2
TosaPortStation_Attendant_1:
# 15 "data/maps/TosaPort_BrendansHouse_2F/scripts.pory"
	settrainstation TRAIN_STATION_TEST_EAST, TRAIN_ACCESS_OPEN
# 16 "data/maps/TosaPort_BrendansHouse_2F/scripts.pory"
	usetrain
# 17 "data/maps/TosaPort_BrendansHouse_2F/scripts.pory"
	release
	end

TosaPortStation_Attendant_2:
# 13 "data/maps/TosaPort_BrendansHouse_2F/scripts.pory"
	giveitem ITEM_RAIL_CARD
	goto TosaPortStation_Attendant_1

