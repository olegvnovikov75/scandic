#!/usr/bin/env python3
"""Generate missing family-*.html pages from entities CSV.

Only generates pages for actual characters (gods, giants, beings).
Skips worlds, runes, events, locations, and structural entities.
"""
import csv
import os
from pathlib import Path

SCANDIC_DIR = Path('/home/user/scandic')
FAMILY_DIR = SCANDIC_DIR / 'family'
CSV_PATH = SCANDIC_DIR / 'data' / 'entities-table.csv'

# Existing family pages (filenames without .html)
EXISTING_FAMILY = {
    'aeir', 'angrboda', 'audumbla', 'baldr', 'borr', 'bragi', 'buri',
    'fenrir', 'forseti', 'freyja', 'freyr', 'frigg', 'gerdr',
    'heimdall', 'hel', 'hermod', 'hod', 'idunn', 'jord',
    'jormungandr', 'loki', 'magni', 'mimir', 'modi', 'nanna',
    'njord', 'odin', 'odin-frigg', 'odin-grid', 'odin-jord',
    'odin-ran', 'odin-rindr', 'odr', 'ran', 'sif', 'sigyn',
    'skadi', 'thor', 'thruth', 'tyr', 'ull', 'vali', 've', 'vidar', 'vili', 'yimir'
}

def csv_to_slug(norse_name):
    """Convert norse_name to a filename-safe slug."""
    slug = norse_name.lower()
    # Remove special chars, keep alnum and -_
    slug = ''.join(c if c.isalnum() or c in '_-' else '-' for c in slug)
    # Collapse multiple dashes
    while '--' in slug:
        slug = slug.replace('--', '-')
    slug = slug.strip('-')
    return slug

def get_unique_slug(norse_name):
    """Get a unique filename for this entity."""
    slug = csv_to_slug(norse_name)
    base = slug
    counter = 1
    while slug in EXISTING_FAMILY or Path(FAMILY_DIR / f'{slug}.html').exists():
        slug = f'{base}_{counter}'
        counter += 1
    return slug

def is_family_character(entity):
    """Determine if this entity is a family character (not a world/rune/event/location)."""
    norse = entity['norse_name'].lower()
    origin = entity['origin'].lower()
    role = entity['role'].lower()
    
    # Skip keywords for non-family entities
    skip_keywords = [
        # Worlds (9 realms)
        'мир', 'обитель', 'зельфхейм', 'альфхейм', 'свартальфхейм',
        # Runes (elder futhark)
        'руна', 'феху', 'урюз', 'турисаз', 'ансуз', 'райдо',
        'кеназ', 'гебо', 'вунхо', 'хаглаз', 'иса', 'йера',
        'эйваз', 'перт', 'альгиз', 'соуло', 'тейваз', 'берканан',
        'меназ', 'ингвиз', 'дагаз', 'матхузанг', 'лаутиз', 'кауназ',
        'наудиз',
        # Events/myths
        'война', 'битва', 'свадьба', 'пиры', 'утление',
        'обмен', 'конечная битва', 'повесился', 'выколол',
        'похитил', 'рыбачит', 'переодет', 'увязание',
        'прикован', 'практикует', 'создали', 'создают',
        'выбор', 'оскорбляет', 'траур',
        # World structures
        'мировое дерево', 'радужный мост', 'зал павших',
        'поле', 'трон', 'источник судьбы', 'источник мудрости',
        'пропасть', 'первозданная пустота', 'источник в',
        'глаз', 'река у ворот',
        # Non-characters
        'эпитет', 'альтернативное имя', 'из червей',
        'самый мудрый', 'пророчица', 'нёрна',
        'связь миров', 'защитная сила', 'изобилие',
        'жизненная сила', 'героизм', 'плодородие',
        'трансформация', 'семейная связь', 'испытание',
        'ожог', 'нужда', 'выживание',
        # World IDs (102-110) are explicitly worlds
    ]
    
    for kw in skip_keywords:
        if kw in norse or kw in origin or kw in role:
            return False
    
    return True

