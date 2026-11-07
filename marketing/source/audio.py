import numpy as np, wave
SR=44100; D=30.0; N=int(SR*D)
mix=np.zeros(N)
def add(sig,t,g=1.0):
    i=int(t*SR); j=min(N,i+len(sig)); mix[i:j]+=sig[:j-i]*g
def env(n,a=0.005,r=0.2):
    t=np.arange(n)/SR; e=np.minimum(1,t/a)*np.exp(-t/r); return e
def tone(f,dur,wave='tri',r=0.25):
    n=int(dur*SR); t=np.arange(n)/SR
    if wave=='tri': s=2*np.abs(2*((t*f)%1)-1)-1
    elif wave=='sq': s=np.sign(np.sin(2*np.pi*f*t))*0.6
    else: s=np.sin(2*np.pi*f*t)
    return s*env(n,r=r)
bpm=112; beat=60/bpm; bar=4*beat
# chords: C, Am, F, G  (root midi)
prog=[[60,64,67],[57,60,64],[53,57,60],[55,59,62]]
m2f=lambda m:440*2**((m-69)/12)
t=0.0; k=0
while t<D-0.5:
    ch=prog[k%4]
    # bass on beats 1 and 3
    for b in (0,2): add(tone(m2f(ch[0]-24),beat*0.9,'sin',r=0.35),t+b*beat,0.35)
    # plucky arpeggio in 8ths
    for e in range(8):
        n=ch[e%3]+(12 if e in (3,7) else 0)
        add(tone(m2f(n),beat*0.5,'tri',r=0.12),t+e*beat/2,0.10)
    # kick + hat
    for b in range(4):
        n=int(0.15*SR); tt=np.arange(n)/SR
        add(np.sin(2*np.pi*(120*np.exp(-tt*25)+45)*tt)*np.exp(-tt*18),t+b*beat,0.45)
        hat=np.random.randn(int(0.04*SR))*env(int(0.04*SR),r=0.012)
        add(hat,t+b*beat+beat/2,0.08)
    t+=bar; k+=1
# fade out music at end
fade=np.ones(N); fs=int(1.2*SR); fade[-fs:]=np.linspace(1,0,fs); mix*=fade
# SFX
def whoosh():
    n=int(0.35*SR); s=np.random.randn(n); 
    from numpy.fft import rfft, irfft
    tt=np.arange(n)/SR; s=np.convolve(s,np.ones(20)/20,'same')
    return s*np.sin(np.pi*tt/0.35)*0.9
def pop(f=880): return tone(f,0.12,'sin',r=0.05)+tone(f*1.5,0.12,'sin',r=0.04)*0.5
def thud():
    n=int(0.25*SR); tt=np.arange(n)/SR
    return np.sin(2*np.pi*(90*np.exp(-tt*10)+40)*tt)*np.exp(-tt*12)+np.random.randn(n)*np.exp(-tt*40)*0.3
S2,S3,S4,S5,S6=3.6,8.6,16.6,21.2,25.6
for i,tt in enumerate([0.6,1.4,2.2]): add(whoosh(),S2+tt,0.5)
add(whoosh(),S3+1.9,0.7); add(whoosh(),S3+4.6,0.7)
add(tone(660,0.1,'sin',r=0.05),S3+1.95,0.3); add(tone(440,0.1,'sin',r=0.05),S3+4.65,0.3)
for d in (0,0.18): add(tone(300,0.12,'sq',r=0.08),S3+5.2+d,0.25)
for i in range(4): add(thud(),S4+0.8+i*0.45,0.8)
for i in range(10): add(pop(660+i*40),S5+0.4+i*0.12,0.35)
for i,f in enumerate([523,659,784,1047]): add(tone(f,0.6,'tri',r=0.4),S6+0.1+i*0.09,0.25)
mix=mix/np.max(np.abs(mix))*0.85
w=wave.open('music.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((mix*32767).astype(np.int16).tobytes()); w.close(); print('ok')
