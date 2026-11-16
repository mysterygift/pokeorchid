#include "global.h"
#include "berry.h"
#include "decompress.h"
#include "graphics.h"
#include "item.h"
#include "item_menu.h"
#include "item_icon.h"
#include "item_menu_icons.h"
#include "malloc.h"
#include "menu_helpers.h"
#include "menu.h"
#include "sprite.h"
#include "window.h"
#include "util.h"
#include "trig.h"
#include "constants/items.h"
#include "data/item_menu_satchel.h"

enum {
    TAG_BAG_GFX = 100,
    TAG_ROTATING_BALL_GFX,
    TAG_ITEM_ICON,
    TAG_ITEM_ICON_ALT,
};
// Satchel bag sprites. The pocket-icon palette is shared by the ring and the scrollbar thumb.
#define TAG_SATCHEL_POCKET_ICONS 120
#define TAG_SATCHEL_RING         121
#define TAG_SATCHEL_THUMB        122
#define TAG_SATCHEL_ARROW        123
#define TAG_BERRY_CHECK_CIRCLE_GFX 10000
#define TAG_BERRY_PIC_PAL 30020

// this file's functions
static void SpriteCB_BagVisualSwitchingPockets(struct Sprite *sprite);
static void SpriteCB_ShakeBagSprite(struct Sprite *sprite);
static void SpriteCB_SatchelRing(struct Sprite *sprite);
static void SpriteCB_SatchelPocketArrow(struct Sprite *sprite);

// static const rom data
static const u8 sCherryUnused[] = INCGFX_U8("graphics/unused/cherry.png", ".4bpp");
static const u16 sCherryUnused_Pal[] = INCGFX_U16("graphics/unused/cherry.png", ".gbapal");

static const struct OamData sBagOamData =
{
    .y = 0,
    .affineMode = ST_OAM_AFFINE_NORMAL,
    .objMode = ST_OAM_OBJ_NORMAL,
    .mosaic = FALSE,
    .bpp = ST_OAM_4BPP,
    .shape = SPRITE_SHAPE(64x64),
    .x = 0,
    .matrixNum = 0,
    .size = SPRITE_SIZE(64x64),
    .tileNum = 0,
    .priority = 1,
    .paletteNum = 0,
    .affineParam = 0
};

static const union AnimCmd sSpriteAnim_Bag_Closed[] =
{
    ANIMCMD_FRAME(0, 4),
    ANIMCMD_END
};

// Satchel sheet: 6 frames of 64x64 (64 tiles each), closed first, then the pockets in pocket order.
static const union AnimCmd sSpriteAnim_Bag_Items[] =
{
    ANIMCMD_FRAME(64, 4),
    ANIMCMD_END
};

static const union AnimCmd sSpriteAnim_Bag_Pokeballs[] =
{
    ANIMCMD_FRAME(128, 4),
    ANIMCMD_END
};

static const union AnimCmd sSpriteAnim_Bag_TMsHMs[] =
{
    ANIMCMD_FRAME(192, 4),
    ANIMCMD_END
};

static const union AnimCmd sSpriteAnim_Bag_Berries[] =
{
    ANIMCMD_FRAME(256, 4),
    ANIMCMD_END
};

static const union AnimCmd sSpriteAnim_Bag_KeyItems[] =
{
    ANIMCMD_FRAME(320, 4),
    ANIMCMD_END
};

static const union AnimCmd *const sBagSpriteAnimTable[] =
{
    [POCKET_ITEMS]      = sSpriteAnim_Bag_Items,
    [POCKET_POKE_BALLS] = sSpriteAnim_Bag_Pokeballs,
    [POCKET_TM_HM]      = sSpriteAnim_Bag_TMsHMs,
    [POCKET_BERRIES]    = sSpriteAnim_Bag_Berries,
    [POCKET_KEY_ITEMS]  = sSpriteAnim_Bag_KeyItems,
    [POCKET_DUMMY]       = sSpriteAnim_Bag_Closed,
};

static const union AffineAnimCmd sSpriteAffineAnim_BagNormal[] =
{
    AFFINEANIMCMD_FRAME(256, 256, 0, 0),
    AFFINEANIMCMD_END
};

static const union AffineAnimCmd sSpriteAffineAnim_BagShake[] =
{
    AFFINEANIMCMD_FRAME(0, 0, 254, 2),
    AFFINEANIMCMD_FRAME(0, 0, 2, 4),
    AFFINEANIMCMD_FRAME(0, 0, 254, 4),
    AFFINEANIMCMD_FRAME(0, 0, 2, 2),
    AFFINEANIMCMD_END
};

