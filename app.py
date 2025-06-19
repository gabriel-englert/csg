# app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Avisos de Rodovias - CSG", layout="wide")

st.title("📍 Avisos de Rodovias - CSG")
st.write("Última atualização automática às 8h da manhã.")

try:
    df = pd.read_csv("data/avisos.csv")
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Baixar CSV", data=csv, file_name="avisos_csg.csv", mime="text/csv")
except FileNotFoundError:
    st.error("CSV ainda não gerado. Aguarde o scraping agendado.")
