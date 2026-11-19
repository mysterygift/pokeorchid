HolonResearchTower_2F_MapScripts::
	.byte 0


HolonResearchTower_2F_EventScript_Faba::
# 8 "data/maps/HolonResearchTower_2F/scripts.pory"
	trainerbattle_single TRAINER_HOLON_FABA, HolonResearchTower_2F_Text_FabaIntro, HolonResearchTower_2F_Text_FabaDefeat, HolonResearchTower_2F_EventScript_FabaDefeated
# 9 "data/maps/HolonResearchTower_2F/scripts.pory"
	msgbox HolonResearchTower_2F_Text_FabaPost, MSGBOX_AUTOCLOSE
	return


HolonResearchTower_2F_EventScript_FabaDefeated::
# 13 "data/maps/HolonResearchTower_2F/scripts.pory"
	msgbox HolonResearchTower_2F_Text_FabaPost, MSGBOX_DEFAULT
# 14 "data/maps/HolonResearchTower_2F/scripts.pory"
	closemessage
# 15 "data/maps/HolonResearchTower_2F/scripts.pory"
	setflag FLAG_HOLON_FABA_DEFEATED
# 16 "data/maps/HolonResearchTower_2F/scripts.pory"
	setflag FLAG_HOLON_POWER_SPOTS_HEALED
# 17 "data/maps/HolonResearchTower_2F/scripts.pory"
	fadescreen FADE_TO_BLACK
# 18 "data/maps/HolonResearchTower_2F/scripts.pory"
	removeobject LOCALID_HOLON_FABA
# 19 "data/maps/HolonResearchTower_2F/scripts.pory"
	fadescreen FADE_FROM_BLACK
# 20 "data/maps/HolonResearchTower_2F/scripts.pory"
	release
	end


HolonResearchTower_2F_EventScript_Researcher1::
# 37 "data/maps/HolonResearchTower_2F/scripts.pory"
	trainerbattle_single TRAINER_HOLON_TOBIAS, HolonResearchTower_2F_Text_Researcher1Intro, HolonResearchTower_2F_Text_Researcher1Defeat
# 38 "data/maps/HolonResearchTower_2F/scripts.pory"
	goto_if_set FLAG_HOLON_FABA_DEFEATED, HolonResearchTower_2F_EventScript_Researcher1_1
# 41 "data/maps/HolonResearchTower_2F/scripts.pory"
	msgbox HolonResearchTower_2F_Text_Researcher1Post, MSGBOX_AUTOCLOSE
	return

HolonResearchTower_2F_EventScript_Researcher1_1:
# 39 "data/maps/HolonResearchTower_2F/scripts.pory"
	msgbox HolonResearchTower_2F_EventScript_Researcher1_Text_0, MSGBOX_AUTOCLOSE
	return


HolonResearchTower_2F_EventScript_Researcher2::
# 58 "data/maps/HolonResearchTower_2F/scripts.pory"
	trainerbattle_single TRAINER_HOLON_KENJI, HolonResearchTower_2F_Text_Researcher2Intro, HolonResearchTower_2F_Text_Researcher2Defeat
# 59 "data/maps/HolonResearchTower_2F/scripts.pory"
	goto_if_set FLAG_HOLON_FABA_DEFEATED, HolonResearchTower_2F_EventScript_Researcher2_1
# 62 "data/maps/HolonResearchTower_2F/scripts.pory"
	msgbox HolonResearchTower_2F_Text_Researcher2Post, MSGBOX_AUTOCLOSE
	return

HolonResearchTower_2F_EventScript_Researcher2_1:
# 60 "data/maps/HolonResearchTower_2F/scripts.pory"
	msgbox HolonResearchTower_2F_EventScript_Researcher2_Text_0, MSGBOX_AUTOCLOSE
	return


