#!/usr/bin/env python3
"""
fix_broken_links.py — Исправляет битые ссылки на family страницы
"""

import re
from pathlib import Path

ROOT = Path('/home/user/Projects/scandic')

# Паттерны для исправления
replacements = [
    # family/* → family/family-* (если ссылается на файл в той же папке)
    (r'href=["\']family-([^\s"\'>]+)\.html["\']', r'href="family-\1.html"'),
    # ../family-* → ../family/family-*
    (r'href=["\]\.\./family-([^\s"\'>]+)\.html["\']', r'href="../family/family-\1.html"'),
]

def fix_links_in_file(filepath):
    """Исправляет битые ссылки в HTML файле"""
    content = open(filepath, 'r', encoding='utf-8').read()
    original = content
    
    # Исправить ссылки вида ../family-xxx.html → ../family/family-xxx.html
    content = re.sub(
        r'href=["\']\.\./family-([^\s"\'>]+\.html)["\']',
        r'href="../family/family-\1"',
        content
    )
    
    # Исправить ссылки вида family-xxx.html (в world/* и других) → ../family/family-xxx.html
    content = re.sub(
        r'href=["\']family-([^\s"\'>]+\.html)["\']',
        r'href="../family/family-\1"',
        content
    )
    
    if content != original:
        open(filepath, 'w', encoding='utf-8').write(content)
        return True
    return False

def main():
    print("=" * 60)
    print("🔧 Scandic — Исправление битых ссылок")
    print("=" * 60)
    
    modified = 0
    
    for html_file in ROOT.rglob('*.html'):
        if fix_links_in_file(html_file):
            rel_path = html_file.relative_to(ROOT)
            print(f"  ✅ {rel_path}")
            modified += 1
    
    print()
    print("=" * 60)
    print(f"📊 ИТОГО: Исправлено файлов: {modified}")
    print("=" * 60)

if __name__ == '__main__':
    main()
