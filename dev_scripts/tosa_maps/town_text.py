"""
Content for dev_scripts/tosa_maps/towns.py: per town, its size and theme, which buildings it gets,
the town sign, and the NPCs outdoors and in each house. Lore comes from TODO.md and the region map
tagger notes; everything else is light filler meant to be rewritten.

buildings: kit names placed in order (centre, mart, hawker, house_p / house_r / house_w, or a special
           with a sign: ("coldstore", "sign text"), ("warehouse", ...), ("depot", ...), ("stall", None)).
npcs:      (graphics, where, movement, text). where = plaza / station / centre / mart / house:N / special:N /
           mouth:KEY / coast / exit / any. movement = wander / look / up / down / left / right.
houses:    one list per house_* building, in order: [(graphics, text), ...] (interior NPCs).
"""
from collections import OrderedDict as O

G = lambda s: "OBJ_EVENT_GFX_" + s

TOWNS = O()

TOWNS["MoongroveCity"] = dict(
    size=(42, 38), theme="marsh", road="cobble", trees=0.16,
    sign="Moongrove City\n“Roots in the mud, eyes on the tide.”",
    buildings=["centre", "mart", "gym", "house_r", "house_p", "house_w", "house_p"],
    npcs=[
        (G("FISHERMAN"), "exit", "look", "Tork, our Gym Leader, was out on the mudflats before dawn again.\\pHe swears the big catfish only bite when the tide turns."),
        (G("OLD_WOMAN"), "plaza", "wander", "The mangroves keep the sea from swallowing the town. Their roots hold this whole place together."),
        (G("BOY_1"), "house:2", "wander", "Have you seen the lights at the Abandoned House? My brother says it's a ghost.\\pI say it's Mum looking for her keys."),
        (G("WOMAN_3"), "exit", "wander", "Moongrove Marsh is a fisher's dream. Bring a rod, some patience… and bug spray."),
        (G("POKEFAN_M"), "station", "look", "The train's made Moongrove easy to reach. Shame half the visitors only come to gawk at the haunted house."),
    ],
    houses=[
        [(G("OLD_MAN"), "When I was young there was no train. Just little boats poling through the mangrove channels."),
         (G("LITTLE_GIRL"), "Grandpa says the marsh ghosts only come out for people who drop litter!")],
        [(G("FISHERMAN"), "Catfish Pokémon can sense earthquakes before they happen. Tork says that's why he trains Ground types.")],
        [(G("WOMAN_2"), "Professor Palm's assistant came through counting Pokémon in the marsh. Fewer Lotad than last year, apparently.")],
        [(G("MAN_2"), "I hung my washing out and a Wingull stole a sock. Wingull aren't even from around here!")],
    ],
)

TOWNS["TimahCity"] = dict(
    size=(42, 38), theme="city", road="cobble", trees=0.30,
    sign="Timah City\n“The green heart of the Tosa Reserve.”",
    buildings=["centre", "mart", "gym", "house_p", "house_r", "house_w", "house_p"],
    npcs=[
        (G("ORCHIDIST"), "plaza", "look", "Hana grows orchids in her garden that bloom nowhere else in the world. She guards them better than her Gym Badge!"),
        (G("POKEMON_RANGER_F"), "exit", "look", "Timah sits right in the middle of the Tosa Reserve. Stick to the paths. The Rangers are watching for poachers."),
        (G("PICNICKER"), "any", "wander", "It rains here every afternoon, like clockwork. Bring an umbrella. Or a Lotad."),
        (G("OLD_MAN"), "centre", "wander", "This city grew up around the old rubber trees on the hill. Now look at it: trains, Pokémon Centres…"),
        (G("YOUNGSTER"), "any", "wander", "There are Pokémon up in the canopy that never come down to the ground. I've been waiting all week!"),
    ],
    houses=[
        [(G("WOMAN_1"), "My Oddish wandered into Hana's garden once. She sent it home with a ribbon and a very stern note.")],
        [(G("SCIENTIST_1"), "Invasive species are crowding out the native Pokémon.\\pSomebody is bringing them in on purpose. I'm sure of it.")],
        [(G("LITTLE_BOY"), "When I grow up I'm going to be a Pokémon Ranger and live in a tree house!"),
         (G("WOMAN_4"), "The Rangers say the Reserve is changing faster than they can keep up with. It's worrying.")],
        [(G("GENTLEMAN"), "Timah is where Tosa keeps its heart. Treat the forest kindly and it will be kind to you.")],
    ],
)

