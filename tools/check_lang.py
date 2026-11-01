"""Проверка файла перевода: python tools/check_lang.py lang/de.txt [lang/de_names.txt ...]
Файл перевода: строки "номер<TAB>текст" (перенос строки пишется как \\n), номера и подстановки {имя} - как в lang/_source.txt.
Файл имён: строки "код<TAB>название языка" для всех 34 кодов из lang/_codes.txt."""
import re, sys
from pathlib import Path
root = Path(__file__).resolve().parent.parent / "lang"
src = {}
for line in (root / "_source.txt").read_text(encoding="utf-8").splitlines():
    n, ru, en = line.split("\t"); src[int(n)] = (ru, en)
codes = [l.split("\t")[0] for l in (root / "_codes.txt").read_text(encoding="utf-8").splitlines() if l.strip()]
ph = lambda s: sorted(re.findall(r"\{(\w+)\}", s))      # noqa: E731
bad = 0
for arg in sys.argv[1:]:
    p = Path(arg); rows = {}
    for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        if line.count("\t") != 1:
            print(f"{p.name}:{i}: нужна ровно одна табуляция"); bad += 1; continue
        k, t = line.split("\t"); rows[k] = t
    if p.name.endswith("_names.txt"):
        for c in codes:
            if not rows.get(c, "").strip():
                print(f"{p.name}: нет названия для {c}"); bad += 1
        continue
    for n, (ru, en) in src.items():
        t = rows.get(str(n), "")
        if not t.strip():
            print(f"{p.name}: нет строки {n} ({ru[:30]!r})"); bad += 1
        elif ph(t) != ph(ru):
            print(f"{p.name}: строка {n}: подстановки {ph(t)} вместо {ph(ru)}"); bad += 1
    extra = set(rows) - {str(n) for n in src}
    if extra:
        print(f"{p.name}: лишние номера {sorted(extra)[:5]}"); bad += 1
print("ОШИБОК:", bad) if bad else print("ок")
sys.exit(1 if bad else 0)
