# 1 "data/maps/TosaPort/scripts.pory"

# 2 "data/maps/TosaPort/scripts.pory"
TosaPort_MapScripts::
# 3 "data/maps/TosaPort/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, TosaPort_OnTransition
# 4 "data/maps/TosaPort/scripts.pory"
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, TosaPort_OnWarp
# 5 "data/maps/TosaPort/scripts.pory"
	.byte 0
# 6 "data/maps/TosaPort/scripts.pory"

# 7 "data/maps/TosaPort/scripts.pory"
TosaPort_OnTransition:
# 8 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_VISITED_TOSA_PORT
# 9 "data/maps/TosaPort/scripts.pory"
	end
# 10 "data/maps/TosaPort/scripts.pory"

# 11 "data/maps/TosaPort/scripts.pory"
@ After object events exist; RunScriptImmediately — use only instant cmds (turnobject is OK).
# 12 "data/maps/TosaPort/scripts.pory"
TosaPort_OnWarp:
# 13 "data/maps/TosaPort/scripts.pory"
	map_script_2 VAR_TEMP_0, 0, TosaPort_EventScript_WarpFaceNorthIfNoMon
# 14 "data/maps/TosaPort/scripts.pory"
	.2byte 0
# 15 "data/maps/TosaPort/scripts.pory"

# 16 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_WarpFaceNorthIfNoMon::
# 17 "data/maps/TosaPort/scripts.pory"
	goto_if_set FLAG_SYS_POKEMON_GET, TosaPort_EventScript_WarpFaceNorthIfNoMon_End
# 18 "data/maps/TosaPort/scripts.pory"
	turnobject LOCALID_PLAYER, DIR_NORTH
# 19 "data/maps/TosaPort/scripts.pory"

# 20 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_WarpFaceNorthIfNoMon_End::
# 21 "data/maps/TosaPort/scripts.pory"
	end
# 22 "data/maps/TosaPort/scripts.pory"

# 23 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_TownSign::
# 24 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_TownSign, MSGBOX_SIGN
# 25 "data/maps/TosaPort/scripts.pory"
	end
# 26 "data/maps/TosaPort/scripts.pory"

# 27 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_TruckSign::
# 28 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_TruckSign, MSGBOX_SIGN
# 29 "data/maps/TosaPort/scripts.pory"
	end
# 30 "data/maps/TosaPort/scripts.pory"

# 31 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_ColdStorageSign::
# 32 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_ColdStorageSign, MSGBOX_SIGN
# 33 "data/maps/TosaPort/scripts.pory"
	end
# 34 "data/maps/TosaPort/scripts.pory"

# 35 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_GatewaySign::
# 36 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_GatewaySign, MSGBOX_SIGN
# 37 "data/maps/TosaPort/scripts.pory"
	end
# 38 "data/maps/TosaPort/scripts.pory"

# 39 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_StarterGuide::
# 40 "data/maps/TosaPort/scripts.pory"
	lock
# 41 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 42 "data/maps/TosaPort/scripts.pory"
	goto_if_set FLAG_HIDE_ROUTE_101_BIRCH_STARTERS_BAG, TosaPort_EventScript_StarterGuide_AfterStarter
# 43 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_STARTER_AIDE, Common_Movement_QuestionMark
# 44 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 45 "data/maps/TosaPort/scripts.pory"
	playSE SE_M_METRONOME
# 46 "data/maps/TosaPort/scripts.pory"
	delay 24
# 47 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_YouMustBePlayer, MSGBOX_NPC
# 48 "data/maps/TosaPort/scripts.pory"
	delay 48
# 49 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_STARTER_AIDE, Common_Movement_ExclamationMark
# 50 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 51 "data/maps/TosaPort/scripts.pory"
	playse SE_PIN
# 52 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_GivePokemon, MSGBOX_DEFAULT
# 53 "data/maps/TosaPort/scripts.pory"
	fadescreen FADE_TO_BLACK
# 54 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_SYS_POKEMON_GET
# 55 "data/maps/TosaPort/scripts.pory"
	special ChooseStarterOverworld
# 56 "data/maps/TosaPort/scripts.pory"
	waitstate
# 57 "data/maps/TosaPort/scripts.pory"
	fadescreen FADE_FROM_BLACK
# 58 "data/maps/TosaPort/scripts.pory"
	bufferleadmonspeciesname STR_VAR_2
# 59 "data/maps/TosaPort/scripts.pory"
	playfanfare MUS_OBTAIN_TMHM
