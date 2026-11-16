#include "global.h"
#include "battle.h"
#include "battle_anim.h"
#include "battle_bg.h"
#include "battle_environment.h"
#include "battle_main.h"
#include "battle_mode7.h"
#include "decompress.h"
#include "gpu_regs.h"
#include "graphics.h"
#include "malloc.h"
#include "palette.h"
#include "scanline_effect.h"
#include "sprite.h"
#include "trig.h"
#include "constants/battle.h"

#if B_MODE7_BATTLE_FLOOR

// ---------------------------------------------------------------------------
// Camera model
//
// Screen line y samples the floor at depth z = lambda * FOCAL where
// lambda = HEIGHT / (y - HORIZON) texels per pixel. The horizon sits a little
// above the top of the screen; lines deeper than MAX_DEPTH show a flat "haze"
// band instead, which hides the far-away repeats of the 512x512 texture.
// At rest the framing matches the classic 2D backgrounds (nearly orthographic,
// the opponent side ~1.14x further away); the 3D comes from the camera orbit.
// The camera orbits (yaw) around the midpoint between the two platforms.
// ---------------------------------------------------------------------------
#define M7_HORIZON      (-328)  // fitted so the rest view matches the classic
#define M7_HEIGHT       418     //   128x32 platform ellipses at (176,64) and (64,117)
#define M7_FOCAL        1470
// Texels; must stay well below the nearest repeat of a platform's outer grass
// (player platform detail reaches ~1814 deep once the 512-texel texture wraps),
// with margin for the camera orbit.
#define M7_MAX_DEPTH    1740
#define M7_HAZE_U       4       // texel in the plain column 0 of the floor: base ground colour
#define M7_HAZE_V       8
#define M7_CENTER_X     (DISPLAY_WIDTH / 2)
#define M7_REST_U       256
#define M7_REST_V       1780
#define M7_PIVOT_U      ((MODE7_PLAYER_PLATFORM_U + MODE7_OPPONENT_PLATFORM_U) / 2)
#define M7_PIVOT_V      ((MODE7_PLAYER_PLATFORM_V + MODE7_OPPONENT_PLATFORM_V) / 2)

#define M7_PLAYER_PLATFORM_Y    117 // screen y of each side's platform centre at rest
#define M7_OPPONENT_PLATFORM_Y  64

#define M7_INTRO_YAW    0x480   // ~6 degrees; eases to rest after the intro slide
#define M7_INTRO_ZOOM   236
#define M7_SWAY_YAW     0x170   // idle sway amplitude (~2 degrees)
#define M7_SWAY_ZOOM    8       // idle zoom amplitude (Q8, ~3%)
#define M7_RESUME_DELAY 6       // idle frames before leaving the flat fallback

#define M7_NUM_TILES        256 // the floor owns all of charblock 2 while active
#define M7_TILE_ADDR        BG_CHAR_ADDR(2)
#define M7_MAP_ADDR         BG_SCREEN_ADDR(26)
#define M7_MAP_SIZE         (64 * 64)
#define M7_BG2CNT           (BGCNT_PRIORITY(3) | BGCNT_CHARBASE(2) | BGCNT_256COLOR | BGCNT_SCREENBASE(26) | BGCNT_WRAP | BGCNT_AFF512x512)
#define M7_DMACNT           (((DMA_ENABLE | DMA_START_HBLANK | DMA_REPEAT | DMA_SRC_INC | DMA_DEST_RELOAD | DMA_32BIT) << 16) | 4)
#define M7_DISPCNT_MODE_MASK 0x0007

struct Mode7Line
{
    s16 pa, pb, pc, pd; // matches BG2PA..BG2PD
    s32 x, y;           // matches BG2X, BG2Y (20.8 fixed point)
};

struct Mode7Floor
{
    const u32 *tiles;
    const u8 *map;
    const u16 *palette; // 3 palettes loaded to BG palette rows 2-4
};

