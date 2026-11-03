# Novedades de Portabilizer

## v9.1

- Idioma de la interfaz: una pestaña "Idioma" (con un globo terráqueo), como en la configuración de Windows: cada idioma se muestra con su propio nombre y, debajo, su nombre en el idioma de la interfaz. La ventana, las ayudas, el registro, los cuadros de diálogo y el historial están traducidos. Al cambiar el idioma la ventana se reinicia; se conservan tus ajustes
- Idiomas: 34 (русский, English, Eesti, Français, Español, Deutsch, Italiano, Português, Nederlands, Polski, Українська, Svenska, Suomi, Türkçe, 中文, 日本語, 한국어, العربية, Čeština, Română, Magyar, Ελληνικά, עברית, हिन्दी, Indonesia, Tiếng Việt, ไทย, Български, Српски, Hrvatski, Latviešu, Lietuvių, Norsk, Dansk)
- En el primer inicio se usa el idioma de Windows (si está entre los traducidos); si no, inglés
- El archivo portabilizer.log sigue escribiéndose en ruso, lo que facilita analizar los errores

## v9.0

- No hace falta instalar bibliotecas: el programa detecta cuáles necesita un juego o aplicación y ofrece colocarlas junto al exe (los archivos están integrados en Portabilizer)
- DirectX: versión de junio de 2010 y versiones antiguas 2005-2009 (d3dx9_24…43, d3dx10, XACT, XAudio, xinput) para juegos antiguos
- Visual C++ 2010, 2012, 2013 y 2015-2022, OpenAL (junto con wrap_oal.dll)
- Los conjuntos Cab que el programa no puede leer por sí mismo ya no se omiten: la extracción la realiza expand.exe (Windows)
- El conjunto de bibliotecas se genera con el script tools/collect_redist.bat

## v8.9

- Modo R: un exe normal ya no se copia, sino que se mueve a la carpeta App. En una misma unidad es instantáneo y no necesita espacio extra (antes se necesitaba el doble de espacio mientras se ejecutaba)
- Para archivos comprimidos e instaladores, el modo R sigue necesitando espacio: primero se extraen y solo después se elimina el origen. Puedes extraer en otra unidad con el campo "Destino"
- Se actualizaron la ayuda y la ventana de confirmación del modo R
- Iconos de lápiz de píxeles (azul para la versión normal, rojo para R) con el tema "Clásico (del sistema)"; los demás temas conservan iconos suaves

## v8.8

- Comprobación de actualizaciones: el programa consulta GitHub Releases por sí mismo y avisa cuando sale una versión nueva (se puede desactivar con la casilla de la pestaña "Versiones")
- Funciona mejor con Portabilizer Launcher: versiones en lista, descripción de novedades, instalación con un clic

## v8.7

- Temas: claro, oscuro, temas rojos para el modo R, elige tu propio color
- Búsqueda automática de un 7-Zip instalado
- Bibliotecas DirectX dentro del programa (aparece un cuadro de diálogo si a un juego le faltan)
- Inicio sin solicitud de UAC para programas que piden derechos de administrador
- Se eliminó una ayuda duplicada sobre la memoria
