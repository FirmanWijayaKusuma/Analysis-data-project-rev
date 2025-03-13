import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset yang sudah diproses
df_day = pd.read_csv("dashboard/day_processed.csv", parse_dates=["dteday"])
df_hour = pd.read_csv("dashboard/hour_processed.csv")

# Pastikan dteday dalam format datetime
df_day["dteday"] = pd.to_datetime(df_day["dteday"])

# **Pastikan kolom "season" berisi angka, bukan teks**
season_mapping = {"Spring": 1, "Summer": 2, "Fall": 3, "Winter": 4}
if df_day["season"].dtype == "object":
    df_day["season"] = df_day["season"].map(season_mapping)

# Sidebar untuk navigasi
st.sidebar.title("Dashboard Bike Sharing Firman Wijaya Kusuma")
menu = st.sidebar.radio("Pilih Analisis", ["Overview", "Tren Bulanan & Musiman", "Pengaruh Cuaca", "Waktu Sibuk", "Tipe Pengguna"])

# **Fitur Interaktif: Filter Tanggal**
min_date = df_day["dteday"].min()
max_date = df_day["dteday"].max()

selected_date = st.sidebar.slider(
    "Pilih Rentang Tanggal",
    min_value=min_date.date(), 
    max_value=max_date.date(),
    value=(min_date.date(), max_date.date())
)

# Filter dataset berdasarkan tanggal
df_filtered = df_day[
    (df_day["dteday"].dt.date >= selected_date[0]) & (df_day["dteday"].dt.date <= selected_date[1])
]

# **1. Overview**
if menu == "Overview":
    st.title("Overview Dataset")
    st.write(df_filtered.head())

# **2. Tren Bulanan & Musiman**
elif menu == "Tren Bulanan & Musiman":
    st.title("Tren Peminjaman Sepeda per Bulan & Musim")
    
    # **Visualisasi Tren Bulanan**
    monthly_trend = df_filtered.groupby("mnth")["cnt"].mean()
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=monthly_trend.index, y=monthly_trend.values, palette="Blues", ax=ax)
    ax.set_title("Rata-rata Peminjaman Sepeda per Bulan")
    st.pyplot(fig)

    # **Pastikan kolom season berisi angka**
    df_filtered = df_filtered[df_filtered["season"].notna()]  # Hilangkan NaN jika ada
    df_filtered["season"] = df_filtered["season"].astype(int)

    # **Mapping Musim**
    season_labels = {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}

    # **Visualisasi Tren Musiman**
    season_trend = df_filtered.groupby("season")["cnt"].mean()
    
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=season_trend.index, y=season_trend.values, palette="coolwarm", ax=ax)
    ax.set_xticklabels([season_labels[i] for i in season_trend.index], rotation=30)
    ax.set_title("Rata-rata Peminjaman Sepeda per Musim")
    st.pyplot(fig)

# **3. Pengaruh Cuaca**
elif menu == "Pengaruh Cuaca":
    st.title("Pengaruh Cuaca terhadap Peminjaman Sepeda")

    weather_trend = df_filtered.groupby("weathersit")["cnt"].mean()
    
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=weather_trend.index, y=weather_trend.values, palette="viridis", ax=ax)
    ax.set_title("Rata-rata Peminjaman Sepeda berdasarkan Kondisi Cuaca")
    ax.set_xticklabels(["Cerah/Sedikit Berawan", "Mendung", "Hujan/Salju"])
    st.pyplot(fig)

# **4. Waktu Sibuk**
elif menu == "Waktu Sibuk":
    st.title("Tren Peminjaman Berdasarkan Waktu")

    hourly_trend = df_hour.groupby("hr")["cnt"].mean()
    
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.lineplot(x=hourly_trend.index, y=hourly_trend.values, marker="o", color="crimson", ax=ax)
    ax.set_title("Rata-rata Peminjaman Sepeda Berdasarkan Jam dalam Sehari")
    st.pyplot(fig)

# **5. Tipe Pengguna**
elif menu == "Tipe Pengguna":
    st.title("Perbandingan Pengguna Kasual vs. Terdaftar")

    user_type_trend = df_filtered[["casual", "registered"]].mean()
    
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=user_type_trend.index, y=user_type_trend.values, palette="Set2", ax=ax)
    ax.set_title("Perbandingan Pengguna Kasual vs. Terdaftar")
    st.pyplot(fig)
