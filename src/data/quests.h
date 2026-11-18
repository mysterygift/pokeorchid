// Quest data (PSF Unbound Quest Menu format, include/quests.h). Edits to quests are made here.
// PLACEHOLDER CONTENT: quests 1-5 are the Tosa samples from the approved mockup (mock_quests.py) so the
// app has something to show; the rest are PSF's numbered placeholders. Real quests are written on dev.

#define sub_quest(i, n, d, m, s, st, t) {.id = i, .name = n, .desc = d, .map = m, .sprite = s, .spritetype = st, .type = t}
#define side_quest(n, d, dd, m, s, st, sq, ns) {.name = n, .desc = d, .donedesc = dd, .map = m, .sprite = s, .spritetype = st, .subquests = sq, .numSubquests = ns}

static const u8 sText_TosaPort[] = _("Tosa Port");
static const u8 sText_TelokTown[] = _("Telok Town");

static const struct SubQuest sSubQuests1[QUEST_1_SUB_COUNT] =
{
    sub_quest(0, COMPOUND_STRING("Cup by the ferry gate"), COMPOUND_STRING("Found behind the ticket\nbooth. One down!"),
              sText_TosaPort, ITEM_SOOTHE_BELL, ITEM, NULL),
    sub_quest(1, COMPOUND_STRING("Cup in the fish market"), COMPOUND_STRING("The fishmonger was using\nit as a scoop!"),
              sText_TosaPort, ITEM_SOOTHE_BELL, ITEM, NULL),
    sub_quest(2, COMPOUND_STRING("Cup on the rail bridge"), COMPOUND_STRING("Kopi uncle says he heard\nclinking under the rail bridge."),
              COMPOUND_STRING("Reserve"), ITEM_SOOTHE_BELL, ITEM, NULL),
    sub_quest(3, COMPOUND_STRING("Cup at the hawker stall"), COMPOUND_STRING("Someone left it by the\nchicken rice stall."),
              sText_TelokTown, ITEM_SOOTHE_BELL, ITEM, NULL),
    sub_quest(4, COMPOUND_STRING("Cup on the pier"), COMPOUND_STRING("The last cup, rolling\nabout on the pier!"),
              COMPOUND_STRING("Tosa Pier"), ITEM_SOOTHE_BELL, ITEM, NULL),
};

static const struct SubQuest sSubQuests2[QUEST_2_SUB_COUNT] =
{
    sub_quest(5, COMPOUND_STRING("First Torpesquid"), COMPOUND_STRING("One down. The fishers\ncheered from the jetty."),
              COMPOUND_STRING("Tosa Pier"), SPECIES_TORPESQUID, PKMN, NULL),
    sub_quest(6, COMPOUND_STRING("Second Torpesquid"), COMPOUND_STRING("Another one tangled in\nthe nets after dark."),
              COMPOUND_STRING("Tosa Pier"), SPECIES_TORPESQUID, PKMN, NULL),
    sub_quest(7, COMPOUND_STRING("Third Torpesquid"), COMPOUND_STRING("The biggest one lurks at\nthe end of the pier."),
              COMPOUND_STRING("Tosa Pier"), SPECIES_TORPESQUID, PKMN, NULL),
};

#define PLACEHOLDER_QUEST(n) \
    side_quest(COMPOUND_STRING("Quest " #n), COMPOUND_STRING("Description " #n), COMPOUND_STRING("Completed quest " #n), \
               COMPOUND_STRING("Map " #n), OBJ_EVENT_GFX_WALLY, OBJECT, NULL, 0)

const struct SideQuest gSideQuests[QUEST_COUNT] =
{
    [QUEST_1] = {
        .name = COMPOUND_STRING("Lost Kopi Cups"),
        .desc = COMPOUND_STRING("The kopi uncle lost his cups\naround the harbour. Find 5!"),
        .donedesc = COMPOUND_STRING("All five cups are back.\nKopi's on the house!"),
        .map = sText_TosaPort, .sprite = ITEM_SOOTHE_BELL, .spritetype = ITEM,
        .subquests = sSubQuests1, .numSubquests = QUEST_1_SUB_COUNT,
    },
    [QUEST_2] = {
        .name = COMPOUND_STRING("Hawker's Recipe"),
        .desc = COMPOUND_STRING("Find the stall owner's\nmissing recipe card."),
        .donedesc = COMPOUND_STRING("The recipe is safe. The\nlaksa tastes right again!"),
        .map = COMPOUND_STRING("Hawker Centre"), .sprite = ITEM_LETTER, .spritetype = ITEM,
    },
    [QUEST_3] = {
        .name = COMPOUND_STRING("Squid on the Pier"),
        .desc = COMPOUND_STRING("Torpesquid keep tangling the\nnets. Battle 3 at night."),
        .donedesc = COMPOUND_STRING("The nets are clear and the\nfishers are happy."),
        .map = COMPOUND_STRING("Tosa Pier"), .sprite = SPECIES_TORPESQUID, .spritetype = PKMN,
        .subquests = sSubQuests2, .numSubquests = QUEST_2_SUB_COUNT,
    },
    [QUEST_4] = {
        .name = COMPOUND_STRING("Ferry Timetable"),
        .desc = COMPOUND_STRING("Deliver the new timetable\nto the ferry office."),
        .donedesc = COMPOUND_STRING("You delivered the new\ntimetable. Ferries run on time!"),
        .map = sText_TosaPort, .sprite = ITEM_TOWN_MAP, .spritetype = ITEM,
    },
    [QUEST_5] = {
        .name = COMPOUND_STRING("Old Sea Chart"),
        .desc = COMPOUND_STRING("The old sailor's chart shows\nan island nobody has seen."),
        .donedesc = COMPOUND_STRING("The island was real after\nall!"),
        .map = sText_TelokTown, .sprite = ITEM_OLD_SEA_MAP, .spritetype = ITEM,
        .newdesc = COMPOUND_STRING("Talk to the old sailor in\nTelok Town to begin."),
    },
    [QUEST_6] = PLACEHOLDER_QUEST(6),   [QUEST_7] = PLACEHOLDER_QUEST(7),   [QUEST_8] = PLACEHOLDER_QUEST(8),
    [QUEST_9] = PLACEHOLDER_QUEST(9),   [QUEST_10] = PLACEHOLDER_QUEST(10), [QUEST_11] = PLACEHOLDER_QUEST(11),
    [QUEST_12] = PLACEHOLDER_QUEST(12), [QUEST_13] = PLACEHOLDER_QUEST(13), [QUEST_14] = PLACEHOLDER_QUEST(14),
    [QUEST_15] = PLACEHOLDER_QUEST(15), [QUEST_16] = PLACEHOLDER_QUEST(16), [QUEST_17] = PLACEHOLDER_QUEST(17),
    [QUEST_18] = PLACEHOLDER_QUEST(18), [QUEST_19] = PLACEHOLDER_QUEST(19), [QUEST_20] = PLACEHOLDER_QUEST(20),
    [QUEST_21] = PLACEHOLDER_QUEST(21), [QUEST_22] = PLACEHOLDER_QUEST(22), [QUEST_23] = PLACEHOLDER_QUEST(23),
    [QUEST_24] = PLACEHOLDER_QUEST(24), [QUEST_25] = PLACEHOLDER_QUEST(25), [QUEST_26] = PLACEHOLDER_QUEST(26),
    [QUEST_27] = PLACEHOLDER_QUEST(27), [QUEST_28] = PLACEHOLDER_QUEST(28), [QUEST_29] = PLACEHOLDER_QUEST(29),
    [QUEST_30] = PLACEHOLDER_QUEST(30),
};
