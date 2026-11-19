# -*- coding: utf-8 -*-
"""Delta species: Pokédex text, δ level-up move patches. Data only; used by gen_delta.py."""

# delta constant suffix (base species without SPECIES_) -> (category, [4 description lines])
DEX = {
    "STANTLER": ("Dream Horn", [
        "Its antlers soaked up the Research",
        "Tower's magnetic waves. The space",
        "between them warps, showing dreamlike",
        "visions of faraway places."]),
    "RALTS": ("Sprout", [
        "A Ralts changed by Holon's magnetic",
        "tower. The horns on its head sprouted",
        "leaves. It basks in sunlight to sense",
        "the feelings of nearby plants."]),
    "KIRLIA": ("Bloom", [
        "It dances in Holon's meadows at dawn.",
        "Each spin scatters pollen that makes",
        "flowers bloom. Researchers think its",
        "type shifted near the tower."]),
    "GARDEVOIR": ("Garden", [
        "It shields its Trainer with a wall of",
        "vines. The researchers' magnetic tower",
        "turned its psychic power into the",
        "power of plants."]),
    "GALLADE": ("Thornblade", [
        "Its arm blades grew into sharp leaves",
        "that never wilt. It cuts through",
        "Holon's thickets to protect the weak",
        "and tends the gardens it clears."]),
    "DRATINI": ("Spark", [
        "Static crackles along its body after",
        "it swims near Holon's magnetic tower.",
        "Fishermen say its sparks light up",
        "the canals at night."]),
    "DRAGONAIR": ("Static", [
        "The orbs on its tail store electricity",
        "drawn from the air. When they are",
        "full, it can call down lightning on",
        "a cloudless day."]),
    "DRAGONITE": ("Thunder", [
        "It flies through thunderclouds to",
        "recharge. The tower's magnetic waves",
        "changed its type, but it is still",
        "kind and rescues lost sailors."]),
    "PURRLOIN": ("Charm", [
        "Its cute act is no longer a trick.",
        "Since the tower changed its type, it",
        "gives back what it steals, along with",
        "a sweet, sparkling meow."]),
    "LIEPARD": ("Grace", [
        "Its spotted coat shimmers in soft",
        "pastel colors. People who watch it",
        "move forget their worries. It lives",
        "close to Holon's Research Tower."]),
    "GLAMEOW": ("Pretty", [
        "Holon's researchers say its fickle",
        "temper softened when its type changed.",
        "It purrs when hugged, but still lashes",
        "out with its tail when it is bored."]),
    "PURUGLY": ("Pastel", [
        "It ties its tails around its waist",
        "like a ribbon. Its glare charms foes",
        "instead of scaring them. It claims",
        "Holon's sunny rooftops as its own."]),
    "DRIFLOON": ("Hot Air", [
        "Warm air inside it lets it float",
        "higher than other Drifloon. Children",
        "in Holon follow it, hoping it will",
        "carry them up into the sky."]),
    "DRIFBLIM": ("Sky Lantern", [
        "It drifts over Holon at dusk, glowing",
        "like a paper lantern. The heat inside",
        "it comes from magnetic waves it took",
        "in from the Research Tower."]),
    "KLINK": ("Frost Gear", [
        "Its gears turned to stone and ice",
        "near the Research Tower. Frost forms",
        "where they mesh, so they spin slowly",
        "but never wear down."]),
    "KLANG": ("Frost Gear", [
        "The small gear is hard rock and the",
        "big one is ice. If they spin out of",
        "step, friction melts the ice gear and",
        "it must stop to freeze again."]),
    "KLINKLANG": ("Frost Gear", [
        "Its red core charges its icy gears",
        "with magnetic energy. It fires shards",
        "of frozen rock from its spikes at",
        "anything that nears the tower."]),
    "FARFETCHD": ("Steel Duck", [
        "The stalk it carries hardened into a",
        "blade of steel. It guards Holon's",
        "canals and fences with any challenger",
        "brave enough to approach."]),
    "PANCHAM": ("Mystic", [
        "It glares at foes to unsettle them,",
        "and now its glare carries psychic",
        "power. The leaf in its mouth floats",
        "when it concentrates."]),
    "PANGORO": ("Mystic", [
        "It meditates in Holon's bamboo groves.",
        "Its leaf floats in midair as it reads",
        "the intentions of its foes. One stare",
        "can stop a brawl before it starts."]),
    "RELICANTH": ("Mossback", [
        "Moss and roots cover its rocky scales.",
        "Holon's magnetic waves drove it from",
        "the deep sea into muddy shallows,",
        "where it digs in the silt for food."]),
    "LARVITAR": ("Ember Skin", [
        "It is born deep in Holon's hot ground.",
        "It eats volcanic rock, and its body",
        "heat rises as it grows. Its skin is",
        "too hot to touch."]),
    "PUPITAR": ("Magma Shell", [
        "Molten rock churns inside its shell.",
        "When it vents the pressure, it rockets",
        "about in bursts of flame. It is found",
        "near Holon's hot springs."]),
    "TYRANITAR": ("Forge", [
        "Its armor is like iron fresh from the",
        "forge, and its steps leave scorch",
        "marks on the ground. The tower's waves",
        "made it Fire and Steel."]),
    "BAGON": ("Hot Head", [
        "It headbutts rocks until sparks fly",
        "and its head glows red. It longs to",
        "fly, so it leaps from Holon's cliffs",
        "warmed by its own flames."]),
    "SHELGON": ("Kiln", [
        "Its shell is as hot as a kiln. Inside,",
        "its cells reshape themselves with",
        "heat. Holon's scientists study it for",
        "clues to how Delta species form."]),
    "SALAMENCE": ("Forge Wing", [
        "Its wings are plated with steel that",
        "glows red in flight. When angry, it",
        "breathes flames hot enough to melt",
        "iron."]),
    "BELDUM": ("Magnet", [
        "It floats on magnetic force it took",
        "in from Holon's Research Tower.",
        "Electricity sparks from its claws",
        "when it meets others of its kind."]),
    "METANG": ("Magnet", [
        "Two Beldum-δ linked by an electric",
        "current. Its brains swap signals",
        "through crackling sparks, so it thinks",
        "faster than a computer."]),
    "METAGROSS": ("Iron Leg", [
        "Its four brains run on electricity.",
        "It holds itself in the air with",
        "magnetism and charges its legs with",
        "current before it strikes."]),
    "EEVEE": ("Evolution", [
        "Its fur grew a metallic sheen after",
        "it slept near the Research Tower. Its",
        "unstable genes carry the tower's",
        "magnetism into every evolution."]),
    "VAPOREON": ("Bubble Jet", [
        "Its body is coated in a thin layer of",
        "metal that never rusts. It can melt",
        "into water and then re-form its steel",
        "scales at will."]),
    "JOLTEON": ("Lightning", [
        "Its steely fur bristles like needles.",
        "It draws electricity from the",
        "magnetic field around Holon's tower",
        "and stores it in its coat."]),
    "FLAREON": ("Flame", [
        "A metal shell holds in its body heat.",
        "Its fluffy collar glows like hot",
        "steel when it breathes fire, and it",
        "is warm enough to melt snow nearby."]),
    "ESPEON": ("Sun", [
        "The gem on its forehead turned to",
        "polished steel. It reflects sunlight",
        "into beams and reads the future in",
        "their shimmer."]),
    "UMBREON": ("Moonlight", [
        "Its rings shine silver, not gold.",
        "Steel plates under its fur make it",
        "hard to injure. It lurks in the shadow",
        "of the Research Tower at night."]),
    "LEAFEON": ("Verdant", [
        "Its leaves have metal edges sharp",
        "enough to cut stone. It soaks up",
        "sunlight beside the Research Tower",
        "and gives off clean, crisp air."]),
    "GLACEON": ("Fresh Snow", [
        "It freezes the air around it into",
        "steel-hard ice crystals. Its fur",
        "shines like frosted metal. It is",
        "calmest on cold Holon mornings."]),
    "SYLVEON": ("Intertwine", [
        "Its ribbon feelers are threaded with",
        "fine steel wire. They pick up both",
        "magnetic signals and the feelings of",
        "its Trainer."]),
    "MAGIKARP": ("Fish", [
        "Its scales turned to tarnished metal.",
        "It is heavier than other Magikarp, so",
        "it splashes even more clumsily. Some",
        "say its steel scales bring luck."]),
    "GYARADOS": ("Atrocious", [
        "Its golden scales crackle with",
        "electricity. Holon legend says one",
        "rose from the lake on the day the",
        "Research Tower was switched on."]),
    "PICHU": ("Tiny Mouse", [
        "Its cheeks hold no electricity. They",
        "feel cold and hard like metal. It",
        "still tries to zap people, then looks",
        "puzzled when nothing happens."]),
    "PIKACHU": ("Mouse", [
        "Its cheek pouches turned to steel. It",
        "gathers iron sand on its tail and",
        "hones it into a blade. It lives in",
        "the woods near Holon's tower."]),
    "RAICHU": ("Mouse", [
        "Its tail is heavy metal that it swings",
        "like a hammer. It no longer stores",
        "electricity, but its steel body can",
        "shrug off most attacks."]),
    "HORSEA": ("Ember", [
        "It lives in Holon's warm springs. It",
        "spits hot embers instead of ink to",
        "drive off foes. The water bubbles",
        "around it when it is upset."]),
    "SEADRA": ("Ember", [
        "The spines on its body burn anyone",
        "who touches them. It swims in the",
        "steaming water of Holon's lake, where",
        "magma warms the ground."]),
    "KINGDRA": ("Ember", [
        "Its armored scales gleam like hot",
        "metal. When it yawns, it stirs up a",
        "whirlpool of steam that scalds",
        "everything nearby."]),
    "TRAPINCH": ("Ant Pit", [
        "It digs pits lined with sticky leaves",
        "in Holon's meadows. Its jaws can grip",
        "anything, but it would rather munch",
        "on sweet fruit."]),
    "VIBRAVA": ("Vibration", [
        "Its wings rustle like leaves in the",
        "wind. The soothing sound makes foes",
        "drowsy. It lives in the gardens",
        "around the Research Tower."]),
    "FLYGON": ("Mystic", [
        "Its wings are edged with steel leaves.",
        "It stirs up storms of petals that",
        "hide it from view. Holon calls it the",
        "spirit of the forest."]),
    "MEOWTH": ("Scratch Cat", [
        "It hoards metal scraps, not coins.",
        "Since the tower changed its type, it",
        "sneaks into the lab at night to steal",
        "spare parts."]),
    "PERSIAN": ("Classy Cat", [
        "Its gem turned to dark iron. It prowls",
        "Holon's alleys at night, and its steel",
        "claws strike sparks on the stones. It",
        "respects only the strong."]),
    "CHARMANDER": ("Lizard", [
        "The flame on its tail turned into a",
        "ball of crackling electricity. If the",
        "spark fades, it rushes off to recharge",
        "by Holon's power lines."]),
    "CHARMELEON": ("Spark", [
        "It slashes with claws charged with",
        "electricity. When it gets excited,",
        "sparks fly from its tail and make the",
        "air around it crackle."]),
    "CHARIZARD": ("Thunder", [
        "Its wings are plated with steel, and",
        "its tail flame burns blue with",
        "electricity. It flies near Holon's",
        "tower to charge before a battle."]),
    "FEEBAS": ("Fish", [
        "It lives in Holon's hot springs. Its",
        "shabby scales are warm to the touch.",
        "Most people ignore it, but its fins",
        "give off tiny flickering flames."]),
    "MILOTIC": ("Tender", [
        "Its scales shimmer like glowing coals.",
        "Gazing at it is said to warm the",
        "heart. It rests on Holon's lake on",
        "cold nights."]),
    # ---- tier B (Holon Phantoms / Crystal Guardians / Dragon Frontiers lines)
    "PIDGEY": ("Tiny Bird", [
        "Its feathers crackle with static. It",
        "nests on the Research Tower's iron",
        "beams, where the magnetic waves",
        "keep its wings charged."]),
    "PIDGEOTTO": ("Bird", [
        "It patrols the skies over Holon. When",
        "it beats its wings hard, sparks fly",
        "from its plumage and stun the prey",
        "it spots below."]),
    "PIDGEOT": ("Bird", [
        "Its crest feathers became thin steel",
        "blades. It soars through storms at",
        "high speed, drawing lightning into",
        "its wings."]),
    "PSYDUCK": ("Duck", [
        "When its headache flares, sparks",
        "jump from its head. The more it",
        "hurts, the stronger the current it",
        "gives off."]),
    "GOLDUCK": ("Duck", [
        "It swims Holon's lakes at night,",
        "lighting the water with the current",
        "from its forehead gem. Fish gather",
        "toward the glow."]),
    "ODDISH": ("Weed", [
        "It buries itself in damp soil by",
        "day. Its leaves soak up rainwater,",
        "and it sprays it at anything that",
        "comes too close."]),
    "GLOOM": ("Weed", [
        "The nectar that drips from its mouth",
        "gives off a sweet psychic haze.",
        "Those who breathe it in see visions",
        "of distant fields."]),
    "VILEPLUME": ("Flower", [
        "Its petals hardened into metal plates",
        "near the tower. It shakes them to",
        "scatter pollen that confuses the",
        "mind of its foe."]),
    "BELLOSSOM": ("Flower", [
        "When it dances in the rain, its",
        "petals ring like little bells. It is",
        "said to call down showers on dry",
        "Holon fields."]),
    "KABUTO": ("Shellfish", [
        "Revived from a fossil in the Research",
        "Tower's lab. Its shell stores static",
        "charge, and it gives off sparks when",
        "it is touched."]),
    "KABUTOPS": ("Shellfish", [
        "Its scythes carry a strong current.",
        "It slashes its prey with them and",
        "stuns it in a single blow, then",
        "drags it into the sea."]),
    "OMANYTE": ("Spiral", [
        "A fossil Pokemon revived near the",
        "tower. It floats in the air using",
        "psychic power instead of swimming,",
        "spinning its shell."]),
    "OMASTAR": ("Spiral", [
        "Its spiral shell bends light into",
        "strange patterns. Gazing at the",
        "pattern for too long is said to",
        "put people to sleep."]),
    "ANORITH": ("Old Shrimp", [
        "Its claws turned to iron while it",
        "lay fossilised in Holon's magnetic",
        "rock. It clacks them together to",
        "scare off its foes."]),
    "ARMALDO": ("Plate", [
        "Its body is covered in thick steel",
        "plates. It can shrug off almost any",
        "attack, then strikes back with its",
        "iron-hard claws."]),
    "LILEEP": ("Sea Lily", [
        "A fossil Pokemon that turned dark",
        "and shadowy after its revival. It",
        "waits motionless in murky water to",
        "ambush its prey."]),
    "CRADILY": ("Barnacle", [
        "Its tentacles became hard as steel.",
        "It drags prey into the dark of the",
        "deep sea, where few Pokemon dare to",
        "follow it."]),
    "TREECKO": ("Wood Gecko", [
        "The magnetic waves sharpened its",
        "senses. It can tell what its foe",
        "will do next and dodges the attack",
        "before it starts."]),
    "GROVYLE": ("Wood Gecko", [
        "It leaps from tree to tree in Holon's",
        "forests. The leaves on its arms glow",
        "faintly when it focuses its psychic",
        "power."]),
    "SCEPTILE": ("Forest", [
        "The leaves on its arms channel its",
        "psychic power into blades of light.",
        "It guards the deepest part of the",
        "forest alone."]),
    "KRABBY": ("River Crab", [
        "It lives near Holon's hot springs.",
        "Its shell heats up when it is angry,",
        "and the bubbles it blows are hot",
        "enough to scald."]),
    "KINGLER": ("Pincer", [
        "Its giant claw glows red-hot. It",
        "crushes iron with a single pinch,",
        "and its steel shell protects it from",
        "its own heat."]),
    "WINGULL": ("Seagull", [
        "It rides the winds before a storm.",
        "Its wings build up static charge as",
        "it glides, and it zaps fish near the",
        "surface."]),
    "PELIPPER": ("Water Bird", [
        "It stores charge in its big bill and",
        "releases it in a flash to signal its",
        "flock. Fishermen read its flashes to",
        "predict storms."]),
    "SWABLU": ("Cotton Bird", [
        "Its fluffy wings soak up mist like a",
        "sponge. On hot days it shakes them",
        "out to cool down the Pokemon around",
        "it."]),
    "ALTARIA": ("Humming", [
        "It flies among the rain clouds and",
        "sings. Its cotton wings hold so much",
        "water that its song is said to bring",
        "the rain."]),
    "MAREEP": ("Wool", [
        "Its wool lost all its static near",
        "the tower. It is soft and warm, and",
        "Holon's villagers weave it into",
        "winter clothes."]),
    "FLAAFFY": ("Wool", [
        "Its pink skin is tough and smooth.",
        "It is very friendly, and it follows",
        "the villagers around the fields as",
        "they work."]),
    "AMPHAROS": ("Light", [
        "The orb on its tail no longer glows.",
        "Instead it rings a deep, clear tone",
        "that carries far across Holon's",
        "foggy coast."]),
    "TOTODILE": ("Big Jaw", [
        "Its jaws spark when it snaps them",
        "shut. It bites anything that moves,",
        "so even its Trainer should take",
        "care around it."]),
    "CROCONAW": ("Big Jaw", [
        "Its fangs carry an electric charge.",
        "Once it bites down, the current",
        "numbs its prey so that it can't",
        "break free."]),
    "FERALIGATR": ("Big Jaw", [
        "It charges through the water with",
        "its huge jaws open. The current",
        "around its body lights up the",
        "lake at night."]),
    "VULPIX": ("Fox", [
        "It was born with a single tail that",
        "splits as it grows. It reads the",
        "thoughts of people nearby and plays",
        "tricks on them."]),
    "NINETALES": ("Fox", [
        "Its nine tails shine with a pale",
        "light. It is said to show visions of",
        "the future to those who stare into",
        "its eyes."]),
}

