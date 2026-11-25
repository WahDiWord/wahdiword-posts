#!/usr/bin/env python3
"""Wah Di Word? Reel maker (1080x1920, ~12.5s, with music and game sounds).
Usage: python3 kit/reel.py reel.json OUT.mp4
reel.json: {"theme":"night", "kicker":"GUESS DI WORD", "title":"Yuh know|*dis one?*",
  "tiles":"??????" (shown first), "answer":"GALANG" (optional: tiles flip to this at 7s),
  "lines":["Clue: ...", "..."] (up to 3 short lines), "tilly":"jamaica-wave", "bed":1|2|3,
  "end":"Coming soon to Google Play"}
Spaces in tiles/answer make a gap. *stars* = yellow, | = new line.
"""
import json, sys, os, html, re, wave, subprocess, shutil, tempfile
import numpy as np
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT,'kit'))
from make import THEMES, rich
DUR=12.5; FPS=30

def page(p):
    a,b,c,k,bd,sh,ts=THEMES[p.get('theme','green')]
    gold=p.get('theme')=='gold'
    ink,hi,shc=('#4A1F00','#0B7A3E','#FFE58A') if gold else ('#fff','#FFD84A',sh)
    tiles=p.get('tiles',''); ans=p.get('answer','')
    tl=''.join('<div class="sp"></div>' if ch==' ' else f'<div class="t" data-a="{html.escape(ans[i] if i<len(ans) else ch)}"><span>{html.escape(ch)}</span></div>' for i,ch in enumerate(tiles))
    lines=''.join(f'<p class="ln">{rich(l)}</p>' for l in p.get('lines',[])[:3])
    tilly=os.path.join(ROOT,'assets','tilly',p.get('tilly','gold-wave')+'.png')
    cheer=os.path.join(ROOT,'assets','tilly',p.get('end_tilly','jamaica-cheer')+'.png')
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0}}*{{box-sizing:border-box}}
.c{{width:1080px;height:1920px;position:relative;overflow:hidden;font-family:Poppins,sans-serif;background:radial-gradient(circle at 50% 70%,{a} 0%,{b} 55%,{c} 100%)}}
.ray{{position:absolute;left:-600px;top:-200px;width:2280px;height:2280px;background:repeating-conic-gradient(from 0deg at 50% 60%,rgba(255,255,255,.06) 0 6deg,transparent 6deg 18deg)}}
.k{{position:absolute;left:0;right:0;top:230px;text-align:center;margin:0;font-size:40px;font-weight:800;letter-spacing:10px;color:{k}}}
.h{{position:absolute;left:50px;right:50px;top:300px;text-align:center;margin:0;font-size:140px;line-height:1.04;font-weight:900;color:{ink};text-shadow:0 8px 0 {shc},0 22px 34px rgba(0,0,0,.3)}}
.y{{color:{hi}}}
.tiles{{position:absolute;left:0;right:0;display:flex;justify-content:center;gap:14px;perspective:900px}}
.t{{width:110px;height:110px;border-radius:26px;background:#fff;box-shadow:0 10px 0 {ts};display:flex;align-items:center;justify-content:center;font-size:68px;font-weight:900;color:{b}}}
.t.ok{{background:#16A85C;color:#fff;box-shadow:0 10px 0 #0B6A38}}
.sp{{width:26px}}
.ln{{position:absolute;left:80px;right:80px;text-align:center;margin:0;font-size:52px;line-height:1.3;font-weight:700;color:{bd}}}
.ti{{position:absolute;left:50%;width:700px;margin-left:-350px;filter:drop-shadow(0 28px 34px rgba(0,0,0,.4))}}
.end{{position:absolute;inset:0;background:radial-gradient(circle at 50% 45%,#1E9E55,#0B5A2E 60%,#052C16);display:flex;flex-direction:column;align-items:center;justify-content:center;opacity:0}}
.end .lg{{font-size:118px;font-weight:900;color:#fff;line-height:1;text-shadow:0 9px 0 #063C1E}}
.end .lg span{{color:#FFD84A}}
.end img{{width:640px;margin:30px 0 10px;filter:drop-shadow(0 24px 30px rgba(0,0,0,.4))}}
.end .s{{font-size:54px;font-weight:800;color:#D9FBE6;margin:0}}
.end .at{{font-size:60px;font-weight:900;color:#FFD84A;margin:18px 0 0}}
</style></head><body><div class="c"><div class="ray" id="ray"></div>
<p class="k" id="k">{html.escape(p.get('kicker',''))}</p><h1 class="h" id="h">{rich(p.get('title',''))}</h1>
<div class="tiles" id="tiles">{tl}</div><div id="lines">{lines}</div>
<img class="ti" id="ti" src="file://{tilly}">
<div class="end" id="end"><div class="lg">Wah Di <span>Word?</span></div><img src="file://{cheer}"><p class="s">{html.escape(p.get('end','Coming soon to Google Play'))}</p><p class="at">@wahdiword</p></div>
</div><script>
const H=document.getElementById('h');let fs=140;while((H.scrollWidth>980||H.offsetHeight>460)&&fs>64){{fs-=4;H.style.fontSize=fs+'px'}}
let y=H.offsetTop+H.offsetHeight+60;const T=document.getElementById('tiles');const tt=[...T.querySelectorAll('.t')];
if(tt.length){{const n=tt.length,sp=T.querySelectorAll('.sp').length;const w=Math.min(110,Math.floor((980-sp*26-14*(n+sp-1))/n));
tt.forEach(e=>{{e.style.width=e.style.height=w+'px';e.style.fontSize=Math.round(w*.62)+'px';e.style.borderRadius=Math.round(w*.24)+'px'}});T.style.top=y+'px';y+=w+70}}
const L=[...document.querySelectorAll('.ln')];L.forEach(l=>{{l.style.top=y+'px';y+=l.offsetHeight+22}});
const TI=document.getElementById('ti');TI.style.top=Math.max(y+10,1600-778)+'px';
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)),ob=x=>{{const c=1.7;x-=1;return 1+(c+1)*x*x*x+c*x*x}},seg=(t,a,b)=>cl((t-a)/(b-a));
const HASANS={json.dumps(bool(ans))};
window.draw=function(t){{
 document.getElementById('ray').style.transform=`rotate(${{t*3}}deg)`;
 const K=document.getElementById('k');K.style.opacity=seg(t,0,.5);K.style.transform=`translateY(${{(1-seg(t,0,.5))*-40}}px)`;
 const hs=ob(seg(t,.25,.85));H.style.opacity=seg(t,.25,.5);H.style.transform=`scale(${{.4+.6*hs}})`;
 tt.forEach((e,i)=>{{const a=1.3+i*.18;const s=seg(t,a,a+.3);e.style.opacity=s>0?1:0;e.style.transform=`rotateX(${{(1-ob(s))*90}}deg)`;
   if(HASANS){{const r=7.0+i*.16;const q=seg(t,r,r+.3);if(q>0){{const ang=q<.5?q*180:(1-q)*180;e.style.transform=`rotateX(${{ang}}deg)`;if(q>=.5){{e.firstChild.textContent=e.dataset.a;e.classList.add('ok')}}}}}}}});
 L.forEach((l,i)=>{{const a=3.0+i*.7;const s=seg(t,a,a+.5);l.style.opacity=s;l.style.transform=`translateY(${{(1-s)*40}}px)`}});
 const e=ob(seg(t,.6,1.4));TI.style.transform=`translateY(${{(1-e)*900+Math.sin(t*2.4)*12}}px) rotate(${{Math.sin(t*1.7)*2}}deg)`;
 const E=document.getElementById('end');const es=seg(t,9.7,10.2);E.style.opacity=es;E.style.transform=`scale(${{1.08-.08*es}})`;
}};
</script></body></html>'''

def sfx_times(p):
    ev=[('ui_open',0.2,.5)]
    n=0
    for i,ch in enumerate(p.get('tiles','')):
        if ch==' ': continue
        ev.append((f'tile_green_{n%8+1}',1.3+i*.18,.45)); n+=1
    if p.get('answer'):
        for i,ch in enumerate(p['answer']):
            if ch!=' ': ev.append(('tile_flip',7.0+i*.16+.15,.5))
        ev.append(('win_daily',7.2+len(p['answer'])*.16,.6))
    for i,_ in enumerate(p.get('lines',[])[:3]): ev.append(('hint_reveal_letter',3.0+i*.7,.35))
    ev.append(('wheel_win',9.8,.6))
    return ev

def readwav(f):
    with wave.open(f) as w:
        sr=w.getframerate();ch=w.getnchannels();d=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(np.float32)/32768
    d=d.reshape(-1,ch)
    if ch==1: d=np.repeat(d,2,axis=1)
    if sr!=44100:
        idx=np.linspace(0,len(d)-1,int(len(d)*44100/sr)); d=np.stack([np.interp(idx,np.arange(len(d)),d[:,k]) for k in (0,1)],1)
    return d

def audio(p,out):
    SR=44100;N=int(DUR*SR);mix=np.zeros((N,2),np.float32)
    tmp=out+'.bed.wav'
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',os.path.join(ROOT,'assets','audio',f"bed{p.get('bed',1)}.mp3"),'-ar','44100','-ac','2',tmp],check=True)
    bed=readwav(tmp)[:N];os.remove(tmp)
    loop=np.zeros((N,2),np.float32);loop[:len(bed)]=bed
    tt=np.arange(N)/SR;env=np.clip(tt/.4,0,1)*np.clip((DUR-tt)/1.0,0,1)
    mix+=loop*.42*env[:,None]
    for name,at,g in sfx_times(p):
        s=readwav(os.path.join(ROOT,'assets','audio',name+'.wav'));i=int(at*SR)
        if i>=N: continue
        s=s[:N-i];mix[i:i+len(s)]+=s*g
    mix/=max(1.0,np.abs(mix).max()/0.95)
    with wave.open(out,'wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((mix*32767).astype('<i2').tobytes())

def main(spec,out):
    p=json.load(open(spec)) if isinstance(spec,str) else spec
    d=tempfile.mkdtemp();open(os.path.join(d,'r.html'),'w').write(page(p))
    js=f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const pg=await b.newPage({{viewport:{{width:1080,height:1920}}}});
await pg.goto('file://{d}/r.html');await pg.waitForTimeout(400);
for(let i=0;i<{int(DUR*FPS)};i++){{await pg.evaluate(t=>draw(t),i/{FPS});await pg.screenshot({{path:'{d}/f'+String(i).padStart(4,'0')+'.jpg',type:'jpeg',quality:92}});}}
await b.close();}})();"""
    open(os.path.join(d,'r.js'),'w').write(js)
    env=dict(os.environ,NODE_PATH=subprocess.run('npm root -g',shell=True,capture_output=True,text=True).stdout.strip())
    subprocess.run(['node',os.path.join(d,'r.js')],check=True,env=env)
    audio(p,os.path.join(d,'a.wav'))
    tmpout=out[:-4]+'.part.mp4'
    subprocess.run(['ffmpeg','-loglevel','error','-y','-framerate',str(FPS),'-i',f'{d}/f%04d.jpg','-i',f'{d}/a.wav','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',tmpout],check=True)
    os.replace(tmpout,out);shutil.rmtree(d)

if __name__=='__main__':
    main(sys.argv[1],sys.argv[2])