# 60 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_ReceivedPokemon, MSGBOX_AUTOCLOSE
# 61 "data/maps/TosaPort/scripts.pory"
	waitfanfare
# 62 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_Nickname, MSGBOX_YESNO
# 63 "data/maps/TosaPort/scripts.pory"
	call_if_eq VAR_RESULT, 1, TosaPort_EventScript_GiveNickname
# 64 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_HIDE_ROUTE_101_BIRCH_STARTERS_BAG
# 65 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_TakeTosaPass, MSGBOX_DEFAULT
# 66 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_StarterGuideTelokHint
# 67 "data/maps/TosaPort/scripts.pory"
	setvar VAR_TOSA_PORT_STATE 1
# 68 "data/maps/TosaPort/scripts.pory"
	release
# 69 "data/maps/TosaPort/scripts.pory"
	end
# 70 "data/maps/TosaPort/scripts.pory"

# 71 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_GiveNickname::
# 72 "data/maps/TosaPort/scripts.pory"
	fadescreen FADE_TO_BLACK
# 73 "data/maps/TosaPort/scripts.pory"
	special ChangePokemonNickname
# 74 "data/maps/TosaPort/scripts.pory"
	waitstate
# 75 "data/maps/TosaPort/scripts.pory"
	fadescreen FADE_FROM_BLACK
# 76 "data/maps/TosaPort/scripts.pory"
	return
# 77 "data/maps/TosaPort/scripts.pory"

# 78 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_StarterGuide_AfterStarter::
# 79 "data/maps/TosaPort/scripts.pory"
	lock
# 80 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 81 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_StarterGuideTelokHint, MSGBOX_DEFAULT
# 82 "data/maps/TosaPort/scripts.pory"
	release
# 83 "data/maps/TosaPort/scripts.pory"
	end
# 84 "data/maps/TosaPort/scripts.pory"

# 85 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_YouMustBePlayer:
# 86 "data/maps/TosaPort/scripts.pory"
	.string "Ah! You must be {PLAYER}.\p"
# 87 "data/maps/TosaPort/scripts.pory"
	.string "Professor Palm sent me to meet you\n"
# 88 "data/maps/TosaPort/scripts.pory"
	.string "once the Seagallop-20 made port.$"
# 89 "data/maps/TosaPort/scripts.pory"

# 90 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_GivePokemon:
# 91 "data/maps/TosaPort/scripts.pory"
	.string "I've brought you a little welcome\n"
# 92 "data/maps/TosaPort/scripts.pory"
	.string "present on behalf of the University.\p"
# 93 "data/maps/TosaPort/scripts.pory"
	.string "With the journey being so long from\n"
# 94 "data/maps/TosaPort/scripts.pory"
	.string "Galar, we figured you wouldn't bring\l"
# 95 "data/maps/TosaPort/scripts.pory"
	.string "your partners along.\p"
# 96 "data/maps/TosaPort/scripts.pory"
	.string "You peer inside the bag.$"
# 97 "data/maps/TosaPort/scripts.pory"

# 98 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_ReceivedPokemon:
# 99 "data/maps/TosaPort/scripts.pory"
	.string "You received a {STR_VAR_2}!$"
# 100 "data/maps/TosaPort/scripts.pory"

# 101 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_Nickname:
# 102 "data/maps/TosaPort/scripts.pory"
	.string "Would you like to give {STR_VAR_2} a\n"
# 103 "data/maps/TosaPort/scripts.pory"
	.string "nickname?$"
# 104 "data/maps/TosaPort/scripts.pory"

# 105 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_TakeTosaPass:
# 106 "data/maps/TosaPort/scripts.pory"
	.string "If you're going to reach Professsor Palm,\n"
# 107 "data/maps/TosaPort/scripts.pory"
	.string "you'll need this Tosa Pass.\p"
# 108 "data/maps/TosaPort/scripts.pory"
	.string "(Placeholder: TOSA PASS received.)$"
# 109 "data/maps/TosaPort/scripts.pory"

# 110 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_StarterGuideTelokHint:
# 111 "data/maps/TosaPort/scripts.pory"
	.string "The road to TELOK TOWN runs through\n"
# 112 "data/maps/TosaPort/scripts.pory"
	.string "the Tosa nature reserve to the north.\p"
# 113 "data/maps/TosaPort/scripts.pory"
	.string "You'll find Palm Labs there.$"
# 114 "data/maps/TosaPort/scripts.pory"

# 115 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_TownSign:
# 116 "data/maps/TosaPort/scripts.pory"
	.string "Welcome to Tosa!\n"
