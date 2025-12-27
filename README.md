# Sistem Informasi Klinik Sederhana (Python + Tkinter)

Aplikasi desktop sederhana untuk manajemen operasional klinik, dikembangkan sebagai pemenuhan Tugas Mata Kuliah Pemrograman Berbasis Objek (PBO). Sistem ini dirancang berdasarkan analisis Use Case, Class Diagram, dan Activity Diagram.

## 📋 Deskripsi Proyek

Sistem ini membantu mengelola alur kerja klinik mulai dari pendaftaran pasien, pemeriksaan dokter, hingga pembayaran di kasir. Aplikasi ini dibangun menggunakan bahasa **Python** dengan antarmuka grafis (GUI) **Tkinter** dan database **SQLite**.

Aplikasi ini menerapkan konsep **Object-Oriented Programming (OOP)** secara menyeluruh, termasuk *Encapsulation*, *Inheritance*, dan *Polymorphism*.

## 🚀 Fitur Utama

Sesuai dengan rancangan Use Case Diagram:
1.  **Dashboard Menu Utama**: Navigasi terpusat untuk memisahkan peran pengguna (Front Desk, Dokter, Kasir).
2.  **Front Desk (Pendaftaran)**:
    * Input data pasien baru/lama.
    * Validasi NIK unik.
    * Pencetakan nomor antrean otomatis.
3.  **Dokter (Pemeriksaan Medis)**:
    * Melihat daftar pasien status "Menunggu".
    * Input diagnosa, keluhan, dan tanda vital (Tekanan Darah, Berat Badan).
    * Penyimpanan rekam medis.
4.  **Kasir (Pembayaran)**:
    * Melihat tagihan pasien yang sudah diperiksa.
    * Kalkulasi biaya (Jasa + Obat).
    * Update status pembayaran menjadi "Lunas".
5.  **Database Storage**: Penyimpanan data persisten menggunakan SQLite.

## 🛠️ Teknologi yang Digunakan

* **Bahasa Pemrograman**: Python 3.x
* **GUI Framework**: Tkinter (Bawaan Python)
* **Database**: SQLite3
* **Tools Desain**: Draw.io / Mermaid (untuk perancangan diagram)

## 📂 Struktur Database

Berdasarkan Class Diagram, database `klinik_final.db` terdiri dari tabel:
* `pasien`: Menyimpan data demografis (Nama, NIK, Alamat).
* `pendaftaran`: Menyimpan riwayat kunjungan dan antrean.
* `pemeriksaan`: Menyimpan hasil diagnosa dokter.
* `dokter`: Data tenaga medis.
* `obat`: Data stok dan harga obat.

## 🧩 Penerapan Konsep OOP

Kode program ini mengimplementasikan pilar OOP sebagai berikut:

1.  **Encapsulation (Pembungkusan)**
    * Atribut sensitif seperti NIK pada class `Pasien` dibuat *private* (`self.__nik`) dan hanya bisa diakses melalui *getter method*.
    
2.  **Inheritance (Pewarisan)**
    * Terdapat *Base Class* abstrak `Manusia`.
    * Class `Pasien` mewarisi atribut dan method dasar dari class `Manusia`.

3.  **Polymorphism (Banyak Bentuk)**
    * Penggunaan *Abstract Method* `deskripsi_peran()` pada class `Manusia`.
    * Class `Pasien` mengimplementasikan ulang (override) method tersebut sesuai dengan konteksnya.

## ⚙️ Cara Menjalankan Program

1.  **Clone Repository ini**
    ```bash
    git clone [https://github.com/username-anda/nama-repo-anda.git](https://github.com/username-anda/nama-repo-anda.git)
    ```
2.  **Masuk ke Direktori**
    ```bash
    cd nama-repo-anda
    ```
3.  **Jalankan Aplikasi**
    Pastikan Python sudah terinstal di komputer Anda.
    ```bash
    python sistem_klinik_v2.py
    ```
    *(Ganti `sistem_klinik_v2.py` dengan nama file python kamu)*

## 📷 Cuplikan Layar (Screenshots)

*(Opsional: Anda bisa menambahkan screenshot aplikasi di sini)*
1.  **Menu Utama**
    ![Menu Utama](link-gambar-menu.png)
2.  **Form Pendaftaran**
    ![Form Pendaftaran](link-gambar-registrasi.png)

## 👤 Author

* **Nama**: [Nama Anda, misal: Faqih Al Bashori]
* **NIM**: [NIM Anda, misal: 5240411097]
* **Prodi**: Informatika - Universitas Teknologi Yogyakarta
