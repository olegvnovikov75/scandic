#!/usr/bin/env python3
"""
Проверка всех ссылок в файлах Scandic на корректность.
"""

import os
from pathlib import Path
from html.parser import HTMLParser
import re

scandic_dir = Path('/home/user/.openclaw/workspace/scandic-project/Scandic')

class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    self.links.append(attr[1])

def extract_links(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parser = LinkExtractor()
    parser.feed(content)
    return parser.links

def verify_link(link, all_files):
    """Проверить ссылку на существование."""
    # Игнорируем внешние ссылки и якоря
    if link.startswith('http') or link.startswith('#') or 'scandic' in link:
        return True, "Внешняя ссылка"
    
    # Проверяем относительные пути
    for f in all_files:
        full_path = scandic_dir / link
        if full_path.exists() or (f.name == link and Path(f).parent.exists()):
            return True, "Ссылка найдена"
    
    return False, "Ссылка не найдена"

def main():
    # Собрать все файлы
    all_files = list(scandic_dir.glob('*.html')) + \
                 list(scandic_dir.glob('world-*.html')) + \
                 list(scandic_dir.glob('literature.html')) + \
                 list(scandic_dir.glob('about.html')) + \
                 list(scandic_dir.glob('contacts.html')) + \
                 list(scandic_dir.glob('404.html'))
    
    print(f"📂 Найдено {len(all_files)} файлов\n")
    
    all_links = set()
    for f in all_files:
        links = extract_links(str(f))
        all_links.update(links)
    
    broken = []
    for link in sorted(all_links):
        exists, reason = verify_link(link, all_files)
        status = "✅" if exists else "❌"
        print(f"{status} {link[:60]}{'...' if len(link) > 60 else ''}")
        
        if not exists:
            broken.append((link, f"Не найдена в {len(all_files)} файлах"))
    
    print(f"\n{'='*50}")
    print(f"📊 ИТОГО: {len(broken)} потенциально битых ссылок")

if __name__ == '__main__':
    main()