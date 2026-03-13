# EcoTrack — MVP Huella de Carbono en Lenguaje Natural

Aplicación web sencilla para registrar tu huella de carbono diaria escribiendo en lenguaje natural (ej.: *"Hoy comí carne y viajé 20 km en bus"*). El sistema estima un equivalente en kg CO₂.

## Cómo ejecutar

### Local (Cursor / terminal)

```bash
pip install -r requirements.txt
streamlit run app.py
```

Abre la URL que muestra Streamlit (por defecto `http://localhost:8501`).

### Replit

1. Crea un nuevo Repl e importa este repositorio (o pega los archivos).
2. Replit usará el archivo `.replit` para ejecutar: `streamlit run app.py --server.port=3000`.
3. Usa **Run** y luego **Deploy** si quieres una URL pública.

## Estructura del proyecto

| Archivo / carpeta | Descripción |
|-------------------|-------------|
| `app.py` | Interfaz Streamlit (entrada de texto y resultado). |
| `parser.py` | Parsing de lenguaje natural → actividades (transporte, alimentación). |
| `emission_factors.py` | Factores de emisión (kg CO₂ por km, por porción de alimento). |
| `.cursorrules` | Reglas de Cursor para el proyecto. |
| `.cursor/rules/` | Reglas adicionales (visión y estándares EcoTrack). |
| `.replit` | Configuración para ejecutar y desplegar en Replit. |
| `VIBE_REPORT.md` | Reflexión del proceso (configuración, dificultades, orquestación). |

## Ejemplos de entrada

- *"Hoy comí carne y viajé 20 km en bus"*
- *"Desayuné huevos, almorcé pollo y recorrí 15 km en coche"*
- *"Solo ensalada y 5 km en bici"*

Los factores son aproximados; el objetivo del MVP es conciencia y validación de idea, no contabilidad exacta.
