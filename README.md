# Proyek 2EZ4U APP - Delivery Service Backend Engine

> **Mata Kuliah:** Struktur Data & Analisa Algoritma (EC234303) - FTEIC ITS (Gasal 2026/2027)  
> **Dosen Pengampu:** Ir. Arta Kusuma Hernanda, S.T., M.T.  
> **Mahasiswa:** M. Gielang Fitrawan Mukhlish (NRP: 5024251019) - Kelas A  
> **Repository:** `https://github.com/Jsooonx/2ez4u.git` | **Video Demo:** [Tautan Video Demo]

---

## 1. Gambaran Umum & Batasan Sistem

**2EZ4U APP** adalah simulasi engine backend layanan pesan-antar makanan berskala besar yang menguji efisiensi struktur data buatan sendiri (*from scratch*) pada dataset transaksi **200.000 pesanan** (`data/pesanan.csv`).

* **Arsitektur:** 3 Lapisan (Data Layer `data/`, Backend Struktur Data `backend/`, Desktop GUI Tkinter `frontend/`).
* **Batasan Ketat:**
  - Dilarang: `dict`, `{}`, `set`, `sorted()`, `.sort()`, `heapq`, `bisect`, `collections.*`, dan *comprehension*.
  - Diperbolehkan: `list` (array primitif tetap `[None] * capacity`), `tuple`, class OOP manual, aritmetika, dan file I/O.

---

## 2. Status Milestone

| Milestone | Struktur Data & Algoritma | Berkas Backend | Status |
| :-: | :--- | :---: | :-: |
| **M1** | Dynamic Array vs Singly Linked List (Model `Pesanan` 200k) | `backend/m1_pesanan.py` | Selesai |
| **M2** | Circular Queue FIFO & Stack LIFO (Antrean Dapur & Undo Kasir) | `backend/m2_antrean.py` | Selesai |
| **M3** | Sorting Kuadratik & Binary Search (Laporan Omset & Pencarian Cepat) | `backend/m3_laporan.py` | Selesai |
| **M4** | Hash Map Chaining & Merge Sort | `backend/m4_pencarian.py` | Segera |
| **M5** | Binary Search Tree & Min-Heap Dispatch | `backend/m5_katalog.py` | Segera |
| **M6** | Graf Kampus, Algoritma BFS & Dijkstra | `backend/m6_peta.py` | Segera |

---

## 3. Milestone 1 (M1) - Dynamic Array vs Singly Linked List

Mengelola penyimpanan 200.000 pesanan dengan 3 tingkat prioritas: Reguler (belakang), Prioritas (tengah $n/2$), dan VIP (depan / indeks 0). Atribut `Pesanan` dioptimasi dengan `__slots__` untuk memangkas ~45% konsumsi memori RAM.

| Operasi (200.000 Data) | Array | Linked List | Analisis & Pemenang |
| :--- | :---: | :---: | :--- |
| Akses Indeks ($n/2$) | **0.005 ms** | 11.684 ms | **Array** ($O(1)$ vs $O(n)$ traversal) |
| Tambah Reguler (Belakang) | 0.006 ms | **0.005 ms** | **Imbang** ($O(1)$ amortized vs $O(1)$ tail pointer) |
| Tambah Prioritas (Tengah) | 22.290 ms | **6.209 ms** | **Linked List** (pergeseran $n/2$ elemen vs transversal pointer) |
| Tambah VIP (Depan) | 56.676 ms | **0.016 ms** | **Linked List** (~3.500x lebih cepat, $O(1)$ vs $O(n)$ shift) |

---

## 4. Milestone 2 (M2) - Circular Queue & Stack (Undo)

* **Circular Queue (FIFO Dapur):** Buffer melingkar berbasis indeks modulo `(idx + 1) % capacity` pada array tetap. Mencegah pergeseran data $O(n)$ pada antrean ratusan ribu item.
* **Stack (LIFO Undo Kasir):** Struktur tumpukan untuk mencatat riwayat transaksi kasir ($O(1)$).
* **Mekanisme Undo:** Membatalkan aksi kasir secara instan $O(1)$ melalui operasi khusus `requeue_front()` (rumus `(front - 1 + cap) % cap`) dan `unqueue_rear()` (rumus `(rear - 1 + cap) % cap`).

| Operasi Antrean & Kasir | Array Biasa (`pop(0)`) | Circular Queue | Stack (Undo) | Waktu Riil |
| :--- | :---: | :---: | :---: | :---: |
| Enqueue Antrean Dapur | $O(1)$ amortized | **$O(1)$ amortized** | - | 0.0020 ms |
| Dequeue Layani Pesanan | $O(n)$ (geser memori) | **$O(1)$ murni** | - | 0.0021 ms |
| Undo Batal Layani (`requeue_front`) | $O(n)$ (`insert(0)`) | **$O(1)$ murni** | - | 0.0022 ms |
| Undo Batal Masuk (`unqueue_rear`) | $O(1)$ | **$O(1)$** | - | 0.0020 ms |
| Push / Pop Riwayat Aksi | - | - | **$O(1)$** | 0.0018 ms |

