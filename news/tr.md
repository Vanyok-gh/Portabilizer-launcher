# Portabilizer'da neler yeni

## v9.1

- Arayüz dili: Windows ayarlarındaki gibi (küre simgeli) bir "Dil" sekmesi: her dil kendi adıyla, altında ise arayüz dilindeki adıyla gösterilir. Pencere, ipuçları, günlük, iletişim kutuları ve geçmiş çevrilmiştir. Dil değiştirildiğinde pencere yeniden başlar; ayarlarınız korunur
- Diller: 34 (русский, English, Eesti, Français, Español, Deutsch, Italiano, Português, Nederlands, Polski, Українська, Svenska, Suomi, Türkçe, 中文, 日本語, 한국어, العربية, Čeština, Română, Magyar, Ελληνικά, עברית, हिन्दी, Indonesia, Tiếng Việt, ไทย, Български, Српски, Hrvatski, Latviešu, Lietuvių, Norsk, Dansk)
- İlk açılışta Windows dili kullanılır (çevrilenler arasındaysa), aksi halde İngilizce
- portabilizer.log dosyası hâlâ Rusça yazılır; bu, hataları çözmeyi kolaylaştırır

## v9.0

- Kitaplık kurmaya gerek yok: program bir oyunun veya uygulamanın hangilerine ihtiyaç duyduğunu görür ve bunları exe dosyasının yanına koymayı önerir (dosyalar Portabilizer'a gömülüdür)
- DirectX: Haziran 2010 ve eski oyunlar için 2005-2009 sürümleri (d3dx9_24…43, d3dx10, XACT, XAudio, xinput)
- Visual C++ 2010, 2012, 2013 ve 2015-2022, OpenAL (wrap_oal.dll ile birlikte)
- Programın kendi başına okuyamadığı Cab setleri artık atlanmıyor: açma işlemini expand.exe (Windows) yapar
- Kitaplık seti tools/collect_redist.bat betiğiyle oluşturulur

## v8.9

- R modu: normal bir exe artık kopyalanmaz, App klasörüne taşınır. Aynı sürücüde bu anında olur ve ek alan gerektirmez (önceden çalışırken iki kat alan gerekiyordu)
- Arşivler ve yükleyiciler için R modu hâlâ alan gerektirir: önce açılırlar, kaynak ancak sonra silinir. "Hedef" alanını kullanarak başka bir sürücüye açabilirsiniz
- R modu ipucu ve onay penceresi güncellendi
- "Klasik (sistem)" temasıyla piksel kalem simgeleri (normal sürüm için mavi, R için kırmızı); diğer temalarda yumuşak simgeler korunur

## v8.8

- Güncelleme denetimi: program GitHub Releases'i kendisi denetler ve yeni sürüm çıktığında size bildirir ("Sürümler" sekmesindeki kutucukla kapatılabilir)
- Portabilizer Launcher ile daha iyi çalışır: liste hâlinde sürümler, "neler yeni" açıklaması, tek tıkla kurulum

## v8.7

- Temalar: açık, koyu, R modu için kırmızı temalar, kendi renginizi seçin
- Kurulu 7-Zip'in otomatik aranması
- DirectX kitaplıkları programın içinde (bir oyunda eksikse bir iletişim kutusu görünür)
- Yönetici hakları isteyen programlar için UAC istemi olmadan başlatma
- Yinelenen bellek ipucu kaldırıldı
