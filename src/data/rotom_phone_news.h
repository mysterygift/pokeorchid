// Rotom Phone news ticker headlines (approved 2026-11-17, dev_scripts/orchid_ui/mock_phone.py NEWS).
// A headline is eligible while minBadges <= badges <= maxBadges and, if flag != 0,
// FlagGet(flag) == flagState. The pool is shuffled once each time the phone opens.

struct PhoneNews
{
    const u8 *text;
    u8 minBadges;
    u8 maxBadges;
    u16 flag;
    bool8 flagState;
};

static const struct PhoneNews sPhoneNews[] =
{
    { COMPOUND_STRING("Rookie Trainers spotted leaving Tosa Port!"),  0, 0, 0, FALSE },
    { COMPOUND_STRING("Ferry timetable back to normal after storm."), 0, 8, 0, FALSE },
    { COMPOUND_STRING("TOSA FM: new hits every hour, bzzt!"),         0, 8, 0, FALSE },
    { COMPOUND_STRING("Local Trainer wins first Gym Badge!"),         1, 1, 0, FALSE },
    { COMPOUND_STRING("Cold Storage reports a strange chill..."),     2, 8, FLAG_COLD_STORAGE_THAWED, FALSE },
    // TODO: no story flag opens Tosa Rail yet; gate this on it once one exists (mock: FLAG_TOSA_RAIL_OPEN set).
    { COMPOUND_STRING("Tosa Rail adds extra trains for fans."),       3, 8, 0, FALSE },
    { COMPOUND_STRING("Halfway there! Challenger holds 4 badges."),   4, 5, 0, FALSE },
    { COMPOUND_STRING("Tosa League braces for a new challenger!"),    8, 8, 0, FALSE },
    { COMPOUND_STRING("A new Champion is crowned in Tosa!"),          0, 8, FLAG_SYS_GAME_CLEAR, TRUE },
};

static const u8 sText_PhoneNoNews[] = _("No news today, bzzt!");
