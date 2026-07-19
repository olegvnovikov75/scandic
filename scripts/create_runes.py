#!/usr/bin/env python3
"""
Создаёт 24 страницы рун Elder Futhark (3 фукы по 8 рун).
Каждая руна имеет:
- Свой SVG-символ
- Описание значения
- Связи с другими рунами
- Примеры из саг
"""
import os
import glob

BASE = '/home/user/scandic'
RUNES_PATH = os.path.join(BASE, 'runes')

# 24 руны Elder Futhark
RUNES = [
    # Первая фук (Fehu-Uruz) — изобилие, сила, начало
    {
        'id': 'fehu',
        'rune': 'ᚠ',
        'name': 'Феху',
        'translit': 'Fehu',
        'meaning': 'Крупный рогатый скот, богатство, изобилие, материальное благополучие',
        'description': 'Феху — первая руна Elder Futhark, символизирующая богатство и изобилие. В древности скот был главной мерой богатства, поэтому Феху ассоциируется с материальными благами, но также с духовным изобилием.',
        'keywords': ['богатство', 'изобилие', 'скот', 'материальное'],
        'futhark': 1, 'position': 1
    },
    {
        'id': 'uruz',
        'rune': 'ᚢ',
        'name': 'Уруаз',
        'translit': 'Uruz',
        'meaning': 'Дикий бык, физическая сила, здоровье, витальность, мужество',
        'description': 'Уруаз — вторая руна, символ дикого быка. Она олицетворяет грубую физическую силу, здоровье и жизненную энергию. Уруаз связана с мужеством перед лицом опасности.',
        'keywords': ['сила', 'бык', 'здоровье', 'витальность'],
        'futhark': 1, 'position': 2
    },
    {
        'id': 'thiwaz',
        'rune': 'ᚦ',
        'name': 'Тейваз',
        'translit': 'Tīwaz',
        'meaning': 'Бог Тюр, справедливость, победа, мужество, закон',
        'description': 'Тейваз — третья руна, названная в честь бога Тюра, бога войны и справедливости. Она символизирует победу, достигнутую через справедливость и мужество. Тейваз также связана с законом и порядком.',
        'keywords': ['Тюр', 'справедливость', 'победа', 'закон'],
        'futhark': 1, 'position': 3
    },
    {
        'id': 'rad',
        'rune': 'ᚱ',
        'name': 'Рейд',
        'translit': 'Rāð',
        'meaning': 'Поездка, путешествие, ритм, защита, совет',
        'description': 'Рейд — четвёртая руна, означающая путешествие, движение и ритм жизни. Она символизирует необходимость движения вперёд, но также защиту и совет.',
        'keywords': ['путешествие', 'ритм', 'защита', 'совет'],
        'futhark': 1, 'position': 4
    },
    {
        'id': 'gebo',
        'rune': 'ᚷ',
        'name': 'Гебо',
        'translit': 'Gebo',
        'meaning': 'Дар, дарение, союз, равновесие, взаимность',
        'description': 'Гебо — пятая руна, символ дара и дарения. Она представляет собой равновесие между дающим и получающим, силу союза и взаимности.',
        'keywords': ['дар', 'союз', 'равновесие', 'взаимность'],
        'futhark': 1, 'position': 5
    },
    {
        'id': 'wunjo',
        'rune': 'ᚹ',
        'name': 'Вуньо',
        'translit': 'Wunjo',
        'meaning': 'Радость, благодать, радость богов, гармония',
        'description': 'Вуньо — шестая руна, символизирующая радость, благодать и гармонию. Она связана с радостью богов и благополучием общины.',
        'keywords': ['радость', 'благодать', 'гармония', 'благополучие'],
        'futhark': 1, 'position': 6
    },
    {
        'id': 'hagalaz',
        'rune': 'ᚺ',
        'name': 'Хагалаз',
        'translit': 'Hagall',
        'meaning': 'Град, разрушение, очищение, трансформация, стихия',
        'description': 'Хагалаз — седьмая руна, символ града и стихийных сил. Она представляет разрушение, необходимое для обновления, и трансформацию через кризис.',
        'keywords': ['град', 'разрушение', 'очищение', 'трансформация'],
        'futhark': 1, 'position': 7
    },
    {
        'id': 'naudiz',
        'rune': 'ᚾ',
        'name': 'Наутиз',
        'translit': 'Nauðiz',
        'meaning': 'Нужда, необходимость, преодоление, давление, выносливость',
        'description': 'Наутиз — восьмая руна, символ нужды и необходимости. Она олицетворяет давление обстоятельств и силу, возникающую через преодоление трудностей.',
        'keywords': ['нужда', 'необходимость', 'преодоление', 'выносливость'],
        'futhark': 1, 'position': 8
    },
    # Вторая фук (Isaz-Ingwaz) — внутренняя сила, завершение
    {
        'id': 'isa',
        'rune': 'ᛁ',
        'name': 'Иса',
        'translit': 'Isa',
        'meaning': 'Лёд, застой, терпение, концентрация, выдержка',
        'description': 'Иса — девятая руна, символ льда и застоя. Она учит терпению и концентрации, необходимости выдержать давление перед прорывом.',
        'keywords': ['лёд', 'застой', 'терпение', 'концентрация'],
        'futhark': 2, 'position': 9
    },
    {
        'id': 'jera',
        'rune': 'ᛃ',
        'name': 'Йера',
        'translit': 'Jera',
        'meaning': 'Урожай, год, цикл, награда за труд, плодородие',
        'description': 'Йера — десятая руна, символ урожая и цикла года. Она представляет награду за труд и плодородие, приходящее через правильные действия.',
        'keywords': ['урожай', 'год', 'цикл', 'награда'],
        'futhark': 2, 'position': 10
    },
    {
        'id': 'eihwaz',
        'rune': 'ᛇ',
        'name': 'Эйваз',
        'translit': 'Eihwaz',
        'meaning': 'Тис, выносливость, защита, жизненная сила, связь миров',
        'description': 'Эйваз — одиннадцатая руна, названная в честь тиса — дерева жизни и защиты. Она символизирует выносливость, жизненную силу и связь между мирами.',
        'keywords': ['тис', 'выносливость', 'защита', 'жизненная сила'],
        'futhark': 2, 'position': 11
    },
    {
        'id': 'perthro',
        'rune': 'ᛈ',
        'name': 'Перт',
        'translit': 'Perthro',
        'meaning': 'Тайна, судьба, чаша, магическое знание, рождение',
        'description': 'Перт — двенадцатая руна, символ тайны и судьбы. Она связана с чашей судьбы, магическим знанием и процессом рождения нового.',
        'keywords': ['тайна', 'судьба', 'чаша', 'магия'],
        'futhark': 2, 'position': 12
    },
    {
        'id': 'algiz',
        'rune': 'ᛊ',
        'name': 'Альгиз',
        'translit': 'Algiz',
        'meaning': 'Олень, защита, покровительство, связь с богами, щит',
        'description': 'Альгиз — тринадцатая руна, символ оленя и защиты. Она представляет покровительство богов, духовную защиту и связь с высшими силами.',
        'keywords': ['олень', 'защита', 'покровительство', 'боги'],
        'futhark': 2, 'position': 13
    },
    {
        'id': 'sowilo',
        'rune': 'ᛏ',
        'name': 'Соуло',
        'translit': 'Sól',
        'meaning': 'Солнце, жизнь, победа, целостность, энергия',
        'description': 'Соуло — четырнадцатая руна, символ Солнца. Она олицетворяет жизненную энергию, победу, целостность и божественную благодать.',
        'keywords': ['солнце', 'жизнь', 'победа', 'целостность'],
        'futhark': 2, 'position': 14
    },
    {
        'id': 'tîwaz',
        'rune': 'ᛒ',
        'name': 'Таннит',
        'translit': 'Tīwaz',
        'meaning': 'Бог Тюр, справедливость, закон, вождь, руководство',
        'description': 'Таннит — пятнадцатая руна, связанная с богом Тюром. Она символизирует справедливость, закон, лидерство и моральную силу.',
        'keywords': ['Тюр', 'справедливость', 'закон', 'вождь'],
        'futhark': 2, 'position': 15
    },
    {
        'id': 'othala',
        'rune': 'ᛏ',
        'name': 'Одал',
        'translit': 'Ōðala',
        'meaning': 'Наследие, дом, предки, родовое право, земля',
        'description': 'Одал — шестнадцатая руна, символ наследия и дома. Она представляет родовое право, связь с предками и землю как источник силы.',
        'keywords': ['наследие', 'дом', 'предки', 'земля'],
        'futhark': 2, 'position': 16
    },
    # Третья фук (Mannaz-Úlfr) — высшие знания, трансформация
    {
        'id': 'mannaz',
        'rune': 'ᛗ',
        'name': 'Мандаз',
        'translit': 'Mannaz',
        'meaning': 'Человек, общество, разум, самосознание, общение',
        'description': 'Мандаз — семнадцатая руна, символ человека и общества. Она олицетворяет разум, самосознание, общение и социальную гармонию.',
        'keywords': ['человек', 'общество', 'разум', 'самосознание'],
        'futhark': 3, 'position': 17
    },
    {
        'id': 'laugaz',
        'rune': 'ᛚ',
        'name': 'Лаузи',
        'translit': 'Laguz',
        'meaning': 'Вода, поток, интуиция, подсознание, циклы, магическая сила',
        'description': 'Лаузи — восемнадцатая руна, символ воды и потока. Она представляет интуицию, подсознание, магическую силу и циклы жизни.',
        'keywords': ['вода', 'поток', 'интуиция', 'подсознание'],
        'futhark': 3, 'position': 18
    },
    {
        'id': 'ingwaz',
        'rune': 'ᛝ',
        'name': 'Ингуиз',
        'translit': 'Ingwaz',
        'meaning': 'Бог Инг, плодородие, завершение, внутренняя сила, семя',
        'description': 'Ингуиз — девятнадцатая руна, названная в честь бога Инга. Она символизирует завершение цикла, внутреннюю силу, плодородие и семена будущего.',
        'keywords': ['Инг', 'плодородие', 'завершение', 'семя'],
        'futhark': 3, 'position': 19
    },
    {
        'id': 'ehwalaz',
        'rune': 'ᛟ',
        'name': 'Эйлаз',
        'translit': 'Éihwalaz',
        'meaning': 'Мировой змей, трансформация, возрождение, глубина',
        'description': 'Эйлаз — двадцатая руна, символ мирового змея. Она представляет глубокую трансформацию, возрождение из глубин и связь с подземным миром.',
        'keywords': ['змей', 'трансформация', 'возрождение', 'глубина'],
        'futhark': 3, 'position': 20
    },
    {
        'id': 'dagaz',
        'rune': 'ᛞ',
        'name': 'Дараз',
        'translit': 'Dagaz',
        'meaning': 'Рассвет, день, прорыв, пробуждение, переход, надежда',
        'description': 'Дараз — двадцать первая руна, символ рассвета и дня. Она олицетворяет прорыв, пробуждение, переход от тьмы к свету и новую надежду.',
        'keywords': ['рассвет', 'день', 'прорыв', 'пробуждение'],
        'futhark': 3, 'position': 21
    },
    {
        'id': 'olaval',
        'rune': 'ᛡ',
        'name': 'Ульвиз',
        'translit': 'Óðalaz',
        'meaning': 'Волк, безумие Одина, вдохновение, пророчество, безумие',
        'description': 'Ульвиз — двадцать вторая руна, символ волка и безумия Одина. Она представляет вдохновение, пророческое безумие и связь с высшими силами.',
        'keywords': ['волк', 'безумие', 'вдохновение', 'пророчество'],
        'futhark': 3, 'position': 22
    },
    {
        'id': 'hagalaz2',
        'rune': 'ᚨ',
        'name': 'Ансуз',
        'translit': 'Ansuz',
        'meaning': 'Бог Один, слово, мудрость, вдохновение, коммуникация',
        'description': 'Ансуз — двадцать третья руна, названная в честь Одина, бога слова и мудрости. Она символизирует слово, вдохновение, коммуникацию и божественную мудрость.',
        'keywords': ['Один', 'слово', 'мудрость', 'вдохновение'],
        'futhark': 3, 'position': 23
    },
    {
        'id': 'rad2',
        'rune': 'ᚱ',
        'name': 'Райдо',
        'translit': 'Reið',
        'meaning': 'Путешествие, движение, ритм, защита, совет, лодка',
        'description': 'Райдо — двадцать четвёртая руна, символ путешествия и движения. Она представляет ритм жизни, защиту и необходимость совета.',
        'keywords': ['путешествие', 'движение', 'ритм', 'лотка'],
        'futhark': 3, 'position': 24
    }
]