HolonResearchTower_2F_EventScript_Npc::
# 79 "data/maps/HolonResearchTower_2F/scripts.pory"
	goto_if_set FLAG_HOLON_FABA_DEFEATED, HolonResearchTower_2F_EventScript_Npc_1
# 82 "data/maps/HolonResearchTower_2F/scripts.pory"
	msgbox HolonResearchTower_2F_EventScript_Npc_Text_1, MSGBOX_NPC
	return

HolonResearchTower_2F_EventScript_Npc_1:
# 80 "data/maps/HolonResearchTower_2F/scripts.pory"
	msgbox HolonResearchTower_2F_EventScript_Npc_Text_0, MSGBOX_NPC
	return


# 85 "data/maps/HolonResearchTower_2F/scripts.pory"

# 86 "data/maps/HolonResearchTower_2F/scripts.pory"
HolonResearchTower_2F_EventScript_HeadOfResearch::
# 87 "data/maps/HolonResearchTower_2F/scripts.pory"
	lock
# 88 "data/maps/HolonResearchTower_2F/scripts.pory"
	faceplayer
# 89 "data/maps/HolonResearchTower_2F/scripts.pory"
	goto_if_set FLAG_HOLON_RECEIVED_EEVEE, HolonResearchTower_2F_EventScript_HeadAfter
# 90 "data/maps/HolonResearchTower_2F/scripts.pory"
	goto_if_unset FLAG_HOLON_FABA_DEFEATED, HolonResearchTower_2F_EventScript_HeadNotNow
# 91 "data/maps/HolonResearchTower_2F/scripts.pory"
	msgbox HolonResearchTower_2F_Text_HeadOffer, MSGBOX_YESNO
# 92 "data/maps/HolonResearchTower_2F/scripts.pory"
	goto_if_eq VAR_RESULT, NO, HolonResearchTower_2F_EventScript_HeadDeclined
# 93 "data/maps/HolonResearchTower_2F/scripts.pory"
	@ TODO(delta): SPECIES_EEVEE -> SPECIES_EEVEE_DELTA (Eevee-δ gift, Lv 50)
# 94 "data/maps/HolonResearchTower_2F/scripts.pory"
	setvar VAR_TEMP_TRANSFERRED_SPECIES, SPECIES_EEVEE_DELTA
# 95 "data/maps/HolonResearchTower_2F/scripts.pory"
	givemon SPECIES_EEVEE_DELTA, 50
# 96 "data/maps/HolonResearchTower_2F/scripts.pory"
	goto_if_eq VAR_RESULT, MON_GIVEN_TO_PARTY, HolonResearchTower_2F_EventScript_EeveeParty
# 97 "data/maps/HolonResearchTower_2F/scripts.pory"
	goto_if_eq VAR_RESULT, MON_GIVEN_TO_PC, HolonResearchTower_2F_EventScript_EeveePC
# 98 "data/maps/HolonResearchTower_2F/scripts.pory"
	goto Common_EventScript_NoMoreRoomForPokemon
# 99 "data/maps/HolonResearchTower_2F/scripts.pory"
	end
# 100 "data/maps/HolonResearchTower_2F/scripts.pory"

# 101 "data/maps/HolonResearchTower_2F/scripts.pory"
HolonResearchTower_2F_EventScript_EeveeParty::
# 102 "data/maps/HolonResearchTower_2F/scripts.pory"
	call HolonResearchTower_2F_EventScript_EeveeFanfare
# 103 "data/maps/HolonResearchTower_2F/scripts.pory"
	msgbox gText_NicknameThisPokemon, MSGBOX_YESNO
# 104 "data/maps/HolonResearchTower_2F/scripts.pory"
	goto_if_eq VAR_RESULT, NO, HolonResearchTower_2F_EventScript_EeveeDone
# 105 "data/maps/HolonResearchTower_2F/scripts.pory"
	call Common_EventScript_GetGiftMonPartySlot
# 106 "data/maps/HolonResearchTower_2F/scripts.pory"
	call Common_EventScript_NameReceivedPartyMon
