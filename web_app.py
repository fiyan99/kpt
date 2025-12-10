import streamlit as st
import subprocess
import os
import sys
import re
import pandas as pd
import altair as alt
import time

st.set_page_config(page_title="Parallel Matrix Multiplication", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🚀 Parallel Matrix Multiplication (MPI4Py)")
st.markdown("### Benchmark Performa & Skalabilitas Komputasi Paralel")
st.divider()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["▶️ Single Run", "⚡ Scalability Benchmark", "📊 Informasi", "⚙️ Pengaturan"])

# Lokasi script
script_path = os.path.join(os.path.dirname(__file__), "parallel_matrix.py")

# Fungsi helper untuk menjalankan MPI
def run_mpi(num_proc, use_oversubscribe=False, timeout=60):
    # Flag --oversubscribe hanya dipakai jika dicentang user
    flag = "--oversubscribe" if use_oversubscribe else ""
    
    cmd = f"mpiexec {flag} -n {num_proc} python {script_path}"
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=True,
            timeout=timeout
        )
        return result
    except subprocess.TimeoutExpired:
        return None

# Fungsi parser output
def parse_output(output):
    data = []
    current_chunk = None
    
    lines = output.split('\n')
    scatter, compute, gather = 0, 0, 0
    
    for line in lines:
        if "Menguji chunk size" in line:
            # Simpan data sebelumnya jika ada
            if current_chunk is not None:
                data.append({
                    "Chunk Size": str(current_chunk),
                    "Scatter": scatter,
                    "Compute": compute,
                    "Gather": gather,
                    "Total": scatter + compute + gather
                })
            # Reset
            current_chunk = int(re.search(r'chunk size: (\d+)', line).group(1))
            scatter, compute, gather = 0, 0, 0
            
        elif "Scatter Latency" in line:
            scatter = float(re.search(r': (\d+\.\d+)', line).group(1))
        elif "Compute Time" in line:
            compute = float(re.search(r': (\d+\.\d+)', line).group(1))
        elif "Gather Latency" in line:
            gather = float(re.search(r': (\d+\.\d+)', line).group(1))
            
    # Append yang terakhir
    if current_chunk is not None:
        data.append({
            "Chunk Size": str(current_chunk),
            "Scatter": scatter,
            "Compute": compute,
            "Gather": gather,
            "Total": scatter + compute + gather
        })
        
    return data

# ============================================================
# TAB 1: SINGLE RUN (Visualisasi Chunk + Ringkasan)
# ============================================================
with tab1:
    st.header("Single Execution Analysis")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        num_process = st.slider("Jumlah Proses (Workers)", 1, 16, 4)
        
        # Checkbox untuk mengatasi masalah error pada >8 proses di Windows
        enable_oversub = st.checkbox("Paksa Oversubscribe (Linux/WSL)", value=False, 
                                     help="Centang ini HANYA jika Anda menggunakan Linux/WSL dan jumlah proses > jumlah core CPU. Di Windows (Git Bash) biarkan kosong agar tidak error.")
        
        run_btn = st.button("▶️ Jalankan Program", type="primary")
    
    if run_btn:
        if not os.path.exists(script_path):
            st.error("File parallel_matrix.py tidak ditemukan!")
        else:
            with st.spinner(f"Menjalankan MPI dengan {num_process} proses..."):
                start_time = time.time()
                # Panggil fungsi dengan parameter checkbox
                result = run_mpi(num_process, use_oversubscribe=enable_oversub, timeout=120)
                
                if result and result.returncode == 0:
                    st.success(f"Selesai dalam {time.time() - start_time:.2f} detik")
                    
                    # 1. Parsing Data & DataFrame
                    parsed_data = parse_output(result.stdout)
                    df = pd.DataFrame(parsed_data)
                    
                    # 2. Tampilkan Grafik
                    st.subheader("📊 Analisis Visual")
                    
                    if not df.empty:
                        # Transform data untuk Stacked Bar Chart
                        df_melt = df.melt(id_vars=["Chunk Size", "Total"], 
                                          value_vars=["Scatter", "Compute", "Gather"],
                                          var_name="Tahapan", value_name="Waktu (detik)")
                        
                        chart = alt.Chart(df_melt).mark_bar().encode(
                            x=alt.X('Chunk Size', title='Ukuran Chunk'),
                            y=alt.Y('Waktu (detik)', title='Waktu Eksekusi (s)'),
                            color=alt.Color('Tahapan', scale=alt.Scale(scheme='tableau10')),
                            tooltip=['Chunk Size', 'Tahapan', 'Waktu (detik)']
                        ).properties(height=400)
                        
                        st.altair_chart(chart, use_container_width=True)
                    else:
                        st.warning("Tidak ada data yang bisa divisualisasikan dari output.")
                    
                    st.divider()

                    # 3. Tampilkan Hasil Ringkas (METRIK TEKS)
                    st.subheader("📋 Hasil Ringkas (Rata-rata)")
                    
                    if not df.empty:
                        avg_scatter = df["Scatter"].mean()
                        avg_compute = df["Compute"].mean()
                        avg_gather = df["Gather"].mean()
                        
                        m1, m2, m3, m4 = st.columns(4)
                        with m1:
                            st.metric("Jumlah Proses", num_process)
                        with m2:
                            st.metric("Scatter Avg", f"{avg_scatter:.6f} s")
                        with m3:
                            st.metric("Compute Avg", f"{avg_compute:.6f} s")
                        with m4:
                            st.metric("Gather Avg", f"{avg_gather:.6f} s")
                    else:
                        st.warning("Data ringkas tidak tersedia.")
                    
                    st.divider()
                    
                    # 4. Tampilkan Output Terminal Lengkap
                    with st.expander("📄 Lihat Output Terminal Lengkap"):
                        st.code(result.stdout)
                        
                elif result is None:
                    st.error("Timeout! Proses memakan waktu terlalu lama.")
                else:
                    st.error("Terjadi Error pada MPI:")
                    st.code(result.stderr) 
                    st.warning("Tips: Jika error menyebutkan 'oversubscribe' atau 'bad termination', coba ubah status Checkbox 'Paksa Oversubscribe'.")

