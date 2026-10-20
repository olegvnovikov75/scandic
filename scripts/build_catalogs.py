#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_catalogs.py — каталоги восстановленного контента (этап 2, 20.10.2026)
1) entities.html  — энциклопедия: все family/-страницы, по алфавиту
2) realms.html    — секция-сетка со ссылками на world/
3) timeline.html  — секция-сетка со ссылками на events/
4) creatures.html — карточка-указатель на энциклопедию
5) runes.html     — rune-box'ы становятся ссылками на runes/*.html (по имени)
Все вставки аддитивны, перед </main>; повторный запуск идемпотентен
(маркеры <!-- RESTORED-CATALOG:BEGIN/END -->).
"""
import os, re, sys, glob
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BEGIN, END = "<!-- RESTORED-CATALOG -->", "<!-- /RESTORED-CATALOG -->"

# Эдда-футарк: имя бокса в runes.html → файл в runes/ (ручная сверка 20.10,
# т.к. старый генератор местами напутствовал глифы и имена; Кеназ/Беркана — файлов нет)
BOX2FILE = {"Феху":"fehu.html","Уруз":"uruz.html","Турисаз":"thiwaz.html","Ансуз":"ansuz.html",
  "Рейдз":"rad.html","Гебо":"gebo.html","Вуньо":"wunjo.html","Хагалаз":"hagalaz.html",
  "Наутиз":"naudiz.html","Иса":"isa.html","Йера":"jera.html","Эйваз":"eihwaz.html",
  "Пертро":"perthro.html","Эльгиз":"algiz.html","Совило":"sowilo.html","Тиваз":"tîwaz.html",
  "Эваз":"ehwalaz.html","Манназ":"mannaz.html","Лагуз":"laugaz.html","Ингуз":"ingwaz.html",
  "Дагаз":"dagaz.html","Одала":"othala.html"}

NAV = [("index.html","Главная"),("cosmos.html","Космос"),("realms.html","Девять миров"),
       ("gods.html","Боги"),("runes.html","Руны"),("creatures.html","Существа"),
       ("entities.html","Энциклопедия"),("eddas.html","Эдды"),("ragnarok.html","Рагнарёк"),
       ("vikings.html","Викинги"),("timeline.html","Хронология"),("about.html","О сайте")]

def nav_html(pfx="", active=""):
    ls = "\n".join(f'    <a href="{pfx}{h}"{" class=\"active\"" if h==active else ""}>{l}</a>'
                   for h,l in NAV)
    return (f'<header class="nav">\n  <a class="nav__logo" href="{pfx}index.html">ᛋ <span>Скандик</span></a>\n'
            f'  <button class="nav__burger" aria-label="Меню">☰</button>\n'
            f'  <nav class="nav__links">\n{ls}\n  </nav>\n</header>')

def esc(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def page_info(f):
    s = BeautifulSoup(open(f, encoding='utf-8'), 'html.parser')
    h1 = s.find('h1')
    name = h1.get_text(strip=True) if h1 else os.path.basename(f)
    ep = s.select_one('.god-hero__epithets')
    lead = s.select_one('.section__lead')
    sub = (ep or lead)
    sub = sub.get_text(' ', strip=True) if sub else ''
    glyph_el = s.select_one('.god-hero__rune')
    glyph = glyph_el.get_text(strip=True) if glyph_el else ''
    return dict(file=os.path.basename(f), name=name, sub=sub, glyph=glyph)

def cards(items, pfx="", note_len=110):
    out=[]
    for it in items:
        sub = it['sub']
        sub = re.sub(r'\s*[—-]\s*Scandic\s*\|.*$', '', sub)      # SEO-хвост
        sub = re.sub(r'\(\s*'+re.escape(it['name'])+r'\s*\)', '', sub)  # дубль имени в скобках
        if sub.lower().startswith(it['name'].lower()): sub = sub[len(it['name']):].lstrip(' —:·')
        if len(sub) > note_len: sub = sub[:note_len].rstrip(' ,.;—')+'…'
        rune = f'<span class="card__rune" aria-hidden="true">{it["glyph"] or "ᛋ"}</span>' if it.get('glyph') else ''
        txt = f'<p class="card__text">{esc(sub)}</p>' if sub and sub != it['name'] else ''
        out.append(f'      <a class="card" href="{pfx}{it.get("href", it["file"])}">{rune}'
                   f'<h3 class="card__title">{esc(it["name"])}</h3>{txt}</a>')
    return "\n".join(out)

def section(title, sub, items, pfx=""):
    return (f'{BEGIN}\n  <section class="section">\n    <h2 class="section__title">{title}</h2>\n'
            f'    <p class="section__lead">{sub}</p>\n'
            f'    <div class="grid" style="margin-top:1.6rem;">\n{cards(items, pfx)}\n    </div>\n  </section>\n{END}\n')

def inject(path, sec_html):
    raw = open(path, encoding='utf-8').read()
    # удалить прежнюю вставку (идемпотентность)
    raw = re.sub(re.escape(BEGIN)+r'.*?'+re.escape(END)+r'\n?', '', raw, flags=re.S)
    anchor = '</main>'
    if anchor not in raw:
        print(f"! {path}: нет </main>, пропуск"); return False
    raw = raw.replace(anchor, sec_html + anchor, 1)
    open(path, 'w', encoding='utf-8').write(raw)
    return True

def main():
    dry = '--dry' in sys.argv
    # 0) раскладка runes/: настоящие руны связываются с runes.html по глифу,
    #    не-руны (осколки старого генератора «Руна X») уходят в энциклопедию
    rp = os.path.join(ROOT,'runes.html')
    rsoup = BeautifulSoup(open(rp, encoding='utf-8'), 'html.parser')
    boxes = {}
    for b in rsoup.select('.rune-box'):
        nm = b.select_one('.rune-box__name')
        if nm: boxes.setdefault(nm.get_text(strip=True), b)
    rune_files = {v for v in BOX2FILE.values() if os.path.exists(os.path.join(ROOT,'runes',v))}
    extra_pages = []
    for f in sorted(glob.glob(os.path.join(ROOT,'runes','*.html'))):
        pi = page_info(f)
        if pi['file'] not in rune_files:
            pi2 = dict(pi)
            pi2['name'] = re.sub(r'^Руна\s+', '', pi2['name']).strip() or pi2['file']
            extra_pages.append(pi2)
    # 1) entities.html
    fam_items = []
    for f in glob.glob(os.path.join(ROOT,'family','*.html')):
        pi = page_info(f); pi['href'] = 'family/' + pi['file']; fam_items.append(pi)
    for pi in extra_pages:
        pi['href'] = 'runes/' + pi['file']; fam_items.append(pi)
    fam = sorted(fam_items, key=lambda x: x['name'].lower())
    letters = {}
    for it in fam:
        l = it['name'][0].upper() if it['name'] else 'А'
        letters.setdefault(l, []).append(it)
    secs=[]
    for l in sorted(letters, key=str):
        items=letters[l]
        secs.append(f'''  <section class="section">
    <h2 class="section__title">{l}</h2>
    <div class="grid" style="margin-top:1.2rem;">
{cards(items, note_len=90)}
    </div>
  </section>''')
    entities = f'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Энциклопедия — Скандик</title>
<meta name="description" content="Энциклопедия скандинавской мифологии: {len(fam)} существ — боги, великаны, чудовища, герои и предметы. Скандик.">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
{nav_html("", "entities.html")}
<main class="main">
  <section class="page-head">
    <h1 class="page-head__title">Энциклопедия</h1>
    <p class="page-head__sub">{len(fam)} существ и мест скандинавской мифологии: асы и ваны, великаны и чудовища, герои и предметы — по алфавиту.</p>
  </section>

{chr(10).join(secs)}
  <div class="ornament">ᛖ</div>
</main>
<footer class="footer">Скандик · мифология Скандинавии · 2026</footer>
<script src="js/main.js"></script>
</body>
</html>
'''
    if dry:
        print(f"[dry] entities.html: {len(fam)} карточек, {len(letters)} букв")
    else:
        open(os.path.join(ROOT,'entities.html'),'w',encoding='utf-8').write(entities)

    # 2) realms.html ← world/
    worlds = sorted((page_info(f) for f in glob.glob(os.path.join(ROOT,'world','*.html'))),
                    key=lambda x: x['name'].lower())
    if not dry: inject(os.path.join(ROOT,'realms.html'),
        section('Все миры', f'{len(worlds)} страниц миров и мест Иггдрасиля.', worlds, 'world/'))
    # 3) timeline.html ← events/
    events = sorted((page_info(f) for f in glob.glob(os.path.join(ROOT,'events','*.html'))),
                    key=lambda x: x['name'].lower())
    if not dry: inject(os.path.join(ROOT,'timeline.html'),
        section('События и сказания', f'{len(events)} страниц: мифы, эпизоды и понятия.', events, 'events/'))
    # 4) creatures.html ← указатель
    if not dry: inject(os.path.join(ROOT,'creatures.html'),
        f'''{BEGIN}
  <section class="section">
    <h2 class="section__title">Население девяти миров</h2>
    <p class="section__lead">Здесь — избранные существа. Полный каталог из {len(fam)} имён (великаны и асы, карлики и эльфы, чудовища и герои) — в <a href="entities.html">Энциклопедии</a>.</p>
    <p><a class="btn" href="entities.html">Открыть энциклопедию</a></p>
  </section>
{END}
''')
    # 5) runes.html — rune-box → ссылка по BOX2FILE; + починить глифы на страницах рун
    linked = 0
    # сброс предыдущих инкапсуляций (первый проход связал часть боксов неверно)
    for b in rsoup.select('a.rune-box'):
        b.name = 'div'
        if b.has_attr('href'): del b['href']
    for name, f in BOX2FILE.items():
        b = boxes.get(name)
        if b is None or not os.path.exists(os.path.join(ROOT,'runes',f)): continue
        g = b.select_one('.rune-box__glyph')
        box_glyph = g.get_text(strip=True) if g else ''
        if b.name != 'a':
            b.name = 'a'; b['href'] = 'runes/' + f
            linked += 1
        # глиф страницы = глиф бокса (старый генератор путал ᛉ/ᛊ, ᛜ/ᛝ, ᛟ/ᛏ...)
        if not dry and box_glyph:
            pf = os.path.join(ROOT,'runes',f)
            ps = BeautifulSoup(open(pf, encoding='utf-8'), 'html.parser')
            gr = ps.select_one('.god-hero__rune')
            if gr and gr.get_text(strip=True) != box_glyph:
                gr.string = box_glyph
                open(pf,'w',encoding='utf-8').write(str(ps))
    if not dry:
        open(rp,'w',encoding='utf-8').write(str(rsoup))
    print(f"runes.html: linked rune-box = {linked}; рун-файлов: {len(rune_files)}; extras (не-руны) → энцикл.: {len(extra_pages)}")
    print("каталоги готовы")

if __name__ == '__main__':
    main()
