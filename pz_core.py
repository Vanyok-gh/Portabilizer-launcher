"""Ядро Portabilizer Launcher: версии, установка, запуск. Без графики, поэтому проверяется тестами.

Версии берутся из GitHub Releases репозитория (см. README). Каждый релиз - один zip с
Portabilizer.exe: в нём уже есть и обычный режим, и режим R (ключ --r).
"""
import dataclasses
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
import zipfile
from pathlib import Path

from pz_i18n import tr

OWNER, REPO = "Vanyok-gh", "Portabilizer-launcher"          # репозиторий самого лаунчера
# откуда брать версии Portabilizer: пока тот же репозиторий; когда появится отдельный
# (например Vanyok-gh/Portabilizer), достаточно поменять эту строку или параметр versions_repo в настройках
VERSIONS_OWNER, VERSIONS_REPO = "Vanyok-gh", "Portabilizer"
API_URL = "https://api.github.com/repos/{owner}/{repo}/releases"
EXE_NAME = "Portabilizer.exe"
USER_AGENT = "Portabilizer-Launcher"


class Cancelled(Exception):
    pass


def app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent


def fmt_size(n) -> str:
    n = float(n or 0)
    for unit in ("Б", "КБ", "МБ", "ГБ"):
        if n < 1024 or unit == "ГБ":
            return f"{n:.0f} {tr(unit)}" if unit == "Б" else f"{n:.1f} {tr(unit)}"
        n /= 1024
    return f"{n:.1f} {tr('ГБ')}"


# ------------------------------------------------------------------ версии и релизы

def parse_version(tag: str) -> tuple:
    """'v8.7' -> (8, 7); 'v7.3.1-beta' -> (7, 3, 1). Нечисловые версии получают (0,)."""
    nums = tuple(int(x) for x in re.findall(r"\d+", tag or ""))
    return nums or (0,)


@dataclasses.dataclass
class Release:
    tag: str
    name: str = ""
    notes: str = ""
    prerelease: bool = False
    published: str = ""
    asset_name: str = ""
    asset_url: str = ""
    asset_size: int = 0
    sha256: str = ""
    sha_url: str = ""          # отдельный файл с суммой, если в релизе он есть
    local: bool = False        # версия есть только на диске (нет в GitHub)
    alts: list = dataclasses.field(default_factory=list)   # запасные файлы релиза (если в первом нет программы)

    @property
    def channel(self) -> str:
        return "Beta" if self.prerelease else "Stable"

    @property
    def available(self) -> bool:
        return bool(self.asset_url)


def rank_assets(assets: list) -> list:
    """Файлы релиза, из которых можно поставить программу (zip или готовый exe), лучшие первыми:
    голый Portabilizer.exe, затем zip с 'portabilizer' в имени."""
    ok = [a for a in assets or [] if str(a.get("name", "")).lower().endswith((".zip", ".exe"))]
    ok.sort(key=lambda a: (not a["name"].lower().endswith(".exe"),
                           "portabilizer" not in a["name"].lower(),
                           "x64" not in a["name"].lower() and "win" not in a["name"].lower(),
                           a["name"].lower()))
    return ok


def pick_asset(assets: list, tag: str = ""):
    ranked = rank_assets(assets)
    return ranked[0] if ranked else None


def _sha_from(asset: dict, assets: list, body: str) -> tuple:
    """(сумма, ссылка_на_файл_с_суммой). GitHub сам кладёт digest 'sha256:...' в описание файла."""
    d = str(asset.get("digest") or "")
    if d.lower().startswith("sha256:") and re.fullmatch(r"[0-9a-fA-F]{64}", d[7:]):
        return d[7:].lower(), ""
    for a in assets:
        if a.get("name", "").lower() in (asset["name"].lower() + ".sha256", "sha256sums.txt",
                                          "sha256sums", "checksums.txt"):
            return "", a.get("browser_download_url", "")
    m = re.search(r"sha-?256\W+([0-9a-fA-F]{64})", body or "", re.I)
    return (m.group(1).lower(), "") if m else ("", "")


