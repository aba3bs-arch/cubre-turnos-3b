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
df_descansos = pd.DataFrame(descansos_data)

# --- 2. CONFIGURACIÓN DEL PERSONAL GENERAL ---
# Leyver y Azul ya no están aquí porque tienen sus propias reglas automáticas
personal_general = {
    "Sofía": ["Día", "Noche"],
    "Esmeralda": ["Día", "Noche"],
    "Luz": ["Domingo Día"],
    "Jenny": ["Día", "Noche"],
    "Nicol": ["Día", "Noche"],
    "Kenia": ["Día", "Noche"]
}

# --- 3. SIMULACIÓN DE NOTIFICACIONES (Simula los pendientes de la semana) ---
if "notificaciones" not in st.session_state:
    st.session_state.notificaciones = {
        "Leyver": {"tienda": "3B2 Pueblo Nuevo", "dia": "Domingo", "turno": "Día", "estado": "pendiente"},
        "Azul": {"tienda": "3B10 El Mezquite", "dia": "Sábado/Domingo", "turno": "Día", "estado": "pendiente"},
        "Sofía": None, "Esmeralda": None, "Jenny": None, "Luz": None, "Nicol": None, "Kenia": None
    }

# --- 4. ACCESO DE EMPLEADOS ---
usuario_actual = st.selectbox("👤 Selecciona tu nombre para ingresar:", 
                             ["Selecciona...", "Leyver", "Azul", "Sofía", "Esmeralda", "Jenny", "Luz", "Nicol", "Kenia"])

if usuario_actual != "Selecciona...":
    st.divider()
    notif = st.session_state.notificaciones.get(usuario_actual)

    if notif and notif["estado"] == "pendiente":
        play_voice_alert()
        st.markdown('### <span class="badge-red"></span> ¡TIENES UN TURNO ASIGNADO!', unsafe_allow_html=True)
        
        with st.container(border=True):
            st.warning(f"Hola **{usuario_actual}**, confirma tu asistencia para tu turno fijo:")
            st.write(f"📍 **Tienda:** {notif['tienda']}")
            st.write(f"📅 **Día:** {notif['dia']}")
            st.write(f"⏰ **Turno:** {notif['turno']}")
            
            col1, col2 = st.columns(2)
            if col1.button("✅ CONFIRMAR ASISTENCIA", use_container_width=True):
                st.session_state.notificaciones[usuario_actual]["estado"] = "confirmado"
                st.success("¡Gracias! Turno confirmado.")
                st.balloons()
                st.rerun()
            if col2.button("❌ RECHAZAR (Aviso a Admin)", use_container_width=True):
                st.session_state.notificaciones[usuario_actual]["estado"] = "rechazado"
                st.error("Has rechazado el turno. Se envió una alerta a administración.")
                st.rerun()
                
    elif notif and notif["estado"] == "confirmado":
        st.success(f"🔒 Tienes tu turno asignado fijo en **{notif['tienda']}**.")
    else:
        st.success("✨ No tienes solicitudes pendientes por responder.")

# --- 5. PANEL DE CONTROL ADMINISTRADOR ---
st.divider()
with st.expander("⚙️ Panel de Control (Solo Andrés)"):
    st.subheader(index=None, body="Estatus de Asignaciones y Confirmaciones")
    st.json(st.session_state.notificaciones)