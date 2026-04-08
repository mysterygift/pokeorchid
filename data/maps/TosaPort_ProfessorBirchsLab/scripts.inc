# 1 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"

# 2 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"
TosaPort_ProfessorBirchsLab_MapScripts::
# 3 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, TosaPort_ProfessorBirchsLab_OnTransition
# 4 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"
	.byte 0
# 5 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"

# 6 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"
TosaPort_ProfessorBirchsLab_OnTransition:
# 7 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"
	call Common_EventScript_SetupRivalGfxId
# 8 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"
	end
# 9 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"

# 10 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"
TosaPort_ProfessorBirchsLab_EventScript_Machine::
# 11 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"
	msgbox TosaPort_ProfessorBirchsLab_Text_SeriousLookingMachine, MSGBOX_SIGN
# 12 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"
	end
# 13 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"

# 14 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"
TosaPort_ProfessorBirchsLab_EventScript_PC::
# 15 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"
	msgbox TosaPort_ProfessorBirchsLab_Text_PCUsedForResearch, MSGBOX_SIGN
# 16 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"
	end
# 17 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"

# 18 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"
TosaPort_ProfessorBirchsLab_EventScript_Bookshelf::
# 19 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"
	msgbox TosaPort_ProfessorBirchsLab_Text_CrammedWithBooksOnPokemon, MSGBOX_SIGN
# 20 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"
	end
# 21 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"

# 22 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"
TosaPort_ProfessorBirchsLab_EventScript_Book::
# 23 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"
	msgbox TosaPort_ProfessorBirchsLab_Text_BookTooHardToRead, MSGBOX_SIGN
# 24 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"
	end
# 25 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"

# 26 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"
TosaPort_ProfessorBirchsLab_Text_SeriousLookingMachine:
# 27 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"
	.string "It's a serious-looking machine.\n"
# 28 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"
	.string "The PROF must use this for research.$"
# 29 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"

# 30 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"
TosaPort_ProfessorBirchsLab_Text_PCUsedForResearch:
# 31 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"
	.string "It's a PC used for research.\n"
# 32 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"
	.string "Better not mess around with it.$"
# 33 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"

# 34 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"
TosaPort_ProfessorBirchsLab_Text_CrammedWithBooksOnPokemon:
# 35 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"
	.string "It's crammed with books on POKéMON.$"
# 36 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"

# 37 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"
TosaPort_ProfessorBirchsLab_Text_BookTooHardToRead:
# 38 "data/maps/TosaPort_ProfessorBirchsLab/scripts.pory"
	.string "It's a book that's too hard to read.$"
