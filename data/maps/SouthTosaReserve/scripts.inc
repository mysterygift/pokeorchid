# 1 "data/maps/SouthTosaReserve/scripts.pory"

# 2 "data/maps/SouthTosaReserve/scripts.pory"
SouthTosaReserve_MapScripts::
# 3 "data/maps/SouthTosaReserve/scripts.pory"
	.byte 0
# 4 "data/maps/SouthTosaReserve/scripts.pory"

# 5 "data/maps/SouthTosaReserve/scripts.pory"
SouthTosaReserve_EventScript_RouteSign::
# 6 "data/maps/SouthTosaReserve/scripts.pory"
	msgbox SouthTosaReserve_Text_RouteSign, MSGBOX_SIGN
# 7 "data/maps/SouthTosaReserve/scripts.pory"
	end
# 8 "data/maps/SouthTosaReserve/scripts.pory"

# 9 "data/maps/SouthTosaReserve/scripts.pory"
SouthTosaReserve_EventScript_BirchsBag::
# 10 "data/maps/SouthTosaReserve/scripts.pory"
	@ lock
# 11 "data/maps/SouthTosaReserve/scripts.pory"
	@ faceplayer
# 12 "data/maps/SouthTosaReserve/scripts.pory"
	@ setflag FLAG_SYS_POKEMON_GET
# 13 "data/maps/SouthTosaReserve/scripts.pory"
	@ setflag FLAG_RESCUED_BIRCH
# 14 "data/maps/SouthTosaReserve/scripts.pory"
	@ fadescreen FADE_TO_BLACK
# 15 "data/maps/SouthTosaReserve/scripts.pory"
	@ removeobject LOCALID_SOUTHTOSARESERVE_ZIGZAGOON
# 16 "data/maps/SouthTosaReserve/scripts.pory"
	@ setobjectxy LOCALID_PLAYER, 6, 13
# 17 "data/maps/SouthTosaReserve/scripts.pory"
	@ applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterLeft
# 18 "data/maps/SouthTosaReserve/scripts.pory"
	@ waitmovement 0
# 19 "data/maps/SouthTosaReserve/scripts.pory"
	@ special ChooseStarter
# 20 "data/maps/SouthTosaReserve/scripts.pory"
	@ waitstate
# 21 "data/maps/SouthTosaReserve/scripts.pory"
	@ applymovement LOCALID_SOUTHTOSARESERVE_BIRCH, SouthTosaReserve_Movement_BirchApproachPlayer
# 22 "data/maps/SouthTosaReserve/scripts.pory"
	@ waitmovement 0
# 23 "data/maps/SouthTosaReserve/scripts.pory"
	@ msgbox SouthTosaReserve_Text_YouSavedMe, MSGBOX_DEFAULT
# 24 "data/maps/SouthTosaReserve/scripts.pory"
	@ special HealPlayerParty
# 25 "data/maps/SouthTosaReserve/scripts.pory"
	@ setflag FLAG_HIDE_SOUTH_TOSA_RESERVE_BIRCH_ZIGZAGOON_BATTLE
# 26 "data/maps/SouthTosaReserve/scripts.pory"
	@ clearflag FLAG_HIDE_TOSA_PORT_BIRCHS_LAB_BIRCH
# 27 "data/maps/SouthTosaReserve/scripts.pory"
	@ setflag FLAG_HIDE_SOUTH_TOSA_RESERVE_BIRCH_STARTERS_BAG
# 28 "data/maps/SouthTosaReserve/scripts.pory"
	@ setvar VAR_BIRCH_LAB_STATE, 2
# 29 "data/maps/SouthTosaReserve/scripts.pory"
	@ setvar VAR_SOUTHTOSARESERVE_STATE, 3
# 30 "data/maps/SouthTosaReserve/scripts.pory"
	@ clearflag FLAG_HIDE_MAP_NAME_POPUP
# 31 "data/maps/SouthTosaReserve/scripts.pory"
	@ checkplayergender
# 32 "data/maps/SouthTosaReserve/scripts.pory"
	@ call_if_eq VAR_RESULT, MALE, SouthTosaReserve_EventScript_HideMayInBedroom
# 33 "data/maps/SouthTosaReserve/scripts.pory"
	@ call_if_eq VAR_RESULT, FEMALE, SouthTosaReserve_EventScript_HideBrendanInBedroom
# 34 "data/maps/SouthTosaReserve/scripts.pory"
	@ warp MAP_TELOK_TOWN_PALM_LABS, 6, 5
# 35 "data/maps/SouthTosaReserve/scripts.pory"
	@ waitstate
# 36 "data/maps/SouthTosaReserve/scripts.pory"
	@ release