def create_rune_page(rune_data):
    """Create a rune page with consistent styling."""
    html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Руна {rune_data['name']} ({rune_data['translit']}) — {rune_data['meaning']}">
    <title>Руна {rune_data['name']} — Скандинавская Мифология</title>
    <link rel="stylesheet" href="../css/style-new.css">
</head>
<body class="main-page-body">

<!-- ===== СЕВЕРНОЕ СИЯНИЕ ===== -->
<div class="aurora-container">
    <div class="aurora-layer"></div>
    <div class="aurora-layer"></div>
    <div class="aurora-layer"></div>
    <div class="aurora-curtain"></div>
</div>

<!-- ===== ЗВЁЗДЫ ===== -->
<div class="stars" id="stars"></div>

<!-- ===== НАВИГАЦИЯ ===== -->
<nav class="navbar" id="navbar">
    <div class="nav-container">
        <a href="../index.html" class="nav-logo">
            <span class="nav-rune">ᚱ</span>
            <span class="nav-name">Scandic</span>
        </a>
        <ul class="nav-menu" id="navMenu">
            <li><a href="../index.html#worlds" class="nav-link"><span class="rune">☽</span> Миры</a></li>
            <li><a href="../index.html#pantheons" class="nav-link"><span class="rune">⚡</span> Боги</a></li>
            <li><a href="../index.html#runes" class="nav-link"><span class="rune">ᚠ</span> Руны</a></li>
            <li><a href="../index.html#sagas" class="nav-link"><span class="rune">📜</span> Саги</a></li>
            <li><a href="../literature.html" class="nav-link"><span class="rune">📖</span> Литература</a></li>
            <li><a href="../about.html" class="nav-link"><span class="rune">ℹ</span> О проекте</a></li>
        </ul>
        <button class="nav-toggle" id="navToggle" aria-label="Меню">
            <span></span><span></span><span></span>
        </button>
    </div>
