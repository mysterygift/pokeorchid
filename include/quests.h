#ifndef GUARD_QUESTS_H
#define GUARD_QUESTS_H

#include "constants/quests.h"
#include "main.h"

// sprite types (the tray's icon well)
#define OBJECT 1
#define ITEM 2
#define PKMN 3

struct SubQuest
{
    const u8 id;            // unique across all quests (bit in gSaveBlock2Ptr->subQuests)
    const u8 *name;
    const u8 *desc;
    const u8 *map;
    const u16 sprite;
    const u8 spritetype;
    const u8 *type;
};

struct SideQuest
{
    const u8 *name;
    const u8 *desc;         // active
    const u8 *donedesc;     // completed
    const u8 *map;
    const u16 sprite;
    const u8 spritetype;
    const struct SubQuest *subquests;
    const u8 numSubquests;
    const u8 *newdesc;      // Orchid: inactive ("New") hint; NULL = generic "Talk to someone in <map>"
};

enum QuestCases
{
    FLAG_GET_UNLOCKED,      // check if quest is unlocked
    FLAG_GET_INACTIVE,      // check if quest is unlocked but has no other state
    FLAG_GET_ACTIVE,        // check if quest is active
    FLAG_GET_REWARD,        // check if quest is ready for reward
    FLAG_GET_COMPLETED,     // check if quest is completed
    FLAG_GET_FAVORITE,      // check if quest is favorited
    FLAG_SET_UNLOCKED,      // mark quest as unlocked
    FLAG_SET_INACTIVE,      // mark quest as inactive
    FLAG_SET_ACTIVE,        // mark quest as active
    FLAG_SET_REWARD,        // mark quest ready for reward
    FLAG_SET_COMPLETED,     // mark completed quest
    FLAG_SET_FAVORITE,      // mark quest as a favorite
    FLAG_REMOVE_INACTIVE,   // remove inactive flag from quest
    FLAG_REMOVE_ACTIVE,     // remove active flag from quest
    FLAG_REMOVE_REWARD,     // remove reward flag from quest
    FLAG_REMOVE_FAVORITE,   // remove favorite flag from quest
};

extern const struct SideQuest gSideQuests[QUEST_COUNT];

void QuestMenu_Init(u8 a0, MainCallback callback);         // src/rotom_phone_quests.c
u8 QuestMenu_GetSetSubquestState(u8 quest, u8 caseId, u8 childQuest);
u8 QuestMenu_GetSetQuestState(u8 quest, u8 caseId);
void QuestMenu_CopyQuestName(u8 *dst, u8 questId);
void QuestMenu_CopySubquestName(u8 *dst, u8 parentId, u8 childId);
void QuestMenu_ResetMenuSaveData(void);
u32 Quests_CountInState(u8 caseId);

#endif // GUARD_QUESTS_H
