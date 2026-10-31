"""Самообновление лаунчера, отдельный репозиторий версий, иконки. Запуск: python tests/test_launcher_update.py"""
import sys, io, json, base64, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pz_core as C, pz_icons, launcher as L
n = 0
def check(c, m):
    global n; assert c, "ПРОВАЛ: " + m; n += 1

# адрес репозитория версий
check(C.versions_api_url({}).endswith("/Vanyok-gh/Portabilizer/releases"), "по умолчанию")
check(C.versions_api_url({"versions_repo": "Vanyok-gh/Other"}).endswith("/Vanyok-gh/Other/releases"), "свой репозиторий")
check(C.versions_api_url({"versions_repo": "плохо//../x y"}).endswith("/Vanyok-gh/Portabilizer/releases"), "мусор -> по умолчанию")

data = [{"tag_name": "launcher-v0.4", "html_url": "http://r/0.4", "body": "n"},
        {"tag_name": "launcher-v0.10", "html_url": "http://r/0.10"},
        {"tag_name": "launcher-v0.3"},
        {"tag_name": "launcher-v0.9", "prerelease": True}, {"tag_name": "launcher-v0.11", "draft": True}]
r = C.parse_launcher_release(data, "0.3")
check(r and r["version"] == "0.10", f"0.10 новее 0.4 (числовое сравнение): {r}")
check(C.parse_launcher_release(data, "0.10") is None, "уже последняя")
check(C.parse_launcher_release("мусор", "0.1") is None, "мусор")

class Resp(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *a): return False
def opener(payload):
    def f(req, timeout=0):
        if isinstance(payload, Exception): raise payload
        return Resp(json.dumps(payload).encode())
    return f
check(C.check_launcher_update("0.3", opener=opener(data))["version"] == "0.10", "через сеть")
check(C.check_launcher_update("0.3", opener=opener(OSError("нет сети"))) is None, "ошибка сети не мешает")

tmp = Path(tempfile.mkdtemp())
mix = data + [{"tag_name": "v8.9", "assets": [{"name": "Portabilizer-v8.9.zip", "browser_download_url": "http://x", "size": 1}]}]
m = L.Model({"versions_dir": str(tmp / "v")}, opener=opener(mix), cache=tmp / "c.json")
m.refresh()
check(m.launcher_new and m.launcher_new["version"] == "0.10", "Model.refresh видит новый лаунчер")
check([x.tag for x in m.releases] == ["v8.9"], "launcher-теги не попадают в список версий")

# иконки
from PIL import Image
for k in ("smooth64", "smooth32", "pixel64", "pixel32"):
    im = Image.open(io.BytesIO(base64.b64decode(pz_icons.ICONS[k]))).convert("RGBA")
    check(im.size == (int(k[-2:]),) * 2 and im.getpixel((0, 0))[3] == 0, f"{k}: размер и прозрачный угол")
print(f"самообновление и иконки: {n} проверок пройдено")
cl = open(Path(__file__).resolve().parent.parent / "CHANGELOG.md", encoding="utf-8").read()
d = C.parse_changelog(cl)
check(set(d) == {"8.9", "8.8", "8.7"} and "переносится" in d["8.9"] and "UAC" in d["8.7"], "разбор CHANGELOG")
rs = [C.Release("V8.9"), C.Release("V8.7", notes="своё")]
C.fill_notes_from_changelog(rs, cl)
check("переносится" in rs[0].notes and rs[1].notes == "своё", "пустое заполняется, своё не трогается")
print(f"changelog: всего {n} проверок")

# --- установка: в первом файле нет exe -> берём следующий; голый exe; ничего подходящего
import zipfile, threading, http.server, functools
srv_dir = Path(tempfile.mkdtemp()); (srv_dir / "src.zip").write_bytes(b"")
with zipfile.ZipFile(srv_dir / "portabilizer_v9.zip", "w") as z: z.writestr("portabilizer_v8.py", "print(1)")
with zipfile.ZipFile(srv_dir / "Portabilizer-v9.zip", "w") as z: z.writestr("Portabilizer-v9/Portabilizer.exe", b"MZ" + b"\0" * 50)
(srv_dir / "Portabilizer.exe").write_bytes(b"MZ" + b"\0" * 30)
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(srv_dir))
class Q(H.func):
    def log_message(self, *a): pass
httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Q, directory=str(srv_dir)))
threading.Thread(target=httpd.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{httpd.server_port}/"
def asset(name): return {"name": name, "browser_download_url": base + name, "size": 1}
def rel(*names): return C.parse_releases([{"tag_name": "v9.0", "assets": [asset(x) for x in names]}])[0]
r1 = rel("portabilizer_v9.zip", "Portabilizer-v9.zip")        # первым идёт исходник без exe
check(r1.asset_name == "Portabilizer-v9.zip" or r1.alts, "оба файла учтены")
d = Path(tempfile.mkdtemp()); p = C.install_release(r1, d); check(C.find_exe(p), "поставилось из второго файла")
r2 = rel("Portabilizer.exe", "portabilizer_v9.zip"); check(r2.asset_name == "Portabilizer.exe", "голый exe в приоритете")
d = Path(tempfile.mkdtemp()); p = C.install_release(r2, d); check((p / "Portabilizer.exe").read_bytes()[:2] == b"MZ", "голый exe установлен")
r3 = rel("portabilizer_v9.zip"); d = Path(tempfile.mkdtemp())
try: C.install_release(r3, d); check(False, "должна быть ошибка")
except ValueError as e: check("нет собранной программы" in str(e), f"понятная ошибка: {e}")
check(not any(x.name.startswith("_install_") for x in d.iterdir()), "временные папки убраны")
httpd.shutdown()
print(f"установка из релиза: всего {n} проверок")
