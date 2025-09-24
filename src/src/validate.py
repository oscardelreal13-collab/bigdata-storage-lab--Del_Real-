import pandas as pd
from typing import List

def basic_checks(df: pd.DataFrame) -> List[str]:
    """
    Ejecuta validaciones mínimas sobre un DataFrame canónico.
    Devuelve lista de errores encontrados.
    """
    errors = []
    required_cols = ["date", "partner", "amount"]

    # Verificar columnas presentes
    for col in required_cols:
        if col not in df.columns:
            errors.append(f"Columna faltante: {col}")

    # Validar date como datetime
    if "date" in df.columns:
        if not pd.api.types.is_datetime64_any_dtype(df["date"]):
            errors.append("Columna 'date' no es datetime")

    # Validar amount numérico y >= 0
    if "amount" in df.columns:
        if not pd.api.types.is_numeric_dtype(df["amount"]):
            errors.append("Columna 'amount' no es numérica")
        elif (df["amount"] < 0).any():
            errors.append("Valores negativos en 'amount'")

    return errors
