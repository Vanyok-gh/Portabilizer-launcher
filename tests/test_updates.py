"""Уведомление о новой версии, фильтр тегов, ярлык. Запуск: python tests/test_updates.py"""
import sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pz_core as C, launcher as L
n = 0
def check(c, m):
    global n; assert c, "ПРОВАЛ: " + m; n += 1

tmp = Path(tempfile.mkdtemp())
# теги, не похожие на версию Portabilizer, пропускаются
rels = C.parse_releases([
    {"tag_name": "v8.7", "assets": [{"name": "Portabilizer-v8.7.zip", "browser_download_url": "http://x/a", "size": 5}]},
    {"tag_name": "launcher-v0.2", "assets": [{"name": "Launcher.zip", "browser_download_url": "http://x/l", "size": 5}]},
    {"tag_name": "nightly", "assets": []},
    {"tag_name": "v8.8", "body": "Новое\n- пункт", "assets": [{"name": "Portabilizer-v8.8.zip", "browser_download_url": "http://x/b", "size": 7}]},
    {"tag_name": "v8.9-beta", "prerelease": True, "assets": [{"name": "Portabilizer-v8.9-beta.zip", "browser_download_url": "http://x/c", "size": 7}]},
])
check([r.tag for r in rels] == ["v8.9-beta", "v8.8", "v8.7"], f"фильтр тегов {[r.tag for r in rels]}")

st = {"versions_dir": str(tmp / "v"), "show_beta": True}
m = L.Model(st, cache=tmp / "c.json"); m.releases = rels
check(m.new_version() is None, "ничего не установлено: баннер не нужен")
(tmp / "v" / "v8.7").mkdir(parents=True); (tmp / "v" / "v8.7" / "Portabilizer.exe").write_bytes(b"MZ"); m.scan_installed()
check(m.new_version().tag == "v8.9-beta", "новая Beta видна при show_beta")
st["show_beta"] = False
check(m.new_version().tag == "v8.8", "Beta скрыта: новая стабильная v8.8")
rows = {r["tag"]: r for r in m.rows()}
check(rows["v8.8"]["kind"] == "new" and rows["v8.8"]["state"].startswith("новая"), "строка помечена как новая")
check(rows["v8.7"]["kind"] == "inst", "установленная")
(tmp / "v" / "v8.8").mkdir(); (tmp / "v" / "v8.8" / "Portabilizer.exe").write_bytes(b"MZ"); m.scan_installed()
check(m.new_version() is None, "всё установлено: новых нет")
st["show_beta"] = True; check(m.new_version().tag == "v8.9-beta", "после v8.8 есть ещё Beta")
check("Новое" in m.info("v8.8"), "описание в info")
# ярлык: команда с кавычками и русскими символами
ps = C.shortcut_ps(r"C:\Users\O'Brien\Лаунчер\Portabilizer Launcher.exe", "Portabilizer: Launcher", "--x", r"C:\a b", r"C:\i.ico")
check("O''Brien" in ps and "Лаунчер" in ps and "Portabilizer_ Launcher.lnk" in ps and "GetFolderPath('Desktop')" in ps and "IconLocation" in ps, "скрипт ярлыка")
check("IconLocation" not in C.shortcut_ps("C:\\x.exe", "n"), "без иконки")
import os
if os.name != "nt":
    try: C.create_desktop_shortcut("/x"); check(False, "не Windows")
    except OSError: check(True, "вне Windows ярлык не создаётся")
print(f"обновления и ярлык: {n} проверок пройдено")
