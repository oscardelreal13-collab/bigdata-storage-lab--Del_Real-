# 🛡️ Gobernanza de Datos

Este documento establece los principios y prácticas para garantizar la **calidad**, **seguridad** y **trazabilidad** de los datos dentro del laboratorio.

---

## 1. Origen y Linaje
- Cada archivo CSV debe registrarse con:
  - Fuente (origen del dataset).
  - Fecha de ingesta.
  - Transformaciones aplicadas (Bronze → Silver → Gold).
- Se recomienda mantener metadatos en logs o tablas auxiliares.

---

## 2. Validaciones Mínimas
- Formato de fecha válido (`YYYY-MM-DD`).
- Campos obligatorios no nulos (`date`, `partner`, `amount`).
- `amount` debe ser numérico (float) y en EUR.
- Eliminación de duplicados.
- Verificación de rangos lógicos (ejemplo: `amount > 0`).

---

## 3. Política de Mínimos Privilegios
- Acceso **sólo** a las capas necesarias:
  - *Raw*: acceso restringido a roles técnicos.
  - *Bronze/Silver*: acceso a Data Engineers y Data Analysts.
  - *Gold*: acceso general para análisis y reporting.
- No almacenar credenciales en el repositorio.
- Uso de `.gitignore` para excluir información sensible.

---

## 4. Trazabilidad
- Cada dataset debe poder rastrearse desde **origen** hasta **capa Gold**.
- Mantener identificadores únicos por archivo (ej. hash o checksum).
- Documentar reglas de transformación en `src/` y en `docs/`.

---

## 5. Roles y Responsabilidades
- **Data Engineer**: diseña pipelines de ingesta, validación y transformación.  
- **Data Analyst**: consulta datos en capas Silver/Gold, construye KPIs.  
- **Data Steward**: vela por la calidad, gobernanza y cumplimiento de políticas.  
- **Administrador del Repositorio**: gestiona permisos y revisa PRs.  
