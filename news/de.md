# Neues in Portabilizer

## v9.1

- Oberflächensprache: ein Tab "Sprache" (mit Globus), wie in den Windows-Einstellungen: Jede Sprache wird mit ihrem eigenen Namen angezeigt, darunter der Name in der Sprache der Oberfläche. Fenster, Hinweise, Protokoll, Dialoge und Verlauf sind übersetzt. Beim Wechsel der Sprache startet das Fenster neu; Ihre Einstellungen bleiben erhalten
- Sprachen: 34 (русский, English, Eesti, Français, Español, Deutsch, Italiano, Português, Nederlands, Polski, Українська, Svenska, Suomi, Türkçe, 中文, 日本語, 한국어, العربية, Čeština, Română, Magyar, Ελληνικά, עברית, हिन्दी, Indonesia, Tiếng Việt, ไทย, Български, Српски, Hrvatski, Latviešu, Lietuvių, Norsk, Dansk)
- Beim ersten Start wird die Windows-Sprache verwendet (sofern sie übersetzt ist), sonst Englisch
- Die Datei portabilizer.log wird weiterhin auf Russisch geschrieben, was die Fehlersuche erleichtert

## v9.0

- Bibliotheken müssen nicht mehr installiert werden: Das Programm erkennt, welche ein Spiel oder eine Anwendung braucht, und bietet an, sie neben die exe zu legen (die Dateien sind in Portabilizer eingebaut)
- DirectX: Juni 2010 und ältere Versionen 2005-2009 (d3dx9_24…43, d3dx10, XACT, XAudio, xinput) für alte Spiele
- Visual C++ 2010, 2012, 2013 und 2015-2022, OpenAL (zusammen mit wrap_oal.dll)
- Cab-Sätze, die das Programm nicht selbst lesen kann, werden nicht mehr übersprungen: Das Entpacken übernimmt expand.exe (Windows)
- Der Bibliothekssatz wird mit dem Skript tools/collect_redist.bat erstellt

## v8.9

- Modus R: Eine normale exe wird nicht mehr kopiert, sondern in den Ordner App verschoben. Auf einem Laufwerk geht das sofort und braucht keinen zusätzlichen Platz (früher wurde währenddessen der doppelte Platz benötigt)
- Bei Archiven und Installern braucht Modus R weiterhin Platz: Sie werden zuerst entpackt, erst danach wird die Quelle gelöscht. Über das Feld "Ziel" können Sie auf ein anderes Laufwerk entpacken
- Hinweis und Bestätigungsfenster für Modus R wurden aktualisiert
- Pixel-Stiftsymbole (blau für die normale Version, rot für R) beim Design "Klassisch (System)"; andere Designs behalten glatte Symbole

## v8.8

- Update-Prüfung: Das Programm prüft GitHub Releases selbst und meldet, wenn eine neue Version erscheint (lässt sich mit dem Kontrollkästchen im Tab "Versionen" ausschalten)
- Bessere Zusammenarbeit mit Portabilizer Launcher: Versionen als Liste, Beschreibung der Neuerungen, Installation mit einem Klick

## v8.7

- Designs: hell, dunkel, rote Designs für Modus R, eigene Farbe wählbar
- Automatische Suche nach einem installierten 7-Zip
- DirectX-Bibliotheken im Programm (ein Dialog erscheint, wenn sie einem Spiel fehlen)
- Start ohne UAC-Abfrage für Programme, die Administratorrechte verlangen
- Doppelten Speicherhinweis entfernt
