import streamlit as st
import pandas as pd


st.title("EDA🔝")


file = st.file_uploader("Sube un archivo .xlsx", type=["xlsx"])


if file is not None:

    df = pd.read_excel(file)
    st.write("Datos del archivo:")
    st.dataframe(df)

    


