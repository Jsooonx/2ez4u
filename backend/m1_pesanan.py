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

    # Inisialisasi atribut pesanan
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

    # Format ringkas untuk tampilan teks / terminal
    def ringkasan(self):
        return f"[{self.oid}] {self.pelanggan} | {self.resto} - {self.menu} | Rp{self.harga:,} | Prio:{self.prioritas} |Status:{self.status}"

    def __repr__(self):
        return f"<Pesanan {self.oid} ({self.pelanggan})>"
    

class Array:
    # Dynamic Array primitif dengan penggandaan kapasitas
    def __init__(self, capacity=4):
        self.capacity = capacity if capacity > 0 else 4
        self.size = 0
        self.data = [None] * self.capacity

    def __len__(self):
        return self.size

    def _resize(self, new_capacity):
        # Gandakan kapasitas array dan salin data lama
        new_data = [None] * new_capacity
        for i in range(self.size):
            new_data[i] = self.data[i]

        self.data = new_data
        self.capacity = new_capacity

    def append(self, v):
        # Tambah pesanan di posisi paling belakang
        if self.size == self.capacity:
            self._resize(self.capacity * 2)

        self.data[self.size] = v
        self.size += 1

    def get(self, i):
        # Ambil pesanan berdasarkan indeks langsung
        if i < 0 or i >= self.size:
            raise IndexError(f"Indeks {i} di luar batas (ukuran array: {self.size})")
        return self.data[i]

    def insert(self, i, v):
        # Sisipkan pesanan pada indeks ke-i (geser elemen ke kanan)
        if i < 0 or i > self.size:
            raise IndexError(f"Indeks penyisipan di luar batas: {i} (size:{self.size})")

        if self.size == self.capacity:
            self._resize(self.capacity * 2)

        for k in range(self.size, i, -1):
            self.data[k] = self.data[k - 1]

        self.data[i] = v
        self.size += 1

    def delete(self, i):
        # Hapus pesanan pada indeks ke-i dan geser sisa elemen ke kiri
        if i < 0 or i >= self.size:
            raise IndexError(f"Indeks di luar batas: {i} (size: {self.size})")

        deleted_item = self.data[i]
        for k in range(i, self.size - 1):
            self.data[k] = self.data[k + 1]

        self.data[self.size - 1] = None
        self.size -= 1
        return deleted_item


class Node:
    # Simpul singly linked list
    __slots__ = ('val', 'next')

    def __init__(self, val, next=None):
        self.val = val
        self.next = next


class LinkList:
    # Singly Linked List dengan pointer head dan tail
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __len__(self):
        return self.size

    def append(self, v):
        # Tambah pesanan di ujung rantai lewat tail
        new_node = Node(v)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def insert_front(self, v):
        # Tambah pesanan di urutan paling depan (head)
        new_node = Node(v, next=self.head)
        self.head = new_node
        if self.tail is None:
            self.tail = new_node
        self.size += 1

    def insert(self, i, v):
        # Sisipkan pesanan pada urutan ke-i
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
        # Ambil pesanan ke-i dengan traversal dari head
        if i < 0 or i >= self.size:
            raise IndexError(f"Indeks di luar batas: {i} (size: {self.size})")

        if i == self.size - 1 and self.tail is not None:
            return self.tail.val

        curr = self.head
        for _ in range(i):
            curr = curr.next
        return curr.val

    def delete(self, i):
        # Hapus pesanan pada urutan ke-i
        if i < 0 or i >= self.size:
            raise IndexError(f"Indeks di luar batas: {i} (size: {self.size})")

        if i == 0:
            deleted_val = self.head.val
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            self.size -= 1
            return deleted_val

        curr = self.head
        for _ in range(i - 1):
            curr = curr.next

        deleted_val = curr.next.val
        curr.next = curr.next.next

        if i == self.size - 1:
            self.tail = curr

        self.size -= 1
        return deleted_val


def muat_pesanan_csv(filepath, limit=None):
    # Baca file CSV pesanan dan masukkan ke Array & LinkList
    import csv
    import time

    arr = Array(capacity=8)
    ll = LinkList()

    t_mulai = time.perf_counter()
    count = 0

    with open(filepath, mode='r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)

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