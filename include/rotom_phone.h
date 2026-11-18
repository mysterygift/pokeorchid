#ifndef GUARD_ROTOM_PHONE_H
#define GUARD_ROTOM_PHONE_H

// The Rotom Phone replaces the PokéNav (dev_scripts/orchid_ui/DESIGN.md, "Rotom Phone").
// Home screen: src/rotom_phone.c. Apps return to the home screen with CB2_ReturnToRotomPhone.

enum
{
    PHONE_APP_MAP,
    PHONE_APP_CALL,
    PHONE_APP_QUESTS,
    PHONE_APP_RADIO,
    PHONE_APP_COUNT
};

void CB2_InitRotomPhone(void);      // from the start menu (slide-up intro)
void CB2_ReturnToRotomPhone(void);  // from an app (no intro, cursor kept)

// App hooks (src/rotom_phone_apps.c): launchers set the next CB2 and return through CB2_ReturnToRotomPhone.
void PhoneApp_LaunchCall(void);
void PhoneApp_LaunchQuests(void);
void PhoneApp_LaunchRadio(void);
u32 PhoneApp_CountContacts(void);
u32 PhoneApp_CountQuestRewards(void);   // quests in the REWARD state = home-screen badge
void PhoneApp_RadioRotomText(u8 *dest);

// src/rotom_phone_call.c
void CB2_InitPhoneCall(void);
u32 PhoneCall_CountContacts(void);

#endif // GUARD_ROTOM_PHONE_H
