#ifndef GUARD_BATTLE_BG_H
#define GUARD_BATTLE_BG_H

struct BattleBackground
{
    const void *tileset;
    const void *tilemap;
};

struct BattleBackgroundEntry
{
    const void *tileset;
    const void *tilemap;
};

void BattleInitBgsAndWindows(void);
void InitBattleBgsVideo(void);
void LoadBattleMenuWindowGfx(void);
void DrawMainBattleBackground(void);
void LoadBattleTextboxAndBackground(void);
void InitLinkBattleVsScreen(u8 taskId);
void DrawBattleEntryBackground(void);
bool8 LoadChosenBattleElement(u8 caseId);
void DrawTerrainTypeBattleBackground(void);
u8 GetBattleEnvironmentOverride(void);
u32 GetBattleEnvironmentForMapScene(u32 mapBattleScene);
bool32 IsBattleNight(void);
const u16 *GetBattleEnvironmentPalette(u32 environment);

// Debug menu overrides for the next debug battle (0 = automatic).
extern EWRAM_DATA u8 gDebugBattleEnvironment; // environment + 1
extern EWRAM_DATA u8 gDebugBattleTime;        // DEBUG_BATTLE_TIME_*
#define DEBUG_BATTLE_TIME_AUTO  0
#define DEBUG_BATTLE_TIME_DAY   1
#define DEBUG_BATTLE_TIME_NIGHT 2

#endif // GUARD_BATTLE_BG_H