# 37 "data/maps/SouthTosaReserve/scripts.pory"
	@ end
# 38 "data/maps/SouthTosaReserve/scripts.pory"
	end
# 39 "data/maps/SouthTosaReserve/scripts.pory"

# 40 "data/maps/SouthTosaReserve/scripts.pory"
SouthTosaReserve_Text_RouteSign:
# 41 "data/maps/SouthTosaReserve/scripts.pory"
	.string "Tosa Reserve South\n"
# 42 "data/maps/SouthTosaReserve/scripts.pory"
	.string "{DOWN_ARROW} Tosa Port$"

SouthTosaReserve_EventScript_Ranger::
# 52 "data/maps/SouthTosaReserve/scripts.pory"
	msgbox SouthTosaReserve_EventScript_Ranger_Text_0, MSGBOX_NPC
	end


SouthTosaReserve_EventScript_FieldNurse::
# 57 "data/maps/SouthTosaReserve/scripts.pory"
	lock
# 58 "data/maps/SouthTosaReserve/scripts.pory"
	faceplayer
# 59 "data/maps/SouthTosaReserve/scripts.pory"
	msgbox SouthTosaReserve_EventScript_FieldNurse_Text_0, MSGBOX_YESNO
# 60 "data/maps/SouthTosaReserve/scripts.pory"
	compare VAR_RESULT, NO
	goto_if_eq SouthTosaReserve_EventScript_FieldNurse_2
# 65 "data/maps/SouthTosaReserve/scripts.pory"
	msgbox SouthTosaReserve_EventScript_FieldNurse_Text_2
# 66 "data/maps/SouthTosaReserve/scripts.pory"
	closemessage
# 67 "data/maps/SouthTosaReserve/scripts.pory"
	call Common_EventScript_OutOfCenterPartyHeal
# 68 "data/maps/SouthTosaReserve/scripts.pory"
	msgbox SouthTosaReserve_EventScript_FieldNurse_Text_3
# 69 "data/maps/SouthTosaReserve/scripts.pory"
	release
	end

SouthTosaReserve_EventScript_FieldNurse_2:
# 61 "data/maps/SouthTosaReserve/scripts.pory"
	msgbox SouthTosaReserve_EventScript_FieldNurse_Text_1
# 62 "data/maps/SouthTosaReserve/scripts.pory"
	release
	end


SouthTosaReserve_EventScript_GirlByTent::
# 74 "data/maps/SouthTosaReserve/scripts.pory"
	msgbox SouthTosaReserve_EventScript_GirlByTent_Text_0, MSGBOX_NPC
	end


SouthTosaReserve_EventScript_FishermanRiver::
# 79 "data/maps/SouthTosaReserve/scripts.pory"
	msgbox SouthTosaReserve_EventScript_FishermanRiver_Text_0, MSGBOX_NPC
	end


SouthTosaReserve_EventScript_WomanByFlowers::
# 84 "data/maps/SouthTosaReserve/scripts.pory"
	msgbox SouthTosaReserve_EventScript_WomanByFlowers_Text_0, MSGBOX_NPC
	end


SouthTosaReserve_EventScript_AhHuat::
# 89 "data/maps/SouthTosaReserve/scripts.pory"
	trainerbattle_single TRAINER_AH_HUAT, SouthTosaReserve_Text_AhHuatIntro, SouthTosaReserve_Text_AhHuatDefeat
# 90 "data/maps/SouthTosaReserve/scripts.pory"
	msgbox SouthTosaReserve_Text_AhHuatPostBattle, MSGBOX_AUTOCLOSE
	end


SouthTosaReserve_EventScript_Darren::
# 95 "data/maps/SouthTosaReserve/scripts.pory"
	trainerbattle_single TRAINER_DARREN, SouthTosaReserve_Text_DarrenIntro, SouthTosaReserve_Text_DarrenDefeat
# 96 "data/maps/SouthTosaReserve/scripts.pory"
	msgbox SouthTosaReserve_Text_DarrenPostBattle, MSGBOX_AUTOCLOSE
	end


SouthTosaReserve_EventScript_HikerLookout::
# 130 "data/maps/SouthTosaReserve/scripts.pory"
	msgbox SouthTosaReserve_EventScript_HikerLookout_Text_0, MSGBOX_NPC
	end


SouthTosaReserve_EventScript_MeiLing::
# 135 "data/maps/SouthTosaReserve/scripts.pory"
	trainerbattle_single TRAINER_MEI_LING, SouthTosaReserve_Text_MeiLingIntro, SouthTosaReserve_Text_MeiLingDefeat