def parse_releases(data) -> list:
    """Разбор ответа GitHub API в список Release (новые версии первыми, черновики пропускаем)."""
    out = []
    for r in data if isinstance(data, list) else []:
        if not isinstance(r, dict) or r.get("draft") or not r.get("tag_name"):
            continue
        if not re.match(r"^[vV]?\d", str(r["tag_name"])):     # например launcher-v0.2: не версия Portabilizer
            continue
        assets = r.get("assets") or []
        ranked = rank_assets(assets)
        a = ranked[0] if ranked else None
        sha, sha_url = _sha_from(a, assets, r.get("body") or "") if a else ("", "")
        alts = []
        for b in ranked[1:]:
            bs, bu = _sha_from(b, assets, "")
            alts.append({"name": b["name"], "url": b.get("browser_download_url", ""),
                         "size": int(b.get("size") or 0), "sha256": bs, "sha_url": bu})
        out.append(Release(alts=alts,
            tag=r["tag_name"], name=r.get("name") or r["tag_name"], notes=r.get("body") or "",
            prerelease=bool(r.get("prerelease")), published=(r.get("published_at") or "")[:10],
            asset_name=a["name"] if a else "", asset_url=a.get("browser_download_url", "") if a else "",
            asset_size=int(a.get("size") or 0) if a else 0, sha256=sha, sha_url=sha_url))
    out.sort(key=lambda x: parse_version(x.tag), reverse=True)
    return out


def parse_changelog(text: str) -> dict:
    """CHANGELOG.md -> {'8.9': 'текст', ...}. Раздел начинается с '## v8.9' (v необязательна)."""
    out, key, buf = {}, None, []
    for line in str(text or "").splitlines():
        m = re.match(r"^##\s+[vV]?(\d+(?:\.\d+)*)\b", line)
        if m:
            if key:
                out[key] = "\n".join(buf).strip()
            key, buf = m.group(1), []
        elif key:
            buf.append(line)
    if key:
        out[key] = "\n".join(buf).strip()
    return out


def notes_empty(notes) -> bool:
    """Пусто или только заголовок вроде 'Portabilizer v9.0': настоящего описания нет."""
    t = (notes or "").strip()
    return not t or bool(re.fullmatch(r"(?i)(portabilizer\s*)?v?\d+(?:\.\d+)*(?:[-\w.]*)", t))


def fill_notes_from_changelog(releases, text: str):
    """Подставляет описание из CHANGELOG тем релизам, у которых оно пустое."""
    log = parse_changelog(text)
    for r in releases:
        if notes_empty(r.notes):
            body = log.get(".".join(map(str, parse_version(r.tag))))
            if body:
                r.notes = f"Portabilizer {r.tag}\n\n{body}"


def fetch_changelog(owner, repo, timeout=15, opener=None) -> str:
    """Читает CHANGELOG.md из репозитория (ветка main). Любая ошибка -> пустая строка."""
    try:
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/CHANGELOG.md"
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with (opener or urllib.request.urlopen)(req, timeout=timeout) as r:
            return r.read().decode("utf-8")
    except Exception:                                       # noqa: BLE001
        return ""


NEWS_URL = "https://raw.githubusercontent.com/Vanyok-gh/Portabilizer-launcher/main/news/{code}.md"


def fetch_news(code, timeout=6, opener=None) -> dict:
    """Перевод «Что нового» на язык code: {'9.1': 'текст', ...}. Нет файла или связи -> пустой словарь."""
    if not re.fullmatch(r"[a-z]{2,3}", str(code or "")):
        return {}
    try:
        req = urllib.request.Request(NEWS_URL.format(code=code), headers={"User-Agent": USER_AGENT})
        with (opener or urllib.request.urlopen)(req, timeout=timeout) as r:
            return parse_changelog(r.read().decode("utf-8"))
    except Exception:                                       # noqa: BLE001
        return {}


