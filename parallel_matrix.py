"""
Parallel Matrix Multiplication using MPI4Py
Benchmark komunikasi dan komputasi matriks besar
"""

from mpi4py import MPI
import numpy as np
import time
from typing import Optional, List

# ---------------------------------------------------------
# MPI INITIALIZATION
# ---------------------------------------------------------
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# ---------------------------------------------------------
# PARAMETER UTAMA
# ---------------------------------------------------------
N: int = 4096
chunk_sizes: List[int] = [256, 512, 1024]

if rank == 0:
    print("=== Parallel Matrix Multiplication (MPI4Py) ===")
    print(f"Jumlah proses MPI: {size}")
    print(f"Ukuran matriks: {N} x {N}")
    print("-----------------------------------------------")

# ---------------------------------------------------------
# INISIALISASI MATRIKS (hanya rank 0)
# ---------------------------------------------------------
if rank == 0:
    A_full: np.ndarray = np.random.rand(N, N).astype(np.float64)
    B: Optional[np.ndarray] = np.random.rand(N, N).astype(np.float64)
else:
    A_full = None
    B = None

# Broadcast matrix B ke semua proses
comm.Barrier()
t_bcast_start = MPI.Wtime()
B = comm.bcast(B, root=0)
t_bcast_end = MPI.Wtime()

if rank == 0:
    print(f"Latency Broadcast (B): {t_bcast_end - t_bcast_start:.6f} detik")

# ---------------------------------------------------------
# LOOP UNTUK SETIAP VARIASI SUB-MATRIK
# ---------------------------------------------------------
for chunk in chunk_sizes:
    comm.Barrier()
    if rank == 0:
        print(f"\n>>> Menguji chunk size: {chunk} baris per proses")

    # Pastikan chunk * jumlah proses tidak melebihi ukuran matriks
    total_rows = chunk * size
    if total_rows > N:
        if rank == 0:
            print("Chunk terlalu besar untuk jumlah proses.")
        continue

    # MASTER menyiapkan submatriks untuk setiap proses
    if rank == 0:
        A = A_full[:total_rows, :]  # ambil sejumlah total_rows pertama
    else:
        A = None

    # Buffer untuk menerima submatriks
    subA = np.zeros((chunk, N), dtype=np.float64)

    # ----------------------------
    # SCATTER
    # ----------------------------
    comm.Barrier()
    t_scatter_start = MPI.Wtime()
    comm.Scatter(A, subA, root=0)
    t_scatter_end = MPI.Wtime()

    # ----------------------------
    # COMPUTATION
    # ----------------------------
    comm.Barrier()
    t_compute_start = time.time()
    subC = np.dot(subA, B)
    t_compute_end = time.time()

    # ----------------------------
    # GATHER
    # ----------------------------
    if rank == 0:
        C = np.zeros((total_rows, N), dtype=np.float64)
    else:
        C = None

    comm.Barrier()
    t_gather_start = MPI.Wtime()
    comm.Gather(subC, C, root=0)
    t_gather_end = MPI.Wtime()

    # ----------------------------
    # OUTPUT MASTER
    # ----------------------------
    if rank == 0:
        print(f"Chunk {chunk} selesai.")
        print(f"  Scatter Latency   : {t_scatter_end - t_scatter_start:.6f} detik")
        print(f"  Compute Time      : {t_compute_end - t_compute_start:.6f} detik")
        print(f"  Gather Latency    : {t_gather_end - t_gather_start:.6f} detik")

if __name__ == "__main__":
    pass
