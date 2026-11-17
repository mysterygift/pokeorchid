#include "global.h"
#include "test/battle.h"

// Kopi (Pokemon Orchid): a held drink. When the holder's HP is below 40% and it is awake, it drinks
// the Kopi, which raises its critical-hit ratio by two stages (Focus Energy) and uses the item up.
// It shares HOLD_EFFECT_CRITICAL_UP with the Lansat Berry but is not a Berry.

ASSUMPTIONS
{
    ASSUME(gItemsInfo[ITEM_KOPI].holdEffect == HOLD_EFFECT_CRITICAL_UP);
    ASSUME(gItemsInfo[ITEM_KOPI].holdEffectParam == 40);
    ASSUME(gItemsInfo[ITEM_KOPI].pocket != POCKET_BERRIES);
    ASSUME(GetMoveEffect(MOVE_DRAGON_RAGE) == EFFECT_FIXED_HP_DAMAGE);
    ASSUME(GetMoveFixedHPDamage(MOVE_DRAGON_RAGE) == 40);
}

SINGLE_BATTLE_TEST("Kopi is drunk when the holder's HP drops below 40%, and is used up")
{
    u32 hp;
    PARAMETRIZE { hp = 79; } // 39 HP left: below 40%
    PARAMETRIZE { hp = 80; } // 40 HP left: exactly 40%, not below
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { MaxHP(100); HP(hp); Item(ITEM_KOPI); }
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(opponent, MOVE_DRAGON_RAGE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_DRAGON_RAGE, opponent);
        if (hp == 79) {
            ANIMATION(ANIM_TYPE_GENERAL, B_ANIM_HELD_ITEM_BERRY, player);
            MESSAGE("Wobbuffet used the Kopi to get pumped!");
        } else {
            NONE_OF {
                ANIMATION(ANIM_TYPE_GENERAL, B_ANIM_HELD_ITEM_BERRY, player);
                MESSAGE("Wobbuffet used the Kopi to get pumped!");
            }
        }
    } THEN {
        if (hp == 79) {
            EXPECT_EQ(player->item, ITEM_NONE);
            EXPECT(player->volatiles.focusEnergy);
        } else {
            EXPECT_EQ(player->item, ITEM_KOPI);
            EXPECT(!player->volatiles.focusEnergy);
        }
    }
}

SINGLE_BATTLE_TEST("Kopi is not drunk at full HP when the holder enters battle")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Item(ITEM_KOPI); }
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { }
    } SCENE {
        NOT MESSAGE("Wobbuffet used the Kopi to get pumped!");
    } THEN {
        EXPECT_EQ(player->item, ITEM_KOPI);
    }
}

SINGLE_BATTLE_TEST("Kopi is not drunk while the holder is asleep")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { MaxHP(100); HP(79); Status1(STATUS1_SLEEP); Item(ITEM_KOPI); }
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(opponent, MOVE_DRAGON_RAGE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_DRAGON_RAGE, opponent);
        NOT MESSAGE("Wobbuffet used the Kopi to get pumped!");
    } THEN {
        EXPECT_EQ(player->item, ITEM_KOPI);
        EXPECT(!player->volatiles.focusEnergy);
    }
}

SINGLE_BATTLE_TEST("Kopi is drunk on switching in if the holder is already below 40% HP")
{
    GIVEN {
        PLAYER(SPECIES_WYNAUT);
        PLAYER(SPECIES_WOBBUFFET) { MaxHP(100); HP(30); Item(ITEM_KOPI); }
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { SWITCH(player, 1); }
    } SCENE {
        ANIMATION(ANIM_TYPE_GENERAL, B_ANIM_HELD_ITEM_BERRY, player);
        MESSAGE("Wobbuffet used the Kopi to get pumped!");
    } THEN {
        EXPECT_EQ(player->item, ITEM_NONE);
    }
}

SINGLE_BATTLE_TEST("Kopi raises the holder's critical-hit-ratio by 2 stages")
{
    u32 genConfig = 0, chance;
    for (u32 j = GEN_1; j <= GEN_5; j++)
        PARAMETRIZE { genConfig = j; chance = 4; } // 25%
    for (u32 j = GEN_6; j <= GEN_9; j++)
        PARAMETRIZE { genConfig = j; chance = 2; } // 50%
    PASSES_RANDOMLY(1, chance, RNG_CRITICAL_HIT);
    GIVEN {
        WITH_CONFIG(B_CRIT_CHANCE, genConfig);
        ASSUME(GetMoveCriticalHitStage(MOVE_SCRATCH) == 0);
        PLAYER(SPECIES_WOBBUFFET) { MaxHP(100); HP(79); Item(ITEM_KOPI); }
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(opponent, MOVE_DRAGON_RAGE); MOVE(player, MOVE_SCRATCH); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_DRAGON_RAGE, opponent);
        MESSAGE("Wobbuffet used the Kopi to get pumped!");
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SCRATCH, player);
        MESSAGE("A critical hit!");
    }
}

SINGLE_BATTLE_TEST("Kopi is not a Berry, so Unnerve does not stop it")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { MaxHP(100); HP(79); Item(ITEM_KOPI); }
        OPPONENT(SPECIES_JOLTIK) { Ability(ABILITY_UNNERVE); }
    } WHEN {
        TURN { MOVE(opponent, MOVE_DRAGON_RAGE); }
    } SCENE {
        MESSAGE("Wobbuffet used the Kopi to get pumped!");
    } THEN {
        EXPECT_EQ(player->item, ITEM_NONE);
    }
}
