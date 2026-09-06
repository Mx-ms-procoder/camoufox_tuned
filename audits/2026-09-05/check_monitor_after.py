"""Recheck repaired security monitor against the captured primary-source index."""
from contextlib import redirect_stdout
from io import StringIO
import importlib.util
import json
from pathlib import Path
import sys
from unittest.mock import patch

here = Path(__file__).resolve().parent
repo = here.parents[1]
spec = importlib.util.spec_from_file_location('audit_security_after', repo/'scripts/check_upstream_security.py')
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
html = (here/'evidence/mozilla-advisories.html').read_text(encoding='utf-8')
log = StringIO()
with patch.object(module, 'fetch_mfsa_index', return_value=html), redirect_stdout(log):
    code = module.main(['--json', '--upstream', str(repo/'upstream.sh')])
result = {'exit_code': code, 'result': json.loads(log.getvalue())}
(here/'evidence/security-monitor-after.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
