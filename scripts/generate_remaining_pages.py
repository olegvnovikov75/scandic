#!/usr/bin/env python3
"""Generate ALL remaining pages for Scandic project.

Covers:
- Family character pages (missing from CSV)
- World pages (9 realms)
- Rune pages (Elder Futhark)
- Event/Myth pages
- Structure/Location pages
"""
import csv
import os
import re
from pathlib import Path

SCANDIC_DIR = Path('/home/user/scandic')
FAMILY_DIR = SCANDIC_DIR / 'family'
WORLD_DIR = SCANDIC_DIR / 'world'
RUNES_DIR = SCANDIC_DIR / 'runes'
EVENTS_DIR = SCANDIC_DIR / 'events'
CSV_PATH = SCANDIC_DIR / 'data' / 'entities-table.csv'

# Load existing pages
existing_pages = set()
for d in [SCANDIC_DIR, FAMILY_DIR, WORLD_DIR, RUNES_DIR, EVENTS_DIR]:
    if d.exists():
        for f in d.glob('*.html'):
            existing_pages.add(f.stem)

def slugify(name):
    """Convert a name to a safe slug."""
    slug = name.lower()
    # Replace special chars
    slug = re.sub(r'[^\w]+', '-', slug)
    slug = slug.strip('-')
    # Ensure unique
    base = slug
    counter = 1
    while slug in existing_pages:
        slug = f'{base}_{counter}'
        counter += 1
    return slug

def make_unique_slug(name, dir_name):
    """Make a unique slug considering the target directory."""
    slug = slugify(name)
    base = slug
    counter = 1
    while slug in existing_pages:
        slug = f'{base}_{counter}'
        counter += 1
    return slug

def create_dir_if_needed(path):
    """Create directory if it doesn't exist."""
    parent = path.parent
    if not parent.exists():
        parent.mkdir(parents=True)

def generate_character_page(row):
    """Generate a character page for family/."""
    russian = row['russian_name']
    norse = row['norse_name']
    german = row['german_name']
    origin = row['origin']
    role = row['role']
    
    slug = make_unique_slug(norse, 'family')
    filepath = FAMILY_DIR / f'{slug}.html'
    create_dir_if_needed(filepath)
    
    existing_pages.add(slug)
    
    # Build related links
    related = []
    pairs = [
        ('odin', 'Óðinn'), ('thor', 'Þórr'), ('freyja', 'Freyja'),
        ('freyr', 'Freyr'), ('loki', 'Loki'), ('hel', 'Hel'),
        ('fenrir', 'Fenrir'), ('jormungandr', 'Jörmungandr'),
        ('baldr', 'Baldr'), ('borr', 'Borr'), ('buri', 'Búri'),
        ('mimir', 'Mímir'), ('heimdall', 'Heimdall'), ('skadi', 'Skadi'),
        ('jord', 'Jörð'), ('frigg', 'Frigg'), ('sif', 'Sif'),
        ('bragi', 'Bragi'), ('tyr', 'Týr'), ('vidar', 'Víðarr'),
        ('vali', 'Váli'), ('magni', 'Magni'), ('modi', 'Móði'),
        ('thruth', 'Þrúðr'), ('ull', 'Ullr'), ('hermod', 'Hermóðr'),
        ('forseti', 'Forseti'), ('angrboda', 'Angrboða'), ('yimir', 'Ymir'),
        ('ran', 'Rán'), ('njord', 'Njörðr'), ('idunn', 'Idunn'),
        ('od', 'Óðr'),
    ]
    norse_l = norse.lower()
    russ_l = russian.lower()
    for k, n in pairs:
        if k in norse_l or k in russ_l:
            related.append((f'../family/{k}.html', n))
    
    html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{russian} ({norse}) — {role}">
    <title>{russian} — Скандинавская Мифология</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <div class="container">
        <header>
            <a href="../index.html" class="back-link">← На главную</a>
            <h1>{russian}</h1>
            <p class="subtitle">{norse} — {role}</p>
        </header>

        <div class="character-page">
            <div class="character-main">
                <div class="character-image">
                    <img src="../images/{slug}.svg" alt="{norse}" onerror="this.src='../images/odin.svg'">
                </div>
                <div class="character-info">
                    <h2>{norse}</h2>
                    <p><strong>Происхождение:</strong> {origin}</p>
                    <p><strong>Германическое имя:</strong> {german}</p>
                    <p><strong>Роль:</strong> {role}</p>
                </div>
            </div>

            <div class="character-links">
                <h3>🔗 Связанные сущности</h3>
                <div class="link-grid">
