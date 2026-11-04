import swisseph as swe, datetime as dt
swe.set_ephe_path(None)
SIGNS=['Овен','Телец','Близнецы','Рак','Лев','Дева','Весы','Скорпион','Стрелец','Козерог','Водолей','Рыбы']
P={'Солнце':swe.SUN,'Луна':swe.MOON,'Меркурий':swe.MERCURY,'Венера':swe.VENUS,'Марс':swe.MARS,'Юпитер':swe.JUPITER,'Сатурн':swe.SATURN,'Уран':swe.URANUS,'Нептун':swe.NEPTUNE,'Плутон':swe.PLUTO}
FL=swe.FLG_MOSEPH|swe.FLG_SPEED
def jd(t): return swe.julday(t.year,t.month,t.day,t.hour+t.minute/60+t.second/3600)
def lon(p,t): return swe.calc_ut(jd(t),p,FL)[0]
TZ=dt.timedelta(hours=4)
start=dt.datetime(2026,11,4,20)-TZ  # UTC
end=dt.datetime(2026,12,1,0)-TZ
step=dt.timedelta(minutes=10)
ASP={0:'соединение',60:'секстиль',90:'квадрат',120:'тригон',180:'оппозиция'}
def d(a,b):
    x=(a-b)%360
    return x
events=[]
prev=None
t=start
names=list(P)
while t<=end:
    cur={n:lon(P[n],t) for n in names}
    if prev:
        for n in names:
            s0=int(prev[n][0]//30); s1=int(cur[n][0]//30)
            if s0!=s1: events.append((t,f'{n} входит в {SIGNS[s1]}'))
            if prev[n][3]*cur[n][3]<0: events.append((t,f'{n} {"разворот в директ" if cur[n][3]>0 else "разворот в ретроград"} ({SIGNS[int(cur[n][0]//30)]} {cur[n][0]%30:.1f}°)'))
        for i,a in enumerate(names):
            for b in names[i+1:]:
                if a!='Луна' and b!='Луна' and a in('Сатурн','Уран','Нептун','Плутон') and b in('Сатурн','Уран','Нептун','Плутон'): continue
                for ang,nm in ASP.items():
                    for sgn in ([ang] if ang in(0,180) else [ang,360-ang]):
                        e0=((prev[a][0]-prev[b][0]-sgn+180)%360)-180
                        e1=((cur[a][0]-cur[b][0]-sgn+180)%360)-180
                        if e0*e1<0 and abs(e0-e1)<30:
                            events.append((t,f'{a} {nm} {b} ({SIGNS[int(cur[a][0]//30)]}–{SIGNS[int(cur[b][0]//30)]})'))
        # lunations
        e0=((prev['Луна'][0]-prev['Солнце'][0]+180)%360)-180; e1=((cur['Луна'][0]-cur['Солнце'][0]+180)%360)-180
    prev=cur; t+=step
for t,e in events:
    lt=t+TZ
    print(lt.strftime('%d.%m %H:%M'),e)
