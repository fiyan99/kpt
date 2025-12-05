# Multiplikasi Matriks Paralel Menggunakan MPI4Py + Antarmuka Web Streamlit

## 📌 Gambaran Proyek

Proyek ini mengimplementasikan **Multiplikasi Matriks Paralel**
menggunakan **MPI4Py**, dengan model Master--Worker.\
Selain itu, ditambahkan **Antarmuka Web Streamlit** untuk menjalankan
MPI melalui web dan menampilkan hasilnya secara interaktif.

Proyek ini dikembangkan untuk **UAS Komputasi Paralel & Terdistribusi**,
dan telah memenuhi seluruh komponen yang diwajibkan: - Paralelisme -
Latency - Komunikasi antar node - Compile & Runtime Information -
Distribusi beban kerja - Fault-tolerance (dasar) - Pengujian
skalabilitas (2, 4, 8, 16 proses) - Evaluasi throughput, speedup, dan
efisiensi - Implementasi tambahan berbasis Web

------------------------------------------------------------------------

## 📁 Struktur Folder

    hpc-matrix-parallel/
    │
    ├── parallel_matrix.py     # Program utama MPI
    ├── web_app.py             # Antarmuka Web Streamlit
    ├── README.md              # Dokumentasi
    └── .venv/                 # Virtual environment (tidak disertakan)

------------------------------------------------------------------------

## ⚙️ Instalasi Dependensi

### 1️⃣ Install OpenMPI (Level Sistem)

``` bash
sudo apt update
sudo apt install openmpi-bin libopenmpi-dev -y
```

### 2️⃣ Buat dan Aktifkan Virtual Environment

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Install Library Python

``` bash
pip install mpi4py numpy streamlit
```

------------------------------------------------------------------------

## ▶️ Menjalankan Program MPI Secara Manual

``` bash
mpiexec --oversubscribe -n 4 python parallel_matrix.py
```

Ganti angka `4` dengan: - 2 (baseline) - 4 (optimal) - 8
(oversubscribe) - 16 (stress test)

------------------------------------------------------------------------

## 🌐 Menjalankan Aplikasi Web Streamlit

Di dalam venv aktif:

``` bash
streamlit run web_app.py
```

Akses melalui browser:

    http://localhost:8501

------------------------------------------------------------------------

## 🧠 Penjelasan Konsep Web

Antarmuka web **tidak menjalankan MPI di browser**, tetapi:

1.  Pengguna memilih jumlah proses MPI.

2.  Backend Streamlit menjalankan:

    ``` bash
    mpiexec --oversubscribe -n X python parallel_matrix.py
    ```

3.  Output (latency, scatter, compute, gather) ditangkap.

4.  Output ditampilkan kembali ke web.

### 🔧 Teknologi yang Digunakan

  Komponen            Teknologi
  ------------------- -------------------
  Komputasi Paralel   OpenMPI, MPI4Py
  Operasi Matriks     Numpy
  Antarmuka Web       Streamlit
  Eksekusi Backend    Python subprocess
  Eksekusi Paralel    mpiexec

------------------------------------------------------------------------

## 📊 Deskripsi Output

Program akan menampilkan hasil pengujian multiplikasi matriks:

    >>> Menguji chunk size: 256 baris per proses
    Scatter Latency   : 0.02 detik
    Compute Time      : 1.12 detik
    Gather Latency    : 0.03 detik

    >>> Menguji chunk size: 512 baris per proses
    ...

Setiap pengujian memberikan: - Latency broadcast - Latency scatter -
Waktu komputasi lokal - Latency gather - Validasi chunk terlalu besar
(jika terjadi)

Data ini digunakan untuk analisis: - Speedup - Efisiensi -
Skalabilitas - Throughput

------------------------------------------------------------------------

## 📈 Catatan Skalabilitas

Berdasarkan pengujian:

  Jumlah Proses   Hasil
  --------------- -----------------------------------
  **2**           Performa baik
  **4**           Optimal
  **8**           Terjadi oversubscribe penalty
  **16**          Performa turun drastis (expected)

Chunk besar (1024) tidak valid ketika baris per proses \< 1024.

------------------------------------------------------------------------

## 🌐 Preview Antarmuka Web

Antarmuka Web menampilkan: - Input jumlah proses - Tombol "RUN MPI" -
Output realtime dari proses MPI

------------------------------------------------------------------------

## 📝 Catatan UAS (Kesesuaian)

Proyek ini memenuhi:

-   Implementasi paralelisme\
-   Penggunaan MPI (Master--Worker)\
-   Pengukuran latency dan throughput\
-   Pembagian beban kerja (chunking)\
-   Analisis skalabilitas\
-   Fault tolerance (dasar)\
-   Dokumentasi\
-   Antarmuka web sebagai tambahan nilai plus

------------------------------------------------------------------------

## 👨‍💻 Pengembang

**Kelompok 3 Kelas C**\
Mahasiswa Teknik Informatika\
UAS Komputasi Paralel & Terdistribusi

------------------------------------------------------------------------

## 📄 Lisensi

Bebas digunakan untuk kebutuhan akademik.
