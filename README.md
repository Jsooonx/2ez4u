# Proyek 2EZ4U APP - Delivery Service Backend Engine & Analisis Struktur Data

> **Mata Kuliah:** Struktur Data & Analisa Algoritma (EC234303)  
> **Departemen:** Teknik Komputer, Fakultas Teknologi Elektro dan Informatika Cerdas (FTEIC)  
> **Institut Teknologi Sepuluh Nopember (ITS) - Semester Gasal 2026/2027**  
> **Dosen Pengampu:** Ir. Arta Kusuma Hernanda, S.T., M.T.  

---

### Informasi Mahasiswa
* **Nama Lengkap:** M. Gielang Fitrawan Mukhlish
* **NRP:** 5024251019
* **Kelas:** Struktur Data & Analisa Algoritma A
* **Repository GitHub:** `https://github.com/Jsooonx/2ez4u.git`
* **Video Demo:** [Tautan Video YouTube / Google Drive Demo]

---

## 1. Gambaran Umum Proyek & Aturan Main

**2EZ4U APP** adalah simulasi engine *backend* layanan pesan-antar makanan berskala tinggi yang menguji performa struktur data buatan sendiri (*from scratch*) pada dataset transaksi **200.000 pesanan** (`data/pesanan.csv`).

### Arsitektur 3 Lapisan
1. **Data Layer (`data/`):** Menyimpan 200.000 data CSV pesanan transaksi dan peta antarkampus.
2. **Backend Layer (`backend/`):** Enam modul struktur data mandiri dari M1 hingga M6 tanpa library instan.
3. **Frontend Layer (`frontend/` & `app.py`):** Antarmuka desktop 3-panel Tkinter untuk pengujian operasi dan stopwatch milidetik ($ms$).

### Batasan Implementasi
* **Dilarang:** `dict`, literal `{}`, `set`, `sorted()`, `.sort()`, `heapq`, `bisect`, `collections.*`, dictionary/set comprehension.
* **Diperbolehkan:** `list` (sebagai array primitif berukuran tetap), `tuple`, class OOP manual, operasi aritmetika, dan standard file I/O.

---

## 2. Peta Perjalanan Milestone

| Milestone | Topik & Struktur Data | Berkas Backend | Status |
| :---: | :--- | :---: | :---: |
| **M1** | **Data Pesanan (Dynamic Array vs Singly Linked List)** | `backend/m1_pesanan.py` | Selesai |
| **M2** | **Antrean Pesanan & Undo (Circular Queue & Stack)** | `backend/m2_antrean.py` | Selesai |
| **M3** | **Laporan Terurut & Pencarian Cepat (Insertion Sort & Binary Search)** | `backend/m3_laporan.py` | Selesai |
| **M4** | Pencarian Instan & Pengurutan (Hash Map & Merge Sort) | `backend/m4_pencarian.py` | Segera |
| **M5** | Katalog Rentang Harga & Dispatch (BST & Min-Heap) | `backend/m5_katalog.py` | Segera |
| **M6** | Peta Antarkampus & Navigasi Tercepat (Graf, BFS, Dijkstra) | `backend/m6_peta.py` | Segera |

---

## 3. Milestone 1 (M1) - Array vs Singly Linked List

### 3.1. Aturan Bisnis & Desain Backend (`backend/m1_pesanan.py`)
M1 mengelola penyimpanan pesanan dengan aturan tiga tingkatan prioritas:
* **Reguler (Prioritas 3):** Antre di barisan paling belakang.
* **Prioritas (Prioritas 2):** Menyerobot ke tengah barisan ($n/2$).
* **VIP (Prioritas 1):** Langsung ke urutan pertama (indeks 0).

Implementasi:
* **`Pesanan`**: 9 atribut CSV dengan `__slots__` untuk memangkas konsumsi RAM hingga ~45%.
* **`Array`**: Fixed array berkapasitas dinamis (`_resize` doubling 2x lipat). Akses $O(1)$, insert/delete $O(n)$ karena pergeseran memori.
* **`LinkList`**: Singly linked list dengan pointer `head`, `tail`, dan `size`. Akses $O(n)$, insert depan (VIP) dan insert belakang (Reguler) instan $O(1)$.

### 3.2. Hasil Benchmark Riil M1 (200.000 Data)
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

---