TOWNS["FaberTown"] = dict(
    size=(36, 32), theme="rocky", road="dirt", trees=0.0,
    mouths={"batok_w": "W", "batok_e": "E"},
    sign="Faber Town\n“A town carved from the cliffs.”",
    buildings=["centre", "mart", "gym", "house_r", "house_p", "house_r"],
    npcs=[
        (G("BLACK_BELT"), "plaza", "look", "Meru heads up into the mountains alone to spar with wild Rock types. Bare-handed! That's our town leader."),
        (G("HIKER"), "mouth:batok_w", "look", "I took the climb up Mt. Batok instead of the cable car. My knees will never forgive me."),
        (G("OLD_WOMAN"), "house:1", "wander", "Faber's houses are built right into the cliff. Mind the edge after dark."),
        (G("PORT_WORKER"), "station", "look", "The cable car's been out of service for months. Good thing the railway came through."),
        (G("CAMPER"), "mouth:batok_e", "wander", "From up here you can see all the way to Kantu Falls. Folk bathe in the mineral water there once or twice a year."),
    ],
    houses=[
        [(G("MAN_4"), "Meru trained my Machop when it was tiny. Now it carries my shopping up the cliff.")],
        [(G("EXPERT_F"), "Rock Pokémon tumble down from the peaks after a storm. We dig them out and send them home.")],
        [(G("BOY_2"), "I tried to follow Meru up the mountain once. I made it about ten steps.")],
    ],
)

TOWNS["ChanguCity"] = dict(
    size=(44, 38), theme="city", road="cobble", trees=0.08,
    sign="Changu City\n“Gateway to the Tosa region.”",
    buildings=["centre", "mart", "gym", ("warehouse", "CHANGU BUSINESS PARK\nOffices to let."), "house_w", "house_p", "house_r", "house_p"],
    npcs=[
        (G("MAN_3"), "plaza", "wander", "Synergise! Innovate! Profit!\\pSorry, force of habit. I fly in every Monday for meetings."),
        (G("TOURIST_F"), "exit", "look", "The airport's just up Route 306. They call Changu the gateway to Tosa. So far it's mostly office blocks."),
        (G("WOMAN_4"), "special:3", "wander", "Our Gym Leader Larry was sent over from Paldea by their Champion. He seems… tired. Very, very tired."),
        (G("LASS"), "mart", "wander", "I saw Larry at the hawker stall eating the same set lunch as yesterday. And the day before."),
        (G("MAN_4"), "station", "look", "Customs has tightened up. Too many Pokémon have been coming in without import permits lately."),
    ],
    houses=[
        [(G("MAN_2"), "I walk to the airport every day on Route 306. It's a short, pleasant commute… when it isn't raining.")],
        [(G("WOMAN_5"), "My company sent me here from Kalos. The food's spicy, the weather's hot, and I'd never go back.")],
        [(G("RICH_BOY"), "Daddy says Tosa is an “emerging market”. I don't know what that means, but it sounds expensive.")],
        [(G("OLD_MAN"), "Changu was a fishing village before the airport. Now the only thing we catch is flights.")],
    ],
)

TOWNS["ChanguAirport"] = dict(
    size=(38, 30), theme="city", road="cobble", trees=0.05,
    sign="Changu Airport\n“Tosa's door to the world.”",
    buildings=[("coldstore", "CHANGU AIRPORT TERMINAL\nClosed for refurbishment. Please use the train."), ("depot", "AIR CARGO\nAuthorised personnel only."), "house_w"],
    npcs=[
        (G("TOURIST_M"), "special:0", "wander", "Flights from Hoenn, Johto and Paldea all land here. Customs checks every single Poké Ball."),
        (G("MAN_4"), "special:0", "look", "All imported Pokémon need a PokéPermit. No permit, no entry. We've caught a lot of smugglers lately."),
        (G("BEAUTY"), "plaza", "wander", "I just flew in from Paldea! Is it always this humid?"),
        (G("PORT_WORKER"), "special:1", "look", "The terminal's being refurbished, so everyone's taking the train into the city."),
    ],
    houses=[
        [(G("PORT_WORKER"), "I handle air cargo. You wouldn't believe what people try to fly in. A Sharpedo in a suitcase, once!")],
    ],
)

