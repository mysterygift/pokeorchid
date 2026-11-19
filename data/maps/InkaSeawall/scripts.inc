InkaSeawall_MapScripts::
	.byte 0


InkaSeawall_EventScript_Sign1::
# 5 "data/maps/InkaSeawall/scripts.pory"
	msgbox InkaSeawall_EventScript_Sign1_Text_0, MSGBOX_SIGN
	return


InkaSeawall_EventScript_Sign2::
# 9 "data/maps/InkaSeawall/scripts.pory"
	msgbox InkaSeawall_EventScript_Sign2_Text_0, MSGBOX_SIGN
	return


InkaSeawall_EventScript_Amir::
# 12 "data/maps/InkaSeawall/scripts.pory"
	trainerbattle_double TRAINER_AMIR_AND_NUR, InkaSeawall_Text_AmirIntro, InkaSeawall_Text_AmirDefeat, InkaSeawall_Text_AmirNotEnough
# 13 "data/maps/InkaSeawall/scripts.pory"
	msgbox InkaSeawall_Text_AmirPost, MSGBOX_AUTOCLOSE
	return


InkaSeawall_EventScript_Nur::
# 33 "data/maps/InkaSeawall/scripts.pory"
	trainerbattle_double TRAINER_AMIR_AND_NUR, InkaSeawall_Text_NurIntro, InkaSeawall_Text_NurDefeat, InkaSeawall_Text_NurNotEnough
# 34 "data/maps/InkaSeawall/scripts.pory"
	msgbox InkaSeawall_Text_NurPost, MSGBOX_AUTOCLOSE
	return


InkaSeawall_EventScript_Jun::
# 54 "data/maps/InkaSeawall/scripts.pory"
	trainerbattle_double TRAINER_JUN_AND_HUI, InkaSeawall_Text_JunIntro, InkaSeawall_Text_JunDefeat, InkaSeawall_Text_JunNotEnough
# 55 "data/maps/InkaSeawall/scripts.pory"
	msgbox InkaSeawall_Text_JunPost, MSGBOX_AUTOCLOSE
	return


InkaSeawall_EventScript_Hui::
# 75 "data/maps/InkaSeawall/scripts.pory"
	trainerbattle_double TRAINER_JUN_AND_HUI, InkaSeawall_Text_HuiIntro, InkaSeawall_Text_HuiDefeat, InkaSeawall_Text_HuiNotEnough
# 76 "data/maps/InkaSeawall/scripts.pory"
	msgbox InkaSeawall_Text_HuiPost, MSGBOX_AUTOCLOSE
	return


InkaSeawall_EventScript_Chloe::
# 96 "data/maps/InkaSeawall/scripts.pory"
	trainerbattle_single TRAINER_CHLOE, InkaSeawall_Text_ChloeIntro, InkaSeawall_Text_ChloeDefeat
# 97 "data/maps/InkaSeawall/scripts.pory"
	msgbox InkaSeawall_Text_ChloePost, MSGBOX_AUTOCLOSE
	return


InkaSeawall_EventScript_Imran::
# 113 "data/maps/InkaSeawall/scripts.pory"
	trainerbattle_single TRAINER_IMRAN, InkaSeawall_Text_ImranIntro, InkaSeawall_Text_ImranDefeat
# 114 "data/maps/InkaSeawall/scripts.pory"
	msgbox InkaSeawall_Text_ImranPost, MSGBOX_AUTOCLOSE
	return


InkaSeawall_EventScript_Siti::
# 130 "data/maps/InkaSeawall/scripts.pory"
	trainerbattle_single TRAINER_SITI, InkaSeawall_Text_SitiIntro, InkaSeawall_Text_SitiDefeat
# 131 "data/maps/InkaSeawall/scripts.pory"
	msgbox InkaSeawall_Text_SitiPost, MSGBOX_AUTOCLOSE
	return