# line (base species of the line) -> [(level, MOVE)], applied to every member of the line.
LINE_MOVES = {
    "STANTLER":   [(11, "CONFUSION"), (21, "PSYBEAM"), (33, "ZEN_HEADBUTT")],
    "RALTS":      [(9, "MAGICAL_LEAF"), (23, "GIGA_DRAIN"), (38, "ENERGY_BALL")],
    "DRATINI":    [(1, "THUNDER_SHOCK"), (18, "SPARK"), (41, "WILD_CHARGE")],
    "PURRLOIN":   [(6, "FAIRY_WIND"), (21, "DRAINING_KISS"), (36, "PLAY_ROUGH")],
    "GLAMEOW":    [(5, "FAIRY_WIND"), (20, "DRAINING_KISS"), (37, "PLAY_ROUGH")],
    "DRIFLOON":   [(8, "EMBER"), (20, "INCINERATE"), (40, "HEAT_WAVE")],
    "KLINK":      [(4, "POWDER_SNOW"), (16, "ROCK_TOMB"), (42, "ICICLE_CRASH")],
    "FARFETCHD":  [(9, "METAL_CLAW"), (21, "STEEL_WING"), (37, "IRON_HEAD")],
    "PANCHAM":    [(8, "CONFUSION"), (27, "ZEN_HEADBUTT"), (40, "PSYCHO_CUT")],
    "RELICANTH":  [(6, "MUD_SLAP"), (16, "BULLET_SEED"), (31, "SEED_BOMB")],
    "LARVITAR":   [(6, "EMBER"), (21, "FIRE_FANG"), (47, "FLARE_BLITZ")],
    "BAGON":      [(5, "EMBER"), (20, "FIRE_FANG"), (45, "FLARE_BLITZ")],
    "BELDUM":     [(1, "SPARK"), (26, "THUNDER_PUNCH"), (50, "WILD_CHARGE")],
    "EEVEE":      [(10, "METAL_CLAW"), (25, "MIRROR_SHOT"), (40, "FLASH_CANNON")],
    "MAGIKARP":   [(21, "THUNDER_FANG"), (30, "IRON_HEAD"), (42, "WILD_CHARGE")],
    "PICHU":      [(8, "METAL_CLAW"), (20, "MIRROR_SHOT"), (36, "FLASH_CANNON")],
    "HORSEA":     [(1, "EMBER"), (20, "INCINERATE"), (38, "FLAMETHROWER")],
    "TRAPINCH":   [(10, "BULLET_SEED"), (26, "SEED_BOMB"), (40, "LEAF_BLADE")],
    "MEOWTH":     [(8, "METAL_CLAW"), (32, "IRON_HEAD")],
    "CHARMANDER": [(4, "THUNDER_SHOCK"), (17, "THUNDER_FANG"), (36, "DISCHARGE")],
    "FEEBAS":     [(15, "EMBER"), (32, "FLAMETHROWER"), (44, "HEAT_WAVE")],
    # tier B
    "PIDGEY":     [(9, "THUNDER_SHOCK"), (21, "SPARK"), (37, "DISCHARGE")],
    "PSYDUCK":    [(7, "THUNDER_SHOCK"), (17, "SPARK"), (35, "DISCHARGE")],
    "ODDISH":     [(6, "WATER_GUN"), (22, "BUBBLE_BEAM"), (38, "MUDDY_WATER")],
    "KABUTO":     [(6, "THUNDER_SHOCK"), (20, "THUNDER_FANG"), (45, "WILD_CHARGE")],
    "OMANYTE":    [(5, "CONFUSION"), (20, "PSYBEAM"), (45, "PSYCHIC")],
    "ANORITH":    [(18, "IRON_HEAD"), (40, "METEOR_MASH")],
    "LILEEP":     [(6, "SNARL"), (22, "ASSURANCE"), (40, "DARK_PULSE")],
    "TREECKO":    [(6, "CONFUSION"), (21, "PSYBEAM"), (36, "PSYCHO_CUT")],
    "KRABBY":     [(5, "EMBER"), (20, "FIRE_FANG"), (44, "FLARE_BLITZ")],
    "WINGULL":    [(5, "THUNDER_SHOCK"), (20, "SHOCK_WAVE"), (40, "DISCHARGE")],
    "SWABLU":     [(4, "WATER_GUN"), (20, "WATER_PULSE"), (40, "HYDRO_PUMP")],
    "MAREEP":     [(11, "SWIFT"), (25, "TRI_ATTACK"), (39, "HYPER_VOICE")],
    "TOTODILE":   [(6, "THUNDER_SHOCK"), (19, "THUNDER_FANG"), (41, "WILD_CHARGE")],
    "VULPIX":     [(4, "CONFUSION"), (16, "PSYBEAM"), (40, "PSYCHIC")],
}

