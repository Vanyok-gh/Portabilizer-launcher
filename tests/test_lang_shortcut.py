"""Смена языка и ярлык установленной версии (окно на поддельном tkinter). Запуск: python tests/test_lang_shortcut.py"""
import sys, tempfile
from pathlib import Path
from unittest.mock import MagicMock
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pz_core as C, pz_i18n as I
n = 0
def check(c, m):
    global n; assert c, "ПРОВАЛ: " + m; n += 1

# ярлык: имя и аргументы
check(C.version_shortcut_name("v9.0") == "Portabilizer v9.0" and C.version_shortcut_name("v9.0", True) == "Portabilizer v9.0 R", "имя ярлыка")
ps = C.shortcut_ps("C:/x/Portabilizer.exe", C.version_shortcut_name("v9.0", True), "--r", "C:/x", "C:/x/Portabilizer.exe")
check("Portabilizer v9.0 R.lnk" in ps and "$s.Arguments='--r'" in ps and "IconLocation='C:/x/Portabilizer.exe'" in ps, "команда ярлыка")

import launcher as L
class Var:
    def __init__(self, master=None, value=None): self.v = value; self.cbs = []
    def get(self): return self.v
    def set(self, v):
        self.v = v
        for c in self.cbs: c()
    def trace_add(self, mode, cb): self.cbs.append(lambda: cb())
tk = MagicMock(name="tk"); tk.StringVar = Var; tk.BooleanVar = Var
ttk = MagicMock(name="ttk"); style = MagicMock(); style.theme_use.return_value = "vista"; ttk.Style.return_value = style
rootm = MagicMock(); rootm.cget.return_value = "#f0f0f0"; rootm.geometry.return_value = "1000x640+10+10"; tk.Tk.return_value = rootm
tv = MagicMock(); tv.selection.return_value = (); tv.get_children.return_value = (); ttk.Treeview.return_value = tv
sys.modules.update({"tkinter": tk, "tkinter.ttk": ttk})
tk.ttk = ttk
L.T.save_settings = lambda d, path=None: None
L.T.load_settings = lambda path=None: {}
tmp = Path(tempfile.mkdtemp())
made = []
C.create_version_shortcut = lambda exe, tag, radical=False: made.append((Path(exe).name, tag, radical)) or "desk.lnk"
res = {}

def hook(ctx):
    global n
    st, ui, mb = ctx["settings"], ctx["ui"], tk.messagebox
    m = ctx["model"]
    d = tmp / "v9.0"; d.mkdir(); (d / "Portabilizer.exe").write_bytes(b"MZ")
    m.installed = {"v9.0": d}
    mb.askyesno.return_value = True
    ui["shortcuts"] = False; ctx["offer_version_shortcut"]("v9.0"); check(not made, "не Windows: ярлык не предлагается")
    ui["shortcuts"] = True; ctx["offer_version_shortcut"]("v9.0")
    check(made == [("Portabilizer.exe", "v9.0", False)], f"ярлык после установки {made}")
    mb.askyesno.return_value = False; ctx["offer_version_shortcut"]("v9.0"); check(len(made) == 1, "отказ: ярлыка нет")
    mb.askyesno.return_value = True; st["offer_version_shortcut"] = False; ctx["offer_version_shortcut"]("v9.0")
    check(len(made) == 1, "настройка выключена: не спрашиваем")
    ctx["mode_var"].set("r"); check(ctx["make_version_shortcut"]("v9.0") and made[-1][2] is True, "ярлык режима R")
    check(not ctx["make_version_shortcut"]("v1.0") and len(made) == 2, "нет такой версии - нет ярлыка")
    # язык
    check(I.get_lang() == "ru" and ctx["lang_var"].get() == "ru", "по умолчанию русский")
    ctx["lang_var"].set("en")
    check(st.get("language") == "en" and L.RESTART["flag"] and L.RESTART["geometry"] == "1000x640+10+10", "смена языка: сохранено и перезапуск")
    check(rootm.destroy.called, "окно закрыто для перезапуска")
    res["ok"] = True
L.gui(_hook=hook); check(res.get("ok"), "окно прошло")
I.set_lang("en"); L.RESTART["flag"] = False
r2 = {}
def hook2(ctx):
    check(ctx["lang_var"].get() == "en", "язык en берётся из настроек")
    check(I.tr("Запустить") == "Launch", "tr на английском")
    r2["ok"] = True
L.T.load_settings = lambda path=None: {"language": "fr"}
L.gui(_hook=lambda ctx: (check(I.get_lang() == "fr", "язык fr из настроек"), r2.update(ok=True)))
check(r2.get("ok"), "второй запуск")
I.set_lang("ru")
print(f"язык и ярлык: {n} проверок пройдено")
