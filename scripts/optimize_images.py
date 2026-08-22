#!/usr/bin/env python3
"""
optimize_images.py — Scandic: PNG → WebP (Pillow, quality=80) + lazy loading.

Подкоманды (атомарные шаги, порядок: convert → patch-links → lazy → delete-referenced):

  convert             Конвертирует все images/*.png → images/*.webp (q80, альфа сохраняется).
                      Сравнивает размеры, определяет сирот (PNG без ссылок), пишет JSON-отчёт.
                      Файлы НЕ удаляет, ссылки НЕ трогает.
  patch-links         Заменяет .png → .webp в *.html (src=, data-src=) и *.css (url(...))
                      ТОЛЬКО для файлов, где webp <= png.
  lazy                Добавляет loading="lazy" + decoding="async" ко ВСЕМ <img>
                      (без дублей: если атрибут уже есть — не трогаем).
  delete-referenced   Убирает из images/ только ЗАРЕФЕРЕНСИРОВАННЫЕ PNG, где webp <= png.
                      Файлы не rm'ятся: переносятся в ~/.local/share/Trash/files/
                      (+ оригиналы в git-истории и /tmp-тарболе). Сироты НЕ трогаем.

Отчёт: scripts/optimize_report.json (+ человекочитаемый вывод).
"""

import json
import re
import shutil
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / 'images'
REPORT = Path(__file__).resolve().parent / 'optimize_report.json'
TRASH = Path.home() / '.local' / 'share' / 'Trash' / 'files'
QUALITY = 80

TEXT_EXTS = {'.html', '.css', '.js', '.xml', '.md', '.txt'}


def iter_text_files():
    for p in ROOT.rglob('*'):
        if p.is_file() and p.suffix in TEXT_EXTS and '.git' not in p.parts:
            yield p


def load_report() -> dict:
    if REPORT.exists():
        return json.loads(REPORT.read_text(encoding='utf-8'))
    return {}


def save_report(rep: dict):
    REPORT.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding='utf-8')


def png_files():
    return sorted(IMAGES.glob('*.png'))


def referenced_png_names() -> set:
    """Имена PNG-файлов, на которые есть ссылка в любом текстовом файле проекта."""
    names = set()
    for tf in iter_text_files():
        try:
            text = tf.read_text(encoding='utf-8', errors='ignore')
        except OSError:
            continue
        for m in re.finditer(r'[\w\-.%А-Яа-яЁё\U00010000-\U0010ffff]*\.png', text, re.IGNORECASE):
            names.add(m.group(0).rsplit('/', 1)[-1])
    return names


def convert_one(png: Path) -> dict:
    """Один PNG → WebP. Возвращает запись: status=ok|broken, размеры."""
    webp = png.with_suffix('.webp')
    rec = {'file': png.name, 'png_bytes': png.stat().st_size}
    try:
        im = Image.open(png)
        im.load()
        # Альфа: RGBA/LA/P+transparency → RGBA (Pillow сохранит прозрачность в WebP)
        if im.mode == 'P' and 'transparency' in im.info:
            im = im.convert('RGBA')
        elif im.mode in ('LA', 'L', '1'):
            im = im.convert('RGBA' if im.mode == 'LA' else 'RGB')
        elif im.mode not in ('RGB', 'RGBA'):
            im = im.convert('RGB')
        im.save(webp, 'WEBP', quality=QUALITY)
        rec['webp_bytes'] = webp.stat().st_size
        rec['status'] = 'ok'
    except Exception as e:  # битый/пустой файл
        rec['status'] = 'broken'
        rec['error'] = str(e)
        if webp.exists():
            webp.unlink()
    return rec


def cmd_convert():
    print('== convert: images/*.png → images/*.webp (quality=%d) ==' % QUALITY)
    refs = referenced_png_names()
    records = []
    for png in png_files():
        rec = convert_one(png)
        if rec['status'] == 'ok':
            rec['webp_smaller_or_equal'] = rec['webp_bytes'] <= rec['png_bytes']
            rec['orphan'] = png.name not in refs
        records.append(rec)
        flag = '' if rec['status'] == 'ok' else '  ⚠️ БИТЫЙ'
        size = f"{rec['png_bytes']} → {rec['webp_bytes']}" if rec['status'] == 'ok' else '-'
        print(f"  {png.name}: {size} {flag}")

    rep = load_report()
    rep['png_count'] = len(records)
    rep['converted'] = [r for r in records if r['status'] == 'ok']
    rep['broken'] = [r for r in records if r['status'] == 'broken']
    rep['kept_png'] = [r['file'] for r in rep['converted'] if not r['webp_smaller_or_equal']]
    rep['orphan_png'] = sorted(r['file'] for r in rep['converted'] if r['orphan'])
    rep['referenced_png'] = sorted(r['file'] for r in rep['converted'] if not r['orphan'])
    save_report(rep)
    print(f"Отчёт: {REPORT}")
    print(f"Ок: {len(rep['converted'])}, битые: {len(rep['broken'])}, "
          f"webp больше png (PNG оставляем): {rep['kept_png']}, "
          f"сирот: {len(rep['orphan_png'])}")


