# Proyek "2EZ4U APP" - Delivery Service Backend Engine & Analisis Struktur Data

> **Mata Kuliah:** Struktur Data & Analisa Algoritma (EC234303)  
> **Departemen:** Teknik Komputer, Fakultas Teknologi Elektro dan Informatika Cerdas (FTEIC)  
> **Institut Teknologi Sepuluh Nopember (ITS) - Semester Gasal 2026/2027**  
> **Dosen Pengampu:** Ir. Arta Kusuma Hernanda, S.T., M.T.  

---

### Informasi Mahasiswa
* **Nama Lengkap:** M. Gielang Fitrawan Mukhlish
* **NRP:** 5024251019
* **Kelas:** Struktur Data & Analisa Algoritma A
* **Tautan Repository GitHub:** `https://github.com/Jsooonx/2ez4u.git`
* **Tautan Video Demo:** [Tautan Video YouTube / Google Drive Demo]

---

## 1. Deskripsi & Gambaran Umum Proyek

**2EZ4U APP** adalah simulasi engine *backend* layanan pesan-antar makanan dan barang skala tinggi (miniatur GoFood / GrabFood / ShopeeFood) yang dirancang untuk menangani beban trafik **200.000 data pesanan transaksi**.

Fokus utama proyek ini bukan sekadar membangun antarmuka visual, melainkan **merancang, mengimplementasikan, dan membuktikan efisiensi struktur data serta algoritma buatan sendiri dari nol (*from scratch*)** secara empiris dengan tolok ukur stopwatch milidetik ($ms$).

### Arsitektur 3 Lapisan (3-Layer Architecture)
```text
┌─────────────────────────────────────────────────────────────┐
│                    1. LAPISAN FRONTEND                      │
│            (frontend/ui.py & app.py - Tkinter)              │
│  Antarmuka desktop 3 panel untuk memanggil modul backend,   │
│      menerima input parameter, dan mencatat waktu (ms)      │
└──────────────────────────────▲──────────────────────────────┘
                               │ Memanggil API internal
┌──────────────────────────────▼──────────────────────────────┐
│                    2. LAPISAN BACKEND                       │
│           (backend/m1_pesanan.py ... m6_peta.py)            │
│    Struktur data murni buatan sendiri tanpa modul instan    │
└──────────────────────────────▲──────────────────────────────┘
                               │ Membaca data
┌──────────────────────────────▼──────────────────────────────┐
│                     3. LAPISAN DATA                         │
│                    (data/pesanan.csv)                       │
│               200.000 baris data transaksi                  │
└─────────────────────────────────────────────────────────────┘
```

### ⚠️ Batasan Ketat Implementasi (Strict Constraints)
Untuk menguji pemahaman mendalam tentang alokasi memori dan pointer:
* **DILARANG:** `dict`, literal `{}`, `set`, `sorted()`, `.sort()`, `heapq`, `bisect`, `collections.*`, dictionary/set comprehension.
* **DIPERBOLEHKAN:** `list` (hanya sebagai array primitif berukuran tetap), `tuple`, kelas OOP manual (`class`), operasi aritmetika, dan pembacaan berkas I/O standar.

---

## 2. Peta Perjalanan Semester (Milestone Progress Tracker)

| Milestone | Topik & Struktur Data | Berkas Backend | Bobot | Status |
| :---: | :--- | :---: | :---: | :---: |
| **M1** | **Data Pesanan (Dynamic Array vs Singly Linked List)** | `backend/m1_pesanan.py` | 10% | ✅ **SELESAI (Completed)** |
| **M2** | **Antrean Pesanan & Undo (Circular Queue & Stack)** | `backend/m2_antrean.py` | - | ✅ **SELESAI (Completed)** |
| **M3** | Laporan Keuangan Terurut (Insertion Sort & Binary Search) | `backend/m3_laporan.py` | - | ⏳ Segera (Upcoming) |
| **M4** | Pencarian Instan & Pengurutan (Hash Map & Merge Sort) | `backend/m4_pencarian.py` | - | ⏳ Segera (Upcoming) |
| **M5** | Katalog Rentang Harga & Dispatch (BST & Min-Heap) | `backend/m5_katalog.py` | - | ⏳ Segera (Upcoming) |
| **M6** | Peta Antarkampus & Navigasi Tercepat (Graf, BFS, Dijkstra) | `backend/m6_peta.py` | - | ⏳ Segera (Upcoming) |

