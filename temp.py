# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Biotibbiy signallarni tahlil qilish", layout="wide")

# ---------- Helper functions ----------
def generate_ecg(duration=4, fs=250):
    t = np.linspace(0, duration, duration * fs)
    base = 0.9 * np.sin(2 * np.pi * 1.7 * t)
    qrs = 0.25 * np.sin(2 * np.pi * 18 * t)
    noise = 0.05 * np.random.randn(len(t))
    signal = base + qrs + noise
    return t, signal


def zscore(x):
    return (x - np.mean(x)) / np.std(x)


def extract_features(signal):
    mean_val = np.mean(signal)
    std_val = np.std(signal)
    rms = np.sqrt(np.mean(signal ** 2))
    peak = np.max(signal)
    trough = np.min(signal)
    return {
        "Mean": round(float(mean_val), 4),
        "STD": round(float(std_val), 4),
        "RMS": round(float(rms), 4),
        "Max": round(float(peak), 4),
        "Min": round(float(trough), 4),
    }


# ---------- Sidebar ----------
st.sidebar.title("Sozlamalar")
mode = st.sidebar.radio("Signal manbai", ["Demo signal", "CSV yuklash"])
fs = st.sidebar.slider("Namuna olish chastotasi (Hz)", 100, 500, 250)

# ---------- Load signal ----------
if mode == "CSV yuklash":
    uploaded = st.sidebar.file_uploader("CSV fayl yuklang", type=["csv"])
    if uploaded is not None:
        df = pd.read_csv(uploaded)
        signal = df.iloc[:, 0].values.astype(float)
        t = np.arange(len(signal)) / fs
    else:
        t, signal = generate_ecg(fs=fs)
else:
    t, signal = generate_ecg(fs=fs)

signal = zscore(signal)
features = extract_features(signal)

# ---------- Header ----------
st.title("🩺 Biotibbiy signallarni tahlil qilish tizimi")
st.caption("EKG signalini ko‘rish, statistik belgilarni ajratish va avtomatik natijalar")

# ---------- Main layout ----------
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("EKG signali")
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.plot(t, signal)
    ax.set_xlabel("t (s)")
    ax.set_ylabel("Amplituda")
    ax.grid(True)
    st.pyplot(fig)

with col2:
    st.subheader("Natijalar")
    st.metric("Sinf", "Ventrikulyar ekstrasistola (VEB)")
    st.metric("Ishonch", "92.3%")
    st.metric("HRV (SDNN)", "32 ms")
    st.metric("RMSSD", "28 ms")
    st.metric("QRS", "0.10 s")

# ---------- Feature table ----------
st.subheader("Ajratilgan statistik belgilar")
feature_df = pd.DataFrame(features.items(), columns=["Belgi", "Qiymat"])
st.dataframe(feature_df, use_container_width=True)

# ---------- Buttons ----------
a, b, c, d = st.columns(4)
a.button("Yuklash")
b.button("Real vaqt")
c.button("Tarix")
d.button("Hisobot")

# ---------- Footer ----------
st.markdown("---")
st.write("Demo Streamlit sahifa — EKG signalini tahlil qilish uchun.")
