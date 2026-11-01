"""Portabilizer Launcher - список версий Portabilizer: установка, запуск (обычный и R), папки.

Слева версии, справа настройки лаунчера, менеджер версий, оформление, журнал.
Версии берутся из GitHub Releases (см. README). Логика (класс Model) не зависит от окна.
"""
import json
import os
import queue
import sys
import threading
import time
import webbrowser
from pathlib import Path

import pz_core as C
import pz_icons
import pz_theme as T
from pz_i18n import LANGS, detect_lang, get_lang, set_lang, tr

VERSION = "0.4"
REPO_URL = f"https://github.com/{C.OWNER}/{C.REPO}"
DEFAULTS = {"show_beta": True, "close_after_launch": False, "mode": "normal", "last_tag": "",
            "versions_dir": "", "versions_repo": "", "offer_version_shortcut": True}
RESTART = {"flag": False, "geometry": ""}            # смена языка перезапускает окно (см. run)


def init_language(settings: dict):
    """Выбирает язык: из настроек; при первом запуске собранного exe - язык системы, иначе русский."""
    lang = settings.get("language")
    if not lang:
        lang = detect_lang() if getattr(sys, "frozen", False) else "ru"
    return set_lang(lang)


class Model:
    """Состояние лаунчера без графики: список версий, действия, установка, запуск."""

    def __init__(self, settings: dict, api_url=None, opener=None, cache=None):
        self.settings = settings
        for k, v in DEFAULTS.items():
            self.settings.setdefault(k, v)
        self.api_url, self.opener = api_url, opener
        self.cache = cache if cache is not None else C.app_dir() / "releases_cache.json"
        self.releases = []
        self.launcher_new = None            # новая версия самого лаунчера (dict) или None
        self.installed = {}
        self.online = False
        self.status = ""

    @property
    def versions_dir(self) -> Path:
        return Path(self.settings.get("versions_dir") or (C.app_dir() / "versions"))

    # --- обновление списка
    def scan_installed(self):
        self.installed = C.installed_versions(self.versions_dir)

    def refresh(self) -> str:
        """Запрашивает релизы (с запасным кэшем) и сканирует диск. Возвращает текст статуса."""
        try:
            url = self.api_url or C.versions_api_url(self.settings)
            self.releases = C.fetch_releases(url, opener=self.opener, cache=self.cache)
            self.online = True
            if any(C.notes_empty(r.notes) for r in self.releases):
                try:
                    owner, repo = url.split("/repos/")[1].split("/")[:2]
                    C.fill_notes_from_changelog(self.releases,
                                                C.fetch_changelog(owner, repo, opener=self.opener))
                except (IndexError, ValueError):
                    pass                                   # нестандартный адрес (тесты): описание не подставляем
            self.status = tr("Версий в GitHub: {n}.", n=len(self.releases))
        except C.OfflineCache as e:
            self.releases, self.online = e.releases, False
            self.status = tr("Нет связи с GitHub: показан последний сохранённый список.")
        except Exception as e:                              # noqa: BLE001
            self.releases, self.online = [], False
            self.status = tr("Не удалось получить список версий ({e}). Показаны установленные.", e=e)
        self.scan_installed()
        self.launcher_new = C.check_launcher_update(VERSION, opener=self.opener) if self.online else None
        return self.status

    # --- список для окна
    def items(self) -> list:
        res = []
        for r in C.merge_versions(self.releases, self.installed):
            inst = r.tag in self.installed
            if r.prerelease and not inst and not self.settings.get("show_beta", True):
                continue
            res.append(r)
        return res

    def rows(self) -> list:
        out = []
        for r in self.items():
            inst = r.tag in self.installed
            if inst:
                state, kind = (tr("установлена (своя)") if r.local else tr("установлена")), "inst"
            elif r.available:
                newer = bool(self.installed) and C.parse_version(r.tag) > self.newest_installed()
                state = (tr("новая, можно установить") if newer else tr("можно установить")) + \
                        f" ({C.fmt_size(r.asset_size)})"
                kind = "new" if newer else "avail"
            else:
                state, kind = tr("нет файла в релизе"), "local"
            out.append({"tag": r.tag, "title": r.tag + (" [Beta]" if r.prerelease else ""),
                        "state": state, "kind": kind})
        return out

    def newest_installed(self) -> tuple:
        return max((C.parse_version(t) for t in self.installed), default=())

    def new_version(self):
        """Самый новый релиз, который новее всех установленных (или None). Beta - по настройке."""
        if not self.installed:
            return None
        top = self.newest_installed()
        for r in self.items():                           # items() отсортирован: новые первыми
            if r.available and r.tag not in self.installed and C.parse_version(r.tag) > top:
                return r
        return None

    def get(self, tag):
        for r in self.items():
            if r.tag == tag:
                return r
        return None

    def action(self, tag) -> tuple:
        """('launch'|'install'|'none', подпись кнопки) для выбранной версии."""
        r = self.get(tag)
        if r is None:
            return "none", tr("Запустить")
        if tag in self.installed:
            return "launch", tr("Запустить")
        if r.available:
            return "install", tr("Установить")
        return "none", tr("Недоступна")

    # --- действия
    def install(self, tag, progress=None, cancel=None, log=None) -> Path:
        r = self.get(tag)
        if r is None:
            raise ValueError(tr("версия не найдена"))
        path = C.install_release(r, self.versions_dir, progress, cancel, log, self.opener)
        self.scan_installed()
        return path

    def exe_of(self, tag):
        d = self.installed.get(tag)
        return C.find_exe(d) if d else None

    def launch(self, tag, radical: bool):
        exe = self.exe_of(tag)
        if not exe:
            raise FileNotFoundError(tr("версия {tag} не установлена", tag=tag))
        return C.launch(exe, radical)

    def remove(self, tag):
        d = self.installed.get(tag)
        if not d:
            raise ValueError(tr("версия не установлена"))
        C.remove_version(d, self.versions_dir)
        self.scan_installed()

    def import_file(self, path, name="") -> Path:
        p = C.import_local(path, self.versions_dir, name)
        self.scan_installed()
        return p

    def folder_of(self, tag) -> Path:
        return self.installed.get(tag) or self.versions_dir

    def disk_size(self, tag) -> int:
        d = self.installed.get(tag)
        total = 0
        if d:
            for p in Path(d).rglob("*"):
                try:
                    if p.is_file():
                        total += p.stat().st_size
                except OSError:
                    pass
        return total

    def info(self, tag) -> str:
        r = self.get(tag)
        if r is None:
            return tr("Версия не найдена.")
        lines = [tr("Версия: {tag}", tag=r.tag), tr("Канал: {ch}", ch=r.channel)]
        if r.published:
            lines.append(tr("Дата выпуска: {d}", d=r.published))
        if r.asset_name:
            lines.append(tr("Файл: {name} ({size})", name=r.asset_name, size=C.fmt_size(r.asset_size)))
        if r.sha256:
            lines.append(f"SHA-256: {r.sha256}")
        if tag in self.installed:
            lines.append(tr("Установлена: {path} ({size})", path=self.installed[tag],
                            size=C.fmt_size(self.disk_size(tag))))
        elif r.local:
            lines.append(tr("Есть только на диске (не из GitHub)."))
        lines += ["", tr("Что нового:"), (r.notes or tr("Описание не указано.")).strip()]
        return "\n".join(lines)


