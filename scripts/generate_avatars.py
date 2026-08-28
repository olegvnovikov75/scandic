#!/usr/bin/env python3
"""
Scandic — Генератор персональных SVG-иконок (Цикл 3)
Создаёт 86 SVG для персонажей без иконок
"""

from pathlib import Path

# Список персонажей без иконок (86)
CHARACTERS = [
    "ægir", "angrboða", "ás", "ask", "auðumbla", "baldr_1", "baldrs-dauði",
    "balðrs-ok-nóttar", "billangr", "bjarkan", "bragi_1", "dagr", "eikþyrnir",
    "eldrýð", "elimir", "embla", "eyr", "fárbautaz", "fenrisulfs-binding",
    "forseti_1", "freyja_1", "freyju-ok-óðrs", "freyr_1", "garmr", "gerðr",
    "gríð", "hagl", "heimdallr", "hermóðs-ferð", "hónir-ok-lóðurr", "hrymgelmir",
    "huginn", "idunn_1", "ís", "jár", "jörð", "kauk", "kenn", "laufey",
    "lóki-ok-angrboðu", "menn", "miðgarðr", "mundilfari", "muninn", "nerþuz",
    "níðhöggr", "njörðr", "norvi", "nótt", "óðinn-ok-friggjar", "óðr", "per",
    "ratatoskr", "rindr", "röskva", "sif_1", "skaði", "skóll", "skölnir",
    "skuld", "sleipnir", "sǫðufarnir", "sól", "surtr", "tríðrún",
    "týrs-berjask-við-fenri", "úr", "valhollar-veizlur_1", "valhollar-veizlur",
    "vanir", "veðrfimnir", "veðrfölnir", "verðandi", "vili-ok-vé_1", "vili-ok-vé",
    "völva", "wun", "ymir", "þjálfi", "þökk", "þórr", "þórr-ok-sifs",
    "þrekkr", "þriazi", "þrymr", "þurs"
]

# Цветовая палитра (скандинавская мифология)
COLORS = [
    "#8B4513",  # brown (земля)
    "#2F4F4F",  # dark slate (море)
    "#8B0000",  # dark red (кровь/железо)
    "#006400",  # dark green (лес)
    "#4B0082",  # indigo (ночь)
    "#8B8B00",  # dark yellow (золото)
    "#00008B",  # dark blue (небо)
    "#8B008B",  # dark magenta (магия)
]

# Рунные символы (Unicode)
RUNES = [
    "ᚠ", "ᚢ", "ᚦ", "ᚨ", "ᚱ", "ᚲ", "ᚷ", "ᚹ",
    "ᚺ", "ᚾ", "ᛁ", "ᛃ", "ᛇ", "ᛈ", "ᛉ", "ᛊ",
    "ᛏ", "ᛒ", "ᛖ", "ᛗ", "ᛚ", "ᛜ", "ᛞ", "ᛟ"
]

def char_to_hash(name: str) -> int:
    """Простой hash для детерминированной генерации"""
    return sum(ord(c) for c in name.lower())

def generate_svg(name: str, output_path: str) -> None:
    """Генерирует персональный SVG для персонажа"""
    
    h = char_to_hash(name)
    color = COLORS[h % len(COLORS)]
    rune = RUNES[h % len(RUNES)]
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <circle cx="32" cy="32" r="30" fill="#1a1a2e"/>
  <circle cx="32" cy="32" r="28" fill="none" stroke="{color}" stroke-width="2"/>
  <text x="32" y="38" font-family="serif" font-size="24" fill="{color}" text-anchor="middle">{rune}</text>
  <circle cx="10" cy="10" r="2" fill="{color}"/>
  <circle cx="54" cy="10" r="2" fill="{color}"/>
  <circle cx="10" cy="54" r="2" fill="{color}"/>
  <circle cx="54" cy="54" r="2" fill="{color}"/>
</svg>'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg)

def main():
    images_dir = Path("images")
    images_dir.mkdir(exist_ok=True)
    
    print(f"Генерация {len(CHARACTERS)} SVG-иконок...")
    
    created = 0
    skipped = 0
    
    for name in CHARACTERS:
        output_path = images_dir / f"{name}.svg"
        
        if output_path.exists():
            skipped += 1
            continue
        
        generate_svg(name, str(output_path))
        created += 1
    
    print(f"\n✅ Готово: {created} создано, {skipped} пропущено (уже существуют)")
    print(f"   Всего: {len(CHARACTERS)} персонажей")

if __name__ == "__main__":
    main()
