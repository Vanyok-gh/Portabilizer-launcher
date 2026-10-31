"""Самообновление лаунчера, отдельный репозиторий версий, иконки. Запуск: python tests/test_launcher_update.py"""
import sys, io, json, base64, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pz_core as C, pz_icons, launcher as L
n = 0
def check(c, m):
    global n; assert c, "ПРОВАЛ: " + m; n += 1

# адрес репозитория версий
check(C.versions_api_url({}).endswith("/Vanyok-gh/portabilizer-launcher/releases"), "по умолчанию")
check(C.versions_api_url({"versions_repo": "Vanyok-gh/Portabilizer"}).endswith("/Vanyok-gh/Portabilizer/releases"), "свой репозиторий")
check(C.versions_api_url({"versions_repo": "плохо//../x y"}).endswith("/portabilizer-launcher/releases"), "мусор -> по умолчанию")

data = [{"tag_name": "launcher-v0.4", "html_url": "http://r/0.4", "body": "n"},
        {"tag_name": "launcher-v0.10", "html_url": "http://r/0.10"},
        {"tag_name": "launcher-v0.3"},
        {"tag_name": "launcher-v0.9", "prerelease": True}, {"tag_name": "launcher-v0.11", "draft": True}]
r = C.parse_launcher_release(data, "0.3")
check(r and r["version"] == "0.10", f"0.10 новее 0.4 (числовое сравнение): {r}")
check(C.parse_launcher_release(data, "0.10") is None, "уже последняя")
check(C.parse_launcher_release("мусор", "0.1") is None, "мусор")

class Resp(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *a): return False
def opener(payload):
    def f(req, timeout=0):
        if isinstance(payload, Exception): raise payload
        return Resp(json.dumps(payload).encode())
    return f
check(C.check_launcher_update("0.3", opener=opener(data))["version"] == "0.10", "через сеть")
check(C.check_launcher_update("0.3", opener=opener(OSError("нет сети"))) is None, "ошибка сети не мешает")

tmp = Path(tempfile.mkdtemp())
mix = data + [{"tag_name": "v8.9", "assets": [{"name": "Portabilizer-v8.9.zip", "browser_download_url": "http://x", "size": 1}]}]
m = L.Model({"versions_dir": str(tmp / "v")}, opener=opener(mix), cache=tmp / "c.json")
m.refresh()
check(m.launcher_new and m.launcher_new["version"] == "0.10", "Model.refresh видит новый лаунчер")
check([x.tag for x in m.releases] == ["v8.9"], "launcher-теги не попадают в список версий")

# иконки
from PIL import Image
for k in ("smooth64", "smooth32", "pixel64", "pixel32"):
    im = Image.open(io.BytesIO(base64.b64decode(pz_icons.ICONS[k]))).convert("RGBA")
    check(im.size == (int(k[-2:]),) * 2 and im.getpixel((0, 0))[3] == 0, f"{k}: размер и прозрачный угол")
print(f"самообновление и иконки: {n} проверок пройдено")
