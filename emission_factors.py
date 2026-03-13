"""
Factores de emisión (kg CO2e) para el cálculo de huella de carbono.
Fuentes aproximadas: IPCC, EPA, estudios de ciclo de vida.
"""

# Transporte: kg CO2 por km por persona (promedio)
TRANSPORT_PER_KM = {
    "bus": 0.089,
    "autobús": 0.089,
    "autobus": 0.089,
    "car": 0.192,
    "coche": 0.192,
    "auto": 0.192,
    "carro": 0.192,
    "moto": 0.113,
    "motocicleta": 0.113,
    "bike": 0.0,
    "bici": 0.0,
    "bicicleta": 0.0,
    "walk": 0.0,
    "caminando": 0.0,
    "pie": 0.0,
    "train": 0.041,
    "tren": 0.041,
    "metro": 0.041,
    "plane": 0.255,
    "avión": 0.255,
    "avion": 0.255,
    "vuelo": 0.255,
    "uber": 0.192,
    "taxi": 0.192,
}

# Alimentación: kg CO2 por porción/comida típica
FOOD_PER_SERVING = {
    "carne": 6.0,       # carne de res
    "res": 6.0,
    "vacuno": 6.0,
    "cerdo": 2.9,
    "pollo": 1.4,
    "pescado": 1.3,
    "huevos": 0.4,
    "lácteos": 0.6,
    "lacteos": 0.6,
    "queso": 0.5,
    "vegetariano": 0.2,
    "vegano": 0.1,
    "ensalada": 0.2,
    "arroz": 0.2,
    "pasta": 0.2,
}

# Electricidad: kg CO2 por kWh (mix promedio latinoamérica ~0.2)
KG_CO2_PER_KWH = 0.25


def get_transport_factor(vehicle_key: str) -> float:
    """Devuelve el factor de emisión por km para un medio de transporte."""
    key = vehicle_key.lower().strip()
    return TRANSPORT_PER_KM.get(key, 0.1)  # default: transporte público genérico


def get_food_factor(food_key: str) -> float:
    """Devuelve el factor de emisión por porción para un alimento."""
    key = food_key.lower().strip()
    return FOOD_PER_SERVING.get(key, 0.5)  # default: comida mixta


def co2_transport(vehicle: str, km: float) -> float:
    """Calcula kg CO2 para un trayecto."""
    return round(get_transport_factor(vehicle) * km, 2)


def co2_food(food: str, servings: float = 1.0) -> float:
    """Calcula kg CO2 por porciones de alimento."""
    return round(get_food_factor(food) * servings, 2)


def co2_electricity(kwh: float) -> float:
    """Calcula kg CO2 por consumo eléctrico."""
    return round(KG_CO2_PER_KWH * kwh, 2)
