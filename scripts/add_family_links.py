#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""add_family_links.py — блок «Семья и род» на страницах-сущностях family/*.html:
ссылки на страницы родов (family-*.html), где персонаж живёт в семейном древе.
Совпадение: имя сущности (лемма) встречается в заголовке рода («Род Сиф», «Один и Грёд»).
Идемпотентно: маркер <!-- FAMLINK -->.
"""
import os, re, glob
import pymorphy3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = "<!-- FAMLINK -->"

def h1(path):
    m = re.search(r'<h1>([^<]+)</h1>', open(path, encoding='utf-8').read())
    return m.group(1).strip() if m else None

def lems(text, morph):
    return {morph.parse(w)[0].normal_form for w in re.findall(r'[А-ЯЁа-яё]+', text)}

def main():
    morph = pymorphy3.MorphAnalyzer()
    fam = os.path.join(ROOT, 'family')
    clans = []
    for f in sorted(glob.glob(os.path.join(fam, 'family-*.html'))):
        t = h1(f)
        if not t: continue
        words = [w for w in re.findall(r'[А-ЯЁа-яё]+', t) if w.lower() not in ('род', 'и', 'или')]
        for w in words:
            lem = morph.parse(w.lower())[0].normal_form
            clans.append((lem, os.path.basename(f), t))
    by_lem = {}
    for lem, fn, t in clans:
        by_lem.setdefault(lem, {})[fn] = t

    n = 0
    for p in sorted(glob.glob(os.path.join(fam, '*.html'))):
        base = os.path.basename(p)
        if base.startswith('family-'): continue
        s = open(p, encoding='utf-8').read()
        if MARK in s: continue
        name = h1(p)
        if not name: continue
        nl = lems(name, morph)
        hits = sorted({fn for lem in nl for fn in by_lem.get(lem, {})})
        # без самоссылок: род назван в честь этого же персонажа — всё равно полезен
        if not hits: continue
        titles = {fn: t for lem in nl for fn, t in by_lem.get(lem, {}).items()}
        lis = "\n        ".join(f'<li><a class="entity-link" href="{fn}">{titles[fn]} — семья и родичи</a></li>' for fn in hits)
        block = ('  <section class="section">\n    ' + MARK + '\n    <div class="prose">\n'
                 '      <h2>Семья и род</h2>\n      <ul>\n        ' + lis +
                 '\n      </ul>\n    </div>\n  </section>\n')
        m = re.search(r'\n(\s*<div class="ornament">)', s)
        if m:
            s = s[:m.start(1)] + block + s[m.start(1):]
        else:
            s = s.replace('</main>', block + '</main>', 1)
        open(p, 'w', encoding='utf-8').write(s)
        n += 1
    print('страниц с блоком «Семья и род»:', n)

if __name__ == '__main__':
    main()
