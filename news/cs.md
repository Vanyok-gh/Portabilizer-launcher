# Co je nového v Portabilizeru

## v9.1

- Jazyk rozhraní: karta „Jazyk“ (se zeměkoulí), stejně jako v nastavení Windows: každý jazyk je zobrazen svým vlastním názvem a pod ním jeho název v jazyce rozhraní. Okno, nápovědy, log, dialogy i historie jsou přeloženy. Po změně jazyka se okno restartuje, vaše nastavení zůstanou zachována
- Jazyků: 34 (русский, English, Eesti, Français, Español, Deutsch, Italiano, Português, Nederlands, Polski, Українська, Svenska, Suomi, Türkçe, 中文, 日本語, 한국어, العربية, Čeština, Română, Magyar, Ελληνικά, עברית, हिन्दी, Indonesia, Tiếng Việt, ไทย, Български, Српски, Hrvatski, Latviešu, Lietuvių, Norsk, Dansk)
- Při prvním spuštění se použije jazyk Windows (pokud je mezi přeloženými), jinak angličtina
- Soubor portabilizer.log se stále zapisuje rusky, což usnadňuje hledání chyb

## v9.0

- Není třeba instalovat knihovny: program sám pozná, které hra nebo aplikace potřebuje, a nabídne je umístit vedle exe (soubory jsou součástí Portabilizeru)
- DirectX: vydání June 2010 a starší vydání 2005-2009 (d3dx9_24…43, d3dx10, XACT, XAudio, xinput) pro staré hry
- Visual C++ 2010, 2012, 2013 a 2015-2022, OpenAL (spolu s wrap_oal.dll)
- Sady Cab, které program neumí přečíst sám, se už nepřeskakují: rozbalení zajistí expand.exe (Windows)
- Sada knihoven se sestavuje skriptem tools/collect_redist.bat

## v8.9

- Režim R: běžný exe se už nekopíruje, ale přesouvá do složky App. Na jednom disku je to okamžité a nepotřebuje místo navíc (dříve bylo během práce potřeba dvojnásobné místo)
- U archivů a instalátorů Režim R stále potřebuje místo: nejprve se rozbalí a teprve poté se zdroj smaže. Rozbalit lze na jiný disk pomocí pole „Kam“
- Nápověda a potvrzovací okno Režimu R byly aktualizovány
- Pixelové ikony pera (modré pro běžnou verzi, červené pro R) s motivem „Klasické (systémové)“; ostatní motivy mají hladké ikony

## v8.8

- Kontrola aktualizací: program sám kontroluje GitHub Releases a oznámí, že vyšla nová verze (lze vypnout zaškrtávátkem na kartě „Verze“)
- Lepší spolupráce s Portabilizer Launcher: verze v seznamu, popis „co je nového“, instalace jedním kliknutím

## v8.7

- Motivy: světlý, tmavý, červené motivy pro Režim R, volba vlastní barvy
- Automatické vyhledání nainstalovaného 7-Zip
- Knihovny DirectX uvnitř programu (pokud je hře chybí, zobrazí se dialog)
- Spuštění bez výzvy UAC pro programy, které žádají práva správce
- Odstraněna duplicitní nápověda o paměti