enum {
    ANIM_BAG_NORMAL,
    ANIM_BAG_SHAKE,
};

static const union AffineAnimCmd *const sBagAffineAnimCmds[] =
{
    [ANIM_BAG_NORMAL] = sSpriteAffineAnim_BagNormal,
    [ANIM_BAG_SHAKE]  = sSpriteAffineAnim_BagShake
};

// The bag sprite is now the Orchid satchel (64x384, 6 frames).
const struct CompressedSpriteSheet gBagMaleSpriteSheet =
{
    gSatchelMale_Gfx, 0x3000, TAG_BAG_GFX
};

const struct CompressedSpriteSheet gBagFemaleSpriteSheet =
{
    gSatchelFemale_Gfx, 0x3000, TAG_BAG_GFX
};

const struct SpritePalette gBagMalePaletteTable =
{
    gSatchelMale_Pal, TAG_BAG_GFX
};

const struct SpritePalette gBagFemalePaletteTable =
{
    gSatchelFemale_Pal, TAG_BAG_GFX
};

static const struct SpriteTemplate sBagSpriteTemplate =
{
    .tileTag = TAG_BAG_GFX,
    .paletteTag = TAG_BAG_GFX,
    .oam = &sBagOamData,
    .anims = sBagSpriteAnimTable,
    .affineAnims = sBagAffineAnimCmds,
};

// Satchel pocket buttons: 32x32, frames 0-4 normal, 5-9 selected (pocket order).
static const struct OamData sSatchelOamData_32x32 =
{
    .affineMode = ST_OAM_AFFINE_OFF,
    .objMode = ST_OAM_OBJ_NORMAL,
    .bpp = ST_OAM_4BPP,
    .shape = SPRITE_SHAPE(32x32),
    .size = SPRITE_SIZE(32x32),
    .priority = 1,
};

static const struct OamData sSatchelOamData_8x16 =
{
    .affineMode = ST_OAM_AFFINE_OFF,
    .objMode = ST_OAM_OBJ_NORMAL,
    .bpp = ST_OAM_4BPP,
    .shape = SPRITE_SHAPE(8x16),
    .size = SPRITE_SIZE(8x16),
    .priority = 1,
};

#define POCKET_BUTTON_FRAME(n) static const union AnimCmd sSpriteAnim_PocketButton##n[] = { ANIMCMD_FRAME((n) * 16, 0), ANIMCMD_END }
POCKET_BUTTON_FRAME(0);
POCKET_BUTTON_FRAME(1);
POCKET_BUTTON_FRAME(2);
POCKET_BUTTON_FRAME(3);
POCKET_BUTTON_FRAME(4);
POCKET_BUTTON_FRAME(5);
POCKET_BUTTON_FRAME(6);
POCKET_BUTTON_FRAME(7);
POCKET_BUTTON_FRAME(8);
POCKET_BUTTON_FRAME(9);
#undef POCKET_BUTTON_FRAME

// Anim k = pocket k normal, anim k + POCKETS_COUNT = pocket k selected
static const union AnimCmd *const sSpriteAnimTable_PocketButton[] =
{
    sSpriteAnim_PocketButton0, sSpriteAnim_PocketButton1, sSpriteAnim_PocketButton2,
    sSpriteAnim_PocketButton3, sSpriteAnim_PocketButton4, sSpriteAnim_PocketButton5,
    sSpriteAnim_PocketButton6, sSpriteAnim_PocketButton7, sSpriteAnim_PocketButton8,
    sSpriteAnim_PocketButton9,
};

static const struct CompressedSpriteSheet sSpriteSheet_SatchelPocketIcons =
{
    gSatchelPocketIcons_Gfx, 32 * 320 / 2, TAG_SATCHEL_POCKET_ICONS
};

static const struct SpritePalette sSpritePal_SatchelPocketIcons =
{
    gSatchelPocketIcons_Pal, TAG_SATCHEL_POCKET_ICONS
};

static const struct SpriteSheet sSpriteSheet_SatchelRing =
{
    gSatchelRing_Gfx, 32 * 32 / 2, TAG_SATCHEL_RING
};

static const struct SpriteSheet sSpriteSheet_SatchelThumb =
{
    gSatchelThumb_Gfx, 8 * 16 / 2, TAG_SATCHEL_THUMB
};

