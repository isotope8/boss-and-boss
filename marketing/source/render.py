import subprocess, os, time
from playwright.sync_api import sync_playwright
FPS=30
t0=time.time()
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.goto('file:///home/claude/video/scenes.html');pg.wait_for_timeout(800)
    dur=pg.evaluate('DUR')
    for sc,d in dur.items():
        n=round(d*FPS);tmp=f'{sc}.tmp.mp4'
        ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-framerate',str(FPS),'-c:v','mjpeg','-i','-',
            '-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-r',str(FPS),tmp],stdin=subprocess.PIPE)
        pg.evaluate(f"show('{sc}')")
        for i in range(n):
            pg.evaluate(f"render({i/FPS})")
            ff.stdin.write(pg.screenshot(type='jpeg',quality=92))
        ff.stdin.close();rc=ff.wait()
        if rc==0: os.replace(tmp,f'{sc}.mp4')
        print(sc,n,'frames rc',rc,round(time.time()-t0),'s',flush=True)
    open('list.txt','w').write(''.join(f"file '{sc}.mp4'\n" for sc in dur))
    print('total',sum(dur.values()))