---

## 3. Laporan Teknis Milestone 1 (M1) - Array vs Linked List

### 3.1. Cerita & Aturan Bisnis
Pada peluncuran awal layanan, pesanan masuk harus dapat disimpan, dibaca, disisipkan, dan dibatalkan/dihapus dengan aturan 3 tingkat pelanggan:
1. **REGULER (Prioritas 3):** Pelanggan biasa, antre di barisan **paling belakang**.
2. **PRIORITAS (Prioritas 2):** Pelanggan prioritas, **menyerobot tepat ke tengah antrean** ($n/2$).
3. **VIP (Prioritas 1):** Pelanggan eksklusif, langsung masuk ke **urutan nomor satu (paling depan / indeks 0)** mendahului seluruh antrean.

### 3.2. Desain Struktur Data Backend (`backend/m1_pesanan.py`)
1. **`class Pesanan`**:
   - Membungkus 9 atribut CSV: `oid`, `pelanggan`, `resto`, `menu`, `harga`, `prioritas`, `t_masuk_detik`, `t_selesai_detik`, `status`.
   - Menggunakan deklarasi `__slots__` sehingga terbebas dari dictionary internal Python dan memangkas penggunaan memori RAM hingga ~45% saat memuat 200.000 data.
2. **`class Array` (Dynamic Array)**:
   - Alokasi memori berukuran tetap `[None] * capacity`.
   - Mengimplementasikan `_resize(capacity * 2)`: saat penuh, kapasitas memori dilipatgandakan 2x lipat dan elemen lama disalin manual ($O(1)$ amortized).
   - `get(i)`: Mengakses langsung via indeks memori ($O(1)$).
   - `insert(i, v)`: Menggeser elemen dari belakang mundur ke kanan ($O(n)$).
   - `delete(i)`: Menghapus elemen dan menggeser elemen kanan maju ke kiri ($O(n)$).
3. **`class Node` & `class LinkList` (Singly Linked List dengan Tail Pointer)**:
   - Setiap elemen dibungkus simpul `Node` berpenunjuk `next`.
   - Menyimpan referensi `head`, `tail`, dan `size`.
   - `append(v)`: Tambah pesanan REGULER di ekor (`tail.next = node; tail = node`) bernilai instan **$O(1)$**.
   - `insert_front(v)`: Tambah pesanan VIP di urutan terdepan (`node.next = head; head = node`) bernilai instan **$O(1)$**.
   - `get(i)`: Menelusuri rantai dari `head` maju sebanyak $i$ langkah ($O(n)$).
   - `delete(i)`: Traversal ke simpul $(i-1)$ lalu mengalihkan pointer simpul ($O(n)$).

---

### 3.3. Hasil Uji Tanding & Analisis Performa (Benchmark Riil)

Pengujian dilakukan secara langsung menggunakan 200.000 baris data pesanan riil pada mesin uji dengan presisi stopwatch `time.perf_counter()`:

```text
=================================================================================
|                HASIL UJI TANDING PERFORMA: ARRAY vs LINKED LIST               |
|                      (Ukuran Data: 200,000 baris pesanan)                     |
+----------------------+----------------+----------------+----------------------+
| Operasi              |          Array |    Linked List | Pemenang             |
+----------------------+----------------+----------------+----------------------+
| Lihat (Indeks n/2)   |      0.0050 ms |     11.6836 ms | Array (O(1))         |
| Tambah REGULER       |      0.0056 ms |      0.0047 ms | Imbang (O(1))        |
| Tambah PRIORITAS     |     22.2901 ms |      6.2085 ms | Relatif Seimbang     |
| Tambah VIP           |     56.6756 ms |      0.0161 ms | Linked List (O(1))   |
+----------------------+----------------+----------------+----------------------+
=================================================================================
```