struct Mode7State
{
    struct Mode7Line lines[2][DISPLAY_HEIGHT + 1];
    const struct Mode7Floor *floor;
    u32 frame;
    s32 yaw;            // 0x10000 = full turn
    s32 zoom;           // Q8, 256 = rest
    u16 savedDispcnt;
    u16 savedBg2cnt;
    u8 environment;
    u8 buffer;          // lines[buffer] is being scanned out
    bool8 ready;        // lines[buffer ^ 1] holds the next frame
    bool8 suspended;    // classic flat background is showing
    bool8 pendingResume;
    u8 idleFrames;
    u8 trackedSpriteId[MAX_BATTLERS_COUNT];
    s16 appliedDx[MAX_BATTLERS_COUNT];
    s16 appliedDy[MAX_BATTLERS_COUNT];
    s16 restX[MAX_BATTLERS_COUNT];
    s16 restY[MAX_BATTLERS_COUNT];
    s16 worldU[MAX_BATTLERS_COUNT];
    s16 worldV[MAX_BATTLERS_COUNT];
};

static EWRAM_DATA struct Mode7State *sMode7 = NULL;

static const u32 sFloorTiles_TallGrass[] = INCBIN_U32("graphics/battle_environment/tall_grass/mode7_tiles.bin");
static const u8 sFloorMap_TallGrass[] = INCBIN_U8("graphics/battle_environment/tall_grass/mode7_map.bin");
static const u16 sFloorPalette_TallGrass[] = INCBIN_U16("graphics/battle_environment/tall_grass/mode7_palette.gbapal");

static const struct Mode7Floor sFloor_TallGrass =
{
    .tiles = sFloorTiles_TallGrass,
    .map = sFloorMap_TallGrass,
    .palette = sFloorPalette_TallGrass,
};

static const struct Mode7Floor *GetFloor(u32 environment)
{
    switch (environment)
    {
    default:
        // Prototype: every environment uses the lawn test floor until each
        // environment gets its own mode7_floor.png.
        return &sFloor_TallGrass;
    }
}

// Interpolated gSineTable lookup: angle 0x10000 = full turn, result Q8.
static s32 M7_Sin(u32 angle)
{
    u32 i = (angle >> 8) & 0xFF;
    s32 frac = angle & 0xFF;
    s32 a = gSineTable[i];
    s32 b = gSineTable[(i + 1) & 0xFF];
    return a + (((b - a) * frac) >> 8);
}

static s32 M7_Cos(u32 angle)
{
    return M7_Sin(angle + 0x4000);
}

static void GetCamera(s32 yaw, s32 *camU, s32 *camV, s32 *sinOut, s32 *cosOut)
{
    s32 s = M7_Sin(yaw);
    s32 c = M7_Cos(yaw);
    s32 du = M7_REST_U - M7_PIVOT_U;
    s32 dv = M7_REST_V - M7_PIVOT_V;

    *camU = (M7_PIVOT_U << 8) + c * du - s * dv; // Q8
    *camV = (M7_PIVOT_V << 8) + s * du + c * dv;
    *sinOut = s;
    *cosOut = c;
}

static void ComputeLines(struct Mode7Line *lines, s32 yaw, s32 zoom)
{
    s32 y, camU, camV, s, c;
    s32 heightQ8 = (M7_HEIGHT << 16) / zoom;
    s32 shakeX = (s16)gBattle_BG3_X; // battle anims shake BG3; reuse it as a screen-space shake
    s32 shakeY = (s16)gBattle_BG3_Y;

    GetCamera(yaw, &camU, &camV, &s, &c);
    for (y = 0; y <= DISPLAY_HEIGHT; y++)
    {
        s32 d = y + shakeY - M7_HORIZON;
        s32 lambda, pa, pc, z;

        if (d < 1)
            d = 1;
        lambda = (heightQ8 << 8) / d;       // Q16
        pa = (lambda * c) >> 16;            // Q8
        pc = (lambda * s) >> 16;
        z = (lambda * M7_FOCAL) >> 8;       // Q8 depth
        if (z > (M7_MAX_DEPTH << 8))
        {
            // Distance haze: every pixel on the line samples one flat ground texel,
            // hiding the far-away repeats of the 512x512 texture.
            lines[y].pa = lines[y].pb = lines[y].pc = lines[y].pd = 0;
            lines[y].x = M7_HAZE_U << 8;
            lines[y].y = M7_HAZE_V << 8;
            continue;
        }
        lines[y].pa = pa;
        lines[y].pb = 0;
        lines[y].pc = pc;
        lines[y].pd = 0;
        lines[y].x = camU + ((z * s) >> 8) - (M7_CENTER_X - shakeX) * pa;
        lines[y].y = camV - ((z * c) >> 8) - (M7_CENTER_X - shakeX) * pc;
    }
}

