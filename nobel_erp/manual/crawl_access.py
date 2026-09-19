import os
WORK = os.environ.get('NBL_MANUAL_WORK', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'work'))
CHROME = os.environ.get('NBL_CHROME', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
import sys, json, os, re
from playwright.sync_api import sync_playwright
BASE = 'http://127.0.0.1:9096'
ROOT = WORK + '/manual'
def login(p, user):
    p.goto(BASE + '/web/login', wait_until='domcontentloaded'); p.wait_for_timeout(1500)
    p.fill('input[name="login"]', user); p.fill('input[name="password"]', 'nobel-test-1234')
    p.click('button[type="submit"]'); p.wait_for_timeout(7000)
    assert '/web/login' not in p.url, 'LOGIN_FAILED ' + user
def safe(name): return re.sub(r'[^\w؀-ۿ]+', '_', name)[:40]
def open_apps(p):
    if p.locator('.o_home_menu .o_app').count() > 0:
        return
    try: p.locator('a.o_menu_toggle').first.click(timeout=8000)
    except Exception: p.goto(BASE + '/odoo', wait_until='domcontentloaded')
    p.wait_for_timeout(2500)
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
    for who in sys.argv[1:]:
        out = f'{ROOT}/{who}'; os.makedirs(out, exist_ok=True)
        ctx = b.new_context(viewport={'width': 1500, 'height': 1000}); p = ctx.new_page()
        try:
            login(p, who)
            p.goto(BASE + '/odoo', wait_until='domcontentloaded'); p.wait_for_timeout(6000)
            open_apps(p)
            try: p.locator('.database_expiration_panel .close, .o_home_menu .alert .btn-close').first.click(timeout=1200)
            except Exception: pass
            p.screenshot(path=f'{out}/00_apps.png')
            items = p.locator('.o_home_menu .o_app').all()
            names = []
            for a in items:
                try:
                    t = a.inner_text().strip(); x = a.get_attribute('data-menu-xmlid') or ''
                    if t and (t, x) not in names: names.append((t, x))
                except Exception: pass
            print(who, 'APPS', len(names), flush=True)
            info = {'apps': [], 'user': who}
            for i, (name, xmlid) in enumerate(names):
                try:
                    p.goto(BASE + '/odoo', wait_until='domcontentloaded'); p.wait_for_timeout(2500)
                    open_apps(p)
                    p.locator('.o_home_menu .o_app', has_text=name).first.click(); p.wait_for_timeout(6500)
                    p.keyboard.press('Escape'); p.wait_for_timeout(300)
                    sections = [s.strip() for s in p.locator('.o_menu_sections > *').all_inner_texts() if s.strip()]
                    subs = {}
                    for btn in p.locator('.o_menu_sections .dropdown-toggle').all():
                        try:
                            label = btn.inner_text().strip(); btn.click(); p.wait_for_timeout(700)
                            its = [t.strip() for t in p.locator('.o-dropdown--menu .dropdown-item').all_inner_texts() if t.strip()]
                            subs[label] = its; p.keyboard.press('Escape'); p.wait_for_timeout(300)
                        except Exception: pass
                    fname = f'{out}/app_{i:02d}_{safe(name)}.png'
                    p.screenshot(path=fname)
                    info['apps'].append({'name': name, 'xmlid': xmlid, 'url': p.url, 'sections': sections, 'subs': subs, 'shot': os.path.basename(fname)})
                    print(who, '|', name, '|', ' · '.join(sections)[:150], flush=True)
                except Exception as e:
                    print(who, '| ERR', name, str(e)[:100], flush=True)
            json.dump(info, open(f'{out}/access.json', 'w'), ensure_ascii=False, indent=1)
        except Exception as e:
            print('FATAL', who, str(e)[:200], flush=True)
        ctx.close()
    b.close()
