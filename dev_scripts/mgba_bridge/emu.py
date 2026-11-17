#!/usr/bin/env python3
"""Client for bridge.lua running inside mGBA.

Usage:
  emu.py "press A" "wait 60" "shot /tmp/x.png"     run commands in order
  emu.py --script steps.txt                         one command per line (# comments)
  emu.py "read32 gSaveBlock1Ptr"                    symbols resolve via pokeemerald.map

Commands are documented at the top of bridge.lua. Relative screenshot/savestate
paths are made absolute against the current directory.
"""
import argparse
import os
import re
import socket
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MAP_FILE = os.path.join(REPO, "pokeemerald.map")
PATH_CMDS = {"shot", "savestate", "loadstate"}
ADDR_CMDS = {"read8", "read16", "read32", "readrange", "write8", "write16", "write32"}

_symbols = None


def symbols():
    global _symbols
    if _symbols is None:
        _symbols = {}
        sym_re = re.compile(r"^\s+0x([0-9a-fA-F]{8,16})\s+([A-Za-z_]\w*)\s*$")
        try:
            with open(MAP_FILE) as f:
                for line in f:
                    m = sym_re.match(line)
                    if m:
                        _symbols.setdefault(m.group(2), int(m.group(1), 16))
        except FileNotFoundError:
            pass
    return _symbols


def resolve(token):
    base, _, off = token.partition("+")
    try:
        addr = int(base, 0)
    except ValueError:
        if base not in symbols():
            sys.exit(f"unknown symbol: {base}")
        addr = symbols()[base]
    if off:
        addr += int(off, 0)
    return hex(addr)


def prepare(line):
    parts = line.split()
    if not parts:
        return None
    cmd = parts[0].lower()
    if cmd in PATH_CMDS and len(parts) > 1:
        parts[1] = os.path.abspath(parts[1])
        os.makedirs(os.path.dirname(parts[1]), exist_ok=True)
    if cmd in ADDR_CMDS and len(parts) > 1:
        parts[1] = resolve(parts[1])
    return " ".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("commands", nargs="*")
    ap.add_argument("--script")
    ap.add_argument("--port", type=int, default=int(os.environ.get("ORCHID_BRIDGE_PORT", 8888)))
    ap.add_argument("--timeout", type=float, default=120)
    a = ap.parse_args()

    lines = list(a.commands)
    if a.script:
        with open(a.script) as f:
            lines += [l.split("#", 1)[0].strip() for l in f]
    # allow "cmd1; cmd2" in one arg
    lines = [p.strip() for l in lines for p in l.split(";")]
    lines = [p for p in (prepare(l) for l in lines if l) if p]
    if not lines:
        ap.print_help()
        return

    s = socket.create_connection(("127.0.0.1", a.port), timeout=a.timeout)
    f = s.makefile("rw", newline="\n")
    failed = False
    for line in lines:
        f.write(line + "\n")
        f.flush()
        resp = f.readline().strip()
        print(f"{line} -> {resp}")
        if not resp.startswith("ok"):
            failed = True
            break
    s.close()
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