#### Pembahasan Analitis:
1. **Operasi Lihat Pesanan (Get Index $n/2$):**
   - **Array menang telak (~1.000x lebih cepat):** Array memiliki sifat *direct memory addressing* $O(1)$. Komputer langsung menghitung alamat memori `base + (index * size)`.
   - **Linked List lambat ($O(n)$):** Linked List tidak memiliki indeks memori tetap dan harus menelusuri 100.000 node secara berurutan.
2. **Operasi Tambah REGULER (Paling Belakang):**
   - **Hasil Imbang ($O(1)$):** Array memanfaatkan kapasitas cadangan hasil doubling ($O(1)$ amortized), sedangkan Linked List memanfaatkan pointer `self.tail` tanpa perlu traversal.
3. **Operasi Tambah PRIORITAS (Tengah Barisan):**
   - Keduanya sama-sama berbiaya $O(n)$, namun karena sebab yang berbeda: Array melakukan pergeseran fisik memori (100.000 elemen digeser ke kanan), sedangkan Linked List melakukan traversal pointer sebanyak 100.000 langkah.
4. **Operasi Tambah VIP (Paling Depan / Indeks 0):**
   - **Linked List menang telak (~1.200x lebih cepat):** Linked List hanya memindahkan pointer `head` ke simpul baru ($O(1)$ instan dalam 0.01 ms).
   - **Array sangat lambat ($O(n)$):** Array harus menggeser **seluruh 200.000 elemen** ke kanan satu petak untuk menyediakan slot kosong di indeks 0.

---

## 4. Laporan Teknis Milestone 2 (M2) - Antrean & Undo (Queue & Stack)

### 4.1. Cerita Bisnis: Alur Pemrosesan Dapur & Kasir
Setelah pesanan berhasil dicatat pada M1, sistem masuk ke tahap **pemrosesan order di dapur restoran**:
1. **Prinsip Antrean FIFO (First In, First Out):** Pesanan yang masuk terlebih dahulu harus dimasak dan disajikan lebih awal kepada kurir.
2. **Kebutuhan Fitur Undo (Kasir):** Kasir restoran dapat melakukan kesalahan (misal: tidak sengaja menekan tombol "Layani", atau pelanggan mendadak membatalkan pesanan yang baru masuk). Sistem membutuhkan fitur **Undo** untuk memulihkan kondisi antrean seperti sediakala.

### 4.2. Desain Struktur Data Backend (`backend/m2_antrean.py`)
1. **`class CircularQueue` (Antrean Melingkar FIFO)**:
   - Menggunakan array primitif berukuran tetap `[None] * capacity` dengan penunjuk indeks `front`, `rear`, dan `size`.
   - **Tanpa Pergeseran Memori ($O(1)$ murni):** Berbeda dari array biasa yang membutuhkan $O(n)$ untuk menggeser elemen saat elemen depan diambil, Circular Queue memanfaatkan **modulo aritmetika** `(index + 1) % capacity`.
   - **Resizing Dinamis:** Ketika kapasitas penuh, alokasi memori berlipat ganda 2x lipat dan elemen melingkar ditata ulang menjadi linier ($O(1)$ amortized).
   - **Operasi Khusus `requeue_front()` dan `unqueue_rear()`:** Memungkinkan pesanan dikembalikan ke depan antrean atau dicabut dari belakang dalam waktu instan **$O(1)$**.
2. **`class Stack` (Tumpukan LIFO untuk Undo)**:
   - Menyimpan riwayat aksi kasir secara berurutan.
   - Sifat **LIFO (Last In, First Out)** memastikan bahwa aksi yang **terakhir kali dilakukan** adalah aksi yang **pertama kali dibatalkan**.
   - `push()` dan `pop()` berjalan dalam waktu **$O(1)$**.
