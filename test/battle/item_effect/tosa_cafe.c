#include "global.h"
#include "test/battle.h"

// Snacks sold at the Pokemon Centre cafe (Pokemon Orchid).

SINGLE_BATTLE_TEST("Steamed Bao heals a battler from any primary status")
{
    u16 status;
    PARAMETRIZE { status = STATUS1_SLEEP; }
    PARAMETRIZE { status = STATUS1_POISON; }
    PARAMETRIZE { status = STATUS1_BURN; }
    PARAMETRIZE { status = STATUS1_FREEZE; }
    PARAMETRIZE { status = STATUS1_PARALYSIS; }
    PARAMETRIZE { status = STATUS1_TOXIC_POISON; }
    PARAMETRIZE { status = STATUS1_FROSTBITE; }
    GIVEN {
        ASSUME(gItemsInfo[ITEM_STEAMED_BAO].battleUsage == EFFECT_ITEM_CURE_STATUS);
        PLAYER(SPECIES_WOBBUFFET) { Status1(status); }
        OPPONENT(SPECIES_WYNAUT);
    } WHEN {
        TURN { USE_ITEM(player, ITEM_STEAMED_BAO, partyIndex: 0); }
    } THEN {
        EXPECT_EQ(player->status1, STATUS1_NONE);
    }
}

SINGLE_BATTLE_TEST("Kaya Toast restores 60 HP")
{
    GIVEN {
        ASSUME(gItemsInfo[ITEM_KAYA_TOAST].battleUsage == EFFECT_ITEM_RESTORE_HP);
        PLAYER(SPECIES_WOBBUFFET) { HP(1); MaxHP(400); }
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { USE_ITEM(player, ITEM_KAYA_TOAST, partyIndex: 0); }
    } SCENE {
        HP_BAR(player, damage: -60);
    }
}