static const struct SpriteSheet sSpriteSheet_SatchelArrow =
{
    gSatchelArrow_Gfx, 8 * 16 / 2, TAG_SATCHEL_ARROW
};

static const struct SpritePalette sSpritePal_SatchelArrow =
{
    gSatchelArrow_Pal, TAG_SATCHEL_ARROW
};

static const struct SpriteTemplate sSpriteTemplate_SatchelPocketButton =
{
    .tileTag = TAG_SATCHEL_POCKET_ICONS,
    .paletteTag = TAG_SATCHEL_POCKET_ICONS,
    .oam = &sSatchelOamData_32x32,
    .anims = sSpriteAnimTable_PocketButton,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = SpriteCallbackDummy,
};

static const struct SpriteTemplate sSpriteTemplate_SatchelRing =
{
    .tileTag = TAG_SATCHEL_RING,
    .paletteTag = TAG_SATCHEL_POCKET_ICONS,
    .oam = &sSatchelOamData_32x32,
    .anims = gDummySpriteAnimTable,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = SpriteCB_SatchelRing,
};

static const struct SpriteTemplate sSpriteTemplate_SatchelThumb =
{
    .tileTag = TAG_SATCHEL_THUMB,
    .paletteTag = TAG_SATCHEL_POCKET_ICONS,
    .oam = &sSatchelOamData_8x16,
    .anims = gDummySpriteAnimTable,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = SpriteCallbackDummy,
};

static const struct SpriteTemplate sSpriteTemplate_SatchelArrow =
{
    .tileTag = TAG_SATCHEL_ARROW,
    .paletteTag = TAG_SATCHEL_ARROW,
    .oam = &sSatchelOamData_8x16,
    .anims = gDummySpriteAnimTable,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = SpriteCB_SatchelPocketArrow,
};

static const struct OamData sBerryPicOamData =
{
    .y = 0,
    .affineMode = ST_OAM_AFFINE_OFF,
    .objMode = ST_OAM_OBJ_NORMAL,
    .mosaic = FALSE,
    .bpp = ST_OAM_4BPP,
    .shape = SPRITE_SHAPE(64x64),
    .x = 0,
    .matrixNum = 0,
    .size = SPRITE_SIZE(64x64),
    .tileNum = 0,
    .priority = 1,
    .paletteNum = 7,
    .affineParam = 0
};

static const struct OamData sBerryPicRotatingOamData =
{
    .y = 0,
    .affineMode = ST_OAM_AFFINE_DOUBLE,
    .objMode = ST_OAM_OBJ_NORMAL,
    .mosaic = FALSE,
    .bpp = ST_OAM_4BPP,
    .shape = SPRITE_SHAPE(64x64),
    .x = 0,
    .matrixNum = 0,
    .size = SPRITE_SIZE(64x64),
    .tileNum = 0,
    .priority = 0,
    .paletteNum = 7,
    .affineParam = 0
};

static const union AnimCmd sAnim_BerryPic[] =
{
    ANIMCMD_FRAME(0, 0),
    ANIMCMD_END
};

static const union AnimCmd *const sBerryPicSpriteAnimTable[] =
{
    sAnim_BerryPic
};

static const struct SpriteTemplate sBerryPicSpriteTemplate =
{
    .tileTag = TAG_NONE,
    .paletteTag = TAG_BERRY_PIC_PAL,
    .oam = &sBerryPicOamData,
    .anims = sBerryPicSpriteAnimTable,
};

static const union AffineAnimCmd sSpriteAffineAnim_BerryPicRotation1[] =
{
    AFFINEANIMCMD_FRAME(-1, -1, 253, 96),
    AFFINEANIMCMD_FRAME(0, 0, 0, 16),
    AFFINEANIMCMD_FRAME(-2, -2, 255, 64),
    AFFINEANIMCMD_FRAME(-8, 0, 0, 16),
    AFFINEANIMCMD_FRAME(0, -8, 0, 16),
    AFFINEANIMCMD_FRAME(256, 256, 0, 0),
    AFFINEANIMCMD_JUMP(0)
};

static const union AffineAnimCmd sSpriteAffineAnim_BerryPicRotation2[] =
{
    AFFINEANIMCMD_FRAME(-1, -1, 3, 96),
    AFFINEANIMCMD_FRAME(0, 0, 0, 16),
    AFFINEANIMCMD_FRAME(-2, -2, 1, 64),
    AFFINEANIMCMD_FRAME(-8, 0, 0, 16),
    AFFINEANIMCMD_FRAME(0, -8, 0, 16),
    AFFINEANIMCMD_FRAME(256, 256, 0, 0),
    AFFINEANIMCMD_JUMP(0)
};

