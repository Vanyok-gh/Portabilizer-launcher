# Kas jauns Portabilizer

## v9.1

- Interfeisa valoda: cilne "Valoda" (ar globusu), tāpat kā Windows iestatījumos: katra valoda parādīta ar savu nosaukumu, bet zem tā ir nosaukums interfeisa valodā. Logs, padomi, žurnāls, dialogi un vēsture ir tulkoti. Mainot valodu, logs tiek pārstartēts; iestatījumi tiek saglabāti
- Valodas: 34 (русский, English, Eesti, Français, Español, Deutsch, Italiano, Português, Nederlands, Polski, Українська, Svenska, Suomi, Türkçe, 中文, 日本語, 한국어, العربية, Čeština, Română, Magyar, Ελληνικά, עברית, हिन्दी, Indonesia, Tiếng Việt, ไทย, Български, Српски, Hrvatski, Latviešu, Lietuvių, Norsk, Dansk)
- Pirmajā palaišanas reizē tiek izmantota Windows valoda (ja tā ir starp tulkotajām), citādi angļu valoda
- Fails portabilizer.log joprojām tiek rakstīts krieviski, kas atvieglo kļūdu izpēti

## v9.0

- Bibliotēkas nav jāinstalē: programma redz, kuras vajadzīgas spēlei vai lietotnei, un piedāvā tās novietot blakus exe (faili ir iebūvēti Portabilizer)
- DirectX: 2010. gada jūnijs un vecākie 2005-2009 izlaidumi (d3dx9_24…43, d3dx10, XACT, XAudio, xinput) vecām spēlēm
- Visual C++ 2010, 2012, 2013 un 2015-2022, OpenAL (kopā ar wrap_oal.dll)
- Cab komplekti, ko programma pati nevar nolasīt, vairs netiek izlaisti: izvilkšanu veic expand.exe (Windows)
- Bibliotēku komplekts tiek veidots ar skriptu tools/collect_redist.bat

## v8.9

- Režīms R: parasts exe vairs netiek kopēts, bet pārvietots uz mapi App. Vienā diskā tas notiek acumirklī un nav vajadzīga papildu vieta (agrāk darbības laikā bija vajadzīga divkārša vieta)
- Arhīviem un instalētājiem režīmam R vēl joprojām vajadzīga vieta: tie vispirms tiek izpakoti un tikai pēc tam avots tiek dzēsts. Izpakot var uz citu disku, izmantojot lauku "Kur"
- Režīma R padoms un apstiprinājuma logs ir atjaunināti
- Pikseļu pildspalvas ikonas (zilas parastajai versijai, sarkanas R) ar tēmu "Klasiskā (sistēmas)"; citas tēmas saglabā gludās ikonas

## v8.8

- Atjauninājumu pārbaude: programma pati pārbauda GitHub Releases un paziņo, kad iznākusi jauna versija (var izslēgt ar izvēles rūtiņu cilnē "Versijas")
- Labāka sadarbība ar Portabilizer Launcher: versijas sarakstā, apraksts "kas jauns", instalēšana ar vienu klikšķi

## v8.7

- Tēmas: gaišā, tumšā, sarkanās tēmas režīmam R, savas krāsas izvēle
- Automātiska instalētā 7-Zip meklēšana
- DirectX bibliotēkas programmas iekšienē (ja spēlei to trūkst, parādās dialogs)
- Palaišana bez UAC pieprasījuma programmām, kas prasa administratora tiesības
- Noņemts dublētais atmiņas padoms
