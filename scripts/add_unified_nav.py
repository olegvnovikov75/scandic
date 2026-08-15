#!/usr/bin/env python3
"""
Добавляет унифицированную навигацию во все HTML страницы Scandic.
"""

from pathlib import Path

scandic_dir = Path('/home/user/Projects/scandic')

UNIFIED_NAV = '''
<!-- ===== НАВИГАЦИЯ ===== -->
<nav class="navbar" id="navbar">
    <div class="nav-container">
        <a href="index.html" class="nav-logo">
            <span class="nav-rune">ᚱ</span>
            <span class="nav-name">Scandic</span>
        </a>
        <ul class="nav-menu" id="navMenu">
            <li><a href="index.html#worlds" class="nav-link"><span class="rune">☽</span> Миры</a></li>
            <li><a href="index.html#pantheons" class="nav-link"><span class="rune">⚡</span> Боги</a></li>
            <li><a href="index.html#runes" class="nav-link"><span class="rune">ᚠ</span> Руны</a></li>
            <li><a href="index.html#sagas" class="nav-link"><span class="rune">📜</span> Саги</a></li>
            <li><a href="literature.html" class="nav-link"><span class="rune">📖</span> Литература</a></li>
            <li><a href="about.html" class="nav-link"><span class="rune">ℹ</span> О проекте</a></li>
        </ul>
        <button class="nav-toggle" id="navToggle" aria-label="Меню">
            <span></span><span></span><span></span>
        </button>
    </div>
</nav>

<!-- ===== СЕВЕРНОЕ СИЯНИЕ ===== -->
<div class="aurora-container">
    <div class="aurora-layer"></div>
    <div class="aurora-layer"></div>
    <div class="aurora-layer"></div>
</div>
'''

UNIFIED_FOOTER = '''
<!-- ===== FOOTER ===== -->
<footer class="footer">
    <div class="footer-content">
        <div class="footer-rune">ᚱ</div>
        <div class="footer-name">SCANDIC</div>
        <p>Скандинавская мифология — миры, боги, руны и легенды</p>
        <div style="margin: 1.5em 0;">
            <a href="about.html" style="color: var(--gold-auric); text-decoration: none; margin: 0 12px;">О проекте</a>
            <a href="contact.html" style="color: var(--gold-auric); text-decoration: none; margin: 0 12px;">Контакты</a>
            <a href="literature.html" style="color: var(--gold-auric); text-decoration: none; margin: 0 12px;">Литература</a>
        </div>
        <p class="footer-copy">© 2026 Scandic. Создано с любовью к северным мифам.</p>
    </div>
</footer>
'''

UNIFIED_SCRIPT = '''
<script>
// Навигация (мобильная)
document.getElementById('navToggle').addEventListener('click', function() {
    document.getElementById('navMenu').classList.toggle('active');
});

// Навбар при скролле
window.addEventListener('scroll', function() {
    const navbar = document.getElementById('navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Плавный скролл
document.querySelectorAll('.nav-link[href^="#"]').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
        document.getElementById('navMenu').classList.remove('active');
    });
});

// Анимация появления
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.section, .card, .item').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});
</script>
'''

updated = 0
for html_file in scandic_dir.glob('**/*.html'):
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Пропускаем если уже есть nav
    if '<nav' in content or 'navbar' in content:
        continue
    
    # Добавляем nav после </head>
    if '</head>' in content:
        content = content.replace('</head>', UNIFIED_NAV + '\n</head>')
        updated += 1
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"✅ Навбара добавлено на {updated} страниц")
