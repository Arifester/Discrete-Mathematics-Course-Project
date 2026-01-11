import pandas as pd
import streamlit as st
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

@st.cache_resource
def load_and_train_model():
    url = "https://raw.githubusercontent.com/Arifester/Datasets/refs/heads/main/heart.csv"
    try:
        df = pd.read_csv(url)
    except Exception as e:
        st.error(f"Gagal memuat dataset: {e}")
        return None, None, None, None

    X = df.drop(columns=['target'])
    Y = df['target']

    # FIX DATA LEAKAGE: Split dulu, baru Scale
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    scaler = MinMaxScaler()
    X_train = scaler.fit_transform(X_train_raw)
    X_test = scaler.transform(X_test_raw)

    # Batasi max_depth agar tidak overfitting
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    
    # Hitung akurasi untuk evaluasi
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    
    metrics = {
        "accuracy": accuracy,
        "confusion_matrix": cm,
        "class_names": ["Sehat", "Sakit Jantung"]
    }

    return model, scaler, X.columns, metrics

def predict_single_input(model, scaler, input_data, columns):
    data_baru_df = pd.DataFrame([input_data], columns=columns)
    data_baru_scaled = scaler.transform(data_baru_df)
    
    prediction = model.predict(data_baru_scaled)
    probability = model.predict_proba(data_baru_scaled)
    
    return prediction[0], probability[0]
    