TOWNS["InkaCity"] = dict(
    size=(46, 38), theme="city", road="cobble", trees=0.06,
    sign="Inka City\n“Tosa's logistics hub.”",
    buildings=["centre", "mart", "gym", ("coldstore", "INKA COLD DISTRIBUTION CENTRE\nManaged by Frea. Staff only."),
               ("warehouse", "MARLIN CO. SHIPPING\nAuthorised personnel only."), "house_p", "house_w", "house_r", "house_p"],
    npcs=[
        (G("PORT_WORKER"), "special:3", "look", "Every crate of imported food in Tosa passes through Inka. Frea makes sure it's all kept cold and on time."),
        (G("PORT_WORKER"), "special:4", "wander", "Marlin Co.? Shipping company. Keeps odd hours.\\pTheir trucks come and go at night with the lights off."),
        (G("MAN_1"), "plaza", "wander", "Frea runs the cold store and the Gym. I've never once seen her without a clipboard."),
        (G("WOMAN_4"), "centre", "wander", "The warehouses never sleep. Forklifts at three in the morning, Ice types cooling the containers… It's noisy!"),
        (G("SCHOOL_KID_M"), "house:5", "wander", "I tried to peek inside Marlin Co. A man in a blue bandana told me to scram!"),
    ],
    houses=[
        [(G("WOMAN_4"), "My Snorunt works night shifts at the cold store. It gets paid in ice cubes.")],
        [(G("OLD_WOMAN"), "Inka used to be all farmland. Now it's lorries as far as the eye can see.")],
        [(G("MAN_3"), "Marlin Co. offered me a job. Good pay, no questions asked.\\pThat's exactly what worried me.")],
        [(G("TWIN"), "Frea let me hold her Spheal! It was cold!")],
    ],
)

TOWNS["BuraCity"] = dict(
    size=(40, 34), theme="city", road="cobble", trees=0.12,
    sign="Bura City\n“Stop a while.”",
    buildings=["centre", "mart", "gym", "hawker", ("stall", None), "house_r", "house_p", "house_p"],
    npcs=[
        (G("TOURIST_M"), "station", "look", "Bura? I'm only here to change trains. Though the hawker centre's worth getting off for."),
        (G("OLD_WOMAN"), "plaza", "wander", "Maria's gone to Juran for the weekend again. Her cats are minding the Gym till Monday."),
        (G("LITTLE_GIRL"), "house:5", "wander", "Maria dressed her Skitty up as a Wingull yesterday. It did not look happy."),
        (G("HAWKER_M"), "special:4", "look", "Chicken rice! Laksa! Char kway teow! The best food between Changu and Juran!"),
        (G("SKITTY"), "plaza", "wander", "Skitty: Nyaa!\\p(It's wearing a tiny sailor hat.)"),
    ],
    houses=[
        [(G("WOMAN_2"), "Nobody stays in Bura long. That's what I like about it. It's quiet.")],
        [(G("MAN_4"), "My wife won't let me go to Juran with Maria any more. Something about “the rent money”.")],
        [(G("OLD_MAN"), "Thirty years I've cooked at that hawker centre. Trains come, trains go. People always need noodles.")],
    ],
)

