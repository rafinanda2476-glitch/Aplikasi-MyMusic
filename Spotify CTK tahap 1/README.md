## Tujuan
Tujuan dari pengembangan pada Tahap 1 ini adalah untuk membangun fondasi teknis dan struktural yang solid bagi proyek aplikasi pemutar musik CustomTkinter (CTK).

### songs.csv
File Comma Separated Values (CSV) yang berisi data lagu awal. Ini berfungsi sebagai sumber data dummy yang akan digunakan aplikasi untuk menampilkan dan memutar daftar lagu lokal di Tahap 2.

### songs_dummy_real.csv
Sama seperti songs.csv, ini adalah sumber data dummy tambahan atau alternatif. Nama dummy_real menunjukkan bahwa ini mungkin data yang lebih mendekati format yang akan digunakan saat integrasi API Spotify di Tahap 3.

### spotify.py
Ini adalah file inti tempat Anda akan menulis logika utama dari aplikasi. Di Tahap 1, ini kemungkinan berisi kode dasar untuk:

    a. Membuat jendela utama CustomTkinter.
    b. Memuat dan menampilkan komponen GUI dasar (sidebar, player bar).
    c. Mempersiapkan kelas atau fungsi untuk berinteraksi dengan songs.csv.

### test.py
File terpisah yang digunakan untuk tujuan pengujian cepat (debugging). File ini digunakan untuk mencoba fungsionalitas kecil, seperti pengujian widget CTK tertentu, koneksi database, atau fungsi pemrosesan data, tanpa mengganggu kode utama di spotify.py.
