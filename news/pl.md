# Co nowego w Portabilizer

## v9.1

- Język interfejsu: zakładka "Język" (z globusem), jak w ustawieniach Windows: każdy język jest pokazany pod własną nazwą, a pod nią nazwa w języku interfejsu. Okno, podpowiedzi, dziennik, okna dialogowe i historia są przetłumaczone. Zmiana języka restartuje okno; ustawienia zostają zachowane
- Języki: 34 (русский, English, Eesti, Français, Español, Deutsch, Italiano, Português, Nederlands, Polski, Українська, Svenska, Suomi, Türkçe, 中文, 日本語, 한국어, العربية, Čeština, Română, Magyar, Ελληνικά, עברית, हिन्दी, Indonesia, Tiếng Việt, ไทย, Български, Српски, Hrvatski, Latviešu, Lietuvių, Norsk, Dansk)
- Przy pierwszym uruchomieniu używany jest język Windows (jeśli jest wśród przetłumaczonych), w przeciwnym razie angielski
- Plik portabilizer.log nadal jest zapisywany po rosyjsku, co ułatwia analizę błędów

## v9.0

- Nie trzeba instalować bibliotek: program widzi, których potrzebuje gra lub aplikacja, i proponuje umieścić je obok exe (pliki są wbudowane w Portabilizer)
- DirectX: czerwiec 2010 i starsze wydania 2005-2009 (d3dx9_24…43, d3dx10, XACT, XAudio, xinput) dla starych gier
- Visual C++ 2010, 2012, 2013 i 2015-2022, OpenAL (razem z wrap_oal.dll)
- Zestawy Cab, których program nie potrafi odczytać sam, nie są już pomijane: rozpakowaniem zajmuje się expand.exe (Windows)
- Zestaw bibliotek jest budowany skryptem tools/collect_redist.bat

## v8.9

- Tryb R: zwykły exe nie jest już kopiowany, lecz przenoszony do folderu App. Na jednym dysku jest to natychmiastowe i nie wymaga dodatkowego miejsca (wcześniej podczas pracy potrzeba było dwa razy więcej miejsca)
- W przypadku archiwów i instalatorów tryb R nadal wymaga miejsca: najpierw są rozpakowywane, a dopiero potem źródło jest usuwane. Możesz rozpakować na inny dysk, używając pola "Dokąd"
- Zaktualizowano podpowiedź i okno potwierdzenia trybu R
- Pikselowe ikony ołówka (niebieska dla zwykłej wersji, czerwona dla R) w motywie "Klasyczny (systemowy)"; inne motywy zachowują gładkie ikony

## v8.8

- Sprawdzanie aktualizacji: program sam sprawdza GitHub Releases i informuje o nowej wersji (można wyłączyć polem wyboru na zakładce "Wersje")
- Lepiej współpracuje z Portabilizer Launcher: wersje w postaci listy, opis nowości, instalacja jednym kliknięciem

## v8.7

- Motywy: jasny, ciemny, czerwone motywy dla trybu R, własny kolor do wyboru
- Automatyczne wyszukiwanie zainstalowanego 7-Zip
- Biblioteki DirectX wbudowane w program (pojawia się okno, jeśli grze ich brakuje)
- Uruchamianie bez monitu UAC dla programów wymagających uprawnień administratora
- Usunięto zduplikowaną podpowiedź o pamięci
