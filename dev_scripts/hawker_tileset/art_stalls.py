"""Cuisine-specific art: sign icons, counter displays, kitchen kit and wall props for 8 stalls.

Every piece is a top-layer overlay in its stall's palette (see kit.stall_pal). Greys available
in every stall palette: K (outline), d, l, W. Sign ramp letters: a/A/h (ramp A) or g/G/j (ramp B).
"""
from kit import Art, art, P1, P2, P3, P4

RAMP = {"A": dict(s="a", S="A", i="h"), "B": dict(s="g", S="G", i="j")}

# ------------------------------------------------------------------ signboard (48x16, 3 tiles)
SIGN_L = """
................
KKKKKKKKKKKKKKKK
Kiiiiiiiiiiiiiii
KSSSSSSSSSSSSSSS
KSSSSSSSSSSSSSSS
KSSWWWSWWWSWWWSS
KSSWWWSWWWSWWWSS
KSSWWWSWWWSWWWSS
KSSWWWSWWWSWWWSS
KSSSSSSSSSSSSSSS
KSSSSSSSSSSSSSSS
KSSiiiiiSiiiiSSS
KSSSSSSSSSSSSSSS
Ksssssssssssssss
KKKKKKKKKKKKKKKK
"""
SIGN_R = """
................
KKKKKKKKKKKKKKKK
iiiiiiiiiiiiiiiK
SSSSSSSSSSSSSSSK
SSSSSSSSSSSSSSSK
SSWWWSWWWSWWWSSK
SSWWWSWWWSWWWSSK
SSWWWSWWWSWWWSSK
SSWWWSWWWSWWWSSK
SSSSSSSSSSSSSSSK
SSSSSSSSSSSSSSSK
SSSiiiSiiiiiiSSK
SSSSSSSSSSSSSSSK
sssssssssssssssK
KKKKKKKKKKKKKKKK
"""
SIGN_M = """
................
KKKKKKKKKKKKKKKK
iiiiiiiiiiiiiiii
sSWWWWWWWWWWWWSs
sWWWWWWWWWWWWWWs
sWWWWWWWWWWWWWWs
sWWWWWWWWWWWWWWs
sWWWWWWWWWWWWWWs
sWWWWWWWWWWWWWWs
sWWWWWWWWWWWWWWs
sWWWWWWWWWWWWWWs
sWWWWWWWWWWWWWWs
sSWWWWWWWWWWWWSs
ssssssssssssssss
KKKKKKKKKKKKKKKK
"""
STRIPE = """
................
................
................
................
................
................
................
................
................
................
SSSSSSSSSSSSSSSS
ssssssssssssssss
"""

# stove / prep table that most kit props stand on (6 rows)
TABLE = """
KKKKKKKKKKKKKKKK
KllllllllllllllK
KlddlllllllddllK
KllllllllllllllK
KllllllllllllldK
KKKKKKKKKKKKKKKK
"""
WOK = """
..2..........2..
..KKKKKKKKKKKK..
.Kn11h111h11nnK.
.Knn11h113nnnnK.
..KnnnnnnnnnnK..
.2.KnnnnnnnnK.2.
212.KKKKKKKK.212
.2.KllllllllK.2.
...KllllllldK...
...KlddddlldK...
...KllllllldK...
...KllllllldK...
...KKKKKKKKKK...
"""
RICE_POT = """
....d...d.......
.....d...d......
....d...d.......
...KKKKKKKKKK...
..KWWcWWWcWWWK..
..KlWWWWWWWWlK..
.KKllllllllllKK.
.KKllllllllldKK.
..KllllllllldK..
..KlSSSSSSSSdK..
..KllllllllldK..
..KdlllllllldK..
...KKKKKKKKKK...
"""


