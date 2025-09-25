import streamlit as st
import pandas as pd

from src.validate import basic_checks
from src.transform import normalize_columns, to_silver
from src.ingest import tag_lineage, concat_bronze

st.title("🚀 Laboratorio: De CSVs heterogéneos a un almacén analítico")

# 1. Subida de archivos
uploaded_files = st.file_uploader(
    "Sube tus CSVs aquí", 
    type=["csv"], 
    accept_multiple_files=True
)

# 2. Inputs en la barra lateral
st.sidebar.header("Mapeo de columnas origen → canónico")
date_col = st.sidebar.text_input("Columna para fecha (ej: fecha, date_time, Fecha)", "fecha")
partner_col = st.sidebar.text_input("Columna para partner (ej: cliente, partner_name, Partner)", "cliente")
amount_col = st.sidebar.text_input("Columna para importe (ej: importe, sales, Importe)", "importe")

mapping = {
    date_col: "date",
    partner_col: "partner",
    amount_col: "amount"
}

bronze_frames = []

if uploaded_files:
    for file in uploaded_files:
        try:
            df = pd.read_csv(file, encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(file, encoding="latin-1")

        # Normalizar columnas
        df = normalize_columns(df, mapping)

        # Añadir linaje
        df = tag_lineage(df, file.name)

        bronze_frames.append(df)

    # Concatenar a Bronze
    bronze = concat_bronze(bronze_frames)

    st.subheader("📊 Datos Bronze (unificados)")
    st.dataframe(bronze)

    # Validaciones
    errors = basic_checks(bronze)
    if errors:
        st.error("❌ Errores encontrados en las validaciones:")
        for e in errors:
            st.write("-", e)
    else:
        st.success("✅ Validaciones OK")

        # Derivar a Silver
        silver = to_silver(bronze)

        st.subheader("🥈 Datos Silver (agregados partner × mes)")
        st.dataframe(silver)

        # KPI simples
        st.metric("Total Amount", f"€ {silver['amount'].sum():,.2f}")
        st.bar_chart(silver, x="month", y="amount")

        # Descargas
        st.download_button(
            "⬇ Descargar Bronze CSV",
            bronze.to_csv(index=False).encode("utf-8"),
            "bronze.csv",
            "text/csv"
        )
        st.download_button(
            "⬇ Descargar Silver CSV",
            silver.to_csv(index=False).encode("utf-8"),
            "silver.csv",
            "text/csv"
        )
else:
    st.info("Sube al menos un archivo CSV para empezar 🚀")
