import streamlit as st

# ==========================================
# 1. CONFIGURACIÓN COMPLETA Y BLINDADA (CORREGIDA)
# ==========================================
st.set_page_config(
    page_title="Control de Turnos - 3B", 
    page_icon="📋", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Corrección del parámetro de HTML para evitar el TypeError
st.markdown("""
    <style>
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        .stSelectbox label { font-size: 1.1rem; font-weight: bold; }
    </style>
""", allow_html=True) # <-- Aquí estaba el detalle, se cambió unsafe_allowed_html por allow_html