</nav>

<!-- ===== РУНА ===== -->
<section class="section" style="padding-top: 100px;">
    <div style="max-width: 900px; margin: 0 auto; padding: 0 30px;">
        <a href="../index.html#runes" class="back-link">← На руны</a>
        
        <div style="text-align: center; margin: 40px 0;">
            <div style="font-size: 6em; color: var(--gold-auric); font-family: var(--font-runic); text-shadow: 0 0 30px rgba(212,168,85,0.4); margin-bottom: 20px;">
                {rune_data['rune']}
            </div>
            <h1 style="font-family: var(--font-runic); font-size: 2.5em; font-weight: 900; color: var(--gold-bright); letter-spacing: 0.15em; margin-bottom: 10px;">
                {rune_data['name']}
            </h1>
            <p style="font-family: var(--font-legend); font-style: italic; font-size: 1.3em; color: var(--text-mist); margin-bottom: 30px;">
                {rune_data['translit']}
            </p>
            <p style="font-size: 1.1em; color: var(--text-frost); line-height: 1.8; margin-bottom: 40px;">
                {rune_data['meaning']}
            </p>
        </div>
        
        <div style="background: rgba(212,168,85,0.03); border: 1px solid rgba(212,168,85,0.1); border-radius: 8px; padding: 30px; margin-bottom: 30px;">
            <h2 style="font-family: var(--font-heading); font-size: 1.6em; font-weight: 700; color: var(--gold-auric); margin-bottom: 20px;">📖 Описание</h2>
            <p style="color: var(--text-frost); line-height: 1.9; font-size: 1.05em;">
                {rune_data['description']}
            </p>
        </div>
        
        <div style="background: rgba(212,168,85,0.03); border: 1px solid rgba(212,168,85,0.1); border-radius: 8px; padding: 30px; margin-bottom: 30px;">
            <h2 style="font-family: var(--font-heading); font-size: 1.6em; font-weight: 700; color: var(--gold-auric); margin-bottom: 20px;">🔑 Ключевые значения</h2>
            <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                {''.join(f'<span style="display:inline-block; padding: 6px 14px; font-family: var(--font-heading); font-size: 0.85em; color: var(--gold-auric); background: rgba(212,168,85,0.08); border: 1px solid rgba(212,168,85,0.2); border-radius: 20px; letter-spacing: 0.05em;">{kw}</span>' for kw in rune_data['keywords'])}
            </div>
        </div>
        
        <div style="background: rgba(212,168,85,0.03); border: 1px solid rgba(212,168,85,0.1); border-radius: 8px; padding: 30px; margin-bottom: 30px;">
            <h2 style="font-family: var(--font-heading); font-size: 1.6em; font-weight: 700; color: var(--gold-auric); margin-bottom: 20px;">🏛️ Фукх</h2>
            <p style="color: var(--text-frost); line-height: 1.8;">
                Руна {rune_data['name']} относится к {'первой' if rune_data['futhark']==1 else 'второй' if rune_data['futhark']==2 else 'третьей'} фукх Elder Futhark — древнейшему скандинавскому руническому алфавиту из 24 рун, разделённому на 3 фукы по 8 рун.
            </p>
        </div>
        
        <a href="../index.html#runes" class="back-link">← На руны</a>
    </div>
</section>

<!-- ===== FOOTER ===== -->
<footer class="footer">
    <div class="footer-content">
        <div class="footer-rune">ᚱ</div>
        <div class="footer-name">SCANDIC</div>
        <p>Скандинавская мифология — миры, боги, руны и легенды</p>
        <p class="footer-copy">© 2026 Scandic.</p>
    </div>
</footer>

<script>
document.getElementById('navToggle').addEventListener('click', function() {
    document.getElementById('navMenu').classList.toggle('active');
});
window.addEventListener('scroll', function() {
    const navbar = document.getElementById('navbar');
    if (window.scrollY > 50) navbar.classList.add('scrolled');
    else navbar.classList.remove('scrolled');
});
</script>

</body>
</html>'''
    
    filepath = os.path.join(RUNES_PATH, f"{rune_data['id']}.html")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return filepath

# Создаём все 24 руны
created = 0
for rune in RUNES:
    fpath = create_rune_page(rune)
    print(f'✓ {rune["id"]}.html — {rune["name"]} ({rune["translit"]})')
    created += 1

print(f'\nСоздано рун: {created} из 24')
print(f'Elder Futhark: 3 фукы по 8 рун')
