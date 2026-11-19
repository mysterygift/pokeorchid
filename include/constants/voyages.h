#ifndef GUARD_CONSTANTS_VOYAGES_H
#define GUARD_CONSTANTS_VOYAGES_H

// Orchid: the Sailor's voyages from Wavebreak Town (post-game, passcode-unlocked). See src/voyages.c.
#define VOYAGE_DEST_WAVEBREAK   0
#define VOYAGE_DEST_EON         1
#define VOYAGE_DEST_SEVII       2
#define VOYAGE_DEST_HOLON       3
#define VOYAGE_DEST_NEWMOON     4
#define VOYAGE_DEST_FULLMOON    5
#define VOYAGE_DEST_COUNT       6

// Extra ids returned by the destination menu (dynmultistack) and Voyage_CheckCode.
#define VOYAGE_MENU_ENTER_CODE  100
#define VOYAGE_MENU_CANCEL      101
#define VOYAGE_DEST_NONE        0xFF

// Legendary levels on the voyage islands (Orchid's Champion tops out at 58).
#define VOYAGE_LEGENDARY_LEVEL  70

#endif // GUARD_CONSTANTS_VOYAGES_H
