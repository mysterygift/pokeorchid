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
#include "pokemon.h"
#include "pokemon_animation.h"
#include "battle_util.h"
#include "random.h"
#include "scanline_effect.h"
#include "sprite.h"
#include "test_runner.h"
#include "trig.h"
#include "constants/battle.h"
#include "constants/rgb.h"

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
// The camera orbits (yaw) around the midpoint between the two platforms, and a
// lens zooms about any screen point (used for the intro and move focus).
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

#define M7_ZOOM_ONE     0x10000 // zoom is Q16
#define M7_ZOOM_CENTER_Y 90     // the idle "breathing" zoom is centred here

// Intro: the camera starts rotated and close in, then pulls back to rest.
#define M7_INTRO_FRAMES 84
#define M7_INTRO_YAW    0x1000  // 22.5 degrees
#define M7_INTRO_ZOOM   (M7_ZOOM_ONE * 165 / 100)

// Idle motion while the player chooses an action: a slight orbit around the
// centre of the battle. (Floor art avoids single-pixel detail, which would
// shimmer as the floor is resampled at new angles.)
#define M7_SWAY_YAW         0x130     // ~1.7 degrees
#define M7_SWAY_YAW_SPEED   168       // one orbit cycle every ~6.5 s
#define M7_SWAY_ZOOM        (M7_ZOOM_ONE * 2 / 100)
#define M7_SWAY_ZOOM_SPEED  110     // one breathing cycle every ~10 s

// Focus on the attacker while "X used Y!" is shown.
#define M7_FOCUS_ZOOM       (M7_ZOOM_ONE * 118 / 100)
#define M7_FOCUS_YAW        0x180
#define M7_FOCUS_BODY_Y     24      // zoom about the body, not the feet

#define M7_EASE_SHIFT       3       // ease 1/8 of the way to the target each frame
#define M7_EASE_SHIFT_FAST  2       // hurrying back to the wide shot for an animation
#define M7_RESUME_DELAY     6       // idle frames before leaving the flat fallback

#define M7_NUM_TILES        256 // the floor owns all of charblock 2 while active
#define M7_TILE_ADDR        BG_CHAR_ADDR(2)
#define M7_MAP_ADDR         BG_SCREEN_ADDR(26)
#define M7_MAP_SIZE         (64 * 64)
#define M7_BG2CNT           (BGCNT_PRIORITY(3) | BGCNT_CHARBASE(2) | BGCNT_256COLOR | BGCNT_SCREENBASE(26) | BGCNT_WRAP | BGCNT_AFF512x512)
#define M7_DMACNT           (((DMA_ENABLE | DMA_START_HBLANK | DMA_REPEAT | DMA_SRC_INC | DMA_DEST_RELOAD | DMA_32BIT) << 16) | 4)
#define M7_DISPCNT_MODE_MASK 0x0007

// Sprites kept on their platforms: battlers, plus the trainers during the intro.
#define M7_SLOT_TRAINER     MAX_BATTLERS_COUNT
#define M7_NUM_SLOTS        (MAX_BATTLERS_COUNT * 2)

struct Mode7Line
{
    s16 pa, pb, pc, pd; // matches BG2PA..BG2PD
    s32 x, y;           // matches BG2X, BG2Y (20.8 fixed point)
};

struct Mode7Camera
{
    s32 yaw;    // 0x10000 = full turn
    s32 zoom;   // Q16 lens zoom
    s32 lensX;  // Q8 screen point the zoom is centred on
    s32 lensY;
    s32 panX;   // Q8 screen-space pan
    s32 panY;
};

struct Mode7Floor
{
    const u32 *tiles;
    const u8 *map;
    const u16 *palette;         // 3 palettes loaded to BG palette rows 2-4
};