static const union AffineAnimCmd *const sBerryPicRotatingAnimCmds[] =
{
    sSpriteAffineAnim_BerryPicRotation1,
    sSpriteAffineAnim_BerryPicRotation2
};

static const struct SpriteTemplate sBerryPicRotatingSpriteTemplate =
{
    .tileTag = TAG_NONE,
    .paletteTag = TAG_BERRY_PIC_PAL,
    .oam = &sBerryPicRotatingOamData,
    .anims = sBerryPicSpriteAnimTable,
    .affineAnims = sBerryPicRotatingAnimCmds,
};

const struct CompressedSpriteSheet gBerryCheckCircleSpriteSheet =
{
    gBerryCheckCircle_Gfx, 0x800, TAG_BERRY_CHECK_CIRCLE_GFX
};

const struct SpritePalette gBerryCheckCirclePaletteTable =
{
    gBerryCheck_Pal, TAG_BERRY_CHECK_CIRCLE_GFX
};

static const struct OamData sBerryCheckCircleOamData =
{
    .y = 0,
    .affineMode = ST_OAM_AFFINE_OFF,
    .objMode = ST_OAM_OBJ_NORMAL,
    .mosaic = FALSE,
    .bpp = ST_OAM_4BPP,
    .shape = SPRITE_SHAPE(64x64),
    .x = 0,
    .matrixNum = 0,
    .size = SPRITE_SIZE(64x64),
    .tileNum = 0,
    .priority = 1,
    .paletteNum = 0,
    .affineParam = 0
};

static const union AnimCmd sSpriteAnim_BerryCheckCircle[] =
{
    ANIMCMD_FRAME(0, 0),
    ANIMCMD_END
};

static const union AnimCmd *const sBerryCheckCircleSpriteAnimTable[] =
{
    sSpriteAnim_BerryCheckCircle
};

static const struct SpriteTemplate sBerryCheckCircleSpriteTemplate =
{
    .tileTag = TAG_BERRY_CHECK_CIRCLE_GFX,
    .paletteTag = TAG_BERRY_CHECK_CIRCLE_GFX,
    .oam = &sBerryCheckCircleOamData,
    .anims = sBerryCheckCircleSpriteAnimTable,
};

// code
void RemoveBagSprite(u8 id)
{
    u8 *spriteId = &gBagMenu->spriteIds[id];
    if (*spriteId != SPRITE_NONE)
    {
        FreeSpriteTilesByTag(id + TAG_BAG_GFX);
        FreeSpritePaletteByTag(id + TAG_BAG_GFX);
        FreeSpriteOamMatrix(&gSprites[*spriteId]);
        DestroySprite(&gSprites[*spriteId]);
        *spriteId = SPRITE_NONE;
    }
}

void AddBagVisualSprite(u8 bagPocketId)
{
    u32 i;
    u8 *spriteId = &gBagMenu->spriteIds[ITEMMENUSPRITE_BAG];

    // The satchel sits in the middle of the pocket wheel; the pocket buttons are drawn over it.
    *spriteId = CreateSprite(&sBagSpriteTemplate, SATCHEL_WHEEL_X, SATCHEL_WHEEL_Y, 2);
    SetBagVisualPocketId(bagPocketId, FALSE);

    for (i = 0; i < POCKETS_COUNT; i++)
    {
        u8 buttonId = CreateSprite(&sSpriteTemplate_SatchelPocketButton, sSatchelButtonPos[i][0], sSatchelButtonPos[i][1], 1);
        if (buttonId == MAX_SPRITES)
            buttonId = SPRITE_NONE;
        else
            StartSpriteAnim(&gSprites[buttonId], i == bagPocketId ? i + POCKETS_COUNT : i);
        gBagMenu->spriteIds[ITEMMENUSPRITE_POCKET_BUTTON + i] = buttonId;
    }
}

#define sPocketId data[0]

void SetBagVisualPocketId(u8 bagPocketId, bool8 isSwitchingPockets)
{
    struct Sprite *sprite = &gSprites[gBagMenu->spriteIds[ITEMMENUSPRITE_BAG]];
    if (isSwitchingPockets)
    {
        sprite->y2 = -5;
        sprite->callback = SpriteCB_BagVisualSwitchingPockets;
        sprite->sPocketId = bagPocketId;
        StartSpriteAnim(sprite, POCKET_DUMMY);
    }
    else
    {
        StartSpriteAnim(sprite, bagPocketId);
    }
}