# 136 "data/maps/SouthTosaReserve/scripts.pory"
	msgbox SouthTosaReserve_Text_MeiLingPostBattle, MSGBOX_AUTOCLOSE
	end


SouthTosaReserve_EventScript_Rizal::
# 141 "data/maps/SouthTosaReserve/scripts.pory"
	trainerbattle_single TRAINER_RIZAL, SouthTosaReserve_Text_RizalIntro, SouthTosaReserve_Text_RizalDefeat
# 142 "data/maps/SouthTosaReserve/scripts.pory"
	msgbox SouthTosaReserve_Text_RizalPostBattle, MSGBOX_AUTOCLOSE
	end


SouthTosaReserve_EventScript_JunJie::
# 147 "data/maps/SouthTosaReserve/scripts.pory"
	trainerbattle_single TRAINER_JUN_JIE, SouthTosaReserve_Text_JunJieIntro, SouthTosaReserve_Text_JunJieDefeat
# 148 "data/maps/SouthTosaReserve/scripts.pory"
	msgbox SouthTosaReserve_Text_JunJiePostBattle, MSGBOX_AUTOCLOSE
	end


SouthTosaReserve_EventScript_Priya::
# 153 "data/maps/SouthTosaReserve/scripts.pory"
	trainerbattle_single TRAINER_PRIYA, SouthTosaReserve_Text_PriyaIntro, SouthTosaReserve_Text_PriyaDefeat
# 154 "data/maps/SouthTosaReserve/scripts.pory"
	msgbox SouthTosaReserve_Text_PriyaPostBattle, MSGBOX_AUTOCLOSE
	end


SouthTosaReserve_EventScript_Ravi::
# 159 "data/maps/SouthTosaReserve/scripts.pory"
	trainerbattle_single TRAINER_RAVI, SouthTosaReserve_Text_RaviIntro, SouthTosaReserve_Text_RaviDefeat
# 160 "data/maps/SouthTosaReserve/scripts.pory"
	msgbox SouthTosaReserve_Text_RaviPostBattle, MSGBOX_AUTOCLOSE
	end


SouthTosaReserve_EventScript_Ranger_Text_0:
# 52 "data/maps/SouthTosaReserve/scripts.pory"
	.string "Welcome to the Tosa Reserve! I'm one of\n"
	.string "the Pokémon Rangers who look after it.\p"
	.string "We've had all sorts of Pokémon turning\n"
	.string "up lately that don't belong here, so\l"
	.string "keep your eyes peeled.\p"
	.string "If your Pokémon get worn out, our Field\n"
	.string "Nurse has a tent just up the path.\p"
	.string "Us rangers are here if you need any\n"
	.string "help.$"

SouthTosaReserve_EventScript_FieldNurse_Text_0:
# 59 "data/maps/SouthTosaReserve/scripts.pory"
	.string "Hello there! I'm the Field Nurse for this\n"
	.string "part of the reserve.\p"
	.string "Would you like me to look after your\n"
	.string "Pokémon?$"

SouthTosaReserve_EventScript_FieldNurse_Text_1:
# 61 "data/maps/SouthTosaReserve/scripts.pory"
	.string "All right. Take care out there!$"

SouthTosaReserve_EventScript_FieldNurse_Text_2:
# 65 "data/maps/SouthTosaReserve/scripts.pory"
	.string "Leave it to me!$"

SouthTosaReserve_EventScript_FieldNurse_Text_3:
# 68 "data/maps/SouthTosaReserve/scripts.pory"
	.string "There we go, all patched up! Come back\n"
	.string "any time you need me.$"

SouthTosaReserve_EventScript_GirlByTent_Text_0:
# 74 "data/maps/SouthTosaReserve/scripts.pory"
	.string "I came all the way to Tosa to see wild\n"
	.string "Pokémon. The Starly here are so cute!$"

SouthTosaReserve_EventScript_FishermanRiver_Text_0:
# 79 "data/maps/SouthTosaReserve/scripts.pory"
	.string "Used to be you'd only reel in Magikarp\n"
	.string "on this river.\p"
	.string "Now it's Corphish this, Corphish that.\n"
	.string "Somebody must have let them loose.$"

SouthTosaReserve_EventScript_WomanByFlowers_Text_0:
# 84 "data/maps/SouthTosaReserve/scripts.pory"
	.string "A wild Mareep jumped out of the grass\n"
	.string "and paralysed my Pokémon!\p"
	.string "I'm so thankful there's a Field Nurse\n"
	.string "close by. She had them back on their\l"
	.string "feet in no time.$"

