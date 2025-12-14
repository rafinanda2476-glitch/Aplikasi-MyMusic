## TUJUAN
Tahap 2 merupakan titik krusial dalam pengembangan proyek Aplikasi-MyMusic karena fokusnya adalah pada transformasi dari kerangka (skeleton) menjadi aplikasi yang fungsional. Tujuan utama pada tahap ini adalah untuk membangun arsitektur kode yang terstruktur dan modular, sekaligus mengimplementasikan fungsionalitas inti pemutar musik.

Kami bertujuan untuk mencapai modularisasi penuh dengan memisahkan logika antarmuka pengguna (GUI) ke dalam folder components dan pages_user, memastikan setiap elemen desain CustomTkinter dapat digunakan kembali. Logika backend yang menangani pemrosesan data lagu dan kontrol pemutaran akan diisolasi di folder logic. Pemisahan ini (app.py sebagai controller yang menghubungkan semua modul) sangat penting untuk mempermudah pemeliharaan dan pengembangan di masa depan.

Secara bersamaan, Tahap 2 akan melihat implementasi fungsi pemutaran musik inti. Ini mencakup integrasi library audio yang sesuai untuk mengontrol fungsi Play, Pause, Stop, serta pengaturan volume untuk lagu-lagu lokal yang datanya dimigrasikan. Data lagu yang sebelumnya berada dalam format .csv (dari Tahap 1) akan dikonversi dan disimpan dalam format JSON (songs_store.json), yang merupakan format yang lebih efisien dan terstruktur untuk diakses oleh modul logika Python, sehingga aplikasi dapat menampilkan dan memutar daftar lagu dengan lancar.

### components
Berisi widget atau elemen antarmuka (UI) yang lebih kecil dan dapat digunakan kembali. Contoh: Tombol kustom, bilah slider volume, atau frame spesifik yang dibuat dengan CustomTkinter. Tujuannya adalah menjaga app.py tetap bersih.

### logic
Berisi semua logika backend yang terpisah dari GUI. Ini bisa mencakup modul untuk:
  a. Pemrosesan file lagu (.csv atau .json) 
  b. Kontrol pemutaran musik (fungsi Play/Pause/Stop)
  c. Interaksi database atau API (walaupun API utamanya di Tahap 3).

### pages_admin
Berisi file Python untuk halaman/tampilan yang hanya dapat diakses oleh administrator (jika ada). Ini menunjukkan niat untuk membedakan hak akses di masa depan.

### pages_user
Berisi file Python untuk semua tampilan utama yang dapat diakses oleh pengguna biasa (e.g., Halaman Beranda, Halaman Daftar Putar, Halaman Pencarian).

### app.py
File eksekusi utama. File ini bertanggung jawab untuk:

  a. Menginisialisasi aplikasi CTK.
  b. Menggabungkan semua components dan pages yang berbeda.
  c. Bertindak sebagai penghubung (controller) antara GUI dan logic.

### login.py
File yang secara spesifik menangani fungsionalitas Login dan Registrasi Pengguna.

### main.py
Modul alternatif atau legacy untuk menjalankan aplikasi. Dalam arsitektur modern, seringkali app.py menjadi titik masuk utama, dan main.py dapat menjadi loader sederhana.

### songs_store.json
Sumber data lagu yang diperbarui dari file .csv di Tahap 1. Menggunakan format JSON lebih disukai untuk data terstruktur yang akan mudah diproses di Python.

### __pycache__ 
Dibuat secara otomatis oleh Python untuk menyimpan bytecode yang dikompilasi, fungsinya adalah mempercepat waktu loading modul.
