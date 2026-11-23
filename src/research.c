// Orchid: Professor Palm's research tasks. See include/research.h.
#include "global.h"
#include "event_data.h"
#include "event_scripts.h"
#include "field_player_avatar.h"
#include "item.h"
#include "palette.h"
#include "pokedex.h"
#include "pokedex_habitats.h"
#include "quests.h"
#include "region_map.h"
#include "research.h"
#include "script.h"
#include "string_util.h"
#include "constants/items.h"
#include "constants/region_map_sections.h"
#include "constants/vars.h"

#include "data/research_tasks.h"

STATIC_ASSERT(ARRAY_COUNT(sResearchTasks) <= 32, ResearchTasksFitInClaimedBits);

static EWRAM_DATA bool8 sResearchDirty = FALSE;

bool32 Research_IsUnlocked(void)
{
    return VarGet(VAR_ORCHID_RESEARCH) >= RESEARCH_UNLOCKED;
}

u32 Research_Count(void)
{
    return ARRAY_COUNT(sResearchTasks);
}

const struct ResearchTask *Research_GetTask(u32 id)
{
    return &sResearchTasks[id];
}

// Tiksi tasks appear once Tiksi does (first landing at Furong Village)
bool32 Research_IsVisible(u32 id)
{
    if (!Research_IsUnlocked())
        return FALSE;
    if (sResearchTasks[id].region == HAB_REGION_TIKSI && !FlagGet(FLAG_VISITED_FURONG_VILLAGE))
        return FALSE;
    return TRUE;
}

static bool32 IsClaimed(u32 id)
{
    return (gSaveBlock3Ptr->researchClaimed >> id) & 1;
}

bool32 Research_IsStepDone(mapsec_u16_t mapsec)
{
    struct HabitatCounts c;

    Habitats_CountSections(&mapsec, 1, &c);
    return c.total != 0 && c.catalogued == c.total;
}

u32 Research_GetSteps(u32 id, mapsec_u16_t *out)
{
    const struct ResearchTask *t = &sResearchTasks[id];

    if (t->type != RESEARCH_SURVEY)
        return 0;
    return Habitats_GetSections(t->region, t->zone, out, RESEARCH_MAX_STEPS);
}

// survey: habitats fully catalogued / habitats; night watch: night-only species catalogued; request: 0 / 1
void Research_GetProgress(u32 id, u16 *done, u16 *total)
{
    const struct ResearchTask *t = &sResearchTasks[id];
    mapsec_u16_t secs[RESEARCH_MAX_STEPS];
    struct HabitatCounts c;
    u32 n, i;

    *done = *total = 0;
    switch (t->type)
    {
    case RESEARCH_SURVEY:
        n = Research_GetSteps(id, secs);
        *total = n;
        for (i = 0; i < n; i++)
            *done += Research_IsStepDone(secs[i]) ? 1 : 0;
        break;
    case RESEARCH_NIGHT_WATCH:
        n = Habitats_GetSections(t->region, t->zone, secs, RESEARCH_MAX_STEPS);
        Habitats_CountNightOnly(secs, n, &c);
        *done = c.catalogued;
        *total = c.total;
        break;
    default:
        *total = 1;
        *done = IsSpeciesCatalogued(SpeciesToNationalPokedexNum(t->species)) ? 1 : 0;
        break;
    }
}

static bool32 IsComplete(u32 id)
{
    u16 done, total;

    Research_GetProgress(id, &done, &total);
    return total != 0 && done >= total;
}

static bool32 IsStarted(u32 id)
{
    const struct ResearchTask *t = &sResearchTasks[id];
    u16 done, total;

    if (t->type == RESEARCH_REQUEST)
        return GetSetPokedexFlag(SpeciesToNationalPokedexNum(t->species), FLAG_GET_SEEN);
    Research_GetProgress(id, &done, &total);
    return done > 0;
}

u32 Research_GetState(u32 id)
{
    if (!Research_IsVisible(id))
        return RESEARCH_ST_LOCKED;
    if (IsClaimed(id))
        return RESEARCH_ST_DONE;
    if (IsComplete(id))
        return RESEARCH_ST_REWARD;
    if (IsStarted(id))
        return RESEARCH_ST_ACTIVE;
    return RESEARCH_ST_NEW;
}

const u8 *Research_GetLocationName(u32 id, u8 *buffer)
{
    const struct ResearchTask *t = &sResearchTasks[id];

    if (t->type == RESEARCH_REQUEST)
    {
        GetMapName(buffer, t->mapsec, 0);
        return buffer;
    }
    if (t->region == HAB_REGION_TIKSI)
        return COMPOUND_STRING("Tiksi");
    return Habitats_GetZoneName(t->zone);
}