def hanging(bodies):
    """Three birds on hooks inside a glass case; each body string is 3 chars per row."""
    rows = [".KKKKKKKKKKKKKK.", "KWWWWWWWWWWWWllK", "KKKKKKKKKKKKKKKK"]
    for r in range(5):
        rows.append("Kl" + "ll".join(b[r] for b in bodies) + "K")
    rows += ["KddddddddddddddK", "KKKKKKKKKKKKKKKK"]
    return "\n".join(rows)


ROAST = ["lal", "hoa", "ooa", "oaa", "lal"]
POACHED = ["lal", "Wca", "cca", "caa", "lal"]

STALLS = [
    # ============================================================== curry (pal 9, ramp A)
    dict(
        name="Curry", leg=P1, ramp="A",
        icon="""
....d...d.....
.....d...d....
....d...d.....
.KKKKKKKKKKKK.
KAAhhAAAmAAAAK
KlAAAAGAAAAAlK
.KWWWWWWWWWlK.
.KWWWWWWWWllK.
..KKlllllKKK..
....KKKKKK....
""",
        cab_l="""
.KKKKKKKKKKKKKK.
KWWWWWWWWWWWWllK
KKKKKKKKKKKKKKKK
KlAAAAlYYYYlGGWK
KdAhAAdYcYYdGjGK
KdAAmAdYYBYdGGGK
KdmAAAdYYYYdgGGK
KllllllllllllllK
KddddddddddddddK
KKKKKKKKKKKKKKKK
""",
        cab_r="""
................
.......KKKKKKK..
.KKKK.KAAhAAAAKd
KcYccKKAAAmAAAKd
KYccYKKlAAAAAlK.
KcYccKKlllllldK.
KYccYKKlllllldK.
KcccYK.KllllldK.
KKKKKK..KKKKKK..
""",
        kit_l="""
....d......d....
...d......d.....
.KKKKKK..KKKKKK.
KAAhAAAKKYYcYYYK
KlAAAAlKKlYYYYlK
KllllldKKllllldK
.KlllldK.KlllldK
.KKKKKK..KKKKKK.
""" + TABLE,
        kit_r=RICE_POT, kit_r_subs={"S": "A"},
    ),
    # ============================================================== hokkien mee (pal 10, ramp A)
    dict(
        name="HokkienMee", leg=P2, ramp="A",
        icon="""
..............
....KKKKKK....
..KKAhAAhAKK..
.KAhAAprAAhAK.
.KAAhAppAhAAK.
KWWAAhAAAAGWWK
KlWWWAAAGjGWlK
.KllWWWWWWllK.
..KKKKKKKKKK..
..............
""",
        cab_l="""
................
....KKKKKKK.....
..KKAhAAAhAKK...
.KAAhApprAhAAK..
KWAhAAAppAAhAWK.
KWWAAhAAAAhGGWK.
KlWWWAAAAAGjGlK.
.KllWWWWWWWllK..
..KKKKKKKKKKK...
""",
        cab_r="""
................
..........KKKK..
.KKKKKKK..KrrK..
KWWWWWWWK.KrpK..
.KlllllK.KKKKKK.
KWWWWWWWKKlrrlK.
.KlllllK.KlrrlK.
KWWWWWWWKKlrrlK.
.KKKKKKK.KKKKKK.
""",
        kit_l=WOK, kit_l_subs={"1": "A", "3": "p", "2": "r"},
        kit_r="""
.KKKKKK..KKKKKK.
KpprpppKKcWcWccK
KprpprpKKWccWcWK
KllllldKKllllldK
.KKKKKK..KKKKKK.
""" + TABLE,
    ),
    # ============================================================== soft-shell crab (pal 11, ramp A)
    dict(
        name="Crab", leg=P3, ramp="A",
        icon="""
.aa........aa.
aAAa......aAAa
aAa........aAa
.aAa.aaaa.aAa.
..aAaAAAAaAa..
..aAAnAAnAAa..
.aaAhAAAAAAaa.
a.aAAAAAAAAa.a
.a.aaaaaaaa.a.
..............
""",
        cab_l="""
.KKKKKKKKKKKKKK.
KWWWWWWWWWWWWllK
KKKKKKKKKKKKKKKK
KUUUUUUUUUUUWUUK
KUuUUaUaUUuUUWUK
KUUaaAAAaaUUUUuK
KuUUaAnAaUUaAaUK
KUUaUaaaUaUUaUUK
KccccccccccccccK
KKKKKKKKKKKKKKKK
""",
        cab_r="""
................
.aAAa.KKK.aAAa..
..aAaKAAAKaAa...
.KKaAAAhAAAaKK..
KWoaAnAAAnAaoWK.
KWooaAAAAAaooWK.
KlWoooaaaoooWlK.
.KllWWWWWWWllK..
..KKKKKKKKKKK...
""",
        kit_l=WOK, kit_l_subs={"1": "A", "3": "o", "2": "o", "h": "o"},
        kit_r="""
....d....d......
.....d....d.....
..KKKKKKKKKKKK..
.KjjjjjjjjjjjjK.
.KGjGjGjGjGjGgK.
.KKKKKKKKKKKKKK.
.KjjjjjjjjjjjjK.
.KGjGjGjGjGjGgK.
.KKKKKKKKKKKKKK.
.KjjjjjjjjjjjjK.
.KGjGjGjGjGjGgK.
.KggggggggggggK.
..KKKKKKKKKKKK..
""",
    ),
    # ============================================================== chicken rice (pal 10, ramp B)
    dict(
        name="ChickenRice", leg=P2, ramp="B",
        icon="""
..............
.....aaaaa....
...aaooohoa...
..aooohhoooa..
.aooooooooooa.
.aoaooooooaoa.
..aaoaaaaoaa..
.KKKaKKKKaKKK.
..KWWWWWWWWK..
...KKKKKKKK...
""",
        cab_l=hanging([ROAST, POACHED, ROAST]),
        cab_r="""
................
....KKKKKKK.....
..KKWWcccccKK...
.KWWWcchccccWK..
KWWWWWcccooohWK.
KWGjGWWWooohoWK.
KlWGjGWWWoooWlK.
.KllWWWWWWWllK..
..KKKKKKKKKKK...
""",
        kit_l="""
..KKKKKKKKKKK...
.KohoooooooooK..
KooKKKKKoccchoK.
KooKllllKcchcoK.
KooKKKKKKnncooK.
.KooooooooooaK..
.KaaaaaaaaaaaK..
KKKKKKKKKKKKKKKK
KllllllllllllldK
KlddddddddddddlK
KKKKKKKKKKKKKKKK
""",
        kit_r=RICE_POT, kit_r_subs={"S": "G"},
        wall="""
................
KKKKKKKKKKKKKKKK
dddddddddddddddd
..a....a.....a..
.aoa..aca...aoa.
aohoa.acha.aohoa
aoooa.acca.aoooa
aoooa.acca.aoooa
.aaa..aaa...aaa.
""",
    ),
    # ============================================================== satay (pal 9, ramp B)
    dict(
        name="Satay", leg=P1, ramp="B",
        icon="""
..............
.BBbBBbBBb....
.YBbYBbYBbbbbb
..............
...BBbBBbBBb..
bbbYBbYBbYBb..
..............
.BBbBBbBBb....
.YBbYBbYBbbbbb
..............
""",
        cab_l="""
................
................
.KKKKKKKKK.KKKK.
KWBbBbBYYYKBBbBK
KWWbBbBBYYKBbBBK
KWbBbBBYYYKWBBWK
KlWWWWWWWlK.KKK.
.KlllllllK......
..KKKKKKK.......
""",
        cab_r="""
................
....KK....KK....
...KjGK..KjGK...
..KjGjGKKjGjGK..
.KGjGjGKKGjGjGK.
..KGjGgK.KGjGgK.
...KGgK...KGgK..
.KKKKKKKKKKKKKK.
KWWWWWWWWWWWWWlK
.KKKKKKKKKKKKKK.
""",
        kit_l="""
....d.....d.....
.....d...d......
................
KKKKKKKKKKKKKKKK
KBbBYBbBYBbBYBbK
KAmAAmAhmAAmAAmK
KBbBYBbBYBbBYBbK
KKKKKKKKKKKKKKKK
KllllllllllllldK
KlddddddddddddlK
KKKKKKKKKKKKKKKK
.Kd..........dK.
.Kd..........dK.
.KK..........KK.
""",
        kit_r="""
.....KKKKKK.....
....KBBbBBBK....
...KlBBBBbBlK...
...KllllllldK...
...KllllllldK...
....KllllldK....
....KKKKKKK.....
""" + TABLE,
        wall="""
................
KKKKKKKKKKKKKKKK
dddddddddddddddd
..K....K.....K..
..K...KjK....K..
.KjK.KjGjK..KjK.
KjGjKKGjGgKKjGjK
KGjgK.KGgK.KGjgK
.KgK...KK...KgK.
..K..........K..
""",
    ),
    # ============================================================== kopi & drinks (pal 11, ramp B)
    dict(
        name="Kopi", leg=P3, ramp="B",
        icon="""
....d..d......
.....d..d.....
....d..d......
..KKKKKKKK....
..KGGgGGGKKK..
..KWGGGGWK.K..
..KWWWWWWKKK..
..KlWWWWlK....
.KKKKKKKKKKK..
..KlllllllK...
""",
        cab_l="""
................
.KKKK.KKKK......
.KGGKKKjjKK.....
.KgGKKKjGKKKKKK.
.KGGK.KjjKGcGcGK
.KWWK.KWWKccGccK
.KKKK.KKKKGcGcGK
..........KKKKK.
""",
        cab_r="""
................
.KK..KK..KK..KK.
KllKKllKKllKKllK
KAAKKuuKKooKKAAK
KAhKKuUKKocKKAhK
KAAKKuuKKooKKAAK
KaaKKuuKKooKKaaK
KKKKKKKKKKKKKKKK
""",
        kit_l="""
......KKKK......
.....KllllK.....
..K..KKKKKK.....
.KlK.KlllldK.KK.
.KlKKKlllldKKlK.
..KllKlllldKlK..
...KKKlllldKK...
.....KlllldK....
.....KKKKKKK....
""" + TABLE,
        kit_r="""
.KKK.KKK.KKK....
.KWK.KWK.KWK.KK.
.KlK.KlK.KlKKAAK
.KWK.KWK.KWKKccK
.KlK.KlK.KlKKAAK
.KWK.KWK.KWKKuuK
.KKK.KKK.KKKKKKK
""" + TABLE,
    ),
    # ============================================================== berries (pal 12, ramp A)
    dict(
        name="Berry", leg=P4, ramp="A",
        icon="""
.....E........
....EeE..E....
..ggeEgg.eE...
.gGGjGGGgaaa..
.gGjGGGGaAhAa.
.gGGGGGGaAAAa.
.gGGGGGgaAAAa.
..gGGGgg.aAa..
...ggg....a...
..............
""",
        cab_l="""
................
...E....E..E....
..gGg..aAa.rr.E.
.gGjGgaAhAarrYY.
.gGGGgaAAAarYYYY
KBBBBBBBBBBBBBBK
KBYBYBYBYBYBYBBK
.KBBBBBBBBBBBBK.
..KKKKKKKKKKKK..
""",
        cab_r="""
...r....r....r..
.KKrK.KKrK.KKrK.
.KAAK.KGGK.KYYK.
.KAhK.KGjK.KYWK.
.KAAK.KGGK.KYYK.
.KAAK.KGGK.KYYK.
.KaaK.KggK.KYYK.
.KKKK.KKKK.KKKK.
""",
        kit_l="""
....KKKKKK......
....KllllK......
...KKKKKKKK.....
...KWAAAAAK.....
...KWAhAAAK..rr.
...KWAAAAAK.rrYY
....KAAAAK..rYYY
...KKKKKKKK.KYYK
...KlddddlK..KK.
...KKKKKKKK.....
""" + TABLE,
        kit_r="""
..gGg.aAa.gGg...
.gGjGaAhAagGjGg.
.gGGaAAAArrGGGg.
KKKKKKKKKKKKKKKK
KBBBBBBBBBBBBBBK
KBYYBYYBYYBYYBBK
KBBBBBBBBBBBBBBK
KBYYBYYBYYBYYBBK
KBBBBBBBBBBBBBBK
KKKKKKKKKKKKKKKK
""",
        wall="""
................
KKKKKKKKKKKKKKKK
dddddddddddddddd
..E....E.....E..
.EeE..EeE...EeE.
..E....E.....E..
.aAa..gGg...rr..
aAhAagGjGg.rrrr.
aAAAagGGGg.rrrr.
.aAa..gGg...rr..
""",
    ),
    # ============================================================== ice kachang (pal 12, ramp B)
    dict(
        name="IceKachang", leg=P4, ramp="B",
        icon="""
......dd......
.....dWWd.....
....drWWed....
...drrWWeed...
..dYrrWWeeYd..
.KKKKKKKKKKKK.
.KjjjjjjjjjjK.
..KGGGGGGGGK..
...KKKKKKKK...
..............
""",
        cab_l="""
......dWWd......
.....dWWWWd.....
....drWWWWed....
...drrWWYWeed...
..dYrrWWWWeeYd..
.KKKKKKKKKKKKKK.
.KjjjjjjjjjjjjK.
..KGGGGGGGGGGK..
...KKKKKKKKKK...
""",
        cab_r="""
................
.KKKK.KKKK.KKKK.
.KddK.KddK.KddK.
.KrrK.KeeK.KYYK.
.KrBK.KEeK.KYWK.
.KrrK.KeeK.KYYK.
.KBrK.KeEK.KWYK.
.KKKK.KKKK.KKKK.
""",
        kit_l="""
.....KKKKKK.....
....KWWjWWWK....
....KWjWWWjK....
....KKKKKKKK....
...KGGGGGGGGK...
..KKGjGGGGGGKK..
.KlKGGGGGGGGKlK.
..KKGGGGGGGgKK..
...KKKKKKKKKK...
....KWWWWWWK....
...KKjjjjjjKK...
....KKKKKKKK....
KKKKKKKKKKKKKKKK
KllllllllllllldK
KKKKKKKKKKKKKKKK
""",
        kit_r="""
..KK...KK...KK..
..KK...KK...KK..
.KrrK.KeeK.KYYK.
.KrrK.KeeK.KYYK.
.KWWK.KWWK.KWWK.
.KrrK.KeeK.KYYK.
.KrrK.KEEK.KYYK.
.KKKK.KKKK.KKKK.
""" + TABLE,
    ),
]


def build(stall):
    """ASCII -> Art for one stall. Returns dict of 16x16 overlays."""
    leg, ramp = stall["leg"], RAMP[stall["ramp"]]
    out = {
        "sign_l": art(leg, SIGN_L, h=16, subs=ramp),
        "sign_r": art(leg, SIGN_R, h=16, subs=ramp),
        "stripe": art(leg, STRIPE, h=16, subs=ramp),
    }
    mid = art(leg, SIGN_M, h=16, subs=ramp)
    mid.blit(art(leg, stall["icon"], w=14), 1, 3)
    out["sign_m"] = mid
    for key in ("cab_l", "cab_r"):
        a = art(leg, stall[key], h=16, subs=stall.get(key + "_subs"))
        out[key + "_plain"] = a
        out[key] = out["stripe"].over(a)
    for key in ("kit_l", "kit_r"):
        subs = dict(stall.get(key + "_subs") or {})
        out[key] = art(leg, stall[key], h=16, anchor="bottom", subs=subs)
    if "wall" in stall:
        out["wall"] = art(leg, stall["wall"], h=16)
    return out
