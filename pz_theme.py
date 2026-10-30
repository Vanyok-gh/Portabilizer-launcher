"""Темы оформления Portabilizer Launcher (общий код с Portabilizer v8.7: те же палитры и проверка читаемости)."""
import json
import os
import re
import sys
from pathlib import Path


def app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent


# ------------------------------------------------------------------ темы оформления

SETTINGS_FILE = "launcher_settings.json"
THEME_ROLES = ("bg", "surface", "surface2", "fg", "muted", "border", "accent", "accent_fg", "hover",
               "sel_bg", "sel_fg", "ok", "warn", "danger", "dis")
# Встроенные темы. Свои темы - файлы *.json в папке themes рядом с программой (те же ключи,
# плюс "name", "kind": "light" или "dark", "r": true для красных тем режима R).
THEMES_BUILTIN = {
    "light": {
        "name": "Светлая",
        "kind": "light",
        "r": False,
        "bg": "#f3f4f6",
        "surface": "#ffffff",
        "surface2": "#e4e7eb",
        "fg": "#1f2328",
        "muted": "#555e68",
        "border": "#c4c9d0",
        "accent": "#1f5fd1",
        "accent_fg": "#ffffff",
        "hover": "#1a4fb0",
        "sel_bg": "#cfe0ff",
        "sel_fg": "#111827",
        "ok": "#1a7f37",
        "warn": "#8a5a00",
        "danger": "#b3261e",
        "dis": "#8c959f"
    },
    "dark": {
        "name": "Тёмная",
        "kind": "dark",
        "r": False,
        "bg": "#1b1d21",
        "surface": "#23262b",
        "surface2": "#2e3238",
        "fg": "#e6e8eb",
        "muted": "#a3a9b1",
        "border": "#3d424a",
        "accent": "#3568be",
        "accent_fg": "#ffffff",
        "hover": "#4171c2",
        "sel_bg": "#2f4b7c",
        "sel_fg": "#ffffff",
        "ok": "#5fcf80",
        "warn": "#f0b45a",
        "danger": "#ff7b7b",
        "dis": "#6b727b"
    },
    "light_r": {
        "name": "Светло-красная (R)",
        "kind": "light",
        "r": True,
        "bg": "#fbf1f1",
        "surface": "#ffffff",
        "surface2": "#f1d9d9",
        "fg": "#2b1618",
        "muted": "#6a464a",
        "border": "#deb7b7",
        "accent": "#c62828",
        "accent_fg": "#ffffff",
        "hover": "#a61e1e",
        "sel_bg": "#f6c9c9",
        "sel_fg": "#2b1618",
        "ok": "#1f6f33",
        "warn": "#8a5200",
        "danger": "#b00020",
        "dis": "#a88a8c"
    },
    "dark_r_charcoal": {
        "name": "Уголь с красным акцентом",
        "kind": "dark",
        "r": True,
        "bg": "#18191c",
        "surface": "#212226",
        "surface2": "#2c2d32",
        "fg": "#ececee",
        "muted": "#a9aab0",
        "border": "#3d3e45",
        "accent": "#c8323d",
        "accent_fg": "#ffffff",
        "hover": "#ce444e",
        "sel_bg": "#5a2329",
        "sel_fg": "#ffffff",
        "ok": "#6fd08a",
        "warn": "#f0b45a",
        "danger": "#ff7f89",
        "dis": "#6c6d74"
    },
    "dark_r_wine": {
        "name": "Бордо",
        "kind": "dark",
        "r": True,
        "bg": "#1f1316",
        "surface": "#2b1b1f",
        "surface2": "#3b2429",
        "fg": "#f4e8e9",
        "muted": "#c7a9ac",
        "border": "#5c3b41",
        "accent": "#c4303b",
        "accent_fg": "#ffffff",
        "hover": "#ca424d",
        "sel_bg": "#6a2a32",
        "sel_fg": "#ffffff",
        "ok": "#72d38b",
        "warn": "#f2b865",
        "danger": "#ff8089",
        "dis": "#7d6366"
    },
    "dark_r_cherry": {
        "name": "Вишнёвая",
        "kind": "dark",
        "r": True,
        "bg": "#260d13",
        "surface": "#321219",
        "surface2": "#471b25",
        "fg": "#fbeaec",
        "muted": "#d4a6ad",
        "border": "#6e2c38",
        "accent": "#c8303f",
        "accent_fg": "#ffffff",
        "hover": "#ce4250",
        "sel_bg": "#7a2b37",
        "sel_fg": "#ffffff",
        "ok": "#78d68f",
        "warn": "#f5bb68",
        "danger": "#ff8a94",
        "dis": "#85606a"
    }
}
CLASSIC = {"bg": None, "surface": "white", "surface2": None, "fg": "black", "muted": "#666666",
           "border": None, "accent": None, "accent_fg": None, "hover": None, "sel_bg": "#0078d7",
           "sel_fg": "white", "ok": "#1b6e2d", "warn": "#b36b00", "danger": "#b00020", "dis": "#888888"}
