#!/usr/bin/env python3
"""
T3 (Цикл 2, 23.08.2026): унификация <title> всех HTML-страниц Scandic.

Целевой формат:
  - обычные страницы:  {Название} — Scandic | Скандинавская мифология
  - index.html:        Scandic — Скандинавская мифология
  - 404.html:          404 — Scandic | Скандинавская мифология

Действия:
  - обходит все *.html (включая подпапки, кроме scripts/);
  - извлекает <title>...</title>;
  - обрезает существующие суффиксы-варианты: « — Скандинавская Мифология»,
    « - Скандинавская Мифология», « — Скандинавская мифология»,
    « | Скандинавская мифология», « — Scandic», « - Scandic»
    и любые их комбинации с разделителями « — » / « - » / « | »
    (case-insensitive, в цикле — по одному суффиксу за итерацию);
  - убирает эмодзи и лишние пробелы;
  - если после обрезки название пустое или равно «Scandic» / «Скандинавская мифология»
    — файл НЕ трогает, выписывает в отчёт как edge case;
  - печатает отчёт: файл → старый title → новый title (только изменённые).

Идемпотентен: повторный запуск не меняет ничего (0 изменений).
Коммит НЕ делает — его делает контролёр.
"""
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # корень проекта

BRAND_WORDS = [
    'Скандинавская Мифология',
    'Скандинавская мифология',
    'Scandic',
]

# Эмодзи и служебные символы (проверено сканом: не пересекаются с
# легитимными диакритиками U+00D0–U+00FF и кириллицей)
EMOJI_RE = re.compile(
    '['
    '\U0001F000-\U0001FAFF'   # pictographs, emoticons, symbols (вкл. U+1F300–U+1FAFF)
    '\u2600-\u27BF'           # misc symbols & dingbats (⚡ и т.п.)
    '\u2B00-\u2BFF'           # stars и пр.
    '\u2300-\u23FF'           # technical (⌚⏰)
    '\u2139'                 # ℹ
    '\u200D'                 # ZWJ
    '\uFE0F'                 # variation selector
    '\u2764'                 # ❤
    '\u2728'                 # ✨
    ']'
)

TITLE_RE = re.compile(r'<title[^>]*>(.*?)</title>', re.S | re.I)

INDEX_TARGET = 'Scandic — Скандинавская мифология'
NOTFOUND_TARGET = '404 — Scandic | Скандинавская мифология'
BRAND_SUFFIX = ' — Scandic | Скандинавская мифология'


def strip_suffixes(s):
    """Обрезает хвостовые бренд-суффиксы с разделителями, в любых комбинациях."""
    changed = True
    while changed:
        changed = False
        for word in BRAND_WORDS:
            pat = re.compile(
                r'(\s*[—\-|]\s*)?' + re.escape(word) + r'\s*$',
                re.IGNORECASE,
            )
            m = pat.search(s)
            if m and m.start() > 0:  # не срезаем название целиком
                s = s[:m.start()].strip()
                changed = True
    return s


def clean_name(s):
    """Убирает эмодзи (собирает список) и лишние пробелы."""
    removed = []
    def _collect(m):
        removed.append(m.group(0))
    s = EMOJI_RE.sub(_collect, s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s, removed


def main():
    files = []
    for root, dirs, fnames in os.walk(BASE):
        rel = os.path.relpath(root, BASE)
        if rel == 'scripts' or rel.startswith('scripts' + os.sep):
            continue
        for f in fnames:
            if f.endswith('.html'):
                files.append(os.path.join(root, f))
    files.sort()

    changed, unchanged, edge_cases, emoji_found = [], 0, [], []

    for path in files:
        rel = os.path.relpath(path, BASE)
        data = open(path, encoding='utf-8', errors='replace').read()
        m = TITLE_RE.search(data)
        if not m:
            edge_cases.append((rel, '<NO TITLE TAG>', 'нет тега <title>'))
            continue
        old = m.group(1)
        old_disp = re.sub(r'\s+', ' ', old).strip()

        # Специальные страницы — целевой title целиком
        if rel == 'index.html':
            new = INDEX_TARGET
        elif rel == '404.html':
            new = NOTFOUND_TARGET
        else:
            name, removed = clean_name(old)
            if removed:
                emoji_found.append((rel, old_disp, removed))
            name = strip_suffixes(name)
            if name == '' or name.lower() in {'scandic', 'скандинавская мифология'}:
                edge_cases.append((rel, old_disp,
                                   f'название после обрезки: {name!r} — не чиним молча'))
                continue
            new = name + BRAND_SUFFIX

        if new == old_disp:
            unchanged += 1
            continue

        new_data = TITLE_RE.sub(lambda _: f'<title>{new}</title>', data, count=1)
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(new_data)
        changed.append((rel, old_disp, new))

    # ---------- ОТЧЁТ ----------
    print('=' * 70)
    print(f'fix_titles.py: всего HTML={len(files)}, изменено={len(changed)}, '
          f'без изменений={unchanged}, edge cases={len(edge_cases)}')
    print('=' * 70)

    print(f'\n--- ИЗМЕНЕНО ({len(changed)}) ---')
    for rel, old, new in changed:
        print(f'{rel}\n  old: {old}\n  new: {new}')

    print(f'\n--- УБРАНО ЭМОДЗИ ({len(emoji_found)}) ---')
    for rel, old, removed in emoji_found:
        marks = ', '.join(f'{ch!r} U+{ord(ch):04X}' for ch in removed)
        print(f'{rel}: title {old!r} → удалено: {marks}')

    print(f'\n--- EDGE CASES ({len(edge_cases)}) — файлы НЕ изменены ---')
    for rel, old, why in edge_cases:
        print(f'{rel}: title {old!r} — {why}')

    return 0


if __name__ == '__main__':
    sys.exit(main())