struct Mode7State
{
    struct Mode7Line lines[2][DISPLAY_HEIGHT + 1];
    const struct Mode7Floor *floor;
    struct Mode7Camera cam;
    u32 frame;
    u16 savedDispcnt;
    u16 savedBg2cnt;
    u8 environment;
    u8 buffer;          // lines[buffer] is being scanned out
    bool8 ready;        // lines[buffer ^ 1] holds the next frame
    bool8 suspended;    // classic flat background is showing
    bool8 pendingResume;
    u8 idleFrames;
    u8 introTimer;      // counts up to M7_INTRO_FRAMES while the floor is visible
    u8 focusAction;     // turn action the focus belongs to
    u8 focusBattler;
    bool8 focusActive;  // cleared when an animation launches or its timer runs out
    u16 focusTimer;     // frames left (0 = until cleared)
    u8 pendingState;    // focus queued behind an animation: 1 = await start, 2 = await end
    u8 pendingBattler;
    u8 pendingTimer;
    u16 pendingDuration;
    u8 trackedSpriteId[M7_NUM_SLOTS];
    s16 appliedDx[M7_NUM_SLOTS];
    s16 appliedDy[M7_NUM_SLOTS];
    s16 restX[MAX_BATTLERS_COUNT];
    s16 restY[MAX_BATTLERS_COUNT];
    s16 worldU[MAX_BATTLERS_COUNT];
    s16 worldV[MAX_BATTLERS_COUNT];
    u16 idleAnimTimer[MAX_BATTLERS_COUNT];
};

static EWRAM_DATA struct Mode7State *sMode7 = NULL;


static const struct Mode7Camera sRestCamera =
{
    .yaw = 0,
    .zoom = M7_ZOOM_ONE,
    .lensX = M7_CENTER_X << 8,
    .lensY = M7_ZOOM_CENTER_Y << 8,
    .panX = 0,
    .panY = 0,
};

static const u32 sFloorTiles_TallGrass[] = INCBIN_U32("graphics/battle_environment/tall_grass/mode7_tiles.bin");
static const u8 sFloorMap_TallGrass[] = INCBIN_U8("graphics/battle_environment/tall_grass/mode7_map.bin");
static const u16 sFloorPalette_TallGrass[] = INCBIN_U16("graphics/battle_environment/tall_grass/mode7_palette.gbapal");

static const struct Mode7Floor sFloor_TallGrass =
{
    .tiles = sFloorTiles_TallGrass,
    .map = sFloorMap_TallGrass,
    .palette = sFloorPalette_TallGrass,
};

// Orchid (Singapore set): floors generated by
// tools/orchid/battle_envs.py.
#include "data/battle_mode7_floors.h"

// Environments without a floor stay on the classic flat background.
static const struct Mode7Floor *GetFloor(u32 environment)
{
    switch (environment)
    {
    case BATTLE_ENVIRONMENT_GRASS:
        return &sFloor_OrchidGrass;
    case BATTLE_ENVIRONMENT_SAND:
        return &sFloor_OrchidBeach;
    case BATTLE_ENVIRONMENT_PLAIN:
        return &sFloor_OrchidVoidDeck;
    case BATTLE_ENVIRONMENT_LONG_GRASS:
        return &sFloor_TallGrass;
    default:
        return NULL;
    }
}

static bool32 BattleTypeAllowsMode7(void)
{
    return !(gBattleTypeFlags & (BATTLE_TYPE_LINK | BATTLE_TYPE_RECORDED | BATTLE_TYPE_RECORDED_LINK));
}

// Interpolated gSineTable lookup: angle 0x10000 = full turn, result Q16.
// The table is only Q8; interpolating into Q16 matters because the camera
// orbits ~1500 texels from its pivot, so 1/256 steps would jump the floor
// by several pixels at a time.
static s32 M7_Sin(u32 angle)
{
    u32 i = (angle >> 8) & 0xFF;
    s32 frac = angle & 0xFF;
    s32 a = gSineTable[i];
    s32 b = gSineTable[(i + 1) & 0xFF];
    return (a << 8) + (b - a) * frac;
}

static s32 M7_Cos(u32 angle)
{
    return M7_Sin(angle + 0x4000);
}

// NOTE: all per-frame maths is 32-bit. The GBA has no hardware divide and
// 64-bit division is a slow library call; using it per scanline halved the
// frame rate.

static void GetOrbit(const struct Mode7Camera *cam, s32 *camU, s32 *camV, s32 *sinOut, s32 *cosOut)
{
    s32 s = M7_Sin(cam->yaw);
    s32 c = M7_Cos(cam->yaw);
    s32 du = M7_REST_U - M7_PIVOT_U;
    s32 dv = M7_REST_V - M7_PIVOT_V;

    *camU = (M7_PIVOT_U << 8) + ((c * du - s * dv) >> 8); // Q8
    *camV = (M7_PIVOT_V << 8) + ((s * du + c * dv) >> 8);
    *sinOut = s;
    *cosOut = c;
}

