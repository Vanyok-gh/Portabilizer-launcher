"""Проверка ядра лаунчера. Запуск: python tests/test_core.py"""
import hashlib, http.server, io, json, os, shutil, stat, sys, tempfile, threading, time, zipfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pz_core as C

def mkzip(files: dict) -> bytes:
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w", zipfile.ZIP_DEFLATED) as z:
        for n, d in files.items(): z.writestr(n, d)
    return b.getvalue()

GOOD = mkzip({"Portabilizer.exe": b"MZ-fake-v87", "readme.txt": "hi"})
NESTED = mkzip({"dist/Portabilizer.exe": b"MZ-fake-v86"})
EVIL = mkzip({"../evil.txt": b"x", "Portabilizer.exe": b"MZ"})
NOEXE = mkzip({"other.txt": b"x"})
sha = lambda b: hashlib.sha256(b).hexdigest()
files = {"/a/Portabilizer-v8.7.zip": GOOD, "/a/Portabilizer-v8.6.zip": NESTED, "/a/evil.zip": EVIL,
         "/a/noexe.zip": NOEXE, "/a/sums.txt": f"{sha(NESTED)}  Portabilizer-v8.6.zip\n".encode()}

class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/releases":
            base = f"http://127.0.0.1:{self.server.server_port}"
            data = [
              {"tag_name": "v8.6", "name": "8.6", "body": "тема", "prerelease": False, "draft": False, "published_at": "2026-10-29T10:00:00Z",
               "assets": [{"name": "Portabilizer-v8.6.zip", "size": len(NESTED), "browser_download_url": base + "/a/Portabilizer-v8.6.zip"},
                          {"name": "SHA256SUMS.txt", "size": 10, "browser_download_url": base + "/a/sums.txt"}]},
              {"tag_name": "v8.7", "name": "8.7", "body": "дубль подсказки", "prerelease": True, "draft": False, "published_at": "2026-10-30T10:00:00Z",
               "assets": [{"name": "Portabilizer-v8.7.zip", "size": len(GOOD), "digest": "sha256:" + sha(GOOD), "browser_download_url": base + "/a/Portabilizer-v8.7.zip"}]},
              {"tag_name": "v9.0", "draft": True, "assets": []},
              {"tag_name": "v7.3", "name": "7.3", "body": "", "prerelease": False, "draft": False, "assets": []},
              {"tag_name": "v10.0", "name": "10", "body": "SHA-256: " + sha(EVIL), "prerelease": False, "draft": False,
               "assets": [{"name": "evil.zip", "size": len(EVIL), "browser_download_url": base + "/a/evil.zip"}]},
              {"tag_name": "v10.1", "name": "10.1", "body": "", "prerelease": False, "draft": False,
               "assets": [{"name": "noexe.zip", "size": len(NOEXE), "browser_download_url": base + "/a/noexe.zip"}]},
              {"tag_name": "v8.7-bad", "name": "bad", "body": "", "prerelease": False, "draft": False,
               "assets": [{"name": "Portabilizer-v8.7.zip", "size": len(GOOD), "digest": "sha256:" + "0" * 64, "browser_download_url": base + "/a/Portabilizer-v8.7.zip"}]},
            ]
            body = json.dumps(data).encode()
        elif path in files:
            body = files[path]
        else:
            self.send_response(404); self.end_headers(); return
        self.send_response(200); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{srv.server_port}/releases"
tmp = Path(tempfile.mkdtemp()); ok = 0
def check(cond, msg):
    global ok
    assert cond, "ПРОВАЛ: " + msg
    ok += 1

# версии и порядок
check(C.parse_version("v8.7") == (8, 7) and C.parse_version("v10.0") > C.parse_version("v9.9") and C.parse_version("beta") == (0,), "parse_version")
cache = tmp / "cache.json"
rels = C.fetch_releases(URL, cache=cache)
tags = [r.tag for r in rels]
check(tags == ["v10.1", "v10.0", "v8.7", "v8.7-bad", "v8.6", "v7.3"] or tags[:2] == ["v10.1", "v10.0"], f"порядок/черновики: {tags}")
check("v9.0" not in tags, "черновик скрыт")
by = {r.tag: r for r in rels}
check(by["v8.7"].channel == "Beta" and by["v8.6"].channel == "Stable", "канал")
check(by["v8.7"].sha256 == sha(GOOD), "digest из API")
check(by["v8.6"].sha_url.endswith("sums.txt") and by["v8.6"].sha256 == "", "файл сумм")
check(by["v10.0"].sha256 == sha(EVIL), "сумма из описания релиза")
check(not by["v7.3"].available, "релиз без файла")

