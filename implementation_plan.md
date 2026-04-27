# Plan de Implementación: Asistente para Profesores Estud-IA (Google ADK)

Este documento detalla la arquitectura, estructura de código, interfaz de usuario y las consideraciones éticas fundamentales para el desarrollo de la plataforma Estud-IA. El sistema utilizará una arquitectura multi-agente basada en **Google ADK** para analizar calificaciones y comentarios de estudiantes, con el objetivo final de generar retroalimentación constructiva para los profesores.

---

## 1. Consideraciones Éticas (INDISPENSABLE)

El uso de datos de estudiantes (calificaciones y opiniones) para evaluar el desempeño de una materia requiere un marco ético riguroso para proteger a los alumnos y asegurar que la retroalimentación sea justa para los profesores.

> [!CAUTION]
> **Riesgos de Privacidad (Estudiantes)**
> - **Reidentificación (De-anonymization):** Aunque los comentarios sean anónimos, el estilo de escritura, quejas muy específicas sobre un incidente en clase, o el cruce de datos (ej. un alumno que sacó muy baja calificación y escribe un comentario muy enojado) pueden permitir al profesor identificar al estudiante.
> - **Fuga de datos:** Manejo inseguro de los archivos `.csv` que exponga las calificaciones al público o a otros estudiantes.

> [!IMPORTANT]
> **Criterios Éticos de Evaluación del Agente**
> - **Enfoque Constructivo y No Punitivo:** El prompt del agente final debe obligarle a usar principios de Comunicación No Violenta. El agente nunca debe insultar, denigrar ni culpar al profesor, sino sugerir áreas de oportunidad pedagógica.
> - **Despersonalización:** El análisis debe centrarse en la *metodología de la clase* y el *material*, no en la personalidad del profesor. Se deben filtrar comentarios de estudiantes que contengan ataques personales (hate speech) antes de que influyan en el reporte final.
> - **Mitigación de Sesgos:** Evitar penalizar a profesores de materias inherentemente difíciles (ej. matemáticas avanzadas) donde las calificaciones suelen ser más bajas por naturaleza.

> [!NOTE]
> **Diseño Ético del Ciclo de Vida de la Plataforma**
> 1. **Minimización de Datos:** El sistema solo debe procesar los datos en memoria. Los archivos `.csv` deben eliminarse inmediatamente después de generar el reporte.
> 2. **Transparencia:** El reporte generado debe incluir un descargo de responsabilidad indicando claramente que fue generado por IA a partir de datos limitados.
> 3. **Human-in-the-Loop:** En una fase posterior, el reporte debería ser revisado por un coordinador académico antes de ser entregado directamente al profesor, para asegurar la calidad y el tono de la retroalimentación.

---

## 2. Arquitectura del Sistema (Google ADK)

Se propone un sistema compuesto por cuatro agentes especializados que colaboran en secuencia:

1. **`DataSanitizationAgent`:** Recibe los CSVs y elimina cualquier posible PII (Información Personal Identificable). Filtra comentarios con insultos explícitos para proteger al profesor.
2. **`GradesAnalyzerAgent`:** Analiza la evolución entre el Parcial 1 y Parcial 2. Identifica tendencias (ej. caída generalizada de calificaciones, varianza extrema, etc.).
3. **`FeedbackAnalyzerAgent`:** Procesa los comentarios anónimos. Realiza análisis de sentimiento y extrae los "temas principales" (ej. "tareas excesivas", "explicaciones poco claras", "excelente material de apoyo").
4. **`TeacherCoachAgent`:** Actúa como el agente orquestador/sintetizador final. Recibe los insights de calificaciones y comentarios, y redacta el reporte constructivo dirigido al profesor utilizando un tono empático y profesional.

---

## 3. Propuesta de Estructura de Código

Se sugiere una estructura modular en Python, preparada para escalar e integrarse fácilmente con una interfaz web (como Streamlit).

```text
estud-ia/
├── data/                      # (Excluido en .gitignore) Carpeta temporal para CSVs 
├── agents/                    # Definición de Agentes ADK
│   ├── __init__.py
│   ├── base_agent.py          # Configuración base de Google ADK
│   ├── sanitization.py        # DataSanitizationAgent
│   ├── grades_analyzer.py     # GradesAnalyzerAgent
│   ├── feedback_analyzer.py   # FeedbackAnalyzerAgent
│   └── teacher_coach.py       # TeacherCoachAgent
├── models/                    # Estructuras de datos (Pydantic / Dataclasses)
│   ├── __init__.py
│   ├── student_record.py
│   └── feedback_report.py
├── utils/                     # Utilidades
│   ├── csv_parser.py          # Lógica para leer y validar CSVs
│   └── ethics_filters.py      # Filtros de palabras altisonantes / PII Regex
├── app.py                     # Interfaz de Usuario (Streamlit)
├── requirements.txt           # Dependencias (google-genai, streamlit, pandas)
└── .env.example               # Ejemplo de variables de entorno (API Keys)
```

---

## 4. Diseño de la Interfaz de Usuario

Dado que se requiere una interfaz pequeña y muy básica para la validación inicial del concepto (MVP), se utilizará **Streamlit**. Esto permite crear una UI limpia y funcional con código puramente en Python.

**Flujo de la UI (`app.py`):**
1. **Header:** Logo de Estud-IA y título "Asistente de Retroalimentación Docente".
2. **Disclaimer Ético:** Un mensaje advirtiendo que los datos serán procesados de forma temporal y anónima.
3. **Zona de Carga (Drag & Drop):**
   - Input 1: Archivo CSV de Calificaciones (Parcial 1 y 2).
   - Input 2: Archivo CSV de Comentarios Anónimos.
4. **Botón de Acción:** "Generar Reporte Constructivo".
5. **Panel de Resultados:**
   - Una vez procesado, mostrará un reporte dividido en:
     - *Resumen Estadístico* (Evolución de calificaciones).
     - *Temas Clave* detectados por los alumnos.
     - *Recomendaciones Prácticas y Empáticas* para el profesor.

---

## 5. Plan de Verificación

1. **Pruebas de Ingestión:** Crear CSVs falsos (mock data) con nombres ficticios y comentarios variados. Verificar que el `DataSanitizationAgent` elimine correctamente cualquier dato personal introducido a propósito.
2. **Pruebas de Análisis:** Validar que los agentes detecten correctamente las tendencias (ej. si programo una bajada del 30% en el parcial 2 en el mock de datos, el agente debe mencionarlo).
3. **Pruebas de Tono (Red Teaming):** Incluir comentarios de "hate" en los CSVs de prueba para asegurar que el `TeacherCoachAgent` no propague toxicidad hacia el profesor y mantenga su postura constructiva.
4. **Verificación de UI:** Levantar el servidor local de Streamlit y simular la experiencia completa del usuario.
