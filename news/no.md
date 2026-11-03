# Hva er nytt i Portabilizer

## v9.1

- Grensesnittspråk: fanen "Språk" (med en globus), som i Windows-innstillinger: hvert språk vises med sitt eget navn, og under det står navnet på grensesnittspråket. Vinduet, tipsene, loggen, dialogene og historikken er oversatt. Når språket endres, starter vinduet på nytt; innstillingene beholdes
- Språk: 34 (русский, English, Eesti, Français, Español, Deutsch, Italiano, Português, Nederlands, Polski, Українська, Svenska, Suomi, Türkçe, 中文, 日本語, 한국어, العربية, Čeština, Română, Magyar, Ελληνικά, עברית, हिन्दी, Indonesia, Tiếng Việt, ไทย, Български, Српски, Hrvatski, Latviešu, Lietuvių, Norsk, Dansk)
- Ved første oppstart brukes Windows-språket (hvis det er blant de oversatte), ellers engelsk
- Filen portabilizer.log skrives fortsatt på russisk, noe som gjør det lettere å finne ut av feil

## v9.0

- Du trenger ikke installere biblioteker: programmet ser hvilke et spill eller en app trenger, og tilbyr å legge dem ved siden av exe (filene er bygd inn i Portabilizer)
- DirectX: juni 2010 og eldre utgaver fra 2005-2009 (d3dx9_24…43, d3dx10, XACT, XAudio, xinput) for gamle spill
- Visual C++ 2010, 2012, 2013 og 2015-2022, OpenAL (sammen med wrap_oal.dll)
- Cab-sett som programmet ikke kan lese selv, hoppes ikke lenger over: utpakkingen tas av expand.exe (Windows)
- Biblioteksettet bygges med skriptet tools/collect_redist.bat

## v8.9

- Modus R: en vanlig exe kopieres ikke lenger, men flyttes til mappen App. På én disk skjer det umiddelbart og krever ingen ekstra plass (før trengtes dobbelt så mye plass mens det pågikk)
- For arkiver og installasjonsprogrammer krever modus R fortsatt plass: de pakkes først ut, og først deretter slettes kilden. Du kan pakke ut til en annen disk via feltet "Til"
- Tipset og bekreftelsesvinduet for modus R er oppdatert
- Piksel-penneikoner (blå for vanlig versjon, røde for R) med temaet "Klassisk (system)"; andre temaer beholder de myke ikonene

## v8.8

- Oppdateringssjekk: programmet sjekker GitHub Releases selv og sier fra når en ny versjon er ute (kan slås av med avkrysningsboksen på fanen "Versjoner")
- Bedre samspill med Portabilizer Launcher: versjoner som liste, en "hva er nytt"-beskrivelse, installasjon med ett klikk

## v8.7

- Temaer: lys, mørk, røde temaer for modus R, velg din egen farge
- Automatisk søk etter installert 7-Zip
- DirectX-biblioteker inne i programmet (en dialog vises hvis et spill mangler dem)
- Start uten UAC-forespørsel for programmer som ber om administratorrettigheter
- Fjernet et duplisert minnetips
