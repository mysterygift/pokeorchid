#!/bin/bash
# usage: harness_build.sh <worktree> <outdir/outname> <savfile>
# e.g. dev_scripts/mgba_headless/harness_build.sh $PWD /tmp/emu/ed ../pokeorchid-ui-card/pokeemerald.sav
# Builds a harness ROM (key injection + save read from ROM @0x1F00000), copies to scratch, reverts sources.
set -e
WT=$1; OUT=$2; SAV=$3
S=$(cd "$(dirname "$OUT")" && pwd); OUT=$(basename "$OUT")
cd "$WT"
python3 - <<'PY'
p='src/main.c'; s=open(p).read()
s=s.replace("static void ReadKeys(void)\n{\n    u16 keyInput = REG_KEYINPUT ^ KEYS_MASK;","EWRAM_DATA volatile u16 gHarnessKeys = 0;\nstatic void ReadKeys(void)\n{\n    u16 keyInput = (REG_KEYINPUT ^ KEYS_MASK) | gHarnessKeys;",1)
open(p,'w').write(s)
p='src/agb_flash.c'; s=open(p).read()
s=s.replace("""    void (*readFlash_Core)(vu8 *, u8 *, u32);

    REG_WAITCNT""","""    void (*readFlash_Core)(vu8 *, u8 *, u32);

    if (*(vu32 *)0x09F00000 == 0x48415256)
    {
        const u8 *hs = (const u8 *)0x09F00010 + sectorNum * 0x1000 + offset;
        while (size--)
            *dest++ = *hs++;
        return;
    }

    REG_WAITCNT""",1)
open(p,'w').write(s)
PY
make -j8 >/dev/null 2>&1 || { git checkout src/main.c src/agb_flash.c; echo BUILD FAILED; exit 1; }
cp pokeemerald.gba "$S/$OUT.gba"; cp pokeemerald.elf "$S/$OUT.elf"
git checkout src/main.c src/agb_flash.c
python3 - "$S/$OUT.gba" "$SAV" <<'PY'
import sys
rom=bytearray(open(sys.argv[1],'rb').read()); sav=open(sys.argv[2],'rb').read()[:0x20000]
off=0x1F00000
assert all(b==0xFF for b in rom[off:off+0x20010]) or all(b==0 for b in rom[off:off+0x20010]), 'region not free'
rom[off:off+4]=(0x48415256).to_bytes(4,'little'); rom[off+0x10:off+0x10+len(sav)]=sav
open(sys.argv[1],'wb').write(rom)
PY
echo built $S/$OUT.gba
