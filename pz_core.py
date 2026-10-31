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

OWNER, REPO = "Vanyok-gh", "portabilizer-launcher"          # репозиторий самого лаунчера
# откуда брать версии Portabilizer: пока тот же репозиторий; когда появится отдельный
# (например Vanyok-gh/Portabilizer), достаточно поменять эту строку или параметр versions_repo в настройках
VERSIONS_OWNER, VERSIONS_REPO = "Vanyok-gh", "portabilizer-launcher"
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
            return f"{n:.0f} {unit}" if unit == "Б" else f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} ГБ"


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

    @property
    def channel(self) -> str:
        return "Beta" if self.prerelease else "Stable"

    @property
    def available(self) -> bool:
        return bool(self.asset_url)


def pick_asset(assets: list, tag: str = ""):
    """Выбирает zip с программой. Сначала с 'portabilizer' в имени, затем любой zip."""
    zips = [a for a in assets or [] if str(a.get("name", "")).lower().endswith(".zip")]
    if not zips:
        return None
    zips.sort(key=lambda a: (("portabilizer" not in a["name"].lower()),
                             ("x64" not in a["name"].lower() and "win" not in a["name"].lower()),
                             a["name"].lower()))
    return zips[0]


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
        a = pick_asset(assets, r["tag_name"])
        sha, sha_url = _sha_from(a, assets, r.get("body") or "") if a else ("", "")
        out.append(Release(
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


def fill_notes_from_changelog(releases, text: str):
    """Подставляет описание из CHANGELOG тем релизам, у которых оно пустое."""
    log = parse_changelog(text)
    for r in releases:
        if not (r.notes or "").strip():
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
        m = re.match(r"^launcher-v(\d+(?:\.\d+)*)$", str(r.get("tag_name", "")))
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
                raise ValueError(f"небезопасный путь в архиве: {info.filename}")
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
    """Скачивает, проверяет сумму и ставит версию в versions_dir/<тег>. Возвращает папку."""
    log = log or (lambda m: None)
    if not rel.available:
        raise ValueError("у этого релиза нет zip-файла с программой")
    versions_dir = Path(versions_dir)
    versions_dir.mkdir(parents=True, exist_ok=True)
    final = versions_dir / rel.tag
    work = Path(tempfile.mkdtemp(prefix="_install_", dir=versions_dir))
    try:
        zpath = work / rel.asset_name
        log(f"Скачиваю {rel.asset_name} ({fmt_size(rel.asset_size)})...")
        got = download(rel.asset_url, zpath, progress, cancel, opener=opener)
        want = _expected_sha(rel, opener)
        if want and got.lower() != want.lower():
            raise ValueError("контрольная сумма не совпала: файл повреждён или подменён. "
                             "Установка отменена.")
        log("Контрольная сумма совпала." if want else
            "Внимание: у релиза нет контрольной суммы, целостность не проверена.")
        stage = work / "unpacked"
        stage.mkdir()
        safe_extract(zpath, stage)
        if not find_exe(stage):
            raise ValueError(f"в архиве нет {EXE_NAME}. Похоже, к релизу приложены исходники, а не "
                             f"собранная программа: соберите её через build.bat и приложите "
                             f"zip с {EXE_NAME} (как у v8.7)")
        if final.exists():
            shutil.rmtree(final)
        shutil.move(str(stage), str(final))
        (final / ".installed.json").write_text(json.dumps(
            {"tag": rel.tag, "sha256": got, "installed": time.strftime("%Y-%m-%dT%H:%M:%S"),
             "channel": rel.channel}, ensure_ascii=False), encoding="utf-8")
        log(f"Установлено: {final}")
        return final
    finally:
        shutil.rmtree(work, ignore_errors=True)


def import_local(path, versions_dir: Path, name: str = "") -> Path:
    """Добавляет свою версию из zip или exe (например, старую v7.3). Папка = name или имя файла."""
    p = Path(path)
    if not p.is_file():
        raise ValueError("файл не найден")
    versions_dir = Path(versions_dir)
    versions_dir.mkdir(parents=True, exist_ok=True)
    name = re.sub(r'[\\/:*?"<>|]+', "_", (name or p.stem).strip()) or "custom"
    final = versions_dir / name
    if final.exists():
        raise ValueError(f"версия «{name}» уже есть")
    final.mkdir()
    try:
        if p.suffix.lower() == ".zip":
            safe_extract(p, final)
            if not find_exe(final):
                raise ValueError(f"в архиве нет {EXE_NAME}. Похоже, к релизу приложены исходники, "
                                 f"а не собранная программа: соберите её через build.bat")
        elif p.suffix.lower() == ".exe":
            shutil.copy2(p, final / EXE_NAME)
        else:
            raise ValueError("нужен .zip или .exe")
    except Exception:
        shutil.rmtree(final, ignore_errors=True)
        raise
    return final


def remove_version(folder: Path, versions_dir: Path):
    """Удаляет папку версии, только если она лежит внутри versions_dir."""
    folder, root = Path(folder).resolve(), Path(versions_dir).resolve()
    if root not in folder.parents:
        raise ValueError("удалять можно только папки внутри папки версий")
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


def create_desktop_shortcut(target, name="Portabilizer Launcher", args="", workdir=None, icon=None) -> str:
    """Создаёт ярлык на рабочем столе (только Windows). Возвращает путь к ярлыку."""
    if os.name != "nt":
        raise OSError("ярлыки на рабочем столе поддерживаются только в Windows")
    target = Path(target)
    ps = shortcut_ps(target, name, args, workdir or target.parent, icon or "")
    r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps],
                       capture_output=True, text=True, timeout=30, stdin=subprocess.DEVNULL,
                       creationflags=0x08000000)
    out = (r.stdout or "").strip().splitlines()
    if r.returncode != 0 or not out:
        raise OSError((r.stderr or r.stdout or "не удалось создать ярлык").strip()[:300])
    return out[-1]
