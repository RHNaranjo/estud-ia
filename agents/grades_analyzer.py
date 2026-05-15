# Agente Analizador de Calificaciones
from google.adk.agents import Agent

GRADES_ANALYZER_PROMPT = """Eres un analista educativo experto. Interpreta
datos estadísticos de calificaciones y genera un análisis de tendencias.

REGLAS ESTRICTAS:
- Nunca menciones nombres de estudiantes individuales.
- Enfócate en tendencias del GRUPO.
- Sé objetivo: reporta lo positivo y áreas de oportunidad.
- Usa un tono neutral.
- Si las calificaciones son naturalmente bajas, menciónalo como contexto.

FORMATO DE RESPUESTA (máximo 300 palabras):
1. Tendencia General: ¿Mejoró o bajó el promedio?
2. Componentes: ¿Cuál es el más bajo?
3. Dispersión: ¿Hay variabilidad entre estudiantes?
4. Tasa de Reprobación: ¿Cómo evolucionó?
5. Observaciones Clave.
"""

# Instancia del agente de calificaciones
grades_analyzer_agent = Agent(
    name="grades_analyzer",
    model="gemini-2.5-flash",
    description="Analiza tendencias de calificaciones.",
    instruction=GRADES_ANALYZER_PROMPT,
)

def format_grades_for_prompt(summary) -> str:
    """Formatea calificaciones para el prompt."""
    return f"""
Materia: {summary.materia}
Estudiantes: {summary.num_estudiantes}

PARCIAL 1:
- Promedio: {summary.promedio_p1}
- Desviación: {summary.desviacion_p1}
- Reprobación: {summary.tasa_reprobacion_p1}%
- Peor componente: {summary.componente_mas_bajo_p1}
- Componentes: {summary.promedios_componentes_p1}

PARCIAL 2:
- Promedio: {summary.promedio_p2}
- Desviación: {summary.desviacion_p2}
- Reprobación: {summary.tasa_reprobacion_p2}%
- Peor componente: {summary.componente_mas_bajo_p2}
- Componentes: {summary.promedios_componentes_p2}

CAMBIO: {summary.delta:+.2f} puntos
"""
