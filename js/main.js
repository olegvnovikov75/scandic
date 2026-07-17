/* ========================================
   SCANDIC — JavaScript
   Интерактивность и анимации
   ======================================== */

document.addEventListener('DOMContentLoaded', () => {

  // ===== НАВИГАЦИЯ =====
  const navToggle = document.getElementById('navToggle');
  const navMenu = document.getElementById('navMenu');
  const navLinks = document.querySelectorAll('.nav-link');

  // Toggle mobile menu
  navToggle.addEventListener('click', () => {
    navMenu.classList.toggle('active');
  });

  // Close mobile menu on link click
  navLinks.forEach(link => {
    link.addEventListener('click', () => {
      navMenu.classList.remove('active');
    });
  });

  // ===== ПЛАВНЫЙ СКРОЛЛ =====
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        const offset = 70;
        const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - offset;
        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth'
        });
      }
    });
  });

  // ===== АНИМАЦИЯ ПОЯВЛЕНИЯ ЭЛЕМЕНТОВ =====
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, observerOptions);

  // Наблюдаем за всеми секциями и карточками
  document.querySelectorAll('.god-card, .myth-card, .rune-cell, .world-card, .saga-card, .gallery-item').forEach(el => {
    el.classList.add('fade-in');
    observer.observe(el);
  });

  // ===== РУНЫ — МОДАЛЬНОЕ ОКНО =====
  const runeCells = document.querySelectorAll('.rune-cell');
  const runeModal = document.getElementById('runeModal');
  const runeModalClose = document.getElementById('runeModalClose');
  const modalRuneSymbol = document.getElementById('modalRuneSymbol');
  const modalRuneName = document.getElementById('modalRuneName');
  const modalRuneMeaning = document.getElementById('modalRuneMeaning');
  const modalRuneAttributes = document.getElementById('modalRuneAttributes');

  // Данные рун
  const runesData = {
    feoh: { name: 'Feoh', meaning: 'Богатство, достояние, материальное благополучие' },
    uruz: { name: 'Uruz', meaning: 'Сила, здоровье, дикий бык, жизненная энергия' },
    thurisaz: { name: 'Thurisaz', meaning: 'Великан, шип, защита, кармическое воздаяние' },
    ansuz: { name: 'Ansuz', meaning: 'Бог, слово, вдохновение, мудрость Одина' },
    raidho: { name: 'Raidho', meaning: 'Путешествие, колесница, внутренний порядок' },
    kenaz: { name: 'Kenaz', meaning: 'Факел, знание, творчество, просветление' },
    gebo: { name: 'Gebo', meaning: 'Дар, дружба, взаимность, изобилие' },
    wunjo: { name: 'Wunjo', meaning: 'Радость, счастье, благополучие, гармония' },
    haglaz: { name: 'Haglaz', meaning: 'Мётл, буря, испытание, трансформация' },
    haggiz: { name: 'Haggiz', meaning: 'Мётл, защита, разрушение преград' },
    nauthiz: { name: 'Nauthiz', meaning: 'Нужда, необходимость, терпение, выживание' },
    isa: { name: 'Isa', meaning: 'Лёд, застой, ясность, внутреннее сосредоточение' },
    jera: { name: 'Jera', meaning: 'Урожай, сезон, цикл, терпение и награда' },
    eihwaz: { name: 'Eihwaz', meaning: 'Иггдрасиль, прочность, жизненная сила' },
    perthro: { name: 'Perthro', meaning: 'Тайна, судьба, кровь, скрытое знание' },
    algiz: { name: 'Algiz', meaning: 'Защита, олень, щит, покровительство богов' },
    sowilo: { name: 'Sowilo', meaning: 'Солнце, сила, победа, целостность' },
    tiwaz: { name: 'Tiwaz', meaning: 'Тюр, справедливость, победа, героизм' },
    beorthan: { name: 'Beorthan', meaning: 'Берёза, обновление, очищение, рождение' },
    menaz: { name: 'Menaz', meaning: 'Мудрец, порядок, учение, дисциплина' },
    ingwaz: { name: 'Ingwaz', meaning: 'Инг, плодородие, завершение, внутренняя сила' },
    dagaz: { name: 'Dagaz', meaning: 'День, рассвет, прорыв, пробуждение' },
    mathuzang: { name: 'Mathuzang', meaning: 'Дом, отцовский дом, семейная связь' },
    lauthiz: { name: 'Lauthiz', meaning: 'Рана, знание через боль, прозрение' },
    kaunan: { name: 'Kaunan', meaning: 'Рана, огонь, знание, творческий огонь' },
    nauðiz: { name: 'Nauðiz', meaning: 'Нужда, вынужденность, преодоление' }
  };

  runeCells.forEach(cell => {
    cell.addEventListener('click', () => {
      const runeKey = cell.dataset.rune;
      const rune = runesData[runeKey];

      if (rune) {
        modalRuneSymbol.textContent = cell.querySelector('.rune-symbol').textContent;
        modalRuneName.textContent = rune.name;
        modalRuneMeaning.textContent = rune.meaning;
        runeModal.classList.add('active');
      }
    });
  });

  // Закрытие модального окна
  runeModalClose.addEventListener('click', () => {
    runeModal.classList.remove('active');
  });

  runeModal.addEventListener('click', (e) => {
    if (e.target === runeModal) {
      runeModal.classList.remove('active');
    }
  });

  // Закрытие на Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      runeModal.classList.remove('active');
    }
  });

  // ===== НАВИГАЦИЯ — ПОДСВЕТКА АКТИВНОЙ СЕКЦИИ =====
  const sections = document.querySelectorAll('.section[id]');

  function updateActiveNav() {
    const scrollPos = window.scrollY + 100;

    sections.forEach(section => {
      const top = section.offsetTop;
      const height = section.offsetHeight;
      const id = section.getAttribute('id');

      if (scrollPos >= top && scrollPos < top + height) {
        navLinks.forEach(link => {
          link.classList.remove('active-link');
          if (link.getAttribute('href') === `#${id}`) {
            link.classList.add('active-link');
          }
        });
      }
    });
  }

  window.addEventListener('scroll', updateActiveNav);

  // ===== СТИЛЬ НАВИГАЦИИ ПРИ СКРОЛЛЕ =====
  const navbar = document.getElementById('navbar');

  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      navbar.style.borderBottomColor = 'rgba(196, 163, 90, 0.25)';
    } else {
      navbar.style.borderBottomColor = 'rgba(196, 163, 90, 0.15)';
    }
  });

});
