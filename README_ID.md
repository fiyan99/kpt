# Analisis & Benchmark Multiplikasi Matriks Paralel (MPI4Py + Streamlit Visualization)

## 📌 Gambaran Proyek

Proyek ini adalah implementasi Sistem Komputasi Paralel untuk operasi multiplikasi matriks menggunakan MPI (Message Passing Interface).

Berbeda dengan implementasi MPI standar yang hanya berbasis terminal, proyek ini dilengkapi dengan Dashboard Analitik Berbasis Web (Streamlit) yang berfungsi untuk:
1. Visualisasi Overhead: Membedah waktu eksekusi menjadi Scatter, Compute, dan Gather menggunakan grafik interaktif (Stacked Bar Chart).
2. Benchmark Otomatis: Menguji skalabilitas program (Speedup & Efficiency) dengan menjalankan simulasi multi-proses secara otomatis.
3. Cross-Platform Support: Mendukung eksekusi di Linux/WSL maupun Windows (dengan penanganan oversubscribe manual).

Proyek ini dikembangkan untuk memenuhi komponen penilaian UAS Komputasi Paralel & Terdistribusi:
- Paralelisme Master-Worker
- Pengukuran Latency & Throughput
- Analisis Skalabilitas (Amdahl's Law)
- Visualisasi Data Real-time

------------------------------------------------------------------------

## 📁 Struktur Folder

    hpc-matrix-parallel/
    │
    ├── parallel_matrix.py     # Backend: Core logic MPI (Master-Worker)
    ├── web_app.py             # Frontend: Dashboard Streamlit & Visualisasi
    ├── README_ID.md           # Dokumentasi Proyek
    └── .venv/                 # Virtual Environment

------------------------------------------------------------------------

## ⚙️ Instalasi & Persiapan

### 1. Prasyarat Sistem
Pastikan MPI sudah terinstall di sistem operasi Anda:
- Linux/WSL: sudo apt install openmpi-bin libopenmpi-dev
- Windows: Install MS-MPI (v10.0 atau terbaru).

### 2. Instalasi Library Python
Gunakan virtual environment agar terisolasi.

   # Buat dan aktifkan venv
   python -m venv .venv
   
   # Windows:
   source .venv/Scripts/activate
   # Linux/Mac:
   source .venv/bin/activate

   # Install dependensi (Wajib install pandas & altair untuk grafik)
   pip install mpi4py numpy streamlit pandas altair

------------------------------------------------------------------------

## 🚀 Cara Menjalankan Aplikasi

Anda memiliki dua opsi untuk menjalankan proyek ini:

### Opsi A: Melalui Dashboard Web (Direkomendasikan)
Gunakan cara ini untuk mendapatkan pengalaman visual penuh (grafik & benchmark otomatis).

   # Pastikan virtual environment aktif, lalu jalankan:
   python -m streamlit run web_app.py

   (Aplikasi akan terbuka otomatis di browser Anda di http://localhost:8501)

### Opsi B: Menjalankan Backend MPI Saja (Manual)
Gunakan cara ini jika Anda hanya ingin melihat output teks mentah di terminal tanpa antarmuka web.

   # Contoh menjalankan dengan 4 proses
   mpiexec -n 4 python parallel_matrix.py

------------------------------------------------------------------------

## 📊 Panduan Fitur Dashboard

Dashboard aplikasi ini dibagi menjadi dua tab utama dengan fungsi berbeda:

### 1. Tab "Single Run" (Analisis Detail)
Digunakan untuk satu kali pengujian mendalam.
- Input: Geser slider untuk memilih jumlah proses.
- Checkbox "Paksa Oversubscribe":
  * Windows: Jangan centang (biarkan kosong).
  * Linux/WSL: Centang jika jumlah proses > jumlah core CPU laptop Anda.
- Output:
  * Grafik Stacked Bar: Memvisualisasikan porsi waktu Scatter (kirim), Compute (hitung), dan Gather (terima).
  * Ringkasan Angka: Rata-rata waktu eksekusi dalam detik.
  * Terminal Log: Output asli dari MPI untuk verifikasi data.

### 2. Tab "Scalability Benchmark" (Uji Skalabilitas)
Digunakan untuk pembuktian konsep paralelisme secara otomatis.
- Cara Kerja: Klik tombol "Mulai Benchmark", sistem akan otomatis menjalankan simulasi berurutan (2, 4, dan 8 proses).
- Output:
  * Grafik Waktu Eksekusi: Menunjukkan tren penurunan waktu saat proses ditambah (Lower is Better).
  * Grafik Speedup: Menunjukkan seberapa kali lipat program lebih cepat dibanding baseline (Higher is Better).

------------------------------------------------------------------------

## 🛠️ Troubleshooting & Catatan Teknis

### Mengatasi Error "Bad Termination" / "Oversubscribe"
Jika Anda menemukan error saat menjalankan program dengan jumlah proses yang banyak (misal 8 proses), perhatikan sistem operasi Anda:

* Pengguna Windows (MS-MPI):
  MS-MPI di Windows biasanya TIDAK mendukung flag '--oversubscribe'.
  > Solusi: Di dashboard web, pastikan checkbox "Paksa Oversubscribe" TIDAK DICENTANG. Kode program telah dirancang untuk menangani ini.

* Pengguna Linux / WSL (OpenMPI):
  OpenMPI membatasi jumlah proses sesuai jumlah core fisik CPU secara default.
  > Solusi: Jika Anda ingin mensimulasikan 8 proses di laptop 4 core, Anda WAJIB MENCENTANG checkbox "Paksa Oversubscribe".

### Arsitektur Sistem
- Backend: Python (mpi4py, numpy)
- Frontend: Streamlit (pandas, altair)
- Komunikasi: Menggunakan metode Scatter (distribusi data) dan Gather (pengumpulan hasil).
- Data: Matriks random float64 ukuran 4096 x 4096.

------------------------------------------------------------------------

## 👨‍💻 Pengembang

Kelompok 3 Kelas C
Mahasiswa Teknik Informatika
UAS Komputasi Paralel & Terdistribusi

------------------------------------------------------------------------

## 📄 Lisensi

Bebas digunakan untuk kebutuhan akademik.