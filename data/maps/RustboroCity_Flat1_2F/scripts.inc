# 1 "data/maps/RustboroCity_Flat1_2F/scripts.pory"

# 2 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
RustboroCity_Flat1_2F_MapScripts::
# 3 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.byte 0
# 4 "data/maps/RustboroCity_Flat1_2F/scripts.pory"

# 5 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
RustboroCity_Flat1_2F_EventScript_WaldasDad::
# 6 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	lock
# 7 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	faceplayer
# 8 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	specialvar VAR_RESULT, TryBufferWaldaPhrase
# 9 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, RustboroCity_Flat1_2F_EventScript_WaldasDadFirstPhrase
# 10 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	goto_if_eq VAR_RESULT, TRUE, RustboroCity_Flat1_2F_EventScript_WaldasDadNewPhrase
# 11 "data/maps/RustboroCity_Flat1_2F/scripts.pory"

# 12 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
RustboroCity_Flat1_2F_EventScript_GivePhrase::
# 13 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	special DoWaldaNamingScreen
# 14 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	goto_if_eq VAR_0x8004, 1, RustboroCity_Flat1_2F_EventScript_CancelGivePhrase
# 15 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	goto_if_eq VAR_0x8004, 2, RustboroCity_Flat1_2F_EventScript_CancelGiveFirstPhrase
# 16 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	specialvar VAR_RESULT, TryGetWallpaperWithWaldaPhrase
# 17 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	goto_if_eq VAR_RESULT, TRUE, RustboroCity_Flat1_2F_EventScript_WaldaLikesPhrase
# 18 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, RustboroCity_Flat1_2F_EventScript_WaldaDoesntLikePhrase
# 19 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	end
# 20 "data/maps/RustboroCity_Flat1_2F/scripts.pory"

# 21 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
RustboroCity_Flat1_2F_EventScript_WaldasDadFirstPhrase::
# 22 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	msgbox RustboroCity_Flat1_2F_Text_HelloDoYouKnowFunnyPhrase, MSGBOX_YESNO
# 23 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	goto_if_eq VAR_RESULT, NO, RustboroCity_Flat1_2F_EventScript_DeclineGivePhrase
# 24 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	msgbox RustboroCity_Flat1_2F_Text_WonderfulLetsHearSuggestion, MSGBOX_DEFAULT
# 25 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	goto RustboroCity_Flat1_2F_EventScript_GivePhrase
# 26 "data/maps/RustboroCity_Flat1_2F/scripts.pory"

# 27 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
RustboroCity_Flat1_2F_EventScript_WaldasDadNewPhrase::
# 28 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	msgbox RustboroCity_Flat1_2F_Text_BeenSayingXDoYouKnowBetterPhrase, MSGBOX_YESNO
# 29 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	goto_if_eq VAR_RESULT, NO, RustboroCity_Flat1_2F_EventScript_DeclineGivePhrase
# 30 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	msgbox RustboroCity_Flat1_2F_Text_WonderfulLetsHearSuggestion, MSGBOX_DEFAULT
# 31 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	goto RustboroCity_Flat1_2F_EventScript_GivePhrase
# 32 "data/maps/RustboroCity_Flat1_2F/scripts.pory"

# 33 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
RustboroCity_Flat1_2F_EventScript_DeclineGivePhrase::
# 34 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	msgbox RustboroCity_Flat1_2F_Text_OhIsThatRight, MSGBOX_DEFAULT
# 35 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	release
# 36 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	end
# 37 "data/maps/RustboroCity_Flat1_2F/scripts.pory"

# 38 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
RustboroCity_Flat1_2F_EventScript_CancelGivePhrase::
# 39 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	msgbox RustboroCity_Flat1_2F_Text_OhYouDontKnowAny, MSGBOX_DEFAULT
# 40 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	release
# 41 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	end
# 42 "data/maps/RustboroCity_Flat1_2F/scripts.pory"

# 43 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
RustboroCity_Flat1_2F_EventScript_CancelGiveFirstPhrase::
# 44 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	msgbox RustboroCity_Flat1_2F_Text_ThinkOfMyOwnPhrase, MSGBOX_DEFAULT
# 45 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	call RustboroCity_Flat1_2F_EventScript_WaldasDadFaceWalda
# 46 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	msgbox RustboroCity_Flat1_2F_Text_ShesNotSmilingAtAll2, MSGBOX_DEFAULT
# 47 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	release
# 48 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	end
# 49 "data/maps/RustboroCity_Flat1_2F/scripts.pory"

