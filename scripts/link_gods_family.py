#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""link_gods_family.py — блок «Семья и связи» на новых страницах gods/*.html:
прямые ссылки на страницу сущности в Энциклопедии и страницы рода (family-*.html).
Идемпотентен: маркер <!-- GODS-FAMILY -->."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = "<!-- GODS-FAMILY -->"

MAP = {
  "odin":     ("Энциклопедия: Óðinn", None,
               [("Род Одина", "family-odin.html"),
                ("Род Одина и Фригг", "family-odin-frigg.html"),
                ("Один и Грёд", "family-odin-grid.html"),
                ("Один и Ёрд", "family-odin-jord.html"),
                ("Один и Рана", "family-odin-ran.html"),
                ("Один и Ринд", "family-odin-rindr.html")]),
  "thor":     ("Тор", "þórr.html", [("Род Тора", "family-thor.html"), ("Сив — жена", "family-sif.html")]),
  "freya":    ("Фрейя", "freyja_1.html", [("Род Фрейи", "family-freyja.html"), ("Одр — муж", "family-odr.html")]),
  "loki":     ("Локи", "lóki.html", [("Род Локи", "family-loki.html"), ("Сигюн — жена", "family-sigyn.html"),
               ("Фенрир, сын", "family-fenrir.html"), ("Хель, дочь", "family-hel.html")]),
  "tyr":      ("Тюр", "týr.html", [("Род Тюра", "family-tyr.html")]),
  "heimdall": ("Хеймдалль", "heimdallr.html", [("Род Хеймдалля", "family-heimdall.html")]),
  "balder":   ("Бальдр", "baldr_1.html", [("Род Бальдра", "family-baldr.html"), ("Нанна — жена", "family-nanna.html")]),
  "njord":    ("Ньёрд", "njörðr.html", [("Род Ньёрда", "family-njord.html"), ("Скади — жена", "family-skadi.html")]),
}

def block(name, entity, clans):
    items = []
    if entity:
        items.append(f'<li><a href="../family/{entity}">{name} — справка в Энциклопедии</a></li>')
    for label, fn in clans:
        items.append(f'<li><a href="../family/{fn}">{label}</a></li>')
    return ('  <section class="section">\n    ' + MARK + '\n    <div class="prose">\n'
            '      <h2>Семья и связи</h2>\n      <ul>\n        ' + "\n        ".join(items) +
            '\n      </ul>\n    </div>\n  </section>\n')

def main():
    n = 0
    for gid, (name, entity, clans) in MAP.items():
        p = os.path.join(ROOT, "gods", gid + ".html")
        s = open(p, encoding="utf-8").read()
        if MARK in s:
            continue
        ins = block(name, entity, clans)
        m = re.search(r'(\n\s*<div class="ornament">)', s)
        if m:
            s = s[:m.start(1)] + "\n" + ins + s[m.start(1):]
        else:
            s = s.replace("</main>", ins + "</main>", 1)
        open(p, "w", encoding="utf-8").write(s)
        n += 1
    print("обновлено страниц богов:", n)

if __name__ == "__main__":
    main()
