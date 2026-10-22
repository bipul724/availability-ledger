"""Pages (UI-09, D-34): / is the landing page, /app is the review app, and the landing page loads nothing from another
site (D-11). Run: python3 -m unittest discover -s tests"""
import re
import sys
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import server  # noqa: E402


class Pages(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
        threading.Thread(target=cls.httpd.serve_forever, daemon=True).start()
        cls.base = f"http://127.0.0.1:{cls.httpd.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()

    def get(self, path):
        try:
            with urllib.request.urlopen(self.base + path, timeout=5) as r:
                return r.status, r.headers.get("Content-Type"), r.read().decode()
        except urllib.error.HTTPError as e:
            with e:
                return e.code, e.headers.get("Content-Type"), e.read().decode()

    def test_root_is_the_landing_page_even_with_a_query_string(self):
        for path in ("/", "/?ref=dev.to"):
            code, ctype, body = self.get(path)
            self.assertEqual((code, ctype), (200, "text/html; charset=utf-8"), path)
            self.assertIn('id="demo"', body)
            self.assertIn('href="/app"', body)

    def test_app_is_served_at_app_and_still_at_index_html(self):
        for path in ("/app", "/app?x=1", "/index.html"):
            code, _, body = self.get(path)
            self.assertEqual(code, 200, path)
            self.assertIn('id="workspace"', body)
            self.assertIn('<a href="/"', body)  # the title leads back to the landing page

    def test_guide_at_docs(self):
        code, _, body = self.get("/docs")
        self.assertEqual(code, 200)
        self.assertIn('class="arch"', body)

    def test_other_paths_unchanged(self):
        self.assertEqual(self.get("/app/")[0], 404)
        code, ctype, body = self.get("/nope")
        self.assertEqual((code, ctype), (404, "text/html; charset=utf-8"))
        self.assertIn('href="/app"', body)  # the 404 page leads back
        self.assertEqual(self.get("/../server.py")[0], 404)
        self.assertEqual(self.get("/home.css")[:2], (200, "text/css; charset=utf-8"))
        self.assertEqual(self.get("/home.js")[:2], (200, "text/javascript; charset=utf-8"))

    def test_landing_page_loads_nothing_from_another_site(self):
        html = "".join((ROOT / "ui" / f).read_text() for f in ("home.html", "docs.html", "404.html"))
        css = "".join((ROOT / "ui" / f).read_text() for f in ("home.css", "docs.css"))
        js = (ROOT / "ui" / "home.js").read_text()
        loads = re.findall(r'<(?:script|img|iframe|source|video|audio)\b[^>]*\bsrc="([^"]+)"', html)
        loads += re.findall(r'<link\b[^>]*\bhref="([^"]+)"', html)
        loads += re.findall(r'url\(\s*["\']?([^"\')]+)', css) + re.findall(r'@import\s+["\']?([^"\';\s]+)', css)
        self.assertTrue(loads)
        for url in loads:
            self.assertFalse(re.match(r"(https?:)?//", url), url)
        self.assertEqual(re.findall(r'fetch\("([^"]+)"', js), ["/api/status"])


if __name__ == "__main__":
    unittest.main()
