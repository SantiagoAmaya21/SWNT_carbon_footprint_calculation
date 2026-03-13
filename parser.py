"""
Parser de lenguaje natural: extrae actividades (transporte, alimentación)
a partir de texto libre para calcular huella de carbono.
"""

import re
from typing import Any

from emission_factors import (
    TRANSPORT_PER_KM,
    FOOD_PER_SERVING,
    co2_transport,
    co2_food,
)


def extract_transport(text: str) -> list[dict[str, Any]]:
    """
    Detecta patrones como "20km en bus", "viajé 15 km en carro", "5 km en bici".
    Devuelve lista de {"vehicle": str, "km": float, "co2_kg": float}.
    """
    text_lower = text.lower()
    results = []

    # Patrón: número (opcional decimal) + (km|kilómetros) + (en|por) + medio
    # También: "viajé X km", "recorrí X km"
    number_km = r"(\d+(?:[.,]\d+)?)\s*(?:km|kilómetros|kilometros)"
    for vehicle in TRANSPORT_PER_KM:
        # "20 km en bus", "20km en bus", "viajé 20 km en bus"
        patterns = [
            rf"{number_km}\s+(?:en|por|in)\s+{re.escape(vehicle)}\b",
            rf"{re.escape(vehicle)}\s+{number_km}",
        ]
        for pat in patterns:
            for m in re.finditer(pat, text_lower, re.IGNORECASE):
                km = float(m.group(1).replace(",", "."))
                co2 = co2_transport(vehicle, km)
                results.append({"type": "transport", "vehicle": vehicle, "km": km, "co2_kg": co2})

    # Evitar duplicados por mismo vehicle+km
    seen = set()
    unique = []
    for r in results:
        key = (r["vehicle"], r["km"])
        if key not in seen:
            seen.add(key)
            unique.append(r)

    return unique


def extract_food(text: str) -> list[dict[str, Any]]:
    """
    Detecta menciones de alimentos: "comí carne", "desayuné huevos", "almuerzo vegetariano".
    Devuelve lista de {"food": str, "servings": float, "co2_kg": float}.
    """
    text_lower = text.lower()
    results = []

    for food in FOOD_PER_SERVING:
        # Cuenta apariciones de la palabra como token (evita doble conteo en misma frase)
        pattern = rf"\b{re.escape(food)}\b"
        matches = list(re.finditer(pattern, text_lower))
        if matches:
            servings = max(1, len(matches))
            co2 = co2_food(food, servings)
            results.append({"type": "food", "food": food, "servings": servings, "co2_kg": co2})

    return results


def parse_and_calculate(text: str) -> dict[str, Any]:
    """
    Parsea el texto, extrae actividades y calcula el CO2 total.
    Devuelve: { "activities": [...], "total_kg_co2": float, "summary": str }
    """
    if not text or not text.strip():
        return {
            "activities": [],
            "total_kg_co2": 0.0,
            "summary": "Escribe tu día en lenguaje natural (ej: Hoy comí carne y viajé 20km en bus).",
        }

    transport = extract_transport(text)
    food = extract_food(text)
    activities = transport + food
    total = round(sum(a["co2_kg"] for a in activities), 2)

    summary_parts = []
    if transport:
        summary_parts.append(f"Transporte: {sum(a['co2_kg'] for a in transport)} kg CO₂")
    if food:
        summary_parts.append(f"Alimentación: {sum(a['co2_kg'] for a in food)} kg CO₂")
    summary = " | ".join(summary_parts) if summary_parts else "No se detectaron actividades con factores de emisión."

    return {
        "activities": activities,
        "total_kg_co2": total,
        "summary": summary,
    }
