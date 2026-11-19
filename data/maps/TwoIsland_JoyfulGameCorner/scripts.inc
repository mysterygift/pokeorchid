# 1 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 2 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_MapScripts::
# 3 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.byte 0
# 4 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 5 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	@ Game Corner prices
# 6 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.set TM_DOUBLE_TEAM_COINS, 1500
# 7 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.set TM_PSYCHIC_COINS, 3500
# 8 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.set TM_FLAMETHROWER_COINS, 4000
# 9 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.set TM_THUNDERBOLT_COINS, 4000
# 10 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.set TM_ICE_BEAM_COINS, 4000
# 11 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.set DOLL_COINS, 1000
# 12 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 13 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.set COINS_PRICE_50,  1000
# 14 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.set COINS_PRICE_500, 10000
# 15 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 16 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_CoinsClerk::
# 17 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	lock
# 18 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	faceplayer
# 19 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_ThisIsMauvilleGameCorner, MSGBOX_DEFAULT
# 20 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkitem ITEM_COIN_CASE
# 21 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, TwoIsland_JoyfulGameCorner_EventScript_NeedCoinCase
# 22 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	message TwoIsland_JoyfulGameCorner_Text_WereYouLookingForCoins
# 23 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	waitmessage
# 24 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	showmoneybox 0, 0
# 25 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	showcoinsbox 0, 5
# 26 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_ChooseCoinsDefault50
# 27 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 28 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_ChooseCoinsDefault50::
# 29 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	multichoicedefault 15, 0, MULTI_GAME_CORNER_COINS, 0, FALSE
# 30 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	switch VAR_RESULT
# 31 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	case 0, TwoIsland_JoyfulGameCorner_EventScript_Buy50Coins
# 32 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	case 1, TwoIsland_JoyfulGameCorner_EventScript_Buy500Coins
# 33 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_CancelBuyCoins
# 34 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 35 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 36 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
@ Unused
# 37 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_ChooseCoinsDefault500::
# 38 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	multichoicedefault 15, 0, MULTI_GAME_CORNER_COINS, 1, FALSE
# 39 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	switch VAR_RESULT
# 40 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	case 0, TwoIsland_JoyfulGameCorner_EventScript_Buy50Coins
# 41 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	case 1, TwoIsland_JoyfulGameCorner_EventScript_Buy500Coins
# 42 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_CancelBuyCoins
# 43 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 44 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 45 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_Buy50Coins::
# 46 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkcoins VAR_TEMP_1
# 47 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_ge VAR_TEMP_1, (MAX_COINS + 1 - 50), TwoIsland_JoyfulGameCorner_EventScript_NoRoomForCoins
# 48 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkmoney COINS_PRICE_50
# 49 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, TwoIsland_JoyfulGameCorner_EventScript_NotEnoughMoney
# 50 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	addcoins 50
# 51 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	removemoney COINS_PRICE_50
# 52 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	updatemoneybox
# 53 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	updatecoinsbox
# 54 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	playse SE_SHOP
# 55 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_ThankYouHereAreYourCoins, MSGBOX_DEFAULT
# 56 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	hidemoneybox
# 57 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	hidecoinsbox
# 58 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	release
# 59 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 60 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 61 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_Buy500Coins::
# 62 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkcoins VAR_TEMP_1
# 63 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_ge VAR_TEMP_1, (MAX_COINS + 1 - 500), TwoIsland_JoyfulGameCorner_EventScript_NoRoomForCoins
# 64 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkmoney COINS_PRICE_500
# 65 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, TwoIsland_JoyfulGameCorner_EventScript_NotEnoughMoney
# 66 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	addcoins 500
# 67 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	removemoney COINS_PRICE_500
# 68 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	updatemoneybox
# 69 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	updatecoinsbox
# 70 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	playse SE_SHOP
# 71 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_ThankYouHereAreYourCoins, MSGBOX_DEFAULT
# 72 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	hidemoneybox
# 73 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	hidecoinsbox
# 74 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	release
# 75 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 76 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 77 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_NeedCoinCase::
# 78 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_NeedCoinCaseForCoins, MSGBOX_DEFAULT
# 79 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	release
# 80 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 81 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 82 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_NotEnoughMoney::
# 83 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_DontHaveEnoughMoney, MSGBOX_DEFAULT
# 84 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	hidemoneybox
# 85 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	hidecoinsbox
# 86 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	release
# 87 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 88 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 89 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_CancelBuyCoins::
# 90 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_DontNeedCoinsThen, MSGBOX_DEFAULT
# 91 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	hidemoneybox
# 92 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	hidecoinsbox
# 93 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	release
# 94 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 95 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 96 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_NoRoomForCoins::
# 97 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_CoinCaseIsFull, MSGBOX_DEFAULT
# 98 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	hidemoneybox
# 99 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	hidecoinsbox
# 100 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	release
# 101 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 102 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 103 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_PrizeCornerDolls::
# 104 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	lock
# 105 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	faceplayer
# 106 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_ExchangeCoinsForPrizes, MSGBOX_DEFAULT
# 107 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkitem ITEM_COIN_CASE
# 108 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, TRUE, TwoIsland_JoyfulGameCorner_EventScript_ChooseDollPrizeMessage
# 109 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	release
# 110 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 111 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 112 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_ChooseDollPrizeMessage::
# 113 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	message TwoIsland_JoyfulGameCorner_Text_WhichPrize
# 114 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	waitmessage
# 115 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setvar VAR_TEMP_1, 0
# 116 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	showcoinsbox 0, 0
# 117 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_ChooseDollPrize
# 118 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 119 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_ReturnToChooseDollPrize::
# 120 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	message TwoIsland_JoyfulGameCorner_Text_WhichPrize
# 121 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	waitmessage
# 122 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_ChooseDollPrize
# 123 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 124 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_ChooseDollPrize::
# 125 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	multichoice 12, 0, MULTI_GAME_CORNER_DOLLS, FALSE
# 126 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	switch VAR_RESULT
# 127 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	case 0, TwoIsland_JoyfulGameCorner_EventScript_TreeckoDoll
# 128 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	case 1, TwoIsland_JoyfulGameCorner_EventScript_TorchicDoll
# 129 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	case 2, TwoIsland_JoyfulGameCorner_EventScript_MudkipDoll
# 130 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	case 3, TwoIsland_JoyfulGameCorner_EventScript_CancelDollSelect
# 131 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_CancelDollSelect
# 132 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 133 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 134 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_TreeckoDoll::
# 135 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setvar VAR_TEMP_1, 1
# 136 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	bufferdecorationname STR_VAR_1, DECOR_TREECKO_DOLL
# 137 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_ConfirmDollPrize
# 138 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 139 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_TorchicDoll::
# 140 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setvar VAR_TEMP_1, 2
# 141 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	bufferdecorationname STR_VAR_1, DECOR_TORCHIC_DOLL
# 142 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_ConfirmDollPrize
# 143 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 144 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_MudkipDoll::
# 145 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setvar VAR_TEMP_1, 3
# 146 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	bufferdecorationname STR_VAR_1, DECOR_MUDKIP_DOLL
# 147 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_ConfirmDollPrize
# 148 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 149 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_ConfirmDollPrize::
# 150 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_SoYourChoiceIsX, MSGBOX_YESNO
# 151 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, NO, TwoIsland_JoyfulGameCorner_EventScript_CancelDollSelect
# 152 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	switch VAR_TEMP_1
# 153 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	case 1, TwoIsland_JoyfulGameCorner_EventScript_BuyTreeckoDoll
# 154 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	case 2, TwoIsland_JoyfulGameCorner_EventScript_BuyTorchicDoll
# 155 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	case 3, TwoIsland_JoyfulGameCorner_EventScript_BuyMudkipDoll
# 156 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 157 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 158 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_BuyTreeckoDoll::
# 159 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkcoins VAR_TEMP_2
# 160 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_lt VAR_TEMP_2, DOLL_COINS, TwoIsland_JoyfulGameCorner_EventScript_NotEnoughCoinsForDoll
# 161 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	bufferdecorationname STR_VAR_2, DECOR_TREECKO_DOLL
# 162 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkdecorspace DECOR_TREECKO_DOLL
# 163 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, TwoIsland_JoyfulGameCorner_EventScript_NoRoomForDoll
# 164 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	removecoins DOLL_COINS
# 165 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	adddecoration DECOR_TREECKO_DOLL
# 166 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	updatecoinsbox
# 167 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	playse SE_SHOP
# 168 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_SendToYourHomePC, MSGBOX_DEFAULT
# 169 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_ReturnToChooseDollPrize
# 170 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 171 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 172 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_BuyTorchicDoll::
# 173 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkcoins VAR_TEMP_2
# 174 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_lt VAR_TEMP_2, DOLL_COINS, TwoIsland_JoyfulGameCorner_EventScript_NotEnoughCoinsForDoll
# 175 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	bufferdecorationname STR_VAR_2, DECOR_TORCHIC_DOLL
# 176 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkdecorspace DECOR_TORCHIC_DOLL
# 177 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, TwoIsland_JoyfulGameCorner_EventScript_NoRoomForDoll
# 178 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	removecoins DOLL_COINS
# 179 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	adddecoration DECOR_TORCHIC_DOLL
# 180 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	updatecoinsbox
# 181 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	playse SE_SHOP
# 182 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_SendToYourHomePC, MSGBOX_DEFAULT
# 183 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_ReturnToChooseDollPrize
# 184 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 185 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 186 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_BuyMudkipDoll::
# 187 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkcoins VAR_TEMP_2
# 188 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_lt VAR_TEMP_2, DOLL_COINS, TwoIsland_JoyfulGameCorner_EventScript_NotEnoughCoinsForDoll
# 189 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	bufferdecorationname STR_VAR_2, DECOR_MUDKIP_DOLL
# 190 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkdecorspace DECOR_MUDKIP_DOLL
# 191 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, TwoIsland_JoyfulGameCorner_EventScript_NoRoomForDoll
# 192 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	removecoins DOLL_COINS
# 193 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	adddecoration DECOR_MUDKIP_DOLL
# 194 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	updatecoinsbox
# 195 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	playse SE_SHOP
# 196 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_SendToYourHomePC, MSGBOX_DEFAULT
# 197 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_ReturnToChooseDollPrize
# 198 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 199 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 200 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_NotEnoughCoinsForDoll::
# 201 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_NotEnoughCoins, MSGBOX_DEFAULT
# 202 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_ReturnToChooseDollPrize
# 203 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 204 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 205 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_NoRoomForDoll::
# 206 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	call Common_EventScript_NoRoomForDecor
# 207 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_ReturnToChooseDollPrize
# 208 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 209 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 210 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_CancelDollSelect::
# 211 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_OhIsThatSo, MSGBOX_DEFAULT
# 212 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	hidecoinsbox
# 213 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	release
# 214 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 215 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 216 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_PrizeCornerTMs::
# 217 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	lock
# 218 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	faceplayer
# 219 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_ExchangeCoinsForPrizes, MSGBOX_DEFAULT
# 220 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkitem ITEM_COIN_CASE
# 221 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, TRUE, TwoIsland_JoyfulGameCorner_EventScript_ChooseTMPrizeMessage
# 222 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	release
# 223 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 224 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 225 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_ChooseTMPrizeMessage::
# 226 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	message TwoIsland_JoyfulGameCorner_Text_WhichPrize
# 227 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	waitmessage
# 228 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setvar VAR_TEMP_1, 0
# 229 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	showcoinsbox 0, 0
# 230 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_ChooseTMPrize
# 231 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 232 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_ReturnToChooseTMPrize::
# 233 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	message TwoIsland_JoyfulGameCorner_Text_WhichPrize
# 234 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	waitmessage
# 235 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_ChooseTMPrize
# 236 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 237 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_ChooseTMPrize::
# 238 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	multichoice 12, 0, MULTI_GAME_CORNER_TMS, FALSE
# 239 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	switch VAR_RESULT
# 240 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	case 0, TwoIsland_JoyfulGameCorner_EventScript_TMDoubleTeam
# 241 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	case 1, TwoIsland_JoyfulGameCorner_EventScript_TMPsychic
# 242 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	case 2, TwoIsland_JoyfulGameCorner_EventScript_TMFlamethrower
# 243 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	case 3, TwoIsland_JoyfulGameCorner_EventScript_TMThunderbolt
# 244 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	case 4, TwoIsland_JoyfulGameCorner_EventScript_TMIceBeam
# 245 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	case 5, TwoIsland_JoyfulGameCorner_EventScript_CancelTMSelect
# 246 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_CancelTMSelect
# 247 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 248 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 249 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_TMDoubleTeam::
# 250 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setvar VAR_TEMP_1, 1
# 251 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	bufferitemname STR_VAR_1, ITEM_TM_DOUBLE_TEAM
# 252 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setvar VAR_0x8004, ITEM_TM_DOUBLE_TEAM
# 253 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_ConfirmTMPrize
# 254 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 255 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_TMPsychic::
# 256 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setvar VAR_TEMP_1, 2
# 257 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	bufferitemname STR_VAR_1, ITEM_TM_PSYCHIC
# 258 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setvar VAR_0x8004, ITEM_TM_PSYCHIC
# 259 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_ConfirmTMPrize
# 260 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 261 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_TMFlamethrower::
# 262 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setvar VAR_TEMP_1, 3
# 263 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	bufferitemname STR_VAR_1, ITEM_TM_FLAMETHROWER
# 264 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setvar VAR_0x8004, ITEM_TM_FLAMETHROWER
# 265 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_ConfirmTMPrize
# 266 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 267 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_TMThunderbolt::
# 268 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setvar VAR_TEMP_1, 4
# 269 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	bufferitemname STR_VAR_1, ITEM_TM_THUNDERBOLT
# 270 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setvar VAR_0x8004, ITEM_TM_THUNDERBOLT
# 271 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_ConfirmTMPrize
# 272 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 273 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_TMIceBeam::
# 274 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setvar VAR_TEMP_1, 5
# 275 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	bufferitemname STR_VAR_1, ITEM_TM_ICE_BEAM
# 276 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setvar VAR_0x8004, ITEM_TM_ICE_BEAM
# 277 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_ConfirmTMPrize
# 278 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 279 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_ConfirmTMPrize::
# 280 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	special BufferTMHMMoveName
# 281 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_SoYourChoiceIsTheTMX, MSGBOX_YESNO
# 282 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, NO, TwoIsland_JoyfulGameCorner_EventScript_CancelTMSelect
# 283 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	switch VAR_TEMP_1
# 284 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	case 1, TwoIsland_JoyfulGameCorner_EventScript_BuyTMDoubleTeam
# 285 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	case 2, TwoIsland_JoyfulGameCorner_EventScript_BuyTMPsychic
# 286 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	case 3, TwoIsland_JoyfulGameCorner_EventScript_BuyTMFlamethrower
# 287 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	case 4, TwoIsland_JoyfulGameCorner_EventScript_BuyTMThunderbolt
# 288 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	case 5, TwoIsland_JoyfulGameCorner_EventScript_BuyTMIceBeam
# 289 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 290 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 291 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_BuyTMDoubleTeam::
# 292 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkcoins VAR_TEMP_2
# 293 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_lt VAR_TEMP_2, TM_DOUBLE_TEAM_COINS, TwoIsland_JoyfulGameCorner_EventScript_NotEnoughCoinsForTM
# 294 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkitemspace ITEM_TM_DOUBLE_TEAM
# 295 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, TwoIsland_JoyfulGameCorner_EventScript_NoRoomForTM
# 296 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	removecoins TM_DOUBLE_TEAM_COINS
# 297 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	additem ITEM_TM_DOUBLE_TEAM
# 298 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	updatecoinsbox
# 299 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	playse SE_SHOP
# 300 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_HereYouGo, MSGBOX_DEFAULT
# 301 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_ReturnToChooseTMPrize
# 302 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 303 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 304 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_BuyTMPsychic::
# 305 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkcoins VAR_TEMP_2
# 306 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_lt VAR_TEMP_2, TM_PSYCHIC_COINS, TwoIsland_JoyfulGameCorner_EventScript_NotEnoughCoinsForTM
# 307 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkitemspace ITEM_TM_PSYCHIC
# 308 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, TwoIsland_JoyfulGameCorner_EventScript_NoRoomForTM
# 309 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	removecoins TM_PSYCHIC_COINS
# 310 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	additem ITEM_TM_PSYCHIC
# 311 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	updatecoinsbox
# 312 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	playse SE_SHOP
# 313 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_HereYouGo, MSGBOX_DEFAULT
# 314 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_ReturnToChooseTMPrize
# 315 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 316 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 317 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_BuyTMFlamethrower::
# 318 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkcoins VAR_TEMP_2
# 319 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_lt VAR_TEMP_2, TM_FLAMETHROWER_COINS, TwoIsland_JoyfulGameCorner_EventScript_NotEnoughCoinsForTM
# 320 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkitemspace ITEM_TM_FLAMETHROWER
# 321 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, TwoIsland_JoyfulGameCorner_EventScript_NoRoomForTM
# 322 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	removecoins TM_FLAMETHROWER_COINS
# 323 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	additem ITEM_TM_FLAMETHROWER
# 324 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	updatecoinsbox
# 325 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	playse SE_SHOP
# 326 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_HereYouGo, MSGBOX_DEFAULT
# 327 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_ReturnToChooseTMPrize
# 328 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 329 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 330 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_BuyTMThunderbolt::
# 331 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkcoins VAR_TEMP_2
# 332 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_lt VAR_TEMP_2, TM_THUNDERBOLT_COINS, TwoIsland_JoyfulGameCorner_EventScript_NotEnoughCoinsForTM
# 333 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkitemspace ITEM_TM_THUNDERBOLT
# 334 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, TwoIsland_JoyfulGameCorner_EventScript_NoRoomForTM
# 335 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	removecoins TM_THUNDERBOLT_COINS
# 336 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	additem ITEM_TM_THUNDERBOLT
# 337 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	updatecoinsbox
# 338 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	playse SE_SHOP
# 339 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_HereYouGo, MSGBOX_DEFAULT
# 340 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_ReturnToChooseTMPrize
# 341 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 342 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 343 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_BuyTMIceBeam::
# 344 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkcoins VAR_TEMP_2
# 345 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_lt VAR_TEMP_2, TM_ICE_BEAM_COINS, TwoIsland_JoyfulGameCorner_EventScript_NotEnoughCoinsForTM
# 346 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkitemspace ITEM_TM_ICE_BEAM
# 347 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, TwoIsland_JoyfulGameCorner_EventScript_NoRoomForTM
# 348 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	removecoins TM_ICE_BEAM_COINS
# 349 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	additem ITEM_TM_ICE_BEAM
# 350 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	updatecoinsbox
# 351 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	playse SE_SHOP
# 352 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_HereYouGo, MSGBOX_DEFAULT
# 353 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_ReturnToChooseTMPrize
# 354 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 355 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 356 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_NotEnoughCoinsForTM::
# 357 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_NotEnoughCoins, MSGBOX_DEFAULT
# 358 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_ReturnToChooseTMPrize
# 359 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 360 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 361 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_NoRoomForTM::
# 362 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	call Common_EventScript_BagIsFull
# 363 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_ReturnToChooseTMPrize
# 364 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 365 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 366 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_CancelTMSelect::
# 367 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_OhIsThatSo, MSGBOX_DEFAULT
# 368 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	hidecoinsbox
# 369 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	release
# 370 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 371 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 372 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_Woman2::
# 373 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_CoinsAreNeededToPlay, MSGBOX_NPC
# 374 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 375 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 376 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_Gentleman::
# 377 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_RouletteOnlyLuck, MSGBOX_NPC
# 378 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 379 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 380 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_Girl::
# 381 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	lock
# 382 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	faceplayer
# 383 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_set FLAG_RECEIVED_STARTER_DOLL, TwoIsland_JoyfulGameCorner_EventScript_ReceivedStarterDoll
# 384 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_GotTwoOfSameDollWantOne, MSGBOX_YESNO
# 385 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, NO, TwoIsland_JoyfulGameCorner_EventScript_DeclineStarterDoll
# 386 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	switch VAR_STARTER_MON
# 387 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	case 0, TwoIsland_JoyfulGameCorner_EventScript_GiveTreeckoDoll
# 388 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	case 1, TwoIsland_JoyfulGameCorner_EventScript_GiveTorchicDoll
# 389 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	case 2, TwoIsland_JoyfulGameCorner_EventScript_GiveMudkipDoll
# 390 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 391 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 392 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_GiveTreeckoDoll::
# 393 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	bufferdecorationname STR_VAR_2, DECOR_TREECKO_DOLL
# 394 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkdecorspace DECOR_TREECKO_DOLL
# 395 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, TwoIsland_JoyfulGameCorner_EventScript_NoRoomForStarterDoll
# 396 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_HereYouGo2, MSGBOX_DEFAULT
# 397 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	givedecoration DECOR_TREECKO_DOLL
# 398 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setflag FLAG_RECEIVED_STARTER_DOLL
# 399 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_ReceivedStarterDoll
# 400 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 401 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 402 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_GiveTorchicDoll::
# 403 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	bufferdecorationname STR_VAR_2, DECOR_TORCHIC_DOLL
# 404 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkdecorspace DECOR_TORCHIC_DOLL
# 405 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, TwoIsland_JoyfulGameCorner_EventScript_NoRoomForStarterDoll
# 406 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_HereYouGo2, MSGBOX_DEFAULT
# 407 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	givedecoration DECOR_TORCHIC_DOLL
# 408 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setflag FLAG_RECEIVED_STARTER_DOLL
# 409 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_ReceivedStarterDoll
# 410 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 411 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 412 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_GiveMudkipDoll::
# 413 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	bufferdecorationname STR_VAR_2, DECOR_MUDKIP_DOLL
# 414 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkdecorspace DECOR_MUDKIP_DOLL
# 415 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, TwoIsland_JoyfulGameCorner_EventScript_NoRoomForStarterDoll
# 416 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_HereYouGo2, MSGBOX_DEFAULT
# 417 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	givedecoration DECOR_MUDKIP_DOLL
# 418 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setflag FLAG_RECEIVED_STARTER_DOLL
# 419 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_ReceivedStarterDoll
# 420 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 421 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 422 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_NoRoomForStarterDoll::
# 423 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	call Common_EventScript_NoRoomForDecor
# 424 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_YouWantItButNotNow, MSGBOX_DEFAULT
# 425 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	release
# 426 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 427 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 428 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_DeclineStarterDoll::
# 429 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_DontBeNegative, MSGBOX_DEFAULT
# 430 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	release
# 431 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 432 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 433 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_ReceivedStarterDoll::
# 434 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_CantWinJackpot, MSGBOX_DEFAULT
# 435 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	release
# 436 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 437 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 438 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_PokefanM::
# 439 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	lock
# 440 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	faceplayer
# 441 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkitem ITEM_COIN_CASE
# 442 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, TRUE, TwoIsland_JoyfulGameCorner_EventScript_TryGive20Coins
# 443 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_NeedCoinCaseGoNextDoor, MSGBOX_DEFAULT
# 444 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_NPCReturnToSlots
# 445 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 446 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 447 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_TryGive20Coins::
# 448 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_set FLAG_RECEIVED_20_COINS, TwoIsland_JoyfulGameCorner_EventScript_PokefanMNormal
# 449 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkcoins VAR_TEMP_1
# 450 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_ge VAR_TEMP_1, 1, TwoIsland_JoyfulGameCorner_EventScript_PokefanMNormal @ Only give 20 coins if player has no coins
# 451 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setflag FLAG_RECEIVED_20_COINS
# 452 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	addcoins 20
# 453 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_LuckOnlyLastSoLongTakeCoins, MSGBOX_DEFAULT
# 454 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	playse SE_SHOP
# 455 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_PokefanMNormal
# 456 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 457 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 458 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_PokefanMNormal::
# 459 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_MauvilleSomethingForEveryone, MSGBOX_DEFAULT
# 460 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_NPCReturnToSlots
# 461 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 462 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 463 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_OldMan::
# 464 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	lock
# 465 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	faceplayer
# 466 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_RouletteTablesDifferentRates, MSGBOX_DEFAULT
# 467 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_NPCReturnToSlots
# 468 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 469 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 470 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_Cook::
# 471 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	lock
# 472 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	faceplayer
# 473 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_EasyToLoseTrackOfTime, MSGBOX_DEFAULT
# 474 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_NPCReturnToSlots
# 475 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 476 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 477 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_Man::
# 478 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	lock
# 479 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	faceplayer
# 480 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_UpTo3CoinsCanBeUsed, MSGBOX_DEFAULT
# 481 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_NPCReturnToSlots
# 482 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 483 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 484 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_NPCReturnToSlots::
# 485 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	closemessage
# 486 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	applymovement VAR_LAST_TALKED, Common_Movement_FaceOriginalDirection
# 487 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	waitmovement 0
# 488 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	release
# 489 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 490 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 491 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_Maniac::
# 492 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	lock
# 493 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	faceplayer
# 494 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_DifficultToStopOn7, MSGBOX_DEFAULT
# 495 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_NPCReturnToSlots
# 496 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 497 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 498 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_Woman::
# 499 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	lock
# 500 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	faceplayer
# 501 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_HeresSomeSlotsInfo, MSGBOX_DEFAULT
# 502 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto TwoIsland_JoyfulGameCorner_EventScript_NPCReturnToSlots
# 503 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 504 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 505 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_SlotMachine0::
# 506 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	lockall
# 507 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkitem ITEM_COIN_CASE
# 508 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, TwoIsland_JoyfulGameCorner_EventScript_NoCoinCase
# 509 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setvar VAR_0x8004, 0
# 510 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	specialvar VAR_RESULT, GetSlotMachineId
# 511 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	playslotmachine VAR_RESULT
# 512 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	releaseall
# 513 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 514 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 515 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_SlotMachine1::
# 516 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	lockall
# 517 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkitem ITEM_COIN_CASE
# 518 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, TwoIsland_JoyfulGameCorner_EventScript_NoCoinCase
# 519 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setvar VAR_0x8004, 1
# 520 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	specialvar VAR_RESULT, GetSlotMachineId
# 521 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	playslotmachine VAR_RESULT
# 522 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	releaseall
# 523 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 524 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 525 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_SlotMachine2::
# 526 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	lockall
# 527 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkitem ITEM_COIN_CASE
# 528 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, TwoIsland_JoyfulGameCorner_EventScript_NoCoinCase
# 529 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setvar VAR_0x8004, 2
# 530 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	specialvar VAR_RESULT, GetSlotMachineId
# 531 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	playslotmachine VAR_RESULT
# 532 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	releaseall
# 533 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 534 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 535 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_SlotMachine3::
# 536 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	lockall
# 537 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkitem ITEM_COIN_CASE
# 538 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, TwoIsland_JoyfulGameCorner_EventScript_NoCoinCase
# 539 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setvar VAR_0x8004, 3
# 540 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	specialvar VAR_RESULT, GetSlotMachineId
# 541 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	playslotmachine VAR_RESULT
# 542 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	releaseall
# 543 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 544 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 545 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_SlotMachine4::
# 546 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	lockall
# 547 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkitem ITEM_COIN_CASE
# 548 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, TwoIsland_JoyfulGameCorner_EventScript_NoCoinCase
# 549 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setvar VAR_0x8004, 4
# 550 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	specialvar VAR_RESULT, GetSlotMachineId
# 551 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	playslotmachine VAR_RESULT
# 552 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	releaseall
# 553 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 554 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 555 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_SlotMachine5::
# 556 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	lockall
# 557 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkitem ITEM_COIN_CASE
# 558 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, TwoIsland_JoyfulGameCorner_EventScript_NoCoinCase
# 559 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setvar VAR_0x8004, 5
# 560 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	specialvar VAR_RESULT, GetSlotMachineId
# 561 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	playslotmachine VAR_RESULT
# 562 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	releaseall
# 563 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 564 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 565 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_SlotMachine6::
# 566 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	lockall
# 567 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkitem ITEM_COIN_CASE
# 568 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, TwoIsland_JoyfulGameCorner_EventScript_NoCoinCase
# 569 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setvar VAR_0x8004, 6
# 570 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	specialvar VAR_RESULT, GetSlotMachineId
# 571 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	playslotmachine VAR_RESULT
# 572 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	releaseall
# 573 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 574 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 575 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_SlotMachine7::
# 576 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	lockall
# 577 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkitem ITEM_COIN_CASE
# 578 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, TwoIsland_JoyfulGameCorner_EventScript_NoCoinCase
# 579 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setvar VAR_0x8004, 7
# 580 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	specialvar VAR_RESULT, GetSlotMachineId
# 581 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	playslotmachine VAR_RESULT
# 582 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	releaseall
# 583 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 584 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 585 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_SlotMachine8::
# 586 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	lockall
# 587 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkitem ITEM_COIN_CASE
# 588 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, TwoIsland_JoyfulGameCorner_EventScript_NoCoinCase
# 589 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setvar VAR_0x8004, 8
# 590 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	specialvar VAR_RESULT, GetSlotMachineId
# 591 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	playslotmachine VAR_RESULT
# 592 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	releaseall
# 593 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 594 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 595 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_SlotMachine9::
# 596 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	lockall
# 597 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkitem ITEM_COIN_CASE
# 598 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, TwoIsland_JoyfulGameCorner_EventScript_NoCoinCase
# 599 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setvar VAR_0x8004, 9
# 600 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	specialvar VAR_RESULT, GetSlotMachineId
# 601 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	playslotmachine VAR_RESULT
# 602 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	releaseall
# 603 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 604 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 605 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_SlotMachine10::
# 606 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	lockall
# 607 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkitem ITEM_COIN_CASE
# 608 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, TwoIsland_JoyfulGameCorner_EventScript_NoCoinCase
# 609 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setvar VAR_0x8004, 10
# 610 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	specialvar VAR_RESULT, GetSlotMachineId
# 611 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	playslotmachine VAR_RESULT
# 612 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	releaseall
# 613 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 614 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 615 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_SlotMachine11::
# 616 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	lockall
# 617 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	checkitem ITEM_COIN_CASE
# 618 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, TwoIsland_JoyfulGameCorner_EventScript_NoCoinCase
# 619 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	setvar VAR_0x8004, 11
# 620 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	specialvar VAR_RESULT, GetSlotMachineId
# 621 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	playslotmachine VAR_RESULT
# 622 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	releaseall
# 623 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 624 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 625 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_EventScript_NoCoinCase::
# 626 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_Text_CantPlayWithNoCoinCase, MSGBOX_DEFAULT
# 627 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	releaseall
# 628 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	end
# 629 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 630 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_ThisIsMauvilleGameCorner:
# 631 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "This is MAUVILLE GAME CORNER.$"
# 632 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 633 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_NeedCoinCaseForCoins:
# 634 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "Okay, you wanted some COINS for\n"
# 635 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "the games?\p"
# 636 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "But you don't have a COIN CASE for\n"
# 637 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "stowing the COINS.$"
# 638 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 639 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_WereYouLookingForCoins:
# 640 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "Were you looking for COINS?\p"
# 641 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "It's ¥1000 for 50 COINS.\n"
# 642 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "Would you like some?$"
# 643 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 644 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_ThankYouHereAreYourCoins:
# 645 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "Thank you very much!\n"
# 646 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "Here are your COINS!$"
# 647 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 648 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_DontHaveEnoughMoney:
# 649 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "Um… You don't appear to have\n"
# 650 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "enough money…$"
# 651 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 652 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_CoinCaseIsFull:
# 653 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "Oh?\n"
# 654 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "Your COIN CASE is full.$"
# 655 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 656 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_DontNeedCoinsThen:
# 657 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "Oh… You don't need COINS, then?\n"
# 658 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "Good luck on your adventure!$"
# 659 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 660 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_ExchangeCoinsForPrizes:
# 661 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "Welcome.\p"
# 662 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "You can exchange your COINS for\n"
# 663 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "prizes here.$"
# 664 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 665 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_WhichPrize:
# 666 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "Which prize would you like?$"
# 667 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 668 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_SoYourChoiceIsTheTMX:
# 669 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "So your choice is\n"
# 670 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "the {STR_VAR_1} {STR_VAR_2}?$"
# 671 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 672 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_SendToYourHomePC:
# 673 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "Thank you!\n"
# 674 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "We'll send it to your PC at home.$"
# 675 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 676 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_NotEnoughCoins:
# 677 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "You don't have enough COINS.$"
# 678 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 679 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
@ Unused
# 680 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_NoRoomForPlacingDecor:
# 681 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "There isn't any room available for\n"
# 682 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "placing {STR_VAR_1}.$"
# 683 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 684 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_OhIsThatSo:
# 685 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "Oh, is that so? \n"
# 686 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "You need to save some COINS before\l"
# 687 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "coming back here.$"
# 688 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 689 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_SoYourChoiceIsX:
# 690 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "So your choice is {STR_VAR_1}?$"
# 691 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 692 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_HereYouGo:
# 693 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "Here you go!$"
# 694 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 695 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
@ Unused
# 696 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_CantCarryAnyMore:
# 697 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "Oh, you can't carry any more than that.$"
# 698 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 699 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_GotTwoOfSameDollWantOne:
# 700 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "I made a mistake and got two of\n"
# 701 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "the same DOLLS.\p"
# 702 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "Would you like one of them?$"
# 703 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 704 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_HereYouGo2:
# 705 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "Here you go!$"
# 706 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 707 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_YouWantItButNotNow:
# 708 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "Huh?\n"
# 709 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "You want it, but not right now?$"
# 710 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 711 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_DontBeNegative:
# 712 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "Oh, don't be so negative!\n"
# 713 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "You can have this!$"
# 714 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 715 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_CantWinJackpot:
# 716 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "There's a prize I want, but I can't win\n"
# 717 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "the jackpot.$"
# 718 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 719 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_NeedCoinCaseGoNextDoor:
# 720 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "Hey, kid, if you want to play here,\n"
# 721 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "you need a COIN CASE.\p"
# 722 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "I think the young lady next door\n"
# 723 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "had one. Go see her!$"
# 724 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 725 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_LuckOnlyLastSoLongTakeCoins:
# 726 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "My luck can only last so long.\n"
# 727 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "This is too much for me.\l"
# 728 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "Here, take some COINS!$"
# 729 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 730 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_MauvilleSomethingForEveryone:
# 731 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "MAUVILLE has something for\n"
# 732 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "everyone.\p"
# 733 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "For me, it's the GAME CORNER.$"
# 734 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 735 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_RouletteTablesDifferentRates:
# 736 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "The ROULETTE tables have different\n"
# 737 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "rates.\p"
# 738 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "Check your COINS if you're going to\n"
# 739 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "pick a table.$"
# 740 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 741 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_EasyToLoseTrackOfTime:
# 742 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "It's easy to lose track of time in here. \n"
# 743 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "I should get back to work.$"
# 744 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 745 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_CoinsAreNeededToPlay:
# 746 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "COINS are needed to play here\n"
# 747 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "in the GAME CORNER.$"
# 748 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 749 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_RouletteOnlyLuck:
# 750 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "This ROULETTE thing…\n"
# 751 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "It's rather demanding.\p"
# 752 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "Win or lose, it's only by luck.$"
# 753 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 754 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_UpTo3CoinsCanBeUsed:
# 755 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "Up to three COINS can be used to play\n"
# 756 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "the SLOTS.$"
# 757 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 758 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_DifficultToStopOn7:
# 759 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "It's very difficult to make it stop\n"
# 760 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "right on “7.”\p"
# 761 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "If it stops on “7” during the REEL TIME\n"
# 762 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "bonus game, you'll receive extra COINS.$"
# 763 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 764 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_HeresSomeSlotsInfo:
# 765 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "Here's some information for you\n"
# 766 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "about the SLOTS.\p"
# 767 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "The more lightning bolts you stock,\n"
# 768 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "the more REEL TIME chances you get.\p"
# 769 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "In a game with the maximum five\n"
# 770 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "REEL TIME chances…\p"
# 771 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "It is possible to receive four regular\n"
# 772 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "bonuses, then a big bonus.\p"
# 773 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "That would total 660 COINS, but it's\n"
# 774 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "very difficult to get.$"
# 775 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"

