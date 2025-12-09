import streamlit as st
import pandas as pd
from cbr import CBRSystem
from utils import normalize_age, load_dataset, append_case


# Path to dataset (same folder)
DATA_PATH = "cases.csv"


st.set_page_config(page_title="CBR Skin Recommendation", layout="centered")
st.title("CBR — Sistem Rekomendasi Perawatan Kulit")
st.write("Retrieve → Reuse → Revise → Retain — sistem rekomendasi perawatan kulit berbasis kasus.")


# Load dataset
df = load_dataset(DATA_PATH)
cbr = CBRSystem(df)


st.sidebar.header("Masukkan Data Kasus Baru")
age = st.sidebar.number_input("Usia", min_value=0, max_value=120, value=25)
gender = st.sidebar.selectbox("Jenis Kelamin", options=["male","female","other"])
skin_type = st.sidebar.selectbox("Tipe Kulit", options=["oily","dry","combination","sensitive","normal"])


st.sidebar.write("Gejala (centang jika ada):")
acne = st.sidebar.checkbox("Acne (Jerawat)")
blackheads = st.sidebar.checkbox("Blackheads / Komedo")
dryness = st.sidebar.checkbox("Kekeringan")
redness = st.sidebar.checkbox("Kemerahan")
dark_spots = st.sidebar.checkbox("Noda Gelap / Dark spots")
aging = st.sidebar.checkbox("Tanda Penuaan")


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


# Reuse (recommend solution from best match)
best_case = neighbors[0][0]
recommended = cbr.reuse(best_case)
st.subheader("Rekomendasi Awal (Reuse)")
st.write(recommended)


st.subheader("Revise — Sunting Rekomendasi jika perlu")
revised = st.text_area("Edit rekomendasi perawatan (ver. final):", value=recommended, height=200)


if st.button("Simpan ke Kasus (Retain)"):
new_case = {
"id": cbr.next_id(),
st.dataframe(df)