static void SpriteCB_BagVisualSwitchingPockets(struct Sprite *sprite)
{
    if (sprite->y2 != 0)
    {
        sprite->y2++;
    }
    else
    {
        StartSpriteAnim(sprite, sprite->sPocketId);
        // A pocket switch also shakes the satchel (see ShakeBagSprite). Hand over to the
        // shake callback, which resets the affine anim once the shake ends (or right away).
        sprite->callback = SpriteCB_ShakeBagSprite;
    }
}

#undef sPocketId

void ShakeBagSprite(void)
{
    struct Sprite *sprite = &gSprites[gBagMenu->spriteIds[ITEMMENUSPRITE_BAG]];
    if (sprite->affineAnimEnded)
    {
        StartSpriteAffineAnim(sprite, ANIM_BAG_SHAKE);
        // Don't interrupt the pocket-switch rise; it hands over to SpriteCB_ShakeBagSprite when done.
        if (sprite->callback != SpriteCB_BagVisualSwitchingPockets)
            sprite->callback = SpriteCB_ShakeBagSprite;
    }
}

static void SpriteCB_ShakeBagSprite(struct Sprite *sprite)
{
    // Wait for shaking to end
    if (sprite->affineAnimEnded)
    {
        StartSpriteAffineAnim(sprite, ANIM_BAG_NORMAL);
        sprite->callback = SpriteCallbackDummy;
    }
}

// The satchel bag has no rotating ball; the travelling ring (StartSatchelPocketRing) replaces it.
void AddSwitchPocketRotatingBallSprite(s16 rotationDirection)
{
}

// Loads the satchel UI sprite sheets/palettes (pocket buttons, ring, scrollbar thumb, pocket arrows).
// Everything is freed by ResetSpriteData/FreeAllSpritePalettes when the bag closes.
void LoadSatchelSpriteGfx(void)
{
    LoadCompressedSpriteSheet(&sSpriteSheet_SatchelPocketIcons);
    LoadSpritePalette(&sSpritePal_SatchelPocketIcons);
    LoadSpriteSheet(&sSpriteSheet_SatchelRing);
    LoadSpriteSheet(&sSpriteSheet_SatchelThumb);
    LoadSpriteSheet(&sSpriteSheet_SatchelArrow);
    LoadSpritePalette(&sSpritePal_SatchelArrow);
}

// --- Travelling selection ring -------------------------------------------------------------

#define sRingAngle  data[0] // Current angle in degrees (0-359, 0 = +x, clockwise on screen)
#define sRingFrom   data[1]
#define sRingDelta  data[2]
#define sRingTimer  data[3]
#define sRingPocket data[4]

#define SATCHEL_RING_FRAMES 12

// Rounded RADIUS * trig / 4096 (Sin2/Cos2 return 4096 = 1.0)
static s32 SatchelRingOffset(s32 trig)
{
    s32 v = SATCHEL_BUTTON_RADIUS * trig;
    return (v >= 0) ? (v + 2048) / 4096 : (v - 2048) / 4096;
}

static void SetSatchelRingAngle(struct Sprite *sprite, s32 angle)
{
    angle %= 360;
    if (angle < 0)
        angle += 360;
    sprite->sRingAngle = angle;
    sprite->x = SATCHEL_WHEEL_X + SatchelRingOffset(Cos2(angle));
    sprite->y = SATCHEL_WHEEL_Y + SatchelRingOffset(Sin2(angle));
}

static void SetSatchelPocketButtonSelected(u8 pocket, bool8 selected)
{
    u8 spriteId = gBagMenu->spriteIds[ITEMMENUSPRITE_POCKET_BUTTON + pocket];
    if (spriteId != SPRITE_NONE)
        StartSpriteAnim(&gSprites[spriteId], selected ? pocket + POCKETS_COUNT : pocket);
}

static void SpriteCB_SatchelRing(struct Sprite *sprite)
{
    s32 t;

    if (sprite->sRingTimer < SATCHEL_RING_FRAMES)
        sprite->sRingTimer++;
    t = sprite->sRingTimer;

    // Ease-out: from + delta * t * (24 - t) / 144
    SetSatchelRingAngle(sprite, sprite->sRingFrom + sprite->sRingDelta * t * (2 * SATCHEL_RING_FRAMES - t) / (SATCHEL_RING_FRAMES * SATCHEL_RING_FRAMES));

    if (t >= SATCHEL_RING_FRAMES)
    {
        // Arrived: the button's own selected frame takes over from the ring
        SetSatchelPocketButtonSelected(sprite->sRingPocket, TRUE);
        gBagMenu->spriteIds[ITEMMENUSPRITE_POCKET_RING] = SPRITE_NONE;
        DestroySprite(sprite);
    }
}

