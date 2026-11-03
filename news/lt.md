# Kas naujo Portabilizer

## v9.1

- Sąsajos kalba: skirtukas "Kalba" (su gaublio piktograma), kaip Windows nustatymuose: kiekviena kalba rodoma savo pavadinimu, o po juo yra pavadinimas sąsajos kalba. Langas, patarimai, žurnalas, dialogai ir istorija išversti. Pakeitus kalbą langas paleidžiamas iš naujo; nustatymai išsaugomi
- Kalbos: 34 (русский, English, Eesti, Français, Español, Deutsch, Italiano, Português, Nederlands, Polski, Українська, Svenska, Suomi, Türkçe, 中文, 日本語, 한국어, العربية, Čeština, Română, Magyar, Ελληνικά, עברית, हिन्दी, Indonesia, Tiếng Việt, ไทย, Български, Српски, Hrvatski, Latviešu, Lietuvių, Norsk, Dansk)
- Pirmą kartą paleidus naudojama Windows kalba (jei ji tarp išverstų), kitaip anglų
- Failas portabilizer.log vis dar rašomas rusų kalba, tad lengviau išsiaiškinti klaidas

## v9.0

- Bibliotekų diegti nereikia: programa mato, kurių reikia žaidimui ar programai, ir siūlo jas padėti šalia exe (failai įmontuoti į Portabilizer)
- DirectX: 2010 m. birželio ir senesni 2005-2009 m. leidimai (d3dx9_24…43, d3dx10, XACT, XAudio, xinput) seniems žaidimams
- Visual C++ 2010, 2012, 2013 ir 2015-2022, OpenAL (kartu su wrap_oal.dll)
- Cab rinkiniai, kurių programa pati neperskaito, nebeaplenkiami: išskleidimą atlieka expand.exe (Windows)
- Bibliotekų rinkinys sudaromas scenarijumi tools/collect_redist.bat

## v8.9

- Režimas R: įprastas exe nebekopijuojamas, o perkeliamas į aplanką App. Viename diske tai vyksta akimirksniu ir nereikia papildomos vietos (anksčiau darbo metu reikėjo dvigubai daugiau vietos)
- Archyvams ir diegimo programoms režimui R vis dar reikia vietos: jie pirmiausia išskleidžiami ir tik tada ištrinamas šaltinis. Išskleisti galima į kitą diską naudojant lauką "Kur"
- Režimo R patarimas ir patvirtinimo langas atnaujinti
- Pikselių rašiklio piktogramos (mėlynos įprastai versijai, raudonos R) su tema "Klasikinė (sistemos)"; kitos temos išlaiko lygias piktogramas

## v8.8

- Naujinimų tikrinimas: programa pati tikrina GitHub Releases ir praneša, kai išleidžiama nauja versija (galima išjungti žymimuoju langeliu skirtuke "Versijos")
- Geresnis darbas su Portabilizer Launcher: versijos sąrašu, aprašas "kas naujo", diegimas vienu spustelėjimu

## v8.7

- Temos: šviesi, tamsi, raudonos temos režimui R, savo spalvos pasirinkimas
- Automatinė įdiegto 7-Zip paieška
- DirectX bibliotekos pačioje programoje (jei žaidimui jų trūksta, pasirodo dialogas)
- Paleidimas be UAC užklausos programoms, kurios prašo administratoriaus teisių
- Pašalintas pasikartojantis atminties patarimas
