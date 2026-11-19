"""Post-game Sevii trainers (polish pass). Each entry turns one of the former FRLG trainers (left as flavour NPCs
by build_sevii.py) or an invented sea-route swimmer back into a real trainer. The post-battle line is the NPC's
existing flavour line, kept as it was.

Fields: map folder, script label suffix, constant suffix (TRAINER_SEVII_<x>), name (<=10 chars), class, pic,
gender, music, party [(species, level)], sight, optional overrides {"gfx", "movement"}, intro, defeat.
Teams follow FRLG's rematch teams for the same trainer (evolved, levels 58-68), default movesets, no items.
"""

T = []


def t(folder, label, const, name, cls, pic, gender, music, party, sight, intro, defeat, **over):
    T.append(dict(folder=folder, label=label, const="TRAINER_SEVII_" + const, name=name, cls=cls, pic=pic,
                  gender=gender, music=music, party=party, sight=sight, intro=intro, defeat=defeat, over=over))


SWIM_M = ("Swimmer M", "Swimmer M", "Male", "Swimmer")
SWIM_F = ("Swimmer F", "Swimmer F", "Female", "Swimmer")
RANGER_M = ("Pkmn Ranger", "Pokemon Ranger M", "Male", "Cool")
RANGER_F = ("Pkmn Ranger", "Pokemon Ranger F", "Female", "Cool")
AROMA = ("Aroma Lady", "Aroma Lady", "Female", "Female")
BIRD = ("Bird Keeper", "Bird Keeper", "Male", "Cool")
HIKER = ("Hiker", "Hiker", "Male", "Hiker")
RUIN = ("Ruin Maniac", "Ruin Maniac", "Male", "Hiker")

# ---------------------------------------------------------------- Isles 1-3 (Lv 58-61)
t("OneIsland_KindleRoad", "Maria", "MARIA", "Maria", *SWIM_F, [("Seadra", 58), ("Kingdra", 59)], 4,
  "The sea off Kindle Road is my training pool!", "I swallowed seawater...")
t("OneIsland_KindleRoad", "Finn", "FINN", "Finn", *SWIM_M, [("Tentacruel", 59), ("Starmie", 60)], 2,
  "Surfing past me? Not without a battle!", "Washed right out.")
t("OneIsland_KindleRoad", "Tommy", "TOMMY", "Tommy", "Fisherman", "Fisherman", "Male", "Hiker",
  [("Seaking", 58), ("Seaking", 58), ("Gyarados", 60)], 0,     # fishing off the shore: talk-to only (FRLG: sight 0)
  "Shh! You'll scare the fish! Fine, let's battle.", "My line snapped...")
t("OneIsland_KindleRoad", "Shea", "SHEA", "Shea", "Black Belt", "Black Belt", "Male", "Intense",
  [("Machoke", 59), ("Machamp", 60)], 2,
  "Kindle Road is my training ground! Hiyah!", "My stance was off!")
t("OneIsland_KindleRoad", "Bryce", "BRYCE", "Bryce", "Camper", "Camper", "Male", "Male",
  [("Raticate", 58), ("Sandslash", 59), ("Nidoking", 60)], 3,
  "I'm camping by the hot springs. Want to battle?", "Back to my tent...")
t("OneIsland_KindleRoad", "Claire", "CLAIRE", "Claire", "Picnicker", "Picnicker", "Female", "Girl",
  [("Persian", 58), ("Raichu", 59), ("Clefable", 59)], 2,
  "A picnic and a battle! The perfect day out!", "My picnic is ruined!")
t("OneIsland_TreasureBeach", "Amara", "AMARA", "Amara", *SWIM_F, [("Dewgong", 59), ("Cloyster", 60)], 2,
  "Looking for treasure? Get past me first!", "You found my weak spot.")
t("ThreeIsland_BondBridge", "Nikki", "NIKKI", "Nikki", *AROMA, [("Victreebel", 60), ("Bellossom", 60)], 3,
  "Breathe in the sea breeze... then battle!", "What a sour ending.")
t("ThreeIsland_BondBridge", "Amira", "AMIRA", "Amira", "Tuber F", "Tuber F", "Female", "Girl",
  [("Poliwhirl", 58), ("Poliwrath", 60)], 2,
  "My float ring and I are ready!", "Waaah! I lost!", movement="MOVEMENT_TYPE_FACE_LEFT")  # faced the sea
