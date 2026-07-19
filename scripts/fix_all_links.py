#!/usr/bin/env python3
"""
Массовое исправление всех битых ссылок в Scandic.
- contacts.html → contact.html
- family/family-ymir.html → family/ymir.html
"""
import os
import re
import glob

BASE = '/home/user/scandic'

def fix_file(filepath):
    """Fix all known broken links in a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Fix 1: contacts.html → contact.html
    content = re.sub(r'href="contacts\.html"', 'href="contact.html"', content)
    
    # Fix 2: family/family-ymir.html → family/ymir.html  
    content = re.sub(r'href="family/family-ymir\.html"', 'href="family/ymir.html"', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Find all HTML files
all_files = glob.glob(os.path.join(BASE, '*.html'))
all_files += glob.glob(os.path.join(BASE, 'family', '*.html'))
all_files += glob.glob(os.path.join(BASE, 'world', '*.html'))
all_files += glob.glob(os.path.join(BASE, 'events', '*.html'))
all_files += glob.glob(os.path.join(BASE, 'runes', '*.html'))

fixed_count = 0
for fpath in all_files:
    if fix_file(fpath):
        fixed_count += 1
        print(f'✓ {os.path.relpath(fpath, BASE)}')

print(f'\nИсправлено файлов: {fixed_count}')
