// Rotom Phone app hooks: launchers and the numbers the home screen shows.
#include "global.h"
#include "rotom_phone.h"
#include "main.h"
#include "string_util.h"

void PhoneApp_LaunchCall(void)
{
    SetMainCallback2(CB2_ReturnToRotomPhone);   // TODO: CALL app
}

void PhoneApp_LaunchQuests(void)
{
    SetMainCallback2(CB2_ReturnToRotomPhone);   // TODO: QUESTS app
}

void PhoneApp_LaunchRadio(void)
{
    SetMainCallback2(CB2_ReturnToRotomPhone);   // TODO: RADIO app
}

u32 PhoneApp_CountContacts(void)
{
    return 0;
}

u32 PhoneApp_CountQuestRewards(void)
{
    return 0;
}

void PhoneApp_RadioRotomText(u8 *dest)
{
    StringCopy(dest, COMPOUND_STRING("Tune in to TOSA FM!\nNew hits every hour!"));
}
