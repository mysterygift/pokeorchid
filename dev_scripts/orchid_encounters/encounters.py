#!/usr/bin/env python3
"""Orchid placeholder wild encounters for every Tosa and Tiksi map.

    python3 dev_scripts/orchid_encounters/encounters.py          # rewrite JSON + README
    python3 dev_scripts/orchid_encounters/encounters.py --check  # validate only, write nothing

What it does
  * Every map below gets a day table (base_label g<Map>, the fallback used for morning/day/evening)
    and a night table (g<Map>_Night).
  * It owns every encounter entry whose map is in the Tosa/Tiksi map groups or uses a Tosa/Tiksi
    region map section (see owned_maps()). Re-running deletes those entries and writes the spec
    below in their place, so it is idempotent. Battle Pyramid/Pike, Sevii, Holon, Voyages, Kanto
    and Hoenn tables are never touched.
  * Methods are checked against the map: land needs grass/cave/sand encounter metatiles, water and
    fishing need surfable water with encounters, rock smash needs a breakable rock object event.
    A method with nothing to back it is dropped with a warning (keep_without_tiles=True keeps it,
    for placeholder maps that will get the terrain later). Maps left with no methods are skipped,
    so a spec written for a map with no grass yet (Power Plant...) switches on by itself once the
    terrain is painted and the script is re-run.

How to retune
  Each table is a whitespace-separated species list in slot order (SPECIES_ prefix optional).
  Add @lo-hi (or @lv) to a species to override its levels, e.g. "SALAMENCE@50-54".

  land (12)      rates 20 20 | 10 10 10 10 | 5 5 | 4 4 | 1 1        -> commons first, rares last
  water (5)      rates 60 30 5 4 1
  rock smash (5) rates 60 30 5 4 1
  fishing (10)   "old old | good good good | super super super super super"
                 old 70 30, good 60 20 20, super 40 40 15 4 1

  Land slots 8-11 (the 4%/1% rares) get +1 level on top of the table range (RARE_BUMP).
  Fishing levels come from one number, the tier (usually the Surf level of that water): see rods().
  Night tables reuse the day levels unless night_lv is given; night_rate changes the encounter rate.

Time-of-day gotcha: tools/wild_encounters/wild_encounters_to_header.py decides the time slot by
searching base_label for "Morning", "Day", "Evening", "Night". A map folder name containing one of
those words (e.g. "...Holiday...") would be misfiled, so validate() refuses it.
"""
import json
import re
import struct
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JSON_PATH = ROOT / 'src/data/wild_encounters.json'
README_PATH = Path(__file__).resolve().parent / 'README.md'

LEVEL_CAP = 65
RARE_BUMP = 1
TIME_WORDS = ('Morning', 'Day', 'Evening', 'Night')
SLOTS = {'land_mons': 12, 'water_mons': 5, 'rock_smash_mons': 5, 'fishing_mons': 10}
METHOD_ORDER = ['land_mons', 'water_mons', 'rock_smash_mons', 'fishing_mons']
NEVER_OWN_GROUPS = {'gMapGroup_Voyages', 'gMapGroup_Holon', 'gMapGroup_Sevii'}
TOSA_GROUPS = {'gMapGroup_TosaRail', 'gMapGroup_TosaOverworld'}
TIKSI_GROUPS = {'gMapGroup_Tiksi'}


# ---------------------------------------------------------------------------------------------
# Spec helpers
# ---------------------------------------------------------------------------------------------
class T:
    """One method's day + night table."""
    def __init__(self, method, rate, lv, day, night, night_rate=None, night_lv=None):
        self.method, self.rate, self.lv = method, rate, lv
        self.day, self.night = day, night
        self.night_rate = rate if night_rate is None else night_rate
        self.night_lv = lv if night_lv is None else night_lv


def land(lv, day, night, rate=20, **kw):
    return T('land_mons', rate, lv, day, night, **kw)


def cave(lv, day, night, rate=10, **kw):
    return T('land_mons', rate, lv, day, night, **kw)


def surf(tier, day, night, rate=4, **kw):
    return T('water_mons', rate, (tier, tier + 6), day, night, **kw)


def rocks(lv, day, night, rate=20, **kw):
    return T('rock_smash_mons', rate, lv, day, night, **kw)


def fish(tier, day, night, rate=30, **kw):
    return T('fishing_mons', rate, tier, day, night, **kw)