# 107 "data/maps/HolonResearchTower_2F/scripts.pory"
	goto HolonResearchTower_2F_EventScript_EeveeDone
# 108 "data/maps/HolonResearchTower_2F/scripts.pory"
	end
# 109 "data/maps/HolonResearchTower_2F/scripts.pory"

# 110 "data/maps/HolonResearchTower_2F/scripts.pory"
HolonResearchTower_2F_EventScript_EeveePC::
# 111 "data/maps/HolonResearchTower_2F/scripts.pory"
	call HolonResearchTower_2F_EventScript_EeveeFanfare
# 112 "data/maps/HolonResearchTower_2F/scripts.pory"
	msgbox gText_NicknameThisPokemon, MSGBOX_YESNO
# 113 "data/maps/HolonResearchTower_2F/scripts.pory"
	goto_if_eq VAR_RESULT, NO, HolonResearchTower_2F_EventScript_EeveeToPC
# 114 "data/maps/HolonResearchTower_2F/scripts.pory"
	call Common_EventScript_NameReceivedBoxMon
# 115 "data/maps/HolonResearchTower_2F/scripts.pory"
	goto HolonResearchTower_2F_EventScript_EeveeToPC
# 116 "data/maps/HolonResearchTower_2F/scripts.pory"
	end
# 117 "data/maps/HolonResearchTower_2F/scripts.pory"

# 118 "data/maps/HolonResearchTower_2F/scripts.pory"
HolonResearchTower_2F_EventScript_EeveeToPC::
# 119 "data/maps/HolonResearchTower_2F/scripts.pory"
	call Common_EventScript_TransferredToPC
# 120 "data/maps/HolonResearchTower_2F/scripts.pory"
	goto HolonResearchTower_2F_EventScript_EeveeDone
# 121 "data/maps/HolonResearchTower_2F/scripts.pory"
	end
# 122 "data/maps/HolonResearchTower_2F/scripts.pory"

# 123 "data/maps/HolonResearchTower_2F/scripts.pory"
HolonResearchTower_2F_EventScript_EeveeFanfare::
# 124 "data/maps/HolonResearchTower_2F/scripts.pory"
	bufferspeciesname STR_VAR_1, SPECIES_EEVEE_DELTA
# 125 "data/maps/HolonResearchTower_2F/scripts.pory"
	playfanfare MUS_OBTAIN_ITEM
# 126 "data/maps/HolonResearchTower_2F/scripts.pory"
	message HolonResearchTower_2F_Text_ReceivedEevee
# 127 "data/maps/HolonResearchTower_2F/scripts.pory"
	waitmessage
# 128 "data/maps/HolonResearchTower_2F/scripts.pory"
	waitfanfare
# 129 "data/maps/HolonResearchTower_2F/scripts.pory"
	return
# 130 "data/maps/HolonResearchTower_2F/scripts.pory"

# 131 "data/maps/HolonResearchTower_2F/scripts.pory"
HolonResearchTower_2F_EventScript_EeveeDone::
# 132 "data/maps/HolonResearchTower_2F/scripts.pory"
	setflag FLAG_HOLON_RECEIVED_EEVEE
# 133 "data/maps/HolonResearchTower_2F/scripts.pory"
	msgbox HolonResearchTower_2F_Text_HeadAfter, MSGBOX_DEFAULT
# 134 "data/maps/HolonResearchTower_2F/scripts.pory"
	release
# 135 "data/maps/HolonResearchTower_2F/scripts.pory"
	end
# 136 "data/maps/HolonResearchTower_2F/scripts.pory"

# 137 "data/maps/HolonResearchTower_2F/scripts.pory"
HolonResearchTower_2F_EventScript_HeadDeclined::
# 138 "data/maps/HolonResearchTower_2F/scripts.pory"
	msgbox HolonResearchTower_2F_Text_HeadDeclined, MSGBOX_DEFAULT