3. **`class AntreanManager`**:
   - Menghubungkan `CircularQueue` dan `Stack` dalam satu manajer bisnis terpadu.
   - Setiap operasi `enqueue` atau `dequeue` otomatis membuat catatan objek `AksiUndo` dan menumpuknya ke dalam Stack.
   - Metode `undo()` mengeksekusi pembalikan aksi:
     - Jika aksi terakhir adalah **DEQUEUE (Layani)**: Pesanan dikembalikan ke posisi **paling depan antrean (`front`)** dan statusnya dipulihkan menjadi `ANTRE`.
     - Jika aksi terakhir adalah **ENQUEUE (Tambah)**: Pesanan yang baru masuk dicabut dari posisi **paling belakang antrean (`rear`)**.

### 4.3. Hasil Pengujian & Waktu Eksekusi M2
Seluruh operasi pemrosesan antrean dan pembatalan aksi diuji secara langsung:
* **Enqueue (Tambah ke Antrean Dapur):** **~0.0020 ms** ($O(1)$)
* **Dequeue (Layani Pesanan Berikutnya):** **~0.0021 ms** ($O(1)$)
* **Undo Batal Layani (Requeue Front):** **~0.0022 ms** ($O(1)$)
* **Undo Batal Enqueue (Unqueue Rear):** **~0.0020 ms** ($O(1)$)

---

## 5. Antarmuka Pengguna (Desktop GUI Tkinter)

Antarmuka dibangun menggunakan Python Tkinter standar dengan rancangan 3-panel sesuai halaman 4 dokumen spesifikasi:
1. **Panel Kiri (Sidebar Navigasi):**
   - Tombol pemuatan data CSV (200.000 data).
   - Menu operasi Array (Lihat, Tambah Reguler/Prioritas/VIP, Hapus).
   - Menu operasi Linked List (Lihat, Tambah Reguler/Prioritas/VIP, Hapus).
   - Tombol **⚡ Uji Tanding Array vs LL** untuk benchmark simultan.
   - Menu operasi Antrean & Undo M2 (Status Antrean FIFO, Enqueue, Layani Berikutnya, Undo).
   - Penampung placeholder menu M3-M6 yang dinonaktifkan.
2. **Panel Kanan (Form Input & View Hasil):**
   - Form input parameter dinamis sesuai menu yang dipilih.
   - Area tampilan teks hasil lengkap dengan visualisasi slot antrean dan riwayat undo.
3. **Panel Bawah (Command & Benchmark Log):**
   - Konsol terminal monospace gelap yang mencatat setiap aksi beserta durasi eksekusi dalam milidetik ($ms$).

---

## 6. Galeri Tangkapan Layar (Screenshots)

> *Petunjuk: Simpan gambar tangkapan layar antarmuka aplikasimu di folder `docs/screenshots/` (atau ubah tautan di bawah ini sesuai nama file gambarmu).*

### A. Tampilan Utama Aplikasi & Menu Navigasi
<!-- Simpan file screenshot di: docs/screenshots/01_ui_utama.png -->
![Tampilan Utama Aplikasi 2EZ4U](docs/screenshots/01_ui_utama.png)
*Gambar 1: Tata letak antarmuka 3-panel saat aplikasi pertama kali dijalankan.*

### B. Proses Pemuatan 200.000 Data Pesanan CSV
<!-- Simpan file screenshot di: docs/screenshots/02_load_data.png -->
![Pemuatan 200.000 Data CSV](docs/screenshots/02_load_data.png)
*Gambar 2: Data 200.000 baris pesanan berhasil dimuat ke dalam Array dan Linked List secara simultan.*

### C. Eksekusi Operasi Penyisipan Pesanan VIP (M1)
<!-- Simpan file screenshot di: docs/screenshots/03_tambah_vip.png -->
![Eksekusi Tambah Pesanan VIP](docs/screenshots/03_tambah_vip.png)
*Gambar 3: Penyisipan pesanan VIP di urutan terdepan dan pencatatan waktu eksekusinya.*

