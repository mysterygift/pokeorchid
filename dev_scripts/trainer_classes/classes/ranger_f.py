"""OW ONLY: Pokémon Ranger ♀ overworld, a recolour of the vanilla Picnicker OW (see ranger_m.py).
Moved from npc_3 to npc_white: green cap/top -> orange (same slots 8-A), auburn hair B/C/D -> dark slate 13 with a silver 12 highlight + black outline (her front pic has a near-black ponytail)
so it separates from the orange cap, straps/greys -> greys B-D, green skirt -> blue-grey
shorts (white frills -> mid grey), green shoes -> brown boots (6/7).
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from kit import *

ID = 'ranger_f'
o_ = load_ow('picnicker')
o_.pal = npc_pal('npc_white')

GREYS = {5: 11, 6: 12, 7: 13}
for i in range(9):
    o = 0 if i < 3 else 1
    x0, x1 = i * 16, i * 16 + 15
    # head + hair (hair reaches the shoulders)
    o_.remap({**GREYS, 11: 12, 12: 13, 13: 15}, (x0, 0, x1, 21 + o))
    # top: stays orange; straps -> greys; any hair ends -> dark slate
    o_.remap({**GREYS, 11: 12, 12: 13, 13: 15}, (x0, 22 + o, x1, 25 + o))
    # skirt -> blue-grey shorts
    o_.remap({8: 11, 9: 12, 10: 15, 5: 12, 14: 12, 6: 12, 7: 13, 11: 12, 12: 13, 13: 15}, (x0, 26 + o, x1, 27 + o))
    # shoes -> brown boots
    o_.remap({8: 6, 9: 7, 10: 15, **GREYS}, (x0, 28 + o, x1, 31))

p, probs = o_.save_ow(ID, 'npc_white')
print(p, probs or 'ok', o_.used())
compare(ID, 'pokemon_ranger_f', 'picnicker')
