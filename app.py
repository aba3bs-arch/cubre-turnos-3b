import streamlit as st
import pandas as pd
import time
import os

# --- CONFIGURACIÓN DE LA PÁGINA (Icono oficial logo3b.png) ---
logo_path = "logo3b.png"
if os.path.exists(logo_path):
    st.set_page_config(page_title="Las 3B - Roles", page_icon=logo_path, layout="wide", initial_sidebar_state="collapsed")
else:
    st.set_page_config(page_title="Las 3B - Roles", layout="wide", initial_sidebar_state="collapsed")

# --- ESTILOS VISUALES (Punto rojo parpadeante) ---
st.markdown("""
    <style>
    .badge-red { 
        height: 18px; width: 18px; background-color: #ff4b4b; 
        border-radius: 50%; display: inline-block; animation: pulse 1s infinite; 
    }
    @keyframes pulse { 
        0% { transform: scale(0.9); opacity: 1; } 
        70% { transform: scale(1.3); opacity: 0.7; } 
        100% { transform: scale(0.9); opacity: 1; } 
    }
    </style>
    """, unsafe_allow_html=True)

def play_alarm_sound():
    audio_html = """
        <audio autoplay loop>
            <source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg">
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# --- 1. INICIALIZACIÓN DE BASES DE DATOS EN MEMORIA ---
if "descansos_tiendas" not in st.session_state:
    st.session_state.descansos_tiendas = [
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

if "personal" not in st.session_state:
    st.session_state.personal = {
        "Sofía": ["Día", "Noche"],
        "Esmeralda": ["Día", "Noche"],
        "Luz": ["Domingo Día"],
        "Jenny": ["Día", "Noche"],
        "Nicol": ["Día", "Noche"],
        "Kenia": ["Día", "Noche"],
        "Dulce": ["Día", "Noche"],
        "Leyver": ["Fijo 3B2"],
        "Azul": ["Fijo Mezquite"],
        "CT Test": ["Día", "Noche"]
    }

if "notificaciones" not in st.session_state:
    st.session_state.notificaciones = {
        "tienda": "3B10 El Mezquite",
        "dia": "Domingo",
        "turno": "Día",
        "historial_intentos": ["Azul"],
        "ct_actual": "Azul",
        "estado": "pendiente"
    }

if "confirmando_rechazo" not in st.session_state:
    st.session_state.confirmando_rechazo = False

if "usuario_activo" not in st.session_state:
    st.session_state.usuario_activo = None

# --- LOGO SUPERIOR ---
col_logo1, col_logo2, col_logo3 = st.columns([1, 1, 1])
with col_logo2:
    if os.path.exists(logo_path):
        st.image(logo_path, width=150)

st.title("🏪 Sistema Las 3B")
rol_panel = st.sidebar.radio("Navegación:", ["📱 Panel de Usuarios (CT)", "⚙️ Panel Administrativo"])

# ==============================================================================
# 📱 PANEL DE USUARIOS (CUBRE TURNOS)
# ==============================================================================
if rol_panel == "📱 Panel de Usuarios (CT)":
    st.header("Portal de Personal")
    
    if st.session_state.usuario_activo is None:
        st.info("👋 Bienvenido. Selecciona tu nombre para ingresar a tus notificaciones de hoy.")
        lista_empleados = ["Selecciona tu nombre..."] + list(st.session_state.personal.keys())
        seleccion = st.selectbox("👤 ¿Quién eres?", lista_empleados)
        
        if seleccion != "Selecciona tu nombre...":
            if st.button("🔒 Entrar a mi Perfil", use_container_width=True):
                st.session_state.usuario_activo = seleccion
                st.rerun()
                
    else:
        usuario_actual = st.session_state.usuario_activo
        st.caption(f"👤 Perfil activo: **{usuario_actual}**")
        notif = st.session_state.notificaciones

        if notif["estado"] == "pendiente" and notif["ct_actual"] == usuario_actual:
            if not st.session_state.confirmando_rechazo:
                play_alarm_sound()  
                st.markdown('### <span class="badge-red"></span> ¡TIENES UN TURNO ASIGNADO URGENTE!', unsafe_allow_html=True)
                
                with st.container(border=True):
                    st.error("🚨 ATENCIÓN: Confirma de inmediato tu asistencia para apagar la alarma.")
                    st.write(f"📍 **Tienda:** {notif['tienda']}")
                    st.write(f"📅 **Día:** {notif['dia']} | ⏰ **Turno:** {notif['turno']}")
                    
                    col1, col2 = st.columns(2)
                    if col1.button("✅ SÍ ME PRESENTARÉ", use_container_width=True):
                        st.session_state.notificaciones["estado"] = "confirmado"
                        st.success("¡Turno confirmado! Alarma desactivada.")
                        st.balloons()
                        st.rerun()
                    if col2.button("❌ NO PUEDO IR", use_container_width=True):
                        st.session_state.confirmando_rechazo = True
                        st.rerun()
            else:
                st.markdown("### ⚠️ ADVERTENCIA IMPORTANTE DE PENALIZACIÓN")
                with st.container(border=True):
                    st.write(f"⚠️ **{usuario_actual}**, piénsalo bien antes de confirmar:")
                    st.error(
                        "🛑 Al rechazar el turno tu posibilidad de que te dé otro turno queda en 10%, "
                        "así que primero le darán turnos a los otros 9 antes que a ti."
                    )
                    st.write("¿Estás seguro de que deseas proceder con el rechazo y perder tu prioridad?")
                    
                    col_si, col_no = st.columns(2)
                    if col_si.button("💥 SÍ, RECHAZAR Y PERDER PRIORIDAD", use_container_width=True):
                        st.session_state.confirmando_rechazo = False
                        st.session_state.notificaciones["estado"] = "rechazado"
                        st.rerun()
                    if col_no.button("🔙 REGRESAR Y ACEPTAR TURNO", use_container_width=True):
                        st.session_state.confirmando_rechazo = False
                        st.rerun()
                    
        elif notif["estado"] == "confirmado" and notif["ct_actual"] == usuario_actual:
            st.success(f"🔒 Tienes tu turno confirmado en **{notif['tienda']}** para el día **{notif['dia']}**.")
        elif notif["estado"] == "justificado_sistema" and "Azul" == usuario_actual:
            st.info("🤒 Tu ausencia por enfermedad del día de hoy quedó registrada como Justificada. ¡Recupérate pronto!")
        else:
            st.success("✨ Todo al corriente. No tienes solicitudes pendientes por ahora.")
            
        st.divider()
        if st.button("👤 Cerrar Sesión / Ver otros perfiles", key="logout_btn"):
            st.session_state.usuario_activo = None
            st.rerun()

# ==============================================================================
# ⚙️ PANEL ADMINISTRATIVO (ANDRÉS)
# ==============================================================================
else:
    st.header("Panel de Control Administrativo")
    password = st.text_input("🔑 Introduce tu contraseña:", type="password")
    
    if password == "1234":
        st.success("Acceso concedido.")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "➕ Agregar Nuevo CT", 
            "📢 Asignar Turnos", 
            "📊 Monitor de Emergencias",
            "⚙️ Configurar Tiendas"
        ])
        
        with tab1:
            st.subheader("Registrar nuevo personal")
            with st.form("nuevo_ct_form", clear_on_submit=True):
                nuevo_nombre = st.text_input("Nombre del nuevo CT:")
                st.write("Selecciona su disponibilidad:")
                disp_dia = st.checkbox("Turno Día")
                disp_noche = st.checkbox("Turno Noche")
                disp_domingo = st.checkbox("Solo Domingo Día")
                
                if st.form_submit_button("Guardar en el Sistema") and nuevo_nombre:
                    turnos_lista = []
                    if disp_dia: turnos_lista.append("Día")
                    if disp_noche: turnos_lista.append("Noche")
                    if disp_domingo: turnos_lista.append("Domingo Día")
                    
                    if not turnos_lista:
                        st.error("Selecciona al menos una opción de turno.")
                    else:
                        st.session_state.personal[nuevo_nombre] = turnos_lista
                        st.success(f"¡{nuevo_nombre} integrado al equipo temporalmente!")
                        st.rerun()

        with tab2:
            st.subheader("Mandar alerta de cobertura")
            lista_tiendas_disponibles = sorted(list(set([t["Tienda"] for t in st.session_state.descansos_tiendas])))
            tienda_sel = st.selectbox("Tienda a cubrir:", lista_tiendas_disponibles)
            dia_sel = st.selectbox("Día:", ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"])
            turno_sel = st.radio("Turno:", ["Día", "Noche"], horizontal=True)
            
            ct_filtrados =