InkaSeawall_EventScript_UncleHock::
# 147 "data/maps/InkaSeawall/scripts.pory"
	trainerbattle_double TRAINER_HOCK_AND_LAN, InkaSeawall_Text_UncleHockIntro, InkaSeawall_Text_UncleHockDefeat, InkaSeawall_Text_UncleHockNotEnough
# 148 "data/maps/InkaSeawall/scripts.pory"
	msgbox InkaSeawall_Text_UncleHockPost, MSGBOX_AUTOCLOSE
	return


InkaSeawall_EventScript_AuntieLan::
# 168 "data/maps/InkaSeawall/scripts.pory"
	trainerbattle_double TRAINER_HOCK_AND_LAN, InkaSeawall_Text_AuntieLanIntro, InkaSeawall_Text_AuntieLanDefeat, InkaSeawall_Text_AuntieLanNotEnough
# 169 "data/maps/InkaSeawall/scripts.pory"
	msgbox InkaSeawall_Text_AuntieLanPost, MSGBOX_AUTOCLOSE
	return


InkaSeawall_EventScript_Yuki::
# 189 "data/maps/InkaSeawall/scripts.pory"
	trainerbattle_single TRAINER_YUKI, InkaSeawall_Text_YukiIntro, InkaSeawall_Text_YukiDefeat
# 190 "data/maps/InkaSeawall/scripts.pory"
	msgbox InkaSeawall_Text_YukiPost, MSGBOX_AUTOCLOSE
	return


InkaSeawall_EventScript_Faiz::
# 206 "data/maps/InkaSeawall/scripts.pory"
	trainerbattle_single TRAINER_FAIZ, InkaSeawall_Text_FaizIntro, InkaSeawall_Text_FaizDefeat
# 207 "data/maps/InkaSeawall/scripts.pory"
	msgbox InkaSeawall_Text_FaizPost, MSGBOX_AUTOCLOSE
	return


InkaSeawall_EventScript_Npc1::
# 224 "data/maps/InkaSeawall/scripts.pory"
	msgbox InkaSeawall_EventScript_Npc1_Text_0, MSGBOX_NPC
	return


InkaSeawall_EventScript_Npc2::
# 228 "data/maps/InkaSeawall/scripts.pory"
	msgbox InkaSeawall_EventScript_Npc2_Text_0, MSGBOX_NPC
	return


InkaSeawall_EventScript_Sign1_Text_0:
# 5 "data/maps/InkaSeawall/scripts.pory"
	.string "INKA SEAWALL\n"
	.string "Reclaimed from the sea for the people\l"
	.string "of Inka.$"

InkaSeawall_EventScript_Sign2_Text_0:
# 9 "data/maps/InkaSeawall/scripts.pory"
	.string "LOVERS' KNOT\n"
	.string "Couples who walk the seawall at sunset\l"
	.string "are said to stay together forever.$"

InkaSeawall_EventScript_Npc1_Text_0:
# 224 "data/maps/InkaSeawall/scripts.pory"
	.string "This seawall used to be open sea. My\n"
	.string "father fished from a boat right where\l"
	.string "I'm standing.\p"
	.string "Now I fish from the wall. Same fish,\n"
	.string "though.$"

InkaSeawall_EventScript_Npc2_Text_0:
# 228 "data/maps/InkaSeawall/scripts.pory"
	.string "Couples tie a ribbon on the Lovers' Knot\n"
	.string "and make a wish.\p"
	.string "I tied three. Just to be safe.$"

InkaSeawall_Text_AmirIntro::
# 16 "data/maps/InkaSeawall/scripts.pory"
	.string "AMIR: We come here every Friday. Nur\n"
	.string "says the sunset's better than any film.$"

InkaSeawall_Text_AmirDefeat::
# 20 "data/maps/InkaSeawall/scripts.pory"
	.string "AMIR: Even losing is fine, as long as\n"
	.string "it's together.$"