t("ThreeIsland_BondBridge", "Tisha", "TISHA", "Tisha", *SWIM_F, [("Kingler", 60), ("Starmie", 60)], 2,
  "Swimming under Bond Bridge is the best!", "I'm all washed up.")
t("MtEmber_Exterior", "Logan", "LOGAN", "Logan", *RANGER_M, [("Tangela", 60), ("Exeggutor", 61)], 4,
  "Rangers keep Mt. Ember safe. Show me your skill!", "You're the real deal.",
  gfx="OBJ_EVENT_GFX_POKEMON_RANGER_M")
t("MtEmber_Exterior", "Beth", "BETH", "Beth", *RANGER_F, [("Vileplume", 60), ("Victreebel", 61)], 3,
  "The mountain path is dangerous. Let me test you!", "You can handle Mt. Ember.",
  gfx="OBJ_EVENT_GFX_POKEMON_RANGER_F")
t("SeviiSeaRouteA", "Swimmer1", "DYLAN", "Dylan", *SWIM_M, [("Tentacruel", 59), ("Golduck", 60)], 3,
  "Crossing the strait? Race you... in battle!", "You're faster than the current!",
  movement="MOVEMENT_TYPE_FACE_LEFT_AND_RIGHT")

# ---------------------------------------------------------------- Isles 4-5 (Lv 61-64)
t("FiveIsland_MemorialPillar", "Milo", "MILO", "Milo", *BIRD, [("Fearow", 62), ("Pidgeot", 63)], 3,
  "My birds soar over Five Isle! Battle!", "Grounded!")
t("FiveIsland_MemorialPillar", "Chaz", "CHAZ", "Chaz", *BIRD, [("Fearow", 62), ("Dodrio", 63)], 2,
  "The wind off the sea is perfect for flying!", "My birds lost their wind.")
t("FiveIsland_MemorialPillar", "Harold", "HAROLD", "Harold", *BIRD, [("Noctowl", 62), ("Xatu", 63)], 3,
  "Hoo! Hoo! Battle me!", "My owl saw that coming...")
t("SeviiSeaRouteC", "Swimmer1", "RORY", "Rory", *SWIM_M, [("Tentacruel", 62), ("Gyarados", 63)], 3,
  "These waters are mine. Let's go!", "I'm sunk!", movement="MOVEMENT_TYPE_FACE_LEFT_AND_RIGHT")
t("SeviiSeaRouteC", "Swimmer2", "LANA", "Lana", *SWIM_F, [("Seaking", 62), ("Dewgong", 63)], 3,
  "Swimming between the islands builds stamina!", "I need a rest...",
  movement="MOVEMENT_TYPE_FACE_DOWN_AND_UP")

# ---------------------------------------------------------------- Isles 6-7 (Lv 64-68)
t("SixIsland_WaterPath", "Rose", "ROSE", "Rose", *AROMA, [("Sunflora", 64), ("Bellossom", 64)], 3,
  "The flowers along Water Path smell lovely!", "My petals wilted...")
t("SixIsland_WaterPath", "Samir", "SAMIR", "Samir", *SWIM_M, [("Starmie", 64), ("Gyarados", 65)], 3,
  "Nobody swims Water Path faster than me!", "Overtaken!")
t("SixIsland_WaterPath", "Denise", "DENISE", "Denise", *SWIM_F, [("Lanturn", 64), ("Azumarill", 64)], 2,
  "The water's so clear here! Battle?", "That light went out.")
t("SixIsland_WaterPath", "Earl", "EARL", "Earl", *HIKER, [("Steelix", 64), ("Machamp", 65)], 3,
  "Ruin Valley's hills keep me strong!", "My knees gave out.")
t("SixIsland_RuinValley", "Stanly", "STANLY", "Stanly", *RUIN, [("Golem", 65), ("Steelix", 65)], 3,
  "These ruins are mine to dig! Out of my way!", "Buried alive!")
t("SixIsland_RuinValley", "Daryl", "DARYL", "Daryl", *HIKER, [("Rhydon", 65), ("Sudowoodo", 66)], 2,
  "Is that a tree? No, it's my partner!", "Timber!")
t("SixIsland_RuinValley", "Hector", "HECTOR", "Hector", "Pokemaniac", "Pokemaniac", "Male", "Suspicious",
  [("Rhydon", 66), ("Kangaskhan", 66)], 2,
  "My rare Pokémon will crush you!", "My collection!")
