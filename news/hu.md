# Újdonságok a Portabilizerben

## v9.1

- Felület nyelve: „Nyelv” lap (földgömbbel), mint a Windows beállításaiban: minden nyelv a saját nevén jelenik meg, alatta a neve a felület nyelvén. Az ablak, a súgók, a napló, a párbeszédablakok és az előzmények le vannak fordítva. A nyelv váltásakor az ablak újraindul; a beállítások megmaradnak
- Nyelvek: 34 (русский, English, Eesti, Français, Español, Deutsch, Italiano, Português, Nederlands, Polski, Українська, Svenska, Suomi, Türkçe, 中文, 日本語, 한국어, العربية, Čeština, Română, Magyar, Ελληνικά, עברית, हिन्दी, Indonesia, Tiếng Việt, ไทย, Български, Српски, Hrvatski, Latviešu, Lietuvių, Norsk, Dansk)
- Első indításkor a Windows nyelvét használja (ha szerepel a fordítottak között), különben az angolt
- A portabilizer.log fájl továbbra is oroszul készül, így könnyebb kiszűrni a hibákat

## v9.0

- Nem kell könyvtárakat telepíteni: a program látja, melyekre van szüksége egy játéknak vagy alkalmazásnak, és felajánlja, hogy az exe mellé teszi őket (a fájlok be vannak építve a Portabilizerbe)
- DirectX: a June 2010 kiadás és a régebbi 2005-2009 kiadások (d3dx9_24…43, d3dx10, XACT, XAudio, xinput) régi játékokhoz
- Visual C++ 2010, 2012, 2013 és 2015-2022, OpenAL (a wrap_oal.dll-lel együtt)
- Azokat a Cab készleteket, amelyeket a program maga nem tud olvasni, már nem hagyja ki: a kicsomagolást az expand.exe végzi (Windows)
- A könyvtárkészletet a tools/collect_redist.bat szkript állítja össze

## v8.9

- R mód: a szokásos exe-t már nem másolja, hanem áthelyezi az App mappába. Egy lemezen ez azonnali, és nem kell hozzá extra hely (korábban futás közben kétszeres helyre volt szükség)
- Archívumoknál és telepítőknél az R módnak továbbra is kell hely: először kicsomagolja őket, és csak utána törli a forrást. Másik lemezre is kicsomagolhat a „Hová” mező segítségével
- Az R mód súgója és megerősítő ablaka frissült
- Pixeles tollikonok (kék a szokásos verzióhoz, piros az R-hez) a „Klasszikus (rendszer)” témával; a többi téma sima ikonokat tart meg

## v8.8

- Frissítésellenőrzés: a program maga ellenőrzi a GitHub Releases oldalt, és szól, ha új verzió jelent meg (a „Verziók” lapon a jelölőnégyzettel kikapcsolható)
- Jobb együttműködés a Portabilizer Launcherrel: verziók listában, „újdonságok” leírás, telepítés egy kattintással

## v8.7

- Témák: világos, sötét, piros témák az R módhoz, saját szín választása
- A telepített 7-Zip automatikus keresése
- DirectX könyvtárak a programon belül (ha egy játékból hiányoznak, párbeszédablak jelenik meg)
- Indítás UAC-kérés nélkül a rendszergazdai jogot kérő programokhoz
- Egy duplikált memóriasúgó eltávolítva
