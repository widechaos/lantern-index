"""Loopback-only demo; no uploads, accounts, telemetry or query log."""
import json, os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from archive import Archive, ROOT
PORT = int(os.environ.get("PORT", "8804"))
class Handler(BaseHTTPRequestHandler):
    engine = None
    def log_message(self, *args):
        pass
    def send(self, status, body, mime="application/json; charset=utf-8"):
        if not isinstance(body, bytes): body = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'")
        self.end_headers(); self.wfile.write(body)
    def allowed(self):
        return self.headers.get("Host") in {f"127.0.0.1:{PORT}", f"localhost:{PORT}"} and self.headers.get("Origin") in {None, f"http://127.0.0.1:{PORT}", f"http://localhost:{PORT}"}
    def do_GET(self):
        if not self.allowed(): return self.send(403, {"error":"Local origin required"})
        files = {"/": ("index.html","text/html"), "/app.js": ("app.js","text/javascript"), "/style.css": ("style.css","text/css")}
        if self.path not in files: return self.send(404, {"error":"Not found"})
        name,mime=files[self.path]; self.send(200,(ROOT/"web"/name).read_bytes(),mime+"; charset=utf-8")
    def do_POST(self):
        if not self.allowed(): return self.send(403,{"error":"Local origin required"})
        if self.path not in {"/search","/ending"}: return self.send(404,{"error":"Not found"})
        try:
            length=int(self.headers.get("Content-Length","0"))
            if not 0 < length <= 4096: raise ValueError("Request size must be 1–4096 bytes")
            if self.headers.get("Content-Type") != "application/json": raise ValueError("JSON required")
            data=json.loads(self.rfile.read(length))
            if not isinstance(data,dict):raise ValueError("Object required")
            if self.path == "/search" and set(data)=={"query"}: result=self.engine.search(data["query"])
            elif self.path == "/ending" and set(data)=={"ids"}:result=self.engine.ending(data["ids"])
            else:raise ValueError("Unexpected request fields")
            self.send(200,result)
        except (ValueError, UnicodeError, TypeError) as e:self.send(400,{"error":str(e)})
if __name__ == "__main__":
    Handler.engine=Archive()
    print(f"Lantern Index ready at http://127.0.0.1:{PORT}",flush=True)
    HTTPServer(("127.0.0.1",PORT),Handler).serve_forever()
