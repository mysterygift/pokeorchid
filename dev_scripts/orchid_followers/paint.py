class G:
    def __init__(s,w,h): s.w=w; s.g=[['.']*w for _ in range(h)]
    def p(s,y,x,t):
        for i,c in enumerate(t):
            if c!='.' and 0<=x+i<s.w: s.g[y][x+i]=c
        return s
    def mp(s,y,x,t):  # mirrored placement across the centre (reverses string)
        return s.p(y, s.w-x-len(t), t[::-1])
    def copy(s):
        n=G(s.w,len(s.g)); n.g=[r[:] for r in s.g]; return n
    def clear(s,y,x0,x1):
        for x in range(x0,x1+1): s.g[y][x]='.'
        return s
    def __str__(s): return '\n'.join(''.join(r) for r in s.g)
