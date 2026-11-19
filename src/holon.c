#include "global.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_weather.h"
#include "fieldmap.h"
#include "holon.h"
#include "palette.h"
#include "script.h"
#include "sprite.h"
#include "tilesets.h"
#include "constants/event_objects.h"
#include "constants/field_effects.h"
#include "constants/flags.h"
#include "constants/holon.h"

// Orchid Holon (Wavebreak Voyages).
//
// Field effects: the Holon outdoor maps draw their greens desaturated (gTileset_General_Holon + gTileset_Holon),
// so grass rustles, long grass, footprints, etc. load desaturated copies of the two general field-effect OBJ
// palettes there. Same tags, so everything that looks a palette up by tag keeps working.
static const u16 sFieldEffectPal_Holon0[] = INCGFX_U16("graphics/field_effects/palettes/general_0_holon.pal", ".gbapal");
static const u16 sFieldEffectPal_Holon1[] = INCGFX_U16("graphics/field_effects/palettes/general_1_holon.pal", ".gbapal");
static const struct SpritePalette sSpritePalette_HolonFieldEffect0 = {sFieldEffectPal_Holon0, FLDEFF_PAL_TAG_GENERAL_0};
static const struct SpritePalette sSpritePalette_HolonFieldEffect1 = {sFieldEffectPal_Holon1, FLDEFF_PAL_TAG_GENERAL_1};

// The lake sphere's glow: the same tiles with the glowing palette swapped into its OBJ palette slot.
static const u16 sHolonSpherePal_Glow[] = INCGFX_U16("graphics/object_events/palettes/holon_sphere_glow.pal", ".gbapal");

bool32 IsHolonOverworld(void)
{
    return gMapHeader.mapLayout != NULL && gMapHeader.mapLayout->primaryTileset == &gTileset_General_Holon;
}

const struct SpritePalette *Holon_GetFieldEffectPalette(const struct SpritePalette *palette)
{
    if (!IsHolonOverworld())
        return palette;
    if (palette->tag == FLDEFF_PAL_TAG_GENERAL_0)
        return &sSpritePalette_HolonFieldEffect0;
    if (palette->tag == FLDEFF_PAL_TAG_GENERAL_1)
        return &sSpritePalette_HolonFieldEffect1;
    return palette;
}

extern const u16 gObjectEventPal_HolonSphere[];

// Object palette loader hook (event_object_movement.c): the sphere spawns already glowing once the flag is set,
// however late the camera reaches it.
u8 Holon_LoadSpherePalette(void)
{
    struct SpritePalette palette = {gObjectEventPal_HolonSphere, OBJ_EVENT_PAL_TAG_HOLON_SPHERE};

    u32 slot = IndexOfSpritePaletteTag(OBJ_EVENT_PAL_TAG_HOLON_SPHERE);

    if (slot != 0xFF)
        return slot;
    if (FlagGet(HOLON_SPHERE_GLOW_FLAG))
        palette.data = sHolonSpherePal_Glow;
    slot = LoadSpritePalette(&palette);
    if (slot != 0xFF)
        UpdateSpritePaletteWithWeather(slot, FALSE);
    return slot;
}

// callnative Holon_SetSphereGlow (Holon Lake): no-op while the sphere's palette isn't loaded.
void Holon_SetSphereGlow(struct ScriptContext *ctx)
{
    u32 slot = IndexOfSpritePaletteTag(OBJ_EVENT_PAL_TAG_HOLON_SPHERE);

    if (slot >= 16)
        return;
    LoadPalette(sHolonSpherePal_Glow, OBJ_PLTT_ID(slot), PLTT_SIZE_4BPP);
    UpdateSpritePaletteWithWeather(slot, TRUE);
}

// Power Spot rings (Wavebreak Voyages, Faba). The drained cells round the Research Tower and the lake pillar island are
// palette-07 twins of General palette-02 metatiles (gTileset_Holon 07 = "drained foliage"). Once Faba is beaten the
// rings heal: slot 7 gets General_Holon's palette 02, the same greens as the grass round them, so the twins draw
// exactly like the cells next to them. 0 tiles, 0 metatiles; the rest of Holon keeps its desaturated look.
extern const u16 gTilesetPalettes_GeneralHolon[][16];
extern const struct Tileset gTileset_Holon;

#define HOLON_DRAINED_FOLIAGE_PAL 7
#define HOLON_HEALTHY_FOLIAGE_PAL 2

void Holon_LoadHealedRingsPalette(const struct MapLayout *mapLayout, bool8 skipFaded)
{
    if (mapLayout == NULL || mapLayout->secondaryTileset != &gTileset_Holon || !FlagGet(FLAG_HOLON_POWER_SPOTS_HEALED))
        return;
    if (skipFaded)
        CpuCopy16(gTilesetPalettes_GeneralHolon[HOLON_HEALTHY_FOLIAGE_PAL], &gPlttBufferUnfaded[BG_PLTT_ID(HOLON_DRAINED_FOLIAGE_PAL)], PLTT_SIZE_4BPP);
    else
        LoadPalette(gTilesetPalettes_GeneralHolon[HOLON_HEALTHY_FOLIAGE_PAL], BG_PLTT_ID(HOLON_DRAINED_FOLIAGE_PAL), PLTT_SIZE_4BPP);
}
