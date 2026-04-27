# =============================================================================
# Estud-IA — Agente de Sanitización de Datos
# =============================================================================
"""
DataSanitizationAgent: Primer agente en la cadena.

Responsabilidades:
  1. Eliminar nombres de estudiantes de los datos de calificaciones.
  2. Aplicar filtros de PII a los comentarios.
  3. Filtrar comentarios tóxicos o con ataques personales.
  4. Generar resúmenes estadísticos por materia (sin datos personales).

Este agente NO usa el LLM — opera con lógica determinista para garantizar
que la sanitización sea predecible y auditable.
"""

import pandas as pd
from collections import defaultdict
from models import GradesRecord, FeedbackRecord, GradesSummary, FeedbackSummary
from utils.ethics_filters import sanitize_comments


def sanitize_grades(records: list[GradesRecord]) -> list[GradesSummary]:
    """
    Transforma registros individuales de calificaciones en resúmenes
    estadísticos por materia, eliminando toda información personal.

    Args:
        records: Lista de GradesRecord con nombres de estudiantes.

    Returns:
        Lista de GradesSummary sin datos personales, uno por materia.
    """
    # Agrupar por materia
    by_subject: dict[str, dict[str, list[GradesRecord]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for r in records:
        by_subject[r.materia][r.parcial].append(r)

    summaries = []
    for materia, parciales in by_subject.items():
        p1_records = parciales.get("Parcial 1", [])
        p2_records = parciales.get("Parcial 2", [])

        if not p1_records or not p2_records:
            continue

        # Calcular estadísticas por parcial
        def stats(recs):
            promedios = [r.promedio for r in recs]
            n = len(promedios)
            mean = sum(promedios) / n if n else 0
            variance = sum((x - mean) ** 2 for x in promedios) / n if n else 0
            std = variance ** 0.5
            reprobados = sum(1 for x in promedios if x < 70) / n * 100 if n else 0

            # Promedios por componente
            comp = {
                "Tareas": sum(r.tareas for r in recs) / n,
                "Actividades": sum(r.actividades for r in recs) / n,
                "Proyecto": sum(r.proyecto for r in recs) / n,
                "Examen": sum(r.examen for r in recs) / n,
            }
            peor = min(comp, key=comp.get)
            return mean, std, reprobados, comp, peor

        mean_p1, std_p1, rep_p1, comp_p1, peor_p1 = stats(p1_records)
        mean_p2, std_p2, rep_p2, comp_p2, peor_p2 = stats(p2_records)

        summaries.append(GradesSummary(
            materia=materia,
            num_estudiantes=len(p1_records),
            promedio_p1=round(mean_p1, 2),
            promedio_p2=round(mean_p2, 2),
            delta=round(mean_p2 - mean_p1, 2),
            desviacion_p1=round(std_p1, 2),
            desviacion_p2=round(std_p2, 2),
            tasa_reprobacion_p1=round(rep_p1, 1),
            tasa_reprobacion_p2=round(rep_p2, 1),
            componente_mas_bajo_p1=peor_p1,
            componente_mas_bajo_p2=peor_p2,
            promedios_componentes_p1={k: round(v, 2) for k, v in comp_p1.items()},
            promedios_componentes_p2={k: round(v, 2) for k, v in comp_p2.items()},
        ))

    return summaries


def sanitize_feedback(records: list[FeedbackRecord]) -> list[FeedbackSummary]:
    """
    Agrupa evaluaciones por materia, elimina PII y filtra toxicidad.

    Args:
        records: Lista de FeedbackRecord sin procesar.

    Returns:
        Lista de FeedbackSummary con comentarios limpios, uno por materia.
    """
    by_subject: dict[str, list[FeedbackRecord]] = defaultdict(list)
    for r in records:
        by_subject[r.materia].append(r)

    summaries = []
    for materia, feedbacks in by_subject.items():
        # Distribución de satisfacción
        dist = {i: 0 for i in range(1, 6)}
        for f in feedbacks:
            if 1 <= f.satisfaccion <= 5:
                dist[f.satisfaccion] += 1

        # Sanitizar comentarios
        raw_comments = [f.comentario for f in feedbacks]
        clean_comments = sanitize_comments(raw_comments)

        sat_values = [f.satisfaccion for f in feedbacks]
        avg_sat = sum(sat_values) / len(sat_values) if sat_values else 0

        summaries.append(FeedbackSummary(
            materia=materia,
            num_evaluaciones=len(feedbacks),
            satisfaccion_promedio=round(avg_sat, 2),
            distribucion_satisfaccion=dist,
            comentarios_limpios=clean_comments,
        ))

    return summaries