TOWNS["JuranCity"] = dict(
    size=(44, 38), theme="city", road="cobble", trees=0.06,
    sign="Juran City\n“Shop, stay, play.”",
    buildings=["centre", "mart", ("warehouse", "GRAND JURAN HOTEL & CASINO\nOpening soon."), ("stall", None), "house_w", "house_p", "house_r", "house_p"],
    npcs=[
        (G("BEAUTY"), "plaza", "wander", "Shops, hotels, casinos… Juran has it all. Even its own train line to Pokétopia!"),
        (G("GENTLEMAN"), "special:2", "look", "I won big at the casino last night. Strange, though. The same fellows seem to win every night."),
        (G("WOMAN_1"), "special:3", "look", "Some men in suits came by my stall asking for “protection money”. The big chains never get visits like that."),
        (G("TOURIST_F"), "station", "wander", "I'm taking the train to Pokétopia tomorrow. The night safari is supposed to be amazing!"),
        (G("MAN_4"), "centre", "look", "Keep your wallet close in Juran. Not everyone at the tables plays fair."),
    ],
    houses=[
        [(G("MAN_5"), "I used to own a little bakery. Then the rent went up… and the “visits” started.")],
        [(G("WOMAN_3"), "The hotels look lovely from the outside. I clean the rooms, so I know better.")],
        [(G("LITTLE_BOY"), "Mum says I'm not allowed in the casino until I'm forty.")],
        [(G("OLD_WOMAN"), "Maria from Bura comes here every weekend. She always brings a cat in a different hat.")],
    ],
)

TOWNS["SenokoCity"] = dict(
    size=(42, 38), theme="city", road="cobble", trees=0.10,
    sign="Senoko City\n“Powering Tosa, one turbine at a time.”",
    buildings=["centre", "mart", "gym", ("depot", "TOSA NATIONAL GRID\nSenoko control office."), "house_p", "house_r", "house_w"],
    npcs=[
        (G("PORT_WORKER"), "special:3", "look", "Mo runs the national power grid from Senoko. If the lights go out anywhere in Tosa, he's the one who gets the call."),
        (G("SCIENTIST_2"), "plaza", "wander", "The wind farms around town spin day and night. Electric Pokémon love napping by the turbines."),
        (G("WOMAN_5"), "centre", "wander", "When the wind drops, Mo sends his Electric Pokémon to the Power Plant to help out. True story!"),
        (G("BOY_3"), "exit", "wander", "I counted forty turbines on the hill! Then I lost count."),
        (G("OLD_MAN"), "house:3", "wander", "Senoko was a sleepy place before the turbines. Now it powers the whole region."),
    ],
    houses=[
        [(G("WOMAN_4"), "I climb turbines for a living. Magnemite keep sticking to my hard hat.")],
        [(G("MAN_1"), "My electricity bill is the lowest in Tosa. Perks of living next to the Power Plant.")],
        [(G("LITTLE_GIRL"), "Mo's Pikachu came to my birthday party and lit all the candles! Then it blew a fuse.")],
    ],
)

TOWNS["PokemonLeague"] = dict(
    size=(36, 34), theme="city", road="cobble", trees=0.10,
    mouths={"trail": "W"},
    sign="Pokémon League\n“Only the strongest Trainers stand here.”",
    buildings=["centre", "mart", "house_w", "house_p"],
    npcs=[
        (G("MAN_3"), "mouth:trail", "look", "You made it up Challenger's Trail? Then you're ready to face the Elite Four."),
        (G("WOMAN_5"), "plaza", "wander", "Siya, Fue, Stern and Mawray. Four of the strongest Trainers in Tosa, one after the other."),
        (G("OLD_MAN"), "house:2", "wander", "Captain Stern sailed the seas for thirty years before joining the Elite Four. His Steel Pokémon are as tough as an anchor."),
        (G("EXPERT_M"), "centre", "look", "Stock up at the Mart and rest at the Pokémon Centre. Once you're inside, there's no turning back."),
    ],
    houses=[
        [(G("WOMAN_4"), "My son challenged the League three times. He's a chef now. Very happy.")],
        [(G("GENTLEMAN"), "I've watched Challengers come and go for decades. The ones who care for their Pokémon always go furthest.")],
    ],
)

