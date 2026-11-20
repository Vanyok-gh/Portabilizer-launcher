"""Папка данных лаунчера (не во временной папке) и запасной запуск версии через bat.
Запуск: python tests/test_fallback.py"""
import os
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pz_core as C
import pz_theme as T

ok = 0


def check(c, m):
    global ok
    assert c, "ПРОВАЛ: " + m
    ok += 1


# --- временная папка: запуск exe прямо из архива в Проводнике
check(T.is_temp_location(r"C:\Users\Ivan\AppData\Local\Temp\Temp1_Portabilizer-Launcher-v0.7.zip"), "Temp1_...zip")
check(T.is_temp_location(r"D:\x\Portabilizer-Launcher-v0.7.zip\inner"), "путь внутри zip")
check(T.is_temp_location(os.path.join(tempfile.gettempdir(), "abc")), "системная временная папка")
check(not T.is_temp_location(r"C:\Users\Ivan\Downloads\Launcher"), "обычная папка")
check(not T.is_temp_location(r"D:\Portabilizer"), "диск D")

# --- data_dir
tmp = Path(tempfile.mkdtemp())
saved = {k: os.environ.get(k) for k in ("HOME", "USERPROFILE", T.HOME_ENV)}
saved_app = T.app_dir
try:
    os.environ["HOME"] = os.environ["USERPROFILE"] = str(tmp / "home")
    os.environ.pop(T.HOME_ENV, None)
    (tmp / "home").mkdir()
    T.app_dir = lambda: Path("/opt/launcher")
    check(T.data_dir() == Path("/opt/launcher"), "постоянная папка: данные рядом с exe")
    T.app_dir = lambda: Path(tempfile.gettempdir()) / "Temp1_x.zip"
    d = T.data_dir()
    check(d == tmp / "home" / "Portabilizers" and d.is_dir(), "временная папка: данные в Portabilizers профиля")
    check(C.data_dir() == d, "pz_core отдаёт ту же папку")
    os.environ[T.HOME_ENV] = str(tmp / "forced")
    check(T.data_dir() == tmp / "forced", "переменная PORTABILIZER_LAUNCHER_HOME главнее")
finally:
    T.app_dir = saved_app
    for k, v in saved.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v

# --- запасной запуск версии через bat, когда exe не даёт запустить
calls = []
real_popen = C.subprocess.Popen


def fake_popen(args, **kw):
    calls.append(args)
    if str(args[0]).lower().endswith(".exe"):
        raise PermissionError(13, "Access is denied")
    return "bat-process"


C.subprocess.Popen = fake_popen
try:
    ver = tmp / "versions" / "v10.8"
    inner = ver / "Portabilizer-v10.8"
    inner.mkdir(parents=True)
    exe = inner / "Portabilizer.exe"
    exe.write_bytes(b"MZ")
    try:
        C.launch(exe)
        check(False, "без bat ошибка должна пробрасываться")
    except PermissionError:
        check(True, "bat нет: PermissionError пробрасывается")
    (ver / C.PY_BAT_NAME).write_text("@echo off\r\n", encoding="utf-8")
    calls.clear()
    check(C.launch(exe) == "bat-process" and Path(calls[-1][0]).name == C.PY_BAT_NAME and len(calls[-1]) == 1,
          "exe заблокирован: запуск через Portabilizer-py.bat (bat в папке версии)")
    calls.clear()
    C.launch(exe, radical=True)
    check(calls[-1][-1] == "--r", "режим R передаётся в bat")
    (ver / C.PY_BAT_NAME).unlink()
    (inner / "Portabilizer.bat").write_text("@echo off\r\n", encoding="utf-8")
    calls.clear()
    C.launch(exe)
    check(Path(calls[-1][0]).name == "Portabilizer.bat", "запасной Portabilizer.bat рядом с exe")
    (inner / "Portabilizer (R).bat").write_text("@echo off\r\n", encoding="utf-8")
    calls.clear()
    C.launch(exe, radical=True)
    check(Path(calls[-1][0]).name == "Portabilizer (R).bat", "режим R: Portabilizer (R).bat")

    def blocked(args, **kw):
        calls.append(args)
        if str(args[0]).lower().endswith(".exe"):
            e = OSError(1260, "blocked by policy")
            e.winerror = 1260
            raise e
        return "ok"
    C.subprocess.Popen = blocked
    check(C.launch(exe) == "ok", "winerror 1260 (политика) тоже ведёт к bat")

    def other(args, **kw):
        raise OSError(2, "нет такого файла")
    C.subprocess.Popen = other
    try:
        C.launch(exe)
        check(False, "другая ошибка не должна заменяться запуском bat")
    except OSError:
        check(True, "другие ошибки не маскируются")
finally:
    C.subprocess.Popen = real_popen
print(f"OK: {ok} проверок")
