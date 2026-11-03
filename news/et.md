# Mis on Portabilizeris uut

## v9.1

- Liidese keel: vahekaart "Keel" (gloobusega), nagu Windowsi sätetes: iga keel on näidatud oma nimega ja selle all nimi liidese keeles. Aken, vihjed, logi, dialoogid ja ajalugu on tõlgitud. Keele vahetamisel aken taaskäivitub; sätted säilivad
- Keeled: 34 (русский, English, Eesti, Français, Español, Deutsch, Italiano, Português, Nederlands, Polski, Українська, Svenska, Suomi, Türkçe, 中文, 日本語, 한국어, العربية, Čeština, Română, Magyar, Ελληνικά, עברית, हिन्दी, Indonesia, Tiếng Việt, ไทย, Български, Српски, Hrvatski, Latviešu, Lietuvių, Norsk, Dansk)
- Esimesel käivitamisel kasutatakse Windowsi keelt (kui see on tõlgitute hulgas), muidu inglise keelt
- Fail portabilizer.log kirjutatakse endiselt vene keeles, mis teeb vigade analüüsi lihtsamaks

## v9.0

- Teeke pole vaja installida: programm näeb, mida mäng või rakendus vajab, ja pakub need exe kõrvale panna (failid on Portabilizerisse sisse ehitatud)
- DirectX: juuni 2010 ja vanemad 2005-2009 väljalasked (d3dx9_24…43, d3dx10, XACT, XAudio, xinput) vanade mängude jaoks
- Visual C++ 2010, 2012, 2013 ja 2015-2022, OpenAL (koos wrap_oal.dll-iga)
- Cab-komplekte, mida programm ise lugeda ei oska, enam vahele ei jäeta: lahtipakkimise teeb expand.exe (Windows)
- Teekide komplekt koostatakse skriptiga tools/collect_redist.bat

## v8.9

- Režiim R: tavalist exe-faili enam ei kopeerita, vaid teisaldatakse kausta App. Ühel kettal on see hetkeline ega vaja lisaruumi (varem oli töö ajal vaja kahekordset ruumi)
- Arhiivide ja installerite puhul vajab režiim R siiski ruumi: need pakitakse kõigepealt lahti ja alles siis kustutatakse algfail. Saad lahti pakkida teisele kettale, kasutades välja "Kuhu"
- Režiimi R vihjet ja kinnitusakent uuendati
- Pikslilised pliiatsiikoonid (sinine tavaversioonile, punane režiimile R) teemaga "Klassikaline (süsteemne)"; teised teemad jätavad siledad ikoonid

## v8.8

- Uuenduste kontroll: programm kontrollib ise GitHub Releases'i ja teatab, kui ilmub uus versioon (saab välja lülitada vahekaardil "Versioonid" märkeruuduga)
- Töötab paremini koos Portabilizer Launcheriga: versioonid loendina, kirjeldus "mis on uut", paigaldus ühe klõpsuga

## v8.7

- Teemad: hele, tume, punased teemad režiimile R, vali oma värv
- Installitud 7-Zipi automaatne otsing
- DirectX-i teegid programmi sees (kui mängul neid pole, ilmub dialoog)
- Käivitamine ilma UAC-i päringuta programmidele, mis nõuavad administraatoriõigusi
- Eemaldatud korduv mälu vihje
