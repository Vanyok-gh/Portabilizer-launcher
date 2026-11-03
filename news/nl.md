# Nieuw in Portabilizer

## v9.1

- Interfacetaal: een tabblad "Taal" (met een wereldbol), zoals in de instellingen van Windows: elke taal wordt getoond met zijn eigen naam en daaronder de naam in de taal van de interface. Het venster, de hints, het logboek, de dialoogvensters en de geschiedenis zijn vertaald. Bij het wisselen van taal start het venster opnieuw op; uw instellingen blijven behouden
- Talen: 34 (русский, English, Eesti, Français, Español, Deutsch, Italiano, Português, Nederlands, Polski, Українська, Svenska, Suomi, Türkçe, 中文, 日本語, 한국어, العربية, Čeština, Română, Magyar, Ελληνικά, עברית, हिन्दी, Indonesia, Tiếng Việt, ไทย, Български, Српски, Hrvatski, Latviešu, Lietuvių, Norsk, Dansk)
- Bij de eerste start wordt de taal van Windows gebruikt (als die tussen de vertaalde talen zit), anders Engels
- Het bestand portabilizer.log wordt nog steeds in het Russisch geschreven, wat het uitzoeken van fouten makkelijker maakt

## v9.0

- Bibliotheken hoeven niet meer geïnstalleerd te worden: het programma ziet welke een spel of app nodig heeft en stelt voor ze naast de exe te plaatsen (de bestanden zijn in Portabilizer ingebouwd)
- DirectX: juni 2010 en oudere releases 2005-2009 (d3dx9_24…43, d3dx10, XACT, XAudio, xinput) voor oude spellen
- Visual C++ 2010, 2012, 2013 en 2015-2022, OpenAL (samen met wrap_oal.dll)
- Cab-sets die het programma zelf niet kan lezen worden niet meer overgeslagen: het uitpakken wordt door expand.exe gedaan (Windows)
- De bibliotheekset wordt gebouwd met het script tools/collect_redist.bat

## v8.9

- Modus R: een gewone exe wordt niet meer gekopieerd maar verplaatst naar de map App. Op één schijf gaat dat direct en is er geen extra ruimte nodig (eerder was tijdens het werk twee keer zoveel ruimte nodig)
- Voor archieven en installatieprogramma's heeft modus R nog steeds ruimte nodig: ze worden eerst uitgepakt en pas daarna wordt de bron verwijderd. U kunt naar een andere schijf uitpakken via het veld "Naar"
- De hint en het bevestigingsvenster van modus R zijn bijgewerkt
- Pixelpotlood-pictogrammen (blauw voor de gewone versie, rood voor R) bij het thema "Klassiek (systeem)"; andere thema's houden gladde pictogrammen

## v8.8

- Updatecontrole: het programma controleert zelf GitHub Releases en meldt wanneer er een nieuwe versie is (uit te schakelen met het selectievakje op het tabblad "Versies")
- Werkt beter samen met Portabilizer Launcher: versies als lijst, beschrijving van wat er nieuw is, installatie met één klik

## v8.7

- Thema's: licht, donker, rode thema's voor modus R, kies uw eigen kleur
- Automatisch zoeken naar een geïnstalleerde 7-Zip
- DirectX-bibliotheken in het programma (er verschijnt een dialoogvenster als een spel ze mist)
- Starten zonder UAC-melding voor programma's die beheerdersrechten vragen
- Dubbele geheugenhint verwijderd
