#!/usr/bin/env python3
"""Скандик: реальные фото рунных камней (лид-изображения статей en.wikipedia) + подписи с атрибуцией."""
import json, os, re, time, urllib.parse, urllib.request, html as H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMGD = os.path.join(ROOT, 'images', 'stones')
os.makedirs(IMGD, exist_ok=True)

# страница -> (заголовок статьи, подпись)
JOBS = {
 'vikings.html': ('Jelling stones',
   'Йеллингские камни — «свидетельство о рождении» Дании: Харальд Синезубец возвёл их в память о родителях и о себе — «…приобрёл себе Данию и сделал датчан христианами». Около 965 года.'),
 'runes.html': ('Rök runestone',
   'Рёк — самый длинный рунический текст в мире: около семисот рун, IX век. Гадательные загадки, песни о готских конунгах и погоне на льду — память о Великом переселении народов.'),
 'creatures.html': ('Altuna runestone',
   'Альтуна (Уппланд): Сигурд, поражающий змея Фафнира среди его витков, — один из древнейших каменных образов саги о Вёльсунгах, XI век.'),
 'timeline.html': ('Kylver stone',
   'Кюльверский камень с Готланда — древнейший полный футарк: все двадцать четыре руны подряд, около 400 года.'),
}

CSS = '''
/* --- фотографии рунных камней --- */
.hero-photo { margin: 1.6rem 0 0; }
.hero-photo img { width: 100%; max-height: 460px; object-fit: cover;
  border-radius: 14px; border: 1px solid rgba(201,162,39,.35); }
.hero-photo figcaption { font-size: .85rem; color: var(--ink-dim, #9aa7b8);
  text-align: center; margin-top: .45rem; line-height: 1.5; }
.hero-photo figcaption a { color: inherit; }
'''
css_path = os.path.join(ROOT, 'css', 'style.css')
_ct = open(css_path, encoding='utf-8').read()
if '.hero-photo {' not in _ct:
    open(css_path, 'a', encoding='utf-8').write(CSS)

def api(url, tries=4):
    for i in range(tries):
        req = urllib.request.Request(url, headers={'User-Agent': 'Scandic-site/1.0 (contact: olegvnovikov75@github.com)'})
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.load(r)
        except Exception as e:
            if i < tries-1 and ('429' in str(e) or 'timed out' in str(e) or 'Timeout' in str(e)):
                time.sleep(5*(i+1)); continue
            raise

def strip_tags(s):
    return H.unescape(re.sub(r'<[^>]+>', '', s or '')).strip()

def lead(wtitle):
    d = api('https://en.wikipedia.org/w/api.php?action=query&format=json&prop=pageimages&piprop=name&titles=' + urllib.parse.quote(wtitle))
    for p in d.get('query', {}).get('pages', {}).values():
        n = p.get('image', {}).get('name')
        if n:
            return n
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
for page, (wt, cap) in JOBS.items():
    p = os.path.join(ROOT, page)
    html = open(p, encoding='utf-8').read()
    if 'hero-photo' in html:
        print('уже:', page); continue
    time.sleep(2.5)
    try:
        name = lead(wt)
    except Exception as e:
        print('FAIL лид', page, repr(e)); continue
    if not name:
        print('FAIL нет лид-картинки', page, wt); continue
    time.sleep(2.0)
    try:
        info = cinfo(name)
    except Exception as e:
        print('FAIL инфо', page, repr(e)); continue
    if not info or not info['thumb'] or not any(x in info['mime'] for x in ('jpeg','png')):
        print('FAIL mime', page, name); continue
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
    print('OK', page, '<-', name, '(%s)' % info['license'])
    done += 1

print('вставлено:', done)
