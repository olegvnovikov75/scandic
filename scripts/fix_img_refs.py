#!/usr/bin/env python3
"""fix_img_refs.py — фикс битых <img src> на images/*.

Алгоритм для каждого src, начинающегося с images/ или ../images/:
  (1) путь резолвится относительно директории файла        -> оставить
  (2) не резолвится, но с/без ../ резолвится               -> поправить путь
  (3) не резолвится, но basename по транслиту резолвится   -> заменить имя
  (4) иначе                                                -> avatar-default.svg

Идемпотентен. Отчёт: число правок по типам + список (3).
"""
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRANSLIT = {'þ': 'th', 'ð': 'd', 'æ': 'ae', 'ǫ': 'o', 'ø': 'o', 'ǵ': 'g'}


def translit(s: str) -> str:
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return s.lower().translate(TRANSLIT)


def resolve(html_dir: str, src: str) -> str:
    return os.path.normpath(os.path.join(ROOT, html_dir, src))


def fix_file(path: str, stats: dict, rename_list: list):
    html_dir = os.path.dirname(path)
    text = open(path, encoding='utf-8').read()
    changed = False

    def repl(m):
        nonlocal changed
        src = m.group(3)
        if not (src.startswith('images/') or src.startswith('../images/')):
            return m.group(0)
        # (1) уже ок
        if os.path.exists(resolve(html_dir, src)):
            return m.group(0)
        # (2) поправить путь: ../images/ <-> images/
        alt = ('../' + src if not src.startswith('../') else src[4:])
        if os.path.exists(resolve(html_dir, alt)):
            stats['path'] += 1
            changed = True
            return m.group(1) + m.group(2) + alt + m.group(2)
        # (3) транслит имени
        d, name = os.path.split(src)
        base, ext = os.path.splitext(name)
        target = os.path.join(d, translit(base) + ext)
        if target != src and os.path.exists(resolve(html_dir, target)):
            stats['translit'] += 1
            changed = True
            rename_list.append((os.path.basename(path), src, target))
            return m.group(1) + m.group(2) + target + m.group(2)
        # (4) плейсхолдер
        ph = ('../images/avatar-default.svg' if html_dir and html_dir != '.'
              else 'images/avatar-default.svg')
        if src != ph:
            stats['placeholder'] += 1
            changed = True
        return m.group(1) + m.group(2) + ph + m.group(2)

    new = re.sub(r'(<img\b[^>]*?\bsrc=)(["\'])([^"\']+)\2',
                 lambda m: repl(m), text)
    if changed:
        open(path, 'w', encoding='utf-8').write(new)
        stats['files'] += 1


def main():
    stats = {'files': 0, 'path': 0, 'translit': 0, 'placeholder': 0}
    rename_list = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in ('.git', 'scripts', 'memory')]
        for fn in sorted(filenames):
            if fn.endswith('.html'):
                fix_file(os.path.join(dirpath, fn), stats, rename_list)
    print(f"Файлов изменено: {stats['files']}")
    print(f"  (2) путь:        {stats['path']}")
    print(f"  (3) транслит:    {stats['translit']}")
    print(f"  (4) плейсхолдер: {stats['placeholder']}")
    for f, old, new in rename_list:
        print(f"  {f}: {old} -> {new}")


if __name__ == '__main__':
    sys.exit(main())
