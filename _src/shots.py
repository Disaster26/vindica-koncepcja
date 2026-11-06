# -*- coding: utf-8 -*-
"""Zrzuty i testy: python _src/shots.py <runda> [baza] [mapa]
_src/shots/<runda>/: pierwszy ekran i full-page, menu mobilne, raport (konsola, przewijanie poziome, koniec hero, h1)."""
import sys, json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
runda = sys.argv[1] if len(sys.argv) > 1 else "r1"
BASE = sys.argv[2] if len(sys.argv) > 2 else "http://127.0.0.1:8833/"
MAPA = len(sys.argv) > 3
OUT = ROOT / "_src" / "shots" / runda
OUT.mkdir(parents=True, exist_ok=True)
EXE = str(Path.home() / "AppData/Local/ms-playwright/chromium_headless_shell-1228/chrome-headless-shell-win64/chrome-headless-shell.exe")
VP = [(360, 640), (390, 844), (412, 915), (1366, 768), (1440, 900), (2000, 950)]
FULL = {(390, 844), (2000, 950), (1440, 900), (360, 640)}
raport = []
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path=EXE)
    for w, h in VP:
        ctx = br.new_context(viewport={"width": w, "height": h}, is_mobile=w < 768, has_touch=w < 768, locale="pl-PL", device_scale_factor=1)
        if not MAPA:
            ctx.route("**/maps.google.com/**", lambda r: r.abort())
            ctx.route("**/www.google.com/maps/**", lambda r: r.abort())
        pg = ctx.new_page()
        bl = []
        pg.on("console", lambda m: bl.append(m.text) if m.type in ("error", "warning") else None)
        pg.on("pageerror", lambda e: bl.append(str(e)))
        pg.goto(BASE, wait_until="load")
        pg.wait_for_timeout(500)
        pg.screenshot(path=str(OUT / f"home_{w}x{h}.png"))
        info = pg.evaluate("""() => {const cw = document.documentElement.clientWidth;
          const hero = document.querySelector('.hero'); const h1 = document.querySelector('h1');
          const r = document.createRange(); r.selectNodeContents(h1);
          const cta = document.querySelector('#hero-cta').getBoundingClientRect();
          const fig = document.querySelector('.hero-foto').getBoundingClientRect();
          return {sw: document.documentElement.scrollWidth, cw, ih: innerHeight,
            heroBottom: Math.round(hero.getBoundingClientRect().bottom), ctaBottom: Math.round(cta.bottom),
            h1right: Math.round(r.getBoundingClientRect().right), foto: [Math.round(fig.width), Math.round(fig.height)],
            wide: [...document.querySelectorAll('body *')].filter(e => {const b = e.getBoundingClientRect(); return b.right > cw + 1 && b.width > 0 && getComputedStyle(e).position !== 'fixed' && !e.closest('.karty,.gal-tor,.skip');}).slice(0, 5).map(e => e.tagName + '.' + e.className),
            h1n: document.querySelectorAll('h1').length, H: document.body.scrollHeight}}""")
        if (w, h) in FULL:
            pg.evaluate("async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 50)); } window.scrollTo(0, 0); }")
            pg.add_style_tag(content=".mob{display:none!important}.top{position:relative!important}"); pg.wait_for_timeout(400)
            pg.screenshot(path=str(OUT / f"home_{w}x{h}_full.png"), full_page=True)
            pg.reload(wait_until="load"); pg.wait_for_timeout(300)
        if w < 768:
            pg.click("#burger"); pg.wait_for_timeout(350)
            pg.screenshot(path=str(OUT / f"menu_{w}x{h}.png"))
            pg.click("#burger")
            pg.evaluate("window.scrollTo(0, 2600)"); pg.wait_for_timeout(500)
            info["mob"] = pg.evaluate("document.getElementById('mob').classList.contains('widac')")
            pg.screenshot(path=str(OUT / f"przewiniete_{w}x{h}.png"))
        info.update({"vp": f"{w}x{h}", "bledy": bl[:6]})
        raport.append(info)
        ctx.close()
    br.close()
(OUT / "raport.json").write_text(json.dumps(raport, ensure_ascii=False, indent=1), encoding="utf-8")
for r in raport: print(json.dumps(r, ensure_ascii=False))