'''
    for lp, ln in related:
        html += f'                    <a href="{lp}" class="link-card">{ln}</a>\n'
    if not related:
        html += '                    <p class="no-links">Нет связанных сущностей</p>\n'
    
    html += f'''                </div>
            </div>
        </div>

        <footer>
            <p>© 2024 Скандинавская Мифология</p>
            <p><a href="../index.html">← На главную</a> | <a href="../about.html">О проекте</a></p>
        </footer>
    </div>
</body>
</html>'''
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return slug, 'family'

def generate_world_page(row):
    """Generate a world page in world/."""
    russian = row['russian_name']
    norse = row['norse_name']
    origin = row['origin']
    role = row['role']
    
    slug = make_unique_slug(norse, 'world')
    filepath = WORLD_DIR / f'{slug}.html'
    create_dir_if_needed(filepath)
    existing_pages.add(slug)
    
    html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{russian} ({norse}) — {role}">
    <title>{russian} — Скандинавская Мифология</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <div class="container">
        <header>
            <a href="../index.html" class="back-link">← На главную</a>
            <h1>{russian}</h1>
            <p class="subtitle">{norse} — {role}</p>
        </header>

        <div class="character-page">
            <div class="character-main">
                <div class="character-image">
                    <img src="../images/odin.svg" alt="{norse}">
                </div>
                <div class="character-info">
                    <h2>{norse}</h2>
                    <p><strong>Происхождение:</strong> {origin}</p>
                    <p><strong>Роль:</strong> {role}</p>
                </div>
            </div>
        </div>

        <footer>
            <p>© 2024 Скандинавская Мифология</p>
            <p><a href="../index.html">← На главную</a> | <a href="../about.html">О проекте</a></p>
        </footer>
    </div>
</body>
</html>'''
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return slug, 'world'

def generate_rune_page(row):
    """Generate a rune page in runes/."""
    norse = row['norse_name']
    german = row['german_name']
    role = row['role']
    
    slug = make_unique_slug(norse, 'runes')
    filepath = RUNES_DIR / f'{slug}.html'
    create_dir_if_needed(filepath)
    existing_pages.add(slug)
    
    html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Руна {norse}: {role}">
    <title>Руна {norse} — Скандинавская Мифология</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <div class="container">
        <header>
            <a href="../index.html" class="back-link">← На главную</a>
            <h1>Руна {norse}</h1>
            <p class="subtitle">{german} — {role}</p>
        </header>

        <div class="rune-page">
            <div class="rune-main">
                <div class="rune-symbol-large">
                    <span style="font-size: 5em; color: var(--accent-gold);">ᚠ</span>
                </div>
                <div class="rune-info">
                    <h2>{norse}</h2>
                    <p><strong>Германическое имя:</strong> {german}</p>
                    <p><strong>Значение:</strong> {role}</p>
                </div>
            </div>
        </div>

        <footer>
            <p>© 2024 Скандинавская Мифология</p>
            <p><a href="../index.html">← На главную</a> | <a href="../literature.html">Источники</a></p>
        </footer>
    </div>
</body>
</html>'''
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return slug, 'runes'

def generate_event_page(row):
    """Generate an event/myth page in events/."""
    russian = row['russian_name']
    norse = row['norse_name']
    origin = row['origin']
    role = row['role']
    
    slug = make_unique_slug(norse, 'events')
    filepath = EVENTS_DIR / f'{slug}.html'
    create_dir_if_needed(filepath)
    existing_pages.add(slug)
    
    html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{russian} ({norse}): {role}">
    <title>{russian} — Скандинавская Мифология</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <div class="container">
        <header>
            <a href="../index.html" class="back-link">← На главную</a>
            <h1>{russian}</h1>
            <p class="subtitle">{norse} — {origin}</p>
        </header>

        <div class="event-page">
            <div class="event-main">
                <div class="event-icon">
                    <span style="font-size: 4em;">⚔️</span>
                </div>
                <div class="event-info">
                    <h2>{norse}</h2>
                    <p><strong>Место:</strong> {origin}</p>
                    <p><strong>Описание:</strong> {role}</p>
                </div>
            </div>
        </div>

        <footer>
            <p>© 2024 Скандинавская Мифология</p>
            <p><a href="../index.html">← На главную</a> | <a href="../literature.html">Источники</a></p>
        </footer>
    </div>
</body>
</html>'''
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return slug, 'events'

