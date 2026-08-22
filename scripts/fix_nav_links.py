#!/usr/bin/env python3
"""
fix_nav_links.py — Исправляет навигационные ссылки в подпапках
"""

import os
import re
from pathlib import Path

ROOT = Path('/home/user/Projects/scandic')

def fix_nav_in_file(filepath):
    """Исправляет навигационные ссылки в HTML файле"""
    content = open(filepath, 'r', encoding='utf-8').read()
    original = content
    
    # Путь относительно ROOT
    rel_path = filepath.relative_to(ROOT)
    depth = len(rel_path.parts) - 1  # Количество папок от ROOT
    
    if depth == 0:
        return False  # Файл в корне не нужно менять
    
    # Префикс для выхода из подпапки
    prefix = '../' * depth
    
    # Исправить навигационные ссылки в navbar
    # href="index.html" → href="../index.html" (в подпапках)
    nav_patterns = [
        # Навигационное меню
        (r'href=["\']index\.html(["\'])', f'href="{prefix}index.html\\1'),
        (r'href=["\']index\.html#(worlds|pantheons|runes|sagas)["\']', f'href="{prefix}index.html#\\1"'),
        (r'href=["\']gods\.html(["\'])', f'href="{prefix}gods.html\\1'),
        (r'href=["\']myths\.html(["\'])', f'href="{prefix}myths.html\\1'),
        (r'href=["\']literature\.html(["\'])', f'href="{prefix}literature.html\\1'),
        (r'href=["\']about\.html(["\'])', f'href="{prefix}about.html\\1'),
        (r'href=["\']contact\.html(["\'])', f'href="{prefix}contact.html\\1'),
        
        # Back-link
        (r'href=["\']index\.html["\']', f'href="{prefix}index.html"'),
        
        # CSS и JS (уже должны быть правильными, но проверим)
        (r'href=["\']css/style-new\.css(["\'])', f'href="{prefix}css/style-new.css\\1'),
        (r'src=["\']js/main\.js(["\'])', f'src="{prefix}js/main.js\\1'),
    ]
    
    for pattern, replacement in nav_patterns:
        content = re.sub(pattern, replacement, content)
    
    if content != original:
        open(filepath, 'w', encoding='utf-8').write(content)
        return True
    return False

def main():
    print("=" * 60)
    print("🔧 Scandic — Исправление навигационных ссылок")
    print("=" * 60)
    
    modified = 0
    
    for html_file in ROOT.rglob('*.html'):
        rel_path = html_file.relative_to(ROOT)
        if rel_path.parts[0] != rel_path.name:  # В подпапке
            if fix_nav_in_file(html_file):
                print(f"  ✅ {rel_path}")
                modified += 1
    
    print()
    print("=" * 60)
    print(f"📊 ИТОГО: Исправлено файлов: {modified}")
    print("=" * 60)

if __name__ == '__main__':
    main()