## 4. Milestone 2 (M2) - Circular Queue & Stack (Undo)

### 4.1. Alur Dapur & Mekanisme Undo (`backend/m2_antrean.py`)
* **Circular Queue (FIFO Dapur):** Menggunakan fixed array `[None] * capacity` dengan penunjuk `front` dan `rear`. Menggunakan modulo aritmetika `(index + 1) % capacity` sehingga `enqueue` dan `dequeue` murni $O(1)$ tanpa menggeser ratusan ribu data.
* **Stack (LIFO Undo):** Mencatat riwayat aksi kasir secara berurutan. Operasi `push()` dan `pop()` berjalan dalam $O(1)$.
* **Operasi Pemulihan Undo:**
  - Batal Layani (Dequeue): Pesanan dikembalikan ke depan antrean via `requeue_front()` dengan rumus `(front - 1 + capacity) % capacity` ($O(1)$).
  - Batal Masuk (Enqueue): Pesanan dicabut dari belakang via `unqueue_rear()` dengan rumus `(rear - 1 + capacity) % capacity` ($O(1)$).

### 4.2. Perbandingan Kompleksitas & Benchmark Riil M2
| Operasi | Array Biasa (`list.pop(0)`) | Circular Queue | Stack (Undo) | Waktu Riil |
| :--- | :---: | :---: | :---: | :---: |
| Enqueue Antrean | $O(1)$ amortized | **$O(1)$ amortized** | - | 0.0020 ms |
| Dequeue Layani | $O(n)$ (geser data) | **$O(1)$ murni** | - | 0.0021 ms |
| Undo Batal Layani | $O(n)$ (`insert(0)`) | **$O(1)$ murni** | - | 0.0022 ms |
| Undo Batal Masuk | $O(1)$ | **$O(1)$** | - | 0.0020 ms |
| Push / Pop Stack | - | - | **$O(1)$** | 0.0018 ms |

---

## 5. Milestone 3 (M3) - Laporan Terurut & Binary Search

### 5.1. Rekapitulasi & Desain Algoritma (`backend/m3_laporan.py`)
M3 menyortir laporan keuangan transaksi harian dan mempercepat pencarian audit:
* **`insertion_sort`**: Algoritma utama *in-place* $O(n^2)$. Bersifat adaptif (mendekati $O(n)$ jika data hampir terurut).
* **`selection_sort` & `bubble_sort`**: Algoritma pembanding untuk pembuktian empiris.
* **`binary_search`**: Membagi ruang pencarian menjadi dua di setiap langkah ($O(\log n)$), memangkas waktu pencarian secara drastis dibanding Linear Search ($O(n)$).
* **`LaporanManager`**: Mengelola penyaringan batch data, menghitung statistik omset (total, rata-rata, min, max), dan menjalankan benchmark duel sort.

### 5.2. Hasil Uji Tanding Sorting M3 (500 Data)
```text
=================================================================================
|               HASIL UJI TANDING ALGORITMA SORTING M3 (500 DATA)               |
|                 Kunci Pengurutan: Nominal Harga (Rp) Ascending                |
+---------------------+-----------------+---------------+-----------------------+
| Algoritma Sorting   |  Waktu Eksekusi | Kompleksitas  | Efisiensi             |
+---------------------+-----------------+---------------+-----------------------+
| Insertion Sort      |       5.2104 ms | O(n^2)        | Tercepat (Adaptive)   |
| Selection Sort      |      14.8320 ms | O(n^2)        | Stabil Min Swap       |
| Bubble Sort         |      18.6415 ms | O(n^2)        | Banyak Swap           |
+---------------------+-----------------+---------------+-----------------------+
=================================================================================
```

### 5.3. Pembuktian Binary Search vs Linear Search (Target Rp15.000 pada 1.000 Data)
| Algoritma Pencarian | Langkah Komparasi | Durasi Eksekusi | Kompleksitas |
| :--- | :---: | :---: | :---: |
| **Binary Search** | **1 langkah** | **0.0316 ms** | **$O(\log n)$** |
| **Linear Search** | 449 langkah | 0.0541 ms | $O(n)$ |

---

## 6. Antarmuka Pengguna (Desktop GUI Tkinter)

