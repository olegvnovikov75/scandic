# 📋 Инструкция по запуску проекта Scandic

## Локальный сервер для просмотра

### Вариант 1: Python HTTP Server (рекомендуется)

```bash
cd /home/user/.openclaw/workspace/scandic-project/Scandic
python3 -m http.server 8000
```

Затем откройте в браузере: **http://localhost:8000**

---

### Вариант 2: Node.js Static Server

```bash
cd /home/user/.openclaw/workspace/scandic-project/Scandic
npx serve . -p 3000
```

Затем откройте в браузере: **http://localhost:3000**

---

### Вариант 3: Через OpenClaw (если настроен)

Используйте встроенный веб-сервер OpenClaw для просмотра файлов из workspace.

---

## 📂 Что доступно для просмотра

| Путь | Описание |
|------|----------|
| `index.html` | Главная страница с навигацией по мирам |
| `styles.css` | ОПТИМИЗИРОВАННЫЙ CSS |
| `images/*.svg` | 49 SVG изображений (полный набор) |
| `family-*.html` | 46 персонажей с обновленными изображениями |

---

## ⚠️ Примечание

Поскольку проект находится в локальном workspace, для просмотра нужен локальный веб-сервер. Если у вас уже запущен OpenClaw сервер, файлы доступны по пути:

```
http://<host>:<port>/home/user/.openclaw/workspace/scandic-project/Scandic/
```

---

**Хотите, чтобы я запустил локальный сервер для вас?**