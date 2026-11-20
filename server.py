#!/usr/bin/env python3
"""
One-time installer for the wall panel. You only need this running while you set up the iPad
(or push an update). The iPad then keeps the page in its offline cache and fetches the MTA and
weather data itself, so this computer can be turned off.

    python3 server.py        # then open the printed address in Safari on the iPad
"""
import os
import re
import socket
import sys
import urllib.parse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("PORT", "8080"))
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")


class Handler(SimpleHTTPRequestHandler):
    extensions_map = {**SimpleHTTPRequestHandler.extensions_map, ".appcache": "text/cache-manifest"}

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def end_headers(self):
        # The manifest must never be cached by HTTP, or update checks won't see new versions.
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def do_GET(self):
        path, _, query = self.path.partition("?")
        if path == "/diag":
            # The page reports its offline-cache status here so you can see it in this window.
            msg = urllib.parse.unquote_plus(query.partition("=")[2])[:300]
            print(f"  >> iPad offline cache: {msg}", flush=True)
            self.send_response(204)
            self.end_headers()
            return
        if path in ("/", "/index.html"):
            ua = self.headers.get("User-Agent", "?")
            m = re.search(r"OS (\d+)_(\d+)", ua)
            device = f"iOS {m.group(1)}.{m.group(2)}" if m else "not iOS"
            mode = "home screen app" if "Safari/" not in ua and m else "Safari"
            print(f"  >> Page requested by {self.client_address[0]}: {device}, {mode}", flush=True)
        super().do_GET()

    def log_message(self, fmt, *args):
        if "/diag" not in str(args[0] if args else ""):
            super().log_message(fmt, *args)


class Server(ThreadingHTTPServer):
    def handle_error(self, request, client_address):
        # The iPad often drops idle connections; that's normal, so don't print a traceback for it.
        if isinstance(sys.exc_info()[1], (ConnectionResetError, BrokenPipeError)):
            return
        super().handle_error(request, client_address)


def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


if __name__ == "__main__":
    print(f"On the iPad, open  http://{lan_ip()}:{PORT}  in Safari, then Add to Home Screen.")
    print("After it has loaded once, you can stop this (Ctrl-C).")
    try:
        Server(("0.0.0.0", PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        pass