# ------------------------------------------------------------------ окно

def gui(_hook=None):
    import tkinter as tk
    from tkinter import colorchooser, filedialog, messagebox, ttk

    root = tk.Tk()
    root.title(f"Portabilizer Launcher {VERSION}")
    root.geometry(RESTART["geometry"] or "1080x640")
    root.minsize(1000, 560)

    settings = T.load_settings()
    init_language(settings)
    themes = T.load_themes()
    model = Model(settings)
    style = ttk.Style(root)
    native_theme = style.theme_use()
    default_bg = root.cget("bg")
    q = queue.Queue()
    ui = {"busy": False, "cancel": False, "theme": None, "dark_sys": None, "shortcuts": os.name == "nt"}
    mode_var = tk.StringVar(value="r" if settings.get("mode") == "r" else "normal")
    status_var = tk.StringVar(value=tr("Загружаю список версий..."))

    def save():
        T.save_settings(settings)

    def log(msg):
        stamp = time.strftime("%H:%M:%S")
        q.put(("log", f"[{stamp}] {msg}\n"))

    def bg(fn, done):
        """Выполняет fn в потоке, результат (или ошибку) отдаёт done в главном потоке."""
        def work():
            try:
                res, err = fn(), None
            except Exception as e:                           # noqa: BLE001
                res, err = None, e
            q.put(("done", (done, res, err)))
        threading.Thread(target=work, daemon=True).start()

    # ------------------------------------------------------------ левая панель
    left = ttk.Frame(root, padding=10)
    left.pack(side="left", fill="y")
    ttk.Label(left, text=tr("Версии Portabilizer")).pack(anchor="w")
    tv = ttk.Treeview(left, columns=("tag", "state"), show="headings", selectmode="browse", height=14)
    tv.heading("tag", text=tr("Версия"))
    tv.heading("state", text=tr("Состояние"))
    tv.column("tag", width=110, anchor="w")
    tv.column("state", width=190, anchor="w")
    tv.pack(fill="both", expand=True, pady=(4, 8))

    modef = ttk.Frame(left)
    modef.pack(fill="x")
    ttk.Radiobutton(modef, text=tr("Обычный режим"), value="normal", variable=mode_var).pack(anchor="w")
    ttk.Radiobutton(modef, text=tr("Режим R (радикальный)"), value="r", variable=mode_var).pack(anchor="w")
    r_hint = ttk.Label(left, style="Danger.TLabel", wraplength=300,
                       text=tr("R: после успешной сборки исходный файл удаляется. Программа "
                                   "попросит подтверждение."))
    banner_var = tk.StringVar()
    banner = ttk.Label(left, textvariable=banner_var, style="Accent.TLabel", wraplength=300)
    btn_main = ttk.Button(left, text=tr("Запустить"), style="Big.Accent.TButton")
    btn_main.pack(fill="x", pady=(10, 6))
    pb = ttk.Progressbar(left, mode="determinate", maximum=100)
    btn_cancel = ttk.Button(left, text=tr("Отмена"))
    row = ttk.Frame(left)
    row.pack(fill="x")
    btn_info = ttk.Button(row, text=tr("Инфо"), width=7)
    btn_dir = ttk.Button(row, text=tr("Папка"), width=8)
    btn_ref = ttk.Button(row, text=tr("Обновить"), width=11)
    btn_menu = ttk.Button(row, text="≡", width=3)
    for b in (btn_info, btn_dir, btn_ref, btn_menu):
        b.pack(side="left", expand=True, fill="x", padx=2)
    ttk.Label(left, textvariable=status_var, style="Muted.TLabel", wraplength=300).pack(
        anchor="w", pady=(8, 0))

    # ------------------------------------------------------------ правая панель
    nb = ttk.Notebook(root)
    nb.pack(side="right", fill="both", expand=True, padx=(0, 10), pady=10)
    tab_news, tab_set, tab_vers, tab_look, tab_lang, tab_log, tab_about = (ttk.Frame(nb) for _ in range(7))
    for tab, title in ((tab_news, "Что нового"), (tab_set, "Лаунчер"), (tab_vers, "Менеджер версий"),
                       (tab_look, "Оформление"), (tab_lang, "Язык"), (tab_log, "Журнал"),
                       (tab_about, "О программе")):
        nb.add(tab, text=tr(title))

    # --- Что нового: описание выбранной версии
    tab_news.grid_columnconfigure(0, weight=1)
    tab_news.grid_rowconfigure(0, weight=1)
    news = tk.Text(tab_news, state="disabled", wrap="word", relief="flat")
    news.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)
    nsb = ttk.Scrollbar(tab_news, command=news.yview)
    nsb.grid(row=0, column=1, sticky="ns", pady=10, padx=(0, 10))
    news.config(yscrollcommand=nsb.set)

    # --- Лаунчер: настройки
    tab_set.grid_columnconfigure(1, weight=1)
    ttk.Label(tab_set, text=tr("Папка версий:")).grid(row=0, column=0, sticky="w", padx=12, pady=(14, 6))
    dir_var = tk.StringVar(value=str(model.versions_dir))
    dir_entry = ttk.Entry(tab_set, textvariable=dir_var)
    dir_entry.grid(row=0, column=1, sticky="ew", padx=4, pady=(14, 6))
    beta_var = tk.BooleanVar(value=bool(settings.get("show_beta", True)))
    close_var = tk.BooleanVar(value=bool(settings.get("close_after_launch", False)))
    offer_var = tk.BooleanVar(value=bool(settings.get("offer_version_shortcut", True)))
    ttk.Checkbutton(tab_set, text=tr("Показывать пробные версии (Beta)"), variable=beta_var).grid(
        row=1, column=0, columnspan=3, sticky="w", padx=12, pady=4)
    ttk.Checkbutton(tab_set, text=tr("Закрывать лаунчер после запуска версии"), variable=close_var).grid(
        row=2, column=0, columnspan=3, sticky="w", padx=12, pady=4)
    ttk.Checkbutton(tab_set, text=tr("Предлагать ярлык на рабочем столе после установки версии"),
                    variable=offer_var).grid(row=3, column=0, columnspan=3, sticky="w", padx=12, pady=4)
    ttk.Label(tab_set, style="Muted.TLabel", wraplength=560, text=tr(
        "Источник версий: {url}. Новые версии появляются в списке после «Обновить». "
        "Версии, добавленные вручную, остаются в папке версий и в списке.", url=REPO_URL)).grid(
        row=4, column=0, columnspan=3, sticky="w", padx=12, pady=(10, 4))

    # --- Менеджер версий
    tab_vers.grid_columnconfigure(0, weight=1)
    tab_vers.grid_rowconfigure(0, weight=1)
    mv = ttk.Treeview(tab_vers, columns=("tag", "size", "path"), show="headings", selectmode="browse")
    for c, t, w in (("tag", tr("Версия"), 110), ("size", tr("Размер"), 90), ("path", tr("Папка"), 380)):
        mv.heading(c, text=t)
        mv.column(c, width=w, anchor="w")
    mv.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)
    mbar = ttk.Frame(tab_vers)
    mbar.grid(row=1, column=0, columnspan=4, sticky="w", padx=10, pady=(0, 10))
    btn_m_open = ttk.Button(mbar, text=tr("Открыть папку"))
    btn_m_del = ttk.Button(mbar, text=tr("Удалить версию"))
    btn_m_add = ttk.Button(mbar, text=tr("Добавить свою версию (zip или exe)..."))
    for b in (btn_m_open, btn_m_del, btn_m_add):
        b.pack(side="left", padx=(0, 8))

    # --- Журнал
    tab_log.grid_columnconfigure(0, weight=1)
    tab_log.grid_rowconfigure(0, weight=1)
    logbox = tk.Text(tab_log, state="disabled", wrap="word")
    logbox.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)
    lsb = ttk.Scrollbar(tab_log, command=logbox.yview)
    lsb.grid(row=0, column=1, sticky="ns", pady=10, padx=(0, 10))
    logbox.config(yscrollcommand=lsb.set)
    text_defaults = {k: logbox.cget(k) for k in ("bg", "fg", "insertbackground", "selectbackground",
                                                 "selectforeground", "highlightthickness",
                                                 "highlightbackground", "highlightcolor")}

    # --- О программе
    ttk.Label(tab_about, wraplength=560, justify="left", text=(
        f"Portabilizer Launcher {VERSION}\n\n"
        + tr("Устанавливает и запускает версии Portabilizer: обычный режим и режим R в одной версии. "
             "Каждая версия лежит в своей папке и не мешает другим. Контрольная сумма скачанного "
             "файла проверяется перед установкой.")
        + "\n\n" + tr("Репозиторий: {url}", url=REPO_URL))).pack(anchor="w", padx=14, pady=14)
    ttk.Button(tab_about, text=tr("Открыть репозиторий"),
               command=lambda: webbrowser.open(REPO_URL)).pack(anchor="w", padx=14)

    # ------------------------------------------------------------ оформление
    cur = {"theme": None}
    combos = []
    icon_refs = {}

    def set_icon(classic):
        try:                                   # «Классическая» тема - пиксельная иконка, иначе гладкая
            key = "pixel" if classic else "smooth"
            imgs = [tk.PhotoImage(data=pz_icons.ICONS[f"{key}{n}"]) for n in (64, 32)]
            icon_refs["imgs"] = imgs
            root.iconphoto(True, *imgs)
        except Exception:
            pass

    def apply_theme():
        t = T.pick_theme(settings, mode_var.get() == "r", themes)
        cur["theme"], ui["dark_sys"] = t, T.system_prefers_dark()
        if t is None:
            style.theme_use(native_theme)
            c = dict(T.CLASSIC)
            for nm, key in (("Muted.TLabel", "muted"), ("Warn.TLabel", "warn"),
                            ("Danger.TLabel", "danger")):
                style.configure(nm, foreground=c[key])
            style.configure("Big.Accent.TButton", font=("Segoe UI", 12, "bold"), padding=(12, 8))
            style.configure("Accent.TLabel", foreground="#0b5cd5", font=("Segoe UI", 9, "bold"))
            root.configure(bg=default_bg)
            try:
                menu.configure(**menu_defaults)
            except tk.TclError:
                pass
            tcfg = dict(text_defaults)
        else:
            style.theme_use("clam")
            for nm, conf, mp in T.ttk_style_spec(t):
                style.configure(nm, **conf)
                if mp:
                    style.map(nm, **mp)
            style.configure("Big.Accent.TButton", font=("Segoe UI", 12, "bold"), padding=(12, 9))
            style.configure("Accent.TLabel", foreground=t["accent"] if T.contrast(t["accent"], t["bg"]) >= 4.5
                            else t["fg"], font=("Segoe UI", 9, "bold"))
            c = t
            root.configure(bg=t["bg"])
            tcfg = dict(bg=t["surface"], fg=t["fg"], insertbackground=t["fg"],
                        selectbackground=t["sel_bg"], selectforeground=t["sel_fg"],
                        highlightthickness=1, highlightbackground=t["border"],
                        highlightcolor=t["accent"])
            root.option_add("*TCombobox*Listbox.background", t["surface"])
            root.option_add("*TCombobox*Listbox.foreground", t["fg"])
            root.option_add("*TCombobox*Listbox.selectBackground", t["sel_bg"])
            root.option_add("*TCombobox*Listbox.selectForeground", t["sel_fg"])
            root.option_add("*Toplevel.background", t["bg"])
            try:
                menu.configure(bg=t["surface"], fg=t["fg"], activebackground=t["sel_bg"],
                               activeforeground=t["sel_fg"], relief="flat")
            except tk.TclError:
                pass
        logbox.configure(**tcfg)
        news.configure(**tcfg)
        for tag, key in (("inst", "ok"), ("avail", "fg"), ("new", "warn"), ("local", "muted")):
            tv.tag_configure(tag, foreground=c[key])
        T.set_dark_titlebar(root, bool(t) and t["kind"] == "dark")
        set_icon(t is None)
        set_lang_icon(t is None)
        draw_swatches(t)
        if mode_var.get() == "r":
            r_hint.pack(anchor="w", pady=(6, 0), after=modef)
        else:
            r_hint.pack_forget()

    tab_look.grid_columnconfigure(1, weight=1)
    ttk.Label(tab_look, wraplength=560, text=tr(
        "Внешний вид окна. Изменения применяются сразу. Режим R включает красную тему.")).grid(
        row=0, column=0, columnspan=3, sticky="w", padx=12, pady=(12, 10))
    ap_var, dr_var, lr_var = tk.StringVar(), tk.StringVar(), tk.StringVar()

    def ap_choices():
        d = dict((tr(v), k) for k, v in T.APPEARANCES.items())
        for tid, t in themes.items():
            if not t.get("r") and t.get("user"):
                d[tr(t["name"]) + tr(" (своя)")] = tid
        return d

    def r_choices(kind):
        return {tr(t["name"]) + (tr(" (своя)") if t.get("user") else ""): tid for tid, t in themes.items()
                if t.get("r") and t["kind"] == kind}

    def sync_look_vars():
        ac = ap_choices()
        ap_var.set(next((n for n, k in ac.items() if k == settings.get("appearance", "auto")),
                        tr(T.APPEARANCES["auto"])))
        for var, kind, key, dflt in ((dr_var, "dark", "dark_r", "dark_r_charcoal"),
                                     (lr_var, "light", "light_r", "light_r")):
            ch = r_choices(kind)
            var.set(next((n for n, k in ch.items() if k == settings.get(key, dflt)),
                         next(iter(ch), "")))

    look_combos = []
    for i, (lab, var, getter) in enumerate(((tr("Тема:"), ap_var, ap_choices),
                                            (tr("Тёмная красная (R):"), dr_var, lambda: r_choices("dark")),
                                            (tr("Светлая красная (R):"), lr_var, lambda: r_choices("light"))),
                                           start=1):
        ttk.Label(tab_look, text=lab).grid(row=i, column=0, sticky="w", padx=12, pady=6)
        cb = ttk.Combobox(tab_look, textvariable=var, state="readonly", width=38, values=list(getter()))
        cb.grid(row=i, column=1, sticky="w", padx=4)
        look_combos.append((cb, var, getter))
        combos.append(cb)

    def on_look_change(_e=None):
        settings["appearance"] = ap_choices().get(ap_var.get(), "auto")
        settings["dark_r"] = r_choices("dark").get(dr_var.get(), "dark_r_charcoal")
        settings["light_r"] = r_choices("light").get(lr_var.get(), "light_r")
        save()
        apply_theme()

    for cb, _v, _g in look_combos:
        cb.bind("<<ComboboxSelected>>", on_look_change)

    sw_frame = ttk.Frame(tab_look)
    sw_frame.grid(row=4, column=0, columnspan=3, sticky="w", padx=12, pady=(14, 6))
    sw_cap = ttk.Label(tab_look, style="Muted.TLabel", wraplength=560)
    sw_cap.grid(row=5, column=0, columnspan=3, sticky="w", padx=12)

    def draw_swatches(t):
        for w in sw_frame.winfo_children():
            w.destroy()
        if t is None:
            sw_cap.config(text=tr("Классический вид: цвета задаёт Windows."))
            return
        for role in ("bg", "surface", "surface2", "fg", "muted", "accent", "ok", "warn", "danger"):
            tk.Frame(sw_frame, width=34, height=22, bg=t[role], highlightthickness=1,
                     highlightbackground=t["border"]).pack(side="left", padx=2)
        sw_cap.config(text=tr("Сейчас: {name}", name=tr(t["name"])))

    def reload_themes():
        themes.clear()
        themes.update(T.load_themes())
        for cb, var, getter in look_combos:
            cb.config(values=list(getter()))
        sync_look_vars()

    def pick_my_color():
        base = cur["theme"] or themes["light"]
        res = colorchooser.askcolor(color=base["accent"], title=tr("Главный цвет"), parent=root)
        if not res or not res[1]:
            return
        tint = res[1] if messagebox.askyesno(
            tr("Свой цвет"), tr("Подкрасить в этот цвет и фон окна?\n\nНет - фон останется нейтральным."),
            parent=root) else "#808080"
        try:
            t = T.make_theme_from_color(res[1], base["kind"], bg_tint=tint, name="Мой цвет")
            d = C.app_dir() / "themes"
            d.mkdir(exist_ok=True)
            (d / "my_color.json").write_text(json.dumps(t, ensure_ascii=False, indent=2),
                                             encoding="utf-8")
        except (ValueError, OSError) as e:
            messagebox.showwarning(tr("Свой цвет"), str(e), parent=root)
            return
        reload_themes()
        settings["appearance"] = "my_color"
        save()
        sync_look_vars()
        apply_theme()

    ttk.Button(tab_look, text=tr("Выбрать свой цвет..."), style="Accent.TButton",
               command=pick_my_color).grid(row=6, column=0, columnspan=2, sticky="w", padx=12,
                                           pady=(14, 4))
    sync_look_vars()

    # --- Язык
    lang_var = tk.StringVar(value=get_lang())
    ttk.Label(tab_lang, text=tr("Язык интерфейса:")).pack(anchor="w", padx=12, pady=(14, 6))
    for code, name in LANGS:
        ttk.Radiobutton(tab_lang, text=name, value=code, variable=lang_var).pack(anchor="w", padx=24, pady=2)
    ttk.Label(tab_lang, style="Muted.TLabel", wraplength=560, text=tr(
        "Язык меняется сразу: окно перезапустится само, версии и настройки сохранятся.")).pack(
        anchor="w", padx=12, pady=(12, 0))

    def change_language(*_a):
        code = lang_var.get()
        if code == get_lang():
            return
        if ui["busy"] and not messagebox.askyesno(tr("Идёт установка"), tr("Прервать установку и выйти?"),
                                                  icon="warning", parent=root):
            lang_var.set(get_lang())
            return
        settings["language"] = code
        save()
        RESTART.update(flag=True, geometry=root.geometry())
        ui["cancel"] = True
        root.destroy()

    lang_var.trace_add("write", change_language)

    def set_lang_icon(classic):
        try:
            img = tk.PhotoImage(data=pz_icons.GLOBE["pixel" if classic else "smooth"])
            icon_refs["globe"] = img
            nb.tab(tab_lang, image=img, compound="left")
        except Exception:                                  # noqa: BLE001
            pass

    # ------------------------------------------------------------ логика окна
    def selected_tag():
        sel = tv.selection()
        return sel[0] if sel else ""

    def fill_list(keep=None):
        keep = keep or selected_tag() or settings.get("last_tag", "")
        tv.delete(*tv.get_children())
        for r in model.rows():
            tv.insert("", "end", iid=r["tag"], values=(r["title"], r["state"]), tags=(r["kind"],))
        ids = tv.get_children()
        if keep and keep in ids:
            tv.selection_set(keep)
        elif ids:
            tv.selection_set(ids[0])
        fill_manager()
        update_buttons()

    def fill_manager():
        mv.delete(*mv.get_children())
        for tag, d in model.installed.items():
            mv.insert("", "end", iid=tag, values=(tag, C.fmt_size(model.disk_size(tag)), str(d)))

    def update_buttons(_e=None):
        tag = selected_tag()
        kind, label = model.action(tag) if tag else ("none", tr("Запустить"))
        if ui["busy"]:
            return
        btn_main.config(text=label)
        btn_main.state(["!disabled"] if kind != "none" else ["disabled"])
        for b in (btn_info,):
            b.state(["!disabled"] if tag else ["disabled"])
        btn_dir.state(["!disabled"])
        news.config(state="normal")
        news.delete("1.0", "end")
        news.insert("end", model.info(tag) if tag else tr("Выберите версию в списке слева."))
        news.config(state="disabled")
        if tag:
            settings["last_tag"] = tag

    def set_busy(on):
        ui["busy"] = on
        if on:
            pb.pack(fill="x", before=row, pady=(0, 6))
            btn_cancel.pack(fill="x", before=row, pady=(0, 6))
            btn_main.state(["disabled"])
        else:
            pb.pack_forget()
            btn_cancel.pack_forget()
            pb["value"] = 0
        tv.state(["disabled"] if on else ["!disabled"])

    def check_new(startup=False):
        ln = model.launcher_new
        if ln and startup and settings.get("notified_launcher") != ln["tag"]:
            settings["notified_launcher"] = ln["tag"]
            save()
            if messagebox.askyesno(tr("Новая версия лаунчера"),
                                   tr("Вышел новый Portabilizer Launcher {v} (у вас {cur}).\n\nОткрыть страницу загрузки?",
                                      v=ln["version"], cur=VERSION), parent=root):
                webbrowser.open(ln["url"] or REPO_URL + "/releases")
        r = model.new_version()
        if r is None:
            if ln:
                banner_var.set(tr("Вышел новый лаунчер {v}: {url}", v=ln["version"], url=f"{REPO_URL}/releases"))
                banner.pack(anchor="w", before=btn_main, pady=(8, 0))
            else:
                banner.pack_forget()
            return
        banner_var.set(tr("Доступна новая версия: {tag}. Выберите её и нажмите «Установить».", tag=r.tag)
                       + (tr("\nИ новый лаунчер {v}.", v=ln["version"]) if ln else ""))
        banner.pack(anchor="w", before=btn_main, pady=(8, 0))
        if startup and settings.get("notified_tag") != r.tag:
            settings["notified_tag"] = r.tag
            save()
            first = (r.notes or "").strip().splitlines()[:6]
            if messagebox.askyesno(tr("Новая версия Portabilizer"),
                                   tr("Вышла новая версия: {tag}.\n\n{notes}\n\nУстановить сейчас?",
                                      tag=r.tag, notes="\n".join(first)), parent=root):
                fill_list(r.tag)
                do_install(r.tag)

    def after_refresh(res, err, startup=False):
        status_var.set(res if res else tr("Ошибка: {e}", e=err))
        log(res or str(err))
        fill_list()
        check_new(startup)

    def do_refresh(_e=None, startup=False):
        if ui["busy"]:
            return
        status_var.set(tr("Проверяю версии в GitHub..."))
        bg(model.refresh, lambda res, err: after_refresh(res, err, startup))

    def do_install(tag):
        ui["cancel"] = False
        set_busy(True)
        status_var.set(tr("Устанавливаю {tag}...", tag=tag))

        def progress(got, total):
            q.put(("progress", (got, total)))

        def finished(res, err):
            set_busy(False)
            if err is None:
                status_var.set(tr("Версия {tag} установлена.", tag=tag))
                fill_list(tag)
                check_new()
                offer_version_shortcut(tag)
            elif isinstance(err, C.Cancelled):
                status_var.set(tr("Установка отменена."))
                update_buttons()
            else:
                status_var.set(tr("Не удалось установить версию."))
                log(tr("Ошибка установки {tag}: {err}", tag=tag, err=err))
                messagebox.showerror(tr("Установка"), tr("Не удалось установить {tag}:\n\n{err}", tag=tag, err=err),
                                     parent=root)
                update_buttons()

        bg(lambda: model.install(tag, progress, lambda: ui["cancel"], log), finished)

    def do_main(_e=None):
        tag = selected_tag()
        if not tag or ui["busy"]:
            return
        kind, _label = model.action(tag)
        if kind == "install":
            do_install(tag)
        elif kind == "launch":
            radical = mode_var.get() == "r"
            try:
                model.launch(tag, radical)
            except (OSError, ValueError) as e:
                messagebox.showerror(tr("Запуск"), tr("Не удалось запустить {tag}:\n\n{e}", tag=tag, e=e), parent=root)
                return
            log(tr("Запущена версия {tag}", tag=tag) + (tr(" (режим R)") if radical else "") + ".")
            status_var.set(tr("Запущено: {tag}", tag=tag) + (" (R)" if radical else ""))
            if settings.get("close_after_launch"):
                root.after(600, root.destroy)

    def open_folder(path):
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            if os.name == "nt":
                os.startfile(str(path))      # noqa
            else:
                webbrowser.open(Path(path).as_uri())
        except OSError as e:
            messagebox.showwarning(tr("Папка"), tr("Не удалось открыть: {e}", e=e), parent=root)

    def do_dir(_e=None):
        tag = selected_tag()
        open_folder(model.folder_of(tag) if tag in model.installed else model.versions_dir)

    def do_info(_e=None):
        tag = selected_tag()
        if not tag:
            return
        win = tk.Toplevel(root)
        win.title(tr("Версия {tag}", tag=tag))
        win.geometry("560x420")
        txt = tk.Text(win, wrap="word")
        txt.pack(fill="both", expand=True, padx=10, pady=10)
        txt.insert("end", model.info(tag))
        txt.config(state="disabled")
        t = cur["theme"]
        if t:
            txt.config(bg=t["surface"], fg=t["fg"], insertbackground=t["fg"],
                       selectbackground=t["sel_bg"], selectforeground=t["sel_fg"])
            win.configure(bg=t["bg"])

    def do_remove(tag=None):
        tag = tag or selected_tag()
        if tag not in model.installed:
            return
        if not messagebox.askyesno(tr("Удалить версию"), tr("Удалить версию {tag} с диска?\n\n{path}",
                                   tag=tag, path=model.installed[tag]), icon="warning", parent=root):
            return
        try:
            model.remove(tag)
            log(tr("Удалена версия {tag}.", tag=tag))
        except (OSError, ValueError) as e:
            messagebox.showerror(tr("Удаление"), str(e), parent=root)
        fill_list()

    def do_add_file():
        p = filedialog.askopenfilename(parent=root, filetypes=[(tr("Версия Portabilizer"), "*.zip *.exe"),
                                                              (tr("Все файлы"), "*.*")])
        if not p:
            return
        from tkinter import simpledialog
        name = simpledialog.askstring(tr("Название версии"), tr("Как назвать версию (например, v7.3)?"),
                                      initialvalue=Path(p).stem, parent=root)
        if not name:
            return
        try:
            model.import_file(p, name)
            log(tr("Добавлена версия {name} из {p}.", name=name, p=p))
        except (OSError, ValueError) as e:
            messagebox.showerror(tr("Добавить версию"), str(e), parent=root)
            return
        fill_list(name.strip())

    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label=tr("Настройки лаунчера"), command=lambda: nb.select(tab_set))
    menu.add_command(label=tr("Менеджер версий"), command=lambda: nb.select(tab_vers))
    menu.add_command(label=tr("Язык"), command=lambda: nb.select(tab_lang))
    menu.add_command(label=tr("Добавить свою версию..."), command=do_add_file)
    menu.add_command(label=tr("Удалить выбранную версию"), command=do_remove)
    menu.add_separator()
    menu.add_command(label=tr("Создать ярлык на рабочем столе"), command=lambda: make_shortcut(True))
    menu.add_command(label=tr("Создать ярлык выбранной версии на рабочем столе"),
                     command=lambda: make_version_shortcut(selected_tag(), True))
    menu.add_command(label=tr("Открыть папку версий"), command=lambda: open_folder(model.versions_dir))
    menu.add_command(label=tr("О программе"), command=lambda: nb.select(tab_about))

    def make_shortcut(verbose=False):
        if not getattr(sys, "frozen", False):
            if verbose:
                messagebox.showinfo(tr("Ярлык"), tr("Ярлык создаётся для собранного Portabilizer Launcher.exe "
                                    "(build_launcher.bat). Из исходников он не нужен."), parent=root)
            return
        try:
            path = C.create_desktop_shortcut(sys.executable, "Portabilizer Launcher")
            log(tr("Создан ярлык: {p}", p=path))
            if verbose:
                messagebox.showinfo(tr("Ярлык"), tr("Ярлык создан:\n{p}", p=path), parent=root)
        except OSError as e:
            log(tr("Ярлык не создан: {e}", e=e))
            if verbose:
                messagebox.showwarning(tr("Ярлык"), tr("Не удалось создать ярлык: {e}", e=e), parent=root)

    def first_run_shortcut():
        if getattr(sys, "frozen", False) and not settings.get("shortcut_asked"):
            settings["shortcut_asked"] = True
            save()
            if messagebox.askyesno(tr("Ярлык"), tr("Создать ярлык Portabilizer Launcher на рабочем столе?"),
                                   parent=root):
                make_shortcut(True)

    def make_version_shortcut(tag, verbose=False):
        """Ярлык на рабочем столе, который запускает выбранную версию Portabilizer (в режиме R - с --r)."""
        exe = model.exe_of(tag) if tag else None
        if not exe:
            return False
        radical = mode_var.get() == "r"
        try:
            path = C.create_version_shortcut(exe, tag, radical)
        except OSError as e:
            log(tr("Ярлык не создан: {e}", e=e))
            if verbose:
                messagebox.showwarning(tr("Ярлык"), tr("Не удалось создать ярлык: {e}", e=e), parent=root)
            return False
        log(tr("Ярлык версии: {p}", p=path))
        if verbose:
            messagebox.showinfo(tr("Ярлык"), tr("Ярлык создан:\n{p}", p=path), parent=root)
        return True

    def offer_version_shortcut(tag):
        """После установки версии спрашивает, нужен ли её ярлык на рабочем столе."""
        if not (ui["shortcuts"] and settings.get("offer_version_shortcut", True)):
            return
        if messagebox.askyesno(tr("Ярлык"), tr("Версия {tag} установлена.\n\nСоздать ярлык этой версии Portabilizer на рабочем столе?", tag=tag), parent=root):
            make_version_shortcut(tag, True)

    menu_defaults = {k: menu.cget(k) for k in ("bg", "fg", "activebackground", "activeforeground",
                                              "relief")}

    def show_menu(_e=None):
        menu.tk_popup(btn_menu.winfo_rootx(), btn_menu.winfo_rooty() + btn_menu.winfo_height())

    def settings_changed(*_a):
        settings["show_beta"] = bool(beta_var.get())
        settings["close_after_launch"] = bool(close_var.get())
        settings["offer_version_shortcut"] = bool(offer_var.get())
        d = dir_var.get().strip()
        settings["versions_dir"] = "" if d == str(C.app_dir() / "versions") else d
        save()
        model.scan_installed()
        fill_list()

    beta_var.trace_add("write", settings_changed)
    close_var.trace_add("write", settings_changed)
    offer_var.trace_add("write", settings_changed)
    dir_entry.bind("<FocusOut>", settings_changed)
    dir_entry.bind("<Return>", settings_changed)
    ttk.Button(tab_set, text="...", width=4, command=lambda: (
        dir_var.set(filedialog.askdirectory(parent=root) or dir_var.get()), settings_changed())
               ).grid(row=0, column=2, padx=4, pady=(14, 6))

    def mode_changed(*_a):
        settings["mode"] = mode_var.get()
        save()
        apply_theme()

    mode_var.trace_add("write", mode_changed)

    def pump():
        """Забирает сообщения из потоков и обновляет окно (только главный поток трогает виджеты)."""
        try:
            while True:
                kind, payload = q.get_nowait()
                if kind == "log":
                    logbox.config(state="normal")
                    logbox.insert("end", payload)
                    logbox.config(state="disabled")
                    logbox.see("end")
                elif kind == "progress":
                    got, total = payload
                    if total:
                        pb["value"] = got * 100 / total
                        status_var.set(tr("Скачано {got} из {total}", got=C.fmt_size(got), total=C.fmt_size(total)))
                    else:
                        pb.config(mode="indeterminate")
                elif kind == "done":
                    done, res, err = payload
                    done(res, err)
        except queue.Empty:
            pass
        if settings.get("appearance", "auto") == "auto" and T.system_prefers_dark() != ui["dark_sys"]:
            apply_theme()
        root.after(120, pump)

    tv.bind("<<TreeviewSelect>>", update_buttons)
    tv.bind("<Double-1>", do_main)
    btn_main.config(command=do_main)
    btn_info.config(command=do_info)
    btn_dir.config(command=do_dir)
    btn_ref.config(command=do_refresh)
    btn_menu.config(command=show_menu)
    btn_cancel.config(command=lambda: ui.update(cancel=True))
    btn_m_open.config(command=lambda: open_folder(model.folder_of(mv.selection()[0] if mv.selection() else "")))
    btn_m_del.config(command=lambda: do_remove(mv.selection()[0] if mv.selection() else None))
    btn_m_add.config(command=do_add_file)

    def on_close():
        if ui["busy"] and not messagebox.askyesno(tr("Идёт установка"), tr("Прервать установку и выйти?"),
                                                  icon="warning", parent=root):
            return
        ui["cancel"] = True
        save()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    apply_theme()
    fill_list()
    pump_job = root.after(120, pump)
    root.after(200, lambda: do_refresh(startup=True))
    root.after(1500, first_run_shortcut)

    if _hook:
        _hook({"root": root, "model": model, "settings": settings, "mode_var": mode_var,
               "tv": tv, "mv": mv, "fill_list": fill_list, "update_buttons": update_buttons,
               "do_main": do_main, "do_refresh": do_refresh, "apply_theme": apply_theme,
               "theme_cur": cur, "pump": pump, "q": q, "btn_main": btn_main, "status_var": status_var,
               "do_remove": do_remove, "style": style, "themes": themes, "ui": ui,
               "check_new": check_new, "banner_var": banner_var, "news": news,
               "make_shortcut": make_shortcut, "make_version_shortcut": make_version_shortcut,
               "offer_version_shortcut": offer_version_shortcut, "lang_var": lang_var,
               "tab_lang": tab_lang, "nb": nb})
        return
    root.mainloop()


def run():
    """Запускает окно; смена языка закрывает его и открывает заново уже на новом языке."""
    while True:
        RESTART["flag"] = False
        gui()
        if not RESTART["flag"]:
            break


if __name__ == "__main__":
    run()
