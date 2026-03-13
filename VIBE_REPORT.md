# Vibe Report — EcoTrack

**Proyecto Integrador: Configuración del Ecosistema y Primer "Vibe"**

---

## 1. Cómo configuré las reglas del agente

Se usaron dos mecanismos para que la IA entienda el proyecto:

- **`.cursorrules`** (en la raíz del repo): archivo clásico de Cursor donde se definió la identidad del proyecto (EcoTrack, MVP de huella de carbono en lenguaje natural), preferencias de código limpio y modular, frameworks modernos (Next.js o Python/Streamlit), y que la lógica de parsing y factores de emisión esté documentada y sea fácil de extender. También se indicó no hardcodear secretos y priorizar que el prototipo funcione de punta a punta.

- **`.cursor/rules/ecotrack-standards.mdc`**: regla con `alwaysApply: true` que resume la visión (usuario escribe en lenguaje natural y recibe estimado de CO₂), pide modularidad (parsing, factores, presentación), mensajes al usuario en español y código en inglés, y un ejemplo de estructura deseada. Así el agente mantiene el mismo “vibe” en cualquier archivo.

La idea fue dar contexto de producto y estilo en `.cursorrules` y reforzar la visión y el flujo (texto → actividades → CO₂) en la regla aplicada siempre.

---

## 2. Dificultades al delegar el código a la IA

- **Precisión del parsing**: que el parser detecte bien “viajé 20 km en bus” o “comí carne” sin depender de un LLM externo requirió definir bien los patrones (regex) y los diccionarios de transporte y alimentos. La IA propone estructura rápido, pero ajustar los casos borde (número con coma, “autobús” vs “bus”, evitar doble conteo de “carne” en la misma frase) implicó iterar con prompts del tipo “si el usuario escribe X, debe salir Y”.

- **Equilibrio MVP vs completitud**: el enunciado pide que “la IA calcule” el estimado; aquí “la IA” es tanto el agente que genera el código como la lógica del producto. Para que el MVP funcione sin API keys se optó por reglas + factores de emisión en código; si luego se integra un LLM para interpretar texto libre, la estructura (parser, factores, UI) ya está separada y es fácil conectar.

- **Entorno y despliegue**: asegurar que el mismo código corra en local (Cursor) y en Replit llevó a configurar `.replit` con el comando `streamlit run app.py` y puerto 3000, y a mantener un `requirements.txt` mínimo para que Replit instale solo Streamlit.

---

## 3. De “escribir código” a “orquestar una visión”

Pasar de escribir cada línea a orquestar el flujo se siente más como **definir el qué** (que el usuario escriba su día y vea un estimado de CO₂) y **dejar que la IA proponga el cómo** (estructura de carpetas, módulos de factores y parser, interfaz en Streamlit). Mi rol fue dar el enunciado claro, aceptar o refinar la arquitectura propuesta y corregir solo cuando el comportamiento no coincidía con el ejemplo “Hoy comí carne y viajé 20 km en bus”. No tuve que implementar regex ni factores a mano; sí revisar que el resultado fuera coherente y que las reglas del proyecto guiaran respuestas futuras. La sensación es de **dirigir un pequeño producto** en lugar de codificar cada detalle, manteniendo el “vibe” del MVP y dejando que la implementación concreta sea iterativa con el agente.

---

**Entregables**

| Item | Ubicación |
|------|-----------|
| Repositorio | (tu URL de Git o Repl aquí) |
| `.cursorrules` | Raíz del proyecto |
| Vibe Report | Este archivo (`VIBE_REPORT.md`) |
| Captura | Añadir captura de Cursor + Replit cuando estén operando |

**Nota**: Sustituye “(tu URL de Git o Repl aquí)” por el enlace real a tu repo o Repl una vez lo subas, y añade la captura de pantalla al entregar.
