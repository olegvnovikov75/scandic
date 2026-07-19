#!/usr/bin/env python3
"""
Массовое обновление всех страниц на единый стиль.
Фиксит:
- CSS ссылки на style-new.css
- Классы для нового дизайна
- Добавляет мир-специфичные стили
"""
import os
import re
import glob

BASE = '/home/user/scandic'

# Определения миров для автоматической генерации
WORLD_DATA = {
    'world-asgard.html': {
        'name': 'Асгард',
        'translit': 'Ásgarðr',
        'subtitle': 'Обитель Асов — дом богов',
        'description': 'Асгард — одна из девяти миров в скандинавской мифологии. Это обитель богов Асов, расположенная на одной из ветвей Мирового Древа Иггдрасиля. Асгард соединён с Мидгардом мостом Бифрёст, радужным мостом, который хранит бог Хеймдалль.',
        'ruler': 'Один (Óðinn)',
        'color': 'gold',
        'icon': '⚡'
    },
    'world-vanaheim.html': {
        'name': 'Ванахейм',
        'translit': 'Vanaheimr',
        'subtitle': 'Обитель Ваннир — богов плодородия',
        'description': 'Ванахейм — мир Ваннир, древних богов плодородия, fertility и мудрости. После войны Асов и Ваннир многие Ванир переселились в Асгард, став частью асовского пантеона.',
        'ruler': 'Фрейр (Freyr) и Фрейя (Freyja)',
        'color': 'purple',
        'icon': '🌿'
    },
    'world-midgard.html': {
        'name': 'Мидгард',
        'translit': 'Miðgarðr',
        'subtitle': 'Средний мир — обитель людей',
        'description': 'Мидгард — Средний мир, мир людей, расположенный вокруг моря на земле, созданной из тела первозданного великана Имира. Мидгард окружён океаном, в котором обитает мировой змей Ёрмунганд.',
        'ruler': 'Нет единого правителя',
        'color': 'blue',
        'icon': '🌍'
    },
    'world-jotunheim.html': {
        'name': 'Йотунхейм',
        'translit': 'Jötunheimr',
        'subtitle': 'Обитель великанов Ётунов',
        'description': 'Йотунхейм — мир великанов, древних существ, часто врагов богов, но также и их предков. Некоторые великаны стали супругами богов и родителями великих героев.',
        'ruler': 'Нет единого правителя',
        'color': 'green',
        'icon': '❄️'
    },
    'álfheimr.html': {
        'name': 'Альфхейм',
        'translit': 'Álfheimr',
        'subtitle': 'Обитель светлых эльфов',
        'description': 'Альфхейм — мир светлых эльфов, существ красоты и света. По преданию, этот мир дан богу Фрейру как награда за его подвиги.',
        'ruler': 'Фрейр (Freyr)',
        'color': 'light-alves',
        'icon': '✨'
    },
    'svartálfaheimr.html': {
        'name': 'Свартальфхейм',
        'translit': 'Svartálfaheimr',
        'subtitle': 'Обитель тёмных эльфов и dwarfs',
        'description': 'Свартальфхейм — подземный мир тёмных эльфов (свартальвов) и dwarfs, великих кузнецов и мастеров. Здесь создаются легендарные артефакты богов.',
        'ruler': 'Нет единого правителя',
        'color': 'dark-alves',
        'icon': '⚒️'
    },
    'world-muspelheim.html': {
        'name': 'Муспельхейм',
        'translit': 'Múspellsheimr',
        'subtitle': 'Огненный мир великана Сурта',
        'description': 'Муспельхейм — южный огненный мир, управляемый огненным великаном Суртом. В Рагнароке Сурт сожжёт весь мир своим мечом.',
        'ruler': 'Сурт (Surtr)',
        'color': 'muspelheim',
        'icon': '🔥'
    },
    'world-niflheim.html': {
        'name': 'Нифльхейм',
        'translit': 'Niflheimr',
        'subtitle': 'Мир тумана и льда',
        'description': 'Нифльхейм — северный мир холода, тумана и льда. Из его источников вытекают реки Эливагар, которые в сочетании с пламенем Муспельхейма создали первозданного великана Имира.',
        'ruler': 'Нет единого правителя',
        'color': 'niflheim',
        'icon': '🧊'
    },
    'helheimr.html': {
        'name': 'Хельхейм',
        'translit': 'Hel',
        'subtitle': 'Царство мёртвых, не погибших в бою',
        'description': 'Хельхейм — подземное царство мёртвых, управляемое богиней Хель, дочерью Локи. туда попадают все, кто умер не в бою — от болезни, старости или болезни.',
        'ruler': 'Хель (Hel)',
        'color': 'helheim',
        'icon': '👻'
    }
}

