@ Sevii Islands shared scripts (dev_scripts/voyages/sevii/build_sevii.py)

Sevii_EventScript_End::
	end

@ VAR_0x8004 = boat local id, VAR_0x8005 = sailor local id
SeviiFerry_EventScript_Board::
	msgbox SeviiFerry_Text_AllAboard, MSGBOX_DEFAULT
	closemessage
	applymovement VAR_0x8005, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	delay 20
	removeobject VAR_0x8005
	call Common_EventScript_FerryDepartIsland
	return

SeviiFerry_Text_WhereTo:
	.string "Ahoy! Mr. Briney's boat runs between\n"
	.string "all seven islands. Where to?$"

SeviiFerry_Text_AllAboard:
	.string "All aboard! Hold on to your hat!$"

SeviiFerry_Text_Stay:
	.string "Right you are. Come back any time!$"

SeviiFerry_Text_OneIsland:
	.string "ONE ISLAND$"

SeviiFerry_Text_TwoIsland:
	.string "TWO ISLAND$"

SeviiFerry_Text_ThreeIsland:
	.string "THREE ISLE PORT$"

SeviiFerry_Text_FourIsland:
	.string "FOUR ISLAND$"

SeviiFerry_Text_FiveIsland:
	.string "FIVE ISLAND$"

SeviiFerry_Text_SixIsland:
	.string "SIX ISLAND$"

SeviiFerry_Text_SevenIsland:
	.string "SEVEN ISLAND$"

SeviiFerry_Text_Stay_Option:
	.string "STAY HERE$"

@ Two Island market stall: rare goods at CONFIG stall_price_multiplier x their price
TwoIsland_EventScript_Clerk::
	lock
	faceplayer
	message SeviiStall_Text_Welcome
	waitmessage
	setvar VAR_SHOP_PRICE_MULTIPLIER, 3
	pokemart SeviiStall_Items
	setvar VAR_SHOP_PRICE_MULTIPLIER, 0
	msgbox SeviiStall_Text_Bye, MSGBOX_DEFAULT
	release
	end

	.align 2
SeviiStall_Items:
	.2byte ITEM_ABILITY_CAPSULE
	.2byte ITEM_ABILITY_PATCH
	.2byte ITEM_BOTTLE_CAP
	.2byte ITEM_GOLD_BOTTLE_CAP
	.2byte ITEM_PP_MAX
	.2byte ITEM_RARE_CANDY
	.2byte ITEM_EXP_CANDY_XL
	.2byte ITEM_LUCKY_EGG
	.2byte ITEM_DESTINY_KNOT
	.2byte ITEM_ADAMANT_MINT
	.2byte ITEM_JOLLY_MINT
	.2byte ITEM_MODEST_MINT
	.2byte ITEM_TIMID_MINT
	.2byte ITEM_LINKING_CORD
	.2byte ITEM_DUSK_STONE
	.2byte ITEM_SHINY_STONE
	.2byte ITEM_DAWN_STONE
	.2byte ITEM_ICE_STONE
	.2byte ITEM_RAZOR_CLAW
	.2byte ITEM_RAZOR_FANG
	.2byte ITEM_KINGS_ROCK
	.2byte ITEM_METAL_COAT
	.2byte ITEM_PRISM_SCALE
	.2byte ITEM_PROTECTOR
	.2byte ITEM_ELECTIRIZER
	.2byte ITEM_MAGMARIZER
	.2byte ITEM_REAPER_CLOTH
	.2byte ITEM_DUBIOUS_DISC
	.2byte ITEM_UPGRADE
	.2byte ITEM_DRAGON_SCALE
	pokemartlistend

SeviiStall_Text_Welcome:
	.string "Welcome to the market stall!\n"
	.string "Rare goods from every island!$"

SeviiStall_Text_Bye:
	.string "Rare goods don't come cheap.\n"
	.string "Come again!$"

	.align 2
SeviiMart_Items:
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_MAX_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_REVIVE
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_ESCAPE_ROPE
	.2byte ITEM_X_ATTACK
	pokemartlistend

OneIsland_KindleRoad_EmberSpa_EventScript_SpaHeal::
	lockall
	fadescreen FADE_TO_WHITE
	special HealPlayerParty
	fadescreen FADE_FROM_WHITE
	msgbox SeviiSpa_Text_Healed, MSGBOX_DEFAULT
	setvar VAR_TEMP_1, 1
	releaseall
	end

SeviiSpa_Text_Healed:
	.string "The hot spring water soothed your\n"
	.string "POKéMON. They look refreshed!$"

