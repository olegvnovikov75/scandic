#!/usr/bin/env python3
"""Генерация sitemap.xml для сайта Scandic (github.io).

Обходит все *.html в корне проекта и подпапках (кроме scripts/ и .git/),
строит URL относительно базового https://olegvnovikov75.github.io/scandic/,
пишет sitemap.xml в корень проекта.

Правила:
  - index.html (корень)  -> https://olegvnovikov75.github.io/scandic/
  - остальные            -> https://olegvnovikov75.github.io/scandic/<относительный путь>
  - имена с диакритикой (óðinn, jǫrmungandr, ...) — в URL как есть (UTF-8),
    percent-encoding НЕ нужен для github.io
  - lastmod — единая дата для всех
  - URL отсортированы по алфавиту, без дублей
"""

import os
import sys

BASE_URL = "https://olegvnovikov75.github.io/scandic/"
LASTMOD = "2026-08-23"

# Директории, которые пропускаем
EXCLUDE_DIRS = {".git", "scripts"}

# Корень проекта = родитель папки scripts/ (скрипт лежит в <root>/scripts/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def collect_html_files(root):
    """Собрать относительные пути всех *.html (без EXCLUDE_DIRS)."""
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        # не спускаться в исключённые папки (in-place модификация)
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fn in filenames:
            if fn.lower().endswith(".html"):
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, root)
                files.append(rel.replace(os.sep, "/"))
    return files


def to_url(rel_path):
    """Относительный путь -> URL."""
    if rel_path == "index.html":
        return BASE_URL  # корень, без index.html
    return BASE_URL + rel_path


def main():
    rel_files = collect_html_files(PROJECT_ROOT)

    # URL: без дублей, по алфавиту (детерминированный вывод)
    urls = sorted({to_url(p) for p in rel_files})

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for u in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{u}</loc>")
        lines.append(f"    <lastmod>{LASTMOD}</lastmod>")
        lines.append("  </url>")
    lines.append("</urlset>")
    lines.append("")  # завершающий newline

    out_path = os.path.join(PROJECT_ROOT, "sitemap.xml")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Сгенерировано URL: {len(urls)}")
    print(f"Найдено HTML-файлов: {len(rel_files)}")
    print(f"Записано: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