# ============================================================
# TAB 2: SCALABILITY BENCHMARK (Visualisasi Speedup)
# ============================================================
with tab2:
    st.header("Scalability Benchmark")
    st.markdown("Menguji performa dengan meningkatkan jumlah proses secara otomatis (2, 4, 8).")
    
    # Tambahkan opsi oversubscribe juga di sini
    enable_oversub_bench = st.checkbox("Paksa Oversubscribe untuk Benchmark (Linux/WSL)", value=False, key="bench_oversub")

    if st.button("⚡ Mulai Benchmark Skalabilitas"):
        if not os.path.exists(script_path):
            st.error("File tidak ditemukan!")
        else:
            results_benchmark = []
            procs_to_test = [2, 4, 8]
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, p in enumerate(procs_to_test):
                status_text.write(f"🏃 Menjalankan dengan {p} proses...")
                
                # Jalankan dengan parameter oversubscribe yang dipilih
                res = run_mpi(p, use_oversubscribe=enable_oversub_bench)
                
                if res and res.returncode == 0:
                    data = parse_output(res.stdout)
                    if data:
                        # Ambil rata-rata total waktu dari semua chunk size
                        avg_total_time = sum([d['Total'] for d in data]) / len(data)
                        results_benchmark.append({
                            "Process": p,
                            "Avg Time (s)": avg_total_time
                        })
                    else:
                         st.warning(f"Output kosong pada {p} proses")
                else:
                    st.warning(f"Gagal pada {p} proses (Cek setting oversubscribe)")
                
                progress_bar.progress(int((i + 1) / len(procs_to_test) * 100))
            
            status_text.write("✅ Benchmark Selesai!")
            
            if results_benchmark:
                df_bench = pd.DataFrame(results_benchmark)
                
                # Hitung Speedup
                baseline_time = df_bench.iloc[0]["Avg Time (s)"]
                df_bench["Speedup"] = baseline_time / df_bench["Avg Time (s)"]
                
                col_chart1, col_chart2 = st.columns(2)
                
                with col_chart1:
                    st.subheader("📉 Waktu Eksekusi (Lower is Better)")
                    line_chart = alt.Chart(df_bench).mark_line(point=True).encode(
                        x=alt.X('Process:O', title="Jumlah Proses"),
                        y=alt.Y('Avg Time (s)', title="Waktu Rata-rata (detik)"),
                        tooltip=['Process', 'Avg Time (s)']
                    ).properties(height=300)
                    st.altair_chart(line_chart, use_container_width=True)
                
                with col_chart2:
                    st.subheader("🚀 Speedup (Higher is Better)")
                    speedup_chart = alt.Chart(df_bench).mark_line(point=True, color='green').encode(
                        x=alt.X('Process:O', title="Jumlah Proses"),
                        y=alt.Y('Speedup', title="Kali Lebih Cepat"),
                        tooltip=['Process', 'Speedup']
                    ).properties(height=300)
                    st.altair_chart(speedup_chart, use_container_width=True)
                
                st.dataframe(df_bench)
            else:
                st.error("Tidak ada data benchmark yang berhasil dikumpulkan. Cek log error.")

# ============================================================
# TAB 3: INFORMASI
# ============================================================
with tab3:
    st.subheader("ℹ️ Tentang Aplikasi")
    st.info("""
    Aplikasi ini adalah antarmuka visual untuk program MPI (Message Passing Interface)
    yang melakukan perkalian matriks secara paralel.
    
    **Fitur Utama:**
    - **Single Run:** Analisis mendalam tentang distribusi waktu (komunikasi vs komputasi).
    - **Benchmark:** Pembuktian konsep skalabilitas (Amdahl's Law).
    """)

# ============================================================
# TAB 4: PENGATURAN
# ============================================================
with tab4:
    st.subheader("⚙️ System Check")
    st.write(f"Python: {sys.version}")
    st.write(f"Script Path: {script_path}")
    if st.button("Cek Instalasi MPI"):
        try:
            ver = subprocess.run("mpiexec --version", shell=True, capture_output=True, text=True)
            st.code(ver.stdout if ver.stdout else ver.stderr)
        except Exception as e:
            st.error(str(e))