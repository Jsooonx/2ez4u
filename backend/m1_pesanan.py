class Pesanan:
    # Pake slots supaya hemat RAM
    __slots__ = (
        'oid',
        'pelanggan',
        'resto',
        'menu',
        'harga',
        'prioritas',
        't_masuk_detik',
        't_selesai_detik',
        'status'
    )

    # harga diubah ke int supaya bisa dibandingin, kalau kosong diisi 0
    # prioritas diubah ke int supaya bisa dibandingin, kalau kosong diisi 3
    # t_masuk_detik diubah ke int supaya bisa dibandingin, kalau kosong diisi 0
    # t_selesai_detik diubah ke int supaya bisa dibandingin, kalau kosong diisi None
    # status diubah ke string
    def __init__(self, oid, pelanggan, resto, menu, harga, prioritas, t_masuk_detik, t_selesai_detik, status):
        self.oid = str(oid)
        self.pelanggan = str(pelanggan)
        self.resto = str(resto)
        self.menu = str(menu)
        self.harga = int(harga) if harga != "" and harga is not None else 0
        self.prioritas = int(prioritas) if prioritas != "" and prioritas is not None else 3
        self.t_masuk_detik = int(t_masuk_detik) if t_masuk_detik != "" and t_masuk_detik is not None else 0
        self.t_selesai_detik = int(t_selesai_detik) if t_selesai_detik != "" and t_selesai_detik is not None else None
        self.status = str(status)

    # helper method supaya data enak dibaca saat diprint
    def ringkasan(self):
        return f"[{self.oid}] {self.pelanggan} | {self.resto} - {self.menu} | Rp{self.harga:,} | Prio:{self.prioritas} |Status:{self.status}"

    # representasi objek supaya enak dibaca
    def __repr__(self):
        return f"<Pesanan {self.oid} ({self.pelanggan})>"
    
class Array:
    def __init__(self, capacity=4):
        # kapasitas awal minimal 4
        self.capacity = capacity if capacity > 0 else 4
        self.size = 0
        # alokasi memori array
        self.data = [None] * self.capacity

    def __len__(self):
        # memungkkinkan utk memanggil len(array_objek)
        return self.size

    def _resize(self, new_capacity):
        """
        Menggandakan alokasi memori array dan menyalin data lama secara manual.
        Kompleksitas: O(n) saat resize terjadi.
        """
        new_data = [None] * new_capacity
        # salin elemen dari array lama ke array baru
        for i in range(self.size):
            new_data[i] = self.data[i]

        # ganti array lama dengan yang baru
        self.data = new_data
        self.capacity = new_capacity

    def append(self,v):
        """
        Menambahkan pesanan REGULER di posisi paling belakang antrean.
        Kompleksitas: O(1) amortized.
        """

        # jika kapasitas penuh, gandakan kapasitasnya x2
        if self.size == self.capacity:
            self._resize(self.capacity * 2)

        self.data[self.size] = v
        self.size += 1

    def get(self, i):
        """
        Melihat pesanan ke-i secara instan via indeks memori.
        Kompleksitas: O(1).
        """
        # validasi batas indeks
        if i < 0 or i >= self.size:
            raise IndexError(f"Indeks {i} di luar batas (ukuran array: {self.size})")
        return self.data[i]

    def insert(self, i, v):
        """menyimpan pesanan pada indeks ke-i
        - VIP (i = 0): O(n)
        - PRIORITAS (i = size // 2): O(n)
        """
        if i < 0 or i > self.size:
            raise IndexError(f"Indeks penyisipan di luar batas: {i} (size:{self.size})")

        #jika kapasitas penuh, gandakan kapasitas
        if self.size == self.capacity:
            self._resize(self.capacity * 2)

        for k in range(self.size, i, -1):
            self.data[k] = self.data[k - 1]

        #letakkan elemen baru di slot indeks i
        self.data[i] = v
        self.size += 1

    def delete(self, i):
        """
        Menghapus pesanan pada indeks ke-i dan menggeser elemen kanan ke kiri.
        Kompleksitas: O(n).
        """
        if i < 0 or i >= self.size:
            raise IndexError(f"Indeks di luar batas: {i} (size: {self.size})")

        deleted_item = self.data[i]

        #geser elemen di sebelah kanan indeks i satu langkah ke kiri
        for k in range(i, self.size - 1):
            self.data[k] = self.data[k + 1]

        #kosongkan slot terakhir dan kurangi ukuran
        self.data[self.size - 1] = None
        self.size -= 1
        return deleted_item