TOWNS["PoketopiaGate"] = dict(
    size=(32, 30), theme="coast", road="cobble", trees=0.12, coast="S",
    sign="Pokétopia Gate\n“All aboard for paradise!”",
    buildings=["house_r", "house_p", ("stall", None)],
    npcs=[
        (G("SAILOR"), "station", "look", "The train runs straight across to Pokétopia. Resort island, marina, night safari, you name it."),
        (G("TOURIST_M"), "plaza", "wander", "I've got my swimming trunks on under my suit. Don't tell my boss."),
        (G("FISHERMAN"), "coast", "look", "Tentacool wash up on this beach after storms. Tread carefully."),
    ],
    houses=[
        [(G("WOMAN_1"), "Ferries used to sail to Pokétopia from here. Now everyone takes the train.")],
        [(G("OLD_MAN"), "Marina, the Gym Leader in Corral City, once swam here from Pokétopia. In a storm!")],
    ],
)

TOWNS["CorralCity"] = dict(
    size=(44, 42), theme="coast", road="cobble", trees=0.10, coast="S",
    sign="Corral City\n“Sun, sea and Pokétopia.”",
    buildings=["centre", "mart", "gym", ("stall", None), "house_r", "house_p", "house_w"],
    npcs=[
        (G("BEAUTY"), "plaza", "wander", "Marina's Gym is right by the water. They say she's mastered the seas themselves."),
        (G("TUBER_M"), "coast", "wander", "I'm going to swim to the little islands! Mum says I need a boat first. And to learn to swim."),
        (G("SAILOR"), "coast", "look", "Boats leave the marina for the small islands around Pokétopia. Once they're running again, anyway."),
        (G("TOURIST_F"), "station", "wander", "The night safari opens after dark. You can see nocturnal Pokémon up close!"),
        (G("FAT_MAN"), "special:3", "look", "I came to Pokétopia for a quiet holiday. Then I found the ice cream stall."),
    ],
    houses=[
        [(G("WOMAN_2"), "We rent rooms to holidaymakers in the summer. Pokémon are welcome. Sand is not.")],
        [(G("SAILOR"), "I crewed for Marina once. Never met anyone who reads the waves like she does.")],
        [(G("LITTLE_BOY"), "I found a Shellder on the beach! Then it found my finger.")],
    ],
)

TOWNS["WavebreakTown"] = dict(
    size=(32, 30), theme="coast", road="dirt", trees=0.18, coast="W",
    sign="Wavebreak Town\n“Tosa's first harbour.”",
    buildings=["centre", "mart", "house_r", "house_p", "house_r"],
    npcs=[
        (G("OLD_MAN"), "plaza", "wander", "Wavebreak was Tosa's first port, you know. Then Tosa Port opened and the ships stopped coming."),
        (G("FISHERMAN"), "coast", "look", "Nobody's left to scare the Pokémon off, so the fishing's never been better."),
        (G("OLD_WOMAN"), "house:2", "wander", "My husband worked the docks here for forty years. Now the only thing that washes in is seaweed."),
        (G("SAILOR"), "coast", "look", "Smugglers love a quiet harbour. Just saying."),
    ],
    houses=[
        [(G("OLD_MAN"), "This house belonged to the old harbourmaster. I kept his bell.")],
        [(G("WOMAN_3"), "The young ones all left for Tosa Port and the cities. I don't blame them.")],
        [(G("FISHERMAN"), "I've seen boats come in at night with no lights. Not fishing boats, either.")],
    ],
)

TOWNS["PinestampTown"] = dict(
    size=(32, 28), theme="town", road="dirt", trees=0.35,
    sign="Pinestamp Town\n“A quiet town among the pines.”",
    buildings=["centre", "mart", "house_p", "house_r", "house_p"],
    npcs=[
        (G("WOMAN_1"), "plaza", "wander", "The pine trees keep Pinestamp cool, even in the dry season."),
        (G("CAMPER"), "any", "wander", "Bug Pokémon love pine sap. Check the trees around town for a surprise!"),
        (G("HIKER"), "exit", "look", "Most Trainers pass straight through on their way somewhere else. Stop and smell the pines, I say."),
    ],
    houses=[
        [(G("LITTLE_BOY"), "I collect stamps! Well… stamp. I've got one.")],
        [(G("OLD_WOMAN"), "My family has lived in Pinestamp for five generations. It's never changed, and that suits me fine.")],
        [(G("MAN_2"), "I carve little Pokémon out of pine wood. The Zigzagoon ones sell best.")],
    ],
)

