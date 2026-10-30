/* ================================================================
   «СКАНДИК» — скрипт сайта (чистый JS, без зависимостей)
   1) Бургер-меню: класс .open на <header class="nav"> (узкие экраны).
   2) Активный пункт меню по имени файла страницы
      (+ правило для каталога gods/: подсвечивается «Боги»).
   3) Плавный скролл по якорным ссылкам (с уважением к reduced-motion).
================================================================ */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 1. Бургер-меню ---------- */
  var nav = document.querySelector('.nav');
  var burger = document.querySelector('.nav__burger');

  function setMenu(open) {
    if (!nav || !burger) return;
    nav.classList.toggle('open', !!open);
    burger.setAttribute('aria-expanded', String(!!open));
  }

  if (nav && burger) {
    burger.addEventListener('click', function () {
      setMenu(!nav.classList.contains('open'));
    });

    // На мобильном меню закрывается после клика по ссылке.
    Array.prototype.forEach.call(document.querySelectorAll('.nav__links a'), function (a) {
      a.addEventListener('click', function () { setMenu(false); });
    });

    // Escape закрывает открытое меню и возвращает фокус на кнопку.
    document.addEventListener('keydown', function (e) {
      if ((e.key === 'Escape' || e.keyCode === 27) && nav.classList.contains('open')) {
        setMenu(false);
        burger.focus();
      }
    });

    // При расширении окна до десктопа — сбросить состояние меню.
    window.addEventListener('resize', function () {
      if (window.innerWidth > 1239) setMenu(false);
    });
  }

  /* ---------- 2. Активный пункт меню по имени файла ---------- */
  (function () {
    var links = document.querySelectorAll('.nav__links a');
    if (!links.length) return;

    var path = window.location.pathname || '/';
    var cleanPath = path.replace(/\/+$/, '');
    var file = cleanPath.split('/').pop().toLowerCase();

    // Корень сайта → index.html.
    if (!file) {
      file = 'index.html';
    } else if (/^([a-z0-9_-]+)$/i.test(file)) {
      // Путь без расширения, например http://host/cosmos/ → cosmos.html.
      file += '.html';
    }

    var insideGods = /(^|\/)gods\//i.test(path);

    Array.prototype.forEach.call(links, function (a) {
      var href = a.getAttribute('href') || '';
      var hfile = href.split('/').pop().split('#')[0].split('?')[0].toLowerCase();

      var match = (hfile === file);
      // Страницы богов лежат в gods/ — имя файла не совпадает с пунктом меню,
      // поэтому внутри каталога подсвечиваем «Боги».
      if (!match && insideGods) {
        match = (hfile === 'gods.html');
      }

      a.classList.toggle('active', match);
    });
  })();

  /* ---------- 3. Плавный скролл по якорям ---------- */
  document.addEventListener('click', function (e) {
    var t = e.target;
    if (!t || !t.closest) return;

    var a = t.closest('a[href^="#"]');
    if (!a) return;

    var href = a.getAttribute('href') || '';

    // «#» без имени — вверх страницы.
    if (href === '#') {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
      return;
    }

    var id = href.slice(1);
    var el = document.getElementById(id) || (id ? document.querySelector(href) : null);
    if (!el) return; // Не наш элемент — пусть браузер делает сам.

    e.preventDefault();
    el.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
    if (window.history && history.pushState) {
      history.pushState(null, '', href);
    }
  });
})();

/* === SHARED MAST-SLIDE v1 === */
/* Шапка-слайдер (идея Шефа 30.10): сдвигаешь верхнюю строку влево —
   из-за правого края выезжает карточка побратима; отпустил за порогом —
   переправляет на страницу другой веры. Палец и мышь. */
(function () {
  'use strict';
  var mast = document.querySelector('.masthead[data-twin-href]');
  if (!mast) return;
  var slide = mast.querySelector('.mslide');
  var peek = mast.querySelector('.mpeek');
  var href = mast.getAttribute('data-twin-href');
  if (!slide || !peek || !href) return;

  var x0 = 0, y0 = 0, px = 0, active = false, decided = false, horiz = false, t0 = 0, gone = false;

  function set(p) { // p: 0..1 — насколько уехали
    var w = mast.clientWidth || 1;
    if (p > 1) p = 1; if (p < 0) p = 0;
    slide.style.transform = 'translate3d(' + (-p * w) + 'px,0,0)';
    peek.style.transform = 'translate3d(' + ((1 - p) * w) + 'px,0,0)';
    slide.style.opacity = String(1 - 0.55 * p);
    peek.style.opacity = String(0.35 + 0.65 * p);
  }
  function snap(to, ms) {
    slide.style.transition = peek.style.transition = 'transform ' + ms + 'ms ease, opacity ' + ms + 'ms ease';
    set(to);
  }
  function start() {
    slide.style.transition = peek.style.transition = 'none';
    x0 = y0 = 0; px = 0; decided = false; horiz = false; t0 = Date.now();
  }
  function down(cx, cy, e) {
    if (gone) return;
    if (e && e.target && e.target.closest && e.target.closest('a,button')) return;
    active = true; start();
    x0 = cx; y0 = cy;
  }
  function move(cx, cy) {
    if (!active || gone) return;
    var ddx = cx - x0, ddy = cy - y0;
    if (!decided) {
      if (Math.abs(ddx) + Math.abs(ddy) < 10) return;
      decided = true;
      horiz = Math.abs(ddx) > Math.abs(ddy) * 1.4;
    }
    if (!horiz) return;
    var w = mast.clientWidth || 1;
    px = Math.max(0, Math.min(w, -ddx));      // тянем только влево
    set(px / w);
  }
  function up() {
    if (!active || gone) return;
    active = false;
    if (!horiz) return;
    var w = mast.clientWidth || 1;
    var v = px / Math.max(60, Date.now() - t0); // px/мс
    if (px > w * 0.38 || (v > 0.55 && px > 60)) {
      gone = true;
      snap(1, 180);
      setTimeout(function () { location.href = href; }, 190);
    } else {
      snap(0, 220);
    }
  }

  mast.addEventListener('touchstart', function (e) {
    if (e.touches.length === 1) down(e.touches[0].clientX, e.touches[0].clientY, e);
  }, { passive: true });
  mast.addEventListener('touchmove', function (e) {
    if (active && horiz) e.preventDefault();
    if (e.touches.length === 1) move(e.touches[0].clientX, e.touches[0].clientY);
  }, { passive: false });
  mast.addEventListener('touchend', up);
  mast.addEventListener('touchcancel', up);

  // мышь (десктоп)
  var mdown = false;
  mast.addEventListener('mousedown', function (e) { down(e.clientX, e.clientY, e); mdown = true; });
  window.addEventListener('mousemove', function (e) { if (mdown) move(e.clientX, e.clientY); });
  window.addEventListener('mouseup', function () { if (mdown) { mdown = false; up(); } });

  // клавиатура: Alt + стрелка вправо
  document.addEventListener('keydown', function (e) {
    if (e.altKey && e.key === 'ArrowRight') location.href = href;
  });
})();