t("SevenIsland_SevaultCanyon_Entrance", "Miah", "MIAH", "Miah", *AROMA, [("Vileplume", 65), ("Bellossom", 66)], 3,
  "A sweet scent drifts through the canyon...", "How bitter...")
t("SevenIsland_SevaultCanyon_Entrance", "Nicolas", "NICOLAS", "Nicolas", *RANGER_M,
  [("Victreebel", 66), ("Exeggutor", 66)], 2,
  "Sevault Canyon is tough. Prove you're ready!", "You'll do fine in there.",
  gfx="OBJ_EVENT_GFX_POKEMON_RANGER_M")
t("SevenIsland_SevaultCanyon_Entrance", "Madeline", "MADELINE", "Madeline", *RANGER_F,
  [("Tangela", 66), ("Vileplume", 66)], 2,
  "Rangers patrol here. Let's see your skill!", "Impressive work.",
  gfx="OBJ_EVENT_GFX_POKEMON_RANGER_F")
t("SevenIsland_SevaultCanyon", "Jackson", "JACKSON", "Jackson", *RANGER_M,
  [("Tangela", 66), ("Exeggutor", 67)], 3,
  "Only the strong make it through Sevault Canyon!", "You're strong, all right.",
  gfx="OBJ_EVENT_GFX_POKEMON_RANGER_M")
t("SevenIsland_SevaultCanyon", "Leroy", "LEROY", "Leroy", "Cooltrainer", "Cooltrainer M", "Male", "Cool",
  [("Slowbro", 67), ("Rhydon", 67), ("Ursaring", 68)], 2,
  "I came all the way here to train. Face me!", "My training isn't over.")
t("SevenIsland_SevaultCanyon", "Michelle", "MICHELLE", "Michelle", "Cooltrainer", "Cooltrainer F", "Female", "Cool",
  [("Ninetales", 67), ("Rapidash", 67), ("Girafarig", 68)], 2,
  "Only elite Trainers come this far. Battle!", "You're elite too.")
t("SevenIsland_TanobyRuins", "Brandon", "BRANDON", "Brandon", *RUIN, [("Golem", 67), ("Steelix", 68)], 2,
  "The ruins hold secrets. You won't take them!", "Crumbled like old stone.")
t("SevenIsland_TanobyRuins", "Clifford", "CLIFFORD", "Clifford", "Gentleman", "Gentleman", "Male", "Rich",
  [("Golduck", 67), ("Marowak", 67)], 2,
  "A gentleman's battle among the ruins?", "Splendid, simply splendid.")

# reused vanilla slots, in order (31 upward; rematch/Match Call/gym-roster/Gabby & Ty slots skipped)
SLOTS = [(31, "TRAINER_ZANDER"), (32, "TRAINER_SHELLY_WEATHER_INSTITUTE"), (33, "TRAINER_SHELLY_SEAFLOOR_CAVERN"),
         (34, "TRAINER_ARCHIE"), (35, "TRAINER_LEAH"), (36, "TRAINER_DAISY"), (38, "TRAINER_FELIX"),
         (39, "TRAINER_VIOLET"), (45, "TRAINER_CHIP"), (46, "TRAINER_FOSTER"), (58, "TRAINER_AUSTINA"),
         (59, "TRAINER_GWEN"), (65, "TRAINER_SIMON"), (66, "TRAINER_CHARLIE"), (75, "TRAINER_BRAXTON"),
         (76, "TRAINER_VINCENT"), (77, "TRAINER_LEROY"), (79, "TRAINER_EDGAR"), (80, "TRAINER_ALBERT"),
         (81, "TRAINER_SAMUEL"), (82, "TRAINER_VITO"), (83, "TRAINER_OWEN"), (88, "TRAINER_WARREN"),
         (92, "TRAINER_WENDY"), (93, "TRAINER_KEIRA"), (95, "TRAINER_JENNIFER"), (96, "TRAINER_HOPE"),
         (97, "TRAINER_SHANNON"), (98, "TRAINER_MICHELLE"), (99, "TRAINER_CAROLINE"), (100, "TRAINER_JULIE"),
         (105, "TRAINER_PATRICIA"), (106, "TRAINER_KINDRA")]
