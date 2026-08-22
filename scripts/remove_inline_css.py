#!/usr/bin/env python3
"""
remove_inline_css.py — Удаляет inline <style> блоки из HTML страниц Scandic
"""

import os
import re
from pathlib import Path

ROOT = Path('/home/user/Projects/scandic')

def remove_inline_style(filepath):
    """Удаляет <style>...</style> блоки из HTML файла"""
    content = open(filepath, 'r', encoding='utf-8').read()
    
    # Проверяем есть ли style блок
    if '<style>' not in content:
        return False
    
    # Удалить все <style>...</style> блоки
    original = content
    content = re.sub(r'\s*<style>.*?</style>\s*', '', content, flags=re.DOTALL)
    
    if content != original:
        # Записать обратно
        open(filepath, 'w', encoding='utf-8').write(content)
        return True
    return False

def main():
    print("=" * 60)
    print("🔧 Scandic — Удаление inline CSS")
    print("=" * 60)
    
    modified = 0
    total = 0
    
    # Проверить все HTML файлы
    for html_file in ROOT.rglob('*.html'):
        total += 1
        if remove_inline_style(html_file):
            rel_path = html_file.relative_to(ROOT)
            print(f"  ✅ {rel_path}")
            modified += 1
    
    print()
    print("=" * 60)
    print(f"📊 ИТОГО: Удалено inline стилей: {modified} из {total} файлов")
    print("=" * 60)

if __name__ == '__main__':
    main()
