import streamlit as st
import subprocess
import os
import sys
import re
from datetime import datetime

st.set_page_config(page_title="Parallel Matrix Multiplication", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .success-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("# 🚀 Parallel Matrix Multiplication (MPI4Py)")
st.markdown("### Benchmark Performa Komputasi Paralel dengan MPI")
st.divider()

# Tabs
tab1, tab2, tab3 = st.tabs(["▶️ Jalankan", "📊 Informasi", "⚙️ Pengaturan Lanjut"])

# ============================================================
# TAB 1: JALANKAN
# ============================================================
with tab1:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📈 Jumlah Proses", st.session_state.get("num_process", 4))
    with col2:
        st.metric("⏱️ Timeout", f"{st.session_state.get('timeout', 60)}s")
    with col3:
        st.metric("📁 Status File", "✅ Siap" if os.path.exists(os.path.join(os.path.dirname(__file__), "parallel_matrix.py")) else "❌ Tidak")
    
    st.divider()
    
    # Input di main area
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("Konfigurasi Eksekusi")
        num_process = st.slider("Jumlah Proses MPI:", min_value=1, max_value=32, value=4, key="num_proc_main")
    
    with col_right:
        st.subheader("Kontrol")
        if st.button("▶️ Jalankan Program", use_container_width=True, key="run_main"):
            st.session_state.run_clicked = True

    st.divider()
    
    # Cek file script
    script_path = os.path.join(os.path.dirname(__file__), "parallel_matrix.py")
    
    if not os.path.exists(script_path):
        st.error(f"❌ File tidak ditemukan: {script_path}")
        st.stop()
    
    # Jalankan jika tombol diklik
    if st.session_state.get("run_clicked", False):
        progress_container = st.container()
        
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.info(f"⏳ Inisialisasi {num_process} proses MPI...")
            progress_bar.progress(10)
            
            try:
                # Gunakan --oversubscribe untuk proses >= 8
                if num_process >= 8:
                    cmd = f"mpiexec --oversubscribe -n {num_process} python {script_path}"
                else:
                    cmd = f"mpiexec -n {num_process} python {script_path}"
                
                status_text.info(f"⏳ Menjalankan: `{cmd}`")
                progress_bar.progress(25)
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    shell=True,
                    timeout=120
                )
                
                progress_bar.progress(75)
                
                # Parse output untuk metrik
                output_lines = result.stdout.split('\n')
                scatter_times = []
                compute_times = []
                gather_times = []
                
                for line in output_lines:
                    if "Scatter Latency" in line:
                        try:
                            val = float(re.search(r'(\d+\.\d+)', line).group(1))
                            scatter_times.append(val)
                        except:
                            pass
                    elif "Compute Time" in line:
                        try:
                            val = float(re.search(r'(\d+\.\d+)', line).group(1))
                            compute_times.append(val)
                        except:
                            pass
                    elif "Gather Latency" in line:
                        try:
                            val = float(re.search(r'(\d+\.\d+)', line).group(1))
                            gather_times.append(val)
                        except:
                            pass
                
                progress_bar.progress(90)
                
                # Tampilkan hasil
                status_text.empty()
                progress_bar.progress(100)
                
                if result.returncode == 0:
                    st.success("✅ Program selesai dengan sukses!")
                    
                    # Metrik ringkas
                    st.subheader("📊 Hasil Ringkas")
                    metric_cols = st.columns(4)
                    
                    with metric_cols[0]:
                        st.metric("Proses", num_process)
                    with metric_cols[1]:
                        avg_scatter = sum(scatter_times) / len(scatter_times) if scatter_times else 0
                        st.metric("Scatter Avg (s)", f"{avg_scatter:.6f}")
                    with metric_cols[2]:
                        avg_compute = sum(compute_times) / len(compute_times) if compute_times else 0
                        st.metric("Compute Avg (s)", f"{avg_compute:.6f}")
                    with metric_cols[3]:
                        avg_gather = sum(gather_times) / len(gather_times) if gather_times else 0
                        st.metric("Gather Avg (s)", f"{avg_gather:.6f}")
                    
                    # Output lengkap
                    st.subheader("📝 Output Lengkap")
                    st.code(result.stdout, language="text")
                    
                else:
                    st.warning(f"⚠️ Program keluar dengan kode: {result.returncode}")
                    if result.stdout:
                        st.subheader("Output:")
                        st.code(result.stdout, language="text")
                
                if result.stderr:
                    st.subheader("⚠️ Peringatan/Error:")
                    st.code(result.stderr, language="text")
            
            except subprocess.TimeoutExpired:
                st.error("❌ Timeout! Program tidak selesai dalam 120 detik.")
            except Exception as e:
                st.error(f"❌ Error: {type(e).__name__}: {str(e)}")
        
        st.session_state.run_clicked = False

# ============================================================
# TAB 2: INFORMASI
# ============================================================
with tab2:
    st.subheader("ℹ️ Tentang Program")
    st.info("""
    **Parallel Matrix Multiplication (MPI4Py)**
    
    Program ini menggunakan Message Passing Interface (MPI) untuk melakukan:
    - Perkalian matriks paralel
    - Benchmark komunikasi antar proses
    - Pengukuran latency Scatter/Gather
    - Perhitungan waktu komputasi
    """)
    
    st.subheader("📋 Parameter Matriks")
    param_cols = st.columns(3)
    with param_cols[0]:
        st.metric("Ukuran Matriks", "4096 × 4096")
    with param_cols[1]:
        st.metric("Chunk Sizes", "256, 512, 1024")
    with param_cols[2]:
        st.metric("Data Type", "float64")
    
    st.subheader("🔍 Penjelasan Metrik")
    st.markdown("""
    - **Scatter Latency**: Waktu untuk mendistribusikan sub-matriks ke proses
    - **Compute Time**: Waktu aktual komputasi perkalian matriks
    - **Gather Latency**: Waktu untuk mengumpulkan hasil dari semua proses
    """)

# ============================================================
# TAB 3: PENGATURAN LANJUT
# ============================================================
with tab3:
    st.subheader("⚙️ Pengaturan Lanjut")
    
    timeout = st.slider("Timeout (detik):", min_value=10, max_value=600, value=120)
    st.session_state.timeout = timeout
    
    st.divider()
    
    st.subheader("🔧 Informasi Sistem")
    system_info = st.columns(2)
    with system_info[0]:
        st.write(f"**Working Directory**: {os.getcwd()}")
    with system_info[1]:
        st.write(f"**Python Version**: {sys.version.split()[0]}")
    
    # Status file
    st.subheader("📁 Status File")
    script_path = os.path.join(os.path.dirname(__file__), "parallel_matrix.py")
    if os.path.exists(script_path):
        st.success(f"✅ parallel_matrix.py ditemukan")
        file_size = os.path.getsize(script_path)
        st.write(f"Ukuran: {file_size} bytes")
    else:
        st.error(f"❌ parallel_matrix.py tidak ditemukan")
