#ifndef GUARD_CONSTANTS_TRAIN_SOUNDS_H
#define GUARD_CONSTANTS_TRAIN_SOUNDS_H

// Tosa Rail sound effects, all existing game sounds (src/train_travel.c and the fare gate script
// TosaGateway_FareGate). To try another sound, change one line here; Debug menu > Sound plays any SE.
// Needs constants/songs.h first.

#define SE_TRAIN_RUMBLE         SE_TRUCK_MOVE       // train moving; loops until stopped
#define SE_TRAIN_BRAKES         SE_TRUCK_STOP       // played as the train slows into the platform
#define SE_TRAIN_DOOR_OPEN      SE_SLIDING_DOOR
#define SE_TRAIN_DOOR_CHIME     SE_DING_DONG        // "doors closing" chime, before they shut
#define SE_TRAIN_DOOR_SHUT      SE_SLIDING_DOOR

#define SE_FARE_GATE_TAP        SE_SUCCESS          // Rail Card accepted
#define SE_FARE_GATE_DENIED     SE_FAILURE          // no Rail Card
#define SE_FARE_GATE_OPEN       SE_ROTATING_GATE    // barrier opens
#define SE_FARE_GATE_SHUT       SE_ROTATING_GATE    // barrier closes behind the player

#endif // GUARD_CONSTANTS_TRAIN_SOUNDS_H