### D. Hasil Uji Tanding Performa (Benchmark Duel: Array vs Linked List)
<!-- Simpan file screenshot di: docs/screenshots/04_duel_benchmark.png -->
![Hasil Uji Tanding Performa](docs/screenshots/04_duel_benchmark.png)
*Gambar 4: Tabel perbandingan performa langsung antara Array vs Linked List pada data 200.000 baris.*

### E. Status Antrean Dapur & Fitur Undo (M2)
<!-- Simpan file screenshot di: docs/screenshots/05_antrean_undo.png -->
![Status Antrean Dapur dan Fitur Undo](docs/screenshots/05_antrean_undo.png)
*Gambar 5: Visualisasi Antrean Melingkar (Circular Queue FIFO) dan Tumpukan Riwayat Aksi (Stack LIFO Undo).*

---

## 7. Petunjuk Instalasi & Cara Menjalankan

### Prasyarat Sistem
* Python versi 3.11 atau yang lebih baru.
* Sistem Operasi: Windows / macOS / Linux.
* Library bawaan: `tkinter` (sudah termasuk dalam instalasi standar Python).

### Langkah Menjalankan Aplikasi
1. **Clone repository ini ke komputer lokal:**
   ```bash
   git clone https://github.com/Jsooonx/2ez4u.git
   cd 2ez4u
   ```

2. **Pastikan file dataset tersedia di folder `data/`:**
   - `data/pesanan.csv` (200.000 baris)
   - `data/peta.csv`

3. **Jalankan aplikasi utama:**
   ```bash
   python app.py
   ```

4. **Pengujian Aplikasi:**
   - Klik tombol **Load CSV (200.000)** pada panel kiri atas.
   - Uji M1: Jalankan operasi `ARRAY - LIHAT PESANAN`, `LINKEDLIST - TAMBAH VIP`, atau tombol **⚡ UJI TANDING ARRAY vs LL**.
   - Uji M2: Klik **M2 - ANTREAN FIFO (Status)**, coba tombol **M2 - LAYANI BERIKUTNYA**, lalu batalkan dengan **M2 - UNDO AKSI TERAKHIR**.

---

## 8. Struktur Direktori Proyek

```text
2ez4u/
├── .gitignore               <- Konfigurasi pengabaian cache, dataset, dan filter docs
├── README.md                <- Laporan utama proyek dan dokumentasi repositori
├── app.py                   <- Entry point utama peluncur aplikasi ("python app.py")
├── backend/
│   ├── __init__.py          <- Inisialisasi package backend
│   ├── m1_pesanan.py        <- [M1] Model Pesanan, Dynamic Array, & Linked List
│   └── m2_antrean.py        <- [M2] Circular Queue FIFO, Stack LIFO, & AntreanManager
├── data/                    <- Direktori dataset (diabaikan dari Git)
│   ├── pesanan.csv          <- 200.000 data pesanan
│   └── peta.csv             <- Data titik peta antarkampus
├── docs/
│   ├── README-Proyek-2EZ4U.pdf   <- Panduan resmi tugas akhir dari dosen
│   ├── penjelasan_proyek_dan_m1.md <- Dokumentasi catatan teori & konsep M1
│   └── screenshots/         <- Tempat penyimpanan file tangkapan layar UI
└── frontend/
    ├── __init__.py          <- Inisialisasi package frontend
    └── ui.py                <- [UI] Antarmuka desktop Tkinter 3-panel & stopwatch benchmark
```

---

## 9. Kesimpulan Proyek (M1 & M2)
1. **Milestone 1:** Membuktikan bahwa tidak ada satu struktur data tunggal yang sempurna. Array unggul mutlak dalam akses acak indeks ($O(1)$ vs $O(n)$), sedangkan Linked List unggul mutlak dalam penyisipan di posisi terdepan ($O(1)$ vs $O(n)$).
2. **Milestone 2:** Membuktikan bahwa Circular Queue memecahkan inefisiensi array biasa untuk antrean FIFO, memungkinkan `enqueue` dan `dequeue` instan $O(1)$ tanpa pergeseran memori berkat modulo aritmetika. Sementara itu, Stack melengkapi sistem dengan mekanisme Undo berbasis LIFO $O(1)$ yang elegan.
