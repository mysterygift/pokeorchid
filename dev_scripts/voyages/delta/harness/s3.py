from common import *
e=start()
try:
    e.press('START',after=60); e.press('A',after=120); shot(e,'c0_party.png'); print(cb2(e))
    e.press('A',after=60); shot(e,'c1_partyaction.png')
    e.press('A',after=150); shot(e,'c2_summary.png'); print(cb2(e))
    e.press('RIGHT',after=60); shot(e,'c3_summary2.png')
    e.press('RIGHT',after=60); shot(e,'c4_summary3.png')
    e.press('DOWN',after=60); e.press('LEFT',after=60); e.press('LEFT',after=60); shot(e,'c5_summary_mon2.png')
finally:
    e.close()
strip('c_strip.png')