# 50 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
RustboroCity_Flat1_2F_EventScript_WaldaLikesPhrase::
# 51 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	msgbox RustboroCity_Flat1_2F_Text_LetsGiveItATry2, MSGBOX_DEFAULT
# 52 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	call RustboroCity_Flat1_2F_EventScript_WaldasDadFaceWalda
# 53 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	msgbox RustboroCity_Flat1_2F_Text_OhShesLaughing, MSGBOX_DEFAULT
# 54 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	applymovement LOCALID_WALDAS_DAD, Common_Movement_FacePlayer
# 55 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	waitmovement 0
# 56 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	msgbox RustboroCity_Flat1_2F_Text_ThankYouIllGiveYouWallpaper, MSGBOX_DEFAULT
# 57 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	release
# 58 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	end
# 59 "data/maps/RustboroCity_Flat1_2F/scripts.pory"

# 60 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
RustboroCity_Flat1_2F_EventScript_WaldaDoesntLikePhrase::
# 61 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	msgbox RustboroCity_Flat1_2F_Text_LetsGiveItATry, MSGBOX_DEFAULT
# 62 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	call RustboroCity_Flat1_2F_EventScript_WaldasDadFaceWalda
# 63 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	msgbox RustboroCity_Flat1_2F_Text_ShesNotSmilingAtAll, MSGBOX_DEFAULT
# 64 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	release
# 65 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	end
# 66 "data/maps/RustboroCity_Flat1_2F/scripts.pory"

# 67 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
RustboroCity_Flat1_2F_EventScript_WaldasDadFaceWalda::
# 68 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	turnobject LOCALID_WALDAS_DAD, DIR_EAST
# 69 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	return
# 70 "data/maps/RustboroCity_Flat1_2F/scripts.pory"

# 71 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
RustboroCity_Flat1_2F_EventScript_WaldasMom::
# 72 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	msgbox RustboroCity_Flat1_2F_Text_ComingUpWithMealsIsHard, MSGBOX_NPC
# 73 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	end
# 74 "data/maps/RustboroCity_Flat1_2F/scripts.pory"

# 75 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
RustboroCity_Flat1_2F_EventScript_PokeDoll::
# 76 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	msgbox RustboroCity_Flat1_2F_Text_ItsAPokemonPlushDoll, MSGBOX_SIGN
# 77 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	end
# 78 "data/maps/RustboroCity_Flat1_2F/scripts.pory"

# 79 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
RustboroCity_Flat1_2F_Text_ComingUpWithMealsIsHard:
# 80 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "Oh, it's so hard every day…\p"
# 81 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "What's hard?\n"
# 82 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "You need to ask?\p"
# 83 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "It's trying to figure out what to\n"
# 84 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "make for meals every day.\p"
# 85 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "It really isn't easy coming up with\n"
# 86 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "meals every day.$"
# 87 "data/maps/RustboroCity_Flat1_2F/scripts.pory"

# 88 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
RustboroCity_Flat1_2F_Text_HelloDoYouKnowFunnyPhrase:
# 89 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "Oh, hello!\n"
# 90 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "Welcome to the PEPPER household.\p"
# 91 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "I have a question for you.\n"
# 92 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "Have you ever baby-sat?\p"
# 93 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "You see, I'm a new father, so raising\n"
# 94 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "a child is all new to me.\p"
# 95 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "And I have a problem. My daughter\n"
# 96 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "WALDA doesn't laugh enough.\p"
# 97 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "I think she'd laugh for me if I told\n"
# 98 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "her something funny.\p"
# 99 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "Do you know of a funny word or\n"
# 100 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "phrase you can tell me?$"
# 101 "data/maps/RustboroCity_Flat1_2F/scripts.pory"

# 102 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
RustboroCity_Flat1_2F_Text_BeenSayingXDoYouKnowBetterPhrase:
# 103 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "I've been saying “{STR_VAR_1}”\n"
# 104 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "to amuse her lately.\p"
# 105 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "Do you know of a better word or\n"
# 106 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "a phrase that might work?$"
# 107 "data/maps/RustboroCity_Flat1_2F/scripts.pory"

