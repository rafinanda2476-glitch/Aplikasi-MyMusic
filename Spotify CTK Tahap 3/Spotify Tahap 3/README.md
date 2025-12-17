## Tujuan
Tahap 3 menandai transisi proyek dari aplikasi lokal yang fungsional menjadi aplikasi yang berorientasi pengalaman pengguna yang kaya dan terhubung. Fokus utamanya adalah persiapan dan implementasi untuk integrasi data eksternal, dengan asumsi menggunakan Spotify API.

Tujuan utama pada tahap ini adalah untuk menyempurnakan interaksi pengguna. Ini mencakup pembaruan pada modul login untuk menangani mekanisme otentikasi lanjutan (seperti OAuth), yang sangat penting untuk mendapatkan akses ke data pribadi pengguna dari platform eksternal. Selain itu, pengembangan fitur akan diperluas untuk mencakup kemampuan menangani dan menampilkan data daftar putar secara efektif, yang ditunjukkan dengan adanya file baru playlists.json.

Secara keseluruhan, Tahap 3 bertujuan untuk menguji batas fungsionalitas aplikasi dengan data dunia nyata atau data yang lebih kompleks, menciptakan fondasi bagi fitur-fitur yang dipersonalisasi seperti pencarian canggih dan manajemen daftar putar pengguna.

### Transisi Utama: Dari .csv ke .mp3
Perubahan paling signifikan pada tahap ini adalah:
Tahap Sebelumnya: Data lagu bersifat dummy dan dibaca secara manual dari file songs.csv.
Tahap 3: Aplikasi secara otomatis memindai folder musik, mengekstraksi metadata langsung dari file .mp3, dan menyimpannya ke database songs_store.json

### Alasan Transisi (.csv ke .mp3)
Perpindahan ini dilakukan untuk mengotomatisasi manajemen library musik. Dengan beralih ke pengolahan file .mp3, aplikasi tidak lagi bergantung pada input manual di file .csv, melainkan menggunakan algoritma pemindaian folder dan ekstraksi metadata (TinyTag) untuk membangun basis data secara otomatis dan akurat

### Alasan Transisi (.csv ke .mp3)
Perpindahan ini dilakukan untuk mengotomatisasi manajemen library musik. Dengan beralih ke pengolahan file .mp3, aplikasi tidak lagi bergantung pada input manual di file .csv, melainkan menggunakan algoritma pemindaian folder dan ekstraksi metadata (TinyTag) untuk membangun basis data secara otomatis dan akurat


### songs_store.json
Merupakan database utama berbasis JSON yang menyimpan metadata lagu lengkap. File ini menggantikan format CSV untuk memastikan performa pembacaan data yang lebih cepat dan struktur data yang lebih rapi.

### playlists.json
File baru yang sangat penting di Tahap 3. Ini akan digunakan untuk menyimpan data daftar putar (playlists) pengguna, baik dummy untuk pengembangan atau hasil caching dari API Spotify. Ini adalah persiapan langsung untuk fitur personalisasi pengguna.

### login.py
Akan ditingkatkan untuk menangani proses autentikasi OAuth atau otorisasi token yang diperlukan untuk mengakses data pengguna dari Spotify API.

### Kesimpulan
Aplikasi MyMusic Tahap 3 telah berhasil diimplementasikan sebagai pemutar musik lokal yang stabil. Dengan kombinasi struktur data Doubly Linked List dan database JSON, aplikasi mampu memberikan performa navigasi yang mulus dan manajemen data yang persisten bagi pengguna.
