from .grades_analyzer import grades_analyzer_agent, format_grades_for_prompt
from .feedback_analyzer import feedback_analyzer_agent, format_feedback_for_prompt
from .teacher_coach import teacher_coach_agent
from models import GradesSummary, FeedbackSummary, TeacherReport
from google.adk.runners import InMemoryRunner, types

def run_pipeline(grades_summary: GradesSummary, feedback_summary: FeedbackSummary) -> TeacherReport:
    """Ejecuta los agentes usando InMemoryRunner y maneja el flujo de eventos."""
    
    def get_agent_response(agent, message):
        # Habilitar auto_create_session para que cree la sesión si no existe
        runner = InMemoryRunner(agent=agent)
        runner.auto_create_session = True
        
        # Envolver el mensaje en el formato esperado por ADK (Content object)
        msg = types.Content(role="user", parts=[types.Part(text=message)])
        
        # El runner es un generador, acumulamos el texto de los eventos
        events = runner.run(new_message=msg, user_id="teacher_user", session_id="session_1")
        full_text = ""
        for event in events:
            # Buscamos eventos que contengan texto (model responses)
            if hasattr(event, 'text') and event.text:
                full_text += event.text
            elif hasattr(event, 'content') and hasattr(event.content, 'parts'):
                for part in event.content.parts:
                    if hasattr(part, 'text'):
                        full_text += part.text
        return full_text

    # 1. Analiza calificaciones
    grades_text = format_grades_for_prompt(grades_summary)
    grades_analysis = get_agent_response(grades_analyzer_agent, f"Analiza estos datos:\n{grades_text}")
    
    # 2. Analiza comentarios
    feedback_text = format_feedback_for_prompt(feedback_summary)
    feedback_analysis = get_agent_response(feedback_analyzer_agent, f"Analiza estos datos:\n{feedback_text}")
    
    # 3. Genera reporte final
    coach_prompt = f"""
    Genera el reporte basado en:
    --- ANÁLISIS DE CALIFICACIONES ---
    {grades_analysis}
    
    --- ANÁLISIS DE COMENTARIOS ---
    {feedback_analysis}
    """
    final_report_text = get_agent_response(teacher_coach_agent, coach_prompt)
    
    return TeacherReport(
        materia=grades_summary.materia,
        reporte_markdown=final_report_text
    )
