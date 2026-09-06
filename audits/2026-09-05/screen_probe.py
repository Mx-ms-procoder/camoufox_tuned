"""Compare CSS screen queries with and without a Playwright viewport override."""
import asyncio
import json
import os
from pathlib import Path
import sys
from playwright.async_api import async_playwright

async def main(executable):
    env = {k:v for k,v in os.environ.items() if not k.startswith(('CAMOU_CONFIG', 'CAMOU_TLS_'))}
    env['CAMOU_CONFIG'] = json.dumps({'screen.width':1664, 'screen.height':936, 'allowMainWorld':True})
    result = []
    async with async_playwright() as p:
        browser = await p.firefox.launch(executable_path=executable,headless=True,env=env)
        try:
            for name, options in [('viewport', {'viewport':{'width':800,'height':600}}), ('no_viewport', {'no_viewport':True})]:
                context = await browser.new_context(**options)
                try:
                    page = await context.new_page()
                    await page.goto('data:text/html,<pre id="result"></pre><script>document.querySelector("pre").textContent=JSON.stringify({screen:screen.width,inner:innerWidth,cssConfigured:matchMedia("(device-width:1664px)").matches,css1920:matchMedia("(device-width:1920px)").matches,css800:matchMedia("(device-width:800px)").matches,cssInner:matchMedia("(device-width:"+innerWidth+"px)").matches})</script>')
                    result.append({'mode':name,'result':json.loads(await page.locator('#result').text_content())})
                finally:
                    await context.close()
        finally:
            await browser.close()
    (Path(__file__).parent/'evidence/screen-probe.json').write_text(json.dumps(result, indent=2),encoding='utf-8')
    print(json.dumps(result, indent=2))

asyncio.run(main(sys.argv[1]))