// The lens maps a rest-camera screen point p to lens + pan + (p - lens) * zoom.
// For the floor that means scaling the focal length and moving the screen
// centre and virtual horizon accordingly.
static void GetLens(const struct Mode7Camera *cam, s32 *centerXQ8, s32 *horizonQ8, s32 *focal)
{
    s32 z12 = cam->zoom >> 4;
    *focal = (M7_FOCAL * cam->zoom) >> 16;
    *centerXQ8 = cam->lensX + cam->panX + ((((M7_CENTER_X << 8) - cam->lensX) * z12) >> 12);
    *horizonQ8 = cam->lensY + cam->panY + ((((M7_HORIZON << 8) - cam->lensY) * z12) >> 12);
}

static void ComputeLines(struct Mode7Line *lines, const struct Mode7Camera *cam)
{
    s32 y, camU, camV, s, c, centerXQ8, horizonQ8, focal, sampleX;
    s32 shakeX = (s16)gBattle_BG3_X; // battle anims shake BG3; reuse it as a screen-space shake
    s32 shakeY = (s16)gBattle_BG3_Y;

    GetOrbit(cam, &camU, &camV, &s, &c);
    GetLens(cam, &centerXQ8, &horizonQ8, &focal);
    sampleX = centerXQ8 - (shakeX << 8);
    for (y = 0; y <= DISPLAY_HEIGHT; y++)
    {
        s32 d = ((y + shakeY) << 8) - horizonQ8; // Q8
        s32 lambda, pa, pc, z;

        if (d < 256)
            d = 256;
        lambda = (M7_HEIGHT << 22) / (d >> 2);  // Q16 texels per pixel
        pa = (lambda * (c >> 8)) >> 16;         // Q8
        pc = (lambda * (s >> 8)) >> 16;
        z = (lambda * focal) >> 8;              // Q8 depth
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
        // Q12 trig on the depth term keeps slow camera motion smooth
        lines[y].x = camU + ((z * (s >> 4)) >> 12) - ((sampleX * pa) >> 8);
        lines[y].y = camV - ((z * (c >> 4)) >> 12) - ((sampleX * pc) >> 8);
    }
}

// World texel -> screen pixel for a camera. depthOut (Q8 texels) may be NULL.
static void ProjectEx(s32 u, s32 v, const struct Mode7Camera *cam, s32 *sx, s32 *sy, s32 *depthOut)
{
    s32 camU, camV, s, c, ru, rv, depth, lateral, centerXQ8, horizonQ8, focal;

    GetOrbit(cam, &camU, &camV, &s, &c);
    GetLens(cam, &centerXQ8, &horizonQ8, &focal);
    ru = (u << 8) - camU;
    rv = (v << 8) - camV;
    depth = (ru * (s >> 6) - rv * (c >> 6)) >> 10;   // along forward (sin, -cos)
    lateral = (ru * (c >> 6) + rv * (s >> 6)) >> 10; // along right (cos, sin)
    if (depth < 256)
        depth = 256;
    *sx = (centerXQ8 + ((lateral * focal) / (depth >> 8)) + 128) >> 8;   // rounded
    *sy = (horizonQ8 + ((M7_HEIGHT * focal) << 8) / (depth >> 8) + 128) >> 8;
    if (depthOut != NULL)
        *depthOut = depth;
}

static void Project(s32 u, s32 v, const struct Mode7Camera *cam, s32 *sx, s32 *sy)
{
    ProjectEx(u, v, cam, sx, sy, NULL);
}

static bool32 FloorBlocked(void)
{
    return gScanlineEffect.state != 0
        || (B_TERRAIN_BG_CHANGE == TRUE && gFieldTimers.terrain != B_TERRAIN_NONE);
}

// ---------------------------------------------------------------------------
// Battler (and intro trainer) sprites follow their platforms.
// ---------------------------------------------------------------------------
static void ForgetSpriteDeltas(struct Mode7State *m)
{
    u32 i;
    for (i = 0; i < M7_NUM_SLOTS; i++)
    {
        m->trackedSpriteId[i] = MAX_SPRITES;
        m->appliedDx[i] = 0;
        m->appliedDy[i] = 0;
    }
}