TOWNS["ChallengerGate"] = dict(
    size=(34, 34), theme="city", road="cobble", trees=0.12,
    mouths={"trail": "E"},
    sign="Challenger Gate\n“The last stop before the Pokémon League.”",
    buildings=["centre", "mart", "house_w", "house_p"],
    npcs=[
        (G("WOMAN_5"), "mouth:trail", "look", "Only Trainers with every Badge in Tosa are allowed onto Challenger's Trail."),
        (G("EXPERT_M"), "plaza", "wander", "The Trail climbs right up the mountain to the Pokémon League. Plenty turn back."),
        (G("BLACK_BELT"), "centre", "wander", "Every Badge in Tosa, and I still got lost in that cave. Bring Repels."),
        (G("YOUNGSTER"), "any", "wander", "One day I'll walk the Trail. Today I'm just here for the café."),
    ],
    houses=[
        [(G("MAN_3"), "I'm resting up before my third attempt at the Trail. Third time lucky!")],
        [(G("OLD_WOMAN"), "I sell sandwiches to Trainers heading up the mountain. Nobody ever comes back for a second one.")],
    ],
)

# landmarks built by the same composer (no Centre / Mart)
TOWNS["IndustrialPark"] = dict(
    size=(34, 28), theme="city", road="cobble", trees=0.04, landmark=True,
    sign="Industrial Park",
    buildings=[("warehouse", "UNIT 1\nDeliveries round the back."), ("depot", "UNIT 2\nNo entry."), ("warehouse", "UNIT 3\nTo let."), ("depot", "UNIT 4\nNo entry.")],
    npcs=[
        (G("PORT_WORKER"), "special:0", "look", "Hard hats on past this point. Pokémon included."),
        (G("WOMAN_4"), "special:1", "wander", "Half these units belong to companies nobody's ever heard of. Funny that."),
        (G("PORT_WORKER"), "plaza", "look", "Careful round here. The forklifts don't stop for anyone."),
    ],
    houses=[],
)

TOWNS["PowerPlant"] = dict(
    size=(28, 22), theme="town", road="dirt", trees=0.12, landmark=True,
    sign="Power Plant\n“Senoko City Wind Power Plant.”",
    buildings=[("depot", "SENOKO WIND POWER PLANT\nControl building. Staff only.")],
    npcs=[
        (G("PORT_WORKER"), "special:0", "look", "The turbines feed straight into Mo's grid. When the wind drops, his Electric Pokémon pick up the slack."),
        (G("SCIENTIST_1"), "plaza", "wander", "Voltorb keep rolling in from the hills. We think the hum of the generators attracts them."),
    ],
    houses=[],
)

TOWNS["AbandonedHouse"] = dict(
    size=(24, 20), theme="town", road="dirt", trees=0.45, landmark=True,
    sign="Abandoned House\n“…”",
    buildings=["house_w"], house_layout="LAYOUT_HOUSE2", hub_y=12, haunted=True,
    npcs=[
        (G("HEX_MANIAC"), "house:0", "look", "People in Moongrove see lights in that house at night.\\pNobody has lived there since the early days of Tosa…"),
    ],
    houses=[
        [(G("HEX_MANIAC"), "…Hello? Is someone there?\\p…Oh. It's only you. I thought I heard footsteps upstairs. There is no upstairs."),
         (G("DUSCLOPS"), "…\\p(It stares at you without blinking.)")],
    ],
)


