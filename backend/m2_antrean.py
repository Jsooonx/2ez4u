# Milestone 2: Antrean Dapur (Circular Queue) & Fitur Undo (Stack)

import time
from backend.m1_pesanan import Pesanan


class CircularQueue:
    # Circular Queue FIFO berbasis fixed array
    def __init__(self, capacity=16):
        self.capacity = capacity if capacity > 0 else 16
        self.data = [None] * self.capacity
        self.front = 0
        self.rear = -1
        self.size = 0

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def is_full(self):
        return self.size == self.capacity

    def _resize(self, new_capacity):
        # Gandakan ukuran array dan tata ulang urutan elemen jadi linear
        new_data = [None] * new_capacity
        for i in range(self.size):
            old_idx = (self.front + i) % self.capacity
            new_data[i] = self.data[old_idx]

        self.data = new_data
        self.capacity = new_capacity
        self.front = 0
        self.rear = self.size - 1

    def enqueue(self, item):
        # Masuk antrean dari belakang (FIFO)
        if self.is_full():
            self._resize(self.capacity * 2)

        self.rear = (self.rear + 1) % self.capacity
        self.data[self.rear] = item
        self.size += 1

    def dequeue(self):
        # Ambil dan layani pesanan paling depan
        if self.is_empty():
            raise IndexError("Antrean kosong, tidak ada pesanan yang bisa dilayani.")

        item = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return item

    def peek(self):
        # Intip pesanan paling depan tanpa mengeluarkan
        if self.is_empty():
            return None
        return self.data[self.front]

    def requeue_front(self, item):
        # Undo: kembalikan pesanan ke posisi paling depan
        if self.is_full():
            self._resize(self.capacity * 2)

        self.front = (self.front - 1 + self.capacity) % self.capacity
        self.data[self.front] = item
        self.size += 1

    def unqueue_rear(self):
        # Undo: batalkan pesanan terakhir di belakang antrean
        if self.is_empty():
            raise IndexError("Antrean kosong.")

        item = self.data[self.rear]
        self.data[self.rear] = None
        self.rear = (self.rear - 1 + self.capacity) % self.capacity
        self.size -= 1
        return item

    def to_list(self):
        # Konversi antrean ke list dari depan ke belakang
        hasil = []
        for i in range(self.size):
            idx = (self.front + i) % self.capacity
            hasil.append(self.data[idx])
        return hasil


class Stack:
    # Stack LIFO untuk riwayat aksi (fitur undo)
    def __init__(self, capacity=16):
        self.capacity = capacity if capacity > 0 else 16
        self.data = [None] * self.capacity
        self.top = -1

    def __len__(self):
        return self.top + 1

    def is_empty(self):
        return self.top == -1

    def _resize(self, new_capacity):
        # Gandakan ukuran array stack
        new_data = [None] * new_capacity
        for i in range(self.top + 1):
            new_data[i] = self.data[i]
        self.data = new_data
        self.capacity = new_capacity

    def push(self, item):
        # Simpan aksi ke tumpukan paling atas
        if self.top + 1 == self.capacity:
            self._resize(self.capacity * 2)

        self.top += 1
        self.data[self.top] = item

    def pop(self):
        # Ambil aksi paling atas untuk di-undo
        if self.is_empty():
            raise IndexError("Tumpukan kosong, tidak ada aksi yang bisa di-undo.")

        item = self.data[self.top]
        self.data[self.top] = None
        self.top -= 1
        return item

    def peek(self):
        # Lihat aksi paling atas
        if self.is_empty():
            return None
        return self.data[self.top]

    def to_list(self):
        # Ambil daftar riwayat aksi dari yang terbaru
        hasil = []
        for i in range(self.top, -1, -1):
            hasil.append(self.data[i])
        return hasil


class AksiUndo:
    # Data riwayat aksi untuk undo (tipe: ENQUEUE / DEQUEUE)
    __slots__ = ('tipe', 'pesanan', 'waktu_str', 'keterangan')

    def __init__(self, tipe, pesanan, waktu_str=None, keterangan=""):
        self.tipe = str(tipe)
        self.pesanan = pesanan
        self.waktu_str = waktu_str if waktu_str is not None else time.strftime("%H:%M:%S")
        self.keterangan = str(keterangan)

    def __repr__(self):
        return f"<AksiUndo {self.tipe}: {self.pesanan.oid} @ {self.waktu_str}>"


class AntreanManager:
    # Pengelola antrean dapur (CircularQueue) dan riwayat undo (Stack)
    def __init__(self):
        self.queue = CircularQueue(capacity=16)
        self.undo_stack = Stack(capacity=16)

    def tambah_antrean(self, pesanan):
        # Enqueue pesanan dan catat aksi ke stack undo
        self.queue.enqueue(pesanan)
        aksi = AksiUndo(
            tipe="ENQUEUE",
            pesanan=pesanan,
            keterangan=f"Pesanan {pesanan.oid} ({pesanan.pelanggan}) masuk antrean dapur"
        )
        self.undo_stack.push(aksi)
        return aksi

    def layani_berikutnya(self):
        # Dequeue pesanan terdepan dan catat aksi ke stack undo
        if self.queue.is_empty():
            return None

        pesanan = self.queue.dequeue()
        status_lama = pesanan.status
        pesanan.status = "DONE"

        aksi = AksiUndo(
            tipe="DEQUEUE",
            pesanan=pesanan,
            keterangan=f"Pesanan {pesanan.oid} ({pesanan.pelanggan}) selesai dilayani (Status: {status_lama} -> DONE)"
        )
        self.undo_stack.push(aksi)
        return pesanan

    def undo(self):
        # Batalkan aksi terakhir (LIFO)
        if self.undo_stack.is_empty():
            return None

        aksi = self.undo_stack.pop()

        if aksi.tipe == "DEQUEUE":
            # Kembalikan pesanan ke urutan terdepan antrean
            aksi.pesanan.status = "ANTRE"
            self.queue.requeue_front(aksi.pesanan)
            return ("BATAL_LAYANI", aksi.pesanan, aksi)

        elif aksi.tipe == "ENQUEUE":
            # Batalkan pesanan terakhir di belakang antrean
            pesanan_batal = self.queue.unqueue_rear()
            return ("BATAL_TAMBAH", pesanan_batal, aksi)

        return None
