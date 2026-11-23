// Professor Palm's research tasks (PLACEHOLDER text and rewards - rewrite freely). One entry per task; the order
// is the order in the QUESTS Research tab and the bit in SaveBlock3.researchClaimed (append new tasks at the end).
//   SURVEY       catalogue every species (day + night) of every habitat in a zone; one step per habitat
//   NIGHT_WATCH  catalogue the zone's night-only species
//   REQUEST      catalogue one species (Palm says where to look)

#define SURVEY(nm, ds, rg, zn, item, qty, pts) \
    {.name = COMPOUND_STRING(nm), .desc = COMPOUND_STRING(ds), .type = RESEARCH_SURVEY, .region = rg, .zone = zn, \
     .sprite = ITEM_TOWN_MAP, .spriteType = ITEM, .rewardItem = item, .rewardQty = qty, .rp = pts}
#define NIGHT_WATCH(nm, ds, rg, zn, item, qty, pts) \
    {.name = COMPOUND_STRING(nm), .desc = COMPOUND_STRING(ds), .type = RESEARCH_NIGHT_WATCH, .region = rg, .zone = zn, \
     .sprite = ITEM_MOON_STONE, .spriteType = ITEM, .rewardItem = item, .rewardQty = qty, .rp = pts}
#define REQUEST(nm, ds, sp, sec, item, qty, pts) \
    {.name = COMPOUND_STRING(nm), .desc = COMPOUND_STRING(ds), .type = RESEARCH_REQUEST, .region = HAB_REGION_TOSA, \
     .species = sp, .mapsec = sec, .sprite = sp, .spriteType = PKMN, .rewardItem = item, .rewardQty = qty, .rp = pts}

static const struct ResearchTask sResearchTasks[] =
{
    SURVEY("Western Tosa survey", "Catalogue every species on\neach Western Tosa route.", HAB_REGION_TOSA, HAB_ZONE_WEST, ITEM_GREAT_BALL, 10, 40),
    NIGHT_WATCH("Night watch: Western Tosa", "Catalogue the species that only\ncome out at night in the west.", HAB_REGION_TOSA, HAB_ZONE_WEST, ITEM_MOON_STONE, 1, 30),
    SURVEY("Southern Tosa survey", "Catalogue every species on\neach Southern Tosa route.", HAB_REGION_TOSA, HAB_ZONE_SOUTH, ITEM_ULTRA_BALL, 5, 60),
    NIGHT_WATCH("Night watch: Southern Tosa", "Catalogue the species that only\ncome out at night in the south.", HAB_REGION_TOSA, HAB_ZONE_SOUTH, ITEM_DUSK_BALL, 5, 30),
    SURVEY("Northern Tosa survey", "Catalogue every species on\neach Northern Tosa route.", HAB_REGION_TOSA, HAB_ZONE_NORTH, ITEM_LEAF_STONE, 1, 60),
    NIGHT_WATCH("Night watch: Northern Tosa", "Catalogue the species that only\ncome out at night in the north.", HAB_REGION_TOSA, HAB_ZONE_NORTH, ITEM_DUSK_STONE, 1, 30),
    SURVEY("Eastern Tosa survey", "Catalogue every species on\neach Eastern Tosa route.", HAB_REGION_TOSA, HAB_ZONE_EAST, ITEM_THUNDER_STONE, 1, 60),
    NIGHT_WATCH("Night watch: Eastern Tosa", "Catalogue the species that only\ncome out at night in the east.", HAB_REGION_TOSA, HAB_ZONE_EAST, ITEM_DUSK_BALL, 5, 30),
    REQUEST("Request: reserve fighter", "Palm wants a Tyrogue from\nthe reserve catalogued.", SPECIES_TYROGUE, MAPSEC_SOUTH_TOSA_RESERVE_1, ITEM_POKE_BALL, 5, 10),
    REQUEST("Request: marsh catfish", "Palm wants a Barboach from\nthe marsh catalogued.", SPECIES_BARBOACH, MAPSEC_MOONGROVE_MARSH, ITEM_NET_BALL, 3, 10),
    REQUEST("Request: mudskipper", "Wild Mudkip in the mangroves?\nPalm needs proof: catalogue one.", SPECIES_MUDKIP, MAPSEC_MOONGROVE_MARSH, ITEM_GREAT_BALL, 3, 10),
    REQUEST("Request: rush stalker", "Purrchi stalk the marsh rushes.\nCatalogue one for the notes.", SPECIES_PURRCHI, MAPSEC_MOONGROVE_MARSH, ITEM_NEST_BALL, 3, 10),
    REQUEST("Request: the elusive one", "Old fishers swear Feebas live\nin the marsh. Catalogue one!", SPECIES_FEEBAS, MAPSEC_MOONGROVE_MARSH, ITEM_PRISM_SCALE, 1, 20),
    REQUEST("Request: night owl", "Hoothoot only call at night.\nCatalogue one for Palm.", SPECIES_HOOTHOOT, MAPSEC_SOUTH_TOSA_RESERVE_1, ITEM_MOON_BALL, 2, 10),
    REQUEST("Request: tunnel smog", "Koffing are clogging the rail\ntunnels. Catalogue one.", SPECIES_KOFFING, MAPSEC_RAILWAY_TUNNELS, ITEM_SUPER_POTION, 3, 10),
    REQUEST("Request: reserve native", "Iyepure are Tosa natives.\nCatalogue one for the survey.", SPECIES_IYEPURE, MAPSEC_SOUTH_TOSA_RESERVE_1, ITEM_GREAT_BALL, 3, 10),
    REQUEST("Request: foothill pup", "Rockruff roam the foothills\npast Timah. Catalogue one.", SPECIES_ROCKRUFF, MAPSEC_ROUTE_302, ITEM_ULTRA_BALL, 2, 10),
    REQUEST("Request: life-ring thief", "Torpesquid steal life rings in\nthe harbour. Catalogue one.", SPECIES_TORPESQUID, MAPSEC_TOSA_PORT, ITEM_DIVE_BALL, 3, 10),
    SURVEY("Tiksi survey", "Catalogue every species on\neach Tiksi route.", HAB_REGION_TIKSI, HAB_ZONE_NONE, ITEM_RARE_CANDY, 3, 80),
    NIGHT_WATCH("Night watch: Tiksi", "Catalogue the species that only\ncome out at night on Tiksi.", HAB_REGION_TIKSI, HAB_ZONE_NONE, ITEM_DUSK_BALL, 10, 40),
};

// Research Rank: RP needed, title, and Palm's gift on reaching it
static const u16 sResearchRankRP[] = {0, 40, 120, 240, 400};
static const u8 *const sResearchRankNames[] = {
    COMPOUND_STRING("Field Assistant"), COMPOUND_STRING("Junior Researcher"), COMPOUND_STRING("Researcher"),
    COMPOUND_STRING("Senior Researcher"), COMPOUND_STRING("Palm's Partner"),
};
static const u16 sResearchRankGifts[] = {ITEM_NONE, ITEM_RARE_CANDY, ITEM_LUCKY_EGG, ITEM_ABILITY_PATCH, ITEM_MASTER_BALL};

#undef SURVEY
#undef NIGHT_WATCH
#undef REQUEST
