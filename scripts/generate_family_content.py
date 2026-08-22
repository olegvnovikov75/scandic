#!/usr/bin/env python3
"""
generate_family_content.py — Наполняет страницы персонажей контентом из CSV и Эдд
"""

import csv
import re
from pathlib import Path

ROOT = Path('/home/user/Projects/scandic')
CSV_FILE = ROOT / 'data' / 'entities-table.csv'

# База знаний о персонажах (мифологические данные)
MYTHOLOGY_DATA = {
    'ægir': {
        'russian': 'Эгир',
        'norse': 'Ægir',
        'description': 'Эгир — великан, хозяин моря. Живёт в подводном дворце, где устраивает пиры для богов. Его жена — Ран, собирающая утопленников в своей сети. Эгир олицетворяет мощь и непредсказуемость морских волн.',
        'origin': 'Род великанов',
        'family': {
            'spouse': 'Ран (Rán)',
            'children': 'Херсим (Hergim), Бард (Bár), Рагнар (Ragnarr)'
        },
        'connections': ['rán', 'lók', 'tórr'],
        'legends': [
            'Эгир заставил богов сварить для него эль в огромных котлах',
            'Тор добыл котёл у великана Хьёрра для Эгира',
            'На пирах у Эгира Локи устроил ссору с богами'
        ],
        'sources': 'Прозаическая Эдда, Гюльвагиннинг'
    },
    'angrboða': {
        'russian': 'Анграбода',
        'norse': 'Angrboða',
        'description': 'Анграбода ("Вносящая скорбь") — великанша из Йотунхейма, жена Локи и мать трёх ужасных существ: Фенрира (огромного волка), Ёрмунганда (Мирового Змея) и Хель (владычицы мёртвых). Она символизирует злобу и хаос.',
        'origin': 'Йотунхейм, род великанов',
        'family': {
            'spouse': 'Локи (Lóki)',
            'children': 'Фенрир (волк), Ёрмунганд (змей), Хель (владычица мёртвых)'
        },
        'connections': ['lóki', 'fenrir', 'jǫrmungandr', 'hel'],
        'legends': [
            'Богам предсказали, что дети Анграбоды принесут беды Асгарду',
            'Хель была отправлена Одином в Хельхейм',
            'Ёрмунганд бросили в море, где он вырос и обвил Мир'
        ],
        'sources': 'Прозаическая Эдда, Скильдакапа'
    },
    'auðumbla': {
        'russian': 'Аудумбла',
        'norse': 'Auðumbla',
        'description': 'Аудумбла — первозданная корова, возникшая из тающего льда в Нифльхейме. Из её сосков текло четыре реки молока, которыми она кормила Ймира. Сама она питалась, обликая солёный лед.',
        'origin': 'Первозданный лёд Нифльхейма',
        'family': {
            'children': 'Борр (лизала лёд три дня)'
        },
        'connections': ['ýmir', 'borr', 'bestla'],
        'legends': [
            'Первый день — из льда появилась голова человека',
            'Второй день — появилась голова и плечи',
            'Третий день — весь человек (Борр) был создан'
        ],
        'sources': 'Прозаическая Эдда, Младшая Эдда'
    },
    'mimir': {
        'russian': 'Мимир',
        'norse': 'Mímir',
        'description': 'Мимир — хранитель источника мудрости у корней Иггдрасиля. Один пожертвовал своим глазом, чтобы напиться из источника и получить мудрость. Мимир олицетворяет знание и память.',
        'origin': 'Род Ванов',
        'family': {
            'siblings': 'Бельгорн (отец Одина по некоторым версиям)'
        },
        'connections': ['óðinn', 'vandir', 'yggdrasill'],
        'legends': [
            'Один пожертвовал глазом, чтобы напиться из источника Мимира',
            'Мимир был отрублен во время войны Асов и Ванов',
            'Один сохранил голову Мимира, которая давала советы'
        ],
        'sources': 'Прозаическая Эдда, Поэтическая Эдда'
    }
}

def get_mythology_info(name):
    """Получить мифологическую информацию о персонаже"""
    return MYTHOLOGY_DATA.get(name.lower(), {})

def generate_family_content(csv_row):
    """Сгенерировать контент для страницы персонажа"""
    info = get_mythology_info(csv_row['norse_name'])
    
    if not info:
        return None
    
    description = info.get('description', csv_row['role'])
    origin = info.get('origin', csv_row['origin'])
    
    family = info.get('family', {})
    connections = info.get('connections', [])
    legends = info.get('legends', [])
    sources = info.get('sources', 'Эдды')
    
    return {
        'description': description,
        'origin': origin,
        'family': family,
        'connections': connections,
        'legends': legends,
        'sources': sources
    }

def update_family_page(filepath, content_data):
    """Обновить HTML страницу персонажа новым контентом"""
    html = open(filepath, 'r', encoding='utf-8').read()
    
    # Добавить описание
    if 'description' in content_data:
        desc_pattern = r'(<div class="character-info">.*?<h2>.*?</h2>)'
        desc_html = f'''
                <p class="character-description">{content_data['description']}</p>
                <p><strong>Происхождение:</strong> {content_data['origin']}</p>'''
        html = re.sub(desc_pattern, r'\1' + desc_html, html, flags=re.DOTALL)
    
    # Добавить семью
    if 'family' in content_data and content_data['family']:
        family_html = '<h3>👨‍👩‍👧 Семья</h3><ul class="family-list">'
        for rel, name in content_data['family'].items():
            family_html += f'<li><strong>{rel}:</strong> {name}</li>'
        family_html += '</ul>'
        html = re.sub(r'(<h3>🔗 Связанные сущности</h3>)', family_html + r'\1', html)
    
    # Добавить легенды
    if 'legends' in content_data and content_data['legends']:
        legends_html = '<h3>📜 Легенды</h3><ul class="legends-list">'
        for legend in content_data['legends']:
            legends_html += f'<li>{legend}</li>'
        legends_html += '</ul>'
        html = re.sub(r'(<div class="character-links">)', legends_html + r'\1', html)
    
    # Добавить источники
    sources_html = f'<h3>📚 Источники</h3><p>{content_data["sources"]}</p>'
    html = re.sub(r'(<footer>)', sources_html + r'\1', html)
    
    open(filepath, 'w', encoding='utf-8').write(html)
    return True

def main():
    print("=" * 60)
    print("🔧 Scandic — Наполнение контента персонажей")
    print("=" * 60)
    
    updated = 0
    
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['norse_name'].lower().replace('/', '-')
            filepath = ROOT / 'family' / f'family-{name}.html'
            
            if filepath.exists():
                content_data = generate_family_content(row)
                if content_data:
                    if update_family_page(filepath, content_data):
                        print(f"  ✅ {filepath.name}")
                        updated += 1
    
    print()
    print("=" * 60)
    print(f"📊 ИТОГО: Обновлено страниц: {updated}")
    print("=" * 60)

if __name__ == '__main__':
    main()
