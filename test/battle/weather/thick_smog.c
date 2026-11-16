#include "global.h"
#include "field_weather.h"
#include "test/battle.h"
#include "constants/weather.h"

// Thick Smog is a custom weather. It is started by the overworld weather WEATHER_THICK_SMOG.
// Note: un-rigged RandomPercentage calls in tests default to success, so the poison roll always
// "hits" unless PASSES_RANDOMLY is used. That makes the immunity tests below meaningful.

SINGLE_BATTLE_TEST("Thick Smog starts from the overworld weather")
{
    gWeatherPtr->currWeather = WEATHER_THICK_SMOG;
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_GRIMER);
    } WHEN {
        TURN { }
    } SCENE {
        MESSAGE("A thick, toxic smog hangs in the air!");
        MESSAGE("The toxic smog lingers…");
    } THEN {
        gWeatherPtr->currWeather = WEATHER_NONE;
    }
}

SINGLE_BATTLE_TEST("Thick Smog has a 30% chance to poison each Pokémon at the end of the turn")
{
    PASSES_RANDOMLY(B_THICK_SMOG_POISON_CHANCE, 100, RNG_THICK_SMOG);
    gWeatherPtr->currWeather = WEATHER_THICK_SMOG;
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_GRIMER); // Poison type, so only the player's Pokémon rolls
    } WHEN {
        TURN { }
    } SCENE {
        MESSAGE("The toxic smog lingers…");
        MESSAGE("Wobbuffet was poisoned by the smog!");
        STATUS_ICON(player, poison: TRUE);
    } THEN {
        gWeatherPtr->currWeather = WEATHER_NONE;
    }
}

SINGLE_BATTLE_TEST("Thick Smog does not poison Poison- or Steel-type Pokémon")
{
    gWeatherPtr->currWeather = WEATHER_THICK_SMOG;
    GIVEN {
        PLAYER(SPECIES_SKARMORY);
        OPPONENT(SPECIES_GRIMER);
    } WHEN {
        TURN { }
    } SCENE {
        MESSAGE("The toxic smog lingers…");
        NONE_OF {
            MESSAGE("Skarmory was poisoned by the smog!");
            MESSAGE("The opposing Grimer was poisoned by the smog!");
        }
    } THEN {
        gWeatherPtr->currWeather = WEATHER_NONE;
    }
}

SINGLE_BATTLE_TEST("Thick Smog does not poison Pokémon holding Safety Goggles or with Overcoat")
{
    u32 species, item;
    enum Ability ability;
    PARAMETRIZE { species = SPECIES_WOBBUFFET; item = ITEM_SAFETY_GOGGLES; ability = ABILITY_TELEPATHY; }
    PARAMETRIZE { species = SPECIES_PINECO;    item = ITEM_NONE;           ability = ABILITY_OVERCOAT; } // Pure Bug type
    gWeatherPtr->currWeather = WEATHER_THICK_SMOG;
    GIVEN {
        PLAYER(species) { Item(item); Ability(ability); }
        OPPONENT(SPECIES_GRIMER);
    } WHEN {
        TURN { }
    } SCENE {
        MESSAGE("The toxic smog lingers…");
        NOT STATUS_ICON(player, poison: TRUE);
    } FINALLY {
        gWeatherPtr->currWeather = WEATHER_NONE;
    }
}

SINGLE_BATTLE_TEST("Thick Smog does not poison Pokémon protected by Safeguard")
{
    gWeatherPtr->currWeather = WEATHER_THICK_SMOG;
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_GRIMER);
    } WHEN {
        TURN { MOVE(player, MOVE_SAFEGUARD); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SAFEGUARD, player);
        MESSAGE("The toxic smog lingers…");
        NOT STATUS_ICON(player, poison: TRUE);
    } THEN {
        gWeatherPtr->currWeather = WEATHER_NONE;
    }
}

SINGLE_BATTLE_TEST("Thick Smog is cleared by Defog")
{
    gWeatherPtr->currWeather = WEATHER_THICK_SMOG;
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_GRIMER);
    } WHEN {
        TURN { MOVE(opponent, MOVE_DEFOG); MOVE(player, MOVE_CELEBRATE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_DEFOG, opponent);
        MESSAGE("The smog cleared.");
        NONE_OF {
            MESSAGE("The toxic smog lingers…");
            MESSAGE("Wobbuffet was poisoned by the smog!");
        }
    } THEN {
        gWeatherPtr->currWeather = WEATHER_NONE;
    }
}
