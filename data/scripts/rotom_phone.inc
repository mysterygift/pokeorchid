@ Orchid: the Rotom Phone tells the player about quest changes (MSGBOX_ROTOM: Rotom's cry + a message box).
@ The quest macros in asm/macros/event.inc buffer the quest's name into STR_VAR_1 and print one of these.

@ src/research.c Research_Update: a catch finished one or more of Palm's research tasks.
Rotom_EventScript_ResearchTaskDone::
	lockall
	msgbox gText_Rotom_ResearchTaskDone, MSGBOX_ROTOM
	closemessage
	releaseall
	end

gText_Rotom_QuestStarted::
	.string "Bzzt! New quest added to QUESTS:\n“{STR_VAR_1}”!$"

gText_Rotom_QuestUnlocked::
	.string "Bzzt! New quest unlocked:\n“{STR_VAR_1}”!$"

gText_Rotom_QuestReward::
	.string "Bzzt! Reward ready in QUESTS:\n“{STR_VAR_1}”!$"

gText_Rotom_QuestComplete::
	.string "Bzzt! Quest complete:\n“{STR_VAR_1}”!$"

gText_Rotom_QuestUpdated::
	.string "Bzzt! Quest updated:\n“{STR_VAR_1}”!$"

gText_Rotom_ResearchTaskDone::
	.string "Bzzt! A research task is done!\nClaim the reward in QUESTS!$"