Antarmuka dibangun dengan Python Tkinter standar melalui layout 3 panel:
1. **Panel Kiri (Sidebar Navigasi):** Memuat data CSV, menu operasi M1 (Array vs LinkList), M2 (Antrean FIFO & Undo), serta M3 (Laporan Terurut, Binary Search, dan Duel Sorting).
2. **Panel Kanan (Form Parameter & Detail Hasil):** Input parameter dinamis serta area tampilan teks hasil dengan border monospace ASCII 81-karakter yang rapi.
3. **Panel Bawah (Command & Benchmark Log):** Konsol terminal yang mencatat riwayat pemanggilan fungsi dan stopwatch eksekusi ($ms$).

---

## 7. Galeri Tangkapan Layar (Screenshots)

### A. Tampilan Utama Aplikasi
![Tampilan Utama Aplikasi 2EZ4U](docs/screenshots/01_ui_utama.png)

### B. Pemuatan 200.000 Data CSV
![Pemuatan 200.000 Data CSV](docs/screenshots/02_load_data.png)

### C. Operasi Penyisipan Pesanan VIP (M1)
![Eksekusi Tambah Pesanan VIP](docs/screenshots/03_tambah_vip.png)

### D. Uji Tanding Array vs Linked List (M1)
![Hasil Uji Tanding Performa](docs/screenshots/04_duel_benchmark.png)

### E. Status Antrean Dapur & Undo (M2)
![Status Antrean Dapur dan Fitur Undo](docs/screenshots/05_antrean_undo.png)

### F. Laporan Terurut & Binary Search (M3)
![Laporan Harian Terurut dan Binary Search](docs/screenshots/06_laporan_m3.png)

---

## 8. Petunjuk Instalasi & Menjalankan

### Prasyarat
* Python 3.11 atau lebih baru.
* Library standar `tkinter` (bawaan instalasi Python).

### Langkah Menjalankan
1. Clone repositori:
   ```bash
   git clone https://github.com/Jsooonx/2ez4u.git
   cd 2ez4u
   ```
2. Pastikan file `data/pesanan.csv` dan `data/peta.csv` tersedia di folder `data/`.
3. Jalankan aplikasi utama:
   ```bash
   python app.py
   ```
4. Klik **Load CSV (200.000)** di sidebar kiri atas, lalu jalankan pengujian operasi M1, M2, atau M3.

---

## 9. Struktur Direktori Proyek

```text
2ez4u/
├── .gitignore
├── README.md
├── app.py
├── backend/
│   ├── __init__.py
│   ├── m1_pesanan.py        <- [M1] Model Pesanan, Dynamic Array, & Linked List
│   ├── m2_antrean.py        <- [M2] Circular Queue FIFO, Stack LIFO, & AntreanManager
│   └── m3_laporan.py        <- [M3] Insertion Sort, Selection Sort, Bubble Sort, & Binary Search
├── data/                    <- Direktori dataset (diabaikan dari Git)
│   ├── pesanan.csv
│   └── peta.csv
├── docs/
│   ├── README-Proyek-2EZ4U.pdf      <- Panduan resmi tugas akhir
│   ├── penjelasan_proyek_dan_m1.md  <- Catatan teori M1
│   ├── penjelasan_m2.md             <- Catatan teori M2
│   ├── penjelasan_m3.md             <- Catatan teori M3
│   └── screenshots/                 <- Tangkapan layar antarmuka
└── frontend/
    ├── __init__.py
    └── ui.py                <- Antarmuka desktop Tkinter 3-panel
```

---

## 10. Kesimpulan Proyek (M1, M2, & M3)

1. **M1 (Array vs Linked List):** Array unggul mutlak dalam akses acak memori ($O(1)$ vs $O(n)$), sementara Linked List unggul mutlak dalam penyisipan di posisi terdepan ($O(1)$ vs $O(n)$).
2. **M2 (Circular Queue & Stack):** Circular Queue memecahkan inefisiensi array biasa untuk antrean FIFO ($O(1)$ tanpa pergeseran memori via modulo), sementara Stack memfasilitasi fitur Undo kasir berbasis LIFO $O(1)$.
3. **M3 (Sorting & Binary Search):** Pengurutan data membuka akselerasi pencarian eksponensial melalui Binary Search ($O(\log n)$ dibanding Linear Search $O(n)$). Di antara algoritma kuadratik, Insertion Sort terbukti paling adaptif dan efisien.
