#!/usr/bin/env python3
"""Рендер картинки утреннего прогноза.
Пример: python3 render.py --date "26 октября" --moon "Луна в Тельце 🌙" \
  --badge "Меркурий <i>℞</i>" --badge "Полнолуние" --note "рукописная пометка" \
  --footer "подпись внизу" --out ../threads/2026-10/prognoz-26.png
Перед первым запуском: cd tools && npm i
"""
import argparse,subprocess,os
p=argparse.ArgumentParser()
p.add_argument('--date',required=True);p.add_argument('--moon',required=True)
p.add_argument('--badge',action='append',default=[]);p.add_argument('--note',default='')
p.add_argument('--footer',default='');p.add_argument('--out',required=True)
a=p.parse_args()
here=os.path.dirname(os.path.abspath(__file__))
s=open(os.path.join(here,'prognoz-template.html'),encoding='utf-8').read()
badges=''.join(f'<span class="badge">{b}</span>' for b in a.badge)
s=s.replace('{{DATE}}',a.date).replace('{{MOON}}',a.moon).replace('{{BADGES}}',badges).replace('{{NOTE}}',a.note).replace('{{FOOTER}}',a.footer)
tmp=os.path.join(here,'_tmp.html');open(tmp,'w',encoding='utf-8').write(s)
out=os.path.abspath(a.out);os.makedirs(os.path.dirname(out),exist_ok=True)
subprocess.run(['node','shot.js','_tmp.html',out],cwd=here,check=True);os.remove(tmp);print(out)
