# Synthesizes the Orchid custom species cries (Pinguin, Iyepure, Torpesquid).
# Needs numpy + scipy. Run from the repo root; writes sound/direct_sound_samples/cries/<name>.wav
import numpy as np, wave
from scipy.signal import butter, sosfilt
SR=13379
rng=np.random.default_rng(7)
# vowel formants (F1,F2,F3)
V={'i':(300,2300,3000),'ih':(400,2000,2600),'u':(320,900,2300),'ui':(320,1600,2500),'a':(750,1200,2500),
   'ai':(650,1500,2500),'e':(500,1800,2500),'o':(500,850,2400),'er':(480,1350,1700),'oo':(350,800,2200)}
def bp(x,f,q=6):
    lo,hi=f*(1-1/(2*q)),min(f*(1+1/(2*q)),SR/2-50)
    return sosfilt(butter(2,[lo,hi],btype='band',fs=SR,output='sos'),x)
def env(n,a=0.01,r=0.06,shape=1.0):
    t=np.arange(n)/SR; e=np.ones(n)
    ai=min(int(a*SR),n//2); ri=min(int(r*SR),n-ai)
    if ai: e[:ai]=np.linspace(0,1,ai)
    if ri: e[-ri:]*=np.linspace(1,0,ri)**shape
    return e
def syll(dur,f0a,f0b,vow,vow2=None,buzz=0.0,vib=0.0,vibf=18,rough=0.0,a=0.01,r=0.06,curve=1.0):
    n=int(dur*SR); t=np.linspace(0,1,n)
    f0=f0a+(f0b-f0a)*t**curve
    f0=f0*(1+vib*np.sin(2*np.pi*vibf*np.arange(n)/SR))
    if rough: f0=f0*(1+rough*np.sin(2*np.pi*f0*0.5*np.arange(n)/SR))
    ph=2*np.cumsum(f0)/SR*np.pi
    src=(2*((ph/(2*np.pi))%1)-1)                  # saw
    src+=buzz*np.sign(np.sin(ph*0.5))            # sub-octave buzz
    fa=np.array(V[vow]); fb=np.array(V[vow2 or vow])
    out=np.zeros(n); seg=256
    for s in range(0,n,seg):
        k=s/n; F=fa+(fb-fa)*k
        chunk=src[max(0,s-64):s+seg]
        y=sum(g*bp(chunk,f) for f,g in zip(F,(1.0,0.7,0.35)))
        out[s:s+seg]=y[-len(src[s:s+seg]):]
    return out*env(n,a,r)
def noise(dur,lo,hi,a=0.002,r=0.02,g=1.0):
    n=int(dur*SR); x=rng.standard_normal(n)
    x=sosfilt(butter(2,[lo,min(hi,SR/2-50)],btype='band',fs=SR,output='sos'),x)
    return g*x*env(n,a,r)
def cat(*parts,gap=0.0):
    g=np.zeros(int(gap*SR)); out=[]
    for p in parts: out+= [p,g]
    return np.concatenate(out)
def mix(base,add,at):
    i=int(at*SR); end=i+len(add)
    if end>len(base): base=np.concatenate([base,np.zeros(end-len(base))])
    base[i:end]+=add; return base
def save(name,x):
    x=x/np.max(np.abs(x))*0.95
    x=np.tanh(x*1.6)/np.tanh(1.6)                # gen3-ish saturation
    x=np.concatenate([x,np.zeros(int(0.02*SR))])
    pcm=np.clip(np.round(x*127)+128,0,255).astype(np.uint8)
    with wave.open(name,'wb') as w:
        w.setnchannels(1); w.setsampwidth(1); w.setframerate(SR); w.writeframes(pcm.tobytes())
    print(name,round(len(pcm)/SR,2),'s')

# PINGUIN — "PIN-GWIN!": bright chirpy squawk; short rising "pin", then a squeaky up-down "gwiin"
p = noise(0.018,1500,5000,g=0.6)                                        # p burst
pin = syll(0.13,880,1050,'ih','i',buzz=0.15,vib=0.02,a=0.004,r=0.03)
g = noise(0.015,300,1500,g=0.4)
gwin= syll(0.36,780,1250,'u','i',buzz=0.2,vib=0.035,vibf=22,curve=0.6,a=0.01,r=0.12)
gwin2= syll(0.12,1250,700,'i','ih',buzz=0.2,a=0.002,r=0.08)
x=cat(p,pin,np.zeros(int(0.03*SR)),g,gwin,gwin2)
save('sound/direct_sound_samples/cries/pinguin.wav',x)

# IYEPURE — "EYE-PYUU-REH": warbly, nasal three-beat call from a leafy critter; mid pitch with a trill on the R
eye = syll(0.17,420,520,'a','i',buzz=0.35,vib=0.03,a=0.02,r=0.04)
p2  = noise(0.016,1200,4500,g=0.5)
pyuu= syll(0.24,560,380,'ui','u',buzz=0.3,vib=0.05,vibf=11,a=0.006,r=0.05)
rr  = syll(0.22,470,610,'er','e',buzz=0.45,rough=0.08,vib=0.12,vibf=26,a=0.01,r=0.12)  # rolled-r trill
x=cat(eye,np.zeros(int(0.02*SR)),p2,pyuu,np.zeros(int(0.01*SR)),rr)
save('sound/direct_sound_samples/cries/iyepure.wav',x)

# TORPESQUID — "TOR-PE-SQUIIID!": low gurgling torpedo rumble, then a sharp aggressive squeal
t   = noise(0.02,1500,5500,g=0.7)
tor = syll(0.22,170,140,'o','er',buzz=0.6,rough=0.18,vib=0.06,vibf=9,a=0.008,r=0.03)
p3  = noise(0.015,1000,4000,g=0.5)
pe  = syll(0.09,230,260,'e',buzz=0.5,rough=0.1,a=0.004,r=0.03)
s   = noise(0.09,3000,6500,a=0.01,r=0.01,g=0.55)
k   = noise(0.015,800,3000,g=0.6)
quid= syll(0.42,520,880,'u','i',buzz=0.35,rough=0.04,vib=0.05,vibf=16,curve=0.5,a=0.01,r=0.18)
x=cat(t,tor,p3,pe,s,k,quid)
# bubbly gurgle under the start
bub=np.zeros(int(0.35*SR))
for i in range(7):
    b=syll(0.035,300+60*i,600+80*i,'oo',a=0.003,r=0.02)*0.35; bub=mix(bub,b,0.04*i)
x=mix(x,bub,0.0)
save('sound/direct_sound_samples/cries/torpesquid.wav',x)
