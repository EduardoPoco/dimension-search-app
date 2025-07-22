import streamlit as st
import pandas as pd

st.set_page_config(page_title="3D Part Finder", layout="centered")

st.title("🔍 Part Finder by 1, 2 or 3 Dimensions")

@st.cache_data
def load_data():
    return pd.read_excel("parts.xlsx")  # Make sure this file exists in GitHub

df = load_data()

st.markdown("Enter any **1, 2 or 3 dimensions** to find matching parts:")

dim1 = st.number_input("Dimension 1 (leave 0 if unknown)", min_value=0.0, step=0.1, format="%.2f")
dim2 = st.number_input("Dimension 2 (leave 0 if unknown)", min_value=0.0, step=0.1, format="%.2f")
dim3 = st.number_input("Dimension 3 (leave 0 if unknown)", min_value=0.0, step=0.1, format="%.2f")

tolerance = st.slider("Tolerance (± mm)", min_value=0.0, max_value=5.0, value=0.5)

if st.button("🔍 Find Matching Parts"):
    query = pd.Series([True] * len(df))  # Start with all rows

    if dim1 > 0:
        query &= df["Dimension1"].between(dim1 - tolerance, dim1 + tolerance)
    if dim2 > 0:
        query &= df["Dimension2"].between(dim2 - tolerance, dim2 + tolerance)
    if dim3 > 0:
        query &= df["Dimension3"].between(dim3 - tolerance, dim3 + tolerance)

    matches = df[query]

    if not matches.empty:
        st.success(f"✅ Found {len(matches)} matching part(s):")
        st.dataframe(matches)
    else:
        st.warning("❌ No matching parts found. Try adjusting the dimensions or tolerance.")

