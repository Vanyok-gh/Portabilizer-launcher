# Noutăți în Portabilizer

## v9.1

- Limba interfeței: o filă „Limbă” (cu un glob), ca în setările Windows: fiecare limbă este afișată cu numele ei, iar dedesubt apare numele în limba interfeței. Fereastra, indiciile, jurnalul, dialogurile și istoricul sunt traduse. La schimbarea limbii fereastra se repornește; setările sunt păstrate
- Limbi: 34 (русский, English, Eesti, Français, Español, Deutsch, Italiano, Português, Nederlands, Polski, Українська, Svenska, Suomi, Türkçe, 中文, 日本語, 한국어, العربية, Čeština, Română, Magyar, Ελληνικά, עברית, हिन्दी, Indonesia, Tiếng Việt, ไทย, Български, Српски, Hrvatski, Latviešu, Lietuvių, Norsk, Dansk)
- La prima pornire se folosește limba Windows (dacă se află printre cele traduse), altfel engleza
- Fișierul portabilizer.log se scrie în continuare în rusă, ceea ce ușurează depistarea erorilor

## v9.0

- Nu mai e nevoie să instalați biblioteci: programul vede de care are nevoie un joc sau o aplicație și propune să le pună lângă exe (fișierele sunt încorporate în Portabilizer)
- DirectX: versiunea June 2010 și versiunile mai vechi 2005-2009 (d3dx9_24…43, d3dx10, XACT, XAudio, xinput) pentru jocuri vechi
- Visual C++ 2010, 2012, 2013 și 2015-2022, OpenAL (împreună cu wrap_oal.dll)
- Seturile Cab pe care programul nu le poate citi singur nu mai sunt omise: extragerea o face expand.exe (Windows)
- Setul de biblioteci este construit cu scriptul tools/collect_redist.bat

## v8.9

- Mod R: un exe obișnuit nu mai este copiat, ci mutat în folderul App. Pe același disc este instantaneu și nu cere spațiu suplimentar (înainte era nevoie de dublul spațiului pe durata lucrului)
- Pentru arhive și programe de instalare, Mod R tot are nevoie de spațiu: acestea se extrag mai întâi, abia apoi sursa este ștearsă. Puteți extrage pe alt disc folosind câmpul „Destinație”
- Indiciul și fereastra de confirmare pentru Mod R au fost actualizate
- Pictograme cu stilou în stil pixel (albastre pentru versiunea obișnuită, roșii pentru R) cu tema „Clasică (de sistem)”; celelalte teme păstrează pictogramele fine

## v8.8

- Verificarea actualizărilor: programul verifică singur GitHub Releases și anunță când apare o versiune nouă (poate fi dezactivată din caseta de pe fila „Versiuni”)
- Funcționează mai bine cu Portabilizer Launcher: versiuni într-o listă, descriere „noutăți”, instalare dintr-un clic

## v8.7

- Teme: luminoasă, întunecată, teme roșii pentru Mod R, alegerea propriei culori
- Căutare automată a unui 7-Zip instalat
- Biblioteci DirectX în interiorul programului (apare un dialog dacă unui joc îi lipsesc)
- Pornire fără solicitarea UAC pentru programele care cer drepturi de administrator
- Eliminat un indiciu duplicat despre memorie
