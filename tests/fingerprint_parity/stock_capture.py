"""Capture an official Firefox build without requiring Playwright's Juggler fork."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import subprocess
import signal
import sys
import tempfile
import threading


def capture(executable: str, probe: Path, headless: bool = True):
    done = threading.Event()
    result = {}
    document = probe.read_text(encoding='utf-8') + '''
<script>
const captureTimer = setInterval(async () => {
  const output = document.getElementById('output').textContent;
  if (!output.startsWith('ERR:') && !output.trim().startsWith('{')) return;
  clearInterval(captureTimer);
  await fetch('/result', {method: 'POST', body: output});
  window.close();
}, 50);
</script>'''

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_GET(self):
            if self.path != '/':
                self.send_error(404)
                return
            body = document.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_POST(self):
            size = int(self.headers.get('Content-Length', '0'))
            if self.path != '/result' or not 0 < size <= 1_000_000:
                self.send_error(400)
                return
            result['body'] = self.rfile.read(size).decode('utf-8')
            self.send_response(204)
            self.end_headers()
            done.set()

    with ThreadingHTTPServer(('127.0.0.1', 0), Handler) as server:
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            with tempfile.TemporaryDirectory(prefix='camoufox-stock-probe-') as profile:
                Path(profile, 'user.js').write_text(
                    'user_pref("dom.allow_scripts_to_close_windows", true);\n',
                    encoding='utf-8')
                args = [executable, '--no-remote', '--profile', profile]
                if sys.platform == 'win32':
                    args.append('--wait-for-browser')
                if headless:
                    args.append('--headless')
                args.append(f'http://127.0.0.1:{server.server_port}/')
                process = subprocess.Popen(args, stdout=subprocess.DEVNULL,
                                           stderr=subprocess.DEVNULL,
                                           start_new_session=sys.platform != 'win32')
                try:
                    if not done.wait(60):
                        raise TimeoutError('Stock Firefox did not return fingerprint probes within 60s')
                    if result['body'].startswith('ERR:'):
                        raise RuntimeError(result['body'])
                    return json.loads(result['body'])
                finally:
                    try:
                        process.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        if sys.platform == 'win32':
                            # Terminating only the parent leaves content processes
                            # holding this disposable profile's SQLite files open.
                            subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'],
                                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                           check=True)
                        else:
                            os.killpg(process.pid, signal.SIGKILL)
                        process.wait()
        finally:
            server.shutdown()
            worker.join()
