# Novidades do Portabilizer

## v9.1

- Idioma da interface: uma aba "Idioma" (com um globo), como nas configurações do Windows: cada idioma aparece com seu próprio nome e, abaixo, o nome no idioma da interface. A janela, as dicas, o registro, as caixas de diálogo e o histórico estão traduzidos. Ao trocar o idioma, a janela reinicia; suas configurações são mantidas
- Idiomas: 34 (русский, English, Eesti, Français, Español, Deutsch, Italiano, Português, Nederlands, Polski, Українська, Svenska, Suomi, Türkçe, 中文, 日本語, 한국어, العربية, Čeština, Română, Magyar, Ελληνικά, עברית, हिन्दी, Indonesia, Tiếng Việt, ไทย, Български, Српски, Hrvatski, Latviešu, Lietuvių, Norsk, Dansk)
- Na primeira execução, é usado o idioma do Windows (se estiver entre os traduzidos); caso contrário, inglês
- O arquivo portabilizer.log continua sendo escrito em russo, o que facilita a análise de erros

## v9.0

- Não é preciso instalar bibliotecas: o programa vê quais um jogo ou aplicativo precisa e oferece colocá-las ao lado do exe (os arquivos estão embutidos no Portabilizer)
- DirectX: junho de 2010 e versões antigas 2005-2009 (d3dx9_24…43, d3dx10, XACT, XAudio, xinput) para jogos antigos
- Visual C++ 2010, 2012, 2013 e 2015-2022, OpenAL (junto com wrap_oal.dll)
- Conjuntos Cab que o programa não consegue ler sozinho não são mais ignorados: a extração fica por conta do expand.exe (Windows)
- O conjunto de bibliotecas é gerado pelo script tools/collect_redist.bat

## v8.9

- Modo R: um exe comum não é mais copiado, mas movido para a pasta App. No mesmo disco isso é instantâneo e não exige espaço extra (antes, era preciso o dobro de espaço durante a execução)
- Para arquivos compactados e instaladores, o modo R ainda precisa de espaço: eles são extraídos primeiro e só depois a origem é excluída. Você pode extrair para outro disco usando o campo "Destino"
- A dica e a janela de confirmação do modo R foram atualizadas
- Ícones de lápis em pixels (azul para a versão comum, vermelho para R) com o tema "Clássico (do sistema)"; os outros temas mantêm ícones suaves

## v8.8

- Verificação de atualizações: o programa consulta o GitHub Releases por conta própria e avisa quando sai uma nova versão (pode ser desativada na caixa de seleção da aba "Versões")
- Funciona melhor com o Portabilizer Launcher: versões em lista, descrição das novidades, instalação com um clique

## v8.7

- Temas: claro, escuro, temas vermelhos para o modo R, escolha sua própria cor
- Busca automática por um 7-Zip instalado
- Bibliotecas DirectX dentro do programa (aparece uma caixa de diálogo se um jogo não as tiver)
- Inicialização sem solicitação do UAC para programas que pedem direitos de administrador
- Removida uma dica duplicada sobre memória