# установка
vd = tmp / "versions"; msgs = []; prog = []
p = C.install_release(by["v8.7"], vd, progress=lambda g, t: prog.append((g, t)), log=msgs.append)
check((p / "Portabilizer.exe").read_bytes() == b"MZ-fake-v87" and (p / ".installed.json").is_file(), "установка v8.7")
check(prog and prog[-1][0] == len(GOOD) and prog[-1][1] == len(GOOD), "прогресс с Content-Length")
check(any("совпала" in m for m in msgs), "сообщение о сумме")
p6 = C.install_release(by["v8.6"], vd)
check(C.find_exe(p6).parent.name == "dist", "exe во вложенной папке dist")
check(not list(vd.glob("_install_*")), "временные папки убраны")
try: C.install_release(by["v8.7-bad"], vd); check(False, "неверная сумма не поймана")
except ValueError as e: check("сумма" in str(e), "неверная сумма -> ошибка")
check(not (vd / "v8.7-bad").exists(), "после неверной суммы ничего не осталось")
try: C.install_release(by["v10.0"], vd); check(False, "zip slip не пойман")
except ValueError as e: check("небезопасный" in str(e), "zip slip отклонён")
check(not (tmp / "evil.txt").exists() and not (vd / "evil.txt").exists(), "файл вне папки не создан")
try: C.install_release(by["v10.1"], vd); check(False, "архив без exe")
except ValueError as e: check("нет собранной программы" in str(e), "архив без exe отклонён")
try: C.install_release(by["v7.3"], vd); check(False, "релиз без файла")
except ValueError: check(True, "релиз без файла отклонён")
# отмена
try: C.install_release(by["v8.7"], tmp / "v2", cancel=lambda: True); check(False, "отмена")
except C.Cancelled: check(True, "отмена скачивания")
check(not list((tmp / "v2").glob("*")), "после отмены чисто")

# установленные + слияние
inst = C.installed_versions(vd)
check(set(inst) == {"v8.7", "v8.6"}, f"installed {set(inst)}")
merged = C.merge_versions(rels, inst); check({r.tag for r in merged} >= {"v8.7", "v8.6", "v7.3"}, "слияние")
extra = C.import_local(tmp / "x.exe" if (tmp / "x.exe").write_bytes(b"MZ") else None, vd, "v7.3-old")
check(C.find_exe(extra) and "v7.3-old" in C.installed_versions(vd), "импорт exe")
zp = tmp / "old.zip"; zp.write_bytes(GOOD)
check(C.find_exe(C.import_local(zp, vd, "v5")), "импорт zip")
try: C.import_local(zp, vd, "v5"); check(False, "дубль имени")
except ValueError: check(True, "дубль имени отклонён")
bad = tmp / "bad.zip"; bad.write_bytes(NOEXE)
try: C.import_local(bad, vd, "v4"); check(False, "импорт без exe")
except ValueError: check(not (vd / "v4").exists(), "импорт без exe: папка убрана")
merged = C.merge_versions([], C.installed_versions(vd)); check(all(r.local for r in merged), "локальные помечены")

# удаление
C.remove_version(vd / "v5", vd); check(not (vd / "v5").exists(), "удаление")
try: C.remove_version(tmp, vd); check(False, "удаление вне папки")
except ValueError: check(True, "удалять вне папки версий нельзя")

# оффлайн
srv.shutdown()
try: C.fetch_releases(URL, timeout=2, cache=cache); check(False, "оффлайн без исключения")
except C.OfflineCache as e: check(len(e.releases) >= 4, "оффлайн: список из кэша")
try: C.fetch_releases(URL, timeout=2, cache=tmp / "none.json"); check(False, "оффлайн без кэша")
except Exception as e: check(not isinstance(e, C.OfflineCache), "оффлайн без кэша: обычная ошибка")

# запуск
check(C.build_command(Path("/x/Portabilizer.exe"), True) == ["/x/Portabilizer.exe", "--r"] and C.build_command(Path("/x/P.exe"), False) == ["/x/P.exe"], "команда запуска")
if os.name != "nt":
    sh = tmp / "Portabilizer.exe"; out = tmp / "out.txt"
    sh.write_text(f"#!/bin/sh\necho \"$@|$(pwd)\" > '{out}'\n"); sh.chmod(0o755)
    C.launch(sh, True).wait(); check(out.read_text().strip() == f"--r|{tmp}", f"запуск с --r и cwd: {out.read_text()!r}")
    C.launch(sh, False).wait(); check(out.read_text().strip() == f"|{tmp}", "запуск без --r")
try: C.launch(tmp / "nope.exe"); check(False, "запуск несуществующего")
except FileNotFoundError: check(True, "запуск несуществующего")
print(f"ядро лаунчера: {ok} проверок пройдено")
shutil.rmtree(tmp, ignore_errors=True)
