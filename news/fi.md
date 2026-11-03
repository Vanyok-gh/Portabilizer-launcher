# Uutta Portabilizerissa

## v9.1

- Käyttöliittymän kieli: "Kieli"-välilehti (maapallokuvakkeella), kuten Windowsin asetuksissa: jokainen kieli näkyy omalla nimellään ja sen alla on nimi käyttöliittymän kielellä. Ikkuna, vihjeet, loki, valintaikkunat ja historia on käännetty. Kielen vaihtaminen käynnistää ikkunan uudelleen; asetuksesi säilyvät
- Kielet: 34 (русский, English, Eesti, Français, Español, Deutsch, Italiano, Português, Nederlands, Polski, Українська, Svenska, Suomi, Türkçe, 中文, 日本語, 한국어, العربية, Čeština, Română, Magyar, Ελληνικά, עברית, हिन्दी, Indonesia, Tiếng Việt, ไทย, Български, Српски, Hrvatski, Latviešu, Lietuvių, Norsk, Dansk)
- Ensimmäisellä käynnistyskerralla käytetään Windowsin kieltä (jos se on käännetyistä), muuten englantia
- portabilizer.log-tiedosto kirjoitetaan edelleen venäjäksi, mikä helpottaa virheiden selvittämistä

## v9.0

- Kirjastoja ei tarvitse asentaa: ohjelma näkee, mitä peli tai sovellus tarvitsee, ja tarjoaa niiden asettamista exe-tiedoston viereen (tiedostot on sisäänrakennettu Portabilizeriin)
- DirectX: kesäkuu 2010 ja vanhemmat 2005-2009 julkaisut (d3dx9_24…43, d3dx10, XACT, XAudio, xinput) vanhoille peleille
- Visual C++ 2010, 2012, 2013 ja 2015-2022, OpenAL (yhdessä wrap_oal.dll:n kanssa)
- Cab-paketteja, joita ohjelma ei osaa lukea itse, ei enää ohiteta: purkamisen hoitaa expand.exe (Windows)
- Kirjastokokoelma rakennetaan tools/collect_redist.bat-skriptillä

## v8.9

- R-tila: tavallista exe-tiedostoa ei enää kopioida vaan se siirretään App-kansioon. Samalla asemalla tämä on välitön eikä vaadi lisätilaa (aiemmin työn aikana tarvittiin kaksinkertainen tila)
- Arkistoille ja asennusohjelmille R-tila vaatii edelleen tilaa: ne puretaan ensin ja vasta sitten lähde poistetaan. Voit purkaa toiselle asemalle "Kohde"-kentän avulla
- R-tilan vihje ja vahvistusikkuna on päivitetty
- Pikselikynäkuvakkeet (siniset tavalliselle versiolle, punaiset R:lle) "Klassinen (järjestelmän)" -teemassa; muissa teemoissa säilyvät pehmeät kuvakkeet

## v8.8

- Päivitysten tarkistus: ohjelma tarkistaa GitHub Releasesin itse ja kertoo, kun uusi versio on ilmestynyt (voidaan poistaa käytöstä "Versiot"-välilehden valintaruudulla)
- Toimii paremmin Portabilizer Launcherin kanssa: versiot luettelona, "uutta"-kuvaus, asennus yhdellä napsautuksella

## v8.7

- Teemat: vaalea, tumma, punaiset teemat R-tilalle, valitse oma värisi
- Asennetun 7-Zipin automaattinen haku
- DirectX-kirjastot ohjelman sisällä (valintaikkuna tulee näkyviin, jos pelistä ne puuttuvat)
- Käynnistys ilman UAC-kehotetta ohjelmille, jotka pyytävät järjestelmänvalvojan oikeuksia
- Poistettu kaksinkertainen muistivihje
