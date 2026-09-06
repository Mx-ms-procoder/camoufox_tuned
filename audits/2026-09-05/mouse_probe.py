"""Bounded mouse-ack regression probe in fresh headless browser instances."""
import asyncio,json,os,sys,time
from pathlib import Path
from playwright.async_api import async_playwright
HERE=Path(__file__).resolve().parent
async def main(exe):
    rows=[]
    async with async_playwright() as p:
        for humanize in [False,True]:
            env={k:v for k,v in os.environ.items() if not k.startswith('CAMOU_CONFIG')}
            env['CAMOU_CONFIG']=json.dumps({'humanize':humanize,'navigator.platform':'Win32','navigator.userAgent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:152.0) Gecko/20100101 Firefox/152.0'})
            b=await p.firefox.launch(executable_path=exe,headless=True,env=env,timeout=20000)
            try:
                page=await b.new_page(viewport={'width':800,'height':600});await page.goto('data:text/html,<title>Local mouse test</title><p>test</p>')
                row={'humanize':humanize}
                for name,x,y in [('near_edge',100,0),('interior_after_edge',100,100)]:
                    start=time.monotonic()
                    try:await asyncio.wait_for(page.mouse.move(x,y),timeout=3);row[name]='completed'
                    except asyncio.TimeoutError:row[name]='timed_out_3s'
                    row[name+'_seconds']=round(time.monotonic()-start,3)
                rows.append(row)
            finally:await b.close()
    (HERE/'evidence/mouse-probe.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');print(json.dumps(rows,indent=2))
asyncio.run(main(sys.argv[1]))
