"""
EcoTrack - Registro de huella de carbono en lenguaje natural.
Interfaz Streamlit: el usuario escribe su día y recibe un estimado de CO2.
"""

import streamlit as st
from parser import parse_and_calculate

st.set_page_config(
    page_title="EcoTrack | Huella de Carbono",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Estilo simple y claro
st.markdown("""
<style>
    .stApp { max-width: 640px; margin: 0 auto; }
    h1 { color: #0d7a4a; font-weight: 700; }
    .result-box {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 1.25rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid #0d7a4a;
    }
    .metric { font-size: 1.5rem; font-weight: 700; color: #1b5e20; }
    .activity { padding: 0.35rem 0; font-size: 0.95rem; }
</style>
""", unsafe_allow_html=True)

st.title("🌱 EcoTrack")
st.caption("Registra tu día en lenguaje natural y obtén un estimado de tu huella de carbono.")

default_example = "Hoy comí carne y viajé 20 km en bus."
user_input = st.text_area(
    "¿Qué hiciste hoy?",
    value=default_example,
    height=120,
    placeholder="Ej: Desayuné huevos, almorcé pollo y recorrí 15 km en coche.",
    help="Escribe en español: comidas y desplazamientos (con km y medio de transporte).",
)

if st.button("Calcular estimado de CO₂", type="primary"):
    result = parse_and_calculate(user_input)
    total = result["total_kg_co2"]
    activities = result["activities"]

    st.markdown("---")
    st.subheader("Resultado")

    if total > 0:
        st.markdown(f'<div class="result-box"><span class="metric">~{total} kg CO₂e</span><br><span>{result["summary"]}</span></div>', unsafe_allow_html=True)
        if activities:
            st.markdown("**Desglose:**")
            for a in activities:
                if a["type"] == "transport":
                    st.markdown(f'- <span class="activity">🚌 {a["vehicle"]}: {a["km"]} km → **{a["co2_kg"]} kg CO₂**</span>', unsafe_allow_html=True)
                else:
                    st.markdown(f'- <span class="activity">🍽️ {a["food"]}: {a["servings"]} porción(es) → **{a["co2_kg"]} kg CO₂**</span>', unsafe_allow_html=True)
    else:
        st.info(result["summary"])
        st.markdown("Prueba con algo como: *\"Hoy comí carne y viajé 20 km en bus\"*.")

st.markdown("---")
st.caption("EcoTrack MVP · Los factores de emisión son aproximados. Pensado para conciencia, no para contabilidad exacta.")