APPEARANCES = {"auto": "Авто (как в Windows)", "light": "Светлая", "dark": "Тёмная",
               "classic": "Классическая (системная)"}


def _is_hex(v) -> bool:
    return isinstance(v, str) and re.fullmatch(r"#[0-9a-fA-F]{6}", v) is not None


def load_settings(path=None) -> dict:
    try:
        d = json.loads(Path(path or (app_dir() / SETTINGS_FILE)).read_text(encoding="utf-8"))
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError):
        return {}


def save_settings(d: dict, path=None):
    pth = Path(path or (app_dir() / SETTINGS_FILE))
    try:
        tmp = pth.with_name(pth.name + ".tmp")
        tmp.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tmp, pth)
    except OSError:
        pass


def load_themes(folder=None) -> dict:
    """Встроенные темы + пользовательские из папки themes. Битые файлы пропускаем."""
    themes = {k: dict(v, id=k) for k, v in THEMES_BUILTIN.items()}
    d = Path(folder) if folder else app_dir() / "themes"
    try:
        files = sorted(d.glob("*.json")) if d.is_dir() else []
    except OSError:
        files = []
    for f in files:
        if f.stem.startswith("_"):             # _пример.json и подобные не загружаем
            continue
        try:
            t = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not isinstance(t, dict):
            continue
        kind = t.get("kind") if t.get("kind") in ("light", "dark") else "light"
        base = dict(THEMES_BUILTIN["dark_r_charcoal" if t.get("r") and kind == "dark" else
                                   "light_r" if t.get("r") else kind])
        for role in THEME_ROLES:                # недостающие цвета берём из базовой темы
            if _is_hex(t.get(role)):
                base[role] = t[role]
        base.update(name=str(t.get("name") or f.stem), kind=kind, r=bool(t.get("r")), id=f.stem,
                    user=True)
        themes[f.stem] = base
    return themes


def system_prefers_dark() -> bool:
    if os.name != "nt":
        return False
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize") as k:
            return winreg.QueryValueEx(k, "AppsUseLightTheme")[0] == 0
    except (OSError, ImportError):
        return False


def pick_theme(settings: dict, radical: bool, themes: dict, dark_system=None):
    """Какую тему применить. None - классический системный вид (ничего не красим)."""
    ap = settings.get("appearance", "auto")
    if ap == "classic":
        return None
    if ap in themes and not themes[ap].get("r"):
        kind = themes[ap]["kind"]
    elif ap == "dark":
        kind = "dark"
    elif ap == "light":
        kind = "light"
    else:
        kind = "dark" if (system_prefers_dark() if dark_system is None else dark_system) else "light"
    if radical:
        want = settings.get("dark_r" if kind == "dark" else "light_r", "")
        t = themes.get(want)
        if t and t.get("r") and t["kind"] == kind:
            return t
        return themes["dark_r_charcoal" if kind == "dark" else "light_r"]
    if ap in themes and not themes[ap].get("r"):
        return themes[ap]
    return themes[kind]


def _mix(a: str, b: str, t: float) -> str:
    a, b = a.lstrip("#"), b.lstrip("#")
    return "#" + "".join(f"{round(int(a[i:i + 2], 16) * (1 - t) + int(b[i:i + 2], 16) * t):02x}"
                         for i in (0, 2, 4))


def _lum(h: str) -> float:
    h = h.lstrip("#")
    r, g, b = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4   # noqa
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(a: str, b: str) -> float:
    la, lb = _lum(a), _lum(b)
    if la < lb:
        la, lb = lb, la
    return (la + 0.05) / (lb + 0.05)