def eligible_webp_names(rep: dict) -> set:
    """Имена (без расширения) PNG, где конвертация ок и webp <= png."""
    return {Path(r['file']).stem for r in rep.get('converted', []) if r['webp_smaller_or_equal']}


def cmd_patch_links():
    print('== patch-links: .png → .webp (только для webp <= png) ==')
    rep = load_report()
    eligible = eligible_webp_names(rep)
    if not eligible:
        print('  нет подходящих файлов — выход')
        return
    # точечные паттерны: только файлы из eligible
    pat = re.compile(
        r'([A-Za-z][\w\-]*\s*=\s*["\'][^"\']*?|url\(\s*[\'"]?)([^/\'"]*/)?'
        r'(' + '|'.join(re.escape(e) for e in sorted(eligible, key=len, reverse=True)) + r')'
        r'\.png', re.IGNORECASE)

    def repl(m):
        return m.group(1) + m.group(2) + m.group(3) + '.webp'

    rep.setdefault('links_replaced', {'html': 0, 'css': 0, 'files': []})
    for tf in iter_text_files():
        if tf.suffix not in ('.html', '.css'):
            continue
        text = tf.read_text(encoding='utf-8')
        new, n = pat.subn(repl, text)
        if n:
            tf.write_text(new, encoding='utf-8')
            kind = 'html' if tf.suffix == '.html' else 'css'
            rep['links_replaced'][kind] += n
            rep['links_replaced']['files'].append(f"{tf.relative_to(ROOT)} ({n})")
            print(f"  {tf.relative_to(ROOT)}: {n} замен")
    save_report(rep)
    print(f"Всего замен: html={rep['links_replaced']['html']}, css={rep['links_replaced']['css']}")


def cmd_lazy():
    print('== lazy: loading="lazy" + decoding="async" ко всем <img> ==')

    def add_attrs(m):
        tag = m.group(0)
        if 'loading=' not in tag:
            tag = re.sub(r'<img\b', '<img loading="lazy"', tag, count=1)
        if 'decoding=' not in tag:
            tag = re.sub(r'<img\b', '<img decoding="async"', tag, count=1)
        return tag

    total = lazy = 0
    files = []
    for tf in iter_text_files():
        if tf.suffix != '.html':
            continue
        text = tf.read_text(encoding='utf-8')
        if '<img' not in text:
            continue
        new = re.sub(r'<img\b[^>]*>', add_attrs, text)
        if new != text:
            tf.write_text(new, encoding='utf-8')
            files.append(str(tf.relative_to(ROOT)))
        t = len(re.findall(r'<img\b', new))
        l = len(re.findall(r'<img\b[^>]*\bloading=', new))
        total += t
        lazy += l
    rep = load_report()
    rep['lazy'] = {'img_total': total, 'img_lazy': lazy, 'files_modified': len(files)}
    save_report(rep)
    print(f"<img> всего: {total}, с loading=: {lazy}, изменено файлов: {len(files)}")


def cmd_delete_referenced():
    print('== delete-referenced: только зареференсированные PNG (webp <= png) ==')
    rep = load_report()
    TRASH.mkdir(parents=True, exist_ok=True)
    deleted = []
    for r in rep.get('converted', []):
        if not r['webp_smaller_or_equal'] or r['orphan']:
            continue  # сироты НЕ трогаем (решение контролёра)
        png = IMAGES / r['file']
        if not png.exists():
            continue
        dest = TRASH / png.name
        if dest.exists():
            dest = TRASH / f"{png.name}.t5-{int(__import__('time').time())}"
        shutil.move(str(png), str(dest))
        deleted.append(r['file'])
        print(f"  {r['file']} → trash ({dest})")
    rep['deleted_png'] = deleted
    save_report(rep)
    print(f"Удалено (в trash): {len(deleted)}")


if __name__ == '__main__':
    cmds = {'convert': cmd_convert, 'patch-links': cmd_patch_links,
            'lazy': cmd_lazy, 'delete-referenced': cmd_delete_referenced}
    if len(sys.argv) != 2 or sys.argv[1] not in cmds:
        print(__doc__)
        sys.exit(1)
    cmds[sys.argv[1]]()