# 117 "data/maps/TosaPort/scripts.pory"
	.string "- The Tosa Tourism Board$"
# 118 "data/maps/TosaPort/scripts.pory"

# 119 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_GatewaySign:
# 120 "data/maps/TosaPort/scripts.pory"
	.string "Tosa Reserve Gateway\n"
# 121 "data/maps/TosaPort/scripts.pory"
	.string "Trainer passes strictly required$"
# 122 "data/maps/TosaPort/scripts.pory"

# 123 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_TruckSign:
# 124 "data/maps/TosaPort/scripts.pory"
	.string "Machamp Moving Co.\n"
# 125 "data/maps/TosaPort/scripts.pory"
	.string "No Load too Lumbersome!$"
# 126 "data/maps/TosaPort/scripts.pory"

# 127 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_ColdStorageSign:
# 128 "data/maps/TosaPort/scripts.pory"
	.string "Tosa Port Cold Storage$"

TosaPort_ScrubbingSailor::
# 133 "data/maps/TosaPort/scripts.pory"
	lock
# 134 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 135 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ScrubbingSailor_Text_0
# 137 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_ShuntingSailor::
# 142 "data/maps/TosaPort/scripts.pory"
	lock
# 143 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 144 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ShuntingSailor_Text_0
# 146 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_VigorothCry::
# 151 "data/maps/TosaPort/scripts.pory"
	lock
# 152 "data/maps/TosaPort/scripts.pory"
	playmoncry SPECIES_VIGOROTH, CRY_MODE_NORMAL
# 153 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_VigorothCry_Text_0
# 154 "data/maps/TosaPort/scripts.pory"
	waitmoncry
# 155 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_ChefStall::
# 160 "data/maps/TosaPort/scripts.pory"
	lock
# 161 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 162 "data/maps/TosaPort/scripts.pory"
	goto_if_unset FLAG_CHEF_STALL_MET, TosaPort_ChefStall_2
# 178 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ChefStall_Text_2
# 180 "data/maps/TosaPort/scripts.pory"
	pokemart ChefStallGoods
# 181 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ChefStall_Text_3
# 182 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_ChefStall_2:
# 163 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ChefStall_Text_0
# 172 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_CHEF_STALL_MET
# 173 "data/maps/TosaPort/scripts.pory"
	pokemart ChefStallGoods
# 174 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ChefStall_Text_1
# 175 "data/maps/TosaPort/scripts.pory"
	release
	end


	.align 2
# 186 "data/maps/TosaPort/scripts.pory"
ChefStallGoods:
# 187 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_LAVA_COOKIE
# 188 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_PEWTER_CRUNCHIES
# 189 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_OLD_GATEAU
# 190 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_BIG_MALASADA
# 191 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_SHALOUR_SABLE
	.2byte ITEM_NONE

TosaPort_PSPKid::
# 195 "data/maps/TosaPort/scripts.pory"
	lock
# 196 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 197 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PSPKid_Text_0
# 199 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_RepelGuy::
# 204 "data/maps/TosaPort/scripts.pory"
	lock
# 205 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 206 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_RepelGuy_Text_0
# 209 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_BreakTrucker::
# 214 "data/maps/TosaPort/scripts.pory"
	lock
# 215 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 216 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_BreakTrucker_Text_0
# 217 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_LoadingTrucker::
# 222 "data/maps/TosaPort/scripts.pory"
	lock
# 223 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 224 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_LoadingTrucker_Text_0
# 226 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_OldMan::
# 231 "data/maps/TosaPort/scripts.pory"
	lock
# 232 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldMan_Text_0
# 234 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_OldWoman::
# 239 "data/maps/TosaPort/scripts.pory"
	lock
# 240 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldWoman_Text_0
# 242 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_Skitty::
# 247 "data/maps/TosaPort/scripts.pory"
	lock
# 248 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 249 "data/maps/TosaPort/scripts.pory"
	playmoncry SPECIES_SKITTY, CRY_MODE_NORMAL
# 250 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Skitty_Text_0
# 251 "data/maps/TosaPort/scripts.pory"
	waitmoncry
# 252 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_Fisherman::
# 257 "data/maps/TosaPort/scripts.pory"
	lock
# 258 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 259 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Fisherman_Text_0
# 261 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_Tuber::
# 266 "data/maps/TosaPort/scripts.pory"
	lock
# 267 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 268 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Tuber_Text_0
# 272 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_ColdStorageGuard::
# 277 "data/maps/TosaPort/scripts.pory"
	lock
# 278 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 279 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ColdStorageGuard_Text_0
# 281 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_Martin::
# 286 "data/maps/TosaPort/scripts.pory"
	lock