# Tiksi: the approved town layouts stay; their door-only houses get interiors and NPCs.
TIKSI = O()
TIKSI["FurongVillage"] = dict(
    npcs=[
        (G("FISHERMAN"), (14, 9), "look", "A boat from Tosa? We don't get many of those. Not legal ones, anyhow."),
        (G("OLD_WOMAN"), (8, 13), "wander", "Tiksi is a hard land. The sea feeds us and the mountain watches over us."),
        (G("LITTLE_GIRL"), (12, 15), "wander", "Are you from Tosa? Grandpa says Tosa people are soft. You look all right to me."),
    ],
    houses=[
        [(G("FISHERMAN"), "That ship you came in on has been running between here and Tosa for months. Always at night.")],
        [(G("OLD_MAN"), "Tosa and Tiksi haven't got along for a hundred years. Don't take it personally.")],
    ],
)
TIKSI["DrakeBaseCamp"] = dict(
    npcs=[
        (G("HIKER"), (10, 12), "look", "The peak of Mt. Drake is said to be home to an ancient dragon Pokémon. Nobody's climbed high enough to check."),
        (G("EXPERT_M"), (19, 14), "wander", "The old stories say this mountain was carved by beams of light from the maw of an ancient Pokémon."),
        (G("CAMPER"), (14, 19), "wander", "Some strangers in blue came through last week, heading up the mountain. Didn't say hello."),
    ],
    houses=[
        [(G("HIKER"), "Every climber rests here before the ascent. Take a breather while you can.")],
        [(G("WOMAN_4"), "The shrine guardians have been on edge. They say something woke up inside the mountain.")],
    ],
)
TIKSI["UbeCity"] = dict(
    npcs=[
        (G("MAN_3"), (19, 8), "look", "Silph Co.'s Tiksi office! Well… it's more of a cupboard. Sales have been slow."),
        (G("WOMAN_5"), (8, 11), "wander", "Ube's the only city in Tiksi. Which is why it's the only place with a decent cup of tea."),
        (G("OLD_MAN"), (16, 17), "wander", "The guardians keep watch at the old shrines. If they're standing at the doors, something's very wrong."),
        (G("BOY_1"), (13, 14), "wander", "My dad says Tosa people think we're backward. We've got a fountain! Have they got a fountain?"),
    ],
    houses=[
        [(G("WOMAN_2"), "Silph Co. keeps trying to sell us Poké Balls. We've used the same ones for thirty years!")],
        [(G("MAN_4"), "People in Ube are tough. You have to be, out here.")],
        [(G("OLD_WOMAN"), "My grandmother told me about the giants sealed in the shrines. I never thought I'd live to see them stir.")],
    ],
)
TIKSI["TanglynTown"] = dict(
    npcs=[
        (G("EXPERT_F"), (14, 7), "look", "The murals in the hall show giants sealed away by Tiksi's ancestors. Five of them! Not three."),
        (G("OLD_WOMAN"), (10, 13), "wander", "The murals are older than any record. Some say people from Sevii painted them."),
        (G("FISHERMAN"), (22, 16), "look", "Frigo Cave's off the north shore. Locals say it's colder inside than it has any right to be."),
    ],
    houses=[
        [(G("PICNICKER"), "The Mural Hall's closed for restoration. I came all this way!")],
        [(G("MAN_2"), "Tanglyn's quiet. Just the sea, the murals and the wind.")],
    ],
)


# Gyms (TODO.md "GYM TYPES"). Placeholder interiors: the vanilla Dewford Gym room with the leader and a
# guide. Leaders reuse the vanilla gym-leader trainer slots (renamed, old names aliased); teams are
# placeholders with legal levels in TODO.md's listed order, default movesets, no items.
# slot, constant, name, pic, gender, overworld graphics, badge flag, party [(species, level)], lines
GYMS = O()
GYMS["TimahCity"] = dict(slot="TRAINER_ROXANNE_1", const="TRAINER_LEADER_HANA", name="Hana", pic="Aroma Lady", gender="Female",
    gfx=G("ORCHIDIST"), badge="FLAG_BADGE01_GET", type="Grass",
    party=[("Seedot", 12), ("Oddish", 12), ("Roselia", 14)],
    intro="Welcome to my garden. My orchids bloom nowhere else in the world, and neither does my battling style!",
    defeat="Oh my… you pruned my team right back.", post="Treat every living thing as gently as an orchid and it will grow strong for you.")
