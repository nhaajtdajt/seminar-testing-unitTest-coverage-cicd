#!/usr/bin/env python3
"""Serve a local evidence viewer that sends real requests to the packaged app."""
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'evidence/tuan-04-demo'
PAGE = '''<!doctype html><html lang="vi"><meta charset="utf-8">
<title>Minh chứng API mượn sách — Tuần 04</title>
<style>body{font:20px/1.5 Arial,sans-serif;max-width:1120px;margin:32px auto;padding:0 24px;color:#17212b}
h1{font-size:32px}small{display:block;color:#52606d}button{font:inherit;padding:10px 18px;margin:18px 0;cursor:pointer}
table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:10px;border:1px solid #bbb}
th{background:#edf2f7}.pass{color:#126b35;font-weight:bold}pre{font:17px/1.5 monospace;background:#f3f5f7;padding:20px;white-space:pre-wrap}#progress{font-weight:bold}</style>
<h1>Case study thư viện · Kiểm tra API mượn sách</h1>
<small>Trang kiểm tra phục vụ minh chứng; ứng dụng cung cấp REST API, chưa có giao diện người dùng riêng.</small>
<p>Java 25 · Spring Boot 4.1.1 · H2/JPA · POST /api/loans</p>
<button id="run">Chạy 5 tình huống API thật</button>
<p id="progress">Sẵn sàng. Mỗi thao tác gửi HTTP tới ứng dụng đang chạy tại máy.</p>
<table><thead><tr><th>Tình huống</th><th>bookId / memberId</th><th>Kỳ vọng</th><th>Thực tế</th><th>Kết quả</th></tr></thead><tbody id="rows"></tbody></table>
<h2>Phản hồi vừa nhận</h2><pre id="response">Chưa gửi yêu cầu.</pre>
<script>
const cases=[['Mượn thành công',1,1,201,null],['Sách đã được mượn',1,1,409,'BOOK_UNAVAILABLE'],['Không tìm thấy sách',99,1,404,'BOOK_NOT_FOUND'],['bookId không hợp lệ',-1,1,400,null],['Thành viên còn phí chưa trả',3,2,409,'UNPAID_FINE']];
document.querySelector('#run').onclick=async()=>{
 document.querySelector('#run').disabled=true;let passed=0;
 for(const [name,bookId,memberId,status,code] of cases){
  document.querySelector('#progress').textContent='Đang chạy: '+name;
  const request={bookId,memberId};const r=await fetch('/api/loans',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(request)});
  const body=await r.json();const ok=r.status===status&&(!code||body.code===code);if(ok)passed++;
  const row=document.createElement('tr');for(const value of [name,`${bookId} / ${memberId}`,status,r.status,ok?'PASS':'FAIL']){const td=document.createElement('td');td.textContent=value;if(value==='PASS')td.className='pass';row.append(td)}document.querySelector('#rows').append(row);
  document.querySelector('#response').textContent=JSON.stringify({request,http_status:r.status,response:body},null,2);
  await new Promise(resolve=>setTimeout(resolve,2200));
 }
 document.querySelector('#progress').textContent=`Hoàn tất: ${passed}/5 tình huống đạt. Phản hồi được lấy từ ứng dụng thật.`;
};
</script></html>'''


def main():
    if DEST.exists():
        raise SystemExit('Demo evidence already exists; keep the previous capture intact.')
    DEST.mkdir(parents=True)
    results = []
    with tempfile.TemporaryDirectory(prefix='seminar-live-demo-') as temp:
        project = Path(temp) / 'case-study'
        shutil.copytree(ROOT / 'case-study', project, ignore=shutil.ignore_patterns('target'))
        command = [str(project / 'mvnw'), '-o', '-B', '-ntp', '-f', str(project / 'pom.xml'), '-DskipTests', 'package']
        with (DEST / 'package.log').open('w') as log:
            subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=True, timeout=90)
        app_command = ['java', '-jar', str(project / 'target/library-case-study-0.1.0.jar'), '--server.address=127.0.0.1', '--server.port=0']
        with (DEST / 'application.log').open('w') as log:
            app = subprocess.Popen(app_command, stdout=log, stderr=subprocess.STDOUT)
            server = None
            try:
                deadline = time.monotonic() + 45
                while time.monotonic() < deadline:
                    match = re.search(r'Tomcat started on port (\d+)', (DEST / 'application.log').read_text())
                    if match:
                        app_port = int(match.group(1))
                        break
                    if app.poll() is not None:
                        raise RuntimeError('App exited before startup')
                    time.sleep(.2)
                else:
                    raise RuntimeError('App startup timed out')

                class Handler(SimpleHTTPRequestHandler):
                    def __init__(self, *args, **kwargs):
                        super().__init__(*args, directory=str(ROOT), **kwargs)

                    def do_GET(self):
                        if self.path != '/demo':
                            return super().do_GET()
                        body = PAGE.encode()
                        self.send_response(200)
                        self.send_header('Content-Type', 'text/html; charset=utf-8')
                        self.send_header('Content-Length', str(len(body)))
                        self.end_headers()
                        self.wfile.write(body)

                    def do_POST(self):
                        if self.path != '/api/loans':
                            self.send_error(404)
                            return
                        body = self.rfile.read(int(self.headers.get('Content-Length', '0')))
                        request = urllib.request.Request(f'http://127.0.0.1:{app_port}/api/loans', data=body, headers={'Content-Type': 'application/json'})
                        try:
                            response = urllib.request.urlopen(request, timeout=10)
                        except urllib.error.HTTPError as error:
                            response = error
                        with response:
                            status, result = response.status, response.read()
                        results.append({'time_utc': datetime.now(timezone.utc).isoformat(), 'request': json.loads(body), 'actual_status': status, 'response': json.loads(result)})
                        (DEST / 'results.json').write_text(json.dumps({'app_command': app_command, 'cases': results}, ensure_ascii=False, indent=2) + '\n')
                        self.send_response(status)
                        self.send_header('Content-Type', 'application/json')
                        self.send_header('Content-Length', str(len(result)))
                        self.end_headers()
                        self.wfile.write(result)

                    def log_message(self, *args):
                        pass

                server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
                (DEST / 'run.json').write_text(json.dumps({'started_at_utc': datetime.now(timezone.utc).isoformat(), 'viewer_port': server.server_port, 'app_port': app_port, 'package_command': command, 'app_command': app_command, 'note': 'Browser evidence viewer proxies real HTTP responses; this is not the application UI. Packaging skips tests; test results are in evidence/tuan-05/.'}, ensure_ascii=False, indent=2) + '\n')
                print(f'Demo URL: http://127.0.0.1:{server.server_port}/demo', flush=True)
                server.serve_forever()
            except KeyboardInterrupt:
                pass
            finally:
                if server:
                    server.server_close()
                app.terminate()
                try:
                    app.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    app.kill()
                    app.wait()
                metadata = DEST / 'run.json'
                if metadata.exists():
                    value = json.loads(metadata.read_text())
                    value['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
                    metadata.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
