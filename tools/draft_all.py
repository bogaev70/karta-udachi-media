import math,subprocess,sys
import os
T=os.path.dirname(os.path.abspath(__file__))
def moon(k,wax,cx,cy,r):
    rx=r*abs(1-2*k); top=f'{cx},{cy-r}'; bot=f'{cx},{cy+r}'
    if wax: d=f'M{top} A{r},{r} 0 0 1 {bot} A{rx:.1f},{r} 0 0 {0 if k<.5 else 1} {top}Z'
    else:   d=f'M{top} A{r},{r} 0 0 0 {bot} A{rx:.1f},{r} 0 0 {1 if k<.5 else 0} {top}Z'
    craters=''.join(f'<circle cx="{cx+dx*r}" cy="{cy+dy*r}" r="{s*r}" fill="url(#cr)"/>' for dx,dy,s in
      [(-.35,-.3,.16),(.2,-.45,.09),(-.1,.15,.22),(.4,.25,.12),(-.5,.35,.1),(.1,.55,.08),(.45,-.1,.07),(-.6,-.05,.06)])
    return f'''<svg class="moon" width="{2*r+120}" height="{2*r+120}" viewBox="{cx-r-60} {cy-r-60} {2*r+120} {2*r+120}">
<defs><radialGradient id="glow"><stop offset=".55" stop-color="#f3d9a6" stop-opacity=".55"/><stop offset="1" stop-color="#f3d9a6" stop-opacity="0"/></radialGradient>
<radialGradient id="lit" cx="40%" cy="35%" r="75%"><stop offset="0" stop-color="#fffaf0"/><stop offset=".6" stop-color="#f2e3c6"/><stop offset="1" stop-color="#d9bf8f"/></radialGradient>
<radialGradient id="cr"><stop offset="0" stop-color="#c9ad7c" stop-opacity=".55"/><stop offset=".8" stop-color="#d8bf92" stop-opacity=".35"/><stop offset="1" stop-color="#fff6e4" stop-opacity=".5"/></radialGradient>
<clipPath id="lc"><path d="{d}"/></clipPath></defs>
<circle cx="{cx}" cy="{cy}" r="{r+55}" fill="url(#glow)"/>
<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ece2d3"/><g opacity=".25">{craters}</g>
<g clip-path="url(#lc)"><circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#lit)"/>{craters}</g>
<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#c08a45" stroke-width="2" opacity=".6"/><circle cx="{cx}" cy="{cy}" r="{r+38}" fill="none" stroke="#c08a45" stroke-width="1.2" stroke-dasharray="2 8" opacity=".7"/></svg>'''
html=open(T+'/prognoz-template-d.html',encoding='utf-8').read()
def build(date,moontxt,lead,note,k,wax,stars,cname,out):
    pts=' '.join(f'{x},{y}' for x,y in stars)
    const=f'''<svg class="const" width="720" height="230" viewBox="0 0 720 230"><polyline points="{pts}" fill="none" stroke="#c08a45" stroke-width="1.6" stroke-dasharray="4 6" opacity=".8"/>
{''.join(f'<circle cx="{x}" cy="{y}" r="{7 if i%2==0 else 5}" fill="#c08a45"/><circle cx="{x}" cy="{y}" r="14" fill="#e0a85a" opacity=".18"/>' for i,(x,y) in enumerate(stars))}
<text x="{max(x for x,_ in stars)+40}" y="{sum(y for _,y in stars)//len(stars)+8}" font-family="Man" font-size="22" letter-spacing="5" fill="#9a6a35">СОЗВЕЗДИЕ {cname}</text></svg>'''
    page=f'''<!doctype html><html><head><meta charset="utf-8"><style>
{html.split('<style>')[1].split('</style>')[0]}
.c{{background:radial-gradient(ellipse at 75% 20%,#fbf6ee 0%,#f1e9de 50%,#e6dbcc 100%)}}
.c::before{{content:"";position:absolute;inset:0;background:repeating-radial-gradient(circle at 30% 70%,rgba(160,120,80,.025) 0 2px,transparent 2px 5px)}}
.moon{{position:absolute;left:590px;top:140px}}
.const{{position:absolute;left:96px;top:620px}}
.card{{position:absolute;left:150px;top:880px;width:700px;padding:44px 48px 40px;background:#fffdf8;transform:rotate(-1.8deg);
 box-shadow:0 18px 40px rgba(120,80,40,.18),0 2px 6px rgba(120,80,40,.1);border-radius:6px}}
.card .t{{font-family:Man;font-size:40px;line-height:1.3;color:#3b2a20}}
.card .h{{font-family:Cav;font-size:58px;color:#a7703a;margin-top:26px;line-height:1}}
.tape{{position:absolute;top:-22px;left:250px;width:170px;height:46px;background:rgba(224,190,140,.55);transform:rotate(3deg)}}
.head{{position:absolute;left:96px;top:96px}}
.lbl{{font-family:Man;font-weight:600;font-size:26px;letter-spacing:9px;color:#9a6a35}}
.dt{{font-family:Corm;font-weight:700;font-size:100px;line-height:.95;margin-top:160px;text-transform:uppercase;
 background:linear-gradient(180deg,#d9a45c,#b47835 55%,#8a5623);-webkit-background-clip:text;background-clip:text;color:transparent}}
.mn{{font-family:Corm;font-weight:700;font-size:80px;line-height:1.02;max-width:540px;color:#2a1a12;margin-top:24px}}
.dash2{{width:120px;height:3px;background:#c08a45;margin-top:30px}}
.st{{position:absolute;color:#c08a45;font-family:Man}}
</style></head><body><div class="c">
{moon(k,wax,250,250,200)}
<div class="head"><div class="lbl">АСТРОПРОГНОЗ</div><div class="dt">{date}</div><div class="dash2"></div><div class="mn">{moontxt}</div></div>
{const}
<div class="st" style="left:520px;top:120px;font-size:30px">✦</div><div class="st" style="left:930px;top:690px;font-size:22px">✦</div>
<div class="st" style="left:860px;top:1080px;font-size:36px">✦</div><div class="st" style="left:110px;top:690px;font-size:20px">✦</div>
<div class="card"><div class="tape"></div><div class="t">{lead}</div><div class="h">{note}</div></div>
<div class="acc">@annetbo_</div><div class="nick">@karta.udachi</div></div></body></html>'''
    open(T+'/_draft.html','w',encoding='utf-8').write(page)
    subprocess.run(['node','shot.js','_draft.html',out],cwd=T,check=True)

