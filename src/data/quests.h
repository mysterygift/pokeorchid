// Quest data (PSF Unbound Quest Menu format, include/quests.h). Edits to quests are made here.
// Quest names live in include/constants/quests.h (QUEST_PSP_BATTERIES ...); QUEST_4 onward are PSF's numbered
// placeholders, hidden until a script unlocks them. Tray text: 2 lines of about 26 characters.

#define sub_quest(i, n, d, m, s, st, t) {.id = i, .name = n, .desc = d, .map = m, .sprite = s, .spritetype = st, .type = t}
#define side_quest(n, d, dd, m, s, st, sq, ns) {.name = n, .desc = d, .donedesc = dd, .map = m, .sprite = s, .spritetype = st, .subquests = sq, .numSubquests = ns}

static const u8 sText_TosaPort[] = _("Tosa Port");

// subquest ids are unique across all quests (bits in gSaveBlock2Ptr->subQuests)
static const struct SubQuest sSubQuests_PspBatteries[QUEST_PSP_BATTERIES_SUB_COUNT] =
{
    sub_quest(0, COMPOUND_STRING("Find the kid's dad"), COMPOUND_STRING("He left the fruit stall for\na snack and never came back."),
              sText_TosaPort, ITEM_CELL_BATTERY, ITEM, NULL),
    sub_quest(1, COMPOUND_STRING("Back to the fruit stall"), COMPOUND_STRING("Dad handed over a Cell\nBattery. Take it to the kid."),
              sText_TosaPort, ITEM_CELL_BATTERY, ITEM, NULL),
};

#define PLACEHOLDER_QUEST(n) \
    side_quest(COMPOUND_STRING("Quest " #n), COMPOUND_STRING("Description " #n), COMPOUND_STRING("Completed quest " #n), \
               COMPOUND_STRING("Map " #n), OBJ_EVENT_GFX_WALLY, OBJECT, NULL, 0)

const struct SideQuest gSideQuests[QUEST_COUNT] =
{
    [QUEST_PSP_BATTERIES] = {
        .name = COMPOUND_STRING("Flat Batteries"),
        .desc = COMPOUND_STRING("The fruit stall kid's PSP\nis dead. Find his dad!"),
        .donedesc = COMPOUND_STRING("Dad's battery was for\nPokémon. You got to keep it!"),
        .map = sText_TosaPort, .sprite = ITEM_CELL_BATTERY, .spritetype = ITEM,
        .subquests = sSubQuests_PspBatteries, .numSubquests = QUEST_PSP_BATTERIES_SUB_COUNT,
    },
    [QUEST_HEART_SCALE] = {
        .name = COMPOUND_STRING("A Scale to Remember"),
        .desc = COMPOUND_STRING("Show the old man by the\nlighthouse a Heart Scale."),
        .donedesc = COMPOUND_STRING("He proposed all over again.\nShe said yes, of course!"),
        .map = sText_TosaPort, .sprite = ITEM_HEART_SCALE, .spritetype = ITEM,
    },
    [QUEST_TASTE_OF_HOME] = {
        .name = COMPOUND_STRING("A Taste of Home"),
        .desc = COMPOUND_STRING("Bring the homesick Kalos\nartist an Old Gateau."),
        .donedesc = COMPOUND_STRING("One bite and he was back\nin Lumiose. Magnifique!"),
        .map = COMPOUND_STRING("Changu City"), .sprite = ITEM_OLD_GATEAU, .spritetype = ITEM,
    },
    [QUEST_4] = PLACEHOLDER_QUEST(4),   [QUEST_5] = PLACEHOLDER_QUEST(5),
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
