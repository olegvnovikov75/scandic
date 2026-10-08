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
