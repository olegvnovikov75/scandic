#!/usr/bin/env python3
"""
add_og_tags.py — Добавляет Open Graph meta tags на все страницы Scandic
"""

import os
import re
from pathlib import Path

ROOT = Path('/home/user/Projects/scandic')

OG_TEMPLATE = '''    <!-- ===== Open Graph / Social Media ===== -->
    <meta property="og:title" content="{title} — Scandic">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="https://olegvnovikov75.github.io/scandic/images/favicon.svg">
    <meta property="og:url" content="https://olegvnovikov75.github.io/scandic/{page}">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title} — Scandic">
    <meta name="twitter:description" content="{description}">
'''

def get_page_info(filepath):
    """Определяет title и description для страницы"""
    rel_path = str(filepath.relative_to(ROOT))
    
    # Базовые описания для основных страниц
    descriptions = {
        'index.html': 'Скандинавская мифология — миры, боги, саги и легенды древних северных народов. Интерактивная энциклопедия с родословным древом.',
        'gods.html': 'Полный справочник богов скандинавской мифологии — асы, ваны, их атрибуты, легенды и взаимосвязи.',
        'myths.html': 'Мифы и саги скандинавской мифологии — от создания мира до Рагнарёка.',
        'literature.html': 'Источники и литература по скандинавской мифологии — Эдды, саги, исследования.',
        'about.html': 'О проекте Scandic — интерактивная энциклопедия скандинавской мифологии.',
        'contact.html': 'Контакты проекта Scandic — скандинавская мифология.',
        '404.html': 'Страница не найдена — Scandic, скандинавская мифология.',
    }
    
    # Для family страниц
    if rel_path.startswith('family/'):
        name = filepath.stem.replace('-', ' ').replace('_', ' ').replace('family-', '').replace('1', '').strip()
        title = name.capitalize()
        description = f'{name.capitalize()} — персонаж скандинавской мифологии. Информация о происхождении, связях и легендах.'
    elif rel_path.startswith('world/'):
        name = filepath.stem.replace('-', ' ').replace('_', ' ').replace('world-', '')
        title = name.capitalize()
        description = f'{name.capitalize()} — один из девяти миров Иггдрасиля в скандинавской мифологии.'
    elif rel_path.startswith('runes/'):
        name = filepath.stem.replace('-', ' ').replace('_', ' ')
        title = name.capitalize()
        description = f'Руна {name.capitalize()} — значение, символы и использование в скандинавской мифологии.'
    elif rel_path.startswith('events/'):
        name = filepath.stem.replace('-', ' ').replace('_', ' ')
        title = name.capitalize()
        description = f'{name.capitalize()} — миф или событие из скандинавской мифологии.'
    else:
        title = filepath.stem.replace('-', ' ').replace('_', ' ').capitalize()
        description = f'{title} — скандинавская мифология. Миры, боги, саги и легенды.'
    
    # Если есть в описаниях, используем его
    if rel_path in descriptions:
        description = descriptions[rel_path]
    
    return title, description, rel_path

def add_og_tags(filepath):
    """Добавляет Open Graph tags на страницу"""
    content = open(filepath, 'r', encoding='utf-8').read()
    
    # Если OG tags уже есть, пропускаем
    if 'property="og:title"' in content:
        return False
    
    title, description, page = get_page_info(filepath)
    
    # Найти место для вставки (после последнего meta tag в head)
    og_tags = OG_TEMPLATE.format(title=title, description=description, page=page)
    
    # Вставить после <title>
    pattern = r'(<title>.*?</title>)'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        insert_pos = match.end()
        new_content = content[:insert_pos] + '\n' + og_tags + content[insert_pos:]
        open(filepath, 'w', encoding='utf-8').write(new_content)
        return True
    
    return False

def main():
    print("=" * 60)
    print("🔧 Scandic — Добавление Open Graph Tags")
    print("=" * 60)
    
    modified = 0
    
    for html_file in ROOT.rglob('*.html'):
        if add_og_tags(html_file):
            rel_path = html_file.relative_to(ROOT)
            print(f"  ✅ {rel_path}")
            modified += 1
    
    print()
    print("=" * 60)
    print(f"📊 ИТОГО: Добавлено OG tags: {modified} файлов")
    print("=" * 60)

if __name__ == '__main__':
    main()
