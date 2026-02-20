# Carbon Tracker Service
## Microservicio de Cálculo de Huella de Carbono
**Proyecto: EcoLogistics**
**Desarrollo Asistido con IA Generativa**

---

# 1. Introducción

En el desarrollo de software moderno, la Ingeniería de Prompts se ha convertido en una competencia clave para utilizar Modelos de Lenguaje Grandes (LLMs) como colaboradores estratégicos en el SDLC.

Este proyecto documenta el desarrollo de un microservicio de cálculo de huella de carbono utilizando técnicas avanzadas de prompting:

- Zero-shot Prompting
- Few-shot Prompting
- Chain-of-Thought (CoT)
- Contextualización por Rol
- Identificación de Gaps Técnicos
- Refinamiento Iterativo

El objetivo no fue solo generar código, sino demostrar dominio estratégico del uso de IA en análisis, diseño, implementación y validación.

---

# 2. Contexto del Proyecto

## Empresa: EcoLogistics

EcoLogistics busca transformar sus operaciones hacia un modelo sostenible mediante un microservicio llamado **Carbon Tracker Service**, que calcule emisiones de CO₂ basadas en:

- Tipo de vehículo
- Peso de carga
- Distancia recorrida
- Factor de eficiencia energética

---

# 3. Fase 0 – Definición de Requerimientos con IA

Antes de escribir código, se aplicó Ingeniería de Prompts para transformar la idea en especificaciones técnicas claras.

---

## 3.1 Idea Bruta Inicial

> "Necesitamos un servicio que calcule la huella de carbono según el vehículo, la distancia y el peso transportado."

Problemas detectados:
- No define fórmula.
- No especifica validaciones.
- No contempla casos de error.
- No define contrato de API.
- No establece criterios de aceptación.

---

## 3.2 Prompt Estratégico (Contextualización por Rol)