// World texel -> screen pixel for the current camera.
static void Project(s32 u, s32 v, s32 yaw, s32 zoom, s32 *sx, s32 *sy)
{
    s32 camU, camV, s, c, ru, rv, depth, lateral;
    s32 heightQ8 = (M7_HEIGHT << 16) / zoom;

    GetCamera(yaw, &camU, &camV, &s, &c);
    ru = (u << 8) - camU;
    rv = (v << 8) - camV;
    depth = (ru * s - rv * c) >> 8;     // along forward (sin, -cos)
    lateral = (ru * c + rv * s) >> 8;   // along right (cos, sin)
    if (depth < 256)
        depth = 256;
    *sx = M7_CENTER_X + (lateral * M7_FOCAL) / depth;
    *sy = M7_HORIZON + (heightQ8 * M7_FOCAL) / depth;
}

static bool32 FloorBlocked(void)
{
    return gScanlineEffect.state != 0
        || (B_TERRAIN_BG_CHANGE == TRUE && gFieldTimers.terrain != B_TERRAIN_NONE);
}

static void ForgetSpriteDeltas(struct Mode7State *m)
{
    u32 i;
    for (i = 0; i < MAX_BATTLERS_COUNT; i++)
    {
        m->trackedSpriteId[i] = MAX_SPRITES;
        m->appliedDx[i] = 0;
        m->appliedDy[i] = 0;
    }
}

static void RemoveSpriteDeltas(struct Mode7State *m)
{
    u32 i;
    for (i = 0; i < MAX_BATTLERS_COUNT; i++)
    {
        u32 id = m->trackedSpriteId[i];
        if (id < MAX_SPRITES && gSprites[id].inUse && id == gBattlerSpriteIds[i])
        {
            gSprites[id].x -= m->appliedDx[i];
            gSprites[id].y -= m->appliedDy[i];
        }
    }
    ForgetSpriteDeltas(m);
}

// Keep battler sprites standing on their (moving) platforms.
static void ApplySpriteDeltas(struct Mode7State *m)
{
    u32 i;
    for (i = 0; i < gBattlersCount && i < MAX_BATTLERS_COUNT; i++)
    {
        u32 id = gBattlerSpriteIds[i];
        s32 sx, sy, dx, dy;

        if (id >= MAX_SPRITES || !gSprites[id].inUse)
        {
            m->trackedSpriteId[i] = MAX_SPRITES;
            continue;
        }
        if (id != m->trackedSpriteId[i])
        {
            m->trackedSpriteId[i] = id;
            m->appliedDx[i] = 0;
            m->appliedDy[i] = 0;
        }
        Project(m->worldU[i], m->worldV[i], m->yaw, m->zoom, &sx, &sy);
        dx = sx - m->restX[i];
        dy = sy - m->restY[i];
        if (GetBattlerSide(i) == B_SIDE_PLAYER && dy < 0)
            dy = 0; // back sprites rely on the text box hiding their lower half
        gSprites[id].x += dx - m->appliedDx[i];
        gSprites[id].y += dy - m->appliedDy[i];
        m->appliedDx[i] = dx;
        m->appliedDy[i] = dy;
    }
}

