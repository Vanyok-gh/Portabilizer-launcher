"""Модель лаунчера и окно (на поддельном tkinter). Запуск: python tests/test_model.py"""
import hashlib, http.server, io, json, os, sys, tempfile, threading, zipfile
from pathlib import Path
from unittest.mock import MagicMock
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

def mkzip(d):
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w") as z:
        for n, x in d.items(): z.writestr(n, x)
    return b.getvalue()
Z87 = mkzip({"Portabilizer.exe": b"MZ87"}); Z86 = mkzip({"Portabilizer.exe": b"MZ86"})
sha = lambda b: hashlib.sha256(b).hexdigest()
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        base = f"http://127.0.0.1:{self.server.server_port}"; p = self.path.split("?")[0]
        if p == "/r":
            body = json.dumps([
                {"tag_name": "v8.7", "name": "8.7", "body": "дубль подсказки убран", "prerelease": False, "published_at": "2026-10-30T10:00:00Z",
                 "assets": [{"name": "Portabilizer-v8.7.zip", "size": len(Z87), "digest": "sha256:" + sha(Z87), "browser_download_url": base + "/z87"}]},
                {"tag_name": "v8.8-beta", "name": "8.8b", "body": "", "prerelease": True,
                 "assets": [{"name": "Portabilizer-v8.8-beta.zip", "size": len(Z86), "digest": "sha256:" + sha(Z86), "browser_download_url": base + "/z86"}]},
                {"tag_name": "v7.3", "name": "7.3", "body": "", "prerelease": False, "assets": []}]).encode()
        elif p == "/z87": body = Z87
        elif p == "/z86": body = Z86
        else: self.send_response(404); self.end_headers(); return
        self.send_response(200); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{srv.server_port}/r"
tmp = Path(tempfile.mkdtemp()); n = 0
def check(c, m):
    global n; assert c, "ПРОВАЛ: " + m; n += 1

import launcher as L
st = {"versions_dir": str(tmp / "v")}
m = L.Model(st, api_url=URL, cache=tmp / "c.json")
check("Версий в GitHub: 3" in m.refresh() and m.online, "refresh")
rows = {r["tag"]: r for r in m.rows()}
check(list(rows) == ["v8.8-beta", "v8.7", "v7.3"], f"порядок {list(rows)}")
check(rows["v8.8-beta"]["title"].endswith("[Beta]") and rows["v8.7"]["kind"] == "avail" and rows["v7.3"]["state"] == "нет файла в релизе", "строки")
check(m.action("v8.7") == ("install", "Установить") and m.action("v7.3")[0] == "none", "действие install/none")
st["show_beta"] = False; check("v8.8-beta" not in [r["tag"] for r in m.rows()], "Beta скрыта"); st["show_beta"] = True
m.install("v8.7", log=lambda s: None)
check(m.action("v8.7") == ("launch", "Запустить") and m.installed["v8.7"].name == "v8.7", "после установки")
st["show_beta"] = False; m.install("v8.8-beta") if False else None
check("установлена" in {r["tag"]: r for r in m.rows()}["v8.7"]["state"], "статус установлена")
m.import_file(Path(__file__), "x") if False else None
(tmp / "o.exe").write_bytes(b"MZ"); m.import_file(tmp / "o.exe", "v7.3")
r73 = {r["tag"]: r for r in m.rows()}["v7.3"]
check(r73["kind"] == "inst" and m.action("v7.3")[0] == "launch", "ручная версия v7.3 стала установленной")
(tmp / "o2.exe").write_bytes(b"MZ"); m.import_file(tmp / "o2.exe", "v5")
check({r["tag"]: r for r in m.rows()}["v5"]["state"] == "установлена (своя)", "ручная версия помечена как своя")
info = m.info("v8.7"); check("дубль подсказки убран" in info and "SHA-256" in info and "Установлена" in info, "info")
if os.name != "nt":
    exe = m.exe_of("v8.7"); out = tmp / "o.txt"
    exe.write_text(f"#!/bin/sh\necho \"$@\" > '{out}'\n"); exe.chmod(0o755)
    m.launch("v8.7", True).wait(); check(out.read_text().strip() == "--r", "запуск R")
    m.launch("v8.7", False).wait(); check(out.read_text().strip() == "", "запуск обычный")