// Sends the gold ring along the wheel from fromPocket's button (or from wherever the ring
// currently is, if it is still travelling) to toPocket's, going the way of the press
// (direction > 0 = R / right = clockwise = increasing angle).
void StartSatchelPocketRing(u8 fromPocket, u8 toPocket, s16 direction)
{
    u8 *ringId = &gBagMenu->spriteIds[ITEMMENUSPRITE_POCKET_RING];
    struct Sprite *ring;
    s32 from, delta;
    u32 i;

    for (i = 0; i < POCKETS_COUNT; i++)
        SetSatchelPocketButtonSelected(i, FALSE);

    if (*ringId == SPRITE_NONE)
    {
        u8 spriteId = CreateSprite(&sSpriteTemplate_SatchelRing, sSatchelButtonPos[fromPocket][0], sSatchelButtonPos[fromPocket][1], 0);
        if (spriteId == MAX_SPRITES)
        {
            // No sprite slot: just jump straight to the new pocket
            SetSatchelPocketButtonSelected(toPocket, TRUE);
            return;
        }
        *ringId = spriteId;
        from = sSatchelButtonAngle[fromPocket];
    }
    else
    {
        from = gSprites[*ringId].sRingAngle;
    }

    // Shortest step in the direction of the press. This also covers IsVictoryCatch()
    // skipping the Poke Ball pocket (the ring then simply travels two buttons).
    if (direction > 0)
        delta = ((sSatchelButtonAngle[toPocket] - from) % 360 + 360) % 360;
    else
        delta = -(((from - sSatchelButtonAngle[toPocket]) % 360 + 360) % 360);

    ring = &gSprites[*ringId];
    ring->sRingFrom = from;
    ring->sRingDelta = delta;
    ring->sRingTimer = 0;
    ring->sRingPocket = toPocket;
    SetSatchelRingAngle(ring, from);
}

#undef sRingAngle
#undef sRingFrom
#undef sRingDelta
#undef sRingTimer
#undef sRingPocket

// --- Scrollbar thumb ------------------------------------------------------------------------

static void SetSatchelScrollThumbPos(struct Sprite *sprite, u16 scroll, u16 maxScroll)
{
    if (scroll > maxScroll)
        scroll = maxScroll;
    // SATCHEL_TRACK_TOP is the thumb's top edge; the sprite is positioned by its centre (8x16)
    sprite->y = SATCHEL_TRACK_TOP + (SATCHEL_TRACK_SPAN * scroll) / maxScroll + 8;
}

// Only shown when the pocket scrolls (maxScroll = numItemStacks - numShownItems > 0)
void CreateSatchelScrollThumb(u16 scroll, u16 maxScroll)
{
    u8 *spriteId = &gBagMenu->spriteIds[ITEMMENUSPRITE_SCROLL_THUMB];

    if (*spriteId != SPRITE_NONE || maxScroll == 0)
        return;
    *spriteId = CreateSprite(&sSpriteTemplate_SatchelThumb, SATCHEL_TRACK_X, SATCHEL_TRACK_TOP + 8, 0);
    if (*spriteId == MAX_SPRITES)
        *spriteId = SPRITE_NONE;
    else
        SetSatchelScrollThumbPos(&gSprites[*spriteId], scroll, maxScroll);
}

void UpdateSatchelScrollThumb(u16 scroll, u16 maxScroll)
{
    u8 spriteId = gBagMenu->spriteIds[ITEMMENUSPRITE_SCROLL_THUMB];

    if (spriteId != SPRITE_NONE && maxScroll != 0)
        SetSatchelScrollThumbPos(&gSprites[spriteId], scroll, maxScroll);
}

void DestroySatchelScrollThumb(void)
{
    u8 *spriteId = &gBagMenu->spriteIds[ITEMMENUSPRITE_SCROLL_THUMB];

    if (*spriteId != SPRITE_NONE)
    {
        DestroySprite(&gSprites[*spriteId]);
        *spriteId = SPRITE_NONE;
    }
}

// --- Pocket switch arrows -------------------------------------------------------------------

#define sArrowDir   data[0] // -1 = left, 1 = right
#define sArrowTimer data[1]

