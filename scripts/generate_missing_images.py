#!/usr/bin/env python3
"""
Генератор недостающих SVG изображений для персонажей Scandic.
Создает простые векторные изображения с использованием базовых форм.
"""

import os
from pathlib import Path

scandic_dir = Path('/home/user/.openclaw/workspace/scandic-project/Scandic')
images_dir = scandic_dir / 'images'

def generate_aeir_svg():
    """Айр - богиня воздуха, символ ветра."""
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect fill="#e8f4f8" width="100" height="100"/>
  <path d="M50 10 Q70 30 60 50 T90 70 T20 70 T50 10 Z" fill="#b8d4e8"/>
  <circle cx="50" cy="50" r="15" fill="#fff"/>
</svg>'''

def generate_mimir_svg():
    """Мимир - мудрый великан, символ знания."""
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect fill="#f5e8d8" width="100" height="100"/>
  <circle cx="50" cy="45" r="20" fill="#fff"/>
  <path d="M30 70 Q50 90 70 70 L70 85 Q50 100 30 85 Z" fill="#d4a574"/>
</svg>'''

def generate_skadi_svg():
    """Скади - великанша, богиня гор и зимы."""
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect fill="#e8f4f8" width="100" height="100"/>
  <path d="M20 60 L35 75 L50 55 L65 75 L80 60 Z" fill="#a8d5ba"/>
  <circle cx="50" cy="40" r="12" fill="#fff"/>
</svg>'''

def generate_placeholder_svg(name: str, color: str):
    """Генератор заглушки для любого персонажа."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect fill="{color}" width="100" height="100"/>
  <text x="50" y="60" font-size="40" text-anchor="middle" fill="#fff">{name[0].upper()}</text>
</svg>'''

def main():
    # Персонажи, для которых нужны новые изображения
    missing = {
        'aeir': generate_aeir_svg(),
        'mimir': generate_mimir_svg(),
        'skadi': generate_skadi_svg(),
    }
    
    for name, svg_content in missing.items():
        filepath = images_dir / f'{name}.svg'
        with open(filepath, 'w') as f:
            f.write(svg_content)
        print(f"✅ Создан: {filepath}")

if __name__ == '__main__':
    main()