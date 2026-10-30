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

/* === SHARED MAST-SLIDE v2 === */
/* Слайдер «верхней строки» (идея Шефа 30.10): две зоны —
   шапка-наименование (.masthead) и верхняя строка навигации (.nav).
   Тянешь влево пальцем или мышью → выезжает золотая карточка побратима
   (или всего соседнего сайта); отпустил за порогом — переправляет.
   Клавиатура: Alt + →. */
(function () {
  'use strict';
  var zones = Array.prototype.slice.call(
    document.querySelectorAll('.masthead[data-twin-href], .nav[data-nav-href]'));
  if (!zones.length) return;

  function attach(zone) {
    var isMast = zone.classList.contains('masthead');
    var href = zone.getAttribute('data-twin-href') || zone.getAttribute('data-nav-href');
    if (!href) return;
    var track = isMast ? zone.querySelector('.mslide') : null;
    var peek;
    if (isMast) {
      peek = zone.querySelector('.mpeek');
    } else {
      var lab = zone.getAttribute('data-nav-label') || 'на другой берег';
      zone.insertAdjacentHTML('afterbegin',
        '<div class="npeekwrap"><div class="npeek" aria-hidden="true"><b></b><small>отпусти — переправишь →</small></div></div>');
      peek = zone.querySelector('.npeek');
      peek.querySelector('b').textContent = lab;
    }
    if (!peek) return;

    var x0 = 0, y0 = 0, px = 0, active = false, decided = false, horiz = false,
        t0 = 0, gone = false, moved = false;

    function set(p) {
      var w = zone.clientWidth || 1;
      if (p > 1) p = 1; if (p < 0) p = 0;
      peek.style.transform = 'translate3d(' + ((1 - p) * w) + 'px,0,0)';
      peek.style.opacity = String(0.35 + 0.65 * p);
      if (track) {
        track.style.transform = 'translate3d(' + (-p * w) + 'px,0,0)';
        track.style.opacity = String(1 - 0.55 * p);
      }
    }
    function snap(to, ms) {
      var tr = 'transform ' + ms + 'ms ease, opacity ' + ms + 'ms ease';
      peek.style.transition = tr;
      if (track) track.style.transition = tr;
      set(to);
    }
    function down(cx, cy, e) {
      if (gone) return;
      if (e && e.target && e.target.closest &&
          e.target.closest('button,.nav__burger,.nav__links')) return;
      active = true; decided = false; horiz = false; px = 0; t0 = Date.now();
      x0 = cx; y0 = cy;
      track && (track.style.transition = 'none');
      peek.style.transition = 'none';
      document.body.style.userSelect = 'none';
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
      var w = zone.clientWidth || 1;
      px = Math.max(0, Math.min(w, -ddx));
      set(px / w);
    }
    function up() {
      if (!active || gone) return;
      active = false;
      document.body.style.userSelect = '';
      if (!horiz) return;
      var w = zone.clientWidth || 1;
      if (px > 8) moved = true;
      setTimeout(function () { moved = false; }, 400);
      var v = px / Math.max(60, Date.now() - t0);
      if (px > w * 0.3 || (v > 0.5 && px > 50)) {
        gone = true;
        snap(1, 170);
        setTimeout(function () { location.href = href; }, 180);
      } else {
        snap(0, 220);
      }
    }

    // чтобы затяжка не «рождала» клик по ссылке под пальцем
    zone.addEventListener('click', function (e) {
      if (moved) { e.preventDefault(); e.stopPropagation(); }
    }, true);

    zone.addEventListener('touchstart', function (e) {
      if (e.touches.length === 1) down(e.touches[0].clientX, e.touches[0].clientY, e);
    }, { passive: true });
    zone.addEventListener('touchmove', function (e) {
      if (active && horiz) e.preventDefault();
      if (e.touches.length === 1) move(e.touches[0].clientX, e.touches[0].clientY);
    }, { passive: false });
    zone.addEventListener('touchend', up);
    zone.addEventListener('touchcancel', up);

    var mdown = false;
    zone.addEventListener('mousedown', function (e) { down(e.clientX, e.clientY, e); mdown = true; });
    window.addEventListener('mousemove', function (e) { if (mdown) move(e.clientX, e.clientY); });
    window.addEventListener('mouseup', function () { if (mdown) { mdown = false; up(); } });
  }

  zones.forEach(attach);

  // клавиатура: Alt + стрелка вправо → на соседний берег
  document.addEventListener('keydown', function (e) {
    if (e.altKey && e.key === 'ArrowRight') {
      var z = zones[0];
      location.href = z.getAttribute('data-twin-href') || z.getAttribute('data-nav-href');
    }
  });
})();
