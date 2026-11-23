// Quests: hand port of PokemonSanFran's Unbound Quest Menu (github.com/PokemonSanFran/pokeemerald,
// branch unbound-quest-menu) onto pokeemerald-expansion. Kept from PSF: the quest / subquest tables,
// the save bits (gSaveBlock2Ptr->questData / subQuests), QuestMenu_GetSet*State and the script
// commands + macros. The screen is the Rotom Phone QUESTS app (src/rotom_phone_quests.c), and
// announcements are a Rotom buzz on the field instead of PSF's message box (DESIGN.md).
#include "global.h"
#include "quests.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "graphics.h"
#include "item.h"
#include "overworld.h"
#include "palette.h"
#include "script.h"
#include "sound.h"
#include "sprite.h"
#include "string_util.h"
#include "task.h"
#include "constants/event_objects.h"
#include "constants/items.h"
#include "constants/songs.h"
#include "constants/species.h"
#include "data/quests.h"

u8 QuestMenu_GetSetSubquestState(u8 quest, u8 caseId, u8 childQuest)
{
    u8 uniqueId = gSideQuests[quest].subquests[childQuest].id;
    u8 index = uniqueId / 8; // 8 bits per byte
    u8 bit = uniqueId % 8;
    u8 mask = 1 << bit;

    switch (caseId)
    {
    case FLAG_GET_COMPLETED:
        return gSaveBlock2Ptr->subQuests[index] & mask;
    case FLAG_SET_COMPLETED:
        gSaveBlock2Ptr->subQuests[index] |= mask;
        return 1;
    }
    return -1;
}

u8 QuestMenu_GetSetQuestState(u8 quest, u8 caseId)
{
    u8 index = quest * 5 / 8;
    u8 bit = quest * 5 % 8;
    u8 mask = 0, index2 = 0, bit2 = 0, index3 = 0, bit3 = 0, mask2 = 0, mask3 = 0;

    // 0 : unlocked
    // 1 : active
    // 2 : reward
    // 3 : completed
    // 4 : favorite
    switch (caseId)
    {
    case FLAG_GET_UNLOCKED:
    case FLAG_SET_UNLOCKED:
        break;
    case FLAG_GET_INACTIVE:
    case FLAG_GET_ACTIVE:
    case FLAG_SET_ACTIVE:
    case FLAG_REMOVE_ACTIVE:
        bit += 1;
        break;
    case FLAG_GET_REWARD:
    case FLAG_SET_REWARD:
    case FLAG_REMOVE_REWARD:
        bit += 2;
        break;
    case FLAG_GET_COMPLETED:
    case FLAG_SET_COMPLETED:
        bit += 3;
        break;
    case FLAG_GET_FAVORITE:
    case FLAG_SET_FAVORITE:
    case FLAG_REMOVE_FAVORITE:
        bit += 4;
        break;
    }
    if (bit >= 8)
    {
        index += 1;
        bit %= 8;
    }
    mask = 1 << bit;

    switch (caseId)
    {
    case FLAG_GET_UNLOCKED:
        return gSaveBlock2Ptr->questData[index] & mask;
    case FLAG_SET_UNLOCKED:
        gSaveBlock2Ptr->questData[index] |= mask;
        return 1;
    case FLAG_GET_INACTIVE:
        // PSF: unlocked-or-not doesn't matter here; no active / reward / completed bit
        bit2 = bit + 1;
        bit3 = bit + 2;
        index2 = index;
        index3 = index;
        if (bit2 >= 8)
        {
            index2 += 1;
            bit2 %= 8;
        }
        if (bit3 >= 8)
        {
            index3 += 1;
            bit3 %= 8;
        }
        mask2 = 1 << bit2;
        mask3 = 1 << bit3;
        return !(gSaveBlock2Ptr->questData[index] & mask)
            && !(gSaveBlock2Ptr->questData[index2] & mask2)
            && !(gSaveBlock2Ptr->questData[index3] & mask3);
    case FLAG_GET_ACTIVE:
    case FLAG_GET_REWARD:
    case FLAG_GET_COMPLETED:
    case FLAG_GET_FAVORITE:
        return gSaveBlock2Ptr->questData[index] & mask;
    case FLAG_SET_ACTIVE:
    case FLAG_SET_REWARD:
    case FLAG_SET_COMPLETED:
    case FLAG_SET_FAVORITE:
        gSaveBlock2Ptr->questData[index] |= mask;
        return 1;
    case FLAG_REMOVE_ACTIVE:
    case FLAG_REMOVE_REWARD:
    case FLAG_REMOVE_FAVORITE:
        gSaveBlock2Ptr->questData[index] &= ~mask;
        return 1;
    }
    return -1;  // failure
}

void QuestMenu_CopyQuestName(u8 *dst, u8 questId)
{
    StringCopy(dst, gSideQuests[questId].name);
}

void QuestMenu_CopySubquestName(u8 *dst, u8 parentId, u8 childId)
{
    StringCopy(dst, gSideQuests[parentId].subquests[childId].name);
}

void QuestMenu_ResetMenuSaveData(void)
{
    memset(&gSaveBlock2Ptr->questData, 0, sizeof(gSaveBlock2Ptr->questData));
    memset(&gSaveBlock2Ptr->subQuests, 0, sizeof(gSaveBlock2Ptr->subQuests));
}

