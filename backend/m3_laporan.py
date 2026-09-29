# Milestone 3: Laporan Terurut & Binary Search

import time
from backend.m1_pesanan import Pesanan


def insertion_sort(data, key_func=None, reverse=False):
    # Insertion sort
    n = len(data)
    for i in range(1, n):
        key_item = data[i]
        key_val = key_func(key_item) if key_func else key_item
        j = i - 1

        if not reverse:
            while j >= 0 and (key_func(data[j]) if key_func else data[j]) > key_val:
                data[j + 1] = data[j]
                j -= 1
        else:
            while j >= 0 and (key_func(data[j]) if key_func else data[j]) < key_val:
                data[j + 1] = data[j]
                j -= 1

        data[j + 1] = key_item
    return data


def selection_sort(data, key_func=None, reverse=False):
    # Selection sort
    n = len(data)
    for i in range(n - 1):
        target_idx = i
        for j in range(i + 1, n):
            val_j = key_func(data[j]) if key_func else data[j]
            val_target = key_func(data[target_idx]) if key_func else data[target_idx]

            if not reverse:
                if val_j < val_target:
                    target_idx = j
            else:
                if val_j > val_target:
                    target_idx = j

        if target_idx != i:
            data[i], data[target_idx] = data[target_idx], data[i]
    return data


def bubble_sort(data, key_func=None, reverse=False):
    # Bubble sort
    n = len(data)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            val_a = key_func(data[j]) if key_func else data[j]
            val_b = key_func(data[j + 1]) if key_func else data[j + 1]

            if not reverse:
                if val_a > val_b:
                    data[j], data[j + 1] = data[j + 1], data[j]
                    swapped = True
            else:
                if val_a < val_b:
                    data[j], data[j + 1] = data[j + 1], data[j]
                    swapped = True
        if not swapped:
            break
    return data


def binary_search(data, target_val, key_func=None):
    # Binary search O(log n)
    low = 0
    high = len(data) - 1
    steps = 0
    found_idx = -1

    while low <= high:
        steps += 1
        mid = (low + high) // 2
        mid_val = key_func(data[mid]) if key_func else data[mid]

        if mid_val == target_val:
            found_idx = mid
            break
        elif mid_val < target_val:
            low = mid + 1
        else:
            high = mid - 1

    if found_idx == -1:
        return -1, steps, []

    # Ambil elemen dengan nilai sama di sekitar mid
    matches = [data[found_idx]]

    left = found_idx - 1
    while left >= 0:
        val = key_func(data[left]) if key_func else data[left]
        if val == target_val:
            matches.append(data[left])
            left -= 1
        else:
            break

    right = found_idx + 1
    while right < len(data):
        val = key_func(data[right]) if key_func else data[right]
        if val == target_val:
            matches.append(data[right])
            right += 1
        else:
            break

    return found_idx, steps, matches


def linear_search(data, target_val, key_func=None):
    # Linear search pembanding
    steps = 0
    for i in range(len(data)):
        steps += 1
        val = key_func(data[i]) if key_func else data[i]
        if val == target_val:
            return i, steps
    return -1, steps


class LaporanManager:
    # Pengelola laporan terurut dan pencarian
    def __init__(self):
        self.data_laporan = []
        self.kunci_terakhir = None
        self.algoritma_terakhir = None
        self.durasi_sort_ms = 0.0
        self.total_omset = 0
        self.rata_rata_harga = 0
        self.min_harga = 0
        self.max_harga = 0

    def salin_subset(self, array_sumber, limit=1000, status_filter=None):
        # Ambil subset data pesanan
        n_total = len(array_sumber)
        hasil = []
        count = 0

        for i in range(n_total):
            item = array_sumber.get(i)
            if status_filter is not None and item.status != status_filter:
                continue

            hasil.append(item)
            count += 1
            if limit is not None and count >= limit:
                break

        return hasil

    def buat_laporan(self, array_sumber, limit=1000, sort_by="harga", algoritma="insertion", status_filter=None, reverse=False):
        daftar = self.salin_subset(array_sumber, limit=limit, status_filter=status_filter)
        n = len(daftar)
        if n == 0:
            return [], 0.0

        if sort_by == "waktu":
            def kunci(p): return p.t_masuk_detik
        else:
            def kunci(p): return p.harga

        t0 = time.perf_counter()
        if algoritma == "selection":
            selection_sort(daftar, key_func=kunci, reverse=reverse)
        elif algoritma == "bubble":
            bubble_sort(daftar, key_func=kunci, reverse=reverse)
        else:
            insertion_sort(daftar, key_func=kunci, reverse=reverse)
        t1 = time.perf_counter()

        self.durasi_sort_ms = (t1 - t0) * 1000.0
        self.data_laporan = daftar
        self.kunci_terakhir = sort_by
        self.algoritma_terakhir = algoritma

        # Hitung statistik omset
        tot = 0
        min_h = daftar[0].harga
        max_h = daftar[0].harga
        for i in range(n):
            h = daftar[i].harga
            tot += h
            if h < min_h:
                min_h = h
            if h > max_h:
                max_h = h

        self.total_omset = tot
        self.rata_rata_harga = tot // n if n > 0 else 0
        self.min_harga = min_h
        self.max_harga = max_h

        return self.data_laporan, self.durasi_sort_ms

    def cari_laporan(self, target_val):
        # Cari pesanan di laporan terurut
        if not self.data_laporan:
            return None

        if self.kunci_terakhir == "waktu":
            def kunci(p): return p.t_masuk_detik
        else:
            def kunci(p): return p.harga

        t0_bs = time.perf_counter()
        idx_bs, steps_bs, matches = binary_search(self.data_laporan, target_val, key_func=kunci)
        t1_bs = time.perf_counter()
        durasi_bs_ms = (t1_bs - t0_bs) * 1000.0

        t0_ls = time.perf_counter()
        idx_ls, steps_ls = linear_search(self.data_laporan, target_val, key_func=kunci)
        t1_ls = time.perf_counter()
        durasi_ls_ms = (t1_ls - t0_ls) * 1000.0

        return {
            "found_idx": idx_bs,
            "steps_bs": steps_bs,
            "durasi_bs_ms": durasi_bs_ms,
            "steps_ls": steps_ls,
            "durasi_ls_ms": durasi_ls_ms,
            "matches": matches,
            "total_data": len(self.data_laporan)
        }

    def duel_sort(self, array_sumber, limit=500, sort_by="harga"):
        # Duel 3 algoritma sorting
        def kunci(p): return p.harga if sort_by == "harga" else p.t_masuk_detik

        list_ins = self.salin_subset(array_sumber, limit=limit)
        list_sel = self.salin_subset(array_sumber, limit=limit)
        list_bub = self.salin_subset(array_sumber, limit=limit)

        t0 = time.perf_counter()
        insertion_sort(list_ins, key_func=kunci)
        durasi_ins_ms = (time.perf_counter() - t0) * 1000.0

        t0 = time.perf_counter()
        selection_sort(list_sel, key_func=kunci)
        durasi_sel_ms = (time.perf_counter() - t0) * 1000.0

        t0 = time.perf_counter()
        bubble_sort(list_bub, key_func=kunci)
        durasi_bub_ms = (time.perf_counter() - t0) * 1000.0

        return {
            "limit": limit,
            "durasi_ins_ms": durasi_ins_ms,
            "durasi_sel_ms": durasi_sel_ms,
            "durasi_bub_ms": durasi_bub_ms
        }
