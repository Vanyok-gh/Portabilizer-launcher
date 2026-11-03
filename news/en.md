# What's new in Portabilizer

## v9.1

- Interface language: a "Language" tab (with a globe), like in Windows settings: each language is shown in its own name with the name in the interface language below it. The window, hints, log, dialogs and history are translated. Changing the language restarts the window; your settings are kept
- Languages: 34 (русский, English, Eesti, Français, Español, Deutsch, Italiano, Português, Nederlands, Polski, Українська, Svenska, Suomi, Türkçe, 中文, 日本語, 한국어, العربية, Čeština, Română, Magyar, Ελληνικά, עברית, हिन्दी, Indonesia, Tiếng Việt, ไทย, Български, Српски, Hrvatski, Latviešu, Lietuvių, Norsk, Dansk)
- On first launch the Windows language is used (if it is among the translated ones), otherwise English
- The portabilizer.log file is still written in Russian, which makes errors easier to sort out

## v9.0

- No need to install libraries: the program sees which ones a game or app needs and offers to put them next to the exe (the files are built into Portabilizer)
- DirectX: June 2010 and older 2005-2009 releases (d3dx9_24…43, d3dx10, XACT, XAudio, xinput) for old games
- Visual C++ 2010, 2012, 2013 and 2015-2022, OpenAL (together with wrap_oal.dll)
- Cab sets that the program cannot read itself are no longer skipped: extraction is handled by expand.exe (Windows)
- The library set is built by the tools/collect_redist.bat script

## v8.9

- Mode R: a regular exe is no longer copied but moved into the App folder. On one drive this is instant and needs no extra space (before, twice the space was needed while it ran)
- For archives and installers, Mode R still needs space: they are extracted first, and only then is the source deleted. You can extract to another drive using the "Where to" field
- The Mode R hint and confirmation window were updated
- Pixel pen icons (blue for the regular version, red for R) with the "Classic (system)" theme; other themes keep smooth icons

## v8.8

- Update check: the program checks GitHub Releases itself and tells you when a new version is out (can be turned off with the checkbox on the "Versions" tab)
- Works better with Portabilizer Launcher: versions as a list, a "what's new" description, one-click install

## v8.7

- Themes: light, dark, red themes for Mode R, choose your own colour
- Automatic search for an installed 7-Zip
- DirectX libraries inside the program (a dialog appears if a game is missing them)
- Launch without a UAC prompt for programs that ask for administrator rights
- Removed a duplicate memory hint
