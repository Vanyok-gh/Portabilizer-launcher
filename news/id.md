# Yang baru di Portabilizer

## v9.1

- Bahasa antarmuka: tab «Bahasa» (dengan ikon globe), seperti di pengaturan Windows: setiap bahasa ditampilkan dengan namanya sendiri dan di bawahnya nama dalam bahasa antarmuka. Jendela, petunjuk, log, dialog, dan riwayat sudah diterjemahkan. Saat bahasa diganti, jendela dimulai ulang; pengaturan Anda tetap tersimpan
- Bahasa: 34 (русский, English, Eesti, Français, Español, Deutsch, Italiano, Português, Nederlands, Polski, Українська, Svenska, Suomi, Türkçe, 中文, 日本語, 한국어, العربية, Čeština, Română, Magyar, Ελληνικά, עברית, हिन्दी, Indonesia, Tiếng Việt, ไทย, Български, Српски, Hrvatski, Latviešu, Lietuvių, Norsk, Dansk)
- Saat pertama dijalankan, bahasa Windows digunakan (jika termasuk yang diterjemahkan), jika tidak, bahasa Inggris
- File portabilizer.log masih ditulis dalam bahasa Rusia, sehingga lebih mudah menelusuri kesalahan

## v9.0

- Tidak perlu memasang pustaka: program melihat pustaka mana yang dibutuhkan game atau aplikasi dan menawarkan untuk menaruhnya di samping exe (file sudah tertanam di Portabilizer)
- DirectX: rilis June 2010 dan rilis lama 2005-2009 (d3dx9_24…43, d3dx10, XACT, XAudio, xinput) untuk game lama
- Visual C++ 2010, 2012, 2013 dan 2015-2022, OpenAL (bersama wrap_oal.dll)
- Set Cab yang tidak dapat dibaca sendiri oleh program tidak lagi dilewati: ekstraksi ditangani oleh expand.exe (Windows)
- Set pustaka dibuat dengan skrip tools/collect_redist.bat

## v8.9

- Mode R: exe biasa tidak lagi disalin, melainkan dipindahkan ke folder App. Pada satu drive ini instan dan tidak butuh ruang tambahan (sebelumnya selama proses dibutuhkan dua kali lipat ruang)
- Untuk arsip dan installer, Mode R tetap butuh ruang: keduanya diekstrak lebih dulu, baru kemudian sumbernya dihapus. Anda dapat mengekstrak ke drive lain lewat kolom «Tujuan»
- Petunjuk dan jendela konfirmasi Mode R telah diperbarui
- Ikon pena piksel (biru untuk versi biasa, merah untuk R) dengan tema «Klasik (sistem)»; tema lain tetap memakai ikon halus

## v8.8

- Pemeriksaan pembaruan: program memeriksa GitHub Releases sendiri dan memberi tahu saat versi baru terbit (dapat dimatikan dengan kotak centang di tab «Versi»)
- Bekerja lebih baik dengan Portabilizer Launcher: versi dalam daftar, deskripsi «yang baru», pemasangan sekali klik

## v8.7

- Tema: terang, gelap, tema merah untuk Mode R, pilih warna sendiri
- Pencarian otomatis 7-Zip yang terpasang
- Pustaka DirectX di dalam program (muncul dialog jika game tidak memilikinya)
- Peluncuran tanpa permintaan UAC untuk program yang meminta hak administrator
- Menghapus petunjuk memori yang ganda
