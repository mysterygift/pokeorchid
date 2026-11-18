// Rotom Phone app hooks: launchers and the numbers the home screen shows.
#include "global.h"
#include "rotom_phone.h"
#include "main.h"
#include "quests.h"
#include "string_util.h"

void PhoneApp_LaunchCall(void)
{
    CB2_InitPhoneCall();
}

void PhoneApp_LaunchQuests(void)
{
    QuestMenu_Init(0, CB2_ReturnToRotomPhone);
}

void PhoneApp_LaunchRadio(void)
{
    SetMainCallback2(CB2_ReturnToRotomPhone);   // TODO: RADIO app
}

u32 PhoneApp_CountContacts(void)
{
    return PhoneCall_CountContacts();
}

u32 PhoneApp_CountQuestRewards(void)
{
    return Quests_CountInState(FLAG_GET_REWARD);
}

void PhoneApp_RadioRotomText(u8 *dest)
{
    StringCopy(dest, COMPOUND_STRING("Tune in to TOSA FM!\nNew hits every hour!"));
}
