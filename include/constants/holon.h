#ifndef GUARD_CONSTANTS_HOLON_H
#define GUARD_CONSTANTS_HOLON_H

// Orchid Holon (Wavebreak Voyages) placeholders.
// TODO(trainers): the six Holon Researcher trainers come from the trainers stream. Until it is merged,
// these alias existing vanilla trainers on unreachable maps so the Holon maps build and the battles start.
// Swap each TODO_TRAINER_HOLON_RESEARCHER_n for the real TRAINER_* id (and delete this block) after merging.

// The lake sphere glows once this flag is set (Holon Lake ON_RESUME swaps its OBJ palette).
// TODO(trainers): swap to FLAG_CYNTHIA_BEATEN_AT_LAKE (swap_placeholders.py), so it lights up after her battle.
#define HOLON_SPHERE_GLOW_FLAG            FLAG_CYNTHIA_BEATEN_AT_LAKE

#endif // GUARD_CONSTANTS_HOLON_H
