import streamlit as st
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay
from src.model_loader import load_and_train_model, predict_single_input
from src.ui_helper import render_sidebar, render_input_form, render_dataset_info # <--- Import fungsi baru

st.set_page_config(page_title="Heart Disease Detector", page_icon="💓", layout="centered")

model, scaler, columns, metrics = load_and_train_model()

render_sidebar()

st.title("💓 Prediksi Risiko Penyakit Jantung")

if model is None:
    st.error("Gagal memuat model. Periksa koneksi internet.")
    st.stop()

# --- UPDATE DISINI: JADI 3 TAB ---
tab1, tab2, tab3 = st.tabs(["🕵️‍♂️ Aplikasi Prediksi", "📊 Evaluasi Model", "ℹ️ Info Dataset"])

# TAB 1: PREDIKSI
with tab1:
    with st.form("prediction_form"):
        user_input = render_input_form()
        submitted = st.form_submit_button("Analisis Risiko", use_container_width=True, type="primary")

    if submitted:
        prediction, probability = predict_single_input(model, scaler, user_input, columns)
        
        st.markdown("---")
        st.subheader("Hasil Analisis:")
        
        col_result, col_prob = st.columns([2, 1])
        
        with col_result:
            if prediction == 1:
                st.error("⚠️ **POSITIF: BERISIKO TINGGI**")
                st.write("Berdasarkan pola data, pasien memiliki indikasi penyakit jantung.")
            else:
                st.success("✅ **NEGATIF: RISIKO RENDAH**")
                st.write("Berdasarkan pola data, kondisi pasien cenderung aman.")
        
        with col_prob:
            prob_score = probability[1] * 100
            st.metric(label="Probabilitas Sakit", value=f"{prob_score:.1f}%")

# TAB 2: EVALUASI
with tab2:
    st.header("Performa Model (Random Forest)")
    st.caption("Evaluasi menggunakan 20% data testing.")

    st.metric(label="Akurasi Model", value=f"{metrics['accuracy'] * 100:.2f}%")
    
    st.subheader("Confusion Matrix")
    fig, ax = plt.subplots(figsize=(6, 4))
    cm_display = ConfusionMatrixDisplay(confusion_matrix=metrics['confusion_matrix'], display_labels=metrics['class_names'])
    cm_display.plot(cmap='Blues', ax=ax, values_format='d')
    ax.grid(False)
    st.pyplot(fig)

# TAB 3: INFO DATASET (Baru)
with tab3:
    render_dataset_info()
    