# 776 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
TwoIsland_JoyfulGameCorner_Text_CantPlayWithNoCoinCase:
# 777 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "You can't play if you don't have\n"
# 778 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "a COIN CASE.$"

TwoIsland_JoyfulGameCorner_EventScript_JoyfulWoman2::
# 782 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_EventScript_JoyfulWoman2_Text_0, MSGBOX_NPC
	return


TwoIsland_JoyfulGameCorner_EventScript_JoyfulGentleman::
# 786 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_EventScript_JoyfulGentleman_Text_0, MSGBOX_NPC
	return


TwoIsland_JoyfulGameCorner_EventScript_JoyfulOldMan::
# 790 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_EventScript_JoyfulOldMan_Text_0, MSGBOX_NPC
	return


TwoIsland_JoyfulGameCorner_EventScript_JoyfulCook::
# 794 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_EventScript_JoyfulCook_Text_0, MSGBOX_NPC
	return


TwoIsland_JoyfulGameCorner_EventScript_JoyfulMan::
# 798 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_EventScript_JoyfulMan_Text_0, MSGBOX_NPC
	return


TwoIsland_JoyfulGameCorner_EventScript_JoyfulManiac::
# 802 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_EventScript_JoyfulManiac_Text_0, MSGBOX_NPC
	return