# 108 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
RustboroCity_Flat1_2F_Text_WonderfulLetsHearSuggestion:
# 109 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "Oh, that's wonderful.\n"
# 110 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "So, let's hear it, your suggestion.$"
# 111 "data/maps/RustboroCity_Flat1_2F/scripts.pory"

# 112 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
RustboroCity_Flat1_2F_Text_OhIsThatRight:
# 113 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "Oh, is that right?\p"
# 114 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "Well, if you come up with a good\n"
# 115 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "suggestion, I'm all ears.$"
# 116 "data/maps/RustboroCity_Flat1_2F/scripts.pory"

# 117 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
RustboroCity_Flat1_2F_Text_LetsGiveItATry2:
# 118 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "Ah, I see.\n"
# 119 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "Well, let's give it a try, shall we?$"
# 120 "data/maps/RustboroCity_Flat1_2F/scripts.pory"

# 121 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
RustboroCity_Flat1_2F_Text_OhShesLaughing:
# 122 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "{STR_VAR_1}.\n"
# 123 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "{STR_VAR_1}.\p"
# 124 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "Oh, yes! She's laughing!\n"
# 125 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "Oh, I am as delighted as she!$"
# 126 "data/maps/RustboroCity_Flat1_2F/scripts.pory"

# 127 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
RustboroCity_Flat1_2F_Text_LetsGiveItATry:
# 128 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "Ah, I see.\n"
# 129 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "Well, let's give it a try, shall we?$"
# 130 "data/maps/RustboroCity_Flat1_2F/scripts.pory"

# 131 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
RustboroCity_Flat1_2F_Text_ShesNotSmilingAtAll:
# 132 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "{STR_VAR_1}.\n"
# 133 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "{STR_VAR_1}.\p"
# 134 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "Hmmm… She's not smiling at all.\n"
# 135 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "Maybe WALDA is one serious child…$"
# 136 "data/maps/RustboroCity_Flat1_2F/scripts.pory"

# 137 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
RustboroCity_Flat1_2F_Text_ThinkOfMyOwnPhrase:
# 138 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "Oh, so you don't know any good words.\n"
# 139 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "I'd better think for myself, then.\p"
# 140 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "Hmm…\n"
# 141 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "How about “{STR_VAR_1}”?\l"
# 142 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "Let's see if that will work.$"
# 143 "data/maps/RustboroCity_Flat1_2F/scripts.pory"

# 144 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
RustboroCity_Flat1_2F_Text_ShesNotSmilingAtAll2:
# 145 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "{STR_VAR_1}.\n"
# 146 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "{STR_VAR_1}.\p"
# 147 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "Hmmm… She's not smiling at all.\n"
# 148 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "Maybe WALDA is one serious child…$"
# 149 "data/maps/RustboroCity_Flat1_2F/scripts.pory"

# 150 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
RustboroCity_Flat1_2F_Text_OhYouDontKnowAny:
# 151 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "Oh, so you don't know any good words.\n"
# 152 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "I guess I'll try to amuse her with\l"
# 153 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "the saying I used before.\p"
# 154 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "Anyways, if you have a good suggestion,\n"
# 155 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "don't hesitate in telling me, okay?$"
# 156 "data/maps/RustboroCity_Flat1_2F/scripts.pory"

# 157 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
RustboroCity_Flat1_2F_Text_ThankYouIllGiveYouWallpaper:
# 158 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "Thank you!\p"
# 159 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "Thanks to you, my darling WALDA\n"
# 160 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "laughed for me!\p"
# 161 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "Actually, I may not look all that\n"
# 162 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "special, but I'm one of DEVON\l"
# 163 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "CORPORATION's top researchers.\p"
# 164 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "So, how about I do something in return\n"
# 165 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "for you?\p"
# 166 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "I know, I'll add some new wallpaper\n"
# 167 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "patterns for the BOXES in the PC\l"
# 168 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "POKéMON Storage System.\p"
# 169 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "In the wallpaper pattern menu,\n"
# 170 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "select “FRIENDS.”\p"
# 171 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "That will give you access to the new\n"
# 172 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "wallpaper patterns.$"
# 173 "data/maps/RustboroCity_Flat1_2F/scripts.pory"

# 174 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
RustboroCity_Flat1_2F_Text_ItsAPokemonPlushDoll:
# 175 "data/maps/RustboroCity_Flat1_2F/scripts.pory"
	.string "It's a POKéMON plush DOLL!$"
