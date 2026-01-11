import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.header("Tentang Aplikasi")
        st.info("Aplikasi ini menggunakan Random Forest. Default value diatur mengikuti profil mayoritas data 'Sehat' dari dataset.")
        st.markdown("---")
        st.caption("Dikembangkan untuk Proyek Mata Kuliah Matematika Diskrit.")

def render_input_form():
    st.write("### Masukkan Data Klinis Pasien")
    st.caption("Arahkan mouse ke tanda tanya (?) di samping input untuk melihat rentang nilai normal.")
    
    # --- 1. DATA DEMOGRAFIS ---
    with st.expander("👤 Data Demografis", expanded=True):
        c1, c2 = st.columns(2)
        age = c1.number_input('Usia (tahun)', 0, 120, 58, help="Rata-rata pasien di dataset: 54 tahun.")
        sex = c2.radio('Jenis Kelamin', [0, 1], index=1, format_func=lambda x: "Perempuan" if x == 0 else "Laki-laki")

    # --- 2. TANDA VITAL ---
    with st.expander("❤️ Tanda Vital & Kondisi Fisik", expanded=True):
        c1, c2 = st.columns(2)
        trestbps = c1.number_input('Tekanan Darah (mmHg)', 50, 200, 140, help="Normal: <120. Pre-hipertensi: 120-139. Hipertensi: >140.")
        chol = c2.number_input('Kolesterol (mg/dL)', 100, 600, 212, help="Normal: <200. Batas tinggi: 200-239. Tinggi: >240.")
        
        c3, c4 = st.columns(2)
        thalach = c3.number_input('Detak Jantung Maksimum (bpm)', 50, 250, 132, help="Rumus estimasi max heart rate: 220 - Usia.")
        fbs_val = c4.radio('Gula Darah Puasa > 120 mg/dL?', [0, 1], index=0, format_func=lambda x: "Ya (Tinggi)" if x == 1 else "Tidak (Normal)", help="1 = Gula darah tinggi (>120 mg/dL), indikasi diabetes.")

    # --- 3. RIWAYAT JANTUNG ---
    with st.expander("🩺 Riwayat & Hasil Tes Jantung"):
        cp_labels = {0: 'Typical Angina', 1: 'Atypical Angina', 2: 'Non-anginal Pain', 3: 'Asymptomatic'}
        cp = st.selectbox('Jenis Nyeri Dada (CP)', options=list(cp_labels.keys()), index=0, format_func=lambda x: cp_labels[x], help="Typical Angina (0) adalah nyeri dada paling umum terkait jantung di dataset ini.")
        
        c1, c2 = st.columns(2)
        restecg = c1.selectbox('Hasil EKG Istirahat', [0, 1, 2], index=0, format_func=lambda x: {0: 'Normal', 1: 'ST-T Abnormal', 2: 'Hipertrofi'}.get(x))
        exang = c2.radio('Angina akibat Olahraga?', [0, 1], index=1, format_func=lambda x: "Ya" if x == 1 else "Tidak")
        
        c3, c4 = st.columns(2)
        oldpeak = c3.number_input('Depresi ST (Oldpeak)', 0.0, 10.0, 0.0, step=0.1, help="Nilai 0 biasanya normal. Nilai tinggi menunjukkan stres jantung saat olahraga.")
        slope = c4.selectbox('Kemiringan ST (Slope)', [0, 1, 2], index=1, format_func=lambda x: ["Downsloping", "Flat", "Upsloping"][x])
        
        c5, c6 = st.columns(2)
        ca = c5.selectbox('Jumlah Pembuluh Darah Utama (0-3)', [0, 1, 2, 3], index=0, help="0 = Normal. Semakin banyak pembuluh terlihat, semakin besar indikasi penyumbatan.")
        
        thal_labels = {1: 'Fixed Defect', 2: 'Normal', 3: 'Reversable Defect'}
        thal = c6.selectbox('Thalassemia', options=list(thal_labels.keys()), index=2, format_func=lambda x: thal_labels[x], help="Kelainan darah. Di dataset ini, kode 3 sering muncul pada orang sehat.")

    return [age, sex, cp, trestbps, chol, fbs_val, restecg, thalach, exang, oldpeak, slope, ca, thal]

# --- FUNGSI BARU UNTUK TAB INFO ---
def render_dataset_info():
    st.markdown("### ℹ️ Panduan & Referensi Data")
    st.info("""
    **PENTING:** Aplikasi ini menggunakan dataset *UCI Heart Disease*. 
    Beberapa definisi "Normal" di dataset ini mungkin berbeda dengan standar medis umum karena karakteristik sampel data.
    """)
    
    st.markdown("#### Tabel Referensi Nilai")
    st.markdown("""
    Berikut adalah panduan untuk memahami input berdasarkan pola dataset yang digunakan:
    
    | Nama Atribut | Keterangan | Nilai Normal / Risiko Rendah (Di Dataset) | Nilai Berisiko (Indikasi Penyakit) |
    | :--- | :--- | :--- | :--- |
    | **CP (Nyeri Dada)** | Jenis ketidaknyamanan dada | **0 (Typical Angina)** *[Unik di dataset ini]* | 1, 2, 3 |
    | **Thalach** | Detak Jantung Maksimum | **> 130 bpm** (Tergantung usia) | < 100 bpm (Jantung lemah memompa) |
    | **Oldpeak** | Depresi ST saat olahraga | **0.0 - 1.0** | > 1.5 (Menandakan masalah suplai darah) |
    | **Slope** | Kemiringan gelombang ST | **1 (Flat)** *[Mayoritas data sehat]* | 0 (Downsloping) atau 2 (Upsloping) |
    | **CA** | Jumlah pembuluh darah utama | **0** | 1, 2, atau 3 (Ada penyumbatan) |
    | **Thal** | Thalassemia | **3 (Reversable Defect)** *[Mayoritas data sehat]* | 1 (Fixed Defect) atau 2 (Normal) |
    | **Exang** | Nyeri dada saat olahraga | **1 (Ya)** *[Pola unik dataset]* | 0 (Tidak) |
    """)

    st.warning("""
    **Catatan Medis:** Prediksi ini hanyalah alat bantu statistik berdasarkan data historis. 
    Hasil prediksi **TIDAK BISA** menggantikan diagnosis dokter profesional.
    """)