static void UpdateCamera(struct Mode7State *m)
{
    s32 targetYaw = 0, targetZoom = 256;

    if (IsBattleInActionSelection())
    {
        // Gentle orbit while the player is choosing; back to rest for the turn
        // so animations (which use the fixed battler coordinates) line up.
        targetYaw = (M7_Sin(m->frame * 80) * M7_SWAY_YAW) >> 8;
        targetZoom = 256 + ((M7_Sin(m->frame * 53 + 0x4000) * M7_SWAY_ZOOM) >> 8);
    }
    m->yaw += (targetYaw - m->yaw) / 12;
    m->zoom += (targetZoom - m->zoom) / 12;
    if (abs(targetYaw - m->yaw) < 12)
        m->yaw = targetYaw;
    if (abs(targetZoom - m->zoom) < 12 && targetZoom == 256)
        m->zoom = targetZoom;
}

static void BeginResume(struct Mode7State *m)
{
    m->savedDispcnt = GetGpuReg(REG_OFFSET_DISPCNT);
    m->savedBg2cnt = GetGpuReg(REG_OFFSET_BG2CNT);
    LoadPalette(m->floor->palette, BG_PLTT_ID(2), 3 * PLTT_SIZE_4BPP);
    ComputeLines(m->lines[0], m->yaw, m->zoom);
    m->buffer = 0;
    m->ready = FALSE;
    m->pendingResume = TRUE; // tiles, map and registers switch in the next VBlank
}

void BattleMode7_Start(void)
{
    struct Mode7State *m;
    u32 i;

    BattleMode7_End();
    if (gBattleTypeFlags & (BATTLE_TYPE_LINK | BATTLE_TYPE_RECORDED | BATTLE_TYPE_RECORDED_LINK))
        return;

    m = AllocZeroed(sizeof(*m));
    if (m == NULL)
        return;
    sMode7 = m;
    m->environment = GetBattleEnvironmentOverride();
    m->floor = GetFloor(m->environment);
    m->suspended = TRUE;
    m->yaw = M7_INTRO_YAW;
    m->zoom = M7_INTRO_ZOOM;
    ForgetSpriteDeltas(m);

    // Place each battler on the floor where its sprite stands at rest.
    for (i = 0; i < MAX_BATTLERS_COUNT; i++)
    {
        s32 x = GetBattlerSpriteCoord(i, BATTLER_COORD_X);
        s32 y = (GetBattlerSide(i) == B_SIDE_PLAYER) ? M7_PLAYER_PLATFORM_Y : M7_OPPONENT_PLATFORM_Y;
        s32 d = y - M7_HORIZON;
        s32 sx, sy;

        m->worldU[i] = M7_REST_U + ((x - M7_CENTER_X) * M7_HEIGHT) / d;
        m->worldV[i] = M7_REST_V - (M7_HEIGHT * M7_FOCAL) / d;
        Project(m->worldU[i], m->worldV[i], 0, 256, &sx, &sy);
        m->restX[i] = sx;
        m->restY[i] = sy;
    }
}

void BattleMode7_End(void)
{
    if (sMode7 == NULL)
        return;
    if (!sMode7->suspended && gScanlineEffect.state == 0)
        DmaStop(0);
    FREE_AND_SET_NULL(sMode7);
}

bool32 BattleMode7_IsActive(void)
{
    return sMode7 != NULL && !sMode7->suspended;
}

void BattleMode7_Suspend(void)
{
    struct Mode7State *m = sMode7;
    u16 dispcnt;

    if (m == NULL)
        return;
    m->idleFrames = 0;
    if (m->suspended)
    {
        m->pendingResume = FALSE;
        return;
    }

    RemoveSpriteDeltas(m);
    if (gScanlineEffect.state == 0)
        DmaStop(0);

    // Back to the classic flat environment on BG3. Write the registers
    // immediately as well as through the buffer to avoid a frame of garbage.
    dispcnt = GetGpuReg(REG_OFFSET_DISPCNT) & ~(M7_DISPCNT_MODE_MASK | DISPCNT_BG2_ON | DISPCNT_BG3_ON);
    dispcnt |= m->savedDispcnt & (DISPCNT_BG2_ON | DISPCNT_BG3_ON);
    SetGpuReg(REG_OFFSET_DISPCNT, dispcnt);
    SetGpuReg(REG_OFFSET_BG2CNT, m->savedBg2cnt);
    REG_DISPCNT = dispcnt;
    REG_BG2CNT = m->savedBg2cnt;
    LoadPalette(gBattleEnvironmentInfo[m->environment].palette, BG_PLTT_ID(2), 3 * PLTT_SIZE_4BPP);
    DecompressDataWithHeaderVram(gBattleEnvironmentInfo[m->environment].background.tileset, (void *)BG_CHAR_ADDR(2));
    DecompressDataWithHeaderVram(gBattleEnvironmentInfo[m->environment].background.tilemap, (void *)M7_MAP_ADDR);
    m->suspended = TRUE;
    m->pendingResume = FALSE;
}

