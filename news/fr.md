# Nouveautés de Portabilizer

## v9.1

- Langue de l'interface : un onglet "Langue" (avec un globe), comme dans les paramètres de Windows : chaque langue s'affiche sous son propre nom, avec en dessous son nom dans la langue de l'interface. La fenêtre, les info-bulles, le journal, les boîtes de dialogue et l'historique sont traduits. Changer de langue redémarre la fenêtre ; vos paramètres sont conservés
- Langues : 34 (русский, English, Eesti, Français, Español, Deutsch, Italiano, Português, Nederlands, Polski, Українська, Svenska, Suomi, Türkçe, 中文, 日本語, 한국어, العربية, Čeština, Română, Magyar, Ελληνικά, עברית, हिन्दी, Indonesia, Tiếng Việt, ไทย, Български, Српски, Hrvatski, Latviešu, Lietuvių, Norsk, Dansk)
- Au premier lancement, la langue de Windows est utilisée (si elle fait partie des langues traduites), sinon l'anglais
- Le fichier portabilizer.log est toujours écrit en russe, ce qui facilite le diagnostic des erreurs

## v9.0

- Plus besoin d'installer des bibliothèques : le programme voit lesquelles un jeu ou une application requiert et propose de les placer à côté de l'exe (les fichiers sont intégrés à Portabilizer)
- DirectX : version de juin 2010 et anciennes versions 2005-2009 (d3dx9_24…43, d3dx10, XACT, XAudio, xinput) pour les vieux jeux
- Visual C++ 2010, 2012, 2013 et 2015-2022, OpenAL (avec wrap_oal.dll)
- Les ensembles Cab que le programme ne sait pas lire lui-même ne sont plus ignorés : l'extraction est confiée à expand.exe (Windows)
- L'ensemble de bibliothèques est généré par le script tools/collect_redist.bat

## v8.9

- Mode R : un exe ordinaire n'est plus copié mais déplacé dans le dossier App. Sur un même disque, c'est instantané et sans espace supplémentaire (avant, il fallait le double d'espace pendant l'opération)
- Pour les archives et les installateurs, le mode R a toujours besoin d'espace : ils sont d'abord extraits, puis la source est supprimée. Vous pouvez extraire vers un autre disque avec le champ "Destination"
- L'info-bulle et la fenêtre de confirmation du mode R ont été mises à jour
- Icônes de crayon en pixels (bleue pour la version normale, rouge pour R) avec le thème "Classique (système)" ; les autres thèmes gardent des icônes lissées

## v8.8

- Vérification des mises à jour : le programme consulte lui-même GitHub Releases et vous prévient de la sortie d'une nouvelle version (peut être désactivée avec la case à cocher de l'onglet "Versions")
- Meilleure collaboration avec Portabilizer Launcher : versions sous forme de liste, description des nouveautés, installation en un clic

## v8.7

- Thèmes : clair, sombre, thèmes rouges pour le mode R, choix de votre propre couleur
- Recherche automatique d'un 7-Zip installé
- Bibliothèques DirectX intégrées au programme (une boîte de dialogue s'affiche si un jeu en a besoin)
- Lancement sans demande UAC pour les programmes qui exigent les droits d'administrateur
- Suppression d'une info-bulle en double sur la mémoire