// Gentle Gen 3 style bounce: x2 goes 0 -> 2 -> 0 (outwards) over 32 frames
static void SpriteCB_SatchelPocketArrow(struct Sprite *sprite)
{
    u8 phase = (sprite->sArrowTimer++) & 31;
    s16 offset = (phase < 16 ? phase : 31 - phase) * 3 / 16; // 0..2

    sprite->x2 = sprite->sArrowDir * offset;
}

void CreateSatchelPocketArrows(void)
{
    u8 *leftId = &gBagMenu->spriteIds[ITEMMENUSPRITE_POCKET_ARROW_LEFT];
    u8 *rightId = &gBagMenu->spriteIds[ITEMMENUSPRITE_POCKET_ARROW_RIGHT];

    if (*leftId == SPRITE_NONE)
    {
        *leftId = CreateSprite(&sSpriteTemplate_SatchelArrow, SATCHEL_ARROW_LEFT_X, SATCHEL_ARROW_Y, 0);
        if (*leftId == MAX_SPRITES)
            *leftId = SPRITE_NONE;
        else
            gSprites[*leftId].sArrowDir = -1;
    }
    if (*rightId == SPRITE_NONE)
    {
        *rightId = CreateSprite(&sSpriteTemplate_SatchelArrow, SATCHEL_ARROW_RIGHT_X, SATCHEL_ARROW_Y, 0);
        if (*rightId == MAX_SPRITES)
        {
            *rightId = SPRITE_NONE;
        }
        else
        {
            // The art points left; the right arrow is the same tiles flipped
            // (sprite->hFlip is XORed into the OAM flip bits by the anim code)
            gSprites[*rightId].hFlip = TRUE;
            gSprites[*rightId].oam.matrixNum |= ST_OAM_HFLIP;
            gSprites[*rightId].sArrowDir = 1;
        }
    }
}

void DestroySatchelPocketArrows(void)
{
    u32 i;

    for (i = ITEMMENUSPRITE_POCKET_ARROW_LEFT; i <= ITEMMENUSPRITE_POCKET_ARROW_RIGHT; i++)
    {
        if (gBagMenu->spriteIds[i] != SPRITE_NONE)
        {
            DestroySprite(&gSprites[gBagMenu->spriteIds[i]]);
            gBagMenu->spriteIds[i] = SPRITE_NONE;
        }
    }
}

#undef sArrowDir
#undef sArrowTimer

void AddBagItemIconSprite(enum Item itemId, u8 id)
{
    u8 *spriteId = &gBagMenu->spriteIds[id + ITEMMENUSPRITE_ITEM];
    if (*spriteId == SPRITE_NONE)
    {
        u8 iconSpriteId;

        // Either TAG_ITEM_ICON or TAG_ITEM_ICON_ALT
        FreeSpriteTilesByTag(id + TAG_ITEM_ICON);
        FreeSpritePaletteByTag(id + TAG_ITEM_ICON);
        iconSpriteId = AddItemIconSprite(id + TAG_ITEM_ICON, id + TAG_ITEM_ICON, itemId);
        if (iconSpriteId != MAX_SPRITES)
        {
            *spriteId = iconSpriteId;
            // Centred in the satchel screen's icon well
            gSprites[iconSpriteId].x2 = SATCHEL_ICON_X;
            gSprites[iconSpriteId].y2 = SATCHEL_ICON_Y;
        }
    }
}

void RemoveBagItemIconSprite(u8 id)
{
// BUG: For one frame, the item you scroll to in the Bag menu
// will have an incorrect palette and may be seen as a flicker.
#ifdef BUGFIX
    u8 *spriteId = &gBagMenu->spriteIds[ITEMMENUSPRITE_ITEM];

    if (spriteId[id ^ 1] != SPRITE_NONE)
        gSprites[spriteId[id ^ 1]].invisible = TRUE;

    if (spriteId[id] != SPRITE_NONE)
    {
        DestroySpriteAndFreeResources(&gSprites[spriteId[id]]);
        spriteId[id] = SPRITE_NONE;
    }
#else
    RemoveBagSprite(id + ITEMMENUSPRITE_ITEM);
#endif
}

void CreateItemMenuSwapLine(void)
{
    CreateSwapLineSprites(&gBagMenu->spriteIds[ITEMMENUSPRITE_SWAP_LINE], ITEMMENU_SWAP_LINE_LENGTH);
}

