"""
AutoFlow AI - Gemini Parser Service
Convierte instrucciones en lenguaje natural a un plan JSON validado.
"""

import json
from typing import Any

import requests
from pydantic import ValidationError

from config import settings
from schemas.job import ExecutionPlan


class GeminiParserError(Exception):
    """Error controlado del parser de Gemini."""


def _build_prompt(instruction: str) -> str:
    return (
        "Eres un parser para una plataforma de automatizacion RPA. "
        "Convierte la instruccion del usuario en un plan JSON ejecutable.\n\n"
        "Reglas obligatorias:\n"
        "1) Responde SOLO con JSON valido, sin markdown ni texto adicional.\n"
        "2) Formato exacto:\n"
        "{\n"
        "  \"total_steps\": <int>,\n"
        "  \"steps\": [\n"
        "    {\n"
        "      \"id\": <int>,\n"
        "      \"action\": \"<string>\",\n"
        "      \"description\": \"<string>\",\n"
        "      \"params\": { ... }\n"
        "    }\n"
        "  ]\n"
        "}\n"
        "3) Los IDs deben ser unicos y arrancar en 1.\n"
        "4) Usa acciones concretas y cortas (ej: open_web, click, fill, wait, screenshot, scrape_data).\n"
        "5) Si falta contexto, crea pasos razonables y explicitos.\n\n"
        f"Instruccion del usuario:\n{instruction}"
    )


def _extract_text_from_gemini(payload: dict[str, Any]) -> str:
    candidates = payload.get("candidates", [])
    if not candidates:
        raise GeminiParserError("Gemini no devolvio candidatos en la respuesta")

    parts = candidates[0].get("content", {}).get("parts", [])
    if not parts:
        raise GeminiParserError("Gemini devolvio respuesta vacia")

    text = parts[0].get("text", "").strip()
    if not text:
        raise GeminiParserError("Gemini devolvio texto vacio")

    return text


def _safe_json_loads(raw_text: str) -> dict[str, Any]:
    cleaned = raw_text.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise GeminiParserError(f"Gemini devolvio JSON invalido: {exc}") from exc

    if not isinstance(data, dict):
        raise GeminiParserError("El JSON devuelto por Gemini debe ser un objeto")

    return data


def parse_instruction_with_gemini(instruction: str) -> ExecutionPlan:
    """Genera y valida un plan de ejecucion usando Gemini."""
    if not settings.GEMINI_API_KEY:
        raise GeminiParserError("Falta configurar GEMINI_API_KEY en variables de entorno")

    endpoint = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{settings.GEMINI_MODEL}:generateContent?key={settings.GEMINI_API_KEY}"
    )

    payload = {
        "contents": [{"parts": [{"text": _build_prompt(instruction)}]}],
        "generationConfig": {
            "temperature": 0.2,
            "response_mime_type": "application/json",
        },
    }

    try:
        response = requests.post(endpoint, json=payload, timeout=40)
    except requests.RequestException as exc:
        raise GeminiParserError(f"Error de red al invocar Gemini: {exc}") from exc

    if response.status_code >= 400:
        raise GeminiParserError(
            f"Gemini respondio con error HTTP {response.status_code}: {response.text}"
        )

    raw_text = _extract_text_from_gemini(response.json())
    json_data = _safe_json_loads(raw_text)

    try:
        return ExecutionPlan.model_validate(json_data)
    except ValidationError as exc:
        raise GeminiParserError(f"El JSON de Gemini no cumple el esquema esperado: {exc}") from exc
