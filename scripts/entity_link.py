#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""entity_link.py v2 — упоминания сущностей → ссылки (хирургически, без пересборки HTML).

Словарь: h1 страниц family/, gods/, world/, events/, runes/ + алиасы.
Морфология: pymorphy3 — ловит любые падежи («под Иггдрасилем», «Одина»).
Правила:
  - текст внутри <main>, вне <a>, вне h1/nav/footer/script/style;
  - на собственную страницу не ссылается;
  - существующим <a> на страницу сущности добавляется класс entity-link;
  - diff минимален: changing только изменённые текстовые сегменты.
Запуск: python3 entity_link.py --page PATH [--dry] | --all [--dry]
"""
import os, re, sys, glob
import pymorphy3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRS = ['family', 'gods', 'world', 'events', 'runes']
EXCLUDE = ('rad2.html', 'olaval.html')

ALIAS = {
    'Всеотец': 'gods/odin.html', 'Вседержитель': 'gods/odin.html',
    'Громовик': 'gods/thor.html', 'Громовержец': 'gods/thor.html',
    'Ванатис': 'gods/freya.html',
    'Лоптр': 'gods/loki.html',
    'Мировой ясень': 'world/world-yggdrasill.html',
    'Мировое древо': 'world/world-yggdrasill.html',
    'Древо Иггдрасиль': 'world/world-yggdrasill.html',
    # имена-варианты и справочные
    'Имир': 'family/ymir.html',
    'Вальхалла': 'runes/valhöll.html', 'Валхалла': 'runes/valhöll.html',
    'Эдда': 'eddas.html', 'Старшая Эдда': 'eddas.html', 'Младшая Эдда': 'eddas.html',
    'Гюльвагиннинг': 'eddas.html', 'Прорицание вёльвы': 'eddas.html',
    'Руна': 'runes.html', 'Футарк': 'runes.html', 'Старший Футарк': 'runes.html',
}

SKIP_TAGS = {'a', 'h1', 'nav', 'footer', 'script', 'style', 'button'}

def collect_entities():
    ents = {}
    # gods в приоритете: сначала остальные, потом gods перезапишут
    ordered = [d for d in DIRS if d != 'gods'] + ['gods']
    for d in ordered:
        for f in sorted(glob.glob(os.path.join(ROOT, d, '*.html'))):
            rel = os.path.relpath(f, ROOT)
            if any(x in rel for x in EXCLUDE): continue
            s = open(f, encoding='utf-8').read()
            m = re.search(r'<h1>([^<]+)</h1>', s)
            if not m: continue
            name = m.group(1).strip()
            if len(name) < 2: continue
            ents[name.lower()] = {'page': rel, 'name': name}
    for a, tgt in ALIAS.items():
        ents.setdefault(a.lower(), {'page': tgt, 'name': a})
    # авто-алиасы из страниц родов family-*.html: имена, не имеющие своей страницы,
    # ссылаются на страницу рода («Сив — жена» → family-sif.html)
    clan_names = {re.sub(r'^род\s+', '', n) for n in ents if n.startswith('род ')}
    existing_lemmas = None  # вычислим леммы позже; здесь — по именам
    for f in sorted(glob.glob(os.path.join(ROOT, 'family', 'family-*.html'))):
        rel = os.path.relpath(f, ROOT).replace(os.sep, '/')
        s = open(f, encoding='utf-8').read()
        m = re.search(r'<h1>([^<]+)</h1>', s)
        if not m: continue
        title = m.group(1).strip()
        words = re.findall(r'[А-ЯЁа-яё]+', title)
        for w in words:
            wl = w.lower()
            if wl in ('род', 'и', 'или'): continue
            ents.setdefault(wl, {'page': rel, 'name': w, 'clan': True})
    return ents

def build_indexes(ents, morph):
    single, multi = {}, {}
    for name, e in ents.items():
        words = re.findall(r'[а-яёa-z]+', name.lower())
        if not words: continue
        if len(words) == 1:
            w = words[0]
            if len(w) < 2: continue
            lem = morph.parse(w)[0].normal_form
            prev = single.get(lem)
            # приоритет: gods/ > любая страница > алиас рода (clan)
            if prev is None or (
                (prev.get('clan') and not e.get('clan')) or
                (not prev['page'].startswith('gods/') and e['page'].startswith('gods/'))):
                single[lem] = e
        else:
            lem = ' '.join(morph.parse(w)[0].normal_form for w in words)
            multi[lem] = e
    return single, multi

def process(path, morph, single, multi, pages_set, dry=False):
    cur = os.path.relpath(path, ROOT).replace(os.sep, '/')
    depth = cur.count('/')
    prefix = '../' * depth
    s = open(path, encoding='utf-8').read()
    segs = re.split(r'(<[^>]*>)', s)
    out = []
    n_links = 0
    n_class = 0
    in_main = False
    skip_stack = []  # имена тегов, внутри которых не линкуем
    for i, seg in enumerate(segs):
        if seg.startswith('<'):
            t = seg.lower()
            # комментарий?
            if t.startswith('<!--'):
                out.append(seg); continue
            mtag = re.match(r'<(/?)([a-z0-9]+)', t)
            if mtag:
                closing, tag = mtag.group(1) == '/', mtag.group(2)
                void = tag in ('img', 'br', 'hr', 'meta', 'link', 'input')
                if tag == 'main':
                    in_main = not closing
                if tag in SKIP_TAGS and not void:
                    if closing:
                        if skip_stack and skip_stack[-1] == tag:
                            skip_stack.pop()
                        else:
                            # закрывающий без открывающего — игнор
                            pass
                    else:
                        skip_stack.append(tag)
            # класс entity-link для существующих <a> на страницы-сущности
            if re.match(r'<a[\s>]', t) and 'href=' in seg and 'entity-link' not in seg:
                hm = re.search(r'href="([^"#]+?)(?:#[^"]*)?"', seg)
                if hm and not hm.group(1).startswith(('http', 'mailto', 'tel', 'javascript')):
                    tgt = os.path.normpath(os.path.join(os.path.dirname(cur), hm.group(1))).replace(os.sep, '/')
                    if not tgt.endswith('.html'): tgt += '.html'
                    if tgt in pages_set and tgt != cur:
                        if 'class="' in seg:
                            seg2 = seg.replace('class="', 'class="entity-link ', 1)
                        else:
                            seg2 = re.sub(r'(<a)\b', r'\1 class="entity-link"', seg, count=1)
                        n_class += 1
                        out.append(seg2); continue
            out.append(seg); continue
        # текстовый сегмент
        if not in_main or skip_stack or not re.search(r'[А-ЯЁа-яё]{2,}', seg):
            out.append(seg); continue
        linked, cnt = link_text(seg, morph, single, multi, cur, prefix)
        n_links += cnt
        out.append(linked)
    res = ''.join(out)
    if not dry and res != s:
        open(path, 'w', encoding='utf-8').write(res)
    return n_links, n_class

WORD = re.compile(r'[А-ЯЁа-яёA-Za-z]+')
CAPITAL_ONLY = {'один'}  # леклеммы-омонимы: ссылаться только на заглавную форму (Бог Один, не «один глаз»)

def link_text(text, morph, single, multi, cur, prefix):
    spans = []
    consumed = -1
    for m in WORD.finditer(text):
        if m.start() < consumed: continue
        w = m.group(0)
        nxt = WORD.search(text, m.end())
        pair_hit = False
        if nxt and 0 <= nxt.start() - m.end() <= 2:
            pair = (w + ' ' + nxt.group(0)).lower()
            lem_pair = ' '.join(morph.parse(x)[0].normal_form for x in pair.split())
            e = multi.get(lem_pair)
            if e and e['page'] != cur:
                spans.append((m.start(), nxt.end(), e))
                consumed = nxt.end()
                pair_hit = True
        if not pair_hit:
            lem = morph.parse(w.lower())[0].normal_form
            e = single.get(lem)
            if e and lem in CAPITAL_ONLY and not w[0].isupper():
                e = None
            if e and e['page'] != cur:
                spans.append((m.start(), m.end(), e))
                consumed = m.end()
    if not spans:
        return text, 0
    pieces, last = [], 0
    for a, b, e in spans:
        pieces.append(text[last:a])
        pieces.append(f'<a class="entity-link" href="{prefix}{e["page"]}">{text[a:b]}</a>')
        last = b
    pieces.append(text[last:])
    return ''.join(pieces), len(spans)

def main():
    args = sys.argv[1:]
    dry = '--dry' in args
    if '--page' in args:
        pages = [os.path.join(ROOT, args[args.index('--page') + 1])]
    elif '--all' in args:
        pages = [f for d in DIRS for f in glob.glob(os.path.join(ROOT, d, '*.html'))]
        roots = ['index', 'cosmos', 'ragnarok', 'eddas', 'vikings', 'myths',
                 'literature', 'about', 'creatures', 'gods', 'realms', 'timeline',
                 'entities', 'contact']
        pages += [os.path.join(ROOT, r + '.html') for r in roots if
                  os.path.exists(os.path.join(ROOT, r + '.html'))]
    else:
        print(__doc__); sys.exit(1)
    morph = pymorphy3.MorphAnalyzer()
    ents = collect_entities()
    single, multi = build_indexes(ents, morph)
    pages_set = {e['page'] for e in ents.values()}
    print(f'словарь: {len(single)} однословных лемм, {len(multi)} фраз')
    tl = tc = 0
    for p in pages:
        nl, nc = process(p, morph, single, multi, pages_set, dry)
        tl += nl; tc += nc
        if nl or nc:
            print(f'  {os.path.relpath(p, ROOT)}: новых ссылок {nl}, помечено существующих {nc}')
    print(f'ИТОГО: {tl} ссылок + {tc} помеченных{" (dry-run)" if dry else ""}')

if __name__ == '__main__':
    main()
