"""OW ONLY: Pokémon Ranger ♂ overworld, a recolour of the vanilla Camper OW.
The Pkmn Ranger class and its front pics already exist (pokemon_ranger_m/f); vanilla Emerald just
reused the Camper/Picnicker overworlds. Colours follow the ranger front pic, moved from npc_3 to the
shared npc_white palette (orange 8-A sits on the same slots as the Camper's greens):
green cap/shirt -> orange cap/jacket, white undershirt -> dark grey, greys/navy straps -> greys B-D,
green shorts -> blue-grey, hair -> dark brown (A + black), shoes -> dark brown.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from kit import *

ID = 'ranger_m'
o_ = load_ow('camper')
o_.pal = npc_pal('npc_white')

GREYS = {5: 11, 6: 12, 7: 13}           # npc_3 greys/navy -> npc_white greys
for i in range(9):
    o = 0 if i < 3 else 1                # walk frames sit one pixel lower
    x0, x1 = i * 16, i * 16 + 15
    # head: cap stays on 8-A (now orange); hair C/D -> dark brown A / black outline
    o_.remap({**GREYS, 12: 10, 13: 15}, (x0, 0, x1, 20 + o))
    # torso: shirt stays 8-A (orange jacket); front-facing white undershirt -> dark grey shirt
    torso = dict(GREYS)
    if i in (0, 3, 4):
        torso[5] = 13
    o_.remap(torso, (x0, 21 + o, x1, 25 + o))
    # shorts -> blue-grey, black hem; shoes D -> dark brown A
    o_.remap({**GREYS, 8: 11, 9: 12, 10: 15, 13: 10, 12: 4}, (x0, 26 + o, x1, 31))

p, probs = o_.save_ow(ID, 'npc_white')
print(p, probs or 'ok', o_.used())
compare(ID, 'pokemon_ranger_m', 'camper')