def fix_world_page(filepath, data):
    """Fix a world page to use the new unified style."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace old structure with new
    new_content = f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{data['name']} ({data['translit']}) — {data['subtitle']}">
    <title>{data['name']} — Скандинавская Мифология</title>
    <link rel="stylesheet" href="../css/style-new.css">
</head>
<body class="worlds-page-body">

<!-- ===== СЕВЕРНОЕ СИЯНИЕ ===== -->
<div class="aurora-container">
    <div class="aurora-layer"></div>
    <div class="aurora-layer"></div>
    <div class="aurora-layer"></div>
    <div class="aurora-curtain"></div>
</div>

<!-- ===== ЗВЁЗДЫ ===== -->
<div class="stars" id="stars"></div>

<!-- ===== НАВИГАЦИЯ ===== -->
<nav class="navbar" id="navbar">
    <div class="nav-container">
        <a href="../index.html" class="nav-logo">
            <span class="nav-rune">ᚱ</span>
            <span class="nav-name">Scandic</span>
        </a>
        <ul class="nav-menu" id="navMenu">
            <li><a href="../index.html#worlds" class="nav-link"><span class="rune">☽</span> Миры</a></li>
            <li><a href="../index.html#pantheons" class="nav-link"><span class="rune">⚡</span> Боги</a></li>
            <li><a href="../index.html#runes" class="nav-link"><span class="rune">ᚠ</span> Руны</a></li>
            <li><a href="../index.html#sagas" class="nav-link"><span class="rune">📜</span> Саги</a></li>
            <li><a href="../literature.html" class="nav-link"><span class="rune">📖</span> Литература</a></li>
            <li><a href="../about.html" class="nav-link"><span class="rune">ℹ</span> О проекте</a></li>
        </ul>
        <button class="nav-toggle" id="navToggle" aria-label="Меню">
            <span></span><span></span><span></span>
        </button>
    </div>
</nav>

<!-- ===== ЗАГОЛОВОК МИРА ===== -->
<header class="world-header">
    <div class="world-header-bg"></div>
    <h1 class="world-name">
        <span class="world-name-icon">{data['icon']}</span>
        {data['name']}
    </h1>
    <p class="world-epithet">{data['translit']} — {data['subtitle']}</p>
    <div class="world-divider"></div>
</header>

<!-- ===== КОНТЕНТ ===== -->
<div class="world-content">
    <p>{data['description']}</p>
    
    <h2>👑 Правитель</h2>
    <p><strong>{data['ruler']}</strong></p>
    
    <h2>📖 О {data['name']}</h2>
    <p>{data['description']}</p>
    
    <a href="../index.html" class="back-link">← Назад к древу</a>
</div>

<!-- ===== FOOTER ===== -->
<footer class="footer">
    <div class="footer-content">
        <div class="footer-rune">ᚱ</div>
        <div class="footer-name">SCANDIC</div>
        <p>Скандинавская мифология — миры, боги, руны и легенды</p>
        <p class="footer-copy">© 2026 Scandic.</p>
    </div>
</footer>

<script>
// Навигация
document.getElementById('navToggle').addEventListener('click', function() {{
    document.getElementById('navMenu').classList.toggle('active');
}});
window.addEventListener('scroll', function() {{
    const navbar = document.getElementById('navbar');
    if (window.scrollY > 50) navbar.classList.add('scrolled');
    else navbar.classList.remove('scrolled');
}});
</script>

</body>
</html>'''
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

# Фиксим все мировые страницы
fixed = 0
for fname, data in WORLD_DATA.items():
    fpath = os.path.join(BASE, 'world', fname)
    if os.path.exists(fpath):
        fix_world_page(fpath, data)
        fixed += 1
        print(f'✓ {fname}')
    else:
        print(f'✗ {fname} — не найден')

print(f'\nИсправлено страниц: {fixed}')