def categorize_entity(entity):
    """Determine the category of an entity."""
    norse = entity['norse_name'].lower()
    origin = entity['origin'].lower()
    role = entity['role'].lower()
    
    # Runes
    rune_keywords = ['руна', 'феху', 'урюз', 'турисаз', 'ансуз', 'райдо',
                     'кеназ', 'гебо', 'вунхо', 'хаглаз', 'иса', 'йера',
                     'эйваз', 'перт', 'альгиз', 'соуло', 'тейваз', 'берканан',
                     'меназ', 'ингвиз', 'дагаз', 'матхузанг', 'лаутиз',
                     'кауназ', 'наудиз', 'феху', 'ур', 'тюр', 'гебо', 'вун',
                     'хагл', 'ис', 'яр', 'их', 'пер', 'альг', 'сол', 'тейв',
                     'берк', 'мен', 'инг', 'даг', 'мат', 'лауг', 'каук', 'науд']
    
    for kw in rune_keywords:
        if kw in norse or kw in role:
            return 'rune'
    
    # Worlds
    world_keywords = ['мир', 'обитель', 'хейм', 'царство', 'земля', 'пустота']
    for kw in world_keywords:
        if kw in norse or kw in origin:
            return 'world'
    
    # Events/Myths
    event_keywords = ['война', 'битва', 'свадьба', 'пиры', 'утление',
                      'обмен', 'конечная', 'повесился', 'выколол', 'похитил',
                      'рыбачит', 'переодет', 'увязание', 'прикован',
                      'практикует', 'создали', 'создают', 'выбор',
                      'оскорбляет', 'траур', 'едет', 'убил', 'вложил',
                      'молот', 'создание', 'создал', 'генерация']
    for kw in event_keywords:
        if kw in norse or kw in role or kw in origin:
            return 'event'
    
    # World structures
    structure_keywords = ['мировое дерево', 'радужный мост', 'зал', 'поле',
                          'трон', 'источник', 'пропасть', 'река',
                          'белка', 'олень', 'орёл', 'змей', 'волк',
                          'пёс', 'конь', 'первоздан', 'эпитет',
                          'альтернатив', 'прародитель', 'кузнец',
                          'из червей', 'из глины', 'брачный',
                          'род ', 'связанные', 'брага', 'год',
                          'баня', 'купель', 'дом', 'семейная',
                          'нужда', 'жизненная', 'героизм',
                          'плодородие', 'трансформация', 'защита',
                          'изобилие', 'выживание']
    for kw in structure_keywords:
        if kw in norse or kw in role or kw in origin:
            return 'event'
    
    return 'family'

def main():
    # Read CSV
    entities = []
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            entities.append(row)
    
    print(f"📖 Loaded {len(entities)} entities from CSV")
    
    # Deduplicate
    seen = set()
    unique = []
    for e in entities:
        n = e['norse_name'].strip()
        if n not in seen:
            seen.add(n)
            unique.append(e)
    
    print(f"📖 Unique entities: {len(unique)}")
    
    # Find missing entities
    missing = []
    for entity in unique:
        norse = entity['norse_name'].lower()
        has_match = False
        for slug in existing_pages:
            if norse in slug or slug in norse:
                has_match = True
                break
        if not has_match:
            missing.append(entity)
    
    print(f"⚠️ Missing pages: {len(missing)}")
    
    # Categorize and generate
    family_count = 0
    world_count = 0
    rune_count = 0
    event_count = 0
    
    for entity in missing:
        cat = categorize_entity(entity)
        
        if cat == 'family':
            slug, _ = generate_character_page(entity)
            family_count += 1
        elif cat == 'world':
            slug, _ = generate_world_page(entity)
            world_count += 1
        elif cat == 'rune':
            slug, _ = generate_rune_page(entity)
            rune_count += 1
        else:
            slug, _ = generate_event_page(entity)
            event_count += 1
        
        if (family_count + world_count + rune_count + event_count) % 10 == 0:
            print(f"  Generated {family_count + world_count + rune_count + event_count}...")
    
    total = family_count + world_count + rune_count + event_count
    
    print(f"\n📊 Summary:")
    print(f"  Family pages: +{family_count}")
    print(f"  World pages:  +{world_count}")
    print(f"  Rune pages:   +{rune_count}")
    print(f"  Event pages:  +{event_count}")
    print(f"  Total new:    {total}")
    
    # Final counts
    total_family = len(list(FAMILY_DIR.glob('*.html')))
    total_world = len(list(WORLD_DIR.glob('*.html')))
    total_runes = len(list(RUNES_DIR.glob('*.html')))
    total_events = len(list(EVENTS_DIR.glob('*.html')))
    
    print(f"\n📁 Final counts:")
    print(f"  family/*.html:  {total_family}")
    print(f"  world/*.html:   {total_world}")
    print(f"  runes/*.html:   {total_runes}")
    print(f"  events/*.html:  {total_events}")
    print(f"  Root HTML:      {len(list(SCANDIC_DIR.glob('*.html')))}")

if __name__ == '__main__':
    main()
