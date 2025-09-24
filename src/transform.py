import pandas as pd
from typing import Dict

def normalize_columns(df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
    """
    Normaliza columnas de un DataFrame a esquema canónico:
    - Renombra columnas según mapping (origen -> canónico).
    - Parsea fechas a datetime (ISO).
    - Limpia partner (espacios).
    - Normaliza amount: elimina € y convierte comas decimales.
    """
    # Renombrar columnas
    df = df.rename(columns=mapping)

    # Asegurar columnas esperadas
    expected = ["date", "partner", "amount"]
    for col in expected:
        if col not in df.columns:
            raise ValueError(f"Columna requerida no encontrada: {col}")

    # Normalizar fecha
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date

    # Normalizar partner
    df["partner"] = df["partner"].astype(str).str.strip()

    # Normalizar amount
    df["amount"] = (
        df["amount"]
        .astype(str)
        .str.replace("€", "", regex=False)
        .str.replace(",", ".", regex=False)
    )
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    return df[expected]


def to_silver(bronze: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega los datos bronze en nivel Silver:
    - Suma amount por partner y mes.
    - Devuelve columna 'month' como timestamp (primer día del mes).
    """
    df = bronze.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()

    silver = (
        df.groupby(["partner", "month"], as_index=False)
        .agg({"amount": "sum"})
        .sort_values(["partner", "month"])
    )
    return silver