def make_theme_from_color(accent: str, kind: str = "dark", bg_tint=None, name="Мой цвет",
                          radical=False) -> dict:
    """Полная палитра из одного выбранного цвета (и необязательного оттенка фона).
    Цвета подгоняются так, чтобы текст везде читался (контраст не ниже 4,5:1)."""
    import colorsys
    if not _is_hex(accent):
        raise ValueError("цвет должен быть вида #rrggbb")
    rgb = lambda h: tuple(int(h.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4))   # noqa
    hexc = lambda r, g, b: "#%02x%02x%02x" % tuple(round(max(0, min(1, v)) * 255) for v in (r, g, b))  # noqa
    ah, _al, asat = colorsys.rgb_to_hls(*rgb(accent))
    th = colorsys.rgb_to_hls(*rgb(bg_tint if _is_hex(bg_tint) else accent))[0]
    dark = kind == "dark"
    sat = 0.22 if dark else 0.30
    hls = lambda h, l, sa: hexc(*colorsys.hls_to_rgb(h, l, sa))                       # noqa
    if dark:
        bg, surface, surface2 = hls(th, 0.10, sat), hls(th, 0.14, sat), hls(th, 0.20, sat)
        fg, border, sel_bg = hls(th, 0.93, 0.25), hls(th, 0.28, sat), hls(ah, 0.30, max(asat, .35))
        sel_fg = "#ffffff"
        ok, warn, danger = "#6fd08a", "#f0b45a", "#ff8088"
    else:
        bg, surface, surface2 = hls(th, 0.96, sat), "#ffffff", hls(th, 0.89, sat)
        fg, border, sel_bg = hls(th, 0.11, 0.30), hls(th, 0.78, sat), hls(ah, 0.86, max(asat, .45))
        sel_fg = hls(th, 0.11, 0.30)
        ok, warn, danger = "#1a7f37", "#8a5a00", "#b3261e"
    if dark:                                    # выделение: белый текст на нём должен читаться
        sh, sl, ss = colorsys.rgb_to_hls(*rgb(sel_bg))
        for _ in range(40):
            if contrast("#ffffff", sel_bg) >= 4.6:
                break
            sl = max(0.0, sl - 0.02)
            sel_bg = hls(sh, sl, ss)
    # акцент: подгоняем яркость, чтобы белый текст на нём читался
    h, l, sa = colorsys.rgb_to_hls(*rgb(accent))
    sa = max(sa, 0.45)
    acc = hls(h, l, sa)
    for _ in range(40):
        if contrast("#ffffff", acc) >= 4.6:
            break
        l = max(0.0, l - 0.02)
        acc = hls(h, l, sa)
    hover = hls(h, max(0.0, l - 0.05), sa)
    if contrast("#ffffff", hover) < 4.5:
        hover = acc
    # второстепенный текст: двигаем яркость, пока не станет читаться на фоне и на полях
    mh = th
    ml = 0.70 if dark else 0.34
    muted = hls(mh, ml, 0.12)
    for _ in range(40):
        if min(contrast(muted, bg), contrast(muted, surface), contrast(muted, surface2)) >= 4.5:
            break
        ml = min(1.0, ml + 0.02) if dark else max(0.0, ml - 0.02)
        muted = hls(mh, ml, 0.12)
    dis = hls(th, 0.45, 0.10)
    t = dict(name=name, kind=kind, r=bool(radical), bg=bg, surface=surface, surface2=surface2, fg=fg,
             muted=muted, border=border, accent=acc, accent_fg="#ffffff", hover=hover,
             sel_bg=sel_bg, sel_fg=sel_fg, ok=ok, warn=warn, danger=danger, dis=dis)
    return t


