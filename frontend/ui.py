"""
Antarmuka Pengguna (UI) Tkinter - Proyek 2EZ4U Food Delivery
Sesuai rancangan 3-panel di Buku Panduan EC234303 halaman 4:
1. Panel Kiri: Daftar Menu & Operasi (Data, M1 Array vs LinkList, Placeholder M2-M6)
2. Panel Kanan: Form Parameter Dinamis & Tampilan Hasil
3. Panel Bawah: Panel COMMAND / Log Pencatat Eksekusi & Waktu Benchmark (ms)
"""

import os
import time
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText

from backend.m1_pesanan import Array, LinkList, Pesanan, muat_pesanan_csv
from backend.m2_antrean import AntreanManager, CircularQueue, Stack, AksiUndo
from backend.m3_laporan import LaporanManager, insertion_sort, selection_sort, bubble_sort, binary_search, linear_search


class AppUI:
    def __init__(self, root):
        self.root = root
        self.root.title("2EZ4U Food Delivery - Engine Backend & Analisa Struktur Data")
        self.root.geometry("1100x720")
        self.root.minsize(960, 640)

        # State data M1
        self.array_pesanan = Array(capacity=8)
        self.linklist_pesanan = LinkList()
        self.data_loaded = False
        self.total_loaded = 0
        self.csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "pesanan.csv")

        # State data M2 (Antrean Melingkar FIFO & Tumpukan Undo)
        self.antrean_mgr = AntreanManager()

        # State data M3 (Laporan Terurut & Binary Search)
        self.laporan_mgr = LaporanManager()

        # Konfigurasi Tema & Style
        self._setup_styles()

        # Bangun 3 Panel Utama
        self._create_layout()

        # Inisialisasi tampilan default di panel kanan
        self.set_mode("ARRAY_LIHAT")

    def _setup_styles(self):
        self.colors = {
            "bg_main": "#f4f6f9",
            "sidebar_bg": "#ffffff",
            "sidebar_border": "#dcdfe6",
            "header_bg": "#1e293b",
            "accent_blue": "#2563eb",
            "accent_green": "#16a34a",
            "accent_amber": "#d97706",
            "accent_red": "#dc2626",
            "terminal_bg": "#0f172a",
            "terminal_fg": "#38bdf8",
            "terminal_dim": "#94a3b8",
        }

    def _create_layout(self):
        # Frame utama pembagi atas (kiri & kanan) dan bawah (terminal command)
        self.root.configure(bg=self.colors["bg_main"])

        # PanedWindow vertikal memisahkan (Area Kerja Atas) dan (Command Log Bawah)
        main_pane = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Container Atas
        top_container = ttk.Frame(main_pane)
        main_pane.add(top_container, weight=4)

        # PanedWindow horizontal memisahkan Sidebar (Kiri) dan Work Area (Kanan)
        horizontal_pane = ttk.PanedWindow(top_container, orient=tk.HORIZONTAL)
        horizontal_pane.pack(fill=tk.BOTH, expand=True)

        # 1. PANEL KIRI: SIDEBAR MENU
        self._build_sidebar(horizontal_pane)

        # 2. PANEL KANAN: WORK AREA & RESULT
        self._build_work_area(horizontal_pane)

        # 3. PANEL BAWAH: COMMAND & BENCHMARK LOG
        self._build_command_panel(main_pane)

    def _build_sidebar(self, parent):
        sidebar_frame = tk.Frame(parent, bg=self.colors["sidebar_bg"], width=280, relief=tk.SOLID, bd=1)
        sidebar_frame.pack_propagate(False)
        parent.add(sidebar_frame, weight=1)

        # Scrollable canvas untuk sidebar agar muat di semua ukuran layar
        canvas = tk.Canvas(sidebar_frame, bg=self.colors["sidebar_bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(sidebar_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_content = tk.Frame(canvas, bg=self.colors["sidebar_bg"])

        scrollable_content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_content, anchor="nw", width=265)
        canvas.configure(xscrollcommand=None, yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # SECTION: DATA
        self._add_section_header(scrollable_content, "DATA")
        btn_load = tk.Button(
            scrollable_content, text="📥 Load CSV (200.000)", bg="#3b82f6", fg="white",
            font=("Segoe UI", 9, "bold"), relief=tk.FLAT, pady=4, cursor="hand2",
            command=self.action_load_data
        )
        btn_load.pack(fill=tk.X, padx=10, pady=(2, 4))
        
        self.lbl_data_status = tk.Label(
            scrollable_content, text="Status: Data belum dimuat", bg=self.colors["sidebar_bg"],
            fg="#64748b", font=("Segoe UI", 8), anchor="w"
        )
        self.lbl_data_status.pack(fill=tk.X, padx=12, pady=(0, 8))

        # SECTION: M1 - DATA PESANAN
        self._add_section_header(scrollable_content, "M1 - DATA PESANAN")

        # Sub-header Array
        lbl_arr = tk.Label(scrollable_content, text="— LARIK (ARRAY) —", bg=self.colors["sidebar_bg"], fg="#475569", font=("Segoe UI", 8, "bold"), anchor="w")
        lbl_arr.pack(fill=tk.X, padx=10, pady=(4, 2))

        self._add_menu_btn(scrollable_content, "ARRAY - LIHAT PESANAN", lambda: self.set_mode("ARRAY_LIHAT"))
        self._add_menu_btn(scrollable_content, "ARRAY - TAMBAH REGULER", lambda: self.set_mode("ARRAY_TAMBAH_REG"))
        self._add_menu_btn(scrollable_content, "ARRAY - TAMBAH PRIORITAS", lambda: self.set_mode("ARRAY_TAMBAH_PRIO"))
        self._add_menu_btn(scrollable_content, "ARRAY - TAMBAH VIP", lambda: self.set_mode("ARRAY_TAMBAH_VIP"))
        self._add_menu_btn(scrollable_content, "ARRAY - HAPUS PESANAN", lambda: self.set_mode("ARRAY_HAPUS"))

        # Sub-header Linked List
        lbl_ll = tk.Label(scrollable_content, text="— RANTAI (LINKED LIST) —", bg=self.colors["sidebar_bg"], fg="#475569", font=("Segoe UI", 8, "bold"), anchor="w")
        lbl_ll.pack(fill=tk.X, padx=10, pady=(8, 2))

        self._add_menu_btn(scrollable_content, "LINKEDLIST - LIHAT PESANAN", lambda: self.set_mode("LL_LIHAT"))
        self._add_menu_btn(scrollable_content, "LINKEDLIST - TAMBAH REGULER", lambda: self.set_mode("LL_TAMBAH_REG"))
        self._add_menu_btn(scrollable_content, "LINKEDLIST - TAMBAH PRIORITAS", lambda: self.set_mode("LL_TAMBAH_PRIO"))
        self._add_menu_btn(scrollable_content, "LINKEDLIST - TAMBAH VIP", lambda: self.set_mode("LL_TAMBAH_VIP"))
        self._add_menu_btn(scrollable_content, "LINKEDLIST - HAPUS PESANAN", lambda: self.set_mode("LL_HAPUS"))

        # Tombol Uji Tanding Performa (Duel Array vs LinkedList)
        btn_duel = tk.Button(
            scrollable_content, text="⚡ UJI TANDING ARRAY vs LL", bg="#f59e0b", fg="white",
            font=("Segoe UI", 9, "bold"), relief=tk.FLAT, pady=4, cursor="hand2",
            command=self.action_benchmark_duel
        )
        btn_duel.pack(fill=tk.X, padx=10, pady=(10, 10))

        # SECTION: M2 - ANTREAN DAN UNDO
        self._add_section_header(scrollable_content, "M2 - ANTREAN DAN UNDO")
        self._add_menu_btn(scrollable_content, "M2 - STATUS ANTREAN FIFO", lambda: self.set_mode("M2_STATUS"))
        self._add_menu_btn(scrollable_content, "M2 - ENQUEUE (Masuk Dapur)", lambda: self.set_mode("M2_ENQUEUE"))
        self._add_menu_btn(scrollable_content, "M2 - LAYANI BERIKUTNYA", self.action_m2_dequeue)
        self._add_menu_btn(scrollable_content, "M2 - UNDO AKSI TERAKHIR", self.action_m2_undo)

        self._add_section_header(scrollable_content, "M3 - LAPORAN & SORTING")
        self._add_menu_btn(scrollable_content, "M3 - LAPORAN TERURUT (Sort)", lambda: self.set_mode("M3_SORT"))
        self._add_menu_btn(scrollable_content, "M3 - CARI DI LAPORAN (Binary Search)", lambda: self.set_mode("M3_SEARCH"))
        btn_m3_duel = tk.Button(
            scrollable_content, text="⚡ DUEL SORTING (M3)", bg="#8b5cf6", fg="white",
            font=("Segoe UI", 9, "bold"), relief=tk.FLAT, pady=4, cursor="hand2",
            command=self.action_m3_duel_sort
        )
        btn_m3_duel.pack(fill=tk.X, padx=10, pady=(4, 6))

        self._add_section_header(scrollable_content, "M4 - PENCARIAN & HASH (Segera)")
        self._add_placeholder_btn(scrollable_content, "Bangun Indeks Hash")
        self._add_placeholder_btn(scrollable_content, "Cari Pesanan (OID)")

        self._add_section_header(scrollable_content, "M5 - KATALOG & HEAP (Segera)")
        self._add_placeholder_btn(scrollable_content, "Menu Rentang Harga (BST)")
        self._add_placeholder_btn(scrollable_content, "Dispatch MinHeap")

        self._add_section_header(scrollable_content, "M6 - PETA & RUTE (Segera)")
        self._add_placeholder_btn(scrollable_content, "Navigasi Dijkstra / BFS")

    def _add_section_header(self, parent, text):
        hdr = tk.Label(parent, text=text, bg="#e2e8f0", fg="#0f172a", font=("Segoe UI", 9, "bold"), anchor="w", padx=8, pady=3)
        hdr.pack(fill=tk.X, padx=6, pady=(8, 4))

    def _add_menu_btn(self, parent, text, command):
        btn = tk.Button(
            parent, text=text, bg="#f8fafc", fg="#334155", font=("Segoe UI", 8),
            relief=tk.RIDGE, bd=1, anchor="w", padx=8, pady=3, cursor="hand2",
            activebackground="#e2e8f0", command=command
        )
        btn.pack(fill=tk.X, padx=10, pady=1)

    def _add_placeholder_btn(self, parent, text):
        btn = tk.Button(
            parent, text=text, bg="#f1f5f9", fg="#94a3b8", font=("Segoe UI", 8),
            relief=tk.FLAT, anchor="w", padx=8, pady=2, state=tk.DISABLED
        )
        btn.pack(fill=tk.X, padx=10, pady=1)

    def _build_work_area(self, parent):
        work_frame = tk.Frame(parent, bg=self.colors["bg_main"], padx=16, pady=12)
        parent.add(work_frame, weight=3)

        # Header Info Aksi
        self.lbl_action_title = tk.Label(
            work_frame, text="Operasi Terpilih", bg=self.colors["bg_main"],
            fg="#0f172a", font=("Segoe UI", 13, "bold"), anchor="w"
        )
        self.lbl_action_title.pack(fill=tk.X, pady=(0, 2))

        self.lbl_action_desc = tk.Label(
            work_frame, text="Pilih operasi dari menu di sebelah kiri.", bg=self.colors["bg_main"],
            fg="#64748b", font=("Segoe UI", 9), anchor="w"
        )
        self.lbl_action_desc.pack(fill=tk.X, pady=(0, 12))

        # Kotak Form Parameter
        self.form_frame = tk.LabelFrame(
            work_frame, text=" Form Parameter ", bg="white", fg="#1e293b",
            font=("Segoe UI", 9, "bold"), padx=12, pady=10
        )
        self.form_frame.pack(fill=tk.X, pady=(0, 12))

        # Konten dinamis di dalam form_frame
        self.form_fields_container = tk.Frame(self.form_frame, bg="white")
        self.form_fields_container.pack(fill=tk.X)

        # Tombol Eksekusi Aksi
        self.btn_execute = tk.Button(
            self.form_frame, text="JALANKAN OPERASI", bg=self.colors["accent_blue"],
            fg="white", font=("Segoe UI", 9, "bold"), relief=tk.FLAT, padx=16, pady=5,
            cursor="hand2", command=self.execute_current_action
        )
        self.btn_execute.pack(anchor="e", pady=(8, 0))

        # Kotak Tampilan Hasil Eksekusi
        result_label_frame = tk.LabelFrame(
            work_frame, text=" Detail Hasil Operasi ", bg="white", fg="#1e293b",
            font=("Segoe UI", 9, "bold"), padx=12, pady=10
        )
        result_label_frame.pack(fill=tk.BOTH, expand=True)

        self.txt_result = ScrolledText(
            result_label_frame, bg="#f8fafc", fg="#0f172a", font=("Consolas", 10),
            relief=tk.SOLID, bd=1, height=10
        )
        self.txt_result.pack(fill=tk.BOTH, expand=True)

    def _build_command_panel(self, parent):
        cmd_frame = tk.Frame(parent, bg=self.colors["terminal_bg"], padx=10, pady=6)
        parent.add(cmd_frame, weight=2)

        header_bar = tk.Frame(cmd_frame, bg=self.colors["terminal_bg"])
        header_bar.pack(fill=tk.X, pady=(0, 4))

        lbl_cmd = tk.Label(
            header_bar, text="COMMAND & BENCHMARK LOG", bg=self.colors["terminal_bg"],
            fg=self.colors["terminal_fg"], font=("Consolas", 9, "bold")
        )
        lbl_cmd.pack(side=tk.LEFT)

        btn_clear_log = tk.Button(
            header_bar, text="Clear Log", bg="#334155", fg="white",
            font=("Segoe UI", 8), relief=tk.FLAT, padx=8, pady=1, cursor="hand2",
            command=self.clear_command_log
        )
        btn_clear_log.pack(side=tk.RIGHT)

        self.txt_command_log = ScrolledText(
            cmd_frame, bg=self.colors["terminal_bg"], fg="#e2e8f0",
            font=("Consolas", 9), relief=tk.FLAT, height=6
        )
        self.txt_command_log.pack(fill=tk.BOTH, expand=True)
        self.log_command("Sistem 2EZ4U Food Delivery siap. Silakan klik 'Load CSV' untuk memulai.")

    def log_command(self, text, duration_ms=None):
        timestamp = time.strftime("%H:%M:%S")
        if duration_ms is not None:
            formatted = f"[{timestamp}] {text} -> {duration_ms:.4f} ms\n"
        else:
            formatted = f"[{timestamp}] {text}\n"
        self.txt_command_log.insert(tk.END, formatted)
        self.txt_command_log.see(tk.END)

    def clear_command_log(self):
        self.txt_command_log.delete("1.0", tk.END)

    # -------------------------------------------------------------
    # LOGIKA STATE FORM PARAMETER (Sesuai aksi menu yang dipilih)
    # -------------------------------------------------------------
    def set_mode(self, mode):
        self.current_mode = mode

        # Bersihkan widget form sebelumnya
        for widget in self.form_fields_container.winfo_children():
            widget.destroy()

        if "LIHAT" in mode:
            struct_name = "Array" if "ARRAY" in mode else "Linked List"
            self.lbl_action_title.config(text=f"{struct_name} - LIHAT PESANAN")
            self.lbl_action_desc.config(
                text="Melihat detail pesanan pada indeks ke-i. (Array: O(1) direct index | Linked List: O(n) traversal rantai)."
            )
            self.btn_execute.config(text="CARI PESANAN", bg="#2563eb")

            tk.Label(self.form_fields_container, text="Nomor Indeks (0 s.d. size - 1):", bg="white", font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w", pady=4)
            self.entry_index = ttk.Entry(self.form_fields_container, width=20)
            self.entry_index.insert(0, "0")
            self.entry_index.grid(row=0, column=1, sticky="w", padx=8, pady=4)

        elif "HAPUS" in mode:
            struct_name = "Array" if "ARRAY" in mode else "Linked List"
            self.lbl_action_title.config(text=f"{struct_name} - HAPUS PESANAN")
            self.lbl_action_desc.config(
                text="Menghapus pesanan pada posisi ke-i. (Array: O(n) geser elemen | Linked List: O(n) traversal pointer)."
            )
            self.btn_execute.config(text="HAPUS PESANAN", bg=self.colors["accent_red"])

            tk.Label(self.form_fields_container, text="Indeks yang Ingin Dihapus:", bg="white", font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w", pady=4)
            self.entry_index = ttk.Entry(self.form_fields_container, width=20)
            self.entry_index.insert(0, "0")
            self.entry_index.grid(row=0, column=1, sticky="w", padx=8, pady=4)

        elif "TAMBAH" in mode:
            struct_name = "Array" if "ARRAY" in mode else "Linked List"
            if "REG" in mode:
                jenis = "REGULER (Prioritas 3)"
                desc = "Masuk di barisan PALING BELAKANG. (Array: O(1) amortized | Linked List: O(1) via tail pointer)."
                prio_val = "3"
            elif "PRIO" in mode:
                jenis = "PRIORITAS (Prioritas 2)"
                desc = "Menyerobot ke TENGAH barisan (size // 2). (Array: O(n) geser separuh | Linked List: O(n) traversal ke tengah)."
                prio_val = "2"
            else:
                jenis = "VIP (Prioritas 1)"
                desc = "Langsung masuk di PALING DEPAN (indeks 0). (Array: O(n) geser seluruh memori | Linked List: O(1) ubah head pointer)."
                prio_val = "1"

            self.lbl_action_title.config(text=f"{struct_name} - TAMBAH PESANAN {jenis}")
            self.lbl_action_desc.config(text=desc)
            self.btn_execute.config(text=f"TAMBAH {jenis.split()[0]}", bg=self.colors["accent_green"])

            # Form fields
            labels = ["Nama Pelanggan:", "Restoran:", "Menu:", "Harga (Rp):"]
            defaults = ["Budi Santoso", "kafe-teknik", "Kopi Susu Gula Aren", "18000"]
            self.entries_tambah = []

            for i, (label_text, default_val) in enumerate(zip(labels, defaults)):
                tk.Label(self.form_fields_container, text=label_text, bg="white", font=("Segoe UI", 9)).grid(row=i, column=0, sticky="w", pady=2)
                ent = ttk.Entry(self.form_fields_container, width=32)
                ent.insert(0, default_val)
                ent.grid(row=i, column=1, sticky="w", padx=8, pady=2)
                self.entries_tambah.append(ent)

            self.current_prio_val = int(prio_val)

        elif mode == "M2_STATUS":
            self.lbl_action_title.config(text="M2 - STATUS ANTREAN FIFO (Circular Queue)")
            self.lbl_action_desc.config(
                text="Melihat kondisi antrean dapur terkini (Front, Rear, Kapasitas) dan riwayat Stack Undo."
            )
            self.btn_execute.config(text="🔄 REFRESH STATUS ANTREAN", bg=self.colors["accent_blue"])
            lbl_info = tk.Label(
                self.form_fields_container,
                text="Klik tombol di samping untuk menyegarkan visualisasi antrean melingkar & tumpukan undo.",
                bg="white", font=("Segoe UI", 9, "italic"), fg="#475569"
            )
            lbl_info.pack(anchor="w", pady=4)
            self._render_m2_queue_status()

        elif mode == "M2_ENQUEUE":
            self.lbl_action_title.config(text="M2 - TAMBAH KE ANTREAN (Enqueue FIFO)")
            self.lbl_action_desc.config(
                text="Memasukkan pesanan ke antrean dapur. Menambah di belakang antrean dalam O(1)."
            )
            self.btn_execute.config(text="📥 ENQUEUE KE DAPUR", bg=self.colors["accent_green"])

            tk.Label(self.form_fields_container, text="Pilih dari Data Pesanan (Indeks):", bg="white", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", pady=2)
            self.entry_m2_idx = ttk.Entry(self.form_fields_container, width=15)
            self.entry_m2_idx.insert(0, str(len(self.antrean_mgr.queue)))
            self.entry_m2_idx.grid(row=0, column=1, sticky="w", padx=8, pady=2)

            tk.Label(self.form_fields_container, text="— ATAU Input Pesanan Baru —", bg="white", font=("Segoe UI", 8, "italic"), fg="#64748b").grid(row=1, column=0, columnspan=2, sticky="w", pady=(6, 2))

            labels = ["Nama Pelanggan:", "Restoran:", "Menu:", "Harga (Rp):"]
            defaults = ["Bambang", "bakso-pak-yon", "Bakso Campur Super", "25000"]
            self.entries_m2 = []

            for i, (label_text, default_val) in enumerate(zip(labels, defaults)):
                tk.Label(self.form_fields_container, text=label_text, bg="white", font=("Segoe UI", 9)).grid(row=i + 2, column=0, sticky="w", pady=2)
                ent = ttk.Entry(self.form_fields_container, width=32)
                ent.insert(0, default_val)
                ent.grid(row=i + 2, column=1, sticky="w", padx=8, pady=2)
                self.entries_m2.append(ent)

        elif mode == "M3_SORT":
            self.lbl_action_title.config(text="M3 - LAPORAN TERURUT (Insertion / Selection / Bubble Sort)")
            self.lbl_action_desc.config(
                text="Membuat laporan harian terurut berdasarkan Harga atau Waktu transaksi (O(n²) in-place)."
            )
            self.btn_execute.config(text="📊 PROSES PENGURUTAN LAPORAN", bg="#7c3aed")

            tk.Label(self.form_fields_container, text="Jumlah Data (Limit):", bg="white", font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w", pady=2)
            self.combo_m3_limit = ttk.Combobox(self.form_fields_container, values=["100", "300", "500", "1000", "2000", "5000"], width=20, state="readonly")
            self.combo_m3_limit.set("500")
            self.combo_m3_limit.grid(row=0, column=1, sticky="w", padx=8, pady=2)

            tk.Label(self.form_fields_container, text="Urutkan Berdasarkan:", bg="white", font=("Segoe UI", 9)).grid(row=1, column=0, sticky="w", pady=2)
            self.combo_m3_key = ttk.Combobox(self.form_fields_container, values=["Harga (Termurah -> Termahal)", "Waktu Masuk (Pagi -> Malam)"], width=20, state="readonly")
            self.combo_m3_key.set("Harga (Termurah -> Termahal)")
            self.combo_m3_key.grid(row=1, column=1, sticky="w", padx=8, pady=2)

            tk.Label(self.form_fields_container, text="Algoritma Sorting:", bg="white", font=("Segoe UI", 9)).grid(row=2, column=0, sticky="w", pady=2)
            self.combo_m3_algo = ttk.Combobox(self.form_fields_container, values=["Insertion Sort (Utama)", "Selection Sort", "Bubble Sort"], width=20, state="readonly")
            self.combo_m3_algo.set("Insertion Sort (Utama)")
            self.combo_m3_algo.grid(row=2, column=1, sticky="w", padx=8, pady=2)

            tk.Label(self.form_fields_container, text="Filter Status Pesanan:", bg="white", font=("Segoe UI", 9)).grid(row=3, column=0, sticky="w", pady=2)
            self.combo_m3_status = ttk.Combobox(self.form_fields_container, values=["Semua Status", "DONE", "CANCEL", "ANTRE"], width=20, state="readonly")
            self.combo_m3_status.set("Semua Status")
            self.combo_m3_status.grid(row=3, column=1, sticky="w", padx=8, pady=2)

        elif mode == "M3_SEARCH":
            self.lbl_action_title.config(text="M3 - CARI DI LAPORAN (Binary Search O(log n))")
            self.lbl_action_desc.config(
                text="Mencari pesanan pada laporan yang sudah terurut. Membandingkan efisiensi Binary Search vs Linear Search."
            )
            self.btn_execute.config(text="🔍 CARI DENGAN BINARY SEARCH", bg="#0284c7")

            tk.Label(self.form_fields_container, text="Nilai Target yang Dicari:", bg="white", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", pady=2)
            self.entry_m3_target = ttk.Entry(self.form_fields_container, width=22)
            self.entry_m3_target.insert(0, "15000")
            self.entry_m3_target.grid(row=0, column=1, sticky="w", padx=8, pady=2)

            status_laporan = f"Laporan saat ini: {len(self.laporan_mgr.data_laporan):,} data (Kunci: {self.laporan_mgr.kunci_terakhir or 'Belum ada'})"
            lbl_info = tk.Label(
                self.form_fields_container,
                text=status_laporan + "\n*Jika laporan belum dibuat, sistem otomatis mengurutkan 500 data terlebih dahulu.",
                bg="white", font=("Segoe UI", 8, "italic"), fg="#475569"
            )
            lbl_info.grid(row=1, column=0, columnspan=2, sticky="w", pady=(4, 2))

    # -------------------------------------------------------------
    # EKSEKUSI AKSI & BENCHMARKING
    # -------------------------------------------------------------
    def action_load_data(self):
        if not os.path.exists(self.csv_path):
            messagebox.showerror("File Tidak Ditemukan", f"File CSV tidak ditemukan di:\n{self.csv_path}")
            return

        self.lbl_data_status.config(text="Memuat 200.000 data CSV...", fg="#d97706")
        self.root.update()

        try:
            self.array_pesanan, self.linklist_pesanan, durasi, total = muat_pesanan_csv(self.csv_path)
            self.data_loaded = True
            self.total_loaded = total

            durasi_ms = durasi * 1000
            self.lbl_data_status.config(
                text=f"Aktif: {total:,} data dimuat ({durasi:.2f}s)",
                fg="#16a34a"
            )
            self.log_command(f"LOAD CSV ({total:,} baris dimuat ke Array & LinkList)", durasi_ms)

            # Inisialisasi antrean dapur M2 dengan 10 pesanan pertama dari CSV jika masih kosong
            if self.antrean_mgr.queue.is_empty():
                for k in range(min(10, len(self.array_pesanan))):
                    p_seed = self.array_pesanan.get(k)
                    p_copy = Pesanan(
                        oid=p_seed.oid, pelanggan=p_seed.pelanggan, resto=p_seed.resto,
                        menu=p_seed.menu, harga=p_seed.harga, prioritas=p_seed.prioritas,
                        t_masuk_detik=p_seed.t_masuk_detik, t_selesai_detik=None, status="ANTRE"
                    )
                    self.antrean_mgr.queue.enqueue(p_copy)

            # Tampilkan info pesanan awal & akhir di result text
            p_first = self.array_pesanan.get(0)
            p_last = self.array_pesanan.get(len(self.array_pesanan) - 1)

            res = (
                f"=== DATA BERHASIL DIMUAT ===\n"
                f"Total Data  : {total:,} pesanan\n"
                f"Waktu Muat  : {durasi:.3f} detik ({durasi_ms:.2f} ms)\n\n"
                f"Pesanan Pertama (Indeks 0):\n  {p_first.ringkasan()}\n\n"
                f"Pesanan Terakhir (Indeks {total - 1:,}):\n  {p_last.ringkasan()}\n"
            )
            self.txt_result.delete("1.0", tk.END)
            self.txt_result.insert(tk.END, res)

        except Exception as e:
            self.lbl_data_status.config(text="Gagal memuat data!", fg="#dc2626")
            messagebox.showerror("Error", f"Terjadi kesalahan saat membaca CSV:\n{e}")

    def execute_current_action(self):
        if not self.data_loaded or len(self.array_pesanan) == 0:
            messagebox.showwarning("Peringatan", "Data pesanan masih kosong! Klik 'Load CSV' terlebih dahulu.")
            return

        mode = self.current_mode

        try:
            # 1. LIHAT PESANAN
            if "LIHAT" in mode:
                idx = int(self.entry_index.get())
                is_arr = "ARRAY" in mode
                target_ds = self.array_pesanan if is_arr else self.linklist_pesanan
                name = "Array" if is_arr else "LinkList"

                t0 = time.perf_counter()
                pesanan = target_ds.get(idx)
                durasi_ms = (time.perf_counter() - t0) * 1000

                self.log_command(f"M1 - {name} - Lihat pesanan indeks {idx}", durasi_ms)

                res = (
                    f"=== HASIL PENCARIAN PESANAN ({name}) ===\n"
                    f"Waktu Eksekusi : {durasi_ms:.4f} ms\n"
                    f"Posisi Indeks  : {idx:,} dari total {len(target_ds):,} pesanan\n"
                    f"--------------------------------------------------\n"
                    f"OID            : {pesanan.oid}\n"
                    f"Pelanggan      : {pesanan.pelanggan}\n"
                    f"Restoran       : {pesanan.resto}\n"
                    f"Menu           : {pesanan.menu}\n"
                    f"Harga          : Rp{pesanan.harga:,}\n"
                    f"Tingkat Prioritas : {pesanan.prioritas} ({'VIP' if pesanan.prioritas == 1 else 'Prioritas' if pesanan.prioritas == 2 else 'Reguler'})\n"
                    f"Waktu Masuk    : {pesanan.t_masuk_detik} detik\n"
                    f"Waktu Selesai  : {pesanan.t_selesai_detik if pesanan.t_selesai_detik is not None else '-'}\n"
                    f"Status         : {pesanan.status}\n"
                )
                self.txt_result.delete("1.0", tk.END)
                self.txt_result.insert(tk.END, res)

            # 2. HAPUS PESANAN
            elif "HAPUS" in mode:
                idx = int(self.entry_index.get())
                is_arr = "ARRAY" in mode
                target_ds = self.array_pesanan if is_arr else self.linklist_pesanan
                name = "Array" if is_arr else "LinkList"

                t0 = time.perf_counter()
                deleted_item = target_ds.delete(idx)
                durasi_ms = (time.perf_counter() - t0) * 1000

                self.log_command(f"M1 - {name} - Hapus pesanan indeks {idx} ({deleted_item.oid})", durasi_ms)

                res = (
                    f"=== PESANAN BERHASIL DIHAPUS ({name}) ===\n"
                    f"Waktu Eksekusi : {durasi_ms:.4f} ms\n"
                    f"Indeks Dihapus : {idx}\n"
                    f"Sisa Data      : {len(target_ds):,} pesanan\n"
                    f"--------------------------------------------------\n"
                    f"Data Dihapus   : {deleted_item.ringkasan()}\n"
                )
                self.txt_result.delete("1.0", tk.END)
                self.txt_result.insert(tk.END, res)

            # 3. TAMBAH PESANAN (REGULER, PRIORITAS, VIP)
            elif "TAMBAH" in mode:
                pelanggan = self.entries_tambah[0].get().strip() or "Anonim"
                resto = self.entries_tambah[1].get().strip() or "Resto"
                menu = self.entries_tambah[2].get().strip() or "Menu"
                harga = int(self.entries_tambah[3].get().strip() or 0)
                prio = self.current_prio_val

                is_arr = "ARRAY" in mode
                name = "Array" if is_arr else "LinkList"
                target_ds = self.array_pesanan if is_arr else self.linklist_pesanan

                new_oid = f"O-NEW-{len(target_ds) + 1}"
                new_pesanan = Pesanan(
                    oid=new_oid, pelanggan=pelanggan, resto=resto, menu=menu,
                    harga=harga, prioritas=prio, t_masuk_detik=int(time.time()) % 86400,
                    t_selesai_detik=None, status="ANTRE"
                )

                t0 = time.perf_counter()
                posisi_teks = ""

                if "REG" in mode:
                    # REGULER: paling belakang
                    target_ds.append(new_pesanan)
                    posisi_teks = f"paling belakang (indeks {len(target_ds) - 1:,})"
                elif "VIP" in mode:
                    # VIP: paling depan (indeks 0)
                    if is_arr:
                        self.array_pesanan.insert(0, new_pesanan)
                    else:
                        self.linklist_pesanan.insert_front(new_pesanan)
                    posisi_teks = "paling depan (indeks 0)"
                else:
                    # PRIORITAS: tengah (size // 2)
                    mid_idx = len(target_ds) // 2
                    target_ds.insert(mid_idx, new_pesanan)
                    posisi_teks = f"tengah barisan (indeks {mid_idx:,})"

                durasi_ms = (time.perf_counter() - t0) * 1000
                self.log_command(f"M1 - {name} - Tambah pesanan {new_oid} ({posisi_teks})", durasi_ms)

                res = (
                    f"=== PESANAN BERHASIL DITAMBAHKAN ({name}) ===\n"
                    f"Waktu Eksekusi : {durasi_ms:.4f} ms\n"
                    f"Disisipkan di  : {posisi_teks}\n"
                    f"Total Pesanan  : {len(target_ds):,}\n"
                    f"--------------------------------------------------\n"
                    f"Detail Pesanan : {new_pesanan.ringkasan()}\n"
                )
                self.txt_result.delete("1.0", tk.END)
                self.txt_result.insert(tk.END, res)

            # 4. M2 - STATUS ANTREAN FIFO
            elif mode == "M2_STATUS":
                self._render_m2_queue_status()

            # 5. M2 - ENQUEUE (Masuk Dapur)
            elif mode == "M2_ENQUEUE":
                idx_str = self.entry_m2_idx.get().strip()
                use_existing = False
                pesanan_to_add = None

                if idx_str.isdigit() and self.data_loaded:
                    idx = int(idx_str)
                    if 0 <= idx < len(self.array_pesanan):
                        p_orig = self.array_pesanan.get(idx)
                        pesanan_to_add = Pesanan(
                            oid=p_orig.oid, pelanggan=p_orig.pelanggan, resto=p_orig.resto,
                            menu=p_orig.menu, harga=p_orig.harga, prioritas=p_orig.prioritas,
                            t_masuk_detik=p_orig.t_masuk_detik, t_selesai_detik=None, status="ANTRE"
                        )
                        use_existing = True

                if not use_existing:
                    pelanggan = self.entries_m2[0].get().strip() or "Anonim"
                    resto = self.entries_m2[1].get().strip() or "Resto"
                    menu = self.entries_m2[2].get().strip() or "Menu"
                    harga = int(self.entries_m2[3].get().strip() or 0)
                    new_oid = f"O-Q-{len(self.antrean_mgr.queue) + 1}"
                    pesanan_to_add = Pesanan(
                        oid=new_oid, pelanggan=pelanggan, resto=resto, menu=menu,
                        harga=harga, prioritas=3, t_masuk_detik=int(time.time()) % 86400,
                        t_selesai_detik=None, status="ANTRE"
                    )

                t0 = time.perf_counter()
                self.antrean_mgr.tambah_antrean(pesanan_to_add)
                durasi_ms = (time.perf_counter() - t0) * 1000

                self.log_command(f"M2 - Enqueue Antrean Dapur: {pesanan_to_add.oid}", durasi_ms)
                self._render_m2_queue_status(pesan_tambahan=f"Pesanan {pesanan_to_add.oid} ({pesanan_to_add.pelanggan}) berhasil dimasukkan ke antrean dapur ({durasi_ms:.4f} ms).")

            # 6. M3 - LAPORAN TERURUT (SORT)
            elif mode == "M3_SORT":
                limit = int(self.combo_m3_limit.get())
                kunci_raw = self.combo_m3_key.get()
                sort_by = "waktu" if "Waktu" in kunci_raw else "harga"

                algo_raw = self.combo_m3_algo.get()
                if "Selection" in algo_raw:
                    algoritma = "selection"
                    nama_algo = "Selection Sort"
                elif "Bubble" in algo_raw:
                    algoritma = "bubble"
                    nama_algo = "Bubble Sort"
                else:
                    algoritma = "insertion"
                    nama_algo = "Insertion Sort"

                st_raw = self.combo_m3_status.get()
                st_filter = None if "Semua" in st_raw else st_raw

                data, durasi_ms = self.laporan_mgr.buat_laporan(
                    self.array_pesanan, limit=limit, sort_by=sort_by,
                    algoritma=algoritma, status_filter=st_filter
                )

                self.log_command(f"M3 - {nama_algo} ({len(data)} pesanan by {sort_by})", durasi_ms)
                self._render_m3_report(nama_algo, sort_by, durasi_ms)

            # 7. M3 - CARI DI LAPORAN (BINARY SEARCH)
            elif mode == "M3_SEARCH":
                if not self.laporan_mgr.data_laporan:
                    self.laporan_mgr.buat_laporan(self.array_pesanan, limit=500, sort_by="harga", algoritma="insertion")

                target_val = int(self.entry_m3_target.get().strip())
                res_search = self.laporan_mgr.cari_laporan(target_val)
                self.log_command(
                    f"M3 - Binary Search ({self.laporan_mgr.kunci_terakhir} = {target_val:,})",
                    res_search["durasi_bs_ms"]
                )
                self._render_m3_search_result(target_val, res_search)

        except IndexError as e:
            messagebox.showerror("Indeks Tidak Valid", str(e))
        except ValueError:
            messagebox.showerror("Format Salah", "Pastikan input angka berupa integer yang valid!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

    def action_benchmark_duel(self):
        """
        Menjalankan pengujian langsung adu performa Array vs Linked List
        pada 3 jenis penyisipan + get + delete sesuai tabel halaman 6 PDF.
        """
        if not self.data_loaded or len(self.array_pesanan) < 1000:
            messagebox.showwarning("Peringatan", "Muat minimal sebagian data CSV terlebih dahulu!")
            return

        self.log_command("=== MEMULAI UJI TANDING PERFORMA (ARRAY VS LINKED LIST) ===")
        n = len(self.array_pesanan)

        # 1. GET TENGAH
        mid = n // 2
        t0 = time.perf_counter()
        _ = self.array_pesanan.get(mid)
        t_get_arr = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        _ = self.linklist_pesanan.get(mid)
        t_get_ll = (time.perf_counter() - t0) * 1000

        # 2. TAMBAH REGULER (Belakang)
        p_reg = Pesanan("O-TEST-REG", "Duel Reg", "Resto", "Menu", 15000, 3, 0, None, "ANTRE")
        t0 = time.perf_counter()
        self.array_pesanan.append(p_reg)
        t_reg_arr = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        self.linklist_pesanan.append(p_reg)
        t_reg_ll = (time.perf_counter() - t0) * 1000

        # 3. TAMBAH PRIORITAS (Tengah)
        p_prio = Pesanan("O-TEST-PRIO", "Duel Prio", "Resto", "Menu", 20000, 2, 0, None, "ANTRE")
        mid = len(self.array_pesanan) // 2
        t0 = time.perf_counter()
        self.array_pesanan.insert(mid, p_prio)
        t_prio_arr = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        self.linklist_pesanan.insert(mid, p_prio)
        t_prio_ll = (time.perf_counter() - t0) * 1000

        # 4. TAMBAH VIP (Depan / Indeks 0)
        p_vip = Pesanan("O-TEST-VIP", "Duel VIP", "Resto", "Menu", 50000, 1, 0, None, "ANTRE")
        t0 = time.perf_counter()
        self.array_pesanan.insert(0, p_vip)
        t_vip_arr = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        self.linklist_pesanan.insert_front(p_vip)
        t_vip_ll = (time.perf_counter() - t0) * 1000

        # Log hasil ke terminal
        self.log_command(f"GET (Indeks {mid:,}) -> Array: {t_get_arr:.4f} ms | LL: {t_get_ll:.4f} ms")
        self.log_command(f"TAMBAH REGULER -> Array: {t_reg_arr:.4f} ms | LL: {t_reg_ll:.4f} ms")
        self.log_command(f"TAMBAH PRIORITAS -> Array: {t_prio_arr:.4f} ms | LL: {t_prio_ll:.4f} ms")
        self.log_command(f"TAMBAH VIP -> Array: {t_vip_arr:.4f} ms | LL: {t_vip_ll:.4f} ms")

        # Tampilkan tabel perbandingan di Result
        w1, w2, w3, w4 = 20, 14, 14, 20
        sep = "+" + "-" * (w1 + 2) + "+" + "-" * (w2 + 2) + "+" + "-" * (w3 + 2) + "+" + "-" * (w4 + 2) + "+"
        total_len = len(sep)
        d_sep = "=" * total_len

        def row(c1, c2, c3, c4):
            return f"| {c1:<{w1}} | {c2:>{w2}} | {c3:>{w3}} | {c4:<{w4}} |"

        title = "HASIL UJI TANDING PERFORMA: ARRAY vs LINKED LIST"
        subtitle = f"(Ukuran Data: {n:,} baris pesanan)"

        report_lines = [
            d_sep,
            "|" + title.center(total_len - 2) + "|",
            "|" + subtitle.center(total_len - 2) + "|",
            sep,
            row("Operasi", "Array", "Linked List", "Pemenang"),
            sep,
            row("Lihat (Indeks n/2)", f"{t_get_arr:.4f} ms", f"{t_get_ll:.4f} ms", "Array (O(1))"),
            row("Tambah REGULER", f"{t_reg_arr:.4f} ms", f"{t_reg_ll:.4f} ms", "Imbang (O(1))"),
            row("Tambah PRIORITAS", f"{t_prio_arr:.4f} ms", f"{t_prio_ll:.4f} ms", "Relatif Seimbang"),
            row("Tambah VIP", f"{t_vip_arr:.4f} ms", f"{t_vip_ll:.4f} ms", "Linked List (O(1))"),
            sep,
            d_sep,
            "",
            "Analisa Hasil:",
            "1. Lihat Pesanan: Array O(1) direct indexing jauh lebih cepat dari LL O(n) traversal.",
            "2. Tambah REGULER: Keduanya O(1). Array amortized O(1), LL O(1) berkat pointer tail.",
            "3. Tambah PRIORITAS: Array menggeser n/2 elemen, LL menelusuri n/2 simpul.",
            "4. Tambah VIP: Linked List O(1) telak mengalahkan Array O(n) yang harus menggeser",
            "   seluruh elemen memori ke kanan."
        ]
        report = "\n".join(report_lines)
        self.txt_result.delete("1.0", tk.END)
        self.txt_result.insert(tk.END, report)

    # -------------------------------------------------------------
    # AKSI MILESTONE 2: ANTREAN (CIRCULAR QUEUE) & FITUR UNDO (STACK)
    # -------------------------------------------------------------
    def action_m2_dequeue(self):
        if self.antrean_mgr.queue.is_empty():
            messagebox.showinfo("Antrean Kosong", "Tidak ada pesanan di antrean dapur untuk dilayani.")
            return

        t0 = time.perf_counter()
        pesanan = self.antrean_mgr.layani_berikutnya()
        durasi_ms = (time.perf_counter() - t0) * 1000

        self.log_command(f"M2 - Layani Berikutnya (Dequeue): {pesanan.oid} -> DONE", durasi_ms)
        self._render_m2_queue_status(
            pesan_tambahan=f"PESANAN SELESAI DILAYANI:\n  {pesanan.ringkasan()} ({durasi_ms:.4f} ms)\n[Tips: Klik 'M2 - UNDO AKSI TERAKHIR' jika ingin membatalkan/mengembalikan ke antrean]"
        )

    def action_m2_undo(self):
        if self.antrean_mgr.undo_stack.is_empty():
            messagebox.showinfo("Undo Kosong", "Tidak ada riwayat aksi yang bisa di-undo.")
            return

        t0 = time.perf_counter()
        hasil = self.antrean_mgr.undo()
        durasi_ms = (time.perf_counter() - t0) * 1000

        if hasil is None:
            return

        tipe_undo, pesanan, aksi_asli = hasil
        if tipe_undo == "BATAL_LAYANI":
            msg = (
                f"UNDO BERHASIL (Batal Layani / Dequeue):\n"
                f"  Pesanan {pesanan.oid} dikembalikan ke URUTAN TERDEPAN antrean (Status: ANTRE) dalam {durasi_ms:.4f} ms."
            )
            self.log_command(f"M2 - UNDO: Batal Layani {pesanan.oid} (Kembali ke depan antrean)", durasi_ms)
        else:
            msg = (
                f"UNDO BERHASIL (Batal Enqueue):\n"
                f"  Pesanan {pesanan.oid} dicabut dari antrean dapur dalam {durasi_ms:.4f} ms."
            )
            self.log_command(f"M2 - UNDO: Batal Enqueue {pesanan.oid}", durasi_ms)

        self._render_m2_queue_status(pesan_tambahan=msg)

    def _render_m2_queue_status(self, pesan_tambahan=None):
        q = self.antrean_mgr.queue
        st = self.antrean_mgr.undo_stack
        orders = q.to_list()
        undo_list = st.to_list()

        w = 81
        sep = "+" + "-" * (w - 2) + "+"
        d_sep = "=" * w
        inner_w = w - 4

        def box_line(content):
            return f"| {content:<{inner_w}} |"

        title = "STATUS ANTREAN DAPUR (CIRCULAR QUEUE FIFO)"
        lines = [
            d_sep,
            "|" + title.center(w - 2) + "|",
            sep,
            box_line(f"Kapasitas Memori : {q.capacity} slot (Alokasi Array Primitif Berukuran Tetap)"),
            box_line(f"Jumlah Antrean   : {q.size} pesanan aktif yang sedang menunggu giliran"),
            box_line(f"Pointer FRONT    : Indeks {q.front} (Pesanan terdepan yang siap dimasak)"),
            box_line(f"Pointer REAR     : Indeks {q.rear} (Pesanan terakhir yang baru masuk)"),
            box_line(f"Tumpukan Undo    : {len(st)} aksi tersimpan di Stack (LIFO)"),
            sep,
            d_sep,
            ""
        ]

        if pesan_tambahan:
            lines.append(f">>> NOTIFIKASI AKSI TERAKHIR:\n{pesan_tambahan}\n")

        lines.append(f"--- DAFTAR ANTREAN SIAP DIMASAK (Urutan Terdepan -> Terbelakang) [Total: {len(orders)}] ---")
        if not orders:
            lines.append("  (Antrean dapur kosong. Klik 'M2 - ENQUEUE' untuk menambahkan pesanan!)")
        else:
            for idx, p in enumerate(orders):
                tag = " [SIAP DILAYANI (FRONT)]" if idx == 0 else ""
                lines.append(f"  {idx + 1:2d}. {p.ringkasan()}{tag}")

        lines.append("")
        lines.append(f"--- RIWAYAT TUMPUKAN UNDO (Stack LIFO - Teratas = Paling Baru) [Total: {len(undo_list)}] ---")
        if not undo_list:
            lines.append("  (Tumpukan undo kosong. Belum ada aksi yang dicatat.)")
        else:
            for idx, aksi in enumerate(undo_list[:8]):
                tag = " [TOP / AKSI TERAKHIR]" if idx == 0 else ""
                lines.append(f"  {idx + 1:2d}. [{aksi.waktu_str}] {aksi.tipe}: {aksi.keterangan}{tag}")
            if len(undo_list) > 8:
                lines.append(f"      ... dan {len(undo_list) - 8} aksi sebelumnya tersimpan di bawah tumpukan.")

        report = "\n".join(lines)
        self.txt_result.delete("1.0", tk.END)
        self.txt_result.insert(tk.END, report)

    def _render_m3_report(self, nama_algo, sort_by, durasi_ms):
        w = 81
        sep = "+" + "-" * (w - 2) + "+"
        d_sep = "=" * w
        inner_w = w - 4

        def box_line(content):
            return f"| {content:<{inner_w}} |"

        daftar = self.laporan_mgr.data_laporan
        n = len(daftar)
        title = f"LAPORAN HARIAN TERURUT ({nama_algo.upper()})"
        kunci_str = "Nominal Harga (Rp)" if sort_by == "harga" else "Waktu Transaksi (Detik Masuk)"

        lines = [
            d_sep,
            "|" + title.center(w - 2) + "|",
            sep,
            box_line(f"Algoritma Digunakan: {nama_algo} (Kompleksitas Asimtotik: O(n^2))"),
            box_line(f"Kunci Pengurutan   : {kunci_str}"),
            box_line(f"Jumlah Sampel Data : {n:,} pesanan transaksi"),
            box_line(f"Waktu Eksekusi     : {durasi_ms:.4f} ms"),
            sep,
            box_line("STATISTIK FINANSIAL LAPORAN:"),
            box_line(f"  * Total Omset    : Rp{self.laporan_mgr.total_omset:,}"),
            box_line(f"  * Rata-rata      : Rp{self.laporan_mgr.rata_rata_harga:,}"),
            box_line(f"  * Harga Minimum  : Rp{self.laporan_mgr.min_harga:,}"),
            box_line(f"  * Harga Maksimum : Rp{self.laporan_mgr.max_harga:,}"),
            sep,
            d_sep,
            ""
        ]

        lines.append("--- 10 DATA PERTAMA (TERENDAH / PALING AWAL) ---")
        for i in range(min(10, n)):
            lines.append(f"  {i + 1:2d}. {daftar[i].ringkasan()}")

        if n > 15:
            lines.append("")
            lines.append(f"      ... [terdapat {n - 15} data lainnya yang terurut sempurna] ...")
            lines.append("")
            lines.append("--- 5 DATA TERAKHIR (TERTINGGI / PALING AKHIR) ---")
            for i in range(max(10, n - 5), n):
                lines.append(f"  {i + 1:2d}. {daftar[i].ringkasan()}")

        report = "\n".join(lines)
        self.txt_result.delete("1.0", tk.END)
        self.txt_result.insert(tk.END, report)

    def _render_m3_search_result(self, target_val, res):
        w = 81
        sep = "+" + "-" * (w - 2) + "+"
        d_sep = "=" * w
        inner_w = w - 4

        def box_line(content):
            return f"| {content:<{inner_w}} |"

        kunci_nama = "Harga Rp" if self.laporan_mgr.kunci_terakhir == "harga" else "Waktu Masuk detik ke-"
        title = "HASIL PENCARIAN LAPORAN: BINARY SEARCH vs LINEAR SEARCH"
        found = res["found_idx"] != -1

        lines = [
            d_sep,
            "|" + title.center(w - 2) + "|",
            sep,
            box_line(f"Target Pencarian   : {kunci_nama}{target_val:,}"),
            box_line(f"Total Ruang Data   : {res['total_data']:,} data pesanan terurut"),
            box_line(f"Status Ditemukan   : {'YA (Ditemukan di indeks ' + str(res['found_idx']) + ')' if found else 'TIDAK DITEMUKAN'}"),
            box_line(f"Jumlah Match Cocok : {len(res['matches'])} pesanan"),
            sep,
            box_line("PERBANDINGAN EFISIENSI PENCARIAN:"),
            box_line(f"  1. BINARY SEARCH  : {res['steps_bs']} langkah komparasi (O(log n)) | {res['durasi_bs_ms']:.4f} ms"),
            box_line(f"  2. LINEAR SEARCH  : {res['steps_ls']} langkah komparasi (O(n))     | {res['durasi_ls_ms']:.4f} ms"),
            sep,
            d_sep,
            ""
        ]

        if found:
            lines.append("--- PESANAN COCOK (Menampilkan hingga 8 pesanan pertama) ---")
            for i, p in enumerate(res["matches"][:8]):
                lines.append(f"  {i + 1:2d}. {p.ringkasan()}")
            if len(res["matches"]) > 8:
                lines.append(f"      ... dan {len(res['matches']) - 8} pesanan lainnya dengan nilai yang sama.")
        else:
            lines.append(f"Tidak ada pesanan dengan {kunci_nama}{target_val:,} di laporan ini.")

        report = "\n".join(lines)
        self.txt_result.delete("1.0", tk.END)
        self.txt_result.insert(tk.END, report)

    def action_m3_duel_sort(self):
        if not self.data_loaded or len(self.array_pesanan) == 0:
            messagebox.showwarning("Peringatan", "Muat data CSV terlebih dahulu!")
            return

        limit = 500
        self.log_command(f"=== MEMULAI DUEL ALGORITMA SORTING M3 ({limit} DATA) ===")
        res = self.laporan_mgr.duel_sort(self.array_pesanan, limit=limit, sort_by="harga")

        w1, w2, w3, w4 = 19, 15, 13, 21
        sep = "+" + "-" * (w1 + 2) + "+" + "-" * (w2 + 2) + "+" + "-" * (w3 + 2) + "+" + "-" * (w4 + 2) + "+"
        total_len = len(sep)
        d_sep = "=" * total_len

        def row(c1, c2, c3, c4):
            return f"| {c1:<{w1}} | {c2:>{w2}} | {c3:<{w3}} | {c4:<{w4}} |"

        hdr_row = row("Algoritma Sorting", "Waktu Eksekusi", "Kompleksitas", "Efisiensi")

        lines = [
            d_sep,
            "|" + f"HASIL UJI TANDING ALGORITMA SORTING M3 ({limit} DATA)".center(total_len - 2) + "|",
            "|" + "Kunci Pengurutan: Nominal Harga (Rp) Ascending".center(total_len - 2) + "|",
            sep,
            hdr_row,
            sep,
            row("Insertion Sort", f"{res['durasi_ins_ms']:.4f} ms", "O(n^2)", "Tercepat (Adaptive)"),
            row("Selection Sort", f"{res['durasi_sel_ms']:.4f} ms", "O(n^2)", "Stabil Min Swap"),
            row("Bubble Sort", f"{res['durasi_bub_ms']:.4f} ms", "O(n^2)", "Banyak Swap"),
            sep,
            d_sep,
            "",
            "PEMBAHASAN ANALITIS SORTING M3:",
            "1. Insertion Sort unggul karena sifat adaptifnya: jika sebagian data sudah",
            "   hampir terurut, pergeseran inner loop berhenti lebih cepat (mendekati O(n)).",
            "2. Selection Sort memiliki jumlah pergeseran swap minimum (tepat n kali),",
            "   namun selalu memeriksa seluruh pasangan sehingga tetap berbiaya n(n-1)/2 komparasi.",
            "3. Bubble Sort lambat karena melakukan swap berulang kali di setiap tetangga elemen."
        ]

        report = "\n".join(lines)
        self.txt_result.delete("1.0", tk.END)
        self.txt_result.insert(tk.END, report)
        self.log_command(f"M3 - Duel Sort: Insertion {res['durasi_ins_ms']:.4f}ms | Selection {res['durasi_sel_ms']:.4f}ms | Bubble {res['durasi_bub_ms']:.4f}ms")


def main():
    root = tk.Tk()
    app = AppUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
