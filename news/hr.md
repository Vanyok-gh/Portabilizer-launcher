# Što je novo u Portabilizeru

## v9.1

- Jezik sučelja: kartica "Jezik" (sa globusom), kao u postavkama Windowsa: svaki je jezik prikazan svojim imenom, a ispod njega je ime na jeziku sučelja. Prozor, savjeti, zapisnik, dijalozi i povijest su prevedeni. Pri promjeni jezika prozor se ponovno pokreće; postavke se čuvaju
- Jezici: 34 (русский, English, Eesti, Français, Español, Deutsch, Italiano, Português, Nederlands, Polski, Українська, Svenska, Suomi, Türkçe, 中文, 日本語, 한국어, العربية, Čeština, Română, Magyar, Ελληνικά, עברית, हिन्दी, Indonesia, Tiếng Việt, ไทย, Български, Српски, Hrvatski, Latviešu, Lietuvių, Norsk, Dansk)
- Pri prvom pokretanju koristi se jezik Windowsa (ako je među prevedenima), inače engleski
- Datoteka portabilizer.log i dalje se piše na ruskom, što olakšava razumijevanje pogrešaka

## v9.0

- Nije potrebno instalirati biblioteke: program vidi koje treba igra ili aplikacija i nudi da ih stavi pored exe (datoteke su ugrađene u Portabilizer)
- DirectX: lipanj 2010 i starija izdanja 2005-2009 (d3dx9_24…43, d3dx10, XACT, XAudio, xinput) za stare igre
- Visual C++ 2010, 2012, 2013 i 2015-2022, OpenAL (zajedno s wrap_oal.dll)
- Cab skupovi koje program ne može sam pročitati više se ne preskaču: raspakiravanje obavlja expand.exe (Windows)
- Skup biblioteka gradi se skriptom tools/collect_redist.bat

## v8.9

- Način R: običan exe više se ne kopira, nego premješta u mapu App. Na jednom disku to je trenutno i ne traži dodatan prostor (prije je tijekom rada trebalo dvostruko više prostora)
- Za arhive i instalacijske programe način R i dalje traži prostor: prvo se raspakiraju, a tek zatim se izvor briše. Možete raspakirati na drugi disk putem polja "Kamo"
- Savjet i prozor potvrde načina R su ažurirani
- Pikselne ikone olovke (plava za običnu verziju, crvena za R) uz temu "Klasična (sustavna)"; ostale teme zadržavaju glatke ikone

## v8.8

- Provjera ažuriranja: program sam provjerava GitHub Releases i javlja kad izađe nova verzija (može se isključiti potvrdnim okvirom na kartici "Verzije")
- Bolji rad s Portabilizer Launcherom: verzije kao popis, opis "što je novo", instalacija jednim klikom

## v8.7

- Teme: svijetla, tamna, crvene teme za način R, odabir vlastite boje
- Automatsko traženje instaliranog 7-Zipa
- DirectX biblioteke unutar programa (ako igri nedostaju, pojavljuje se dijalog)
- Pokretanje bez UAC upita za programe koji traže administratorska prava
- Uklonjen je dupli savjet o memoriji
