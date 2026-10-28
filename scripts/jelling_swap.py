#!/usr/bin/env python3
"""Замена гравюры 1591 года на странице «Викинги» на реальный снимок Еллинского камня."""
import json, re, time, urllib.parse, urllib.request, html as H, subprocess, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {'User-Agent': 'Scandic-site/1.0 (contact: olegvnovikov75@github.com)'}

def api(url, tries=6):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return json.load(r)
        except Exception as e:
            if i < tries - 1 and ('429' in str(e) or 'timed out' in str(e) or 'Timeout' in str(e) or 'reset' in str(e).lower() or 'urlopen' in str(e)):
                time.sleep(8 * (i + 1)); continue
            raise

def strip_tags(s):
    return H.unescape(re.sub(r'<[^>]+>', '', s or '')).strip()

BAN = ('prospect', '1591', 'map', 'plan', 'diagram', 'drawing', 'illustration',
       'engraving', 'woodcut', 'etching', 'coat', 'logo', 'model', 'sketch')
QUERIES = ['Jelling stone runic inscription Harald', 'Jelling runestone closeup',
           'Jellingstenen runestone', 'Jelling stone granite monument']
pick = None
for q in QUERIES:
    d = api('https://commons.wikimedia.org/w/api.php?action=query&format=json&list=search&srnamespace=6&srlimit=10&srsearch=' + urllib.parse.quote(q))
    for r in d['query']['search']:
        t = r['title']; tl = t.lower()
        if not tl.endswith(('.jpg', '.jpeg')): continue
        if 'jelling' not in tl or any(b in tl for b in BAN): continue
        pick = t[5:] if t.startswith('File:') else t; break
    if pick: break
    time.sleep(3)
print('выбрано:', pick)
assert pick, 'не найдено фото Еллинского камня'

d = api('https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo&iiprop=url|extmetadata|mime&iiurlwidth=850&iiextmetadatafilter=Artist|LicenseShortName&titles=' + urllib.parse.quote('File:' + pick))
for p in d['query']['pages'].values():
    ii = p.get('imageinfo')
    if not ii: continue
    i = ii[0]; em = i.get('extmetadata', {})
    artist = strip_tags(em.get('Artist', {}).get('value', '')) or 'неизвестный автор'
    lic = strip_tags(em.get('LicenseShortName', {}).get('value', '')) or 'свободная лицензия'
    esc = lambda s: (s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    url = i.get('thumburl') or i.get('url')
    for a in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r, open(os.path.join(ROOT, 'images/stones/vikings.jpg'), 'wb') as f:
                f.write(r.read())
            break
        except Exception as e:
            if a == 3: raise
            time.sleep(10)
    cap = 'Йеллингские камни — «свидетельство о рождении» Дании: Харальд Синезубец возвёл их в память о родителях и о себе — «…приобрёл себе Данию и сделал датчан христианами». Около 965 года.'
    page = i.get('descriptionurl', '')
    h = open(os.path.join(ROOT, 'vikings.html'), encoding='utf-8').read()
    new = re.sub(r'(<img src="images/stones/vikings\.jpg"[^>]*>\s*)<figcaption>.*?</figcaption>',
                 lambda m: m.group(1) + '<figcaption>' + cap + ' Фото: <a href="' + page + '">' + esc(artist)[:120] + '</a> · Wikimedia Commons · ' + esc(lic) + '</figcaption>',
                 h, count=1, flags=re.S)
    open(os.path.join(ROOT, 'vikings.html'), 'w', encoding='utf-8').write(new)
    print('заменено:', lic)

subprocess.run(['git', '-C', ROOT, 'add', '-A'])
subprocess.run(['git', '-C', ROOT, 'commit', '-qm', 'Викинги: Еллинский камень — современный снимок вместо гравюры 1591 года'])
print('коммит есть')
print('пуш:', subprocess.run(['python3', '/home/user/Projects/egypt/scripts/push_github.py', ROOT], capture_output=True, text=True).stdout.strip())
time.sleep(35)
import urllib.request as u2
with u2.urlopen(u2.Request('https://olegvnovikov75.github.io/scandic/vikings.html', headers=UA), timeout=40) as r:
    print('итог в сети, блоков фото:', r.read().decode('utf-8', 'replace').count('hero-photo'))
