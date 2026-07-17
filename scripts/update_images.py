#!/usr/bin/env python3
"""
Скрипт для обновления изображений в файлах персонажей Scandic.
Заменяет placeholder-эмодзи на реальные SVG изображения.
"""

import os
import re
from pathlib import Path

# Мappings: эмодзи -> (имя файла, alt текст)
EMOJI_TO_IMAGE = {
    '👁️': ('odin.svg', 'Odin'),
    '🔨': ('thor.svg', 'Thor'),
    '⚔️': ('loki.svg', 'Loki'),
    '✨': ('baldr.svg', 'Baldr'),
    '🌑': ('hod.svg', 'Hod'),
    '🏹': ('vali.svg', 'Vali'),
    '🤐': ('vidar.svg', 'Vidar'),
    '🏃': ('hermod.svg', 'Hermod'),
    '🎭': ('bragi.svg', 'Bragi'),
    '⚖️': ('tyr.svg', 'Tyr'),
    '🏹': ('ull.svg', 'Ull'),
    '💪': ('magni.svg', 'Magni'),
    '🌊': ('ran.svg', 'Ran'),
    '🧊': ('skadi.svg', 'Skadi'),
    '🐉': ('jormungandr.svg', 'Jormungandr'),
    '🐺': ('fenrir.svg', 'Fenrir'),
    '💀': ('hel.svg', 'Hel'),
    '👨': ('buri.svg', 'Buri'),
    '🌾': ('audumbla.svg', 'Audumbla'),
    '🧬': ('ymir.svg', 'Ymir'),
    '👥': ('mimir.svg', 'Mimir'),
    '🏰': ('odin-frigg.svg', 'Odin-Frigg'),
    '🌍': ('odin-jord.svg', 'Odin-Jord'),
    '🌊': ('odin-ran.svg', 'Odin-Ran'),
    '⚔️': ('odin-rindr.svg', 'Odin-Rindr'),
    '👑': ('frigg.svg', 'Frigg'),
    '🏹': ('freyr.svg', 'Freyr'),
    '🌾': ('freyja.svg', 'Freyja'),
}

def find_and_replace_emoji(text: str, emoji: str, image_path: str, alt_text: str) -> str:
    """Заменить эмодзи на тег <img>."""
    # Ищем эмодзи и заменяем на img tag
    pattern = re.compile(re.escape(emoji))
    
    def replace_func(match):
        return f'<img src="{image_path}" alt="{alt_text}" style="width:100%;height:100%;object-fit:cover;border-radius:8px">'
    
    return pattern.sub(replace_func, text)

def process_file(filepath: str) -> bool:
    """Обработать один файл."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes_made = False
    
    # Проходим по всем эмодзи и заменяем
    for emoji, (image_name, alt_text) in EMOJI_TO_IMAGE.items():
        if emoji in content:
            content = find_and_replace_emoji(content, emoji, image_name, alt_text)
            changes_made = True
    
    if changes_made:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Обновлен: {filepath}")
        return True
    else:
        print(f"ℹ️  Нет изменений: {filepath}")
        return False

def main():
    scandic_dir = Path('/home/user/.openclaw/workspace/scandic-project/Scandic')
    
    # Найти все family-*.html файлы
    family_files = list(scandic_dir.glob('family-*.html'))
    
    print(f"📂 Найдено {len(family_files)} файлов персонажей\n")
    
    changed = 0
    for filepath in family_files:
        if process_file(str(filepath)):
            changed += 1
    
    print(f"\n{'='*50}")
    print(f"✅ Обновлено {changed} из {len(family_files)} файлов")

if __name__ == '__main__':
    main()