def ttk_style_spec(c: dict) -> list:
    """Описание стилей ttk для палитры c: список (имя_стиля, configure, map).
    Чистая функция: так её можно проверять без окна."""
    bg, sf, sf2, fg, mu, bd = c["bg"], c["surface"], c["surface2"], c["fg"], c["muted"], c["border"]
    ac, acf, hv = c["accent"], c["accent_fg"], c["hover"]
    sb, sfg, dis = c["sel_bg"], c["sel_fg"], c["dis"]
    hov2 = _mix(sf2, fg, 0.10)
    press = _mix(sf2, fg, 0.18)
    flat = dict(lightcolor=sf2, darkcolor=sf2, bordercolor=bd)
    return [
        (".", dict(background=bg, foreground=fg, bordercolor=bd, troughcolor=sf2, focuscolor=ac,
                   selectbackground=sb, selectforeground=sfg, insertcolor=fg, fieldbackground=sf,
                   lightcolor=bg, darkcolor=bg), {"foreground": [("disabled", dis)]}),
        ("TFrame", dict(background=bg), {}),
        ("TLabel", dict(background=bg, foreground=fg), {}),
        ("Muted.TLabel", dict(foreground=mu), {}),
        ("Warn.TLabel", dict(foreground=c["warn"]), {}),
        ("Danger.TLabel", dict(foreground=c["danger"]), {}),
        ("TLabelframe", dict(background=bg, bordercolor=bd, lightcolor=bg, darkcolor=bg), {}),
        ("TLabelframe.Label", dict(background=bg, foreground=fg), {}),
        ("TButton", dict(background=sf2, foreground=fg, padding=(10, 4), relief="flat", **flat),
         {"background": [("disabled", sf2), ("pressed", press), ("active", hov2)],
          "foreground": [("disabled", dis)],
          "bordercolor": [("focus", ac)]}),
        ("Accent.TButton", dict(background=ac, foreground=acf, padding=(12, 5), relief="flat",
                                lightcolor=ac, darkcolor=ac, bordercolor=ac),
         {"background": [("disabled", sf2), ("pressed", hv), ("active", hv)],
          "foreground": [("disabled", dis)],
          "bordercolor": [("disabled", bd)], "lightcolor": [("disabled", sf2), ("active", hv)],
          "darkcolor": [("disabled", sf2), ("active", hv)]}),
        ("TNotebook", dict(background=bg, bordercolor=bd, lightcolor=bg, darkcolor=bg,
                           tabmargins=(2, 4, 2, 0)), {}),
        ("TNotebook.Tab", dict(background=sf2, foreground=mu, padding=(12, 5), bordercolor=bd,
                               lightcolor=sf2, darkcolor=sf2),
         {"background": [("selected", sf), ("active", hov2)],
          "foreground": [("selected", fg), ("active", fg)],
          "lightcolor": [("selected", sf)], "darkcolor": [("selected", sf)]}),
        ("TEntry", dict(fieldbackground=sf, foreground=fg, insertcolor=fg, bordercolor=bd,
                        lightcolor=sf, darkcolor=sf, padding=3),
         {"bordercolor": [("focus", ac)], "lightcolor": [("focus", ac)], "darkcolor": [("focus", ac)]}),
        ("TCombobox", dict(fieldbackground=sf, background=sf2, foreground=fg, arrowcolor=fg,
                           insertcolor=fg, bordercolor=bd, lightcolor=sf, darkcolor=sf, padding=3,
                           selectbackground=sf, selectforeground=fg),
         {"fieldbackground": [("readonly", sf), ("disabled", sf2)],
          "foreground": [("readonly", fg), ("disabled", dis)],
          "background": [("active", hov2), ("readonly", sf2)],
          "bordercolor": [("focus", ac)], "arrowcolor": [("disabled", dis)]}),
        ("TProgressbar", dict(troughcolor=sf2, background=ac, bordercolor=bd, lightcolor=ac,
                              darkcolor=ac, thickness=14), {}),
        ("TScrollbar", dict(background=sf2, troughcolor=bg, bordercolor=bd, arrowcolor=fg,
                            lightcolor=sf2, darkcolor=sf2, relief="flat"),
         {"background": [("active", hov2), ("pressed", press)]}),
        ("Treeview", dict(background=sf, fieldbackground=sf, foreground=fg, bordercolor=bd,
                          lightcolor=sf, darkcolor=sf, rowheight=22),
         {"background": [("selected", sb)], "foreground": [("selected", sfg)]}),
        ("Treeview.Heading", dict(background=sf2, foreground=fg, relief="flat", bordercolor=bd,
                                  lightcolor=sf2, darkcolor=sf2, padding=(6, 4)),
         {"background": [("active", hov2)]}),
        ("TCheckbutton", dict(background=bg, foreground=fg, indicatorcolor=sf, bordercolor=bd), 
         {"indicatorcolor": [("selected", ac)], "background": [("active", bg)]}),
        ("TRadiobutton", dict(background=bg, foreground=fg, indicatorcolor=sf, bordercolor=bd),
         {"indicatorcolor": [("selected", ac)], "background": [("active", bg)]}),
        ("TSeparator", dict(background=bd), {}),
    ]


def set_dark_titlebar(root, dark: bool):
    """Тёмная рамка окна в Windows 10/11 (если система это умеет). Ошибки не критичны."""
    if os.name != "nt":
        return
    try:
        import ctypes
        root.update_idletasks()
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id()) or root.winfo_id()
        val = ctypes.c_int(1 if dark else 0)
        for attr in (20, 19):                   # 20 - Windows 11 и поздние 10, 19 - ранние 10
            if ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, attr, ctypes.byref(val), 4) == 0:
                break
    except Exception:
        pass