# --- запасной машинный перевод описания (если нет готового файла в news/).
# Неофициальная бесплатная точка Google Translate без ключа: может перестать работать - тогда остаётся английский/русский.
MT_URL = "https://translate.googleapis.com/translate_a/single"
MT_CODES = {"zh": "zh-CN", "he": "iw"}                      # коды, которые у Google отличаются от наших
_PROTECT = re.compile(r"\([^)]{80,}\)|[\w./-]+\.(?:log|dll|exe|bat|ps1|zip)\b|d3dx[\w…]*|XAudio|XACT|xinput|UAC"
                      r"|DirectX|7-Zip|Visual C\+\+|OpenAL|GitHub|Portabilizer|Launcher|Windows")


def machine_translate(text, code, timeout=8, opener=None) -> str:
    """Переводит русский текст описания на язык code построчно. Имена файлов, DirectX, список языков и т.п.
    прячутся за метками {n}; если метка потерялась или пришла ошибка - возвращается '' (покажется другой вариант)."""
    import urllib.parse
    if not re.fullmatch(r"[a-z]{2,3}", str(code or "")) or code == "ru":
        return ""
    out = []
    try:
        for line in str(text or "").splitlines():
            if not line.strip():
                out.append("")
                continue
            keep = []

            def hide(m):
                keep.append(m.group(0))
                return "{%d}" % (len(keep) - 1)
            bullet = "- " if line.startswith("- ") else ""
            body = _PROTECT.sub(hide, line[len(bullet):])
            data = urllib.parse.urlencode({"client": "gtx", "sl": "ru", "tl": MT_CODES.get(code, code),
                                           "dt": "t", "q": body}).encode()
            req = urllib.request.Request(MT_URL, data=data, headers={"User-Agent": USER_AGENT})
            with (opener or urllib.request.urlopen)(req, timeout=timeout) as r:
                parts = json.loads(r.read().decode("utf-8"))[0]
            res = "".join(p[0] for p in parts if p and p[0])
            if not res.strip() or any("{%d}" % i not in res for i in range(len(keep))):
                return ""
            out.append(bullet + re.sub(r"\{(\d+)\}", lambda m: keep[int(m.group(1))], res))
    except Exception:                                       # noqa: BLE001
        return ""
    return "\n".join(out)


def mt_key(lang, tag, notes) -> str:
    return f"{lang}|{tag}|{hashlib.sha1(str(notes).encode('utf-8')).hexdigest()[:8]}"


def versions_api_url(settings=None) -> str:
    """Адрес API релизов с версиями Portabilizer: из настройки versions_repo ('владелец/репозиторий')."""
    spec = str((settings or {}).get("versions_repo") or "").strip().strip("/")
    owner, _, repo = spec.partition("/")
    if not (owner and repo and re.match(r"^[\w.-]+$", owner) and re.match(r"^[\w.-]+$", repo)):
        owner, repo = VERSIONS_OWNER, VERSIONS_REPO
    return API_URL.format(owner=owner, repo=repo)


def parse_launcher_release(data, current: str):
    """Самый новый релиз с тегом launcher-vX.Y, если он новее current. Иначе None."""
    best = None
    for r in data if isinstance(data, list) else []:
        if not isinstance(r, dict) or r.get("draft") or r.get("prerelease"):
            continue
        m = re.match(r"^(?:launcher-)?[vV](\d+(?:\.\d+)*)$", str(r.get("tag_name", "")))
        if not m:
            continue
        v = parse_version(m.group(1))
        if v > parse_version(current) and (best is None or v > best[0]):
            best = (v, {"tag": r["tag_name"], "version": m.group(1), "url": r.get("html_url", ""),
                        "notes": r.get("body") or ""})
    return best[1] if best else None


def check_launcher_update(current: str, timeout=15, opener=None):
    """Проверяет, вышла ли новая версия самого лаунчера. Любая ошибка -> None (не мешаем работе)."""
    try:
        with _open(API_URL.format(owner=OWNER, repo=REPO) + "?per_page=30", timeout, opener) as r:
            return parse_launcher_release(json.loads(r.read().decode("utf-8")), current)
    except Exception:                                       # noqa: BLE001
        return None


