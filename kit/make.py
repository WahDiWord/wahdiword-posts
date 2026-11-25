#!/usr/bin/env python3
"""Wah Di Word? Instagram post maker.
Usage: python3 kit/make.py week.json OUTDIR
week.json = list of posts. Each post:
 {"id":"2026-11-26-word", "theme":"green|gold|night|sea|sunset|pink|purple",
  "kicker":"WORD OF DI DAY", "title":"Line one|*Yellow line*", "body":"text",
  "tiles":"GALANG" or "??????" or "G?L?NG" (optional, max 9),
  "tag":"small pill text (optional)", "tilly":"jamaica-wave" (file in assets/tilly without .png),
  "footer":"Coming soon"}
Text in *stars* is yellow. "|" makes a new line. Run render with node (see render.js).
"""
import json, sys, os, html, re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEMES={
 'green': ('#1E9E55','#0B5A2E','#052C16','#9FF0C2','#D9FBE6','#063C1E','#9FCFB2'),
 'gold':  ('#FFD84A','#FFB300','#E07A00','#7A3A00','#5A2A00','#6A3400','#E8A040'),
 'night': ('#2A3A8C','#151C4A','#070A1E','#9FB4FF','#DCE4FF','#05081A','#8A96C8'),
 'sea':   ('#1BA6D9','#0C5E94','#06294A','#A8ECFF','#DDF6FF','#052540','#8FC4DA'),
 'sunset':('#FF7A3A','#C2367A','#3A0E40','#FFD2A8','#FFE6D6','#3A0A2A','#E0A0B4'),
 'pink':  ('#FF6FA8','#C2306E','#4A0A26','#FFD0E4','#FFE6F0','#4A0820','#E8A8C4'),
 'purple':('#8A4BEF','#4A1A9E','#1A0840','#D8C4FF','#EEE6FF','#14063A','#B8A4E0'),
}
def rich(t):
    t=html.escape(t)
    t=re.sub(r'\*(.+?)\*',r'<span class="y">\1</span>',t)
    return t.replace('|','<br>')
def page(p):
    a,b,c,k,bd,sh,ts=THEMES[p.get('theme','green')]
    ink,hi,shc=('#4A1F00','#0B7A3E','#FFE58A') if p.get('theme')=='gold' else ('#fff','#FFD84A',sh)
    tiles=''
    if p.get('tiles'):
        tiles='<div class="tiles">'+''.join('<div class="sp"></div>' if ch==' ' else f'<div class="t">{html.escape(ch)}</div>' for ch in p['tiles'][:13])+'</div>'
    tag=f'<div class="tag">{html.escape(p["tag"])}</div>' if p.get('tag') else ''
    tilly=os.path.join(ROOT,'assets','tilly',p.get('tilly','gold-wave')+'.png')
    foot=html.escape(p.get('footer','Coming soon'))
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0}}*{{box-sizing:border-box}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;font-family:Poppins,sans-serif;background:radial-gradient(circle at 72% 62%,{a} 0%,{b} 55%,{c} 100%)}}
.orb{{position:absolute;left:560px;top:430px;width:700px;height:700px;border-radius:50%;background:radial-gradient(circle at 40% 35%,rgba(255,255,255,.22),rgba(255,255,255,.04) 60%,transparent 70%);box-shadow:0 0 0 10px rgba(255,255,255,.18)}}
.ray{{position:absolute;inset:0;background:repeating-conic-gradient(from 0deg at 80% 75%,rgba(255,255,255,.05) 0 6deg,transparent 6deg 18deg)}}
.k{{position:absolute;left:80px;top:78px;margin:0;font-size:32px;font-weight:800;letter-spacing:8px;color:{k}}}
.h{{position:absolute;left:76px;top:122px;width:930px;margin:0;font-size:112px;line-height:1.02;font-weight:900;color:{ink};text-shadow:0 7px 0 {shc},0 20px 30px rgba(0,0,0,.3)}}
.y{{color:{hi}}}
.b{{position:absolute;left:82px;width:470px;margin:0;font-size:34px;line-height:1.35;font-weight:700;color:{bd}}}
.tiles{{position:absolute;left:82px;display:flex;gap:12px}}
.t{{width:84px;height:84px;border-radius:20px;background:#fff;box-shadow:0 8px 0 {ts};display:flex;align-items:center;justify-content:center;font-size:52px;font-weight:900;color:{b}}}
.sp{{width:18px}}
.tag{{position:absolute;left:82px;padding:10px 26px;border-radius:40px;background:rgba(255,255,255,.16);border:2px solid rgba(255,255,255,.35);color:#fff;font-size:28px;font-weight:800}}
.ti{{position:absolute;right:30px;bottom:40px;width:520px;height:auto;filter:drop-shadow(0 24px 30px rgba(0,0,0,.4))}}
.f{{position:absolute;left:82px;top:920px;margin:0;font-size:36px;font-weight:900;color:{ink}}}
</style></head><body><div class="c"><div class="ray"></div><div class="orb"></div>
<p class="k">{html.escape(p.get('kicker',''))}</p><h1 class="h" id="h">{rich(p.get('title',''))}</h1>
<p class="b" id="b">{rich(p.get('body',''))}</p>{tiles}{tag}
<img class="ti" src="file://{tilly}">
<p class="f">{foot} · <span class="y">@wahdiword</span></p></div>
<script>
const h=document.getElementById('h');let s=112;while((h.scrollWidth>930||h.offsetHeight>330)&&s>56){{s-=4;h.style.fontSize=s+'px'}}
let y=h.offsetTop+h.offsetHeight+34;
const t=document.querySelector('.tiles');
if(t){{const n=t.querySelectorAll('.t').length;const room=900-t.querySelectorAll('.sp').length*18;
const w=Math.min(84,Math.floor((room-12*(n-1))/n));
for(const e of t.querySelectorAll('.t')){{e.style.width=e.style.height=w+'px';e.style.fontSize=Math.round(w*.62)+'px'}}
t.style.top=y+'px';y+=w+46}}
const b=document.getElementById('b');b.style.top=y+'px';
let bs=34;while(b.offsetHeight>Math.max(120,860-y)&&bs>24){{bs-=2;b.style.fontSize=bs+'px'}}
y+=b.offsetHeight+(b.textContent.trim()?36:0);
const g=document.querySelector('.tag');if(g){{g.style.top=Math.min(y,840)+'px'}}
</script></body></html>'''
if __name__=='__main__':
    posts=json.load(open(sys.argv[1])); out=sys.argv[2]; os.makedirs(out,exist_ok=True)
    for p in posts:
        open(os.path.join(out,p['id']+'.html'),'w').write(page(p))
    os.system(f'NODE_PATH=$(npm root -g) node {ROOT}/kit/render.js {out}')
