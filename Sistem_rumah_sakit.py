import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from abc import ABC, abstractmethod
from datetime import datetime

# ==========================================
# 1. DATABASE MANAGER (Sesuai Class Diagram)
# ==========================================
class DatabaseManager:
    def __init__(self, db_name="RSU_UTY.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.seed_data()

    def create_tables(self):
        # Tabel Pasien
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pasien (
                id_pasien INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT,
                nik TEXT UNIQUE,
                alamat TEXT
            )
        """)
        # Tabel Dokter
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS dokter (
                id_dokter INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT,
                spesialisasi TEXT
            )
        """)
        # Tabel Obat
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS obat (
                kode_obat INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_obat TEXT,
                harga INTEGER
            )
        """)
        # Tabel Pendaftaran & Antrean
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pendaftaran (
                no_registrasi INTEGER PRIMARY KEY AUTOINCREMENT,
                id_pasien INTEGER,
                tgl_kunjungan TEXT,
                no_antrean INTEGER,
                status TEXT,
                FOREIGN KEY(id_pasien) REFERENCES pasien(id_pasien)
            )
        """)
        # Tabel Pemeriksaan
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pemeriksaan (
                id_pemeriksaan INTEGER PRIMARY KEY AUTOINCREMENT,
                no_registrasi INTEGER,
                id_dokter INTEGER,
                diagnosa TEXT,
                keluhan TEXT,
                tekanan_darah INTEGER,
                berat_badan INTEGER,
                FOREIGN KEY(no_registrasi) REFERENCES pendaftaran(no_registrasi)
            )
        """)
        self.conn.commit()

    def seed_data(self):
        # Data awal Obat & Dokter agar tidak kosong
        if not self.cursor.execute("SELECT * FROM obat").fetchone():
            self.cursor.execute("INSERT INTO obat (nama_obat, harga) VALUES ('Paracetamol', 5000)")
            self.cursor.execute("INSERT INTO obat (nama_obat, harga) VALUES ('Amoxicillin', 12000)")
            self.cursor.execute("INSERT INTO obat (nama_obat, harga) VALUES ('Vitamin C', 3000)")
        
        if not self.cursor.execute("SELECT * FROM dokter").fetchone():
            self.cursor.execute("INSERT INTO dokter (nama, spesialisasi) VALUES ('Dr. Faqih', 'Umum')")
            self.cursor.execute("INSERT INTO dokter (nama, spesialisasi) VALUES ('Dr. Sarah', 'Penyakit Dalam')")
        self.conn.commit()

# ==========================================
# 2. IMPLEMENTASI OOP (Encapsulation, Inheritance, Polymorphism)
# ==========================================

# Base Class (Abstract)
class Manusia(ABC):
    def __init__(self, nama):
        self._nama = nama 
    @abstractmethod
    def deskripsi_peran(self): 
        pass

# Class Pasien (Inheritance dari Manusia)
class Pasien(Manusia):
    def __init__(self, nama, nik, alamat, id_pasien=None):
        super().__init__(nama)
        self.__nik = nik    
        self.alamat = alamat
        self.id_pasien = id_pasien

    def deskripsi_peran(self):
        return "Pasien Klinik" 
    def get_nik(self): 
        return self.__nik

    def daftar(self, db_mgr):
        """Method untuk menyimpan data pasien ke DB"""
        cursor = db_mgr.cursor
        cursor.execute("SELECT id_pasien FROM pasien WHERE nik=?", (self.__nik,))
        existing = cursor.fetchone()
        
        if existing:
            return existing[0]
        else:
            cursor.execute("INSERT INTO pasien (nama, nik, alamat) VALUES (?, ?, ?)",
                           (self._nama, self.__nik, self.alamat))
            db_mgr.conn.commit()
            return cursor.lastrowid 

# Class Pendaftaran (Logic untuk Registrasi)
class Pendaftaran:
    def __init__(self, db_mgr):
        self.db = db_mgr

    def buat_registrasi(self, id_pasien):
        tgl = datetime.now().strftime("%Y-%m-%d")
        
        self.db.cursor.execute("SELECT COUNT(*) FROM pendaftaran WHERE tgl_kunjungan=?", (tgl,))
        antrean_ke = self.db.cursor.fetchone()[0] + 1
        
        self.db.cursor.execute("""
            INSERT INTO pendaftaran (id_pasien, tgl_kunjungan, no_antrean, status) 
            VALUES (?, ?, ?, ?)
        """, (id_pasien, tgl, antrean_ke, "Menunggu"))
        self.db.conn.commit()
        return antrean_ke

# ==========================================
# 3. GUI DENGAN TKINTER (Menu Based)
# ==========================================

class AplikasiKlinik(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Informasi Klinik - Menu Utama")
        self.geometry("900x600")
        self.db = DatabaseManager()
        
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        
        self.halaman = {} 
        
        for PageClass in (MenuUtama, HalamanFrontDesk, HalamanDokter, HalamanKasir):
            page_name = PageClass.__name__
            frame = PageClass(parent=self.container, controller=self)
            self.halaman[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.tampilkan_halaman("MenuUtama")

    def tampilkan_halaman(self, page_name):
        frame = self.halaman[page_name]
        frame.tkraise() 
        if hasattr(frame, 'refresh_data'):
            frame.refresh_data()

# --- HALAMAN MENU UTAMA (DASHBOARD) ---
class MenuUtama(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#f0f0f0")

        lbl_judul = tk.Label(self, text="SISTEM INFORMASI KLINIK", font=("Helvetica", 24, "bold"), bg="#f0f0f0")
        lbl_judul.pack(pady=50)

        lbl_sub = tk.Label(self, text="Silakan Pilih Menu Operasional:", font=("Helvetica", 14), bg="#f0f0f0")
        lbl_sub.pack(pady=10)

        # Frame Tombol Menu
        btn_frame = tk.Frame(self, bg="#f0f0f0")
        btn_frame.pack(pady=20)

        # Tombol-tombol navigasi
        btn_fd = tk.Button(btn_frame, text="FRONT DESK\n(Registrasi & Antrean)", font=("Arial", 12), width=25, height=3,
                           bg="#4CAF50", fg="white", command=lambda: controller.tampilkan_halaman("HalamanFrontDesk"))
        btn_fd.grid(row=0, column=0, padx=20, pady=10)

        btn_doc = tk.Button(btn_frame, text="DOKTER & PERAWAT\n(Pemeriksaan Medis)", font=("Arial", 12), width=25, height=3,
                            bg="#2196F3", fg="white", command=lambda: controller.tampilkan_halaman("HalamanDokter"))
        btn_doc.grid(row=0, column=1, padx=20, pady=10)

        btn_kasir = tk.Button(btn_frame, text="KASIR\n(Pembayaran)", font=("Arial", 12), width=25, height=3,
                              bg="#FF9800", fg="white", command=lambda: controller.tampilkan_halaman("HalamanKasir"))
        btn_kasir.grid(row=1, column=0, columnspan=2, pady=10)

        btn_exit = tk.Button(self, text="Keluar", command=controller.quit, bg="#f44336", fg="white", width=10)
        btn_exit.pack(pady=50)

# --- HALAMAN 1: FRONT DESK (Registrasi) ---
class HalamanFrontDesk(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Header
        header = tk.Frame(self, bg="#4CAF50", height=50)
        header.pack(fill="x")
        tk.Label(header, text="FRONT DESK - REGISTRASI", bg="#4CAF50", fg="white", font=("Arial", 16)).pack(pady=10)
        tk.Button(header, text="Kembali ke Menu", command=lambda: controller.tampilkan_halaman("MenuUtama")).pack(anchor="w", padx=10)

        # Form Input
        form_frame = tk.LabelFrame(self, text="Data Pasien Baru / Lama")
        form_frame.pack(pady=20, padx=20, fill="x")

        tk.Label(form_frame, text="Nama Pasien:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.ent_nama = tk.Entry(form_frame)
        self.ent_nama.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="NIK:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.ent_nik = tk.Entry(form_frame)
        self.ent_nik.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Alamat:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.ent_alamat = tk.Entry(form_frame)
        self.ent_alamat.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(form_frame, text="Proses Pendaftaran", command=self.proses_daftar, bg="#4CAF50", fg="white").grid(row=3, column=1, pady=10)

        # Tabel Antrean
        tk.Label(self, text="Antrean Hari Ini:").pack(padx=20, anchor="w")
        self.tree = ttk.Treeview(self, columns=("No", "Nama", "Status"), show="headings")
        self.tree.heading("No", text="No Antrean")
        self.tree.heading("Nama", text="Nama Pasien")
        self.tree.heading("Status", text="Status")
        self.tree.pack(padx=20, pady=10, fill="both", expand=True)

    def refresh_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        rows = self.controller.db.cursor.execute("""
            SELECT p.no_antrean, ps.nama, p.status 
            FROM pendaftaran p
            JOIN pasien ps ON p.id_pasien = ps.id_pasien
            WHERE p.tgl_kunjungan = ?
        """, (datetime.now().strftime("%Y-%m-%d"),)).fetchall()

        for row in rows:
            self.tree.insert("", "end", values=row)

    def proses_daftar(self):
        nama = self.ent_nama.get()
        nik = self.ent_nik.get()
        alamat = self.ent_alamat.get()

        if not nama or not nik:
            messagebox.showerror("Error", "Nama dan NIK wajib diisi!")
            return

        pasien = Pasien(nama, nik, alamat)
        id_pasien = pasien.daftar(self.controller.db) 

        pendaftaran = Pendaftaran(self.controller.db)
        no_antrean = pendaftaran.buat_registrasi(id_pasien)

        messagebox.showinfo("Sukses", f"Registrasi Berhasil!\nNomor Antrean: {no_antrean}")
        self.ent_nama.delete(0, tk.END)
        self.ent_nik.delete(0, tk.END)
        self.ent_alamat.delete(0, tk.END)
        self.refresh_data()

# --- HALAMAN 2: DOKTER (Pemeriksaan) ---
class HalamanDokter(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Header
        header = tk.Frame(self, bg="#2196F3", height=50)
        header.pack(fill="x")
        tk.Label(header, text="RUANG DOKTER - PEMERIKSAAN", bg="#2196F3", fg="white", font=("Arial", 16)).pack(pady=10)
        tk.Button(header, text="Kembali ke Menu", command=lambda: controller.tampilkan_halaman("MenuUtama")).pack(anchor="w", padx=10)

        # Input
        frame_input = tk.LabelFrame(self, text="Input Hasil Pemeriksaan")
        frame_input.pack(pady=10, padx=20, fill="x")

        tk.Label(frame_input, text="Pilih Pasien (Menunggu):").grid(row=0, column=0, sticky="w")
        self.cbo_pasien = ttk.Combobox(frame_input, state="readonly", width=40)
        self.cbo_pasien.grid(row=0, column=1, pady=5)

        tk.Label(frame_input, text="Dokter Pemeriksa:").grid(row=1, column=0, sticky="w")
        self.cbo_dokter = ttk.Combobox(frame_input, state="readonly", width=40)
        self.cbo_dokter.grid(row=1, column=1, pady=5)

        tk.Label(frame_input, text="Keluhan:").grid(row=2, column=0, sticky="w")
        self.ent_keluhan = tk.Entry(frame_input, width=43)
        self.ent_keluhan.grid(row=2, column=1, pady=5)

        tk.Label(frame_input, text="Diagnosa:").grid(row=3, column=0, sticky="w")
        self.ent_diagnosa = tk.Entry(frame_input, width=43)
        self.ent_diagnosa.grid(row=3, column=1, pady=5)

        tk.Label(frame_input, text="Tekanan Darah:").grid(row=4, column=0, sticky="w")
        self.ent_td = tk.Entry(frame_input)
        self.ent_td.grid(row=4, column=1, sticky="w", pady=5)

        tk.Button(frame_input, text="Simpan & Resepkan", command=self.simpan_periksa, bg="#2196F3", fg="white").grid(row=6, column=1, pady=10)

    def refresh_data(self):
        rows = self.controller.db.cursor.execute("""
            SELECT p.no_registrasi, ps.nama 
            FROM pendaftaran p JOIN pasien ps ON p.id_pasien = ps.id_pasien
            WHERE p.status = 'Menunggu'
        """).fetchall()
        self.cbo_pasien['values'] = [f"{r[0]} - {r[1]}" for r in rows]

        docs = self.controller.db.cursor.execute("SELECT id_dokter, nama FROM dokter").fetchall()
        self.cbo_dokter['values'] = [f"{d[0]} - {d[1]}" for d in docs]

    def simpan_periksa(self):
        if not self.cbo_pasien.get(): return
        
        no_reg = self.cbo_pasien.get().split(" - ")[0]
        id_dokter = self.cbo_dokter.get().split(" - ")[0]

        self.controller.db.cursor.execute("""
            INSERT INTO pemeriksaan (no_registrasi, id_dokter, diagnosa, keluhan, tekanan_darah, berat_badan)
            VALUES (?, ?, ?, ?, ?, 0)
        """, (no_reg, id_dokter, self.ent_diagnosa.get(), self.ent_keluhan.get(), self.ent_td.get()))
        
        self.controller.db.cursor.execute("UPDATE pendaftaran SET status='Selesai Periksa' WHERE no_registrasi=?", (no_reg,))
        self.controller.db.conn.commit()
        
        messagebox.showinfo("Info", "Pemeriksaan Selesai. Data dikirim ke Kasir.")
        self.refresh_data()
        self.ent_diagnosa.delete(0, tk.END)
        self.ent_keluhan.delete(0, tk.END)

# --- HALAMAN 3: KASIR (Pembayaran) ---
class HalamanKasir(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        header = tk.Frame(self, bg="#FF9800", height=50)
        header.pack(fill="x")
        tk.Label(header, text="KASIR - PEMBAYARAN", bg="#FF9800", fg="white", font=("Arial", 16)).pack(pady=10)
        tk.Button(header, text="Kembali ke Menu", command=lambda: controller.tampilkan_halaman("MenuUtama")).pack(anchor="w", padx=10)

        tk.Label(self, text="Pilih Tagihan (Selesai Periksa):", font=("Arial", 12)).pack(pady=20)
        self.cbo_tagihan = ttk.Combobox(self, state="readonly", width=50, font=("Arial", 11))
        self.cbo_tagihan.pack(pady=5)

        self.lbl_total = tk.Label(self, text="Total: Rp 0", font=("Arial", 14, "bold"))
        self.lbl_total.pack(pady=20)

        tk.Button(self, text="Hitung Biaya", command=self.hitung, width=20).pack()
        tk.Button(self, text="Proses Bayar & Cetak Resi", command=self.bayar, bg="#FF9800", fg="white", font=("Arial", 12, "bold"), height=2).pack(pady=20)

    def refresh_data(self):
        rows = self.controller.db.cursor.execute("""
            SELECT p.no_registrasi, ps.nama 
            FROM pendaftaran p JOIN pasien ps ON p.id_pasien = ps.id_pasien
            WHERE p.status = 'Selesai Periksa'
        """).fetchall()
        self.cbo_tagihan['values'] = [f"{r[0]} - {r[1]}" for r in rows]

    def hitung(self):
        self.biaya = 65000 
        self.lbl_total.config(text=f"Total: Rp {self.biaya} (Jasa + Obat)")

    def bayar(self):
        if not self.cbo_tagihan.get(): return
        no_reg = self.cbo_tagihan.get().split(" - ")[0]

        self.controller.db.cursor.execute("UPDATE pendaftaran SET status='Lunas' WHERE no_registrasi=?", (no_reg,))
        self.controller.db.conn.commit()
        
        messagebox.showinfo("Lunas", "Pembayaran Berhasil. Resi Dicetak.")
        self.lbl_total.config(text="Total: Rp 0")
        self.refresh_data()

# ==========================================
# MAIN DRIVER
# ==========================================
if __name__ == "__main__":
    app = AplikasiKlinik()
    app.mainloop()