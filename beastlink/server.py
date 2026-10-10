import os
import json
import subprocess
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

from .extractor import ytdlp_meta_command
from .autoinstall import run_autofix


def main():
    password = os.environ.get("BEASTLINK_PASSWORD", "beastlink01")
    port = int(os.environ.get("BEASTLINK_PORT", "2333"))

    print("=" * 50)
    print("  BEASTLINK SERVER")
    print("=" * 50)
    print(f"  Port:     {port}")
    print(f"  Password: {password}")
    print("=" * 50)

    node = run_autofix()

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def _auth(self):
            pw = self.headers.get("X-Beastlink-Password")
            if not pw:
                qs = urllib.parse.urlparse(self.path).query
                params = urllib.parse.parse_qs(qs)
                pw = params.get("password", [None])[0]
            return pw == password

        def _json(self, data, status=200):
            body = json.dumps(data).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path.startswith("/ping"):
                self._json({
                    "status": "ok",
                    "node": bool(node),
                })
                return
            self._json({"error": "Not found"}, 404)

        def do_POST(self):
            if self.path == "/extract":
                if not self._auth():
                    self._json({"error": "Unauthorized"}, 401)
                    return

                length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(length).decode()

                try:
                    data = json.loads(body)
                except Exception:
                    self._json({"error": "Bad JSON"}, 400)
                    return

                query = (data.get("query") or "").strip()
                if not query:
                    self._json({"error": "No query"}, 400)
                    return

                try:
                    r = subprocess.run(
                        ytdlp_meta_command(query),
                        capture_output=True,
                        text=True,
                        timeout=30,
                    )
                    if r.returncode != 0:
                        self._json({"error": r.stderr[:300]}, 500)
                        return

                    info = json.loads(r.stdout)
                    self._json({
                        "title": info.get("title", "Unknown"),
                        "vid": info.get("id", ""),
                        "duration": info.get("duration", 0),
                        "thumbnail": info.get("thumbnail"),
                        "uploader": info.get("uploader", "Unknown"),
                    })
                except Exception as e:
                    self._json({"error": str(e)}, 500)
                return

            self._json({"error": "Not found"}, 404)

    try:
        server = HTTPServer(("0.0.0.0", port), Handler)
        print(f"[HTTP] Running on port {port}")
        server.serve_forever()
    except Exception as e:
        print(f"[HTTP] Failed: {e}")


if __name__ == "__main__":
    main()