# 139 "data/maps/HolonResearchTower_2F/scripts.pory"
	release
# 140 "data/maps/HolonResearchTower_2F/scripts.pory"
	end
# 141 "data/maps/HolonResearchTower_2F/scripts.pory"

# 142 "data/maps/HolonResearchTower_2F/scripts.pory"
HolonResearchTower_2F_EventScript_HeadAfter::
# 143 "data/maps/HolonResearchTower_2F/scripts.pory"
	msgbox HolonResearchTower_2F_Text_HeadAfter, MSGBOX_DEFAULT
# 144 "data/maps/HolonResearchTower_2F/scripts.pory"
	release
# 145 "data/maps/HolonResearchTower_2F/scripts.pory"
	end
# 146 "data/maps/HolonResearchTower_2F/scripts.pory"

# 147 "data/maps/HolonResearchTower_2F/scripts.pory"
@ Wavebreak Voyages: the Eevee-delta gift waits until Faba is beaten.
# 148 "data/maps/HolonResearchTower_2F/scripts.pory"
HolonResearchTower_2F_EventScript_HeadNotNow::
# 149 "data/maps/HolonResearchTower_2F/scripts.pory"
	msgbox HolonResearchTower_2F_Text_HeadNotNow, MSGBOX_DEFAULT
# 150 "data/maps/HolonResearchTower_2F/scripts.pory"
	release
# 151 "data/maps/HolonResearchTower_2F/scripts.pory"
	end

HolonResearchTower_2F_EventScript_Machine::
# 175 "data/maps/HolonResearchTower_2F/scripts.pory"
	goto_if_set FLAG_HOLON_FABA_DEFEATED, HolonResearchTower_2F_EventScript_Machine_1
# 178 "data/maps/HolonResearchTower_2F/scripts.pory"
	msgbox HolonResearchTower_2F_EventScript_Machine_Text_1, MSGBOX_SIGN
	return

HolonResearchTower_2F_EventScript_Machine_1:
# 176 "data/maps/HolonResearchTower_2F/scripts.pory"
	msgbox HolonResearchTower_2F_EventScript_Machine_Text_0, MSGBOX_SIGN
	return


HolonResearchTower_2F_EventScript_Researcher1_Text_0:
# 39 "data/maps/HolonResearchTower_2F/scripts.pory"
	.string "The machines are off. Our Delta\n"
	.string "research will slow down without that\l"
	.string "energy... Maybe that's for the best.$"

HolonResearchTower_2F_EventScript_Researcher2_Text_0:
# 60 "data/maps/HolonResearchTower_2F/scripts.pory"
	.string "Faba's gone and the machines are quiet.\n"
	.string "The farmers should see their fields\l"
	.string "green up again soon.$"

HolonResearchTower_2F_EventScript_Npc_Text_0:
# 80 "data/maps/HolonResearchTower_2F/scripts.pory"
	.string "We've shut the round machines down.\n"
	.string "Faba never told us how much he was\l"
	.string "really draining.$"

HolonResearchTower_2F_EventScript_Npc_Text_1:
# 82 "data/maps/HolonResearchTower_2F/scripts.pory"
	.string "Those round machines store the energy\n"
	.string "we draw from the Power Spot. Please\l"
	.string "don't touch them!$"

HolonResearchTower_2F_EventScript_Machine_Text_0:
# 176 "data/maps/HolonResearchTower_2F/scripts.pory"
	.string "The round machine is silent. The stored\n"
	.string "energy is draining back into the ground.$"

HolonResearchTower_2F_EventScript_Machine_Text_1:
# 178 "data/maps/HolonResearchTower_2F/scripts.pory"
	.string "A round machine humming with stored\n"
	.string "energy.$"