def _open(url, timeout=20, opener=None):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT,
                                               "Accept": "application/vnd.github+json"})
    return (opener or urllib.request.urlopen)(req, timeout=timeout)


def fetch_releases(url=None, timeout=20, opener=None, cache: Path = None) -> list:
    """Список релизов из GitHub. При ошибке сети берёт последний сохранённый список (если есть)."""
    url = url or API_URL.format(owner=OWNER, repo=REPO)
    try:
        with _open(url + ("&" if "?" in url else "?") + "per_page=100", timeout, opener) as r:
            raw = r.read().decode("utf-8")
        data = json.loads(raw)
        if cache:
            try:
                Path(cache).write_text(raw, encoding="utf-8")
            except OSError:
                pass
        return parse_releases(data)
    except Exception as e:                                  # noqa: BLE001 - сеть, JSON, лимиты
        if cache and Path(cache).is_file():
            try:
                rels = parse_releases(json.loads(Path(cache).read_text(encoding="utf-8")))
                if rels:
                    raise OfflineCache(str(e), rels)
            except (OSError, ValueError):
                pass
        raise


class OfflineCache(Exception):
    """Сеть недоступна, но есть сохранённый список: .releases - то, что показать."""

    def __init__(self, reason, releases):
        super().__init__(reason)
        self.reason, self.releases = reason, releases


# ------------------------------------------------------------------ установленные версии

def find_exe(folder: Path):
    """Portabilizer.exe в папке версии (допускаем одну вложенную папку, например dist)."""
    folder = Path(folder)
    for cand in [folder / EXE_NAME] + sorted(folder.glob(f"*/{EXE_NAME}")):
        if cand.is_file():
            return cand
    return None


def installed_versions(root: Path) -> dict:
    """{тег: папка} для всех установленных версий в папке root."""
    res = {}
    try:
        for d in sorted(Path(root).iterdir()):
            if d.is_dir() and not d.name.startswith((".", "_")) and find_exe(d):
                res[d.name] = d
    except OSError:
        pass
    return res


def merge_versions(releases: list, installed: dict) -> list:
    """Единый список: релизы из GitHub + версии, которые есть только на диске."""
    have = {r.tag for r in releases}
    out = list(releases)
    for tag in installed:
        if tag not in have:
            out.append(Release(tag=tag, name=tag, local=True))
    out.sort(key=lambda x: parse_version(x.tag), reverse=True)
    return out


# ------------------------------------------------------------------ скачивание и установка

def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url, dest: Path, progress=None, cancel=None, timeout=30, opener=None) -> str:
    """Скачивает url в dest, возвращает SHA-256. progress(получено, всего|0). cancel() -> bool."""
    h = hashlib.sha256()
    got = 0
    with _open(url, timeout, opener) as r, open(dest, "wb") as f:
        total = int(r.headers.get("Content-Length") or 0)
        while True:
            if cancel and cancel():
                raise Cancelled()
            chunk = r.read(256 * 1024)
            if not chunk:
                break
            f.write(chunk)
            h.update(chunk)
            got += len(chunk)
            if progress:
                progress(got, total)
    return h.hexdigest()


def safe_extract(zip_path, dest: Path):
    """Распаковка zip без выхода за пределы dest (защита от ../ и абсолютных путей)."""
    dest = Path(dest).resolve()
    with zipfile.ZipFile(zip_path) as z:
        for info in z.infolist():
            target = (dest / info.filename).resolve()
            if dest != target and dest not in target.parents:
                raise ValueError(tr("небезопасный путь в архиве: {name}", name=info.filename))
        z.extractall(dest)


def _expected_sha(rel: Release, opener=None) -> str:
    if rel.sha256:
        return rel.sha256
    if rel.sha_url:
        try:
            with _open(rel.sha_url, 15, opener) as r:
                text = r.read().decode("utf-8", "replace")
            for line in text.splitlines():            # формат "<sha>  <имя файла>" или одна сумма
                m = re.match(r"\s*([0-9a-fA-F]{64})(?:\s+\*?(.+))?", line)
                if m and (not m.group(2) or m.group(2).strip() == rel.asset_name):
                    return m.group(1).lower()
        except Exception:                           # noqa: BLE001
            pass
    return ""


