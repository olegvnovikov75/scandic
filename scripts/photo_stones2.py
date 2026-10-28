#!/usr/bin/env python3
"""Скандик: фото рунных камней через прямой поиск Commons (запасной путь, когда en-wiki лид молчит)."""
import json, os, re, time, urllib.parse, urllib.request, html as H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMGD = os.path.join(ROOT, 'images', 'stones')
os.makedirs(IMGD, exist_ok=True)

JOBS = {
 'vikings.html': (['Jelling stone runic monument','Jellingstenen','Jelling Harald Bluetooth'], ['jelling'],
   'Йеллингские камни — «свидетельство о рождении» Дании: Харальд Синезубец возвёл их в память о родителях и о себе — «…приобрёл себе Данию и сделал датчан христианами». Около 965 года.'),
 'runes.html': (['Rökstenen','Rök runestone','Rok runestone Ostergotland'], ['rök','rok'],
   'Рёк — самый длинный рунический текст в мире: около семисот рун, IX век. Загадки, песни о готских конунгах и погоня на льду — память о Великом переселении народов.'),
 'creatures.html': (['Altuna runestone','Altunastensten','Altuna Sigurd dragon'], ['altuna','altunasten'],
   'Альтуна (Уппланд): Сигурд, поражающий змея Фафнира среди его витков, — один из древнейших каменных образов саги о Вёльсунгах, XI век.'),
 'timeline.html': (['Kylver stone','Kylverstenen','Kylver runic futhark'], ['kylver'],
   'Кюльверский камень с Готланда — древнейший полный футарк: все двадцать четыре руны подряд, около 400 года.'),
}

def api(url, tries=5):
    for i in range(tries):
        req = urllib.request.Request(url, headers={'User-Agent': 'Scandic-site/1.0 (contact: olegvnovikov75@github.com)'})
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.load(r)
        except Exception as e:
            if i < tries-1 and ('429' in str(e) or 'timed out' in str(e) or 'Timeout' in str(e)):
                time.sleep(6*(i+1)); continue
            raise

def strip_tags(s):
    return H.unescape(re.sub(r'<[^>]+>', '', s or '')).strip()

def pick(queries, need):
    for q in queries:
        d = api('https://commons.wikimedia.org/w/api.php?action=query&format=json&list=search&srnamespace=6&srlimit=10&srsearch=' + urllib.parse.quote(q))
        for r in d['query']['search']:
            t = r['title']; tl = t.lower()
            if not tl.endswith(('.jpg','.jpeg','.png')): continue
            if any(x in tl for x in ('map','plan','drawing','diagram')): continue
            if not any(n in tl for n in need): continue
            return t[5:] if t.startswith('File:') else t
        time.sleep(3)
    return None

def cinfo(fname):
    d = api('https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo&iiprop=url|extmetadata|mime&iiurlwidth=850&iiextmetadatafilter=Artist|LicenseShortName&titles=' + urllib.parse.quote('File:' + fname))
    for p in d.get('query', {}).get('pages', {}).values():
        ii = p.get('imageinfo')
        if ii:
            i = ii[0]; em = i.get('extmetadata', {})
            return {'thumb': i.get('thumburl') or i.get('url'), 'page': i.get('descriptionurl',''),
                    'artist': strip_tags(em.get('Artist', {}).get('value','')) or 'неизвестный автор',
                    'license': strip_tags(em.get('LicenseShortName', {}).get('value','')) or 'свободная лицензия',
                    'mime': i.get('mime','')}
    return None

def esc(s):
    return (s or '').replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

done = 0
for page, (queries, need, cap) in JOBS.items():
    p = os.path.join(ROOT, page)
    html = open(p, encoding='utf-8').read()
    if 'hero-photo' in html:
        print('уже:', page); continue
    time.sleep(2)
    fname = pick(queries, need)
    if not fname:
        print('FAIL ничего не найдено:', page); continue
    time.sleep(2)
    info = cinfo(fname)
    if not info or not info['thumb'] or not any(x in info['mime'] for x in ('jpeg','png')):
        print('FAIL mime/инфо:', page, fname); continue
    ext = '.jpg' if 'jpeg' in info['mime'] else '.png'
    fn = re.sub(r'[^a-z0-9]+','-', page[:-5].lower()) + ext
    time.sleep(1.5)
    req = urllib.request.Request(info['thumb'], headers={'User-Agent': 'Scandic-site/1.0'})
    with urllib.request.urlopen(req, timeout=60) as r, open(os.path.join(IMGD, fn), 'wb') as f:
        f.write(r.read())
    fig = ('\n  <figure class="hero-photo">\n'
           f'    <img src="images/stones/{fn}" alt="{esc(cap[:100])}" loading="lazy" decoding="async">\n'
           f'    <figcaption>{cap} Фото: <a href="{info["page"]}">{esc(info["artist"])[:120]}</a> · Wikimedia Commons · {esc(info["license"])}</figcaption>\n'
           '  </figure>\n')
    m = re.search(r'<section[^>]*class="[^"]*section[^"]*"', html)
    if not m:
        print('FAIL якорь', page); continue
    html = html[:m.start()] + fig + html[m.start():]
    open(p, 'w', encoding='utf-8').write(html)
    print('OK', page, '<-', fname, '(%s)' % info['license'])
    done += 1

print('вставлено:', done)
