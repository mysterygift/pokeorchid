#!/bin/bash
# Faba harness ROM: polish_content's debug flags (0x29D no trainer sight, 0x29E no wild, 0x29F no collision) +
# dev_scripts/mgba_headless's key injection / embedded save, but every patched source is restored from a cp backup
# (no git checkout, the voyages tree is uncommitted). usage: hbuild.sh <outdir> <save.sav>  -> <outdir>/h.gba/.elf
# Rebuild normally afterwards (grep gHarnessKeys pokeemerald.map must be empty).
set -e
WT=$(cd "$(dirname "$0")/../../../.." && pwd)
OUT=$(cd "$1" && pwd)
SAV=$2
cd "$WT"
FILES="include/config/overworld.h include/config/wild_encounter.h src/party_menu.c src/main.c src/agb_flash.c"
for f in $FILES; do cp "$f" "$OUT/$(basename $f).bak"; done
restore() { for f in $FILES; do cp "$OUT/$(basename $f).bak" "$f"; done; }
trap restore EXIT
sed -i '' 's/^#define OW_FLAG_NO_TRAINER_SEE      0 /#define OW_FLAG_NO_TRAINER_SEE      FLAG_UNUSED_0x29D /; s/^#define OW_FLAG_NO_COLLISION        0 /#define OW_FLAG_NO_COLLISION        FLAG_UNUSED_0x29F /' include/config/overworld.h
sed -i '' 's/^#define WE_FLAG_NO_ENCOUNTER        0 /#define WE_FLAG_NO_ENCOUNTER        FLAG_UNUSED_0x29E /' include/config/wild_encounter.h
python3 - <<'PY'
p='src/party_menu.c'; s=open(p).read()
a="bool8 MonKnowsMove(struct Pokemon *mon, enum Move move)\n{\n"
assert a in s
s=s.replace(a, a+"    if (move == MOVE_SURF || move == MOVE_ROCK_SMASH) return TRUE; // HARNESS ONLY\n",1)
open(p,'w').write(s)
p='src/main.c'; s=open(p).read()
a="static void ReadKeys(void)\n{\n    u16 keyInput = REG_KEYINPUT ^ KEYS_MASK;"
assert a in s
s=s.replace(a,"EWRAM_DATA volatile u16 gHarnessKeys = 0;\nstatic void ReadKeys(void)\n{\n    u16 keyInput = (REG_KEYINPUT ^ KEYS_MASK) | gHarnessKeys;",1)
open(p,'w').write(s)
p='src/agb_flash.c'; s=open(p).read()
a="""    void (*readFlash_Core)(vu8 *, u8 *, u32);

    REG_WAITCNT"""
assert a in s
s=s.replace(a,"""    void (*readFlash_Core)(vu8 *, u8 *, u32);

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
grep -c "FLAG_UNUSED_0x29" include/config/overworld.h include/config/wild_encounter.h
make -j8 > "$OUT/hbuild.log" 2>&1 || { tail -30 "$OUT/hbuild.log"; echo BUILD FAILED; exit 1; }
cp pokeemerald.gba "$OUT/h.gba"; cp pokeemerald.elf "$OUT/h.elf"
python3 - "$OUT/h.gba" "$SAV" <<'PY'
import sys
rom=bytearray(open(sys.argv[1],'rb').read()); sav=open(sys.argv[2],'rb').read()[:0x20000]
off=0x1F00000
assert len(rom) <= off or all(b==0xFF for b in rom[off:off+0x20010]) or all(b==0 for b in rom[off:off+0x20010]), 'region not free'
rom += bytes([0xFF]) * max(0, off + 0x10 + len(sav) - len(rom))
rom[off:off+4]=(0x48415256).to_bytes(4,'little'); rom[off+0x10:off+0x10+len(sav)]=sav
open(sys.argv[1],'wb').write(rom)
PY
echo built "$OUT/h.gba"
