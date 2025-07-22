import streamlit as st
import pandas as pd

st.image("logo.svg", width=200)
st.set_page_config(page_title="3D Part Finder", layout="centered")

st.title("🔍 Procura peças com 1, 2 ou 3 Dimensões")

@st.cache_data
def load_data():
    return pd.read_excel("parts.xlsx")  # Make sure this file exists in GitHub

df = load_data()

st.markdown("Enter any **1, 2 or 3 dimensions** to find matching parts:")

dim1 = st.number_input("Dimensão 1 (coloca 0 se desconhecida)", min_value=0.0, step=0.1, format="%.2f")
dim2 = st.number_input("Dimensão 2 (coloca 0 se desconhecida)", min_value=0.0, step=0.1, format="%.2f")
dim3 = st.number_input("Dimensão 3 (coloca 0 se desconhecida)", min_value=0.0, step=0.1, format="%.2f")

tolerance = st.slider("Tolerância (± mm)", min_value=0.0, max_value=5.0, value=0.5)

if st.button("🔍 Procurar peças correspondentes"):
    query = pd.Series([True] * len(df))  # Start with all rows

    if dim1 > 0:
        query &= df["Dimension1"].between(dim1 - tolerance, dim1 + tolerance)
    if dim2 > 0:
        query &= df["Dimension2"].between(dim2 - tolerance, dim2 + tolerance)
    if dim3 > 0:
        query &= df["Dimension3"].between(dim3 - tolerance, dim3 + tolerance)

    matches = df[query]

    if not matches.empty:
        st.success(f"✅ Encontrei {len(matches)} peça(s) correspondente(s):")
        st.dataframe(matches)
    else:
        st.warning("❌ Nenhuma peça encontrada. Tente ajustar a tolerância.")

