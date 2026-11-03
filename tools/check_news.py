"""Проверка переводов news/<код>.md против news/en.md. Запуск: python3 tools/check_news.py [код ...]
Проверяет: те же разделы '## vX.Y' в том же порядке, то же число пунктов, все числа из английского (лишние можно), те же имена файлов и
технические слова, строка со списком языков не тронута."""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEEP = ["portabilizer.log", "wrap_oal.dll", "expand.exe", "tools/collect_redist.bat", "d3dx9_24", "d3dx10", "XACT",
        "XAudio", "xinput", "UAC", "DirectX", "7-Zip", "Visual C++", "OpenAL", "GitHub", "Windows", "Portabilizer",
        "Launcher", "Cab", "exe", "App"]


def sections(text):
    out, key, buf = [], None, []
    for line in text.splitlines():
        m = re.match(r"^##\s+(v\d+(?:\.\d+)*)\s*$", line)
        if m:
            if key: out.append((key, buf))
            key, buf = m.group(1), []
        elif key and line.strip():
            buf.append(line.strip())
    if key: out.append((key, buf))
    return out


def check(code):
    errs, en, tr = [], sections((ROOT / "news/en.md").read_text("utf-8")), None
    f = ROOT / f"news/{code}.md"
    if not f.exists(): return [f"нет файла news/{code}.md"]
    tr = sections(f.read_text("utf-8"))
    if [k for k, _ in en] != [k for k, _ in tr]: return [f"разделы {[k for k, _ in tr]} != {[k for k, _ in en]}"]
    for (k, be), (_, bt) in zip(en, tr):
        if len(be) != len(bt) or not all(x.startswith("- ") for x in bt):
            errs.append(f"{k}: пунктов {len(bt)} вместо {len(be)} (каждый с '- ')"); continue
        for i, (a, b) in enumerate(zip(be, bt), 1):
            na, nb = sorted(re.findall(r"\d+", a)), sorted(re.findall(r"\d+", b))
            lost = list(na)
            for x in nb:
                if x in lost: lost.remove(x)
            if lost: errs.append(f"{k} п.{i}: нет чисел {lost} (цифры 0-9; лишние числа, например месяц, можно)")
            for w in KEEP:
                if w in a and w not in b and w not in ("exe", "App", "Cab", "Windows", "Launcher"):
                    errs.append(f"{k} п.{i}: нет '{w}'")
            if a.startswith("- Languages: 34") or a.startswith("- Languages:"):
                la, lb = a.split("(", 1)[-1].rsplit(")", 1)[0], b.split("(", 1)[-1].rsplit(")", 1)[0]
                if la != lb: errs.append(f"{k} п.{i}: список 34 языков изменён")
    return errs


if __name__ == "__main__":
    codes = sys.argv[1:] or [c.split()[0] for c in (ROOT / "lang/_codes.txt").read_text("utf-8").split("\n") if c.strip()
                             and c.split()[0] not in ("ru", "en")]
    bad = 0
    for c in codes:
        e = check(c)
        if e: bad += 1; print(c, "->", *e, sep="\n  ")
    print(f"проверено {len(codes)}, с ошибками {bad}")
    sys.exit(1 if bad else 0)
