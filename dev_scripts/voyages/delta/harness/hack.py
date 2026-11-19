# Temporary harness-only debug hack (reverted with git checkout src/debug.c)
p='src/debug.c'; s=open(p).read()
old='''static void DebugAction_Party_HealParty(u8 taskId)
{
    PlaySE(SE_USE_ITEM);
    HealPlayerParty();'''
new='''static void DebugAction_Party_HealParty(u8 taskId)
{
    static const u16 sp[] = {SPECIES_GYARADOS_DELTA, SPECIES_RALTS_DELTA, SPECIES_MAGIKARP_DELTA, SPECIES_CHARMELEON_DELTA, SPECIES_FARFETCHD_DELTA, SPECIES_KLINKLANG_DELTA, SPECIES_GYARADOS_DELTA};
    static const u8 lv[] = {50, 10, 19, 30, 30, 50, 55};
    u32 i;
    struct Pokemon mon;
    ZeroPlayerPartyMons();
    for (i = 0; i < ARRAY_COUNT(sp); i++)
    {
        CreateMonWithIVs(&mon, sp[i], lv[i], Random32(), OTID_STRUCT_PLAYER_ID, 31);
        GiveMonInitialMoveset(&mon);
        if (sp[i] == SPECIES_MAGIKARP_DELTA)
        {
            u32 exp = gExperienceTables[gSpeciesInfo[sp[i]].growthRate][20] - 1;
            u16 mv = MOVE_TACKLE;
            SetMonData(&mon, MON_DATA_EXP, &exp);
            SetMonData(&mon, MON_DATA_MOVE1, &mv);
        }
        if (i < PARTY_SIZE)
            CopyMon(&gParties[B_TRAINER_PLAYER][i], &mon, sizeof(mon));
        else
            SetBoxMonAt(StorageGetCurrentBox(), 0, &mon.box);
        GetSetPokedexFlag(SpeciesToNationalPokedexNum(sp[i]), FLAG_SET_SEEN);
        GetSetPokedexFlag(SpeciesToNationalPokedexNum(sp[i]), FLAG_SET_CAUGHT);
    }
    CalculatePlayerPartyCount();
    FlagSet(FLAG_SYS_POKEDEX_GET);
    PlaySE(SE_USE_ITEM);
    HealPlayerParty();'''
assert old in s; s=s.replace(old,new,1)
old2='''static void DebugAction_Party_ClearPokerus(u8 taskId)
{'''
new2='''static void DebugAction_Party_ClearPokerus(u8 taskId)
{
    struct Pokemon tmp;
    CopyMon(&tmp, &gParties[B_TRAINER_PLAYER][0], sizeof(tmp));
    CopyMon(&gParties[B_TRAINER_PLAYER][0], &gParties[B_TRAINER_PLAYER][2], sizeof(tmp));
    CopyMon(&gParties[B_TRAINER_PLAYER][2], &tmp, sizeof(tmp));'''
assert old2 in s; s=s.replace(old2,new2,1)
open(p,'w').write(s)