def rods(tier):
    """Old / Good / Super Rod level ranges for a water tier."""
    old = (max(5, tier // 2 - 2), max(8, tier // 2 + 3))
    good = (max(10, tier - 10), max(15, tier - 2))
    sup = (tier, tier + 6)
    return [old] * 2 + [good] * 3 + [sup] * 5


class M:
    def __init__(self, name, region, area, levels, note, *tables, keep_without_tiles=False):
        self.name, self.region, self.area, self.levels, self.note = name, region, area, levels, note
        self.tables = {t.method: t for t in tables}
        self.keep_without_tiles = keep_without_tiles

    @property
    def label(self):
        return 'g' + self.name


# ---------------------------------------------------------------------------------------------
# The spec. Level curve = travel distance from Telok Town (MAPSEC_OLDALE_TOWN, cell 7,8):
#   Telok -> South Tosa Reserve 1 -> Tosa Port ; Telok -> Route 311 -> Damp Path -> Wavebreak ;
#   Telok -> STR2 -> STR3 -> NTR -> Timah -> 302/Mt Batok -> Faber -> 307 -> Pinestamp -> 308 ->
#   Changu / 309 -> Bura -> East Tosa Reserve -> Senoko / 310 -> Juran ;
#   Faber -> 303 -> Kantu Falls (Surf gate) -> 304 -> Galangal -> 305 -> Challenger Gate -> Trail.
#   Water is levelled by when Surf / rods are usable, not by distance. Tiksi = post-game, 50-65.
# ---------------------------------------------------------------------------------------------
TOSA = 'Tosa'
TIKSI = 'Tiksi'

MAPS = [
    # ---------------- Telok Town surroundings (Lv 2-10) ----------------
    M('SouthTosaReserve', TOSA, 'Telok - Tosa Port', '2-5 / surf 18', 'First route: coastal rainforest reserve with a river; east bank behind Surf + Rock Smash. Keeps the designer\'s Mareep/Starly/Lotad/Dewpider/Tyrogue core.',
      land((2, 5),
           'STARLY LOTAD MAREEP WURMPLE PIKIPEK YUNGOOS DEWPIDER NINCADA TYROGUE FLETCHLING IYEPURE SMOLIV',
           'HOOTHOOT LOTAD MAREEP SPINARAK WURMPLE RATTATA_ALOLA DEWPIDER VENONAT TYROGUE ODDISH IYEPURE MORELULL',
           night_rate=22),
      surf(18, 'LOTAD SURSKIT WOOPER MASQUERAIN LOMBRE',
               'WOOPER LOTAD ARROKUDA LOMBRE MASQUERAIN'),
      rocks((18, 24), 'GEODUDE DWEBBLE NOSEPASS SHUCKLE ROGGENROLA',
                      'ROGGENROLA GEODUDE DWEBBLE SHUCKLE NOSEPASS'),
      fish(18, 'MAGIKARP GOLDEEN | GOLDEEN CORPHISH MAGIKARP | CORPHISH BARBOACH ARROKUDA CRAWDAUNT FEEBAS',
               'MAGIKARP BARBOACH | CORPHISH BARBOACH GOLDEEN | CORPHISH BARBOACH CHEWTLE CRAWDAUNT WHISCASH')),

    M('Route311_East', TOSA, 'Telok - Damp Path', '3-6', 'Grassy hills west of Telok; Galar squirrels and Paldean piglets have moved in.',
      land((3, 6),
           'PIDGEY ZIGZAGOON SKWOVET NIDORAN_F NIDORAN_M SEWADDLE CATERPIE POOCHYENA LECHONK FLABEBE SHINX RALTS',
           'HOOTHOOT ZIGZAGOON POOCHYENA NIDORAN_F NIDORAN_M KRICKETOT ODDISH RATTATA LECHONK NICKIT SHINX RALTS')),

    M('SouthTosaReserve2', TOSA, 'Telok - STR3', '3-6 / surf 20', 'Jungle edge and coastline east of Telok; macaque-like Mankey raid the bins.',
      land((3, 6),
           'PIKIPEK SEWADDLE STARLY MAREEP BUDEW SCATTERBUG FOMANTIS BOUNSWEET AIPOM MANKEY IYEPURE TAROUNTULA',
           'HOOTHOOT SPINARAK MAREEP SEWADDLE BUDEW ODDISH FOMANTIS VENONAT MORELULL MANKEY IYEPURE LAOMEOW'),
      surf(20, 'TENTACOOL WINGULL PELIPPER MANTYKE FINIZEN',
               'TENTACOOL CHINCHOU WINGULL MANTYKE LANTURN'),
      fish(20, 'MAGIKARP FINNEON | FINNEON WISHIWASHI REMORAID | WISHIWASHI REMORAID CORSOLA LUVDISC BRUXISH',
               'MAGIKARP CHINCHOU | CHINCHOU FINNEON WISHIWASHI | CHINCHOU REMORAID CORSOLA LUMINEON BRUXISH')),

    M('DampPath', TOSA, 'Route 311 tunnel', '5-9', 'Wet abandoned path through the West Tosa hills: Zubat everywhere, hoodlum Scraggy and Timburr hang about.',
      cave((5, 9),
           'ZUBAT ZUBAT WOOPER PARAS GEODUDE WOOBAT SHELLOS TYMPOLE SCRAGGY TIMBURR GOOMY STUNFISK_GALAR',
           'ZUBAT ZUBAT WOOPER PARAS GASTLY WOOBAT SHELLOS SABLEYE SCRAGGY TIMBURR GOOMY MISDREAVUS',
           night_rate=12)),

    M('Route311_West', TOSA, 'Damp Path - Wavebreak', '6-10', 'Coastal meadow down to Wavebreak; seabirds from three regions.',
      land((6, 10),
           'WINGULL ZIGZAGOON SKWOVET FLETCHLING NIDORAN_F NIDORAN_M MAKUHITA ROOKIDEE ELECTRIKE WATTREL ABRA CRAMORANT',
           'HOOTHOOT ZIGZAGOON NICKIT WINGULL NIDORAN_F NIDORAN_M MAKUHITA MURKROW ELECTRIKE GASTLY ABRA IMPIDIMP')),

    M('RailwayTunnels', TOSA, 'Under Tosa Port station', '5-9', 'Railway maintenance tunnels: Koffing in the exhaust, rats on the tracks, Magnemite and Joltik in the wiring. Night = rats and Ghosts.',
      cave((5, 9),
           'KOFFING RATTATA_ALOLA TRUBBISH ZUBAT GRIMER PIDOVE MAGNEMITE VENIPEDE DRILBUR JOLTIK TINKATINK GRIMER_ALOLA',
           'RATTATA_ALOLA KOFFING RATTATA ZUBAT GASTLY TRUBBISH GRIMER EKANS JOLTIK GREAVARD TINKATINK RATICATE_ALOLA@10-12',
           night_rate=14),
      keep_without_tiles=True),

    M('SouthTosaReserve3', TOSA, 'STR2 - NTR / Abandoned House', '5-9 / surf 22', 'Reserve wetland crossroads; Purrchi stalk the rushes.',
      land((5, 9),
           'STARLY PIKIPEK LOTAD SHROOMISH NINCADA FOMANTIS BUDEW SURSKIT PURRCHI DEWPIDER SMOLIV TOGEDEMARU',
           'HOOTHOOT SPINARAK LOTAD SHROOMISH NINCADA VENONAT BUDEW ODDISH PURRCHI DEWPIDER MORELULL GASTLY'),
      surf(22, 'TENTACOOL WINGULL LOTAD PELIPPER LOMBRE',
               'TENTACOOL CHINCHOU LOTAD LOMBRE LANTURN'),
      fish(22, 'MAGIKARP TENTACOOL | MAGIKARP CORPHISH REMORAID | CORPHISH REMORAID SKRELP CRAWDAUNT OCTILLERY',
               'MAGIKARP CHINCHOU | CHINCHOU CORPHISH REMORAID | CORPHISH CHINCHOU SKRELP CRAWDAUNT LANTURN')),

    M('AbandonedHouse', TOSA, 'STR3 - STR4', '8-12', 'Haunted house from the early days of Tosa; lights seen from Moongrove at night.',
      land((8, 12),
           'RATTATA GASTLY SPINARAK SHUPPET DUSKULL MURKROW LITWICK SINISTEA PHANTUMP MISDREAVUS GREAVARD MIMIKYU',
           'GASTLY GASTLY SHUPPET DUSKULL LITWICK MISDREAVUS SINISTEA RATTATA PHANTUMP GREAVARD MIMIKYU ROTOM',
           night_rate=25)),

    M('SouthTosaReserve4', TOSA, 'Abandoned House - Moongrove', '8-12 / surf 22', 'Mangrove fringe pond; invasive Paldean Wooper outcompete the natives.',
      land((8, 12),
           'STARLY WOOPER_PALDEA LOTAD POLIWAG SHROOMISH BUDEW STUNKY SKWOVET PURRCHI YUNGOOS TANGELA PAWMI',
           'HOOTHOOT WOOPER_PALDEA LOTAD POLIWAG SHROOMISH GASTLY STUNKY RATTATA_ALOLA PURRCHI MURKROW TANGELA PHANTUMP'),
      surf(22, 'POLIWAG WOOPER LOTAD SURSKIT POLIWHIRL',
               'POLIWAG WOOPER_PALDEA LOTAD POLIWHIRL MASQUERAIN'),
      fish(22, 'MAGIKARP GOLDEEN | GOLDEEN POLIWAG BARBOACH | BARBOACH POLIWHIRL SEAKING WHISCASH BASCULIN',
               'MAGIKARP POLIWAG | BARBOACH POLIWAG GOLDEEN | BARBOACH WHISCASH POLIWHIRL BASCULIN CHEWTLE')),

    M('NorthTosaReserve', TOSA, 'STR3 - Timah City', '7-11 / surf 22', 'Flowering heart of the reserve below Hana\'s orchid city: bees, blossoms, Tropius.',
      land((7, 11),
           'PIKIPEK COMBEE BUDEW CHERUBI SEWADDLE PETILIL COTTONEE TOGEDEMARU IYEPURE BOUNSWEET TROPIUS COMFEY',
           'HOOTHOOT SPINARAK BUDEW CHERUBI ODDISH PETILIL VENONAT MORELULL IYEPURE LAOMEOW TROPIUS NOIBAT'),
      surf(22, 'SURSKIT LOTAD WOOPER MASQUERAIN LOMBRE',
               'WOOPER LOTAD SURSKIT LOMBRE POLIWAG'),
      fish(22, 'MAGIKARP GOLDEEN | GOLDEEN BARBOACH POLIWAG | BARBOACH SEAKING BASCULIN WHISCASH CHEWTLE',
               'MAGIKARP POLIWAG | BARBOACH POLIWAG GOLDEEN | BARBOACH WHISCASH BASCULIN SEAKING CHEWTLE')),

    M('MoongroveMarsh', TOSA, 'East of Moongrove City', '10-14 / surf 24', 'Mangrove marsh: mudskipper Mudkip, catfish for Tork, elusive Feebas and Dratini on the Super Rod.',
      land((10, 14),
           'WOOPER TYMPOLE LOTAD CROAGUNK SHELLOS MUDBRAY PURRCHI STUNFISK YANMA SALANDIT GOOMY MUDKIP',
           'WOOPER TYMPOLE SPINARAK CROAGUNK SHELLOS HOOTHOOT PURRCHI STUNFISK GASTLY SALANDIT GOOMY WOOPER_PALDEA',
           night_rate=25),
      surf(24, 'WOOPER LOTAD SURSKIT QUAGSIRE LOMBRE',
               'WOOPER LOTAD QUAGSIRE LOMBRE CHEWTLE'),
      fish(24, 'MAGIKARP BARBOACH | BARBOACH GOLDEEN CORPHISH | BARBOACH WHISCASH CHEWTLE FEEBAS DRATINI',
               'MAGIKARP BARBOACH | BARBOACH CORPHISH POLIWAG | WHISCASH BARBOACH CRAWDAUNT DRATINI FEEBAS')),

    # ---------------- Timah - Faber (Lv 11-21) ----------------
    M('Route302', TOSA, 'Timah - Faber', '11-15', 'Foothills climbing to the cliff town; fighters and Rockruff.',
      land((11, 15),
           'TAILLOW SKWOVET MACHOP GEODUDE PONYTA LILLIPUP MANKEY ROCKRUFF DUNSPARCE KLAWF RIOLU HAWLUCHA',
           'HOOTHOOT SKWOVET MACHOP GEODUDE MURKROW LILLIPUP MANKEY ROCKRUFF MEOWTH NICKIT RIOLU ZORUA')),

    M('MtBatok_1F', TOSA, 'Mt. Batok quarry', '12-16', 'Old granite quarry hill: miners\' Makuhita, coal Rolycoly, salt Nacli.',
      cave((12, 16),
           'ZUBAT GEODUDE ROGGENROLA WHISMUR MAKUHITA DIGLETT ROLYCOLY NOSEPASS TIMBURR NACLI ONIX CUFANT',
           'ZUBAT GEODUDE ROGGENROLA WOOBAT MAKUHITA DIGLETT ROLYCOLY SABLEYE TIMBURR NACLI ONIX GASTLY')),
    M('MtBatok_2F', TOSA, 'Mt. Batok quarry', '13-17', 'Deeper quarry galleries; Aron chew the ore seams.',
      cave((13, 17),
           'ZUBAT GEODUDE ROGGENROLA DRILBUR ARON MACHOP ROLYCOLY WHISMUR NACLI MAWILE ONIX CARBINK',
           'ZUBAT GEODUDE ROGGENROLA DRILBUR ARON WOOBAT ROLYCOLY SABLEYE NACLI MAWILE ONIX CARBINK')),
    M('MtBatok_3F', TOSA, 'Mt. Batok summit', '14-18', 'Summit caves where Meru trains: Meditite and Mienfoo; a rare Larvitar.',
      cave((14, 18),
           'ZUBAT GEODUDE ROGGENROLA ARON MACHOP MEDITITE DRILBUR NOSEPASS NACLI MIENFOO LARVITAR CARBINK',
           'ZUBAT GEODUDE ROGGENROLA ARON MACHOP WOOBAT DRILBUR SABLEYE NACLI MIENFOO LARVITAR DUSKULL')),
    M('MtBatok_East_2F', TOSA, 'Mt. Batok east', '16-20', 'Steel-ore side of the mountain: Tinkatink hammer ore, Beldum drift in.',
      cave((16, 20),
           'ZUBAT GEODUDE ARON ROGGENROLA MAGNEMITE BRONZOR TINKATINK MAWILE DRILBUR NACLI BELDUM VAROOM',
           'ZUBAT GEODUDE ARON ROGGENROLA WOOBAT BRONZOR TINKATINK SABLEYE DRILBUR NACLI BELDUM DUSKULL')),
    M('MtBatok_East_1F', TOSA, 'Mt. Batok east - Route 307', '17-21', 'Sandy lower tunnels: Sandile, Cufant, a rare Gible.',
      cave((17, 21),
           'ZUBAT GEODUDE MACHOP ROGGENROLA DIGLETT TIMBURR ROLYCOLY CUFANT DWEBBLE ONIX SANDILE GIBLE',
           'ZUBAT GEODUDE MACHOP ROGGENROLA DIGLETT WOOBAT ROLYCOLY SABLEYE DWEBBLE ONIX SANDILE GIBLE')),

    M('Route303', TOSA, 'Faber - Kantu Falls', '17-21', 'Cliff path up to the falls; escaped Squawkabilly flocks.',
      land((17, 21),
           'SPEAROW MANKEY PONYTA MACHOP ROCKRUFF HOPPIP SWABLU TAUROS_PALDEA_COMBAT HERACROSS SKIDDO HAWLUCHA SQUAWKABILLY',
           'HOOTHOOT MANKEY PONYTA MACHOP ROCKRUFF MURKROW SWABLU ZUBAT HERACROSS SKIDDO HAWLUCHA NOIBAT')),

    M('KantuFalls', TOSA, 'Kantu Falls', 'surf 28', 'Mineral-rich bathing falls: Slowpoke soak, Magikarp leap, Dratini hide under the spray.',
      surf(28, 'PSYDUCK MARILL SLOWPOKE AZUMARILL GOLDUCK',
               'PSYDUCK SLOWPOKE MARILL LOTAD GOLDUCK'),
      fish(28, 'MAGIKARP GOLDEEN | GOLDEEN POLIWAG BASCULIN | SEAKING POLIWHIRL BASCULIN DRATINI GYARADOS',
               'MAGIKARP POLIWAG | POLIWAG GOLDEEN BARBOACH | POLIWHIRL SEAKING WHISCASH DRATINI POLITOED')),

    # ---------------- Faber - Changu - Bura (Lv 18-33) ----------------
    M('Route307', TOSA, 'Faber - Pinestamp', '18-22', 'Pine woods towards Pinestamp: Pineco, Deerling, Stantler.',
      land((18, 22),
           'STARAVIA PINECO SKWOVET SEEDOT TEDDIURSA PONYTA DEERLING VULPIX STANTLER BUNEARY DEDENNE KECLEON',
           'HOOTHOOT PINECO NICKIT SEEDOT TEDDIURSA MURKROW DEERLING VULPIX STANTLER SPINARAK DEDENNE ZORUA')),

    M('Route308', TOSA, 'Pinestamp - Changu / Route 309', '20-25', 'Peri-urban grassland with farm escapes; Zangoose by day, Seviper by night.',
      land((20, 25),
           'PIDOVE LINOONE LECHONK ELECTRIKE YUNGOOS SENTRET TAUROS GROWLITHE PAWMI SQUAWKABILLY SCYTHER ZANGOOSE',
           'HOOTHOOT LINOONE LECHONK ELECTRIKE RATTATA_ALOLA MEOWTH STUNKY GROWLITHE PAWMI MURKROW SCYTHER SEVIPER')),

    M('IndustrialPark', TOSA, 'South of Route 308', '22-26', 'Factories and depots: Magnemite, Klink, Grimer in the drains.',
      land((22, 26),
           'MAGNEMITE KLINK GRIMER KOFFING TRUBBISH VOLTORB TIMBURR PAWMO TOXEL ROLYCOLY VAROOM ELEKID',
           'MAGNEMITE KLINK GRIMER KOFFING TRUBBISH RATTATA_ALOLA GRIMER_ALOLA PAWMO TOXEL GASTLY VAROOM ROTOM')),

    M('Route306', TOSA, 'Changu - Airport', '24-28', 'Airport perimeter: stowaways and escaped pets from every region; Bombirdier deliver.',
      land((24, 28),
           'TRANQUILL CORVISQUIRE FLETCHINDER SWABLU FURFROU TOGEDEMARU MEOWTH_GALAR EMOLGA SQUAWKABILLY DUCKLETT EEVEE BOMBIRDIER',
           'NOCTOWL CORVISQUIRE MURKROW SWABLU FURFROU MEOWTH MEOWTH_GALAR NOIBAT WOOBAT DUCKLETT EEVEE ZORUA_HISUI')),

    M('Route309', TOSA, 'Route 308 - Bura City', '25-30', 'Cat country on the way to Maria\'s gym; Laomeow sing at night.',
      land((25, 30),
           'TRANQUILL SKITTY GLAMEOW MEOWTH FURRET ESPURR LITLEO LUXIO FIDOUGH PURRLOIN MILTANK PERSIAN',
           'NOCTOWL SKITTY GLAMEOW MEOWTH_ALOLA PURRLOIN ESPURR STUNKY LUXIO MURKROW LIEPARD LAOMEOW ABSOL')),

    M('EastTosaReserve2', TOSA, 'Bura - Route 310 - ETR3', '26-30', 'Reserve woodland with Heracross/Pinsir trees and monkey troops.',
      land((26, 30),
           'STARAVIA KRICKETUNE COMBEE BURMY AIPOM TEDDIURSA HERACROSS PINSIR MINCCINO IYEPURE SCYTHER PASSIMIAN',
           'NOCTOWL KRICKETUNE ARIADOS BURMY ORANGURU TEDDIURSA HERACROSS PINSIR HAUNTER IYEPURE VENONAT LAOMEOW')),

    M('EastTosaReserve', TOSA, 'Bura - Challenger Gate', '27-31 / surf 30', 'Open savanna reserve: Phanpy, Girafarig, Blitzle herds round the waterhole.',
      land((27, 31),
           'STARAVIA DODUO PHANPY GIRAFARIG TAUROS RHYHORN BLITZLE DONPHAN LITLEO HIPPOPOTAS IYEPURE KANGASKHAN',
           'NOCTOWL DODUO PHANPY GIRAFARIG TAUROS RHYHORN BLITZLE MIGHTYENA LITLEO HIPPOPOTAS LAOMEOW ZORUA'),
      surf(30, 'MARILL PSYDUCK MASQUERAIN AZUMARILL GOLDUCK',
               'PSYDUCK WOOPER QUAGSIRE MARILL GOLDUCK'),
      fish(30, 'MAGIKARP GOLDEEN | GOLDEEN BARBOACH POLIWAG | SEAKING WHISCASH POLIWHIRL BASCULIN GYARADOS',
               'MAGIKARP POLIWAG | BARBOACH POLIWAG GOLDEEN | WHISCASH POLIWHIRL SEAKING BASCULIN POLITOED')),

    M('Route310', TOSA, 'ETR2 - Juran City', '28-32', 'Road to the casino city: lucky Chansey, coin-chest Gimmighoul, thugs\' Houndour; Honchkrow at night.',
      land((28, 32),
           'TRANQUILL LINOONE WATCHOG SPINDA MEOWTH SNUBBULL SCRAGGY HOUNDOUR DUNSPARCE SANDILE CHANSEY GIMMIGHOUL',
           'NOCTOWL LINOONE WATCHOG MURKROW MEOWTH PURRLOIN SCRAGGY HOUNDOUR SABLEYE SANDILE HONCHKROW GIMMIGHOUL')),

    M('EastTosaReserve3', TOSA, 'ETR2 - Senoko (wind farms)', '29-33 / surf 30', 'Windswept grassland under Senoko\'s turbines: Electric and wind riders; Tynamo in the ponds.',
      land((29, 33),
           'SWABLU SKIPLOOM FLETCHINDER ELECTRIKE LUXIO WATTREL PACHIRISU EMOLGA FLAAFFY TOGEDEMARU RUFFLET ORICORIO_POM_POM',
           'NOCTOWL DRIFLOON SWABLU ELECTRIKE LUXIO WATTREL PACHIRISU EMOLGA FLAAFFY NOIBAT RUFFLET MURKROW'),
      surf(30, 'PSYDUCK WOOPER MARILL GOLDUCK AZUMARILL',
               'WOOPER PSYDUCK QUAGSIRE GOLDUCK MARILL'),
      fish(30, 'MAGIKARP GOLDEEN | GOLDEEN BARBOACH TYNAMO | SEAKING WHISCASH EELEKTRIK BASCULIN GYARADOS',
               'MAGIKARP TYNAMO | TYNAMO BARBOACH POLIWAG | EELEKTRIK WHISCASH POLIWHIRL SEAKING EELEKTROSS@39-40')),

    M('PowerPlant', TOSA, 'Senoko wind power plant', '32-36', 'Wind power plant: Magnemite, Voltorb, Electabuzz, Rotom in the control room.',
      land((32, 36),
           'MAGNEMITE VOLTORB ELECTABUZZ PIKACHU MAGNETON KLANG JOLTIK PAWMO TOXEL ELECTRODE ROTOM GALVANTULA',
           'MAGNEMITE VOLTORB ELECTABUZZ PIKACHU MAGNETON KLANG JOLTIK GASTLY TOXEL ELECTRODE ROTOM HAUNTER')),

    # ---------------- Road to the League (Lv 30-55) ----------------
    M('Route304', TOSA, 'Kantu Falls - Galangal', '30-34', 'Highland rainforest above the falls: Tropius, Breloom, Capsakid.',
      land((30, 34),
           'TRUMBEAK SKIPLOOM TROPIUS PANSAGE LOMBRE BRELOOM HERACROSS AMBIPOM PASSIMIAN DOLLIV CAPSAKID TANGELA',
           'NOCTOWL ARIADOS TROPIUS ORANGURU LOMBRE BRELOOM HERACROSS GLOOM PASSIMIAN SHIINOTIC CAPSAKID MISDREAVUS')),

    M('GalangalForest', TOSA, 'Galangal Forest', '33-37', 'Forest of medicinal plants: healing Comfey, cordyceps Parasect, ginger-root Iyepure; Spiritomb at night.',
      land((33, 37),
           'PETILIL ROSELIA GLOOM CHERRIM WEEPINBELL STEENEE COMFEY BRELOOM IYEPURE PARASECT TOEDSCOOL ARBOLIVA@35-37',
           'NOCTOWL ROSELIA GLOOM SHIINOTIC WEEPINBELL FOONGUS PHANTUMP COMFEY IYEPURE PARASECT TOEDSCOOL SPIRITOMB')),

    M('Route305', TOSA, 'Galangal - Challenger Gate', '38-43', 'Mountain approach to the League: tough herds and birds of prey.',
      land((38, 43),
           'STARAPTOR FEAROW RAPIDASH@40-43 PRIMEAPE BOUFFALANT SAWSBUCK GOGOAT TAUROS_PALDEA_COMBAT HAWLUCHA MIGHTYENA SCYTHER FRAXURE',
           'NOCTOWL FEAROW RAPIDASH@40-43 PRIMEAPE MIGHTYENA SAWSBUCK GOGOAT HOUNDOOM HAWLUCHA HAUNTER SNEASEL FRAXURE')),

    M('ChallengersTrail_1F', TOSA, 'Challenger\'s Trail', '44-48', 'Victory Road caves: fighters, steel and young dragons.',
      cave((44, 48),
           'GOLBAT GRAVELER BOLDORE LAIRON MACHOKE HARIYAMA ONIX MEDICHAM GABITE KLANG STEELIX LUCARIO',
           'GOLBAT GRAVELER BOLDORE LAIRON MACHOKE SWOOBAT ONIX SABLEYE GABITE DUSCLOPS STEELIX LUCARIO')),
    M('ChallengersTrail_2F', TOSA, 'Challenger\'s Trail', '46-50', 'Mid trail: Shelgon, Fraxure, Druddigon lurk in the cracks.',
      cave((46, 50),
           'GOLBAT GRAVELER BOLDORE LAIRON HARIYAMA MAWILE SHELGON MEDICHAM GABITE KLANG FRAXURE DRUDDIGON',
           'GOLBAT GRAVELER BOLDORE LAIRON HARIYAMA SWOOBAT SHELGON SABLEYE GABITE DUSCLOPS FRAXURE DRUDDIGON')),
    M('ChallengersTrail_3F', TOSA, 'Challenger\'s Trail (League exit)', '48-54', 'Final stretch: Aggron, Excadrill and very rare Zweilous / Salamence.',
      cave((48, 53),
           'GOLBAT GRAVELER BOLDORE AGGRON HARIYAMA EXCADRILL SHELGON CARBINK GABITE DRUDDIGON ZWEILOUS@50-54 SALAMENCE@50-54',
           'GOLBAT GRAVELER BOLDORE AGGRON HARIYAMA SWOOBAT SHELGON SABLEYE GABITE DUSCLOPS ZWEILOUS@50-54 SALAMENCE@50-54')),

    # ---------------- Sea routes (Surf, levelled by access) ----------------
    M('Route312', TOSA, 'Wavebreak - south sea', 'surf 26', 'Open sea south of Wavebreak; Torpesquid raid boats.',
      surf(26, 'TENTACOOL WINGULL FINIZEN PELIPPER TORPESQUID',
               'TENTACOOL CHINCHOU WINGULL LANTURN TORPESQUID'),
      fish(26, 'MAGIKARP TENTACOOL | TENTACOOL FINNEON WAILMER | WAILMER CARVANHA SKRELP SHARPEDO TORPESQUID',
               'MAGIKARP CHINCHOU | CHINCHOU CARVANHA FINNEON | CARVANHA LANTURN SKRELP SHARPEDO TORPESQUID')),
    M('Route313', TOSA, 'South-west sea', 'surf 28', 'Deep south-west water: Wailmer pods, Mantine, sunken-wreck Dhelmise.',
      surf(28, 'TENTACOOL WINGULL WAILMER TENTACRUEL MANTINE',
               'TENTACOOL CHINCHOU WAILMER LANTURN MANTINE'),
      fish(28, 'MAGIKARP TENTACOOL | TENTACOOL WAILMER CLAUNCHER | WAILMER CLAUNCHER SHELLDER RELICANTH DHELMISE',
               'MAGIKARP CHINCHOU | CHINCHOU SHELLDER CLAUNCHER | LANTURN CLAWITZER SHELLDER RELICANTH DHELMISE')),
    M('Route314', TOSA, 'Shipping lane to Inka', 'surf 30', 'Shipping lane to the logistics hub: reef-killing Mareanie hitched in on hulls; Frillish at night.',
      surf(30, 'TENTACOOL PELIPPER WAILMER TENTACRUEL WAILORD',
               'TENTACOOL CHINCHOU WAILMER LANTURN FRILLISH'),
      fish(30, 'MAGIKARP TENTACOOL | TENTACOOL REMORAID FINNEON | OCTILLERY LUMINEON MAREANIE SHARPEDO TOXAPEX',
               'MAGIKARP CHINCHOU | CHINCHOU REMORAID FRILLISH | LANTURN FRILLISH MAREANIE SHARPEDO JELLICENT')),
    M('InkaSeawall', TOSA, 'Route 314 - Inka City', 'surf 32', 'Cold-storage seawall: Spheal, imported fugu Qwilfish, an escaped Pinguin.',
      surf(32, 'TENTACOOL WINGULL SPHEAL PELIPPER PINGUIN',
               'TENTACOOL SPHEAL CHINCHOU SEALEO LAPRAS'),
      fish(32, 'MAGIKARP TENTACOOL | SHELLDER REMORAID TENTACOOL | OCTILLERY QWILFISH ARROKUDA BARRASKEWDA CLOYSTER',
               'MAGIKARP CHINCHOU | CHINCHOU SHELLDER REMORAID | LANTURN QWILFISH OCTILLERY QWILFISH_HISUI CLOYSTER')),

    # ---------------- Towns / cities with water (water + fishing only) ----------------
    M('TelokTown', TOSA, 'Telok Town', '2-4 / surf 20', 'Starter town: gentle garden grass round Professor Palm\'s lab (user 2026-11-23: town grass gets a table matching the next route); quiet bay.',
      land((2, 4),
           'STARLY LOTAD WURMPLE PIKIPEK YUNGOOS SKWOVET LECHONK PIDGEY FLETCHLING SMOLIV MAREEP IYEPURE',
           'HOOTHOOT LOTAD WURMPLE SPINARAK RATTATA_ALOLA SKWOVET LECHONK ODDISH MAREEP VENONAT NICKIT IYEPURE'),
      surf(20, 'TENTACOOL WINGULL MANTYKE PELIPPER FINIZEN',
               'TENTACOOL CHINCHOU WINGULL MANTYKE LANTURN'),
      fish(20, 'MAGIKARP TENTACOOL | TENTACOOL FINNEON WISHIWASHI | WISHIWASHI REMORAID CORSOLA LUVDISC FINIZEN',
               'MAGIKARP CHINCHOU | CHINCHOU FINNEON WISHIWASHI | CHINCHOU REMORAID CORSOLA LUMINEON LANTURN')),
    M('TosaPort', TOSA, 'Tosa Port harbour', 'surf 20', 'Domestic port: ship-borne invasives (Buizel, Carvanha, Skrelp) and life-ring thief Torpesquid.',
      surf(20, 'TENTACOOL WINGULL BUIZEL PELIPPER WAILMER',
               'TENTACOOL CHINCHOU BUIZEL WINGULL LANTURN'),
      fish(20, 'MAGIKARP TENTACOOL | TENTACOOL FINNEON REMORAID | CARVANHA REMORAID SKRELP WAILMER TORPESQUID',
               'MAGIKARP CHINCHOU | CHINCHOU REMORAID FINNEON | CARVANHA REMORAID SKRELP LANTURN TORPESQUID')),
    M('WavebreakTown', TOSA, 'Wavebreak harbour', 'surf 24', 'Sailors\' harbour where the voyages leave: Horsea in the moorings.',
      surf(24, 'TENTACOOL WINGULL PELIPPER MANTYKE WAILMER',
               'TENTACOOL CHINCHOU WINGULL LANTURN MANTYKE'),
      fish(24, 'MAGIKARP TENTACOOL | TENTACOOL WAILMER HORSEA | HORSEA WAILMER CORSOLA SEADRA LUVDISC',
               'MAGIKARP CHINCHOU | CHINCHOU HORSEA WAILMER | HORSEA CORSOLA_GALAR LANTURN SEADRA SKRELP')),
    M('MoongroveCity', TOSA, 'Moongrove canals', 'surf 22', 'Mangrove city canals: catfish and crayfish; Purrchi snatch fish from the shallows.',
      surf(22, 'WOOPER LOTAD SURSKIT QUAGSIRE PURRCHI',
               'WOOPER LOTAD CHEWTLE QUAGSIRE PURRCHI'),
      fish(22, 'MAGIKARP BARBOACH | BARBOACH CORPHISH GOLDEEN | WHISCASH BARBOACH CORPHISH CRAWDAUNT STUNFISK',
               'MAGIKARP BARBOACH | BARBOACH CORPHISH CHEWTLE | WHISCASH BARBOACH CRAWDAUNT DREDNAW STUNFISK_GALAR')),
    M('TimahCity', TOSA, 'Timah garden ponds', 'surf 22', 'Orchid-garden ponds (koi Goldeen); map has no water yet.',
      surf(22, 'SURSKIT LOTAD MARILL MASQUERAIN LOMBRE',
               'LOTAD WOOPER MARILL LOMBRE MASQUERAIN'),
      fish(22, 'MAGIKARP GOLDEEN | GOLDEEN POLIWAG LUVDISC | SEAKING GOLDEEN POLIWHIRL BASCULIN FEEBAS',
               'MAGIKARP POLIWAG | POLIWAG GOLDEEN BARBOACH | SEAKING POLIWHIRL BARBOACH BASCULIN FEEBAS'),
      keep_without_tiles=True),
    M('ChanguCity', TOSA, 'Changu waterfront', 'surf 26', 'Business-district waterfront; map has no water yet.',
      surf(26, 'TENTACOOL WINGULL PELIPPER BUIZEL FLOATZEL',
               'TENTACOOL CHINCHOU BUIZEL PELIPPER LANTURN'),
      fish(26, 'MAGIKARP TENTACOOL | TENTACOOL ARROKUDA FINNEON | ARROKUDA WAILMER LUMINEON BARRASKEWDA BRUXISH',
               'MAGIKARP CHINCHOU | CHINCHOU ARROKUDA FINNEON | ARROKUDA LANTURN LUMINEON BARRASKEWDA BRUXISH'),
      keep_without_tiles=True),
    M('JuranCity', TOSA, 'Juran marina', 'surf 30', 'Luxury marina: Luvdisc and gold-scaled show fish; map has no water yet.',
      surf(30, 'TENTACOOL WINGULL FINIZEN PELIPPER LUVDISC',
               'TENTACOOL CHINCHOU WINGULL LANTURN LUVDISC'),
      fish(30, 'MAGIKARP LUVDISC | LUVDISC FINNEON REMORAID | LUMINEON OCTILLERY ALOMOMOLA RELICANTH GYARADOS',
               'MAGIKARP CHINCHOU | CHINCHOU LUVDISC REMORAID | LANTURN OCTILLERY ALOMOMOLA RELICANTH GYARADOS'),
      keep_without_tiles=True),
    M('CorralCity', TOSA, 'Corral beach + marina', 'surf 30', 'Pokétopia beach reef near Marina\'s gym: Staryu, Corsola, Pyukumuku; Torpesquid.',
      surf(30, 'TENTACOOL WINGULL FINIZEN PELIPPER MANTINE',
               'TENTACOOL CHINCHOU WINGULL LANTURN MANTINE'),
      fish(30, 'MAGIKARP LUVDISC | CORSOLA LUVDISC STARYU | STARYU CORSOLA MAREANIE PYUKUMUKU TORPESQUID',
               'MAGIKARP CHINCHOU | STARYU CORSOLA CHINCHOU | STARYU CORSOLA_GALAR MAREANIE PYUKUMUKU TORPESQUID')),
    M('PoketopiaGate', TOSA, 'Pokétopia Gate shore', 'surf 30', 'Resort-island ferry shore: Wishiwashi schools, a rare Lapras.',
      surf(30, 'TENTACOOL WINGULL FINIZEN PELIPPER LAPRAS',
               'TENTACOOL CHINCHOU WINGULL LANTURN LAPRAS'),
      fish(30, 'MAGIKARP TENTACOOL | TENTACOOL FINNEON WISHIWASHI | WISHIWASHI LUMINEON BRUXISH SHARPEDO DHELMISE',
               'MAGIKARP CHINCHOU | CHINCHOU FINNEON WISHIWASHI | WISHIWASHI LANTURN BRUXISH SHARPEDO DHELMISE')),
    M('ChallengerGate', TOSA, 'Challenger Gate lake', 'surf 42', 'Mountain lake below the League; map has no water yet.',
      surf(42, 'GOLDUCK AZUMARILL QUAGSIRE SWANNA DRAGONAIR',
               'GOLDUCK QUAGSIRE AZUMARILL POLITOED DRAGONAIR'),
      fish(42, 'MAGIKARP GOLDEEN | SEAKING POLIWHIRL GOLDEEN | SEAKING WHISCASH GYARADOS DRAGONAIR MILOTIC',
               'MAGIKARP POLIWAG | POLIWHIRL SEAKING BARBOACH | WHISCASH SEAKING GYARADOS DRAGONAIR POLITOED'),
      keep_without_tiles=True),

    # ================= TIKSI (post-game, Lv 50-65) =================
    M('DrakeBaseCamp', TIKSI, 'Drake Base Camp meadows', '55-58', 'Climbers\' camp on the plateau below Mt. Drake: grazing Gogoat and Bouffalant, Torkoal by the vents (user 2026-11-23: town grass gets a table matching the next route).',
      land((55, 58),
           'FEAROW SKARMORY GOGOAT BOUFFALANT SAWSBUCK LYCANROC ALTARIA BRAVIARY TORKOAL CAMERUPT SANDSLASH DRAMPA',
           'NOCTOWL SKARMORY GOGOAT BOUFFALANT SAWSBUCK LYCANROC ALTARIA HONCHKROW TORKOAL CAMERUPT MIGHTYENA NOIVERN')),
    M('FurongVillage', TIKSI, 'Furong fishing village', 'surf 50', 'Fishing village where the smuggling boat lands: Seadra and Octillery for the nets.',
      surf(50, 'TENTACRUEL PELIPPER WAILMER MANTINE LAPRAS',
               'TENTACRUEL LANTURN PELIPPER MANTINE LAPRAS'),
      fish(50, 'MAGIKARP TENTACOOL | SEADRA TENTACRUEL OCTILLERY | OCTILLERY SHARPEDO WAILORD BARRASKEWDA KINGDRA',
               'MAGIKARP CHINCHOU | LANTURN SEADRA OCTILLERY | LANTURN SHARPEDO DHELMISE JELLICENT KINGDRA')),
    M('Route401', TIKSI, 'Furong - west coast', '50-54', 'Warm arid scrub along Tiksi\'s south coast: Sandslash, Maractus, Krokorok.',
      land((50, 54),
           'FEAROW SANDSLASH KROKOROK MARACTUS DUGTRIO HIPPOWDON TAUROS ZEBSTRIKA DONPHAN SANDACONDA MANDIBUZZ GARGANACL',
           'NOCTOWL SANDSLASH KROKOROK MARACTUS DUGTRIO HIPPOWDON MIGHTYENA ZEBSTRIKA DONPHAN SANDACONDA HONCHKROW ZOROARK')),
    M('Route410', TIKSI, 'Hidden locals\' path', '51-54', 'Well-concealed route (only 2 grass tiles): masters of disguise - Kecleon, Ditto, Zoroark, Mimikyu.',
      land((51, 54),
           'KECLEON KECLEON DITTO SHUCKLE SMEARGLE SPINDA CHATOT SUDOWOODO ZOROARK MIMIKYU CHANSEY AUDINO',
           'KECLEON MISMAGIUS DITTO SHUCKLE SMEARGLE SPINDA BANETTE SUDOWOODO ZOROARK MIMIKYU CHANSEY SPIRITOMB')),
    M('TanobyDelta', TIKSI, 'Tanoby Delta', 'surf 52', 'River delta round the Sevii-built ruin: ancient Relicanth, Hisuian Basculegion.',
      surf(52, 'QUAGSIRE PELIPPER FLOATZEL GOLDUCK RELICANTH',
               'QUAGSIRE LANTURN FLOATZEL GOLDUCK RELICANTH'),
      fish(52, 'MAGIKARP BARBOACH | WHISCASH SEAKING BARBOACH | WHISCASH GYARADOS BARRASKEWDA RELICANTH BASCULEGION',
               'MAGIKARP BARBOACH | WHISCASH BARBOACH LANTURN | WHISCASH LANTURN BASCULEGION RELICANTH DHELMISE')),
    M('Route407', TIKSI, 'Route 401 - Ube City', '52-55', 'Dry savanna: Zebstrika, Donphan, Pyroar prides.',
      land((52, 55),
           'FEAROW ZEBSTRIKA DONPHAN GIRAFARIG TAUROS RHYDON PYROAR KROKOROK HIPPOWDON HEATMOR DURANT FARIGIRAF',
           'NOCTOWL ZEBSTRIKA DONPHAN GIRAFARIG MIGHTYENA RHYDON PYROAR KROKOROK HIPPOWDON HEATMOR DURANT ZOROARK')),
    M('Route402', TIKSI, 'Route 401 - Mt. Drake', '52-56', 'Rocky foothills of Mt. Drake: Skarmory, Lycanroc, a rare Drampa.',
      land((52, 56),
           'FEAROW GRAVELER PRIMEAPE GOGOAT RHYDON SKARMORY LYCANROC KROKOROK HAWLUCHA PANGORO FLYGON DRAMPA',
           'NOCTOWL GRAVELER PRIMEAPE GOGOAT RHYDON SKARMORY LYCANROC_MIDNIGHT KROKOROK HOUNDOOM PANGORO FLYGON DRAMPA')),
    M('Route405', TIKSI, 'Route 404 - Ube farmland', '54-57', 'Farmland near Ube City and the Silph Co. office: Miltank, Ditto and an escaped Porygon2.',
      land((54, 57),
           'STARAPTOR FURRET TAUROS MILTANK OINKOLOGNE BELLOSSOM GOGOAT SAWSBUCK MAGNETON GRUMPIG DITTO PORYGON2',
           'NOCTOWL FURRET TAUROS MIGHTYENA OINKOLOGNE VILEPLUME GOGOAT SAWSBUCK MAGNETON GRUMPIG DITTO PORYGON2')),
    M('MtDrake_1F', TIKSI, 'Mt. Drake caves', '56-59', 'Volcanic dragon mountain: Torkoal vents, Gabite and Druddigon; ghost-dragon Drakloak.',
      cave((56, 59),
           'GOLBAT GRAVELER BOLDORE ONIX KROKOROK GABITE TORKOAL DRUDDIGON SHELGON MAGCARGO FRAXURE DRAKLOAK',
           'GOLBAT GRAVELER BOLDORE ONIX KROKOROK GABITE SABLEYE DRUDDIGON SHELGON DUSCLOPS FRAXURE DRAKLOAK')),
    M('Route404', TIKSI, 'Drake Base Camp plateau', '56-59', 'High plateau linking the Drake routes: Bouffalant, Braviary, Altaria.',
      land((56, 59),
           'FEAROW SKARMORY GOGOAT BOUFFALANT SAWSBUCK LYCANROC TAUROS_PALDEA_BLAZE ALTARIA BRAVIARY DRAMPA FLYGON NOIVERN',
           'NOCTOWL SKARMORY GOGOAT BOUFFALANT SAWSBUCK LYCANROC_MIDNIGHT MIGHTYENA ALTARIA MANDIBUZZ DRAMPA HOUNDOOM NOIVERN')),
    M('Route406', TIKSI, 'Route 404 - Tanglyn', '56-59', 'Long northern ridge to the mural town: ancient Sigilyph and Bronzong.',
      land((56, 59),
           'STARAPTOR KILOWATTREL SKARMORY SAWSBUCK BOUFFALANT GOGOAT SIGILYPH MEDICHAM BRONZONG ALTARIA BRAVIARY ESPATHRA',
           'NOCTOWL KILOWATTREL SKARMORY SAWSBUCK BOUFFALANT MIGHTYENA SIGILYPH MEDICHAM BRONZONG BANETTE BRAVIARY ABSOL')),
    M('GavaniPath', TIKSI, 'Gavani Path (Regileki)', '57-60', 'Electromagnetic cave: Magneton, Galvantula, Eelektrik in the charged rock. No Regileki (static).',
      cave((57, 60),
           'GOLBAT MAGNETON BOLDORE ELECTRODE GALVANTULA PROBOPASS EELEKTRIK KLANG LUXRAY TOXTRICITY ROTOM MAGNEZONE',
           'GOLBAT MAGNETON BOLDORE ELECTRODE GALVANTULA PROBOPASS EELEKTRIK SABLEYE LUXRAY TOXTRICITY_LOW_KEY ROTOM MAGNEZONE')),
    M('TanglynTown', TIKSI, 'Tanglyn shore', 'surf 55', 'Mural town shore: Relicanth from the old stories.',
      surf(55, 'TENTACRUEL PELIPPER WAILMER MANTINE RELICANTH',
               'TENTACRUEL LANTURN WAILMER JELLICENT RELICANTH'),
      fish(55, 'MAGIKARP TENTACOOL | OCTILLERY CLAWITZER TENTACRUEL | CLAWITZER BARRASKEWDA OCTILLERY RELICANTH DHELMISE',
               'MAGIKARP CHINCHOU | LANTURN CLAWITZER OCTILLERY | LANTURN BARRASKEWDA JELLICENT RELICANTH DHELMISE')),
    M('MtDrake_2F', TIKSI, 'Mt. Drake caves', '58-61', 'Middle galleries: Steelix, Zweilous, Fraxure.',
      cave((58, 61),
           'GOLBAT GRAVELER BOLDORE STEELIX GABITE SHELGON TORKOAL DRUDDIGON FRAXURE ZWEILOUS GOLEM DRAKLOAK',
           'GOLBAT GRAVELER BOLDORE STEELIX GABITE SHELGON SABLEYE DRUDDIGON FRAXURE ZWEILOUS DUSCLOPS DRAKLOAK')),
    M('Route408', TIKSI, 'Tanglyn - Route 409 coast', '58-61 / surf 58', 'North coast turning cold: Abomasnow, Delibird, dawn flocks of Pinguin.',
      land((58, 61),
           'STARAPTOR ABOMASNOW SAWSBUCK DELIBIRD CRAMORANT KILOWATTREL PILOSWINE VANILLISH CETITAN ALTARIA PINGUIN FROSMOTH',
           'NOCTOWL ABOMASNOW SAWSBUCK DELIBIRD SNEASEL KILOWATTREL PILOSWINE VANILLISH CETITAN FROSLASS PINGUIN WEAVILE'),
      surf(58, 'TENTACRUEL PELIPPER SEALEO DEWGONG LAPRAS',
               'TENTACRUEL LANTURN SEALEO DEWGONG LAPRAS'),
      fish(58, 'MAGIKARP TENTACOOL | SHELLDER TENTACRUEL OCTILLERY | CLOYSTER OCTILLERY BARRASKEWDA KINGDRA GYARADOS',
               'MAGIKARP CHINCHOU | SHELLDER LANTURN OCTILLERY | CLOYSTER LANTURN BARRASKEWDA KINGDRA GYARADOS')),
    M('Route403', TIKSI, 'Mt. Drake west - Regolis desert', '59-62', 'Desert to the Regirock shrine: Krookodile, Flygon, ancient Golurk and Claydol; mummies at night.',
      land((59, 62),
           'SANDSLASH MARACTUS KROOKODILE HIPPOWDON DUGTRIO SANDACONDA FLYGON GARGANACL GOLURK TORKOAL CLAYDOL GARCHOMP',
           'SANDSLASH CACTURNE KROOKODILE HIPPOWDON DUGTRIO SANDACONDA FLYGON GARGANACL GOLURK COFAGRIGUS CLAYDOL RUNERIGUS')),
    M('FerrumShrine', TIKSI, 'Ferrum Shrine (Registeel)', '60-63', 'Iron-cored shrine: Steel types only. No Registeel (static).',
      cave((60, 63),
           'GOLBAT LAIRON BRONZONG KLANG MAGNETON METANG AGGRON PROBOPASS DURANT EXCADRILL KLINKLANG COPPERAJAH',
           'GOLBAT LAIRON BRONZONG KLANG MAGNETON METANG AGGRON SABLEYE DURANT DOUBLADE KLINKLANG COPPERAJAH')),
    M('MtDrake_3F', TIKSI, 'Mt. Drake upper caves', '60-63', 'Upper caves under the peak: Noivern roosts, rare Salamence and Garchomp.',
      cave((60, 63),
           'GOLBAT GOLEM GIGALITH STEELIX GABITE SHELGON DRUDDIGON FRAXURE ZWEILOUS NOIVERN SALAMENCE GARCHOMP',
           'GOLBAT GOLEM GIGALITH STEELIX GABITE SHELGON DRUDDIGON SABLEYE ZWEILOUS NOIVERN DUSCLOPS DRAKLOAK')),
    M('RegolisShrine', TIKSI, 'Regolis Shrine (Regirock)', '61-64', 'Desert shrine of stone: Golurk, Claydol, monolith Stonjourner. No Regirock (static).',
      cave((61, 64),
           'GOLBAT BOLDORE GRAVELER CLAYDOL SANDSLASH GOLURK RHYDON GIGALITH CARBINK GOLEM STONJOURNER SUDOWOODO',
           'GOLBAT BOLDORE GRAVELER CLAYDOL SANDSLASH GOLURK RHYDON SABLEYE CARBINK COFAGRIGUS STONJOURNER RUNERIGUS')),
    M('Route409', TIKSI, 'Frozen route', '61-64 / surf 61', 'Strangely frozen route (Regice\'s chill): Pinguin flocks crow at dawn, Glalie, Avalugg, rare Arctibax. Night is harsher.',
      land((61, 64),
           'PINGUIN PILOSWINE SNEASEL VANILLISH BEARTIC GLALIE ABOMASNOW CETITAN FROSMOTH AVALUGG MAMOSWINE ARCTIBAX',
           'SNEASEL PILOSWINE FROSLASS VANILLISH BEARTIC GLALIE ABOMASNOW WEAVILE FROSMOTH AVALUGG PINGUIN ARCTIBAX',
           night_rate=25, night_lv=(62, 65)),
      surf(61, 'SEALEO TENTACRUEL DEWGONG WALREIN LAPRAS',
               'SEALEO DEWGONG LANTURN WALREIN LAPRAS'),
      fish(61, 'MAGIKARP SHELLDER | SHELLDER OCTILLERY TENTACRUEL | CLOYSTER OCTILLERY BARRASKEWDA KINGDRA WISHIWASHI',
               'MAGIKARP CHINCHOU | SHELLDER LANTURN OCTILLERY | CLOYSTER LANTURN BARRASKEWDA KINGDRA JELLICENT')),
    M('FrigoCave_Exterior', TIKSI, 'Frigo Cave cove', '61-64 / surf 61', 'Icy north-shore cove outside Regice\'s cave: Cryogonal and Walrein.',
      land((61, 64),
           'PINGUIN SNEASEL SEALEO VANILLISH BEARTIC GLALIE CETITAN CRYOGONAL AVALUGG WALREIN MAMOSWINE ARCTIBAX',
           'SNEASEL PINGUIN SEALEO FROSLASS BEARTIC GLALIE WEAVILE CRYOGONAL AVALUGG WALREIN MAMOSWINE ARCTIBAX',
           night_rate=25),
      surf(61, 'SEALEO DEWGONG PELIPPER WALREIN LAPRAS',
               'SEALEO DEWGONG LANTURN WALREIN LAPRAS'),
      fish(61, 'MAGIKARP SHELLDER | SHELLDER OCTILLERY TENTACRUEL | CLOYSTER OCTILLERY BARRASKEWDA KINGDRA LAPRAS',
               'MAGIKARP CHINCHOU | SHELLDER LANTURN OCTILLERY | CLOYSTER LANTURN BARRASKEWDA KINGDRA LAPRAS')),
    M('FrigoCave', TIKSI, 'Frigo Cave (Regice)', '62-65', 'Deep ice cave: Glalie, Vanilluxe, Cryogonal, Arctibax. No Regice (static).',
      cave((62, 65),
           'GOLBAT SNEASEL GLALIE VANILLUXE CRYOGONAL BEARTIC AVALUGG PILOSWINE WALREIN MAMOSWINE ARCTIBAX ABOMASNOW',
           'GOLBAT SNEASEL GLALIE VANILLUXE CRYOGONAL FROSLASS AVALUGG PILOSWINE WEAVILE MAMOSWINE ARCTIBAX SABLEYE')),
    M('MtDrakeSummit', TIKSI, 'Mt. Drake summit (Regidrago)', '63-65', 'Summit chamber carved by an ancient maw: dragons of every region. No Regidrago (static).',
      cave((63, 65),
           'GOLBAT GABITE SHELGON ZWEILOUS DRUDDIGON FRAXURE FLYGON ALTARIA SLIGGOO DRAMPA HAKAMO_O GARCHOMP',
           'GOLBAT GABITE SHELGON ZWEILOUS DRUDDIGON FRAXURE DRAKLOAK NOIVERN SLIGGOO DRAMPA HAKAMO_O HYDREIGON@64-65')),
]


# ---------------------------------------------------------------------------------------------
# Map data
# ---------------------------------------------------------------------------------------------
def read_json(p):
    with open(p) as f:
        return json.load(f)


def region_sections():
    ref = ROOT / 'dev_scripts/orchid_ui/ref'
    tosa = set(re.findall(r'`(MAPSEC_\w+)`', (ref / 'tosa_places.md').read_text()))
    tiksi = set(re.findall(r'`(MAPSEC_\w+)`', (ref / 'tiksi_places.md').read_text()))
    return tosa, tiksi


def owned_maps():
    """Map folder -> map.json for every Tosa/Tiksi map (whose encounter entries this script owns)."""
    groups = read_json(ROOT / 'data/maps/map_groups.json')
    tosa, tiksi = region_sections()
    out = {}
    for g in groups['group_order']:
        if g in NEVER_OWN_GROUPS:
            continue
        for m in groups[g]:
            j = read_json(ROOT / f'data/maps/{m}/map.json')
            if g in TOSA_GROUPS | TIKSI_GROUPS or j['region_map_section'] in tosa | tiksi:
                out[m] = j
    return out


class Terrain:
    """Counts encounter-capable metatiles in a map's layout."""
    def __init__(self):
        beh = (ROOT / 'include/constants/metatile_behaviors.h').read_text()
        body = beh[beh.index('{'):beh.index('}')]
        self.mb = {}
        val = -1
        for line in body.splitlines():
            m = re.match(r'\s*(MB_\w+)(\s*=\s*(\w+))?', line)
            if m:
                val = int(m.group(3), 0) if m.group(3) else val + 1
                self.mb[val] = m.group(1)
        src = (ROOT / 'src/metatile_behavior.c').read_text()
        table = src.split('sTileBitAttributes')[1].split('};')[0]
        self.flags = {m.group(1): m.group(2) for m in re.finditer(r'\[(MB_\w+)\]\s*=\s*([^,\n]+)', table)}
        headers = (ROOT / 'src/data/tilesets/headers.h').read_text()
        self.ts_attr = {}
        for m in re.finditer(r'const struct Tileset (gTileset_\w+)\s*=\s*\{(.*?)\};', headers, re.S):
            self.ts_attr[m.group(1)] = re.search(r'\.metatileAttributes\s*=\s*(\w+)', m.group(2)).group(1)
        metatiles = (ROOT / 'src/data/tilesets/metatiles.h').read_text()
        self.attr_path = {m.group(2): (m.group(3), int(m.group(1))) for m in re.finditer(
            r'const u(16|32) (gMetatileAttributes_\w+)\[\]\s*=\s*INCBIN_U(?:16|32)\("([^"]+)"\)', metatiles)}
        self.layouts = {l['id']: l for l in read_json(ROOT / 'data/layouts/layouts.json')['layouts'] if 'id' in l}
        self._cache = {}

    def attrs(self, ts):
        if ts not in self._cache:
            path, width = self.attr_path[self.ts_attr[ts]]
            data = (ROOT / path).read_bytes()
            if width == 16:
                self._cache[ts] = [x & 0xFF for x in struct.unpack('<%dH' % (len(data) // 2), data)]
            else:
                self._cache[ts] = [x & 0x1FF for x in struct.unpack('<%dI' % (len(data) // 4), data)]
        return self._cache[ts]

    def scan(self, mapjson):
        lay = self.layouts[mapjson['layout']]
        nprim = 640 if lay.get('layout_version') == 'frlg' else 512
        prim, sec = self.attrs(lay['primary_tileset']), self.attrs(lay['secondary_tileset'])
        data = (ROOT / lay['blockdata_filepath']).read_bytes()
        land, water = Counter(), Counter()
        for b in struct.unpack('<%dH' % (len(data) // 2), data):
            mid = b & 0x3FF
            a, i = (prim, mid) if mid < nprim else (sec, mid - nprim)
            name = self.mb.get(a[i] if i < len(a) else 0, '?')
            f = self.flags.get(name, '')
            if 'HAS_ENCOUNTERS' in f:
                (water if 'SURFABLE' in f else land)[name] += 1
        rocks = sum(1 for o in mapjson.get('object_events', []) if 'BREAKABLE_ROCK' in o.get('graphics_id', ''))
        return {'land_mons': sum(land.values()), 'water_mons': sum(water.values()),
                'fishing_mons': sum(water.values()), 'rock_smash_mons': rocks,
                'detail': dict(land, **water, rocks=rocks)}


def species_names():
    text = (ROOT / 'include/constants/species.h').read_text()
    return set(re.findall(r'^\s*(SPECIES_\w+)\s*[=,]', text, re.M)) - {'SPECIES_NONE'}


# ---------------------------------------------------------------------------------------------
# Building entries
# ---------------------------------------------------------------------------------------------
def parse(spec):
    out = []
    for tok in spec.replace('|', ' ').split():
        lv = None
        if '@' in tok:
            tok, l = tok.split('@')
            lo, _, hi = l.partition('-')
            lv = (int(lo), int(hi or lo))
        out.append(('SPECIES_' + tok if not tok.startswith('SPECIES_') else tok, lv))
    return out


def slot_levels(t, lv):
    if t.method == 'fishing_mons':
        return rods(lv)
    lo, hi = lv
    n = SLOTS[t.method]
    if t.method == 'land_mons':
        return [(lo, hi)] * 8 + [(lo + RARE_BUMP, hi + RARE_BUMP)] * 4
    return [(lo, hi)] * n


def build(t, night):
    mons = parse(t.night if night else t.day)
    lv = t.night_lv if night else t.lv
    levels = slot_levels(t, lv)
    entries = []
    for (species, override), (lo, hi) in zip(mons, levels):
        lo, hi = override or (lo, hi)
        lo, hi = min(lo, LEVEL_CAP), min(hi, LEVEL_CAP)
        entries.append({'min_level': lo, 'max_level': hi, 'species': species})
    return {'encounter_rate': t.night_rate if night else t.rate, 'mons': entries}


def validate(maps, species, errors):
    seen = set()
    for m in maps:
        if m.name in seen:
            errors.append(f'{m.name}: listed twice')
        seen.add(m.name)
        for label in (m.label, m.label + '_Night'):
            words = [w for w in TIME_WORDS if w in label]
            if words != (['Night'] if label.endswith('_Night') else []):
                errors.append(f'{label}: contains time-of-day word(s) {words}')
            if 'FireRed' in label or 'LeafGreen' in label:
                errors.append(f'{label}: FireRed/LeafGreen in a label switches its #ifdef')
        for t in m.tables.values():
            day, night = parse(t.day), parse(t.night)
            for which, mons in (('day', day), ('night', night)):
                if len(mons) != SLOTS[t.method]:
                    errors.append(f'{m.name} {t.method} {which}: {len(mons)} slots, need {SLOTS[t.method]}')
                for s, lv in mons:
                    if s not in species:
                        errors.append(f'{m.name} {t.method} {which}: unknown species {s}')
                    if lv and not (1 <= lv[0] <= lv[1] <= 100):
                        errors.append(f'{m.name} {t.method} {which}: bad levels {s}@{lv}')
            d, n = {s for s, _ in day}, {s for s, _ in night}
            if len(d & n) / len(n) < 0.4:
                errors.append(f'{m.name} {t.method}: day/night overlap {len(d & n)}/{len(n)} < 40%')


def generate(check_only=False):
    data = read_json(JSON_PATH)
    group = next(g for g in data['wild_encounter_groups'] if g['label'] == 'gWildMonHeaders')
    owned = owned_maps()
    terrain = Terrain()
    errors, warnings, skipped = [], [], []
    validate(MAPS, species_names(), errors)

    new_entries, readme_rows = [], []
    for m in MAPS:
        if m.name not in owned:
            errors.append(f'{m.name}: not a Tosa/Tiksi map folder')
            continue
        mj = owned[m.name]
        tiles = terrain.scan(mj)
        methods = []
        for meth in METHOD_ORDER:
            if meth not in m.tables:
                continue
            if tiles[meth] or m.keep_without_tiles:
                if not tiles[meth]:
                    warnings.append(f'{m.name}: {meth} kept with no matching terrain (keep_without_tiles)')
                methods.append(meth)
            else:
                warnings.append(f'{m.name}: {meth} dropped - no matching terrain')
        if not methods:
            skipped.append(m.name)
            continue
        for night in (False, True):
            e = {'map': mj['id'], 'base_label': m.label + ('_Night' if night else '')}
            for meth in methods:
                e[meth] = build(m.tables[meth], night)
            new_entries.append(e)
        readme_rows.append((m, methods, tiles))

    # terrain with no table (towns etc.) - reported, not filled
    specs = {m.name: m for m in MAPS}
    untabled = []
    for name, mj in owned.items():
        if mj['map_type'] == 'MAP_TYPE_INDOOR':
            continue
        t = terrain.scan(mj)
        missing = [meth for meth in ('land_mons', 'water_mons', 'rock_smash_mons')
                   if t[meth] and (name not in specs or meth not in specs[name].tables)]
        if missing:
            untabled.append(f'{name} ({mj["map_type"]}): no {"/".join(missing)} table; terrain {t["detail"]}')

    owned_ids = {mj['id'] for mj in owned.values()}
    old = group['encounters']
    removed = [e['base_label'] for e in old if e['map'] in owned_ids]
    insert_at = next((i for i, e in enumerate(old) if e['map'] in owned_ids), len(old))
    kept = [e for e in old if e['map'] not in owned_ids]  # nothing before insert_at is owned
    group['encounters'] = kept[:insert_at] + new_entries + kept[insert_at:]

    for w in warnings:
        print('warning:', w)
    for s in skipped:
        print('skipped (no encounter terrain):', s)
    for u in untabled:
        print('no table (has terrain):', u)
    print(f'replaced {len(removed)} existing Tosa/Tiksi entries')
    n_tosa = sum(1 for m, _, _ in readme_rows if m.region == TOSA)
    n_tiksi = sum(1 for m, _, _ in readme_rows if m.region == TIKSI)
    print(f'wrote {len(new_entries)} entries for {len(readme_rows)} maps (Tosa {n_tosa}, Tiksi {n_tiksi})')
    if errors:
        for e in errors:
            print('ERROR:', e)
        sys.exit(1)
    if check_only:
        return
    with open(JSON_PATH, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')
    write_readme(readme_rows, skipped, untabled)


# ---------------------------------------------------------------------------------------------
# README
# ---------------------------------------------------------------------------------------------
def pretty(s):
    s = s[len('SPECIES_'):] if s.startswith('SPECIES_') else s
    return s.replace('_', '-').title().replace('-Alola', ' (Alola)').replace('-Galar', ' (Galar)') \
        .replace('-Paldea', ' (Paldea)').replace('-Hisui', ' (Hisui)')


def highlights(m):
    day, night = [], []
    for t in m.tables.values():
        d = [s for s, _ in parse(t.day)]
        n = [s for s, _ in parse(t.night)]
        day += [s for s in d if s not in n and s not in day]
        night += [s for s in n if s not in d and s not in night]
    return ', '.join(pretty(s) for s in day[:6]) or '-', ', '.join(pretty(s) for s in night[:6]) or '-'


def write_readme(rows, skipped, untabled):
    short = {'land_mons': 'land', 'water_mons': 'surf', 'rock_smash_mons': 'rock smash', 'fishing_mons': 'fish'}
    lines = [
        '# Orchid wild encounters (placeholder pass)',
        '',
        'Generated by `encounters.py` in this folder - edit the `MAPS` spec there and re-run',
        '`python3 dev_scripts/orchid_encounters/encounters.py`; it rewrites the Tosa/Tiksi entries of',
        '`src/data/wild_encounters.json` and this README. `--check` validates without writing.',
        '',
        'Every map has a day table (`g<Map>`, also used for morning and evening) and a night table',
        '(`g<Map>_Night`). Levels follow travel distance from Telok Town; water and fishing are levelled',
        'by when Surf / rods become usable. Tiksi is post-game (Lv 50-65). Regi shrines have themed',
        'tables but no Regis (those are static encounters). "Day only" / "Night only" list species',
        'that appear in one table and not the other.',
        '',
        '| Map | Area | Levels | Methods | Theme | Day only | Night only |',
        '|---|---|---|---|---|---|---|',
    ]
    for region in (TOSA, TIKSI):
        lines.append(f'| **{region}** | | | | | | |')
        for m, methods, _ in rows:
            if m.region != region:
                continue
            d, n = highlights(m)
            flag = ' (kept, no terrain yet)' if m.keep_without_tiles else ''
            lines.append(f'| {m.name} | {m.area} | {m.levels} | {", ".join(short[x] for x in methods)}{flag} | '
                         f'{m.note} | {d} | {n} |')
    lines += ['', '## Specs waiting for terrain', '',
              'These maps have a spec but no encounter metatiles yet, so no table is written.',
              'Paint grass / cave floor (or add water) and re-run the script to switch them on.', '']
    lines += [f'- {s}' for s in skipped] or ['- none']
    lines += ['', '## Encounter terrain with no table', '',
              'Left empty on purpose (towns get water/fishing only). Add a spec if they should have one.', '']
    lines += [f'- {u}' for u in untabled] or ['- none']
    lines += ['', '## Slot rates', '',
              '- land: 20 20 10 10 10 10 5 5 4 4 1 1 (slots 8-11 get +1 level)',
              '- surf / rock smash: 60 30 5 4 1',
              '- fishing: Old Rod 70 30, Good Rod 60 20 20, Super Rod 40 40 15 4 1',
              '- rod levels for water tier t: Old t/2-2..t/2+3 (min 5-8), Good t-10..t-2, Super t..t+6', '']
    README_PATH.write_text('\n'.join(lines))


if __name__ == '__main__':
    generate(check_only='--check' in sys.argv)
