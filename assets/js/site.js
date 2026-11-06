(() => {
  // menu mobilne
  const burger = document.getElementById('burger');
  const menu = document.getElementById('menu-tel');
  const zamknij = () => { menu.hidden = true; burger.setAttribute('aria-expanded', 'false'); };
  burger.addEventListener('click', () => {
    const otw = menu.hidden;
    menu.hidden = !otw;
    burger.setAttribute('aria-expanded', String(otw));
  });
  menu.addEventListener('click', e => { if (e.target.closest('a')) zamknij(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') zamknij(); });

  // dolny pasek dopiero po przewinięciu za przyciski z pierwszego ekranu
  const mob = document.getElementById('mob');
  const cta = document.getElementById('hero-cta');
  if ('IntersectionObserver' in window && mob && cta) {
    new IntersectionObserver(([w]) => {
      const pokaz = !w.isIntersecting && w.boundingClientRect.top < 0;
      mob.classList.toggle('widac', pokaz);
      mob.setAttribute('aria-hidden', String(!pokaz));
      mob.querySelectorAll('a').forEach(a => a.tabIndex = pokaz ? 0 : -1);
    }).observe(cta);
  }

  // aktywna pozycja menu
  const linki = [...document.querySelectorAll('.nav a, .menu-tel nav a')];
  const sekcje = [...new Set(linki.map(a => a.getAttribute('href')))].map(h => document.querySelector(h)).filter(Boolean);
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(wpisy => {
      wpisy.forEach(w => {
        if (!w.isIntersecting) return;
        const id = '#' + w.target.id;
        linki.forEach(a => a.getAttribute('href') === id ? a.setAttribute('aria-current', 'true') : a.removeAttribute('aria-current'));
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    sekcje.forEach(s => io.observe(s));
  }

  // galerie: palec (natywny scroll-snap), mysz (przeciąganie), strzałki, klawiatura, licznik
  document.querySelectorAll('[data-galeria]').forEach(g => {
    const tor = g.querySelector('.gal-tor');
    const n = tor.children.length;
    const licz = g.querySelector('.gal-licz');
    const idx = () => Math.round(tor.scrollLeft / tor.clientWidth);
    const idz = i => tor.scrollTo({ left: Math.max(0, Math.min(n - 1, i)) * tor.clientWidth, behavior: 'smooth' });
    g.querySelector('.gal-l').addEventListener('click', () => idz(idx() - 1));
    g.querySelector('.gal-p').addEventListener('click', () => idz(idx() + 1));
    tor.addEventListener('keydown', e => {
      if (e.key === 'ArrowLeft') { e.preventDefault(); idz(idx() - 1); }
      if (e.key === 'ArrowRight') { e.preventDefault(); idz(idx() + 1); }
    });
    tor.addEventListener('scroll', () => { licz.textContent = (idx() + 1) + ' / ' + n; }, { passive: true });
    let x0 = 0, s0 = 0, ciag = false;
    tor.addEventListener('pointerdown', e => {
      if (e.pointerType !== 'mouse') return;
      ciag = true; x0 = e.clientX; s0 = tor.scrollLeft;
      tor.setPointerCapture(e.pointerId); tor.classList.add('ciagnie');
    });
    tor.addEventListener('pointermove', e => { if (ciag) tor.scrollLeft = s0 - (e.clientX - x0); });
    const koniec = e => {
      if (!ciag) return;
      ciag = false; tor.classList.remove('ciagnie');
      const d = e.clientX - x0;
      const start = Math.round(s0 / tor.clientWidth);
      idz(Math.abs(d) > 40 ? start + (d < 0 ? 1 : -1) : start);
    };
    tor.addEventListener('pointerup', koniec);
    tor.addEventListener('pointercancel', koniec);
  });

  // formularz pokazowy
  const f = document.getElementById('formularz');
  f.addEventListener('submit', e => {
    e.preventDefault();
    const info = document.getElementById('f-info');
    info.hidden = false;
  });
})();
