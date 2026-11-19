Common_EventScript_CynthiaHolonLake::
# 13 "data/scripts/cynthia.pory"
	lock
# 14 "data/scripts/cynthia.pory"
	faceplayer
# 15 "data/scripts/cynthia.pory"
	playbgm MUS_ORCHID_ENCOUNTER_CYNTHIA, FALSE
# 16 "data/scripts/cynthia.pory"
	msgbox Common_EventScript_CynthiaHolonLake_Text_0, MSGBOX_YESNO
# 17 "data/scripts/cynthia.pory"
	compare VAR_RESULT, NO
	goto_if_eq Common_EventScript_CynthiaHolonLake_2
# 23 "data/scripts/cynthia.pory"
	msgbox Common_EventScript_CynthiaHolonLake_Text_2, MSGBOX_DEFAULT
# 24 "data/scripts/cynthia.pory"
	trainerbattle_no_intro TRAINER_CYNTHIA_LAKE, Common_EventScript_CynthiaHolonLake_Text_3
# 25 "data/scripts/cynthia.pory"
	msgbox Common_EventScript_CynthiaHolonLake_Text_4, MSGBOX_DEFAULT
# 26 "data/scripts/cynthia.pory"
	setflag FLAG_CYNTHIA_BEATEN_AT_LAKE
# 27 "data/scripts/cynthia.pory"
	fadescreen FADE_TO_BLACK
# 28 "data/scripts/cynthia.pory"
	removeobject VAR_LAST_TALKED
# 29 "data/scripts/cynthia.pory"
	fadescreen FADE_FROM_BLACK
# 30 "data/scripts/cynthia.pory"
	fadedefaultbgm
# 31 "data/scripts/cynthia.pory"
	release
	end

Common_EventScript_CynthiaHolonLake_2:
# 18 "data/scripts/cynthia.pory"
	msgbox Common_EventScript_CynthiaHolonLake_Text_1, MSGBOX_DEFAULT
# 19 "data/scripts/cynthia.pory"
	fadedefaultbgm
# 20 "data/scripts/cynthia.pory"
	release
	end


Common_EventScript_CynthiaCafe::
# 36 "data/scripts/cynthia.pory"
	lock
# 37 "data/scripts/cynthia.pory"
	faceplayer
# 38 "data/scripts/cynthia.pory"
	specialvar VAR_RESULT, IsCynthiaCafeRematchAvailable
# 39 "data/scripts/cynthia.pory"
	compare VAR_RESULT, FALSE
	goto_if_eq Common_EventScript_CynthiaCafe_2
# 44 "data/scripts/cynthia.pory"
	msgbox Common_EventScript_CynthiaCafe_Text_1, MSGBOX_YESNO
# 45 "data/scripts/cynthia.pory"
	compare VAR_RESULT, NO
	goto_if_eq Common_EventScript_CynthiaCafe_5
# 50 "data/scripts/cynthia.pory"
	playbgm MUS_ORCHID_ENCOUNTER_CYNTHIA, FALSE
# 51 "data/scripts/cynthia.pory"
	msgbox Common_EventScript_CynthiaCafe_Text_3, MSGBOX_DEFAULT
# 52 "data/scripts/cynthia.pory"
	cleartrainerflag TRAINER_CYNTHIA_CAFE
# 53 "data/scripts/cynthia.pory"
	trainerbattle_no_intro TRAINER_CYNTHIA_CAFE, Common_EventScript_CynthiaCafe_Text_4
# 54 "data/scripts/cynthia.pory"
	special SetCynthiaCafeRematchDay
# 55 "data/scripts/cynthia.pory"
	msgbox Common_EventScript_CynthiaCafe_Text_0, MSGBOX_DEFAULT
# 56 "data/scripts/cynthia.pory"
	fadedefaultbgm
# 57 "data/scripts/cynthia.pory"
	release
	end

Common_EventScript_CynthiaCafe_2:
# 40 "data/scripts/cynthia.pory"
	msgbox Common_EventScript_CynthiaCafe_Text_0, MSGBOX_DEFAULT
# 41 "data/scripts/cynthia.pory"
	release
	end

Common_EventScript_CynthiaCafe_5:
# 46 "data/scripts/cynthia.pory"
	msgbox Common_EventScript_CynthiaCafe_Text_2, MSGBOX_DEFAULT
# 47 "data/scripts/cynthia.pory"
	release
	end


Common_EventScript_CynthiaHolonLake_Text_0:
# 16 "data/scripts/cynthia.pory"
	.string "Oh, hello. You must be the Trainer\n"
	.string "everyone in Tosa keeps talking about.\p"
	.string "I'm Cynthia. I came to Holon to study\n"
	.string "the Pokémon that live around this lake.\p"
	.string "The researchers call them Delta\n"
	.string "Species. Their types have changed, but\l"
	.string "the bond they share with people hasn't\l"
	.string "changed at all.\p"
	.string "I'd like to see your bond for myself. Will\n"
	.string "you battle me?$"

Common_EventScript_CynthiaHolonLake_Text_1:
# 18 "data/scripts/cynthia.pory"
	.string "I understand. Take all the time you\n"
	.string "need. I'll be right here by the lake.$"

Common_EventScript_CynthiaHolonLake_Text_2:
# 23 "data/scripts/cynthia.pory"
	.string "Then let's begin. Show me everything\n"
	.string "you and your Pokémon have!$"

Common_EventScript_CynthiaHolonLake_Text_3:
# 24 "data/scripts/cynthia.pory"
	.string "Splendid… That was a wonderful battle.$"

Common_EventScript_CynthiaHolonLake_Text_4:
# 25 "data/scripts/cynthia.pory"
	.string "You and your Pokémon trust each other\n"
	.string "completely. I could feel it in every\l"
	.string "move.\p"
	.string "Holon's mysteries can wait a little\n"
	.string "longer. I think I'll rest in Changu City\l"
	.string "for a while.\p"
	.string "There's a café there I'm fond of. If\n"
	.string "you'd like a rematch, come and find me.$"

Common_EventScript_CynthiaCafe_Text_0:
# 40 "data/scripts/cynthia.pory"
	.string "Splendid. I think I'll stay in Changu a\n"
	.string "little longer.\p"
	.string "Come back tomorrow, and we'll battle\n"
	.string "again.$"

Common_EventScript_CynthiaCafe_Text_1:
# 44 "data/scripts/cynthia.pory"
	.string "Ah, it's you. The coffee here is\n"
	.string "wonderful, but I was hoping you'd come\l"
	.string "by.\p"
	.string "Shall we have another battle?$"

Common_EventScript_CynthiaCafe_Text_2:
# 46 "data/scripts/cynthia.pory"
	.string "That's all right. I'll be here, enjoying\n"
	.string "my coffee.$"

Common_EventScript_CynthiaCafe_Text_3:
# 51 "data/scripts/cynthia.pory"
	.string "Wonderful. Let's not hold back.$"

Common_EventScript_CynthiaCafe_Text_4:
# 53 "data/scripts/cynthia.pory"
	.string "Splendid… You've grown even stronger.$"
