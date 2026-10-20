#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_real_images.py — 20.10.2026: заменить медальоны-плейсхолдеры на реальные иллюстрации.
Августовский batch наделал SVG-медальонов с диакритикой в именах (ægir.svg),
а настоящие картинки лежат под транслитерированными именами (aegir.svg).
Если у img-ссылки файл — медальон, и существует неплейсхолдерный «транслит-близнец» — переключаем.
"""
import os, re, glob, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICE = {'æ':'ae','þ':'th','ð':'d','ǫ':'o','ø':'o','á':'a','é':'e','í':'i','ó':'o','ú':'u','ý':'y','ö':'o','å':'a','ü':'u','ń':'n'}

def is_medal(path):
    try: d = open(path,'rb').read()
    except OSError: return False
    return len(d) < 600 and b'<circle' in d and b'<text' in d

def translit(name):
    out = []
    for ch in name:
        if ch in ICE: out.append(ICE[ch]); continue
        nf = unicodedata.normalize('NFKD', ch)
        base = ''.join(c for c in nf if not unicodedata.combining(c))
        out.append(base.lower() if base else ch)
    return ''.join(out)

def main():
    fixable = {}   # medal filename -> real twin filename
    for f in glob.glob(os.path.join(ROOT,'images','*.svg')):
        base = os.path.basename(f)
        if not is_medal(f): continue
        twin = translit(base)
        if twin == base: continue
        tp = os.path.join(ROOT,'images',twin)
        if os.path.exists(tp) and not is_medal(tp):
            fixable[base] = twin
    print(f"медальонов с реальной заменой: {len(fixable)}")
    n = 0
    pat = re.compile(r'src="([^"]*images/([^"]+\.svg))"')
    for page in glob.glob(os.path.join(ROOT,'**','*.html'), recursive=True):
        if '/.git' in page: continue
        s = open(page, encoding='utf-8').read()
        def rep(m):
            nonlocal n
            full, base = m.group(1), m.group(2)
            if base in fixable:
                n += 1
                return 'src="' + full[:-len(base)] + fixable[base] + '"'
            return m.group(0)
        s2 = pat.sub(rep, s)
        if s2 != s:
            open(page,'w',encoding='utf-8').write(s2)
    print(f"заменено img-ссылок: {n}")

if __name__ == '__main__':
    main()
