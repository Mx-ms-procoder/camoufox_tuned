"""Deterministic probes against the imported local source; network is mocked."""
from contextlib import redirect_stdout
from io import StringIO
import importlib.util
import json
from pathlib import Path
import sys
import time
from types import SimpleNamespace
from unittest.mock import patch

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]
sys.path.insert(0,str(REPO/'pythonlib'))
spec=importlib.util.spec_from_file_location('audit_security_check',HERE/'evidence/check_upstream_security.before.py')
sec=importlib.util.module_from_spec(spec);sys.modules[spec.name]=sec;spec.loader.exec_module(sec)
html=(HERE/'evidence/mozilla-advisories.html').read_text(encoding='utf-8')
log=StringIO()
with patch.object(sec,'fetch_mfsa_index',return_value=html),redirect_stdout(log):
    rc=sec.main(['--upstream',str(REPO/'upstream.sh')])
results={'security_monitor':{'parsed_records':len(sec.parse_mfsa_index(html)),'parse_major_153':str(sec.FirefoxVersion.parse('153')),'exit_code':rc,'output':log.getvalue()}}

from camoufox import ip
class Response:
    def __init__(self,value):self.text=value
    def __enter__(self):return self
    def __exit__(self,*args):pass
    def raise_for_status(self):pass
ip.public_ip.cache_clear()
with patch.object(ip.requests,'get',return_value=Response('192.0.2.10')):
    first=ip.public_ip('http://rotating.example:8080')
with patch.object(ip.requests,'get',return_value=Response('198.51.100.20')) as mocked:
    second=ip.public_ip('http://rotating.example:8080');calls=mocked.call_count
results['rotating_proxy_cache']={'first_exit':first,'new_exit_available':'198.51.100.20','second_result':second,'network_calls_second_launch':calls}
ip.public_ip.cache_clear()
def fake_get(url,**kwargs):
    time.sleep(.02 if 'ipify' in url else .2)
    return Response('192.0.2.10')
with patch.object(ip.requests,'get',side_effect=fake_get):
    start=time.monotonic();ip.public_ip('http://timing.example:8080');elapsed=time.monotonic()-start
results['first_ip_response_latency']={'first_ready_seconds':.02,'slow_response_seconds':.2,'returned_after_seconds':round(elapsed,3)}
ip.public_ip.cache_clear()

from camoufox.device_profiles.coherence import _panel_exists, _screen_aspect_ratio
portrait=SimpleNamespace(screen_width=1080,screen_height=1920,device_pixel_ratio=1,os_family='win')
results['portrait_panel']={'aspect_rule_accepts':_screen_aspect_ratio(portrait),'panel_rule_accepts':_panel_exists(portrait)}

from camoufox.tls_profiles import get_firefox_profile_for_version,get_tls_env_vars,get_http2_config
profile=get_firefox_profile_for_version(152)
results['network_152']={'source':profile.fingerprint_source,'tls_override_keys':sorted(k for k in get_tls_env_vars(profile) if k.startswith('CAMOU_TLS_')),'http2_overrides':get_http2_config(profile)}
(HERE/'evidence/source-probes.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results,indent=2))
