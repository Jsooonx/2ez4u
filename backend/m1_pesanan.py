class Pesanan:
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

    def ringkasan(self):
        return f"[{self.oid}] {self.pelanggan} | {self.resto} - {self.menu} | Rp{self.harga:,} | Prio:{self.prioritas} |Status:{self.status}"

    def __repr__(self):
        return f"<Pesanan {self.old} ({self.pelanggan})>"
    
