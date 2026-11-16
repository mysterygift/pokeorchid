#ifndef GUARD_BATTLE_MODE7_H
#define GUARD_BATTLE_MODE7_H

// Orchid: "3D" battle floor. The environment is drawn as a perspective
// (Mode 7) plane on affine BG2 in BG mode 1, with a slowly moving camera.
// Whenever something needs the classic text BG2/BG3 (move backgrounds,
// battler-on-BG2 anims, scanline effects, terrain backgrounds) the floor
// suspends back to the flat 4bpp environment, and resumes once idle.

// World layout of the floor texture (texels), shared with tools/orchid/mode7_floor.py.
#define MODE7_PLAYER_PLATFORM_U    204
#define MODE7_PLAYER_PLATFORM_V    419
#define MODE7_OPPONENT_PLATFORM_U  332
#define MODE7_OPPONENT_PLATFORM_V  259

void BattleMode7_Start(void);
void BattleMode7_StartIntro(void);
bool32 BattleMode7_IntroDone(void);
void BattleMode7_FocusOn(u32 battler);
void BattleMode7_FocusFor(u32 battler, u32 frames);
void BattleMode7_FocusAfterAnim(u32 battler, u32 frames);
void BattleMode7_ClearFocus(void);
bool32 IsBattleIntroMode7(void);
void BattleMode7_End(void);
void BattleMode7_Update(void);
void BattleMode7_VBlank(void);
void BattleMode7_Suspend(void);
void BattleMode7_SuspendForMoveBg(void);
void BattleMode7_FinishBgLoad(void);
bool32 BattleMode7_IsActive(void);

#endif // GUARD_BATTLE_MODE7_H