import swisseph as swe, datetime as dt
from eph import lon,TZ
from posts import IMG
from lead import LEAD
IMG[5]=("Луна в Деве",[],"сначала дела, потом свидание")
GEN={'Овне':'ОВНА','Тельце':'ТЕЛЬЦА','Близнецах':'БЛИЗНЕЦОВ','Раке':'РАКА','Льве':'ЛЬВА','Деве':'ДЕВЫ','Весах':'ВЕСОВ','Скорпионе':'СКОРПИОНА','Стрельце':'СТРЕЛЬЦА','Козероге':'КОЗЕРОГА','Водолее':'ВОДОЛЕЯ','Рыбах':'РЫБ'}
SH={'Овне':[(20,150),(120,110),(210,95),(270,120)],
'Тельце':[(20,150),(110,90),(200,120),(290,60),(250,170)],
'Близнецах':[(30,40),(60,120),(80,190),(150,30),(180,110),(200,185)],
'Раке':[(40,60),(130,110),(110,190),(220,150),(260,70)],
'Льве':[(260,40),(220,20),(180,50),(200,100),(120,130),(30,160),(140,180)],
'Деве':[(20,60),(90,100),(160,80),(220,130),(150,180),(280,170)],
'Весах':[(20,140),(90,60),(180,100),(140,190),(270,150)],
'Скорпионе':[(20,50),(80,70),(130,100),(170,150),(220,180),(270,160),(280,120)],
'Стрельце':[(30,170),(100,130),(170,150),(150,70),(230,90),(280,40)],
'Козероге':[(20,60),(110,130),(200,170),(270,110),(230,40)],
'Водолее':[(20,80),(80,110),(140,80),(200,110),(260,80),(230,180)],
'Рыбах':[(20,40),(70,90),(120,140),(170,180),(230,130),(290,90)]}
OUT=os.path.join(T,'..','threads','2026-11','prognoz-%02de.png')
for d in map(int,sys.argv[1:]):
    t=dt.datetime(2026,11,d,8)-TZ
    el=(lon(swe.MOON,t)[0]-lon(swe.SUN,t)[0])%360; k=(1-math.cos(math.radians(el)))/2
    moontxt=IMG[d][0].replace(' в ',' в\u00a0').replace(' во ',' во\u00a0'); sign=moontxt.split()[-1]
    build(f'{d} ноября',moontxt,LEAD[d],IMG[d][2],k,el<180,SH[sign],GEN[sign],OUT%d)
    print(d,sign,round(k,2))