void SetItemMenuSwapLineInvisibility(bool8 invisible)
{
    SetSwapLineSpritesInvisibility(&gBagMenu->spriteIds[ITEMMENUSPRITE_SWAP_LINE], ITEMMENU_SWAP_LINE_LENGTH, invisible);
}

void UpdateItemMenuSwapLinePos(u8 y)
{
    UpdateSwapLineSpritesPos(&gBagMenu->spriteIds[ITEMMENUSPRITE_SWAP_LINE], ITEMMENU_SWAP_LINE_LENGTH | SWAP_LINE_HAS_MARGIN, 104, (y + 1) * 16); // List window starts at x = 104
}

static void ArrangeBerryGfx(void *src, void *dest)
{
    u8 i, j;

    memset(dest, 0, 0x800);

    // Create top margin
    dest += 0x100;

    for (i = 0; i < 6; i++)
    {
        // Create left margin
        dest += 0x20;

        // Copy one row of berry's icon
        for (j = 0; j < 6; j++)
        {
            memcpy(dest, src, 0x20);
            dest += 0x20;
            src += 0x20;
        }

        // Create right margin
        if (i != 5)
            dest += 0x20;
    }
}

#define BERRY_SPRITE_SIZE ((64*64)/2) // 0x800

struct BerryDynamicGfx
{
    ALIGNED(4) u8 gfx[BERRY_SPRITE_SIZE];
    struct SpriteFrameImage images[1];
};

static struct BerryDynamicGfx *LoadBerryGfx(u8 berryId)
{
    struct SpritePalette pal;

    pal.data = gBerries[berryId].berryPal;
    pal.tag = TAG_BERRY_PIC_PAL + berryId;
    LoadSpritePalette(&pal);
    struct BerryDynamicGfx *gfxAlloced = Alloc(sizeof(struct BerryDynamicGfx));
    void *buffer = malloc_and_decompress(gBerries[berryId].berryPic, NULL);
    ArrangeBerryGfx(buffer, gfxAlloced->gfx);
    Free(buffer);

    return gfxAlloced;
}

static u32 CreateBerrySprite(const struct SpriteTemplate *sprTemplate, u32 berryId, s32 x, s32 y)
{
    u32 spriteId;
    struct BerryDynamicGfx *dynamicGfx = LoadBerryGfx(berryId);
    struct SpriteTemplate newSprTemplate = *sprTemplate;

    newSprTemplate.paletteTag += berryId;
    newSprTemplate.images = dynamicGfx->images;

    dynamicGfx->images[0].data = dynamicGfx->gfx;
    dynamicGfx->images[0].size = BERRY_SPRITE_SIZE;
    dynamicGfx->images[0].relativeFrames = FALSE;

    spriteId = CreateSprite(&newSprTemplate, x, y, 0);
    StoreWordInTwoHalfwords((u16 *) &gSprites[spriteId].data[BERRY_ICON_GFX_PTR_DATA_ID], (u32) dynamicGfx);
    return spriteId;
}

u32 CreateBerryTagSprite(u32 id, s32 x, s32 y)
{
    return CreateBerrySprite(&sBerryPicSpriteTemplate, id, x, y);
}

// For throwing berries into the Berry Blender
u32 CreateSpinningBerrySprite(u32 berryId, s32 x, s32 y, bool32 startAffine)
{
    u32 spriteId = CreateBerrySprite(&sBerryPicRotatingSpriteTemplate, berryId, x, y);
    if (startAffine)
        StartSpriteAffineAnim(&gSprites[spriteId], 1);

    return spriteId;
}

void DestroyBerryIconSprite(u32 spriteId, u32 berryId, bool32 freePal)
{
    DestroyBerryIconSpritePtr(&gSprites[spriteId], berryId, freePal);
}

void DestroyBerryIconSpritePtr(struct Sprite *sprite, u32 berryId, bool32 freePal)
{
    u32 gfxBuffer;

    LoadWordFromTwoHalfwords((u16 *) &sprite->data[BERRY_ICON_GFX_PTR_DATA_ID], &gfxBuffer);
    Free((void *)gfxBuffer);
    DestroySprite(sprite);
    if (freePal)
        FreeBerryIconSpritePalette(berryId);
}

void FreeBerryIconSpritePalette(u32 berryId)
{
    FreeSpritePaletteByTag(TAG_BERRY_PIC_PAL + berryId);
}

u8 CreateBerryFlavorCircleSprite(s16 x)
{
    return CreateSprite(&sBerryCheckCircleSpriteTemplate, x, 116, 0);
}
