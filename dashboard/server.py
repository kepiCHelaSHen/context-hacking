#!/usr/bin/env python3
"""
CHP Dashboard Server
Run from project root: python dashboard/server.py
Open: http://localhost:8765
"""
import json
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).parent.parent  # project root
PORT = 8765
DASHBOARD = Path(__file__).parent


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urlparse(self.path)
        path   = parsed.path

        if path in ('/', '/app.html'):
            self.serve_file(DASHBOARD / 'app.html', 'text/html; charset=utf-8')

        elif path == '/api/index':
            idx = ROOT / 'experiments' / 'EXPERIMENT_INDEX.json'
            if idx.exists():
                self.serve_file(idx, 'application/json')
            else:
                self.send_json({'error': 'EXPERIMENT_INDEX.json not found — run rebuild_index.py'})

        elif path == '/api/file':
            qs  = parse_qs(parsed.query)
            rel = qs.get('path', [''])[0]
            if not rel:
                self.send_error(400, 'path param required')
                return
            target = ROOT / rel
            # Safety: must stay inside project root
            try:
                target.resolve().relative_to(ROOT.resolve())
            except ValueError:
                self.send_error(403, 'path outside project root')
                return
            if target.exists():
                self.serve_file(target, 'text/plain; charset=utf-8')
            else:
                self.send_error(404, f'{rel} not found')

        elif path == '/api/ls':
            qs  = parse_qs(parsed.query)
            rel = qs.get('path', [''])[0]
            target = ROOT / rel if rel else ROOT
            try:
                target.resolve().relative_to(ROOT.resolve())
            except ValueError:
                self.send_error(403)
                return
            if target.is_dir():
                entries = [
                    {'name': e.name, 'type': 'dir' if e.is_dir() else 'file'}
                    for e in sorted(target.iterdir())
                ]
                self.send_json(entries)
            else:
                self.send_error(404)

        else:
            self.send_error(404)

    def serve_file(self, path: Path, content_type: str):
        try:
            data = path.read_bytes()
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(data)
        except Exception as e:
            self.send_error(500, str(e))

    def send_json(self, obj):
        data = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        pass  # silent


if __name__ == '__main__':
    print(f'CHP Dashboard')
    print(f'Project root : {ROOT}')
    print(f'Open         : http://localhost:{PORT}')
    print(f'Stop         : Ctrl+C')
    try:
        HTTPServer(('', PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print('\nStopped.')
