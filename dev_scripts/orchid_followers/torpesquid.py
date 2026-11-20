import sys,os; sys.path.insert(0,os.path.dirname(__file__)); from paint import G
AUTO_OUTLINE=True
CMAP={'W':1,'L':2,'q':3,'M':4,'O':5,'D':6,'B':7,'m':8,'V':9,'R':10,'o':11}
CONE=[(5,"WL"),(4,"WWLM"),(4,"WWLM"),(3,"WWWLMM"),(2,"LWWWLLMD"),(1,"LWWWWLLMMD"),(0,"LLWWWWLLMMDD")]
def front(face, k):
    g=G(12,16)
    for y,(x,t) in enumerate(CONE): g.p(y,x,t)
    g.p(7,0,"DMMDDDDDDMMD")
    if face: g.p(8,1,"WOOWWWWOOL").p(9,1,"WBVWWWWVBM")   # white band with orange eyes
    else:    g.p(8,1,"WWWWWWWWWL").p(9,1,"LLLLLLLLLM")
    g.p(10,1,"DDDDDDDDDD").p(11,2,"MLLMMMMD").p(12,2,"LMWLLWML")
    if k==0: g.p(13,1,"LM").p(13,4,"W").p(13,7,"L").p(13,9,"ML").p(14,0,"LM").p(14,4,"L").p(14,7,"M").p(14,10,"ML").p(15,0,"M").p(15,4,"M").p(15,7,"D").p(15,11,"M")
    else:    g.p(13,2,"LM").p(13,4,"W").p(13,7,"L").p(13,8,"ML").p(14,1,"LM").p(14,3,"L").p(14,8,"M").p(14,9,"ML").p(15,1,"M").p(15,3,"M").p(15,8,"D").p(15,10,"M")
    return str(g)
def left(k):
    g=G(12,16)
    for y,(x,t) in enumerate(CONE): g.p(y,x,t)
    g.p(7,0,"DMMMDDDDDDDD").p(8,1,"OWWWWWWLM").p(9,1,"BLLLLLLMD")
    g.p(10,2,"LWWLLLMD").p(11,2,"MLLMMMDD").p(12,3,"LMWLLM")
    if k==0: g.p(13,2,"LM").p(13,5,"W").p(13,8,"MD").p(14,1,"LM").p(14,5,"L").p(14,9,"MD").p(15,1,"M").p(15,5,"M").p(15,10,"D")
    else:    g.p(13,3,"LM").p(13,5,"W").p(13,7,"MD").p(14,2,"LM").p(14,6,"L").p(14,8,"MD").p(15,2,"M").p(15,6,"M").p(15,9,"D")
    return str(g)
def frames(): return [front(True,0),front(True,1),front(False,0),front(False,1),left(0),left(1)]