try: m.launch("v9", False); check(False, "запуск не установленной")
except FileNotFoundError: check(True, "не установленную не запустить")
m.remove("v8.7"); check("v8.7" not in m.installed and m.action("v8.7")[0] == "install", "удаление")
# --- перевод «Что нового» по языку интерфейса
import pz_core as C2
from pz_i18n import set_lang as _sl
_EN = "# x\n\n## v8.7\n\n- duplicate hint removed\n"
class _R:
    def __init__(s, b): s.b = b
    def read(s): return s.b
    def __enter__(s): return s
    def __exit__(s, *a): return False
def _op(req, timeout=0):
    u = req.full_url
    if u.endswith("/en.md"): return _R(_EN.encode())
    raise OSError("нет файла")
mm = L.Model({"versions_dir": str(tmp / "v2")}, api_url=URL, cache=tmp / "c2.json"); mm.news_opener = _op
_sl("en"); mm.refresh(); r87 = mm.get("v8.7")
check("duplicate hint removed" in mm.info("v8.7") and "дубль" not in mm.info("v8.7"), "английское описание при языке en")
_sl("de"); check("duplicate hint removed" in mm.info("v8.7"), "для языка без перевода берётся английский")
check(mm.notes_for(mm.get("v8.8-beta")) == "", "нет перевода и пустое описание -> пусто")
_sl("ru"); check("дубль подсказки убран" in mm.info("v8.7"), "русский язык: текст релиза")
mm2 = L.Model({"versions_dir": str(tmp / "v3")}, api_url=URL, cache=tmp / "c3.json"); mm2.news_opener = lambda *a, **k: (_ for _ in ()).throw(OSError("offline"))
_sl("en"); mm2.refresh(); check("дубль подсказки убран" in mm2.info("v8.7"), "нет связи с переводами -> русский текст")
_sl("ru")
check(C2.fetch_news("../x", opener=_op) == {} and C2.fetch_news("en", opener=_op).get("8.7"), "fetch_news: имя языка проверяется, разбор разделов")
print("перевод описаний:", "ок")
srv.shutdown()
m2 = L.Model(st, api_url=URL, cache=tmp / "c.json"); check("сохранённый список" in m2.refresh() and not m2.online and len(m2.releases) == 3, "оффлайн: кэш")
m3 = L.Model(st, api_url=URL, cache=tmp / "none.json"); check("Не удалось" in m3.refresh() and {"v7.3", "v5"} <= {r["tag"] for r in m3.rows()}, "оффлайн без кэша: показаны установленные")

# ---- окно на поддельном tkinter
class Var:
    def __init__(self, master=None, value=None): self.v = value; self.cbs = []
    def get(self): return self.v
    def set(self, v):
        self.v = v
        for c in self.cbs: c()
    def trace_add(self, mode, cb): self.cbs.append(lambda: cb())
tk = MagicMock(name="tk"); tk.StringVar = Var; tk.BooleanVar = Var
ttk = MagicMock(name="ttk"); style = MagicMock(); style.theme_use.return_value = "vista"; ttk.Style.return_value = style
rootm = MagicMock(); rootm.cget.return_value = "#f0f0f0"; tk.Tk.return_value = rootm
tv = MagicMock(); sel = {"v": ()}
tv.selection.side_effect = lambda: sel["v"]; tv.get_children.return_value = ()
ttk.Treeview.return_value = tv
sys.modules.update({"tkinter": tk, "tkinter.ttk": ttk, "tkinter.filedialog": MagicMock(), "tkinter.messagebox": MagicMock(), "tkinter.colorchooser": MagicMock(), "tkinter.simpledialog": MagicMock()})
tk.ttk = ttk
import pz_theme as T
T.save_settings = lambda d, path=None: None
L.T.save_settings = lambda d, path=None: None
res = {}
def hook(ctx):
    for ap in ("auto", "light", "dark", "classic"):
        for mode in ("normal", "r"):
            ctx["settings"].clear(); ctx["settings"].update(appearance=ap)
            ctx["mode_var"].set(mode)
            t = ctx["theme_cur"]["theme"]
            check((ap == "classic") == (t is None), f"тема {ap}/{mode}")
            if t: check(t["r"] == (mode == "r"), f"красная тема только в R: {ap}/{mode}")
    ctx["q"].put(("log", "x\n")); ctx["pump"]()
    res["ok"] = True
L.gui(_hook=hook); check(res.get("ok"), "окно: все темы и режимы")
print(f"лаунчер (модель и окно): {n} проверок пройдено")
