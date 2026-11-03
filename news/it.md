# Novità di Portabilizer

## v9.1

- Lingua dell'interfaccia: una scheda "Lingua" (con un globo), come nelle impostazioni di Windows: ogni lingua è mostrata con il proprio nome e, sotto, il nome nella lingua dell'interfaccia. Finestra, suggerimenti, registro, finestre di dialogo e cronologia sono tradotti. Cambiando lingua la finestra si riavvia; le impostazioni vengono mantenute
- Lingue: 34 (русский, English, Eesti, Français, Español, Deutsch, Italiano, Português, Nederlands, Polski, Українська, Svenska, Suomi, Türkçe, 中文, 日本語, 한국어, العربية, Čeština, Română, Magyar, Ελληνικά, עברית, हिन्दी, Indonesia, Tiếng Việt, ไทย, Български, Српски, Hrvatski, Latviešu, Lietuvių, Norsk, Dansk)
- Al primo avvio viene usata la lingua di Windows (se è tra quelle tradotte), altrimenti l'inglese
- Il file portabilizer.log viene ancora scritto in russo, il che facilita l'analisi degli errori

## v9.0

- Non serve installare librerie: il programma vede quali servono a un gioco o a un'app e propone di metterle accanto all'exe (i file sono integrati in Portabilizer)
- DirectX: giugno 2010 e versioni precedenti 2005-2009 (d3dx9_24…43, d3dx10, XACT, XAudio, xinput) per i vecchi giochi
- Visual C++ 2010, 2012, 2013 e 2015-2022, OpenAL (insieme a wrap_oal.dll)
- I set Cab che il programma non riesce a leggere da solo non vengono più saltati: l'estrazione è affidata a expand.exe (Windows)
- Il set di librerie viene creato con lo script tools/collect_redist.bat

## v8.9

- Modalità R: un exe normale non viene più copiato ma spostato nella cartella App. Su un solo disco è istantaneo e non richiede spazio extra (prima durante l'operazione serviva il doppio dello spazio)
- Per archivi e installer la modalità R richiede ancora spazio: vengono prima estratti e solo dopo l'origine viene eliminata. Puoi estrarre su un altro disco con il campo "Destinazione"
- Sono stati aggiornati il suggerimento e la finestra di conferma della modalità R
- Icone a matita in pixel (blu per la versione normale, rossa per R) con il tema "Classico (di sistema)"; gli altri temi mantengono icone morbide

## v8.8

- Controllo degli aggiornamenti: il programma controlla da solo GitHub Releases e avvisa quando esce una nuova versione (si può disattivare con la casella nella scheda "Versioni")
- Funziona meglio con Portabilizer Launcher: versioni in elenco, descrizione delle novità, installazione con un clic

## v8.7

- Temi: chiaro, scuro, temi rossi per la modalità R, scegli il tuo colore
- Ricerca automatica di un 7-Zip installato
- Librerie DirectX nel programma (compare una finestra se a un gioco mancano)
- Avvio senza richiesta UAC per i programmi che chiedono i diritti di amministratore
- Rimosso un suggerimento duplicato sulla memoria
