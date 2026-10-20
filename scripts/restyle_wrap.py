#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""restyle_wrap.py — обёртка старых страниц scandic (family/world/events/runes)
в новый дизайн-шаблон (css/style.css, эталон gods/odin.html).
IN PLACE: пути и имена файлов не меняются → inter-links остаются валидными.
Запуск: python3 scripts/restyle_wrap.py [--dirs family,world,events,runes] [--dry]
"""
import os, re, sys, glob
from bs4 import BeautifulSoup, NavigableString

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NAV = [("index.html","Главная"),("cosmos.html","Космос"),("realms.html","Девять миров"),
       ("gods.html","Боги"),("runes.html","Руны"),("creatures.html","Существа"),
       ("entities.html","Энциклопедия"),("eddas.html","Эдды"),("ragnarok.html","Рагнарёк"),
       ("vikings.html","Викинги"),("timeline.html","Хронология"),("about.html","О сайте")]
# hub: к какой корневой странице тянем breadcrumb и какой пункт nav активен
HUB = {"family": ("entities.html","Энциклопедия",""),
       "world":  ("realms.html","Девять миров","realms.html"),
       "events": ("timeline.html","Хронология","timeline.html"),
       "runes":  ("runes.html","Руны","runes.html")}

EMOJI_RE = re.compile(r'^[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F\u200D\s]+')
RUNIC_RE = re.compile(r'^[\u16A0-\u16FF\U00016FE0-\U00016FFF]{1,2}$')
DROP_CLASSES = {'navbar','aurora-container','stars','nav-menu','nav-container','nav-toggle'}

def nav_html(pfx, active):
    ls = "\n".join(f'    <a href="{pfx}{h}"{" class=\"active\"" if h==active else ""}>{l}</a>'
                   for h,l in NAV)
    return (f'<header class="nav">\n  <a class="nav__logo" href="{pfx}index.html">ᛋ <span>Скандик</span></a>\n'
            f'  <button class="nav__burger" aria-label="Меню">☰</button>\n'
            f'  <nav class="nav__links">\n{ls}\n  </nav>\n</header>')

def clean_heading(t):
    return EMOJI_RE.sub('', t).strip()

def unwrap(el):
    """заменить div на его содержимое (сохраняя порядок)"""
    el.unwrap()

def extract(path):
    raw = open(path, encoding='utf-8').read()
    soup = BeautifulSoup(raw, 'html.parser')
    title = soup.title.get_text(strip=True) if soup.title else os.path.basename(path)
    md = soup.find('meta', attrs={'name':'description'})
    desc = md['content'] if md and md.get('content') else title
    body = soup.body
    # удалить шумold-дизайна
    for sel in ['nav','script','style','footer','.aurora-container','.stars','.navbar']:
        for t in body.select(sel): t.decompose()
    for t in body.find_all('a', class_=['back-link','nav-link']): t.decompose()
    for t in body.find_all(class_=DROP_CLASSES): t.decompose()
    for t in body.find_all('footer'): t.decompose()
    # контейнер контента
    cont = (body.select_one('.character-page') or body.select_one('.event-page')
            or body.select_one('section.section') or body.select_one('.container') or body)
    h1 = cont.find(['h1'])
    name = h1.get_text(strip=True) if h1 else title
    name = EMOJI_RE.sub('', name).strip()
    name = re.sub(r'\s*[—-]\s*Scandic\s*\|.*$', '', name).strip()
    if h1: h1.decompose()
    # subtitle (только p.subtitle — первый p оставим контентом)
    sub = cont.select_one('p.subtitle')
    subtitle = ''
    if sub is not None:
        subtitle = sub.get_text(' ', strip=True)
        sub.decompose()
    # рунический глиф (runes)
    glyph = ''
    for d in cont.find_all('div'):
        t = d.get_text(strip=True)
        if t and RUNIC_RE.match(t):
            glyph = t; d.decompose(); break
    # картинка
    img = cont.find('img')
    img_src = img.get('src','') if img else ''
    img_alt = img.get('alt','') if img else ''
    if img: img.decompose()
    # «Связанные сущности»: ссылки
    related = []
    lk = cont.select_one('.character-links') or cont.select_one('.link-grid')
    if lk:
        for a in lk.find_all('a'):
            related.append((a.get('href',''), a.get_text(' ',strip=True)))
        lk_parent = lk.find_parent('.character-links')
        (lk_parent or lk).decompose()
    # зачистка layout-дивов внутри контента: разворачиваем div'ы без смысловых детей-блоков? 
    # проще: разворачиваем ВСЕ div'ы (порядок сохраняется)
    for _ in range(6):
        divs = cont.find_all('div')
        if not divs: break
        for d in divs: unwrap(d)
    # чистка атрибутов/emojis в сохранённых узлах; href правим под новую структуру
    cur_dir = os.path.dirname(os.path.relpath(path, ROOT))
    def fix_href(h):
        h = h.split('#')[0]
        m = re.match(r'^(family|world|events|runes|gods)/(.+\.html)$', h)
        if m:  # ссылкa вида <dir>/file.html → относительная правильная
            return m.group(2) if m.group(1) == cur_dir else '../' + h
        if re.match(r'^[a-z0-9_-]+\.html$', h):  # корневая страница
            return '../' + h
        return h
    for el in cont.find_all(True):
        if el.name == 'a':
            el.attrs = {'href': fix_href(el.get('href',''))}
        elif el.name == 'img':
            el.attrs = {'src': el.get('src',''), 'alt': el.get('alt',''),
                        'loading':'lazy', 'decoding':'async'}
            if not el['src']: el.decompose(); continue
        else:
            el.attrs = {}
    for h in cont.find_all(['h2','h3','h4']):
        if h.string and EMOJI_RE.match(h.string):
            h.string = clean_heading(h.string)
        else:
            nt = EMOJI_RE.sub('', h.get_text()).strip()
            h.clear(); h.append(NavigableString(nt))
    # пересборка относительных путей не нужна: файл остаётся в той же папке
    inner = ''.join(str(c) for c in cont.children).strip()
    inner = re.sub(r'\s*\n\s*\n+', '\n', inner)
    return dict(name=name, subtitle=subtitle, glyph=glyph, img=img_src, img_alt=img_alt,
                desc=desc, related=related, inner=inner)

def render(d, path, data):
    pfx = '../'  # все обёрнутые страницы лежат на глубине 1
    hub, hub_name, active = HUB[d]
    hero_bits = []
    if data['glyph']:
        hero_bits.append(f'    <div class="god-hero__rune">{data["glyph"]}</div>')
    if data['img']:
        hero_bits.append(f'    <img class="entity-hero__img" src="{data["img"]}" alt="{data["img_alt"]}" loading="lazy" decoding="async">')
    ep = f'    <p class="god-hero__epithets">{data["subtitle"]}</p>' if data['subtitle'] else ''
    desc = f'\n\n  <section class="section">\n    <div class="prose">\n      <p class="section__lead">{data["desc"]}</p>\n    </div>\n  </section>' if data['desc'] and data['desc'] != data['name'] else ''
    rel = ''
    if data['related']:
        def fx(h):
            h = h.split('#')[0]
            m = re.match(r'^(family|world|events|runes|gods)/(.+\.html)$', h)
            if m:
                return m.group(2) if m.group(1) == d else '../' + h
            if re.match(r'^[a-z0-9_-]+\.html$', h):
                return '../' + h
            return h
        cards = "\n".join(f'      <a class="card" href="{fx(h)}"><span class="card__title">{t}</span></a>' for h,t in data['related'] if h)
        if cards:
            rel = f'\n\n  <section class="section">\n    <h2 class="section__title">Связанные</h2>\n    <div class="grid">\n{cards}\n    </div>\n  </section>'
    inner = data['inner']
    page = f'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{data['name']} — Скандик</title>
<meta name="description" content="{data['desc'][:150]}">
<link rel="stylesheet" href="{pfx}css/style.css">
</head>
<body>
{nav_html(pfx, active)}
<main class="main">
  <p class="crumbs"><a href="{pfx}index.html">Главная</a> · <a href="{pfx}{hub}">{hub_name}</a></p>

  <section class="god-hero entity-hero">
{chr(10).join(hero_bits)}
    <h1>{data['name']}</h1>
{ep}
  </section>
{desc}
  <section class="section">
    <div class="prose">
{inner}
    </div>
  </section>{rel}
  <div class="ornament">{"ᚱ" if not data["glyph"] else data["glyph"]}</div>
</main>
<footer class="footer">Скандик · мифология Скандинавии · 2026</footer>
<script src="{pfx}js/main.js"></script>
</body>
</html>
'''
    return page

def main():
    dirs = (sys.argv[sys.argv.index('--dirs')+1].split(',') if '--dirs' in sys.argv
            else ['family','world','events','runes'])
    dry = '--dry' in sys.argv
    n=0
    for d in dirs:
        for f in sorted(glob.glob(os.path.join(ROOT,d,'*.html'))):
            rel = os.path.relpath(f, ROOT)
            data = extract(f)
            page = render(d, rel, data)
            if dry:
                print(f"[dry] {rel}: {data['name']!r} inner={len(data['inner'])}b rel={len(data['related'])}")
            else:
                open(f,'w',encoding='utf-8').write(page)
            n+=1
    print(f"обёрнуто страниц: {n}{' (dry-run)' if dry else ''}")

if __name__ == '__main__':
    main()
