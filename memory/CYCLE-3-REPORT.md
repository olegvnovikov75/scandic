# Scandic — Цикл 3: Персональные SVG-иконки

**Дата:** 28.08.2026
**Статус:** ✅ ЗАКРЫТ
**Коммит:** f6308bf

## ✅ Что сделано

1. **Генератор SVG** — `scripts/generate_avatars.py` (руны + цвета, детерминированная генерация)
2. **86 персональных SVG** — созданы в images/ (67 → 153)
3. **86 HTML-файлов** — обновлены (avatar-default.svg → <name>.svg)
4. **0 ссылок на avatar-default.svg** — все персонажи с персональными иконками

## 📊 Метрики

| Показатель | Было | Стало |
|------------|------|-------|
| SVG-иконок | 67 | 153 (+86) |
| Персонажей без иконок | 86 | 0 |
| HTML-файлов обновлено | — | 86 |
| Ссылок на avatar-default.svg | 86 | 0 |

## 🎨 Дизайн SVG

- **Формат:** 64×64, viewBox="0 0 64 64"
- **Фон:** тёмный круг (#1a1a2e)
- **Кольцо:** цвет персонажа (8 цветов: земля, море, кровь, лес, ночь, золото, небо, магия)
- **Руна:** 24 рунных символа (Unicode), выбирается по hash имени
- **Декор:** 4 точки по углам (цвет персонажа)

**Пример:**
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <circle cx="32" cy="32" r="30" fill="#1a1a2e"/>
  <circle cx="32" cy="32" r="28" fill="none" stroke="#8B4513" stroke-width="2"/>
  <text x="32" y="38" font-family="serif" font-size="24" fill="#8B4513" text-anchor="middle">ᚠ</text>
  <circle cx="10" cy="10" r="2" fill="#8B4513"/>
  <circle cx="54" cy="10" r="2" fill="#8B4513"/>
  <circle cx="10" cy="54" r="2" fill="#8B4513"/>
  <circle cx="54" cy="54" r="2" fill="#8B4513"/>
</svg>
```

## 🔄 Обновление HTML

Скрипт (inline Python):
```python
for html_file in family_dir.glob("*.html"):
    char_name = html_file.stem
    content.replace('src="../images/avatar-default.svg"', f'src="../images/{char_name}.svg"')
```

## ✅ Критерии приёмки

- [x] 86 новых SVG в images/
- [x] 0 ссылок на avatar-default.svg (все персональные)
- [x] Git: 1 коммит (f6308bf, 172 файла)
- [ ] Визуальный тест (5–10 страниц) — **ожидает Шефа**

## ⏳ Осталось / для Шефа

- **Визуальный тест:** открыть 5–10 страниц (family/*.html), проверить рендер SVG
- **Push в GitHub:** `git push origin main` (коммит f6308bf)
- **Поиск по сайту** — опционально, отдельный цикл (проблема #12)
- **Удаление css/style.css** (legacy) — можно, если style-new.css везде

---

*Отчёт: Гаечка 🧩 · 28.08.2026*
