# =============================================================================
# Estud-IA — Modelos de Datos
# =============================================================================
"""
Estructuras de datos (dataclasses) para representar la información procesada
de calificaciones, evaluaciones y reportes generados.
"""

from dataclasses import dataclass, field


@dataclass
class GradesRecord:
    """Registro individual de calificaciones de un estudiante en una materia."""
    estudiante: str
    materia: str
    parcial: str
    tareas: float
    actividades: float
    proyecto: float
    examen: float
    promedio: float


@dataclass
class GradesSummary:
    """Resumen estadístico de calificaciones por materia (ya sin nombres)."""
    materia: str
    num_estudiantes: int
    promedio_p1: float
    promedio_p2: float
    delta: float              # Cambio entre P1 y P2 (positivo = mejora)
    desviacion_p1: float
    desviacion_p2: float
    tasa_reprobacion_p1: float   # Porcentaje de alumnos < 70
    tasa_reprobacion_p2: float
    componente_mas_bajo_p1: str  # Ej: "Examen", "Tareas", etc.
    componente_mas_bajo_p2: str
    promedios_componentes_p1: dict = field(default_factory=dict)
    promedios_componentes_p2: dict = field(default_factory=dict)


@dataclass
class FeedbackRecord:
    """Registro individual de evaluación anónima."""
    materia: str
    satisfaccion: int         # 1 a 5
    comentario: str


@dataclass
class FeedbackSummary:
    """Resumen de evaluaciones por materia."""
    materia: str
    num_evaluaciones: int
    satisfaccion_promedio: float
    distribucion_satisfaccion: dict  # {1: n, 2: n, 3: n, 4: n, 5: n}
    comentarios_limpios: list       # Comentarios ya sanitizados


@dataclass
class TeacherReport:
    """Reporte final generado para el profesor de una materia."""
    materia: str
    resumen_estadistico: str
    temas_clave: str
    recomendaciones: str
    disclaimer: str = (
        "⚠️ Este reporte fue generado por inteligencia artificial a partir "
        "de datos limitados. Debe ser interpretado como una herramienta de "
        "apoyo, no como una evaluación definitiva del desempeño docente."
    )
