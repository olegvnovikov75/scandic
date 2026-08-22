#!/usr/bin/env python3
"""Fix all broken links in the Scandic project.

Issues:
- Links like family-odin.html should be family/family-odin.html
- Links like world-asgard.html should be world/world-asgard.html
- Same fix needed from within family/ and world/ subdirectories
"""
import os
import re
from pathlib import Path

SCANDIC_DIR = Path('/home/user/scandic')

def count_and_fix(filepath):
    """Count and fix broken links in a file. Returns count of changes."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    count = 0
    
    # Fix family-*.html links
    # Pattern: href="family-<name>.html" -> href="family/family-<name>.html"
    def fix_family_links(text):
        nonlocal count
        # Match href="family-<something>.html" but NOT href="family/family-<something>.html"
        pattern = r'href="(family-[a-z0-9_-]+\.html)"'
        matches = re.findall(pattern, text)
        for match in matches:
            if '/family/' not in match:
                count += 1
        return re.sub(
            r'href="(family-[a-z0-9_-]+\.html)"',
            r'href="family/\1"',
            text
        )
    
    # Fix world-*.html links  
    def fix_world_links(text):
        nonlocal count
        pattern = r'href="(world-[a-z0-9_-]+\.html)"'
        matches = re.findall(pattern, text)
        for match in matches:
            if '/world/' not in match:
                count += 1
        return re.sub(
            r'href="(world-[a-z0-9_-]+\.html)"',
            r'href="world/\1"',
            text
        )
    
    content = fix_family_links(content)
    content = fix_world_links(content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return count

def main():
    total_changes = 0
    
    # Process all HTML files
    for html_file in SCANDIC_DIR.rglob('*.html'):
        changes = count_and_fix(html_file)
        if changes > 0:
            print(f"  {html_file.relative_to(SCANDIC_DIR)}: {changes} fixes")
            total_changes += changes
    
    print(f"\n✅ Total fixes: {total_changes}")
    
    # Verify no broken links remain
    remaining = 0
    for html_file in SCANDIC_DIR.rglob('*.html'):
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for flat family links
        flat_family = re.findall(r'href="(family-[a-z0-9_-]+\.html)"', content)
        for link in flat_family:
            if '/family/' not in link:
                remaining += 1
                print(f"  REMAINING: {html_file.relative_to(SCANDIC_DIR)} → {link}")
        
        # Check for flat world links
        flat_world = re.findall(r'href="(world-[a-z0-9_-]+\.html)"', content)
        for link in flat_world:
            if '/world/' not in link:
                remaining += 1
                print(f"  REMAINING: {html_file.relative_to(SCANDIC_DIR)} → {link}")
    
    if remaining == 0:
        print("✅ All family/world links are now correct!")
    else:
        print(f"⚠️ Still {remaining} broken links remaining")

if __name__ == '__main__':
    main()
