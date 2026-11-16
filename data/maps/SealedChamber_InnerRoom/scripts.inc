# 1 "data/maps/SealedChamber_InnerRoom/scripts.pory"

# 2 "data/maps/SealedChamber_InnerRoom/scripts.pory"
SealedChamber_InnerRoom_MapScripts::
# 3 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	.byte 0
# 4 "data/maps/SealedChamber_InnerRoom/scripts.pory"

# 5 "data/maps/SealedChamber_InnerRoom/scripts.pory"
SealedChamber_InnerRoom_EventScript_BrailleBackWall::
# 6 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	lockall
# 7 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	braillemsgbox SealedChamber_InnerRoom_Braille_FirstWailordLastRelicanth
# 8 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	goto_if_set FLAG_REGI_DOORS_OPENED, SealedChamber_InnerRoom_EventScript_NoEffect
# 9 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	specialvar VAR_RESULT, CheckRelicanthWailord
# 10 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, SealedChamber_InnerRoom_EventScript_NoEffect
# 11 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	fadeoutbgm 0
# 12 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	playse SE_TRUCK_MOVE
# 13 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	special DoSealedChamberShakingEffect_Long
# 14 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	delay 40
# 15 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	special DoSealedChamberShakingEffect_Short
# 16 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	playse SE_DOOR
# 17 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	delay 40
# 18 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	special DoSealedChamberShakingEffect_Short
# 19 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	playse SE_DOOR
# 20 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	delay 40
# 21 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	special DoSealedChamberShakingEffect_Short
# 22 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	playse SE_DOOR
# 23 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	delay 40
# 24 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	msgbox gText_DoorOpenedFarAway, MSGBOX_DEFAULT
# 25 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	closemessage
# 26 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	fadeinbgm 0
# 27 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	setflag FLAG_REGI_DOORS_OPENED
# 28 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	releaseall
# 29 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	end
# 30 "data/maps/SealedChamber_InnerRoom/scripts.pory"

# 31 "data/maps/SealedChamber_InnerRoom/scripts.pory"
SealedChamber_InnerRoom_EventScript_NoEffect::
# 32 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	releaseall
# 33 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	end
# 34 "data/maps/SealedChamber_InnerRoom/scripts.pory"

# 35 "data/maps/SealedChamber_InnerRoom/scripts.pory"
SealedChamber_InnerRoom_EventScript_BrailleStoryPart1::
# 36 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	lockall
# 37 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	braillemsgbox SealedChamber_InnerRoom_Braille_InThisCaveWeHaveLived
# 38 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	releaseall
# 39 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	end
# 40 "data/maps/SealedChamber_InnerRoom/scripts.pory"

# 41 "data/maps/SealedChamber_InnerRoom/scripts.pory"
SealedChamber_InnerRoom_EventScript_BrailleStoryPart2::
# 42 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	lockall
# 43 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	braillemsgbox SealedChamber_InnerRoom_Braille_WeOweAllToThePokemon
# 44 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	releaseall
# 45 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	end
# 46 "data/maps/SealedChamber_InnerRoom/scripts.pory"

# 47 "data/maps/SealedChamber_InnerRoom/scripts.pory"
SealedChamber_InnerRoom_EventScript_BrailleStoryPart3::
# 48 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	lockall
# 49 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	braillemsgbox SealedChamber_InnerRoom_Braille_ButWeSealedThePokemonAway
# 50 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	releaseall
# 51 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	end
# 52 "data/maps/SealedChamber_InnerRoom/scripts.pory"

# 53 "data/maps/SealedChamber_InnerRoom/scripts.pory"
SealedChamber_InnerRoom_EventScript_BrailleStoryPart4::
# 54 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	lockall
# 55 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	braillemsgbox SealedChamber_InnerRoom_Braille_WeFearedIt
# 56 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	releaseall
# 57 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	end
# 58 "data/maps/SealedChamber_InnerRoom/scripts.pory"

# 59 "data/maps/SealedChamber_InnerRoom/scripts.pory"
SealedChamber_InnerRoom_EventScript_BrailleStoryPart5::
# 60 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	lockall
# 61 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	braillemsgbox SealedChamber_InnerRoom_Braille_ThoseWithCourageHope
# 62 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	releaseall
# 63 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	end
# 64 "data/maps/SealedChamber_InnerRoom/scripts.pory"

# 65 "data/maps/SealedChamber_InnerRoom/scripts.pory"
SealedChamber_InnerRoom_EventScript_BrailleStoryPart6::
# 66 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	lockall
# 67 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	braillemsgbox SealedChamber_InnerRoom_Braille_OpenDoorEternalPokemonWaits
# 68 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	releaseall
# 69 "data/maps/SealedChamber_InnerRoom/scripts.pory"
	end
