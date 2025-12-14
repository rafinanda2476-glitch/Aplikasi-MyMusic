## Tujuan
Tahap 3 menandai transisi proyek dari aplikasi lokal yang fungsional menjadi aplikasi yang berorientasi pengalaman pengguna yang kaya dan terhubung. Fokus utamanya adalah persiapan dan implementasi untuk integrasi data eksternal, dengan asumsi menggunakan Spotify API.

Tujuan utama pada tahap ini adalah untuk menyempurnakan interaksi pengguna. Ini mencakup pembaruan pada modul login untuk menangani mekanisme otentikasi lanjutan (seperti OAuth), yang sangat penting untuk mendapatkan akses ke data pribadi pengguna dari platform eksternal. Selain itu, pengembangan fitur akan diperluas untuk mencakup kemampuan menangani dan menampilkan data daftar putar secara efektif, yang ditunjukkan dengan adanya file baru playlists.json.

Secara keseluruhan, Tahap 3 bertujuan untuk menguji batas fungsionalitas aplikasi dengan data dunia nyata atau data yang lebih kompleks, menciptakan fondasi bagi fitur-fitur yang dipersonalisasi seperti pencarian canggih dan manajemen daftar putar pengguna.

### playlists.json
File baru yang sangat penting di Tahap 3. Ini akan digunakan untuk menyimpan data daftar putar (playlists) pengguna, baik dummy untuk pengembangan atau hasil caching dari API Spotify. Ini adalah persiapan langsung untuk fitur personalisasi pengguna.

### components, logic, pages_admin, pages_user
Struktur modular ini (diwarisi dari Tahap 2) akan diperluas untuk mengakomodasi logika API dan tampilan UI baru (misalnya, halaman 'Search' atau halaman 'Profile').

### gabung.py, full_codebase.txt
File legacy yang harus dihilangkan di Tahap 3 untuk menjaga kode tetap bersih, seperti yang telah kita diskusikan sebelumnya.

### songs.csv, songs_dummy_real.csv, songs_store.json
Data dummy ini akan dipertahankan untuk tujuan testing (uji coba), tetapi fungsi utamanya adalah sebagai fallback ketika integrasi API selesai.

### login.py
Akan ditingkatkan untuk menangani proses autentikasi OAuth atau otorisasi token yang diperlukan untuk mengakses data pengguna dari Spotify API.
