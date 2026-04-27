# =============================================================================
# Estud-IA — Agente Analizador de Evaluaciones / Comentarios
# =============================================================================
"""
FeedbackAnalyzerAgent: Agente de Google ADK que analiza los comentarios
anónimos de los estudiantes sobre cada materia.

Recibe un FeedbackSummary (ya sanitizado) y extrae temas recurrentes,
sentimiento general y puntos clave mencionados por los estudiantes.
"""

from google.adk.agents import Agent

FEEDBACK_ANALYZER_PROMPT = """Eres un analista de retroalimentación educativa. Tu trabajo es
sintetizar los comentarios anónimos de estudiantes sobre una materia y extraer
los temas principales y el sentimiento general.

REGLAS ESTRICTAS:
- Los comentarios ya fueron anonimizados. No intentes inferir la identidad
  de ningún estudiante.
- No reproduzcas comentarios ofensivos ni ataques personales.
- Agrupa los comentarios en TEMAS RECURRENTES (ej. "ritmo de clase",
  "carga de trabajo", "calidad del material", "claridad de explicaciones").
- Reporta tanto lo positivo como lo negativo de forma equilibrada.
- Nunca inventes comentarios que no estén en los datos.

FORMATO DE RESPUESTA:
Genera un análisis breve (máximo 300 palabras) que cubra:
1. **Sentimiento General:** ¿Cómo se sienten los estudiantes? (basado en 
   satisfacción promedio y distribución)
2. **Temas Positivos:** ¿Qué valoran los estudiantes? (máximo 3 temas)
3. **Áreas de Oportunidad:** ¿Qué aspectos mejorar? (máximo 3 temas)
4. **Citas Representativas:** Incluye 2-3 comentarios textuales que mejor 
   representen el sentir general (no los más extremos).

DATOS A ANALIZAR:
{feedback_data}
"""

feedback_analyzer_agent = Agent(
    name="feedback_analyzer",
    model="gemini-2.5-flash",
    description="Analiza comentarios anónimos de estudiantes y extrae temas clave.",
    instruction=FEEDBACK_ANALYZER_PROMPT,
)


def format_feedback_for_prompt(summary) -> str:
    """Formatea un FeedbackSummary como texto legible para el prompt del agente."""
    comments_text = "\n".join(
        f"  - \"{c}\"" for c in summary.comentarios_limpios
    )
    return f"""
Materia: {summary.materia}
Número de evaluaciones: {summary.num_evaluaciones}
Satisfacción promedio: {summary.satisfaccion_promedio} / 5.0
Distribución de satisfacción: {summary.distribucion_satisfaccion}

Comentarios de los estudiantes:
{comments_text}
"""