static u32 GetSlotSpriteId(struct Mode7State *m, u32 slot)
{
    u32 battler = slot % MAX_BATTLERS_COUNT;

    if (battler >= gBattlersCount)
        return MAX_SPRITES;
    if (slot < M7_SLOT_TRAINER)
        return gBattlerSpriteIds[battler];
    // Trainer pics only exist during the intro; afterwards the ids may be stale.
    if (m->introTimer >= M7_INTRO_FRAMES || gBattleStruct == NULL)
        return MAX_SPRITES;
    if (gBattleStruct->trainerSlideSpriteIds[battler] == gBattlerSpriteIds[battler])
        return MAX_SPRITES;
    return gBattleStruct->trainerSlideSpriteIds[battler];
}

static void RemoveSpriteDeltas(struct Mode7State *m)
{
    u32 i;
    for (i = 0; i < M7_NUM_SLOTS; i++)
    {
        u32 id = m->trackedSpriteId[i];
        if (id < MAX_SPRITES && gSprites[id].inUse && id == GetSlotSpriteId(m, i))
        {
            gSprites[id].x -= m->appliedDx[i];
            gSprites[id].y -= m->appliedDy[i];
        }
    }
    ForgetSpriteDeltas(m);
}

static void ApplySpriteDeltas(struct Mode7State *m)
{
    u32 slot;
    for (slot = 0; slot < M7_NUM_SLOTS; slot++)
    {
        u32 battler = slot % MAX_BATTLERS_COUNT;
        u32 id = GetSlotSpriteId(m, slot);
        s32 sx, sy, dx, dy;

        if (id >= MAX_SPRITES || !gSprites[id].inUse)
        {
            m->trackedSpriteId[slot] = MAX_SPRITES;
            continue;
        }
        if (id != m->trackedSpriteId[slot])
        {
            m->trackedSpriteId[slot] = id;
            m->appliedDx[slot] = 0;
            m->appliedDy[slot] = 0;
        }
        Project(m->worldU[battler], m->worldV[battler], &m->cam, &sx, &sy);
        dx = sx - m->restX[battler];
        dy = sy - m->restY[battler];
        if (GetBattlerSide(battler) == B_SIDE_PLAYER && dy < 0)
            dy = 0; // back sprites rely on the text box hiding their lower half
        gSprites[id].x += dx - m->appliedDx[slot];
        gSprites[id].y += dy - m->appliedDy[slot];
        m->appliedDx[slot] = dx;
        m->appliedDy[slot] = dy;
    }
}

// While the player chooses, opponent Pokemon occasionally replay their species
// front animation (the same affine squash/shake/flash used when sent out),
// without the cry.
#define M7_IDLE_ANIM_MIN    300
#define M7_IDLE_ANIM_RANGE  420

static void UpdateIdleAnims(struct Mode7State *m)
{
    u32 b;
    bool32 idle = IsBattleInActionSelection() && !gAnimScriptActive;

    for (b = 0; b < gBattlersCount && b < MAX_BATTLERS_COUNT; b++)
    {
        u32 id = gBattlerSpriteIds[b];
        struct Sprite *sprite;
        enum Species species;

        if (!idle)
        {
            m->idleAnimTimer[b] = M7_IDLE_ANIM_MIN / 2 + Random() % M7_IDLE_ANIM_RANGE;
            continue;
        }
        if (m->idleAnimTimer[b] > 0 && --m->idleAnimTimer[b] > 0)
            continue;
        m->idleAnimTimer[b] = M7_IDLE_ANIM_MIN + Random() % M7_IDLE_ANIM_RANGE;

        if (GetBattlerSide(b) != B_SIDE_OPPONENT || id >= MAX_SPRITES || !gSprites[id].inUse)
            continue;
        sprite = &gSprites[id];
        if (sprite->invisible || sprite->callback != SpriteCallbackDummy
         || gBattleSpritesDataPtr == NULL || gBattleSpritesDataPtr->battlerData[b].behindSubstitute
         || (gBattleTypeFlags & BATTLE_TYPE_GHOST))
            continue;
        species = GetBattlerVisualSpecies(b);
        if (HasTwoFramesAnimation(species))
            StartSpriteAnim(sprite, 1);
        LaunchAnimationTaskForFrontSprite(sprite, gSpeciesInfo[species].frontAnimId);
        sprite->callback = SpriteCallbackDummy_2; // the anim task restores SpriteCallbackDummy
    }
}

