import streamlit as st
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importar lógica del backend
from utils.csv_parser import parse_grades_csv, parse_evals_csv
from agents.sanitization import sanitize_grades, sanitize_feedback
from agents.pipeline import run_pipeline

# Configuración básica de la página
st.set_page_config(
    page_title="Estud-IA | Asistente de Retroalimentación",
    page_icon="🎓",
    layout="wide"
)

# Estilo adicional (CSS) para asegurar que el contenido markdown luzca bien con el fondo oscuro
st.markdown("""
<style>
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #D5BF86 !important;
    }
    .disclaimer {
        font-size: 0.85em;
        color: #D5BF86;
        border: 1px solid #4E3822;
        padding: 10px;
        border-radius: 5px;
        background-color: rgba(78, 56, 34, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Logo y Título
col1, col2 = st.columns([1, 4])
with col1:
    if os.path.exists("logoestudia.png"):
        st.image("logoestudia.png", width="stretch")
with col2:
    st.title("Estud-IA")
    st.subheader("Generador de Reportes de Retroalimentación Docente")

st.markdown("Sube los datos académicos de tus materias. Estud-IA analizará las tendencias y comentarios anónimos para crear un reporte constructivo y empático para cada profesor.")

st.divider()

# Formularios de Subida de Archivos
col_grades, col_evals = st.columns(2)

with col_grades:
    st.markdown("### 📊 Calificaciones")
    grades_file = st.file_uploader(
        "Sube el archivo CSV de calificaciones (con columnas requeridas).",
        type=["csv"],
        key="grades_uploader"
    )

with col_evals:
    st.markdown("### 📝 Evaluaciones")
    evals_file = st.file_uploader(
        "Sube el archivo CSV de evaluaciones anónimas.",
        type=["csv"],
        key="evals_uploader"
    )

# Botón de Acción
if st.button("Analizar y Generar Reportes", type="primary", width="stretch"):
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("Error: No se encontró la variable GOOGLE_API_KEY en el archivo .env")
        st.stop()

    if not grades_file or not evals_file:
        st.warning("⚠️ Por favor, sube ambos archivos (Calificaciones y Evaluaciones) en formato CSV para continuar.")
        st.stop()

    # Procesamiento
    with st.spinner("Procesando datos y analizando con IA... (Esto puede tomar un par de minutos)"):
        try:
            # 1. Parseo
            grades_records = parse_grades_csv(grades_file)
            evals_records = parse_evals_csv(evals_file)

            # 2. Sanitización y agrupación
            grades_summaries = sanitize_grades(grades_records, min_estudiantes=3)
            evals_summaries = sanitize_feedback(evals_records, min_evaluaciones=3)

            # Diccionarios por materia
            grades_dict = {s.materia: s for s in grades_summaries}
            evals_dict = {s.materia: s for s in evals_summaries}

            # Encontrar materias comunes con suficientes datos
            materias_comunes = set(grades_dict.keys()).intersection(set(evals_dict.keys()))

            if not materias_comunes:
                st.error("❌ No se encontraron materias en común entre los dos archivos con datos suficientes (mínimo 3 registros por seguridad).")
                st.stop()

            st.success(f"✅ ¡Análisis completado! Se generaron reportes para {len(materias_comunes)} materia(s).")
            st.divider()

            # 3. Pipeline IA por materia y renderizado
            tabs = st.tabs(list(materias_comunes))
            
            for index, materia in enumerate(materias_comunes):
                with tabs[index]:
                    # Ejecutar orquestador
                    report = run_pipeline(grades_dict[materia], evals_dict[materia])
                    
                    # Mostrar resultados
                    st.markdown(report.reporte_markdown)
                    st.markdown(f'<div class="disclaimer"><strong>⚠️ Disclaimer Ético:</strong><br>{report.disclaimer}</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Ocurrió un error procesando los archivos: {str(e)}")
            st.exception(e)