void BattleMode7_Update(void)
{
    struct Mode7State *m = sMode7;

    if (m == NULL)
        return;
    m->frame++;
    UpdateCamera(m);

    if (m->suspended)
    {
        if (m->pendingResume)
            return;
        if (gAnimScriptActive || FloorBlocked())
            m->idleFrames = 0;
        else if (++m->idleFrames >= M7_RESUME_DELAY)
            BeginResume(m);
        return;
    }

    if (FloorBlocked())
    {
        BattleMode7_Suspend();
        return;
    }

    // Something (e.g. returning from the bag/party menu) re-initialised the
    // battle video: the floor is gone, so fall back and resume cleanly.
    if ((GetGpuReg(REG_OFFSET_DISPCNT) & M7_DISPCNT_MODE_MASK) != DISPCNT_MODE_1
     || GetGpuReg(REG_OFFSET_BG2CNT) != M7_BG2CNT)
    {
        if (gScanlineEffect.state == 0)
            DmaStop(0);
        ForgetSpriteDeltas(m);
        m->suspended = TRUE;
        m->idleFrames = 0;
        return;
    }

    ComputeLines(m->lines[m->buffer ^ 1], m->yaw, m->zoom);
    m->ready = TRUE;
    ApplySpriteDeltas(m);
}

void BattleMode7_VBlank(void)
{
    struct Mode7State *m = sMode7;
    struct Mode7Line *lines;

    if (m == NULL)
        return;

    if (m->pendingResume)
    {
        CpuFastCopy(m->floor->tiles, (void *)M7_TILE_ADDR, M7_NUM_TILES * TILE_SIZE_8BPP);
        CpuFastCopy(m->floor->map, (void *)M7_MAP_ADDR, M7_MAP_SIZE);
        SetGpuReg(REG_OFFSET_BG2CNT, M7_BG2CNT);
        SetGpuReg(REG_OFFSET_DISPCNT, (GetGpuReg(REG_OFFSET_DISPCNT) & ~(M7_DISPCNT_MODE_MASK | DISPCNT_BG3_ON)) | DISPCNT_MODE_1 | DISPCNT_BG2_ON);
        m->pendingResume = FALSE;
        m->suspended = FALSE;
    }
    if (m->suspended || gScanlineEffect.state != 0)
        return;

    if (m->ready)
    {
        m->buffer ^= 1;
        m->ready = FALSE;
    }
    lines = m->lines[m->buffer];
    DmaStop(0);
    REG_BG2PA = lines[0].pa;
    REG_BG2PB = 0;
    REG_BG2PC = lines[0].pc;
    REG_BG2PD = 0;
    REG_BG2X = lines[0].x;
    REG_BG2Y = lines[0].y;
    DmaSet(0, &lines[1], (void *)REG_ADDR_BG2PA, M7_DMACNT);
}

#else // !B_MODE7_BATTLE_FLOOR

void BattleMode7_Start(void) {}
void BattleMode7_End(void) {}
void BattleMode7_Update(void) {}
void BattleMode7_VBlank(void) {}
void BattleMode7_Suspend(void) {}
bool32 BattleMode7_IsActive(void) { return FALSE; }

#endif // B_MODE7_BATTLE_FLOOR
