import streamlit as st

# Imports correctos (usan la carpeta src)
from src.validate import basic_checks
from src.transform import normalize_columns, to_silver
from src.ingest import tag_lineage, concat_bronze

# Aquí sigue tu código Streamlit...
st.title("Mi app con Streamlit")

# Ejemplo de uso (puedes cambiarlo según tu lógica):
st.write("Validando datos...")
basic_checks()

st.write("Normalizando columnas...")
normalize_columns()

st.write("Transformando a silver layer...")
to_silver()

st.write("Ingestando datos...")
concat_bronze()
tag_lineage()
