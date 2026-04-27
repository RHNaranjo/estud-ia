# =============================================================================
# Estud-IA — Agente Analizador de Calificaciones
# =============================================================================
"""
GradesAnalyzerAgent: Agente de Google ADK que interpreta tendencias
en las calificaciones por materia.

Recibe un GradesSummary (sin datos personales) y genera un análisis
narrativo de las tendencias observadas entre Parcial 1 y Parcial 2.
"""

from google.adk.agents import Agent

GRADES_ANALYZER_PROMPT = """Eres un analista educativo experto. Tu trabajo es interpretar
datos estadísticos de calificaciones de una materia universitaria y generar
un análisis claro y objetivo de las tendencias.

REGLAS ESTRICTAS:
- Nunca menciones nombres de estudiantes individuales.
- Enfócate en tendencias del GRUPO, no en casos individuales.
- Sé objetivo: reporta tanto lo positivo como las áreas de oportunidad.
- Usa un tono profesional y neutral.
- Si la materia tiene calificaciones naturalmente bajas, menciónalo como
  contexto (ej. materias de ciencias exactas tienden a promedios más bajos).

FORMATO DE RESPUESTA:
Genera un análisis breve (máximo 300 palabras) que cubra:
1. **Tendencia General:** ¿Mejoró o bajó el promedio del P1 al P2?
2. **Componentes:** ¿Cuál componente (Tareas, Actividades, Proyecto, Examen) 
   es el más bajo? ¿Qué podría indicar esto?
3. **Dispersión:** ¿Hay mucha variabilidad entre estudiantes? (desviación estándar)
4. **Tasa de Reprobación:** ¿Cómo evolucionó del P1 al P2?
5. **Observaciones Clave:** Cualquier patrón notable.

DATOS A ANALIZAR:
{grades_data}
"""

grades_analyzer_agent = Agent(
    name="grades_analyzer",
    model="gemini-2.5-flash",
    description="Analiza tendencias en calificaciones por materia entre parciales.",
    instruction=GRADES_ANALYZER_PROMPT,
)


def format_grades_for_prompt(summary) -> str:
    """Formatea un GradesSummary como texto legible para el prompt del agente."""
    return f"""
Materia: {summary.materia}
Número de estudiantes: {summary.num_estudiantes}

PARCIAL 1:
  - Promedio general: {summary.promedio_p1}
  - Desviación estándar: {summary.desviacion_p1}
  - Tasa de reprobación: {summary.tasa_reprobacion_p1}%
  - Componente más bajo: {summary.componente_mas_bajo_p1}
  - Promedios por componente: {summary.promedios_componentes_p1}

PARCIAL 2:
  - Promedio general: {summary.promedio_p2}
  - Desviación estándar: {summary.desviacion_p2}
  - Tasa de reprobación: {summary.tasa_reprobacion_p2}%
  - Componente más bajo: {summary.componente_mas_bajo_p2}
  - Promedios por componente: {summary.promedios_componentes_p2}

CAMBIO (P2 - P1): {summary.delta:+.2f} puntos
"""