def install_release(rel: Release, versions_dir: Path, progress=None, cancel=None, log=None,
                    opener=None) -> Path:
    """Скачивает, проверяет сумму и ставит версию в versions_dir/<тег>. Возвращает папку.
    Если в первом файле релиза нет программы (например, приложены исходники), пробует остальные."""
    log = log or (lambda m: None)
    if not rel.available:
        raise ValueError(tr("у этого релиза нет файла с программой (нужен zip с Portabilizer.exe или сам exe)"))
    cands = [rel] + [dataclasses.replace(rel, asset_name=a["name"], asset_url=a["url"],
                                          asset_size=a["size"], sha256=a["sha256"], sha_url=a["sha_url"],
                                          alts=[]) for a in rel.alts if a.get("url")]
    last = None
    for c in cands:
        try:
            return _install_asset(c, versions_dir, progress, cancel, log, opener)
        except NoExeInAsset as e:
            last = e
            log(tr("В файле {name} нет программы, смотрю другие файлы релиза...", name=c.asset_name))
    raise ValueError(tr("в релизе {tag} нет собранной программы ({exe}): приложены только файлы без неё. "
                        "Автору релиза нужно приложить готовый {exe} или zip с ним.",
                        tag=rel.tag, exe=EXE_NAME)) from last


class NoExeInAsset(ValueError):
    pass


def _install_asset(rel: Release, versions_dir: Path, progress, cancel, log, opener) -> Path:
    versions_dir = Path(versions_dir)
    versions_dir.mkdir(parents=True, exist_ok=True)
    final = versions_dir / rel.tag
    work = Path(tempfile.mkdtemp(prefix="_install_", dir=versions_dir))
    try:
        zpath = work / rel.asset_name
        log(tr("Скачиваю {name} ({size})...", name=rel.asset_name, size=fmt_size(rel.asset_size)))
        got = download(rel.asset_url, zpath, progress, cancel, opener=opener)
        want = _expected_sha(rel, opener)
        if want and got.lower() != want.lower():
            raise ValueError(tr("контрольная сумма не совпала: файл повреждён или подменён. Установка отменена."))
        log(tr("Контрольная сумма совпала.") if want else
            tr("Внимание: у релиза нет контрольной суммы, целостность не проверена."))
        stage = work / "unpacked"
        stage.mkdir()
        if zpath.name.lower().endswith(".exe"):          # приложен сам exe
            with open(zpath, "rb") as f:
                if f.read(2) != b"MZ":
                    raise NoExeInAsset(tr("это не exe-файл"))
            shutil.move(str(zpath), str(stage / EXE_NAME))
        else:
            safe_extract(zpath, stage)
            if not find_exe(stage):
                raise NoExeInAsset(tr("в архиве нет {exe}", exe=EXE_NAME))
        if final.exists():
            shutil.rmtree(final)
        shutil.move(str(stage), str(final))
        (final / ".installed.json").write_text(json.dumps(
            {"tag": rel.tag, "sha256": got, "installed": time.strftime("%Y-%m-%dT%H:%M:%S"),
             "channel": rel.channel}, ensure_ascii=False), encoding="utf-8")
        log(tr("Установлено: {p}", p=final))
        return final
    finally:
        shutil.rmtree(work, ignore_errors=True)


def import_local(path, versions_dir: Path, name: str = "") -> Path:
    """Добавляет свою версию из zip или exe (например, старую v7.3). Папка = name или имя файла."""
    p = Path(path)
    if not p.is_file():
        raise ValueError(tr("файл не найден"))
    versions_dir = Path(versions_dir)
    versions_dir.mkdir(parents=True, exist_ok=True)
    name = re.sub(r'[\\/:*?"<>|]+', "_", (name or p.stem).strip()) or "custom"
    final = versions_dir / name
    if final.exists():
        raise ValueError(tr("версия «{name}» уже есть", name=name))
    final.mkdir()
    try:
        if p.suffix.lower() == ".zip":
            safe_extract(p, final)
            if not find_exe(final):
                raise ValueError(tr("в архиве нет {exe}. Похоже, к релизу приложены исходники, а не собранная "
                                    "программа: соберите её через build.bat", exe=EXE_NAME))
        elif p.suffix.lower() == ".exe":
            shutil.copy2(p, final / EXE_NAME)
        else:
            raise ValueError(tr("нужен .zip или .exe"))
    except Exception:
        shutil.rmtree(final, ignore_errors=True)
        raise
    return final


