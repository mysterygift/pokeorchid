"""Check a proposed Cynthia team against the repo's learnsets (P_LVL_UP_LEARNSETS = GEN_LATEST, teachables
generated from Orchid's TMs/tutors, egg moves of the base form) and print the sets + how each move is legal.

usage: cynthia_team.py
"""
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
P = os.path.join(ROOT, 'src', 'data', 'pokemon')

CHAINS = {   # species -> evolution chain (base first) as learnset symbol stems
    'Spiritomb': ['Spiritomb'],
    'Roserade': ['Budew', 'Roselia', 'Roserade'],
    'Togekiss': ['Togepi', 'Togetic', 'Togekiss'],
    'Lucario': ['Riolu', 'Lucario'],
    'Milotic': ['Feebas', 'Milotic'],
    'Garchomp': ['Gible', 'Gabite', 'Garchomp'],
}

# DECIDED (user, DECISIONS.md 16): Platinum species, modern movesets (trainer moves need not be TM-learnable in
# Orchid; each move only has to exist in include/constants/moves.h), held items, Garchomp Mega Evolves, Lv 70-74.
TEAM = [   # species, level, item, ability, nature, moves
    ('Spiritomb', 70, 'Leftovers', 'Pressure', 'Calm', ['Shadow Ball', 'Dark Pulse', 'Will-O-Wisp', 'Psychic']),
    ('Roserade', 70, 'Black Sludge', 'Natural Cure', 'Modest', ['Energy Ball', 'Sludge Bomb', 'Shadow Ball', 'Toxic Spikes']),
    ('Togekiss', 72, 'Life Orb', 'Serene Grace', 'Modest', ['Air Slash', 'Dazzling Gleam', 'Aura Sphere', 'Thunder Wave']),
    ('Lucario', 72, "King's Rock", 'Inner Focus', 'Timid', ['Aura Sphere', 'Flash Cannon', 'Dragon Pulse', 'Nasty Plot']),
    ('Milotic', 70, 'Sitrus Berry', 'Marvel Scale', 'Bold', ['Scald', 'Ice Beam', 'Recover', 'Mirror Coat']),
    ('Garchomp', 74, 'Garchompite', 'Rough Skin', 'Jolly', ['Earthquake', 'Dragon Claw', 'Stone Edge', 'Fire Fang']),
]
ALTS = {   # Platinum moves that were replaced, and modern options, checked too (for the notes)
    'Spiritomb': ['Silver Wind', 'Will-O-Wisp', 'Sucker Punch', 'Hypnosis'], 'Roserade': ['Energy Ball', 'Leaf Storm', 'Toxic Spikes'],
    'Togekiss': ['Dazzling Gleam', 'Thunder Wave', 'Flamethrower', 'Extreme Speed'],
    'Lucario': ['Flash Cannon', 'Nasty Plot', 'Close Combat', 'Extreme Speed'], 'Milotic': ['Scald', 'Recover'],
    'Garchomp': ['Dragon Rush', 'Flamethrower', 'Giga Impact', 'Brick Break', 'Outrage', 'Stone Edge'],
}


def const(move):
    return 'MOVE_' + re.sub(r'[^A-Z0-9]+', '_', move.upper()).strip('_')


def read_all(pattern_dir):
    txt = ''
    for f in sorted(os.listdir(pattern_dir)):
        txt += open(os.path.join(pattern_dir, f)).read()
    return txt


LVL = read_all(os.path.join(P, 'level_up_learnsets')) + open(os.path.join(P, 'orchid_learnsets.h')).read()
TEACH = open(os.path.join(P, 'teachable_learnsets.h')).read()
EGG = open(os.path.join(P, 'egg_moves.h')).read()


def block(src, sym):
    # the GEN_LATEST level-up file is gen_9.h; take the LAST definition (later gens override earlier files)
    ms = list(re.finditer(r'static const [\w ]+ ' + sym + r'\[\] = \{(.*?)\};', src, re.S))
    return ms[-1].group(1) if ms else ''


def lvl_moves(stem):
    # gen_9.h holds GEN_LATEST; look there first
    g9 = open(os.path.join(P, 'level_up_learnsets', 'gen_9.h')).read()
    b = block(g9, f's{stem}LevelUpLearnset') or block(LVL, f's{stem}LevelUpLearnset')
    return {m: int(l) for l, m in re.findall(r'LEVEL_UP_MOVE\(\s*(\d+),\s*(MOVE_\w+)\)', b)}


def teach(stem):
    return set(re.findall(r'MOVE_\w+', block(TEACH, f's{stem}TeachableLearnset')))


def egg(stem):
    return set(re.findall(r'MOVE_\w+', block(EGG, f's{stem}EggMoveLearnset')))


def how(species, level, move):
    c = const(move)
    chain = CHAINS[species]
    for st in reversed(chain):
        lv = lvl_moves(st)
        if c in lv and lv[c] <= level:
            return f'level-up {st} L{lv[c]}'
    for st in reversed(chain):
        if c in teach(st):
            return f'TM/tutor ({st})'
    if c in egg(chain[0]):
        return f'egg move ({chain[0]})'
    return 'NOT LEGAL'


def exists(kind, name):
    hdr = {'MOVE': 'moves.h', 'ITEM': 'items.h', 'ABILITY': 'abilities.h'}[kind]
    c = kind + '_' + re.sub(r'[^A-Z0-9]+', '_', name.upper()).strip('_')
    return c, bool(re.search(r'\b' + c + r'\b', open(os.path.join(ROOT, 'include', 'constants', hdr)).read()))


def party_block():
    out = ['=== TRAINER_CYNTHIA ===', 'Name: Cynthia', 'Class: Champion', 'Pic: Cynthia', 'Gender: Female',
           'Music: Cynthia', 'Items: Full Restore / Full Restore / Full Restore / Full Restore',
           'Double Battle: No', 'AI: Basic Trainer', 'Mugshot: Yellow', '']
    for sp, lv, item, ab, nat, moves in TEAM:
        out += [f'{sp} @ {item}', f'Level: {lv}', f'Ability: {ab}', f'Nature: {nat}',
                'IVs: 31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe'] + [f'- {m}' for m in moves] + ['']
    return '\n'.join(out)


def main():
    bad = []
    for sp, lv, item, ab, nat, moves in TEAM:
        for kind, n in [('ITEM', item), ('ABILITY', ab)] + [('MOVE', m) for m in moves]:
            c, ok = exists(kind, n)
            if not ok:
                bad.append(c)
    print('constants missing:', bad or 'none')
    print(party_block())
    print('--- legality in Orchid (informational: trainer sets need not be learnable) ---')
    for sp, lv, item, ab, nat, moves in TEAM:
        print(f'{sp} L{lv} [{ab}]')
        for m in moves:
            print(f'    - {m:14s} {how(sp, lv, m)}')
        print(f'    @ {item}' if item else '    (no item)')
        for m in ALTS.get(sp, []):
            print(f'      (alt) {m:14s} {how(sp, lv, m)}')


if __name__ == '__main__':
    main()
