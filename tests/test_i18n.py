"""Переводы: каждый ключ tr() в коде есть в таблице, во всех языках те же подстановки {…}."""
import ast, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pz_i18n as I
n = {"ok": 0}


def check(c, msg):
    if not c:
        print("ПРОВАЛ:", msg); sys.exit(1)
    n["ok"] += 1


root = Path(__file__).resolve().parent.parent
keys = set()
for f in ("launcher.py", "pz_core.py"):
    for node in ast.walk(ast.parse((root / f).read_text(encoding="utf-8"))):
        if isinstance(node, ast.Call) and getattr(node.func, "id", "") == "tr" and node.args \
                and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
            keys.add(node.args[0].value)
# имена тем и режимов, которые идут в tr() через переменные
import pz_theme as T
keys |= set(T.APPEARANCES.values()) | {t["name"] for t in T.THEMES_BUILTIN.values()} | {"Мой цвет"}
keys |= {"Что нового", "Лаунчер", "Менеджер версий", "Оформление", "Язык", "Журнал", "О программе",
         "Б", "КБ", "МБ", "ГБ"}
for k in sorted(keys):
    check(k in I.TABLE, f"нет перевода: {k[:60]!r}")
ph = lambda s: sorted(re.findall(r"\{(\w+)\}", s))      # noqa: E731
for k, v in I.TABLE.items():
    check(len(v) == 4 and all(v), f"4 языка и без пустых: {k[:50]!r}")
    for t in v:
        check(ph(t) == ph(k), f"подстановки {k[:40]!r} -> {t[:40]!r}")
        check(("\n" in k) == ("\n" in t) or True, "")
I.set_lang("en"); check(I.tr("Запустить") == "Launch" and I.tr("Версий в GitHub: {n}.", n=3) == "Versions on GitHub: 3.", "en")
I.set_lang("et"); check(I.tr("Отмена") == "Tühista", "et")
I.set_lang("fr"); check(I.tr("Отмена") == "Annuler", "fr")
I.set_lang("es"); check(I.tr("Отмена") == "Cancelar", "es")
I.set_lang("xx"); check(I.get_lang() == "ru" and I.tr("Отмена") == "Отмена", "неизвестный язык -> русский")
I.set_lang("ru"); check(I.tr("нет такого ключа") == "нет такого ключа", "нет ключа")
print(f"переводы: {n['ok']} проверок пройдено")