HolonResearchTower_2F_Text_FabaIntro::
# 24 "data/maps/HolonResearchTower_2F/scripts.pory"
	.string "Ah, the tourist. You've seen the fields?\n"
	.string "Wilted, yes. A small price.\p"
	.string "Every Power Spot on Holon flows into\n"
	.string "these machines. With that energy, my\l"
	.string "Delta Pokémon will rival any legend!\p"
	.string "I am Holon Leader Faba, and no child is\n"
	.string "pulling the plug!$"

HolonResearchTower_2F_Text_FabaDefeat::
# 28 "data/maps/HolonResearchTower_2F/scripts.pory"
	.string "Impossible! My calculations were\n"
	.string "flawless!$"

HolonResearchTower_2F_Text_FabaPost::
# 32 "data/maps/HolonResearchTower_2F/scripts.pory"
	.string "Fine! Shut the machines down! The Power\n"
	.string "Spots will refill... eventually.\p"
	.string "But Holon WILL remember Faba!$"

HolonResearchTower_2F_Text_Researcher1Intro::
# 45 "data/maps/HolonResearchTower_2F/scripts.pory"
	.string "Authorised staff only past this point!$"

HolonResearchTower_2F_Text_Researcher1Defeat::
# 49 "data/maps/HolonResearchTower_2F/scripts.pory"
	.string "I suppose you've earned a look.$"

HolonResearchTower_2F_Text_Researcher1Post::
# 53 "data/maps/HolonResearchTower_2F/scripts.pory"
	.string "Every machine on this floor stores\n"
	.string "energy drawn from the Power Spot.$"

HolonResearchTower_2F_Text_Researcher2Intro::
# 66 "data/maps/HolonResearchTower_2F/scripts.pory"
	.string "Want to see what a Delta Pokémon can do\n"
	.string "on a full charge?$"

HolonResearchTower_2F_Text_Researcher2Defeat::
# 70 "data/maps/HolonResearchTower_2F/scripts.pory"
	.string "Overloaded... and I lost anyway.$"

HolonResearchTower_2F_Text_Researcher2Post::
# 74 "data/maps/HolonResearchTower_2F/scripts.pory"
	.string "Our head of research says the drain is\n"
	.string "temporary. The farmers don't believe\l"
	.string "her.$"

HolonResearchTower_2F_Text_HeadNotNow::
# 154 "data/maps/HolonResearchTower_2F/scripts.pory"
	.string "I'm the head of research here. Forgive\n"
	.string "me, I can't think about anything but\l"
	.string "those machines right now.\p"
	.string "Faba is draining every Power Spot on\n"
	.string "Holon, and he won't listen to a word I\l"
	.string "say.\p"
	.string "If someone could stop him... I'd have\n"
	.string "something to give them.$"

HolonResearchTower_2F_Text_HeadOffer::
# 158 "data/maps/HolonResearchTower_2F/scripts.pory"
	.string "You stopped Faba! Thank you. The Power\n"
	.string "Spots can finally recover.\p"
	.string "You've come a long way to see Holon, and\n"
	.string "I have something for you.\p"
	.string "This Eevee was born right beside the\n"
	.string "Power Spot. Its type shifted as it grew.\l"
	.string "A Delta Species!\p"
	.string "We can't give it the attention it\n"
	.string "deserves. Would you take care of it?$"

HolonResearchTower_2F_Text_HeadDeclined::
# 162 "data/maps/HolonResearchTower_2F/scripts.pory"
	.string "I see. If you change your mind, I'll be\n"
	.string "here.$"

HolonResearchTower_2F_Text_HeadAfter::
# 166 "data/maps/HolonResearchTower_2F/scripts.pory"
	.string "Delta Species are proof of how much\n"
	.string "power sleeps under Holon. Raise that\l"
	.string "Eevee well.$"

HolonResearchTower_2F_Text_ReceivedEevee::
# 170 "data/maps/HolonResearchTower_2F/scripts.pory"
	.string "{PLAYER} received {STR_VAR_1}!$"
