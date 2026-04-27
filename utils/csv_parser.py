# =============================================================================
# Estud-IA — Parser de CSVs
# =============================================================================
"""
Módulo para leer y validar los archivos CSV de calificaciones y evaluaciones.
Adaptado a la estructura real de los datos de prueba.

Formato esperado — Calificaciones:
  Estudiante, Materia, Parcial, Tareas (20%), Actividades (10%),
  Proyecto (20%), Examen (50%), Promedio Parcial

Formato esperado — Evaluaciones:
  Estudiante, Materia, Satisfacción (1-5), Comentario
"""

import pandas as pd
from models import GradesRecord, FeedbackRecord


# Columnas requeridas para validación
REQUIRED_GRADES_COLS = {
    "Estudiante", "Materia", "Parcial",
    "Tareas (20%)", "Actividades (10%)",
    "Proyecto (20%)", "Examen (50%)", "Promedio Parcial"
}

REQUIRED_EVALS_COLS = {
    "Materia", "Satisfacción (1-5)", "Comentario"
}


def _normalize_decimal(value: str) -> float:
    """Convierte valores numéricos que usan coma como separador decimal."""
    if isinstance(value, str):
        return float(value.replace(",", "."))
    return float(value)


def parse_grades_csv(file_path_or_buffer) -> list[GradesRecord]:
    """
    Lee el CSV de calificaciones y retorna una lista de GradesRecord.

    Args:
        file_path_or_buffer: Ruta al archivo CSV o buffer de Streamlit.

    Returns:
        Lista de GradesRecord con los datos parseados.

    Raises:
        ValueError: Si faltan columnas requeridas o los datos son inválidos.
    """
    df = pd.read_csv(file_path_or_buffer, encoding="utf-8")
    df.columns = df.columns.str.strip()

    # Validar columnas
    missing = REQUIRED_GRADES_COLS - set(df.columns)
    if missing:
        raise ValueError(
            f"El CSV de calificaciones no contiene las columnas requeridas: "
            f"{', '.join(missing)}"
        )

    records = []
    for _, row in df.iterrows():
        records.append(GradesRecord(
            estudiante=str(row["Estudiante"]).strip(),
            materia=str(row["Materia"]).strip(),
            parcial=str(row["Parcial"]).strip(),
            tareas=_normalize_decimal(row["Tareas (20%)"]),
            actividades=_normalize_decimal(row["Actividades (10%)"]),
            proyecto=_normalize_decimal(row["Proyecto (20%)"]),
            examen=_normalize_decimal(row["Examen (50%)"]),
            promedio=_normalize_decimal(row["Promedio Parcial"]),
        ))

    if not records:
        raise ValueError("El CSV de calificaciones está vacío.")

    return records


def parse_evals_csv(file_path_or_buffer) -> list[FeedbackRecord]:
    """
    Lee el CSV de evaluaciones anónimas y retorna una lista de FeedbackRecord.

    Args:
        file_path_or_buffer: Ruta al archivo CSV o buffer de Streamlit.

    Returns:
        Lista de FeedbackRecord con los datos parseados.

    Raises:
        ValueError: Si faltan columnas requeridas o los datos son inválidos.
    """
    df = pd.read_csv(file_path_or_buffer, encoding="utf-8")
    df.columns = df.columns.str.strip()

    # Validar columnas
    missing = REQUIRED_EVALS_COLS - set(df.columns)
    if missing:
        raise ValueError(
            f"El CSV de evaluaciones no contiene las columnas requeridas: "
            f"{', '.join(missing)}"
        )

    records = []
    for _, row in df.iterrows():
        comentario = str(row["Comentario"]).strip()
        if comentario and comentario.lower() != "nan":
            records.append(FeedbackRecord(
                materia=str(row["Materia"]).strip(),
                satisfaccion=int(row["Satisfacción (1-5)"]),
                comentario=comentario,
            ))

    if not records:
        raise ValueError("El CSV de evaluaciones está vacío o no contiene comentarios.")

    return records
