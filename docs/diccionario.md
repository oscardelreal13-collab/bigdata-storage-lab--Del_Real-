# 📘 Diccionario de Datos - Esquema Canónico

Este documento define el **esquema canónico** al que deberán transformarse los datos.

## Esquema Canónico

| Campo   | Descripción                               | Tipo   | Formato/Unidad | Ejemplo        |
|---------|-------------------------------------------|--------|----------------|----------------|
| date    | Fecha de la transacción                   | string | YYYY-MM-DD     | 2025-09-24     |
| partner | Identificador o nombre del socio/cliente  | string | texto libre    | "ACME Corp"    |
| amount  | Monto de la transacción                   | float  | EUR            | 1234.56        |

---

## Mapeos Origen → Canónico

| Origen (campo)    | Canónico (campo) | Transformación / Nota                          |
|-------------------|------------------|-----------------------------------------------|
| `fecha`           | `date`           | Convertir a formato `YYYY-MM-DD`              |
| `transaction_dt`  | `date`           | Normalizar a ISO date                         |
| `cliente`         | `partner`        | Copiar como string                            |
| `partner_id`      | `partner`        | Usar ID como string                           |
| `importe`         | `amount`         | Convertir a float (moneda EUR)                |
| `value_in_euros`  | `amount`         | Asegurar decimales con punto (`.`)            |