// ---------------------------------------------------------------------------
// Camera direction
// ---------------------------------------------------------------------------
static s32 EaseTowards(s32 value, s32 target, u32 shift, s32 snap)
{
    value += (target - value) >> shift;
    if (abs(target - value) < snap)
        value = target;
    return value;
}

// smoothstep(t) for t in Q16 [0, 1], result Q16
static s32 SmoothStep(s32 t)
{
    s32 tt = (t * (t >> 4)) >> 12;
    return ((tt >> 4) * ((3 << 16) - 2 * t)) >> 12;
}

static void UpdateCamera(struct Mode7State *m)
{
    struct Mode7Camera target = sRestCamera;
    u32 shift = M7_EASE_SHIFT;

    if (m->introTimer < M7_INTRO_FRAMES)
    {
        // Scripted fly-in from a rotated close-up; timed only while the floor shows.
        s32 e = SmoothStep((m->introTimer << 16) / M7_INTRO_FRAMES);
        m->cam = sRestCamera;
        m->cam.yaw = M7_INTRO_YAW - ((M7_INTRO_YAW * (e >> 4)) >> 12);
        m->cam.zoom = M7_INTRO_ZOOM + (((M7_ZOOM_ONE - M7_INTRO_ZOOM) * (e >> 4)) >> 12);
        if (!m->suspended)
            m->introTimer++;
        return;
    }

    if (IsBattleInActionSelection())
    {
        // Gentle orbit while the player is choosing.
        target.yaw = (M7_Sin(m->frame * M7_SWAY_YAW_SPEED) * M7_SWAY_YAW) >> 16;
        target.zoom = M7_ZOOM_ONE + ((M7_Sin(m->frame * M7_SWAY_ZOOM_SPEED + 0x4000) * M7_SWAY_ZOOM) >> 16);
        m->focusActive = FALSE;
        m->pendingState = 0;
    }
    else
    {
        // Focus on the attacker while "X used Y!" is shown, on the target when a
        // hit lands, and on a battler after its stat-change animation; back to the
        // wide shot when an animation launches, the action ends or a timer expires.
        if (m->pendingState == 1)
        {
            if (gAnimScriptActive)
                m->pendingState = 2;
            else if (++m->pendingTimer > 40)
                m->pendingState = 3; // the animation never came (animations off)
        }
        if ((m->pendingState == 2 && !gAnimScriptActive) || m->pendingState == 3)
        {
            m->focusActive = TRUE;
            m->focusBattler = m->pendingBattler;
            m->focusTimer = m->pendingDuration;
            m->focusAction = gCurrentTurnActionNumber;
            m->pendingState = 0;
        }
        if (m->focusActive && m->focusAction != gCurrentTurnActionNumber)
            m->focusActive = FALSE;
        if (m->focusActive && m->focusTimer > 0 && --m->focusTimer == 0)
            m->focusActive = FALSE;
        if (m->focusActive && m->focusBattler < MAX_BATTLERS_COUNT)
        {
            u32 b = m->focusBattler;
            target.zoom = M7_FOCUS_ZOOM;
            target.lensX = m->restX[b] << 8;
            target.lensY = (m->restY[b] - M7_FOCUS_BODY_Y) << 8;
            if (GetBattlerSide(b) == B_SIDE_OPPONENT)
            {
                target.yaw = -M7_FOCUS_YAW;
                target.panX = (M7_CENTER_X - m->restX[b]) << 6; // drift a quarter of the way to centre
            }
            else
            {
                target.yaw = M7_FOCUS_YAW;
            }
        }
    }
    if (gAnimScriptActive)
        shift = M7_EASE_SHIFT_FAST;

    m->cam.yaw = EaseTowards(m->cam.yaw, target.yaw, shift, 4);
    m->cam.zoom = EaseTowards(m->cam.zoom, target.zoom, shift, 64);
    m->cam.lensX = EaseTowards(m->cam.lensX, target.lensX, shift, 16);
    m->cam.lensY = EaseTowards(m->cam.lensY, target.lensY, shift, 16);
    m->cam.panX = EaseTowards(m->cam.panX, target.panX, shift, 16);
    m->cam.panY = EaseTowards(m->cam.panY, target.panY, shift, 16);
}