# 287 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 288 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Martin_Text_0
# 290 "data/maps/TosaPort/scripts.pory"
	pokemart MartinsMartGoods
# 291 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Martin_Text_1
# 292 "data/maps/TosaPort/scripts.pory"
	release
	end


	.align 2
# 296 "data/maps/TosaPort/scripts.pory"
MartinsMartGoods:
# 297 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_POTION
# 298 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_POKE_BALL
# 299 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_ANTIDOTE
# 300 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_PARALYZE_HEAL
# 301 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_REPEL
	.2byte ITEM_NONE

TosaPort_ScrubbingSailor_Text_0:
# 135 "data/maps/TosaPort/scripts.pory"
	.string "Gotta keep this jetty looking ship-\n"
	.string "shape!$"

TosaPort_ShuntingSailor_Text_0:
# 144 "data/maps/TosaPort/scripts.pory"
	.string "It's a good thing I have my Vigoroth\n"
	.string "with me!$"

TosaPort_VigorothCry_Text_0:
# 153 "data/maps/TosaPort/scripts.pory"
	.string "Vigoroth: Urraw!$"

TosaPort_ChefStall_Text_0:
# 163 "data/maps/TosaPort/scripts.pory"
	.string "Bonjour!\p"
	.string "I have travelled many miles from my\n"
	.string "home in Kalos...mais alors I have grown\l"
	.string "tired.\p"
	.string "I decided that it was time to share my\n"
	.string "love for la cuisine du monde avec the\l"
	.string "people!\p"
	.string "Have a look at my goods, see they are\n"
	.string "the most fresh, non?$"

TosaPort_ChefStall_Text_1:
# 174 "data/maps/TosaPort/scripts.pory"
	.string "See you again, mon ami!$"

TosaPort_ChefStall_Text_2:
# 178 "data/maps/TosaPort/scripts.pory"
	.string "Good to see you mon ami!\n"
	.string "What can I get for you?$"

TosaPort_ChefStall_Text_3:
# 181 "data/maps/TosaPort/scripts.pory"
	.string "Always a pleasure, mon ami!$"

TosaPort_PSPKid_Text_0:
# 197 "data/maps/TosaPort/scripts.pory"
	.string "Ugh, Dad's making me watch his stall.\n"
	.string "At least he let me bring my PSP.$"

TosaPort_RepelGuy_Text_0:
# 206 "data/maps/TosaPort/scripts.pory"
	.string "I read in “Pokémon Garden” that\n"
	.string "spraying repel on your flowers can keep\l"
	.string "bug Pokémon at bay.$"

TosaPort_BreakTrucker_Text_0:
# 216 "data/maps/TosaPort/scripts.pory"
	.string "Buzz off, I'm on my break!$"

TosaPort_LoadingTrucker_Text_0:
# 224 "data/maps/TosaPort/scripts.pory"
	.string "I wish my Pokémon was strong enough to\n"
	.string "load this truck...$"

TosaPort_OldMan_Text_0:
# 232 "data/maps/TosaPort/scripts.pory"
	.string "Fu-fu-fu...I met my wife at this very\n"
	.string "spot 10 years ago.$"

TosaPort_OldWoman_Text_0:
# 240 "data/maps/TosaPort/scripts.pory"
	.string "Ha-ha-ha...we were so reckless back\n"
	.string "then...life is too short...$"

TosaPort_Skitty_Text_0:
# 250 "data/maps/TosaPort/scripts.pory"
	.string "Skitty: Meooow!$"

TosaPort_Fisherman_Text_0:
# 259 "data/maps/TosaPort/scripts.pory"
	.string "I came all this way from Pasira City to\n"
	.string "fish in the reserve.$"

TosaPort_Tuber_Text_0:
# 268 "data/maps/TosaPort/scripts.pory"
	.string "Awww...\n"
	.string "I was hoping to swim while visiting\l"
	.string "Daddy, but the current here is too\l"
	.string "strong!$"

TosaPort_ColdStorageGuard_Text_0:
# 279 "data/maps/TosaPort/scripts.pory"
	.string "Sorry pal, but the site's currently\n"
	.string "closed.$"

TosaPort_Martin_Text_0:
# 288 "data/maps/TosaPort/scripts.pory"
	.string "Welcome to Martin's Mart!\n"
	.string "Trainer Supplies and Sundries.$"

TosaPort_Martin_Text_1:
# 291 "data/maps/TosaPort/scripts.pory"
	.string "Come back soon!$"
