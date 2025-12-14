# Aplikasi MyMusic

## A. Tujuan Program

Tujuan dari pengembangan aplikasi Spotify CTK ini adalah untuk merancang dan mengimplementasikan sebuah aplikasi pemutar musik berbasis desktop menggunakan bahasa pemrograman Python dengan antarmuka grafis CustomTkinter. Aplikasi ini bertujuan untuk membantu pengguna dalam mengelola, memutar, dan mengorganisir koleksi lagu secara terstruktur dan efisien.

## B. Fitur Program
Ada 2 cara masuk akses diaplikasi MyMusic. Ada admin dan user:

Akses bagian Admin:

### 1. Halaman Dashboard
Halaman Dashboard Admin menampilkan ringkasan informasi utama dari database musik dalam bentuk kartu statistik, sehingga admin dapat dengan cepat mengetahui kondisi data lagu saat ini. yakni ada fitur:

    a. Total Lagu: jumlah seluruh lagu yang tersimpan dalam sistem
    b. Total Genre: jumlah genre musik yang tersedia
    c. Total Artis: jumlah artis yang tercatat

### 2. Database Lagu
Fitur Database Lagu berfungsi untuk menampilkan seluruh data lagu dalam bentuk tabel yang rapi dan mudah dibaca. Informasi yang ditampilkan meliputi:

    a. Judul lagu
    b. Nama artis
    c. Genre
    d. Tahun rilis
    e. Durasi lagu
    
#### Pada halaman ini juga tersedia fitur:
    a. Pencarian (Search) berdasarkan kategori tertentu seperti title, artist, year, dan genre
    b. Pagination untuk memudahkan navigasi data dalam jumlah besar
    c. Aksi Edit untuk mengubah data lagu
    d. Aksi Hapus untuk menghapus lagu dari database

### 3. Tambah Lagu Baru
Menu Tambah Baru digunakan untuk menambahkan data lagu secara manual ke dalam sistem. Admin dapat mengisi form yang tersedia, yang terdiri dari:

    a. Judul lagu
    b. Nama artis
    c. Genre
    d. Tahun rilis
    e. Durasi lagu

Setelah data diisi dengan benar, admin dapat menyimpan data dengan menekan tombol Simpan, dan lagu akan langsung ditambahkan ke database.

### 4. Import CSV
Fitur Import CSV memungkinkan admin untuk menambahkan banyak data lagu sekaligus menggunakan file CSV. Proses ini sangat membantu untuk pengelolaan data dalam jumlah besar. Alur penggunaan fitur ini adalah:

    a. Memilih file CSV yang berisi data lagu
    b. Melakukan pratinjau data yang akan diimpor
    c. Menekan tombol Konfirmasi Import untuk menyimpan data ke sistem
    
Fitur ini memastikan proses input data menjadi lebih cepat dan efisien.


Akses bagian User:

### 1.  Halaman Home
Di halaman home terdapat list lagu sebelumnya sudah diputar, terdapat juga fitur untuk play lagu yang di inginkan dan terdapat juga untuk pause, next lagu prev lagu, dan mengulang-ulang lagu tersebut.
terdapat juga fitur search untuk mencari lagu yang ingin diputar.

### 2. Halaman Playlist
Terdapat playlist user yang berisi lagu yang diisi sendiri oleh user tersebut.

### Keluar (Logout)
Tombol Keluar digunakan untuk mengakhiri sesi admin dan keluar dari aplikasi dengan aman.


## C. Algoritma yang Digunakan
Pada aplikasi MyMusic, beberapa algoritma dasar digunakan untuk mendukung pengelolaan data lagu agar berjalan secara efisien dan terstruktur. Algoritma-algoritma ini diimplementasikan menggunakan bahasa pemrograman Python.

### 1. Algoritma CRUD (Create, Read, Update, Delete)
#### Cara Kerja:
    a. Sistem menerima input dari admin melalui form atau file
    b. Data divalidasi agar sesuai format
    c. Data kemudian ditambahkan, ditampilkan, diperbarui, atau dihapus dari database

#### Implementasi:
    a. Create: digunakan saat admin menambah lagu baru atau import CSV
    b. Read: digunakan untuk menampilkan data lagu pada tabel database
    c. Update: digunakan saat admin mengedit informasi lagu
    d. Delete: digunakan saat admin menghapus lagu tertentu

Algoritma ini menjadi inti pengelolaan data pada aplikasi MyMusic.

