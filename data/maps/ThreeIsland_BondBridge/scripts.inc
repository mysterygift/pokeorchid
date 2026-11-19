ThreeIsland_BondBridge_MapScripts::
	.byte 0


ThreeIsland_BondBridge_EventScript_Nikki::
# 4 "data/maps/ThreeIsland_BondBridge/scripts.pory"
	trainerbattle_single TRAINER_SEVII_NIKKI, ThreeIsland_BondBridge_Text_NikkiIntro, ThreeIsland_BondBridge_Text_NikkiDefeat
# 5 "data/maps/ThreeIsland_BondBridge/scripts.pory"
	msgbox ThreeIsland_BondBridge_Text_NikkiPost, MSGBOX_AUTOCLOSE
	return


ThreeIsland_BondBridge_EventScript_Violet::
# 21 "data/maps/ThreeIsland_BondBridge/scripts.pory"
	msgbox ThreeIsland_BondBridge_EventScript_Violet_Text_0, MSGBOX_NPC
	return


ThreeIsland_BondBridge_EventScript_Amira::
# 25 "data/maps/ThreeIsland_BondBridge/scripts.pory"
	trainerbattle_single TRAINER_SEVII_AMIRA, ThreeIsland_BondBridge_Text_AmiraIntro, ThreeIsland_BondBridge_Text_AmiraDefeat
# 26 "data/maps/ThreeIsland_BondBridge/scripts.pory"
	msgbox ThreeIsland_BondBridge_Text_AmiraPost, MSGBOX_AUTOCLOSE
	return


ThreeIsland_BondBridge_EventScript_Alexis::
# 42 "data/maps/ThreeIsland_BondBridge/scripts.pory"
	msgbox ThreeIsland_BondBridge_EventScript_Alexis_Text_0, MSGBOX_NPC
	return


ThreeIsland_BondBridge_EventScript_Tisha::
# 46 "data/maps/ThreeIsland_BondBridge/scripts.pory"
	trainerbattle_single TRAINER_SEVII_TISHA, ThreeIsland_BondBridge_Text_TishaIntro, ThreeIsland_BondBridge_Text_TishaDefeat
# 47 "data/maps/ThreeIsland_BondBridge/scripts.pory"
	msgbox ThreeIsland_BondBridge_Text_TishaPost, MSGBOX_AUTOCLOSE
	return


ThreeIsland_BondBridge_EventScript_Joy::
# 63 "data/maps/ThreeIsland_BondBridge/scripts.pory"
	msgbox ThreeIsland_BondBridge_EventScript_Joy_Text_0, MSGBOX_NPC
	return


ThreeIsland_BondBridge_EventScript_Meg::
# 67 "data/maps/ThreeIsland_BondBridge/scripts.pory"
	msgbox ThreeIsland_BondBridge_EventScript_Meg_Text_0, MSGBOX_NPC
	return


ThreeIsland_BondBridge_EventScript_BerryForestSign::
# 71 "data/maps/ThreeIsland_BondBridge/scripts.pory"
	msgbox ThreeIsland_BondBridge_EventScript_BerryForestSign_Text_0, MSGBOX_SIGN
	return


ThreeIsland_BondBridge_EventScript_BondBridgeSign::
# 76 "data/maps/ThreeIsland_BondBridge/scripts.pory"
	msgbox ThreeIsland_BondBridge_EventScript_BondBridgeSign_Text_0, MSGBOX_SIGN
	return


ThreeIsland_BondBridge_EventScript_Violet_Text_0:
# 21 "data/maps/ThreeIsland_BondBridge/scripts.pory"
	.string "The sunsets out here are something\n"
	.string "special.$"

ThreeIsland_BondBridge_EventScript_Alexis_Text_0:
# 42 "data/maps/ThreeIsland_BondBridge/scripts.pory"
	.string "I'm gonna be the best trainer in all\n"
	.string "seven islands!$"

ThreeIsland_BondBridge_EventScript_Joy_Text_0:
# 63 "data/maps/ThreeIsland_BondBridge/scripts.pory"
	.string "Bond Bridge is a lovely spot for a stroll\n"
	.string "with your partner.$"

ThreeIsland_BondBridge_EventScript_Meg_Text_0:
# 67 "data/maps/ThreeIsland_BondBridge/scripts.pory"
	.string "Berry Forest is at the end of the\n"
	.string "bridge.$"

ThreeIsland_BondBridge_EventScript_BerryForestSign_Text_0:
# 71 "data/maps/ThreeIsland_BondBridge/scripts.pory"
	.string "BERRY FOREST\n"
	.string "Keep to the paths. Wild POKéMON gather\l"
	.string "here for Berries.$"

ThreeIsland_BondBridge_EventScript_BondBridgeSign_Text_0:
# 76 "data/maps/ThreeIsland_BondBridge/scripts.pory"
	.string "BOND BRIDGE\n"
	.string "A place where friendships are tested\l"
	.string "and made.$"

ThreeIsland_BondBridge_Text_NikkiIntro::
# 8 "data/maps/ThreeIsland_BondBridge/scripts.pory"
	.string "Breathe in the sea breeze... then\n"
	.string "battle!$"

ThreeIsland_BondBridge_Text_NikkiDefeat::
# 12 "data/maps/ThreeIsland_BondBridge/scripts.pory"
	.string "What a sour ending.$"

ThreeIsland_BondBridge_Text_NikkiPost::
# 16 "data/maps/ThreeIsland_BondBridge/scripts.pory"
	.string "Each island has its own character. Have\n"
	.string "you visited them all?$"

ThreeIsland_BondBridge_Text_AmiraIntro::
# 29 "data/maps/ThreeIsland_BondBridge/scripts.pory"
	.string "My float ring and I are ready!$"

ThreeIsland_BondBridge_Text_AmiraDefeat::
# 33 "data/maps/ThreeIsland_BondBridge/scripts.pory"
	.string "Waaah! I lost!$"

ThreeIsland_BondBridge_Text_AmiraPost::
# 37 "data/maps/ThreeIsland_BondBridge/scripts.pory"
	.string "Bond Bridge is a lovely spot for a stroll\n"
	.string "with your partner.$"

ThreeIsland_BondBridge_Text_TishaIntro::
# 50 "data/maps/ThreeIsland_BondBridge/scripts.pory"
	.string "Swimming under Bond Bridge is the best!$"

ThreeIsland_BondBridge_Text_TishaDefeat::
# 54 "data/maps/ThreeIsland_BondBridge/scripts.pory"
	.string "I'm all washed up.$"

ThreeIsland_BondBridge_Text_TishaPost::
# 58 "data/maps/ThreeIsland_BondBridge/scripts.pory"
	.string "The water around the Sevii Islands is\n"
	.string "so clear!$"
