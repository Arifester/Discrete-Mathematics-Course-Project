import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# URL raw dari dataset di GitHub
url = "https://raw.githubusercontent.com/Arifester/Datasets/refs/heads/main/heart.csv"

# Membaca dataset
df = pd.read_csv(url)

# X = data fitur -- digunakan untuk mempelajari pola dan membuat prediksi
X = df.drop(columns=['target'])
# Y = data target -- hasil yang ingin diprediksi
Y = df['target']

# Menyediakan MinMaxScaler untuk normalisasi data
scaler = MinMaxScaler()

# Menerapkan MinMaxScaler pada data fitur X
X_scaled = scaler.fit_transform(X)

# Membagi data menjadi data latih dan data uji
X_train, X_test, y_train, y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=0)

# Membuat model Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Melatih model dengan data latih
model.fit(X_train, y_train)

# Fungsi untuk prediksi berdasarkan input pengguna
def predict_disease(data_baru):
    # Konversi data baru menjadi DataFrame dengan nama kolom yang sesuai
    data_baru_df = pd.DataFrame(data_baru, columns=X.columns)
    
    # Melakukan scaling pada data baru menggunakan scaler yang sudah dilatih
    data_baru_scaled = scaler.transform(data_baru_df)
    
    # Melakukan prediksi dengan model yang sudah dilatih
    prediksi_data_baru_rf = model.predict(data_baru_scaled)
    
    # Menentukan hasil prediksi
    if prediksi_data_baru_rf[0] == 1:
        # Warna merah untuk prediksi 1
        return st.markdown('<h3 style="color:red;">Pasien Memiliki Penyakit Jantung</h3>', unsafe_allow_html=True)
    else:
        # Warna hijau untuk prediksi 0
        return st.markdown('<h3 style="color:green;">Pasien Tidak Memiliki Penyakit Jantung</h3>', unsafe_allow_html=True)

# INTERFACE

# Judul Aplikasi
st.title('Aplikasi Pendeteksi Penyakit Jantung')

# Tampilkan gambar
st.image("image.jpg", use_container_width=True)

# Input form untuk data pengguna
st.header('Masukkan Informasi Anda')

# Input untuk usia
age = st.number_input('Usia (tahun)', min_value=0, max_value=120, value=0)

# Input untuk jenis kelamin
sex = st.radio('Jenis Kelamin', options=[0, 1], index=0, help="1 = Laki-laki, 0 = Perempuan")

# Input untuk jenis nyeri dada (cp)
cp = st.selectbox('Jenis Nyeri Dada', options=[0, 1, 2, 3], help="0 = Nyeri dada tidak ada, 1 = Nyeri dada ringan, 2 = Nyeri dada sedang, 3 = Nyeri dada berat")

# Input untuk tekanan darah saat istirahat (trestbps)
trestbps = st.number_input('Tekanan Darah Saat Istirahat (mmHg)', min_value=50, max_value=200, value=50)

# Input untuk kolesterol serum (chol)
chol = st.number_input('Kadar Kolesterol Serum (mg/dL)', min_value=100, max_value=400, value=100)

# Input untuk gula darah puasa (fbs)
fbs = st.radio('Gula Darah Puasa > 120 mg/dL?', options=[0, 1], index=0, help="1 = Ya, 0 = Tidak")

# Input untuk hasil EKG saat istirahat (restecg)
restecg = st.selectbox('Hasil EKG Setelah Istirahat', options=[0, 1, 2], help="0 = Normal, 1 = ST-T abnormal, 2 = Ventrikel hipertrofi")

# Input untuk detak jantung maksimum (thalach)
thalach = st.number_input('Detak Jantung Maksimum yang Dicapai (bpm)', min_value=50, max_value=200, value=50)

# Input untuk angina akibat latihan fisik (exang)
exang = st.radio('Mengalami Angina Setelah Berolahraga?', options=[0, 1], index=0, help="1 = Ya, 0 = Tidak")

# Input untuk depresi segmen ST (oldpeak)
oldpeak = st.number_input('Depresi Segmen ST akibat Olahraga (mm)', min_value=-10.0, max_value=10.0, value=0.00)

# Input untuk gradien/kemiringan segmen ST (slope)
slope = st.selectbox('Kemiringan Segmen ST', options=[0, 1, 2], help="0 = Menurun, 1 = Datar, 2 = Meningkat")

# Input untuk jumlah pembuluh darah utama yang diwarnai (ca)
ca = st.selectbox('Jumlah Pembuluh Darah Utama yang Diwarnai', options=[0, 1, 2, 3], help="Jumlah pembuluh darah utama yang diwarnai pada fluoroskopi")

# Input untuk thalassemia (thal)
thal = st.selectbox('Thalassemia', options=[1, 2, 3], help="1 = Normal, 2 = Cacat Permanen, 3 = Cacat yang Dapat Diperbaiki")

# Tampilkan data yang telah dimasukkan
st.subheader('Informasi yang Dimasukkan:')
st.write(f"Usia: {age} tahun")
st.write(f"Jenis Kelamin: {'Laki-laki' if sex == 1 else 'Perempuan'}")
st.write(f"Jenis Nyeri Dada: {cp}")
st.write(f"Tekanan Darah Saat Istirahat: {trestbps} mmHg")
st.write(f"Kadar Kolesterol Serum: {chol} mg/dL")
st.write(f"Gula Darah Puasa: 120 mg/dL: {'Ya' if fbs == 1 else 'Tidak'}")
st.write(f"Hasil EKG Setelah Istirahat: {restecg}")
st.write(f"Detak Jantung Maksimum yang Dicapai: {thalach} bpm")
st.write(f"Mengalami Angina Setelah Berolahraga: {'Ya' if exang == 1 else 'Tidak'}")
st.write(f"Depresi Segmen ST akibat Olahraga: {oldpeak} mm")
st.write(f"Kemiringan Segmen ST: {slope}")
st.write(f"Jumlah Pembuluh Darah Utama yang Diwarnai: {ca}")
st.write(f"Thalassemia: {thal}")

# Data baru dari input pengguna
data_baru = [[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]]

if st.button('Check Result'):
    # Aksi yang terjadi ketika tombol ditekan
    predict_disease(data_baru)

