import pandas as pd
from typing import List
from datetime import datetime, timezone

def tag_lineage(df: pd.DataFrame, source_name: str) -> pd.DataFrame:
    """
    Añade metadatos de linaje:
    - source_file: nombre del archivo de origen.
    - ingested_at: timestamp UTC ISO 8601.
    """
    df = df.copy()
    df["source_file"] = source_name
    df["ingested_at"] = datetime.now(timezone.utc).isoformat()
    return df


def concat_bronze(frames: List[pd.DataFrame]) -> pd.DataFrame:
    """
    Concatena múltiples DataFrames asegurando el esquema Bronze.
    Esquema esperado: date, partner, amount, source_file, ingested_at
    """
    bronze = pd.concat(frames, ignore_index=True)

    expected = ["date", "partner", "amount", "source_file", "ingested_at"]
    missing = [col for col in expected if col not in bronze.columns]
    if missing:
        raise ValueError(f"Columnas faltantes en Bronze: {missing}")

    return bronze[expected]
