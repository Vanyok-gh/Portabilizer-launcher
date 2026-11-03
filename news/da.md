# Nyheder i Portabilizer

## v9.1

- Grænsefladesprog: fanen "Sprog" (med en globus), som i Windows-indstillinger: hvert sprog vises med sit eget navn, og under det står navnet på grænsefladesproget. Vinduet, tips, loggen, dialogerne og historikken er oversat. Når sproget skiftes, genstarter vinduet; dine indstillinger bevares
- Sprog: 34 (русский, English, Eesti, Français, Español, Deutsch, Italiano, Português, Nederlands, Polski, Українська, Svenska, Suomi, Türkçe, 中文, 日本語, 한국어, العربية, Čeština, Română, Magyar, Ελληνικά, עברית, हिन्दी, Indonesia, Tiếng Việt, ไทย, Български, Српски, Hrvatski, Latviešu, Lietuvių, Norsk, Dansk)
- Ved første start bruges Windows-sproget (hvis det er blandt de oversatte), ellers engelsk
- Filen portabilizer.log skrives stadig på russisk, hvilket gør det nemmere at finde ud af fejl

## v9.0

- Du behøver ikke installere biblioteker: programmet ser, hvilke et spil eller en app har brug for, og tilbyder at lægge dem ved siden af exe (filerne er indbygget i Portabilizer)
- DirectX: juni 2010 og ældre udgaver fra 2005-2009 (d3dx9_24…43, d3dx10, XACT, XAudio, xinput) til gamle spil
- Visual C++ 2010, 2012, 2013 og 2015-2022, OpenAL (sammen med wrap_oal.dll)
- Cab-sæt, som programmet ikke selv kan læse, springes ikke længere over: udpakningen klares af expand.exe (Windows)
- Bibliotekssættet bygges med scriptet tools/collect_redist.bat

## v8.9

- Tilstand R: en almindelig exe kopieres ikke længere, men flyttes til mappen App. På ét drev sker det øjeblikkeligt og kræver ingen ekstra plads (før krævedes dobbelt plads, mens det kørte)
- Til arkiver og installationsprogrammer kræver tilstand R stadig plads: de pakkes først ud, og først derefter slettes kilden. Du kan pakke ud til et andet drev via feltet "Til"
- Tippet og bekræftelsesvinduet for tilstand R er opdateret
- Pixel-penneikoner (blå til den almindelige version, røde til R) med temaet "Klassisk (system)"; andre temaer beholder de bløde ikoner

## v8.8

- Opdateringstjek: programmet tjekker selv GitHub Releases og giver besked, når en ny version er udkommet (kan slås fra med afkrydsningsfeltet på fanen "Versioner")
- Bedre samspil med Portabilizer Launcher: versioner som liste, en "nyheder"-beskrivelse, installation med ét klik

## v8.7

- Temaer: lys, mørk, røde temaer til tilstand R, vælg din egen farve
- Automatisk søgning efter installeret 7-Zip
- DirectX-biblioteker inde i programmet (en dialog vises, hvis et spil mangler dem)
- Start uden UAC-forespørgsel til programmer, der beder om administratorrettigheder
- Fjernet et duplikeret hukommelsestip