```text
Actúa como un Business Analyst senior especializado en sistemas sostenibles.

Transforma la siguiente idea en:
- Historias de Usuario
- Criterios de Aceptación en formato Gherkin
- Consideraciones Técnicas
- Identificación de información faltante
3.3 Historias de Usuario Generadas
Historia 1 – Cálculo de Emisiones

Título: Cálculo de Huella de Carbono

Descripción:
Como operador logístico
Quiero calcular las emisiones de CO₂ de un trayecto
Para medir el impacto ambiental de cada envío

Criterios de Aceptación:

Given un tipo de vehículo válido
And una distancia mayor o igual a 0
And un peso mayor a 0
When se realiza el cálculo
Then el sistema debe retornar emisiones en kg de CO2

Given un tipo de vehículo no soportado
When se realiza el cálculo
Then el sistema debe retornar error 400
3.4 Identificación de Gaps Técnicos

La IA sugirió considerar:

¿Qué ocurre si efficiency_factor = 0?

¿Se permiten distancias negativas?

¿Se deben almacenar los cálculos?

¿Se necesita autenticación?

¿Se deben versionar los endpoints?

Esto redujo ambigüedad antes de codificar.

4. Fase 1 – Ingeniería de Prompts Aplicada
4.1 Zero-shot Prompting

Utilizado para tareas estándar.

Ejemplo:

Escribe una función en Python que calcule emisiones de CO2 usando distancia, peso y tipo de vehículo.

Ventaja:

Rapidez

Ideal para prototipado

Limitación:

Código genérico

Sin arquitectura clara

4.2 Few-shot Prompting

Utilizado para asegurar consistencia en formato y validaciones.

Ejemplo:

Ejemplo 1:
Entrada: vehículo=diesel, distancia=100, peso=10
Salida: emisiones calculadas con validación de tipo

Ejemplo 2:
Entrada: vehículo inválido
Salida: error 400 con mensaje descriptivo

Ahora genera la función siguiendo este patrón.

Ventaja:

Consistencia

Control de estilo

Reducción de ambigüedad

4.3 Chain-of-Thought (CoT)

Aplicado para diseño lógico antes de programar.

Antes de escribir código:

1. Define la fórmula matemática.
2. Explica cómo influye cada variable.
3. Identifica casos de error.
4. Propón estructura modular.

Resultado:

Reducción de alucinaciones

Arquitectura coherente

Mayor precisión lógica

5. Aplicación en el SDLC
Técnica	Fase SDLC	Beneficio
Zero-shot	Implementación rápida	Velocidad
Few-shot	Testing y documentación	Consistencia
Chain-of-Thought	Diseño y debugging	Precisión

6. Implementación Técnica
6.1 Stack Tecnológico

Python 3.11

FastAPI

Pydantic

PyTest

Arquitectura modular

Principios SOLID

6.2 Estructura del Proyecto
carbon-tracker/
│
├── app/
│   ├── main.py
│   ├── api/
│   │   └── routes.py
│   ├── services/
│   │   └── carbon_service.py
│   ├── models/
│   │   └── carbon_model.py
│
├── tests/
│   └── test_carbon_service.py
│
└── requirements.txt
6.3 Modelo de Entrada
from pydantic import BaseModel, Field
from enum import Enum

class VehicleType(str, Enum):
    ELECTRIC = "electric"
    DIESEL = "diesel"
    HYBRID = "hybrid"

class CarbonRequest(BaseModel):
    vehicle_type: VehicleType
    cargo_weight: float = Field(..., gt=0)
    distance: float = Field(..., ge=0)
    efficiency_factor: float = Field(..., gt=0)
6.4 Lógica de Negocio
class CarbonService:

    EMISSION_FACTORS = {
        "electric": 0.02,
        "hybrid": 0.12,
        "diesel": 0.25
    }

    @staticmethod
    def calculate_emissions(vehicle_type: str,
                            cargo_weight: float,
                            distance: float,
                            efficiency_factor: float) -> float:

        if cargo_weight < 0:
            raise ValueError("Cargo weight cannot be negative")

        if efficiency_factor <= 0:
            raise ValueError("Efficiency factor must be greater than zero")

        if vehicle_type not in CarbonService.EMISSION_FACTORS:
            raise ValueError("Unsupported vehicle type")

        emission_factor = CarbonService.EMISSION_FACTORS[vehicle_type]
        cargo_factor = cargo_weight / 20

        emissions = distance * emission_factor * (1 + cargo_factor)
        final_emissions = emissions / efficiency_factor

        return round(final_emissions, 3)
6.5 API
from fastapi import APIRouter, HTTPException
from app.models.carbon_model import CarbonRequest
from app.services.carbon_service import CarbonService

router = APIRouter()

@router.post("/calculate")
def calculate_carbon(data: CarbonRequest):
    try:
        result = CarbonService.calculate_emissions(
            vehicle_type=data.vehicle_type,
            cargo_weight=data.cargo_weight,
            distance=data.distance,
            efficiency_factor=data.efficiency_factor
        )
        return {"co2_emissions_kg": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
7. Suite de Pruebas (Few-shot aplicado)
import pytest
from app.services.carbon_service import CarbonService

def test_valid_calculation():
    result = CarbonService.calculate_emissions(
        vehicle_type="diesel",
        cargo_weight=10,
        distance=100,
        efficiency_factor=1.0
    )
    assert result > 0

def test_zero_distance():
    result = CarbonService.calculate_emissions(
        vehicle_type="electric",
        cargo_weight=5,
        distance=0,
        efficiency_factor=1.0
    )
    assert result == 0

def test_invalid_vehicle():
    with pytest.raises(ValueError):
        CarbonService.calculate_emissions(
            vehicle_type="gasoline",
            cargo_weight=10,
            distance=100,
            efficiency_factor=1.0
        )

def test_invalid_efficiency():
    with pytest.raises(ValueError):
        CarbonService.calculate_emissions(
            vehicle_type="diesel",
            cargo_weight=10,
            distance=100,
            efficiency_factor=0
        )

Cobertura estimada: >90%

8. Code Review con IA (Chain-of-Thought)

Prompt utilizado:

Revisa el siguiente código paso a paso:
1. Identifica riesgos de seguridad.
2. Evalúa validaciones.
3. Detecta posibles mejoras de rendimiento.
4. Evalúa principios SOLID.

Mejoras sugeridas:

Validación adicional de eficiencia

Uso de Enum estrictamente tipado

Logging estructurado

Posible inyección de dependencias futura

9. Reflexión Crítica
Ventajas

Reducción de tiempo en definición de requerimientos

Detección temprana de escenarios de error

Generación rápida de pruebas

Mejora en estructuración arquitectónica

Riesgos

Sobreconfianza en código no auditado

Dependencia excesiva

Posibles alucinaciones si el prompt es ambiguo

Papel del Ingeniero de Software

El ingeniero:

Valida la lógica

Ajusta criterios de aceptación

Verifica seguridad

Garantiza alineación con arquitectura real

La IA es un acelerador, no un reemplazo del criterio técnico.

Conclusión

Este proyecto demuestra que:

La Ingeniería de Prompts es una competencia técnica real.

Zero-shot acelera.

Few-shot estandariza.

Chain-of-Thought profundiza.

La IA mejora el SDLC cuando se usa estratégicamente.

El microservicio cumple:

- Modularidad
- Principios SOLID
- Validaciones robustas
- Cobertura de pruebas alta
- Documentación clara
- Proceso iterativo documentado

Ejecución
pip install -r requirements.txt
uvicorn app.main:app --reload
pytest

Proyecto desarrollado aplicando Ingeniería de Prompts avanzada en el SDLC.