GYMS["CorralCity"] = dict(slot="TRAINER_WINONA_1", const="TRAINER_LEADER_MARINA", name="Marina", pic="Swimmer F", gender="Female",
    gfx=G("BEAUTY"), badge="FLAG_BADGE02_GET", type="Water",
    party=[("Marill", 18), ("Wingull", 18), ("Lombre", 20)],
    intro="I've swum every current around Pokétopia. Let's see if you can keep your head above water!",
    defeat="You read the tide better than I did today.", post="The sea always gives back what you put into it.")
GYMS["ChanguCity"] = dict(slot="TRAINER_NORMAN_1", const="TRAINER_LEADER_LARRY", name="Larry", pic="Leader Norman", gender="Male",
    gfx=G("MAN_3"), badge="FLAG_BADGE03_GET", type="Normal",
    party=[("Linoone", 23), ("Vigoroth", 23), ("Swellow", 25)],
    intro="I'm Larry. Paldea's Champion sent me here to build bridges with the Tosa League. Normal battle, normal Pokémon. Let's get this over with.",
    defeat="…Well. That's that, then.", post="I'd like to go home and have a nap now. That's normal, isn't it?")
GYMS["FaberTown"] = dict(slot="TRAINER_BRAWLY_1", const="TRAINER_LEADER_MERU", name="Meru", pic="Leader Brawly", gender="Male",
    gfx=G("BLACK_BELT"), badge="FLAG_BADGE04_GET", type="Fighting",
    party=[("Machoke", 28), ("Meditite", 28), ("Hariyama", 30)],
    intro="I train alone in the mountains against wild Rock Pokémon. You climbed all the way up here? Then show me your strength!",
    defeat="Hah! You hit harder than a rockslide!", post="Strength comes from the climb, not the summit.")
GYMS["MoongroveCity"] = dict(slot="TRAINER_TATE_AND_LIZA_1", const="TRAINER_LEADER_TORK", name="Tork", pic="Fisherman", gender="Male",
    gfx=G("FISHERMAN"), badge="FLAG_BADGE05_GET", type="Ground",
    party=[("Whiscash", 33), ("Gligar", 33), ("Quagsire", 35)],
    intro="I was up before dawn hunting catfish in the mudflats. You'll find my Pokémon just as slippery!",
    defeat="Well, I'll be. The big one got away again.", post="Patience, that's the secret. In fishing and in battle.")
GYMS["InkaCity"] = dict(slot="TRAINER_JUAN_1", const="TRAINER_LEADER_FREA", name="Frea", pic="Expert F", gender="Female",
    gfx=G("WOMAN_4"), badge="FLAG_BADGE06_GET", type="Ice",
    party=[("Snorunt", 38), ("Sneasel", 38), ("Sealeo", 40)],
    intro="Every crate in Tosa goes through my cold store, on time and at the right temperature. You're next on my list.",
    defeat="Hm. I'll have to note that down.", post="Keep cool and stay organised. That's all there is to it.")
GYMS["BuraCity"] = dict(slot="TRAINER_FLANNERY_1", const="TRAINER_LEADER_MARIA", name="Maria", pic="Pokefan F", gender="Female",
    gfx=G("POKEFAN_F"), badge="FLAG_BADGE07_GET", type="Cat",
    party=[("Delcatty", 43), ("Espeon", 43), ("Persian", 45)],
    intro="Oh, a challenger! I only just got back from Juran. Don't mind the costumes, my darlings love dressing up!",
    defeat="My poor kitties! Let's call it a draw and go for noodles?", post="Win some, lose some. That's what I always say at the tables!")
GYMS["SenokoCity"] = dict(slot="TRAINER_WATTSON_1", const="TRAINER_LEADER_MO", name="Mo", pic="Leader Wattson", gender="Male",
    gfx=G("WATTSON"), badge="FLAG_BADGE08_GET", type="Electric",
    party=[("Manectric", 46), ("Magneton", 46), ("Electabuzz", 46), ("Raichu", 48)],
    intro="I keep the lights on across the whole of Tosa. Let's see if you can handle the full voltage!",
    defeat="Wahahah! You've short-circuited me!", post="Every turbine on the hill turns a little faster when a good battle's going on.")
