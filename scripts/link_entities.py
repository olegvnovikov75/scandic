#!/usr/bin/env python3
"""
link_entities.py — Простановка ссылок на все сущности в текстах HTML-страниц.
v5: разбиение stem по дефисам для точного匹配.
"""

import os, re, csv, glob
from pathlib import Path

ROOT = Path('/home/user/scandic')
CSV_PATH = ROOT / 'data' / 'entities-table.csv'
SKIP_PAGES = {'index.html', 'gods.html', 'myths.html', 'literature.html',
                'about.html', 'contact.html', '404.html'}


def norm_norse(name):
    s = name.lower().strip()
    s = s.replace('ð', 'd').replace('þ', 'th')
    s = s.replace('ó', 'o').replace('á', 'a').replace('é', 'e').replace('ý', 'y')
    s = s.replace('ö', 'o').replace('ü', 'u').replace('å', 'a')
    s = s.replace('æ', 'ae').replace('œ', 'oe')
    return s


def find_best_page(norse_name, all_stems_normed):
    """Находим лучшую страницу для norse_name.
    Разбивает stem по дефисам и ищет совпадения в каждой части."""
    norm_n = norm_norse(norse_name)
    candidates = []
    for stem_n, page in all_stems_normed:
        # 1. Точное совпадение
        if norm_n == stem_n:
            return page
        # 2. Stem целиком содержится в norse_name
        if stem_n and stem_n in norm_n and len(stem_n) >= 3:
            score = 90 - abs(len(norm_n) - len(stem_n))
            candidates.append((score, page))
            continue
        # 3. Norsem_name содержится в stem с дефисным суффиксом
        if norm_n in stem_n:
            suffix = stem_n[len(norm_n):]
            if suffix == '' or suffix.startswith('-') or suffix.startswith('_'):
                score = 60 - len(suffix)
                candidates.append((score, page))
            continue
        # 4. Проверяем каждую часть stem, разбитую по дефисам/подчёркиваниям
        parts = re.split(r'[-_]', stem_n)
        for part in parts:
            if not part or len(part) < 3:
                continue
            # 4a. part ⊂ norse_name
            if part in norm_n:
                score = 85 - abs(len(norm_n) - len(part))
                candidates.append((score, page))
                break
            # 4b. norse_name ⊂ part
            if norm_n in part:
                score = 55 - len(part)
                candidates.append((score, page))
                break
    if candidates:
        candidates.sort(key=lambda x: -x[0])
        return candidates[0][1]
    return None


def collect_entity_map():
    all_stems = []
    for html in glob.glob(str(ROOT / '**' / '*.html'), recursive=True):
        rel = os.path.relpath(html, ROOT)
        if rel in SKIP_PAGES:
            continue
        stem = Path(html).stem.lower()
        stem_n = norm_norse(stem)
        all_stems.append((stem_n, rel))
    print(f"  Индекс файлов: {len(all_stems)}")
    map_rus_to_page = {}
    with open(CSV_PATH, encoding='utf-8') as f:
        for row in csv.DictReader(f):
            rus = row.get('russian_name', '').strip()
            norse = row.get('norse_name', '').strip()
            if not rus or not norse:
                continue
            page = find_best_page(norse, all_stems)
            if page and rus not in map_rus_to_page:
                map_rus_to_page[rus] = page
    return map_rus_to_page


ENTITY_CSS = '''
.entity-link {
    color: #A48B4A;
    text-decoration: none;
    border-bottom: 1px dotted #C4A35A;
    padding-bottom: 1px;
    transition: color .2s ease, border-color .2s ease;
}
.entity-link:hover {
    color: #D4B36A;
    border-bottom-color: #D4B36A;
}
'''


def split_text_and_tags(body):
    parts = []
    cur_text = []
    i, n = 0, len(body)
    while i < n:
        if body[i] == '<':
            if cur_text:
                parts.append((''.join(cur_text), False))
                cur_text = []
            j = body.find('>', i)
            if j == -1:
                cur_text.append(body[i:])
                break
            parts.append((body[i:j + 1], True))
            i = j + 1
        else:
            cur_text.append(body[i])
            i += 1
    if cur_text:
        parts.append((''.join(cur_text), False))
    return parts


def replace_entities_in_text(text, entity_map):
    if not text:
        return text
    result = text
    for name in sorted(entity_map.keys(), key=len, reverse=True):
        escaped = re.escape(name)
        pattern = (r'(?<![a-zA-Zа-яА-ЯёЁ0-9\-\u2013\u2014])'
                   + escaped +
                   r'(?![a-zA-Zа-яА-ЯёЁ0-9\-\u2013\u2014])')
        href = entity_map[name]
        if re.search(pattern, result):
            replacement = f'<a href="{href}" class="entity-link" rel="nofollow">{name}</a>'
            result = re.sub(pattern, replacement, result)
    return result


def process_file(filepath, entity_map):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    rel = os.path.relpath(filepath, ROOT)
    if rel in SKIP_PAGES:
        return 0
    body_m = re.search(r'<body\b[^>]*>([\s\S]*?)</body>', content)
    if not body_m:
        return 0
    body = body_m.group(1)
    parts = split_text_and_tags(body)
    total_replaced = 0
    new_parts = []
    for text, is_tag in parts:
        if not is_tag:
            new_text = replace_entities_in_text(text, entity_map)
            total_replaced += new_text.count('class="entity-link"')
            new_parts.append((new_text, False))
        else:
            new_parts.append((text, True))
    if total_replaced == 0:
        return 0
    new_body = ''.join(t for t, _ in new_parts)
    content = content.replace(body_m.group(1), new_body)
    head_m = re.search(r'<head\b[^>]*>([\s\S]*?)</head>', content)
    if head_m and '.entity-link' not in content:
        css_block = '\n    <style>\n' + ENTITY_CSS.strip() + '\n    </style>'
        content = content.replace('</head>', css_block + '\n</head>')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return total_replaced


def main():
    print("🔍 Сбор сущностей из CSV...")
    entity_map = collect_entity_map()
    print(f"  Связанных со страницами: {len(entity_map)}")
    for name in ['Один', 'Тор', 'Бальдр', 'Локи', 'Фрейя', 'Хель', 'Фенрир', 'Йормунганд', 'Мимир', 'Сурт']:
        if name in entity_map:
            print(f"  {name} → {entity_map[name]}")
    print()
    html_files = []
    for html in glob.glob(str(ROOT / '**' / '*.html'), recursive=True):
        rel = os.path.relpath(html, ROOT)
        if rel not in SKIP_PAGES:
            html_files.append(html)
    print(f"📄 Обработка {len(html_files)} файлов...\n")
    total = 0
    for hf in sorted(html_files):
        rel = os.path.relpath(hf, ROOT)
        count = process_file(hf, entity_map)
        if count > 0:
            total += count
            print(f"  ✅ {rel} — {count} имён")
    print(f"\n✨ Готово! Проставлено {total} ссылок на сущности.")


if __name__ == '__main__':
    main()