### 2. Algoritma Pencarian (Searching)
#### Cara Kerja:
    a. Admin memilih kategori pencarian (judul, artis, tahun, genre)
    b. Admin memasukkan kata kunci pencarian
    c. Sistem membandingkan kata kunci dengan data lagu satu per satu
    d. Data yang cocok akan ditampilkan sebagai hasil pencarian

#### Implementasi:
    a. Menggunakan pencarian linear (linear search)
    b. Cocok untuk jumlah data menengah

Mudah diimplementasikan dan fleksibel

### 3. Algoritma Pagination
#### Cara Kerja:
    a. Sistem membagi data lagu ke dalam beberapa halaman
    b. Setiap halaman menampilkan jumlah data tertentu
    c. Admin dapat berpindah halaman menggunakan tombol navigasi

#### Implementasi:
    a. Data dipotong berdasarkan indeks awal dan akhir
    b. Membantu meningkatkan performa dan keterbacaan data

### 4. Algoritma Import Data CSV
#### Cara Kerja:
    a. Admin memilih file CSV
    b. Sistem membaca file baris per baris
    c. Setiap baris dipecah menjadi atribut lagu
    d. Data divalidasi lalu disimpan ke database

#### Implementasi:
    a. Menggunakan modul CSV Python
    b. Menghindari input manual satu per satu

### 5. Algoritma Backup Data (JSON)
#### Cara Kerja:
    a. Sistem mengambil seluruh data lagu yang tersimpan
    b. Data diubah ke format JSON
    c. File JSON disimpan sebagai cadangan data

#### Implementasi:
    a. Menggunakan serialisasi JSON
    b. Memudahkan proses backup dan restore data
    
#### 6. Struktur Data Doubly linked list
#### Cara Kerja:
    a. Setiap lagu disimpan dalam sebuah Node
    b. Setiap Node memiliki pointer prev dan next
    c. Memungkinkan navigasi dua arah (maju ke lagu berikutnya atau mundur ke lagu sebelumnya) dengan efisien

#### Implementasi:
    a. Digunakan pada Class SongLibrary dan Playlist untuk manajemen urutan lagu
    b. Operasi penyisipan (insert) dan penghapusan (delete) node dilakukan dengan memutus dan menyambung pointer antar node

#### 7. Algoritma Fuzzy Search
#### Cara Kerja:
    a. Menggunakan algoritma Levenshtein Distance untuk menghitung jarak perbedaan antara dua string
    b. Menghitung jumlah operasi minimum (penyisipan, penghapusan, atau penggantian karakter) yang diperlukan untuk mengubah kata kunci pencarian menjadi judul/artis lagu

#### Implementasi:
    a. Terdapat pada modul fuzzy_search.py
    b. Jika pengguna mengetik "Imagin", sistem tetap dapat menemukan lagu "Imagine" karena jarak editnya kecil

#### 8. Struktur Data Queue dan Stack (Playlist & History)
#### Cara Kerja:
    a. Queue (Antrean) Digunakan pada PlayerController untuk menyimpan daftar lagu yang akan diputar selanjutnya (next)
    b. Stack (Tumpukan): Digunakan untuk fitur History

#### Implementasi:
    a. Variabel self.queue pada controller_player.py berfungsi sebagai antrean lagu yang sedang aktif
    b. Variabel self.history berfungsi mencatat jejak lagu untuk navigasi mundur

#### 9. Algoritma Pengurutan (Sorting)
#### Cara Kerja:
    a. Mengambil seluruh node dari Linked List
    b. Membandingkan atribut tertentu (key) antar elemen
    c. Menyusun ulang urutan elemen berdasarkan abjad atau angka
    
#### Implementasi:
    a. Fungsi getSortedSongs pada library.py
    b. Menggunakan Timsort (algoritma sorting bawaan Python yang sangat efisien, gabungan Merge Sort dan Insertion Sort)

#### 10. Algoritma Fisher-Yates Shuffle (Pengacakan Lagu)
#### Cara Kerja:
    a. Algoritma membuat permutasi acak dari daftar lagu yang ada di antrean (queue)
    b. Memastikan setiap lagu memiliki peluang yang sama untuk muncul di urutan mana pun.

#### Implementasi:
    a. Fungsi toggleShuffle pada controller_player.py
    b. Memanfaatkan modul random untuk mengacak indeks antrean pemutaran



    

