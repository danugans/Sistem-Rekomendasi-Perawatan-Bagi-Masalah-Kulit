import streamlit as st
import pandas as pd
from cbr import CBRSystem
from utils import load_dataset, append_case, normalize_age

DATA_PATH = "cases.csv"

# Load dataset
df = load_dataset(DATA_PATH)
cbr = CBRSystem(df)

st.sidebar.header("Masukkan Data Kasus Baru")
age = st.sidebar.number_input("Usia", min_value=0, max_value=120, value=25)
gender = st.sidebar.selectbox("Jenis Kelamin", options=["male", "female", "other"])
skin_type = st.sidebar.selectbox("Tipe Kulit", options=["oily", "dry", "combination", "sensitive", "normal"])

st.sidebar.write("Gejala (centang jika ada):")
acne = st.sidebar.checkbox("Acne (Jerawat)")
blackheads = st.sidebar.checkbox("Blackheads / Komedo")
dryness = st.sidebar.checkbox("Kekeringan")
redness = st.sidebar.checkbox("Kemerahan")
dark_spots = st.sidebar.checkbox("Noda Gelap / Dark spots")
aging = st.sidebar.checkbox("Tanda Penuaan")

# -----------------------
# Dapatkan Rekomendasi
# -----------------------
if st.sidebar.button("Dapatkan Rekomendasi"):
    query = {
        "age": normalize_age(age),
        "gender": gender,
        "skin_type": skin_type,
        "acne": int(acne),
        "blackheads": int(blackheads),
        "dryness": int(dryness),
        "redness": int(redness),
        "dark_spots": int(dark_spots),
        "aging": int(aging),
    }

    # Retrieve
    neighbors = cbr.retrieve(query, k=3)
    st.subheader("Kasus Mirip (Retrieve)")
    for idx, (case, dist) in enumerate(neighbors):
        st.markdown(f"**Kasus {case['id']} — jarak: {dist:.3f}**")
        st.write(pd.json_normalize(case).T)

    # Reuse
    best_case = neighbors[0][0]
    recommended = cbr.reuse(best_case)
    st.subheader("Rekomendasi Awal (Reuse)")
    st.write(recommended)

    # Revise
    st.subheader("Revise — Sunting Rekomendasi jika perlu")
    revised = st.text_area(
        "Edit rekomendasi perawatan (ver. final):",
        value=recommended,
        height=200
    )

    # Retain
    if st.button("Simpan ke Kasus (Retain)"):
        new_case = {
            "age": age,
            "gender": gender,
            "skin_type": skin_type,
            "acne": acne,
            "blackheads": blackheads,
            "dryness": dryness,
            "redness": redness,
            "dark_spots": dark_spots,
            "aging": aging,
            "solution": solution
        }

        cbr.retain(new_case)
        st.success("Kasus baru berhasil disimpan!")


st.sidebar.markdown("---")
st.sidebar.write("Dataset saat ini: %d kasus" % len(df))

# Optional debug dataset viewer
if st.checkbox("Tampilkan dataset (debug)"):
    st.dataframe(df)