def remove_version(folder: Path, versions_dir: Path):
    """Удаляет папку версии, только если она лежит внутри versions_dir."""
    folder, root = Path(folder).resolve(), Path(versions_dir).resolve()
    if root not in folder.parents:
        raise ValueError(tr("удалять можно только папки внутри папки версий"))
    shutil.rmtree(folder)


# ------------------------------------------------------------------ запуск

def build_command(exe: Path, radical: bool) -> list:
    return [str(exe)] + (["--r"] if radical else [])


def launch(exe: Path, radical: bool = False):
    """Запускает версию в отдельном окне. Папка версии - рабочая, чтобы настройки лежали там же."""
    exe = Path(exe)
    if not exe.is_file():
        raise FileNotFoundError(str(exe))
    kw = {}
    if os.name == "nt":
        kw["creationflags"] = 0x00000008 | 0x00000200   # DETACHED_PROCESS | NEW_PROCESS_GROUP
    return subprocess.Popen(build_command(exe, radical), cwd=str(exe.parent), close_fds=True, **kw)


# ------------------------------------------------------------------ ярлык на рабочем столе

def shortcut_ps(target, name, args="", workdir="", icon="") -> str:
    """Команда PowerShell, которая создаёт ярлык на рабочем столе (путь стола берёт у Windows,
    поэтому подходит и для русского «Рабочий стол», и для папки в OneDrive)."""
    esc = lambda v: str(v).replace("'", "''")                           # noqa: E731
    name = re.sub(r'[\\/:*?"<>|]+', "_", name).strip() or "Portabilizer Launcher"
    return ("$d=[Environment]::GetFolderPath('Desktop');"
            f"$p=Join-Path $d '{esc(name)}.lnk';"
            "$s=(New-Object -ComObject WScript.Shell).CreateShortcut($p);"
            f"$s.TargetPath='{esc(target)}';$s.Arguments='{esc(args)}';"
            f"$s.WorkingDirectory='{esc(workdir)}';"
            + (f"$s.IconLocation='{esc(icon)}';" if icon else "")
            + "$s.Save();Write-Output $p")


def version_shortcut_name(tag: str, radical: bool = False) -> str:
    """Имя ярлыка установленной версии: «Portabilizer v9.0» (для режима R - с пометкой R)."""
    return f"Portabilizer {tag}" + (" R" if radical else "")


def create_version_shortcut(exe, tag: str, radical: bool = False) -> str:
    """Ярлык на рабочем столе, который запускает именно эту версию (режим R - ключ --r).
    Значок берётся из самого exe, рабочая папка - папка версии, как при запуске из лаунчера."""
    exe = Path(exe)
    return create_desktop_shortcut(exe, version_shortcut_name(tag, radical), "--r" if radical else "",
                                   exe.parent, exe)


def create_desktop_shortcut(target, name="Portabilizer Launcher", args="", workdir=None, icon=None) -> str:
    """Создаёт ярлык на рабочем столе (только Windows). Возвращает путь к ярлыку."""
    if os.name != "nt":
        raise OSError(tr("ярлыки на рабочем столе поддерживаются только в Windows"))
    target = Path(target)
    ps = shortcut_ps(target, name, args, workdir or target.parent, icon or "")
    r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps],
                       capture_output=True, text=True, timeout=30, stdin=subprocess.DEVNULL,
                       creationflags=0x08000000)
    out = (r.stdout or "").strip().splitlines()
    if r.returncode != 0 or not out:
        raise OSError((r.stderr or r.stdout or tr("не удалось создать ярлык")).strip()[:300])
    return out[-1]