class Node:
    """Simpul tunggal untuk Linked List"""
    __slots__ = ('val', 'next')

    def __init__(self, val, next=None):
        self.val = val
        self.next = next

class LinkList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __len__(self):
        return self.size

    def append(self, v):
        """
        Menambahkan pesanan REGULER di paling belakang barisan.
        Kompleksitas: O(1) menggunakan self.tail.
        """
        new_node = Node(v)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def insert_front(self, v):
        """
        Menambahkan pesanan VIP di urutan terdepan (indeks 0).
        Kompleksitas: O(1) langsung memperbarui self.head.
        """
        new_node = Node(v, next=self.head)
        self.head = new_node
        if self.tail is None:
            self.tail = new_node
        self.size += 1

    def insert(self, i, v):
        """
        Menyisipkan pesanan pada posisi ke-i.
        - Jika i == 0 (VIP) -> O(1) via insert_front.
        - Jika i == size (REGULER) -> O(1) via append.
        - Jika i di tengah (PRIORITAS di size // 2) -> O(n) traversal ke simpul (i - 1).
        """
        if i < 0 or i > self.size:
            raise IndexError(f"Indeks penyisipan di luar batas: {i} (size: {self.size})")

        if i == 0:
            self.insert_front(v)
            return

        if i == self.size:
            self.append(v)
            return

        # Traversal ke simpul tepat sebelum posisi i
        curr = self.head
        for _ in range(i - 1):
            curr = curr.next

        new_node = Node(v, next=curr.next)
        curr.next = new_node
        self.size += 1

    def get(self, i):
        """
        Melihat pesanan ke-i dengan menelusuri rantai dari head.
        Kompleksitas: O(n).
        """
        if i < 0 or i >= self.size:
            raise IndexError(f"Indeks di luar batas: {i} (size: {self.size})")

        # Shortcut jika elemen terakhir
        if i == self.size - 1 and self.tail is not None:
            return self.tail.val

        curr = self.head
        for _ in range(i):
            curr = curr.next
        return curr.val

    def delete(self, i):
        """
        Menghapus pesanan pada simpul ke-i.
        Kompleksitas: O(n) traversal ke simpul (i - 1).
        """
        if i < 0 or i >= self.size:
            raise IndexError(f"Indeks di luar batas: {i} (size: {self.size})")

        # Kasus khusus: hapus elemen pertama (head)
        if i == 0:
            deleted_val = self.head.val
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            self.size -= 1
            return deleted_val

        # Traversal ke simpul sebelum i
        curr = self.head
        for _ in range(i - 1):
            curr = curr.next

        deleted_val = curr.next.val
        curr.next = curr.next.next

        # Jika yang dihapus adalah tail, update pointer tail ke curr
        if i == self.size - 1:
            self.tail = curr

        self.size -= 1
        return deleted_val


def muat_pesanan_csv(filepath, limit=None):
    """
    Membaca data dari CSV pesanan dan memuatnya ke Array dan LinkList sekaligus.
    Mengembalikan (arr, ll, durasi_detik, jumlah_baris).
    """
    import csv
    import time

    arr = Array(capacity=8)
    ll = LinkList()

    t_mulai = time.perf_counter()
    count = 0

    with open(filepath, mode='r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)  # lewati header

        for row in reader:
            if not row or len(row) < 9:
                continue

            p = Pesanan(
                oid=row[0],
                pelanggan=row[1],
                resto=row[2],
                menu=row[3],
                harga=row[4],
                prioritas=row[5],
                t_masuk_detik=row[6],
                t_selesai_detik=row[7],
                status=row[8]
            )
            arr.append(p)
            ll.append(p)
            count += 1

            if limit is not None and count >= limit:
                break

    t_selesai = time.perf_counter()
    durasi = t_selesai - t_mulai
    return arr, ll, durasi, count