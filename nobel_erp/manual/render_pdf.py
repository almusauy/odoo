import sys
from playwright.sync_api import sync_playwright
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
src, out = sys.argv[1], sys.argv[2]
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
    p = b.new_page()
    p.goto('file://' + src, wait_until='load'); p.wait_for_timeout(4000)
    p.emulate_media(media='print')
    p.pdf(path=out, format='A4', print_background=True, prefer_css_page_size=True,
          display_header_footer=True, header_template='<div></div>',
          footer_template='<div style="font-size:9px;width:100%;text-align:center;color:#888;font-family:sans-serif"><span class="pageNumber"></span> / <span class="totalPages"></span></div>')
    b.close()
print('PDF', out)
