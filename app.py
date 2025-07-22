import streamlit as st
import pandas as pd

st.image("logo.svg", width=300)
st.set_page_config(page_title="3D Part Finder", layout="centered")

st.title("🔍 Procura peças com 1, 2 ou 3 Dimensões")

@st.cache_data
def load_data():
    return pd.read_excel("parts.xlsx")  # Make sure this file exists in GitHub

df = load_data()

st.markdown("Preencha alguma **1, 2 ou 3 dimensões** para encontrar as peças em falta:")


dim1 = st.number_input("Dimensão 1", min_value=0.0, step=0.1, format="%.2f")
dim2 = st.number_input("Dimensão 2 (opcional)", min_value=0.0, step=0.1, format="%.2f")
tolerance = st.slider("Tolerância (± mm)", min_value=0.0, max_value=5.0, value=0.5)

# Dimension columns to search
dim_cols = ["Dimension1", "Dimension2", "Dimension3"]

def within_tolerance(value, target):
    return abs(value - target) <= tolerance
    
if st.button("🔍 Procurar peças correspondentes"):
    results = []

    for _, row in df.iterrows():
        values = [row[col] for col in dim_cols]
        matched_indices = []

        # Try to match dim1
        dim1_match = None
        for i, v in enumerate(values):
            if within_tolerance(v, dim1):
                dim1_match = i
                matched_indices.append(i)
                break

        # Try to match dim2 in a different column
        dim2_match = None
        if dim2 > 0:
            for i, v in enumerate(values):
                if i not in matched_indices and within_tolerance(v, dim2):
                    dim2_match = i
                    matched_indices.append(i)
                    break

        # If dim2 was not filled, only check dim1
        if dim1 > 0 and dim2 == 0 and dim1_match is not None:
            results.append(row)
        elif dim1 > 0 and dim2 > 0 and dim1_match is not None and dim2_match is not None:
            results.append(row)

    if results:
        result_df = pd.DataFrame(results)
        st.write("Columns in result dataframe:", result_df.columns.tolist())  # Debugging line
    
        display_cols = [col for col in ["Reference", "Sub-Obra", "Descrição", "Quantidade", "Peso unitário", "Dimension1", "Dimension2", "Dimension3"] if col in result_df.columns]
        
        st.success(f"✅ Encontrei {len(result_df)} peça(s) correspondente(s):")
        st.dataframe(result_df[display_cols])
    else:
        st.warning("❌ Nenhuma peça encontrada. Tente ajustar a tolerância.")
    

    

