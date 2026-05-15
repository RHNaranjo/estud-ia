# Agente Analizador de Evaluaciones
from google.adk.agents import Agent

FEEDBACK_ANALYZER_PROMPT = """Eres un analista educativo. Sintetiza comentarios
anónimos de estudiantes y extrae temas y sentimiento.

REGLAS ESTRICTAS:
- Los datos son anónimos.
- No reproduzcas comentarios ofensivos.
- Agrupa en TEMAS RECURRENTES.
- Reporta lo positivo y negativo equilibradamente.
- Nunca inventes comentarios.

FORMATO DE RESPUESTA (máximo 300 palabras):
1. Sentimiento General: ¿Cómo se sienten?
2. Temas Positivos: (máximo 3 temas)
3. Áreas de Oportunidad: (máximo 3 temas)
4. Citas: Incluye 2-3 comentarios textuales representativos.
"""

# Instancia del agente de retroalimentación
feedback_analyzer_agent = Agent(
    name="feedback_analyzer",
    model="gemini-1.5-flash",
    description="Analiza comentarios de estudiantes.",
    instruction=FEEDBACK_ANALYZER_PROMPT,
)

def format_feedback_for_prompt(summary) -> str:
    """Formatea feedback para el prompt."""
    comments_text = "\n".join(
        f"  - \"{c}\"" for c in summary.comentarios_limpios
    )
    return f"""
Materia: {summary.materia}
Evaluaciones: {summary.num_evaluaciones}
Satisfacción promedio: {summary.satisfaccion_promedio} / 5.0
Distribución: {summary.distribucion_satisfaccion}

Comentarios:
{comments_text}
"""