// unlocked quests whose state is caseId (FLAG_GET_INACTIVE / ACTIVE / REWARD / COMPLETED / UNLOCKED)
u32 Quests_CountInState(u8 caseId)
{
    u32 i, n = 0;
    for (i = 0; i < QUEST_COUNT; i++)
    {
        if (QuestMenu_GetSetQuestState(i, FLAG_GET_UNLOCKED) && QuestMenu_GetSetQuestState(i, caseId))
            n++;
    }
    return n;
}

// ---------------------------------------------------------------- script commands (PSF)
bool8 ScrCmd_questmenu(struct ScriptContext *ctx)
{
    u8 caseId = ScriptReadByte(ctx);
    u8 questId = VarGet(ScriptReadByte(ctx));

    Script_RequestEffects(SCREFF_V1 | SCREFF_SAVE);
    switch (caseId)
    {
    case QUEST_MENU_OPEN:
    default:
        // The quest list lives in the Rotom Phone now; scripts open it directly
        BeginNormalPaletteFade(PALETTES_ALL, 2, 16, 0, 0);
        QuestMenu_Init(0, CB2_ReturnToFieldContinueScriptPlayMapMusic);
        ScriptContext_Stop();
        return TRUE;
    case QUEST_MENU_UNLOCK_QUEST:
        QuestMenu_GetSetQuestState(questId, FLAG_SET_UNLOCKED);
        break;
    case QUEST_MENU_SET_ACTIVE:
        QuestMenu_GetSetQuestState(questId, FLAG_SET_UNLOCKED);
        QuestMenu_GetSetQuestState(questId, FLAG_SET_ACTIVE);
        break;
    case QUEST_MENU_SET_REWARD:
        QuestMenu_GetSetQuestState(questId, FLAG_SET_UNLOCKED);
        QuestMenu_GetSetQuestState(questId, FLAG_SET_REWARD);
        QuestMenu_GetSetQuestState(questId, FLAG_REMOVE_ACTIVE);
        break;
    case QUEST_MENU_COMPLETE_QUEST:
        QuestMenu_GetSetQuestState(questId, FLAG_SET_UNLOCKED);
        QuestMenu_GetSetQuestState(questId, FLAG_SET_COMPLETED);
        QuestMenu_GetSetQuestState(questId, FLAG_REMOVE_ACTIVE);
        QuestMenu_GetSetQuestState(questId, FLAG_REMOVE_REWARD);
        break;
    case QUEST_MENU_CHECK_UNLOCKED:
        gSpecialVar_Result = QuestMenu_GetSetQuestState(questId, FLAG_GET_UNLOCKED) ? TRUE : FALSE;
        break;
    case QUEST_MENU_CHECK_INACTIVE:
        gSpecialVar_Result = QuestMenu_GetSetQuestState(questId, FLAG_GET_INACTIVE) ? TRUE : FALSE;
        break;
    case QUEST_MENU_CHECK_ACTIVE:
        gSpecialVar_Result = QuestMenu_GetSetQuestState(questId, FLAG_GET_ACTIVE) ? TRUE : FALSE;
        break;
    case QUEST_MENU_CHECK_REWARD:
        gSpecialVar_Result = QuestMenu_GetSetQuestState(questId, FLAG_GET_REWARD) ? TRUE : FALSE;
        break;
    case QUEST_MENU_CHECK_COMPLETE:
        gSpecialVar_Result = QuestMenu_GetSetQuestState(questId, FLAG_GET_COMPLETED) ? TRUE : FALSE;
        break;
    case QUEST_MENU_BUFFER_QUEST_NAME:
        QuestMenu_CopyQuestName(gStringVar1, questId);
        break;
    }
    return FALSE;
}

bool8 ScrCmd_subquestmenu(struct ScriptContext *ctx)
{
    u8 caseId = ScriptReadByte(ctx);
    u8 parentId = VarGet(ScriptReadHalfword(ctx));
    u8 childId = VarGet(ScriptReadHalfword(ctx));

    Script_RequestEffects(SCREFF_V1 | SCREFF_SAVE);
    switch (caseId)
    {
    case QUEST_MENU_COMPLETE_QUEST:
        QuestMenu_GetSetSubquestState(parentId, FLAG_SET_COMPLETED, childId);
        break;
    case QUEST_MENU_CHECK_COMPLETE:
        gSpecialVar_Result = QuestMenu_GetSetSubquestState(parentId, FLAG_GET_COMPLETED, childId) ? TRUE : FALSE;
        break;
    case QUEST_MENU_BUFFER_QUEST_NAME:
        QuestMenu_CopySubquestName(gStringVar1, parentId, childId);
        break;
    }
    return FALSE;
}

bool8 ScrCmd_returnqueststate(struct ScriptContext *ctx)
{
    u8 questId = VarGet(ScriptReadByte(ctx));

    Script_RequestEffects(SCREFF_V1);
    if (QuestMenu_GetSetQuestState(questId, FLAG_GET_INACTIVE))
        gSpecialVar_Result = FLAG_GET_INACTIVE;
    else if (QuestMenu_GetSetQuestState(questId, FLAG_GET_ACTIVE))
        gSpecialVar_Result = FLAG_GET_ACTIVE;
    else if (QuestMenu_GetSetQuestState(questId, FLAG_GET_REWARD))
        gSpecialVar_Result = FLAG_GET_REWARD;
    else if (QuestMenu_GetSetQuestState(questId, FLAG_GET_COMPLETED))
        gSpecialVar_Result = FLAG_GET_COMPLETED;
    return FALSE;
}
