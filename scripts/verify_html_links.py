#!/usr/bin/env python3
"""
verify_html_links.py — Проверка битых ссылок на HTML-страницы
"""

import os
import re
from pathlib import Path

ROOT = Path('/home/user/Projects/scandic')

def main():
    print("=" * 60)
    print("🔧 Scandic — Проверка HTML-ссылок")
    print("=" * 60)
    
    broken_links = []
    total_links = 0
    
    # Собрать все существующие HTML файлы
    existing_files = set()
    for html_file in ROOT.rglob('*.html'):
        rel = html_file.relative_to(ROOT)
        existing_files.add(str(rel))
        existing_files.add(rel.name)
        # Добавить с .html если нет
        if not str(rel).endswith('.html'):
            existing_files.add(str(rel) + '.html')
    
    # Проверить все ссылки
    for html_file in ROOT.rglob('*.html'):
        content = open(html_file, 'r', encoding='utf-8').read()
        rel_file = str(html_file.relative_to(ROOT))
        
        # Найти все href (игнорировать #якоря, http, mailto, javascript)
        links = re.findall(r'href=["\']([^"\']+)["\']', content)
        
        for link in links:
            # Пропустить не-HTML ссылки
            if (link.startswith('#') or 
                link.startswith('http') or 
                link.startswith('mailto') or
                link.startswith('javascript') or
                link.endswith('.css') or
                link.endswith('.js') or
                link.endswith('.svg') or
                link.endswith('.png') or
                link.endswith('.jpg') or
                link.endswith('.jpeg') or
                link.endswith('.gif')):
                continue
            
            total_links += 1
            
            # Проверить если это ссылка на HTML файл
            if '.html' in link or link.endswith('/'):
                # Разобрать путь
                base_link = link.split('#')[0].split('?')[0]
                
                # Решить путь относительно текущего файла
                if base_link.startswith('/'):
                    target = ROOT / base_link[1:]
                elif base_link.startswith('../'):
                    # Относительный путь от текущей папки
                    current_dir = html_file.parent
                    target = (current_dir / base_link).resolve()
                    if ROOT not in target.parents and target != ROOT:
                        target = ROOT / base_link[3:]
                elif base_link.startswith('./'):
                    target = ROOT / base_link[2:]
                elif '/' in base_link:
                    target = ROOT / base_link
                else:
                    # Файл в той же папке
                    target = html_file.parent / base_link
                
                # Проверить существование
                if not target.exists():
                    broken_links.append((rel_file, link))
    
    if broken_links:
        print(f"\n⚠️ Найдено {len(broken_links)} битых HTML-ссылок:")
        for file, link in broken_links[:30]:
            print(f"  {file} → {link}")
        if len(broken_links) > 30:
            print(f"  ... и ещё {len(broken_links) - 30}")
    else:
        print("\n✅ Все HTML-ссылки работают!")
    
    print()
    print("=" * 60)
    print(f"📊 ИТОГО: Проверено HTML-ссылок: {total_links}, Битых: {len(broken_links)}")
    print("=" * 60)

if __name__ == '__main__':
    main()
