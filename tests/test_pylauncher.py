"""Запасной запуск через Python: исходники версии и Portabilizer-py.bat кладутся в папку версии.
Запуск: python tests/test_pylauncher.py"""
import http.server, io, shutil, sys, tempfile, threading, zipfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pz_core as C


def mkzip(files):
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w") as z:
        for n, d in files.items():
            z.writestr(n, d)
    return b.getvalue()


SRC = mkzip({"Portabilizer-9.9/portabilizer_v8.py": "print(1)", "Portabilizer-9.9/pzp_isc.py": "x",
             "Portabilizer-9.9/lang/ru.txt": "a", "Portabilizer-9.9/tests/t.py": "t",
             "Portabilizer-9.9/.github/w.yml": "w", "Portabilizer-9.9/__pycache__/a.pyc": "c"})
NOMAIN = mkzip({"Portabilizer-9.9/readme.md": "x"})
files = {"/v9.9.zip": SRC, "/v9.8.zip": NOMAIN}


class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def do_GET(self):
        if self.path not in files:
            self.send_response(404); self.end_headers(); return
        b = files[self.path]
        self.send_response(200); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)


srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
C.SOURCE_URL_FMT = f"http://127.0.0.1:{srv.server_port}/{{tag}}.zip"
tmp = Path(tempfile.mkdtemp()); ok = 0


def check(c, m):
    global ok
    assert c, "ПРОВАЛ: " + m
    ok += 1


v = tmp / "versions" / "v9.9"; v.mkdir(parents=True)
(v / "Portabilizer.exe").write_bytes(b"MZ")
check(C.add_py_launcher(v, "v9.9") is True, "добавление прошло")
check((v / "source" / "portabilizer_v8.py").read_text() == "print(1)" and (v / "source" / "lang" / "ru.txt").is_file(), "исходники на месте")
check(not (v / "source" / "tests").exists() and not (v / "source" / ".github").exists()
      and not (v / "source" / "__pycache__").exists(), "лишнее не скопировано")
bat = (v / C.PY_BAT_NAME).read_bytes()
check(b"\r\n" in bat and b"portabilizer_v8.py" in bat and b"source\\" in bat, "bat записан с CRLF и ищет source")
check(not list((tmp / "versions").glob("_src_*")), "временные папки убраны")
check(C.add_py_launcher(v, "v-нет-в-сети") is True, "повторно: исходники уже есть, сеть не нужна")

w = tmp / "versions" / "v9.8"; w.mkdir()
msgs = []
check(C.add_py_launcher(w, "v9.8", log=msgs.append) is False and not (w / "source").exists() and not (w / C.PY_BAT_NAME).exists(), "нет portabilizer_v8.py: тихий отказ")
check(C.add_py_launcher(w, "v0.0") is False, "404: тихий отказ")
shutil.rmtree(tmp)
print(f"OK: {ok} проверок")