def generate_html(row):
    """Generate HTML for a single entity."""
    csv_id = row['ID']
    russian = row['russian_name']
    norse = row['norse_name']
    german = row['german_name']
    origin = row['origin']
    role = row['role']
    
    slug = get_unique_slug(norse)
    
    # Build links to related family pages
    related_links = []
    # Check common relationships
    rel_pairs = [
        ('odin', 'Óðinn'), ('thor', 'Þórr'), ('freyja', 'Freyja'),
        ('freyr', 'Freyr'), ('loki', 'Loki'), ('hel', 'Hel'),
        ('fenrir', 'Fenrir'), ('jormungandr', 'Jörmungandr'),
        ('baldr', 'Baldr'), ('borr', 'Borr'), ('buri', 'Búri'),
        ('mimir', 'Mímir'), ('heimdall', 'Heimdall'),
        ('skadi', 'Skadi'), ('jord', 'Jörð'), ('frigg', 'Frigg'),
        ('sif', 'Sif'), ('bragi', 'Bragi'), ('tyr', 'Týr'),
        ('vidar', 'Víðarr'), ('vali', 'Váli'), ('magni', 'Magni'),
        ('modi', 'Móði'), ('thruth', 'Þrúðr'), ('ull', 'Ullr'),
        ('hermod', 'Hermóðr'), ('forseti', 'Forseti'),
        ('angrboda', 'Angrboða'), ('yimir', 'Ymir'),
        ('ran', 'Rán'), ('jord', 'Jörð'), ('njord', 'Njörðr'),
        ('idunn', 'Idunn'), ('sif', 'Sif'), ('od', 'Óðr'),
    ]
    
    russian_lower = russian.lower()
    norse_lower = norse.lower()
    
    for key, name in rel_pairs:
        if key in norse_lower or key in russian_lower:
            related_links.append((f'family-{key}.html', name))
    
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
    
    for link_path, link_name in related_links:
        html += f'''                    <a href="../{link_path}" class="link-card">{link_name}</a>
'''
    
    if not related_links:
        html += '''                    <p class="no-links">Нет связанных сущностей</p>
'''
    
    html += f'''                </div>
            </div>
        </div>

        <footer>
            <p>© 2024 Скандинавская Мифология</p>
            <p><a href="../index.html">← На главную</a> | <a href="../about.html">О проекте</a></p>
        </footer>
    </div>
</body>
</html>
'''
    return slug, html

def main():
    # Read CSV
    entities = []
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            entities.append(row)
    
    print(f"📖 Loaded {len(entities)} entities from CSV")
    
    # Deduplicate by norse_name (keep first occurrence)
    seen = set()
    unique_entities = []
    for e in entities:
        n = e['norse_name'].strip()
        if n not in seen:
            seen.add(n)
            unique_entities.append(e)
    
    print(f"📖 Unique entities: {len(unique_entities)}")
    
    # Check existing family pages
    existing_files = set()
    if FAMILY_DIR.exists():
        for f in FAMILY_DIR.glob('*.html'):
            existing_files.add(f.stem)
    
    print(f"📁 Existing family pages: {len(existing_files)}")
    
    # Find missing family characters
    missing = []
    for entity in unique_entities:
        if not is_family_character(entity):
            continue
        
        norse = entity['norse_name']
        slug = csv_to_slug(norse)
        
        # Check if page exists
        if slug in existing_files:
            continue
        
        # Also check the actual filename
        for existing in existing_files:
            if slug == existing or slug.startswith(existing) or existing.startswith(slug):
                continue
        
        missing.append(entity)
    
    print(f"⚠️ Missing family pages: {len(missing)}")
    
    # Generate pages
    generated = 0
    errors = 0
    for entity in missing:
        try:
            slug, html_content = generate_html(entity)
            filepath = FAMILY_DIR / f'{slug}.html'
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            generated += 1
            
            if generated % 20 == 0:
                print(f"  Generated {generated} pages...")
        except Exception as e:
            errors += 1
            print(f"  ERROR: {entity['norse_name']} — {e}")
    
    print(f"\n✅ Generated {generated} new family pages")
    if errors:
        print(f"⚠️ {errors} errors")
    total = len(existing_files) + generated
    print(f"📁 Total family pages: {total}")

if __name__ == '__main__':
    main()