InkaSeawall_Text_AmirPost::
# 24 "data/maps/InkaSeawall/scripts.pory"
	.string "AMIR: Our Pokémon are a couple too.\n"
	.string "They copy everything we do.$"

InkaSeawall_Text_AmirNotEnough::
# 28 "data/maps/InkaSeawall/scripts.pory"
	.string "AMIR: A double battle needs two\n"
	.string "Pokémon. Come back with a partner for\l"
	.string "yours!$"

InkaSeawall_Text_NurIntro::
# 37 "data/maps/InkaSeawall/scripts.pory"
	.string "NUR: You'll battle us both? That's very\n"
	.string "brave. Or very lonely.$"

InkaSeawall_Text_NurDefeat::
# 41 "data/maps/InkaSeawall/scripts.pory"
	.string "NUR: Amir, you were supposed to protect\n"
	.string "me!$"

InkaSeawall_Text_NurPost::
# 45 "data/maps/InkaSeawall/scripts.pory"
	.string "NUR: Plusle and Minun cheer each other\n"
	.string "on. Like us. Mostly.$"

InkaSeawall_Text_NurNotEnough::
# 49 "data/maps/InkaSeawall/scripts.pory"
	.string "NUR: We battle as a pair. You need two\n"
	.string "Pokémon to take us on.$"

InkaSeawall_Text_JunIntro::
# 58 "data/maps/InkaSeawall/scripts.pory"
	.string "JUN: Shh, we're watching the ships come\n"
	.string "in. Unless… you want a battle?$"

InkaSeawall_Text_JunDefeat::
# 62 "data/maps/InkaSeawall/scripts.pory"
	.string "JUN: We were distracted. By the view.\n"
	.string "Obviously.$"

InkaSeawall_Text_JunPost::
# 66 "data/maps/InkaSeawall/scripts.pory"
	.string "JUN: At night Volbeat and Illumise light\n"
	.string "up the whole seawall.$"

InkaSeawall_Text_JunNotEnough::
# 70 "data/maps/InkaSeawall/scripts.pory"
	.string "JUN: Two of us, two of yours. Bring\n"
	.string "another Pokémon.$"

InkaSeawall_Text_HuiIntro::
# 79 "data/maps/InkaSeawall/scripts.pory"
	.string "HUI: This is our anniversary! Make it a\n"
	.string "battle to remember!$"

InkaSeawall_Text_HuiDefeat::
# 83 "data/maps/InkaSeawall/scripts.pory"
	.string "HUI: Well, we'll definitely remember it.$"

InkaSeawall_Text_HuiPost::
# 87 "data/maps/InkaSeawall/scripts.pory"
	.string "HUI: Five years ago Jun asked me out\n"
	.string "right on this spot. He was so nervous.$"

InkaSeawall_Text_HuiNotEnough::
# 91 "data/maps/InkaSeawall/scripts.pory"
	.string "HUI: Come back with two Pokémon and\n"
	.string "we'll battle!$"

InkaSeawall_Text_ChloeIntro::
# 100 "data/maps/InkaSeawall/scripts.pory"
	.string "Golden hour on the seawall! Quick,\n"
	.string "battle me while the lighting's good!$"

InkaSeawall_Text_ChloeDefeat::
# 104 "data/maps/InkaSeawall/scripts.pory"
	.string "Ugh, my followers saw that live.$"

InkaSeawall_Text_ChloePost::
# 108 "data/maps/InkaSeawall/scripts.pory"
	.string "Hashtag Inka Seawall, hashtag sunset,\n"
	.string "hashtag couple goals… I'm here alone,\l"
	.string "but the hashtags don't know that.$"

InkaSeawall_Text_ImranIntro::
# 117 "data/maps/InkaSeawall/scripts.pory"
	.string "Morning run, evening run, I'm always on\n"
	.string "the seawall! Keep up!$"

InkaSeawall_Text_ImranDefeat::
# 121 "data/maps/InkaSeawall/scripts.pory"
	.string "Out of breath… and out of Pokémon.$"

