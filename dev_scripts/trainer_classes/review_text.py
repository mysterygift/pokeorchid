"""Static copy for review.html (intro, unmocked suggestions, open questions)."""

INTRO = """
<p>Twelve new trainer classes for Tosa, each with a 64×64 battle front pic and a 9-frame overworld
sheet. Every sprite is kitbashed from a vanilla Gen 3 sprite (pose, face and anatomy kept; clothes,
hair and props repainted), so proportions and shading stay on-model. Front pics use their own
16-colour palette. Overworld sheets use one of Emerald's shared NPC palettes, the same constraint
the vanilla NPCs follow. Each card notes which vanilla sprites it was built from.</p>
<p>Below the new classes are mocked edits to existing classes, then further edit ideas. Each edit is
tagged with how it lands: <b>Replaces vanilla GFX</b> when it is still the same job (School Kid in a
Tosa uniform), or <b>New class + sprites</b> when it is a different job (a Port Worker is not a
Sailor), in which case the vanilla class stays. Battle mocks use the Orchid battle tray and real
Orchid battle floors at true GBA size.</p>
"""

# vanilla class, idea, change size, lands as
_ROWS = [
    ('Expert ♀', 'Tai Chi Auntie, the pair to the Tai Chi Uncle edit. She already holds a fan, so tai-chi fan form needs only a recolour of the gi and fan.', 'Palette + small edit', 'Replace'),
    ('Psychic ♀', 'Parrot Fortune Teller (Little India street astrologer): a parakeet on her hand picking a card from a fanned deck.', 'Prop redraw', 'New: FORTUNE TELLER'),
    ('Psychic ♂', 'Temple fortune teller with a cylinder of kau chim sticks, plain shirt and spectacles.', 'Prop redraw', 'New: FORTUNE TELLER'),
    ('Fisherman', 'Pier Uncle: bucket hat, singlet, cooler box in place of the tackle; same crouch.', 'Small edit', 'Replace'),
    ('Hiker', 'Trail Trekker for the nature reserve: cap and daypack instead of the alpine rucksack, lighter tropical colours.', 'Small edit', 'Replace'),
    ('Collector', 'Karung Guni (rag-and-bone) man with a trolley of old newspapers and a hand horn.', 'Prop redraw', 'New: KARUNG GUNI'),
    ('Guitarist', 'Busker: same pose, small amp and an open guitar case with coins at his feet.', 'Small edit', 'Replace, rename BUSKER'),
    ('Gentleman', 'Towkay: light batik shirt instead of the tweed suit, keep the cane and moustache.', 'Recolour + small edit', 'New: TOWKAY'),
    ('Battle Girl', 'Wushu athlete: red silk wushu suit with a straight sword or sabre.', 'Small edit', 'Replace'),
    ('Ruin Maniac', 'Heritage Buff: bucket hat, heritage-trail map in place of the pick.', 'Small edit', 'Replace, rename HERITAGE BUFF'),
    ('Camper / Picnicker', 'Scouts and Guides: neckerchief with a woggle, khaki shorts, merit-badge sash.', 'Recolour + small edit', 'Replace'),
    ('Bug Catcher', 'Kampong kid with a matchbox for spider fighting, a traditional game, in place of the net.', 'Small edit', 'Replace'),
    ('Lady', 'Tai Tai: oversized sunglasses, designer-style handbag (no real logos), pearls.', 'Small edit', 'Replace, rename TAI TAI'),
    ('Parasol Lady', 'Monsoon Lady: clear plastic umbrella for Tosa’s afternoon storms.', 'Palette only', 'Replace'),
    ('Pokémaniac', 'Cosplayer: the same costume idea, recoloured as a homemade Pokémon cosplay from a con.', 'Palette only', 'Replace, rename COSPLAYER'),
    ('Hex Maniac', 'Optional folklore twist: Pontianak-inspired ghost-type trainer in a long white dress. Folklore figure, so check tone first.', 'Recolour', 'New: PONTIANAK'),
    ('Cycling Triathlete', 'Park Connector cyclist: recolour only; the new Delivery Rider covers the delivery angle.', 'Palette only', 'Replace'),
]

SUGGESTIONS = ('<div class="tbl"><table><thead><tr><th>Vanilla class</th><th>Orchid idea</th><th>Change size</th><th>Lands as</th></tr></thead><tbody>'
               + ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in _ROWS)
               + '</tbody></table></div>')

QUESTIONS = '<ol class="q"><li>(filled after the art pass)</li></ol>'