u32 Research_GetRP(void)
{
    u32 id, rp = 0;

    for (id = 0; id < ARRAY_COUNT(sResearchTasks); id++)
    {
        if (IsClaimed(id))
            rp += sResearchTasks[id].rp;
    }
    return rp;
}

u32 Research_RankForRP(u32 rp)
{
    u32 r = 0;

    while (r + 1 < ARRAY_COUNT(sResearchRankRP) && rp >= sResearchRankRP[r + 1])
        r++;
    return r;
}

u32 Research_GetRank(void)
{
    return Research_RankForRP(Research_GetRP());
}

const u8 *Research_GetRankName(u32 rank)
{
    return sResearchRankNames[rank < ARRAY_COUNT(sResearchRankNames) ? rank : 0];
}

u16 Research_GetRankGift(u32 rank)
{
    return sResearchRankGifts[rank < ARRAY_COUNT(sResearchRankGifts) ? rank : 0];
}

// Gives the task's reward (and the rank gift if the RP crosses a rank); FALSE (nothing changes) if the bag is full
bool32 Research_Claim(u32 id)
{
    const struct ResearchTask *t = &sResearchTasks[id];
    u32 oldRank = Research_GetRank(), newRank = Research_RankForRP(Research_GetRP() + t->rp);
    u16 gift = (newRank != oldRank) ? Research_GetRankGift(newRank) : ITEM_NONE;

    // a key item the player already owns can't be given twice: skip it rather than block the claim
    if (gift != ITEM_NONE && GetItemPocket(gift) == POCKET_KEY_ITEMS && CheckBagHasItem(gift, 1))
        gift = ITEM_NONE;

    if (Research_GetState(id) != RESEARCH_ST_REWARD)
        return FALSE;
    if (t->rewardItem != ITEM_NONE && !CheckBagHasSpace(t->rewardItem, t->rewardQty))
        return FALSE;
    if (gift != ITEM_NONE && !CheckBagHasSpace(gift, 1))
        return FALSE;
    if (t->rewardItem != ITEM_NONE)
        AddBagItem(t->rewardItem, t->rewardQty);
    if (gift != ITEM_NONE)
        AddBagItem(gift, 1);
    gSaveBlock3Ptr->researchClaimed |= 1u << id;
    gSaveBlock3Ptr->researchNotified |= 1u << id;
    return TRUE;
}

// An open request for the species in this habitat (Habitats marks its well); only the habitat Palm names
bool32 Research_IsSpeciesRequested(u16 species, mapsec_u16_t mapsec)
{
    u32 id;

    for (id = 0; id < ARRAY_COUNT(sResearchTasks); id++)
    {
        const struct ResearchTask *t = &sResearchTasks[id];
        if (t->type == RESEARCH_REQUEST && t->species == species && t->mapsec == mapsec
         && Research_IsVisible(id) && !IsClaimed(id) && !IsComplete(id))
            return TRUE;
    }
    return FALSE;
}

bool32 Research_IsSectionRequested(mapsec_u16_t mapsec)
{
    u32 id;

    for (id = 0; id < ARRAY_COUNT(sResearchTasks); id++)
    {
        const struct ResearchTask *t = &sResearchTasks[id];
        if (t->type == RESEARCH_REQUEST && t->mapsec == mapsec && Research_IsVisible(id) && !IsClaimed(id) && !IsComplete(id))
            return TRUE;
    }
    return FALSE;
}

// Called when something may have finished a task (a catch); checked back on the overworld
void Research_MarkDirty(void)
{
    sResearchDirty = TRUE;
}

void Research_Update(void)
{
    u32 id;
    bool32 buzz = FALSE;   // the Rotom Phone tells the player (data/scripts/rotom_phone.inc)

    if (!sResearchDirty || ArePlayerFieldControlsLocked() || ScriptContext_IsEnabled() || gPaletteFade.active
     || !Research_IsUnlocked())
        return;
    sResearchDirty = FALSE;
    for (id = 0; id < ARRAY_COUNT(sResearchTasks); id++)
    {
        if ((gSaveBlock3Ptr->researchNotified >> id) & 1)
            continue;
        if (Research_GetState(id) == RESEARCH_ST_REWARD)
        {
            gSaveBlock3Ptr->researchNotified |= 1u << id;
            buzz = TRUE;
        }
    }
    if (buzz)
        ScriptContext_SetupScript(Rotom_EventScript_ResearchTaskDone);
}
