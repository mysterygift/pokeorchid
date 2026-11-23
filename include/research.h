#ifndef GUARD_RESEARCH_H
#define GUARD_RESEARCH_H

// Orchid: Professor Palm's research tasks (src/research.c, data in src/data/research_tasks.h).
// Progress is worked out from the Pokédex (Habitats), so tasks track themselves; the save keeps the claimed
// and announced bits (SaveBlock3.researchClaimed / researchNotified). Unlocked when Palm calls after the first
// gym badge (VAR_ORCHID_RESEARCH = RESEARCH_UNLOCKED). Shown in the Rotom Phone QUESTS app's Research tab.

#define RESEARCH_LOCKED        0
#define RESEARCH_CALL_PENDING  1   // first badge won: Palm calls next time the player is outside in Timah City
#define RESEARCH_UNLOCKED      2

enum ResearchType { RESEARCH_SURVEY, RESEARCH_NIGHT_WATCH, RESEARCH_REQUEST };
// same values as the QUESTS app's tag states
enum { RESEARCH_ST_NEW, RESEARCH_ST_ACTIVE, RESEARCH_ST_REWARD, RESEARCH_ST_DONE, RESEARCH_ST_LOCKED };

struct ResearchTask
{
    const u8 *name;
    const u8 *desc;
    u8 type;
    u8 region;          // HAB_REGION_*
    u8 zone;            // HAB_ZONE_* (surveys / night watches)
    u16 species;        // requests
    mapsec_u16_t mapsec;  // requests: where Palm says to look
    u16 sprite;
    u8 spriteType;      // quests.h OBJECT / ITEM / PKMN
    u16 rewardItem;
    u8 rewardQty;
    u8 rp;
};

#define RESEARCH_MAX_STEPS 16

bool32 Research_IsUnlocked(void);
u32 Research_Count(void);
const struct ResearchTask *Research_GetTask(u32 id);
bool32 Research_IsVisible(u32 id);
u32 Research_GetState(u32 id);
void Research_GetProgress(u32 id, u16 *done, u16 *total);
u32 Research_GetSteps(u32 id, mapsec_u16_t *out);           // surveys: one step per habitat
bool32 Research_IsStepDone(mapsec_u16_t mapsec);
const u8 *Research_GetLocationName(u32 id, u8 *buffer);
bool32 Research_Claim(u32 id);                              // FALSE if the bag is full
u32 Research_GetRP(void);
u32 Research_GetRank(void);                                 // 0-4
u32 Research_RankForRP(u32 rp);
const u8 *Research_GetRankName(u32 rank);
u16 Research_GetRankGift(u32 rank);
bool32 Research_IsSpeciesRequested(u16 species, mapsec_u16_t mapsec);
bool32 Research_IsSectionRequested(mapsec_u16_t mapsec);
void Research_MarkDirty(void);
void Research_Update(void);                                 // overworld frame: Rotom buzzes on new completions

#endif // GUARD_RESEARCH_H