TwoIsland_JoyfulGameCorner_EventScript_JoyfulWoman::
# 806 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	msgbox TwoIsland_JoyfulGameCorner_EventScript_JoyfulWoman_Text_0, MSGBOX_NPC
	return


TwoIsland_JoyfulGameCorner_EventScript_JoyfulWoman2_Text_0:
# 782 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "The slots here are a little kinder than\n"
	.string "the ones in Tosa. Or maybe I'm just\l"
	.string "lucky today!$"

TwoIsland_JoyfulGameCorner_EventScript_JoyfulGentleman_Text_0:
# 786 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "I sailed all the way from Tosa just to\n"
	.string "play here. The owner's smile is worth the\l"
	.string "trip.$"

TwoIsland_JoyfulGameCorner_EventScript_JoyfulOldMan_Text_0:
# 790 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "I opened this Game Corner so the\n"
	.string "islanders would have somewhere joyful\l"
	.string "to gather.$"

TwoIsland_JoyfulGameCorner_EventScript_JoyfulCook_Text_0:
# 794 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "I cook for the market stall, then spend\n"
	.string "my wages right here. Ha ha!$"

TwoIsland_JoyfulGameCorner_EventScript_JoyfulMan_Text_0:
# 798 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "Roulette is all luck. Slots? Also luck. I\n"
	.string "love it.$"

TwoIsland_JoyfulGameCorner_EventScript_JoyfulManiac_Text_0:
# 802 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "I've counted every reel symbol. Doesn't\n"
	.string "help at all.$"

TwoIsland_JoyfulGameCorner_EventScript_JoyfulWoman_Text_0:
# 806 "data/maps/TwoIsland_JoyfulGameCorner/scripts.pory"
	.string "The prize corner has dolls you can't get\n"
	.string "anywhere else in the islands.$"