---

## 5. Milestone 3 (M3) - Laporan Terurut & Binary Search

Menyortir transaksi harian berdasarkan nominal harga dan mempercepat audit pencarian target harga tanpa library bawaan.
* **Sorting Kuadratik ($O(n^2)$):** `insertion_sort` (algoritma utama, adaptif mendekati $O(n)$ jika data hampir terurut), dibandingkan dengan `selection_sort` (swap minimum) dan `bubble_sort`.
* **Pencarian Cepat:** `binary_search` membagi interval pencarian secara biner ($O(\log n)$) untuk memangkas waktu pencarian secara drastis dibanding `linear_search` ($O(n)$).

| Algoritma | Kategori | Waktu Riil | Kompleksitas | Kinerja & Evaluasi |
| :--- | :---: | :---: | :---: | :--- |
| **Insertion Sort** | Sorting (500 data) | **5.210 ms** | $O(n^2)$ | **Tercepat** (adaptif, geser minimum) |
| **Selection Sort** | Sorting (500 data) | 14.832 ms | $O(n^2)$ | Stabil (minim swap memori) |
| **Bubble Sort** | Sorting (500 data) | 18.642 ms | $O(n^2)$ | Paling lambat (banyak pertukaran elemen) |
| **Binary Search** | Pencarian (1.000 data) | **0.032 ms** | **$O(\log n)$** | **1 komparasi** (akselerasi drastis) |
| **Linear Search** | Pencarian (1.000 data) | 0.054 ms | $O(n)$ | 449 komparasi berurutan |

---

## 6. Antarmuka Desktop GUI Tkinter

Aplikasi dilengkapi antarmuka 3-panel: Panel Kiri (Navigasi & Menu Operasi), Panel Kanan (Form Input & Display ASCII Box 81 Karakter), dan Panel Bawah (Log Terminal & Stopwatch Milidetik).

| No | Modul / Skenario Pengujian | Tangkapan Layar |
| :-: | :--- | :--- |
| 1 | Tampilan Utama Aplikasi | ![UI Utama](docs/screenshots/01_ui_utama.png) |
| 2 | Pemuatan 200.000 Baris Data CSV | ![Load CSV](docs/screenshots/02_load_data.png) |
| 3 | Penyisipan Pesanan VIP Depan (M1) | ![Tambah VIP](docs/screenshots/03_tambah_vip.png) |
| 4 | Duel Benchmark Array vs Linked List (M1) | ![Duel M1](docs/screenshots/04_duel_benchmark.png) |
| 5 | Antrean Dapur FIFO & Fitur Undo (M2) | ![Antrean M2](docs/screenshots/05_antrean_undo.png) |
| 6 | Laporan Terurut & Binary Search (M3) | ![Laporan M3](docs/screenshots/06_laporan_m3.png) |

---

## 7. Petunjuk Instalasi & Menjalankan

1. **Clone repositori:**
   ```bash
   git clone https://github.com/Jsooonx/2ez4u.git
   cd 2ez4u
   ```
2. **Jalankan aplikasi:**
   ```bash
   python app.py
   ```
3. Klik tombol **Load CSV (200.000)** pada sidebar navigasi, lalu pilih operasi uji tanding M1, M2, atau M3.

---

## 8. Struktur Direktori

```text
2ez4u/
├── app.py                     <- Entry point aplikasi GUI Tkinter
├── backend/
│   ├── m1_pesanan.py          <- [M1] Model Pesanan, Dynamic Array, & Linked List
│   ├── m2_antrean.py          <- [M2] Circular Queue FIFO, Stack LIFO, & Undo
│   └── m3_laporan.py          <- [M3] Sorting Kuadratik & Binary Search
├── data/                      <- Dataset transaksi 200.000 pesanan (pesanan.csv)
├── docs/
│   ├── penjelasan_proyek_dan_m1.md  <- Laporan analisis teknis M1
│   ├── penjelasan_m2.md             <- Laporan analisis teknis M2
│   ├── penjelasan_m3.md             <- Laporan analisis teknis M3
│   └── screenshots/                 <- Berkas tangkapan layar GUI
└── frontend/
    └── ui.py                  <- Implementasi layout 3-panel Tkinter
```

---

## 9. Kesimpulan Teknis (M1 - M3)

1. **M1 (Array vs Linked List):** Array unggul mutlak pada akses acak $O(1)$, sedangkan Linked List unggul mutlak pada penyisipan di posisi terdepan ($O(1)$ vs $O(n)$ pergeseran memori).
2. **M2 (Circular Queue & Stack):** Circular Queue menghilangkan pergeseran memori $O(n)$ antrean FIFO via aritmetika modulo ($O(1)$), sementara Stack mencatat riwayat transaksi untuk pemulihan Undo instan ($O(1)$).
3. **M3 (Sorting & Binary Search):** Pengurutan data memungkinkan akselerasi pencarian eksponensial lewat Binary Search ($O(\log n)$). Di antara algoritma kuadratik, Insertion Sort terbukti paling adaptif dan efisien.
