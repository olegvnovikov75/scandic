#!/usr/bin/env python3
"""
find_issues.py — Поиск недочётов в Scandic
"""

import os, re, glob
from pathlib import Path

ROOT = Path('/home/user/Projects/scandic')

def check_missing_css_links():
    """Проверка: все ли страницы подключают style-new.css"""
    print("🔍 Проверка подключений CSS...")
    missing = []
    for html in glob.glob(str(ROOT / '**' / '*.html'), recursive=True):
        content = open(html, 'r', encoding='utf-8').read()
        if 'style-new.css' not in content:
            rel = os.path.relpath(html, ROOT)
            missing.append(rel)
    if missing:
        print(f"  ⚠️ Найдено {len(missing)} страниц без style-new.css:")
        for m in missing[:10]:
            print(f"    - {m}")
    else:
        print("  ✅ Все страницы подключают style-new.css")
    return missing

def check_missing_nav():
    """Проверка: все ли страницы имеют унифицированную навигацию"""
    print("\n🔍 Проверка навигации...")
    no_nav = []
    for html in glob.glob(str(ROOT / '**' / '*.html'), recursive=True):
        content = open(html, 'r', encoding='utf-8').read()
        if 'navbar' not in content.lower() and 'nav-menu' not in content:
            rel = os.path.relpath(html, ROOT)
            no_nav.append(rel)
    if no_nav:
        print(f"  ⚠️ Найдено {len(no_nav)} страниц без навигации:")
        for n in no_nav[:10]:
            print(f"    - {n}")
    else:
        print("  ✅ Все страницы имеют навигацию")
    return no_nav

def check_missing_footer():
    """Проверка: все ли страницы имеют footer"""
    print("\n🔍 Проверка footer...")
    no_footer = []
    for html in glob.glob(str(ROOT / '**' / '*.html'), recursive=True):
        content = open(html, 'r', encoding='utf-8').read()
        if '<footer' not in content:
            rel = os.path.relpath(html, ROOT)
            no_footer.append(rel)
    print(f"  ℹ️ Страниц без footer: {len(no_footer)}")
    return no_footer

def check_rune_links():
    """Проверка: ссылки на руны ведут на существующие файлы"""
    print("\n🔍 Проверка ссылок на руны...")
    runes_dir = ROOT / 'runes'
    existing_runes = set(f.stem.lower() for f in runes_dir.glob('*.html'))
    broken_rune_links = []
    
    for html in glob.glob(str(ROOT / '**' / '*.html'), recursive=True):
        content = open(html, 'r', encoding='utf-8').read()
        links = re.findall(r'href=["\']runes/([^"\']+)["\']', content)
        for link in links:
            stem = Path(link).stem.lower()
            if stem not in existing_runes:
                rel = os.path.relpath(html, ROOT)
                broken_rune_links.append((rel, link))
    
    if broken_rune_links:
        print(f"  ⚠️ Найдено {len(broken_rune_links)} битых ссылок на руны:")
        for r, l in broken_rune_links[:10]:
            print(f"    - {r} → {l}")
    else:
        print("  ✅ Все ссылки на руны работают")
    return broken_rune_links

def check_world_links():
    """Проверка: ссылки на миры ведут на существующие файлы"""
    print("\n🔍 Проверка ссылок на миры...")
    worlds_dir = ROOT / 'world'
    existing_worlds = set(f.name for f in worlds_dir.glob('*.html'))
    broken_world_links = []
    
    for html in glob.glob(str(ROOT / '**' / '*.html'), recursive=True):
        content = open(html, 'r', encoding='utf-8').read()
        links = re.findall(r'href=["\']world/([^"\']+)["\']', content)
        for link in links:
            if link not in existing_worlds:
                rel = os.path.relpath(html, ROOT)
                broken_world_links.append((rel, link))
    
    if broken_world_links:
        print(f"  ⚠️ Найдено {len(broken_world_links)} битых ссылок на миры:")
        for r, l in broken_world_links[:10]:
            print(f"    - {r} → {l}")
    else:
        print("  ✅ Все ссылки на миры работают")
    return broken_world_links

def check_family_links():
    """Проверка: ссылки на family страницы"""
    print("\n🔍 Проверка ссылок на family страницы...")
    family_dir = ROOT / 'family'
    existing_family = set(f.name for f in family_dir.glob('*.html'))
    broken_family_links = []
    
    for html in glob.glob(str(ROOT / '**' / '*.html'), recursive=True):
        content = open(html, 'r', encoding='utf-8').read()
        links = re.findall(r'href=["\']family/([^"\']+)["\']', content)
        for link in links:
            if link not in existing_family:
                rel = os.path.relpath(html, ROOT)
                broken_family_links.append((rel, link))
    
    if broken_family_links:
        print(f"  ⚠️ Найдено {len(broken_family_links)} битых ссылок на family:")
        for r, l in broken_family_links[:10]:
            print(f"    - {r} → {l}")
    else:
        print("  ✅ Все ссылки на family страницы работают")
    return broken_family_links

def check_duplicate_rune_names():
    """Проверка: дубликатов названий рун"""
    print("\n🔍 Проверка дубликатов рун...")
    runes_dir = ROOT / 'runes'
    stems = [f.stem.lower() for f in runes_dir.glob('*.html')]
    duplicates = [s for s in stems if stems.count(s) > 1]
    if duplicates:
        print(f"  ⚠️ Найдены дубликаты: {set(duplicates)}")
    else:
        print("  ✅ Дубликатов нет")
    return duplicates

def check_entity_links():
    """Проверка: entity-link используется корректно"""
    print("\n🔍 Проверка entity-ссылок...")
    entity_link_count = 0
    for html in glob.glob(str(ROOT / '**' / '*.html'), recursive=True):
        content = open(html, 'r', encoding='utf-8').read()
        entity_link_count += content.count('class="entity-link"')
    print(f"  ℹ️ Найдено {entity_link_count} entity-ссылок")
    return entity_link_count

def main():
    print("=" * 60)
    print("🔧 Scandic — Поиск недочётов")
    print("=" * 60)
    print()
    
    all_issues = []
    all_issues.extend(check_missing_css_links())
    all_issues.extend(check_missing_nav())
    all_issues.extend(check_missing_footer())
    all_issues.extend(check_rune_links())
    all_issues.extend(check_world_links())
    all_issues.extend(check_family_links())
    check_duplicate_rune_names()
    check_entity_links()
    
    print()
    print("=" * 60)
    print("📊 ИТОГО:")
    print(f"  - Страниц без CSS: {len([i for i in all_issues if 'css' in str(i).lower()])}")
    print(f"  - Битых ссылок: {len([i for i in all_issues if isinstance(i, tuple)])}")
    print("=" * 60)

if __name__ == '__main__':
    main()
