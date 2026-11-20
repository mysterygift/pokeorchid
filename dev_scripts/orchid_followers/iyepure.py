import sys,os; sys.path.insert(0,os.path.dirname(__file__)); from paint import G
AUTO_OUTLINE=True
CMAP={'W':1,'L':2,'g':3,'l':4,'y':5,'G':6,'n':7,'P':8,'Y':9,'N':10,'d':11,'k':12,'o':13}
def ears(g):
    for y,x,t in [(0,0,"WL"),(1,0,"WLo"),(2,1,"WLo")]:
        g.p(y,x,t); g.mp(y,x,t)
def down():
    g=G(14,10)
    g.p(0,5,'l').p(0,8,'l').p(1,4,"NnyYnN").p(2,4,"NnoynN")
    ears(g)
    g.p(3,2,"WLggggggLW").p(4,1,"gWggggggggGG").p(5,1,"gWgoggggoGGG")
    g.p(6,0,"GggggLPPLggGGP").p(7,0,"PGgggLLLLggGPd").p(8,1,"PgWgGGGGgWgd")
    a=g.copy().p(9,2,"gGg").p(9,5,"dddd").p(9,9,"gGg"); b=g.copy().p(9,2,"gGgdddd")
    return str(a),str(b)
def up():
    g=G(14,10)
    g.p(1,4,"gggggg").p(2,4,"gggggG")
    ears(g)
    g.p(3,1,"NnyYnllnyYnN").p(4,1,"NnoynNNnoynN").p(5,1,"kNkNNkkNNkNk").p(5,0,"G").p(5,13,"P")
    g.p(6,0,"GggggWWWWggGGP").p(7,0,"PGgggLWWLggGPd").p(8,0,"PgWgGGLLGGgWgP")
    a=g.copy().p(9,1,"gGg").p(9,4,"dddddd").p(9,10,"gGg"); b=g.copy().p(9,1,"gGgdddddd")
    return str(a),str(b)
def left():
    g=G(15,10)
    for y,x,t in [(0,3,"WL"),(1,2,"WLo"),(2,2,"WLo")]: g.p(y,x,t)
    g.p(3,1,"gWggg").p(4,0,"gWoggg").p(5,0,"PLgggGG").p(6,1,"LgggGggggggGWW").p(7,1,"GgWgGGgggGGGPP")
    g.p(2,7,'l').p(2,10,'l').p(3,6,"NyYnyYN").p(4,6,"NoynoyN").p(5,6,"kNkNkNk")
    a=g.copy().p(8,1,"gGWg").p(8,5,"PPPP").p(8,9,"gWWg").p(9,1,"dGGd").p(9,9,"dGGd")
    b=g.copy().p(8,0,"gGWg").p(8,4,"PPPPP").p(8,10,"gWWg").p(9,0,"dGGd").p(9,10,"dGGd")
    return str(a),str(b)
def frames(): return [*down(),*up(),*left()]
