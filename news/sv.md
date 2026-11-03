# Nytt i Portabilizer

## v9.1

- Gränssnittsspråk: fliken "Språk" (med en jordglob), som i Windows-inställningarna: varje språk visas med sitt eget namn och under det namnet på gränssnittsspråket. Fönstret, tipsen, loggen, dialogrutorna och historiken är översatta. När du byter språk startas fönstret om; dina inställningar behålls
- Språk: 34 (русский, English, Eesti, Français, Español, Deutsch, Italiano, Português, Nederlands, Polski, Українська, Svenska, Suomi, Türkçe, 中文, 日本語, 한국어, العربية, Čeština, Română, Magyar, Ελληνικά, עברית, हिन्दी, Indonesia, Tiếng Việt, ไทย, Български, Српски, Hrvatski, Latviešu, Lietuvių, Norsk, Dansk)
- Vid första starten används Windows-språket (om det finns bland de översatta), annars engelska
- Filen portabilizer.log skrivs fortfarande på ryska, vilket gör det lättare att reda ut fel

## v9.0

- Inget behov av att installera bibliotek: programmet ser vilka som behövs för ett spel eller en app och erbjuder sig att lägga dem bredvid exe-filen (filerna är inbyggda i Portabilizer)
- DirectX: juni 2010 och äldre utgåvor från 2005-2009 (d3dx9_24…43, d3dx10, XACT, XAudio, xinput) för gamla spel
- Visual C++ 2010, 2012, 2013 och 2015-2022, OpenAL (tillsammans med wrap_oal.dll)
- Cab-uppsättningar som programmet inte kan läsa själv hoppas inte längre över: uppackningen sköts av expand.exe (Windows)
- Biblioteksuppsättningen byggs av skriptet tools/collect_redist.bat

## v8.9

- Läge R: en vanlig exe kopieras inte längre utan flyttas till mappen App. På en och samma enhet går det direkt och kräver inget extra utrymme (förut behövdes dubbelt så mycket utrymme medan det pågick)
- För arkiv och installationsprogram kräver läge R fortfarande utrymme: de packas först upp och först därefter tas källan bort. Du kan packa upp till en annan enhet med fältet "Till"
- Tipset och bekräftelsefönstret för läge R har uppdaterats
- Pennikoner i pixelstil (blå för den vanliga versionen, röda för R) med temat "Klassiskt (system)"; andra teman behåller mjuka ikoner

## v8.8

- Uppdateringskontroll: programmet kontrollerar GitHub Releases själv och talar om när en ny version finns (kan stängas av med kryssrutan på fliken "Versioner")
- Fungerar bättre med Portabilizer Launcher: versioner som lista, en beskrivning av "nytt", installation med ett klick

## v8.7

- Teman: ljust, mörkt, röda teman för läge R, välj en egen färg
- Automatisk sökning efter ett installerat 7-Zip
- DirectX-bibliotek inuti programmet (en dialogruta visas om ett spel saknar dem)
- Start utan UAC-fråga för program som begär administratörsrättigheter
- En dubblerad minnesnotis har tagits bort
