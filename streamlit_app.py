import streamlit as st
import pandas as pd
from io import BytesIO

from src.transform import normalize_columns, to_silver
from src.validate import basic_checks
from src.ingest import tag_lineage, concat_bronze


st.set_page_config(page_title="Big Data Storage Lab", layout="wide")
st.title("📊 Big Data Storage Lab - Bronze → Silver")

# --- Barra lateral ---
st.sidebar.header("Configuración de columnas origen")
col_date = st.sidebar.text_input("Columna origen para 'date'", value="fecha")
col_partner = st.sidebar.text_input("Columna origen para 'partner'", value="cliente")
col_amount = st.sidebar.text_input("Columna origen para 'amount'", value="importe")

mapping = {
    col_date: "date",
    col_partner: "partner",
    col_amount: "amount",
}

st.sidebar.write("---")
uploaded_files = st.sidebar.file_uploader(
    "Subir uno o varios CSV", type="csv", accept_multiple_files=True
)

# --- Procesamiento ---
bronze_frames = []
if uploaded_files:
    for file in uploaded_files:
        try:
            # Intentar leer con UTF-8 y fallback a latin-1
            try:
                df = pd.read_csv(file)
            except UnicodeDecodeError:
                file.seek(0)
                df = pd.read_csv(file, encoding="latin-1")

            # Normalizar columnas
            df = normalize_columns(df, mapping)

            # Tag lineage
            df = tag_lineage(df, source_name=file.name)

            bronze_frames.append(df)

        except Exception as e:
            st.error(f"❌ Error procesando {file.name}: {e}")

    if bronze_frames:
        bronze = concat_bronze(bronze_frames)
        st.subheader("📂 Datos Bronze Unificados")
        st.dataframe(bronze.head(20), use_container_width=True)

        # Validaciones
        st.subheader("🔍 Validaciones Básicas")
        errors = basic_checks(bronze)
        if errors:
            st.error("Errores detectados:")
            for err in errors:
                st.write(f"- {err}")
        else:
            st.success("✅ Validaciones correctas. Datos listos para Silver.")

            # Derivar Silver
            silver = to_silver(bronze)
            st.subheader("💎 Datos Silver (Partner × Mes)")
            st.dataframe(silver, use_container_width=True)

            # KPIs simples
            st.subheader("📈 KPIs Simples")
            total_amount = silver["amount"].sum()
            n_partners = silver["partner"].nunique()
            n_months = silver["month"].nunique()

            kpi1, kpi2, kpi3 = st.columns(3)
            kpi1.metric("Total Amount (EUR)", f"{total_amount:,.2f}")
            kpi2.metric("N° de Partners", n_partners)
            kpi3.metric("N° de Meses", n_months)

            # Gráfico
            st.subheader("📊 Evolución Mensual (Amount EUR)")
            chart_data = silver.groupby("month", as_index=False).agg({"amount": "sum"})
            st.bar_chart(chart_data.set_index("month"))

            # Botones descarga
            st.subheader("💾 Descargas")
            def to_csv_download(df: pd.DataFrame) -> BytesIO:
                buf = BytesIO()
                df.to_csv(buf, index=False)
                buf.seek(0)
                return buf

            bronze_csv = to_csv_download(bronze)
            silver_csv = to_csv_download(silver)

            st.download_button(
                label="⬇️ Descargar Bronze CSV",
                data=bronze_csv,
                file_name="bronze.csv",
                mime="text/csv",
            )

            st.download_button(
                label="⬇️ Descargar Silver CSV",
                data=silver_csv,
                file_name="silver.csv",
                mime="text/csv",
            )