static void BeginResume(struct Mode7State *m)
{
    m->savedDispcnt = GetGpuReg(REG_OFFSET_DISPCNT);
    m->savedBg2cnt = GetGpuReg(REG_OFFSET_BG2CNT);
    LoadPalette(m->floor->palette, BG_PLTT_ID(2), 3 * PLTT_SIZE_4BPP);
    ComputeLines(m->lines[0], &m->cam);
    m->buffer = 0;
    m->ready = FALSE;
    m->pendingResume = TRUE; // tiles, map and registers switch in the next VBlank
}

bool32 IsBattleIntroMode7(void)
{
    return !B_FAST_INTRO_NO_SLIDE && !gTestRunnerHeadless
        && BattleTypeAllowsMode7()
        && !(gBattleTypeFlags & (BATTLE_TYPE_INGAME_PARTNER | BATTLE_TYPE_FRONTIER))
        && GetFloor(GetBattleEnvironmentOverride()) != NULL;
}

void BattleMode7_Start(void)
{
    struct Mode7State *m;
    u32 i;

    if (sMode7 != NULL)
        return; // already running (started by the Mode 7 intro)
    if (!BattleTypeAllowsMode7() || GetFloor(GetBattleEnvironmentOverride()) == NULL)
        return;

    m = AllocZeroed(sizeof(*m));
    if (m == NULL)
        return;
    sMode7 = m;
    m->environment = GetBattleEnvironmentOverride();
    m->floor = GetFloor(m->environment);
    m->suspended = TRUE;
    m->cam = sRestCamera;
    m->introTimer = M7_INTRO_FRAMES; // no fly-in unless BattleMode7_StartIntro
    m->focusActive = FALSE;
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
        Project(m->worldU[i], m->worldV[i], &sRestCamera, &sx, &sy);
        m->restX[i] = sx;
        m->restY[i] = sy;
        m->idleAnimTimer[i] = M7_IDLE_ANIM_MIN;
    }
}

void BattleMode7_StartIntro(void)
{
    BattleMode7_Start();
    if (sMode7 == NULL)
        return;
    sMode7->introTimer = 0;
    sMode7->idleFrames = M7_RESUME_DELAY - 1; // show the floor as soon as nothing blocks it
    UpdateCamera(sMode7);
}

// Focus until the next animation launches or the action ends.
void BattleMode7_FocusOn(u32 battler)
{
    BattleMode7_FocusFor(battler, 0);
}

// Focus for a number of frames (0 = until cleared).
void BattleMode7_FocusFor(u32 battler, u32 frames)
{
    if (sMode7 == NULL || battler >= MAX_BATTLERS_COUNT)
        return;
    sMode7->focusActive = TRUE;
    sMode7->focusBattler = battler;
    sMode7->focusTimer = frames;
    sMode7->focusAction = gCurrentTurnActionNumber;
}

// Focus once the battle animation queued for this battler has played
// (animations draw at the rest coordinates, so the camera must be wide).
void BattleMode7_FocusAfterAnim(u32 battler, u32 frames)
{
    if (sMode7 == NULL || battler >= MAX_BATTLERS_COUNT)
        return;
    sMode7->pendingState = 1;
    sMode7->pendingBattler = battler;
    sMode7->pendingTimer = 0;
    sMode7->pendingDuration = frames;
}

void BattleMode7_ClearFocus(void)
{
    if (sMode7 != NULL)
        sMode7->focusActive = FALSE;
}

