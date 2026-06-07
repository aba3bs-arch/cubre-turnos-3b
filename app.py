import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN DE ESTILOS (PUNTO ROJO PARPADEANTE) ---
st.markdown("""
    <style>
    .badge-red { 
        height: 18px; width: 18px; background-color: #ff4b4b; 
        border-radius: 50%; display: inline-block; animation: pulse 1.5s infinite; 
    }
    @keyframes pulse { 
        0% { transform: scale(0.9); opacity: 1; } 
        70% { transform: scale(1.2); opacity: 0.7; } 
        100% { transform: scale(0.9); opacity: 1; } 
    }
    </style>
    """, unsafe_allow_html=True)

def play_voice_alert():
    # Sonido de alerta corto al detectar un turno pendiente
    audio_html = """
        <audio autoplay>
            <source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg">
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

st.title("🏪 Portal de Personal - Las 3B")
st.write("Control de asistencia y cadena de notificaciones automatizada.")

# --- 1. BASE DE DATOS DE DESCANSOS (TIENDAS) ---
descansos_data = [
    {"Tienda": "Fusión", "Turno": "Día", "Día Descanso": "Domingo"},
    {"Tienda": "Fusión", "Turno": "Noche", "Día Descanso": "Miércoles"},
    {"Tienda": "3B2 Pueblo Nuevo", "Turno": "Día", "Día Descanso": "Domingo"},
    {"Tienda": "3B2 Pueblo Nuevo", "Turno": "Noche", "Día Descanso": "Jueves"},
    {"Tienda": "3B5 Lomas Dos", "Turno": "Día", "Día Descanso": "Viernes"},
    {"Tienda": "3B5 Lomas Dos", "Turno": "Noche", "Día Descanso": "Martes"},
    {"Tienda": "3B6 Solidaridad", "Turno": "Día", "Día Descanso": "Martes"},
    {"Tienda": "3B6 Solidaridad", "Turno": "Noche", "Día Descanso": "Jueves"},
    {"Tienda": "3B7 Col del Valle", "Turno": "Día", "Día Descanso": "Miércoles"},
    {"Tienda": "3B7 Col del Valle", "Turno": "Noche", "Día Descanso": "Viernes"},
    {"Tienda": "3B10 El Mezquite", "Turno": "Día", "Día Descanso": "Sábado"},
    {"Tienda": "3B10 El Mezquite", "Turno": "Día", "Día Descanso": "Domingo"},
    {"Tienda": "3B10 El Mezquite", "Turno": "Noche", "Día Descanso": "Lunes"},
]
df_descansos = pd
