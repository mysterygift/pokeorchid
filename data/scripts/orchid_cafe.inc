@ The kopi counter in every Pokemon Centre (Pokemon Orchid)
Common_EventScript_OrchidCafe::
	lock
	faceplayer
	message Common_Text_OrchidCafe_Welcome
	waitmessage
	pokemart Common_Pokemart_OrchidCafe
	msgbox Common_Text_OrchidCafe_ComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Common_Pokemart_OrchidCafe:
	.2byte ITEM_KOPI
	.2byte ITEM_STEAMED_BAO
	.2byte ITEM_KAYA_TOAST
	pokemartlistend

Common_Text_OrchidCafe_Welcome:
	.string "Kopi, bao, kaya toast!\n"
	.string "What'll it be?$"

Common_Text_OrchidCafe_ComeAgain:
	.string "Come back while it's hot!$"
