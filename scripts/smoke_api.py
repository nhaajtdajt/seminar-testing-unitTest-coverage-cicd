#!/usr/bin/env python3
"""Start the packaged app on a random loopback port, exercise HTTP, then shut it down."""
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]

def main():
    dest = ROOT / 'evidence/tuan-05/http-smoke'
    if dest.exists():
        raise SystemExit('Evidence exists; use a fresh copy to rerun')
    dest.mkdir(parents=True)
    jar = ROOT / 'case-study/target/library-case-study-0.1.0.jar'
    command = ['java', '-jar', str(jar), '--server.address=127.0.0.1', '--server.port=0']
    results = []
    with (dest/'application.log').open('w') as log:
        app = subprocess.Popen(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
        try:
            deadline = time.monotonic()+45
            port = None
            while time.monotonic() < deadline:
                text = (dest/'application.log').read_text()
                match = re.search(r'Tomcat started on port (\d+)', text)
                if match:
                    port = int(match.group(1)); break
                if app.poll() is not None:
                    raise RuntimeError('Application exited before startup; inspect application.log')
                time.sleep(0.2)
            if port is None:
                raise RuntimeError('Application startup timed out')
            cases = [(1,1,201,None), (1,1,409,'BOOK_UNAVAILABLE'), (99,1,404,'BOOK_NOT_FOUND'), (-1,1,400,None), (3,2,409,'UNPAID_FINE')]
            for book, member, expected_status, expected_code in cases:
                body = {'bookId':book, 'memberId':member}
                req = urllib.request.Request(f'http://127.0.0.1:{port}/api/loans', data=json.dumps(body).encode(), headers={'Content-Type':'application/json'})
                try:
                    response = urllib.request.urlopen(req, timeout=5)
                except urllib.error.HTTPError as error:
                    response = error
                with response:
                    status, result = response.status, json.load(response)
                passed = status == expected_status and (expected_code is None or result.get('code') == expected_code)
                results.append({'time_utc':datetime.now(timezone.utc).isoformat(), 'request':body, 'expected_status':expected_status, 'actual_status':status, 'response':result, 'pass':passed})
                (dest/'results.json').write_text(json.dumps({'command':command, 'port':port, 'cases':results}, ensure_ascii=False, indent=2)+"\n")
                if not passed:
                    raise AssertionError(f'HTTP scenario failed: {body}')
        finally:
            app.terminate()
            try:
                app.wait(timeout=10)
            except subprocess.TimeoutExpired:
                app.kill(); app.wait()
    print(f'HTTP smoke: {len(results)}/5 scenarios passed; app stopped.')

if __name__ == '__main__':
    main()