bool32 BattleMode7_IntroDone(void)
{
    return sMode7 == NULL || sMode7->introTimer >= M7_INTRO_FRAMES;
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

static void SuspendInternal(bool32 restoreClassicGfx);

void BattleMode7_Suspend(void)
{
    SuspendInternal(TRUE);
}

// A move background is about to be loaded into BG3 (after the screen has been
// faded for it), so only switch display modes: restoring the classic tiles and
// palette here would un-fade the screen while the new background loads.
void BattleMode7_SuspendForMoveBg(void)
{
    SuspendInternal(FALSE);
}

static u16 GetClassicDispcnt(struct Mode7State *m)
{
    u16 dispcnt = GetGpuReg(REG_OFFSET_DISPCNT) & ~(M7_DISPCNT_MODE_MASK | DISPCNT_BG2_ON | DISPCNT_BG3_ON);
    return dispcnt | (m->savedDispcnt & (DISPCNT_BG2_ON | DISPCNT_BG3_ON));
}

// Leaving the floor must never display half-loaded VRAM: charblock 2 and
// screenblock 26 hold the 8bpp floor, which reads as garbage on a text BG3.
// So both BG layers are hidden at once (the backdrop briefly takes the floor's
// ground colour), the classic or move background is loaded, and BG3 is only
// shown again from the VBlank after loading has finished. (Staging the
// classic background in RAM instead would run the battle heap out of memory.)
static void SuspendInternal(bool32 restoreClassicGfx)
{
    struct Mode7State *m = sMode7;
    const struct BattleEnvironment *env;
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
    m->suspended = TRUE;
    m->pendingResume = FALSE;
    dispcnt = GetClassicDispcnt(m);
    env = &gBattleEnvironmentInfo[m->environment];

    if (gScanlineEffect.state == 0)
        DmaStop(0);
    // Hide both layers now and in the register buffer (a VBlank may land mid-load).
    REG_DISPCNT = dispcnt & ~(DISPCNT_BG2_ON | DISPCNT_BG3_ON);
    SetGpuReg(REG_OFFSET_DISPCNT, dispcnt & ~(DISPCNT_BG2_ON | DISPCNT_BG3_ON));
    SetGpuReg(REG_OFFSET_BG2CNT, m->savedBg2cnt);
    {
        // Placeholder for the frame(s) while BG3 loads: the floor's ground colour
        // when the classic floor comes straight back, black before a move
        // background (those cut to black and fade the new background in).
        u16 placeholder = restoreClassicGfx ? m->floor->palette[1] : RGB_BLACK;
        *(vu16 *)BG_PLTT = placeholder;
        gPlttBufferFaded[0] = placeholder;
    }

    if (restoreClassicGfx)
    {
        if (m->floor->palette != env->palette)
            LoadPalette(env->palette, BG_PLTT_ID(2), 3 * PLTT_SIZE_4BPP);
        DecompressDataWithHeaderVram(env->background.tileset, (void *)BG_CHAR_ADDR(2));
        DecompressDataWithHeaderVram(env->background.tilemap, (void *)M7_MAP_ADDR);
        BattleMode7_FinishBgLoad();
    }
    // otherwise LoadMoveBg loads the move background and calls BattleMode7_FinishBgLoad
}

// The background for BG3 is fully in VRAM: show it from the next VBlank.
void BattleMode7_FinishBgLoad(void)
{
    struct Mode7State *m = sMode7;

    if (m == NULL || !m->suspended)
        return;
    gPlttBufferFaded[0] = gPlttBufferUnfaded[0];
    SetGpuReg(REG_OFFSET_DISPCNT, GetClassicDispcnt(m));
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

    ComputeLines(m->lines[m->buffer ^ 1], &m->cam);
    m->ready = TRUE;
    ApplySpriteDeltas(m);
    UpdateIdleAnims(m);
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
void BattleMode7_StartIntro(void) {}
void BattleMode7_FocusOn(u32 battler) {}
void BattleMode7_FocusFor(u32 battler, u32 frames) {}
void BattleMode7_FocusAfterAnim(u32 battler, u32 frames) {}
void BattleMode7_ClearFocus(void) {}
bool32 BattleMode7_IntroDone(void) { return TRUE; }
bool32 IsBattleIntroMode7(void) { return FALSE; }
void BattleMode7_End(void) {}
void BattleMode7_Update(void) {}
void BattleMode7_VBlank(void) {}
void BattleMode7_Suspend(void) {}
void BattleMode7_SuspendForMoveBg(void) {}
void BattleMode7_FinishBgLoad(void) {}
bool32 BattleMode7_IsActive(void) { return FALSE; }

#endif // B_MODE7_BATTLE_FLOOR