SouthTosaReserve_EventScript_HikerLookout_Text_0:
# 130 "data/maps/SouthTosaReserve/scripts.pory"
	.string "I've hiked these hills for thirty years.\n"
	.string "There are Pokémon around now that I\l"
	.string "never used to see.$"

SouthTosaReserve_Text_AhHuatIntro::
# 100 "data/maps/SouthTosaReserve/scripts.pory"
	.string "Nothing's biting today... Except this\n"
	.string "Corphish! Let's see how it does against\l"
	.string "you!$"

SouthTosaReserve_Text_AhHuatDefeat::
# 104 "data/maps/SouthTosaReserve/scripts.pory"
	.string "Aiyo, wiped out!$"

SouthTosaReserve_Text_AhHuatPostBattle::
# 108 "data/maps/SouthTosaReserve/scripts.pory"
	.string "Corphish never used to live in this\n"
	.string "river. Now I catch more of them than\l"
	.string "anything else.$"

SouthTosaReserve_Text_DarrenIntro::
# 112 "data/maps/SouthTosaReserve/scripts.pory"
	.string "I've been camping out here all week! My\n"
	.string "Pokémon are raring to go!$"

SouthTosaReserve_Text_DarrenDefeat::
# 116 "data/maps/SouthTosaReserve/scripts.pory"
	.string "Guess we need more training...$"

SouthTosaReserve_Text_DarrenPostBattle::
# 120 "data/maps/SouthTosaReserve/scripts.pory"
	.string "Telok Town is just up north. Watch out\n"
	.string "for the long grass on the way!$"

SouthTosaReserve_Text_MeiLingIntro::
# 164 "data/maps/SouthTosaReserve/scripts.pory"
	.string "I raised my Pokémon right here on the\n"
	.string "reserve. They've grown up so strong!$"

SouthTosaReserve_Text_MeiLingDefeat::
# 168 "data/maps/SouthTosaReserve/scripts.pory"
	.string "We'll have to try harder next picnic!$"

SouthTosaReserve_Text_MeiLingPostBattle::
# 172 "data/maps/SouthTosaReserve/scripts.pory"
	.string "My Flaaffy was just a little Mareep\n"
	.string "when I caught it. It zapped my whole\l"
	.string "team the first time we met!$"

SouthTosaReserve_Text_RizalIntro::
# 176 "data/maps/SouthTosaReserve/scripts.pory"
	.string "Climbing these rocks every day builds\n"
	.string "strength! Same goes for my Pokémon!$"

SouthTosaReserve_Text_RizalDefeat::
# 180 "data/maps/SouthTosaReserve/scripts.pory"
	.string "Ha! You're as tough as a boulder!$"

SouthTosaReserve_Text_RizalPostBattle::
# 184 "data/maps/SouthTosaReserve/scripts.pory"
	.string "The rangers keep telling me to stay off\n"
	.string "the cliffs. Where's the fun in that?$"

SouthTosaReserve_Text_JunJieIntro::
# 188 "data/maps/SouthTosaReserve/scripts.pory"
	.string "I cycle this loop every morning. Think\n"
	.string "you can keep pace?$"

SouthTosaReserve_Text_JunJieDefeat::
# 192 "data/maps/SouthTosaReserve/scripts.pory"
	.string "Outpaced and out-battled...$"

SouthTosaReserve_Text_JunJiePostBattle::
# 196 "data/maps/SouthTosaReserve/scripts.pory"
	.string "Lap twelve... Wait, or was it thirteen?$"

SouthTosaReserve_Text_PriyaIntro::
# 200 "data/maps/SouthTosaReserve/scripts.pory"
	.string "The river Pokémon are my favourite. Let\n"
	.string "me show you why!$"

SouthTosaReserve_Text_PriyaDefeat::
# 204 "data/maps/SouthTosaReserve/scripts.pory"
	.string "Oh no, my picnic's ruined!$"

SouthTosaReserve_Text_PriyaPostBattle::
# 208 "data/maps/SouthTosaReserve/scripts.pory"
	.string "The Lotad in the river grow into Lombre\n"
	.string "if you train them. Mine loves the shade\l"
	.string "up here.$"

SouthTosaReserve_Text_RaviIntro::
# 212 "data/maps/SouthTosaReserve/scripts.pory"
	.string "You made it all the way up here? Then\n"
	.string "you're ready for a real battle!$"

SouthTosaReserve_Text_RaviDefeat::
# 216 "data/maps/SouthTosaReserve/scripts.pory"
	.string "Crumbled like gravel...$"

SouthTosaReserve_Text_RaviPostBattle::
# 220 "data/maps/SouthTosaReserve/scripts.pory"
	.string "From the top of the plateau you can see\n"
	.string "the whole reserve. It's worth the climb.$"
