HawkerCentreTest_MapScripts::
	.byte 0

HawkerCentreTest_EventScript_Curry::
	msgbox HawkerCentreTest_Text_Curry, MSGBOX_NPC
	end

HawkerCentreTest_EventScript_HokkienMee::
	msgbox HawkerCentreTest_Text_HokkienMee, MSGBOX_NPC
	end

HawkerCentreTest_EventScript_Crab::
	msgbox HawkerCentreTest_Text_Crab, MSGBOX_NPC
	end

HawkerCentreTest_EventScript_ChickenRice::
	msgbox HawkerCentreTest_Text_ChickenRice, MSGBOX_NPC
	end

HawkerCentreTest_EventScript_Satay::
	msgbox HawkerCentreTest_Text_Satay, MSGBOX_NPC
	end

HawkerCentreTest_EventScript_IceKachang::
	msgbox HawkerCentreTest_Text_IceKachang, MSGBOX_NPC
	end

HawkerCentreTest_EventScript_Diner1::
	msgbox HawkerCentreTest_Text_Diner1, MSGBOX_NPC
	end

HawkerCentreTest_EventScript_Diner2::
	msgbox HawkerCentreTest_Text_Diner2, MSGBOX_NPC
	end

HawkerCentreTest_EventScript_Diner3::
	msgbox HawkerCentreTest_Text_Diner3, MSGBOX_NPC
	end

HawkerCentreTest_EventScript_Diner4::
	msgbox HawkerCentreTest_Text_Diner4, MSGBOX_NPC
	end

HawkerCentreTest_EventScript_Diner5::
	msgbox HawkerCentreTest_Text_Diner5, MSGBOX_NPC
	end

HawkerCentreTest_EventScript_Diner6::
	msgbox HawkerCentreTest_Text_Diner6, MSGBOX_NPC
	end

HawkerCentreTest_EventScript_Queue::
	msgbox HawkerCentreTest_Text_Queue, MSGBOX_NPC
	end

HawkerCentreTest_EventScript_Berry::
	lock
	faceplayer
	message HawkerCentreTest_Text_Berry
	waitmessage
	pokemart HawkerCentreTest_Mart_Berry
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
HawkerCentreTest_Mart_Berry:
	.2byte ITEM_ORAN_BERRY
	.2byte ITEM_PECHA_BERRY
	.2byte ITEM_CHERI_BERRY
	.2byte ITEM_SITRUS_BERRY
	.2byte ITEM_NONE
	release
	end

HawkerCentreTest_EventScript_Kopi::
	lock
	faceplayer
	message HawkerCentreTest_Text_Kopi
	waitmessage
	pokemart HawkerCentreTest_Mart_Kopi
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
HawkerCentreTest_Mart_Kopi:
	.2byte ITEM_FRESH_WATER
	.2byte ITEM_SODA_POP
	.2byte ITEM_LEMONADE
	.2byte ITEM_MOOMOO_MILK
	.2byte ITEM_NONE
	release
	end

HawkerCentreTest_Text_Curry:
	.string "Fish head curry, rendang, sayur\n"
	.string "lodeh… Point at what you like!$"

HawkerCentreTest_Text_HokkienMee:
	.string "Hokkien mee! Fried over a big\n"
	.string "flame, with prawns and lime.$"

HawkerCentreTest_Text_Crab:
	.string "Soft-shell crab, fresh from the\n"
	.string "port this morning!$"

HawkerCentreTest_Text_ChickenRice:
	.string "Chicken rice. Roasted or steamed?\p"
	.string "The chilli is the secret.$"

HawkerCentreTest_Text_Satay:
	.string "Satay! Ten sticks, peanut sauce,\n"
	.string "ketupat on the side.$"

HawkerCentreTest_Text_IceKachang:
	.string "Ice kachang! Nothing better when\n"
	.string "the afternoon gets hot.$"

HawkerCentreTest_Text_Diner1:
	.string "I come here every day for lunch.\n"
	.string "The kopi uncle knows my order.$"

HawkerCentreTest_Text_Diner2:
	.string "With no walls, the breeze comes\n"
	.string "right through. Very shiok.$"

HawkerCentreTest_Text_Diner3:
	.string "My POKéMON only eats BERRIES from\n"
	.string "the stall in the corner.$"

HawkerCentreTest_Text_Diner4:
	.string "This laksa is too spicy…\n"
	.string "But I can't stop eating it!$"

HawkerCentreTest_Text_Diner5:
	.string "See a packet of tissues on a table?\p"
	.string "That seat is taken. We call it\n"
	.string "“chope”.$"

HawkerCentreTest_Text_Diner6:
	.string "Clear your tray when you're done!\n"
	.string "The rack is by the entrance.$"

HawkerCentreTest_Text_Queue:
	.string "The queue here is always the\n"
	.string "longest. That's how you know.$"

HawkerCentreTest_Text_Berry:
	.string "Berries for your POKéMON!\n"
	.string "All picked this week.$"

HawkerCentreTest_Text_Kopi:
	.string "Kopi? Teh? Something cold?$"
