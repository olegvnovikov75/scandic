# CONTENT-INVENTORY — Скандик (этап 0, Чип, 20.10.2026)

## Учёт HTML (249 стр., сироты = нет входящих ссылок)
| папка | стр. | КБ | сирот | шаблон |
|-------|-----:|---:|------:|--------|
| корень (новые, 08.10) | 15 | 236 | 1* | style.css (nav/main/section/prose) |
| family/ | 147 | 875 | 130 | style-new.css: container>header+character-page |
| gods/ (новые, 08.10) | 8 | 75 | 0 | style.css, связаны из gods.html |
| runes/ | 35 | 209 | 35 | style-new.css: section.section, руна-блоки |
| events/ | 24 | 90 | 24 | style-new.css: event-page (Место/Описание) |
| world/ | 20 | 92 | 20 | style-new.css: тот же character-page, что family |
| ИТОГО | 249 | | 210 | |

\* сирота в корне — 404.html (нормально).

## Качество
- mojibake: 0; заглушек (<200 симв.): 0 — контент полный
- family/world/events: name + native + описание + поля (Происхождение/Роль) + Семья/Легенды/Источники; у части — «Связанные сущности» (реальные ссылки)
- runes: глиф, название, значения, описание, ключевые слова, фукх
- images/: 153 SVG + webp; есть дубли (ægir.svg + aegir.svg) — ссылки починены в августе, не трогать

## Дизайн-системы
- НОВАЯ (эталон): css/style.css (525 стр.) — классы nav, main, hero, page-head, section, prose, stat, note, grid/card, rune-grid/rune-box, timeline, ornament, footer; пример: gods/odin.html
- СТАРАЯ: css/style-new.css (1824 стр.) — только на сиротах; после обёртки станет мёртвой

## План обёртки (Р1=а, Р2=все ~210)
- Обёртка IN PLACE (пути/имена файлов не меняем → все inter-links валидны; диакритика в именах остаётся, проверять линк-чеком)
- family+world → сущность: page-head + image + prose + stats + списки + related-cards
- events → page-head + prose + note
- runes → rune-box-hero + prose + chips + note
- CSS: дополнить style.css блоками для списков/картинок/chips (аддитивно)
- Каталоги: entities.html (все 147 family по типу) + секции в realms.html (20 world), timeline.html (24 events), runes.html (35 runes grid), creatures.html → grid + ссылка на entities.html
- В nav добавить «Энциклопедия» (entities.html)
- sitemap.xml — перегенерить под реальные 249+ URL