InkaSeawall_Text_ImranPost::
# 125 "data/maps/InkaSeawall/scripts.pory"
	.string "Five laps from the beach to Inka every\n"
	.string "day. The couples keep getting in my way.$"

InkaSeawall_Text_SitiIntro::
# 134 "data/maps/InkaSeawall/scripts.pory"
	.string "My date's late. Again. You'll have to do.$"

InkaSeawall_Text_SitiDefeat::
# 138 "data/maps/InkaSeawall/scripts.pory"
	.string "Hmph. At least you showed up.$"

InkaSeawall_Text_SitiPost::
# 142 "data/maps/InkaSeawall/scripts.pory"
	.string "If he isn't here by sunset, I'm giving\n"
	.string "these flowers to my Bellossom.$"

InkaSeawall_Text_UncleHockIntro::
# 151 "data/maps/InkaSeawall/scripts.pory"
	.string "UNCLE HOCK: When we were young, this\n"
	.string "was all water. We courted on a sampan!$"

InkaSeawall_Text_UncleHockDefeat::
# 155 "data/maps/InkaSeawall/scripts.pory"
	.string "UNCLE HOCK: Fifty years married and\n"
	.string "still learning.$"

InkaSeawall_Text_UncleHockPost::
# 159 "data/maps/InkaSeawall/scripts.pory"
	.string "UNCLE HOCK: They filled in the sea so\n"
	.string "people had room to walk. Best thing\l"
	.string "Inka ever did.$"

InkaSeawall_Text_UncleHockNotEnough::
# 163 "data/maps/InkaSeawall/scripts.pory"
	.string "UNCLE HOCK: We battle side by side.\n"
	.string "You'll need two Pokémon.$"

InkaSeawall_Text_AuntieLanIntro::
# 172 "data/maps/InkaSeawall/scripts.pory"
	.string "AUNTIE LAN: Don't go easy on us, dear.\n"
	.string "We certainly won't on you.$"

InkaSeawall_Text_AuntieLanDefeat::
# 176 "data/maps/InkaSeawall/scripts.pory"
	.string "AUNTIE LAN: Oh, well done! Your mother\n"
	.string "must be proud.$"

InkaSeawall_Text_AuntieLanPost::
# 180 "data/maps/InkaSeawall/scripts.pory"
	.string "AUNTIE LAN: Every evening we walk to\n"
	.string "the sculpture and back. Every single\l"
	.string "evening.$"

InkaSeawall_Text_AuntieLanNotEnough::
# 184 "data/maps/InkaSeawall/scripts.pory"
	.string "AUNTIE LAN: Come back with two\n"
	.string "Pokémon, dear.$"

InkaSeawall_Text_YukiIntro::
# 193 "data/maps/InkaSeawall/scripts.pory"
	.string "The guidebook says this is the most\n"
	.string "romantic spot in Tosa! …I came with my\l"
	.string "Pokémon.$"

InkaSeawall_Text_YukiDefeat::
# 197 "data/maps/InkaSeawall/scripts.pory"
	.string "My Pokémon and I had a lovely time\n"
	.string "anyway.$"

InkaSeawall_Text_YukiPost::
# 201 "data/maps/InkaSeawall/scripts.pory"
	.string "I came all the way from Johto for this\n"
	.string "sunset. Totally worth it.$"

InkaSeawall_Text_FaizIntro::
# 210 "data/maps/InkaSeawall/scripts.pory"
	.string "Flower delivery for… a couple on the\n"
	.string "seawall. That narrows it down to\l"
	.string "everyone!$"

InkaSeawall_Text_FaizDefeat::
# 214 "data/maps/InkaSeawall/scripts.pory"
	.string "Okay, okay, you win. Don't tell my\n"
	.string "customer I stopped.$"

InkaSeawall_Text_FaizPost::
# 218 "data/maps/InkaSeawall/scripts.pory"
	.string "Valentine's week, I deliver here forty\n"
	.string "times a day.$"
