#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""restore_sd_images.py — вернуть реальные SD-иллюстрации (id001–id039) из git-истории.
Удалены коммитом cf8f1e6 (T5 «сироты»); оригинальные PNG живы в cf8f1e6^.
Конвертируем в webp (q82) и ставим на hero family-страниц по совпадению имени (CSV).
"""
import os, re, csv, subprocess, io, glob
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = 'cf8f1e6^'

def git(args):
    return subprocess.run(['git','-C',ROOT]+args, capture_output=True, check=True).stdout

def main():
    # 1) список PNG в истории
    tree = git(['-c','core.quotepath=off','ls-tree','-r','--name-only',REF,'images/']).decode('utf-8')
    pngs = [p for p in tree.splitlines() if re.search(r'/id(\d{3})-.*\.png$', p) and '/' in p]
    by_id = {}
    for p in pngs:
        i = int(re.search(r'/id(\d{3})-', p).group(1))
        # кириллический вариант предпочтительнее латинского дубля
        if i not in by_id or not re.search(r'[а-яА-Я]', by_id[i]):
            by_id[i] = p
    # 2) имя берём из ИМЕНИ ФАЙЛА PNG (CSV рассинхронизирован с нумерацией — проверка 20.10)
    fname_id = {}   # cyrillic_name_lower -> id
    for i, p in by_id.items():
        m = re.search(r'/id\d{3}-(.+)\.png$', p)
        if m and re.search(r'[а-я]', m.group(1)):
            nm = m.group(1).replace('ё','е').lower()
            fname_id[nm] = i
    ALIAS = {'хюрмунганд':'йормунганд', 'ньерт':'нёрт'}
    for a,b in ALIAS.items(): fname_id.setdefault(a, None)
    import difflib
    h1s = {}
    for page in glob.glob(os.path.join(ROOT,'family','*.html')):
        mm = re.search(r'<h1>([^<]+)</h1>', open(page, encoding='utf-8').read())
        if mm: h1s[mm.group(1).strip()] = page
    # 3) извлечь и сконвертировать
    restored = {}
    for i, path in sorted(by_id.items()):
        out = os.path.join(ROOT, 'images', f'id{i:03d}.webp')
        blob = git(['show', f'{REF}:{path}'])
        try:
            im = Image.open(io.BytesIO(blob)).convert('RGB')
        except Exception as e:
            print(f'  ! id{i:03d}: не читается ({e})'); continue
        if im.width > 640:
            im = im.resize((640, int(im.height*640/im.width)), Image.LANCZOS)
        im.save(out, 'WEBP', quality=82)
        restored[i] = os.path.basename(out)
    print(f'SD-картинок восстановлено: {len(restored)}')
    # 4) проставить на family-страницы: имя файла → h1 (точно, потом fuzzy 0.82)
    name2img = {nm: f'id{i:03d}.webp' for nm, i in restored_mapped(restored, fname_id).items()}
    used_pages = {}
    for nm, page in h1s.items():
        key = nm.replace('ё','е').lower()
        fn = name2img.get(key)
        if not fn and name2img:
            hit = difflib.get_close_matches(key, list(name2img.keys()), n=1, cutoff=0.82)
            if hit: fn = name2img[hit[0]]
        if fn: used_pages.setdefault(page, fn)
    n = 0
    for page, fn in used_pages.items():
        s = open(page, encoding='utf-8').read()
        if not re.search(r'<h1>([^<]+)</h1>', s): continue
        if 'entity-hero__img' in s:
            s2 = re.sub(r'(<img class="entity-hero__img" src=")[^"]+(")', rf'\g<1>../images/{fn}\g<2>', s, count=1)
        else:
            s2 = s.replace('<h1>', f'<img class="entity-hero__img" src="../images/{fn}" alt="" loading="lazy" decoding="async">\n    <h1>', 1)
        if s2 != s:
            open(page,'w',encoding='utf-8').write(s2); n += 1
    print(f'страниц с реальной картинкой: {n}')

def restored_mapped(restored, fname_id):
    out = {}
    for nm, i in fname_id.items():
        if i is not None and i in restored:
            out[nm] = i
    return out

if __name__ == '__main__':
    main()
