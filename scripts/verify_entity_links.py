#!/usr/bin/env python3
"""
verify_entity_links.py — Проверка работоспособности entity-link
"""

import os
import re
from pathlib import Path

ROOT = Path('/home/user/Projects/scandic')

def main():
    print("=" * 60)
    print("🔧 Scandic — Проверка entity-links")
    print("=" * 60)
    
    broken_links = []
    total_links = 0
    
    # Собрать все существующие HTML файлы
    existing_files = set()
    for html_file in ROOT.rglob('*.html'):
        rel = html_file.relative_to(ROOT)
        existing_files.add(str(rel))
        existing_files.add(rel.name)
    
    # Проверить все ссылки
    for html_file in ROOT.rglob('*.html'):
        content = open(html_file, 'r', encoding='utf-8').read()
        rel_file = html_file.relative_to(ROOT)
        
        # Найти все entity-link href
        links = re.findall(r'href=["\']([^"\']+)["\']', content)
        
        for link in links:
            total_links += 1
            # Проверить если это ссылка на локальный файл
            if not link.startswith('http') and not link.startswith('#'):
                # Нормализовать путь
                if link.startswith('family/'):
                    target = ROOT / link
                elif link.startswith('../family/'):
                    target = ROOT / link[3:]
                elif '/' in link:
                    target = ROOT / link
                else:
                    target = ROOT / link
                
                if not target.exists():
                    broken_links.append((str(rel_file), link))
    
    if broken_links:
        print(f"\n⚠️ Найдено {len(broken_links)} битых ссылок:")
        for file, link in broken_links[:20]:
            print(f"  {file} → {link}")
        if len(broken_links) > 20:
            print(f"  ... и ещё {len(broken_links) - 20}")
    else:
        print("\n✅ Все ссылки работают!")
    
    print()
    print("=" * 60)
    print(f"📊 ИТОГО: Проверено ссылок: {total_links}, Битых: {len(broken_links)}")
    print("=" * 60)

if __name__ == '__main__':
    main()
