# =============================================================================
# Estud-IA — Filtros Éticos
# =============================================================================
"""
Filtros para proteger la privacidad de los estudiantes y asegurar
que la retroalimentación generada sea constructiva y no tóxica.
"""

import re


# -------------------------------------------------------------------------
# Filtro de PII (Información Personal Identificable)
# -------------------------------------------------------------------------

# Patrones regex para detectar PII en comentarios
PII_PATTERNS = [
    # Correos electrónicos
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    # Números de teléfono (formatos mexicanos comunes)
    r"\b\d{2,3}[-.\s]?\d{3,4}[-.\s]?\d{4}\b",
    # Matrículas / IDs estudiantiles (patrones comunes: 6-10 dígitos)
    r"\b\d{6,10}\b",
    # Números de control / CURP
    r"\b[A-Z]{4}\d{6}[HM][A-Z]{5}[A-Z0-9]\d\b",
]


def remove_pii(text: str) -> str:
    """
    Elimina posibles datos personales (PII) de un texto.

    Args:
        text: Texto original del comentario.

    Returns:
        Texto con PII reemplazado por [REDACTADO].
    """
    result = text
    for pattern in PII_PATTERNS:
        result = re.sub(pattern, "[REDACTADO]", result, flags=re.IGNORECASE)
    return result


# -------------------------------------------------------------------------
# Filtro de contenido tóxico / ataques personales
# -------------------------------------------------------------------------

# Palabras o frases que constituyen ataques personales directos
# al profesor (no son críticas constructivas sobre la clase).
TOXIC_KEYWORDS = [
    # Insultos directos
    "idiota", "estúpido", "estupido", "inútil", "inutil", "incompetente",
    "pendejo", "pendeja", "imbécil", "imbecil", "tonto", "tonta",
    "basura", "mediocre", "naco", "naca", "corriente",
    # Amenazas o expresiones violentas
    "lo voy a", "le voy a", "se va a arrepentir", "amenaz",
    # Discriminación
    "viejo", "vieja", "gordo", "gorda", "feo", "fea",
]

# Frases que indican que el comentario es solo un ataque sin contenido útil
ATTACK_PATTERNS = [
    r"(?:es|eres)\s+(?:un|una)\s+\w+",    # "es un/una [insulto]"
    r"(?:odia|odio)\s+(?:al|a la)\s+prof",  # "odio al profe"
    r"que\s+(?:lo|la)\s+corran",            # "que lo/la corran"
]


def is_toxic(text: str) -> bool:
    """
    Determina si un comentario contiene ataques personales o toxicidad.

    Args:
        text: Texto del comentario.

    Returns:
        True si el comentario es tóxico y debe filtrarse.
    """
    lower = text.lower()

    # Verificar palabras tóxicas
    for keyword in TOXIC_KEYWORDS:
        if keyword in lower:
            return True

    # Verificar patrones de ataque
    for pattern in ATTACK_PATTERNS:
        if re.search(pattern, lower):
            return True

    return False


def sanitize_comment(text: str) -> str | None:
    """
    Aplica todos los filtros éticos a un comentario.

    Returns:
        El comentario limpio, o None si debe descartarse por toxicidad.
    """
    # Paso 1: Remover PII
    clean = remove_pii(text)

    # Paso 2: Filtrar toxicidad
    if is_toxic(clean):
        return None

    return clean


def sanitize_comments(comments: list[str]) -> list[str]:
    """
    Aplica sanitización a una lista de comentarios.

    Returns:
        Lista de comentarios limpios (los tóxicos se eliminan).
    """
    sanitized = []
    for comment in comments:
        result = sanitize_comment(comment)
        if result is not None:
            sanitized.append(result)
    return sanitized
