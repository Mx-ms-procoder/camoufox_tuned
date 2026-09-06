"""Run local-only page probes in a disposable profile; no real user profiles."""
import argparse
import asyncio
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import threading
from playwright.async_api import async_playwright

HERE = Path(__file__).resolve().parent
PAGE = (HERE / 'runtime-probes.html').read_bytes()
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body=PAGE
        if self.path.startswith('/headers'):
            body=json.dumps({k:v for k,v in self.headers.items() if k.lower() in ['user-agent','accept-language','pragma','cache-control','accept-encoding']}).encode()
        self.send_response(200);self.send_header('Content-Type','application/json' if self.path.startswith('/headers') else 'text/html; charset=utf-8');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
    def log_message(self,*args):pass

async def main(executable, output_path=None, ua_version='152.0'):
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    outputs=[]
    try:
        async with async_playwright() as p:
            for seed in [0,111,222]:
                config={'canvas:noiseSeed':seed,'audio:seed':seed,'timezone':'Europe/Berlin','locale:language':'de','locale:region':'DE','locale:all':'de,en-US,en','navigator.language':'de','navigator.languages':['de','en-US','en'],'navigator.platform':'Win32','navigator.userAgent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:152.0) Gecko/20100101 Firefox/152.0','navigator.appVersion':'5.0 (Windows)','navigator.hardwareConcurrency':8,'screen.width':1920,'screen.height':1080,'screen.availWidth':1920,'screen.availHeight':1040,'main_world_eval':True,'webrtc:ipv4':'192.0.2.10'}
                # Raw engine config uses allowMainWorld; main_world_eval is a
                # Python launch_options argument, not a MaskConfig property.
                config.pop('main_world_eval', None)
                config['navigator.userAgent'] = (
                    f'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{ua_version}) '
                    f'Gecko/20100101 Firefox/{ua_version}')
                config['allowMainWorld'] = True
                env={k:v for k,v in os.environ.items() if not k.startswith(('CAMOU_CONFIG','CAMOU_TLS_'))}
                env['CAMOU_CONFIG']=json.dumps(config)
                browser=None
                try:
                    browser=await p.firefox.launch(executable_path=executable,headless=True,env=env,timeout=20000,firefox_user_prefs={'app.update.enabled':False,'browser.safebrowsing.provider.google4.updateURL':'','browser.safebrowsing.provider.mozilla.updateURL':'','services.settings.server':'','network.captive-portal-service.enabled':False,'network.connectivity-service.enabled':False})
                    context=await browser.new_context(viewport={'width':800,'height':600})
                    await context.add_init_script('mw: window.__audit_init_marker = "present";')
                    page=await context.new_page();await page.goto(f'http://127.0.0.1:{server.server_port}/',wait_until='load',timeout=15000)
                    data=None
                    for _ in range(80):
                        raw=await page.locator('#result').text_content()
                        if raw and raw!='pending':data=json.loads(raw);break
                        await asyncio.sleep(.1)
                    await page.goto('data:text/html,<pre id="navigation-marker"></pre><script>document.getElementById("navigation-marker").textContent=String(window.__audit_init_marker)</script>')
                    navigation_marker = await page.locator('#navigation-marker').text_content()
                    await page.route('**/headers-route',lambda route:route.continue_())
                    routed=await context.new_page();await routed.route('**/headers-route',lambda route:route.continue_());await routed.goto(f'http://127.0.0.1:{server.server_port}/headers-route')
                    routed_headers=json.loads(await routed.locator('body').text_content());await routed.close()
                    outputs.append({'seed':seed,'browserVersion':browser.version,'result':data,'routed_headers':routed_headers,'navigation_init_marker':navigation_marker})
                except Exception as e:outputs.append({'seed':seed,'error':str(e)})
                finally:
                    if browser:await browser.close()
    finally:server.shutdown();server.server_close()
    result={'executable':executable,'executable_sha256':hashlib.sha256(Path(executable).read_bytes()).hexdigest(),'runs':outputs}
    (Path(output_path) if output_path else HERE/'evidence/runtime-results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({'runs':[{'seed':r['seed'],'error':r.get('error'),'audio':(r.get('result') or {}).get('audio'),'webgl':(r.get('result') or {}).get('webgl'),'screen':(r.get('result') or {}).get('screen'),'animation':(r.get('result') or {}).get('animation'),'headers':(r.get('result') or {}).get('headers'),'routed_headers':r.get('routed_headers')} for r in outputs]},indent=2))
    return result
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('executable');args=ap.parse_args();asyncio.run(main(args.executable))