# per-species overrides of the line patch
SPECIES_MOVES = {
    # Magikarp can't use attacks: it gets the Steel status move instead; Gyarados-δ gets the line patch.
    "MAGIKARP": [(25, "IRON_DEFENSE")],
    "GALLADE": [(1, "LEAF_BLADE"), (9, "MAGICAL_LEAF"), (23, "GIGA_DRAIN"), (38, "ENERGY_BALL")],
    # tier B: Steel second types get a Steel evolution move; the Oddish line changes type per stage.
    "PIDGEOT": [(0, "STEEL_WING"), (9, "THUNDER_SHOCK"), (21, "SPARK"), (37, "DISCHARGE")],
    "KINGLER": [(0, "IRON_HEAD"), (5, "EMBER"), (20, "FIRE_FANG"), (44, "FLARE_BLITZ")],
    "CRADILY": [(0, "FLASH_CANNON"), (6, "SNARL"), (22, "ASSURANCE"), (40, "DARK_PULSE")],
    "GLOOM": [(6, "WATER_GUN"), (1, "CONFUSION"), (22, "PSYBEAM"), (38, "PSYCHIC")],
    "VILEPLUME": [(0, "PSYCHIC"), (1, "CONFUSION"), (1, "PSYBEAM"), (1, "FLASH_CANNON")],
    "BELLOSSOM": [(0, "WATER_PULSE"), (1, "WATER_GUN"), (1, "BUBBLE_BEAM"), (1, "MUDDY_WATER")],
}
