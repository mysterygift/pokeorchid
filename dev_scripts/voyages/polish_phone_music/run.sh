#!/bin/bash
# usage: run.sh test_music.py|test_phone.py <dir with h.gba/h.elf>
# Holds the voyages headless lock, waits until GDB port 2345 is free (other sessions may run emulators without the
# lock), then runs the test with the Pillow venv. Only this run's own emulator is killed on exit.
VENV=/private/tmp/claude-501/-Users-arandavies-Development-pokemon-orchid-pokeorchid/72fd3b53-a4f0-4cad-8c0a-22b751dccb01/scratchpad/venv/bin/python
while ! mkdir /tmp/voyages_mgba.lock 2>/dev/null; do sleep 5; done
trap 'pkill -f "$2/h.gba"; rmdir /tmp/voyages_mgba.lock' EXIT
for i in $(seq 1 180); do pgrep -f mgba-rom-test-mac >/dev/null || lsof -iTCP:2345 -sTCP:LISTEN >/dev/null || break; sleep 5; done
cd "$(dirname "$0")"
timeout 1500 "$VENV" "$1" "$2"
