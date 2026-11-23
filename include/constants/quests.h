#ifndef GUARD_CONSTANTS_QUESTS_H
#define GUARD_CONSTANTS_QUESTS_H

// Quests (port of PokemonSanFran's Unbound Quest Menu, branch unbound-quest-menu; shown in the
// Rotom Phone's QUESTS app). Script macros: asm/macros/event.inc (startquest, completequest, ...).

// questmenu scripting command params
#define QUEST_MENU_OPEN                 0   // opens the quest menu (questId = 0)
#define QUEST_MENU_UNLOCK_QUEST         1   // questId = QUEST_X (0-indexed)
#define QUEST_MENU_SET_ACTIVE           2   // questId = QUEST_X (0-indexed)
#define QUEST_MENU_SET_REWARD           3   // questId = QUEST_X (0-indexed)
#define QUEST_MENU_COMPLETE_QUEST       4   // questId = QUEST_X (0-indexed)
#define QUEST_MENU_CHECK_UNLOCKED       5   // checks if questId has been unlocked. Returns result to gSpecialVar_Result
#define QUEST_MENU_CHECK_INACTIVE       6   // check if a questID is inactive. Returns result to gSpecialVar_Result
#define QUEST_MENU_CHECK_ACTIVE         7   // checks if questId is active. Returns result to gSpecialVar_Result
#define QUEST_MENU_CHECK_REWARD         8   // checks if questId is in Reward state. Returns result to gSpecialVar_Result
#define QUEST_MENU_CHECK_COMPLETE       9   // checks if questId has been completed. Returns result to gSpecialVar_Result
#define QUEST_MENU_BUFFER_QUEST_NAME    10  // buffers a quest name to gStringVar1

// quest number defines
#define QUEST_1          0
#define QUEST_2          1
#define QUEST_3          2
#define QUEST_4          3
#define QUEST_5          4
#define QUEST_6          5
#define QUEST_7          6
#define QUEST_8          7
#define QUEST_9          8
#define QUEST_10         9
#define QUEST_11        10
#define QUEST_12        11
#define QUEST_13        12
#define QUEST_14        13
#define QUEST_15        14
#define QUEST_16        15
#define QUEST_17        16
#define QUEST_18        17
#define QUEST_19        18
#define QUEST_20        19
#define QUEST_21        20
#define QUEST_22        21
#define QUEST_23        22
#define QUEST_24        23
#define QUEST_25        24
#define QUEST_26        25
#define QUEST_27        26
#define QUEST_28        27
#define QUEST_29        28
#define QUEST_30        29
#define QUEST_COUNT     (QUEST_30 + 1)

#define SUB_QUEST_1          0
#define SUB_QUEST_2          1
#define SUB_QUEST_3          2
#define SUB_QUEST_4          3
#define SUB_QUEST_5          4
#define SUB_QUEST_6          5
#define SUB_QUEST_7          6
#define SUB_QUEST_8          7

// Orchid quest names (src/data/quests.h). QUEST_4 onward are still numbered placeholders.
#define QUEST_GBA_BATTERIES     QUEST_1     // Tosa Port: the GBA kid's flat batteries; find his dad
#define QUEST_HEART_SCALE       QUEST_2     // Tosa Port: show the old man a Heart Scale
#define QUEST_TASTE_OF_HOME     QUEST_3     // Changu City Café: bring the Kalos expat an Old Gateau

// steps per quest that has them
#define QUEST_GBA_BATTERIES_SUB_COUNT 2
#define SUB_QUEST_COUNT (QUEST_GBA_BATTERIES_SUB_COUNT)

#define QUEST_ARRAY_COUNT (SUB_QUEST_COUNT > QUEST_COUNT ? SUB_QUEST_COUNT : QUEST_COUNT)
#endif // GUARD_CONSTANTS_QUESTS_H
